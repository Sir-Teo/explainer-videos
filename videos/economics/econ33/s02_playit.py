from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403


def boom_minis(B, width: float = 3.2, height: float = 1.35, reveal: bool = False) -> VGroup:
    """The eight booms as small charts of bank loans to GDP over the ten years to the boom's last year, with the rise
    over the last five and the change in real house prices.  ``reveal`` adds the country, the year and the outcome."""
    cards = VGroup()
    for b in B["booms"]:
        t0 = b["year"]
        ax = plane([-10, 3 if reveal else 0], [0, 200], x_length=width - 0.35, y_length=height,
                   xticks=[-10, -5, 0], yticks=[0, 100, 200], xfmt=lambda v: f"{v:+.0f}" if v else "0",
                   yfmt=lambda v: f"{v:.0f}", font_size=11)
        xs = [y - t0 for y in b["years"]]
        ln = path(ax, [x for x in xs if x <= 0], [v for x, v in zip(xs, b["cg"]) if x <= 0], CREDIT, 2.6,
                  smooth=False)
        parts = [ax, ln]
        if reveal:
            after = path(ax, [x for x in xs if x >= 0], [v for x, v in zip(xs, b["cg"]) if x >= 0], GREY_B, 2.0,
                         smooth=False)
            parts.append(after)
        head = label(rf"\textbf{{{b['letter']}}}", font_size=30, color=WHITE)
        info = VGroup(label(rf"loans +{b['rise']:.0f} points in 5 years", font_size=19, color=CREDIT),
                      label(rf"real house prices {b['house5']:+.0f}\%", font_size=19, color=HOUSE)).arrange(
            DOWN, buff=0.05)
        g = VGroup(head, VGroup(*parts), info).arrange(DOWN, buff=0.08)
        if reveal:
            col = CRISIS if b["crisis"] else CALM
            out = label(rf"{tex_safe(b['name'])} {t0}: \ " + (r"crisis" if b["crisis"] else r"no crisis"),
                        font_size=19, color=col).next_to(g, DOWN, buff=0.06)
            g.add(out)
            g.outcome = out
        box = SurroundingRectangle(g, buff=0.12, corner_radius=0.08, stroke_color=GREY_D, stroke_width=1.5)
        card = VGroup(box, g)
        card.box, card.g = box, g
        cards.add(card)
    cards.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3))
    if cards.width > 13.4:
        cards.width = 13.4
    return cards


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ eight credit booms", r"Which of these booms ended in a crisis?",
             "Chapter one. Play it: eight credit booms.", lit={1955: r"the window opens", 2015: r"and closes"},
             scale=("nation",), horizon=("a decade",))
        self.rules()
        self.choose()

    def rules(self):
        B = load("booms")
        P = load("panel")
        board = VGroup(
            label(r"eight credit booms since 1955, \ from eighteen rich countries", font_size=28, color=E.ACCENT),
            label(r"the rule: \ the biggest rises in bank loans to GDP over five years, \ one per country",
                  font_size=23,
                  color=CREDIT),
            label(r"no crisis during the boom, \ and the economy still growing at its end", font_size=23,
                  color=GREY_A),
            label(r"your task: \ which ended in a systemic banking crisis within three years?", font_size=24,
                  color=WHITE),
            label(rf"for scale: \ a crisis starts in {100 * P['base_rate']:.0f}\% of peacetime years; \ within "
                  rf"any three, \ {100 * P['odds']['base']:.0f}\%", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        tag = data_tag(r"Jord\`a, \ Schularick and Taylor, \ Macrohistory Database R6", corner=DR, font_size=13)
        with self.voiceover(
            "Your turn. Here are eight credit booms, chosen by a rule, not by me. <bookmark mark='a'/> From "
            "eighteen rich countries since 1955, the eight biggest rises in bank lending relative to GDP over five "
            "years, one per country. <bookmark mark='b'/> No crisis happened during any of them, and each economy "
            "was still growing in the boom's last year. <bookmark mark='c'/> Your task: decide which of them ended "
            "in a systemic banking crisis within the next three years. <bookmark mark='d'/> For scale: in these "
            f"countries a crisis starts in about {100 * P['base_rate']:.0f} percent of peacetime years, so in about "
            f"{100 * P['odds']['base']:.0f} percent of all three-year stretches."
        ) as vo:
            self.play(FadeIn(board[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", board[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        del B
        self.clear_scene()

    def choose(self):
        B = load("booms")
        cards = boom_minis(B).move_to(DOWN * 0.15)
        head = label(r"bank loans, \ \% of GDP, \ over the ten years to each boom's end", font_size=22,
                     color=GREY_A).to_edge(UP, buff=0.3)
        ring = countdown().scale(0.55).to_corner(DR, buff=0.35)
        ask = label(r"which ended in a crisis? \ write down your letters", font_size=22, color=YOU).to_edge(
            DOWN, buff=0.25)
        with self.voiceover(
            "Here they are, unlabelled. Each chart shows bank loans as a share of GDP over the ten years to the end "
            "of the boom; under it, the rise over the last five years and the change in real house prices. "
            "<bookmark mark='a'/> Some are enormous: loans up by seventy points of GDP in five years. Others "
            "smaller. Some came with soaring house prices, others not. <bookmark mark='b'/> Which ended in a "
            "crisis? Write down your letters. You will see the answers, and how a statistical model fitted only on "
            "earlier history would have done, in chapter ten."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("a")
            self.play(*[Indicate(cards[i].box, color=WHITE, scale_factor=1.02) for i in (0, 1)])
            vo.wait_until("b")
            self.play(FadeIn(ask), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=10.0, rate_func=linear)
        self.clear_scene()
