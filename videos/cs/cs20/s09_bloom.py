from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)

M = 32


def bit_array(y=0.6, w=0.36):
    cells = VGroup()
    for i in range(M):
        sq = Square(side_length=w, stroke_color=GREY_C, stroke_width=1.2, fill_color=GREY_E, fill_opacity=0.6)
        cells.add(VGroup(sq, mono("0", 14, GREY_B).move_to(sq)))
    cells.arrange(RIGHT, buff=0.02).move_to([0, y, 0])
    idx = VGroup(*[mono(str(i), 10, GREY_D).next_to(c, DOWN, buff=0.06) for i, c in enumerate(cells)])
    return cells, idx


class Bloom(VoiceoverScene):
    def construct(self):
        self.card()
        self.tiny()
        self.derive()
        self.measured()

    def card(self):
        card = chapter_card(8, r"Bloom filters", r"Can a set forget its members and still answer?", lit=(1970,),
                            extra=((1970, r"Bloom's filter"),), part=PART)
        with self.voiceover("Chapter eight. Bloom filters."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tiny(self):
        d = load("bloom")
        head = label(r"32 bits, \ 3 hash functions", font_size=34).to_edge(UP, buff=0.35)
        cells, idx = bit_array()
        on = set()
        with self.voiceover(
            "In 1970 Burton Bloom asked how to test membership in a set using far less memory than the set "
            "itself, if we accept an occasional wrong yes. <bookmark mark='a'/> Take an array of bits, all zero, "
            "and three hash functions. <bookmark mark='b'/> To add a word, hash it three times and set those three "
            "bits. Here go six words from Moby-Dick. <bookmark mark='c'/> The words themselves are not stored "
            "anywhere. Only bits remain."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(idx))
            vo.wait_until("b")
            for w, ix in d["tiny_idx"].items():
                tag = label(rf"\texttt{{{w}}}", font_size=24, color=DATA).move_to(UP * 2.2)
                arrows = VGroup(*[Arrow(tag.get_bottom(), cells[i].get_top(), buff=0.08, stroke_width=2,
                                        color=DATA, max_tip_length_to_length_ratio=0.06) for i in ix])
                self.play(FadeIn(tag), *[GrowArrow(a) for a in arrows], run_time=0.6)
                anims = []
                for i in ix:
                    on.add(i)
                    anims.append(cells[i][0].animate.set_fill(DATA, 0.85))
                    anims.append(Transform(cells[i][1], mono("1", 14, WHITE).move_to(cells[i][0])))
                self.play(*anims, run_time=0.4)
                self.play(FadeOut(tag), FadeOut(arrows), run_time=0.3)
            vo.wait_until("c")
            fill = label(rf"{len(on)} of 32 bits set", font_size=22, color=GREY_A).to_edge(DOWN, buff=1.6)
            self.play(FadeIn(fill))
        self.wait(0.3)
        q = d["tiny_queries"]
        order = ["dog", "boat", "ocean", "deck"]
        res = VGroup()
        with self.voiceover(
            "To ask whether a word is in the set, check its three bits. <bookmark mark='a'/> Dog: one of its bits "
            "is zero, so dog was certainly never added. <bookmark mark='b'/> Boat: also a zero, certainly not. "
            "<bookmark mark='c'/> Ocean: all three of its bits are set, by whale, so the filter says yes, "
            "wrongly. A false positive. <bookmark mark='d'/> Deck: also yes, its bits set by harpoon and "
            "Queequeg. A Bloom filter never says no to a word that is in the set, but it sometimes says yes to "
            "one that isn't. How often?"
        ) as vo:
            self.play(FadeOut(fill))
            for mk, w in zip("abcd", order):
                vo.wait_until(mk)
                ix, ans = q[w]
                tag = label(rf"\texttt{{{w}}}?", font_size=24, color=HEAD).move_to(UP * 2.2)
                arrows = VGroup(*[Arrow(tag.get_bottom(), cells[i].get_top(), buff=0.08, stroke_width=2,
                                        color=HEAD, max_tip_length_to_length_ratio=0.06) for i in ix])
                self.play(FadeIn(tag), *[GrowArrow(a) for a in arrows], run_time=0.6)
                zero = [i for i in ix if i not in on]
                if zero:
                    self.play(*[Indicate(cells[i], color=NO) for i in zero])
                    txt = label(rf"\texttt{{{w}}}: \ a 0, \ so \textbf{{no}}", font_size=22, color=YES)
                else:
                    self.play(*[Indicate(cells[i], color=HEAD) for i in ix])
                    txt = label(rf"\texttt{{{w}}}: \ all 1, \ so \textbf{{yes}} \ (wrong)", font_size=22, color=NO)
                res.add(txt)
                res.arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=1.0)
                self.play(FadeIn(txt), FadeOut(tag), FadeOut(arrows))
        self.wait(0.3)
        self.clear_scene()

    def derive(self):
        head = label(r"The false-positive rate", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"$n$ words, \ $m$ bits, \ $k$ hashes \ (assume the hashes behave randomly)", font_size=22,
                  color=WHITE),
            MathTex(r"\Pr[\text{a given bit is still } 0] = \left(1 - \frac1m\right)^{kn} \approx e^{-kn/m}",
                    font_size=34, color=LAM),
            MathTex(r"\Pr[\text{false positive}] \approx \left(1 - e^{-kn/m}\right)^{k}", font_size=38, color=YES),
            label(r"few hashes: \ each probe is likely to land on a 1; \ many hashes: \ the array fills up", font_size=21,
                  color=GREY_A),
            MathTex(r"\text{best } k = \frac{m}{n} \ln 2 \quad\Longrightarrow\quad \text{half the bits are set, and}"
                    r"\quad \Pr \approx 0.6185^{\,m/n}", font_size=32, color=HEAD),
            label(r"each extra bit per word cuts the error by about a factor of $1.6$; \ ten bits per word: \ about "
                  r"1\%", font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "Suppose we add n words to m bits with k hash functions, and pretend the hashes are truly random. "
            "<bookmark mark='a'/> A particular bit is missed by all k n hashes with probability one minus one over "
            "m, to the k n, which is about e to the minus k n over m. <bookmark mark='b'/> A word that was never "
            "added is a false positive if all k of its bits happen to be set: probability about one minus that, "
            "to the k. <bookmark mark='c'/> There is a balance. With few hash functions each probe is likely to "
            "hit a set bit; with many, the array fills up. <bookmark mark='d'/> Calculus gives the best k, m over "
            "n times log two, and at that point exactly half the bits are set. The error is then about 0.6185 to "
            "the power m over n. <bookmark mark='e'/> Every extra bit per word divides the error by about 1.6, and "
            "ten bits per word give about one percent, whatever the words are and however long."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mk, ln in zip("abcde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("bloom")
        head = label(rf"The novels' {words(d['n'])} distinct words, \ {words(d['probes'])} non-words asked",
                     font_size=30).to_edge(UP, buff=0.35)
        ten = [r for r in d["rows"] if r["bits_per_word"] == 10 and r["k"] >= 2]
        ax = Axes(x_range=[0, 13, 2], y_range=[0, 0.035, 0.01], x_length=6.0, y_length=3.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.4)
        curve = ax.plot(lambda k: (1 - math.exp(-k / 10)) ** k, x_range=[2.0, 13], color=LAM)
        dots = VGroup(*[Dot(ax.c2p(r["k"], r["measured"]), radius=0.07, color=YES) for r in ten])
        xl = VGroup(*[label(str(x), font_size=16, color=GREY_B).next_to(ax.c2p(x, 0), DOWN, buff=0.1)
                      for x in (2, 4, 6, 8, 10, 12)])
        yl = VGroup(*[label(rf"{y}\%", font_size=16, color=GREY_B).next_to(ax.c2p(0, y / 100), LEFT, buff=0.1)
                      for y in (1, 2, 3)])
        xt = label(r"hash functions $k$ \ (10 bits per word)", font_size=18, color=GREY_A).next_to(xl, DOWN, buff=0.15)
        leg = VGroup(label(r"theory $(1 - e^{-k/10})^k$", font_size=18, color=LAM),
                     label(r"measured", font_size=18, color=YES)).arrange(RIGHT, buff=0.5).next_to(ax, UP, buff=0.1)
        best = next(r for r in ten if r["k"] == 7)
        sixteen = next(r for r in d["rows"] if r["bits_per_word"] == 16 and r["k"] == 11)
        side = VGroup(
            label(rf"$k = 7$: \ {best['measured'] * 100:.3f}\% \ against {best['theory'] * 100:.3f}\%",
                  font_size=20, color=YES),
            label(rf"bits set: \ {best['fill'] * 100:.1f}\%", font_size=20, color=GREY_A),
            label(rf"16 bits per word, \ $k = 11$: \ {sixteen['measured'] * 100:.3f}\%", font_size=20, color=YES),
            label(rf"memory: \ {d['kb_10']:.0f} KB, \ against {d['vocab_bytes'] / 1024:.0f} KB of letters", font_size=20,
                  color=HEAD),
            label(r"no word in the set was ever missed", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(UP * 0.2)
        var = label(r"variants: \ counting filters (deletions); \ cuckoo filters (Fan et al., 2014); \ "
                    r"in practice: \ every LSM-tree database, \ Part 34", font_size=19, color=GREY_A
                    ).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"Now a real one: all {words(d['n'])} distinct words of the novels, ten bits per word, queried with a "
            "hundred thousand random strings that are not words of the novels. <bookmark mark='a'/> The purple "
            "curve is the formula, and the green dots are what we measured for each number of hash functions. "
            f"<bookmark mark='b'/> At the best k, seven, {best['measured'] * 100:.2f} percent of the non-words "
            f"slipped through, against a predicted {best['theory'] * 100:.2f}, and almost exactly half the bits "
            "were set. <bookmark mark='c'/> With sixteen bits per word the rate falls to one in two thousand. "
            "<bookmark mark='d'/> The filter takes seventy kilobytes, while just the letters of the words "
            "take four hundred and forty, and it never missed a word that was there. <bookmark mark='e'/> Counting "
            "filters allow deletions, cuckoo filters do better at low error rates, and nearly every log-structured "
            "database keeps a Bloom filter per file to skip disk reads, as Part 34 will show."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xt))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(leg))
            self.play(LaggedStart(*[GrowFromCenter(x) for x in dots], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(var))
        self.wait(0.3)
        self.clear_scene()
