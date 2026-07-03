from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/kpi")
def get_kpi():
    with open("kpi.json", "r", encoding="utf-8") as f:
        return json.load(f)