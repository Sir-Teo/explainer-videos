"""Portable correction tests: synthetic fixtures, no scenes or recipe execution.

Run as a file with Python's unittest runner. Only standard-library modules are
imported at discovery; NumPy is loaded lazily for small synthetic fixtures.
Neither registered fresh recipe nor any project/cache module is imported.
"""
from __future__ import annotations

import ast
import bisect
from contextlib import ExitStack, redirect_stderr, redirect_stdout
import copy
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
import hashlib
import io
import itertools
import json
import math
import os
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest import mock

PART = Path(__file__).resolve().parent
PROGRAM = PART / 'corrected_v1.py'
LEGACY = PART / 'compute.py'


@lru_cache(maxsize=1)
def program():
    tree = ast.parse(PROGRAM.read_text())
    # Avoid package __init__ files. The synthetic module name keeps the real
    # __main__ guard false while preserving every other top-level guard.
    module = ModuleType('ai8_corrected_v1_synthetic_tests')
    module.__file__ = str(PROGRAM)
    exec(compile(tree, str(PROGRAM), 'exec'), module.__dict__)
    return module


def numeric():
    try:
        import numpy
    except ImportError as error:
        raise unittest.SkipTest('NumPy is required for synthetic array fixtures') from error
    return numpy


def function(tree, name):
    return next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name)


def scalar_loss(points, labels, weights):
    values = []
    for point, sign in zip(points, labels):
        z = -float(sign) * math.fsum(float(x) * float(w) for x, w in zip(point, weights))
        values.append(max(z, 0.) + math.log1p(math.exp(-abs(z))))
    return math.fsum(values) / len(values)


class Vector(tuple):
    """Enough exact arithmetic to evaluate the actual CDF AST without NumPy."""
    def __sub__(self, value):
        return Vector(x - value for x in self)

    def __rsub__(self, value):
        return Vector(value - x for x in self)

    def __pow__(self, power):
        return Vector(x ** power for x in self)


def survival(values, n, probability):
    if probability != .5:
        raise AssertionError('fixture represents a fair binomial only')
    return Vector(Fraction(sum(math.comb(n, j) for j in range(int(k) + 1, n + 1)), 2 ** n)
                  for k in values)


