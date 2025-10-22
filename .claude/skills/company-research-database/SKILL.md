---
name: Company Research Database
description: Design and implement a database system for storing, caching, and managing company research results from LangGraph multi-agent workflows. Use this when you need to persist research data, avoid duplicate searches, track research history, implement caching strategies, or analyze research quality metrics. Optimized for private SME (small-to-mid-sized enterprise) research data with JSON schema support.
allowed-tools: Write, Edit, Read, Bash
---

# Company Research Database

This skill implements a database system tailored for the LangGraph-based company research agent. It handles storage of research sessions, search results, extracted data, and quality metrics.

## 🎯 Database Purpose

**Store and reuse research on private small-to-mid-sized companies:**

- **Avoid duplicate searches**: Check if company was already researched
- **Cache search results**: Reduce Tavily API costs
- **Track data evolution**: Monitor company changes over time
- **Quality analytics**: Analyze research completeness metrics
- **Schema versioning**: Support multiple extraction schemas

## When to Use This Skill

- Adding persistence to the company research agent
- Implementing search result caching
- Building company profile databases
- Creating research history tracking
- Analyzing research quality over time
- Supporting multiple extraction schemas

## Database Architecture

### Database Selection

**Recommended: PostgreSQL**

Reasons:
- ✅ **JSONB support**: Perfect for flexible extracted data
- ✅ **Full-text search**: Search company descriptions
- ✅ **Mature**: Production-ready with excellent tooling
- ✅ **GIN indexes**: Fast JSON queries

Alternative: SQLite (for development/small scale)

### Schema Design

```
┌─────────────────────────────────────────────────────┐
│  companies                                          │
│  - id (PK)                                          │
│  - company_name (unique)                            │
│  - industry                                         │
│  - company_size_category (small/mid)                │
│  - is_private (always true for our use case)       │
│  - first_researched_at                              │
│  - last_researched_at                               │
│  - research_count                                   │
└─────────────────┬───────────────────────────────────┘
                  │
                  ├─────────────────────────────────────┐
                  ↓                                     ↓
      ┌───────────────────────┐           ┌───────────────────────┐
      │  research_sessions    │           │  extracted_data       │
      │  - id (PK)            │           │  - id (PK)            │
      │  - company_id (FK)    │           │  - company_id (FK)    │
      │  - started_at         │           │  - session_id (FK)    │
      │  - completed_at       │           │  - schema_name        │
      │  - status             │           │  - data (JSONB)       │
      │  - config_snapshot    │           │  - completeness_score │
      │  - reflection_count   │           │  - created_at         │
      └───────────┬───────────┘           └───────────────────────┘
                  │
                  ├─────────────────────────────────────┐
                  ↓                                     ↓
      ┌───────────────────────┐           ┌───────────────────────┐
      │  search_queries       │           │  search_results       │
      │  - id (PK)            │           │  - id (PK)            │
      │  - session_id (FK)    │           │  - query_id (FK)      │
      │  - query_text         │           │  - url                │
      │  - query_type         │           │  - title              │
      │  - executed_at        │           │  - content (TEXT)     │
      └───────────────────────┘           │  - score              │
                                          │  - cached_at          │
                                          └───────────────────────┘
                  │
                  ↓
      ┌───────────────────────┐
      │  reflection_logs      │
      │  - id (PK)            │
      │  - session_id (FK)    │
      │  - iteration          │
      │  - missing_fields     │
      │  - is_complete        │
      │  - notes (TEXT)       │
      │  - created_at         │
      └───────────────────────┘
```

## Implementation Guide

### 1. Project Structure

Add database components to existing project:

```
company-search-agent/
├── src/
│   ├── agent/              # Existing agent code
│   └── database/           # NEW: Database layer
│       ├── __init__.py
│       ├── models.py       # SQLAlchemy models
│       ├── schemas.py      # Pydantic schemas
│       ├── crud.py         # CRUD operations
│       ├── connection.py   # Database connection
│       └── cache.py        # Search result caching
│
├── alembic/                # NEW: Database migrations
│   ├── versions/
│   └── env.py
│
├── scripts/                # NEW: Database scripts
│   ├── init_db.py         # Initialize database
│   └── migrate_data.py    # Data migration
│
├── alembic.ini            # Alembic config
└── .env                   # Add DATABASE_URL
```

