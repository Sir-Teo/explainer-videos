"""Explicit versioned Part 8 corrections. Legacy recipes and caches are read-only.

Run this file with --item union|maxmargin --mode fresh. Each item reserves a
new bundle in .cache/ai8-corrected-v1 before numerical work. There is no force,
resume, automatic generation on load, or fallback to unversioned outcomes.
--mode derived-weights --input-dir DIR is a distinct MaxMargin-only operation
on caller-supplied maxmargin.json/npz, not a fresh or authenticated old trajectory.
"""
from __future__ import annotations

import argparse
import ast
from decimal import Decimal, localcontext
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ROOT = ROOT / '.cache/ai8-corrected-v1'
SOURCE_SHA = '2250fcee8907efb53dcf0ad6f0d521603ecbd922d6e42b29e265bb33b939f574'
CORRECTED_SOURCE_SHA = 'a3b888242e0708027d5b7f9a89c995bf6773d29f914f3599135260b042d84a2d'
RECIPES = {'union': 'union-minimum-cdf-v1', 'maxmargin': 'maxmargin-postupdate-loss-v1'}
RUNTIME = {'python': '3.12.14', 'numpy': '2.5.4', 'scipy': '1.18.1'}
THREAD_KEYS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
               'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')
CHANGES = (
    ('sf = binom.sf(k - 1, n, 0.5)  # P(errors >= k)',
     'sf = binom.sf(k, n, 0.5)  # P(errors > k)'),
    ('loss = float(np.logaddexp(0, -z).mean())',
     'loss = float(np.logaddexp(0, -(tX @ w)).mean())'),
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    data = Path(path).read_bytes()
    return {'bytes': len(data), 'sha256': sha(data)}


def strict_json(data):
    def invalid(value):
        raise ValueError('nonfinite JSON constant: ' + value)
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError('duplicate JSON key: ' + key)
            out[key] = value
        return out
    return json.loads(data, parse_constant=invalid, object_pairs_hook=unique)


def source_identity():
    original = (ROOT / 'videos/ai/ai8/compute.py').read_bytes()
    if sha(original) != SOURCE_SHA:
        raise ValueError('legacy scientific source differs from the reviewed recipe')
    corrected = original.decode()
    for old, new in CHANGES:
        if corrected.count(old) != 1:
            raise ValueError('scientific correction is not a unique source replacement')
        corrected = corrected.replace(old, new)
    if sha(corrected.encode()) != CORRECTED_SOURCE_SHA:
        raise ValueError('corrected scientific source identity mismatch')
    return {'legacy_compute_sha256': SOURCE_SHA,
            'corrected_compute_sha256': CORRECTED_SOURCE_SHA,
            'recipe_program_sha256': sha(Path(__file__).read_bytes())}, corrected


def runtime_identity():
    current = {'python': platform.python_version(),
               'numpy': importlib.metadata.version('numpy'),
               'scipy': importlib.metadata.version('scipy')}
    if current != RUNTIME or any(os.environ.get(k) != '1' for k in THREAD_KEYS):
        raise ValueError('requires the exact documented numerical runtime and one thread')
    records={}
    for package in ('numpy','scipy'):
        record=importlib.metadata.distribution(package).read_text('RECORD')
        if not record:
            raise ValueError('numerical package build identity is unavailable')
        records[package]=sha(record.encode())
    return {**current, 'machine': platform.machine(), 'byteorder': sys.byteorder,
            'executable_sha256':identity(Path(sys.executable).resolve())['sha256'],
            'package_RECORD_sha256':records,
            'threads': {k: os.environ[k] for k in THREAD_KEYS}}


def fresh_result(item):
    """Execute only selected pure public functions; never import the cache producer."""
    import numpy as np
    _, corrected = source_identity()
    wanted = {'union': ('rng', 'compute_union'),
              'maxmargin': ('rng', 'maxmargin_data', 'svm_dual', 'compute_maxmargin')}[item]
    tree = ast.parse(corrected)
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in wanted]
    if {n.name for n in nodes} != set(wanted):
        raise ValueError('incomplete selected scientific functions')
    namespace = {'np': np, 'math': math}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<ai8-corrected-v1>', 'exec'), namespace)
    return namespace['compute_' + item]()


