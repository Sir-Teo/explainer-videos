"""The fast plain-text path must preserve greedy line breaks and punctuation."""
import pytest

from explainer.analysis import _plain_wrap_lines, _tex_words


def linear(words, limit, measure):
    lines, cur = [], words[0][1]
    for sep, word in words[1:]:
        trial = cur + sep + word
        if measure(trial) <= limit:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


@pytest.mark.parametrize('text', [
    '共同条件均值、有界观测。每方向分配误差，网格交点向外取界。',
    '20个种子的平均FDP及最小至最大范围；每21天评审一次。',
    '不能拆分的longword，保留标点。另起一行！',
])
def test_fast_wrapping_matches_linear_oracle(text):
    words = _tex_words(text)
    for limit in range(1, 50):
        measure = lambda s: sum(2 if '\u4e00' <= c <= '\u9fff' else 1 for c in s)
        assert _plain_wrap_lines(words, limit, measure) == linear(words, limit, measure)


def test_long_chinese_paragraph_uses_fewer_measurements():
    words = _tex_words('有界观测与共同条件均值。' * 50)
    calls = []
    result = _plain_wrap_lines(words, 35, lambda s: calls.append(s) or len(s))
    assert result == linear(words, 35, len)
    assert len(calls) < len(words) // 2
