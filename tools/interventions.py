from mcp.server.fastmcp import FastMCP
from client import tunnel_client


def register(app: FastMCP):
    @app.tool()
    async def get_interventions(
        status: str = None,
        priority: str = None,
        equipement_id: str = None,
        limit: int = 50,
        include_stats: bool = False,
    ) -> dict:
        """Liste les interventions Tunnel avec filtres optionnels."""
        params = {"limit": min(limit, 200)}
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        if equipement_id:
            params["equipement_id"] = equipement_id
        if include_stats:
            params["include"] = "stats"
        return await tunnel_client.get("/interventions", params=params)

    @app.tool()
    async def get_intervention_detail(intervention_id: str) -> dict:
        """Détail complet d'une intervention — actions, status_logs, stats."""
        return await tunnel_client.get(f"/interventions/{intervention_id}")
