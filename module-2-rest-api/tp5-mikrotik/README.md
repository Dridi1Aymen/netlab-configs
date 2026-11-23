# TP 5 : MikroTik CHR (v7) – Introduction à l'API RESTful

## Prérequis
- Python 3.10+
- Dépendances : pip install requests python-dotenv
- Une VM MikroTik RouterOS v7 accessible via HTTP/HTTPS avec un utilisateur ayant les droits API (group=full).

## Installation & Configuration
1. Copier le fichier d'exemple : cp .env.example .env
2. Renseigner DEVICE_SCHEME, DEVICE_HOST, DEVICE_USER et DEVICE_PASSWORD dans .env.

## Exécution des scripts
- Opérations CRUD sur /ip/address : python tp5_crud_ip.py
- Routage statique idempotent : python configure_router.py
