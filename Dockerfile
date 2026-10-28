# ==============================================================================
# Multi-Stage Secure Dockerfile for architect-cad-mcp
# ==============================================================================
# Stage 1: Build stage (compile wheels and install dependencies into venv)
# Stage 2: Minimal, hardened runtime container (non-root UID 10001)
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Builder Stage
# ------------------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build prerequisites for C-extensions if wheel fallbacks are needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create isolated virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade core packaging tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install project dependencies first for layer caching
COPY pyproject.toml README.md ./
COPY architect_cad_mcp ./architect_cad_mcp

# Install the application into /opt/venv
RUN pip install --no-cache-dir .

# ------------------------------------------------------------------------------
# 2. Runtime Stage
# ------------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

# Metadata labels (OCI specification)
LABEL org.opencontainers.image.title="architect-cad-mcp" \
      org.opencontainers.image.description="Dedicated 2D Architectural AutoCAD MCP Server with AIA layers, multi-plane orthographic generator, and Neufert DRC" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.authors="Antigravity Pair Programmer"

# Environment configuration:
# - Headless Matplotlib Agg backend (zero display server required)
# - Unbuffered IO for instant Docker log streaming
# - No .pyc byte-code generation in container
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MPLBACKEND=Agg \
    PATH="/opt/venv/bin:$PATH" \
    CAD_OUTPUT_DIR="/app/cad_output"

# Create a secure, non-privileged system user and group (least-privilege security)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -d /app -s /usr/sbin/nologin appuser

WORKDIR /app

# Copy isolated virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application source and AutoLISP reference scripts
COPY --chown=10001:10001 architect_cad_mcp ./architect_cad_mcp
COPY --chown=10001:10001 lisp-code ./lisp-code
COPY --chown=10001:10001 pyproject.toml README.md ./

# Create default output volume directory with appropriate permissions
RUN mkdir -p /app/cad_output && \
    chown -R 10001:10001 /app

# Expose port for SSE transport mode (default 8000)
EXPOSE 8000

# Health check probe using the built-in diagnostic probe (exit code 0 = healthy)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["architect-cad-health", "--quiet"]

# Drop privileges to non-root user
USER 10001:10001

# Default entrypoint runs the FastMCP server
ENTRYPOINT ["architect-cad-mcp"]

# Default command runs standard input/output transport for MCP clients
CMD ["--transport", "stdio"]
