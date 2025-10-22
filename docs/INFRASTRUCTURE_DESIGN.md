# 인프라 설계 문서

> A2A 기반 분산 시스템 프로덕션 인프라 설계

**버전**: 3.0.0
**작성일**: 2025-10-22
**플랫폼**: AWS (Primary), GCP/Azure (Alternative)

---

## 📋 목차

1. [인프라 개요](#인프라-개요)
2. [네트워크 아키텍처](#네트워크-아키텍처)
3. [컴퓨팅 리소스](#컴퓨팅-리소스)
4. [데이터베이스](#데이터베이스)
5. [스토리지](#스토리지)
6. [보안](#보안)
7. [모니터링 및 로깅](#모니터링-및-로깅)
8. [Terraform 구성](#terraform-구성)

---

## 인프라 개요

### 전체 구성도

```
┌─────────────────────────────────────────────────────────────┐
│                        AWS Cloud                             │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              VPC (10.0.0.0/16)                         │ │
│  │                                                        │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │      Public Subnet (10.0.1.0/24)                 │ │ │
│  │  │                                                  │ │ │
│  │  │  ┌─────────┐  ┌─────────┐                       │ │ │
│  │  │  │   ALB   │  │   NAT   │                       │ │ │
│  │  │  │ Gateway │  │ Gateway │                       │ │ │
│  │  │  └────┬────┘  └────┬────┘                       │ │ │
│  │  └───────┼───────────┼────────────────────────────┘ │ │
│  │          │           │                               │ │
│  │  ┌───────┼───────────┼────────────────────────────┐ │ │
│  │  │      Private Subnet 1 (10.0.10.0/24)          │ │ │
│  │  │      Application Tier (ECS Fargate)           │ │ │
│  │  │                                                │ │ │
│  │  │  ┌─────────────┐  ┌──────────────┐            │ │ │
│  │  │  │ Coordinator │  │ Research x10 │            │ │ │
│  │  │  │   (1 task)  │  │   (10 tasks) │            │ │ │
│  │  │  └─────────────┘  └──────────────┘            │ │ │
│  │  │                                                │ │ │
│  │  │  ┌──────────────┐  ┌──────────────┐           │ │ │
│  │  │  │Extraction x5 │  │Reflection x2 │           │ │ │
│  │  │  │   (5 tasks)  │  │   (2 tasks)  │           │ │ │
│  │  │  └──────────────┘  └──────────────┘           │ │ │
│  │  └────────────────────────────────────────────────┘ │ │
│  │                                                      │ │
│  │  ┌────────────────────────────────────────────────┐ │ │
│  │  │      Private Subnet 2 (10.0.20.0/24)          │ │ │
│  │  │      Data Tier                                │ │ │
│  │  │                                                │ │ │
│  │  │  ┌──────────────┐  ┌──────────────┐           │ │ │
│  │  │  │ RDS Postgres │  │ ElastiCache  │           │ │ │
│  │  │  │   Primary    │  │    Redis     │           │ │ │
│  │  │  └──────────────┘  └──────────────┘           │ │ │
│  │  │                                                │ │ │
│  │  │  ┌──────────────┐                             │ │ │
│  │  │  │ RDS Postgres │                             │ │ │
│  │  │  │   Replica    │                             │ │ │
│  │  │  └──────────────┘                             │ │ │
│  │  └────────────────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Supporting Services                               │   │
│  │  - S3 (Raw data storage)                          │   │
│  │  - Secrets Manager (API keys)                     │   │
│  │  - CloudWatch (Monitoring)                        │   │
│  │  - ECR (Container registry)                       │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 리소스 요약

| 카테고리 | 리소스 | 수량 | 비고 |
|---------|--------|------|------|
| **네트워킹** | VPC | 1 | 10.0.0.0/16 |
| | Public Subnet | 2 | AZ-a, AZ-b |
| | Private Subnet (App) | 2 | AZ-a, AZ-b |
| | Private Subnet (Data) | 2 | AZ-a, AZ-b |
| | NAT Gateway | 2 | HA 구성 |
| | Application Load Balancer | 1 | Internet-facing |
| **컴퓨팅** | ECS Fargate Tasks | 18 | 10+5+2+1 |
| | vCPU 총량 | 106 | - |
| | Memory 총량 | 204 GB | - |
| **데이터베이스** | RDS PostgreSQL | 1+1 | Primary + Replica |
| | ElastiCache Redis | 1 | Cluster mode |
| **스토리지** | S3 Buckets | 3 | Raw data, Logs, Artifacts |
| **보안** | Security Groups | 4 | ALB, App, Data, Redis |
| | IAM Roles | 5 | Tasks, EC2, RDS, S3, CloudWatch |
| **모니터링** | CloudWatch Alarms | 15+ | CPU, Memory, API errors |
| | Prometheus | 1 | Custom metrics |
| | Grafana | 1 | Dashboards |

---

## 네트워크 아키텍처

### VPC 설계

```hcl
# terraform/vpc.tf
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "company-research-vpc"
    Environment = var.environment
    Project     = "company-research"
  }
}

# Availability Zones
data "aws_availability_zones" "available" {
  state = "available"
}

# Public Subnets (for ALB, NAT Gateway)
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-${count.index + 1}"
    Tier = "Public"
  }
}

# Private Subnets - Application Tier
resource "aws_subnet" "private_app" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "private-app-subnet-${count.index + 1}"
    Tier = "Application"
  }
}

# Private Subnets - Data Tier
resource "aws_subnet" "private_data" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 20}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "private-data-subnet-${count.index + 1}"
    Tier = "Data"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "company-research-igw"
  }
}

