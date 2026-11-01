"""Tiny isolated cache fixtures; no Part5 producer, model or network is run."""
import concurrent.futures
import copy
import io
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import Mock, patch
import zipfile

import numpy as np

from videos.ai.ai5.cache_contract import SchemaCache, canonical, digest, valid_structure


def clt():
    return dict(ks=[1], k1=np.ones(6) / 6)


def galton():
    return dict(rows=1, n=2, steps=np.array([[0], [1]]), bins=np.array([0, 1]),
                counts=np.array([1, 1]), binom=np.array([.5, .5]), x=np.array([0., 1.]),
                normal=np.array([.5, .5]), chi2=0.)


def mle():
    return dict(mus=np.array([0., 1.]), sigmas=np.array([1., 2.]), ll=np.zeros((2, 2)),
                mu_hat=.5, sigma_hat=.5, ll_hat=-.3, n=2)


def markov():
    return dict(P=np.ones((27, 27)) / 27, freq=np.ones(27) / 27,
                stationary=np.ones(27) / 27, P3=np.ones((3, 3)) / 3, pi3=np.ones(3) / 3,
                dists=np.ones((2, 27)) / 27, tv=np.zeros(2), lam2=.5, start='q',
                walk3=[0, 1], states3=['space', 'vowel', 'consonant'])


def mixing():
    return dict(xs=np.array([-1., 1.]), U=np.zeros(2), betas=np.array([0., 1.]),
                gap=np.array([.5, .4]), tmix=np.array([1., 2.]), lower=np.zeros(2),
                upper=np.array([3., 4.]), pi=np.array([.5, .5]), ts=[0, 1],
                snaps=np.ones((2, 2)) / 2, slope=1., asym=0., asym_pair='a ', flow_ij=0., flow_ji=0.)


def montecarlo():
    return dict(pts=np.array([[0., 0.]]), inside=np.array([True]), est=np.array([4.]),
                N=1, Ns=np.array([1]), rms=np.array([0.]), slope=-.5, true=.01,
                n=1, plain_hits=0, plain_est=0., is_est=.001, is_y=np.array([1.]), is_w=np.array([1.]), plain_z=np.array([0.]),
                plain_plot_indices=np.array([0]), is_w_full=np.array([1.]))


def ess():
    return dict(s=1.25, n=10, dims=[1, 2], ess=np.array([[10., 5.]]),
                top=np.array([[.1, .5]]), theory=np.array([10., 5.]), ess_rare=1., n_rare=1)


def decoding_fixture():
    from videos.ai.ai5.decoding import configuration
    from videos.ai.ai5.decoding_contract import METRIC_VERSION
    config = configuration()
    settings = [f'{k}{v}' for k, v in config['settings']]
    d = dict(provenance={'selected_prompts_sha256': 'a' * 64}, metric_version=METRIC_VERSION,
             prompt_count=config['prompts'], stochastic_samples=config['samples'], greedy_samples=1,
             settings=settings, kinds=[k for k, _ in config['settings']],
             values=[v for _, v in config['settings']], prompt0='a', prompt3='b',
             human=dict(nll=1., rep=0., text='human'), next_p=np.ones(60) / 100, next_tok=['x'] * 60)
    for key in settings:
        d[key] = dict(nll=1., rep=0., div=None if key == 'greedy0.0' else .5,
                      kept=1., nll_prompt=[1.] * config['prompts'], examples=['x'], ex_prompt=['y'])
    return d


