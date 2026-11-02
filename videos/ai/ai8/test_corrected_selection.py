"""Portable selection/preflight tests; no project, scene or producer imports."""
from __future__ import annotations

import ast
from contextlib import contextmanager, redirect_stderr
import copy
from functools import lru_cache
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest import mock

PART = Path(__file__).resolve().parent
RECIPE = 'EXPLAINER_AI8_RECIPE'


@lru_cache(maxsize=1)
def wrapper():
    module = ModuleType('ai8_selection_wrapper_tests')
    module.__file__ = str(PART / 'qa_cached.py')
    tree = ast.parse(Path(module.__file__).read_text())
    exec(compile(tree, module.__file__, 'exec'), module.__dict__)
    return module


@contextmanager
def isolated_common(recipe=None):
    """Compile only common.load and satisfy its relative import with a fake."""
    tree = ast.parse((PART / 'common.py').read_text())
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'load')
    package = ModuleType('synthetic_ai8_selection')
    package.__path__ = []
    corrected = ModuleType('synthetic_ai8_selection.corrected_v1')
    corrected.load_for_scene = mock.Mock(return_value=object())
    legacy = mock.Mock(return_value=object())
    namespace = {'__name__': 'synthetic_ai8_selection.common', '__package__': package.__name__,
                 'os': os, '_legacy_load': legacy}
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<isolated-common-load>', 'exec'), namespace)
    with mock.patch.dict(sys.modules, {package.__name__: package, corrected.__name__: corrected}), \
         mock.patch.dict(os.environ, {}, clear=False):
        if recipe is None:
            os.environ.pop(RECIPE, None)
        else:
            os.environ[RECIPE] = recipe
        yield namespace['load'], legacy, corrected.load_for_scene


def fake_bundles(qa, *, error=None, observer=None):
    root = Path('synthetic-corrected-bundles')
    receipts = {'union': {'item': 'union', 'mode': 'fresh', 'identity': 'synthetic-union'},
                'maxmargin': {'item': 'maxmargin', 'mode': 'fresh', 'identity': 'synthetic-maxmargin'}}

    def load(path, item, *, expected_mode):
        if path != root or expected_mode != 'fresh':
            raise AssertionError('preflight did not require the intended fresh namespace')
        if any(os.environ.get(key) != '1' for key in qa.THREAD_KEYS):
            raise AssertionError('preflight did not set all six thread guards')
        if observer:
            observer(item)
        if error:
            raise error
        return {}, copy.deepcopy(receipts[item])

    return SimpleNamespace(DEFAULT_ROOT=root, load_bundle=mock.Mock(side_effect=load))


class CommonSelection(unittest.TestCase):
    def test_corrected_results_are_default_for_both_affected_items(self):
        for recipe in (None, 'corrected-v1'):
            for item in ('union', 'maxmargin'):
                with self.subTest(recipe=recipe, item=item), isolated_common(recipe) as (load, legacy, corrected):
                    self.assertIs(load(item), corrected.return_value)
                    corrected.assert_called_once_with(item)
                    legacy.assert_not_called()

    def test_only_explicit_legacy_selection_replays_affected_legacy_items(self):
        for item in ('union', 'maxmargin'):
            with self.subTest(item=item), isolated_common('legacy') as (load, legacy, corrected):
                self.assertIs(load(item), legacy.return_value)
                legacy.assert_called_once_with(item)
                corrected.assert_not_called()

    def test_unaffected_items_delegate_without_loading_unrelated_bundles(self):
        for recipe, item in ((recipe, item) for recipe in (None, 'legacy', 'corrected-v1')
                             for item in ('risk', 'biasvar', 'canary')):
            with self.subTest(recipe=recipe, item=item), isolated_common(recipe) as (load, legacy, corrected):
                self.assertIs(load(item), legacy.return_value)
                legacy.assert_called_once_with(item)
                corrected.assert_not_called()

    def test_unknown_selection_rejects_even_unaffected_items_before_any_load(self):
        for recipe in ('', 'automatic', 'CORRECTED-V1'):
            for item in ('union', 'maxmargin', 'risk'):
                with self.subTest(recipe=recipe, item=item), isolated_common(recipe) as (load, legacy, corrected):
                    with self.assertRaises(ValueError): load(item)
                    legacy.assert_not_called(); corrected.assert_not_called()

    def test_corrected_failures_propagate_without_legacy_fallback(self):
        failures = (FileNotFoundError('synthetic missing bundle'), ValueError('synthetic hash mismatch'),
                    ValueError('synthetic wrong mode'))
        for failure in failures:
            for item in ('union', 'maxmargin'):
                with self.subTest(failure=str(failure), item=item), isolated_common() as (load, legacy, corrected):
                    corrected.side_effect = failure
                    with self.assertRaises(type(failure)) as raised: load(item)
                    self.assertIs(raised.exception, failure)
                    legacy.assert_not_called()