# NAT Gateways (2 for HA)
resource "aws_eip" "nat" {
  count  = 2
  domain = "vpc"

  tags = {
    Name = "nat-eip-${count.index + 1}"
  }
}

resource "aws_nat_gateway" "main" {
  count         = 2
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = {
    Name = "nat-gateway-${count.index + 1}"
  }
}

# Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "public-route-table"
  }
}

resource "aws_route_table" "private_app" {
  count  = 2
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }

  tags = {
    Name = "private-app-route-table-${count.index + 1}"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private_app" {
  count          = 2
  subnet_id      = aws_subnet.private_app[count.index].id
  route_table_id = aws_route_table.private_app[count.index].id
}
```

### Security Groups

```hcl
# terraform/security_groups.tf

# ALB Security Group
resource "aws_security_group" "alb" {
  name        = "company-research-alb-sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTPS from Internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP from Internet (redirect to HTTPS)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "alb-sg"
  }
}

# Application Tier Security Group
resource "aws_security_group" "app" {
  name        = "company-research-app-sg"
  description = "Security group for application tier"
  vpc_id      = aws_vpc.main.id

  # Allow from ALB
  ingress {
    description     = "HTTP from ALB"
    from_port       = 5000
    to_port         = 5003
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  # Allow inter-agent communication
  ingress {
    description = "A2A communication between agents"
    from_port   = 5000
    to_port     = 5003
    protocol    = "tcp"
    self        = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "app-tier-sg"
  }
}

# Database Security Group
resource "aws_security_group" "database" {
  name        = "company-research-db-sg"
  description = "Security group for RDS PostgreSQL"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "PostgreSQL from application tier"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  tags = {
    Name = "database-sg"
  }
}

# Redis Security Group
resource "aws_security_group" "redis" {
  name        = "company-research-redis-sg"
  description = "Security group for ElastiCache Redis"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Redis from application tier"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  tags = {
    Name = "redis-sg"
  }
}
```

---

## 컴퓨팅 리소스

### ECS Fargate 클러스터

```hcl
# terraform/ecs.tf

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "company-research-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name        = "company-research-cluster"
    Environment = var.environment
  }
}

# Task Definition - Research Agent
resource "aws_ecs_task_definition" "research_agent" {
  family                   = "research-agent"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "8192"  # 8 vCPU
  memory                   = "16384" # 16 GB
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name  = "research-agent"
      image = "${aws_ecr_repository.research_agent.repository_url}:latest"

      portMappings = [
        {
          containerPort = 5001
          protocol      = "tcp"
        }
      ]

      environment = [
        {
          name  = "AGENT_TYPE"
          value = "research"
        },
        {
          name  = "PORT"
          value = "5001"
        }
      ]

      secrets = [
        {
          name      = "TAVILY_API_KEY"
          valueFrom = "${aws_secretsmanager_secret.tavily_api_key.arn}"
        },
        {
          name      = "ANTHROPIC_API_KEY"
          valueFrom = "${aws_secretsmanager_secret.anthropic_api_key.arn}"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/research-agent"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }

      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:5001/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])
}

# ECS Service - Research Agent
resource "aws_ecs_service" "research_agent" {
  name            = "research-agent-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.research_agent.arn
  desired_count   = 10
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private_app[*].id
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false
  }

  service_registries {
    registry_arn = aws_service_discovery_service.research_agent.arn
  }

  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }

  tags = {
    Name = "research-agent-service"
  }
}

