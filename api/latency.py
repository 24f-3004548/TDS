import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load telemetry data
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

    weight = position - lower

    return (
        values[lower]
        + (values[upper] - values[lower]) * weight
    )


@app.post("/")
def latency_metrics(request: RequestBody):

    result = {}

    for region in request.regions:

        records = [
            row
            for row in DATA
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

        avg_latency = sum(latencies) / len(latencies)

        p95_latency = percentile(
            latencies,
            0.95
        )

        avg_uptime = sum(uptimes) / len(uptimes)

        breaches = sum(
            1
            for latency in latencies
            if latency > request.threshold_ms
        )

        result[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches
        }

    return JSONResponse(
        content=result,
        headers={
            "Access-Control-Allow-Origin": "*"
        }
    )