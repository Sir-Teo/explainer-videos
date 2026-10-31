"""Censored puzzle data and exact grid priorities, without production jobs."""
import ast
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from explainer.zh_templates import Translator, sources
from videos.ai.ai2 import compute, search


def row(mh_len=-1, pdb_len=-1, misplaced_len=-1, mh=500, pdb=100, misplaced=50):
    return {'manhattan_len':mh_len, 'pdb_len':pdb_len, 'misplaced_len':misplaced_len,
            'manhattan':mh, 'pdb':pdb, 'misplaced':misplaced}


class PuzzleCensoringTests(unittest.TestCase):
    def test_actual_plot_uses_only_established_lengths_including_non_pdb_solutions(self):
        # Execute the scene's actual plot-construction statements with geometry
        # stand-ins: no Manim scene, LaTeX, render or graphics cache is created.
        source = Path(__file__).resolve().parents[1]/'videos/ai/ai2/s05_heuristics.py'
        tree = ast.parse(source.read_text())
        fn = next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='fifteen')
        end = next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and
                   any(isinstance(t,ast.Name) and t.id=='lg' for t in n.targets))
        code = compile(ast.Module(body=fn.body[:end],type_ignores=[]),'actual-puzzle-plot','exec')
        class Group(list):
            def add(self,x):self.append(x);return self
        class Marker:
            def __init__(self,*args,**kwargs):pass
            def scale(self,*args):return self
            def rotate(self,*args):return self
            def move_to(self,point):self.point=point;return self
        class Plot:
            def __init__(self,*args,**kwargs):self.ax=self;self.ranges=args;self.labels=kwargs
            def c2p(self,x,y):return (x,y)
        for rows,expected in [([row(12),row(pdb_len=18),row()], [12,18]),([row()], [])]:
            scope={'load':lambda name:{'rows':rows},'puzzle15_summary':search.puzzle15_summary,
                   'np':np,'axes':Plot,'VGroup':Group,'Triangle':Marker,'Dot':lambda point,**kw:point,
                   'FCOL':'f','HEUR':'h','PATH':'p','PI':np.pi}
            exec(code,scope)
            for group in scope['pts']:
                points=[m.point if isinstance(m,Marker) else m for m in group]
                self.assertEqual([p[0] for p in points],expected)
                self.assertTrue(all(np.isfinite(p).all() for p in points))
            self.assertGreaterEqual(scope['lo'],0)
            if not expected:
                self.assertEqual(scope['g'].labels['xlabel'],'no optimal lengths established')

    def test_any_completed_solver_establishes_length_but_not_other_completion_work(self):
        rows = [row(mh_len=12), row(pdb_len=18), row(misplaced_len=6), row()]
        out = search.puzzle15_summary(rows)
        self.assertEqual(out['optimal_lengths'], [12,18,6,None])
        self.assertEqual(out['unknown_lengths'], 1)
        self.assertEqual(out['capped'], {'misplaced':3, 'manhattan':3, 'pdb':3})
        self.assertEqual(out['paired_completed'], 0)
        self.assertIsNone(out['completed_work_ratio'])

    def test_ratio_excludes_censored_runs_from_both_numerator_and_denominator(self):
        rows = [row(12,12,mh=30,pdb=10), row(18,18,mh=10,pdb=10),
                row(24,-1,mh=1000000,pdb=100), row(-1,30,mh=900000,pdb=1)]
        out = search.puzzle15_summary(rows)
        self.assertEqual(out['paired_completed'], 2)
        self.assertEqual(out['completed_work_ratio'], 2.)
        self.assertEqual(search.puzzle15_summary([row(12,12,mh=5,pdb=10)])['completed_work_ratio'], .5)
        self.assertIsNone(search.puzzle15_summary([row(12,12,mh=0,pdb=0)])['completed_work_ratio'])

    def test_empty_and_all_capped_cases_have_no_fake_negative_length(self):
        for rows in ([], [row()], [row(),row()]):
            out = search.puzzle15_summary(rows)
            self.assertTrue(all(x is None for x in out['optimal_lengths']))
            self.assertIsNone(out['completed_work_ratio'])

    def test_only_completed_length_disagreements_are_rejected(self):
        for bad in (row(12,14), row(12,-1,14), row(-1,12,14)):
            with self.assertRaisesRegex(ValueError, 'disagree'):
                search.puzzle15_summary([bad])

    def test_actual_compute_accepts_pdb_cap_when_manhattan_solves(self):
        # Execute the production orchestration with tiny solver/PDB fixtures;
        # no PDB construction, benchmark, Cache.load or cache write occurs.
        with patch.object(search, 'build_pdb', return_value=np.array([0],dtype=np.uint8)), \
             patch.object(search, 'ida15', side_effect=[(101,-1),(30,12),(51,-1)]), \
             patch.object(search, '_h15', return_value=0):
            out = compute.compute_puzzle15(n_inst=1)
        self.assertEqual(out['schema_version'], compute.CACHE_SCHEMAS['puzzle15'])
        r = out['rows'][0]
        self.assertEqual(r['optimal_len'], 12)
        self.assertEqual((r['pdb_status'],r['manhattan_status'],r['misplaced_status']), ('capped','solved','capped'))

    def test_actual_scene_narration_translates_both_ratio_branches_and_bookmarks(self):
        source_rows = sources('ai2')
        main = next(r['tpl'] for r in source_rows if 'The fifteen-puzzle has about ten trillion states' in r.get('tpl',''))
        matched = next(r['tpl'] for r in source_rows if 'On the {paired} positions both methods solved' in r.get('tpl',''))
        unavailable = next(r['en'] for r in source_rows if 'No matched completion-work ratio is available' in r.get('en',''))
        translate = Translator('ai2')
        for rows in ([row(12,12,mh=5,pdb=10),row()], [row(12),row()], []):
            summary = search.puzzle15_summary(rows)
            paired, ratio = summary['paired_completed'], summary['completed_work_ratio']
            comparison = eval(compile(ast.parse(matched,mode='eval'),'actual-ratio-branch','eval'),
                              {}, {'paired':paired,'ratio':ratio}) if ratio is not None else unavailable
            spoken = eval(compile(ast.parse(main,mode='eval'),'actual-puzzle-narration','eval'),
                          {'len':len}, {'rows':rows,'summary':summary,'n_cap':summary['capped'],
                          'comparison':comparison,'d':{'caps':{'misplaced':50}},
                          'hm':{'pdb':30,'manhattan':25,'misplaced':14}})
            chinese = translate(spoken)
            self.assertIsNotNone(chinese)
            self.assertNotIn('{',chinese)
            self.assertNotIn('times fewer',spoken)
            self.assertNotIn('No matched',chinese)
            self.assertNotIn('On the ',chinese)
            self.assertEqual(re.findall(r"<bookmark[^>]+/>",spoken), re.findall(r"<bookmark[^>]+/>",chinese))
            self.assertIn('最优解长',chinese)
            if ratio is not None:
                self.assertIn('0.50',chinese)
            else:
                self.assertIn('无法报告',chinese)


