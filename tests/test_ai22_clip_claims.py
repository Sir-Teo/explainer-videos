"""Clip conclusions are scoped to the observed toy wobble comparison."""
import ast
from pathlib import Path
import re
import unittest
import numpy as np
from tools.zh_lines import Translator
from unittest.mock import patch
from explainer import lang

ROOT = Path(__file__).resolve().parents[1]

class ClipClaims(unittest.TestCase):
    def test_all_outcome_branches_translate_without_overclaiming(self):
        src = ROOT / 'videos/ai/ai22/s14_clips.py'
        tree = ast.parse(src.read_text())
        fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'agree')
        branches = [n for n in fn.body if isinstance(n, ast.If) and any(
            isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ('verdict','close') for t in x.targets)
            for x in ast.walk(n))]
        self.assertEqual(len(branches), 2)
        call = next(n for n in ast.walk(fn) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute) and n.func.attr == 'voiceover')
        translate = Translator('ai22')
        for jr, ir, jj, ij in [(.8,.6,1.,2.), (.02,.01,1.,2.), (.3,.4,2.,1.)]:
            env = {k: np.array([v,v,v]) for k,v in dict(jr=jr, ir=ir, jj=jj, ij=ij).items()}
            exec(compile(ast.Module(branches, type_ignores=[]), str(src), 'exec'), env)
            en = eval(compile(ast.Expression(call.args[0]), str(src), 'eval'), env)
            zh = translate(en)
            self.assertIsNotNone(zh)
            with patch.object(lang, 'LANG', 'zh'):
                actual = lang.translate(en, ROOT / 'videos/ai/ai22', 'Clips')
            self.assertEqual(actual, lang.zh_numbers(zh))
            self.assertIn('toy comparison', en)
            self.assertIn('玩具对比', zh)
            self.assertNotIn('makes the frames agree', en)
            self.assertEqual(re.findall(r"<bookmark mark='([^']+)'/>", en),
                             re.findall(r"<bookmark mark='([^']+)'/>", zh))

if __name__ == '__main__':
    unittest.main()
