"""Bounded Part 8 QA entry point; always enforce CLI and upstream cache guards.

Run as a file, not a module, to avoid importing the project before the guards:
    python videos/ai/ai8/qa_cached.py --only Hook --lang en

This wrapper starts no producer. Missing/stale inputs must fail in cached-only
loaders. Exact original source/data pins must be checked separately before use.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', nargs='+', required=True, help='explicit scene classes; no whole-part default')
    parser.add_argument('--lang', choices=('en', 'zh'), required=True)
    parser.add_argument('--motion', action='store_true', help='bounded silent 480p15 capture')
    parser.add_argument('--timeout', type=int, default=1200)
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    env = dict(os.environ, EXPLAINER_CACHED_ONLY='1', EXPLAINER_TTS='silent',
               OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    command = [sys.executable, str(ROOT / 'tools/qa_series.py'), 'ai8', '--cached-only',
               '--lang', args.lang, '--only', *args.only, '--timeout', str(args.timeout)]
    if args.motion:
        command.append('--motion')
    return subprocess.run(command, cwd=ROOT, env=env, check=False).returncode


if __name__ == '__main__':
    sys.exit(main())
