from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# 🔐 Tillåt bara din egen frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.hirrdirr.se"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

kommuner = []

@app.on_event("startup")
async def load_kommuner():
    print("🔄 Hämtar kommuner...")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://public.opendatasoft.com/api/records/1.0/search/",
                params={"dataset": "georef-sweden-kommun", "rows": 300},
                headers=headers
            )
            resp.raise_for_status()
            data = resp.json()
            print(f"📦 JSON innehåll: {data.keys()}")
            records = data.get("records", [])
            print(f"📄 Antal records: {len(records)}")
            for rec in records:
                fields = rec.get("fields", {})
                namn = fields.get("kom_name")
                if namn:
                    kommuner.append(namn)
        print(f"✅ Laddade {len(kommuner)} kommuner")
    except Exception as e:
        print(f"❌ Fel vid hämtning: {e}")

@app.get("/match_ort")
def match_ort(q: str = Query(...)):
    matches = [k for k in kommuner if q.lower() in k.lower()]
    return {"matches": matches}