# Service Discovery (Cloud Map)
resource "aws_service_discovery_private_dns_namespace" "main" {
  name        = "company-research.local"
  description = "Service discovery namespace"
  vpc         = aws_vpc.main.id
}

resource "aws_service_discovery_service" "research_agent" {
  name = "research"

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.main.id

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}

# Similar definitions for Extraction, Reflection, Coordinator...
```

### Auto Scaling

```hcl
# terraform/autoscaling.tf

# Target Tracking - Research Agent
resource "aws_appautoscaling_target" "research_agent" {
  max_capacity       = 20
  min_capacity       = 5
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.research_agent.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "research_agent_cpu" {
  name               = "research-agent-cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.research_agent.resource_id
  scalable_dimension = aws_appautoscaling_target.research_agent.scalable_dimension
  service_namespace  = aws_appautoscaling_target.research_agent.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value       = 70.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}

resource "aws_appautoscaling_policy" "research_agent_memory" {
  name               = "research-agent-memory-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.research_agent.resource_id
  scalable_dimension = aws_appautoscaling_target.research_agent.scalable_dimension
  service_namespace  = aws_appautoscaling_target.research_agent.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }

    target_value       = 80.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}
```

---

## 데이터베이스

### RDS PostgreSQL

```hcl
# terraform/rds.tf

# DB Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "company-research-db-subnet-group"
  subnet_ids = aws_subnet.private_data[*].id

  tags = {
    Name = "company-research-db-subnet-group"
  }
}

# RDS PostgreSQL Primary
resource "aws_db_instance" "postgres_primary" {
  identifier     = "company-research-postgres"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.large"

  allocated_storage     = 100
  max_allocated_storage = 500
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = "companyresearch"
  username = "admin"
  password = random_password.db_password.result

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.database.id]

  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  deletion_protection = true
  skip_final_snapshot = false
  final_snapshot_identifier = "company-research-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"

  performance_insights_enabled    = true
  performance_insights_retention_period = 7

  tags = {
    Name = "company-research-postgres-primary"
  }
}

# RDS PostgreSQL Read Replica
resource "aws_db_instance" "postgres_replica" {
  identifier          = "company-research-postgres-replica"
  replicate_source_db = aws_db_instance.postgres_primary.identifier
  instance_class      = "db.t3.large"

  vpc_security_group_ids = [aws_security_group.database.id]

  backup_retention_period = 0
  skip_final_snapshot     = true

  performance_insights_enabled = true

  tags = {
    Name = "company-research-postgres-replica"
  }
}

# Database Password
resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret" "db_password" {
  name = "company-research/db-password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db_password.result
}
```

### ElastiCache Redis

```hcl
# terraform/elasticache.tf

# ElastiCache Subnet Group
resource "aws_elasticache_subnet_group" "main" {
  name       = "company-research-redis-subnet-group"
  subnet_ids = aws_subnet.private_data[*].id
}

# ElastiCache Redis Cluster
resource "aws_elasticache_replication_group" "redis" {
  replication_group_id       = "company-research-redis"
  replication_group_description = "Redis cluster for caching and task queue"

  engine               = "redis"
  engine_version       = "7.0"
  node_type            = "cache.t3.medium"
  number_cache_clusters = 2
  port                 = 6379

  subnet_group_name          = aws_elasticache_subnet_group.main.name
  security_group_ids         = [aws_security_group.redis.id]
  parameter_group_name       = "default.redis7"

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token_enabled         = true
  auth_token                 = random_password.redis_password.result

  automatic_failover_enabled = true
  multi_az_enabled           = true

  snapshot_retention_limit = 5
  snapshot_window          = "03:00-05:00"

  tags = {
    Name = "company-research-redis"
  }
}

resource "random_password" "redis_password" {
  length  = 32
  special = false
}

resource "aws_secretsmanager_secret" "redis_password" {
  name = "company-research/redis-password"
}

resource "aws_secretsmanager_secret_version" "redis_password" {
  secret_id     = aws_secretsmanager_secret.redis_password.id
  secret_string = random_password.redis_password.result
}
```

---

## 스토리지

### S3 Buckets

```hcl
# terraform/s3.tf

