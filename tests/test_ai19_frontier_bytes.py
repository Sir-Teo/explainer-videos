"""Mixed precision accounting from published component counts, not a benchmark."""

import pytest

from videos.ai.ai19.facts import GPT_OSS_20B, gpt_oss_active_weight_bytes


def test_only_active_experts_receive_mxfp4_byte_rate():
    # Table 1's rounded counts: selected experts 19.12B * 4/32 = 2.39B;
    # remaining active weights = 1.22B, kept in BF16.
    expected = 2.39e9 * (4 + 8 / 32) / 8 + 1.22e9 * 2
    assert gpt_oss_active_weight_bytes(GPT_OSS_20B) == pytest.approx(expected)
    assert 153e9 / expected == pytest.approx(41.243364501, rel=1e-6)


def test_mixed_precision_reduces_to_bf16_when_expert_format_is_bf16():
    model = dict(GPT_OSS_20B, mxfp4_bits=16)
    assert gpt_oss_active_weight_bytes(model) == pytest.approx(2 * model["active"])


def test_thinking_cost_scores_each_decode_context_once(monkeypatch):
    import numpy as np
    from videos.ai.ai19 import compute

    products = {
        "roof": {"read_bw": 1e9},
        "phases": {"sizes": {"read": 1}, "decode_tps": [1]},
        "economics": {"kv_tok": 1, "weights": 1},
    }
    monkeypatch.setattr(compute, "load", products.__getitem__)
    contexts = []

    def unit_cost(*args):
        ctx = args[5]
        contexts.append(ctx)
        return np.ones_like(ctx), None, None

    monkeypatch.setattr(compute, "roofline_step", unit_cost)
    result = compute.compute_frontier()["thinking"]
    for ctx, item in zip(contexts, result.values()):
        n = item["n"]
        np.testing.assert_array_equal(ctx, np.arange(500, 500 + n))
        assert item["seconds"] == n
        assert item["avg_ctx"] == 500 + (n - 1) / 2
