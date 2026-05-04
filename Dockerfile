FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e ".[sse]"

COPY . .

ENV MCP_TRANSPORT=sse
ENV MCP_SSE_PORT=8001

EXPOSE ${MCP_SSE_PORT}

CMD ["python", "server.py"]
