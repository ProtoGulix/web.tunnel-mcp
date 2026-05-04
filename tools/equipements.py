from mcp.server.fastmcp import FastMCP
from client import tunnel_client


def register(app: FastMCP):
    @app.tool()
    async def get_equipements(
        limit: int = 100,
        search: str = None,
    ) -> dict:
        """Liste les équipements avec leur état de santé."""
        params = {"limit": limit}
        if search:
            params["search"] = search
        return await tunnel_client.get("/equipements", params=params)

    @app.tool()
    async def get_equipement_detail(equipement_id: str) -> dict:
        """Détail d'un équipement — stats d'interventions."""
        return await tunnel_client.get(f"/equipements/{equipement_id}")
