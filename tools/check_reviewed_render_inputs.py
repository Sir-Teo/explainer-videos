"""Read-only presence check for selected reviewed-input gates in the AI series.

Run from the repository root with `python tools/check_reviewed_render_inputs.py`.
This is not an exhaustive dependency check or a scientific/production approval.
Each part's own reader performs stricter checks when the scene loads.
"""
from __future__ import annotations

import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.check_part23_qa_inputs import REQUIRED as PART23


def requirements(root: Path, run_id: str | None = None) -> dict[str, list[Path]]:
    cache = root / '.cache'
    result = {
        'Part 11: SOAP-V3 capsule': [cache / 'ai11/contracts/soap-v3-v1/manifest.json'],
        'Part 16: reviewed manifest': [cache / 'ai16/render-manifest.json'],
        'Part 21: reviewed manifest': [cache / 'ai21/render-manifest.json'],
        'Part 23: accepted JSON bundles': [cache / 'ai23' / f'{name}.json' for name in PART23],
    }
    if run_id:
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', run_id):
            raise ValueError('AI27_BASELINE_RUN is not a valid run ID')
        run = cache / 'ai27/baseline-runs' / run_id
        result['Part 27: selected run audit'] = [run / 'baselines_f64.audit.json']
    else:
        result['Part 27: default baseline bundle'] = [cache / 'ai27' / name for name in
            ('baselines.json', 'baselines_f64.json', 'baselines_f64.audit.json')]
    return result


def main() -> int:
    try:
        groups = requirements(ROOT, os.environ.get('AI27_BASELINE_RUN'))
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    missing = False
    for title, files in groups.items():
        absent = [p for p in files if not p.is_file()]
        missing |= bool(absent)
        print(f"{'MISSING' if absent else 'PRESENT'}  {title}")
        for p in absent:
            print(f'  {p.relative_to(ROOT)}')
    print('Presence does not validate contents, companion files, models, audio, or complete render readiness.')
    return 1 if missing else 0


if __name__ == '__main__':
    raise SystemExit(main())