### 2. Dependencies

Add to `requirements.txt`:

```
# Database
sqlalchemy>=2.0.0
alembic>=1.12.0
psycopg2-binary>=2.9.0  # PostgreSQL adapter
asyncpg>=0.29.0         # Async PostgreSQL

# For SQLite (development)
# aiosqlite>=0.19.0

# Validation
pydantic>=2.0.0
```

### 3. Database Models

Create `src/database/models.py`:

```python
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey,
    JSON, Text, Float, Index, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Company(Base):
    """Private SME company master record."""
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), unique=True, nullable=False, index=True)

    # Company characteristics (for private SMEs)
    industry = Column(String(100), index=True)
    company_size_category = Column(
        String(20),  # 'small' (10-300) or 'mid' (300-1000)
        index=True
    )
    is_private = Column(Boolean, default=True, nullable=False)  # Always true

    # Research tracking
    first_researched_at = Column(DateTime, default=func.now())
    last_researched_at = Column(DateTime, default=func.now(), onupdate=func.now())
    research_count = Column(Integer, default=0)

    # Relationships
    research_sessions = relationship("ResearchSession", back_populates="company")
    extracted_data = relationship("ExtractedData", back_populates="company")

    __table_args__ = (
        Index('ix_company_industry_size', 'industry', 'company_size_category'),
    )


class ResearchSession(Base):
    """Individual research session (one run of the agent)."""
    __tablename__ = "research_sessions"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Session metadata
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)
    status = Column(
        String(20),  # 'running', 'completed', 'failed'
        default='running',
        index=True
    )

    # Configuration snapshot (JSONB for flexibility)
    config_snapshot = Column(JSONB, nullable=False)  # Store Configuration object

    # Workflow metrics
    reflection_count = Column(Integer, default=0)
    total_search_queries = Column(Integer, default=0)
    total_search_results = Column(Integer, default=0)

    # Relationships
    company = relationship("Company", back_populates="research_sessions")
    search_queries = relationship("SearchQuery", back_populates="session")
    extracted_data = relationship("ExtractedData", back_populates="session")
    reflection_logs = relationship("ReflectionLog", back_populates="session")

    __table_args__ = (
        Index('ix_session_company_status', 'company_id', 'status'),
        Index('ix_session_completed', 'completed_at'),
    )


class SearchQuery(Base):
    """Generated search queries (before executing Tavily)."""
    __tablename__ = "search_queries"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("research_sessions.id"), nullable=False)

    query_text = Column(Text, nullable=False)
    query_type = Column(
        String(50),  # 'initial', 'follow_up', 'reflection'
        index=True
    )
    executed_at = Column(DateTime, default=func.now())

    # Relationships
    session = relationship("ResearchSession", back_populates="search_queries")
    search_results = relationship("SearchResult", back_populates="query")

    __table_args__ = (
        Index('ix_query_session_type', 'session_id', 'query_type'),
    )


class SearchResult(Base):
    """Cached Tavily search results (avoid duplicate API calls)."""
    __tablename__ = "search_results"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("search_queries.id"), nullable=False)

    # Search result data
    url = Column(String(2048), nullable=False)
    title = Column(String(500))
    content = Column(Text)  # Main text content
    raw_content = Column(Text, nullable=True)  # Full HTML if available
    score = Column(Float, nullable=True)  # Relevance score from Tavily

    # Metadata
    cached_at = Column(DateTime, default=func.now())

    # Relationships
    query = relationship("SearchQuery", back_populates="search_results")

    __table_args__ = (
        Index('ix_result_url', 'url'),
        Index('ix_result_cached', 'cached_at'),
    )


class ExtractedData(Base):
    """Structured data extracted from research (JSONB storage)."""
    __tablename__ = "extracted_data"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("research_sessions.id"), nullable=False)

    # Schema information
    schema_name = Column(String(100), nullable=False)  # 'default', 'startup', etc.
    schema_version = Column(String(20), default='1.0')

    # Extracted data (flexible JSONB)
    data = Column(JSONB, nullable=False)

    # Quality metrics
    completeness_score = Column(Float, nullable=True)  # 0.0 to 1.0
    field_count_filled = Column(Integer)
    field_count_total = Column(Integer)

    # Metadata
    created_at = Column(DateTime, default=func.now())

    # Relationships
    company = relationship("Company", back_populates="extracted_data")
    session = relationship("ResearchSession", back_populates="extracted_data")

    __table_args__ = (
        Index('ix_extracted_company_schema', 'company_id', 'schema_name'),
        Index('ix_extracted_completeness', 'completeness_score'),
    )


class ReflectionLog(Base):
    """Reflection phase logs (quality evaluation)."""
    __tablename__ = "reflection_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("research_sessions.id"), nullable=False)

    # Reflection iteration info
    iteration = Column(Integer, nullable=False)  # 1, 2, 3...

    # Quality assessment
    missing_fields = Column(JSONB)  # List of missing field names
    is_complete = Column(Boolean, default=False)
    completeness_score = Column(Float, nullable=True)

    # Follow-up actions
    follow_up_queries = Column(JSONB, nullable=True)  # List of generated queries

    # LLM evaluation notes
    notes = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=func.now())

    # Relationships
    session = relationship("ResearchSession", back_populates="reflection_logs")

    __table_args__ = (
        Index('ix_reflection_session_iter', 'session_id', 'iteration'),
        UniqueConstraint('session_id', 'iteration', name='uq_session_iteration'),
    )
```

