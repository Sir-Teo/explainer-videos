"""Lab 2: measure the economy three ways, rebuild Leontief's inverse from BEA's 2023 table, and test the series' call."""

import numpy as np

from videos.coursekit import labs
from explainer.industry.register import get
from videos.industry.industry2.compute import results

TITLE = "The economy on one page: value added, jobs and Leontief's table"
GOAL = ("Take BEA's 2023 use table for fifteen sectors and rebuild what the film shows: the direct requirements, the "
        "Leontief inverse as the sum of rounds of buying, each sector's upstreamness, and value added per job; then "
        "test the series' call that health care will employ more people than manufacturing and retail combined by "
        "2030.")
TASKS = [
    "Stop the rounds of buying after one, two and three rounds. How much of the total requirement for a dollar of "
    "manufactured goods (about $2.25) does each truncation capture, and why does the series converge?",
    "Scale every entry of A by 1.1, as if every industry bought 10% more from the others. What happens to "
    "manufacturing's total requirement, and what does that say about multipliers in a more specialised economy?",
    "Follow a dollar of exports instead of a household's dollar (use the exports column of bea_io_2023.csv). Which "
    "industries earn most of it, and how much of it is imported content?",
    "Using fred_jobs.csv, project health care (CES6562000001) and manufacturing plus retail (MANEMP + USTRADE) to 2030 "
    "with the average change of the last three years instead of the last one. Does it change the call?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()
    io = R["io"]
    A, L, names = np.array(io["A"]), np.array(io["L"]), io["names"]
    n = len(names)
    m = names.index("Manufacturing")

    # 1. Three measures of size: sales, value added, jobs
    c = R["companies"]
    mck, aapl = c["mck"], (get("rev.apple.fy2025"), get("gp.apple.fy2025"))
    lab.row("McKesson / Apple: sales ($bn)", f"{mck['rev']:.0f} / {aapl[0]:.0f}")
    lab.row("McKesson / Apple: gross profit ($bn)", f"{mck['gp']:.1f} / {aapl[1]:.0f} "
            f"(Apple x{aapl[1] / mck['gp']:.0f})")
    assert abs(mck["rev"] / aapl[0] - 1) < 0.05 and aapl[1] / mck["gp"] > 10

    # 2. The table: direct requirements and the Leontief inverse as the sum of rounds
    rho = max(abs(np.linalg.eigvals(A)))
    assert rho < 1  # every industry adds some value, so the rounds shrink
    e = np.zeros(n)
    e[m] = 1.0
    x, total, rounds = e.copy(), np.zeros(n), []
    for k in range(40):
        total += x
        rounds.append(total.sum())
        x = A @ x
    assert np.allclose(total, L[:, m], atol=1e-6)
    lab.row("manufacturing: inputs per dollar of output (round 1)", f"${A[:, m].sum():.2f}")
    lab.row("manufacturing: total requirement (all rounds)", f"${L[:, m].sum():.2f} (spectral radius of A {rho:.2f})")
    lab.row("rounds 0-3 of that total", ", ".join(f"${r:.2f}" for r in rounds[:4]))
    lab.row("sales of all industries / value added, 2023 ($tn)", f"{io['output_total']:.1f} / {io['va_total']:.1f}")
    assert io["output_total"] > 1.6 * io["va_total"]

    # 3. Upstreamness: farms and mines far from final users, retail and health care next to them
    U = dict(zip(names, io["upstream"]))
    assert min(U.values()) >= 1 - 1e-9 and U["Farms"] > U["Manufacturing"] > U["Retail"]
    top = sorted(U.items(), key=lambda kv: -kv[1])
    lab.row("most upstream / most downstream", f"{top[0][0]} {top[0][1]:.2f} / {top[-1][0]} {top[-1][1]:.2f}")

    # 4. Value added per job
    jobs = sorted(R["jobs"], key=lambda d: -d["per_job"])
    lab.row("value added per job: highest / lowest", f"{jobs[0]['sector']} ${jobs[0]['per_job'] / 1e3:.0f}k / "
            f"{jobs[-1]['sector']} ${jobs[-1]['per_job'] / 1e3:.0f}k")
    va_share = np.array([d["va"] for d in R["jobs"]]) / (1e3 * R["gdp"])
    job_share = np.array([d["jobs"] for d in R["jobs"]]) / R["jobs_total"]

    # 5. A household's dollar followed back: value added by industry plus imports make the dollar
    H = R["household"]
    P = H["pce"]
    assert abs(sum(P["va"]) + P["imports"] + P["other"] - 1) < 1e-9
    bus = H["names"].index("Business services")
    lab.row("household dollar: business services bought / earned", f"{100 * P['bought'][bus]:.0f}¢ / "
            f"{100 * P['va'][bus]:.0f}¢")
    lab.row("abroad per dollar: household / investment / government",
            " / ".join(f"{100 * (H[k]['imports'] + H[k]['other']):.0f}¢" for k in ("pce", "investment", "government")))
    assert H["investment"]["imports"] > H["pce"]["imports"] > H["government"]["imports"]

    # 6. The series' call: health care against manufacturing plus retail in 2030
    from explainer.industry.data.fetch import read
    J = {int(r["year"]): r for r in read("fred_jobs")}
    hc = {y: J[y]["CES6562000001"] / 1e3 for y in J if J[y]["CES6562000001"]}
    mr = {y: (J[y]["MANEMP"] + J[y]["USTRADE"]) / 1e3 for y in J}
    slope1 = hc[2025] - hc[2024]
    gap = mr[2025] - hc[2025]
    lab.row("2025: health care / manufacturing + retail (m)", f"{hc[2025]:.1f} / {mr[2025]:.1f} (gap {gap:.1f}m)")
    lab.row("years to close at 2025's pace (others flat)", f"{gap / slope1:.1f} (crosses in {2025 + gap / slope1:.0f})")
    assert 2029 < 2025 + gap / slope1 < 2033  # close: hence 40%, not 10% or 90%

    fig, (ax1, ax2) = labs.figure(2)
    ax1.scatter(100 * job_share, 100 * va_share, color=labs.BLUE)
    for d, xs, ys in zip(R["jobs"], job_share, va_share):
        ax1.annotate(d["sector"].split(",")[0].split(" and ")[0], (100 * xs, 100 * ys), fontsize=6,
                     xytext=(3, 2), textcoords="offset points")
    lim = 100 * max(job_share.max(), va_share.max()) * 1.08
    ax1.plot([0, lim], [0, lim], color=labs.GREY, lw=0.8, ls="--")
    ax1.set_xlabel("share of payroll jobs, 2025 (%)")
    ax1.set_ylabel("share of value added, 2025 (%)")
    ax1.set_title("Two maps of one economy: above the line, more value per job")
    ax2.plot(range(12), rounds[:12], marker="o", color=labs.GOLD, label="output after k rounds")
    ax2.axhline(L[:, m].sum(), color=labs.GREEN, ls="--", label="Leontief inverse")
    ax2.set_xlabel("round of buying")
    ax2.set_ylabel("output for $1 of manufactured goods ($)")
    ax2.set_title("The rounds converge to the Leontief inverse")
    ax2.legend(fontsize=8)
    lab.fig = fig
    lab.note = ("The inverse is the sum of every round of buying, which converges because each industry pays part of "
                "every dollar to its own workers and owners rather than to suppliers. Value added per job measures "
                "the equipment, property and prices behind each worker, not effort.")
    return lab
