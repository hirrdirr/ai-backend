import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
kommuner = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def load_kommuner():
    print("🔄 Laddar tätorter från JSON...")
    file_path = os.path.join(os.path.dirname(__file__), "alla_tatorter_scb_2023.json")
    with open(file_path, encoding="utf-8") as f:
        kommuner.extend(json.load(f))
    print(f"✅ Laddade {len(kommuner)} tätorter från SCB-data")

@app.get("/match_ort")
async def match_ort(q: str):
    q_lower = q.lower()
    matches = [k for k in kommuner if q_lower in k.lower()]
    return {"matches": matches[:10]}