### 4. CRUD Operations

Create `src/database/crud.py`:

```python
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import select, and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from .models import (
    Company, ResearchSession, SearchQuery, SearchResult,
    ExtractedData, ReflectionLog
)


class CompanyCRUD:
    """CRUD operations for companies."""

    @staticmethod
    async def get_or_create(
        db: AsyncSession,
        company_name: str,
        **kwargs
    ) -> Company:
        """Get existing company or create new one."""
        stmt = select(Company).where(Company.company_name == company_name)
        result = await db.execute(stmt)
        company = result.scalar_one_or_none()

        if not company:
            company = Company(company_name=company_name, **kwargs)
            db.add(company)
            await db.flush()

        return company

    @staticmethod
    async def get_last_research(
        db: AsyncSession,
        company_name: str,
        schema_name: str = "default"
    ) -> Optional[ExtractedData]:
        """Get most recent research result for a company."""
        stmt = (
            select(ExtractedData)
            .join(Company)
            .where(
                and_(
                    Company.company_name == company_name,
                    ExtractedData.schema_name == schema_name
                )
            )
            .order_by(desc(ExtractedData.created_at))
            .limit(1)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def should_refresh_research(
        db: AsyncSession,
        company_name: str,
        max_age_days: int = 30
    ) -> bool:
        """Check if research should be refreshed based on age."""
        last_research = await CompanyCRUD.get_last_research(db, company_name)

        if not last_research:
            return True  # Never researched

        age = datetime.utcnow() - last_research.created_at
        return age > timedelta(days=max_age_days)


class ResearchSessionCRUD:
    """CRUD operations for research sessions."""

    @staticmethod
    async def create_session(
        db: AsyncSession,
        company_id: int,
        config: Dict[str, Any]
    ) -> ResearchSession:
        """Create new research session."""
        session = ResearchSession(
            company_id=company_id,
            config_snapshot=config,
            status='running'
        )
        db.add(session)
        await db.flush()
        return session

    @staticmethod
    async def complete_session(
        db: AsyncSession,
        session_id: int,
        status: str = 'completed'
    ):
        """Mark session as completed."""
        stmt = select(ResearchSession).where(ResearchSession.id == session_id)
        result = await db.execute(stmt)
        session = result.scalar_one()

        session.completed_at = datetime.utcnow()
        session.status = status
        await db.flush()

    @staticmethod
    async def get_session_stats(
        db: AsyncSession,
        session_id: int
    ) -> Dict[str, Any]:
        """Get comprehensive session statistics."""
        # Query counts
        query_count_stmt = select(func.count(SearchQuery.id)).where(
            SearchQuery.session_id == session_id
        )
        result_count_stmt = (
            select(func.count(SearchResult.id))
            .join(SearchQuery)
            .where(SearchQuery.session_id == session_id)
        )
        reflection_count_stmt = select(func.count(ReflectionLog.id)).where(
            ReflectionLog.session_id == session_id
        )

        query_count = (await db.execute(query_count_stmt)).scalar()
        result_count = (await db.execute(result_count_stmt)).scalar()
        reflection_count = (await db.execute(reflection_count_stmt)).scalar()

        return {
            "total_queries": query_count,
            "total_results": result_count,
            "total_reflections": reflection_count
        }


class SearchResultCache:
    """Cache for search results to avoid duplicate Tavily API calls."""

    @staticmethod
    async def get_cached_results(
        db: AsyncSession,
        query_text: str,
        max_age_hours: int = 24
    ) -> Optional[List[SearchResult]]:
        """Get cached search results for a query."""
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)

        stmt = (
            select(SearchResult)
            .join(SearchQuery)
            .where(
                and_(
                    SearchQuery.query_text == query_text,
                    SearchResult.cached_at >= cutoff_time
                )
            )
        )
        result = await db.execute(stmt)
        results = result.scalars().all()

        return list(results) if results else None

    @staticmethod
    async def cache_results(
        db: AsyncSession,
        query_id: int,
        results: List[Dict[str, Any]]
    ):
        """Cache Tavily search results."""
        for result_data in results:
            search_result = SearchResult(
                query_id=query_id,
                url=result_data.get("url"),
                title=result_data.get("title"),
                content=result_data.get("content"),
                raw_content=result_data.get("raw_content"),
                score=result_data.get("score")
            )
            db.add(search_result)

        await db.flush()


class ExtractedDataCRUD:
    """CRUD operations for extracted data."""

    @staticmethod
    async def save_extraction(
        db: AsyncSession,
        company_id: int,
        session_id: int,
        schema_name: str,
        data: Dict[str, Any],
        completeness_score: Optional[float] = None
    ) -> ExtractedData:
        """Save extracted company data."""
        # Calculate field counts
        total_fields = len(data)
        filled_fields = sum(1 for v in data.values() if v is not None and v != "")

        extracted = ExtractedData(
            company_id=company_id,
            session_id=session_id,
            schema_name=schema_name,
            data=data,
            completeness_score=completeness_score or (filled_fields / total_fields),
            field_count_filled=filled_fields,
            field_count_total=total_fields
        )
        db.add(extracted)
        await db.flush()
        return extracted

    @staticmethod
    async def get_company_history(
        db: AsyncSession,
        company_id: int,
        schema_name: str = "default"
    ) -> List[ExtractedData]:
        """Get all historical extractions for a company."""
        stmt = (
            select(ExtractedData)
            .where(
                and_(
                    ExtractedData.company_id == company_id,
                    ExtractedData.schema_name == schema_name
                )
            )
            .order_by(desc(ExtractedData.created_at))
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())


class AnalyticsCRUD:
    """Analytics and reporting queries."""

    @staticmethod
    async def get_research_quality_stats(
        db: AsyncSession,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get aggregate research quality statistics."""
        cutoff = datetime.utcnow() - timedelta(days=days)

        # Average completeness score
        avg_stmt = (
            select(func.avg(ExtractedData.completeness_score))
            .where(ExtractedData.created_at >= cutoff)
        )
        avg_completeness = (await db.execute(avg_stmt)).scalar()

        # Total companies researched
        count_stmt = (
            select(func.count(func.distinct(ExtractedData.company_id)))
            .where(ExtractedData.created_at >= cutoff)
        )
        total_companies = (await db.execute(count_stmt)).scalar()

        # Average reflection iterations
        avg_reflection_stmt = (
            select(func.avg(ResearchSession.reflection_count))
            .where(
                and_(
                    ResearchSession.completed_at >= cutoff,
                    ResearchSession.status == 'completed'
                )
            )
        )
        avg_reflections = (await db.execute(avg_reflection_stmt)).scalar()

        return {
            "period_days": days,
            "total_companies_researched": total_companies or 0,
            "avg_completeness_score": round(avg_completeness or 0, 3),
            "avg_reflection_iterations": round(avg_reflections or 0, 2)
        }

    @staticmethod
    async def get_most_researched_industries(
        db: AsyncSession,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get industries with most research activity."""
        stmt = (
            select(
                Company.industry,
                func.count(Company.id).label('company_count'),
                func.sum(Company.research_count).label('total_researches')
            )
            .where(Company.industry.isnot(None))
            .group_by(Company.industry)
            .order_by(desc('total_researches'))
            .limit(limit)
        )
        result = await db.execute(stmt)

        return [
            {
                "industry": row.industry,
                "company_count": row.company_count,
                "total_researches": row.total_researches
            }
            for row in result
        ]
```

