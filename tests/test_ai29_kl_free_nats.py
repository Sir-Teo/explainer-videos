"""Free-nats clamping makes the KL gradient zero below the floor, not the loss."""
import ast
import hashlib
import json
from pathlib import Path
import re
import unittest
import torch

ROOT = Path(__file__).resolve().parents[1]

class FreeNatsClaim(unittest.TestCase):
    def test_floor_has_nonzero_value_and_zero_gradient_below_threshold(self):
        kl = torch.tensor(0.4, requires_grad=True)
        value = torch.clamp(kl, min=1.0)
        value.backward()
        self.assertEqual(value.item(), 1.0)
        self.assertEqual(kl.grad.item(), 0.0)
        kl2 = torch.tensor(1.4, requires_grad=True)
        torch.clamp(kl2, min=1.0).backward()
        self.assertEqual(kl2.grad.item(), 1.0)

    def test_dream_strip_labels_the_number_of_shown_frames(self):
        src = (ROOT / 'videos/ai/ai29/s13_dreamer.py').read_text()
        tree = ast.parse(src)
        fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'imagine')
        text = ast.unparse(fn)
        self.assertIn('own[:12]', text)
        self.assertIn('min(12, len(own))', text)
        self.assertIn('imagined steps', text)
        self.assertIn('帧', text)

    def test_explanation_and_translation_avoid_guaranteeing_no_collapse(self):
        src = (ROOT / 'videos/ai/ai29/s13_dreamer.py').read_text()
        tree = ast.parse(src)
        fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'loss')
        call = next(n for n in ast.walk(fn) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute) and n.func.attr == 'voiceover')
        en = ast.literal_eval(call.args[0])
        self.assertIn('clamped KL term has zero gradient', en)
        self.assertIn('does not guarantee', en)
        key = hashlib.sha1(' '.join(en.split()).encode()).hexdigest()[:12]
        row = json.loads((ROOT / 'videos/ai/ai29/narration_zh.json').read_text())['lines'][key]
        self.assertEqual(row['en'], en)
        self.assertIn('梯度为零', row['zh'])
        self.assertIn('不保证', row['zh'])
        self.assertEqual(re.findall(r"<bookmark mark='([^']+)'/>", en),
                         re.findall(r"<bookmark mark='([^']+)'/>", row['zh']))

if __name__ == '__main__':
    unittest.main()
