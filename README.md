# TP OpenFaaS – Traitement de commandes pour DataRetailX (US9)

## Objectif

Développer une chaîne de traitement serverless en utilisant **OpenFaaS** sur Kubernetes avec 3 fonctions :
1. **daily-fetcher** : fonction planifiée (CRON)
2. **file-transformer** : fonction déclenchée par message NATS
3. **status-checker** : fonction HTTP pour vérifier l'état

## Technologies utilisées

- Python 3 (`python3-http`)
- OpenFaaS + faas-cli
- SFTP
- NATS
- Kubernetes (Minikube)

## Fonctions

### 1. `daily-fetcher` (planification CRON)

- Déclenchée tous les jours (planifié chaque minute pour le test)
- Envoie un message JSON avec la date sur `orders.import` (topic NATS)

### 2. `file-transformer` (déclenchée par NATS)

- Récupère `/US9/data/input.csv` via SFTP
- Applique la transformation :
  - `customers` → MAJUSCULES
  - `product` → minuscules
  - Ajoute `Processed-Date` et `process_by`
- Envoie `/US9/depot/output.csv`

### 3. `status-checker` (appel HTTP)

- Retourne le **nombre de fichiers dans `/US9/depot`** via SFTP

## Déploiement

```bash
faas-cli up -f daily-fetcher.yml
faas-cli up -f file-transformer.yml
faas-cli up -f status-checker.yml
