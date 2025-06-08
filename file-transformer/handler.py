import pandas as pd
from datetime import datetime
import redis

def handle(req, context):
    try:
        df = pd.read_csv("./function/input.csv")
        df["customer"] = df["customer"].str.upper()
        df["product"] = df["product"].str.lower()
        df["Processed-Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.to_csv("./function/output.csv", index=False)
        
        # Incrémentation du compteur Redis
        r = redis.StrictRedis(
            host="redis-master.openfaas-fn.svc.cluster.local",
            port=6379,
            password="bmTorS4kbv"
        )
        counter = r.incr("transformed_files")
        
        return f"Fichier transformé. Compteur : {counter}"
    
    except Exception as e:
        return f"Erreur : {str(e)}"
