
from fastapi import FastAPI, Query
import httpx

app = FastAPI()

kommuner = []

@app.on_event("startup")
async def load_kommuner():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://public.opendatasoft.com/api/records/1.0/search/",
                                params={"dataset":"georef-sweden-kommun","rows":300})
        if resp.status_code == 200:
            kommuner.extend([rec["fields"]["kommunnamn"] for rec in resp.json()["records"]])

@app.get("/match_ort")
def match_ort(q: str = Query(...)):
    matches = [k for k in kommuner if q.lower() in k.lower()]
    return {"matches": matches}
