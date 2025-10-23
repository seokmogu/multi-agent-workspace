# Multi-Agent Workspace - Python 3.11
FROM python:3.11-slim

# 작업 디렉토리
WORKDIR /workspace

# 시스템 의존성
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 환경 변수
ENV PYTHONPATH=/workspace
ENV PYTHONUNBUFFERED=1

# 기본 명령어 (Bash 셸)
CMD ["/bin/bash"]
