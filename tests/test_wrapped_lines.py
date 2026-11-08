"""Text wrapping preserves greedy breaks without compiling each prefix."""

import pytest

from explainer.analysis import _tex_words, _wrapped_lines


def linear(words, limit, measure):
    lines, current = [], words[0][1]
    for sep, word in words[1:]:
        trial = current + sep + word
        if measure(trial) <= limit:
            current = trial
        else:
            lines.append(current)
            current = word
    return lines + [current]


@pytest.mark.parametrize("text", [
    "premises and conclusions have different logical roles",
    "如果所有独角兽都是马，那么有些马是否一定是独角的？",
    r"the $x^2 = x$ law and \textit{its consequence} follow from these assumptions",
    r"true\ premises and a false conclusion",
    "oversizedword a b c d",
])
@pytest.mark.parametrize("limit", [1, 5, 12, 20, 40])
def test_same_breaks_as_greedy(text, limit):
    words = _tex_words(text)
    assert _wrapped_lines(words, limit, len) == linear(words, limit, len)


def test_long_cjk_paragraph_needs_fewer_width_probes():
    words = _tex_words("哲学的论证需要清楚地区分前提与结论。" * 20)
    probes = []

    def measure(s):
        probes.append(s)
        return len(s)

    assert _wrapped_lines(words, 60, measure) == linear(words, 60, len)
    assert len(probes) < len(words) // 3


def test_cjk_estimate_is_verified_with_proportional_punctuation():
    words = _tex_words("哲学，为什么？因为每一个论证都需要前提……以及结论。" * 3)

    def measure(s):
        return sum(0.4 if c in "，？。…" else 1.0 for c in s)

    for limit in (0.1, 3.5, 7.0, 12.3):
        assert _wrapped_lines(words, limit, measure) == linear(words, limit, measure)