class CorrectedPreflight(unittest.TestCase):
    def test_wrapper_top_level_imports_are_standard_library_only(self):
        tree = ast.parse((PART / 'qa_cached.py').read_text())
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module]
                for name in names: self.assertIn(name.split('.')[0], sys.stdlib_module_names)

    def test_only_selected_fresh_items_are_checked_and_duplicates_are_removed(self):
        qa = wrapper()
        self.assertEqual(set(qa.THREAD_KEYS), {'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                                              'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'})
        fake = fake_bundles(qa)
        result = qa.preflight_corrected(['Hoeffding', 'MaxMargin', 'Hoeffding', 'Outro', 'Risk'], module=fake)
        self.assertEqual(set(result), {'union', 'maxmargin'})
        self.assertEqual(fake.load_bundle.call_args_list,
                         [mock.call(fake.DEFAULT_ROOT, item, expected_mode='fresh') for item in ('maxmargin', 'union')])

    def test_Outro_is_a_control_and_never_imports_or_reads_unrelated_bundles(self):
        qa = wrapper()
        fake = SimpleNamespace(load_bundle=mock.Mock(side_effect=AssertionError('unrelated bundle read')))
        with mock.patch.object(qa.importlib.util, 'spec_from_file_location',
                               side_effect=AssertionError('unrelated corrected module import')):
            self.assertEqual(qa.preflight_corrected(['Outro', 'Risk']), {})
            self.assertEqual(qa.preflight_corrected(['Outro'], module=fake), {})
        fake.load_bundle.assert_not_called()

    def test_all_thread_values_are_temporarily_one_and_restored_on_success_or_failure(self):
        qa = wrapper()
        failures = (None, FileNotFoundError('missing'), ValueError('tampered'))
        for failure in failures:
            with self.subTest(failure=str(failure)), mock.patch.dict(os.environ, {}, clear=False):
                for key in qa.THREAD_KEYS: os.environ.pop(key, None)
                os.environ[qa.THREAD_KEYS[0]] = '8'
                os.environ[qa.THREAD_KEYS[2]] = ''
                os.environ[qa.THREAD_KEYS[4]] = '3'
                before = dict(os.environ)
                fake = fake_bundles(qa, error=failure)
                if failure:
                    with self.assertRaises(type(failure)) as raised:
                        qa.preflight_corrected(['Hoeffding'], module=fake)
                    self.assertIs(raised.exception, failure)
                else:
                    self.assertIn('union', qa.preflight_corrected(['Hoeffding'], module=fake))
                self.assertEqual(dict(os.environ), before)

    def test_thread_environment_is_restored_if_module_loading_raises(self):
        qa = wrapper()
        error = RuntimeError('synthetic module loading failure')
        loader = SimpleNamespace(exec_module=mock.Mock(side_effect=error))
        spec = SimpleNamespace(loader=loader)
        with mock.patch.dict(os.environ, {}, clear=False), \
             mock.patch.object(qa.importlib.util, 'spec_from_file_location', return_value=spec), \
             mock.patch.object(qa.importlib.util, 'module_from_spec', return_value=SimpleNamespace()):
            before = dict(os.environ)
            with self.assertRaises(RuntimeError) as raised: qa.preflight_corrected(['Hoeffding'])
            self.assertIs(raised.exception, error)
            self.assertEqual(dict(os.environ), before)


class ExplicitQAGuards(unittest.TestCase):
    def test_each_affected_scene_requires_a_CLI_recipe_even_if_environment_selects_one(self):
        qa = wrapper()
        for scenes in (['Hoeffding'], ['MaxMargin'], ['Outro'], ['Risk', 'Outro']):
            with self.subTest(scenes=scenes), mock.patch.dict(os.environ, {RECIPE: 'corrected-v1'}), \
                 mock.patch.object(qa, 'preflight_corrected') as preflight, \
                 mock.patch.object(qa.subprocess, 'run') as child, redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised: qa.main(['--only', *scenes, '--lang', 'en'])
                self.assertEqual(raised.exception.code, 2)
                preflight.assert_not_called(); child.assert_not_called()

    def test_explicit_selection_overrides_inherited_recipe_and_both_cache_guards(self):
        qa = wrapper()
        for selected, inherited in (('legacy', 'corrected-v1'), ('corrected-v1', 'legacy'),
                                     ('corrected-v1', 'unknown-inherited-value')):
            inherited_env = {RECIPE: inherited, 'EXPLAINER_CACHED_ONLY': '0', 'EXPLAINER_TTS': 'speech',
                             **{key: '99' for key in qa.THREAD_KEYS}}
            with self.subTest(selected=selected, inherited=inherited), mock.patch.dict(os.environ, inherited_env), \
                 mock.patch.object(qa, 'preflight_corrected', return_value={}) as preflight, \
                 mock.patch.object(qa.subprocess, 'run', return_value=SimpleNamespace(returncode=17)) as child:
                before = dict(os.environ)
                code = qa.main(['--only', 'Hoeffding', '--lang', 'zh', '--recipe', selected, '--motion', '--timeout', '17'])
                self.assertEqual(code, 17)
                self.assertEqual(dict(os.environ), before)
                command = child.call_args.args[0]
                kwargs = child.call_args.kwargs
                self.assertEqual(command[:3], [sys.executable, str(qa.ROOT / 'tools/qa_series.py'), 'ai8'])
                self.assertIn('--cached-only', command)
                self.assertIn('--motion', command)
                self.assertEqual(command[command.index('--lang') + 1], 'zh')
                self.assertEqual(command[command.index('--timeout') + 1], '17')
                self.assertEqual(kwargs['cwd'], qa.ROOT)
                self.assertIs(kwargs['check'], False)
                self.assertEqual(kwargs['env'][RECIPE], selected)
                self.assertEqual(kwargs['env']['EXPLAINER_CACHED_ONLY'], '1')
                self.assertEqual(kwargs['env']['EXPLAINER_TTS'], 'silent')
                self.assertTrue(all(kwargs['env'][key] == '1' for key in qa.THREAD_KEYS))
                self.assertEqual(preflight.call_count, 2 if selected == 'corrected-v1' else 0)

    def test_unaffected_default_does_not_inherit_a_scientific_recipe(self):
        qa = wrapper()
        with mock.patch.dict(os.environ, {RECIPE: 'corrected-v1'}), \
             mock.patch.object(qa, 'preflight_corrected', side_effect=AssertionError('unrelated preflight')) as preflight, \
             mock.patch.object(qa.subprocess, 'run', return_value=SimpleNamespace(returncode=0)) as child:
            self.assertEqual(qa.main(['--only', 'Risk', '--lang', 'en']), 0)
            self.assertEqual(child.call_args.kwargs['env'][RECIPE], 'legacy')
            preflight.assert_not_called()

    def test_legacy_replay_is_explicit_and_does_not_touch_corrected_bundles(self):
        qa = wrapper()
        with mock.patch.object(qa, 'preflight_corrected', side_effect=AssertionError('legacy must not preflight corrected data')) as preflight, \
             mock.patch.object(qa, 'certify_selection') as certify, \
             mock.patch.object(qa.subprocess, 'run', return_value=SimpleNamespace(returncode=0)) as child:
            self.assertEqual(qa.main(['--only', 'Hoeffding', 'MaxMargin', 'Outro', '--lang', 'en', '--recipe', 'legacy']), 0)
            self.assertEqual(child.call_args.kwargs['env'][RECIPE], 'legacy')
            preflight.assert_not_called()
            certify.assert_called_once_with(['Hoeffding', 'MaxMargin', 'Outro'], 'en', 'legacy', {}, False)

    def test_missing_tampered_or_wrong_mode_bundle_fails_before_any_child(self):
        qa = wrapper()
        real_preflight = qa.preflight_corrected
        for error in (FileNotFoundError('missing synthetic bundle'), ValueError('tampered synthetic hash'),
                      ValueError('expected fresh, found derived-weights')):
            for scene, item in (('Hoeffding', 'union'), ('MaxMargin', 'maxmargin')):
                fake = fake_bundles(qa, error=error)
                with self.subTest(error=str(error), scene=scene), \
                     mock.patch.object(qa, 'preflight_corrected', side_effect=lambda scenes: real_preflight(scenes, module=fake)), \
                     mock.patch.object(qa.subprocess, 'run') as child, redirect_stderr(io.StringIO()) as stderr:
                    before = dict(os.environ)
                    with self.assertRaises(SystemExit) as raised:
                        qa.main(['--only', scene, '--lang', 'en', '--recipe', 'corrected-v1'])
                    self.assertEqual(raised.exception.code, 2)
                    self.assertIn('preflight failed', stderr.getvalue())
                    self.assertEqual(dict(os.environ), before)
                    child.assert_not_called()
                    fake.load_bundle.assert_called_once_with(fake.DEFAULT_ROOT, item, expected_mode='fresh')

    def test_postflight_detects_changed_receipt_instead_of_accepting_child_success(self):
        qa = wrapper()
        before = {'union': {'mode': 'fresh', 'output': 'synthetic-before'}}
        after = {'union': {'mode': 'fresh', 'output': 'synthetic-after'}}
        with mock.patch.object(qa, 'preflight_corrected', side_effect=[before, after]) as preflight, \
             mock.patch.object(qa.subprocess, 'run', return_value=SimpleNamespace(returncode=0)) as child, \
             redirect_stderr(io.StringIO()) as stderr:
            with self.assertRaises(SystemExit) as raised:
                qa.main(['--only', 'Hoeffding', '--lang', 'en', '--recipe', 'corrected-v1'])
            self.assertEqual(raised.exception.code, 2)
            self.assertIn('inputs changed during QA', stderr.getvalue())
            self.assertEqual(preflight.call_count, 2); child.assert_called_once()

    def test_postflight_validation_error_fails_after_the_single_child(self):
        qa = wrapper()
        with mock.patch.object(qa, 'preflight_corrected', side_effect=[{'maxmargin': {'mode': 'fresh'}}, ValueError('output changed')]), \
             mock.patch.object(qa.subprocess, 'run', return_value=SimpleNamespace(returncode=0)) as child, \
             redirect_stderr(io.StringIO()) as stderr:
            with self.assertRaises(SystemExit) as raised:
                qa.main(['--only', 'MaxMargin', '--lang', 'en', '--recipe', 'corrected-v1'])
            self.assertEqual(raised.exception.code, 2)
            self.assertIn('postflight failed', stderr.getvalue())
            child.assert_called_once()

    def test_Outro_explicit_corrected_control_runs_without_any_bundle_import(self):
        qa = wrapper()
        with mock.patch.object(qa.importlib.util, 'spec_from_file_location',
                               side_effect=AssertionError('Outro imported unrelated corrected bundle code')), \
             mock.patch.object(qa, 'certify_selection') as certify, \
             mock.patch.object(qa.subprocess, 'run', return_value=SimpleNamespace(returncode=0)) as child:
            self.assertEqual(qa.main(['--only', 'Outro', '--lang', 'zh', '--recipe', 'corrected-v1']), 0)
            child.assert_called_once()
            self.assertEqual(child.call_args.kwargs['env'][RECIPE], 'corrected-v1')
            certify.assert_called_once_with(['Outro'], 'zh', 'corrected-v1', {}, False)

    def test_certification_runs_only_after_successful_explicit_selection_and_postflight(self):
        qa = wrapper()
        for explicit, child_code in ((True, 0), (True, 7), (False, 0)):
            events = []
            snapshots = {'union': {'mode': 'fresh', 'identity': 'synthetic'}}
            def preflight(scenes):
                events.append('preflight')
                return copy.deepcopy(snapshots)
            def child(*args, **kwargs):
                events.append('child')
                return SimpleNamespace(returncode=child_code)
            def certify(*args): events.append('certify')
            arguments = (['--only', 'Hoeffding', '--lang', 'en', '--recipe', 'corrected-v1', '--motion']
                         if explicit else ['--only', 'Risk', '--lang', 'en'])
            with self.subTest(explicit=explicit, child_code=child_code), \
                 mock.patch.object(qa, 'preflight_corrected', side_effect=preflight), \
                 mock.patch.object(qa.subprocess, 'run', side_effect=child), \
                 mock.patch.object(qa, 'certify_selection', side_effect=certify) as certify_mock:
                self.assertEqual(qa.main(arguments), child_code)
                self.assertEqual(events, ['preflight', 'child', 'preflight', 'certify'] if explicit and child_code == 0
                                 else ['preflight', 'child', 'preflight'] if explicit else ['child'])
                if explicit and child_code == 0:
                    certify_mock.assert_called_once_with(['Hoeffding'], 'en', 'corrected-v1', snapshots, True)
                else: certify_mock.assert_not_called()

    def test_failed_certification_never_turns_child_success_into_acceptance(self):
        qa = wrapper()
        with mock.patch.object(qa, 'preflight_corrected', return_value={}), \
             mock.patch.object(qa.subprocess, 'run', return_value=SimpleNamespace(returncode=0)) as child, \
             mock.patch.object(qa, 'certify_selection', side_effect=ValueError('synthetic mismatched QA inputs')), \
             redirect_stderr(io.StringIO()) as stderr:
            with self.assertRaises(SystemExit) as raised:
                qa.main(['--only', 'Outro', '--lang', 'en', '--recipe', 'corrected-v1'])
            self.assertEqual(raised.exception.code, 2)
            self.assertIn('recipe-selection witness failed', stderr.getvalue())
            child.assert_called_once()

    def test_bounded_scope_invalid_modes_force_and_resume_never_start_children(self):
        qa = wrapper()
        base = ['--only', 'Risk', '--lang', 'en']
        cases = [[], ['--lang', 'en'], base + ['--force'], base + ['--resume'],
                 base + ['--recipe', 'automatic'], base + ['--timeout', '0'], base + ['--timeout', '-1']]
        for arguments in cases:
            with self.subTest(arguments=arguments), mock.patch.object(qa, 'preflight_corrected') as preflight, \
                 mock.patch.object(qa.subprocess, 'run') as child, redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit): qa.main(arguments)
                preflight.assert_not_called(); child.assert_not_called()


@contextmanager
def result_fixture(qa, scene='Hoeffding', lang='en', *, items=('union',), motion=False):
    """Only private temporary placeholder bytes; no real QA results or bundles."""
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        snapshots, inputs, files = {}, {}, {}
        for item in items:
            directory = root / '.cache/ai8-corrected-v1' / item
            directory.mkdir(parents=True)
            (directory / 'data.json').write_bytes(b'{"fixture":"synthetic"}\n')
            (directory / 'data.npz').write_bytes(b'synthetic array-archive placeholder; never loaded')
            receipt = {'recipe': item + '-synthetic-recipe', 'mode': 'fresh'}
            (directory / 'receipt.json').write_text(json.dumps(receipt))
            snapshots[item] = copy.deepcopy(receipt)
            files[item] = {}
            for name in ('receipt.json', 'data.json', 'data.npz'):
                path = directory / name
                stat = path.stat()
                inputs[str(path.relative_to(root))] = [stat.st_size, stat.st_mtime_ns]
                files[item][name] = path
        folder = root / 'renders/qa/series/ai8' / lang / (scene + ('_motion' if motion else ''))
        folder.mkdir(parents=True)
        result = {'video': 'ai8', 'scene': scene, 'lang': lang, 'mode': 'motion' if motion else 'endpoints',
                  'status': 'passed', 'warnings': [], 'fingerprint': 'c' * 64, 'inputs': inputs}
        path = folder / 'result.json'
        path.write_text(json.dumps(result, sort_keys=True))
        with mock.patch.object(qa, 'ROOT', root):
            yield SimpleNamespace(root=root, folder=folder, path=path, result=result,
                                  snapshots=snapshots, files=files)


def write_result(fixture):
    fixture.path.write_text(json.dumps(fixture.result, sort_keys=True))


def witness_path(fixture, recipe):
    digest = hashlib.sha256(fixture.path.read_bytes()).hexdigest()
    return fixture.folder / ('recipe-selection-' + recipe + '-' + digest + '.json')


class SelectionWitnesses(unittest.TestCase):
    def test_correct_scene_mapping_and_three_current_paths_are_bound_to_actual_result(self):
        qa = wrapper()
        for scene, item, lang in (('Hoeffding', 'union', 'en'), ('MaxMargin', 'maxmargin', 'zh')):
            with self.subTest(scene=scene), result_fixture(qa, scene, lang, items=(item,)) as fixture:
                original = fixture.path.read_bytes()
                original_mtime = fixture.path.stat().st_mtime_ns
                qa.certify_selection([scene], lang, 'corrected-v1', fixture.snapshots)
                target = witness_path(fixture, 'corrected-v1')
                witness = json.loads(target.read_text())
                self.assertEqual(witness['schema'], 1)
                self.assertEqual(witness['recipe'], 'corrected-v1')
                self.assertEqual((witness['scene'], witness['lang']), (scene, lang))
                self.assertEqual(witness['result_sha256'], hashlib.sha256(original).hexdigest())
                self.assertEqual(witness['source_fingerprint'], fixture.result['fingerprint'])
                self.assertEqual(set(witness['corrected_receipts']), {item})
                self.assertEqual(witness['corrected_receipts'][item]['receipt_sha256'],
                                 hashlib.sha256(fixture.files[item]['receipt.json'].read_bytes()).hexdigest())
                self.assertEqual(witness['corrected_receipts'][item]['recipe'], fixture.snapshots[item]['recipe'])
                self.assertIn('visual and speech acceptance remain separate', witness['acceptance'])
                self.assertEqual(fixture.path.read_bytes(), original)
                self.assertEqual(fixture.path.stat().st_mtime_ns, original_mtime)

    def test_missing_or_stale_bundle_records_and_lost_files_never_get_a_witness(self):
        qa = wrapper()
        for name in ('receipt.json', 'data.json', 'data.npz'):
            for problem in ('missing-record', 'wrong-size', 'wrong-mtime', 'lost-file'):
                with self.subTest(name=name, problem=problem), result_fixture(qa) as fixture:
                    relative = '.cache/ai8-corrected-v1/union/' + name
                    if problem == 'missing-record': fixture.result['inputs'].pop(relative)
                    elif problem == 'wrong-size': fixture.result['inputs'][relative][0] += 1
                    elif problem == 'wrong-mtime': fixture.result['inputs'][relative][1] -= 1
                    else: fixture.files['union'][name].unlink()
                    write_result(fixture)
                    with self.assertRaises((ValueError, OSError)):
                        qa.certify_selection(['Hoeffding'], 'en', 'corrected-v1', fixture.snapshots)
                    self.assertFalse(witness_path(fixture, 'corrected-v1').exists())

    def test_current_receipt_must_equal_the_preflight_snapshot(self):
        qa = wrapper()
        with result_fixture(qa) as fixture:
            fixture.snapshots['union']['recipe'] = 'different-preflight-recipe'
            with self.assertRaises(ValueError):
                qa.certify_selection(['Hoeffding'], 'en', 'corrected-v1', fixture.snapshots)
            self.assertFalse(witness_path(fixture, 'corrected-v1').exists())

    def test_wrong_result_identity_status_mode_or_warnings_fail_before_witness(self):
        qa = wrapper()
        cases = {'video': 'ai9', 'scene': 'MaxMargin', 'lang': 'zh', 'mode': 'motion',
                 'status': 'needs-review', 'warnings': [{'kind': 'synthetic-warning'}],
                 'fingerprint': 'not-a-source-hash', 'inputs': []}
        for field, value in cases.items():
            with self.subTest(field=field), result_fixture(qa) as fixture:
                fixture.result[field] = value; write_result(fixture)
                with self.assertRaises(ValueError):
                    qa.certify_selection(['Hoeffding'], 'en', 'corrected-v1', fixture.snapshots)
                self.assertFalse(witness_path(fixture, 'corrected-v1').exists())

    def test_motion_requires_its_separate_actual_result_mode_and_folder(self):
        qa = wrapper()
        with result_fixture(qa, motion=True) as fixture:
            qa.certify_selection(['Hoeffding'], 'en', 'corrected-v1', fixture.snapshots, motion=True)
            self.assertTrue(witness_path(fixture, 'corrected-v1').is_file())
            with self.assertRaises(OSError):
                qa.certify_selection(['Hoeffding'], 'en', 'corrected-v1', fixture.snapshots, motion=False)

    def test_legacy_replay_is_labeled_and_cannot_have_consumed_corrected_inputs(self):
        qa = wrapper()
        with result_fixture(qa, items=()) as fixture:
            fixture.result['inputs'] = {'.cache/ai8/union.json': [7, 11]}; write_result(fixture)
            qa.certify_selection(['Hoeffding'], 'en', 'legacy', {})
            witness = json.loads(witness_path(fixture, 'legacy').read_text())
            self.assertEqual(witness['recipe'], 'legacy')
            self.assertEqual(witness['scope'], 'explicit legacy replay')
            self.assertEqual(witness['corrected_receipts'], {})
        with result_fixture(qa) as fixture:
            with self.assertRaises(ValueError): qa.certify_selection(['Hoeffding'], 'en', 'legacy', {})
            self.assertFalse(witness_path(fixture, 'legacy').exists())

    def test_Outro_control_needs_no_unrelated_bundle_and_labels_only_its_scope(self):
        qa = wrapper()
        with result_fixture(qa, 'Outro', items=()) as fixture:
            self.assertFalse((fixture.root / '.cache/ai8-corrected-v1').exists())
            qa.certify_selection(['Outro'], 'en', 'corrected-v1', {})
            witness = json.loads(witness_path(fixture, 'corrected-v1').read_text())
            self.assertEqual(witness['corrected_receipts'], {})
            self.assertEqual(witness['scope'], 'regression control; no direct union cache load')

    def test_Outro_no_direct_load_claim_rejects_unexpected_corrected_consumption(self):
        qa = wrapper()
        with result_fixture(qa, 'Outro', items=('union',)) as fixture:
            with self.assertRaises(ValueError): qa.certify_selection(['Outro'], 'en', 'corrected-v1', {})
            self.assertFalse(witness_path(fixture, 'corrected-v1').exists())

    def test_unselected_corrected_items_cannot_be_hidden_in_a_selected_scene(self):
        qa = wrapper()
        with result_fixture(qa, items=('union', 'maxmargin')) as fixture:
            with self.assertRaises(ValueError):
                qa.certify_selection(['Hoeffding'], 'en', 'corrected-v1', fixture.snapshots)
            self.assertFalse(witness_path(fixture, 'corrected-v1').exists())

    def test_generic_QA_absent_receipt_NPZ_sentinel_is_not_a_required_real_file(self):
        qa = wrapper()
        with result_fixture(qa) as fixture:
            # tools/qa_series.record_data records the optional NPZ sibling of
            # every JSON input, including a JSON-only bundle receipt.
            relative = '.cache/ai8-corrected-v1/union/receipt.npz'
            fixture.result['inputs'][relative] = None; write_result(fixture)
            self.assertFalse(os.path.lexists(fixture.root / relative))
            qa.certify_selection(['Hoeffding'], 'en', 'corrected-v1', fixture.snapshots)
            self.assertTrue(witness_path(fixture, 'corrected-v1').is_file())
            self.assertFalse(os.path.lexists(fixture.root / relative))

    def test_only_absent_null_receipt_NPZ_sentinels_for_selected_items_are_allowed(self):
        qa = wrapper()
        for problem in ('nonnull', 'present', 'dangling-symlink', 'unselected-item', 'unknown-optional-name'):
            with self.subTest(problem=problem), result_fixture(qa) as fixture:
                relative = '.cache/ai8-corrected-v1/union/receipt.npz'
                if problem == 'unselected-item': relative = '.cache/ai8-corrected-v1/maxmargin/receipt.npz'
                elif problem == 'unknown-optional-name': relative = '.cache/ai8-corrected-v1/union/extra.npz'
                fixture.result['inputs'][relative] = [0, 0] if problem == 'nonnull' else None
                path = fixture.root / relative
                if problem == 'present': path.write_bytes(b'not an absent optional file')
                elif problem == 'dangling-symlink':
                    try: path.symlink_to(fixture.root / 'missing-synthetic-target')
                    except (OSError, NotImplementedError): continue
                write_result(fixture)
                with self.assertRaises((ValueError, OSError)):
                    qa.certify_selection(['Hoeffding'], 'en', 'corrected-v1', fixture.snapshots)
                self.assertFalse(witness_path(fixture, 'corrected-v1').exists())

    def test_existing_identical_witness_is_immutable_and_mismatches_are_not_overwritten(self):
        qa = wrapper()
        with result_fixture(qa) as fixture:
            qa.certify_selection(['Hoeffding'], 'en', 'corrected-v1', fixture.snapshots)
            target = witness_path(fixture, 'corrected-v1')
            original, mtime = target.read_bytes(), target.stat().st_mtime_ns
            qa.certify_selection(['Hoeffding'], 'en', 'corrected-v1', fixture.snapshots)
            self.assertEqual((target.read_bytes(), target.stat().st_mtime_ns), (original, mtime))
            for field in ('result_sha256', 'corrected_receipt_sha256'):
                modified = json.loads(original)
                if field == 'result_sha256': modified[field] = '0' * 64
                else: modified['corrected_receipts']['union']['receipt_sha256'] = '0' * 64
                target.write_text(json.dumps(modified))
                wrong_bytes = target.read_bytes()
                with self.subTest(field=field), self.assertRaises(ValueError):
                    qa.certify_selection(['Hoeffding'], 'en', 'corrected-v1', fixture.snapshots)
                self.assertEqual(target.read_bytes(), wrong_bytes)

    def test_new_actual_result_gets_a_new_address_without_retagging_prior_proof(self):
        qa = wrapper()
        with result_fixture(qa) as fixture:
            qa.certify_selection(['Hoeffding'], 'en', 'corrected-v1', fixture.snapshots)
            prior = witness_path(fixture, 'corrected-v1'); original = prior.read_bytes()
            fixture.result['fingerprint'] = 'd' * 64; write_result(fixture)
            qa.certify_selection(['Hoeffding'], 'en', 'corrected-v1', fixture.snapshots)
            current = witness_path(fixture, 'corrected-v1')
            self.assertNotEqual(current, prior)
            self.assertTrue(current.is_file())
            self.assertEqual(prior.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
