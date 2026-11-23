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


def run_crud_demo():
    # --- ÉTAPE 2 : LECTURE (GET) ---
    print("=== 1. LECTURE INITIALE (GET /ip/address) ===")
    resp = requests.get(f"{BASE_URL}/ip/address", auth=AUTH, verify=False, timeout=5)
    resp.raise_for_status()
    for item in resp.json():
        print(f"ID: {item.get('.id')} | IP: {item.get('address')} | Interface: {item.get('interface')}")

    # --- ÉTAPE 3 : CRÉATION (POST) ---
    print("\n=== 2. CRÉATION D'UNE ADRESSE IP (POST /ip/address) ===")
    target_ip = "192.168.20.1/24"
    payload = {"address": target_ip, "interface": "ether2"}
    resp = requests.post(f"{BASE_URL}/ip/address", json=payload, auth=AUTH, verify=False, timeout=5)
    resp.raise_for_status()
    print("Réponse création :", resp.json())

    # --- ÉTAPE 4.1 : RÉCUPÉRATION DU .id VIA GET FILTRÉ ---
    print("\n=== 3. RECHERCHE DE L'ID VIA GET FILTRÉ ===")
    resp = requests.get(
        f"{BASE_URL}/ip/address",
        params={"address": target_ip},
        auth=AUTH,
        verify=False,
        timeout=5,
    )
    resp.raise_for_status()
    results = resp.json()
    if not results:
        print("Adresse introuvable.")
        return

    ip_id = results[0][".id"]
    print(f"ID récupéré pour {target_ip} : {ip_id}")

    # --- ÉTAPE 4.2 : MODIFICATION DU COMMENTAIRE (PATCH) ---
    print(f"\n=== 4. MODIFICATION DU COMMENTAIRE (PATCH /ip/address/{ip_id}) ===")
    patch_payload = {"comment": "LAN_Client_Automatise_Python"}
    resp = requests.patch(
        f"{BASE_URL}/ip/address/{ip_id}",
        json=patch_payload,
        auth=AUTH,
        verify=False,
        timeout=5,
    )
    resp.raise_for_status()
    print("Réponse mise à jour :", resp.json())

    # --- ÉTAPE 4.3 : SUPPRESSION (DELETE) ---
    # Décommentez les 4 lignes ci-dessous après avoir pris votre capture d'écran sur le routeur
    # print(f"\n=== 5. SUPPRESSION (DELETE /ip/address/{ip_id}) ===")
    # del_resp = requests.delete(f"{BASE_URL}/ip/address/{ip_id}", auth=AUTH, verify=False, timeout=5)
    # del_resp.raise_for_status()
    # print(f"Adresse {ip_id} supprimée avec succès.")


if __name__ == "__main__":
    run_crud_demo()
