"""Tiny deterministic Part 2 bug reproductions. Never render, train, or write repository caches.

Run: source /workspace/runtime/activate.sh
     NUMBA_DISABLE_JIT=1 PYTHONDONTWRITEBYTECODE=1 python /workspace/runtime/ai2-test-preparation/reproduce.py
"""
import ast
import datetime
import hashlib
import inspect
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path('/workspace/explainer-videos')
OUT = Path('/workspace/runtime/ai2-test-preparation')
os.environ['NUMBA_DISABLE_JIT'] = '1'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
blocked_repo_writes = []

def readonly_repository(event, args):
    if event == 'open':
        name, mode, flags = args
        if isinstance(name, (str, bytes, os.PathLike)) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
            p = Path(os.fsdecode(name)).absolute()
            if p == ROOT or ROOT in p.parents:
                blocked_repo_writes.append(str(p))
                raise RuntimeError('Test preparation forbids writes to the repository: ' + str(p))
    elif event in ('os.mkdir', 'os.remove', 'os.rename', 'os.rmdir'):
        for name in args[:2] if event == 'os.rename' else args[:1]:
            if isinstance(name, (str, bytes, os.PathLike)):
                p = Path(os.fsdecode(name)).absolute()
                if p == ROOT or ROOT in p.parents:
                    blocked_repo_writes.append(str(p))
                    raise RuntimeError('Test preparation forbids repository mutation: ' + str(p))

sys.addaudithook(readonly_repository)
import numpy as np
from videos.ai.ai2 import local, search, logic, sat, compute

assert not hasattr(local.anneal, 'py_func'), 'JIT must be disabled before imports: no compiled caches'
original_tour_len = local.tour_len

def run_with_trace(function, call, full_tours=False):
    """Count exact source-line events, not an inferred asymptotic count."""
    events = {}
    evaluations = []
    def trace(frame, event, arg):
        if frame.f_code is function.__code__:
            if event == 'line':
                events[frame.f_lineno] = events.get(frame.f_lineno, 0) + 1
            return trace
        return None
    def tour_len(t, D):
        length = int(original_tour_len(t, D))
        evaluations.append({'tour': t.tolist(), 'length': length})
        return length
    with patch.object(local, 'tour_len', tour_len):
        previous = sys.gettrace()
        sys.settrace(trace)
        try:
            value = call()
        finally:
            sys.settrace(previous)
    return value, events, evaluations

def line_containing(function, needle):
    lines, start = inspect.getsourcelines(function)
    return next(start + i for i, line in enumerate(lines) if needle in line)

P = np.array([[0,0],[10,0],[12,7],[8,12],[0,10],[-3,4]], dtype=float)
D = local.dist_matrix(P)
t0 = np.array([0,2,4,1,3,5], dtype=np.int64)
initial = int(original_tour_len(t0, D))
t = t0.copy()
(result, looked), events, full = run_with_trace(local.two_opt_climb, lambda: local.two_opt_climb(t, D, 1))
delta_line = line_containing(local.two_opt_climb, 'looked += 1')
candidates = []
for i in range(len(t0)-1):
    for j in range(i+2, len(t0) if i > 0 else len(t0)-1):
        trial = t0.copy()
        trial[i+1:j+1] = trial[i+1:j+1][::-1]
        candidates.append({'i':i, 'j':j, 'length':int(original_tour_len(trial,D)), 'tour':trial.tolist()})
assert looked == events[delta_line] == 9
assert looked > 1
assert result == original_tour_len(t,D)
local_results = {
    'fixture': {'xy':P.tolist(), 'initial_tour':t0.tolist(), 'initial_length':initial},
    'two_opt_budget_1': {'api':'local.two_opt_climb(t,D,budget)', 'requested_budget':1,
        'reported_delta_evaluations':int(looked), 'instrumented_delta_evaluations':events[delta_line],
        'full_tour_len_calls':len(full), 'returned_length':int(result), 'returned_tour':t.tolist(),
        'best_candidate_in_evaluated_sweep':min(candidates,key=lambda r:r['length']),
        'overruns_budget':looked>1, 'budget_exhaustion_skips_best_sweep_move':int(result)>min(r['length'] for r in candidates),
        'counter_source_line':delta_line}
}

n_temps, per = 4, 5
trace = np.zeros((n_temps,4)); snaps = np.zeros((1,len(P)),np.int64)
(a_best,a_tour), events, full = run_with_trace(local.anneal,
    lambda:local.anneal(t0.copy(),D,30.0,.9,per,n_temps,17,0,snaps,trace))
proposal_line = line_containing(local.anneal, 'i = np.random.randint(n)')
delta_line = line_containing(local.anneal, 'delta = D[')
assert int(a_best) == original_tour_len(a_tour,D)
assert events[proposal_line] == per*n_temps
assert events[delta_line] < events[proposal_line]
local_results['annealing'] = {'api':'local.anneal(t,D,T0,alpha,moves_per_T,n_temps,seed,snap_every,snaps,trace)',
    'seed':17, 'nominal_proposals':per*n_temps, 'instrumented_proposals':events[proposal_line],
    'valid_delta_evaluations':events[delta_line], 'rejected_no_op_draws_before_evaluation':events[proposal_line]-events[delta_line],
    'full_tour_len_calls':len(full),'returned_best_length':int(a_best),'returned_best_tour':a_tour.tolist(),
    'final_trace_best_length':int(trace[-1,2]),'trace':trace.tolist(),
    'counter_source_lines':{'proposal':proposal_line,'delta':delta_line}}
