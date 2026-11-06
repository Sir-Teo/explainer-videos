"""A QA child must select its language/backend before importing the toolkit."""

import os
from pathlib import Path
import subprocess
import sys


def test_worker_selects_chinese_and_silent_without_inheriting_parent_defaults():
    # An invalid scene exercises worker startup without data, TeX, or speech.
    # In particular, importing the runner must not freeze English/Kokoro first.
    code = """
import tempfile
from pathlib import Path
from types import SimpleNamespace
from tools import qa_series

with tempfile.TemporaryDirectory() as directory:
    qa_series.OUT = Path(directory)
    status = qa_series.worker(SimpleNamespace(
        video='quant1', worker='NonexistentScene', lang='zh',
        motion=False, cached_only=True,
    ))
    assert status == 1

from explainer import lang, tts, zh_text
assert lang.LANG == 'zh', lang.LANG
assert tts.BACKEND == 'silent', tts.BACKEND
assert zh_text.COLLECT, 'QA must also initialize text collection before imports'
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=Path(__file__).resolve().parents[1],
        env=dict(os.environ, EXPLAINER_LANG="en", EXPLAINER_TTS="kokoro", EXPLAINER_COLLECT_TEXT=""),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
