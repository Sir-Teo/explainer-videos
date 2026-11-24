from __future__ import annotations

from explainer.industry.register import get
from explainer.industry.works.diffusion import bass, predict
from videos.industry.industry7.common import *  # noqa: F403

P_, Q_ = 0.03, 0.38  # an illustrative product for the grid of households


class Bass(VoiceoverScene):
    def construct(self):
        card(self, 8, "How new things spread", "Why does adoption trace an S?",
             "Chapter eight. How new things spread.", lit=("change",))
        self.grid()
        self.fits()

    def grid(self):
        n = 100
        homes = VGroup(*[draw.house(0.42, color="#3A4150") for _ in range(n)]).arrange_in_grid(rows=10, cols=10,
                                                                                         buff=(0.08, 0.06))
        homes.move_to([-3.8, -0.3, 0])
        rng = np.random.default_rng(7)
        order = rng.permutation(n)
        cum = [int(round(100 * bass(t, P_, Q_))) for t in range(0, 21)]
        # who adopts on their own each year (innovators) and by copying (imitators), from the model's two terms
        kinds = {}
        k = 0
        for t in range(1, 21):
            new = cum[t] - cum[t - 1]
            left = 1 - cum[t - 1] / 100
            innov = left * P_ / (left * P_ + left * Q_ * cum[t - 1] / 100) if new else 0
            for j in range(new):
                kinds[order[k]] = (t, "innov" if j < round(new * innov) else "imit")
                k += 1
        pa = viz.plot_axes([0, 20], [0, 100], x_length=5.6, y_length=3.2, xticks=[0, 5, 10, 15, 20], yticks=[50, 100],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}%", xlabel="years after launch", size=14)
        pa.move_to([3.4, 0.2, 0])
        year = ValueTracker(0)

        def curve():
            k_ = int(year.get_value())
            pts = [pa.ax.c2p(t, cum[t]) for t in range(0, k_ + 1)]
            return VMobject(stroke_color=GUESS, stroke_width=4).set_points_as_corners(pts) if len(pts) > 1 else VMobject()
        line = always_redraw(curve)
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=GOLD, fill_opacity=1), tx("on their own (p)", 16, GOLD)
                            ).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, stroke_width=0, fill_color=RETAIL, fill_opacity=1),
                            tx("copying the neighbours (q)", 16, RETAIL)).arrange(RIGHT, buff=0.1)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(homes, UP, buff=0.2)
        eq = MathTex(r"\text{new adopters} = (1 - F)\,(p + q\,F)", font_size=34).next_to(pa, DOWN, buff=0.7)
        tag = estimate_tag(f"a model product: p = {P_}, q = {Q_}", corner=DR, size=14)
        src = source(f"Bass, 'A New Product Growth for Model Consumer Durables', Management Science, {get('bass.1969'):.0f}",
                     size=13)
        with self.voiceover(
            "In 1969 a marketing professor, Frank Bass, wrote down why adoption traces an S. <bookmark mark='a'/> "
            "Picture a hundred households, and a new product. <bookmark mark='b'/> Each year, a few of the households "
            "that do not yet have it buy it on their own: they read about it, they like new things. Bass called that "
            "share p. <bookmark mark='c'/> Others buy it because their neighbours have it: the more neighbours, the "
            "more likely. Bass called that pull q. <bookmark mark='d'/> At first almost nobody has it, so there is "
            "nobody to copy, and growth is slow. Then copying takes over, and the curve goes steep. "
            "<bookmark mark='e'/> And at the end there is nobody left to convince, so it flattens. Two numbers, p "
            "and q, and a ceiling: that is the whole model."
        ) as vo:
            self.play(FadeIn(src), FadeIn(tag), LaggedStart(*[FadeIn(h_) for h_ in homes], lag_ratio=0.005), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(pa), FadeIn(key))
            self.add(line)
            vo.wait_until("b")
            for t in range(1, 5):
                anims = [homes[i].animate.set_color(GOLD if kd == "innov" else RETAIL) for i, (tt, kd) in kinds.items()
                         if tt == t]
                self.play(*anims, year.animate.set_value(t), run_time=0.6)
            vo.wait_until("c")
            for t in range(5, 9):
                anims = [homes[i].animate.set_color(GOLD if kd == "innov" else RETAIL) for i, (tt, kd) in kinds.items()
                         if tt == t]
                self.play(*anims, year.animate.set_value(t), run_time=0.6)
            vo.wait_until("d")
            for t in range(9, 14):
                anims = [homes[i].animate.set_color(GOLD if kd == "innov" else RETAIL) for i, (tt, kd) in kinds.items()
                         if tt == t]
                self.play(*anims, year.animate.set_value(t), run_time=0.5)
            vo.wait_until("e")
            for t in range(14, 21):
                anims = [homes[i].animate.set_color(GOLD if kd == "innov" else RETAIL) for i, (tt, kd) in kinds.items()
                         if tt == t]
                self.play(*anims, year.animate.set_value(t), run_time=0.4)
            self.play(Write(eq))
        line.clear_updaters()
        self.clear_scene()

    def fits(self):
        D = R["diffusion"]
        names = ["Microwave", "Internet", "Smartphone usage"]
        cols = [GUESS, FACTORY, RETAIL]
        panels = VGroup()
        for name, col in zip(names, cols):
            f = D[name]
            ys, ss = f["years"], f["shares"]
            x0, x1 = min(ys) - 2, max(ys) + 2
            pa = viz.plot_axes([x0, x1], [0, 100], x_length=3.8, y_length=2.6, xticks=[int(min(ys)), int(max(ys))],
                               yticks=[50, 100], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}%", size=13)
            dots = VGroup(*[Dot(pa.ax.c2p(y, s), radius=0.045, color=WHITE) for y, s in zip(ys, ss)])
            xs = np.linspace(x0, x1, 80)
            fit = VMobject(stroke_color=col, stroke_width=3).set_points_smoothly(
                [pa.ax.c2p(x, float(predict(f, [x])[0])) for x in xs])
            head = VGroup(tx(name.replace(" usage", "s"), 20, col, bold=True),
                          tx(f"p = {f['p']:.3f}   q = {f['q']:.2f}   ceiling {f['m']:.0f}%", 15, GREY_A)).arrange(
                DOWN, buff=0.04).next_to(pa, UP, buff=0.12)
            panels.add(VGroup(pa, dots, fit, head))
        panels.arrange(RIGHT, buff=0.6).move_to([0, -0.2, 0])
        src = source("Our World in Data (Comin and Hobijn and others); this film's Bass fits by least squares", size=13)
        with self.voiceover(
            "Fit Bass's curve to real products and it does well, after the fact. <bookmark mark='a'/> The white dots "
            "are the share of American households with a microwave oven, year by year; the curve is the model, "
            "with its three numbers chosen to fit. <bookmark mark='b'/> The internet. <bookmark mark='c'/> "
            "Smartphones. Each fits closely, with a small p and a larger q: most people bought because others had. "
            "<bookmark mark='d'/> Here is the catch. These fits were made with the whole curve in hand, ceiling "
            "included. The question a market sizer faces is different: how high will the curve go, and how fast, "
            "when you can only see its first few years?"
        ) as vo:
            self.play(FadeIn(src))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                pa, dots, fit, head = panels[k]
                self.play(FadeIn(pa), FadeIn(head), LaggedStart(*[FadeIn(d_, scale=2) for d_ in dots], lag_ratio=0.05),
                          run_time=1.2)
                self.play(Create(fit), run_time=1.2)
            vo.wait_until("d")
            self.play(*[Indicate(p_[2], color=WHITE) for p_ in panels])
        self.clear_scene()