class GridPriorityTests(unittest.TestCase):
    def test_positive_dijkstra_scaling_preserves_shortest_cost_in_real_api(self):
        free = np.ones((3,3),bool)
        # Before repair wg=1e-8 returned1+sqrt(5), although2sqrt(2) is optimal.
        for scale in (1.,.1,1e-8,1e-12):
            result = search.grid_search(free,0,0,2,2,scale,0.,search.MOVES)
            self.assertAlmostEqual(result[1],2*np.sqrt(2),places=12)
            self.assertEqual(result[0],9)
        self.assertTrue(search.grid_search.nopython_signatures)  # real compiled production function

    def test_astar_positive_priority_scaling_preserves_shortest_cost(self):
        free = np.ones((7,7),bool)
        free[1:6,3] = False
        optimal = search.grid_search(free,3,1,3,5,1.,0.,search.MOVES)[1]
        for scale in (1.,1e-8,1e8):
            actual = search.grid_search(free,3,1,3,5,scale,scale,search.MOVES)
            self.assertAlmostEqual(actual[1],optimal,places=12)

    def test_exact_f_ties_prefer_larger_g(self):
        free = np.ones((3,3),bool)
        _,_,order,_,_ = search.grid_search(free,0,0,2,2,0.,0.,search.MOVES)
        self.assertEqual(order[1,2],1)  # longest one-step g=sqrt(5), then lowest cell id


class SearchCacheRevisionTests(unittest.TestCase):
    def test_cached_only_rejects_old_search_data_without_recomputing(self):
        from tools.qa_series import StaleDataError, require_current_cache
        with tempfile.TemporaryDirectory() as folder:
            cache = compute.SchemaCache('ai2');cache.dir=Path(folder)
            # Write only isolated test fixtures, never production cache data.
            for name,old in [('puzzle15',{'rows':[row()]}),('grid',{'astar_cost':3.})]:
                cache.path(name).write_text(json.dumps(old))
                before=cache.path(name).read_bytes()
                with patch.object(compute,'CACHE',cache):
                    with self.assertRaisesRegex(StaleDataError,'ai2/'+name):
                        require_current_cache(compute,'ai2',cache.path(name),name)
                self.assertEqual(cache.path(name).read_bytes(),before)

    def test_new_schema_requires_explicit_completion_status(self):
        with tempfile.TemporaryDirectory() as folder:
            cache=compute.SchemaCache('ai2');cache.dir=Path(folder)
            cache.path('puzzle15').write_text(json.dumps({'schema_version':1,'rows':[row()]}))
            self.assertFalse(cache.current('puzzle15'))
            r=row();r['optimal_len']=None
            r.update({k+'_status':'capped' for k in ('misplaced','manhattan','pdb')})
            cache.path('puzzle15').write_text(json.dumps({'schema_version':1,'rows':[r]}))
            self.assertTrue(cache.current('puzzle15'))
