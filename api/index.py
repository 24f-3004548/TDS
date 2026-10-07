# api/index.py
import os
import json
import statistics
from typing import Any, Dict, List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Enable CORS for any origin, allowing POST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PASTE YOUR q-vercel-latency.json CONTENT HERE AS A PYTHON LIST OF DICTS
TELEMETRY_DATA: List[Dict[str, Any]] = [
  {
    "region": "apac",
    "service": "checkout",
    "latency_ms": 160.27,
    "uptime_pct": 98.215,
    "timestamp": 20250301
  },
  {
    "region": "apac",
    "service": "payments",
    "latency_ms": 158.15,
    "uptime_pct": 98.041,
    "timestamp": 20250302
  },
  {
    "region": "apac",
    "service": "payments",
    "latency_ms": 201.71,
    "uptime_pct": 98.324,
    "timestamp": 20250303
  },
  {
    "region": "apac",
    "service": "catalog",
    "latency_ms": 200.19,
    "uptime_pct": 99.025,
    "timestamp": 20250304
  },
  {
    "region": "apac",
    "service": "catalog",
    "latency_ms": 116,
    "uptime_pct": 97.914,
    "timestamp": 20250305
  },
  {
    "region": "apac",
    "service": "checkout",
    "latency_ms": 216.1,
    "uptime_pct": 98.081,
    "timestamp": 20250306
  },
  {
    "region": "apac",
    "service": "support",
    "latency_ms": 113.35,
    "uptime_pct": 97.998,
    "timestamp": 20250307
  },
  {
    "region": "apac",
    "service": "support",
    "latency_ms": 220.28,
    "uptime_pct": 97.299,
    "timestamp": 20250308
  },
  {
    "region": "apac",
    "service": "recommendations",
    "latency_ms": 206.96,
    "uptime_pct": 99.365,
    "timestamp": 20250309
  },
  {
    "region": "apac",
    "service": "support",
    "latency_ms": 185.4,
    "uptime_pct": 97.285,
    "timestamp": 20250310
  },
  {
    "region": "apac",
    "service": "catalog",
    "latency_ms": 204.44,
    "uptime_pct": 98.802,
    "timestamp": 20250311
  },
  {
    "region": "apac",
    "service": "support",
    "latency_ms": 204,
    "uptime_pct": 97.139,
    "timestamp": 20250312
  },
  {
    "region": "emea",
    "service": "recommendations",
    "latency_ms": 190.14,
    "uptime_pct": 98.931,
    "timestamp": 20250301
  },
  {
    "region": "emea",
    "service": "payments",
    "latency_ms": 213.73,
    "uptime_pct": 97.166,
    "timestamp": 20250302
  },
  {
    "region": "emea",
    "service": "recommendations",
    "latency_ms": 179.17,
    "uptime_pct": 98.61,
    "timestamp": 20250303
  },
  {
    "region": "emea",
    "service": "analytics",
    "latency_ms": 166.3,
    "uptime_pct": 97.692,
    "timestamp": 20250304
  },
  {
    "region": "emea",
    "service": "recommendations",
    "latency_ms": 110.39,
    "uptime_pct": 98.641,
    "timestamp": 20250305
  },
  {
    "region": "emea",
    "service": "recommendations",
    "latency_ms": 211.86,
    "uptime_pct": 98.144,
    "timestamp": 20250306
  },
  {
    "region": "emea",
    "service": "analytics",
    "latency_ms": 213.47,
    "uptime_pct": 98.879,
    "timestamp": 20250307
  },
  {
    "region": "emea",
    "service": "checkout",
    "latency_ms": 172,
    "uptime_pct": 98.498,
    "timestamp": 20250308
  },
  {
    "region": "emea",
    "service": "checkout",
    "latency_ms": 136.38,
    "uptime_pct": 97.578,
    "timestamp": 20250309
  },
  {
    "region": "emea",
    "service": "payments",
    "latency_ms": 218.86,
    "uptime_pct": 97.384,
    "timestamp": 20250310
  },
  {
    "region": "emea",
    "service": "recommendations",
    "latency_ms": 122.14,
    "uptime_pct": 98.239,
    "timestamp": 20250311
  },
  {
    "region": "emea",
    "service": "recommendations",
    "latency_ms": 142.65,
    "uptime_pct": 97.671,
    "timestamp": 20250312
  },
  {
    "region": "amer",
    "service": "checkout",
    "latency_ms": 212.14,
    "uptime_pct": 97.642,
    "timestamp": 20250301
  },
  {
    "region": "amer",
    "service": "recommendations",
    "latency_ms": 127.89,
    "uptime_pct": 98.029,
    "timestamp": 20250302
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 121.91,
    "uptime_pct": 97.69,
    "timestamp": 20250303
  },
  {
    "region": "amer",
    "service": "recommendations",
    "latency_ms": 150.45,
    "uptime_pct": 97.49,
    "timestamp": 20250304
  },
  {
    "region": "amer",
    "service": "catalog",
    "latency_ms": 209.37,
    "uptime_pct": 98.695,
    "timestamp": 20250305
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 115.04,
    "uptime_pct": 99.05,
    "timestamp": 20250306
  },
  {
    "region": "amer",
    "service": "recommendations",
    "latency_ms": 155.31,
    "uptime_pct": 98.244,
    "timestamp": 20250307
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 194.27,
    "uptime_pct": 97.793,
    "timestamp": 20250308
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 170.62,
    "uptime_pct": 98.369,
    "timestamp": 20250309
  },
  {
    "region": "amer",
    "service": "catalog",
    "latency_ms": 140.57,
    "uptime_pct": 98.13,
    "timestamp": 20250310
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 202.23,
    "uptime_pct": 97.574,
    "timestamp": 20250311
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 121.49,
    "uptime_pct": 99.027,
    "timestamp": 20250312
  }
]

def percentile(values: List[float], p: float) -> float:
    """Return the p-th percentile (0–100) of a sorted list of numbers."""
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f = int(k)
    c = f + 1
    if c >= len(sorted_vals):
        return sorted_vals[-1]
    return sorted_vals[f] + (k - f) * (sorted_vals[c] - sorted_vals[f])

async def calculate_metrics(request: Request):
    body = await request.json()

    regions = body["regions"]
    threshold_ms = body["threshold_ms"]

    output = {}

    for region in regions:
        records = [
            record
            for record in TELEMETRY_DATA
            if record["region"] == region
        ]

        latencies = [record["latency_ms"] for record in records]
        uptimes = [record["uptime"] for record in records]

        output[region] = {
            "avg_latency": statistics.mean(latencies),
            "p95_latency": percentile(latencies, 95),
            "avg_uptime": statistics.mean(uptimes),
            "breaches": sum(
                latency > threshold_ms
                for latency in latencies
            ),
        }

    return output


@app.post("/")
async def analytics_root(request: Request):
    return await calculate_metrics(request)


@app.post("/api")
async def analytics_api(request: Request):
    return await calculate_metrics(request)

@app.post("/api/latency")
async def analytics_api(request: Request):
    return await calculate_metrics(request)