from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


class Drugs(VoiceoverScene):
    def construct(self):
        self.card()
        self.kirsch()
        self.network()

    def card(self):
        card = chapter_card(10, r"Do antidepressants work?", r"How big is the difference from placebo?",
                            lit={2008: r"Kirsch et al.", 2018: r"Cipriani et al."}, part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter ten. Do antidepressants work?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def kirsch(self):
        head = heading(r"Drug, \ placebo, \ and the gap")
        A = axes([-0.6, 1.6], [0, 12], x_length=3.8, y_length=3.0, xticks=None, yticks=[0, 4, 8, 12],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"improvement, \ scale points", center=[-4.0, -0.2, 0],
                 font_size=14)
        b = bars(A.ax, [0, 1], [9.6, 7.8], [GOOD, GREY_A], width=0.6)
        names = VGroup(label(r"drug", font_size=15, color=GOOD).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       label(r"placebo", font_size=15, color=GREY_A).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15))
        gap = DoubleArrow(A.ax.c2p(1.45, 7.8), A.ax.c2p(1.45, 9.6), color=AUTH, buff=0, stroke_width=3,
                          tip_length=0.12)
        lg = label(r"about 1.8", font_size=15, color=AUTH).next_to(gap, RIGHT, buff=0.08)
        note = label(r"schematic heights; \ the gap as reported", font_size=13, color=GREY_B).next_to(A, DOWN,
                                                                                                   buff=0.55)
        rows = rows_of([
            (r"Kirsch and colleagues, \ 2008: \ the trials of four newer antidepressants submitted to the US "
             r"regulator, \ published or not", WHITE),
            (r"both groups improved a lot; \ the average difference between drug and placebo was about 1.8 points "
             r"on the 52-point Hamilton scale", AUTH),
            (r"the gap was larger for the most severely depressed, \ mainly because they responded less to "
             r"placebo", PERSON),
            (r"much of the improvement on a drug is improvement that would have happened on placebo, \ which is "
             r"itself an active treatment of attention, \ hope and time", YOU),
        ], 6.4, 19, 0.36).move_to([3.2, -0.2, 0])
        tag = published_tag(r"Kirsch et al.\ (2008)")
        with self.voiceover(
            "How well do the drugs work? <bookmark mark='a'/> In 2008 Irving Kirsch and colleagues analysed the "
            "trials of four newer antidepressants submitted to the American regulator, published or not. "
            "<bookmark mark='b'/> Both groups improved a lot. The average difference between drug and placebo was "
            "about one point eight points on the fifty-two-point Hamilton scale. <bookmark mark='c'/> The gap was "
            "larger for the most severely depressed, mainly because they responded less to placebo. "
            "<bookmark mark='d'/> Much of the improvement on a drug is improvement that would have happened on "
            "placebo, which is itself a treatment of attention, hope and time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), *[GrowFromEdge(x, DOWN) for x in b], GrowFromCenter(gap), FadeIn(lg))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def network(self):
        head = heading(r"522 trials")
        A = axes([0.9, 2.3], [-0.5, 9.5], x_length=4.6, y_length=3.6, xticks=[1, 1.5, 2], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"odds ratio for response against placebo", center=[-3.6, -0.2, 0],
                 font_size=13)
        rng = np.random.default_rng(522)
        ors = np.sort(np.r_[1.37, 2.13, rng.uniform(1.45, 1.95, 8)])
        ys = np.arange(len(ors))
        pts = VGroup(*[VGroup(Line(A.ax.c2p(o * 0.85, y), A.ax.c2p(o * 1.15, y), color=GREY_B, stroke_width=1.5),
                              Dot(A.ax.c2p(o, y), radius=0.06, color=GOOD)) for o, y in zip(ors, ys)])
        one = DashedLine(A.ax.c2p(1, -0.5), A.ax.c2p(1, 9.5), color=AUTH)
        lo = label(r"no effect", font_size=13, color=AUTH).next_to(A.ax.c2p(1, 9.5), UP, buff=0.05)
        note = label(r"schematic: \ range as reported", font_size=13, color=GREY_B).next_to(A, DOWN, buff=0.35)
        rows = rows_of([
            (r"Cipriani and colleagues, \ 2018: \ a network meta-analysis of 522 trials, \ 116{,}477 people, \ 21 "
             r"antidepressants", WHITE),
            (r"every one was more effective than placebo for adults with major depression; \ odds ratios ran from "
             r"about 1.4 to 2.1", GOOD),
            (r"a real average effect, \ modest in size: \ the Ledger marks antidepressants beating placebo as "
             r"replicated, \ and small", PERSON),
            (r"open: \ who benefits most, \ how to choose a drug for a person, \ and what happens over years, \ "
             r"since most trials last about eight weeks", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Cipriani et al.\ (2018)")
        with self.voiceover(
            "The largest analysis came ten years later. <bookmark mark='a'/> In 2018 Andrea Cipriani and colleagues "
            "combined five hundred and twenty-two trials, a hundred and sixteen thousand people, comparing twenty-"
            "one antidepressants. <bookmark mark='b'/> Every one was more effective than placebo for adults with "
            "major depression, with odds ratios from about one point four to two point one. "
            "<bookmark mark='c'/> A real average effect, modest in size. The Ledger marks antidepressants beating "
            "placebo as replicated, and small. <bookmark mark='d'/> What's open is who benefits most, how to choose "
            "a drug for a particular person, and what happens over years, since most trials last about eight weeks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(one), FadeIn(lo), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.1))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