try:
    local.anneal(t0.copy(),D,30.0,.9,199//200,200,17,0,np.zeros((1,len(P)),np.int64),np.zeros((200,4)))
except Exception as error:
    local_results['annealing_budget_below_temperature_count']={'requested_budget':199,'n_temps':200,'moves_per_T':0,
                                                              'observed_error':type(error).__name__+': '+str(error)}

# Find a tiny deterministic final-generation improvement so it cannot hide in the pre-generation trace.
for seed in range(50):
    bp=np.zeros(2,np.int64)
    best,events,full=run_with_trace(local.genetic,
        lambda:local.genetic(D,4,2,.5,seed,bp,np.zeros((1,len(P)),np.int64),np.array([-1],np.int64)))
    if int(best)<int(bp[-1]): break
assert len(full)==4*(2+1)==12
assert int(best)==min(r['length'] for r in full)
assert int(best)<int(bp[-1])
local_results['genetic']={'api':'local.genetic(D,pop_size,gens,p_mut,seed,best_per_gen,snaps,snap_gens)',
    'requested_budget_in_compute_caller':8,'pop_size':4,'gens_from_budget_floor':2,'seed':seed,
    'instrumented_full_tour_len_calls':len(full),'generation_trace':bp.tolist(),
    'returned_final_best_length':int(best),'best_evaluated_tour':min(full,key=lambda r:r['length']),
    'final_generation_improvement_absent_from_trace':True,
    'full_evaluations':full,'evaluations_over_nominal_budget':len(full)-8}

# The repository has fixed-domain grid/puzzle A*, not an arbitrary weighted-graph API.
# This adapter runs the requested graph through the *actual* repository heap functions and key policy.
G={0:[(1,1),(2,5)],1:[(3,9)],2:[(3,10)],3:[]}; names=['S','A','B','G']
h1={0:0,1:0,2:5,3:0};h2={0:0,1:9,2:5,3:0}
assert all(h2[u]>=h1[u] for u in G)
assert all(h[u]<=cost+h[v] for h in (h1,h2) for u,es in G.items() for v,cost in es)
def graph_search(h,epsilon):
    hk=np.empty(32);hv=np.empty(32,np.int64)
    n=search._heap_push(hk,hv,0,float(h[0]),0)
    distance={0:0};closed=set();order=[]
    while n:
        _,u,n=search._heap_pop(hk,hv,n);u=int(u)
        if u in closed:continue
        closed.add(u);order.append(names[u])
        if u==3:return {'pop_order_including_goal':order,'pops_including_goal':len(order),
                        'expansions_excluding_goal':len(order)-1,'optimal_cost':distance[u]}
        for v,cost in G[u]:
            ng=distance[u]+cost
            if v not in closed and ng<distance.get(v,float('inf')):
                distance[v]=ng
                n=search._heap_push(hk,hv,n,ng+h[v]-epsilon*ng,v)
    raise AssertionError('goal missing')
astar_results={'fixture':{'nodes':names,'directed_edges':[['S','A',1],['A','G',9],['S','B',5],['B','G',10]],
                         'h1':{names[k]:v for k,v in h1.items()},'h2':{names[k]:v for k,v in h2.items()},
                         'both_consistent':True,'h2_dominates_h1':True},
               'scope':'Graph adapter uses actual search._heap_push/_heap_pop and exact repository priority formulas. It does not call fixed-domain grid_search or astar8 on this arbitrary graph.',
               'actual_apis':{'grid_search':'grid_search(free,sr,sc,gr,gc,wg,wh,moves): returns (expanded,cost,order,parent,g); goal pop included',
                              'astar8':'astar8(start,kind): returns (expanded,solution_length); goal pop excluded, no order trace returned'},
               'interpretation':'Blanket dominance claim fails for total expansions on the f=C* boundary; both heuristics remain consistent and both find cost10. This tests theorem framing, not a puzzle/grid optimality failure.'}
for label,eps in [('grid_key_epsilon',1e-7),('puzzle8_key_epsilon',1e-3)]:
    one,two=graph_search(h1,eps),graph_search(h2,eps)
    assert one['pop_order_including_goal']==['S','A','G']
    assert two['pop_order_including_goal']==['S','B','A','G']
    astar_results[label]={'epsilon':eps,'h1':one,'h2':two}

L=logic.lit
positive=frozenset({L(True,'P','x'),L(True,'P','y')})
negative=frozenset({L(False,'P','x'),L(False,'P','y')})
factoring=logic.refute([positive,negative],[],max_clauses=64)
empty_kb=logic.refute([frozenset()],[],max_clauses=64)
empty_goal=logic.refute([], [frozenset()],strategy='support',max_clauses=64)
units=logic.refute([frozenset({L(True,'P','x')})],[frozenset({L(False,'P','A')})],max_clauses=64)
assert not factoring['found'] and not empty_kb['found'] and not empty_goal['found']
assert units['found']
logic_results={'api':'logic.refute(kb,negated_goal,strategy="saturate",max_clauses=20000)',
               'factoring_required_unsatisfiable_input':{'kb':[logic.show_clause(positive),logic.show_clause(negative)],
                   'expected_found':True,'actual_result':factoring,
                   'why_unsatisfiable':'Universal closure of P(x) or P(y) implies P(z) by setting x=y=z; the negative clause similarly implies not P(z).'},
               'initial_empty_kb_clause':{'expected_found':True,'actual_result':empty_kb},
               'initial_empty_goal_clause_support':{'expected_found':True,'actual_result':empty_goal},
               'contradictory_unit_sanity':{'expected_found':True,'actual_result':units}}

sat_formula=np.array([[1,2,3]],np.int64)
# All eight sign combinations prohibit all eight assignments, hence UNSAT.
unsat_formula=np.array([[s1,s2*2,s3*3] for s1 in (-1,1) for s2 in (-1,1) for s3 in (-1,1)],np.int64)
original_solve=sat.solve_dpll
statuses={'sat':original_solve(sat_formula,3,max_decisions=100),
          'unsat':original_solve(unsat_formula,3,max_decisions=100),
          'unknown':original_solve(sat_formula,3,max_decisions=0)}
assert int(statuses['sat'][0])==1 and int(statuses['unsat'][0])==0 and int(statuses['unknown'][0])==-1
plan=['sat','sat','unknown','sat','unsat','unknown','unsat','unsat','unknown']
actual=[]
def controlled_solve(_clauses,_n):
    kind=plan[len(actual)]
    formula=unsat_formula if kind=='unsat' else sat_formula
    limit=0 if kind=='unknown' else 100
    value=original_solve(formula,3,max_decisions=limit)
    actual.append({'fixture':kind,'max_decisions':limit,'status':int(value[0]),'decisions':int(value[1])})
    return value
class MemoryPartial(dict):
    def finish(self): self.finished=True
memory=MemoryPartial()
with patch.object(compute,'Partial',return_value=memory), patch.object(sat,'solve_dpll',controlled_solve):
    aggregation=compute.compute_sat3(ns=(3,),alphas=(1.,2.,3.),per=(3,))
assert len(actual)==9 and memory.finished
assert np.allclose(aggregation['psat_3'],[2/3,1/3,0])
assert not any('unknown' in key or 'censor' in key for key in aggregation)
sat_results={'solver_api':'sat.solve_dpll(clauses,n,max_decisions=10**9) returns (status,decisions), status1 SAT/0 UNSAT/-1 gave up',
             'aggregation_api':'compute.compute_sat3(ns,alphas,per); Partial replaced by an in-memory dict only',
             'direct_controlled_limit_results':{k:[int(v[0]),int(v[1])] for k,v in statuses.items()},
             'aggregation_fixture_calls':actual,'actual_aggregation':aggregation,
             'desired_explicit_censoring':{'unknown_fraction':[1/3,1/3,1/3],
                'sat_fraction_among_resolved':[1.,.5,0.],
                'sat_fraction_all_runs_lower_bound':[2/3,1/3,0.],
                'sat_fraction_all_runs_upper_bound':[1.,2/3,1/3]},
             'observed_issue':'Unknown outcomes contribute false to (st==1).mean(), depress pSAT, and are not reported separately; decision summaries also combine censored and complete runs.'}

files=['videos/ai/ai2/local.py','videos/ai/ai2/search.py','videos/ai/ai2/logic.py','videos/ai/ai2/sat.py',
       'videos/ai/ai2/compute.py','videos/ai/ai2/s05_heuristics.py','videos/ai/ai2/s06_local.py']
report={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':'Independent test-only tiny deterministic reproductions; no source/test edits, no scene renders, no cache/compute training jobs.',
        'execution':'Python functions with NUMBA_DISABLE_JIT=1; bytecode writes disabled; process audit hook rejects repository write opens and mutations.',
        'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files},
        'blocked_repository_writes':blocked_repo_writes,'local_search':local_results,'astar_dominance':astar_results,
        'resolution':logic_results,'sat_censoring':sat_results}
assert not blocked_repo_writes
(OUT/'results.json').write_text(json.dumps(report,indent=2,default=lambda v:v.item() if hasattr(v,'item') else str(v))+'\n')
print(json.dumps({'local_search':{k:v for k,v in local_results.items() if k!='fixture'},
                  'astar':astar_results['grid_key_epsilon'],
                  'factoring_found':factoring['found'],'initial_empty_found':empty_kb['found'],
                  'sat_direct':sat_results['direct_controlled_limit_results'],
                  'sat_psat':aggregation['psat_3'],'repository_writes':blocked_repo_writes},indent=2))
