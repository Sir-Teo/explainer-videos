"""Synthetic checks of the constrained-record automaton, without model or corpus assets."""
import random
import string
import unittest
import numpy as np
from videos.ai.ai19 import grammar as G

class GrammarSynthetic(unittest.TestCase):
    def test_generated_records_match_regex_and_terminate(self):
        rng = random.Random(1929)
        machine = G.Automaton(G.RECORD)
        for _ in range(500):
            name = rng.choice(string.ascii_uppercase) + ''.join(rng.choice(string.ascii_lowercase)
                                                                  for _ in range(rng.randint(1, 11)))
            text = '{"name": "' + name + '", "age": ' + str(rng.randint(1, 99)) + '}'
            state = machine.run(machine.start, text)
            self.assertIsNotNone(state)
            self.assertTrue(machine.accepting(state))
            self.assertTrue(machine.final(state))
            self.assertIsNotNone(G.RECORD_RE.fullmatch(text))
            self.assertIsNone(machine.run(state, 'x'))

    def test_mutations_match_regular_expression(self):
        rng = random.Random(1930)
        machine = G.Automaton(G.RECORD)
        seeds = G.EXAMPLES + ['{"name": "Ab", "age": 1}', '{"name": "Abcdefghijkl", "age": 99}']
        chars = string.ascii_letters + string.digits + ' {},:"\n!'
        for _ in range(1200):
            text = rng.choice(seeds)
            i = rng.randrange(len(text))
            mode = rng.randrange(3)
            text = text[:i] + ('' if mode == 0 else rng.choice(chars)) + text[i + (mode != 2):]
            state = machine.run(machine.start, text)
            accepted = state is not None and machine.accepting(state)
            self.assertEqual(accepted, bool(G.RECORD_RE.fullmatch(text)), text)

    def test_token_index_matches_character_execution(self):
        machine = G.Automaton(G.RECORD)
        tokens = [None, '{"name": "', 'A', 'b', 'z', '", "age": ', '1', '9', '0', '}', 'bad', 'Ab', '99}']
        table, order = G.build_index(machine, tokens)
        self.assertEqual(table.shape, (len(order), len(tokens)))
        for i, state in enumerate(order):
            for t, token in enumerate(tokens):
                target = None if token is None else machine.run(state, token)
                if target is None:
                    self.assertEqual(table[i,t], -1)
                else:
                    self.assertEqual(order[table[i,t]], target)

    def test_masking_and_global_conditioning_are_normalized(self):
        probs = {'A': .25, 'B': .25, 'a': .2, 'b': .1, ' ': .2}
        exact, masked = G.masked_vs_exact(lambda prefix: probs, names=['A', 'Aa', 'Ab', 'B'])
        self.assertAlmostEqual(sum(exact.values()), 1.0)
        self.assertAlmostEqual(sum(masked.values()), 1.0)
        self.assertTrue(all(np.isfinite(v) and 0 <= v <= 1 for v in (*exact.values(), *masked.values())))
        self.assertNotEqual(exact, masked)

if __name__ == '__main__':
    unittest.main()
