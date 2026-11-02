"""A small synthetic model checks the algebra; it is not a trained-series outcome."""

import torch

from explainer.lm.pocket import Config, PocketGPT
from videos.ai.ai19.quant import hadamard, rotate


def test_folding_unequal_norm_gains_preserves_rotated_model_function():
    torch.manual_seed(19)
    torch.set_num_threads(1)
    model = PocketGPT(Config(vocab=17, d=16, layers=1, heads=2, seq=16)).eval()
    with torch.no_grad():
        for norm in [model.blocks[0].n1, model.blocks[0].n2, model.norm]:
            norm.weight.copy_(torch.linspace(0.4, 1.8, 16))
        tokens = torch.randint(0, 17, (2, 11))
        expected = model(tokens)
        rotated = rotate(model, hadamard(16))
        torch.testing.assert_close(rotated(tokens), expected, atol=2e-6, rtol=2e-5)
        # Rotation works on a copy; the source model's unequal gains survive.
        torch.testing.assert_close(model.norm.weight, torch.linspace(0.4, 1.8, 16))
