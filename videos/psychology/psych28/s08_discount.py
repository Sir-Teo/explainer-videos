from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Discount(VoiceoverScene):
    def construct(self):
        self.card()
        self.on_you()
        self.staircase()
        self.curves()
        self.meaning()

    def card(self):
        card = chapter_card(7, r"On you: \ sooner or later", r"How much is a later reward worth to you now?",
                            lit={1987: r"Mazur", 1999: r"Kirby et al.", 2001: r"Myerson et al."},
                            part=PART, scale=("mind", "person"), marr=("what", "how"))
        with self.voiceover("Chapter seven. On you: sooner or later."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def on_you(self):
        stage = demo_stage(12.4, 4.6, center=[0, 0.4, 0])
        q = label(r"50 now, \ or 100 in a month?", font_size=46, color=YOU).move_to([0, 1.2, 0])
        q2 = label(r"75 now, \ or 100 in a month?", font_size=46, color=YOU).move_to([0, 1.2, 0])
        q3 = label(r"62.50 now, \ or 100 in a month?", font_size=46, color=YOU).move_to([0, 1.2, 0])
        note = rows_of([
            (r"answer each in your head, \ honestly, \ before the next", WHITE),
            (r"each answer moves the next offer halfway toward where you switch: \ the adjusting-amount procedure",
             INTR),
        ], 11.6, 25, 0.25).move_to([0, -0.7, 0])
        with self.voiceover(
            "Let's measure something about you. <bookmark mark='a'/> Fifty pounds, or dollars, or euros, now, or a "
            "hundred in a month? Answer in your head, honestly. <bookmark mark='b'/> If you took the fifty, the next "
            "offer is lower; if you waited, it's higher. Say you waited: seventy-five now, or a hundred in a month? "
            "<bookmark mark='c'/> And if you'd now take the seventy-five, the step halves again: sixty-two fifty "
            "now, or a hundred in a month? <bookmark mark='d'/> Each answer moves the next offer halfway toward "
            "the point where you switch. Six questions pin it to within a couple of percent. It's called the "
            "adjusting-amount procedure, and this part's interactive runs it on you at six delays."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(q), FadeIn(note[0]))
            vo.wait_until("b")
            self.play(ReplacementTransform(q, q2))
            vo.wait_until("c")
            self.play(ReplacementTransform(q2, q3))
            vo.wait_until("d")
            self.play(FadeIn(note[1]))
        self.clear_scene()

    def staircase(self):
        d = load("titration")
        offers = d["offers"][2]  # the 30-day delay for the middle chooser
        head = heading(r"Six questions, \ one indifference point")
        A = axes([0, 6], [0, 100], x_length=5.6, y_length=3.6, xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[0, 50, 100],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"question", ylabel=r"offer now, \ of 100 later",
                 center=[-3.3, -0.2, 0], font_size=16)
        later = 100 / (1 + d["middle_k"] * 30)
        target = DashedLine(A.ax.c2p(0, later), A.ax.c2p(6, later), color=GREY_B, stroke_width=2)
        tl = label(rf"true indifference {later:.1f}", font_size=16, color=GREY_B).next_to(A.ax.c2p(0.15, later), UP,
                                                                                          buff=0.05, aligned_edge=LEFT)
        dots = VGroup()
        for i, o in enumerate(offers):
            took_now = i < len(offers) - 1 and offers[i + 1] < o
            col = EXTR if took_now else INTR
            if i == len(offers) - 1:
                col = WHITE
            dots.add(Dot(A.ax.c2p(i, float(o)), color=col, radius=0.08))
        steps = VGroup(*[Line(A.ax.c2p(i, float(offers[i])), A.ax.c2p(i + 1, float(offers[i + 1])), color=GREY_C,
                              stroke_width=2) for i in range(len(offers) - 1)])
        key = legend([(INTR, r"waited: \ offer rises"), (EXTR, r"took it now: \ offer falls")], font_size=16)
        key.move_to(A.ax.c2p(4.2, 18))
        rows = rows_of([
            (r"Psyche: \ a hyperbolic chooser, \ $V = A / (1 + kD)$, \ with $k = 0.02$ a day, \ asked about 100 in "
             r"30 days", MODEL),
            (r"start at half; \ each step is half the last; \ after six steps the offer is within 1.6 of where the "
             r"chooser switches", WHITE),
            (rf"the procedure lands on {offers[-1]:.1f}, \ against a true {later:.1f}", INTR),
            (r"people are noisier than Psyche: \ the interactive repeats a delay to see how consistent you are",
             BODY),
        ], 5.6, 21, 0.3).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{drive.discount\_titration}")
        with self.voiceover(
            "Here's the procedure run on Psyche. <bookmark mark='a'/> Psyche's chooser discounts hyperbolically, as "
            "in Part 26: a reward A at delay D is worth A over one plus k D, with k of 0.02 a day. We ask it about a "
            "hundred in thirty days. <bookmark mark='b'/> The offer starts at half, fifty. Each answer moves it by "
            "a step, and each step is half the last, so after six questions the offer is within about one and a half "
            "of the switching point. <bookmark mark='c'/> The procedure lands on "
            f"{offers[-1]:.1f}, against a true indifference point of {later:.1f}. <bookmark mark='d'/> People are "
            "noisier than Psyche, so the interactive asks one delay twice, to see how consistent you are."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(target), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(key), LaggedStart(*[AnimationGroup(FadeIn(dt), Create(st))
                                                                  for dt, st in zip(dots, steps)], lag_ratio=0.5),
                      run_time=3.0)
            self.play(FadeIn(dots[-1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(dots[-1], color=WHITE))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def curves(self):
        d = load("titration")
        head = heading(r"Three choosers, \ three curves")
        A = axes([0, 365], [0, 105], x_length=5.8, y_length=3.8, xticks=[0, 90, 180, 365], yticks=[0, 50, 100],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"delay, \ days",
                 ylabel=r"worth now, \ of 100 later", center=[-3.3, -0.2, 0], font_size=16)
        g = d["grid"]
        objs = VGroup()
        items = (("patient", INTR), ("middle", BODY), ("impulsive", EXTR))
        for name, col in items:
            k = d[f"{name}_fit"]
            objs.add(VGroup(curve(A.ax, g, 100 / (1 + k * g), col, 3),
                            scatter(A.ax, d["delay"], d[f"{name}_ind"], col, 0.07, 1.0)))
        key = legend([(c, rf"$k = {d[n + '_k']:g}$: \ area {d[n + '_auc']:.2f}") for n, c in items], font_size=17)
        key.move_to(A.ax.c2p(250, 85))
        eq = MathTex(r"\text{AUC} = \int_0^1 \frac{V(D)}{A}\, d\!\left(\frac{D}{D_{\max}}\right)", font_size=32)
        rows = rows_of([
            (r"six delays, \ from a day to a year: \ six indifference points per chooser", WHITE),
            (r"the fitted $k$ recovers each chooser's rate: \ "
             rf"{d['patient_fit']:.3f}, \ {d['middle_fit']:.3f}, \ {d['impulsive_fit']:.3f}", MODEL),
            (r"the area under the points needs no model: \ 1 for a chooser who does not discount, \ near 0 for one "
             r"who wants everything now \ (Myerson, \ Green and Warusawitharana, \ 2001)", INTR),
        ], 5.6, 21, 0.3)
        right = VGroup(eq, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{drive.discount\_titration}: \ three choosers")
        with self.voiceover(
            "Run the procedure at six delays, from a day to a year, and you have a discount curve. "
            "<bookmark mark='a'/> Here are three of Psyche's choosers, patient, middling and impulsive, each a set of "
            "six indifference points. <bookmark mark='b'/> Fitting the hyperbola recovers each chooser's rate. "
            "<bookmark mark='c'/> A second summary needs no model at all: the area under the points, with delay and "
            "value both scaled to run from zero to one. It's one for someone who doesn't discount, and near zero for "
            "someone who wants everything now. Joel Myerson, Leonard Green and Mel Warusawitharana proposed it in "
            "2001, because people's curves often aren't quite hyperbolic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(o) for o in objs], lag_ratio=0.4), FadeIn(key), FadeIn(rows[0]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def meaning(self):
        head = heading(r"What a discount rate measures")
        rows = rows_of([
            (r"heroin users discounted more steeply than controls in 1999, \ and similar results followed for "
             r"smoking, \ problem drinking and gambling: \ a candidate marker across disorders \ (Part 41)", EXTR),
            (r"but a choice about money is also a judgment about the world: \ will the later payment really come? \ "
             r"is money needed now?", WANT),
            (r"discounting is fairly stable within a person over months, \ and also moves with circumstances", BODY),
            (r"which is the question behind the next three chapters: \ is self-control a trait, \ a resource, \ or "
             r"a sensible reading of one's world?", WHITE),
        ], 12.2, 27, 0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Kirby, \ Petry \& Bickel (1999); \ Myerson, \ Green \& Warusawitharana (2001)")
        with self.voiceover(
            "What does your number measure? <bookmark mark='a'/> In 1999 Kris Kirby, Nancy Petry and Warren Bickel "
            "found that heroin users discounted delayed money more steeply than people who didn't use drugs, and "
            "similar results followed for smoking, problem drinking and gambling. It's a candidate marker across "
            "disorders, as Part 41 will discuss. <bookmark mark='b'/> But a "
            "choice about money is also a judgment about the world. Will the later payment really come? Is money "
            "needed now? <bookmark mark='c'/> Discounting is fairly stable within a person over months, and it "
            "also moves with circumstances. <bookmark mark='d'/> And that is the question behind the next three "
            "chapters. Is self-control a trait, a resource that runs down, or a sensible reading of one's world?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
