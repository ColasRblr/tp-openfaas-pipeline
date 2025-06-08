import json
import asyncio
import nats
from datetime import datetime
import redis

def handle(req, context):
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Connexion Redis
    r = redis.StrictRedis(
        host="redis-master.openfaas-fn.svc.cluster.local",
        port=6379,
        password="bmTorS4kbv"
    )
    
    # Si la date a déjà été enregistrée, on arrête
    if r.get("last_fetch") == today.encode():
        message = f"Déjà exécuté aujourd'hui : {today}"
        print(message)
        return json.dumps({"status": "already_executed", "date": today, "message": message})
    
    message_data = {"date": today}
    
    try:
        # Publication du message sur NATS
        asyncio.run(publish_to_nats(message_data))
        print(f"Message publié sur NATS: {message_data}")
        
        # Enregistrement de la date dans Redis
        r.set("last_fetch", today)
        
        return json.dumps({
            "status": "success", 
            "date": today, 
            "message": "Message publié avec succès"
        })
        
    except Exception as e:
        error_msg = f"Erreur lors de la publication NATS: {e}"
        print(error_msg)
        return json.dumps({
            "status": "error", 
            "date": today, 
            "error": str(e)
        })

async def publish_to_nats(message):
    nc = await nats.connect("nats://nats.openfaas:4222")
    await nc.publish("orders.import", json.dumps(message).encode())
    await nc.close()