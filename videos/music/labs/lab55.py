"""Lab 55: rooms and space, computed: Sabine and Eyring, a room's modes against Weyl, a diffuser's Gauss sum, and a
sound placed round a spherical head."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import space as SP

TITLE = "Rooms and space, computed"
GOAL = ("Compute a room's reverberation by Sabine and Eyring and its modes against Weyl's count, check a quadratic-"
        "residue diffuser's Gauss sum and its scattering, and place a sound round a spherical head by its time and level "
        "differences.")
TASKS = [
    "Change DIMS and ALPHA. How do Sabine's and Eyring's times part as the room gets deader, and where is the Schroeder frequency?",
    "Change N (a prime) and F0. Do all the diffraction lobes still carry the same energy? What happens if N is not prime?",
    "Change the azimuths in the ear problem. Which pairs of directions can a spherical head never tell apart?",
]
DIMS = (6.0, 4.5, 3.0)
ALPHA = 0.15
N, F0 = 7, 500.0


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    Lx, Ly, Lz = DIMS
    V = Lx * Ly * Lz
    S = 2 * (Lx * Ly + Ly * Lz + Lx * Lz)
    sab = 0.161 * V / (ALPHA * S)
    eyr = 0.161 * V / (-S * math.log(1 - ALPHA))
    lab.row(f"room {Lx:g} x {Ly:g} x {Lz:g} m, alpha {ALPHA:g}: T60 by Sabine / Eyring", f"{sab:.3f} / {eyr:.3f} s")
    lab.row("Schroeder frequency", f"{SP.schroeder_frequency(eyr, V):.0f} Hz")
    modes = SP.room_modes(DIMS, 200.0)
    lab.row("modes below 200 Hz: counted / Weyl", f"{len(modes)} / {float(SP.weyl_count(DIMS, 200.0)):.1f}")
    lab.row("the first five modes (Hz)", ", ".join(f"{m[0]:.1f} {m[1]}" for m in modes[:5]))
    d = SP.qrd_depths(N, F0)
    lab.row(f"QRD, N = {N}, f0 = {F0:g} Hz: well depths (cm)", ", ".join(f"{100 * x:.1f}" for x in d))
    sums = [abs(sum(np.exp(2j * np.pi * (n * n + k * n) / N) for n in range(N))) for k in range(N)]
    lab.row("|Gauss sum| for every lobe k (sqrt N = %.3f)" % math.sqrt(N), ", ".join(f"{s_:.3f}" for s_ in sums))
    ang = np.linspace(-90, 90, 181)
    q = 20 * np.log10(SP.scattering(d, 0.06, 2 * F0, ang) + 1e-9)
    fl = 20 * np.log10(SP.scattering(np.zeros(N), 0.06, 2 * F0, ang) + 1e-9)
    lab.row(f"diffusion coefficient at {2 * F0:g} Hz: diffuser / flat", f"{SP.diffusion_coefficient(q[::5]):.2f} / {SP.diffusion_coefficient(fl[::5]):.2f}")
    if all(N % p for p in range(2, int(math.isqrt(N)) + 1)) and N > 2:
        assert max(abs(s_ - math.sqrt(N)) for s_ in sums) < 1e-9
    assert eyr < sab

    # sound: noise bursts round the head; ear problem: name each direction
    t = np.arange(int(0.6 * SR)) / SR
    burst = rng.standard_normal(len(t)) * np.hanning(len(t))
    choices = [-90, -30, 0, 30, 90]
    clips, answers = [], []
    for i in range(4):
        az = choices[int(rng.integers(0, len(choices)))]
        hl, hr = SP.ear_filters(math.radians(az))
        y = np.stack([np.convolve(burst, hl), np.convolve(burst, hr)], axis=1)
        clips.append(Clip(0.2 * y / np.max(np.abs(y)), SR))
        answers.append(f"{az:+d} deg")
    lab.audio = concat(clips, gap=0.6)
    lab.row("ear problem (headphones): where was each burst? (listen first)", ", ".join(answers))

    fig, (ax1, ax2) = labs.figure(2)
    f = np.linspace(20, 200, 400)
    ax1.step(f, [sum(1 for m in modes if m[0] <= x) for x in f], color=labs.GOLD, where="post", label="counted")
    ax1.plot(f, SP.weyl_count(DIMS, f), color="C3", label="Weyl")
    ax1.set_xlabel("Hz")
    ax1.set_ylabel("modes below f")
    ax1.legend(fontsize=7)
    ax2.plot(ang, fl, color="0.6", label="flat")
    ax2.plot(ang, q, color=labs.GOLD, label="QRD")
    ax2.set_ylim(-40, 2)
    ax2.set_xlabel("degrees")
    ax2.set_ylabel(f"dB at {2 * F0:g} Hz")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("A room's reverberation is its volume over its absorption; below the Schroeder frequency it is a handful "
                "of modes, whose count grows as the cube of the frequency. A residue diffuser sends equal energy into every "
                "lobe because Gauss's sum has the same size for every k. Two ears read time and level, and a sphere cannot "
                "tell front from back.")
    return lab
