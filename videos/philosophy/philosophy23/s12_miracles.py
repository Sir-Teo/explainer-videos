from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Miracles(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Hume on miracles", r"Could testimony ever establish a miracle?", lit=(1748, 2000),
                            part=PART)
        with self.voiceover("Chapter eleven. Hume on miracles."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.maxim()
        self.witnesses()
        self.independence()

    def maxim(self):
        hc = history_card(1748, r"David Hume", r"\textit{Enquiry Concerning Human Understanding}, \ \S X", width=7.0,
                          color=HIST).to_corner(UL, buff=0.3)
        q = quote_card(r"No testimony is sufficient to establish a miracle, \ unless the testimony be of such a kind, "
                       r"\ that its falsehood would be more miraculous, \ than the fact, \ which it endeavours to "
                       r"establish.", r"David Hume", r"\textit{Enquiry}, \ \S X, \ part 1", width=10.4,
                       font_size=23).move_to([0, 0.6, 0])
        rows = stack([(r"a miracle: \ a violation of a law of nature, \ against which our uniform experience testifies",
                       WHITE),
                      (r"in Bayesian terms: \ compare $P(\text{testimony} \mid \text{miracle}) P(\text{miracle})$ with "
                       r"$P(\text{testimony} \mid \text{no miracle}) P(\text{no miracle})$", ABS)],
                     font_size=20, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In section ten of the Enquiry, David Hume argued that testimony can never make it reasonable to believe "
            "in a miracle. <bookmark mark='a'/>A miracle is a violation of a law of nature, and against it stands "
            "the whole of our uniform experience. So, Hume concluded, no testimony is sufficient to establish a "
            "miracle unless its falsehood would be more miraculous than the fact it tries to establish. "
            "<bookmark mark='b'/>Richard Price, the same Price who published Bayes's essay, answered him in 1767. "
            "<bookmark mark='c'/>In Bayesian terms Hume's maxim compares two products: the probability of the "
            "testimony if the miracle happened, times the prior of the miracle; and the probability of the testimony "
            "if it did not, times the prior of no miracle."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def witnesses(self):
        d = load("hume")
        head = label(r"One witness, \ and several", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, len(d["rows"]) - 1, 1], y_range=[0, 6.5, 1], x_length=6.4, y_length=3.6,
                  axis_config={"color": GREY_B, "font_size": 18}, x_axis_config={"include_numbers": True},
                  y_axis_config={"include_numbers": False}).move_to([-3.0, -0.5, 0])
        ylabels = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_A).next_to(ax.c2p(0, k + 6), LEFT,
                                                                                        buff=0.1)
                           for k in range(-6, 1, 2)])
        pts = [ax.c2p(r["witnesses"], 6 + max(-6, np.log10(r["posterior"]))) for r in d["rows"]]
        curve = VMobject(stroke_color=DIV, stroke_width=3.5).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.08, color=DIV) for p in pts])
        half = DashedLine(ax.c2p(0, 6 + np.log10(0.5)), ax.c2p(len(d["rows"]) - 1, 6 + np.log10(0.5)), color=GOAL,
                          stroke_width=2)
        hl = label(r"one half", font_size=17, color=GOAL).next_to(half, RIGHT, buff=0.1)
        xl = label(r"independent witnesses", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"$P(\text{miracle} \mid \text{reports})$", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1)
        r1 = d["rows"][1]["posterior"]
        rows = stack([(r"prior of the miracle: \ one in a million", WHITE),
                      (r"each witness: \ right 99\% of the time, \ falsely reports 1\% of the time", ARG),
                      (r"one witness: \ posterior about 1 in " + f"{round(1 / r1, -3):,.0f}".replace(",", r"\,"),
                       BAD),
                      (r"four independent witnesses: \ above one half", OK),
                      (r"Hume is right about one witness, \ and wrong in principle about many", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=5.6).move_to([3.8, -0.3, 0])
        with self.voiceover(
            "Put numbers on it. <bookmark mark='a'/>Let the prior probability of the miracle be one in a million. "
            "<bookmark mark='b'/>Let each witness be very reliable: if the miracle happened, they report it ninety-nine "
            "times in a hundred; if it did not, they falsely report it only once in a hundred. "
            "<bookmark mark='c'/>After one such witness the probability of the miracle is about one in ten thousand. "
            "Hume is right: one excellent witness is nowhere near enough. <bookmark mark='d'/>But add witnesses whose "
            "errors are independent. Each multiplies the odds by ninety-nine. With four, the miracle becomes more "
            "probable than not. <bookmark mark='e'/>So Hume's maxim is sound for a single witness, and wrong as a "
            "claim about testimony in principle. Charles Babbage made this point in 1837, and John Earman's book of "
            "2000 called Hume's argument an abject failure."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ylabels), FadeIn(xl), FadeIn(yl), Create(half), FadeIn(hl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(dots[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(dots[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(curve), LaggedStart(*[FadeIn(x) for x in dots[2:]], lag_ratio=0.2), FadeIn(rows[3]),
                      run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def independence(self):
        head = label(r"Where Hume's caution bites", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"independence", r"witnesses who talk to each other, \ or share a hope, \ are not independent: \ their "
                              r"errors correlate", BAD),
            (r"Hume's part 2", r"the love of wonder; \ ignorant and barbarous nations; \ rival miracles cancel out", NAT),
            (r"the prior", r"how small is the prior of a resurrection? \ that depends on whether there is a God",
             DIV),
            (r"the lesson", r"Hume's argument is not a proof but a calculation, \ and its inputs are disputed", GOAL),
            (r"the same mathematics", r"how independent sources build confidence: \ forecasting, \ medicine, \ "
                                      r"journalism", ARG),
        ]
        g = rows_table(rows, top=1.9, gap=0.45, width=8.6, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Hume's caution still bites, in the second part of his essay. <bookmark mark='a'/>Witnesses who talk to "
            "each other, or who share a hope, are not independent, and correlated errors do not multiply away. "
            "<bookmark mark='b'/>Hume pointed to the love of wonder, to stories that grow in the telling, and to "
            "the miracles of rival religions, which cancel each other out. <bookmark mark='c'/>And the prior is "
            "disputed: how improbable a resurrection is depends on whether there is a God who might raise the dead. "
            "<bookmark mark='d'/>So Hume's argument is not a proof but a calculation, with disputed inputs. "
            "<bookmark mark='e'/>The same mathematics governs every judgment about independent sources: how forecasts "
            "combine, how clinical trials replicate, how journalists confirm a story."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
