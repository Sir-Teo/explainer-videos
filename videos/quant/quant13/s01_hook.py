from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, PART, RV, SPOT, VAR, load, pause, real_data

ERA = [
    (1973, r"Black--Scholes--Merton: one volatility", "idea"),
    (1976, r"Merton: jumps", "idea"),
    (1987, r"the crash of 19 October", "crisis"),
    (1987.6, r"Hull--White; Scott; Wiggins: random volatility", "idea"),
    (1991, r"Stein--Stein: volatility as an OU process", "idea"),
    (1993, r"Heston: a closed-form characteristic function", "idea"),
    (1994, r"Dupire; Derman--Kani; Rubinstein: implied trees", "idea"),
    (1996, r"Bates: stochastic volatility with jumps", "idea"),
    (1998, r"Madan--Carr--Chang: variance gamma", "idea"),
    (2002, r"SABR; Kou; CGMY", "idea"),
    (2004, r"Carr--Wu time changes; Cboe lists VIX futures", "idea"),
    (2005, r"Bergomi: smile dynamics, variance curves", "idea"),
    (2006, r"Cboe lists VIX options", "firm"),
    (2008, r"Andersen's QE; Gatheral's SPX/VIX talk", "idea"),
    (2012, r"Guyon--Henry-Labord\`ere: the particle method", "idea"),
    (2020, 'Guyon: a nonparametric joint SPX/VIX construction', "idea"),
    (2022, r"Terra--Luna and FTX", "crisis"),
]


def _yr(ts):
    return 1970 + np.asarray(ts, float) / (365.2425 * 86400)


def _ts(y, m, d):
    return datetime(y, m, d, tzinfo=timezone.utc).timestamp()


