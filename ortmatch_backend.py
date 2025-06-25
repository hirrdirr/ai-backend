from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()
kommuner = []

# Tillåt CORS för frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def load_kommuner():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://public.opendatasoft.com/api/records/1.0/search/",
            params={"dataset": "georef-sweden-tatort", "rows": 10000},
            headers={"User-Agent": "Mozilla/5.0"}
        )
        data = resp.json()
        for rec in data.get("records", []):
            namn = rec.get("fields", {}).get("ortnamn")
            if namn:
                kommuner.append(namn)

@app.get("/match_ort")
async def match_ort(q: str):
    q_lower = q.lower()
    matches = [k for k in kommuner if q_lower in k.lower()]
    return {"matches": matches[:10]}
