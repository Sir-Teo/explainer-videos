from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


class Conjoint(VoiceoverScene):
    def construct(self):
        self.card()
        self.task()
        self.worths()
        self.market()
        self.sample()

    def card(self):
        card = chapter_card(7, r"Conjoint analysis", r"What is a better camera worth?",
                            lit={1964: r"Luce \& Tukey", 1990: r"Green \& Srinivasan"}, part=PART,
                            scale=("person", "society"), marr=("how",))
        with self.voiceover("Chapter seven. Conjoint analysis."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def task(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        cols = VGroup()
        for k, (price, batt, cam, brand) in enumerate(((r"\$600", r"two days", r"good", r"brand A"),
                                                       (r"\$800", r"one day", r"great", r"brand B"),
                                                       (r"\$400", r"one day", r"good", r"brand C"))):
            box = RoundedRectangle(corner_radius=0.1, width=3.4, height=3.0, stroke_color=GREY_B, stroke_width=1.5)
            txt = VGroup(label(rf"phone {k + 1}", font_size=20, color=PERSON),
                         label(price, font_size=20), label(batt, font_size=18, color=GREY_A),
                         label(rf"{cam} camera", font_size=18, color=GREY_A), label(brand, font_size=18, color=GREY_A))
            txt.arrange(DOWN, buff=0.18).move_to(box)
            cols.add(VGroup(box, txt))
        cols.arrange(RIGHT, buff=0.5).move_to([0, 0.5, 0])
        rows = rows_of([
            (r"each task: \ three products built from levels of four attributes; \ pick one", WHITE),
            (r"twelve tasks per person, \ with the levels varied by design, \ so each attribute's effect can be "
             r"separated", MODEL),
            (r"the choices are fitted by McFadden's conditional logit: \ one part-worth per level", GOOD),
        ], 12.4, 20, 0.3).move_to([0, -2.4, 0])
        with self.voiceover(
            "Conjoint analysis turns the logit into a tool for designing products. <bookmark mark='a'/> Each task "
            "shows three products, built from levels of four attributes: price, battery, camera and brand. Pick one. "
            "<bookmark mark='b'/> Each person does twelve tasks, with the levels varied by design, so the effect of "
            "each attribute can be separated. <bookmark mark='c'/> The choices are fitted by the conditional logit, "
            "with one part-worth for each level."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(cols))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def worths(self):
        d = load("conjoint")
        head = heading(r"Part-worths, \ recovered")
        A = axes([0.3, 5.7], [-0.8, 1.0], x_length=5.6, y_length=3.2, xticks=None, yticks=[-0.5, 0, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", ylabel=r"part-worth", center=[-3.3, 0.3, 0], font_size=13)
        xs = np.arange(1, 6)
        tr = VGroup(*[Line(A.ax.c2p(x - 0.3, v), A.ax.c2p(x + 0.3, v), color=YOU, stroke_width=3)
                      for x, v in zip(xs, d["true"])])
        b = bars(A.ax, xs, d["est"], [MODEL] * 5, width=0.45)
        names = VGroup(*[wrapped_label(t, 1.1, 11, GREY_A).next_to(A.ax.c2p(i + 1, -0.8), DOWN, buff=0.1)
                         for i, t in enumerate(d["names"])])
        rows = rows_of([
            (rf"Psyche: \ {d['n_people']} simulated people, \ each with their own part-worths around a known average "
             rf"(yellow lines); \ {num(d['n_tasks'])} choices", WHITE),
            (r"the logit's estimates (bars) sit close to the averages, \ a little shrunk, \ because people differ: \ a "
             r"mixed logit would model that", MODEL),
            (rf"willingness to pay is a ratio of part-worths: \ a two-day battery is worth about "
             rf"\${d['wtp'][0]:.0f}, \ a great camera about \${d['wtp'][1]:.0f}", GOOD),
            (r"the attributes must matter one at a time: \ conjoint assumes their worths add", PERSON),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{scaling.fit\_clogit}, \ simulated respondents")
        with self.voiceover(
            "Does it work? <bookmark mark='a'/> Psyche simulates six hundred people, each with their own part-worths "
            "around a known average, the yellow lines. <bookmark mark='b'/> The logit's estimates sit close to the "
            "averages, a little shrunk, because people differ. A mixed logit would model that spread. "
            "<bookmark mark='c'/> Willingness to pay is a ratio of part-worths. A two-day battery is worth about "
            "a hundred and sixty dollars, a great camera about ninety, close to the planted values. <bookmark mark='d'/> One assumption to keep in view: the "
            "attributes' worths add up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(tr))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def market(self):
        d = load("conjoint")
        head = heading(r"A market, \ simulated")
        A = axes([0.3, 3.7], [0, 0.6], x_length=4.8, y_length=3.0, xticks=None, yticks=[0, 0.25, 0.5],
                 yfmt=lambda v: f"{v:g}", ylabel=r"predicted share", center=[-3.4, 0.3, 0], font_size=13)
        xs = np.array([1, 2, 3])
        b1 = bars(A.ax, xs - 0.17, d["shares"], [GREY_B] * 3, width=0.3)
        b2 = bars(A.ax, xs + 0.17, d["shares_cut"], [GOOD, GREY_A, GREY_A], width=0.3)
        names = VGroup(*[wrapped_label(t, 1.4, 12, GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1) for i, t in
                         enumerate((r"\$600, \ two days", r"\$800, \ great, \ brand B", r"\$400, \ brand C"))])
        rows = rows_of([
            (rf"three phones on sale: \ predicted shares {100 * d['shares'][0]:.0f}\%, \ {100 * d['shares'][1]:.0f}\% "
             rf"and {100 * d['shares'][2]:.0f}\%", WHITE),
            (rf"cut the first to \$500: \ its share rises to {100 * d['shares_cut'][0]:.0f}\%, \ taken from both "
             rf"rivals in proportion: \ the logit's axiom again", GOOD),
            (r"real markets add what a survey cannot: \ awareness, \ availability, \ and choices not to buy at all", AUTH),
            (r"conjoint is a model of stated choices; \ check it against what people do", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "With the part-worths, a firm can simulate a market. <bookmark mark='a'/> Three phones on sale, with "
            "these predicted shares. <bookmark mark='b'/> Cut the first to five hundred dollars, and its share rises "
            "to about half, taken from both rivals in proportion. That's the logit's axiom again, red buses and all. "
            "<bookmark mark='c'/> Real markets add what a survey can't: awareness, availability, and the choice not "
            "to buy at all. <bookmark mark='d'/> Conjoint is a model of stated choices. Check it against what people "
            "actually do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(names), FadeIn(b1))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b2))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def sample(self):
        d = load("wtp_n")
        head = heading(r"How many respondents?")
        A = axes([0, 850], [100, 200], x_length=5.6, y_length=3.0, xticks=[50, 200, 400, 800], yticks=[100, 150, 200],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: rf"\${v:.0f}", xlabel=r"people, \ 12 tasks each",
                 ylabel=r"willingness to pay for the battery", center=[-3.3, 0.3, 0], font_size=13)
        truth = DashedLine(A.ax.c2p(0, d["true"]), A.ax.c2p(850, d["true"]), color=GOOD, stroke_width=2)
        bands = VGroup(*[Line(A.ax.c2p(n, lo), A.ax.c2p(n, hi), color=MODEL, stroke_width=6)
                         for n, lo, hi in zip(d["n"], d["lo"], d["hi"])])
        meds = VGroup(*[Dot(A.ax.c2p(n, m), radius=0.07, color=WHITE) for n, m in zip(d["n"], d["med"])])
        rows = rows_of([
            (r"the same study run 40 times at each size: \ the bars hold the middle 80\% of the estimates", WHITE),
            (rf"with 50 people, \ the two-day battery is worth anything from \${d['lo'][0]:.0f} to "
             rf"\${d['hi'][0]:.0f}", AUTH),
            (rf"with 800, \ \${d['lo'][-1]:.0f} to \${d['hi'][-1]:.0f}, \ around the planted \${d['true']:.0f}", GOOD),
            (r"a ratio of two estimates is noisier than either; \ price the precision before pricing the product", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{scaling.simulate\_conjoint}, \ \texttt{fit\_clogit}")
        with self.voiceover(
            "How many respondents does a conjoint study need? <bookmark mark='a'/> Run the same study forty times at "
            "each size. The bars hold the middle eighty percent of the estimates. <bookmark mark='b'/> With fifty "
            "people, the two-day battery is worth anything from about a hundred and twenty dollars to nearly two "
            "hundred. <bookmark mark='c'/> With eight hundred, within about fifteen dollars of the planted hundred "
            "and fifty. <bookmark mark='d'/> A willingness to pay is a ratio of two estimates, and noisier than "
            "either. Price the precision before pricing the product."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(truth))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(bands), FadeIn(meds))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
