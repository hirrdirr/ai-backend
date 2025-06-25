from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

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
    print("🔄 Hämtar tätorter...")
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://public.opendatasoft.com/api/records/1.0/search/",
            params={"dataset": "georef-sweden-tatorter", "rows": 10000},
            headers={"User-Agent": "Mozilla/5.0"}
        )
        data = resp.json()
        print("🧾 JSON-nycklar:", data.keys())
        recs = data.get("records", [])
        print("📄 Antal records:", len(recs))
        for rec in recs:
            fields = rec.get("fields", {})
            namn = fields.get("ortnamn")
            if namn:
                kommuner.append(namn)
        print("✅ Laddade tätorter:", len(kommuner))

@app.get("/match_ort")
async def match_ort(q: str):
    q_lower = q.lower()
    matches = [k for k in kommuner if q_lower in k.lower()]
    return {"matches": matches[:10]}
