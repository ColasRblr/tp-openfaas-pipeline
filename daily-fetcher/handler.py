import json
from datetime import datetime

def handle(req, context):
    today = datetime.now().strftime("%Y-%m-%d")
    message = {"date": today}
    return json.dumps(message)
