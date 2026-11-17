from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Shape(VoiceoverScene):
    def construct(self):
        self.card()
        self.one_person()
        self.same_mean()

    def card(self):
        card = chapter_card(3, r"The shape of a response time", r"Why does the average mislead?",
                            lit={1965: r"Hohle", 1979: r"Ratcliff", 1998: r"Ratcliff \& Rouder"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter three. The shape of a response time."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def one_person(self):
        d = load("shape")
        head = heading(rf"One person, \ {num(d['n'])} correct answers")
        A = axes([0.2, 2.0], [0, 3.5], x_length=6.6, y_length=3.6, xticks=[0.4, 0.8, 1.2, 1.6, 2.0],
                 yticks=[0, 1, 2, 3], xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"response time, \ s", ylabel=r"density", center=[-3.0, -0.2, 0], font_size=16)
        mids = (d["edges"][:-1] + d["edges"][1:]) / 2
        hist = bars(A.ax, mids, d["hist"], DATA, width=float(np.diff(d["edges"])[0]) * 0.92, opacity=0.7)
        fit = curve_in(A.ax, d["t"], d["pdf"], MODEL, 3)
        ql = VGroup(*[DashedLine(A.ax.c2p(q, 0), A.ax.c2p(q, 3.2), color=EVIDENCE, stroke_width=1.5,
                                 dash_length=0.06) for q in d["q"]])
        mm = VGroup(Line(A.ax.c2p(d["median"], 0), A.ax.c2p(d["median"], 3.2), color=BOUND, stroke_width=3),
                    Line(A.ax.c2p(d["mean"], 0), A.ax.c2p(d["mean"], 3.2), color=LOST, stroke_width=3))
        ml = legend([(BOUND, rf"median {d['median']:.2f} s"), (LOST, rf"mean {d['mean']:.2f} s"),
                     (EVIDENCE, r"10th, \ 30th, \ 50th, \ 70th, \ 90th percentiles")], font_size=17)
        ml.next_to(A.ax.c2p(1.05, 3.2), RIGHT, buff=0.0).align_to(A.ax.c2p(0, 3.2), UP)
        qt = VGroup()
        assert d["mean"] > d["median"] and d["tau"] > 2 * d["sigma"]
        rows = rows_of([
            (rf"the median person of {d['n_people']} \ (by mean time), \ asked to be accurate, \ correct answers only",
             WHITE),
            (r"a steep rise, \ a peak, \ and a long tail to the right: \ the shape of nearly every response-time "
             r"distribution", DATA),
            (rf"ex-Gaussian fit \ (Part 1): \ a normal with mean {d['mu']:.2f} s and sd {d['sigma']:.2f} s, \ "
             rf"plus an exponential with mean {d['tau']:.2f} s", MODEL),
            (r"the tail drags the mean past the median: \ so models are fitted to quantiles, \ not means", LOST),
        ], 5.4, 22, 0.34).move_to([3.7, 0.0, 0])
        tag = psyche_tag(r"\texttt{chronometry.fit\_exgauss}; \ open data: \ Wagenmakers et al. (2008)")
        with self.voiceover(
            "Before modelling a choice, look at what a response time is. <bookmark mark='a'/> Here's one person "
            f"from those seventeen, the median one by mean time, and the {num(d['n'])} times they answered "
            "correctly when asked to be accurate. <bookmark mark='b'/> A steep rise, a peak, and a long tail to the "
            "right. Nearly every response-time distribution ever recorded has this shape. <bookmark mark='c'/> Part "
            "1's ex-Gaussian fits it well: a normal stage plus an exponential one, with most of the spread in the "
            "exponential tail. <bookmark mark='d'/> And the tail drags the mean well past the median. That's why "
            "modern models aren't fitted to mean times at all, but to the whole distribution, summarized by a few "
            "quantiles, for correct answers and errors separately."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(hist), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(fit), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(mm), FadeIn(ml), Create(ql), FadeIn(qt), FadeIn(rows[3]))
        self.clear_scene()

    def same_mean(self):
        d = load("shape")
        head = heading(r"Same mean, \ different minds")
        A = axes([0.2, 2.0], [0, 3.6], x_length=6.6, y_length=3.6, xticks=[0.4, 0.8, 1.2, 1.6, 2.0],
                 yticks=[0, 1, 2, 3], xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"response time, \ s", ylabel=r"density", center=[-3.0, -0.2, 0], font_size=16)
        n1 = curve_in(A.ax, d["same_t"], d["norm"], EVIDENCE, 3)
        n2 = curve_in(A.ax, d["same_t"], d["skew"], TIME, 3)
        ml = DashedLine(A.ax.c2p(d["mean"], 0), A.ax.c2p(d["mean"], 3.4), color=WHITE, stroke_width=2)
        mt = label(rf"both means {d['mean']:.2f} s", font_size=18, color=WHITE).next_to(ml, UP, buff=0.05)
        key = legend([(EVIDENCE, r"every response a little slow"), (TIME, r"most fast, \ a few very slow")],
                     font_size=17).move_to(A.ax.c2p(1.55, 2.6))
        dx = d["same_t"][1] - d["same_t"][0]
        m1 = float((d["same_t"] * d["norm"]).sum() * dx / (d["norm"].sum() * dx))
        m2 = float((d["same_t"] * d["skew"]).sum() * dx / (d["skew"].sum() * dx))
        assert abs(m1 - d["mean"]) < 0.01 and abs(m2 - d["mean"]) < 0.03
        rows = rows_of([
            (r"two distributions with the same mean: \ one shifted, \ one with a long tail", WHITE),
            (r"a slower stage shifts everything; \ occasional lapses, \ or a few hard decisions, \ stretch the "
             r"tail", TIME),
            (r"a difference in means cannot tell them apart; \ the shapes can", BOUND),
            (r"Ratcliff, \ 1979: \ average people's quantiles, \ not their raw times, \ to keep each one's shape",
             MODEL),
        ], 5.4, 23, 0.36).move_to([3.7, 0.0, 0])
        tag = psyche_tag(r"illustrative distributions with the mean of the person above")
        with self.voiceover(
            "Here's why the mean misleads. <bookmark mark='a'/> These two distributions have exactly the same mean. "
            "<bookmark mark='b'/> In the blue one every response is a little slow, as if a stage took longer. In "
            "the pink one most responses are fast and a few are very slow, as if the person occasionally drifted "
            "off, or a few decisions were much harder. <bookmark mark='c'/> A difference in mean response time can't "
            "tell these apart. The shapes can. <bookmark mark='d'/> Roger Ratcliff showed in 1979 how to average "
            "people without destroying the shape: average their quantiles, not their raw times. Every fit in this "
            "part keeps the shape."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(n1), Create(n2), Create(ml), FadeIn(mt), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(key), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
