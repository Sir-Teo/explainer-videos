"""Monochord's studio (Part 53): MIDI bytes, files, the engine's block independence, patterns and canons.

    python -m pytest -q tests/music/test_daw.py
"""

import numpy as np
import pytest

from explainer.music.monochord import daw as W

SR = 48000


def test_messages_and_running_status():
    msgs = [W.note_on(0, 60, 100), W.note_on(0, 64, 100), W.note_off(0, 60), W.control(1, 7, 90), W.bend(1, 12288)]
    plain = W.encode(msgs, running=False)
    run = W.encode(msgs)
    assert plain[:3] == bytes([0x90, 60, 100]) and len(plain) == 15 and len(run) == 13
    dec = W.decode(run)
    assert [d[0] for d in dec] == ["on", "on", "off", "cc", "bend"]
    assert dec[4][2] + 128 * dec[4][3] == 12288


def test_wire_time():
    t = W.wire_times(bytes(3))
    assert t[-1] == pytest.approx(3 * 10 / 31250)


def test_vlq_round_trip():
    for n in (0, 1, 127, 128, 480, 16383, 16384, 2 ** 21, 0x0FFFFFFF):
        b = W.vlq(n)
        assert W.unvlq(b, 0) == (n, len(b))
        assert len(b) == max(1, -(-n.bit_length() // 7))


def test_smf_round_trip():
    tr = [(0, W.note_on(0, 60, 90)), (240, W.note_off(0, 60)), (480, W.note_on(0, 67, 90)), (960, W.note_off(0, 67))]
    data = W.write_smf([tr], division=480, tempo_us=600000)
    back = W.read_smf(data)
    assert back["division"] == 480 and back["tempo_us"] == 600000 and back["tracks"] == 2
    ons = [(t, m[1]) for t, m, s in back["events"] if m[0] & 0xF0 == 0x90 and m[2] > 0]
    assert ons == [(0, 60), (480, 67)]
    assert back["events"][-1][2] == pytest.approx(960 * 0.6 / 480)


def test_engine_is_block_independent():
    ev = [(int(i * 0.19 * SR) + 11, 55 + i % 7, 0.7, int(0.15 * SR), "a" if i % 2 else "b") for i in range(12)]
    def make():
        return W.Engine(ev, tracks={"a": {"cut": 2000.0, "chain": [W.Limiter(64, 0.1)]}, "b": {"cut": 900.0, "chain": [W.Delay(300)]}})
    ref = make().render(3 * SR)
    for B in (17, 64, 500, 4096):
        assert np.array_equal(make().render(3 * SR, B), ref)


def test_quantized_engine_moves_notes_to_block_starts():
    ev = [(1000, 60, 0.8, 2000, "main")]
    a = W.Engine(ev, quantize=True).render(4096, 1024)
    first = np.argmax(np.abs(a) > 0)
    assert first == 1000 - 1000 % 1024 + 1 or first == 0


def test_limiter_latency_and_ceiling():
    x = np.zeros(2000)
    x[500] = 1.0
    x[900:1200] = 0.05
    lim = W.Limiter(64, ceiling=0.25)
    y = lim.process(x.copy())
    assert np.max(np.abs(y)) <= 0.25 + 1e-9 and np.argmax(np.abs(y)) == 564


def test_patterns():
    ev = W.pattern_events("c4 [e4 g4] ~ <a4 b4>", 2, 2.0)
    assert [(round(a, 3), s) for a, d, s in ev] == [(0.0, "c4"), (0.5, "e4"), (0.75, "g4"), (1.5, "a4"), (2.0, "c4"), (2.5, "e4"), (2.75, "g4"), (3.5, "b4")]
    assert W.note_number("c4") == 60 and W.note_number("a4") == 69 and W.note_number("f#3") == 54
    assert len(W.pattern_events("bd*4", 1)) == 4


def test_tempo_canon_converges():
    notes = [(60, 0.0, 1.0), (62, 1.0, 1.0), (64, 2.0, 2.0)]
    ev, T = W.tempo_canon(notes, [1.0, 1.5, 2.0], 2)
    at = [a for v, k, a, d in ev if k == 64]
    assert np.allclose(at, T) and min(a for v, k, a, d in ev) == pytest.approx(0.0)
