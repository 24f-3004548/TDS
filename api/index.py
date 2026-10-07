import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).parent.parent / "q-vercel-latency.json"

with open(DATA_PATH, "r") as f:
    DATA = json.load(f)


class RequestBody(BaseModel):
    regions: list[str]
    threshold_ms: float


def percentile(values, p):
    values = sorted(values)

    if not values:
        return 0

    position = (len(values) - 1) * p
    lower = int(position)
    upper = min(lower + 1, len(values) - 1)

    if lower == upper:
        return values[lower]

    return values[lower] + (
        values[upper] - values[lower]
    ) * (position - lower)


@app.post("/api/latency")
def latency_metrics(request: RequestBody):

    result = {}

    for region in request.regions:

        records = [
            row for row in DATA
            if row["region"] == region
        ]

        if not records:
            continue

        latencies = [row["latency_ms"] for row in records]
        uptimes = [row["uptime_pct"] for row in records]

        result[region] = {
            "avg_latency": sum(latencies) / len(latencies),
            "p95_latency": percentile(latencies, 0.95),
            "avg_uptime": sum(uptimes) / len(uptimes),
            "breaches": sum(
                latency > request.threshold_ms
                for latency in latencies
            )
        }

    return result