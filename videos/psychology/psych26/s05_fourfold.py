from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


class Fourfold(VoiceoverScene):
    def construct(self):
        self.card()
        self.curves()
        self.grid()
        self.common_ratio()

    def card(self):
        card = chapter_card(4, r"The fourfold pattern", r"Why insurance and lottery tickets?",
                            lit={1948: r"Friedman \& Savage", 1992: r"Tversky \& Kahneman"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter four. The fourfold pattern."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def curves(self):
        d = load("fourfold")
        head = heading(r"Certainty equivalents, \ computed")
        def panel(ce, col, title, center):
            A = axes([0, 1], [0, 100], x_length=4.6, y_length=3.8, xticks=[0, 0.5, 1], yticks=[0, 50, 100],
                     xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0f}", xlabel=r"chance $p$ of the 100",
                     ylabel=title, center=center, font_size=16)
            ev = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(1, 100), color=NORM, stroke_width=2)
            c = curve(A.ax, d["p"], np.abs(ce), col, 4)
            dots = scatter(A.ax, d["p"], np.abs(ce), col, 0.05, 1)
            return A, ev, c, dots
        Ag, evg, cg, dg = panel(d["gain_ce"], GAIN, r"sure gain as good as ``100 with chance $p$''", [-3.4, -0.5, 0])
        Al, evl, cl, dl = panel(d["loss_ce"], LOSS, r"sure loss as bad as ``$-$100 with chance $p$''",
                                [3.4, -0.5, 0])
        evlab = label(r"expected value", font_size=17, color=NORM).next_to(Ag.ax.c2p(0.8, 80), UL, buff=0.05)
        sg = label(r"seeks risk", font_size=18, color=RISKY).move_to(Ag.ax.c2p(0.17, 32))
        ag = label(r"avoids risk", font_size=18, color=SURE).move_to(Ag.ax.c2p(0.78, 50))
        al = label(r"avoids risk", font_size=18, color=SURE).move_to(Al.ax.c2p(0.17, 32))
        sl = label(r"seeks risk", font_size=18, color=RISKY).move_to(Al.ax.c2p(0.78, 50))
        tag = psyche_tag(r"\texttt{choice.ce}, \ \texttt{fourfold}: \ the 1992 parameters")
        with self.voiceover(
            "Put the two curves together and they compute a pattern. <bookmark mark='a'/> On the left, for each "
            "chance p of winning a hundred, the sure amount that prospect theory, with the 1992 values, rates as "
            "just as good: the certainty equivalent. The dashed line is the expected value. <bookmark mark='b'/> "
            "For small chances the certainty equivalent lies above the expected value: a ten percent chance of a "
            f"hundred is worth about {d['gain_ce'][3]:.0f}, not ten. That's risk seeking. For large chances it lies "
            f"below: ninety-five percent of a hundred is worth only about {d['cell_gain'][1]:.0f}. That's risk "
            "aversion. <bookmark mark='c'/> On the right, losses, and everything flips. A small chance of losing a "
            f"hundred feels as bad as a sure loss of about {abs(d['cell_loss'][0]):.0f} at five percent, more than "
            "its expected five: risk aversion, the kind that buys insurance. A large chance of losing it is "
            f"preferred to a sure loss of {abs(d['cell_loss'][1]):.0f}: risk seeking."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(Ag), FadeIn(Al))
            vo.wait_until("a")
            self.play(Create(evg), FadeIn(evlab), Create(cg), FadeIn(dg), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(sg), FadeIn(ag))
            vo.wait_until("c")
            self.play(Create(evl), Create(cl), FadeIn(dl), FadeIn(al), FadeIn(sl), run_time=2)
        self.clear_scene()

    def grid(self):
        d = load("fourfold")
        head = heading(r"The fourfold pattern of risk attitudes")
        cells = [
            (r"small chance of a gain", d["cell_gain"][0], 5, r"seeks risk", r"lottery tickets", RISKY, GAIN),
            (r"large chance of a gain", d["cell_gain"][1], 95, r"avoids risk", r"settling a strong lawsuit", SURE,
             GAIN),
            (r"small chance of a loss", d["cell_loss"][0], -5, r"avoids risk", r"insurance", SURE, LOSS),
            (r"large chance of a loss", d["cell_loss"][1], -95, r"seeks risk", r"gambling to escape a sure loss",
             RISKY, LOSS),
        ]
        boxes = VGroup()
        for title, ce_, ev_, att, ex, ac, col in cells:
            box = RoundedRectangle(corner_radius=0.12, width=5.6, height=2.05, stroke_color=col, stroke_width=2,
                                   fill_color=BLACK, fill_opacity=0.5)
            body = VGroup(label(title, font_size=23, color=col),
                          label(rf"worth a sure {ce_:.0f}; \ expected value {ev_}", font_size=21, color=WHITE),
                          label(att, font_size=24, color=ac), label(ex, font_size=21, color=GREY_A)).arrange(
                DOWN, buff=0.12).move_to(box)
            boxes.add(VGroup(box, body))
        grid = VGroup(VGroup(boxes[0], boxes[1]).arrange(RIGHT, buff=0.35),
                      VGroup(boxes[2], boxes[3]).arrange(RIGHT, buff=0.35)).arrange(DOWN, buff=0.3)
        grid.move_to([0, 0.05, 0])
        foot = wrapped_label(r"one person, \ one pair of curves: \ insurance and lottery tickets together, \ with no "
                             r"special love of gambling", 12.0, 24, MODEL).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Tversky \& Kahneman (1992); \ Friedman \& Savage (1948)")
        with self.voiceover(
            "Here are the four cells, with prospect theory's certainty equivalents for five and ninety-five percent "
            "chances of a hundred. <bookmark mark='a'/> A small chance of a gain: worth more than its expected "
            "value, so people seek risk. Lottery tickets. <bookmark mark='b'/> A large chance of a gain: worth less, "
            "so people avoid risk, and accept a settlement below the expected value of a strong lawsuit. "
            "<bookmark mark='c'/> A small chance of a loss: feared more than its expectation, so people avoid risk "
            "and pay for insurance. <bookmark mark='d'/> A large chance of a loss: people seek risk, gambling to "
            "escape a sure loss, as a trader doubles down or a defendant goes to trial. Tversky and Kahneman's own "
            "medians in 1992 showed the same four signs. <bookmark mark='e'/> So that's the answer to today's "
            "question. In 1948 Milton Friedman and Leonard Savage needed a utility curve with a strange wiggle to "
            "explain why one person buys both insurance and lottery tickets. Prospect theory needs no wiggle: the "
            "overweighting of small probabilities does it, for gains and losses alike."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, b in zip("abcd", boxes):
                vo.wait_until(m)
                self.play(FadeIn(b, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def common_ratio(self):
        d = load("fourfold")
        head = heading(r"One more: \ the common-ratio effect")
        pct_ = d["kt_pct"]
        rows_l = VGroup(
            label(r"4{,}000 at .80, \ or 3{,}000 for sure", font_size=26, color=WHITE),
            label(rf"{100 - pct_['P3']}\% \ take the sure 3{{,}}000", font_size=26, color=SURE),
            label(r"4{,}000 at .20, \ or 3{,}000 at .25", font_size=26, color=WHITE),
            label(rf"{pct_['P4']}\% \ take the 4{{,}}000", font_size=26, color=RISKY),
        ).arrange(DOWN, buff=0.3).move_to([-3.2, 0.6, 0])
        rows = rows_of([
            (r"the second pair is the first with every chance divided by four", WHITE),
            (r"expected utility says the ratio of chances is all that matters: \ the choice should not change", NORM),
            (r"prospect theory, \ with the 1992 values, \ makes both popular choices: \ the sure thing, \ then the "
             r"larger prize", MODEL),
        ], 5.8, 23, 0.32).move_to([3.4, 0.4, 0])
        tag = published_tag(r"Kahneman \& Tversky (1979), \ Problems 3 and 4, \ $N = 95$")
        assert d["kt_verdict"]["P3"] == "other" and d["kt_verdict"]["P4"] == "risky"
        with self.voiceover(
            "One more classic, which the same two curves also handle. <bookmark mark='a'/> Offered four thousand "
            f"with probability point eight or three thousand for sure, {100 - pct_['P3']} percent took the sure "
            f"thing. Offered four thousand at point two or three thousand at point two five, {pct_['P4']} percent "
            "took the four thousand. <bookmark mark='b'/> The second pair is the first with every chance divided by "
            "four. <bookmark mark='c'/> For expected utility only the ratio of the chances matters, so the choice "
            "shouldn't flip. <bookmark mark='d'/> For prospect theory it does: the certainty effect protects the "
            "sure three thousand, and once both are long shots, the bigger prize wins. Computed with the 1992 "
            "values, the theory makes both of the popular choices."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_l], lag_ratio=0.6), run_time=4)
            for m, r in zip("bcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
