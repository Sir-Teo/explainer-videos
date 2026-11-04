from __future__ import annotations

from explainer.stats.board import Row, coverage_board
from videos.stats.stats8.common import *  # noqa: F403


def rows8():
    return [Row(**{k: v for k, v in r.items() if k not in ("verdict", "se")}) for r in load("board")["rows"]]


class Board(VoiceoverScene):
    def construct(self):
        self.card()
        self.protocol()
        self.stack()
        self.board()
        self.read()

    def card(self):
        card = chapter_card(11, r"The Coverage Board opens", r"Promises, tested on a population we know", part=PART)
        with self.voiceover("Chapter eleven. The Coverage Board opens."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def protocol(self):
        rows = fit_rows(VGroup(
            label(r"a method promises: \ ``95\% of my intervals catch the truth''", font_size=28),
            label(r"draw 10,000 samples from the World, \ where the truth is known", font_size=26),
            label(r"compute the interval each time; \ count how often it catches the truth", font_size=26),
            MathTex(r"\text{Monte Carlo SE} = \sqrt{0.95 \times 0.05 / 10{,}000} = 0.22\%", font_size=28, color=GREY_A),
            VGroup(label(r"kept:", font_size=26, color=S.KEPT), label(r"within 3 MC SEs of 95\%", font_size=26)).arrange(RIGHT, buff=0.2),
            VGroup(label(r"broken:", font_size=26, color=S.BROKEN), label(r"covers less", font_size=26),
                   label(r"\quad conservative:", font_size=26, color=S.CONS), label(r"covers more", font_size=26)).arrange(RIGHT, buff=0.2),
        ), 12.6, 0.32, [0, 0.2, 0])
        with self.voiceover(
            "In Part 1 we set up an empty scoreboard. Now it gets its first rows. <bookmark mark='a'/> Every interval "
            "makes a promise: ninety-five percent of the intervals it produces will catch the truth. "
            "<bookmark mark='b'/> On real data we can never check that, because we don't know the truth. In the World "
            "we do. <bookmark mark='c'/> So for each method, draw ten thousand samples, compute the interval each time, "
            "and count how often it catches the true value. <bookmark mark='d'/> Ten thousand replications pin the "
            "coverage down to within about a fifth of a percentage point, Chapter 6 of Part 7's Monte Carlo standard "
            "error. <bookmark mark='e'/> A method whose coverage is within three Monte Carlo standard errors of "
            "ninety-five percent keeps its promise. <bookmark mark='f'/> Below that, it's broken; above, conservative."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = rows8()
        b = coverage_board(rows, lit_part=8, placeholders=3, font_size=20)
        with self.voiceover(
            "Here is the board. <bookmark mark='a'/> First, the textbook z-interval when sigma is known, on samples of "
            "five heights: ninety-five point oh five percent. Kept. <bookmark mark='b'/> The same interval with s in "
            "place of sigma: eighty-seven point six percent. Broken: Gosset's discovery, measured. "
            "<bookmark mark='c'/> Student's t with five observations: ninety-four point four, inside the band. Kept. "
            "<bookmark mark='d'/> Now Student's t on the World's incomes, skewed with a heavy tail. With twenty people, "
            "eighty-eight percent. Broken. With five hundred, still only ninety-two point eight. Broken: chapter seven "
            "of Part 6, the central limit theorem's slow arrival, now on the record. <bookmark mark='e'/> And the F-test "
            "for equal variances, whose false-alarm rate should be five percent: on normal heights, four point nine. "
            "Kept. On log incomes, which are only roughly normal, six point three. Broken."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend), *[FadeIn(r) for r in b.body[len(rows):]])
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(b.body[k] if k < 3 else VGroup(b.body[3], b.body[4]), shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(VGroup(b.body[5], b.body[6]), shift=RIGHT * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def read(self):
        d = load("board")["rows"]
        rows = fit_rows(VGroup(
            label(r"what the first rows say", font_size=30, color=S.ACCENT),
            label(r"exact theory keeps exact promises: \ $z$ with $\sigma$, \ $t$ for normal data", font_size=26, color=S.KEPT),
            label(r"plugging in $s$ without paying for it breaks them: \ Gosset's point", font_size=26, color=S.BROKEN),
            label(r"approximations fail in the tails: \ skewed incomes, \ even at $n = 500$", font_size=26, color=S.BROKEN),
            label(rf"the widths: \ $z$ with $s$ is narrower ({d[1]['width']:.1f} cm) than $t$ ({d[2]['width']:.1f} cm) \ \textemdash{{}} \ and "
                  r"that is exactly why it fails", font_size=24, color=GREY_A),
            label(r"every later part adds rows; \ Part 65 shows the whole board", font_size=24, color=GREY_A),
        ), 12.6, 0.36, [0, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What do the first rows say? <bookmark mark='b'/> Exact theory keeps exact promises. "
            "<bookmark mark='c'/> Plugging in an estimate without paying for its uncertainty breaks them. "
            "<bookmark mark='d'/> And large-sample approximations can fail even with large samples, when the data "
            "have heavy tails. <bookmark mark='e'/> Look at the widths, too: the broken interval is narrower than "
            "Student's, and that's exactly why it fails. An interval that's too good to be true usually is. "
            "<bookmark mark='f'/> Every later part will add rows to this board, and Part 65 will show it whole: a public "
            "record of which promises statistics keeps, measured rather than assumed."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def stack(self):
        d = load("extras")["stack"]
        m, hz, ht, mu = np.asarray(d["m"]), np.asarray(d["hz"]), np.asarray(d["ht"]), d["mu"]
        panels = VGroup()
        for k, (half, title, q) in enumerate(((hz, r"$\bar x \pm 1.96\,s/\sqrt 5$", RESID), (ht, r"$\bar x \pm 2.78\,s/\sqrt 5$", EXACT))):
            A = axes([130, 210], [0, 41], x_length=5.4, y_length=5.0, xlabel=r"height (cm)", xticks=[140, 170, 200], center=[-3.4 + 6.8 * k, -0.6, 0])
            A.ax.y_axis.set_opacity(0)
            ax = A.ax
            tl = DashedLine(ax.c2p(mu, 0), ax.c2p(mu, 41), color=S.TRUTH, stroke_width=2)
            bars_ = VGroup()
            miss = 0
            for i, (a, h_) in enumerate(zip(m, half)):
                ok = abs(a - mu) <= h_
                miss += not ok
                c = S.KEPT if ok else S.BROKEN
                bars_.add(Line(ax.c2p(max(130, a - h_), i + 1), ax.c2p(min(210, a + h_), i + 1), color=c, stroke_width=3))
            t = label(title, font_size=26, color=q).next_to(A, UP, buff=0.1)
            r = label(rf"{40 - miss} of 40 catch $\mu$", font_size=24, color=q).next_to(A, DOWN, buff=0.1)
            panels.add(VGroup(A, tl, bars_, t, r))
        tag = simulated_tag(r"simulated: 40 samples of 5 adults")
        with self.voiceover(
            "First, a picture of what coverage means. <bookmark mark='a'/> Forty samples of five heights, each with the "
            "naive interval, using one point nine six and s. The red ones miss the true mean. Three of forty miss: "
            "this time, by luck, it looks fine. <bookmark mark='b'/> On the right, the same forty samples with "
            "Student's multiplier, two point seven eight: every one catches the truth here. Forty intervals can't tell "
            "these two methods apart reliably. Ten thousand can."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(panels[0][0]), Create(panels[0][1]), LaggedStart(*[Create(b) for b in panels[0][2]], lag_ratio=0.05),
                      FadeIn(panels[0][3]), run_time=3.0)
            self.play(FadeIn(panels[0][4]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1][0]), Create(panels[1][1]), LaggedStart(*[Create(b) for b in panels[1][2]], lag_ratio=0.05),
                      FadeIn(panels[1][3]), run_time=3.0)
            self.play(FadeIn(panels[1][4]))
        self.clear_scene()
