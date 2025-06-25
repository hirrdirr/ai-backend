from fastapi import FastAPI, Query
import httpx

app = FastAPI()

kommuner = []

@app.on_event("startup")
async def load_kommuner():
    print("🔄 Hämtar kommuner...")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}  # <- VIKTIGT!
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://public.opendatasoft.com/api/records/1.0/search/",
                params={"dataset": "georef-sweden-kommun", "rows": 300},
                headers=headers
            )
            resp.raise_for_status()
            kommuner.extend([rec["fields"]["kommunnamn"] for rec in resp.json()["records"]])
        print(f"✅ Laddade {len(kommuner)} kommuner")
    except Exception as e:
        print(f"❌ Fel vid hämtning: {e}")

@app.get("/match_ort")
def match_ort(q: str = Query(...)):
    matches = [k for k in kommuner if q.lower() in k.lower()]
    return {"matches": matches}
