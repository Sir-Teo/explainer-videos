"""Read existing Part1 JSON/NPZ only; check arithmetic identities, never call compute/load helpers."""
import hashlib,json,math
from pathlib import Path
import numpy as np
ROOT=Path('/workspace/explainer-videos')
OUT=Path('/workspace/runtime/ai1-source-review')
used={}
def cached(name):
 p=ROOT/'.cache/ai1'/(name+'.json'); raw=p.read_bytes(); used[str(p.relative_to(ROOT))]=hashlib.sha256(raw).hexdigest(); d=json.loads(raw)
 z=p.with_suffix('.npz')
 if z.exists():
  used[str(z.relative_to(ROOT))]=hashlib.sha256(z.read_bytes()).hexdigest()
  with np.load(z) as a:d.update({k:a[k] for k in a.files})
 return d
C={name:cached(name) for name in ['letters','bigram','chain','game','huffman','groups','kraft','huffopt','typical','kl','arith','corpus','lms','probes']}
p=np.asarray(C['letters']['p']);H=float(-(p*np.log2(p)).sum()); assert abs(p.sum()-1)<1e-12 and (p>0).all()
assert abs(H-C['letters']['H'])<1e-12
b=C['bigram'];J=np.asarray(b['joint']);cond=np.asarray(b['cond']);assert abs(J.sum()-1)<1e-12 and np.allclose(cond.sum(1),1)
assert np.allclose(J/J.sum(1,keepdims=True),cond)
assert abs(float(J.sum(1)@np.asarray(b['row_H']))-b['H_cond'])<1e-12
ch=C['chain'];alpha=' abcdefghijklmnopqrstuvwxyz'; ti,hi,ei=[alpha.index(c) for c in 'the']
assert abs(ch['p_the']-ch['p1'][ti]*ch['after_t'][hi]*ch['after_th'][ei])<1e-12
assert np.allclose(ch['after_t'],cond[ti])
g=C['game'];assert len(g['sentence'])==len(g['sentence_ranks'])==len(g['sentence_bits'])==101
assert all(len(guesses)==rank and guesses[-1]==symbol for guesses,rank,symbol in zip(g['sentence_guesses'],g['sentence_ranks'],g['sentence']))
assert abs(float(np.sum(g['sentence_bits']))-g['sentence_total'])<1e-10
hf=C['huffman'];codes=hf['codes'];lengths=np.array([len(c) for c in codes]);assert not any(i!=j and v.startswith(u) for i,u in enumerate(codes) for j,v in enumerate(codes))
assert abs(float(p@lengths)-hf['L'])<1e-12
assert hf['word_bits']==''.join(codes[alpha.index(c)] for c in hf['word'])
assert hf['fixed_bits']==5*len(hf['word'])
gr=C['groups'];assert abs(sum(gr['P'])-1)<1e-12 and abs(gr['H_groups']+float(np.asarray(gr['P'])@np.asarray(gr['within']))-H)<1e-12
kr=C['kraft'];assert np.allclose(kr['shannon_lengths'],np.ceil(-np.log2(p)))
assert abs(np.exp2(-np.asarray(kr['shannon_lengths'],float)).sum()-kr['shannon_kraft'])<1e-12
assert sum(kr['leaves'])==2**kr['prefix']['lmax'] and kr['bad_cross']==16
ho=C['huffopt'];assert abs(ho['L']-hf['L'])<1e-12 and abs(ho['L']-ho['opt27'])<1e-12
assert len(ho['trial_n'])==ho['n_trials']==400 and np.max(abs(ho['trial_h']-ho['trial_o']))<1e-9
T=C['typical'];assert abs(T['H']-H)<1e-12 and abs(T['gap27']-(math.log2(27)-H))<1e-12
assert T['q']==p[0]
for r in T['rows']:assert T['h']-1e-12<=r['shannon_rate']<T['h']+1/r['n']
K=C['kl'];fwd=np.asarray(K['fwd']);rev=np.asarray(K['rev_a']);x=K['x'];density=K['p'];mass=float(np.sum((density[:-1]+density[1:])*np.diff(x)/2))
assert abs(mass-1)<1e-6
assert abs(fwd[-1,0]-K['mean'])<.05 and abs(fwd[-1,1]-K['sd'])<.05
q=p.copy();q[alpha.index('e')],q[alpha.index('z')]=p[alpha.index('z')],p[alpha.index('e')]
ce=float(-(p*np.log2(q)).sum());kl=ce-H;assert kl>=0
# Exact tie-sequence witnesses for exercise3, using integer tenths to avoid float tie ambiguity.
def merge_steps(pairs):
 pool={c:(w,{c:0}) for c,w in zip('abcde',(4,2,2,1,1))};log=[]
 for a,b,name in pairs:
  wa,da=pool[a];wb,db=pool[b];assert sorted((wa,wb))==sorted(w for w,_ in pool.values())[:2]
  pool.pop(a);pool.pop(b);new={c:v+1 for c,v in {**da,**db}.items()};pool[name]=(wa+wb,new);log.append([a,b,name])
 return {'merges':log,'lengths':[next(iter(pool.values()))[1][c] for c in 'abcde']}
flat=merge_steps([('d','e','de'),('de','b','deb'),('c','a','ca'),('deb','ca','root')])
chain=merge_steps([('d','e','de'),('de','c','dec'),('b','dec','bdec'),('a','bdec','root')])
assert flat['lengths']==[2,2,2,3,3] and chain['lengths']==[1,2,3,4,4]
out={'checks':'existing-cache arithmetic and tiny exact Huffman tie witnesses only; no repo experiment functions called',
'cache_sha256':used,'H_letters':H,'H_cond':b['H_cond'],'q_u':b['q_u'],'P_the':ch['p_the'],
'game_sentence_symbols':len(g['sentence']),'game_sentence_bits':g['sentence_total'],
'huffman_L':hf['L'],'shannon_L':hf['L_shannon'],'huffman_word_bits':len(hf['word_bits']),'huffman_fixed_bits':hf['fixed_bits'],
'grouping_H':gr['H_groups']+float(np.asarray(gr['P'])@np.asarray(gr['within'])),
'kraft_shannon_sum':kr['shannon_kraft'],'bad_code_first_cross':kr['bad_cross'],'optimal_checks':ho['n_trials'],
'typical_last_row':T['rows'][-1],
'kl_density_mass_on_grid':mass,'kl_forward_endpoint':fwd[-1].tolist(),'kl_reverse_endpoint':rev[-1].tolist(),
'crossentropy_swapped_letters':ce,'KL_swapped_letters':kl,'exercise3_flat_witness':flat,'exercise3_chain_witness':chain,
'cache_files_changed_during_check':[s for s,h in used.items() if hashlib.sha256((ROOT/s).read_bytes()).hexdigest()!=h]}
assert not out['cache_files_changed_during_check']
(OUT/'cached-identities.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['cache_sha256','typical_last_row']},indent=2))
