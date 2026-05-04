from mcp.server.fastmcp import FastMCP
from client import tunnel_client


def register(app: FastMCP):
    @app.tool()
    async def get_dashboard_summary() -> dict:
        """Compteurs globaux du tableau de bord — interventions ouvertes, urgentes, stock critique, etc."""
        return await tunnel_client.get("/dashboard/summary")

    @app.tool()
    async def get_stats_anomalies_summary() -> dict:
        """Résumé agrégé des anomalies par sévérité et par entité."""
        data = await tunnel_client.get("/stats/anomalies")
        return {
            "total": data.get("total"),
            "par_severite": data.get("par_severite"),
        }