class Part5CacheContracts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in ['cache_contract', 'contracts', 'compute', 'decoding', 'decoding_contract']:
            p = self.root / f'videos/ai/ai5/{name}.py'
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(f'# fixed fixture {name}\n')
        p = self.root / 'videos/ai/ai1/compute.py'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('# fixed upstream fixture\n')
        self.cache = SchemaCache('ai5')
        self.cache.repo_root = self.root
        self.cache.dir = self.root / '.cache/ai5'
        self.producer = Mock(side_effect=AssertionError('unexpected producer'))
        self.cache.items = {name: self.producer for name in ('clt', 'galton', 'mle', 'markov', 'mixing', 'montecarlo', 'ess')}

    def upstream(self):
        b = self.root / '.cache/ai1'
        b.mkdir(parents=True)
        (b / 'train.txt').write_text('a small observed text\n')
        for name, key, value in [('bigram', 'cond', np.ones((27, 27)) / 27),
                                 ('letters', 'p', np.ones(27) / 27)]:
            (b / f'{name}.json').write_text('{}')
            np.savez_compressed(b / f'{name}.npz', **{key: value})

    def rewrite(self, name, fn):
        p = self.cache.path(name)
        d = json.loads(p.read_text())
        fn(d)
        p.write_text(json.dumps(d))

    def assert_stale_without_producer(self, name='clt'):
        self.assertFalse(self.cache.current(name))
        self.producer.assert_not_called()

    def test_saved_fixture_current_and_actual_cached_load_zero_producers(self):
        self.cache.save('clt', clt())
        with patch.object(self.cache, '_produce', side_effect=AssertionError('must not produce')) as producer:
            self.assertTrue(self.cache.current('clt'))
            np.testing.assert_array_equal(self.cache.load('clt')['k1'], np.ones(6) / 6)
            producer.assert_not_called()

    def test_missing_and_unknown_names_never_auto_attested(self):
        self.assert_stale_without_producer()
        self.assertFalse(self.cache.current('../outside'))
        with self.assertRaises(KeyError):
            self.cache.load('../outside')

    def test_all_malformed_top_level_and_metadata_shapes_fail_closed(self):
        self.cache.dir.mkdir(parents=True)
        for value in [None, 1, 'truthy', [], [1], True]:
            self.cache.path('clt').write_text(json.dumps(value))
            self.assert_stale_without_producer()
        for value in [None, [], [1], 1, True, 'truthy']:
            self.cache.save('clt', clt())
            self.rewrite('clt', lambda d: d.update(_cache=value))
            self.assert_stale_without_producer()

    def test_metadata_bool_does_not_alias_integer_version(self):
        self.cache.save('clt', clt())
        self.rewrite('clt', lambda d: d['_cache'].update(schema_version=True))
        self.assert_stale_without_producer()

    def test_json_tampering_rejected_and_partial_bytes_preserved(self):
        self.cache.save('clt', clt())
        partial = self.cache.dir / 'clt.partial.json'
        partial.write_bytes(b'valuable incompatible checkpoint')
        signature = (partial.read_bytes(), partial.stat().st_mtime_ns)
        self.rewrite('clt', lambda d: d.update(ks=[2]))
        self.assert_stale_without_producer()
        self.assertEqual((partial.read_bytes(), partial.stat().st_mtime_ns), signature)

    def test_crc_failure_rejected_even_when_archive_hash_matches_metadata(self):
        self.cache.save('clt', clt())
        p = self.cache.path('clt').with_suffix('.npz')
        array = io.BytesIO()
        np.save(array, np.ones(6) / 6)
        with zipfile.ZipFile(p, 'w', compression=zipfile.ZIP_STORED) as archive:
            archive.writestr('k1.npy', array.getvalue())
        data = bytearray(p.read_bytes())
        index = data.index(b'\x93NUMPY') + len(array.getvalue()) - 1
        data[index] ^= 1
        p.write_bytes(data)
        self.rewrite('clt', lambda d: d['_cache'].update(arrays_sha256=digest(p)))
        self.assert_stale_without_producer()

    def test_object_array_and_duplicate_payload_key_rejected(self):
        for arrays in [dict(k1=np.array([object()], dtype=object)), dict(ks=np.array([1]), k1=np.ones(6) / 6)]:
            self.cache.save('clt', clt())
            p = self.cache.path('clt').with_suffix('.npz')
            np.savez_compressed(p, **arrays)
            self.rewrite('clt', lambda d: d['_cache'].update(arrays_sha256=digest(p)))
            self.assert_stale_without_producer()

    def test_source_recipe_drift_rejected_without_computation(self):
        self.cache.save('clt', clt())
        (self.root / 'videos/ai/ai5/contracts.py').write_text('# changed math\n')
        self.assert_stale_without_producer()

    def test_source_recipe_changes_model_items_only_for_decoder_source(self):
        before = self.cache.recipe('clt')
        model_before = self.cache.recipe('temperature')
        (self.root / 'videos/ai/ai5/decoding.py').write_text('# changed model loader\n')
        self.assertEqual(before, self.cache.recipe('clt'))
        self.assertNotEqual(model_before, self.cache.recipe('temperature'))

    def test_transitive_galton_to_mle_requires_current_payload(self):
        self.cache.save('galton', galton())
        self.cache.save('mle', mle())
        self.assertTrue(self.cache.current('mle'))
        self.rewrite('galton', lambda d: d.update(n=3))
        self.assert_stale_without_producer('mle')

    def test_transitive_parent_replacement_invalidates_existing_child(self):
        self.cache.save('galton', galton())
        self.cache.save('mle', mle())
        changed = galton(); changed['chi2'] = 1.
        self.cache.save('galton', changed)
        self.assert_stale_without_producer('mle')

    def test_markov_upstream_structure_crc_hash_and_train_dependency(self):
        self.upstream()
        self.cache.save('markov', markov())
        self.cache.save('mixing', mixing())
        self.assertTrue(self.cache.current('mixing'))
        (self.root / '.cache/ai1/train.txt').write_text('different observed text')
        self.assert_stale_without_producer('mixing')

    def test_upstream_existence_is_insufficient(self):
        self.upstream()
        self.cache.save('markov', markov())
        np.savez_compressed(self.root / '.cache/ai1/bigram.npz', cond=np.zeros((27, 27)))
        self.assert_stale_without_producer('markov')
        with self.assertRaises(ValueError):
            self.cache.dependencies('markov')

    def test_missing_upstream_aborts_before_producer_or_publication(self):
        with self.assertRaises(FileNotFoundError):
            self.cache._produce('markov', self.producer)
        self.producer.assert_not_called()
        self.assertFalse(self.cache.path('markov').exists())

    def test_ess_depends_on_current_montecarlo_payload(self):
        self.cache.save('montecarlo', montecarlo())
        self.cache.save('ess', ess())
        self.assertTrue(self.cache.current('ess'))
        self.cache.path('montecarlo').with_suffix('.npz').write_bytes(b'incomplete')
        self.assert_stale_without_producer('ess')

    def test_ess_rare_cohort_must_match_actual_parent_count(self):
        self.cache.save('montecarlo', montecarlo())
        self.cache.save('ess', ess())
        broken = ess(); broken['n_rare'] = 400
        with self.assertRaisesRegex(ValueError, 'cohort'):
            self.cache.save('ess', broken)
        # Even deliberately re-signed metadata cannot turn the wrong cohort current.
        def alter(d):
            d['n_rare'] = 400
            d['_cache']['payload_sha256'] = canonical({k: v for k, v in d.items() if k != '_cache'})
        self.rewrite('ess', alter)
        self.assert_stale_without_producer('ess')

    def test_decoder_completed_provenance_binds_observed_assets_not_only_shape(self):
        d = decoding_fixture()
        identity = dict(schema_version=3, assets={'base.pt': 'b' * 64})
        d['provenance'].update(identity)
        self.cache.items['decoding'] = self.producer
        with patch('videos.ai.ai5.decoding.cache_identity', return_value=identity):
            self.cache.save('decoding', d)
            self.assertTrue(self.cache.current('decoding'))
            self.cache.load('decoding')
            self.producer.assert_not_called()
            broken = copy.deepcopy(d)
            broken['provenance']['assets']['base.pt'] = 'c' * 64
            with self.assertRaisesRegex(ValueError, 'identity'):
                self.cache.save('decoding', broken)
        with patch('videos.ai.ai5.decoding.cache_identity', return_value={'schema_version': 3, 'assets': {'base.pt': 'c' * 64}}):
            self.assert_stale_without_producer('decoding')

    def test_dependency_change_during_production_never_publishes(self):
        self.cache.save('galton', galton())
        def produce():
            changed = galton(); changed['chi2'] = 1.
            self.cache.save('galton', changed)
            return mle()
        with self.assertRaisesRegex(ValueError, 'changed during generation'):
            self.cache._produce('mle', produce)
        self.assertFalse(self.cache.path('mle').exists())

    def test_malformed_producer_result_does_not_remove_prior_cache(self):
        self.cache.save('clt', clt())
        p = self.cache.path('clt'); before = (p.read_bytes(), p.stat().st_mtime_ns)
        with self.assertRaises(ValueError):
            self.cache.save('clt', dict(ks=[1], k1=np.zeros(6)))
        self.assertEqual((p.read_bytes(), p.stat().st_mtime_ns), before)

    def test_actual_cached_only_guard_blocks_load_and_producer_for_malformed_marker(self):
        from tools.qa_series import require_current_cache, StaleDataError
        self.cache.dir.mkdir(parents=True)
        self.cache.path('clt').write_text('null')
        guard = type('Guard', (), {'cache_current': self.cache.current})()
        with patch.object(self.cache, 'load', side_effect=AssertionError('loader entered')) as loader:
            with self.assertRaises(StaleDataError):
                require_current_cache(guard, 'ai5', self.cache.path('clt'), 'clt')
            loader.assert_not_called()
        self.producer.assert_not_called()

    def test_concurrent_actual_load_path_owns_item_lock_and_produces_once(self):
        def producer():
            time.sleep(.025)
            return clt()
        producer = Mock(side_effect=producer)
        self.cache.items['clt'] = producer
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            result = list(executor.map(lambda _: self.cache.load('clt'), range(2)))
        self.assertEqual(producer.call_count, 1)
        self.assertTrue(self.cache.current('clt'))
        self.assertEqual(len(result), 2)

    def test_actual_cli_observes_current_cache_and_respects_force_under_lock(self):
        self.cache.save('clt', clt())
        with patch('sys.argv', ['compute', 'clt']):
            self.cache.main({'clt': self.producer})
        self.producer.assert_not_called()
        with patch('sys.argv', ['compute', 'clt', '--force']):
            self.cache.main({'clt': clt})
        self.assertTrue(self.cache.current('clt'))

    def test_wrong_shapes_counts_and_probability_domains_are_not_current(self):
        for field, value in [('n', True), ('counts', np.array([2, 2])), ('binom', np.array([-1., 2.])),
                             ('bins', np.array([2, 0]))]:
            payload = galton(); payload[field] = value
            self.assertFalse(valid_structure('galton', payload))

    def test_stale_recipe_and_missing_dependency_cannot_bless_decoding_partial(self):
        self.cache.dir.mkdir(parents=True)
        p = self.cache.dir / 'decoding.partial.json'
        p.write_bytes(b'expensive partial in a different schema')
        before = (p.read_bytes(), p.stat().st_mtime_ns)
        self.assertFalse(self.cache.current('decoding'))
        self.assertEqual((p.read_bytes(), p.stat().st_mtime_ns), before)

    def test_model_prerequisite_queries_are_pure_and_missing_files_fail_explicitly(self):
        with patch('videos.ai.ai5.decoding_contract.judge_identity', side_effect=FileNotFoundError('pinned model missing')):
            with self.assertRaises(FileNotFoundError):
                self.cache.dependencies('temperature')
        with patch('videos.ai.ai5.decoding.cache_identity', side_effect=FileNotFoundError('base snapshot missing')):
            with self.assertRaises(FileNotFoundError):
                self.cache.dependencies('decoding')
        self.producer.assert_not_called()



