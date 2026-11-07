"""Build explainer/stats/data/nhanes_bp.csv from six public NHANES 2017-2018 files (CDC/NCHS, public domain).

    for f in DEMO_J BPX_J BMX_J DR1TOT_J DR2TOT_J BPQ_J; do
        curl -sSL -o $f.xpt https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/$f.xpt
    done
    python tools/nhanes_extract.py <dir with the .xpt files> explainer/stats/data/nhanes_bp.csv

One row per examined participant aged 18 or over, with only the columns Part 20 of *Statistics, Built* uses, renamed:

    seqn, sex (1 male, 2 female), age (top-coded at 80), race (RIDRETH3 codes), pir (income-to-poverty ratio, top-coded
    at 5), educ (DMDEDUC2 codes), pregnant (RIDEXPRG: 1 yes), wt_mec (exam weight), wt_diet1 (day-1 dietary weight),
    strata, psu, sbp1..sbp4, dbp1..dbp4 (mm Hg; NHANES codes a diastolic of 0 when it could not be read), bmi,
    na1, kcal1, k1, diet1_ok (DR1DRSTZ: 1 = reliable recall), na2, kcal2, diet2_ok (the second-day recall), told_high
    (BPQ020: 1 yes, 2 no), bp_meds (BPQ050A: 1 taking prescribed medicine now).

Missing values stay empty.  Every cleaning decision (exclusions, averaging readings, implausible values) is made in
``videos/stats/stats20/compute.py`` on screen, not here.
"""

import sys

import pandas as pd

COLS = {
    "DEMO_J": {"SEQN": "seqn", "RIAGENDR": "sex", "RIDAGEYR": "age", "RIDRETH3": "race", "INDFMPIR": "pir",
               "DMDEDUC2": "educ", "RIDEXPRG": "pregnant", "WTMEC2YR": "wt_mec", "SDMVSTRA": "strata", "SDMVPSU": "psu",
               "RIDSTATR": "status"},
    "BPX_J": {"SEQN": "seqn", **{f"BPXSY{i}": f"sbp{i}" for i in range(1, 5)}, **{f"BPXDI{i}": f"dbp{i}" for i in range(1, 5)}},
    "BMX_J": {"SEQN": "seqn", "BMXBMI": "bmi"},
    "DR1TOT_J": {"SEQN": "seqn", "WTDRD1": "wt_diet1", "DR1TSODI": "na1", "DR1TKCAL": "kcal1", "DR1TPOTA": "k1",
                 "DR1DRSTZ": "diet1_ok"},
    "DR2TOT_J": {"SEQN": "seqn", "DR2TSODI": "na2", "DR2TKCAL": "kcal2", "DR2DRSTZ": "diet2_ok"},
    "BPQ_J": {"SEQN": "seqn", "BPQ020": "told_high", "BPQ050A": "bp_meds"},
}


def main(src: str, out: str) -> None:
    frames = {}
    for f, cols in COLS.items():
        d = pd.read_sas(f"{src}/{f}.xpt", format="xport")[list(cols)]
        frames[f] = d.rename(columns=cols)
    df = frames["DEMO_J"]
    df = df[(df.age >= 18) & (df.status == 2)].drop(columns="status")  # examined adults
    for f in list(COLS)[1:]:
        df = df.merge(frames[f], on="seqn", how="left")
    for c in df.columns:
        if c not in ("pir", "bmi", "wt_mec", "wt_diet1", "na1", "kcal1", "k1", "na2", "kcal2"):
            df[c] = df[c].round().astype("Int64")
    df["pir"] = df["pir"].round(2)
    df["bmi"] = df["bmi"].round(1)
    for c in ("wt_mec", "wt_diet1"):
        df[c] = df[c].round(1)
    for c in ("na1", "kcal1", "k1", "na2", "kcal2"):
        df[c] = df[c].round(0)
    df.to_csv(out, index=False)
    print(f"{len(df)} adults -> {out}")


def day2_weights(src: str, extract: str, out: str) -> None:
    """Export WTDR2D aligned by SEQN without changing the original 29-column extract."""
    base = pd.read_csv(extract, usecols=["seqn"])
    extra = pd.read_sas(f"{src}/DR2TOT_J.xpt", format="xport")[["SEQN", "WTDR2D"]]
    extra = extra.rename(columns={"SEQN": "seqn", "WTDR2D": "wt_diet2"})
    result = base.merge(extra, on="seqn", how="left", validate="one_to_one", sort=False)
    result["seqn"] = result["seqn"].astype(int)
    result["wt_diet2"] = result["wt_diet2"].round(1)
    result.to_csv(out, index=False)


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "--day2-weights":
        day2_weights(*sys.argv[2:])
    else:
        main(sys.argv[1], sys.argv[2])
