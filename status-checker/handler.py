import redis

def handle(req, context):
    try:
        r = redis.StrictRedis(
            host="redis-master.openfaas-fn.svc.cluster.local",
            port=6379,
            password="bmTorS4kbv"
        )
        transformed_files = r.get("transformed_files")
        return f"Nombre de fichiers transformés : {int(transformed_files) if transformed_files else 0}"
    except Exception as e:
        return f"Erreur : {str(e)}"