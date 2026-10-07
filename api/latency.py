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


def percentile(values, percentile):
    values = sorted(values)

    if not values:
        return 0

    if len(values) == 1:
        return values[0]

    position = (len(values) - 1) * percentile
    lower = int(position)
    upper = min(lower + 1, len(values) - 1)

    weight = position - lower

    return values[lower] + (values[upper] - values[lower]) * weight


@app.post("/")
def latency_metrics(request: RequestBody):

    response = {}

    for region in request.regions:

        records = [
            row for row in DATA
            if row["region"] == region
        ]

        if not records:
            continue

        latencies = [
            row["latency_ms"]
            for row in records
        ]

        uptimes = [
            row["uptime_pct"]
            for row in records
        ]

        response[region] = {
            "avg_latency": sum(latencies) / len(latencies),
            "p95_latency": percentile(latencies, 0.95),
            "avg_uptime": sum(uptimes) / len(uptimes),
            "breaches": sum(
                1 for latency in latencies
                if latency > request.threshold_ms
            )
        }

    return response
