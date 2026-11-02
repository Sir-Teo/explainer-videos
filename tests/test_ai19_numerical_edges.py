"""Independent small-input checks; no shared model/cache generation."""

import numpy as np
import pytest

from videos.ai.ai19 import attn, formats, quant


@pytest.mark.parametrize("n", [1, 17, 63, 64, 65, 127, 130, 512, 131072])
@pytest.mark.parametrize("d", [32, 64, 128])
def test_attention_io_counts_only_actual_query_rows(n, d):
    memory = 228 * 1024 // 2
    _, key_tile = attn.flash_blocks(memory, d)
    key_visits = len(range(0, n, key_tile))
    # Each key/value element is fetched once. Every outer visit reads Q/O
    # and writes O, plus reads/writes the two row statistics.
    expected = 2 * n * d + key_visits * (3 * n * d + 4 * n)
    assert attn.io_flash_formula(n, d, memory) == expected
    assert attn.io_flash_counted(n, d, memory) == expected


@pytest.mark.parametrize("group", ["tensor", "row", 16, 32])
def test_zero_weights_quantize_to_finite_zero(group):
    weights = np.zeros((3, 35))
    with np.errstate(all="raise"):
        result = quant.rtn(weights, 4, group)
    np.testing.assert_array_equal(result, weights)


def test_zero_nvfp4_tensor_has_finite_decodable_codes():
    weights = np.zeros((3, 35))
    with np.errstate(all="raise"):
        result, detail = formats.nvfp4(weights, detail=True)
    np.testing.assert_array_equal(result, weights)
    assert detail["tensor_scale"] > 0
    assert np.isfinite(detail["block_scale"]).all()
    np.testing.assert_array_equal(formats.e2m1_value(detail["codes"]), 0)


def test_zero_mxfp4_picture_has_binary_shared_scale_and_zero_element_codes():
    picture = formats.block_picture(np.zeros(32))
    scale_bits = picture["mx_scale_bits"]
    assert len(scale_bits) == 8 and set(scale_bits) <= {"0", "1"}
    scale = 2.0 ** (int(scale_bits, 2) - 127)
    assert scale == 1
    assert all(code == "0000" for code in picture["mx_codes"])
    assert not picture["mx_clipped"]
    np.testing.assert_array_equal(picture["mx_decoded"], 0)


@pytest.mark.parametrize("value", [2.0**-149, 2.0**-127, 2.0**-126, 2.0**-125, 1.0, float(np.finfo(np.float32).max)])
def test_mxfp4_scale_bytes_decode_at_float32_domain_boundaries(value):
    picture = formats.block_picture(np.full(32, value))
    scale_bits = picture["mx_scale_bits"]
    assert len(scale_bits) == 8 and set(scale_bits) <= {"0", "1"}
    assert int(scale_bits, 2) < 255
    exponent = int(scale_bits, 2) - 127
    assert -127 <= exponent <= 127
    codes = np.array([int(code, 2) for code in picture["mx_codes"]])
    magnitudes = np.array([0, .5, 1, 1.5, 2, 3, 4, 6])
    decoded = np.where(codes & 8, -1, 1) * magnitudes[codes & 7] * 2.0**exponent
    np.testing.assert_array_equal(decoded, picture["mx_decoded"])


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), 2 * float(np.finfo(np.float32).max)])
def test_mxfp4_rejects_inputs_outside_its_declared_finite_domain(value):
    with pytest.raises(ValueError, match="finite.*Float32"):
        formats.mxfp4(np.full((1, 32), value))


@pytest.mark.parametrize("scale", ["fp16", "e4m3"])
def test_zero_integer_tensor_with_float_scales_stays_zero(scale):
    weights = np.zeros((3, 35))
    with np.errstate(all="raise"):
        result = formats.int4_scaled(weights, 16, scale)
    np.testing.assert_array_equal(result, weights)


@pytest.mark.parametrize("causal", [False, True])
@pytest.mark.parametrize("tiles", [(1, 1), (3, 5), (32, 32)])
def test_ragged_tiled_attention_matches_direct_softmax(causal, tiles):
    rng = np.random.default_rng(19)
    q, k, v = [rng.normal(size=(17, 8)) for _ in range(3)]
    scores = q @ k.T / np.sqrt(8)
    if causal:
        scores[np.triu_indices(17, 1)] = -np.inf
    weights = np.exp(scores - scores.max(axis=1, keepdims=True))
    expected = weights @ v / weights.sum(axis=1, keepdims=True)
    np.testing.assert_allclose(attn.flash_attention(q, k, v, *tiles, causal), expected, atol=1e-12)


def test_existing_published_io_sweep_is_unchanged():
    memory = 228 * 1024 // 2
    for n in [512 * 2 ** i for i in range(9)]:
        for d in [64, 128]:
            br, bc = attn.flash_blocks(memory, d)
            old = 2 * n * d + int(np.ceil(n / bc)) * int(np.ceil(n / br)) * (3 * br * d + 4 * br)
            assert attn.io_flash_formula(n, d, memory) == old
