"""Quant, Built: every part's hands-on lab runs, checks its own result, and draws its figure.

    python -m pytest -q tests/test_quant_labs.py

Each lab asserts the theory it illustrates inside ``run()`` (a Monte Carlo estimate against its closed form, an
estimator against the truth it was simulated from), so running it is the test.  The labs are seeded and use no data.
"""

import importlib.util
import os
import subprocess
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import pytest  # noqa: E402

from videos.quant import labs  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PARTS = range(1, labs.N_PARTS + 1)


@pytest.mark.parametrize("part", PARTS)
def test_lab_runs_and_checks_itself(part, tmp_path):
    module = labs.load(part)
    assert module.TITLE and module.GOAL and len(module.TASKS) == 3, "a title, a goal and three things to change"
    assert module.__doc__ and module.__doc__.startswith(f"Lab {part}:")
    start = time.time()
    lab = module.run(seed=0)
    assert time.time() - start < 60, "a lab runs in seconds"
    assert len(lab.rows) >= 3 and all(isinstance(a, str) and isinstance(b, str) for a, b in lab.rows)
    assert lab.note, "one line saying what the numbers mean"
    assert lab.fig is not None and len(lab.fig.axes) >= 1
    png = labs.save(lab, tmp_path / f"lab{part:02d}.png")
    assert png.stat().st_size > 10_000


def test_labs_are_seeded():
    a, b = labs.run(10, seed=0), labs.run(10, seed=0)
    assert a.rows == b.rows


def test_every_part_has_a_lab_and_nothing_else():
    files = sorted(p.name for p in (ROOT / "videos" / "quant" / "labs").glob("lab*.py"))
    assert files == [f"lab{p:02d}.py" for p in PARTS]


def test_house_imports_without_manim(tmp_path):
    """The labs promise ``pip install numpy scipy matplotlib numba``: hide manim and run one from a clean process."""
    blocker = tmp_path / "manim.py"
    blocker.write_text("raise ModuleNotFoundError(\"No module named 'manim'\", name='manim')\n")
    code = ("import importlib.util as u, sys\n"
            "u_find = u.find_spec\n"
            "u.find_spec = lambda name, *a, **k: None if name == 'manim' else u_find(name, *a, **k)\n"
            "from videos.quant import labs\n"
            "lab = labs.run(3)\n"
            "assert 'manim' not in sys.modules and type(sys.modules['explainer']).__name__ == 'module'\n"
            "assert not hasattr(sys.modules['explainer'], 'VoiceoverScene')\n"
            "print(lab.rows[0][1])\n")
    env = dict(os.environ, PYTHONPATH=f"{tmp_path}{os.pathsep}{ROOT}", MPLBACKEND="Agg")
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr[-2000:]
    assert "2,560" in out.stdout


def test_manim_is_what_the_films_use():
    """Where manim is installed the loader must not shadow the real package."""
    if importlib.util.find_spec("manim") is None:
        pytest.skip("manim not installed")
    import explainer

    assert hasattr(explainer, "VoiceoverScene")
