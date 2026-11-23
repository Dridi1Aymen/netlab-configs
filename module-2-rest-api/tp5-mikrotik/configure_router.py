import os
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

SCHEME = os.getenv("DEVICE_SCHEME", "http")
HOST = os.getenv("DEVICE_HOST")
BASE_URL = f"{SCHEME}://{HOST}/rest"
AUTH = (os.getenv("DEVICE_USER"), os.getenv("DEVICE_PASSWORD"))

# Liste des routes statiques désirées (état cible)
DESIRED_ROUTES = [
    {"dst-address": "10.10.10.0/24", "gateway": "10.0.2.2", "comment": "Route_Reseau_A"},
    {"dst-address": "10.20.20.0/24", "gateway": "10.0.2.2", "comment": "Route_Reseau_B"},
    {"dst-address": "172.16.50.0/24", "gateway": "10.0.2.2", "comment": "Route_Reseau_C"},
]


def get_existing_routes() -> list[dict]:
    """Récupère toutes les routes actuelles via GET /ip/route."""
    resp = requests.get(f"{BASE_URL}/ip/route", auth=AUTH, verify=False, timeout=5)
    resp.raise_for_status()
    return resp.json()


def ensure_static_routes(routes: list[dict]):
    """Crée uniquement les routes manquantes (pattern vérifier avant de créer)."""
    existing = get_existing_routes()
    # Ensemble des couples (dst-address, gateway) déjà présents sur le routeur
    existing_pairs = {
        (r.get("dst-address"), r.get("gateway")) for r in existing
    }

    for route in routes:
        pair = (route["dst-address"], route["gateway"])
        if pair in existing_pairs:
            print(f"[OK - EXISTE DÉJÀ] Route {route['dst-address']} via {route['gateway']} ignorée.")
        else:
            resp = requests.put(
                f"{BASE_URL}/ip/route",
                json=route,
                auth=AUTH,
                verify=False,
                timeout=5,
            )
            resp.raise_for_status()
            print(f"[CRÉÉE] Route {route['dst-address']} via {route['gateway']} ajoutée (ID: {resp.json().get('.id')}).")


if __name__ == "__main__":
    print("=== SYNCHRONISATION DES ROUTES STATIQUES (IDEMPOTENTE) ===")
    ensure_static_routes(DESIRED_ROUTES)
