import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

_TOKEN = os.environ.get("TUNNEL_API_TOKEN", "")
_BASE_URL = os.environ.get("TUNNEL_API_BASE_URL", "http://localhost:8000")
_TRANSPORT = os.environ.get("MCP_TRANSPORT", "stdio")
_SSE_PORT = int(os.environ.get("MCP_SSE_PORT", "8001"))

if not _TOKEN:
    log.error("TUNNEL_API_TOKEN is not set — cannot start tunnel-mcp")
    sys.exit(1)

app = Server("tunnel-mcp")

from tools import interventions, actions, equipements, kpis  # noqa: E402

interventions.register(app)
actions.register(app)
equipements.register(app)
kpis.register(app)


async def _run_stdio():
    log.info("tunnel-mcp starting — transport=stdio  api=%s", _BASE_URL)
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


async def _run_sse():
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.routing import Route
    import uvicorn

    log.info(
        "tunnel-mcp starting — transport=sse  port=%d  api=%s", _SSE_PORT, _BASE_URL
    )

    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as (read_stream, write_stream):
            await app.run(
                read_stream, write_stream, app.create_initialization_options()
            )

    starlette_app = Starlette(
        routes=[
            Route("/sse", endpoint=handle_sse),
            Route("/messages/", endpoint=sse.handle_post_message, methods=["POST"]),
        ]
    )

    config = uvicorn.Config(
        starlette_app, host="0.0.0.0", port=_SSE_PORT, log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    if _TRANSPORT == "sse":
        asyncio.run(_run_sse())
    else:
        asyncio.run(_run_stdio())
