"""Run the real translation CLI against an isolated temporary repository root."""
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'tools' / 'text_zh_add.py'


class TranslationMergeTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.script = self.root / 'tools/text_zh_add.py'
        self.script.parent.mkdir()
        shutil.copyfile(SCRIPT, self.script)
        self.table = self.root / 'videos/ai/ai_text_zh.json'
        self.table.parent.mkdir(parents=True)
        self.original = '{ "strings": {"existing": "原文"}, "patterns": [["old", "旧"]] }\n'
        self.table.write_text(self.original)
        self.serial = 0

    def source(self, value):
        self.serial += 1
        path = self.root / f'input-{self.serial}.json'
        path.write_text(json.dumps(value, ensure_ascii=False))
        return path

    def command(self, path):
        return [sys.executable, str(self.script), 'ai', str(path)]

    def run_cli(self, value):
        return subprocess.run(self.command(self.source(value)), capture_output=True, text=True)

    def test_metadata_handoff_is_rejected_without_any_output_mutation(self):
        result = self.run_cli(dict(owner='reviewer', source_frozen_utc='now',
                                   proposed_translations={'New': '新'}, notes=['handoff']))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('invalid translation input', result.stderr)
        self.assertIn('proposed_translations', result.stderr)
        self.assertEqual(self.table.read_text(), self.original)
        self.assertFalse(self.table.with_suffix('.lock').exists())
        self.assertFalse(self.table.with_suffix('.tmp').exists())

    def test_malformed_shapes_rejected_before_writing(self):
        cases = [[], None, 'text', 1, {'English': []}, {'English': None},
                 {'strings': []}, {'strings': {'English': {'nested': '值'}}},
                 {'strings': {'English': 1}}, {'strings': {}, 'notes': 'metadata'},
                 {'strings': {}, 'patterns': {}}, {'strings': {}, 'patterns': [None]},
                 {'strings': {}, 'patterns': [['regex']]},
                 {'strings': {}, 'patterns': [['regex', 2]]}]
        for value in cases:
            with self.subTest(value=value):
                result = self.run_cli(value)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('invalid translation input', result.stderr)
                self.assertEqual(self.table.read_text(), self.original)
                self.assertFalse(self.table.with_suffix('.lock').exists())
                self.assertFalse(self.table.with_suffix('.tmp').exists())

    def test_invalid_json_is_rejected_without_writing(self):
        source = self.root / 'broken.json'; source.write_text('{"strings":')
        result = subprocess.run(self.command(source), capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('invalid translation input', result.stderr)
        self.assertEqual(self.table.read_text(), self.original)
        self.assertFalse(self.table.with_suffix('.lock').exists())

    def test_nonstring_keys_are_rejected_by_same_validator(self):
        # JSON object syntax itself only supports string keys; exercise Python
        # callers of the exact CLI validator for the otherwise-unrepresentable case.
        validate = runpy.run_path(str(SCRIPT))['validate_input']
        for value in ({1: '中'}, {'strings': {1: '中'}}):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'string'):
                validate(value)
        self.assertEqual(self.table.read_text(), self.original)

    def test_valid_bare_mapping_keeps_conflicts_and_allows_literal_field_words(self):
        result = self.run_cli({'New': '新', 'existing': '不覆盖', 'strings': '字符串', 'patterns': '模式'})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('kept existing', result.stdout)
        table = json.loads(self.table.read_text())
        self.assertEqual(table['strings'], {'existing': '原文', 'New': '新', 'strings': '字符串', 'patterns': '模式'})
        self.assertEqual(table['patterns'], [['old', '旧']])
        self.assertIn('3 added', result.stdout)

    def test_valid_wrapped_mapping_and_patterns_preserve_existing(self):
        result = self.run_cli({'strings': {'New': '新', 'existing': '不覆盖'},
                               'patterns': [['old', '不覆盖'], ['new-(.*)', '新-\\1']]})
        self.assertEqual(result.returncode, 0, result.stderr)
        table = json.loads(self.table.read_text())
        self.assertEqual(table['strings'], {'existing': '原文', 'New': '新'})
        self.assertEqual(table['patterns'], [['old', '旧'], ['new-(.*)', '新-\\1']])
        self.assertIn('2 added', result.stdout)

    def test_concurrent_actual_cli_merges_preserve_both_additions(self):
        first = self.source({'first': '一'})
        second = self.source({'strings': {'second': '二'}, 'patterns': [['new', '新']]})
        jobs = [subprocess.Popen(self.command(source), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                for source in (first, second)]
        for job in jobs:
            stdout, stderr = job.communicate(timeout=15)
            self.assertEqual(job.returncode, 0, stdout + stderr)
        table = json.loads(self.table.read_text())
        self.assertEqual(table['strings'], {'existing': '原文', 'first': '一', 'second': '二'})
        self.assertEqual(table['patterns'], [['old', '旧'], ['new', '新']])


if __name__ == '__main__':
    unittest.main()
