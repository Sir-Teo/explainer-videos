from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ the odometer climbs", r"When would you rebuild the engine?",
             "Chapter one. Play it: the odometer climbs.", lit={1987: r"Rust"},
             scale=("firm",), horizon=("a month", "a decade"))
        self.ask()
        self.reveal()
        self.curve()

    def ask(self):
        P = load("playit")
        facts = VGroup()
        for big, small, col in ((r"a rebuild", rf"costs \${P['RC']:,.0f}; \\ the engine is \\ as good as new", REBUILD),
                                (r"upkeep", rf"\${P['per_bin']:.0f} a month for \\ every 5,000 miles \\ on the engine",
                                 BUS),
                                (r"the miles", rf"about {P['miles_month']:,.0f} \\ a month, \ as on \\ Zurcher's buses",
                                 KEEP),
                                (r"your rule", r"rebuild when the \\ engine reaches \\ a mileage you set", YOU)):
            box = RoundedRectangle(width=3.0, height=2.3, corner_radius=0.12, stroke_color=col, stroke_width=2.2,
                                   fill_color="#141821", fill_opacity=1)
            t1 = label(big, font_size=22, color=col).move_to(box.get_top() + DOWN * 0.42)
            t2 = label(small, font_size=16, color=GREY_A).next_to(t1, DOWN, buff=0.22)
            facts.add(VGroup(box, t1, t2))
        facts.arrange(RIGHT, buff=0.3).move_to(UP * 0.7)
        opts = VGroup(*[label(rf"{k}: \ {o // 1000:,}k miles", font_size=26, color=WHITE)
                        for k, o in zip("ABCD", TRUTH["playit"]["options"])]).arrange(RIGHT, buff=0.6).next_to(
            facts, DOWN, buff=0.55)
        head = label(r"Your turn: \ which rule costs the bus line least, \ month after month?", font_size=27,
                     color=E.ACCENT).to_edge(UP, buff=0.35)
        ring = countdown().scale(0.6).next_to(opts, DOWN, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        for f in facts:
            f.set_opacity(0.3)
        with self.voiceover(
            "Your turn. You run the Island's bus line. <bookmark mark='a'/> Rebuilding an engine costs "
            f"{P['RC']:,.0f} dollars and makes it as good as new. <bookmark mark='b'/> Keeping an old engine costs "
            f"upkeep: {P['per_bin']:.0f} dollars a month for every five thousand miles on it, so an engine at a "
            f"hundred and fifty thousand miles costs {P['upkeep_150k']:.0f} dollars a month to keep running. "
            f"<bookmark mark='c'/> A bus covers about {P['miles_month']:,.0f} miles a month, as Zurcher's did. "
            "<bookmark mark='d'/> Your rule: rebuild when the engine reaches a mileage you choose. Which rule "
            "costs least, month after month: fifty thousand miles, a hundred and fifty, two hundred and fifty, or "
            "three hundred and fifty? Pause, and choose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(facts, lag_ratio=0.2), run_time=1.5)
            for mk, f in zip("abcd", facts):
                vo.wait_until(mk)
                self.play(f.animate.set_opacity(1.0), Indicate(f[1], scale_factor=1.1))
            self.play(FadeIn(opts), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.keep = (head, facts, opts, tag)

    def reveal(self):
        P = load("playit")
        head, facts, opts, tag = self.keep
        k = list(TRUTH["playit"]["options"]).index(P["best_option"])
        hl = SurroundingRectangle(opts[k], color=GAIN, buff=0.12)
        costs = label(r", \ ".join(rf"{o // 1000}k: \ \${P['options'][str(o)]:,.0f}" for o in
                                   TRUTH["playit"]["options"]) + r" \ a month", font_size=22,
                      color=E.ACCENT).next_to(opts, DOWN, buff=0.4)
        o = TRUTH["playit"]["options"]
        with self.voiceover(
            f"The answer is {'ABCD'[k]}, {P['best_option'] // 1000} thousand miles. <bookmark mark='a'/> On average "
            f"it costs {P['options'][str(P['best_option'])]:,.0f} dollars a month per bus, counting rebuilds spread "
            f"over the months between them. Rebuilding at {o[0] // 1000} thousand costs "
            f"{P['options'][str(o[0])]:,.0f}: rebuilds come too often. At {o[3] // 1000} thousand it costs "
            f"{P['options'][str(o[3])]:,.0f}: old engines eat the savings in upkeep."
        ) as vo:
            self.play(Create(hl))
            vo.wait_until("a")
            self.play(FadeIn(costs, shift=UP * 0.1))
        self.clear_scene()

    def curve(self):
        P = load("playit")
        th = np.array(P["thresholds"]) / 1000
        c = np.array(P["cost"])
        ax = plane([0, 450], [150, 450], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 100, 200, 300, 400], yticks=[150, 250, 350, 450],
                   xlabel=r"rebuild at this mileage, \ thousands", ylabel=r"average cost per bus per month, \ dollars",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ln = path(ax, th, np.minimum(c, 450), GAIN, 3.4, yr=(150, 450))
        best = VGroup(vline(ax, P["best"] / 1000, 150, 450, GAIN), dot(ax, P["best"] / 1000, P["best_cost"], GAIN,
                                                                        0.09))
        reb = path(ax, th, np.minimum(P["RC"] / (th * 1000 / P["miles_month"]) + 150, 450), REBUILD, 2.2,
                   yr=(150, 450))
        side = VGroup(
            label(r"green: \ the total, \\ rebuilds plus upkeep", font_size=18, color=GAIN),
            label(r"left: \ rebuilds too \\ often", font_size=18, color=REBUILD),
            label(r"right: \ upkeep on \\ old engines", font_size=18, color=BUS),
            label(rf"the best rule: \\ {P['best'] // 1000} thousand miles", font_size=19, color=E.ACCENT),
            label(r"Zurcher's problem had \\ one more thing: \\ surprises", font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        del reb
        with self.voiceover(
            "Here is the whole trade-off. <bookmark mark='a'/> The average cost of a rule, against the mileage at "
            "which it rebuilds. <bookmark mark='b'/> Rebuild early, and the rebuild bill comes round too often. "
            "<bookmark mark='c'/> Rebuild late, and the upkeep on old engines piles up. <bookmark mark='d'/> The "
            f"bottom is at {P['best'] // 1000} thousand miles. <bookmark mark='e'/> Zurcher's real problem had one "
            "more ingredient. Each month brought things the records do not show: an engine that sounded wrong, a "
            "bus needed for a busy route, a mechanic free that week. Those surprises are why the same mileage led "
            "sometimes to a rebuild and sometimes not, and they are the key to how Rust estimated the costs."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(best), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
