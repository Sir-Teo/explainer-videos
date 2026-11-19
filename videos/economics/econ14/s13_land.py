from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403


class Land(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Sharecropping, \ and China's household responsibility system", r"Why give a tenant half "
             r"the crop, \ and what happened when China gave families all of it?",
             "Chapter eleven. Sharecropping, and China's household responsibility system.",
             lit={1890: r"Marshall", 1969: r"Cheung", 1974: r"Stiglitz", 1987: r"Shaban", 1992: r"Lin",
                  2002: r"Banerjee, Gertler and Ghatak"},
             scale=("person", "economy"), horizon=("a season", "a decade"))
        self.debate()
        self.curve()
        self.bengal()
        self.china()

    def debate(self):
        rows = VGroup(
            label(r"three ways to farm another's land:", font_size=27, color=E.ACCENT),
            label(r"for a wage: \ the landlord bears all the risk, \ the worker has no stake", font_size=23,
                  color=GREY_A),
            label(r"for a fixed rent: \ the tenant keeps every extra sack, \ and bears every bad year", font_size=23,
                  color=PAY),
            label(r"for a share of the crop, \ often half: \ in between", font_size=23, color=EFFORT),
            label(r"Alfred Marshall, \ 1890: \ a sharecropper keeps half of what extra work brings, \ so does too "
                  r"little", font_size=22, color=RISK),
            label(r"Steven Cheung, \ 1969: \ landlords watch, \ and write the effort into the contract", font_size=22,
                  color=SIGNAL),
            label(r"Joseph Stiglitz, \ 1974: \ the share is insurance, \ paid for with some of the effort", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.1)
        tag = published_tag(r"Marshall, Principles (1890); \ Cheung, The Theory of Share Tenancy (1969); \ Stiglitz, "
                            r"RES 41(2) (1974)", corner=DR, font_size=12)
        with self.voiceover(
            "The oldest incentive contract is on the land. <bookmark mark='a'/> There are three ways to farm someone "
            "else's land. <bookmark mark='b'/> For a wage, where the landlord bears all the risk and the worker has no "
            "stake in the crop. <bookmark mark='c'/> For a fixed rent, where the tenant keeps every extra sack, and "
            "bears every bad year. <bookmark mark='d'/> Or for a share of the crop, very often half, in between. "
            "Sharecropping has been common from ancient times to the American South to India today. "
            "<bookmark mark='e'/> Alfred Marshall argued in 1890 that it was wasteful: a sharecropper keeps only half "
            "of what extra work brings, and so does too little of it. <bookmark mark='f'/> Steven Cheung replied in "
            "1969 that landlords aren't fools. They watch, and write the effort they want into the contract. "
            "<bookmark mark='g'/> In 1974 Joseph Stiglitz gave the answer this part has been building: the share is "
            "insurance for the tenant, and it is paid for with some of the effort."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdefg", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def curve(self):
        sc = load("sharecrop")
        ss, sur = np.array(sc["s"]), np.array(sc["surplus"])
        ax = plane([0, 1], [0, 34], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.2, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 10, 20, 30], xlabel=r"the tenant's share of the crop",
                   ylabel=r"what the land yields the two, \\ less effort and risk", font_size=16,
                   xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        c = path(ax, ss, sur, color=EFFORT, width=3.5)
        dots = VGroup(
            Dot(a.c2p(0, sc["surplus_wage"]), radius=0.08, color=GREY_A),
            Dot(a.c2p(1, sc["surplus_rent"]), radius=0.08, color=PAY),
            Dot(a.c2p(sc["s_star"], sc["surplus_best"]), radius=0.1, color=E.ACCENT),
        )
        labs = VGroup(
            label(r"a wage", font_size=15, color=GREY_A).next_to(dots[0], UR, buff=0.08),
            label(r"a fixed rent", font_size=15, color=PAY).next_to(dots[1], LEFT, buff=0.12),
            label(rf"the best share: \ {sc['s_star']:.2f}", font_size=15, color=E.ACCENT).next_to(dots[2], UP,
                                                                                               buff=0.15),
        )
        side = VGroup(
            label(r"a wage: \ no stake, \ no effort", font_size=21, color=GREY_A),
            label(rf"a fixed rent: \ full effort, \\ but the tenant carries every bad year: \ {sc['surplus_rent']:.0f}",
                  font_size=21, color=PAY),
            label(rf"a share of {sc['s_star']:.2f}: \ {sc['surplus_best']:.1f}, \\ more than either", font_size=21,
                  color=E.ACCENT),
            label(r"Marshall's loss is real, \\ but it buys the tenant insurance", font_size=21, color=SIGNAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Stiglitz, RES 41(2) (1974); \ the curve: \ Agora", corner=DR, font_size=13)
        with self.voiceover(
            "It is the same model as Friday's grove, with a tenant and a landlord. <bookmark mark='a'/> On a wage, "
            "the tenant has no stake and makes no effort beyond what is watched. <bookmark mark='b'/> On a fixed "
            "rent, the tenant works as if the land were theirs, but carries every bad year, and must be compensated "
            "for it with a lower rent. <bookmark mark='c'/> In Agora, a share of sixty-one percent makes more for "
            "the two of them than either: thirty and a half, against eighteen for the rent. "
            "<bookmark mark='d'/> Marshall's loss of effort is real, but it buys insurance, and for a poor tenant who "
            "cannot survive a bad year, that is worth a great deal."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(c), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(dots[0]), FadeIn(labs[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots[1]), FadeIn(labs[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(dots[2], scale=1.5), FadeIn(labs[2]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def bengal(self):
        tn = tables.TENANCY.data
        c1 = study_card(r"Owned plots and sharecropped ones", r"Radwan Shaban, \ 1987", [
            (r"compared", r"the same households' own plots with the plots they sharecropped, in Indian villages"),
            (r"found", r"less output and fewer inputs on the sharecropped plots"),
        ], design="regression", width=6.2, font_size=21)
        c2 = study_card(r"Operation Barga, \ West Bengal", r"Banerjee, Gertler and Ghatak, \ 2002", [
            (r"the reform", r"from 1978, sharecroppers registered: secure tenure, and a floor on their share"),
            (r"found", rf"about {100 * tn['barga_share_of_growth']:.0f}\% of the state's later growth in farm "
                       r"productivity"),
        ], design="DiD", width=6.2, font_size=21)
        VGroup(c1, c2).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 0.6)
        foot = label(r"security and a larger share: \ more effort, \ and investment in the land", font_size=23,
                     color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Shaban, JPE 95(5) (1987); \ Banerjee, Gertler and Ghatak, JPE 110(2) (2002)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "What does the evidence say about Marshall? <bookmark mark='a'/> Radwan Shaban compared the same "
            "households' plots in Indian villages: the ones they owned and the ones they sharecropped. Same family, "
            "same skills, same weather. The sharecropped plots got fewer inputs and produced less. Marshall's loss "
            "is there. <bookmark mark='b'/> In 1978 the state of West Bengal began Operation Barga, which registered "
            "sharecroppers, gave them security of tenure, and set a floor on their share of the crop. Abhijit "
            "Banerjee, Paul Gertler and Maitreesh Ghatak estimated that it accounts for about twenty-eight percent "
            "of the state's later growth in farm productivity, though they can't separate its direct effects from "
            "the rest. <bookmark mark='c'/> A tenant who can't be evicted and keeps more of the crop works harder, "
            "and has a reason to improve the land."
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def china(self):
        rows = VGroup(
            label(r"Xiaogang's contract was a fixed rent: \ deliver the quota, \ keep the rest", font_size=24,
                  color=PAY),
            label(r"each family kept all of what its extra effort brought", font_size=24, color=EFFORT),
            label(r"by the early 1980s \ the household responsibility system covered almost all of rural China",
                  font_size=23, color=CHINA),
            label(r"Justin Yifu Lin, \ 1992: \ farm output grew fast from 1978 to 1984; \ about half of the growth "
                  r"came from the new contracts", font_size=22, color=E.ACCENT),
            label(r"the rest: \ higher prices paid by the state, \ more fertilizer, \ and more", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Lin, AER 82(1) (1992)", corner=DR, font_size=13)
        with self.voiceover(
            "Now back to Xiaogang. <bookmark mark='a'/> Its secret contract was, in these terms, a fixed rent: each "
            "family delivered its quota to the state and kept everything above it. <bookmark mark='b'/> So each "
            "family kept all of what its extra effort brought, not an eighteenth. The risk was real, but so was the "
            "hunger the old system had produced. <bookmark mark='c'/> The arrangement spread, first quietly, then "
            "with approval, and by the early 1980s the household responsibility system covered almost all of rural "
            "China. <bookmark mark='d'/> In 1992 Justin Yifu Lin measured what it did. Farm output grew fast from 1978 "
            "to 1984, and about half of that growth came from the change of contract. <bookmark mark='e'/> The rest "
            "came from the higher prices the state paid for grain, from more fertilizer, and from other changes. "
            "The intermission's line for China begins its climb from these years."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
