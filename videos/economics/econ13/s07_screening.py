from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403

CAREFUL = "#7BD88F"
CARELESS = "#F2A65A"


class Screening(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Screening: \ contracts that sort", r"If insurers can't tell the careful from the careless, \ can "
             r"they make them tell?", "Chapter six. Screening: contracts that sort.",
             lit={1976: r"Rothschild and Stiglitz"}, scale=("person", "firm", "market"), horizon=("a year",))
        self.menu()
        self.breaks()

    def menu(self):
        s = load("screen")
        xs = np.array(s["xs"])
        ax = plane([0, 62], [0, 26], center=LEFT * 3.1 + DOWN * 0.3, x_length=5.6, y_length=5.0,
                   xticks=[0, 12.57, 30, 60], yticks=[0, 1.26, 6, 12, 24], xlabel=r"cover, \ \$",
                   ylabel=r"premium, \ \$", font_size=16, xfmt=lambda v: f"{v:.1f}" if v % 1 else f"{v:.0f}",
                   yfmt=lambda v: f"{v:.2f}" if v % 1 else f"{v:.0f}")
        a = ax.ax
        fair_h = path(ax, xs, s["line_high"], color=CARELESS, width=2.5, smooth=False)
        fair_l = path(ax, xs, s["line_low"], color=CAREFUL, width=2.5, smooth=False)
        fhl = label(r"fair price for the careless", font_size=14, color=CARELESS).next_to(a.c2p(38, 16), LEFT,
                                                                                         buff=0.1)
        fll = label(r"for the careful", font_size=14, color=CAREFUL).next_to(a.c2p(50, 5), DOWN, buff=0.1)
        ic = path(ax, xs, s["ic_high"], color=CARELESS, width=2, yr=(0, 26))
        ic.set_stroke(opacity=0.6)
        H = Dot(a.c2p(s["x_high"], s["prem_high"]), radius=0.1, color=CARELESS)
        Lc = Dot(a.c2p(s["x_low"], s["prem_low"]), radius=0.1, color=CAREFUL)
        side = VGroup(
            label(rf"boat owners with \${s['W']:.0f}; \ a storm costs \${s['d']:.0f}; \\ careful ones lose with chance "
                  rf"{s['p_low']:.1f}, \ careless ones {s['p_high']:.1f}", font_size=20),
            label(r"Michael Rothschild and Joseph Stiglitz (1976): \\ insurers compete by offering a menu", font_size=20),
            label(rf"full cover at the careless price: \\ \${s['x_high']:.0f} of cover for \${s['prem_high']:.0f}",
                  font_size=21, color=CARELESS),
            label(rf"or a little cover at the careful price: \\ \${s['x_low']:.2f} for \${s['prem_low']:.2f}, \ no more, "
                  r"\\ or the careless would take it too", font_size=21, color=CAREFUL),
            label(r"each picks its own: \ the menu sorts them, \\ and the careful pay by going nearly uninsured",
                  font_size=21, color=EQ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Rothschild and Stiglitz, QJE 90(4) (1976); \ the numbers: \ Agora", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Signals are sent by the informed. Screens are set by the uninformed. <bookmark mark='a'/> The Island's "
            "boat owners each have a hundred dollars, and a storm would cost them sixty. Careful owners lose a boat "
            "with a chance of one in ten, careless ones four in ten, and insurers cannot tell which is which. "
            "<bookmark mark='b'/> In 1976 Michael Rothschild and Joseph Stiglitz showed how competing insurers would "
            "respond: with a menu. <bookmark mark='c'/> One contract offers full cover at the price that is fair for "
            "the careless: sixty dollars of cover for twenty-four. <bookmark mark='d'/> The other offers a little "
            "cover at the price fair for the careful: about twelve dollars and fifty-seven cents of cover for a dollar "
            "twenty-six. It can't offer more, or the careless would take it too; the faint curve is the careless "
            "owners' indifference, which passes through both contracts. <bookmark mark='e'/> Each owner picks the "
            "contract meant for them, so the menu sorts them. The careless are fully insured. The careful pay for "
            "being believed by going nearly uninsured."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(fair_h), Create(fair_l), FadeIn(fhl), FadeIn(fll), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(H, scale=1.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ic), FadeIn(Lc, scale=1.5), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def breaks(self):
        s = load("screen")
        lams = np.array(s["lams"])
        ok = s["exists_by_share"]
        line = NumberLine(x_range=[0, 1, 0.1], length=10.4, include_numbers=False, color=GREY_B).move_to(UP * 1.4)
        nums = VGroup(*[label(f"{100 * v:.0f}\\%", font_size=16, color=GREY_B).next_to(line.n2p(v), DOWN, buff=0.15)
                        for v in (0, 0.25, 0.5, 0.75, 1.0)])
        dots = VGroup(*[Dot(line.n2p(l_), radius=0.07, color=GOOD if o else LOSS) for l_, o in zip(lams, ok)])
        thr = VGroup(DashedLine(line.n2p(s["share_threshold"]) + DOWN * 0.35, line.n2p(s["share_threshold"]) + UP * 0.5,
                                color=WHITE, stroke_width=2),
                     label(rf"{100 * s['share_threshold']:.0f}\%", font_size=17).next_to(
                         line.n2p(s["share_threshold"]) + UP * 0.5, UP, buff=0.05))
        ll = label(r"share of careless owners \ (green: the menu is an equilibrium; \ red: no equilibrium)",
                   font_size=17, color=GREY_B).next_to(line, UP, buff=0.75)
        rows = VGroup(
            label(rf"a single pooled contract at the average price ({s['pbar']:.2f} a dollar of cover) \ can tempt "
                  r"the careful away from their meagre cover", font_size=22),
            label(r"if careless owners are rare, \ the average price is close to the careful one, \ and it does",
                  font_size=22, color=POOL),
            label(r"but a pool can't survive either: \ an insurer can always cream off the careful again", font_size=22,
                  color=GREY_A),
            label(r"so with few careless owners \ there is no equilibrium at all", font_size=24, color=LOSS),
            label(r"competitive insurance markets can be unstable: \ an argument for rules about what must be sold",
                  font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Rothschild and Stiglitz (1976); \ the existence check: \ Agora", corner=UR, font_size=13)
        with self.voiceover(
            "Rothschild and Stiglitz found a crack in their own result. <bookmark mark='a'/> An insurer could offer a "
            "single contract at the average price, nineteen cents for every dollar of cover, to everyone. That can "
            "tempt the careful away from their meagre cover. <bookmark mark='b'/> If careless owners are rare, the "
            "average price is close to the careful price, and it does. <bookmark mark='c'/> But a pooled contract "
            "can't last either, because a rival can always offer the careful a slightly different deal that the "
            "careless don't want, and take them away. <bookmark mark='d'/> So when careless owners make up less than "
            "about eleven percent, there is no equilibrium at all. <bookmark mark='e'/> Competitive insurance markets "
            "can be unstable, which is one argument for rules about what must be sold, and to whom."
        ) as vo:
            self.play(Create(line), FadeIn(nums), FadeIn(ll), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(thr), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
