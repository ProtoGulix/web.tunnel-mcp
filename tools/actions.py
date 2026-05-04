from mcp.server.fastmcp import FastMCP
from client import tunnel_client


def register(app: FastMCP):
    @app.tool()
    async def get_actions(
        intervention_id: str = None,
        limit: int = 100,
    ) -> dict:
        """Liste les actions d'intervention avec filtres."""
        params = {"limit": min(limit, 500)}
        if intervention_id:
            params["intervention_id"] = intervention_id
        return await tunnel_client.get("/intervention-actions", params=params)

    @app.tool()
    async def get_data_quality(
        severite: str = None,
        entite: str = None,
    ) -> dict:
        """Retourne les anomalies de qualité de données détectées (actions sans temps, interventions fermées sans action, etc.)."""
        params = {}
        if severite:
            params["severite"] = severite
        if entite:
            params["entite"] = entite
        return await tunnel_client.get("/stats/anomalies", params=params)
