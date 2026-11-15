from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


class Experience(VoiceoverScene):
    def construct(self):
        self.card()
        self.paradigm()
        self.never_seen()
        self.gap()
        self.data()

    def card(self):
        card = chapter_card(10, r"Decisions from experience", r"What if you learn the odds by sampling them?",
                            lit={2004: r"Hertwig et al.", 2009: r"Hertwig \& Erev", 2018: r"Wulff et al."},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter ten. Decisions from experience."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def paradigm(self):
        head = heading(r"Two buttons, \ no descriptions")
        b1 = RoundedRectangle(corner_radius=0.15, width=2.4, height=1.4, stroke_color=SURE, stroke_width=3,
                              fill_color=BLACK, fill_opacity=0.6).move_to([-2.0, 1.2, 0])
        b2 = RoundedRectangle(corner_radius=0.15, width=2.4, height=1.4, stroke_color=RISKY, stroke_width=3,
                              fill_color=BLACK, fill_opacity=0.6).move_to([2.0, 1.2, 0])
        t1 = label(r"button A", font_size=24, color=SURE).move_to(b1)
        t2 = label(r"button B", font_size=24, color=RISKY).move_to(b2)
        draws1 = label(r"3, \ 3, \ 3, \ 3, \ 3, \ 3, \ 3", font_size=24, color=SURE).next_to(b1, DOWN, buff=0.3)
        draws2 = label(r"0, \ 0, \ 0, \ 0, \ 0, \ 0, \ 0", font_size=24, color=RISKY).next_to(b2, DOWN, buff=0.3)
        rows = rows_of([
            (r"Hertwig, \ Barron, \ Weber and Erev, \ 2004: \ sample each button as often as you like, \ for free; "
             r"\ then choose one for real", WHITE),
            (r"button B pays 32 one time in ten, \ but these seven draws never showed it", RISKY),
            (r"described, \ the rare 32 is overweighted; \ experienced, \ it is often never seen, \ and then "
             r"underweighted", MODEL),
        ], 12.0, 24, 0.3).move_to([0, -1.8, 0])
        tag = published_tag(r"Hertwig, \ Barron, \ Weber \& Erev (2004)")
        with self.voiceover(
            "Every problem so far was described: the outcomes and their chances were written down. Most of life "
            "isn't like that. <bookmark mark='a'/> In 2004 Ralph Hertwig, Greg Barron, Elke Weber and Ido Erev gave "
            "people two buttons with no descriptions. They could click each as often as they liked, for free, to see "
            "what it paid, and then chose one to play for real. <bookmark mark='b'/> Suppose button A always pays "
            "three, and button B pays thirty-two one time in ten and nothing otherwise. Seven clicks on B may well "
            "show nothing but zeros. <bookmark mark='c'/> Described, the rare thirty-two is overweighted, as the "
            "fourfold pattern says. Learned from experience, it's often never seen at all, and choices behave as if "
            "rare events were underweighted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(b1), FadeIn(b2), FadeIn(t1), FadeIn(t2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(draws1), FadeIn(draws2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def never_seen(self):
        d = load("experience")
        head = heading(r"How often a rare outcome is never seen")
        A = axes([0, 40], [0, 1], x_length=6.2, y_length=4.0, xticks=[0, 10, 20, 30, 40], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"draws from the option",
                 ylabel=r"chance the outcome never appears", center=[-3.0, -0.2, 0], font_size=16)
        c5 = curve(A.ax, d["n"], d["never_05"], LOSS, 4)
        c10 = curve(A.ax, d["n"], d["never_10"], RISKY, 4)
        c20 = curve(A.ax, d["n"], d["never_20"], SURE, 4)
        key = legend([(LOSS, r"probability 0.05"), (RISKY, r"probability 0.10"), (SURE, r"probability 0.20")],
                     font_size=18).move_to(A.ax.c2p(31, 0.8))
        seven = DashedLine(A.ax.c2p(7, 0), A.ax.c2p(7, 1), color=GREY_B, stroke_width=2)
        dot = Dot(A.ax.c2p(7, d["never7_10"]), color=RISKY, radius=0.08)
        rows = rows_of([
            (r"$(1 - p)^n$: \ the chance that $n$ draws miss an outcome of probability $p$", NORM),
            (rf"with seven draws, \ an outcome with probability 0.1 is missed {100 * d['never7_10']:.0f}\% of the "
             r"time", RISKY),
            (r"people in these studies typically sample little, \ a handful of draws per option", WHITE),
        ], 5.4, 22, 0.32).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{choice.p\_never\_seen}")
        with self.voiceover(
            "Part of the reason is simple arithmetic. <bookmark mark='a'/> The chance that n draws all miss an "
            "outcome of probability p is one minus p, to the power n. <bookmark mark='b'/> With seven draws, an "
            f"outcome that happens one time in ten is missed {100 * d['never7_10']:.0f} percent of the time. "
            "<bookmark mark='c'/> And people in these studies typically sample little, a handful of draws from "
            "each option, so the rare outcome is very often simply absent from what they know."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(c5), Create(c10), Create(c20), FadeIn(key), FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(seven), FadeIn(dot), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def gap(self):
        d = load("experience")
        head = heading(r"The description--experience gap, \ in Psyche")
        A = axes([-0.5, 3.5], [0, 1], x_length=7.0, y_length=3.6, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", ylabel=r"P(choose the risky option)", center=[-2.4, 0.0, 0], font_size=16)
        xs = np.arange(4)
        b1 = bars(A.ax, xs - 0.18, d["desc"], MODEL, width=0.34)
        b2 = bars(A.ax, xs + 0.18, d["expr"], RISKY, width=0.34)
        names = VGroup(*[label(n_, font_size=17, color=GREY_A).next_to(A.ax.c2p(x, 0), DOWN, buff=0.15)
                         for x, n_ in zip(xs, d["names"])])
        half = DashedLine(A.ax.c2p(-0.5, 0.5), A.ax.c2p(3.5, 0.5), color=GREY_D, stroke_width=1.5)
        key = legend([(MODEL, r"described: \ prospect theory, \ 1992 values"),
                      (RISKY, r"experienced: \ seven draws, \ choose the better sample mean")], font_size=18)
        key.next_to(A, DOWN, buff=0.35)
        rows = rows_of([
            (r"where the rare outcome is good, \ description favours the gamble and experience does not", GAIN),
            (r"where it is bad, \ the reverse", LOSS),
            (r"Wulff, \ Mergenthaler-Canseco and Hertwig, \ 2018: \ across many studies, \ a reliable gap, \ "
             r"smaller with longer samples", WHITE),
        ], 4.0, 21, 0.3).move_to([4.6, 0.2, 0])
        tag = psyche_tag(r"\texttt{choice.cpt}, \ \texttt{sample\_choices}: \ 40{,}000 simulated choosers")
        assert d["desc"][1] > 0.5 > d["expr"][1] - 0.05 and d["desc"][2] < d["expr"][2]
        with self.voiceover(
            "Psyche can show the gap. <bookmark mark='a'/> Four problems in the style of the 2004 study. For each, "
            "the purple bar is the chance of choosing the risky option from a description, by prospect theory with "
            "the 1992 values; the amber bar, the chance after seven draws from each option, choosing whichever "
            "sample looked better. <bookmark mark='b'/> Where the rare outcome is good, as in thirty-two one time "
            "in ten, the description makes the gamble attractive and experience does not. Where the rare outcome is "
            "bad, a loss of thirty-two one time in ten, it's the other way round: from experience, people take the "
            "risk they'd avoid on paper. <bookmark mark='c'/> A 2018 meta-analysis by Dirk Wulff, Max "
            "Mergenthaler-Canseco and Hertwig found the gap reliable across many studies, though smaller when "
            "people sample more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), Create(half))
            vo.wait_until("a")
            self.play(FadeIn(b1), FadeIn(key[0]))
            self.play(FadeIn(b2), FadeIn(key[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def data(self):
        d = load("c13k")
        head = heading(r"In the thirteen thousand: \ feedback")
        A = axes([-0.5, 1.5], [0.3, 0.65], x_length=5.0, y_length=3.6, xticks=None, yticks=[0.3, 0.4, 0.5, 0.6],
                 yfmt=lambda v: f"{v:.1f}", ylabel=r"share choosing the risky option", center=[-3.4, -0.1, 0],
                 font_size=16)
        rg, rb = d["rare_good_rates"], d["rare_bad_rates"]
        g = VGroup(bars(A.ax, [-0.18], [rg[0]], MODEL, width=0.32), bars(A.ax, [0.18], [rg[1]], RISKY, width=0.32))
        b = VGroup(bars(A.ax, [0.82], [rb[0]], MODEL, width=0.32), bars(A.ax, [1.18], [rb[1]], RISKY, width=0.32))
        names = VGroup(label(rf"rare outcome best \ ({d['rare_good_n']})", font_size=18, color=GAIN).next_to(
            A.ax.c2p(0, 0.3), DOWN, buff=0.15),
                       label(rf"rare outcome worst \ ({d['rare_bad_n']})", font_size=18, color=LOSS).next_to(
            A.ax.c2p(1, 0.3), DOWN, buff=0.15))
        key = legend([(MODEL, r"first, \ described only"), (RISKY, r"later blocks, \ with feedback")],
                     font_size=18).next_to(A, DOWN, buff=0.35)
        rows = rows_of([
            (rf"{d['pairs']} problems were played both without and with feedback; \ the risky option against a sure "
             r"amount, \ with an outcome of probability 0.1 or less:", WHITE),
            (rf"when the rare outcome is the worst, \ the risky option gained {100 * d['rare_bad_delta']:.0f} points with feedback, "
             r"\ as experience predicts", LOSS),
            (rf"when it is the best, \ the risky option did not lose, \ as it should have: \ {100 * rg[0]:.0f}\% to {100 * rg[1]:.0f}\%",
             GAIN),
            (r"here feedback comes on top of a description, \ a weaker test than experience alone", GREY_A),
        ], 5.6, 21, 0.3).move_to([3.4, 0.1, 0])
        tag = historical_tag(r"choices13k: \ Peterson et al.\ (2021)")
        with self.voiceover(
            "The thirteen thousand problems offer a check of their own, and it's only half a success. "
            f"<bookmark mark='a'/> {d['pairs']} problems were played first from the description alone and later "
            "with feedback after each choice. Take those where one option is a sure amount and the other has an "
            "outcome with a chance of one in ten or less. <bookmark mark='b'/> When the rare outcome is the worst one, "
            f"the risky option gained about {100 * d['rare_bad_delta']:.0f} points once people saw what their choices "
            "paid, as underweighting from experience predicts. <bookmark mark='c'/> When the rare outcome is the best one, "
            "the risky option should have lost ground, and it didn't: it moved from "
            f"{100 * rg[0]:.0f} to {100 * rg[1]:.0f} percent. <bookmark mark='d'/> In this design the description "
            "stays on the screen while the feedback arrives, a much weaker test than learning from experience "
            "alone. So: a gap in one direction here, and none in the other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(g), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
