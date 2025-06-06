import os
import pandas as pd
from datetime import datetime
import redis

def handle(req, context):
    user_id = os.getenv("USER_ID", "US9")
    base_dir = os.path.join(os.getcwd(), "US9")
    input_dir = os.path.join(base_dir, "data")
    output_dir = os.path.join(base_dir, "depot")

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Simuler un fichier input.csv si inexistant
    input_path = os.path.join(input_dir, "input.csv")
    if not os.path.exists(input_path):
        with open(input_path, "w") as f:
            f.write("order_id,product,quantity,customer\n")
            f.write("101,chAise,2,alIce\n")
            f.write("102,buReau,1,bOB\n")
            f.write("103,lamPe,4,carlA\n")

    try:
        files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
        if not files:
            return "Aucun fichier CSV trouvé dans US9/data/"

        input_path = os.path.join(input_dir, files[0])
        df = pd.read_csv(input_path)

        df["customer"] = df["customer"].str.upper()
        df["product"] = df["product"].str.lower()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df["Processed-Date"] = now
        df["process_by"] = user_id

        output_path = os.path.join(output_dir, "output.csv")
        df.to_csv(output_path, index=False)

        # Mise à jour Redis
        r = redis.StrictRedis(host="redis-master.openfaas-fn.svc.cluster.local", port=6379, password="bmTorS4kbv")
        r.incr("transformed_files")

        return "Fichier transformé et enregistré dans US9/depot/output.csv"
    except Exception as e:
        return f"Erreur : {str(e)}"