### 5. Database Connection

Create `src/database/connection.py`:

```python
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from .models import Base


# Get database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost/company_research"
)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set True for SQL logging
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database (create all tables)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    """Drop all tables (use with caution!)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

### 6. Integration with Research Agent

Modify `src/agent/graph.py` to integrate database:

```python
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.crud import (
    CompanyCRUD, ResearchSessionCRUD, SearchResultCache,
    ExtractedDataCRUD
)
from ..database.models import SearchQuery


async def research_node_with_db(
    state: ResearchState,
    config: Configuration,
    db: AsyncSession
) -> Dict[str, Any]:
    """
    Research node with database integration.
    """
    company_name = state["company_name"]

    # Get or create company
    company = await CompanyCRUD.get_or_create(
        db,
        company_name=company_name,
        is_private=True
    )

    # Check if we should use cached data
    if not await CompanyCRUD.should_refresh_research(db, company_name):
        cached_data = await CompanyCRUD.get_last_research(db, company_name)
        if cached_data:
            print(f"Using cached research for {company_name}")
            return {
                "extracted_data": cached_data.data,
                "is_complete": True,
                "from_cache": True
            }

    # Create new research session
    session = await ResearchSessionCRUD.create_session(
        db,
        company_id=company.id,
        config=config.model_dump()
    )

    # Generate queries (existing code)
    queries = await generate_queries(state, config)

    # Execute searches with caching
    all_results = []
    for query_text in queries:
        # Check cache first
        cached_results = await SearchResultCache.get_cached_results(
            db,
            query_text,
            max_age_hours=24
        )

        if cached_results:
            print(f"Cache hit for query: {query_text}")
            all_results.extend([
                {
                    "url": r.url,
                    "title": r.title,
                    "content": r.content,
                    "score": r.score
                }
                for r in cached_results
            ])
        else:
            # Execute Tavily search
            print(f"Cache miss, executing: {query_text}")
            search_results = await execute_tavily_search(query_text, config)

            # Save query
            query_record = SearchQuery(
                session_id=session.id,
                query_text=query_text,
                query_type='initial'
            )
            db.add(query_record)
            await db.flush()

            # Cache results
            await SearchResultCache.cache_results(
                db,
                query_id=query_record.id,
                results=search_results
            )

            all_results.extend(search_results)

    # Generate research notes (existing code)
    notes = await generate_notes(company_name, all_results, config)

    # Update session stats
    session.total_search_queries = len(queries)
    session.total_search_results = len(all_results)

    return {
        "research_queries": queries,
        "search_results": all_results,
        "research_notes": notes,
        "_session_id": session.id,
        "_company_id": company.id
    }
