from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import (ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, axes3d, fixed, hint3d, illustration,
                                         load, surf)

RECORD = [
    (r"April 2024", r"Jane Street sues Millennium Management and two former traders in New York (S.D.N.Y. 24-cv-2783), "
     r"alleging they took a trading strategy; a hearing reveals it concerns Indian options. Settled in December 2024, "
     r"terms undisclosed (as reported by Bloomberg Law)."),
    (r"3 July 2025", r"SEBI's interim order: four entities (JSI Investments, JSI2 Investments, Jane Street Singapore, "
     r"Jane Street Asia Trading) barred from Indian markets; Rs 4{,}843.57 crore of what the order calls "
     r"``unlawful gains'' to be impounded. Allegations, made ex parte."),
    (r"July 2025", r"The firm deposits the amount in escrow ``without prejudice''; on 21 July SEBI says the trading "
     r"restrictions ``cease to apply'' under the order's terms, with exchanges told to watch its positions."),
    (r"September 2025", r"The firm appeals to the Securities Appellate Tribunal, seeking documents it says it needs "
     r"for its defence; the tribunal admits the appeal."),
    (r"21 October 2026", r"The tribunal reserves its order on the document dispute (as reported by LiveLaw). No final "
     r"finding on the allegations at the time of writing."),
]


