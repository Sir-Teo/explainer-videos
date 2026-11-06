import unittest

from explainer.cs.search import index, links, rank, text

DOCS = [(0, "A", "the white whale swam in the sea"), (1, "A", "a whale and a ship"),
        (2, "B", "the sea the sea the sea"), (3, "B", "white sails on the ship"),
        (4, "C", "call me ishmael the white whale")]


class Text(unittest.TestCase):
    def test_porter(self):
        self.assertTrue(all(ok for _, _, ok in text.check_porter().values()))


class Index(unittest.TestCase):
    def setUp(self):
        self.post, self.lengths = index.build(DOCS)

    def test_intersections_agree(self):
        a, b = list(range(0, 1000, 3)), list(range(0, 1000, 7))
        m, _ = index.merge(a, b)
        self.assertEqual(m, index.skips(a, b)[0])
        self.assertEqual(m, index.gallop(a, b)[0])
        self.assertEqual(m, list(range(0, 1000, 21)))

    def test_phrase(self):
        self.assertEqual([d for d, _ in index.phrase(self.post, ["white", "whale"])], [0, 4])

    def test_codes(self):
        self.assertEqual(index.gamma_code(9), "0001001")
        self.assertEqual(len(index.gamma_code(9)), index.gamma_bits(9))
        self.assertEqual(len(index.delta_code(9)), index.delta_bits(9))
        self.assertEqual(len(index.rice_code(9, 2)), index.rice_bits(9, 2))


class Rank(unittest.TestCase):
    def test_wand_matches_exhaustive(self):
        post, lengths = index.build(DOCS)
        q = [text.porter("white"), text.porter("whale")]
        w = rank.wand(post, lengths, q, k=2)
        self.assertEqual(w["top"], rank.top(rank.bm25_scores(post, lengths, q), 2))

    def test_ndcg(self):
        self.assertAlmostEqual(rank.ndcg([1, 2], {1: 2, 2: 1}), 1.0)


class Links(unittest.TestCase):
    def test_pagerank_sums_to_one(self):
        out, N, _, _ = links.synthetic_web(n=60, farm=5)
        r, _ = links.pagerank(out, N)
        self.assertAlmostEqual(float(r.sum()), 1.0, places=6)

    def test_edit_distance(self):
        self.assertEqual(links.edit_distance("captian", "captain"), 2)
        self.assertEqual(links.BKTree(["captain", "cap", "whale"]).near("captian", 2)[0][1], "captain")


if __name__ == "__main__":
    unittest.main()
