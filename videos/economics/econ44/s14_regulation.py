from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class Regulation(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Regulating a firm that knows more", r"How do you regulate costs you cannot see?",
             "Chapter twelve. Regulating a firm that knows more.",
             lit={1982: r"Baron and Myerson", 1993: r"Laffont and Tirole"}, scale=("firm", "nation"),
             horizon=("a year",))
        self.problem()
        self.solution()
        self.tradeoff()

    def problem(self):
        G = load("regulation")
        R = TRUTH["regulation"]
        rows = VGroup(
            label(rf"a utility's unit cost is {R['c_lo']:.0f} or {R['c_hi']:.0f}, \ equally likely; \ only the firm "
                  r"knows which", font_size=21, color=WHITE),
            label(rf"demand $P$ = {R['a']:.0f} $-$ $q$; \ the regulator sets output and pays the firm", font_size=21,
                  color=GREY_A),
            label(r"the trouble: \ a low-cost firm can claim high costs \ and pocket the difference", font_size=21,
                  color=LOSS),
            label(rf"to make it tell the truth, \ the regulator must leave it a rent: \ (cost gap) $\times$ "
                  rf"(high-cost output) = {G['rent_full']:.0f} at full output", font_size=21, color=FIRM1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.1)
        head = label(r"the regulator's problem", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.REGULATION.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Some markets are natural monopolies, and are regulated rather than broken up. But the regulator "
            "knows less than the firm. <bookmark mark='a'/> Suppose a utility's cost of a unit is either "
            f"{R['c_lo']:.0f} or {R['c_hi']:.0f}, and only the firm knows which. <bookmark mark='b'/> The regulator "
            "sets output and pays the firm. <bookmark mark='c'/> A low-cost firm can claim to have high costs and "
            "keep the difference. <bookmark mark='d'/> To make it tell the truth, the regulator must leave the "
            "low-cost firm a rent: the cost gap times whatever it would be paid to produce if it claimed high "
            f"costs, {G['rent_full']:.0f} if the high-cost output were set efficiently."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def solution(self):
        G = load("regulation")
        R = TRUTH["regulation"]
        a = R["a"]
        ax = plane([0, 10], [0, 10], center=LEFT * 1.8 + DOWN * 0.4, x_length=7.6, y_length=4.8,
                   xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 2, 4, 6, 8, 10], xlabel=r"output", ylabel=r"price",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        dem = seg(ax, 0, a, a, 0, KEEP, 3.0)
        lo = seg(ax, 0, R["c_lo"], 10, R["c_lo"], GAIN, 1.8, dashed=True)
        hi = seg(ax, 0, R["c_hi"], 10, R["c_hi"], FIRM1, 1.8, dashed=True)
        vc = seg(ax, 0, G["virtual"], 10, G["virtual"], LOSS, 1.8, dashed=True)
        p_lo = dot(ax, G["q_lo"], R["c_lo"], GAIN, 0.1)
        p_hi0 = dot(ax, G["q_hi_full"], R["c_hi"], GREY_B, 0.09)
        p_hi = dot(ax, G["q_hi"], G["p_hi"], LOSS, 0.1)
        side = VGroup(
            label(rf"low cost: \ efficient output, \\ {G['q_lo']:.0f} units", font_size=18, color=GAIN),
            label(rf"high cost: \ output cut from \\ {G['q_hi_full']:.0f} to {G['q_hi']:.1f}; \ price "
                  rf"{G['p_hi']:.1f} \\ against a cost of {R['c_hi']:.0f}", font_size=18, color=LOSS),
            label(rf"the rent falls from \\ {G['rent_full']:.0f} to {G['rent']:.1f}", font_size=18, color=FIRM1),
            label(rf"profits weighted {R['weight']} \\ against consumers' 1", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.REGULATION.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "David Baron and Roger Myerson worked out the best the regulator can do, in 1982. "
            "<bookmark mark='a'/> The low-cost firm produces the efficient amount, where price equals its cost. "
            "<bookmark mark='b'/> The high-cost firm is asked to produce less than would be efficient: price is set "
            "above its cost, at a 'virtual cost' that adds the rent its output creates. "
            f"<bookmark mark='c'/> Cutting the high-cost output from {G['q_hi_full']:.0f} to {G['q_hi']:.1f} shrinks "
            f"the rent the low-cost firm must be left, from {G['rent_full']:.0f} to {G['rent']:.1f}. "
            "<bookmark mark='d'/> The regulator accepts a little inefficiency when costs are high to give away less "
            "when they are low, because it values a dollar of the firm's profit less than a dollar for consumers."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(dem), Create(lo), Create(hi), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(p_lo, scale=1.5), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(vc), FadeIn(p_hi0), FadeIn(p_hi, scale=1.5), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def tradeoff(self):
        G = load("regulation")
        w = np.array(G["weights"])
        ax = plane([0, 1], [0, 13], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 3, 6, 9, 12],
                   xlabel=r"weight on the firm's profit", ylabel=r"high-cost output, \ and the low-cost firm's rent",
                   xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        q = path(ax, w, G["q_hi_w"], LOSS, 3.0, smooth=False)
        r = path(ax, w, G["rent_w"], FIRM1, 3.0, smooth=False)
        side = VGroup(
            label(r"red: \ high-cost output", font_size=18, color=LOSS),
            label(r"gold: \ the rent", font_size=18, color=FIRM1),
            label(r"weight 1: \ rents cost \\ nothing, \ no distortion", font_size=18, color=GAIN),
            label(r"Laffont and Tirole: \\ the same logic for \\ procurement and \\ price caps", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.REGULATION.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "How far to distort depends on how much the regulator minds leaving profit to the firm. "
            "<bookmark mark='a'/> The less weight on profit, the more it cuts the high-cost output, "
            "<bookmark mark='b'/> and the smaller the rent. <bookmark mark='c'/> If a dollar of profit counted as "
            "much as a dollar for consumers, rents would cost nothing, and there would be no distortion at all. "
            "<bookmark mark='d'/> Jean-Jacques Laffont and Jean Tirole built a theory of procurement and "
            "regulation on this trade-off between efficiency and rents, which shapes how price caps and cost-sharing "
            "contracts are designed."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(q), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(side[0], color=WHITE), ShowPassingFlash(q.copy().set_stroke(WHITE, 5), time_width=0.5),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(Create(r), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
