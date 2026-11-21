"""Lab 48: environment and climate: Hotelling's paths, Simon and Ehrlich's bet over every window, the fishery under
open access and a quota, a small climate model fitted to Mauna Loa and HadCRUT5, a DICE-style model with its optimal
path and the social cost of carbon by discount rate, fat tails, a climate club, Wright's law and withholding in a
merit-order market."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import climate as cl
from explainer.economics.island import truths

TITLE = "Environment and climate"
GOAL = ("Trace a resource's price under Hotelling's rule; rerun the bet; find a fishery's three efforts; fit a carbon "
        "cycle and an energy balance to the record; build a climate-economy model and price a tonne at any discount "
        "rate; see what fat tails do; and find when a club holds and when a power producer gains by holding back.")
TASKS = [
    "Hotelling: let the extraction cost fall 2% a year instead of 4%. Does the price still fall at first, and when is "
    "the mine exhausted?",
    "The model: double the damage coefficient (as Howard and Sterner's damages would) and find the optimal warming in "
    "2100 and the social cost of carbon at 3%.",
    "Fat tails: raise the Student t's degrees of freedom from 2 to 5. How does the loss at a cut-off of 20 degrees "
    "change, and why?",
]


def _annual(d, key="month"):
    out = {}
    for m, v in zip(d[key], d["value"]):
        if np.isfinite(v):
            out.setdefault(int(m[:4]), []).append(v)
    return {y: float(np.mean(v)) for y, v in out.items() if len(v) == 12}


def run(seed=0):
    lab = labs.Lab()
    T = truths(48)

    h = cl.hotelling(**T["mine"])
    hf = cl.hotelling(**T["mine_falling"])
    pf = np.array(hf["price"][: hf["exhausted"]])
    lab.row("Hotelling: first rent; year exhausted; with falling costs, the price's low (year)",
            f"{h['rent0']:.2f}; {h['exhausted']}; {pf.min():.2f} (year {int(pf.argmin())})")

    cpi = _annual(data.fred("CPIAUCNS"), "date")
    metals = {k: _annual(data.pinksheet(k)) for k in ("copper", "nickel", "tin")}
    years = sorted(set(cpi).intersection(*[set(v) for v in metals.values()]))
    b = cl.bet_windows(years, {k: [metals[k][y] for y in years] for k in metals}, [cpi[y] for y in years])
    lab.row("the bet: windows; Ehrlich's share; 1980-90", f"{b['n']}; {100 * b['ehrlich_share']:.0f}%; "
            f"{100 * b['change'][b['start'].index(1980)]:+.0f}%")

    f = cl.fishery_curves(**T["fishery"])
    lab.row("fishery: effort under open access, at most rent, at most fish", f"{f['e_open']:.2f}, {f['e_mey']:.2f}, "
            f"{f['e_msy']:.2f}")

    g = data.gcp_co2()
    yrs = np.array(g["year"])
    s = data.so2("World")
    sv = np.array(s["value"]) / 1e6
    so2 = np.interp(yrs, s["year"], sv, left=0.0)
    early = yrs < s["year"][0]
    so2[early] = sv[0] * np.clip((yrs[early] - 1850) / (s["year"][0] - 1850), 0, None)   # as in compute.py
    c, hc = data.co2_mlo(), data.hadcrut5()
    fit = cl.fit_climate(yrs, g["fossil"], g["land"], so2, c["year"], c["ppm"], hc["year"], hc["anomaly"])
    lab.row("climate fit: sinks' speed; land weight; other gases; aerosols", f"{fit['speed']:.2f}; "
            f"{fit['land_weight']:.2f}; {fit['ghg_scale']:.2f}; {fit['aerosol']:.2f}")
    lab.row("climate fit: errors (ppm; degrees)", f"{fit['ppm_rmse']:.2f}; {fit['temp_rmse']:.3f}")

    E = np.array(g["fossil"]) + fit["land_weight"] * np.nan_to_num(np.array(g["land"]))
    cc = cl.carbon_cycle(E, fit["speed"])
    Ts, Ds = cl.ebm(cl.forcing(cc["ppm"], so2, fit["ghg_scale"], fit["aerosol"]), fit["ecs"])
    off = Ts[(yrs >= 1850) & (yrs <= 1900)].mean()
    d = cl.Dice(fit, cc["boxes"], (Ts[-1] - off, Ds[-1] - off))
    base_mu = np.interp(d.year, [2025, 2050, 2100, 2300], [0.05, 0.10, 0.22, 0.22])
    base = d.run(base_mu)
    opt = d.optimize(0.015, 1.45)
    lab.row("the model: warming in 2100, business as usual and optimal", f"{base['T'][75]:.2f}, "
            f"{opt['run']['T'][75]:.2f}")
    sc = d.scc(base_mu, 0.015, 1.45, rates=(0.01, 0.02, 0.03, 0.05))
    lab.row("social cost of carbon: Ramsey; at 1, 2, 3, 5%", f"{sc['ramsey']:.0f}; " +
            ", ".join(f"{sc[f'r{r:g}']:.0f}" for r in (0.01, 0.02, 0.03, 0.05)))
    assert sc["r0.01"] > sc["r0.02"] > sc["r0.03"] > sc["r0.05"] > 0
    assert fit["ppm_rmse"] < 3 and opt["run"]["T"][75] < base["T"][75]

    t = cl.tail_losses([6, 10, 20], **{**T["tails"], "seed": T["tails"]["seed"] + seed})
    lab.row("fat tails: loss at cut-offs 6, 10, 20 (thin; fat)", ", ".join(f"{100 * x:.0f}%" for x in t["thin"]) +
            "; " + ", ".join(f"{100 * x:.0f}%" for x in t["fat"]))

    members = [cl.club(tariff=x, **T["club"])["members"] for x in (0.0, 0.05, 0.07, 0.1)]
    lab.row("the club: members at tariffs 0, 5, 7, 10%", ", ".join(map(str, members)))

    sp = data.solar_pv()
    py, pr = np.array(sp["price_year"]), np.array(sp["price"])
    m = np.isin(py, sp["cap_year"])
    lc = cl.learning_curve(np.array(sp["capacity"])[np.isin(sp["cap_year"], py)], pr[m])
    lab.row("solar: learning rate per doubling", f"{100 * lc['learning_rate']:.1f}%")

    P = T["power"]
    w = cl.withholding(P["capacity"], P["cost"], P["owner"], 1, 35.0, cap_price=P["cap_price"], steps=57)
    lab.row("withholding at 35 GW: profit offering all; best; GW held", f"{w['profit_none']:.0f}; "
            f"{w['best_profit']:.0f}; {w['best']:.1f}")

    lab.note = ("Hotelling fixes the rent's path, not the price's; the bet is a coin toss over a decade; open access "
                "fishes to where the rent is gone; four fitted equations reproduce the warming; the social cost of "
                "carbon is mostly a matter of the discount rate; fat tails make the answer follow the cut-off; clubs "
                "need a penalty; and tight power markets reward holding back.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot(base["year"], base["T"], color=labs.ORANGE, label="business as usual")
    ax[0].plot(opt["run"]["year"], opt["run"]["T"], color=labs.BLUE, label="optimal")
    ax[0].set(title="warming, degrees C", xlabel="year")
    ax[0].legend()
    rates = np.linspace(0.01, 0.06, 11)
    ax[1].semilogy(100 * rates, [d.scc(base_mu, rates=(r,))[f"r{r:g}"] for r in rates], color=labs.BLUE)
    ax[1].set(title="social cost of carbon, $ a tonne", xlabel="discount rate, %")
    lab.fig = fig
    return lab
