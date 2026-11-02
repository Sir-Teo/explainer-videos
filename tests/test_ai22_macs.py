"""Count the attention products even when CPU inference fuses them."""
import ast
from pathlib import Path
import unittest

try:
    import torch
except ImportError:
    torch = None


def counting_functions():
    path = Path(__file__).resolve().parents[1] / "videos/ai/ai22/vision.py"
    tree = ast.parse(path.read_text())
    body = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {"_cpu_attention_flops", "macs"}]
    namespace = {}
    exec(compile(ast.Module(body=body, type_ignores=[]), str(path), "exec"), namespace)
    return namespace["macs"], namespace["_cpu_attention_flops"]


@unittest.skipIf(torch is None, "PyTorch is required for operation-count checks")
class MatrixOperationCounts(unittest.TestCase):
    def test_attention_count_is_independent_of_inference_fusion(self):
        macs, _ = counting_functions()

        class Attention(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.attention = torch.nn.MultiheadAttention(8, 2, dropout=0.0, batch_first=True)

            def forward(self, x):
                return self.attention(x, x, x, need_weights=False)[0]

        net = Attention()
        x = torch.ones(1, 3, 8)
        weights = {k: v.clone() for k, v in net.state_dict().items()}
        rng = torch.get_rng_state().clone()
        initial = torch.backends.mha.get_fastpath_enabled()
        try:
            for fastpath in (True, False):
                torch.backends.mha.set_fastpath_enabled(fastpath)
                for training in (True, False):
                    net.train(training)
                    # 576 QKV + 192 output projection + 144 attention QK/AV MACs.
                    self.assertEqual(macs(net, x), 912)
                    self.assertEqual(torch.backends.mha.get_fastpath_enabled(), fastpath)
                    self.assertEqual(net.training, training)
                    self.assertTrue(torch.equal(rng, torch.get_rng_state()))
                    self.assertTrue(all(torch.equal(v, net.state_dict()[k]) for k, v in weights.items()))
        finally:
            torch.backends.mha.set_fastpath_enabled(initial)

    def test_backend_flag_is_restored_when_forward_fails(self):
        macs, _ = counting_functions()

        class Failing(torch.nn.Module):
            def forward(self, x):
                raise RuntimeError("deliberate forward failure")

        initial = torch.backends.mha.get_fastpath_enabled()
        try:
            for fastpath in (True, False):
                torch.backends.mha.set_fastpath_enabled(fastpath)
                with self.assertRaisesRegex(RuntimeError, "deliberate forward failure"):
                    macs(Failing(), torch.ones(1, 3, 8))
                self.assertEqual(torch.backends.mha.get_fastpath_enabled(), fastpath)
        finally:
            torch.backends.mha.set_fastpath_enabled(initial)

    def test_rectangular_attention_shape_count(self):
        _, flops = counting_functions()
        # Two batches, four heads, three queries, five keys; widths eight and twelve.
        self.assertEqual(flops((2, 4, 3, 8), (2, 4, 5, 8), (2, 4, 5, 12)), 4800)
        with self.assertRaises(ValueError):
            flops((2, 4, 3, 8), (2, 4, 5, 7), (2, 4, 5, 12))


if __name__ == "__main__":
    unittest.main()
