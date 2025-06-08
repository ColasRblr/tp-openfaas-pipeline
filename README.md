# TP OpenFaaS – Traitement de commandes 

## Objectif

Développer une chaîne de traitement serverless en utilisant **OpenFaaS** sur Kubernetes avec 3 fonctions :
1. **daily-fetcher** : fonction planifiée (CRON)
2. **file-transformer** : fonction déclenchée par message NATS
3. **status-checker** : fonction HTTP pour vérifier l'état

## Technologies utilisées

- Python 3 (python3-http)
- OpenFaaS, faas-cli
- Redis (pour les compteurs et les blocages de double-exécution)
- NATS (broker de messages)
- Kubernetes (via Minikube)

## Fonctions

### 1. `daily-fetcher` (planification CRON)

- Déclenchée tous les jours
- Ne s'exécute qu'une fois par jour grâce à une vérification de date dans Redis
- Envoie un message JSON avec la date sur `orders.import` (topic NATS)

### 2. `file-transformer` (déclenchée par NATS)

- Abonnée au topic NATS 'orders.import'
- Lit un fichier CSV local `/input.csv` 
- Applique la transformation :
  - `customers` → MAJUSCULES
  - `product` → minuscules
  - Ajoute `Processed-Date` et `process_by`
- Sauvegarde le fichier modifié `output.csv`dans son répertoire

### 3. `status-checker` (appel HTTP)

- Retourne le **nombre de fichiers dans `/US9/depot`** grâce au compteur Redis incrémenté dans file-transformer

## Déploiement

```bash
faas-cli up -f daily-fetcher.yml
faas-cli up -f file-transformer.yml
faas-cli up -f status-checker.yml
