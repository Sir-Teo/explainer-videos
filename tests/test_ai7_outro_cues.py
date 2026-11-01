"""Execute actual recap scheduling with fake drawings, without a renderer."""
import ast
from contextlib import contextmanager
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

import numpy as np


SOURCE = Path(__file__).resolve().parents[1] / 'videos/ai/ai7/s18_outro.py'


def schedule(method, expected_cues):
    tree = ast.parse(SOURCE.read_text())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Outro')
    function = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == method)
    events = []

    class Label:
        def to_edge(self, *args, **kwargs):
            return 'head'

    @contextmanager
    def voiceover(text):
        cues = re.findall(r"<bookmark mark='([^']+)'/>", text)
        if cues != list(expected_cues):
            raise AssertionError((cues, expected_cues))
        yield SimpleNamespace(wait_until=lambda cue: events.append(('cue', cue)))

    scene = SimpleNamespace(tiles=lambda: list(range(12)), voiceover=voiceover,
        play=lambda *animations, **kwargs: events.append(('draw', animations, kwargs)),
        wait=lambda *args: None, clear_scene=lambda: None)
    scope = dict(PART=7, UP=np.array([0., 1., 0.]), RIGHT=np.array([1., 0., 0.]),
                 label=lambda *args, **kwargs: Label(), FadeIn=lambda obj, **kwargs: obj,
                 payoff_card=lambda *args, **kwargs: SimpleNamespace(head='head', rows=list(range(8))))
    exec(compile(ast.Module([function], type_ignores=[]), str(SOURCE), 'exec'), scope)
    scope[method](scene)
    return events


class OutroConceptCues(unittest.TestCase):
    def assert_named_reveals(self, method, cues):
        events = schedule(method, cues)
        self.assertEqual(events[0], ('draw', ('head',), {'run_time': .35}))
        self.assertEqual(len(events), 1 + 2 * len(cues))
        for i, cue in enumerate(cues):
            self.assertEqual(events[1 + 2*i], ('cue', cue))
            self.assertEqual(events[2 + 2*i], ('draw', (i,), {'run_time': .35}))

    def test_each_of_twelve_recaps_is_revealed_at_its_named_concept(self):
        self.assert_named_reveals('recap', ['pca', 'ica', 'em', 'topics', 'hmm', 'alignment',
                                           'counting', 'graphs', 'causes', 'gp', 'optimization', 'vi'])

    def test_payoffs_follow_the_eight_named_destinations(self):
        self.assert_named_reveals('payoffs', ['alignment', 'state', 'experts', 'forward',
                                             'gp', 'elbo', 'causes', 'counting'])


if __name__ == '__main__':
    unittest.main()