# Raw Data Bucket
resource "aws_s3_bucket" "raw_data" {
  bucket = "company-research-raw-data-${var.environment}"

  tags = {
    Name        = "Raw Data Storage"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "raw_data" {
  bucket = aws_s3_bucket.raw_data.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "raw_data" {
  bucket = aws_s3_bucket.raw_data.id

  rule {
    id     = "transition-to-glacier"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "raw_data" {
  bucket = aws_s3_bucket.raw_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Logs Bucket
resource "aws_s3_bucket" "logs" {
  bucket = "company-research-logs-${var.environment}"

  tags = {
    Name        = "Application Logs"
    Environment = var.environment
  }
}

# Block public access for all buckets
resource "aws_s3_bucket_public_access_block" "raw_data" {
  bucket = aws_s3_bucket.raw_data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

---

## 보안

### IAM Roles

```hcl
# terraform/iam.tf

# ECS Task Execution Role
resource "aws_iam_role" "ecs_execution_role" {
  name = "company-research-ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution_role_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Additional policy for Secrets Manager
resource "aws_iam_role_policy" "ecs_execution_secrets" {
  name = "ecs-execution-secrets-policy"
  role = aws_iam_role.ecs_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = [
          aws_secretsmanager_secret.tavily_api_key.arn,
          aws_secretsmanager_secret.anthropic_api_key.arn,
          aws_secretsmanager_secret.db_password.arn,
          aws_secretsmanager_secret.redis_password.arn
        ]
      }
    ]
  })
}

# ECS Task Role
resource "aws_iam_role" "ecs_task_role" {
  name = "company-research-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "ecs_task_s3" {
  name = "ecs-task-s3-policy"
  role = aws_iam_role.ecs_task_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          "${aws_s3_bucket.raw_data.arn}/*",
          aws_s3_bucket.raw_data.arn
        ]
      }
    ]
  })
}
```

### Secrets Manager

```hcl
# terraform/secrets.tf

resource "aws_secretsmanager_secret" "tavily_api_key" {
  name = "company-research/tavily-api-key"

  tags = {
    Name = "Tavily API Key"
  }
}

resource "aws_secretsmanager_secret" "anthropic_api_key" {
  name = "company-research/anthropic-api-key"

  tags = {
    Name = "Anthropic API Key"
  }
}

# Note: Secret values must be manually set via AWS Console or CLI
# aws secretsmanager put-secret-value --secret-id company-research/tavily-api-key --secret-string "your-key"
```

---

## 모니터링 및 로깅

### CloudWatch

```hcl
# terraform/cloudwatch.tf

# Log Groups
resource "aws_cloudwatch_log_group" "research_agent" {
  name              = "/ecs/research-agent"
  retention_in_days = 30

  tags = {
    Name = "Research Agent Logs"
  }
}

# Alarms - Research Agent CPU
resource "aws_cloudwatch_metric_alarm" "research_agent_cpu_high" {
  alarm_name          = "research-agent-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"

  dimensions = {
    ClusterName = aws_ecs_cluster.main.name
    ServiceName = aws_ecs_service.research_agent.name
  }

  alarm_actions = [aws_sns_topic.alerts.arn]

  tags = {
    Name = "Research Agent High CPU"
  }
}

# SNS Topic for Alerts
resource "aws_sns_topic" "alerts" {
  name = "company-research-alerts"
}

resource "aws_sns_topic_subscription" "alerts_email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}
```

---

## 비용 추정

### 월간 비용 (us-east-1 기준)

| 리소스 | 사양 | 수량 | 시간당 비용 | 월간 비용 |
|--------|------|------|------------|----------|
| **ECS Fargate** | | | | |
| Research (8vCPU, 16GB) | - | 10 | $0.49 | $3,528 |
| Extraction (4vCPU, 8GB) | - | 5 | $0.24 | $864 |
| Reflection (2vCPU, 4GB) | - | 2 | $0.12 | $172 |
| Coordinator (2vCPU, 4GB) | - | 1 | $0.12 | $86 |
| **RDS PostgreSQL** | db.t3.large | 1+1 | $0.145 | $208 |
| **ElastiCache Redis** | cache.t3.medium | 2 | $0.068 | $98 |
| **NAT Gateway** | - | 2 | $0.045 | $64 |
| **ALB** | - | 1 | - | $22 |
| **S3** | Standard | - | - | $50 |
| **Data Transfer** | - | - | - | $100 |
| **CloudWatch** | Logs + Metrics | - | - | $30 |
| **총 인프라 비용** | | | | **$5,222** |

---

## 다음 단계

1. DATA_FLOW_DESIGN.md - 데이터 플로우 및 캐싱 전략
2. API_SPECIFICATION.md - OpenAPI 명세
3. DEPLOYMENT_STRATEGY.md - CI/CD 파이프라인

---

**작성**: 2025-10-22
**버전**: 3.0.0
**상태**: Ready for Terraform deployment
