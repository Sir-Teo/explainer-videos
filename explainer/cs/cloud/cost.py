"""Cloud cost (Part 45): per-request serverless billing against a server billed by the second, at AWS's published
us-east-1 list prices; spot instances that can be interrupted, with checkpoints; and the Job's bill."""

from __future__ import annotations

import math
import random

PRICES = {
    "date": "AWS us-east-1 list prices, as published in 2024",
    "m5.large per hour": 0.096,            # 2 vCPU, 8 GiB, on demand, Linux
    "lambda per GB-second": 0.0000166667,  # x86
    "lambda per million requests": 0.20,
    "s3 standard per GB-month": 0.023,
    "egress per GB": 0.09,
}
SPOT_DISCOUNT = 0.65    # illustrative: spot prices vary by hour and zone; a typical discount


def serverless_vs_server(ms=100, mb=512, per_server_rps=200):
    """Cost per month at a steady rate of requests: Lambda at ms per request and mb of memory, against enough
    m5.large servers (each handling per_server_rps) running all month."""
    per_req = ms / 1000 * mb / 1024 * PRICES["lambda per GB-second"] + PRICES["lambda per million requests"] / 1e6
    server_hour = PRICES["m5.large per hour"]
    secs = 30 * 24 * 3600
    rows = []
    for rps in (0.1, 1, 5, 10, 25, 50, 100, 500, 1000):
        lam = per_req * rps * secs
        srv = math.ceil(rps / per_server_rps) * server_hour * 30 * 24
        rows.append({"rps": rps, "lambda": lam, "servers": srv})
    breakeven = server_hour / 3600 / per_req
    return {"per_request": per_req, "breakeven_rps": breakeven, "rows": rows, "ms": ms, "mb": mb}


def spot(job_hours=10.0, interrupt_per_hour=0.1, checkpoint_every=(None, 2.0, 1.0, 0.5, 0.25),
         checkpoint_cost_h=0.02, restart_h=0.05, trials=4000, seed=0):
    """A batch job on spot capacity: interruptions arrive as a Poisson process; work since the last checkpoint is
    lost.  Expected wall-clock hours and cost (at the discounted price) against on demand."""
    rng = random.Random(seed)
    od = PRICES["m5.large per hour"]
    sp = od * (1 - SPOT_DISCOUNT)
    rows = []
    for tau in checkpoint_every:
        tot = 0.0
        for _ in range(trials):
            done, t = 0.0, 0.0
            while done < job_hours - 1e-9:
                seg = min(tau or job_hours, job_hours - done)
                need = seg + (checkpoint_cost_h if tau else 0.0)
                x = rng.expovariate(interrupt_per_hour)
                if x >= need:
                    t += need
                    done += seg
                else:
                    t += x + restart_h
            tot += t
        hours = tot / trials
        rows.append({"checkpoint_every": tau, "hours": hours, "cost": hours * sp})
    young = math.sqrt(2 * checkpoint_cost_h / interrupt_per_hour)
    return {"job_hours": job_hours, "on_demand_cost": job_hours * od, "spot_price": sp, "rows": rows,
            "young_interval": young, "interrupt_per_hour": interrupt_per_hour}


def job_bill(seconds_one_core: float, chunks: int = 16, mb: int = 1024):
    """The Job priced three ways from its measured single-core time: on one on-demand m5.large (billed per
    second, one minute minimum), on a spot m5.large, and as `chunks` parallel Lambda invocations."""
    od = PRICES["m5.large per hour"] / 3600
    ec2 = max(60.0, seconds_one_core / 2) * od          # two vCPUs share the work
    spot_ = ec2 * (1 - SPOT_DISCOUNT)
    lam = seconds_one_core * mb / 1024 * PRICES["lambda per GB-second"] + chunks * PRICES[
        "lambda per million requests"] / 1e6
    return {"seconds": seconds_one_core, "ec2": ec2, "spot": spot_, "lambda": lam,
            "lambda_wall_seconds": seconds_one_core / chunks}
