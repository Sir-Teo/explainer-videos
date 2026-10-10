"""Download LIGO's open data for GW150914 and freeze the part the video shows into a small committed snapshot.

    python -m videos.relativity.fetch        # -> videos/relativity/data/gw150914.json

Source: the Gravitational Wave Open Science Center (GWOSC, https://gwosc.org), event GW150914 in the GWTC-1
catalog: 32 s of strain at 4096 Hz from LIGO Hanford (H1) and Livingston (L1), plus the catalog's parameter
estimates.  Whitening follows GWOSC's "Binary Black Hole Signals in LIGO Open Data" tutorial: estimate each
detector's noise spectrum from the full 32 s (Welch, 4 s Hann segments), divide the Fourier transform of the strain
by the square root of that spectrum, and transform back.  The snapshot keeps 0.65 s of whitened strain around the
event; ``compute.py`` band-passes it, overlays the detectors, and builds the time-frequency map.

It also saves a small copy of the Event Horizon Telescope's 2019 image of the black hole in M87
(ESO image eso1907a, credit: EHT Collaboration, licensed CC BY 4.0) to show next to the ray-traced one.
"""

from __future__ import annotations

import io
import json
import urllib.request
from pathlib import Path

import numpy as np

from explainer.tts import REPO_ROOT

EVENT_API = "https://gwosc.org/eventapi/json/GWTC-1-confident/GW150914/v3/"
RAW = REPO_ROOT / ".cache" / "relativity" / "raw"
OUT = Path(__file__).resolve().parent / "data" / "gw150914.json"
EHT_URL = "https://cdn.eso.org/images/screen/eso1907a.jpg"
EHT_OUT = Path(__file__).resolve().parent / "data" / "eht_m87.jpg"
T_EVENT = 1126259462.44  # GPS time of the peak at Hanford, as in the GWOSC tutorial
WINDOW = (-0.5, 0.15)
L1_SHIFT = 0.007  # Livingston saw the wave ~7 ms before Hanford


def get(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


def strain(det: str, files: list[dict]) -> tuple[np.ndarray, float, float]:
    import h5py

    f = next(x for x in files if x["detector"] == det and x["sampling_rate"] == 4096 and x["duration"] == 32
             and x["format"] == "hdf5")
    RAW.mkdir(parents=True, exist_ok=True)
    local = RAW / Path(f["url"]).name
    if not local.exists():
        local.write_bytes(get(f["url"]))
    with h5py.File(local, "r") as h:
        s = h["strain"]["Strain"][()]
        dt = h["strain"]["Strain"].attrs["Xspacing"]
        t0 = h["meta"]["GPSstart"][()]
    return s.astype(np.float64), float(dt), float(t0)


def whiten(s: np.ndarray, dt: float) -> np.ndarray:
    from scipy.signal import welch
    from scipy.signal.windows import tukey

    fs = 1 / dt
    f, psd = welch(s, fs=fs, nperseg=int(4 * fs), window="hann")
    n = len(s)
    freqs = np.fft.rfftfreq(n, dt)
    hf = np.fft.rfft(s * tukey(n, alpha=1 / 8))
    white = hf / np.sqrt(np.interp(freqs, f, psd) / dt / 2)
    return np.fft.irfft(white, n=n)


def fetch_eht():
    from PIL import Image

    im = Image.open(io.BytesIO(get(EHT_URL))).convert("RGB")
    im.thumbnail((480, 480))
    EHT_OUT.parent.mkdir(exist_ok=True)
    im.save(EHT_OUT, quality=88)
    print(f"Wrote {EHT_OUT.relative_to(REPO_ROOT)} ({EHT_OUT.stat().st_size / 1e3:.0f} kB, {im.size[0]}x{im.size[1]})")


def main():
    fetch_eht()
    ev = json.loads(get(EVENT_API))
    ev = next(iter(ev["events"].values()))
    out = {
        "source": "Gravitational Wave Open Science Center (gwosc.org), GWTC-1-confident GW150914 v3",
        "event_api": EVENT_API,
        "t_event_gps": T_EVENT,
        "L1_shift_s": L1_SHIFT,
    }
    for k in ("mass_1_source", "mass_2_source", "final_mass_source", "chirp_mass_source", "luminosity_distance",
              "redshift", "network_matched_filter_snr"):
        out[k] = ev[k]
    pe = ev["parameters"]["gwtc1_pe_GW150914"]
    out["E_rad"] = pe["E_rad"]
    for det in ("H1", "L1"):
        s, dt, t0 = strain(det, ev["strain"])
        w = whiten(s, dt)
        t = t0 + np.arange(len(s)) * dt - T_EVENT
        sel = (t >= WINDOW[0]) & (t < WINDOW[1])
        out["fs"] = round(1 / dt)
        out["t"] = [round(x, 7) for x in t[sel]]
        out[det + "_white"] = [float(f"{x:.5g}") for x in w[sel]]
        out[det + "_file"] = next(x["url"] for x in ev["strain"] if x["detector"] == det and x["format"] == "hdf5"
                                  and x["sampling_rate"] == 4096 and x["duration"] == 32)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":")))
    print(f"Wrote {OUT.relative_to(REPO_ROOT)} ({OUT.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
