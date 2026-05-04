import logging
import os
import sys

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

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

app = FastMCP("tunnel-mcp", port=_SSE_PORT, host="0.0.0.0")

from tools import interventions, actions, equipements, kpis  # noqa: E402

interventions.register(app)
actions.register(app)
equipements.register(app)
kpis.register(app)

if __name__ == "__main__":
    log.info(
        "tunnel-mcp starting — transport=%s  port=%d  api=%s",
        _TRANSPORT, _SSE_PORT, _BASE_URL,
    )
    app.run(transport=_TRANSPORT)
