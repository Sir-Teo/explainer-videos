from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403


def trade_card(key: str, give: float, get: float, width=2.7, font_size=22, color=E.ACCENT):
    box = RoundedRectangle(width=width, height=1.9, corner_radius=0.12, stroke_color=color, stroke_width=2.5,
                           fill_color=BLACK, fill_opacity=0.35)
    k = label(key, font_size=font_size + 12, color=color)
    a = label(rf"Ana gives {give:g} fish", font_size=font_size, color=FISH)
    b = label(rf"and gets {get:g} {'basket' if get == 1 else 'baskets'}", font_size=font_size, color=COCO)
    body = VGroup(k, a, b).arrange(DOWN, buff=0.14).move_to(box.get_center())
    return VGroup(box, body)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ trade in the box", r"Which trades would both traders accept, and which leaves "
             r"nothing more to gain?", "Chapter one. Play it: trade in the box.", horizon=("a day",))
        self.meet()
        self.choose()
        self.reveal()

    def meet(self):
        b = load("box")
        ana = islander("ana", 1.3, name=True, font_size=24)
        bo = islander("bo", 1.3, name=True, font_size=24)
        fa = VGroup(*[fish_glyph(0.5) for _ in range(8)]).arrange_in_grid(2, 4, buff=0.12)
        ca = VGroup(coconut(0.16), coconut(0.16), coconut(0.1)).arrange(RIGHT, buff=0.1)
        fb = VGroup(*[fish_glyph(0.5) for _ in range(2)]).arrange(RIGHT, buff=0.12)
        cb = VGroup(*[coconut(0.16) for _ in range(8)], coconut(0.1)).arrange_in_grid(2, 5, buff=0.1)
        left = VGroup(ana, VGroup(fa, ca).arrange(DOWN, buff=0.25)).arrange(RIGHT, buff=0.5)
        right = VGroup(bo, VGroup(fb, cb).arrange(DOWN, buff=0.25)).arrange(RIGHT, buff=0.5)
        VGroup(left, right).arrange(RIGHT, buff=1.6).move_to(UP * 1.2)
        rows = VGroup(
            label(rf"Ana: \ {b['eA'][0]:g} fish, \ {b['eA'][1]:g} baskets of coconuts; \ she spends "
                  rf"{100 * b['aA']:.0f}\% of her wealth on fish", font_size=24, color=ANA),
            label(rf"Bo: \ {b['eB'][0]:g} fish, \ {b['eB'][1]:g} baskets; \ he spends {100 * b['aB']:.0f}\% on "
                  rf"fish", font_size=24, color=BO),
            label(r"each likes variety: \ the more of one good you have, \ the less an extra one is worth",
                  font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.7)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Two islanders meet at the market. <bookmark mark='a'/> Ana has eight fish and one and a half baskets "
            "of coconuts. Bo has two fish and eight and a half baskets. <bookmark mark='b'/> Their tastes differ a "
            "little: Ana would spend forty percent of her wealth on fish, Bo sixty percent. And both like variety: "
            "the more of one good you have, the less an extra unit of it is worth to you. <bookmark mark='c'/> "
            "Like Radford's prisoners, they can only trade. Nothing is produced; there are only these ten fish and "
            "ten baskets to share."
        ) as vo:
            self.play(FadeIn(ana), FadeIn(bo), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fa), FadeIn(ca), FadeIn(fb), FadeIn(cb), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Indicate(VGroup(fa, fb), color=FISH), Indicate(VGroup(ca, cb), color=COCO))
        self.clear_scene()

    def choose(self):
        b = load("box")
        stage = game_stage(12.4, 5.8, center=DOWN * 0.2)
        cards = VGroup(*[trade_card(k, v["give"], v["get"]) for k, v in b["play"].items()]).arrange(RIGHT, buff=0.3)
        cards.move_to(stage.box.get_center() + UP * 0.5)
        q = label(r"which trades would both accept? \ and after which is there nothing left to gain?", font_size=27
                  ).next_to(cards, UP, buff=0.45)
        ring = countdown().next_to(cards, DOWN, buff=0.55)
        with self.voiceover(
            "Here are four trades, each proposed as a single swap. Trade A: Ana gives two fish and gets one basket. "
            "Trade B: four point two fish for four point three baskets. Trade C: two fish for six baskets. Trade D: "
            "six fish for one and a half baskets. Which of them would both accept, if the only alternative is no "
            "trade? And after which one would there be nothing left that both could gain from? Pause, and decide."
        ):
            self.play(FadeIn(stage), FadeIn(q))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.4), run_time=2.2)
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=6.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        b = load("box")
        rows = VGroup()
        for k, v in b["play"].items():
            c = trade_card(k, v["give"], v["get"], width=2.6, font_size=20).scale(0.85)
            ya = label(r"Ana: \ better" if v["ana_gains"] else r"Ana: \ worse", font_size=23,
                       color=E.TRUTH if v["ana_gains"] else HOLD)
            yb = label(r"Bo: \ better" if v["bo_gains"] else r"Bo: \ worse", font_size=23,
                       color=E.TRUTH if v["bo_gains"] else HOLD)
            if v["ana_gains"] and v["bo_gains"]:
                verdict = (r"both accept, \ and nothing more to gain" if v["on_cc"] else
                           r"both accept, \ but more trade would help both")
                col = CORE if v["on_cc"] else CC
            else:
                verdict = r"refused"
                col = HOLD
            vd = label(verdict, font_size=23, color=col)
            rows.add(VGroup(c, ya, yb, vd).arrange(RIGHT, buff=0.45))
        for r in rows:
            r[1].align_to(rows[0][1], LEFT)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(DOWN * 0.15)
        for r in rows:
            r[1].align_to(rows[0][1], LEFT)
            r[2].align_to(rows[0][2], LEFT)
            r[3].align_to(rows[0][3], LEFT)
        head = label(r"what each trade does", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here's what each would do. <bookmark mark='a'/> Trade A makes both better off: Ana has more fish "
            "than she wants and Bo more coconuts. But it stops too soon. After it, both could still gain by trading "
            "more. <bookmark mark='b'/> Trade B also makes both better off, and after it there is almost nothing left "
            "that both would want to do: any further swap would hurt one of them. <bookmark mark='c'/> Trade C is too "
            "good for Ana: Bo gives up six baskets for two fish and ends up worse than he started, so he refuses. "
            "<bookmark mark='d'/> Trade D is the reverse, and Ana refuses. <bookmark mark='e'/> B is special in "
            "another way too: to the first decimal, it is the trade the market would make, at the price that clears "
            "both markets. "
            "The next three chapters show why, in one picture."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(Indicate(rows[1], color=CORE, scale_factor=1.03))
        self.clear_scene()
