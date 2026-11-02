"""The timeline must distinguish prefill from decode without changing service."""

import pytest

from videos.ai.ai19 import serve


@pytest.mark.parametrize("chunk", [0, 4])
def test_continuous_trace_never_paints_decode_over_own_prefill(chunk):
    requests = [serve.Req(0, 0, 8, 3), serve.Req(1, 1, 9, 4)]
    cost = serve.Cost(1, 0.1, 0.01, 0.2)
    trace = []
    result = serve.run_continuous(requests, cost, 2, chunk=chunk, trace=trace)
    untraced = serve.run_continuous(requests, cost, 2, chunk=chunk)
    assert [r.__dict__ for r in result] == [r.__dict__ for r in untraced]
    for request in result:
        prefill = [row for row in trace if row[4] == request.rid and row[3] == "prefill"]
        decode = [row for row in trace if row[4] == request.rid and row[3] == "decode"]
        assert max(row[2] for row in prefill) == request.first
        assert len(decode) == 1
        assert decode[0][1:3] == (request.first, request.finish)


def test_simple_case_has_analytically_known_phase_boundary():
    trace = []
    request, = serve.run_continuous([serve.Req(0, 0, 8, 3)], serve.Cost(1, 0, 0, 1), 1, trace=trace)
    assert trace == [(0, 0, 9, "prefill", 0), (0, 9, 11, "decode", 0)]
    assert (request.first, request.finish) == (9, 11)
