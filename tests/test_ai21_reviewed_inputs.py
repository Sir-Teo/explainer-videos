"""Synthetic read-only input contracts; no private manifests, data, models or renders."""
import ast
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pytest

PART = Path(__file__).resolve().parents[1] / 'videos/ai/ai21'


def digest(data):
    return hashlib.sha256(data).hexdigest()


@pytest.fixture
def reviewed(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location('ai21_reviewed_inputs_test', PART / 'reviewed_inputs.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, '_ROOT', tmp_path)
    monkeypatch.delenv('AI21_QUICK', raising=False)
    sources = {}
    for name in module._SOURCES:
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('# synthetic source fixture\n')
        sources[name] = digest(p.read_bytes())
    cache = tmp_path / '.cache/ai21'
    cache.mkdir(parents=True)
    manifest = dict(schema_version=1, part='ai21', compatibility_sources=sources, products={}, upstream={})
    def write_manifest():
        (cache / 'render-manifest.json').write_text(json.dumps(manifest))
    def product(name='forward', arrays=None, recipe='original-recipe', data=None):
        p = cache / f'{name}.json'
        p.write_text(json.dumps({'value': 2} if data is None else data))
        entry = dict(json={'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())}, npz=None,
                     review=dict(accepted=True, recipe=recipe, producer_sha256='1' * 64,
                                 input_sha256={'synthetic': '2' * 64}))
        if arrays is not None:
            p = cache / f'{name}.npz'
            np.savez(p, **arrays)
            entry['npz'] = dict(bytes=p.stat().st_size, sha256=digest(p.read_bytes()),
                                arrays={k: dict(dtype=str(v.dtype), shape=list(v.shape)) for k, v in arrays.items()})
        manifest['products'][name] = entry
        write_manifest()
        return entry
    return module, tmp_path, cache, manifest, write_manifest, product


def snapshot(root):
    return {str(p.relative_to(root)): digest(p.read_bytes()) for p in root.rglob('*') if p.is_file()}


def test_missing_manifest_does_not_create_cache_or_import_producers(reviewed):
    m, root, _, _, _, _ = reviewed
    before = snapshot(root)
    producers = {k for k in sys.modules if k.startswith('videos.ai.ai21.')}
    with pytest.raises(m.ReviewedInputError, match='Cannot read reviewed input'):
        m.load('forward')
    assert snapshot(root) == before
    assert {k for k in sys.modules if k.startswith('videos.ai.ai21.')} == producers


def test_reviewed_arrays_and_json_are_read_without_writes_and_are_rechecked(reviewed):
    m, root, cache, _, _, product = reviewed
    product(arrays={'x': np.array([[1., 2.]])})
    before = snapshot(root)
    result = m.load('forward')
    assert result['value'] == 2
    np.testing.assert_array_equal(result['x'], [[1., 2.]])
    assert snapshot(root) == before
    (cache / 'forward.json').write_text('{"value":3}')
    with pytest.raises(m.ReviewedInputError):
        m.load('forward')


@pytest.mark.parametrize('change', ['unaccepted', 'missing_provenance', 'wrong_source', 'undeclared_npz',
                                   'wrong_shape', 'wrong_dtype', 'nonfinite', 'object_array', 'collision'])
def test_invalid_review_or_payload_fails_closed(reviewed, change):
    m, root, _, manifest, write, product = reviewed
    array = np.array([[1., 2.]])
    if change == 'nonfinite': array[0, 0] = np.nan
    if change == 'object_array': array = np.array([object()], dtype=object)
    entry = product(arrays={'x': array}, data={'x': 0} if change == 'collision' else None)
    if change == 'unaccepted': entry['review']['accepted'] = False
    if change == 'missing_provenance': entry['review']['input_sha256'] = {}
    if change == 'wrong_source':
        next(iter(manifest['compatibility_sources']))
        (root / next(iter(manifest['compatibility_sources']))).write_text('# changed\n')
    if change == 'undeclared_npz': entry['npz'] = None
    if change == 'wrong_shape': entry['npz']['arrays']['x']['shape'] = [2, 1]
    if change == 'wrong_dtype': entry['npz']['arrays']['x']['dtype'] = 'int64'
    write()
    before = snapshot(root)
    with pytest.raises(m.ReviewedInputError): m.load('forward')
    assert snapshot(root) == before


@pytest.mark.parametrize('name', ['solvers', 'solvers_net'])
def test_legacy_solver_acceptance_cannot_satisfy_corrected_initialization_contract(reviewed, name):
    m, _, _, _, write, product = reviewed
    entry = product(name=name)
    with pytest.raises(m.ReviewedInputError, match='euler-common-start-v1'): m.load(name)
    entry['review']['recipe'] = 'euler-common-start-v1'
    write()
    assert m.load(name)['value'] == 2  # schema acceptance only; not numerical verification


def test_upstream_json_is_reviewed_without_compute_imports_or_writes(reviewed):
    m, root, _, manifest, write, _ = reviewed
    p = root / '.cache/ai13/tf.json'
    p.parent.mkdir(parents=True)
    p.write_text('{"ctx":256}')
    manifest['upstream']['tf'] = dict(json={'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())},
                                    review=dict(accepted=True, recipe='historical-original',
                                                producer_sha256='1'*64, input_sha256={'synthetic':'2'*64}))
    write()
    before = snapshot(root)
    assert m.load_upstream('tf') == {'ctx': 256}
    assert snapshot(root) == before
    with pytest.raises(m.ReviewedInputError): m.load_upstream('scoreboard')


def test_missing_file_symlink_and_quick_inputs_fail_closed(reviewed, monkeypatch):
    m, _, cache, _, _, product = reviewed
    product()
    p = cache / 'forward.json'
    data = p.read_bytes()
    p.unlink()
    with pytest.raises(m.ReviewedInputError): m.load('forward')
    other = cache / 'other.json'
    other.write_bytes(data)
    p.symlink_to(other)
    with pytest.raises(m.ReviewedInputError): m.load('forward')
    monkeypatch.setenv('AI21_QUICK', '1')
    with pytest.raises(m.ReviewedInputError, match='Quick fixtures'): m.load('forward')
    with pytest.raises(m.ReviewedInputError): m.load('../forward')


def test_chinese_requires_entrywise_composition_without_overlay_or_writes(reviewed):
    m, root, _, _, _, _ = reviewed
    delta = json.loads((PART / 'text_zh_reviewed.json').read_text())
    local = root / 'videos/ai/ai21/text_zh_reviewed.json'
    local.write_text(json.dumps(delta))
    shared = root / 'videos/ai/ai_text_zh.json'
    table = dict(strings={'unrelated': '保留'}, phrases={}, patterns=[])
    shared.write_text(json.dumps(table))
    before = snapshot(root)
    m.validate_captions('en')
    with pytest.raises(m.ReviewedInputError, match='Compose'): m.validate_captions('zh')
    assert snapshot(root) == before
    table['strings'].update(delta['strings'])
    table['phrases'].update(delta['phrases'])
    table['patterns'].extend(delta['patterns'])
    shared.write_text(json.dumps(table))
    before = snapshot(root)
    m.validate_captions('zh')
    assert snapshot(root) == before
    table['patterns'].append([delta['patterns'][0][0], 'conflicting replacement'])
    shared.write_text(json.dumps(table))
    with pytest.raises(m.ReviewedInputError, match='pattern'): m.validate_captions('zh')


def test_scenes_do_not_import_compute_or_cache_fallbacks():
    paths = [PART / 'common.py', *PART.glob('s[0-9][0-9]_*.py')]
    for path in paths:
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.ImportFrom):
                assert not any(a.name in {'compute', 'Cache'} for a in node.names), path
                assert not (node.module or '').endswith('.compute'), path
            if isinstance(node, ast.Import):
                assert not any(a.name.endswith('.compute') for a in node.names), path
    common = (PART / 'common.py').read_text()
    assert 'validate_captions(_caption_language.LANG)' in common