```

### 7. Database Initialization Script

Create `scripts/init_db.py`:

```python
import asyncio
import os
from dotenv import load_dotenv
from src.database.connection import init_db, engine


async def main():
    """Initialize the database schema."""
    load_dotenv()

    print("Initializing database...")
    print(f"Database URL: {os.getenv('DATABASE_URL')}")

    await init_db()

    print("✅ Database initialized successfully!")
    print("\nCreated tables:")
    print("  - companies")
    print("  - research_sessions")
    print("  - search_queries")
    print("  - search_results")
    print("  - extracted_data")
    print("  - reflection_logs")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
```

### 8. Environment Variables

Add to `.env`:

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/company_research

# For SQLite (development)
# DATABASE_URL=sqlite+aiosqlite:///./company_research.db

# Existing API keys
ANTHROPIC_API_KEY=your_key
TAVILY_API_KEY=your_key
```

### 9. Alembic Migrations (Optional but Recommended)

Initialize Alembic for migrations:

```bash
# Initialize Alembic
alembic init alembic

# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

Edit `alembic/env.py`:

```python
from src.database.models import Base
target_metadata = Base.metadata
```

### 10. Usage Example with Database

```python
import asyncio
from src.agent.graph import build_research_graph
from src.agent.configuration import Configuration
from src.agent.state import DEFAULT_SCHEMA
from src.database.connection import get_db
from src.database.crud import CompanyCRUD, ExtractedDataCRUD


