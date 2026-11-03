"""Synthetic cue/layout contracts; actual visual acceptance requires retained native frames."""
import ast
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'videos/ai/ai29/s03_belief.py'
TREE = ast.parse(SOURCE.read_text())
CLASS = next(n for n in TREE.body if isinstance(n, ast.ClassDef) and n.name == 'Belief')
METHODS = {n.name: n for n in CLASS.body if isinstance(n, ast.FunctionDef)}


class BeliefVisualContracts(unittest.TestCase):
    def test_definition_labels_are_inside_the_loop(self):
        assignments = {n.targets[0].id: n.value for n in METHODS['define'].body
                       if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
        for name, arrow, direction in [('l1', 'a1', 'LEFT'), ('l2', 'a2', 'RIGHT')]:
            call = assignments[name]
            self.assertEqual(call.func.attr, 'next_to')
            self.assertEqual([x.id for x in call.args], [arrow, direction])
            self.assertEqual(next(k.value.value for k in call.keywords if k.arg == 'buff'), 0.15)

    def test_both_sensor_results_are_opaque_and_held(self):
        loop = next(n for n in ast.walk(METHODS['corridor']) if isinstance(n, ast.For)
                    and isinstance(n.iter, ast.Call) and isinstance(n.iter.func, ast.Name)
                    and n.iter.func.id == 'range' and isinstance(n.iter.args[0], ast.Constant)
                    and n.iter.args[0].value == 4)
        start = next(i for i, n in enumerate(loop.body) if isinstance(n, ast.Assign)
                     and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'cue')
        code = compile(ast.Module(body=loop.body[start:], type_ignores=[]), str(SOURCE), 'exec')
        class Cue:
            def __init__(self, text, **kwargs):
                self.text, self.opacity, self.kwargs = text, 1, kwargs
            def next_to(self, position, direction, **kwargs):
                self.position = position
                return self
        for seen, text, color in [(False, 'no door', 'grey'), (True, 'door!', 'yellow')]:
            events = []
            scene = SimpleNamespace(
                add=lambda cue: events.append(('add', cue)),
                play=lambda *anims, **kw: events.append(('play', anims, kw)),
                wait=lambda duration: events.append(('wait', duration)),
                remove=lambda cue: events.append(('remove', cue)),
            )
            ns = dict(Text=Cue, C=SimpleNamespace(BITS='yellow'), GREY_B='grey', DOWN='down',
                      self=scene, t=4, obs=[False, False, False, seen], pos=[0, 1, 2, 3, 4],
                      x0=-6, cw=.3, anims=['posterior', 'robot', 'entropy'])
            exec(code, ns)
            self.assertEqual([event[0] for event in events], ['add', 'play', 'wait', 'remove'])
            cue = events[0][1]
            self.assertEqual((cue.text, cue.opacity, cue.kwargs['color']), (text, 1, color))
            self.assertEqual(cue.position, [-4.65, -.95, 0])
            self.assertEqual(events[1][1], ('posterior', 'robot', 'entropy'))
            self.assertEqual(events[1][2]['run_time'], .24)
            self.assertEqual(events[2][1], .16)
            self.assertIs(events[3][1], cue)

    def test_existing_sensor_caption_translations_and_input_scope(self):
        shared = json.loads((ROOT / 'videos/ai/ai_text_zh.json').read_text())['strings']
        self.assertEqual(shared['door!'], '有门！')
        self.assertEqual(shared['no door'], '没有门')
        for method, expected in [('define', []), ('corridor', ['belief'])]:
            loads = [n.args[0].value for n in ast.walk(METHODS[method]) if isinstance(n, ast.Call)
                     and isinstance(n.func, ast.Name) and n.func.id == 'load']
            self.assertEqual(loads, expected)


if __name__ == '__main__':
    unittest.main()
