from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ two sealed bids", r"Crusoe sells his old canoe twice. \ You value it at 70 shells. "
             r"\ What do you bid?", "Chapter one. Play it: two sealed bids.",
             lit={1961: r"Vickrey", 1988: r"Cox, Smith and Walker"}, scale=("person", "market"), horizon=("a day",))
        self.rules()
        self.reveal()
        self.flat()

    def rules(self):
        p = load("playit")
        stage = game_stage(12.0, 5.9, center=DOWN * 0.2)
        rules = VGroup(
            label(rf"you value Crusoe's canoe at {p['value']:.0f} shells", font_size=25, color=YOU),
            label(rf"three rivals each value it somewhere from 0 to {p['top']:.0f}, \ all values equally likely",
                  font_size=23),
            label(r"nobody knows anyone else's value; \ each writes one bid, \ sealed", font_size=23),
            label(r"sale A: \ the highest bid wins, \ and pays its own bid", font_size=25, color=FIRST),
            label(r"sale B: \ the highest bid wins, \ and pays the second-highest bid", font_size=25, color=SECOND),
            label(r"write down two bids, \ one for each sale, \ and keep them", font_size=26, color=E.ACCENT),
        ).arrange(DOWN, buff=0.22).move_to(stage.box.get_center() + UP * 0.55)
        who = VGroup(*[islander(k, 0.55) for k in ("ana", "bo", "dara")]).arrange(RIGHT, buff=0.3)
        who.move_to(stage.box.get_corner(DR) + LEFT * 1.6 + UP * 0.55)
        seller = gavel(0.6).move_to(stage.box.get_corner(DL) + RIGHT * 1.2 + UP * 0.6)
        ring = countdown().move_to(stage.box.get_bottom() + UP * 0.6)
        with self.voiceover(
            "Crusoe is selling his old canoe, and you would like it: to you it is worth seventy shells. "
            "<bookmark mark='a'/> Three other islanders want it too. Each of them values it somewhere between nothing "
            "and a hundred shells, and any value in that range is as likely as any other. <bookmark mark='b'/> Nobody "
            "knows anyone else's value, and each of you writes down a single bid, sealed. Crusoe sells it twice, by "
            "two rules. <bookmark mark='c'/> In sale A, the highest bid wins, and pays what it bid. "
            "<bookmark mark='d'/> In sale B, the highest bid wins, but pays the second-highest bid. "
            "<bookmark mark='e'/> What do you bid in each? Pause, write down your two bids, and keep them: this part "
            "comes back to them."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(rules[0]), FadeIn(seller))
            for mk, r in zip("abcde", rules[1:]):
                vo.wait_until(mk)
                anims = [FadeIn(r, shift=UP * 0.1)]
                if mk == "a":
                    anims.append(FadeIn(who))
                self.play(*anims)
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        p = load("playit")
        bids = np.array(p["bids"])
        ax = plane([0, 100], [0, 8], center=LEFT * 2.6 + DOWN * 0.35, x_length=7.0, y_length=4.8,
                   xticks=[0, 20, 40, 60, 80, 100], yticks=[0, 2, 4, 6, 8], xlabel=r"your bid, \ shells",
                   ylabel=r"your expected profit, \ shells", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        f1 = path(ax, bids, p["first"], color=FIRST, width=3.5, yr=(0, 8.2), xr=(0, 70))
        f2 = path(ax, bids, p["second"], color=SECOND, width=3.5, yr=(0, 8.2))
        l1 = label(r"sale A: \ pay your bid", font_size=17, color=FIRST).move_to(a.c2p(22, 6.9))
        l2 = label(r"sale B: \ pay the second bid", font_size=17, color=SECOND).move_to(a.c2p(84, 7.4))
        b1, b2 = p["best_first"], p["best_second"]
        m1 = VGroup(DashedLine(a.c2p(b1, 0), a.c2p(b1, p["profit_first"]), color=FIRST, stroke_width=2),
                    Dot(a.c2p(b1, p["profit_first"]), color=FIRST, radius=0.07))
        m2 = VGroup(DashedLine(a.c2p(b2, 0), a.c2p(b2, p["profit_second"]), color=SECOND, stroke_width=2),
                    Dot(a.c2p(b2, p["profit_second"]), color=SECOND, radius=0.07))
        side = VGroup(
            label(r"the rivals play the theory's equilibrium: \\ in A they bid three quarters of their values, \\ "
                  r"in B their values", font_size=19, color=GREY_A),
            label(rf"sale A's best bid: \ {b1:.1f}", font_size=24, color=FIRST),
            label(rf"sale B's best bid: \ {b2:.0f}, \ your value", font_size=24, color=SECOND),
            label(rf"either way you win {p['p_win'] * 100:.0f}\% of the time, \\ and expect "
                  rf"{p['profit_first']:.1f} shells of profit", font_size=21, color=E.ACCENT),
            label(r"the same number twice: \ chapter five", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here is what each bid is worth to you, on average, if your three rivals bid as the theory of this "
            "part says they should. <bookmark mark='a'/> In sale A that means bidding three quarters of their "
            "values; in sale B, bidding their values. <bookmark mark='b'/> In sale A, the yellow curve, a higher bid "
            "wins more often but leaves less when it wins. The best bid is fifty-two and a half. "
            "<bookmark mark='c'/> In sale B, the blue curve, the best bid is seventy, exactly your value, and "
            "bidding above it only adds the chance of winning at a loss. <bookmark mark='d'/> With those bids, you "
            "win the canoe about a third of the time in either sale, and expect six shells of profit in either. "
            "<bookmark mark='e'/> The same six shells twice is not a coincidence, and chapter five explains it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Indicate(side[0], color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(Create(f1), FadeIn(l1), run_time=1.5)
            self.play(Create(m1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(f2), FadeIn(l2), run_time=1.5)
            self.play(Create(m2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def flat(self):
        p = load("playit")
        bids = np.array(p["bids"])
        first = np.array(p["first"])
        v = p["value"]

        def ep(b):
            return float(np.interp(b, bids, first))

        rows = VGroup(
            label(rf"in sale A, \ a bid of 45 expects {ep(45):.1f} shells; \ 60 expects {ep(60):.1f}; \ "
                  rf"{p['best_first']:.1f} expects {p['profit_first']:.1f}", font_size=24, color=FIRST),
            label(r"the top of the curve is flat: \ near-misses cost little", font_size=24, color=GREY_A),
            label(rf"but a bid of {v:.0f} in sale A expects nothing: \ you'd pay all the canoe is worth to you",
                  font_size=24, color=HOLD),
            label(r"in sale B there is no guessing: \ whatever the others do, \ bid your value", font_size=24,
                  color=SECOND),
            label(r"in laboratories people bid more than the theory in both: \ chapter six", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "How much does a near-miss cost? <bookmark mark='a'/> In sale A, a bid of forty-five expects five point "
            "four shells, and a bid of sixty five point one, against six at the best bid. <bookmark mark='b'/> "
            "The top of the curve is flat, so a bid in the right neighbourhood loses little. <bookmark mark='c'/> "
            "But if you bid seventy in sale A, your whole value, you expect nothing at all: whenever you win, you pay "
            "everything the canoe is worth to you. <bookmark mark='d'/> Sale B needs no guessing about the others. "
            "Whatever they do, bidding your value is best, and chapter three proves it. <bookmark mark='e'/> And if "
            "you bid more than the theory says in either sale, you are in good company: people in laboratories do "
            "too, as chapter six shows."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