class Hook(VoiceoverScene):
    def construct(self):
        f = load("facts")
        e = load("exotics")
        self.title_card()
        self.rivers(f)
        self.question(e)
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"The second river")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part thirteen. Stochastic volatility and jumps. Part twelve read the volatility surface as a still "
            "photograph. This part asks what moves it."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def rivers(self, f):
        t = _yr(f["dvol_t"])
        dv = np.asarray(f["dvol"])
        g = axes([2021.25, 2026], [0.2, 1.6], x_length=10.4, y_length=4.4, ylabel=r"DVOL: bitcoin's 30-day implied volatility",
                 xticks=[2022, 2023, 2024, 2025], yticks=[0.4, 0.8, 1.2, 1.6], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=17).move_to(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, np.clip(dv, 0.2, 1.6), IV, stroke_width=2.4)
        tags = VGroup()
        # Terra and FTX peak six months apart: Terra's label rises above (clear of 2021's spike), FTX's to its right
        for (a, b), name, side, lift in (((_ts(2022, 5, 1), _ts(2022, 6, 30)), r"Terra--Luna, May 2022", ORIGIN, 1.0),
                                         ((_ts(2022, 11, 1), _ts(2022, 11, 30)), r"FTX, November 2022", RIGHT, 0.25),
                                         ((_ts(2024, 8, 1), _ts(2024, 8, 15)), r"the yen carry unwind, August 2024", ORIGIN,
                                          0.9)):
            m = (np.asarray(f["dvol_t"]) >= a) & (np.asarray(f["dvol_t"]) <= b)
            i = np.flatnonzero(m)[np.argmax(dv[m])]
            d = Dot(ax.c2p(t[i], dv[i]), radius=0.07, color=BAD)
            lab = label(rf"{name}: {100 * dv[i]:.0f}\%", font_size=18, color=GREY_A)
            lab.move_to(d.get_center() + UP * (lift + lab.height / 2) + side * (lab.width / 2 + 0.05))
            tie = Line(d.get_center(), lab.get_corner(DOWN + (RIGHT if side[0] < 0 else LEFT if side[0] > 0 else ORIGIN)),
                       color=GREY_C, stroke_width=1.2)
            tags.add(VGroup(d, tie, lab))
        src = real_data(r"Deribit DVOL, daily, April 2021 -- November 2025")
        with self.voiceover(
            "Here is Bitcoin's thirty-day implied volatility, every day for four and a half years. It is not a "
            "constant. It is a river of its own, running beside the price. <bookmark mark='a'/> It floods when the "
            "price breaks: the collapse of Terra and Luna, the failure of FTX, the day in August 2024 when a crowded "
            "yen trade unwound across every market. And between floods it drains away, back toward a level it "
            "seems to remember."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(line), run_time=4)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.1) for t_ in tags], lag_ratio=0.6, run_time=3))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def question(self, e):
        names = {"LV": r"local vol", "Heston": r"Heston", "Bates": r"Bates", "VG": r"variance gamma", "SLV": r"SLV"}
        cl = {m: e["models"][m]["cliquet"] for m in names}
        rows = VGroup(*[VGroup(label(names[m], font_size=26, color=MODEL_COL[m]),
                               MathTex(rf"{100 * v:.2f}\%", font_size=34)).arrange(RIGHT, buff=0.5) for m, v in cl.items()])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        for r_ in rows:
            r_[1].align_to(rows, LEFT).shift(RIGHT * 3.4)
        head = label(r"five models, fitted to the same options, price one cliquet", font_size=28).to_edge(UP, buff=0.8)
        rows.next_to(head, DOWN, buff=0.5)
        v = np.array(list(cl.values()))
        q = label('Observed price range: dynamics plus unequal vanilla fits and numerical errors.',
                  font_size=26, color=BAD).next_to(rows, DOWN, buff=0.5)
        pp = pause(r"Five models agree on every vanilla option on the Surface. Can they disagree about anything?",
                   width=5.4).to_corner(DR, buff=0.3)
        with self.voiceover(
            (
            f"""This part gives volatility its own state, and adds jumps and random clocks. Here is the question: fit or project five models to the same pooled Bitcoin marks. Their vanilla errors differ, so they do not agree on every option. <bookmark mark='p'/> Even exact agreement on vanilla prices would leave the joint law across dates undetermined. <bookmark mark='a'/> Our capped monthly-return cliquet differs by {100 * (v.max() - v.min()) / v.mean():.0f} percent across these models. That displayed spread combines dynamics, unequal vanilla fits and numerical error. We will separate those ideas as we go."""
        )
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.3,
                                                run_time=3))
            vo.wait_until("p")
            self.play(FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeOut(pp), FadeIn(q))
        self.wait(0.5)
        self.clear_scene(run_time=0.35)

    def history(self):
        x0, x1, W = 1970, 2025, 12.4
        X = lambda y: -W / 2 + W * (y - x0) / (x1 - x0)  # noqa: E731
        line = Line([X(x0), 2.6, 0], [X(x1), 2.6, 0], color=GREY_D, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(y), 2.54, 0], [X(y), 2.66, 0], color=GREY_D, stroke_width=1.5),
                                Text(str(y), font_size=14, color=GREY_C).move_to([X(y), 2.3, 0]))
                         for y in range(1970, 2026, 10)])
        col = {"idea": QC.IDEA, "crisis": QC.CRISIS, "firm": QC.FIRM}
        dots = VGroup(*[Dot([X(y), 2.6, 0], radius=0.075, color=col[k]) for y, _, k in ERA])
        rows = VGroup(*[VGroup(MathTex(str(int(y)), font_size=24, color=col[k]), label(t, font_size=21, color=GREY_A))
                        .arrange(RIGHT, buff=0.25) for y, t, k in ERA])
        left, right = rows[:9], rows[9:]
        for grp in (left, right):
            grp.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        VGroup(left, right).arrange(RIGHT, buff=0.6, aligned_edge=UP).next_to(line, DOWN, buff=0.75)
        if VGroup(left, right).width > 13.2:
            VGroup(left, right).scale_to_fit_width(13.2)
        head = label(r"How we got here", font_size=30, color=GREY_B).to_edge(UP, buff=0.25)
        marks = ["m%d" % i for i in range(len(ERA))]
        with self.voiceover(
            (
            """The history. 1973: Black, Scholes and Merton's constant-volatility benchmark; 1976: Merton's jumps. <bookmark mark='m2'/> October 1987 made downside index skew especially prominent. <bookmark mark='m3'/> Hull and White, Scott and Wiggins modelled random volatility; <bookmark mark='m4'/> Stein and Stein used an Ornstein–Uhlenbeck factor; <bookmark mark='m5'/> Heston obtained an affine characteristic function. <bookmark mark='m6'/> Dupire, Derman–Kani and Rubinstein developed local-volatility and implied-tree approaches. <bookmark mark='m7'/> Bates combined volatility and jumps; <bookmark mark='m8'/> Madan, Carr and Chang priced variance gamma. <bookmark mark='m9'/> Then SABR, Kou and CGMY; <bookmark mark='m10'/> Carr and Wu's clocks and Cboe's VIX futures; <bookmark mark='m11'/> Bergomi's variance curves; <bookmark mark='m12'/> VIX options; <bookmark mark='m13'/> Andersen's simulation and Gatheral's joint-smile challenge; <bookmark mark='m14'/> Guyon and Henry-Labordère's particles; <bookmark mark='m15'/> Guyon's nonparametric joint-calibration construction; <bookmark mark='m16'/> and Bitcoin's Terra and FTX episodes."""
        )       ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(ticks), FadeIn(dots[0]), FadeIn(rows[0]), FadeIn(dots[1]),
                      FadeIn(rows[1]))
            for i in range(2, len(ERA)):
                vo.wait_until(marks[i])
                self.play(FadeIn(dots[i], scale=1.6), FadeIn(rows[i], shift=RIGHT * 0.15),
                          Flash(dots[i], color=dots[i].get_color(), flash_radius=0.2), run_time=0.8)
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def objectives(self):
        card = objectives_card([
            r"Why volatility must move, and why random volatility makes a smile (mixing, derived)",
            r"Heston: the characteristic function derived, the little trap, the fit replayed, QE simulation",
            r"SABR: Hagan's expansion, the backbone, the negative density and arbitrage-free SABR",
            r"Jumps (Merton, Kou, Bates) and L\'evy models by time change (VG, NIG, CGMY); the skew's term structure",
            r"Stochastic local volatility: the particle method, its convergence, and the mixing fraction",
            'Bergomi forward variance; ratio forward-starts and cliquets; a Bitcoin volatility-index illustration',
            r"Calibration as an inverse problem: valleys, the Hessian, regularisation; how desks judge a model; the "
            r"frontier",
        ], color=QC.IDEA, font_size=24)
        with self.voiceover(
            (
            "The plan. Why volatility must move, and a proof that randomness makes a smile. Heston, derived, fitted "
            "and simulated. SABR and its repair. Jumps and Lévy clocks, sorted by their skews. Stochastic local "
            "volatility and its dial. Variance curves, forward smiles, the S&P–VIX puzzle. Then calibration, the "
            "industry, and the frontier."
        )
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        with self.voiceover(
            "In the House, the volatility desk gets its calibrator. <bookmark mark='a'/> From now on, every model the "
            "desk prices with is fitted by it, and every exotic carries a statement of how much the models disagree."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene(run_time=0.35)