class Part5PayloadMeaning(unittest.TestCase):
    def test_score_estimator_scalar_location_and_explicit_failed_path_gaps(self):
        from videos.ai.ai5.cache_contract import REQUIRED
        d = {key: 0 for key in REQUIRED['scorefn'].split()}
        d.update(mu=1., steps=10, pop=2, paths_plain=np.array([[[0., 0.], [np.nan, np.nan]]]),
                 paths_base=np.zeros((1, 2, 2)), final_plain=np.array([-1.]), final_base=np.array([1.]),
                 div_plain=1, div_base=0)
        self.assertTrue(valid_structure('scorefn', d))
        d['final_plain'] = np.array([1.]); d['div_plain'] = 0
        self.assertFalse(valid_structure('scorefn', d))

    def test_montecarlo_plot_contains_actual_tail_and_full_weight_cohort(self):
        d = montecarlo()
        # The last hit lies outside the first400 display cohort; its true index
        # must survive without inventing a replacement Gaussian coordinate.
        d.update(n=402, plain_z=np.r_[np.zeros(401), 4.5], plain_hits=1,
                 plain_est=1 / 402, plain_plot_indices=np.r_[np.arange(400), 401],
                 is_w_full=np.ones(402))
        self.assertTrue(valid_structure('montecarlo', d))
        for key, value in [
            ('plain_plot_indices', np.arange(400)),
            ('plain_plot_indices', np.r_[np.arange(400), 400]),
            ('plain_plot_indices', np.r_[np.arange(400), 401, 401]),
            ('plain_plot_indices', np.r_[np.arange(400), 402]),
            ('plain_plot_indices', np.r_[np.arange(400), 401.5]),
            ('plain_hits', 0), ('plain_est', 0.),
            ('plain_z', np.zeros(401)), ('is_w_full', np.ones(400)),
            ('is_w_full', np.r_[np.ones(401), -1.]),
            ('is_w_full', np.r_[np.ones(401), np.inf]),
        ]:
            broken = copy.deepcopy(d); broken[key] = value
            self.assertFalse(valid_structure('montecarlo', broken), key)

    def test_rejection_sampling_ordinates_use_envelope_density_units(self):
        from videos.ai.ai5.cache_contract import REQUIRED
        d = {key: 0 for key in REQUIRED['draws'].split()}
        d.update(M=2.5, p=np.array([.25, .75]), freq=np.array([.25, .75]),
                 bm_u=np.array([[.2, .6]]), bm_z=np.array([[1., -1.]]),
                 xp=np.array([.2, .8]), up=np.array([1.5, 2.5]), acc=np.array([True, False]))
        self.assertTrue(valid_structure('draws', d))
        for key, value in [('M', 0.), ('M', -1.), ('M', float('nan')), ('M', float('inf')),
                           ('M', [2.5]), ('up', np.array([1.5, 2.5001])),
                           ('up', np.array([-.1, 1.])), ('up', np.array([np.nan, 1.])),
                           ('xp', np.array([1.1, .8])), ('xp', np.array([-.1, .8])),
                           ('acc', np.array([1, 0])), ('acc', np.array([True])),
                           ('acc', np.array([[True, False]]))]:
            broken = copy.deepcopy(d); broken[key] = value
            self.assertFalse(valid_structure('draws', broken), (key, value))

    def test_declared_required_fields_have_actual_source_publish_sites(self):
        import ast
        import re
        from videos.ai.ai5.cache_contract import REQUIRED
        root = Path(__file__).resolve().parents[1]
        source = ast.parse((root / 'videos/ai/ai5/compute.py').read_text())
        functions = {n.name: n for n in source.body if isinstance(n, ast.FunctionDef)}
        for item, fields in REQUIRED.items():
            tree = (ast.parse((root / 'videos/ai/ai5/decoding.py').read_text()) if item == 'decoding'
                    else functions['compute_' + item])
            published, patterns = set(), []
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    published.update(k.arg for k in node.keywords if k.arg)
                if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant):
                    published.add(node.slice.value)
                if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.JoinedStr):
                    patterns.append('^' + ''.join(re.escape(v.value) if isinstance(v, ast.Constant)
                                    else '.+' for v in node.slice.values) + '$')
                if isinstance(node, ast.DictComp) and isinstance(node.key, ast.JoinedStr):
                    patterns.append('^' + ''.join(re.escape(v.value) if isinstance(v, ast.Constant)
                                    else '.+' for v in node.key.values) + '$')
            dynamic = {'brownian': {'walk8', 'walk64', 'walk1024'},
                       'shape': {'field2.0', 'field0.5', 'field0.1'}}.get(item, set())
            unknown = set(fields.split()) - published - dynamic
            self.assertFalse({k for k in unknown if not any(re.fullmatch(p, k) for p in patterns)}, item)

    def test_decoding_cohorts_and_metric_domains_without_loading_models(self):
        d = decoding_fixture()
        settings = d['settings']
        self.assertTrue(valid_structure('decoding', d))
        for key, value in [('prompt_count', True), ('prompt_count', 1), ('metric_version', True),
                           ('greedy_samples', True), ('stochastic_samples', 1)]:
            broken = copy.deepcopy(d); broken[key] = value
            self.assertFalse(valid_structure('decoding', broken), (key, value))
        broken = copy.deepcopy(d); broken['human']['nll'] = float('nan')
        self.assertFalse(valid_structure('decoding', broken))
        broken = copy.deepcopy(d); broken[settings[-1]]['nll_prompt'] = [1.]
        self.assertFalse(valid_structure('decoding', broken))


if __name__ == "__main__":
    unittest.main()
