from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403

# the game (illustrative, $m a year): the incumbent alone earns 100; an entrant must spend 30 to set up; if both are in,
# each earns 40.  Each lever is (name, what it does, entrant's profit after entry, incumbent's profit if it deters, why)
MONO, ENTRY, DUO = 100, 30, 40
LEVERS = [("Threaten a price war", "promise to cut prices if it enters", 40, None,
           "after entry a war costs the incumbent too, so it will not fight: the threat is empty"),
          ("Build capacity first", "a bigger plant, paid for now", 25, 80,
           "with the plant already built, flooding the market is the incumbent's best reply: credible"),
          ("Advertise", "a brand the entrant must outspend", 25, 85,
           "the entrant needs 15 more a year to win shoppers"),
          ("Lock customers in", "contracts, loyalty schemes, switching costs", 20, 90,
           "with half the customers tied up, the entrant can win only half as many")]


class Entrant(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: the entrant", "A rival wants your castle. What actually stops it?",
             "Chapter one. Run it: the entrant.", lit=("moat",))
        self.setup()
        self.levers()

    def setup(self):
        keep = draw.castle(2.2, moat=0.25).move_to([-4.6, 0.2, 0])
        coins = VGroup(*[draw.coin(0.12) for _ in range(10)]).arrange_in_grid(rows=2, cols=5, buff=0.05).next_to(
            keep, UP, buff=0.2)
        you = tx("you: the incumbent", 22, STONE, bold=True).next_to(keep, DOWN, buff=0.35)
        mono = tx(f"alone: ${MONO}m a year", 20, RET).next_to(you, DOWN, buff=0.12)
        camp = VGroup(draw.crowd(3, 0.45, color=ENTRANT, cols=3),
                      Polygon([-0.35, 0, 0], [0.35, 0, 0], [0, 0.55, 0], stroke_width=0, fill_color=ENTRANT,
                              fill_opacity=0.8)).arrange(RIGHT, buff=0.3).move_to([4.6, 0.0, 0])
        them = tx("the entrant", 22, ENTRANT, bold=True).next_to(camp, DOWN, buff=0.35)
        cost = tx(f"setting up costs ${ENTRY}m a year", 20, COST_).next_to(them, DOWN, buff=0.12)
        duo = VGroup(tx(f"if both are in: ${DUO}m each", 24, WHITE, bold=True),
                     MathTex(rf"{DUO} - {ENTRY} = +10", font_size=40, color=RET),
                     tx("so it comes in", 20, GREY_B)).arrange(DOWN, buff=0.12).move_to([0, 2.3, 0])
        tag = estimate_tag("illustrative: a model market, $m a year", corner=DR)
        with self.voiceover(
            "Play it yourself. <bookmark mark='a'/> You own the only business in a market, and it earns a hundred "
            "million dollars a year. <bookmark mark='b'/> A rival is watching. To come in it would have to spend "
            "thirty million a year on a plant, a brand and a sales force. <bookmark mark='c'/> If it does, you will "
            "share the market and earn forty million each. Forty is more than thirty, so it will come in, and your "
            "hundred becomes forty. You have four moves. Which one stops it?"
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(keep, shift=UP * 0.2), FadeIn(you), FadeIn(mono),
                      LaggedStart(*[FadeIn(c, scale=1.4) for c in coins], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(FadeIn(camp, shift=LEFT * 0.3), FadeIn(them), FadeIn(cost))
            vo.wait_until("c")
            self.play(FadeIn(duo, shift=DOWN * 0.1))
            self.play(camp.animate.shift(LEFT * 2.2), *[c.animate.set_opacity(0.3) for c in coins[4:]], run_time=1.6)
            self.play(camp.animate.shift(RIGHT * 2.2), *[c.animate.set_opacity(1) for c in coins[4:]], run_time=0.8)
        self.keep_, self.camp_, self.coins_ = keep, camp, coins
        self.play(FadeOut(duo), FadeOut(tag))
        self.statics = VGroup(you, mono, them, cost)

    def levers(self):
        cards = VGroup()
        for name, what, after, inc, why in LEVERS:
            ok = after - ENTRY
            box = RoundedRectangle(corner_radius=0.14, width=3.2, height=1.55, stroke_color=GOLD, stroke_width=2,
                                   fill_color="#141A24", fill_opacity=1)
            body = VGroup(tx(name, 22, GOLD, bold=True), tx(what, 15, GREY_B),
                          tx(f"entrant: {after} - {ENTRY} = {ok:+d}", 19, RET if ok < 0 else COST_, bold=True)
                          ).arrange(DOWN, buff=0.1)
            if body.width > 3.0:
                body.scale_to_fit_width(3.0)
            cards.add(VGroup(box, body.move_to(box)))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, 1.55, 0]).scale(0.92)
        verdicts = VGroup(*[tx(v, 18, WHITE) for _, _, _, _, v in LEVERS])
        for v in verdicts:
            v.move_to([0, -2.85, 0])
            if v.width > 12.5:
                v.scale_to_fit_width(12.5)
        stamp = [tx("comes in", 18, COST_, bold=True), tx("stays out", 18, RET, bold=True)]
        with self.voiceover(
            "First move: threaten a price war. <bookmark mark='a'/> It costs nothing to say. But think about the "
            "day after the rival arrives. A war would cost you as much as it costs them, and sharing the market at "
            "forty beats fighting at ten. The rival knows that, so the threat is empty, and it comes in. "
            "<bookmark mark='b'/> Second move: build a bigger plant now, before it arrives. Now the money is spent. "
            "If the rival enters, running that plant flat out is your best reply, prices fall, and the rival would "
            "make twenty-five, less than its thirty of costs. It stays out. The threat is believable because you "
            "can no longer take it back. <bookmark mark='c'/> Third: advertise, so the rival must spend fifteen "
            "million more to win shoppers. It stays out. <bookmark mark='d'/> Fourth: lock your customers in with "
            "contracts and loyalty schemes, so the rival can win only half as many. It stays out. "
            "<bookmark mark='e'/> Three of the four moves work, and they share one thing: each is a cost you pay "
            "now, which changes what the rival can expect later. That is what a moat is made of. You can play this "
            "game, with your own numbers, on the course site."
        ) as vo:
            self.play(*[FadeOut(m) for m in self.statics])
            self.play(self.keep_.animate.scale(0.75).move_to([-5.4, -1.35, 0]),
                      self.camp_.animate.scale(0.8).move_to([5.2, -1.35, 0]))
            home = self.camp_.get_center().copy()
            for k, mark in enumerate("abcd"):
                vo.wait_until(mark)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(verdicts[k]))
                enters = LEVERS[k][2] - ENTRY >= 0
                s_ = stamp[0 if enters else 1].copy().next_to(cards[k][0], DOWN, buff=0.05).align_to(cards[k][0], RIGHT)
                if enters:
                    self.play(self.camp_.animate.move_to([-2.6, -1.35, 0]), FadeIn(s_), run_time=1.4)
                    self.play(self.camp_.animate.move_to(home), run_time=0.8)
                else:
                    self.play(self.camp_.animate.move_to([2.4, -1.35, 0]), run_time=0.8)
                    self.play(self.camp_.animate.move_to(home), FadeIn(s_), run_time=0.8)
                self.play(FadeOut(verdicts[k]), run_time=0.3)
            vo.wait_until("e")
            self.play(Indicate(VGroup(cards[1], cards[2], cards[3]), color=GOLD, scale_factor=1.03),
                      Indicate(self.keep_.moat, color="#7EC8F5"))
        self.clear_scene()
