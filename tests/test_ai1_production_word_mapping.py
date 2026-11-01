"""Production display-word remapping; preserved metadata only, no audio/model I/O."""
import ast
from dataclasses import dataclass
import difflib
from functools import lru_cache
import gzip
import hashlib
import json
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

from explainer import lang

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/qa/evidence/v9-production-word-mapping-reconciliation'
RECEIPT = json.loads((EVIDENCE / 'production-receipt.json').read_text())


def diagnostic(prefix=False):
    path = ('ai1-entropy-prefix-narrated-timing-repair/prefix-exact-diagnostic.json.gz'
            if prefix else 'ai1-crossentropy-narrated-timing-repair/exact-diagnostic.json.gz')
    return json.loads(gzip.decompress((ROOT / 'docs/qa/evidence' / path).read_bytes()))


@lru_cache(maxsize=1)
def production_api():
    """Execute the actual Word/align_words/Tracker functions, without importing TTS backends."""
    tts = ast.parse((ROOT / 'explainer/tts.py').read_text())
    voice = ast.parse((ROOT / 'explainer/voiceover.py').read_text())
    nodes = [ast.ImportFrom(module='__future__', names=[ast.alias(name='annotations')], level=0)]
    nodes += [n for n in tts.body if isinstance(n, (ast.ClassDef, ast.FunctionDef))
              and n.name in ('Word', 'align_words')]
    nodes += [n for n in voice.body if isinstance(n, (ast.ClassDef, ast.FunctionDef))
              and n.name in ('_strip_bookmarks', 'VoiceoverTracker')]
    scope = dict(__name__=__name__, dataclass=dataclass, difflib=difflib, re=re,
                 lang=lang, _norm=lang.norm, _BOOKMARK=lang.BOOKMARK)
    exec(compile(ast.fix_missing_locations(ast.Module(nodes, type_ignores=[])),
                 'actual-production-word-mapping', 'exec'), scope)
    return scope


def tracker(raw, aligned):
    api = production_api()
    text, marks = api['_strip_bookmarks'](raw)
    assert text == aligned['text']
    words = api['align_words'](text, aligned['tokens'], aligned['duration'])
    scene = SimpleNamespace(renderer=SimpleNamespace(time=0.))
    voice = api['VoiceoverTracker'](scene, SimpleNamespace(words=words, duration=aligned['duration']), marks, 0.)
    return voice, words


class ProductionWordMapping(unittest.TestCase):
    def setUp(self):
        self.old_language = lang.LANG
        lang.LANG = 'en'
        self.addCleanup(setattr, lang, 'LANG', self.old_language)

    def test_exact_production_receipt_and_source_functions(self):
        raw = (EVIDENCE / 'production-receipt.json').read_bytes()
        self.assertEqual((len(raw), hashlib.sha256(raw).hexdigest()),
                         (14539, '57793eeddae6188ee631687dd18d606a7333fb210432cea2d1b085c05c4ce5f5'))
        self.assertEqual(RECEIPT['source_gate'], '810fe991600f98b2c14f3dcc4a501c329fb4e3af')
        release = ROOT / 'docs/qa/evidence/production-handoff-parts1-3/manifest-prefix-crossentropy-arithmetic-part3-v9.json'
        self.assertEqual(hashlib.sha256(release.read_bytes()).hexdigest(), RECEIPT['release_manifest_sha256'])
        for item in RECEIPT['actual_source_function_files']:
            self.assertEqual(hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest(), item['sha256'])
        tree = ast.parse((ROOT / 'explainer/tts.py').read_text())
        norm = next(n.value for n in tree.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == '_norm' for t in n.targets))
        self.assertEqual(ast.unparse(norm), 'lang.norm')
        self.assertTrue(RECEIPT['all30speech_files_hash_size_mtime_unchanged'])
        self.assertFalse(RECEIPT['final_acceptance'])

    def test_all_22_targets_match_after_actual_display_word_mapping(self):
        d = diagnostic()
        expected = RECEIPT['all22CrossEntropy_prior_actual_targets_reproduced']
        self.assertEqual(len(expected), 22)
        for row in expected:
            block = d['narration_blocks'][row['block_index']]
            aligned = d['per_utterance_word_alignment_and_duration'][row['utterance_key']]
            voice, words = tracker(block['raw'], aligned)
            self.assertEqual(voice.marks[row['mark']], row['display_index'])
            self.assertEqual(words[row['display_index']].text, row['word'])
            target = voice.mark_time(row['mark'])
            self.assertAlmostEqual(target, row['relative_target_seconds'], places=10)
            self.assertAlmostEqual(block['start'] + target, row['original_actual_runtime_target_seconds'], places=10)
        aligned = d['per_utterance_word_alignment_and_duration']['0c35b58d8418e05b']
        voice, words = tracker(d['narration_blocks'][3]['raw'], aligned)
        self.assertEqual((len(aligned['tokens']), len(words)), (73, 72))
        self.assertEqual(words[33].text, 'Kullback–Leibler')
        self.assertAlmostEqual(words[33].start, 11.86)
        self.assertAlmostEqual(words[33].end, 12.82)
        self.assertEqual((words[41].text, voice.mark_time('c')), ('Swapping', 15.97))
        # The historical raw-index test remains an intentional counterfactual.
        self.assertEqual(aligned['tokens'][41][0], '1951')
        self.assertAlmostEqual(aligned['tokens'][41][1], 14.50)

    def test_prefix_current_owner_master_and_alignment_match_historical_proof(self):
        current = RECEIPT['Prefix']
        self.assertEqual((current['key'], current['master_bytes'], current['master_sha256']),
                         ('86a8352c7e3815ea', 1189520,
                          '099dffe6f458b46652cecea65727f19d16191a1e99107085fb158b546834488f'))
        d = diagnostic(prefix=True)
        aligned = d['per_utterance_word_alignment_and_duration'][current['key']]
        self.assertEqual(len(current['raw_tokens']), len(aligned['tokens']))
        for new, old in zip(current['raw_tokens'], aligned['tokens']):
            self.assertEqual(lang.norm(new[0]), lang.norm(old[0]))
            self.assertAlmostEqual(new[1], old[1], places=10)
            self.assertAlmostEqual(new[2], old[2], places=10)
        source = ROOT / 'videos/ai/ai1/s05_prefix.py'
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), current['v9_source_sha256'])
        fn = next(n for n in ast.walk(ast.parse(source.read_text()))
                  if isinstance(n, ast.FunctionDef) and n.name == 'prefix')
        raw = next(ast.literal_eval(n.args[0]) for n in ast.walk(fn)
                   if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                   and n.func.attr == 'voiceover' and isinstance(n.args[0], ast.Constant)
                   and n.args[0].value.startswith('Watch it decode.'))
        voice, words = tracker(raw, aligned)
        self.assertEqual(len(words), 23)
        self.assertEqual(list(voice.marks), [x['mark'] for x in current['v9_bookmark_alignment']])
        for item in current['v9_bookmark_alignment']:
            self.assertEqual(voice.marks[item['mark']], item['display_index'])
            self.assertEqual(words[item['display_index']].text, item['word'])
            self.assertAlmostEqual(voice.mark_time(item['mark']), item['relative_start_seconds'], places=10)


if __name__ == '__main__':
    unittest.main()
