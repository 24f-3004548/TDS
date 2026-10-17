import time, uuid
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

EMAIL = "24f3004548@ds.study.iitm.ac.in"
ALLOWED = "https://dash-enhga8.example.com"

app = FastAPI()

# Added first so the header middleware below wraps it (outermost),
# which puts X-Request-ID / X-Process-Time on preflight responses too.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)

@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.perf_counter()
    rid = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response

@app.get("/stats")
def stats(values: str = Query(...)):
    try:
        nums = [int(v) for v in values.split(",") if v.strip() != ""]
    except ValueError:
        raise HTTPException(status_code=400, detail="values must be comma-separated integers")
    if not nums:
        raise HTTPException(status_code=400, detail="no values provided")
    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums),
    }