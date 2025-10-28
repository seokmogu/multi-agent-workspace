FROM python:3.10-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for A2A
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    httpx

# Copy source code
COPY . .

# Set Python path
ENV PYTHONPATH=/workspace

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Run the service
CMD ["python", "-m", "uvicorn", "src.agents.a2a.research_agent.app:app", "--host", "0.0.0.0", "--port", "5001"]
