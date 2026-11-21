from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ distributions at the central bank", r"Who uses these models, \ and for what?",
             "Chapter fourteen. In practice: distributions at the central bank.",
             lit={1998: r"Krusell and Smith", 2019: r"the Fed's DFA"}, scale=("household", "nation"),
             horizon=("a decade",))
        self.people()
        self.incidence()
        self.called()

    def people(self):
        rows = VGroup(
            label(r"measurement: \ the Federal Reserve's Distributional Financial Accounts, \ quarterly since 1989, "
                  r"\ published since 2019", font_size=21, color=DATA),
            label(r"models: \ central bank researchers now build HANK models beside the older ones", font_size=21,
                  color=MANY),
            label(r"software: \ the sequence-space Jacobian toolkit, \ open source, \ in Python", font_size=21,
                  color=THEORY),
            label(r"questions: \ who gains from a rate cut, \ a stimulus cheque, \ an inflation", font_size=21,
                  color=INDIRECT),
            label(r"firms: \ the Census Bureau's Business Dynamics Statistics, \ entry and exit by age and size",
                  font_size=21, color=FIRM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.2)
        if rows.width > 13.2:
            rows.width = 13.2
        head = label(r"distributions in practice", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Where is this used? <bookmark mark='a'/> First in measurement. Since 2019 the Federal Reserve has "
            "published distributional financial accounts, which split the nation's balance sheet by wealth, income, "
            "age and education, quarter by quarter back to 1989: the data of chapter six and of the intermission. "
            "<bookmark mark='b'/> Central bank researchers now build HANK models alongside the older "
            "representative-agent ones, <bookmark mark='c'/> often with the open-source sequence-space Jacobian "
            "toolkit. <bookmark mark='d'/> The questions they answer are distributional ones: who gains from a rate "
            "cut, who spends a stimulus cheque, who pays for an inflation. <bookmark mark='e'/> And for firms, the "
            "Census Bureau's Business Dynamics Statistics count entry and exit by firm age and size, the facts "
            "Hopenhayn's industry is fitted to."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def incidence(self):
        P = load("playit")
        rows = P["rows"]
        chain = flow_chain([(r"a policy", DIRECT), (r"paths of rates, \ wages, \ taxes", INDIRECT),
                            (r"every household's rule", MANY), (r"the change in spending, \ by group", DIST)],
                           box_w=2.6, box_h=1.1, font_size=19, buff=0.5).move_to(UP * 1.6)
        ax = plane([-0.5, 4.5], [0, 1.4], center=DOWN * 1.6 + LEFT * 1.2, x_length=7.6, y_length=2.6, xticks=[],
                   yticks=[0, 0.6, 1.2], ylabel=r"\%", yfmt=lambda v: f"{v:.1f}", font_size=13)
        bars = VGroup()
        for i, r in enumerate(rows):
            p0, p1 = ax.ax.c2p(i - 0.3, 0), ax.ax.c2p(i + 0.3, r["total"])
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=FIFTHS[i],
                               fill_opacity=0.85).move_to((p0 + p1) / 2))
        names = VGroup(*[label(t, font_size=15, color=FIFTHS[i]).next_to(ax.ax.c2p(i, 0), DOWN, buff=0.15)
                         for i, t in enumerate((r"poorest", r"second", r"middle", r"fourth", r"richest"))])
        side = label(r"the Play it, \\ as a central bank \\ would report it", font_size=19, color=E.ACCENT).next_to(
            ax, RIGHT, buff=0.6)
        with self.voiceover(
            "A distributional analysis has a fixed shape. <bookmark mark='a'/> Take a policy; <bookmark mark='b'/> "
            "work out the paths of interest rates, wages and taxes it produces in equilibrium; <bookmark mark='c'/> "
            "feed those paths to every household's rule; <bookmark mark='d'/> and add up the changes by group. "
            "<bookmark mark='e'/> The Play it of chapter five was exactly this, for a rate cut, by fifth of wealth. "
            "The answers depend on the model's liquidity and its fiscal rule, so a careful analysis reports them "
            "beside its assumptions."
        ) as vo:
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                an = [FadeIn(chain.boxes[k], shift=UP * 0.1)]
                if k > 0:
                    an.append(Create(chain.arrows[k - 1]))
                self.play(*an)
            vo.wait_until("e")
            self.play(FadeIn(ax), FadeIn(names), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2),
                      FadeIn(side), run_time=2.0)
        self.clear_scene()

    def called(self):
        c = calls.CALLS["krusell_smith_1998"]
        K = load("ks")
        Hk = load("hank")
        row = next(r for r in Hk["rows"] if r["liquid"] == Hk["island"])
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17)
        cc.move_to(UP * 1.2)
        nums = VGroup(
            label(rf"capital, \ chapter seven: \ $R^2$ = {K['r2'][1]:.6f}", font_size=21, color=RULE),
            label(rf"spending after a rate cut, \ chapter nine: \ {100 * (1 - row['share_impact']):.0f}\% through "
                  r"incomes, \ which a single household cannot have", font_size=21, color=INDIRECT),
        ).arrange(DOWN, buff=0.35).next_to(cc, DOWN, buff=0.6)
        tag = published_tag(r"Krusell and Smith (1998); \ Kaplan, \ Moll and Violante (2018)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In October 1998 Per Krusell and Anthony Smith wrote that in their "
            "economy the macroeconomic aggregates could be almost perfectly described using only the mean of the "
            "wealth distribution. <bookmark mark='b'/> For capital, it has held up, in their economy and many "
            "others; chapter seven reproduced it. <bookmark mark='c'/> But it was read, for twenty years, as "
            "permission to ignore the distribution altogether. Where many households have little liquid wealth, "
            "spending and the transmission of policy depend on who holds what, as chapters five and nine showed. "
            "<bookmark mark='d'/> The verdict: partly right. Right about capital, and right about the economy they "
            "studied; not a licence to forget the households who do the spending."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(cc.left, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(nums[0]))
            vo.wait_until("c")
            self.play(FadeIn(cc.right), FadeIn(nums[1]))
            vo.wait_until("d")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
