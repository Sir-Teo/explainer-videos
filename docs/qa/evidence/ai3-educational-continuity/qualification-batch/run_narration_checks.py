from pathlib import Path
import importlib.util,json,unittest,copy,ast,re
import explainer.zh_templates as zt
root=Path('/workspace/explainer-videos');hand=json.loads((Path(__file__).parent/'narration-handoff.json').read_text());original=zt.table

def overlay(video):
 t=copy.deepcopy(original(video))
 if video=='ai3':
  for e in hand['entries']:
   if e['old_mapping_key']!=e['new_mapping_key']:t['ZH'].pop(e['old_mapping_key'],None)
   t['ZH'][e['new_mapping_key']]=e['new_zh']
 return t
zt.table=overlay
spec=importlib.util.spec_from_file_location('ai3_narration_tests',root/'tests/test_ai3_narration_review.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
suite=unittest.defaultTestLoader.loadTestsFromModule(m)
result=unittest.TextTestRunner(verbosity=2).run(suite)
assert result.wasSuccessful()
# Actual changed source paragraphs, using explicit non-measured numeric fixtures only.
translator=zt.Translator('ai3')
checks=[]
for e in hand['entries']:
 node=ast.parse('('+e['new_voiceover_expression']+'\n)',mode='eval').body
 fixtures={'m':{'users':4000,'items':1200,'n_ratings':123456}}
 en=eval(compile(ast.Expression(node),'changed-actual-voiceover','eval'),{},fixtures)
 zh=translator(en)
 assert zh is not None and re.findall(r'<bookmark[^>]+/>',en)==re.findall(r'<bookmark[^>]+/>',zh)
 if 'netflix' in e['file']:
  for q in ['不加正则化','最小二乘','秩k','完整矩阵','已观测','向量和偏置惩罚']:assert q in zh,q
  for q in ['4,000','1,200','123,456']:assert q.replace(',','') in zh.replace(',',''),q
 elif 'words' in e['file']:
  for q in ['字母符号','共享的上下文','1954','1957','1990']:assert q in zh,q
 else:
  for q in ['完全相同的字母模式','计数的孤岛','在意义上相近']:assert q in zh,q
 checks.append({'file':e['file'],'english':en,'chinese':zh,'numeric_values_are_non_measured_translation_fixtures':True,'bookmarks_preserved':True,'qualifiers_checked':True})
(Path(__file__).parent/'actual-changed-paragraph-translation-fixtures.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print('EXISTING10NARRATIONTESTS_PASS_WITH_PRIVATE_PROPOSED_ZH_OVERLAY; changed3paragraphs qualified and bookmark-correct; no shared source/table mutation')
