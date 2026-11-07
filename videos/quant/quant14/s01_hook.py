from __future__ import annotations

import numpy as np

from videos.quant.quant14.common import axes, data_range, skew_range

from explainer.quant import *  # noqa: F403
from explainer.quant.house import sim
from videos.quant.quant14.common import BAD, IV, PART, ROUGH, RV, VAR, illustration, load, pause

HISTORY = [
    (1968, r"Mandelbrot and Van Ness: fractional Brownian motion", QC.IDEA),
    (1987, r"the crash: the skew is born (Part 13)", QC.CRISIS),
    (1993, 'Heston: Brownian-scale stochastic variance', QC.IDEA),
    (1998, r"Comte and Renault: long memory in volatility", QC.IDEA),
    (2004, r"Bergomi: forward variance models", QC.IDEA),
    (2007, r"Al\`os, Le\'on and Vives: a rough kernel makes a power-law skew", QC.IDEA),
    (2014, r"``Volatility is rough'' (Gatheral, Jaisson, Rosenbaum)", QC.IDEA),
    (2016, r"rough Bergomi; nearly unstable Hawkes", QC.IDEA),
    (2019, r"rough Heston's characteristic function", QC.IDEA),
    (2020, r"quadratic rough Heston; Guyon's SPX/VIX answer", QC.IDEA),
    (2021, r"Risk's Quants of the Year: Gatheral and Rosenbaum", QC.FIRM),
    (2023, r"path-dependent volatility (Guyon, Lekeufack)", QC.IDEA),
    (2024, r"5 August: the VIX above 65 before the open", QC.CRISIS),
]


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.zoom()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Rough")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part fourteen. Rough and path-dependent volatility. The newest chapter of volatility modelling, and "
            "the most argued over."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def zoom(self):
        n = 8192
        paths = [(np.asarray(sim.fbm(0.5, n, 1.0, 1, seed=3)).ravel(), VAR, r"$H = 0.5$: Brownian motion"),
                 (np.asarray(sim.fbm(0.1, n, 1.0, 1, seed=3)).ravel(), ROUGH, r"$H = 0.1$: rough")]
        s = ValueTracker(0.0)   # zoom = 2^(8 s): from the whole path to 1/256 of it
        boxes = VGroup()
        for z, col, txt in paths:
            frame = Rectangle(width=10.6, height=2.0, stroke_color=GREY_D, stroke_width=1.5)
            t = label(txt, font_size=22, color=col).next_to(frame, UP, buff=0.08).align_to(frame, LEFT)
            boxes.add(VGroup(frame, t))
        boxes.arrange(DOWN, buff=0.5).to_edge(DOWN, buff=0.75)  # the question card takes the top

        def drawn(i):
            z, col, _ = paths[i]
            frame = boxes[i][0]

            def make():
                span = max(int(n / 2 ** (8 * s.get_value())), 16)
                seg = z[: span + 1]
                idx = np.linspace(0, span, min(span + 1, 700)).astype(int)
                y = seg[idx]
                y = (y - y.min()) / max(y.max() - y.min(), 1e-12)
                x = idx / span
                pts = [frame.get_corner(DL) + RIGHT * (0.1 + 10.4 * a) + UP * (0.1 + 1.8 * b) for a, b in zip(x, y)]
                return VMobject(stroke_color=col, stroke_width=1.6).set_points_as_corners(pts)
            return always_redraw(make)

        lines = VGroup(drawn(0), drawn(1))
        zr = readout(r"\text{zoom}\ \times", lambda: 2 ** (8 * s.get_value()), digits=0, font_size=34,
                     color=YELLOW).to_corner(UR, buff=0.35)
        src = illustration(r"fractional Brownian motion, 8{,}192 steps; each frame rescaled to fill its box")
        q = pause('After rescaling a Brownian segment, must it straighten? (Finite-grid illustration.)', width=6.4, font_size=22).to_corner(UL, buff=0.25)
        with self.voiceover(
            """Two random paths. Zoom into the Brownian path two hundred and fifty-six times, rescaling every segment to fill its box. Should Brownian motion become a straight line? <bookmark mark='a'/> No. Brownian motion and fractional Brownian motion are both self-similar. Under their own theoretical time and amplitude scaling, neither becomes differentiable. This picture instead normalizes each finite segment by its observed range. <bookmark mark='b'/> The lower path has H of one tenth: its increments shrink more slowly with the time interval than Brownian increments do. The final zoom contains only a few dozen simulated steps, so its line segments are a plotting limit, not evidence of smoothness. <bookmark mark='c'/> Gatheral, Jaisson and Rosenbaum's 2014 preprint, published in 2018, found low scaling exponents in realized-volatility proxies. We will measure that pattern, price with rough models, and examine competing explanations."""
        ) as vo:
            self.play(FadeIn(boxes), FadeIn(lines), FadeIn(src), FadeIn(q))
            vo.wait_until("a")
            self.play(FadeOut(q), FadeIn(zr))
            self.play(s.animate.set_value(1.0), run_time=max(vo.remaining(0.0) * 0.45, 6), rate_func=linear)
            vo.wait_until("b")
            self.play(Indicate(boxes[1][1], color=ROUGH))
            vo.wait_until("c")
            self.play(s.animate.set_value(0.0), run_time=3)
        self.wait(0.3)
        lines.clear_updaters()
        zr.clear_updaters()
        self.clear_scene()

    def history(self):
        y0, y1 = 1965, 2026
        width = 12.4
        X = lambda yr: -width / 2 + width * (yr - y0) / (y1 - y0)  # noqa: E731
        axis = Line([X(y0), 0, 0], [X(y1), 0, 0], color=GREY_C, stroke_width=2).shift(UP * 0.2)
        ticks = VGroup(*[VGroup(Line(UP * 0.06, DOWN * 0.06, color=GREY_C).move_to([X(yr), 0.2, 0]),
                                Text(str(yr), font_size=14, color=GREY_C).move_to([X(yr), -0.05, 0]))
                         for yr in (1970, 1980, 1990, 2000, 2010, 2020)])
        events = VGroup()
        for i, (yr, txt, col) in enumerate(HISTORY):
            d = Dot([X(yr), 0.2, 0], radius=0.08, color=col)
            up = i % 2 == 0
            lv = 0.75 + 0.62 * ((i // 2) % 4)
            t = wrapped_label(rf"{yr}: {txt}", 3.0, 16, col)
            t.move_to([X(yr), 0.2 + (lv if up else -lv - 0.15), 0])
            keep_in_frame(t, margin=0.2)
            ld = Line(d.get_center(), t.get_bottom() if up else t.get_top(), stroke_color=GREY_D, stroke_width=1)
            events.add(VGroup(d, ld, t))
        head = label(r"How we got here", font_size=30).to_edge(UP, buff=0.3)
        with self.voiceover(
            "How we got here. In 1968 Benoit Mandelbrot and John Van Ness defined fractional Brownian motion, the process with a Hurst exponent. <bookmark mark='a'/> After the 1987 crash the skew appeared, and the models of the nineties, Heston's above all, gave variance Brownian local regularity, still nondifferentiable away from degeneracy. In 1998 Fabienne Comte and Eric Renault gave volatility long memory: H above one half. <bookmark mark='b'/> Lorenzo Bergomi modelled the forward variance curve, and in 2007 Elisa Alòs, Jorge León and Josep Vives showed that a rough kernel makes the skew a power law. <bookmark mark='c'/> In 2014 came the paper that named the field: volatility is rough. Rough Bergomi followed, then rough Heston, then quadratic rough Heston, and Risk's Quants of the Year for 2021. <bookmark mark='d'/> In 2023, a rival view: path-dependent volatility. And on the fifth of August 2024, the VIX printed above sixty-five before the open."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks))
            self.play(FadeIn(events[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(e) for e in events[1:4]], lag_ratio=0.5, run_time=3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(e) for e in events[4:6]], lag_ratio=0.5, run_time=2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(e) for e in events[6:11]], lag_ratio=0.5, run_time=5))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(e) for e in events[11:]], lag_ratio=0.6, run_time=2))
        self.wait(0.5)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            'Finite-maturity skew magnitudes on the original 102 dates; how kernel asymptotics differ',
            'Measuring roughness: the estimator, two bitcoin eras, and a retrospective forecast comparison',
            r"Rough Bergomi, calibrated and replayed; the hybrid scheme that simulates it",
            r"Rough Heston: the fractional Riccati equation, solved by Adams; how much the Surface cares about $H$",
            r"Where roughness comes from (nearly unstable order flow); Markovian lifts",
            r"The debate: the estimator's bias map, and what the options say",
            r"Path-dependent volatility on bitcoin and on the VIX; 5 August 2024",
            'Joint SPX/VIX; signature volatility; numerical speed; selected 2023--2025 research',
        ], color=QC.IDEA, font_size=23)
        with self.voiceover(
            "The plan. The fact that started it, measured week by week, and why a rough kernel makes it. The "
            "measurement that named roughness, and what it buys a forecaster. The two rough models desks know, with "
            "their numerical methods opened up. Where roughness might come from, and how to make it Markovian. The "
            "case against roughness. The rival view, that volatility is mostly a function of the past, tested on "
            "the fifth of August 2024. And the frontier, and what desks actually run."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=14))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        with self.voiceover(
            "In the House, the volatility desk opens a rough lab. <bookmark mark='a'/> It adds models, the "
            "numerical methods that make them usable, and a rule for when a new model has earned its place."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
