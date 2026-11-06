from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)

CW = 0.4


def row(s, color, font=20):
    g = VGroup(*[VGroup(Square(side_length=CW, stroke_color=color, stroke_width=1.2), mono(c, font, WHITE))
                 for c in s]).arrange(RIGHT, buff=0)
    for c in g:
        c[1].move_to(c[0])
    return g


class BoyerMoore(VoiceoverScene):
    def construct(self):
        self.card()
        self.skip()
        self.rules()
        self.good_suffix()
        self.measured()

    def card(self):
        card = chapter_card(4, r"Boyer and Moore: \ skip ahead", r"Can a search read less than the whole text?",
                            lit=(1977,), extra=((1977, r"Boyer--Moore"),), part=PART)
        with self.voiceover("Chapter four. Boyer and Moore: skip ahead."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def skip(self):
        head = label(r"Compare from the right", font_size=34).to_edge(UP, buff=0.35)
        text = "a whale, a harpoon, Queequeg"
        pat = "Queequeg"
        T = row(text, GREY_B).move_to(UP * 1.2)
        x0 = T[0].get_left()[0]
        P = row(pat, DATA)
        P.move_to([x0 + P.width / 2, 0.5, 0])
        # Horspool's shifts by the window's last character
        shift = {c: len(pat) - 1 - k for k, c in enumerate(pat[:-1])}
        i, steps = 0, []
        while i <= len(text) - len(pat):
            last = text[i + len(pat) - 1]
            steps.append((i, last))
            if text[i:i + len(pat)] == pat:
                break
            i += shift.get(last, len(pat))
        notes = VGroup(
            label(r"look at the window's \textbf{last} character first", font_size=22, color=WHITE),
            label(r"if it doesn't occur in the pattern, \ no alignment covering it can match: \ jump $m$ places",
                  font_size=22, color=YES),
            label(r"otherwise slide so the pattern's rightmost copy of it lines up \ (the bad-character rule)",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "In 1977 Robert Boyer and J Strother Moore turned the comparison around. <bookmark mark='a'/> Put the "
            "pattern under the text and compare its last character first. <bookmark mark='b'/> Here the text has a "
            "space where the pattern has g, and a space appears nowhere in Queequeg. So no alignment that covers "
            "that space can match, and the pattern can jump its whole length. <bookmark mark='c'/> When the "
            "character does occur in the pattern, slide just far enough to line up its rightmost copy. Watch how "
            "few characters of the text are ever looked at."
        ) as vo:
            self.play(FadeIn(head), FadeIn(T), FadeIn(P))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            for i, last in steps:
                self.play(P.animate.move_to([x0 + i * CW + P.width / 2, 0.5, 0]), run_time=0.5)
                k = i + len(pat) - 1
                self.play(T[k][0].animate.set_fill(HEAD, 0.5), run_time=0.3)
            self.play(P.animate.set_color(YES))
        self.wait(0.3)
        self.clear_scene()

    def rules(self):
        head = label(r"Two rules, \ take the larger shift", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"\textbf{bad character}: \ align the mismatched text character with its last occurrence in the "
                  r"pattern", font_size=22, color=HEAD),
            label(r"\textbf{good suffix}: \ the matched suffix must appear again in the pattern: \ shift to its next "
                  r"copy, \ or to a border", font_size=22, color=LAM),
            label(r"preprocessing: \ $O(m + \sigma)$; \ worst case $O(n + m)$ with Galil's rule; \ typical case "
                  r"$O(n / m)$", font_size=22, color=WHITE),
            label(r"Horspool (1980): \ keep only the bad-character rule, \ applied to the window's last character",
                  font_size=22, color=GREY_A),
            label(r"why \texttt{grep} is fast: \ a Boyer--Moore loop that reads only a fraction of the bytes \ "
                  r"(Mike Haertel, 2010)", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The full algorithm has two rules. <bookmark mark='a'/> The bad-character rule lines up the "
            "mismatched text character with its last occurrence in the pattern. <bookmark mark='b'/> The "
            "good-suffix rule uses what did match: that suffix of the pattern must appear again further left, so "
            "shift to its next copy. Take whichever shift is larger. <bookmark mark='c'/> The tables cost time "
            "linear in the pattern and the alphabet, and with Galil's refinement even the worst case is linear. The "
            "typical case is far better than linear: about n over m windows. <bookmark mark='d'/> Nigel Horspool "
            "kept only the bad-character rule, and on ordinary text he lost almost nothing. <bookmark mark='e'/> "
            "This is why grep is fast. Its author, Mike Haertel, explained in 2010 that it avoids looking at most of "
            "the bytes at all."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def good_suffix(self):
        head = label(r"The good-suffix rule, \ on \texttt{ANPANMAN}", font_size=34).to_edge(UP, buff=0.35)
        text = "QQANPAKMANPANMAN"
        pat = "ANPANMAN"
        T = row(text, GREY_B).move_to(UP * 1.4)
        x0 = T[0].get_left()[0]
        P = row(pat, DATA)
        P.move_to([x0 + 2 * CW + P.width / 2, 0.7, 0])
        lines = VGroup(
            label(r"compared from the right: \ \texttt{MAN} matched, \ then a mismatch", font_size=22, color=WHITE),
            label(r"the text there ends in \texttt{MAN}: \ the next alignment must put a \texttt{MAN} of the pattern "
                  r"under it", font_size=22, color=LAM),
            label(r"the pattern's other \texttt{MAN}-like suffix: \ \texttt{AN} at its start, \ a border", font_size=22,
                  color=HEAD),
            label(r"so shift $8 - 2 = 6$, \ not 1: \ the table depends on the pattern alone", font_size=22, color=YES),
            label(r"bad character helps when the alphabet is large; \ good suffix when the pattern repeats itself",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.28).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The good-suffix rule deserves an example. <bookmark mark='a'/> Here the pattern ANPANMAN is lined up "
            "under the text, and comparing from the right, M A N matched before a mismatch. <bookmark mark='b'/> "
            "Whatever the next possible alignment is, the text there still ends in M A N, so the pattern must "
            "have a matching piece under it. <bookmark mark='c'/> ANPANMAN has no other M A N, but its prefix A N "
            "is a suffix of M A N, a border again, so the pattern can slide until that A N lines up. <bookmark "
            "mark='d'/> That is a shift of six instead of one, and here it lands on a match; and the whole table is computed from the pattern "
            "before the search starts. <bookmark mark='e'/> On English the bad-character rule does most of the "
            "work, because the alphabet is large; on DNA, with four letters, the good-suffix rule earns its keep."
        ) as vo:
            self.play(FadeIn(head), FadeIn(T), FadeIn(P))
            vo.wait_until("a")
            for k in (7, 6, 5):
                self.play(P[k][0].animate.set_fill(YES, 0.4), T[2 + k][0].animate.set_fill(YES, 0.4), run_time=0.3)
            self.play(P[4][0].animate.set_fill(NO, 0.5), T[6][0].animate.set_fill(NO, 0.5), run_time=0.3)
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(P.animate.shift(RIGHT * 6 * CW), FadeIn(lines[3]))
            self.play(P.animate.set_color(YES))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("bm")
        h = load("hook")
        head = label(r"Comparisons per character of \textit{Moby-Dick}", font_size=32).to_edge(UP, buff=0.35)
        rs = d["rows"]
        ax = Axes(x_range=[0, 7, 1], y_range=[0, 1.2, 0.2], x_length=6.4, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        xl = VGroup(*[label(str(r["m"]), font_size=16, color=GREY_B).next_to(ax.c2p(k + 1, 0), DOWN, buff=0.1)
                      for k, r in enumerate(rs)])
        yl = VGroup(*[label(f"{v:.1f}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0.2, 0.6, 1.0)])
        xt = label(r"pattern length $m$", font_size=18, color=GREY_A).next_to(xl, DOWN, buff=0.15)

        def series(key, col):
            pts = [ax.c2p(k + 1, r[key]) for k, r in enumerate(rs)]
            return VGroup(VMobject(color=col, stroke_width=3).set_points_as_corners(pts),
                          *[Dot(p, radius=0.06, color=col) for p in pts])
        sk, sb, sh = series("kmp", DATA), series("bm", YES), series("horspool", HEAD)
        side = VGroup(
            label(r"Knuth--Morris--Pratt: \ about 1", font_size=20, color=DATA),
            label(r"Boyer--Moore: \ about $1/m$ when $m$ is short, \ then slower gains", font_size=20, color=YES),
            label(r"Horspool: \ on top of Boyer--Moore", font_size=20, color=HEAD),
            label(rf"\texttt{{Queequeg}} in the corpus: \ {words(h['bm_cmp'])} comparisons, \ {words(h['bm_windows'])} "
                  r"windows", font_size=20, color=WHITE),
            label(rf"\texttt{{grep}}: \ {h['t_grep'] * 1000:.0f} ms for 25 MB; \ Python's \texttt{{count}}: \ "
                  rf"{h['t_find'] * 1000:.0f} ms", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "We measured three random patterns of each length in Moby-Dick. <bookmark mark='a'/> Knuth–Morris–"
            "Pratt does about one comparison per character, whatever the length. <bookmark mark='b'/> Boyer–Moore "
            "does about half a comparison per character for two-letter patterns, a sixth for eight letters, and a "
            "twentieth for sixty-four: the longer the pattern, the less of the text it reads. <bookmark mark='c'/> "
            "Horspool's simplification lies almost exactly on top of it. On English, the good-suffix rule rarely "
            "matters. <bookmark mark='d'/> For Queequeg in the whole corpus, Boyer–Moore made three and a half "
            "million comparisons, seven times fewer than the naive method, and grep searches the twenty-five "
            "megabytes in about twenty milliseconds."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xt))
            vo.wait_until("a")
            self.play(Create(sk), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(sb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(sh), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()