class Case(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.allegation()
        self.record()
        self.toy(load("alleged"))
        self.surface(load("alleged_surface"))

    def card(self):
        c = chapter_card(15, r"Case file: SEBI and Jane Street (alleged)", r"What was alleged, and what is the record?",
                         lit=(2024,), part=PART)
        with self.voiceover("Chapter fifteen. A case file: the Indian regulator's interim order against Jane Street. "
                            "These are allegations, contested by the firm."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def allegation(self):
        card = crisis_card(
            r"3 July 2025", r"SEBI's interim order against Jane Street",
            r"In an interim order, SEBI alleged that on expiry days of the Bank Nifty index, entities of the Jane "
            r"Street group bought the index's constituents and futures in the morning, supporting the index while "
            r"building large positions in index options that would profit from a fall, and then sold in the "
            r"afternoon, pushing the index down. SEBI barred the entities and impounded Rs 4{,}843.57 crore of what it "
            r"called unlawful gains. Jane Street disputes the findings; it deposited the amount in escrow and was "
            r"allowed to resume trading while the case continues.",
            stats=[(r"\text{Rs } 4{,}843.57\ \text{cr}", r"impounded, pending the case"),
                   (r"\text{alleged}", r"not proven; contested by the firm")],
            width=11.4, font_size=23)
        card.move_to(ORIGIN)
        src = note(r"SEBI interim order, 3 July 2025, and SEBI's statement of 21 July 2025; the firm's public "
                   r"statements. Allegations; no final finding had been made at the time of writing.", font_size=17,
                   color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "On the third of July 2025, India's Securities and Exchange Board issued an interim order against four "
            "entities of the Jane Street group. These are allegations, made before the firm was heard, and the firm "
            "contests them. SEBI alleged that on expiry days of the Bank Nifty index, the firm bought the index's "
            "member stocks and futures in the morning, holding the index up while building large positions in index "
            "options that would gain if it fell, then sold in the afternoon and pushed it down. "
            "<bookmark mark='a'/> The order impounded four thousand eight hundred and forty-three crore rupees, about "
            "half a billion dollars, of what it called unlawful gains. Jane Street said it disputed the findings."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(Indicate(card[-1] if len(card) else card, scale_factor=1.02))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def record(self):
        rows = VGroup()
        for d, t in RECORD:
            rows.add(VGroup(label(d, font_size=21, color=QC.CRISIS), wrapped_label(t, 9.6, 19, GREY_A)).arrange(
                RIGHT, buff=0.35, aligned_edge=UP))
        for r_ in rows:
            r_[1].align_to(rows[0][1], LEFT)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        for r_ in rows:
            r_[1].shift(RIGHT * (2.6 - (r_[1].get_left()[0] - r_[0].get_left()[0])))
        rows.to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.5)
        if rows.height > 6.6:
            rows.scale_to_fit_height(6.6)
        head = label(r"The public record", font_size=26, color=GREY_B).next_to(rows, UP, buff=0.15).align_to(rows, LEFT)
        with self.voiceover(
            "The public record, in order. In April 2024 Jane Street sued the hedge fund Millennium Management and "
            "two of its own former traders in New York, alleging that they had taken a trading strategy; a hearing "
            "revealed that it concerned Indian options. The case was settled that December, on terms that were not "
            "disclosed. <bookmark mark='a'/> Then the interim order of July 2025, and that month the escrow deposit "
            "and the lifting of the trading bar. <bookmark mark='b'/> In September 2025 the firm appealed to the "
            "Securities Appellate Tribunal, arguing that it had not been given documents it needed for its defence. "
            "<bookmark mark='c'/> In October 2026, as reported by the legal press, the tribunal reserved its order on "
            "that dispute. There is no final finding on the allegations at the time of writing, and this course does "
            "not judge them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2), FadeIn(rows[2], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[4], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def toy(self, a):
        t, idx = np.asarray(a["t"]), np.asarray(a["index"])
        g = axes([0, 1], [98.5, 101.5], x_length=6.4, y_length=3.6, xlabel=r"the trading day",
                 ylabel=r"index", xticks=[0, 0.5, 1], xfmt=lambda u: {0: "open", 0.5: "noon", 1: "close"}[round(u * 2) / 2],
                 yticks=[99, 100, 101], font_size=17).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        tr = ValueTracker(0.0)
        line = tracing(ax, t, idx, tr, SPOT, stroke_width=3.5)
        rows = VGroup(
            label(r"a toy with linear price impact, to explain the mechanics alleged:", font_size=21, color=GREY_A),
            MathTex(rf"\text{{morning: buy }} Q = {a['Q']:.0f}\ \Rightarrow\ +{a['move_up']:.0f}\ \text{{point}}",
                    font_size=28),
            MathTex(rf"\text{{options: short delta of }} {a['D']:.0f}\ \text{{units, near the top}}", font_size=28,
                    color=VEGA),
            MathTex(rf"\text{{afternoon: sell }} 2Q\ \Rightarrow\ -{a['move_down']:.0f}\ \text{{points}}", font_size=28),
            MathTex(rf"\text{{cash and futures: }} {a['cash_leg']:+.0f};\ \ \text{{options: }} {a['options_leg']:+.0f}",
                    font_size=28, color=OPT),
            wrapped_label(r"if the options position is much larger than the trading that moves the index, the trading "
                          r"can roughly break even and the whole still profit. Whether this happened is for SEBI and the "
                          r"courts", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        src = illustration(r"illustration: invented numbers, not the case's")
        with self.voiceover(
            "Why would anyone trade like that? A toy model with invented numbers shows the mechanics; it is not "
            "evidence of anything. Buying in the morning pushes an index up a point. <bookmark mark='a'/> Meanwhile "
            "a position in index options that gains if the index falls is built, much larger than the trading. "
            "<bookmark mark='b'/> In the afternoon, selling twice as much pushes the index two points down by the "
            "close. The cash and futures trading roughly breaks even, but the options gain on a scale set by their "
            "size. <bookmark mark='c'/> That is all the toy shows: why regulators watch expiry days, and the size of "
            "options positions next to the trading in the underlying, together."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(rows[0]))
            self.add(line)
            self.play(tr.animate.set_value(len(t) * 0.45), FadeIn(rows[1]), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(tr.animate.set_value(len(t) - 1), FadeIn(rows[3]), run_time=2)
            self.play(FadeIn(rows[4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def surface(self, s):
        Qs, Ds = np.asarray(s["Q"]), np.asarray(s["D"])
        lam = s["lam"]
        top = float(np.abs(np.asarray(s["net"])).max())
        ax = axes3d([0, 200, 50], [0, 400, 100], [-1, 1, 0.5], x_length=6.8, y_length=5.0, z_length=3.0)
        f = lambda q, d: float((-lam * q * q + 2 * lam * q * d) / top)  # noqa: E731
        sf = surf(ax, f, (0, 200), (0, 400), [(QC.LOSS, -0.5), (GREY_D, 0.0), (QC.GAIN, 0.8)], resolution=(22, 20),
                  opacity=0.8)
        edge = VMobject(stroke_color=YELLOW, stroke_width=6).set_points_as_corners(
            [ax.c2p(q, q / 2, 0) + OUT * 0.03 for q in np.linspace(0, 200, 30)])
        hint = hint3d((r"trading that moves the index, $Q$", SPOT), (r"options exposure, $D$", VEGA),
                      (r"net P\&L (scaled)", OPT), ax=ax)
        eqs = VGroup(MathTex(r"\text{cash} = -\lambda Q^2,\quad \text{options} = D \cdot 2\lambda Q", font_size=28),
                     MathTex(r"\text{net} > 0 \iff D > Q/2", font_size=32, color=YELLOW),
                     label(r"illustration: invented numbers", font_size=17, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.35)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-58 * DEGREES, zoom=0.9)
        fixed(self, hint, eqs)
        with self.voiceover(
            "Generalize the toy. Let Q be the trading that moves the index and D the options exposure. The trading "
            "costs about lambda Q squared: a trough along Q. The options gain about D times "
            "the move the trading causes, two lambda Q: a ramp along D. <bookmark mark='a'/> Set the sum to zero and "
            "the boundary is a line, D equal to Q over two, in yellow. On the green side the whole profits even "
            "though the trading that moves the price loses. That is why surveillance looks at the options position "
            "and the cash trading on the same screen. Since October 2025 SEBI's circular of the first of September has "
            "had exchanges check every entity's intraday index-option position, measured in delta, against a net "
            "limit of five thousand crore rupees. What tells manipulation from hedging is intent and pattern: for "
            "the regulator and the tribunal to weigh."
            " Next: what happens when short volatility blows up."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), run_time=1.2)
            self.play(Create(sf), FadeIn(eqs[0]), FadeIn(eqs[2]), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(edge), FadeIn(eqs[1]))
            self.move_camera(theta=-25 * DEGREES, phi=68 * DEGREES, run_time=max(vo.remaining(1.0) - 0.3, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, sf, edge)), FadeOut(hint),
                                                                             FadeOut(eqs)], run_time=1.5)
        self.clear_scene()
