"""Real source expressions/template engine on synthetic fixtures; no render/cache imports."""
import ast
from pathlib import Path
import types
import unittest
ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'videos/ai/ai9'

def engine():
    tree=ast.parse((ROOT/'explainer/zh_templates.py').read_text())
    tree.body=[n for n in tree.body if not(isinstance(n,ast.ImportFrom) and n.module=='explainer.paths')]
    module=types.ModuleType('ai9_math_translation_engine');module.video_dir=lambda _:PART
    exec(compile(tree,'actual-template-engine','exec'),module.__dict__)
    tables={'ZH':{},'PHRASES':{},'TITLE':'','CHAPTERS':{}}
    for filename in ('zh_lines.py','math_zh_overrides.py'):
        for node in ast.parse((PART/filename).read_text()).body:
            if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id in tables:
                key=node.targets[0].id
                if isinstance(tables[key],dict):tables[key].update(ast.literal_eval(node.value))
                else:tables[key]=ast.literal_eval(node.value)
            if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call):
                call=node.value
                if isinstance(call.func,ast.Attribute) and isinstance(call.func.value,ast.Name) and call.func.value.id in tables and call.args and isinstance(call.args[0],ast.Dict):
                    tables[call.func.value.id].update(ast.literal_eval(call.args[0]))
    module.table=lambda _:tables
    return module.Translator('ai9')

def assignment(filename,function,name,env):
    fn=next(n for n in ast.walk(ast.parse((PART/filename).read_text())) if isinstance(n,ast.FunctionDef) and n.name==function)
    expr=next(n.value for n in ast.walk(fn) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name)and t.id==name for t in n.targets))
    return eval(compile(ast.Expression(expr),'actual-scene-expression','eval'),env)

class MathNarration(unittest.TestCase):
    def test_both_measured_weight_gradient_change_directions_translate(self):
        tr=engine()
        for fade,word in [(1.,'缩小'),(-1.,'增大'),(0.,'缩小')]:
            en=assignment('s12_residual.py','inside','fade_words',{'fade':fade})
            zh=tr(en)
            self.assertIsNotNone(zh,en)
            self.assertIn(word,zh)
            self.assertIn(f'{10 ** abs(fade):.1f}',zh)
    def test_geometric_mean_qualifier_and_nested_direction_translate_together(self):
        fn=next(n for n in ast.walk(ast.parse((PART/'s12_residual.py').read_text())) if isinstance(n,ast.FunctionDef) and n.name=='inside')
        voice=next(n.args[0] for n in ast.walk(fn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='voiceover')
        for fade,word in [(1.,'缩小'),(-1.,'增大')]:
            direction=assignment('s12_residual.py','inside','fade_words',{'fade':fade})
            en=eval(compile(ast.Expression(voice),'actual-narration','eval'),{'big':'a hundred','rr':2.,'fade_words':direction})
            zh=engine()(en)
            self.assertIn('geometric mean',en)
            self.assertIn('几何平均值',zh)
            self.assertIn(word,zh)
            self.assertNotIn('factor',zh)

    def test_gpt2_history_uses_residual_layer_count_in_both_languages(self):
        fn=next(n for n in ast.walk(ast.parse((PART/'s12_residual.py').read_text())) if isinstance(n,ast.FunctionDef) and n.name=='paths')
        voice=next(n.args[0] for n in ast.walk(fn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='voiceover')
        en=eval(compile(ast.Expression(voice),'actual-history-narration','eval'),{})
        zh=engine()(en)
        self.assertIn('number of residual layers',en)
        self.assertIn('残差层数量',zh)
        self.assertNotIn("stream doesn't grow with depth",en)
        self.assertNotIn('不会随深度变大',zh)

    def test_actual_finite_budget_predicate_translates_criterion_and_budget(self):
        en=assignment('s11_chaos.py','trainable','verdict',{'t':{'steps':300},'agree':.76})
        zh=engine()(en)
        self.assertIsNotNone(zh)
        for text in ['300','50%','76%','不是精确']:
            self.assertIn(text,zh)

if __name__=='__main__':unittest.main()