def correct_postupdate_losses(value):
    """Return new arrays; evaluate losses at recorded weights without any updates."""
    import numpy as np
    for key in ('X','t','rec'):
        if not isinstance(value[key],np.ndarray) or value[key].dtype != np.dtype('float64') or not np.isfinite(value[key]).all():
            raise ValueError('derived inputs must be finite binary64 arrays')
    out = {k: v.copy() if isinstance(v, np.ndarray) else v for k, v in value.items()}
    X, t, rec = out['X'], out['t'], out['rec']
    if X.ndim != 2 or X.shape[1] != 2 or t.shape != (len(X),) or rec.ndim != 2 or rec.shape[1] != 7:
        raise ValueError('invalid signed two-dimensional trajectory')
    for row in rec:
        row[3] = np.logaddexp(0, -(t[:, None] * X) @ row[5:7]).mean()
    return out


def validate_result(item, value, check_losses=True):
    """Independent median boundary checks and same-row geometry/loss contracts."""
    import numpy as np
    arrays = {k: v for k, v in value.items() if isinstance(v, np.ndarray)}
    if any(a.dtype != np.dtype('float64') or not np.isfinite(a).all() for a in arrays.values()):
        raise ValueError('arrays must be finite binary64 values')
    scalars = {k: v for k, v in value.items() if k not in arrays}
    # Reject NaN/Infinity even when supplied through overflowing JSON numbers.
    json.dumps(scalars, allow_nan=False)
    if item == 'union':
        expected = {'best100': (7,), 'gap100': (7,), 'bound100': (7,),
                    'best1000': (7,), 'gap1000': (7,), 'bound1000': (7,), 'sample_errs': (1000,)}
        if {k: a.shape for k, a in arrays.items()} != expected:
            raise ValueError('union array schema mismatch')
        if set(scalars) != {'Ks','delta','ns','sample_best','sample_K','sample_n','fresh_best'}:
            raise ValueError('union metadata schema mismatch')
        if scalars['Ks'] != [1,10,100,1000,10000,100000,1000000] or scalars['ns'] != [100,1000] or scalars['delta'] != .05:
            raise ValueError('union recipe parameters mismatch')
        if scalars['sample_n']!=100 or scalars['sample_K']!=1000 or not 0<=scalars['fresh_best']<=1:
            raise ValueError('union sample parameters mismatch')
        generator=np.random.Generator(np.random.PCG64(1984))
        sample=generator.binomial(100,.5,1000)/100
        fresh=float(generator.binomial(10000,.5)/10000)
        if not np.array_equal(arrays['sample_errs'],sample) or scalars['sample_best']!=float(sample.min()) or scalars['fresh_best']!=fresh:
            raise ValueError('union seeded sample mismatch')
        checked = 0
        with localcontext() as context:
            context.prec = 80
            half_log = Decimal('.5').ln()
            for n in (100, 1000):
                for K, value_at_m in zip(scalars['Ks'], arrays['best' + str(n)]):
                    m = int(round(float(value_at_m) * n))
                    if value_at_m != m / n or not 0 < m < n:
                        raise ValueError('invalid median count')
                    tail = sum(math.comb(n, k) for k in range(m + 1, n + 1))
                    previous_tail = tail + math.comb(n, m)
                    denominator = Decimal(2 ** n)
                    if not (K * (Decimal(tail) / denominator).ln() <= half_log <
                            K * (Decimal(previous_tail) / denominator).ln()):
                        raise ValueError('minimum CDF median boundary failed')
                    index=scalars['Ks'].index(K)
                    gap=float(arrays['gap'+str(n)][index])
                    j=int(round(gap*n))
                    if not 0<j<=n//2 or not math.isclose(gap,j/n,abs_tol=1e-14):
                        raise ValueError('invalid largest-gap count')
                    count=sum(math.comb(n,k) for k in range(n//2-j,n//2+j+1))
                    previous=count-math.comb(n,n//2-j)-math.comb(n,n//2+j)
                    if not (K*(Decimal(previous)/denominator).ln() < Decimal('.95').ln() <= K*(Decimal(count)/denominator).ln()):
                        raise ValueError('largest-gap quantile boundary failed')
                    bound=math.sqrt(math.log(2*K/.05)/(2*n))
                    if not math.isclose(arrays['bound'+str(n)][index],bound,rel_tol=2e-14):
                        raise ValueError('union bound mismatch')
                    checked += 1
        return {'exact_integer_Decimal_median_boundaries': checked}
    if item != 'maxmargin':
        raise ValueError('unknown corrected item')
    expected = {'X': (40,2), 't': (40,), 'w_svm': (2,), 'rec': (142,7)}
    if {k: a.shape for k, a in arrays.items()} != expected:
        raise ValueError('MaxMargin array schema mismatch')
    if set(scalars) != {'gamma','eta','T','c_lo','c_hi','angle_end','norm_end','margin_end'} or scalars['T'] != 1000000:
        raise ValueError('MaxMargin metadata schema mismatch')
    X, t, rec, svm = (arrays[k] for k in ('X','t','rec','w_svm'))
    if not np.isin(t, [-1.,1.]).all() or not np.array_equal(rec[:,0], np.unique(np.round(np.geomspace(1,1000000,160)))):
        raise ValueError('MaxMargin labels or logged steps differ')
    margin=float(((t[:,None]*X)@svm).min())
    eta=1/(.25*float(np.linalg.eigvalsh(X.T@X/len(X)).max()))
    late=rec[rec[:,0]>=1000]
    rate=late[:,1]*np.log(late[:,0])
    if margin<=0 or not math.isclose(float(np.linalg.norm(svm)),1.,rel_tol=2e-12) or not np.allclose(
            [scalars['gamma'],scalars['eta'],scalars['c_lo'],scalars['c_hi']],
            [margin,eta,float(rate.min()),float(rate.max())],rtol=2e-12,atol=2e-12):
        raise ValueError('MaxMargin SVM, step-size or rate metadata mismatch')
    residual = 0.
    for row in rec:
        w = row[5:7]
        norm = float(np.linalg.norm(w))
        if norm <= 0:
            raise ValueError('nonpositive recorded weight norm')
        expected_geometry = [math.degrees(math.acos(min(1.,float(w @ svm / norm)))),
                             norm, float(((t[:,None] * X) @ w).min() / norm)]
        if not np.allclose(row[[1,2,4]], expected_geometry, rtol=2e-12, atol=2e-12):
            raise ValueError('same-row geometry mismatch')
        losses = []
        for point, sign in zip(X, t):
            z = -float(sign) * math.fsum(float(a) * float(b) for a,b in zip(point,w))
            losses.append(max(z,0.) + math.log1p(math.exp(-abs(z))))
        loss = math.fsum(losses) / len(losses)
        residual = max(residual, abs(loss - row[3]))
        if check_losses and not math.isclose(loss, row[3], rel_tol=2e-12, abs_tol=2e-14):
            raise ValueError('loss does not match recorded post-update weights')
    if not np.allclose(rec[-1,[1,2,4]], [scalars['angle_end'],scalars['norm_end'],scalars['margin_end']], rtol=2e-12,atol=2e-12):
        raise ValueError('endpoint metadata mismatch')
    return {'scalar_postupdate_rows': len(rec) if check_losses else 0, 'maximum_absolute_loss_residual': residual}


def read_payload(json_path, npz_path):
    import numpy as np
    raw = Path(json_path).read_bytes()
    value = strict_json(raw)
    if not isinstance(value, dict):
        raise ValueError('metadata must be an object')
    with np.load(npz_path, allow_pickle=False) as archive:
        if len(set(archive.files)) != len(archive.files) or set(value) & set(archive.files):
            raise ValueError('duplicate metadata/array key')
        value.update({k: archive[k].copy() for k in archive.files})
    return value, raw


def checked_root(root):
    root = Path(root).absolute()
    if any(p.is_symlink() for p in (root, *root.parents)):
        raise ValueError('symlink destination is forbidden')
    legacy = (ROOT / '.cache/ai8').resolve()
    if root.resolve() == legacy or root.resolve().is_relative_to(legacy):
        raise ValueError('legacy scientific cache is read-only')
    return root


def reserve_bundle(root, item):
    if item not in RECIPES:
        raise ValueError('unknown corrected item')
    root = checked_root(root)
    root.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(root).free < 3 * 1024**3:
        raise ValueError('requires three GiB disk reserve')
    destination = root / item
    destination.mkdir(exist_ok=False)
    return destination


def parameters(item,mode):
    reference=({'seed':1984,'ns':[100,1000],'Ks':[1,10,100,1000,10000,100000,1000000]}
               if item=='union' else {'seed':2018,'n':40,'T':1000000})
    return reference if mode=='fresh' else {'reference_recipe_parameters':reference,
                                           'input_origin':'caller-supplied; not authenticated'}


def classification(mode):
    return ('new scientific result' if mode=='fresh' else
            'derived losses at caller-supplied recorded weights; no trajectory regeneration or historical authentication')


def validate_inputs(item,mode,inputs):
    if mode not in ('fresh','derived-weights') or (mode=='derived-weights' and item!='maxmargin'):
        raise ValueError('invalid corrected result mode')
    if not isinstance(inputs,dict) or set(inputs)!=(set() if mode=='fresh' else {'maxmargin.json','maxmargin.npz'}):
        raise ValueError('input identity schema mismatch')
    for value in inputs.values():
        if (not isinstance(value,dict) or set(value)!={'bytes','sha256'} or
                type(value['bytes']) is not int or value['bytes']<=0 or
                not isinstance(value['sha256'],str) or len(value['sha256'])!=64 or
                any(c not in '0123456789abcdef' for c in value['sha256'])):
            raise ValueError('invalid input identity')


def write_bundle(destination, item, mode, value, inputs, sources, runtime, elapsed, raw_json=None):
    import numpy as np
    destination = checked_root(destination)
    if destination.is_symlink() or not destination.is_dir() or any(destination.iterdir()):
        raise ValueError('bundle must be an exclusively reserved empty directory')
    validate_inputs(item,mode,inputs)
    if sources!=source_identity()[0] or runtime!=runtime_identity() or not math.isfinite(elapsed) or elapsed<0:
        raise ValueError('source/runtime/timing identity mismatch')
    checks = validate_result(item, value)
    arrays = {k:v for k,v in value.items() if isinstance(v,np.ndarray)}
    scalars = {k:v for k,v in value.items() if k not in arrays}
    data = json.dumps(scalars, ensure_ascii=False, indent=1, allow_nan=False).encode() if raw_json is None else raw_json
    if strict_json(data) != scalars:
        raise ValueError('preserved JSON does not match result metadata')
    with (destination / 'data.npz').open('xb') as handle:
        np.savez_compressed(handle, **arrays)
    with (destination / 'data.json').open('xb') as handle:
        handle.write(data)
    receipt = {'schema':1, 'recipe':RECIPES[item], 'item':item, 'mode':mode,
               'classification':classification(mode),
               'sources':sources, 'runtime':runtime, 'inputs':inputs,
               'parameters':parameters(item,mode),
               'elapsed_numerical_seconds':elapsed, 'validation':checks,
               'outputs':{name:identity(destination/name) for name in ['data.json','data.npz']}}
    with (destination / 'receipt.json').open('x') as handle:
        json.dump(receipt,handle,indent=2,allow_nan=False)
    return receipt


def load_bundle(root, item, expected_mode=None):
    """Validate a complete bundle, never create or upgrade it."""
    if item not in RECIPES:
        raise ValueError('unknown corrected item')
    destination = checked_root(root) / item
    names = {'data.json','data.npz','receipt.json'}
    existing={p.name for p in destination.iterdir()} if destination.is_dir() else set()
    if not destination.is_dir() or destination.is_symlink() or not names<=existing or existing-names-{'data.json.lock','receipt.json.lock'}:
        raise ValueError('missing or incomplete corrected bundle: run the explicit versioned recipe')
    if any((destination/n).is_symlink() or not (destination/n).is_file() for n in names):
        raise ValueError('corrected bundle files must be regular files')
    for name in ('data.json.lock','receipt.json.lock'):
        lock=destination/name
        if lock.is_symlink() or (lock.exists() and (not lock.is_file() or lock.stat().st_size!=0)):
            raise ValueError('unexpected cache coordination file')
    receipt = strict_json((destination/'receipt.json').read_bytes())
    if not isinstance(receipt,dict) or set(receipt)!={'schema','recipe','item','mode','classification','sources','runtime','inputs','parameters','elapsed_numerical_seconds','validation','outputs'}:
        raise ValueError('corrected receipt schema mismatch')
    sources,_ = source_identity()
    if receipt.get('schema')!=1 or receipt.get('item')!=item or receipt.get('recipe')!=RECIPES[item] or receipt.get('sources')!=sources or receipt.get('runtime')!=runtime_identity():
        raise ValueError('corrected recipe/source/runtime identity mismatch')
    mode=receipt.get('mode')
    if mode not in ('fresh','derived-weights') or (item=='union' and mode!='fresh') or (expected_mode is not None and mode!=expected_mode):
        raise ValueError('corrected result mode mismatch')
    validate_inputs(item,mode,receipt['inputs'])
    if receipt['classification']!=classification(mode) or receipt['parameters']!=parameters(item,mode) or not isinstance(receipt['elapsed_numerical_seconds'],(int,float)) or not math.isfinite(receipt['elapsed_numerical_seconds']) or receipt['elapsed_numerical_seconds']<0:
        raise ValueError('corrected provenance metadata mismatch')
    if receipt.get('outputs')!={n:identity(destination/n) for n in ['data.json','data.npz']}:
        raise ValueError('corrected output identity mismatch')
    value,_=read_payload(destination/'data.json',destination/'data.npz')
    if receipt['validation']!=validate_result(item,value):
        raise ValueError('corrected validation contract mismatch')
    return value,receipt


def load_for_scene(item,cache_type=None):
    """Fresh versioned bundles only; use the shared cache hook for QA input recording.

    Bundle validation precedes any cache access. The only permitted write is the
    shared cache's empty coordination lock. Missing data can never start a producer.
    """
    value,receipt=load_bundle(DEFAULT_ROOT,item,expected_mode='fresh')
    receipt_before=identity(DEFAULT_ROOT/item/'receipt.json')
    if cache_type is None:
        from explainer.ai.cache import Cache
        cache_type=Cache
    def absent():
        raise FileNotFoundError('corrected data disappeared; automatic generation is forbidden')
    cache=cache_type('ai8-corrected-v1')
    cache.dir=DEFAULT_ROOT/item
    cache.items={'data':absent,'receipt':absent}
    recorded_receipt=cache.load('receipt')
    if recorded_receipt!=receipt:
        raise ValueError('loaded corrected receipt identity mismatch')
    loaded=cache.load('data')
    current,current_receipt=load_bundle(DEFAULT_ROOT,item,expected_mode='fresh')
    if current_receipt!=receipt or identity(DEFAULT_ROOT/item/'receipt.json')!=receipt_before or set(loaded)!=set(current):
        raise ValueError('corrected bundle changed during load')
    import numpy as np
    for key,expected in current.items():
        actual=loaded[key]
        if isinstance(expected,np.ndarray):
            if not isinstance(actual,np.ndarray) or actual.dtype!=expected.dtype or actual.shape!=expected.shape or actual.tobytes()!=expected.tobytes():
                raise ValueError('loaded corrected array identity mismatch')
        elif actual!=expected:
            raise ValueError('loaded corrected metadata mismatch')
    return loaded


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--item',choices=tuple(RECIPES),required=True)
    parser.add_argument('--mode',choices=('fresh','derived-weights'),required=True)
    parser.add_argument('--input-dir',type=Path)
    parser.add_argument('--output-root',type=Path,default=DEFAULT_ROOT)
    args=parser.parse_args(argv)
    if (args.mode=='derived-weights') != (args.input_dir is not None) or (args.mode=='derived-weights' and args.item!='maxmargin'):
        parser.error('derived-weights is MaxMargin-only and requires --input-dir; fresh accepts no input directory')
    for key in THREAD_KEYS: os.environ[key]='1'
    sources,_=source_identity()
    runtime=runtime_identity()
    destination=reserve_bundle(args.output_root,args.item)
    # Reservation remains on failure; an uncertain/partial run is never retried automatically.
    start=time.perf_counter()
    raw=None
    inputs={}
    if args.mode=='fresh':
        value=fresh_result(args.item)
    else:
        jp,npz=args.input_dir/'maxmargin.json',args.input_dir/'maxmargin.npz'
        inputs={p.name:identity(p) for p in [jp,npz]}
        old,raw=read_payload(jp,npz)
        validate_result('maxmargin',old,check_losses=False)
        value=correct_postupdate_losses(old)
        import numpy as numeric
        if any(not numeric.array_equal(old[k],value[k],equal_nan=True) for k in ('X','t','w_svm')) or not numeric.array_equal(old['rec'][:,[0,1,2,4,5,6]],value['rec'][:,[0,1,2,4,5,6]]):
            raise ValueError('derivation modified non-loss values')
        if inputs!={p.name:identity(p) for p in [jp,npz]}:
            raise ValueError('derived input changed during computation')
    elapsed=time.perf_counter()-start
    if source_identity()[0]!=sources or runtime_identity()!=runtime:
        raise ValueError('source/runtime changed during computation')
    receipt=write_bundle(destination,args.item,args.mode,value,inputs,sources,runtime,elapsed,raw)
    load_bundle(args.output_root,args.item,args.mode)
    print(json.dumps({'item':args.item,'recipe':receipt['recipe'],'mode':args.mode,
                      'elapsed_numerical_seconds':elapsed,'outputs':receipt['outputs'],'validation':receipt['validation']},indent=2))
    return 0


if __name__=='__main__':
    sys.exit(main())
