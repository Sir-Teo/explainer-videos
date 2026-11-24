from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403

COLS = ["#F6C453", "#7EC8F5", "#F2A65A", "#7BD88F", "#B58CFF", "#E9A0C9", "#5DA9E9", "#E8554E"]


class Intermission(VoiceoverScene):
    def construct(self):
        D = R["diffusion"]
        pa = viz.plot_axes([1920, 2020], [0, 100], x_length=11.0, y_length=5.0, xticks=[1920, 1940, 1960, 1980, 2000, 2020],
                           yticks=[25, 50, 75, 100], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}%", size=15)
        pa.move_to([0, -0.5, 0])
        head = tx("Intermission: a century of S-curves (share of American households)", 22, GREY_A).to_edge(UP, buff=0.4)
        t = ValueTracker(1920)
        lines, labels = [], VGroup()
        for k, (name, f) in enumerate(D.items()):
            ys, ss = f["years"], f["shares"]
            col = COLS[k % len(COLS)]

            def mk(ys=ys, ss=ss, col=col):
                pts = [pa.ax.c2p(y, s) for y, s in zip(ys, ss) if 1920 <= y <= t.get_value()]
                if len(pts) < 2:
                    return VMobject()
                return VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(pts)
            lines.append(always_redraw(mk))
            last = [(y, s) for y, s in zip(ys, ss) if y <= 2020][-1]
            labels.add(tx(name.replace(" usage", "s").replace("Household ", ""), 15, col).next_to(
                pa.ax.c2p(*last), RIGHT, buff=0.08))
        yr = draw.number(lambda: t.get_value(), 0, size=30, color=GREY_B, commas=False)
        yr.to_corner(DR, buff=0.5).shift(UP * 0.4)
        src = source("Our World in Data, from Comin and Hobijn (2004) and later sources", size=13)
        with self.voiceover(
            "A pause, and a century of new things arriving in American homes. The radio, the refrigerator, colour "
            "television, the microwave, the mobile phone, the internet, the smartphone and social media. Each line is "
            "the share of households, or of people, who had it. Watch the shapes rather than the dates. Slow at "
            "first, then steep, then flattening out. And notice that not every line flattens at the top: some "
            "things stop well short of every household."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(src), FadeIn(yr))
            for ln in lines:
                self.add(ln)
            self.play(t.animate.set_value(2020), run_time=14, rate_func=linear)
            self.play(LaggedStart(*[FadeIn(l_) for l_ in labels], lag_ratio=0.15), run_time=1.6)
        for ln in lines:
            ln.clear_updaters()
        yr.clear_updaters()
        self.clear_scene()
        self.story()

    def story(self):
        head = tx("The story so far", 36, GOLD, bold=True).to_edge(UP, buff=0.6)
        lines = ["A market size answers four questions: which level, which plants, which products, which buyers.",
                 "Top-down counts what governments count; bottom-up multiplies units by a price you must choose.",
                 "Few firms: add up their accounts. And every growth rate is part price, part quantity.",
                 "Put estimates on one definition before comparing them, and report a range.",
                 "An addressable market is a company's dream, not a forecast.",
                 "Next: how new markets grow, and how well anyone can see it coming."]
        pics = [VGroup(draw.factory(0.5, color=FACTORY), draw.shop(0.5, color=RETAIL)).arrange(RIGHT, buff=0.1),
                VGroup(RoundedRectangle(corner_radius=0.04, width=0.4, height=0.5, stroke_width=0, fill_color="#E8E4DA",
                                        fill_opacity=1), draw.bottle(0.5, color=WATER)).arrange(RIGHT, buff=0.1),
                VGroup(Rectangle(width=0.22, height=0.55, stroke_width=0, fill_color=FACTORY, fill_opacity=1),
                       VGroup(Rectangle(width=0.22, height=0.2, stroke_width=0, fill_color=UNITS, fill_opacity=1),
                              Rectangle(width=0.22, height=0.33, stroke_width=0, fill_color=GUESS, fill_opacity=1)
                              ).arrange(DOWN, buff=0)).arrange(RIGHT, buff=0.1, aligned_edge=DOWN),
                VGroup(*[Dot(radius=0.07, color=c) for c in (FACTORY, RETAIL, GUESS)]).arrange(RIGHT, buff=0.12),
                VGroup(Circle(radius=0.3, stroke_color=TAM, stroke_width=3), Dot(radius=0.04, color=WHITE)),
                FunctionGraph(lambda x: 0.3 / (1 + np.exp(-4 * x)), x_range=[-1, 1], color=GUESS, stroke_width=3)]
        rows = VGroup()
        for k, (pic, ln) in enumerate(zip(pics, lines)):
            pic.scale_to_fit_height(min(max(pic.height, 0.4), 0.65))
            rows.add(VGroup(pic, tx(ln, 22 if k < 5 else 21, WHITE if k < 5 else GREY_B)))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(head, DOWN, buff=0.6)
        for r_ in rows:
            r_[0].move_to([rows.get_left()[0] + 0.6, r_.get_y(), 0])
            r_[1].next_to(r_[0], RIGHT, buff=0.4).align_to(rows[0][1], LEFT)
        if rows.width > 13.4:
            rows.scale_to_fit_width(13.4)
        rows.set_x(0)
        with self.voiceover(
            "The story so far. <bookmark mark='a'/> A market size answers four questions: which level of the chain, "
            "which plants, which products, which buyers. <bookmark mark='b'/> Top-down counts what governments "
            "count; bottom-up multiplies units by a price you have to choose. <bookmark mark='f'/> When a few firms "
            "hold the market, their own accounts add up to it. And every growth rate is part price and part "
            "quantity. <bookmark mark='c'/> Put estimates on "
            "one definition before you compare them, and report a range. <bookmark mark='d'/> An addressable market "
            "is a company's dream, not a forecast. <bookmark mark='e'/> Next: how new markets grow, and how well "
            "anyone can see it coming."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abfcde"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k][0], scale=0.6), FadeIn(rows[k][1], shift=RIGHT * 0.15), run_time=0.9)
        self.clear_scene()
