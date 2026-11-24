from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403


class Panels(VoiceoverScene):
    def construct(self):
        card(self, 7, "Surveys and panels", "Where do the commercial numbers come from, and what can they not see?",
             "Chapter seven. Surveys and panels.", lit=("unit",))
        till = VGroup(RoundedRectangle(corner_radius=0.08, width=1.4, height=0.9, stroke_width=0, fill_color="#2E3645",
                                       fill_opacity=1),
                      Rectangle(width=1.0, height=0.3, stroke_width=0, fill_color="#7BD88F", fill_opacity=0.8).shift(UP * 0.15),
                      Line(LEFT * 0.5 + DOWN * 0.25, RIGHT * 0.5 + DOWN * 0.25, stroke_color=GREY_B, stroke_width=3))
        kinds = [(VGroup(till, tx("scan", 14, GREY_A)).arrange(DOWN, buff=0.08), "Scanner panels",
                  "every barcode at the tills of the shops that share their data",
                  "misses shops that do not share, vending machines, home and office delivery"),
                 (VGroup(draw.house(0.7, color=STONE), draw.person(0.5, color=STONE)).arrange(RIGHT, buff=0.1),
                  "Household panels", "families who record what they buy",
                  "people forget; the families who agree to it are not quite like everyone else"),
                 (VGroup(RoundedRectangle(corner_radius=0.08, width=1.1, height=0.7, stroke_width=0, fill_color="#2B4C9B",
                                          fill_opacity=1), Rectangle(width=1.1, height=0.12, stroke_width=0,
                                                                     fill_color="#0E1117", fill_opacity=1).shift(UP * 0.12)),
                  "Card and app data", "what cardholders of one bank or one app spend",
                  "cash, other banks and other apps are invisible"),
                 (VGroup(RoundedRectangle(corner_radius=0.04, width=0.6, height=0.8, stroke_width=0, fill_color="#E8E4DA",
                                          fill_opacity=1), draw.factory(0.6, color=FACTORY)).arrange(RIGHT, buff=0.1),
                  "Surveys of companies", "what firms report to the statistical office or a trade body",
                  "late, and filed by what the plant mainly makes")]
        rows = VGroup()
        for pic, head, sees, misses in kinds:
            pic.scale_to_fit_height(min(pic.height, 0.75))
            t_ = VGroup(tx(head, 23, WHITE, bold=True), tx("sees: " + sees, 16, RETAIL), tx("misses: " + misses, 16, "#E8554E")
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            rows.add(VGroup(pic, t_).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.35, 0])
        for r_ in rows:
            r_[0].move_to([rows.get_left()[0] + 0.7, r_.get_y(), 0])
            r_[1].next_to(r_[0], RIGHT, buff=0.4).align_to(rows[0][1], LEFT)
        if rows.width > 13.4:
            rows.scale_to_fit_width(13.4)
        head = tx("Every source is a window, not the whole house", 26, GOLD, bold=True).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Most market numbers you read come from firms that sell data, and each of them looks through one "
            "window. <bookmark mark='a'/> Scanner panels collect every barcode beeped at the tills of the shops "
            "that agree to share their data. They see supermarket bottled water in fine detail, and they miss "
            "vending machines, and the five-gallon jugs delivered to offices. <bookmark mark='b'/> Household panels "
            "ask families to record what they buy. People forget, and the families willing to do it are not quite "
            "like everyone else. <bookmark mark='c'/> Card and app data see what one bank's or one app's customers "
            "spend: never the cash, never the other banks. <bookmark mark='d'/> And surveys of companies, by "
            "statistical offices or trade bodies, are thorough and late, and file each plant by what it mainly "
            "makes. When two firms' estimates of the same market differ by a factor of two, the first question is "
            "not who is wrong. It is which window each of them was looking through."
        ) as vo:
            self.play(FadeIn(head))
            for r_, m in zip(rows, "abcd"):
                vo.wait_until(m)
                self.play(FadeIn(r_[0], scale=0.8), FadeIn(r_[1], shift=RIGHT * 0.15))
        self.clear_scene()
        self.moved()

    def moved(self):
        """Windows also move: the share of US retail sold online, which a panel of shop tills never sees."""
        E = R["ecom"]
        yrs, sh = E["years"], E["share"]
        pa = viz.plot_axes([yrs[0] - 0.5, yrs[-1] + 0.5], [0, 20], x_length=7.4, y_length=3.8,
                           xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[5, 10, 15, 20], xfmt=lambda v: f"{int(v)}",
                           yfmt=lambda v: f"{v:g}%", size=15)
        pa.move_to([2.2, -0.6, 0])
        t = ValueTracker(yrs[0])

        def at():
            x = t.get_value()
            k = min(max(int(np.floor(x)) - yrs[0], 0), len(yrs) - 2)
            f = x - yrs[k]
            return sh[k] * (1 - f) + sh[k + 1] * f

        def line():
            x = t.get_value()
            pts = [pa.ax.c2p(y, v) for y, v in zip(yrs, sh) if y <= x] + [pa.ax.c2p(x, at())]
            return VMobject(stroke_color=UNITS, stroke_width=4).set_points_as_corners(pts)
        ln = always_redraw(line)
        dot = always_redraw(lambda: glow_dot(pa.ax.c2p(t.get_value(), at()), color=UNITS, radius=0.09))
        # a shop with tills (seen) and a parcel van (unseen), whose sizes follow the share
        shop = draw.shop(1.6, color=RETAIL).move_to([-4.8, 1.2, 0])
        van = VGroup(RoundedRectangle(corner_radius=0.08, width=1.5, height=0.7, stroke_width=0, fill_color="#B58CFF",
                                      fill_opacity=0.9),
                     *[Circle(radius=0.12, stroke_width=0, fill_color="#20242C", fill_opacity=1).shift(DOWN * 0.38 + RIGHT * x)
                       for x in (-0.45, 0.45)]).move_to([-4.8, -1.4, 0])
        sl = tx("seen at the tills", 16, RETAIL).next_to(shop, DOWN, buff=0.15)
        vl = tx("sold online: no till", 16, UNITS).next_to(van, DOWN, buff=0.22)
        pct = draw.number(at, decimals=1, suffix="% online", size=30, color=UNITS)
        pct.add_updater(lambda m: m.next_to(van, UP, buff=0.25))
        yr = draw.number(lambda: t.get_value(), decimals=0, commas=False, size=26, color=GREY_A)
        yr.add_updater(lambda m: m.next_to(pa, UP, buff=0.1).align_to(pa, RIGHT))
        head = tx("share of US retail sales made online", 18, GREY_A).next_to(pa, UP, buff=0.12).align_to(pa, LEFT)
        src = source("US Census Bureau, Quarterly Retail E-Commerce Sales (via FRED, ECOMPCTSA; annual averages, "
                     "seasonally adjusted)", size=13)
        with self.voiceover(
            "And the windows move. <bookmark mark='a'/> In 2000, a panel built on the tills of shops saw nearly "
            f"everything Americans bought at retail: less than {E['first'] + 0.1:.0f} percent was sold online. "
            "<bookmark mark='b'/> Every year since, a larger share has gone where no till beeps. "
            "<bookmark mark='c'/> It jumped in 2020, when the shops closed, and it never fell back. "
            f"<bookmark mark='d'/> By {E['last_year']}, it was about {E['last']:.0f} percent of all retail sales, "
            "about one dollar in six. A tracker that never moved its window would have seen many markets "
            "shrinking, when what had changed was where people bought. So when you read a market size, ask what "
            "its window was, and when the window was last moved."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head), FadeIn(shop), FadeIn(sl))
            self.add(ln, dot)
            vo.wait_until("a")
            self.play(FadeIn(van, shift=RIGHT * 0.3), FadeIn(vl), FadeIn(pct), FadeIn(yr))
            vo.wait_until("b")
            self.play(t.animate.set_value(2019), run_time=4.5, rate_func=linear)
            vo.wait_until("c")
            self.play(t.animate.set_value(2021), run_time=1.6, rate_func=linear)
            self.play(Flash(dot.get_center(), color=UNITS))
            vo.wait_until("d")
            self.play(t.animate.set_value(yrs[-1]), run_time=2.0, rate_func=linear)
        for m in (ln, dot, pct, yr):
            m.clear_updaters()
        self.clear_scene()
