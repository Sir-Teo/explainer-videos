from __future__ import annotations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403


class Bayes(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.screening()
        self.frequencies()
        self.odds()
        self.ages()
        self.second_test()

    def card(self):
        card = chapter_card(6, r"Bayes' theorem", r"From the chance of the evidence to the chance of the cause",
                            lit=(1763,), part=PART)
        with self.voiceover("Chapter six. Bayes' theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        hc = history_card(1763, r"Thomas Bayes, \ a Presbyterian minister (d.\ 1761)", r"``An essay towards solving "
                          r"a problem in the doctrine of chances'', \ sent to the Royal Society by Richard Price; \ "
                          r"Laplace found the theorem independently (1774) and made it a method", color=S.MUSEUM,
                          width=6.0, font_size=22).to_corner(UL, buff=0.35)
        rows = [
            cmath(r"P(A \cap B)", r"=", r"P(B)\, P(A \mid B)", r"=", r"P(A)\, P(B \mid A)", font_size=36),
            cmath(r"P(A \mid B)", r"=", r"\frac{P(B \mid A)\, P(A)}{P(B)}", font_size=40),
            cmath(r"P(A \mid B)", r"=", r"\frac{P(B \mid A)\, P(A)}{P(B \mid A)\, P(A) + P(B \mid A^c)\, P(A^c)}",
                  font_size=36),
        ]
        whys = [why(r"multiplication rule, \ both ways"), why(r"divide by $P(B)$"), why(r"total probability, \ "
                                                                                      r"$B$ with $A$ or without")]
        for r in rows[1:]:
            r[0].set_color(S.POST)
        th = theorem_card(r"Bayes' theorem", r"the chance of the cause given the evidence, \ from the chance of the "
                          r"evidence given the cause", color=S.POST, width=6.0, font_size=23).to_corner(UL, buff=0.35)
        with self.voiceover(
            "The theorem is named for Thomas Bayes, a Presbyterian minister in Tunbridge Wells. "
            "<bookmark mark='a'/> His essay was found among his papers after his death and sent to the Royal "
            "Society by his friend Richard Price in 1763. Laplace discovered the same result on his own eleven "
            "years later, and it was Laplace who turned it into a method. <bookmark mark='b'/> The derivation is "
            "one line. The chance of A and B can be built in either order: B, then A given B; or A, then B given A. "
            "<bookmark mark='c'/> Divide by the chance of B. The probability of A given B equals the probability of "
            "B given A, times the probability of A, over the probability of B. <bookmark mark='d'/> And the "
            "denominator, by total probability, splits into the two ways B can happen: with A, or without it. "
            "<bookmark mark='e'/> It turns the chance of the evidence given the cause, which we can often measure, "
            "into the chance of the cause given the evidence, which is what we want."
        ) as vo:
            self.play(FadeIn(hc))
            step = ladder(self, rows, whys, keep=3, top=1.5, x=-0.6, buff=0.55)
            vo.wait_until("b")
            self.play(FadeOut(hc))
            step(0)
            vo.wait_until("c")
            step(1, transform=False)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            self.play(FadeIn(th, shift=UP * 0.2))
        self.clear_scene()

    def screening(self):
        d = load("bayes")
        prev, sens, spec = d["prev"], d["sens"], d["spec"]
        cards = VGroup(
            label(rf"a silent condition: \ {100 * prev:.2f}\% of the World's {fmt_int(d['n'])} adults", font_size=28,
                  color=SICK),
            label(r"a test: \ sensitivity $90\%$ \ (positive if you have it)", font_size=28, color=POS),
            label(r"specificity $95\%$ \ (negative if you don't)", font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.5)
        q = label(r"You test positive. \ How likely is it that you have the condition?", font_size=34,
                  color=S.ACCENT).move_to([0, 0.3, 0])
        pc = pause_card(r"Most people guess about $90\%$. \ What do you think?", width=7.0, font_size=26)
        pc.move_to([0, -1.9, 0])
        tag = simulated_tag()
        with self.voiceover(
            "Here's where it matters. <bookmark mark='a'/> In the World, a silent condition affects about one adult "
            f"in a hundred: {100 * prev:.2f} percent of the World's {fmt_int(d['n'])} adults, more of the old than "
            "the young. <bookmark mark='b'/> There's a screening test. It catches ninety percent of people who have "
            "the condition: its sensitivity. <bookmark mark='c'/> And it correctly clears ninety-five percent of "
            "those who don't: its specificity. <bookmark mark='d'/> You take the test, and it's positive. How likely "
            "is it that you have the condition? <bookmark mark='e'/> Pause and make a guess. Many people, doctors "
            "included, say something close to ninety percent."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(2.0)
        self.clear_scene()

    def frequencies(self):
        d = load("bayes")
        nf = d["nf"]
        sick_g, pos_g = np.asarray(d["grid_sick"]), np.asarray(d["grid_pos"])
        order = np.lexsort((~pos_g, ~sick_g))  # sick first, positives first within each
        cols = [SICK if sick_g[i] else WELL for i in order]
        arr = icon_array(cols, cols=40, size=0.13, buff=0.04).move_to([-2.6, 0.2, 0])
        cap = label(r"$1{,}000$ of the World's adults: \ each square a person", font_size=24, color=GREY_A)
        cap.next_to(arr, UP, buff=0.25)
        pos_marks = VGroup(*[Square(side_length=0.17, stroke_color=POS, stroke_width=1.6, fill_opacity=0)
                             .move_to(arr[k]) for k, i in enumerate(order) if pos_g[i]])
        n_sick, n_pos = int(sick_g.sum()), int(pos_g.sum())
        n_sp = int((sick_g & pos_g).sum())
        tally = VGroup(
            label(rf"have it: \ {n_sick}", font_size=28, color=SICK),
            label(rf"positive: \ {n_pos}", font_size=28, color=POS),
            label(rf"positive \emph{{and}} have it: \ {n_sp}", font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.4, 1.4, 0])
        frac_ = MathTex(rf"\frac{{{n_sp}}}{{{n_pos}}}", rf"= {n_sp / n_pos:.2f}", font_size=40, color=S.POST)
        frac_.next_to(tally, DOWN, buff=0.5)
        # the natural-frequency tree, per 10,000
        lv = [r"10{,}000", "", WHITE, [
            (rf"{nf['sick']}\ \text{{have it}}", r"1\%", SICK, [(rf"{nf['sick_pos']}\ +", r"90\%", POS, []),
                                                                 (rf"{nf['sick'] - nf['sick_pos']}\ -", r"10\%", GREY_B, [])]),
            (rf"{fmt_int(nf['well'])}\ \text{{don't}}", r"99\%", WELL, [(rf"{nf['well_pos']}\ +", r"5\%", POS, []),
                                                                          (rf"{fmt_int(nf['well'] - nf['well_pos'])}\ -",
                                                                           r"95\%", GREY_B, [])]),
        ]]
        tree = prob_tree(lv, x0=-5.6, dx=3.3, height=4.6, font_size=28)
        tree.move_to([-1.2, -0.3, 0])
        nf_eq = MathTex(rf"\frac{{{nf['sick_pos']}}}{{{nf['sick_pos']} + {nf['well_pos']}}}",
                        rf"= {nf['post']:.3f}", font_size=40, color=S.POST).move_to([4.8, -0.3, 0])
        gg = label(r"natural frequencies: \ Gigerenzer \& Hoffrage, 1995", font_size=22, color=GREY_B)
        gg.to_corner(DR, buff=0.3)
        tag = simulated_tag(corner=DL)
        with self.voiceover(
            "Let's count instead of guessing. <bookmark mark='a'/> Here are a thousand of the World's adults, one "
            f"square each. <bookmark mark='b'/> {n_sick} of them have the condition. <bookmark mark='c'/> Now test "
            f"everyone. The test catches most of the {n_sick}, but it also flags five percent of the healthy "
            f"majority, and five percent of a big number is a big number. <bookmark mark='d'/> {n_pos} people test "
            f"positive, and only {n_sp} of them have the condition. About one positive in six. "
            "<bookmark mark='e'/> The same calculation is easier to see in round numbers, a style of reasoning "
            "called natural frequencies. Of ten thousand people, a hundred have the condition and ninety of them "
            "test positive. Of the nine thousand nine hundred who don't, four hundred and ninety-five test "
            f"positive too. <bookmark mark='f'/> So of five hundred and eighty-five positives, ninety are real: "
            f"{100 * nf['post']:.1f} percent. Studies by Gerd Gigerenzer and Ulrich Hoffrage found that people "
            "reason far better in counts like these than in percentages and conditional probabilities."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(arr, lag_ratio=0.002), FadeIn(cap), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(tally[0]), *[Indicate(arr[k], color=SICK, scale_factor=1.8)
                                         for k, i in enumerate(order) if sick_g[i]])
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(m) for m in pos_marks], lag_ratio=0.01), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(tally[1]), FadeIn(tally[2]))
            self.play(Write(frac_))
            vo.wait_until("e")
            self.play(FadeOut(VGroup(arr, cap, pos_marks, tally, frac_)))
            self.play(FadeIn(tree, lag_ratio=0.05), run_time=2.0)
            vo.wait_until("f")
            for p in ((0, 0), (1, 0)):
                self.play(tree.edges[p[:1]].animate.set_color(POS).set_stroke(width=5),
                          tree.edges[p].animate.set_color(POS).set_stroke(width=5), run_time=0.5)
            self.play(Write(nf_eq), FadeIn(gg))
        self.clear_scene()

    def odds(self):
        d = load("bayes")
        rows = [
            cmath(r"\frac{P(A \mid B)}{P(A^c \mid B)}", r"=", r"\frac{P(A)}{P(A^c)}", r"\times",
                  r"\frac{P(B \mid A)}{P(B \mid A^c)}", font_size=38),
            cmath(r"\text{posterior odds}", r"=", r"\text{prior odds}", r"\times", r"\text{likelihood ratio}",
                  font_size=36),
            cmath(rf"{d['post_odds']:.3f}", r"=", rf"\frac{{{100 * d['prev']:.2f}}}{{{100 - 100 * d['prev']:.2f}}}",
                  r"\times", r"\frac{0.90}{0.05}", font_size=38),
        ]
        for r in rows:
            r[0].set_color(S.POST)
            r[2].set_color(S.PRIOR)
            r[4].set_color(S.LIK)
        whys = [why(r"Bayes for $A$ and for $A^c$, \ divided: \ $P(B)$ cancels"), None,
                why(r"the World's prevalence; \ $18$ for this test")]
        back = MathTex(rf"P(A \mid +) = \frac{{{d['post_odds']:.3f}}}{{1 + {d['post_odds']:.3f}}} = {d['exact']:.3f}",
                       font_size=36, color=S.POST)
        real = MathTex(rf"\text{{in the World: }} \tfrac{{{fmt_int(d['n_sick_pos'])}}}{{{fmt_int(d['n_pos'])}}} = "
                       rf"{d['realized']:.3f}", font_size=32, color=SIM)
        bot = VGroup(back, real).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        title = label(r"Bayes in odds form", font_size=36).to_edge(UP, buff=0.4)
        with self.voiceover(
            "There's a neater way to write Bayes' theorem, and it's the form to remember. <bookmark mark='a'/> "
            "Write Bayes for the condition and for its absence, and divide one by the other: the awkward "
            "denominator cancels. <bookmark mark='b'/> What's left says posterior odds equal prior odds times the "
            "likelihood ratio. Prior odds, purple, are what you believed before the evidence. The likelihood ratio, "
            "green, is how much more likely the evidence is if the condition is present than if it isn't. Their "
            "product, orange, is what you should believe after. <bookmark mark='c'/> For our test the likelihood "
            "ratio is ninety percent over five percent, eighteen. The prior odds are about one to a hundred. So the "
            "posterior odds are about eighteen to a hundred: <bookmark mark='d'/> a probability of fifteen percent. "
            f"<bookmark mark='e'/> And the World itself, with all its {fmt_int(d['n_pos'])} positive adults, gives "
            f"{d['realized']:.3f}. A strong test, applied to a rare condition, mostly finds false alarms."
        ) as vo:
            self.play(FadeIn(title))
            step = ladder(self, rows, whys, keep=3, top=2.5, x=-0.4, buff=0.55)
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            self.play(Write(back))
            vo.wait_until("e")
            self.play(FadeIn(real, shift=UP * 0.2))
        self.clear_scene()

    def ages(self):
        d = load("bayes")
        groups = d["by_age"]
        A = axes([0, 4], [0, 0.45], x_length=7.6, y_length=4.4, ylabel=r"P(condition $\mid$ positive)",
                 yticks=[0, 0.1, 0.2, 0.3, 0.4], center=[-1.6, -0.2, 0])
        ax = A.ax
        bars, labs, vals, prevs = VGroup(), VGroup(), VGroup(), VGroup()
        for k, g in enumerate(groups):
            h = g["post"]
            b = Rectangle(width=1.1, height=ax.c2p(0, h)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=S.POST,
                          fill_opacity=0.85).move_to(ax.c2p(k + 0.5, h / 2))
            bars.add(b)
            hi = g["hi"] if g["hi"] < 100 else None
            labs.add(label(rf"{g['lo']}--{hi - 1}" if hi else rf"{g['lo']}+", font_size=24, color=GREY_A)
                     .next_to(ax.c2p(k + 0.5, 0), DOWN, buff=0.15))
            vals.add(MathTex(f"{h:.2f}", font_size=26, color=S.POST).next_to(b, UP, buff=0.1))
            prevs.add(MathTex(rf"{100 * g['prev']:.1f}\%", font_size=22, color=SICK).next_to(labs[-1], DOWN, buff=0.12))
        dots = VGroup(*[Dot(ax.c2p(k + 0.5, g["realized"]), radius=0.07, color=SIM) for k, g in enumerate(groups)])
        leg = VGroup(label(r"age group", font_size=22, color=GREY_A), label(r"prevalence", font_size=22, color=SICK))
        leg.arrange(DOWN, aligned_edge=RIGHT, buff=0.2).next_to(labs[0], LEFT, buff=0.35).shift(DOWN * 0.2)
        right = VGroup(label(r"same test, \ same result,", font_size=30), label(r"different meaning", font_size=30,
                                                                                 color=S.ACCENT),
                       label(r"bars: \ Bayes, exactly", font_size=24, color=S.POST),
                       label(r"dots: \ the World's positives", font_size=24, color=SIM)).arrange(DOWN, aligned_edge=LEFT,
                                                                                          buff=0.25)
        right.move_to([4.7, 1.0, 0])
        tag = simulated_tag()
        with self.voiceover(
            "In the World, the condition is rarer in the young. <bookmark mark='a'/> Split the adults by age, and "
            "apply the same test. The prior changes with age, and so does the posterior. <bookmark mark='b'/> A "
            f"positive test means a {100 * groups[0]['post']:.0f} percent chance for someone under thirty-five and a "
            f"{100 * groups[-1]['post']:.0f} percent chance for someone over seventy-five. <bookmark mark='c'/> The "
            "World's actual positives, blue dots, agree with Bayes in every group. Same test, same result, different "
            "meaning. That's why screening programmes target the people most at risk: the test is only as good as "
            "the prior it multiplies."
        ) as vo:
            self.play(FadeIn(A), FadeIn(labs), FadeIn(leg), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(prevs))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(vals))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(dt, scale=1.5) for dt in dots], lag_ratio=0.2), FadeIn(right))
        self.clear_scene()

    def second_test(self):
        d = load("bayes")
        rows = [
            cmath(r"\text{odds after one positive}", r"=", r"\text{prior odds}", r"\times", r"18", font_size=34),
            cmath(r"\text{odds after two positives}", r"=", r"\text{prior odds}", r"\times", r"18 \times 18",
                  font_size=34),
            cmath(r"P(A \mid +,+)", r"=", rf"{d['post2']:.3f}", font_size=38),
        ]
        rows[2][2].set_color(S.POST)
        whys = [None, why(r"if the tests err independently, \ given the condition: \ chapter 9"), None]
        real = MathTex(rf"\text{{in the World: }} {d['realized2']:.3f} \ \ ({fmt_int(d['n_both'])} \text{{ adults}})",
                       font_size=30, color=SIM).to_edge(DOWN, buff=1.0)
        take = label(r"evidence multiplies odds; \ the prior never disappears, \ but it can be overwhelmed",
                     font_size=28, color=S.ACCENT).to_edge(DOWN, buff=0.35)
        intro = label('A second positive test', font_size=36)
        with self.voiceover(
            "What happens if we observe a second positive test? <bookmark mark='a'/> After one positive, the odds "
            "are the prior odds times eighteen. That posterior becomes the prior for the next test. "
            "<bookmark mark='b'/> A second positive multiplies by eighteen again, provided the two tests make their "
            "mistakes independently of each other, among people with the condition and among people without; "
            "that's a condition we'll examine in chapter nine. <bookmark mark='c'/> Now the probability is "
            f"{100 * d['post2']:.0f} percent. <bookmark mark='d'/> The World's adults who tested positive twice "
            f"agree: {100 * d['realized2']:.1f} percent of them have the condition. <bookmark mark='e'/> Evidence "
            "multiplies odds. The prior never disappears from the calculation, but enough evidence can overwhelm "
            "it. That one sentence is the whole of Bayesian statistics, which begins in Part 15."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=0.4, buff=0.7)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            step(0, transform=False)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(real))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.2))
        self.clear_scene()