async def research_with_db(company_name: str):
    """Run research with database integration."""

    config = Configuration(
        max_search_queries=3,
        max_reflection_steps=1
    )

    async for db in get_db():
        # Check if already researched
        if not await CompanyCRUD.should_refresh_research(db, company_name, max_age_days=30):
            print(f"Using cached data for {company_name}")
            cached = await CompanyCRUD.get_last_research(db, company_name)
            print(cached.data)
            return

        # Run research
        graph = build_research_graph(config)
        result = await graph.ainvoke({
            "company_name": company_name,
            "extraction_schema": DEFAULT_SCHEMA,
            # ... other state fields
        })

        # Save results
        company = await CompanyCRUD.get_or_create(db, company_name)
        await ExtractedDataCRUD.save_extraction(
            db,
            company_id=company.id,
            session_id=result["_session_id"],
            schema_name="default",
            data=result["extracted_data"],
            completeness_score=result.get("completeness_score")
        )

        print(f"Research saved for {company_name}")


if __name__ == "__main__":
    asyncio.run(research_with_db("Example Private SME Corp"))
```

## Best Practices

### 1. Caching Strategy

- **Cache search results for 24 hours** (avoid duplicate Tavily calls)
- **Cache extracted data for 30 days** (companies change slowly)
- **Invalidate cache manually** for high-priority updates

### 2. Indexing

Key indexes for performance:

```python
# Fast company lookup
Index('ix_company_name', Company.company_name)

# Research session queries
Index('ix_session_company_status', ResearchSession.company_id, ResearchSession.status)

# JSONB queries (PostgreSQL)
Index('ix_extracted_data_gin', ExtractedData.data, postgresql_using='gin')
```

### 3. Data Retention

```python
async def cleanup_old_data(db: AsyncSession, days: int = 90):
    """Delete old research data beyond retention period."""
    cutoff = datetime.utcnow() - timedelta(days=days)

    # Delete old search results
    await db.execute(
        delete(SearchResult).where(SearchResult.cached_at < cutoff)
    )

    # Keep extracted data but delete intermediate results
    await db.commit()
```

### 4. Error Handling

```python
from sqlalchemy.exc import IntegrityError

try:
    company = await CompanyCRUD.get_or_create(db, company_name)
except IntegrityError:
    await db.rollback()
    # Handle duplicate company name
```

### 5. Monitoring

Track key metrics:

- Average completeness score over time
- Cache hit rate
- Most researched industries
- Failed research sessions

## Troubleshooting

**Connection Issues:**
```bash
# Check PostgreSQL is running
pg_isready

# Test connection
psql -U username -d company_research
```

**Migration Errors:**
```bash
# Reset database (CAUTION: deletes data)
alembic downgrade base
alembic upgrade head
```

**JSONB Queries Not Working:**
```python
# Ensure PostgreSQL, not SQLite
assert "postgresql" in DATABASE_URL

# Use JSONB operators
stmt = select(ExtractedData).where(
    ExtractedData.data['industry'].astext == 'SaaS'
)
```

## Advanced Features

### Full-Text Search on Company Data

```python
from sqlalchemy import func

# Add tsvector column
company_fts = func.to_tsvector('english', Company.company_name)

# Search query
stmt = select(Company).where(
    company_fts.op('@@')(func.plainto_tsquery('english', 'software'))
)
```

### Data Versioning

Track how company data changes over time:

```python
async def get_data_diff(
    db: AsyncSession,
    company_id: int,
    schema_name: str = "default"
):
    """Compare latest extraction with previous one."""
    history = await ExtractedDataCRUD.get_company_history(
        db, company_id, schema_name
    )

    if len(history) < 2:
        return None

    latest = history[0].data
    previous = history[1].data

    # Calculate diff
    diff = {
        "added": {k: v for k, v in latest.items() if k not in previous},
        "changed": {
            k: {"old": previous[k], "new": latest[k]}
            for k in latest
            if k in previous and latest[k] != previous[k]
        },
        "removed": {k: v for k, v in previous.items() if k not in latest}
    }

    return diff
```

## References

- **SQLAlchemy Async**: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- **Alembic**: https://alembic.sqlalchemy.org/
- **PostgreSQL JSONB**: https://www.postgresql.org/docs/current/datatype-json.html
