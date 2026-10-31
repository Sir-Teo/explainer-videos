from pathlib import Path
import ast,hashlib,json,re,subprocess
root=Path('/workspace/explainer-videos');out=Path(__file__).parent
zp=root/'videos/ai/ai3/zh_lines.py';zt=ast.parse(zp.read_text());z=next(ast.literal_eval(n.value) for n in zt.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='ZH' for x in n.targets))
entries=[]
for filename,method,oldkey,newkey,newintro in [
 ('s01_hook.py','islands','In part one, a model learned to guess the next letter by counting','In part one, a model learned to guess the next letter by counting',None),
 ('s13_words.py','history',"Part 1's counting model treated every word as an island.",'Part 1 began with counts of distinct letter symbols.',"第1部分先从不同字母符号的计数开始。现在，我们通过统计词共享的上下文，把词联系起来。这个想法来自语言学。"),
 ('s18_netflix.py','model','f"The model is a sum.','f"The model is a sum.',None)]:
 p=root/'videos/ai/ai3'/filename;before=out/(filename+'.before');old=before.read_text();new=p.read_text();ot=ast.parse(old);nt=ast.parse(new)
 def calls(t):return [n for n in ast.walk(t) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='voiceover']
 oldcalls=calls(ot);newcalls=calls(nt);changed=[(a,b) for a,b in zip(oldcalls,newcalls) if ast.dump(a,include_attributes=False)!=ast.dump(b,include_attributes=False)]
 assert len(oldcalls)==len(newcalls) and len(changed)==1
 a,b=changed[0];oldexpr=a.args[0];newexpr=b.args[0]
 def marks(n):return re.findall(r'<bookmark[^>]+/>',''.join(x.value for x in ast.walk(n) if isinstance(x,ast.Constant) and isinstance(x.value,str)))
 assert marks(oldexpr)==marks(newexpr)
 # Full module AST equality after substituting the one intended voiceover.
 a.args[0]=newexpr
 assert ast.dump(ot,include_attributes=False)==ast.dump(nt,include_attributes=False)
 if filename=='s01_hook.py':
  oldzh=z[oldkey];newzh="在第1部分，一个模型靠计数学会了猜下一个字母，然后撞上了一堵墙。它能共享完全相同的字母模式，但每个上下文仍是一座计数的孤岛。<bookmark mark='a'/>把the dog barked读上100遍，也不会让它学到dog和hound在意义上相近。"
 elif newintro:
  oldzh=z[oldkey];split="<bookmark mark='a'/>";newzh=newintro+split+oldzh.split(split,1)[1]
 else:
  oldzh=z[oldkey];oldpiece='一张满的表，第8章就有答案；有空洞就没有公式，只能沿梯度下降。'
  newpiece='第8章解决的是：对完整矩阵，不加正则化、按最小二乘做秩k近似。这里，我们只优化已观测的评分，同时保留向量和偏置惩罚。'
  assert oldpiece in oldzh;newzh=oldzh.replace(oldpiece,newpiece)
 assert marks(newexpr)==re.findall(r'<bookmark[^>]+/>',newzh)
 entries.append({'file':str(p.relative_to(root)),'method':method,'before_sha256':hashlib.sha256(before.read_bytes()).hexdigest(),'after_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'old_expression':ast.get_source_segment(old,oldexpr) if filename=='NONE' else ast.unparse(ast.parse(old).body[-1])[:0], 'old_voiceover_expression': next(ast.get_source_segment(old,n.args[0]) for n in calls(ast.parse(old)) if n.lineno==a.lineno),'new_voiceover_expression':ast.get_source_segment(new,newexpr),'old_mapping_key':oldkey,'new_mapping_key':newkey,'old_zh':oldzh,'new_zh':newzh,'bookmarks':marks(newexpr),'same_module_AST_except_one_voiceover_expression':True})
 entries[-1].pop('old_expression')
report={'status':'source frozen; shared translation merge pending parent','ownership':'Only s01_hook.py, s13_words.py and s18_netflix.py changed by reviewer; no shared table or tests changed.','zh_lines_sha256_at_handoff':hashlib.sha256(zp.read_bytes()).hexdigest(),'entries':entries,'timing_note':'All three narrator paragraphs have additional/changed wording. Prior rendered outputs/audio do not validate these new utterances. Bookmarks and scene actions/data are unchanged.'}
(out/'narration-handoff.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(out/'source.patch').write_text(subprocess.run(['git','diff','--','videos/ai/ai3/s01_hook.py','videos/ai/ai3/s13_words.py','videos/ai/ai3/s18_netflix.py'],cwd=root,capture_output=True,text=True,check=True).stdout)
print(json.dumps([{'file':x['file'],'after_sha256':x['after_sha256'],'bookmarks':x['bookmarks']} for x in entries],indent=2))
