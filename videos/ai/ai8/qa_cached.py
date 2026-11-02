"""Bounded Part 8 QA entry point; always enforce CLI and upstream cache guards.

Run as a file, not a module, to avoid importing the project before the guards:
    python videos/ai/ai8/qa_cached.py --only Hook --lang en

This wrapper starts no producer. Missing/stale inputs must fail in cached-only
loaders. Exact original source/data pins must be checked separately before use.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
THREAD_KEYS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
               'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')
CORRECTED_ITEMS = {'Hoeffding': ('union',), 'MaxMargin': ('maxmargin',), 'Outro': ()}


def preflight_corrected(scenes, module=None):
    """Read and validate selected fresh bundles before starting any QA child."""
    items = sorted({item for scene in scenes for item in CORRECTED_ITEMS.get(scene, ())})
    if not items:
        return {}
    previous = {key: os.environ.get(key) for key in THREAD_KEYS}
    try:
        os.environ.update({key: '1' for key in THREAD_KEYS})
        if module is None:
            spec = importlib.util.spec_from_file_location('ai8_corrected_preflight',
                                                        ROOT / 'videos/ai/ai8/corrected_v1.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        return {item: module.load_bundle(module.DEFAULT_ROOT, item, expected_mode='fresh')[1]
                for item in items}
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def certify_selection(scenes, lang, recipe, snapshots, motion=False):
    """Bind this explicit selection to actual QA inputs; do not retag fingerprints."""
    if recipe not in ('legacy','corrected-v1'):
        raise ValueError('unknown Part 8 scientific recipe selection')
    for scene in scenes:
        folder = ROOT / 'renders/qa/series/ai8' / lang / (scene + ('_motion' if motion else ''))
        raw = (folder / 'result.json').read_bytes()
        result = json.loads(raw)
        if (result.get('video'), result.get('scene'), result.get('lang'), result.get('mode')) != (
                'ai8', scene, lang, 'motion' if motion else 'endpoints') or result.get('status') != 'passed' or result.get('warnings'):
            raise ValueError('selected QA result identity or preflight status mismatch')
        inputs = result.get('inputs', {})
        fingerprint = result.get('fingerprint')
        if not isinstance(inputs,dict) or not isinstance(fingerprint,str) or len(fingerprint)!=64 or any(c not in '0123456789abcdef' for c in fingerprint):
            raise ValueError('selected QA input/source identity is missing')
        receipts = {}
        if recipe == 'corrected-v1':
            expected_paths = {'.cache/ai8-corrected-v1/' + item + '/' + name
                              for item in CORRECTED_ITEMS.get(scene, ())
                              for name in ('receipt.json','data.json','data.npz')}
            observed_paths = {path for path in inputs if path.startswith('.cache/ai8-corrected-v1/')}
            # The shared recorder also records a JSON file's absent NPZ companion.
            # Accept only this precise sentinel; all other missing/extra paths fail.
            for item in CORRECTED_ITEMS.get(scene, ()):
                absent = '.cache/ai8-corrected-v1/' + item + '/receipt.npz'
                if absent in observed_paths:
                    if inputs[absent] is not None or os.path.lexists(ROOT / absent):
                        raise ValueError('recipe receipt companion must remain absent')
                    observed_paths.remove(absent)
            if observed_paths != expected_paths:
                raise ValueError('QA consumed an unexpected corrected item or omitted a required one')
            for item in CORRECTED_ITEMS.get(scene, ()):
                for name in ('receipt.json','data.json','data.npz'):
                    relative = '.cache/ai8-corrected-v1/' + item + '/' + name
                    path = ROOT / relative
                    stat = path.stat()
                    if inputs.get(relative) != [stat.st_size, stat.st_mtime_ns]:
                        raise ValueError('QA did not record the selected corrected bundle')
                receipt = ROOT / '.cache/ai8-corrected-v1' / item / 'receipt.json'
                receipt_raw = receipt.read_bytes()
                current = json.loads(receipt_raw)
                if current != snapshots[item]:
                    raise ValueError('selected recipe receipt changed')
                receipts[item] = {'recipe': current['recipe'],
                                  'receipt_sha256': hashlib.sha256(receipt_raw).hexdigest()}
        elif any(path.startswith('.cache/ai8-corrected-v1/') for path in inputs):
            raise ValueError('legacy replay consumed corrected data')
        result_sha = hashlib.sha256(raw).hexdigest()
        selection = {'schema': 1, 'recipe': recipe, 'scene': scene, 'lang': lang,
                     'result_sha256': result_sha, 'source_fingerprint': result['fingerprint'],
                     'corrected_receipts': receipts,
                     'scope': 'regression control; no direct union cache load' if scene == 'Outro' else
                              'explicit legacy replay' if recipe == 'legacy' else 'selected corrected inputs',
                     'acceptance': 'runtime/input identity only; independent visual and speech acceptance remain separate'}
        data = (json.dumps(selection, indent=2, sort_keys=True) + '\n').encode()
        target = folder / ('recipe-selection-' + recipe + '-' + result_sha + '.json')
        if target.exists():
            if target.read_bytes() != data:
                raise ValueError('existing recipe-selection witness differs')
        else:
            with target.open('xb') as handle:
                handle.write(data)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', nargs='+', required=True, help='explicit scene classes; no whole-part default')
    parser.add_argument('--lang', choices=('en', 'zh'), required=True)
    parser.add_argument('--recipe', choices=('legacy', 'corrected-v1'),
                        help='required for Hoeffding, MaxMargin and the Outro regression control')
    parser.add_argument('--motion', action='store_true', help='bounded silent 480p15 capture')
    parser.add_argument('--timeout', type=int, default=1200)
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    if args.recipe is None and any(scene in CORRECTED_ITEMS for scene in args.only):
        parser.error('select --recipe corrected-v1 or an explicitly labeled --recipe legacy replay')
    recipe = args.recipe or 'legacy'
    env = dict(os.environ, EXPLAINER_CACHED_ONLY='1', EXPLAINER_TTS='silent',
               EXPLAINER_AI8_RECIPE=recipe, **{key: '1' for key in THREAD_KEYS})
    try:
        before = preflight_corrected(args.only) if recipe == 'corrected-v1' else {}
    except Exception as exc:
        parser.error('corrected-v1 preflight failed: ' + str(exc))
    command = [sys.executable, str(ROOT / 'tools/qa_series.py'), 'ai8', '--cached-only',
               '--lang', args.lang, '--only', *args.only, '--timeout', str(args.timeout)]
    if args.motion:
        command.append('--motion')
    result = subprocess.run(command, cwd=ROOT, env=env, check=False)
    if recipe == 'corrected-v1':
        try:
            if preflight_corrected(args.only) != before:
                parser.error('corrected-v1 inputs changed during QA')
        except Exception as exc:
            parser.error('corrected-v1 postflight failed: ' + str(exc))
    if result.returncode == 0 and args.recipe is not None:
        try:
            certify_selection(args.only, args.lang, recipe, before, args.motion)
        except Exception as exc:
            parser.error('recipe-selection witness failed: ' + str(exc))
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