class SourceAndExactProbability(unittest.TestCase):
    def test_top_level_imports_are_standard_library_only(self):
        tree = ast.parse(PROGRAM.read_text())
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = ([alias.name for alias in node.names] if isinstance(node, ast.Import)
                         else [node.module])
                for name in names:
                    self.assertIn(name.split('.')[0], sys.stdlib_module_names)

    def test_source_identities_match_public_files_and_exact_correction(self):
        module = program()
        identities, corrected = module.source_identity()
        self.assertEqual(identities['legacy_compute_sha256'], hashlib.sha256(LEGACY.read_bytes()).hexdigest())
        self.assertEqual(identities['legacy_compute_sha256'], module.SOURCE_SHA)
        self.assertEqual(identities['corrected_compute_sha256'], hashlib.sha256(corrected.encode()).hexdigest())
        self.assertEqual(identities['corrected_compute_sha256'], module.CORRECTED_SOURCE_SHA)
        self.assertEqual(identities['recipe_program_sha256'], hashlib.sha256(PROGRAM.read_bytes()).hexdigest())

    def test_only_two_reviewed_AST_expressions_change(self):
        _, corrected = program().source_identity()
        expected = ast.parse(LEGACY.read_text())
        union = function(expected, 'compute_union')
        sf = next(node for node in ast.walk(union) if isinstance(node, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == 'sf' for t in node.targets))
        self.assertEqual(ast.dump(sf.value.args[0]), ast.dump(ast.parse('k - 1', mode='eval').body))
        sf.value.args[0] = ast.Name(id='k', ctx=ast.Load())
        margin = function(expected, 'compute_maxmargin')
        loss = next(node for node in ast.walk(margin) if isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'loss' for t in node.targets))
        self.assertEqual(ast.unparse(loss.value), 'float(np.logaddexp(0, -z).mean())')
        loss.value = ast.parse('float(np.logaddexp(0, -(tX @ w)).mean())', mode='eval').body
        self.assertEqual(ast.dump(ast.parse(corrected), include_attributes=False),
                         ast.dump(expected, include_attributes=False))

    def test_wrong_legacy_or_corrected_source_pin_fails_closed(self):
        module = program()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / 'videos/ai/ai8/compute.py'
            path.parent.mkdir(parents=True)
            path.write_bytes(LEGACY.read_bytes() + b'\n# synthetic source mismatch\n')
            with mock.patch.object(module, 'ROOT', root), self.assertRaises(ValueError):
                module.source_identity()
        with mock.patch.object(module, 'CORRECTED_SOURCE_SHA', '0' * 64), self.assertRaises(ValueError):
            module.source_identity()

    def test_actual_CDF_and_lower_median_expressions_match_exact_enumeration(self):
        _, corrected = program().source_identity()
        union = function(ast.parse(corrected), 'compute_union')
        assignments = {node.targets[0].id: node.value for node in ast.walk(union)
                       if isinstance(node, ast.Assign) and len(node.targets) == 1
                       and isinstance(node.targets[0], ast.Name)}
        median = next(node.args[0] for node in ast.walk(union) if isinstance(node, ast.Call)
                      and isinstance(node.func, ast.Attribute) and node.func.attr == 'append'
                      and isinstance(node.func.value, ast.Name) and node.func.value.id == 'best_med')
        for n, count in itertools.product((1, 2, 4), (1, 2, 3, 4)):
            with self.subTest(n=n, rules=count):
                # Enumerate every tuple of binomial counts, rather than using
                # the survival-power identity under test as the reference.
                minimum_mass = [Fraction(0) for _ in range(n + 1)]
                probabilities = [Fraction(math.comb(n, k), 2 ** n) for k in range(n + 1)]
                for outcome in itertools.product(range(n + 1), repeat=count):
                    weight = math.prod(probabilities[k] for k in outcome)
                    minimum_mass[min(outcome)] += weight
                expected = list(itertools.accumulate(minimum_mass))
                namespace = {'k': Vector(range(n + 1)), 'n': n, 'K': count,
                             'binom': SimpleNamespace(sf=survival),
                             'np': SimpleNamespace(searchsorted=bisect.bisect_left), 'float': float}
                namespace['sf'] = eval(compile(ast.Expression(assignments['sf']), '<synthetic-sf>', 'eval'), namespace)
                namespace['cdf_min'] = eval(compile(ast.Expression(assignments['cdf_min']), '<synthetic-cdf>', 'eval'), namespace)
                self.assertEqual(list(namespace['cdf_min']), expected)
                self.assertGreater(expected[0], 0)
                self.assertEqual(expected[-1], 1)
                actual_median = eval(compile(ast.Expression(median), '<synthetic-median>', 'eval'), namespace)
                first = next(k for k, value in enumerate(expected) if value >= Fraction(1, 2))
                self.assertEqual(actual_median, first / n)


def margin_fixture():
    """A consistent artificial rank-one signed design, not a registered run."""
    np = numeric()
    labels = np.r_[np.ones(20), -np.ones(20)].astype('float64')
    points = np.c_[labels, np.zeros(40)].astype('float64')
    steps = np.unique(np.rint(np.geomspace(1, 1_000_000, 160)))
    weights = np.linspace(.5, 2., len(steps))
    rec = np.zeros((len(steps), 7), dtype='float64')
    rec[:, 0], rec[:, 2], rec[:, 4], rec[:, 5] = steps, weights, 1., weights
    rec[:, 3] = [scalar_loss(points, labels, (w, 0.)) for w in weights]
    return {'X': points, 't': labels, 'w_svm': np.array([1., 0.]), 'rec': rec,
            'gamma': 1., 'eta': 4., 'T': 1_000_000, 'c_lo': 0., 'c_hi': 0.,
            'angle_end': 0., 'norm_end': 2., 'margin_end': 1.}


def union_fixture():
    """Analytic quantiles plus a mocked synthetic sample; no seeded draws."""
    np = numeric()
    counts = [1, 10, 100, 1000, 10000, 100000, 1000000]
    result = {'Ks': counts, 'delta': .05, 'ns': [100, 1000], 'sample_best': .5,
              'sample_K': 1000, 'sample_n': 100, 'fresh_best': .5,
              'sample_errs': np.full(1000, .5, dtype='float64')}
    with localcontext() as context:
        context.prec = 90
        for n in (100, 1000):
            coefficients = [math.comb(n, k) for k in range(n + 1)]
            prefix = list(itertools.accumulate(coefficients))
            denominator = Decimal(2 ** n)
            medians, gaps = [], []
            for count in counts:
                # Independent Decimal powers and binary search, whereas the
                # validator uses neighboring integer-tail logarithms.
                low, high = 0, n
                while low < high:
                    middle = (low + high) // 2
                    tail = Decimal(2 ** n - prefix[middle]) / denominator
                    if tail ** count <= Decimal('.5'):
                        high = middle
                    else:
                        low = middle + 1
                medians.append(low / n)
                low, high = 0, n // 2
                while low < high:
                    middle = (low + high) // 2
                    a, b = n // 2 - middle, n // 2 + middle
                    within = Decimal(prefix[b] - (prefix[a - 1] if a else 0)) / denominator
                    if within ** count >= Decimal('.95'):
                        high = middle
                    else:
                        low = middle + 1
                gaps.append(low / n)
            result['best' + str(n)] = np.array(medians, dtype='float64')
            result['gap' + str(n)] = np.array(gaps, dtype='float64')
            result['bound' + str(n)] = np.array([math.sqrt(math.log(2 * k / .05) / (2 * n)) for k in counts])
    return result


class SyntheticNumericalContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.np, cls.module = numeric(), program()

    def setUp(self):
        self.fresh = mock.patch.object(self.module, 'fresh_result', side_effect=AssertionError('registered recipe execution forbidden'))
        self.fresh.start()
        self.addCleanup(self.fresh.stop)

    def test_loss_uses_postupdate_weights_and_changes_no_other_value(self):
        np = self.np
        X = np.array([[1., 0.], [0., 2.], [-1., -1.]])
        labels = np.array([1., 1., -1.])
        post = .6 * ((labels[:, None] * X).sum(0)) / (2 * len(X))
        rec = np.array([[1., 20., .7, math.log(2), -.2, *post],
                        [2., 10., 1.4, math.log(2), .4, 1000., -1000.]])
        value = {'X': X, 't': labels, 'rec': rec, 'w_svm': np.array([1., 0.]),
                 'description': 'synthetic saved weights'}
        original = copy.deepcopy(value)
        corrected = self.module.correct_postupdate_losses(value)
        for key in ('X', 't', 'w_svm'):
            np.testing.assert_array_equal(corrected[key], original[key])
            self.assertIsNot(corrected[key], value[key])
        np.testing.assert_array_equal(corrected['rec'][:, [0, 1, 2, 4, 5, 6]], original['rec'][:, [0, 1, 2, 4, 5, 6]])
        np.testing.assert_array_equal(value['rec'], original['rec'])
        self.assertEqual(corrected['description'], original['description'])
        for row in corrected['rec']:
            self.assertAlmostEqual(row[3], scalar_loss(X, labels, row[5:7]), places=12)
        self.assertLess(corrected['rec'][0, 3], math.log(2))
        self.assertTrue(np.isfinite(corrected['rec']).all())

    def test_actual_loss_expression_ignores_stale_preupdate_logits(self):
        np = self.np
        _, corrected = self.module.source_identity()
        node = next(n.value for n in ast.walk(function(ast.parse(corrected), 'compute_maxmargin'))
                    if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'loss' for t in n.targets))
        points, labels, weights = np.array([[1., 2.], [-2., 1.]]), np.array([1., -1.]), np.array([.3, -.2])
        expected = scalar_loss(points, labels, weights)
        for stale in (np.zeros(2), np.array([800., -800.])):
            actual = eval(compile(ast.Expression(node), '<synthetic-postupdate-loss>', 'eval'),
                          {'np': np, 'float': float, 'z': stale, 'tX': labels[:, None] * points, 'w': weights})
            self.assertAlmostEqual(actual, expected, places=14)

    def test_derived_loss_rejects_nonfinite_wrong_dtype_or_shape(self):
        np = self.np
        for change in ('dtype', 'nan', 'labels-shape', 'rec-shape'):
            value = margin_fixture()
            if change == 'dtype': value['rec'] = value['rec'].astype('float32')
            if change == 'nan': value['X'][0, 0] = np.nan
            if change == 'labels-shape': value['t'] = value['t'][:, None]
            if change == 'rec-shape': value['rec'] = value['rec'][:, :6]
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.module.correct_postupdate_losses(value)

    def test_actual_MaxMargin_schema_accepts_consistent_synthetic_geometry(self):
        value = margin_fixture()
        self.assertEqual(self.module.validate_result('maxmargin', value)['scalar_postupdate_rows'], 142)
        old = copy.deepcopy(value)
        old['rec'][:, 3] = math.log(2)
        self.assertEqual(self.module.validate_result('maxmargin', old, check_losses=False)['scalar_postupdate_rows'], 0)
        with self.assertRaises(ValueError): self.module.validate_result('maxmargin', old)
        self.assertEqual(self.module.validate_result('maxmargin', self.module.correct_postupdate_losses(old))['scalar_postupdate_rows'], 142)

    def test_actual_MaxMargin_schema_rejects_bad_geometry_recipe_and_data(self):
        np = self.np
        for change in ('dtype', 'infinity', 'label', 'steps', 'norm', 'angle', 'margin', 'endpoint',
                       'eta', 'gamma', 'unit-svm', 'c_lo', 'c_hi', 'T', 'extra'):
            value = margin_fixture()
            if change == 'dtype': value['X'] = value['X'].astype('float32')
            elif change == 'infinity': value['rec'][0, 3] = np.inf
            elif change == 'label': value['t'][0] = 0
            elif change == 'steps': value['rec'][0, 0] = 2
            elif change == 'norm': value['rec'][0, 2] += .1
            elif change == 'angle': value['rec'][0, 1] += 1
            elif change == 'margin': value['rec'][0, 4] += .1
            elif change == 'endpoint': value['norm_end'] += .1
            elif change == 'eta': value['eta'] += .1
            elif change == 'gamma': value['gamma'] += .1
            elif change == 'unit-svm':
                value['w_svm'] *= 2
                value['gamma'] = 2.
            elif change in ('c_lo', 'c_hi'): value[change] += .1
            elif change == 'T': value['T'] -= 1
            else: value['extra'] = 1
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.module.validate_result('maxmargin', value)

    def test_actual_union_schema_checks_exact_quantiles_with_a_synthetic_sample(self):
        np, module = self.np, self.module
        value = union_fixture()
        # This stub deliberately prevents even the validator's seeded draw.
        generator = SimpleNamespace(binomial=lambda n, p, size=None: np.full(size, n // 2) if size is not None else n // 2)
        with mock.patch.object(np.random, 'PCG64', return_value=object()), \
             mock.patch.object(np.random, 'Generator', return_value=generator):
            self.assertEqual(module.validate_result('union', value), {'exact_integer_Decimal_median_boundaries': 14})
            for change in ('median-off-by-one', 'gap', 'bound', 'sample', 'seed-metadata', 'shape'):
                bad = copy.deepcopy(value)
                if change == 'median-off-by-one': bad['best100'][0] += .01
                elif change == 'gap': bad['gap100'][0] += .01
                elif change == 'bound': bad['bound100'][0] += .01
                elif change == 'sample': bad['sample_errs'][0] = .4
                elif change == 'seed-metadata': bad['sample_n'] = 101
                else: bad['best100'] = bad['best100'][:-1]
                with self.subTest(change=change), self.assertRaises(ValueError):
                    module.validate_result('union', bad)


class PortableBundleFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.np, cls.module = numeric(), program()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / 'corrected'
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.sources = {'legacy_compute_sha256': self.module.SOURCE_SHA,
                        'corrected_compute_sha256': self.module.CORRECTED_SOURCE_SHA,
                        'recipe_program_sha256': '3' * 64}
        self.runtime = {**self.module.RUNTIME, 'machine': 'synthetic-test-cpu', 'byteorder': 'little',
                        'executable_sha256': '4' * 64,
                        'package_RECORD_sha256': {'numpy': '5' * 64, 'scipy': '6' * 64},
                        'threads': {key: '1' for key in self.module.THREAD_KEYS}}
        self.stack.enter_context(mock.patch.object(self.module, 'source_identity', return_value=(self.sources, 'not executed')))
        self.stack.enter_context(mock.patch.object(self.module, 'runtime_identity', return_value=self.runtime))
        self.actual_validate_result = self.module.validate_result
        self.stack.enter_context(mock.patch.object(self.module, 'validate_result', return_value={'synthetic_fixture': True}))
        self.stack.enter_context(mock.patch.object(self.module.shutil, 'disk_usage', return_value=SimpleNamespace(free=4 * 1024 ** 3)))
        self.producer = self.stack.enter_context(mock.patch.object(self.module, 'fresh_result', side_effect=AssertionError('registered recipe must never execute')))
        self.value = {'fixture': 'synthetic', 'numbers': self.np.array([.25, .5, .75], dtype='float64')}

    def inputs(self, mode):
        return {} if mode == 'fresh' else {'maxmargin.json': {'bytes': 11, 'sha256': '1' * 64},
                                           'maxmargin.npz': {'bytes': 17, 'sha256': '2' * 64}}

    def bundle(self, item='maxmargin', mode='fresh'):
        destination = self.module.reserve_bundle(self.root, item)
        receipt = self.module.write_bundle(destination, item, mode, self.value, self.inputs(mode),
                                           self.sources, self.runtime, .01)
        return destination, receipt

    def rewrite_receipt(self, destination, mutate):
        path = destination / 'receipt.json'
        receipt = json.loads(path.read_text())
        mutate(receipt)
        path.write_text(json.dumps(receipt))

    def test_roundtrip_labels_fresh_and_derived_modes_distinctly(self):
        for index, mode in enumerate(('fresh', 'derived-weights')):
            self.root = self.base / str(index)
            _, expected = self.bundle(mode=mode)
            value, receipt = self.module.load_bundle(self.root, 'maxmargin', expected_mode=mode)
            self.np.testing.assert_array_equal(value['numbers'], self.value['numbers'])
            self.assertEqual(receipt, expected)
            if mode == 'derived-weights':
                self.assertNotIn('seed', receipt['parameters'])
                self.assertIn('reference_recipe_parameters', receipt['parameters'])
                self.assertIn('not authenticated', receipt['parameters']['input_origin'])
                self.assertIn('no trajectory regeneration', receipt['classification'])
            with self.assertRaises(ValueError):
                self.module.load_bundle(self.root, 'maxmargin', expected_mode='derived-weights' if mode == 'fresh' else 'fresh')
        self.producer.assert_not_called()

    def test_reservation_refuses_existing_file_empty_directory_partial_and_symlinks(self):
        for index, kind in enumerate(('empty', 'file', 'partial', 'symlink')):
            root = self.base / str(index)
            root.mkdir()
            target = root / 'union'
            if kind == 'file': target.write_text('existing')
            elif kind == 'symlink':
                other = self.base / 'symlink-target'; other.mkdir()
                try: target.symlink_to(other, target_is_directory=True)
                except (OSError, NotImplementedError): continue
            else:
                target.mkdir()
                if kind == 'partial': (target / 'data.npz').write_bytes(b'partial')
            with self.subTest(kind=kind), self.assertRaises((OSError, ValueError)):
                self.module.reserve_bundle(root, 'union')
        with mock.patch.object(self.module.shutil, 'disk_usage', return_value=SimpleNamespace(free=1024)):
            with self.assertRaises(ValueError): self.module.reserve_bundle(self.base / 'low-space', 'union')

    def test_legacy_and_symlinked_ancestors_are_read_only(self):
        fake_repository = self.base / 'repository'
        legacy = fake_repository / '.cache/ai8'
        legacy.mkdir(parents=True)
        with mock.patch.object(self.module, 'ROOT', fake_repository):
            with self.assertRaises(ValueError): self.module.reserve_bundle(legacy, 'union')
            with self.assertRaises(ValueError): self.module.reserve_bundle(legacy / 'nested', 'union')
        real = self.base / 'real'; real.mkdir()
        alias = self.base / 'alias'
        try: alias.symlink_to(real, target_is_directory=True)
        except (OSError, NotImplementedError): self.skipTest('symlinks unavailable')
        with self.assertRaises(ValueError): self.module.reserve_bundle(alias / 'nested', 'union')
        destination = real / 'reserved'; destination.mkdir()
        with self.assertRaises(ValueError):
            self.module.write_bundle(alias / 'reserved', 'union', 'fresh', self.value, {}, self.sources, self.runtime, 0.)
        self.assertEqual(list(destination.iterdir()), [])

    def test_writer_refuses_dirty_and_symlink_destinations_without_overwriting(self):
        destination = self.module.reserve_bundle(self.root, 'union')
        marker = destination / 'partial.json'; marker.write_bytes(b'preserve this partial')
        with self.assertRaises(ValueError):
            self.module.write_bundle(destination, 'union', 'fresh', self.value, {}, self.sources, self.runtime, 0.)
        self.assertEqual(marker.read_bytes(), b'preserve this partial')
        self.assertEqual({p.name for p in destination.iterdir()}, {'partial.json'})
        alias = self.base / 'destination-alias'
        try: alias.symlink_to(destination, target_is_directory=True)
        except (OSError, NotImplementedError): self.skipTest('symlinks unavailable')
        with self.assertRaises(ValueError):
            self.module.write_bundle(alias, 'union', 'fresh', self.value, {}, self.sources, self.runtime, 0.)

    def test_writer_rejects_mode_input_source_runtime_and_elapsed_before_writes(self):
        cases = ['unknown-mode', 'union-derived', 'fresh-inputs', 'derived-empty', 'bad-input-hash',
                 'wrong-source', 'wrong-runtime', 'negative-time', 'nonfinite-time', 'wrong-raw-json']
        for index, case in enumerate(cases):
            root = self.base / str(index)
            destination = self.module.reserve_bundle(root, 'maxmargin')
            item, mode, inputs, sources, runtime, elapsed, raw = 'maxmargin', 'fresh', {}, self.sources, self.runtime, .01, None
            if case == 'unknown-mode': mode = 'automatic'
            elif case == 'union-derived': item, mode, inputs = 'union', 'derived-weights', self.inputs('derived-weights')
            elif case == 'fresh-inputs': inputs = self.inputs('derived-weights')
            elif case == 'derived-empty': mode = 'derived-weights'
            elif case == 'bad-input-hash':
                mode, inputs = 'derived-weights', self.inputs('derived-weights'); inputs['maxmargin.json']['sha256'] = 'invalid'
            elif case == 'wrong-source': sources = {**self.sources, 'legacy_compute_sha256': '0' * 64}
            elif case == 'wrong-runtime': runtime = {**self.runtime, 'numpy': '0.invalid'}
            elif case == 'negative-time': elapsed = -1
            elif case == 'nonfinite-time': elapsed = math.nan
            else: raw = b'{"fixture":"wrong"}'
            with self.subTest(case=case), self.assertRaises(ValueError):
                self.module.write_bundle(destination, item, mode, self.value, inputs, sources, runtime, elapsed, raw)
            self.assertEqual(list(destination.iterdir()), [])

    def test_loader_refuses_missing_partial_or_lost_files_and_never_produces(self):
        missing = self.base / 'does-not-exist'
        with self.assertRaises(ValueError): self.module.load_bundle(missing, 'union')
        self.assertFalse(missing.exists())
        for index, lost in enumerate(('receipt.json', 'data.json', 'data.npz')):
            self.root = self.base / str(index)
            destination, _ = self.bundle()
            (destination / lost).unlink()
            before = {p.name: p.read_bytes() for p in destination.iterdir()}
            with self.subTest(lost=lost), self.assertRaises(ValueError): self.module.load_bundle(self.root, 'maxmargin')
            self.assertEqual({p.name: p.read_bytes() for p in destination.iterdir()}, before)
        self.producer.assert_not_called()

    def test_loader_rejects_wrong_receipt_recipe_source_runtime_and_output_identity(self):
        mutations = {
            'schema': lambda r: r.update(schema=2),
            'item': lambda r: r.update(item='union'),
            'recipe': lambda r: r.update(recipe='unreviewed'),
            'mode': lambda r: r.update(mode='automatic'),
            'sources': lambda r: r['sources'].update(corrected_compute_sha256='0' * 64),
            'runtime': lambda r: r['runtime'].update(numpy='0.invalid'),
            'runtime-executable-build': lambda r: r['runtime'].update(executable_sha256='0' * 64),
            'runtime-package-build': lambda r: r['runtime']['package_RECORD_sha256'].update(numpy='0' * 64),
            'parameters': lambda r: r['parameters'].update(seed=0),
            'classification': lambda r: r.update(classification='authenticated original trajectory'),
            'inputs': lambda r: r.update(inputs=self.inputs('derived-weights')),
            'elapsed': lambda r: r.update(elapsed_numerical_seconds=-1),
            'validation': lambda r: r.update(validation={'wrong': True}),
            'output-hash': lambda r: r['outputs']['data.npz'].update(sha256='0' * 64),
            'output-size': lambda r: r['outputs']['data.npz'].update(bytes=0),
            'missing-field': lambda r: r.pop('parameters'),
            'extra-field': lambda r: r.update(unknown='not permitted'),
        }
        for index, (case, mutate) in enumerate(mutations.items()):
            self.root = self.base / str(index)
            destination, _ = self.bundle()
            self.rewrite_receipt(destination, mutate)
            with self.subTest(case=case), self.assertRaises(ValueError):
                self.module.load_bundle(self.root, 'maxmargin')
        self.producer.assert_not_called()

    def test_loader_refuses_tampered_payload_extras_and_nonempty_locks(self):
        for index, case in enumerate(('data-bytes', 'extra-file', 'data-lock', 'receipt-lock')):
            self.root = self.base / str(index)
            destination, _ = self.bundle()
            if case == 'data-bytes':
                with (destination / 'data.npz').open('ab') as stream: stream.write(b'tampered')
            elif case == 'extra-file': (destination / 'unexpected.partial').touch()
            else: (destination / ('data.json.lock' if case == 'data-lock' else 'receipt.json.lock')).write_bytes(b'nonempty')
            with self.subTest(case=case), self.assertRaises(ValueError): self.module.load_bundle(self.root, 'maxmargin')
        self.root = self.base / 'empty-locks'
        destination, _ = self.bundle()
        for name in ('data.json.lock', 'receipt.json.lock'): (destination / name).touch()
        self.module.load_bundle(self.root, 'maxmargin')

    def test_symlink_payloads_and_coordination_locks_are_rejected(self):
        for index, name in enumerate(('data.json', 'data.npz', 'receipt.json', 'data.json.lock', 'receipt.json.lock')):
            self.root = self.base / str(index)
            destination, _ = self.bundle()
            path = destination / name
            elsewhere = self.base / ('elsewhere-' + str(index))
            elsewhere.write_bytes(path.read_bytes() if path.exists() else b'')
            path.unlink(missing_ok=True)
            try: path.symlink_to(elsewhere)
            except (OSError, NotImplementedError): self.skipTest('symlinks unavailable')
            with self.subTest(name=name), self.assertRaises(ValueError): self.module.load_bundle(self.root, 'maxmargin')

    def test_payload_reader_and_actual_validator_reject_nonfinite_or_duplicate_metadata(self):
        json_path, npz_path = self.base / 'input.json', self.base / 'input.npz'
        for text in ('{"x":NaN}', '{"x":Infinity}', '{"x":1e999}', '{"x":1,"x":2}', '[]'):
            json_path.write_text(text)
            self.np.savez(npz_path, numbers=self.np.array([1.]))
            with self.subTest(text=text), self.assertRaises((ValueError, OverflowError)):
                value, _ = self.module.read_payload(json_path, npz_path)
                if text == '{"x":1e999}':
                    self.actual_validate_result('maxmargin', value)
        json_path.write_text('{"numbers":1}')
        with self.assertRaises(ValueError): self.module.read_payload(json_path, npz_path)

    def fake_cache(self, transform=None):
        module, calls = self.module, []
        class Cache:
            def __init__(cache, part): calls.append(('init', part))
            def load(cache, name):
                calls.append(('load', name))
                (cache.dir / (name + '.json.lock')).touch()
                value = (module.strict_json((cache.dir / 'receipt.json').read_bytes()) if name == 'receipt'
                         else module.read_payload(cache.dir / 'data.json', cache.dir / 'data.npz')[0])
                return transform(cache, name, value) if transform else value
        return Cache, calls

    def test_scene_hook_records_receipt_then_data_and_never_installs_a_producer(self):
        destination, _ = self.bundle()
        cache_type, calls = self.fake_cache()
        with mock.patch.object(self.module, 'DEFAULT_ROOT', self.root):
            value = self.module.load_for_scene('maxmargin', cache_type=cache_type)
        self.np.testing.assert_array_equal(value['numbers'], self.value['numbers'])
        self.assertEqual(calls, [('init', 'ai8-corrected-v1'), ('load', 'receipt'), ('load', 'data')])
        self.assertEqual({p.name for p in destination.iterdir()},
                         {'receipt.json', 'data.json', 'data.npz', 'receipt.json.lock', 'data.json.lock'})
        self.producer.assert_not_called()

    def test_scene_hook_rejects_missing_and_derived_before_instantiating_cache(self):
        cache_type = mock.Mock(side_effect=AssertionError('unvalidated cache accessed'))
        with mock.patch.object(self.module, 'DEFAULT_ROOT', self.root), self.assertRaises(ValueError):
            self.module.load_for_scene('maxmargin', cache_type=cache_type)
        cache_type.assert_not_called()
        self.bundle(mode='derived-weights')
        with mock.patch.object(self.module, 'DEFAULT_ROOT', self.root), self.assertRaises(ValueError):
            self.module.load_for_scene('maxmargin', cache_type=cache_type)
        cache_type.assert_not_called()

    def test_scene_hook_rejects_tampered_receipt_array_or_scalar_returns(self):
        for index, case in enumerate(('receipt', 'array', 'scalar')):
            self.root = self.base / str(index); self.bundle()
            def transform(cache, name, value):
                if case == 'receipt' and name == 'receipt': value['recipe'] = 'wrong'
                elif case == 'array' and name == 'data': value['numbers'][0] += 1
                elif case == 'scalar' and name == 'data': value['fixture'] = 'wrong'
                return value
            cache_type, _ = self.fake_cache(transform)
            with self.subTest(case=case), mock.patch.object(self.module, 'DEFAULT_ROOT', self.root), self.assertRaises(ValueError):
                self.module.load_for_scene('maxmargin', cache_type=cache_type)

    def test_scene_hook_disappeared_data_calls_only_the_fail_closed_hooks(self):
        destination, _ = self.bundle()
        for missing in ('receipt', 'data'):
            called = []
            class Cache:
                def __init__(cache, part): pass
                def load(cache, name):
                    called.append(name)
                    self.assertEqual(set(cache.items), {'receipt', 'data'})
                    if name == missing:
                        return cache.items[name]()
                    return self.module.strict_json((destination / 'receipt.json').read_bytes())
            with self.subTest(missing=missing), mock.patch.object(self.module, 'DEFAULT_ROOT', self.root), self.assertRaises(FileNotFoundError):
                self.module.load_for_scene('maxmargin', cache_type=Cache)
            self.assertEqual(called, ['receipt'] if missing == 'receipt' else ['receipt', 'data'])
        self.producer.assert_not_called()


class RuntimeAndExplicitCLI(unittest.TestCase):
    def test_runtime_and_thread_mismatches_fail(self):
        module = program()
        versions = lambda name: module.RUNTIME[name]
        environment = {key: '1' for key in module.THREAD_KEYS}
        records = {'numpy': 'synthetic NumPy RECORD\n', 'scipy': 'synthetic SciPy RECORD\n'}
        readers = {name: mock.Mock(side_effect=lambda field, name=name: records[name]
                                  if field == 'RECORD' else None) for name in records}
        distribution = mock.Mock(side_effect=lambda name: SimpleNamespace(read_text=readers[name]))
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(os.environ, environment), \
             mock.patch.object(module.platform, 'python_version', return_value=module.RUNTIME['python']), \
             mock.patch.object(module.importlib.metadata, 'version', side_effect=versions), \
             mock.patch.object(module.importlib.metadata, 'distribution', distribution):
            executable = Path(temporary) / 'synthetic-runtime'
            executable.write_bytes(b'synthetic executable build A')
            with mock.patch.object(module.sys, 'executable', str(executable)):
                identity = module.runtime_identity()
                self.assertEqual(identity['threads'], environment)
                self.assertEqual(identity['executable_sha256'], hashlib.sha256(executable.read_bytes()).hexdigest())
                self.assertEqual(identity['package_RECORD_sha256'],
                                 {name: hashlib.sha256(text.encode()).hexdigest() for name, text in records.items()})
                self.assertEqual(set(identity), set(module.RUNTIME) | {'machine', 'byteorder', 'threads',
                                                                      'executable_sha256', 'package_RECORD_sha256'})
                for reader in readers.values(): reader.assert_called_with('RECORD')
                self.assertEqual({call.args[0] for call in distribution.call_args_list}, {'numpy', 'scipy'})
                # Identical version strings must not conceal different builds.
                records['numpy'] += 'different binary wheel build\n'
                changed_package = module.runtime_identity()
                self.assertNotEqual(identity['package_RECORD_sha256'], changed_package['package_RECORD_sha256'])
                executable.write_bytes(b'synthetic executable build B')
                changed_executable = module.runtime_identity()
                self.assertNotEqual(identity['executable_sha256'], changed_executable['executable_sha256'])
                for name in records:
                    original = records[name]; records[name] = ''
                    with self.subTest(empty_RECORD=name), self.assertRaises(ValueError): module.runtime_identity()
                    records[name] = original
            with mock.patch.dict(os.environ, {module.THREAD_KEYS[0]: '2'}), self.assertRaises(ValueError): module.runtime_identity()
            with mock.patch.object(module.importlib.metadata, 'version', return_value='0.invalid'), self.assertRaises(ValueError): module.runtime_identity()

    def test_CLI_requires_explicit_valid_mode_before_any_reservation(self):
        module = program()
        cases = [[], ['--item', 'union'], ['--item', 'union', '--mode', 'derived-weights', '--input-dir', '.'],
                 ['--item', 'maxmargin', '--mode', 'derived-weights'],
                 ['--item', 'union', '--mode', 'fresh', '--input-dir', '.'],
                 ['--item', 'unknown', '--mode', 'fresh']]
        for arguments in cases:
            with self.subTest(arguments=arguments), mock.patch.object(module, 'reserve_bundle') as reserve, \
                 mock.patch.object(module, 'fresh_result') as fresh, redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit): module.main(arguments)
                reserve.assert_not_called(); fresh.assert_not_called()


if __name__ == '__main__':
    unittest.main()
