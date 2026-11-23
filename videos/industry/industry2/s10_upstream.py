from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403


class Upstream(VoiceoverScene):
    def construct(self):
        card(self, 10, "Upstream and downstream", "How far is each industry from the person who finally buys?",
             "Chapter ten. Upstream and downstream.", lit=("make",))
        io = R["io"]
        pts = sorted(zip(io["names"], io["upstream"]), key=lambda t: -t[1])
        axis = Line(DOWN * 3.0, UP * 2.7, color=I.FAINT).shift(LEFT * 4.6)
        y = lambda u: -3.0 + (u - 0.9) / (2.9 - 0.9) * 5.7  # noqa: E731
        top = T("far from the buyer: upstream", 18, I.MEMORY).next_to(axis, UP, buff=0.1)
        bot = T("sells to the buyer: downstream", 18, I.PROFIT).next_to(axis, DOWN, buff=0.1)
        ticks = VGroup(*[VGroup(Line(LEFT * 0.08, RIGHT * 0.08, color=I.FAINT), T(f"{v:.1f}", 14, I.DIM)).arrange(
            LEFT, buff=0.08).move_to(np.array([-4.75, y(v), 0])) for v in (1.0, 1.5, 2.0, 2.5)])
        dots = VGroup()
        side = 1
        for k, (n, u) in enumerate(pts):
            c = interpolate_color(ManimColor(I.PROFIT), ManimColor(I.MEMORY), (u - 1.0) / 1.8)
            d = Dot(np.array([-4.6, y(u), 0]), radius=0.08, color=c)
            x = -3.9 + (k % 3) * 2.9
            lab = VGroup(T(n, 18, I.TEXT), T(f"{u:.2f}", 16, c)).arrange(RIGHT, buff=0.12).move_to(
                np.array([x, y(u), 0]), aligned_edge=LEFT)
            lead = DashedLine(d.get_center(), lab.get_left() + LEFT * 0.05, stroke_width=1, color=c, dash_length=0.05)
            dots.add(VGroup(d, lead, lab))
        acts = VGroup(T("This series runs from the top of this scale to the bottom:", 18, I.DIM),
                      T("out of the ground, making, building, moving, selling, information, money, people", 18,
                        I.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).to_corner(DR, buff=0.35)
        src = source("BEA 2023 use table: upstreamness after Antras, Chor, Fally and Hillberry (2012)", corner=UR,
                     size=14)
        with self.voiceover(
            "The table answers one more question: how far is each industry from the person who finally buys? "
            "<bookmark mark='a'/> Economists measure it by the average number of steps an industry's output passes "
            "through before someone uses it up. A measure of one means it sells straight to households, the "
            "government or buyers abroad. <bookmark mark='b'/> At the top of the scale are farms and mines, at "
            "about 2.7: wheat becomes flour, flour becomes bread, bread is sold in a shop. Transport and business "
            "services are high too; they mostly serve other businesses. <bookmark mark='c'/> Manufacturing, utilities "
            "and wholesale sit in the middle, around two. <bookmark mark='d'/> And at the bottom, close to "
            "one, are retail, government, education and health care, which sell their services directly to the "
            "people who use them. <bookmark mark='e'/> This series is ordered by the same scale: it starts with oil, "
            "metal and food, and ends with hospitals, schools and the people who work in them."
        ) as vo:
            self.play(Create(axis), FadeIn(top), FadeIn(bot), FadeIn(ticks), FadeIn(src))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dd) for dd in dots[:4]], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(dd) for dd in dots[4:10]], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(dd) for dd in dots[10:]], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("e")
            self.play(FadeIn(acts))
        self.clear_scene()
