"""Domain randomization describes an average objective, not a transfer guarantee."""
import ast
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class DomainRandomizationClaim(unittest.TestCase):
    def test_narration_and_chinese_mapping_preserve_caveat_and_cues(self):
        tree = ast.parse((ROOT / 'videos/ai/ai29/s15_sim2real.py').read_text())
        fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'randomize')
        call = next(n for n in ast.walk(fn) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute) and n.func.attr == 'voiceover')
        en = ast.literal_eval(call.args[0])
        self.assertIn('does not guarantee success', en)
        self.assertNotIn('it works there too', en)
        key = hashlib.sha1(' '.join(en.split()).encode()).hexdigest()[:12]
        row = json.loads((ROOT / 'videos/ai/ai29/narration_zh.json').read_text())['lines'][key]
        self.assertEqual(row['en'], en)
        self.assertIn('并不保证成功', row['zh'])
        cues = lambda t: re.findall(r"<bookmark mark='([^']+)'/>", t)
        self.assertEqual(cues(en), cues(row['zh']))
        self.assertEqual(cues(en), ['a', 'b', 'c'])

    def test_simulated_cartpole_is_not_presented_as_physical_evidence(self):
        src = (ROOT / 'videos/ai/ai29/s15_sim2real.py').read_text()
        self.assertIn('Our test cart-pole is another simulation', src)
        self.assertIn('simulated test cart-pole', src)
        self.assertIn("simulated test system's delay and noise", src)
        self.assertNotIn('Our real cart-pole is a different machine', src)
        self.assertNotIn('In a typical episode on the real cart-pole', src)
        self.assertIn('dashed: performance in nominal simulator', src)
        chinese = (ROOT / 'videos/ai/ai29/zh_lines.py').read_text()
        self.assertIn('我们的测试倒立摆也是仿真', chinese)
        self.assertIn('模拟的测试倒立摆', chinese)

    def test_card_in_both_languages_states_transfer_is_not_guaranteed(self):
        src = (ROOT / 'videos/ai/ai29/s15_sim2real.py').read_text()
        self.assertIn('but does not guarantee it', src)
        self.assertIn('但不能保证成功', src)

if __name__ == '__main__':
    unittest.main()
