from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403

WCOL = {"2.1": "#7FD1B9", "1.7": "#F2C14E", "1.5": "#F25F5C"}


class CorePeriphery(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Core and periphery", r"How does a country split into a rich core and a poor periphery?",
             "Chapter six. Core and periphery.", lit={1991: r"Krugman", 1999: r"Fujita, \ Krugman and Venables"},
             scale=("firm", "nation"), horizon=("a century",))
        self.model()
        self.wiggle()
        self.tomahawk()

    def model(self):
        steps = flow_chain([(r"more workers \\ in the north", CITY), (r"a bigger market \\ there", WAGE),
                            (r"firms with scale \\ economies move in", GOLD),
                            (r"more varieties, \\ cheaper there", AMENITY)],
                           notes=[r"they spend locally", r"firms want to be \\ near customers",
                                  r"and save on shipping", r"real wages rise: \\ more workers come"],
                           box_w=2.7, font_size=19, note_size=16).move_to(UP * 0.6)
        back = CurvedArrow(steps.boxes[-1].get_bottom() + DOWN * 0.9, steps.boxes[0].get_bottom() + DOWN * 0.9,
                           angle=-TAU / 8, color=E.ACCENT, stroke_width=3)
        against = label(r"against it: \ farmers who cannot move, \ and the cost of shipping to them", font_size=20,
                        color=FARM).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Krugman, \ \emph{JPE} 99(3) (1991); \ Fujita, \ Krugman and Venables (1999), \ ch.\ 5",
                            corner=DR, font_size=12)
        with self.voiceover(
            "In 1991 Paul Krugman put Part thirty-six's variety and scale into geography. Two regions; farmers who "
            "stay put, half in each; and manufacturing workers who can move. <bookmark mark='a'/> Suppose a few more "
            "workers live in the north. They spend there, so the north is a bigger market; firms with economies of "
            "scale prefer to produce near the bigger market and ship to the smaller; with more firms in the north, "
            "more varieties are cheap there, so real wages are higher, and more workers come. "
            "<bookmark mark='b'/> The loop feeds itself. <bookmark mark='c'/> Against it: the farmers in the south "
            "still buy manufactures, and shipping to them is costly. Which force wins depends on the cost of "
            "transport."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in steps.boxes[1:]], *[GrowArrow(a) for a in steps.arrows],
                                  *[FadeIn(n) for n in steps.notes[1:]], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(back))
            vo.wait_until("c")
            self.play(FadeIn(against))
        self.clear_scene()

    def wiggle(self):
        C = load("cp")
        lams = np.array(C["lams"])
        ax = plane([0, 1], [-0.08, 0.08], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[-0.08, -0.04, 0, 0.04, 0.08],
                   xlabel=r"the north's share of manufacturing", ylabel=r"real wage, \ north minus south",
                   xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:+.2f}", font_size=14)
        zero = seg(ax, 0, 0, 1, 0, GREY_B, 1.5)
        curves = {k: path(ax, lams, v, WCOL[k], 3.2, yr=(-0.08, 0.08), smooth=True) for k, v in C["wiggle"].items()}
        side = VGroup(
            label(r"transport cost 2.1: \\ a worker who moves north \\ loses, \ and goes back: \\ the even "
                  r"spread is stable", font_size=17, color=WCOL["2.1"]),
            label(r"1.7: \ both the even spread \\ and the core are stable", font_size=17, color=WCOL["1.7"]),
            label(r"1.5: \ any move north \\ pays: \ everything \\ ends up in one region", font_size=17,
                  color=WCOL["1.5"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"solved by Agora: \ $\mu$ = 0.4, \ $\sigma$ = 5", corner=DR, font_size=12)
        with self.voiceover(
            "Agora solves the model for every split of manufacturing between the regions, with manufactures forty "
            "percent of spending. The curve is the real wage in the north minus that in the south. "
            "<bookmark mark='a'/> When shipping costs are high, a hundred and ten percent of the good's value, the "
            "curve slopes down: a worker who moves north lowers the north's real wage relative to the south's, and "
            "has reason to go back. The even spread is stable. <bookmark mark='b'/> At seventy percent, the curve "
            "wiggles: the even spread is stable, but so is a core in either region. <bookmark mark='c'/> At fifty "
            "percent, the curve slopes up: anyone who moves north raises the gain from moving north, and everything "
            "ends up in one place."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), Create(curves["2.1"]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(curves["2.1"], color=WHITE, scale_factor=1.0))
            for mk, k, s in zip("bc", ("1.7", "1.5"), side[1:]):
                vo.wait_until(mk)
                self.play(Create(curves[k]), FadeIn(s), run_time=1.5)
        self.clear_scene()

    def tomahawk(self):
        C = load("cp")
        ax = plane([1.3, 2.2], [0, 1], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[1.3, 1.5, 1.7, 1.9, 2.1], yticks=[0, 0.25, 0.5, 0.75, 1],
                   xlabel=r"transport cost \ (1 = free)", ylabel=r"the north's share of manufacturing",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        B, S = C["break"], C["sustain"]
        stable = VGroup(seg(ax, B, 0.5, 2.2, 0.5, E.ACCENT, 5), seg(ax, 1.3, 1.0, S, 1.0, E.ACCENT, 5),
                        seg(ax, 1.3, 0.0, S, 0.0, E.ACCENT, 5))
        unst = VGroup(seg(ax, 1.3, 0.5, B, 0.5, GREY_B, 2.5, dashed=True))
        up, dn = [], []
        for p in C["tomahawk"]:
            for lam, st in p["eq"]:
                if 0.0 < lam < 0.5 and not st:
                    dn.append((p["T"], lam))
                if 0.5 < lam < 1.0 and not st:
                    up.append((p["T"], lam))
        for branch, end in ((up, 1.0), (dn, 0.0)):
            pts = [(B, 0.5)] + sorted(branch) + [(S, end)]
            unst.add(DashedVMobject(path(ax, [x for x, _ in pts], [y for _, y in pts], GREY_B, 2.5, smooth=False),
                                    num_dashes=24))
        vb = vline(ax, B, 0, 1, RENT)
        vs = vline(ax, S, 0, 1, GAIN)
        side = VGroup(
            label(r"solid: \ stable; \ dashed: \ unstable", font_size=17, color=WHITE),
            label(rf"break point \ {B:.2f}: \\ the even spread \\ collapses", font_size=18, color=RENT),
            label(rf"sustain point \ {S:.2f}: \\ a core can \\ hold itself together", font_size=18, color=GAIN),
            label(rf"history decides \\ between {B:.2f} and {S:.2f}", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Fujita, \ Krugman and Venables (1999), \ ch.\ 5; \ solved by Agora", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Put every transport cost on one picture, and the equilibria make the shape geographers call the "
            "tomahawk. <bookmark mark='a'/> Solid lines are stable, dashed unstable. Start at the right, with "
            "shipping dear: industry is spread evenly, and nothing much changes as costs fall. "
            f"<bookmark mark='b'/> Then, at {B:.2f}, the even spread breaks, suddenly and completely: the "
            "economy tips into a core and a periphery. <bookmark mark='c'/> And the core, once formed, survives "
            f"even if costs rise again, up to {S:.2f}. <bookmark mark='d'/> Between the two points, history "
            "decides. Gradual change can have sudden effects, and a small advantage, like the north's few extra "
            "workers, can lock in a geography for a century."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(stable[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(unst[0]), Create(vb), FadeIn(stable[1:]), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(unst[1:]), Create(vs), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
