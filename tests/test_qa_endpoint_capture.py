"""The actual worker wrapper must capture after voiceover exit settles narration."""
import ast
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest


def _actual_wrapper(original_vo, captures, active):
    tree = ast.parse((Path(__file__).resolve().parents[1] / 'tools/qa_series.py').read_text())
    worker = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'worker')
    node = next(n for n in worker.body if isinstance(n, ast.FunctionDef) and n.name == 'voiceover')
    namespace = {'contextmanager': contextmanager, 'original_vo': original_vo,
                 'active': active, 'capture': lambda scene, reason: captures.append((scene.phase, reason))}
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<actual QA wrapper>', 'exec'), namespace)
    return namespace['voiceover']


def test_endpoint_capture_follows_narration_padding():
    @contextmanager
    def original(scene, text):
        yield 'tracker'
        # Models the actual context exit advancing remaining speech and padding.
        scene.phase = 'settled after narration padding'

    scene = SimpleNamespace(phase='early body')
    captures, active = [], []
    voiceover = _actual_wrapper(original, captures, active)
    with voiceover(scene, 'spoken text') as tracker:
        assert tracker == 'tracker' and active == ['spoken text']
    assert captures == [('settled after narration padding', 'narration-end')]
    assert active == []


def test_failed_voiceover_body_does_not_approve_an_endpoint():
    @contextmanager
    def original(scene, text):
        yield 'tracker'
        scene.phase = 'settled'

    scene = SimpleNamespace(phase='early body')
    captures, active = [], []
    voiceover = _actual_wrapper(original, captures, active)
    with pytest.raises(ValueError, match='body failed'):
        with voiceover(scene, 'spoken text'):
            raise ValueError('body failed')
    assert captures == [] and active == []
