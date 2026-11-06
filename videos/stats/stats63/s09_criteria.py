from __future__ import annotations

import numpy as np

from videos.stats.stats63.common import *  # noqa: F403


class Criteria(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter eight. Fairness criteria: three conditional independences.", 8,
                            r"Fairness criteria", r"Independence, \ separation, \ sufficiency", lit=(2016,))
        self.setup_()
        self.three()
        self.data()
        self.table()
        self.calibration()
        self.pairs()

    def setup_(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The setting: a score R, computed from a person's features, used to predict an outcome "
            "Y, for people who belong to groups A. <bookmark mark='b'/> In COMPAS, R is a decile score from one to ten, Y "
            "is rearrest within two years, and A is race. <bookmark mark='c'/> Solon Barocas, Moritz Hardt and Arvind "
            "Narayanan organize the many proposed definitions into three families, each a conditional independence, the "
            "language of Part five. <bookmark mark='d'/> Leaving race out of the features does not settle anything, "
            "because the other features carry information about it: we saw how few facts identify a person.",
            [(r"R", r":", r"\text{a score}, \ \ Y: \text{the outcome}, \ \ A: \text{the group}", 40),
             (r"\text{COMPAS}", r":", r"\text{decile } 1\text{--}10, \ \text{rearrest in 2 years}, \ \text{race}", 38),
             (r"\text{three families}", r":", r"\text{conditional independences}", 40),
             (r"\text{dropping } A", r":", r"\text{not enough}", 40)],
            [r"the notation", r"ProPublica's data", r"Barocas, \ Hardt \& Narayanan", r"proxies, \ as in the hook"],
            colors=[(3, BADC)])

    def three(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Independence: the score does not depend on the group. The same share of each group is "
            "rated high risk. Also called demographic parity. <bookmark mark='b'/> Separation: the score is independent of "
            "the group given the outcome. Among people who were not rearrested, the same share of each group was rated high "
            "risk: equal false positive rates, and likewise equal false negative rates. Moritz Hardt, Eric Price and Nathan "
            "Srebro called it equalized odds, in 2016. <bookmark mark='c'/> Sufficiency: the outcome is independent of the "
            "group given the score. A score of seven means the same chance of rearrest in every group: calibration within "
            "groups. <bookmark mark='d'/> Each sounds like fairness. Each is a statement a statistician can test.",
            [(r"\text{independence}", r":", r"R \perp A", 40),
             (r"\text{separation}", r":", r"R \perp A \mid Y", 40),
             (r"\text{sufficiency}", r":", r"Y \perp A \mid R", 40),
             (r"\text{each}", r":", r"\text{testable}", 40)],
            [r"demographic parity", r"equalized odds: \ Hardt, \ Price \& Srebro (2016)", r"calibration within groups", r"Part 14's tables"],
            colors=[(0, GRPA), (1, GRPB), (2, S.ACCENT)])

    def data(self):
        d = load("compas")
        self.lad_voiceover(
            f"<bookmark mark='a'/> The data. In 2016 Julia Angwin, Jeff Larson, Surya Mattu and Lauren Kirchner of "
            f"ProPublica obtained COMPAS scores for defendants in Broward County, Florida, in 2013 and 2014, and matched "
            f"them to criminal records over the following two years. <bookmark mark='b'/> After their published filters, "
            f"{d['n_all']:,} defendants remain; the Museum keeps their age, sex, race, number of prior offences, decile "
            f"score and outcome, with names removed. <bookmark mark='c'/> {d['n']:,} are Black or white, the comparison "
            f"ProPublica made. <bookmark mark='d'/> Following ProPublica, a decile of five or more counts as labelled high "
            f"risk.",
            [(r"\text{ProPublica}", r":", r"\text{Broward County, \ 2013--14}", 40),
             (r"\text{after filters}", r":", rf"{d['n_all']:,} \ \text{{defendants}}".replace(",", "{,}"), 40),
             (r"\text{Black or white}", r":", rf"{d['n']:,}".replace(",", "{,}"), 40),
             (r"\text{high risk}", r":", r"\text{decile} \ge 5", 40)],
            [r"Angwin et al. (2016)", r"the Museum", r"the comparison", r"their threshold"])

    def table(self):
        d = load("compas")
        r = d["rates"]
        B, W = r["Black"], r["white"]
        head = [r"", r"Black", r"white"]
        rows = [head,
                [r"defendants", rf"{B['n']:,}".replace(",", "{,}"), rf"{W['n']:,}".replace(",", "{,}")],
                [r"rearrested (base rate)", rf"{B['base']:.3f}", rf"{W['base']:.3f}"],
                [r"labelled high risk", rf"{B['high']:.3f}", rf"{W['high']:.3f}"],
                [r"false positive rate", rf"{B['fpr']:.3f}", rf"{W['fpr']:.3f}"],
                [r"false negative rate", rf"{B['fnr']:.3f}", rf"{W['fnr']:.3f}"],
                [r"PPV: \ rearrested if high", rf"{B['ppv']:.3f}", rf"{W['ppv']:.3f}"]]
        t = table_rows(rows, font_size=34, col_buff=1.0, row_buff=0.34)
        for k in (1, 2):
            t[0][k].set_color(GRPA if k == 1 else GRPB)
        t.move_to([-1.9, -0.1, 0])
        side = side_groups([
            [(r"independence fails:", GRPA), (r"0.58 vs 0.33 high", GRPA)],
            [(r"separation fails:", GRPB), (r"FPR 0.42 vs 0.22", GRPB), (r"FNR 0.28 vs 0.50", GRPB)],
            [(r"PPV close:", S.ACCENT), (r"0.65 vs 0.59", S.ACCENT)],
        ], pos=(4.7, -0.1, 0), font_size=26, width=3.6)
        with self.voiceover(
            f"<bookmark mark='a'/> The rates, by group. <bookmark mark='b'/> {100 * B['base']:.0f} percent of Black "
            f"defendants and {100 * W['base']:.0f} percent of white defendants were rearrested: the base rates differ. "
            f"{100 * B['high']:.0f} and {100 * W['high']:.0f} percent were labelled high risk, so independence fails. "
            f"<bookmark mark='c'/> Among those not rearrested, {100 * B['fpr']:.0f} percent of Black defendants were "
            f"labelled high risk, against {100 * W['fpr']:.0f} percent of white defendants: false positive rates nearly two "
            f"to one. Among those rearrested, the false negative rates run the other way, {100 * B['fnr']:.0f} against "
            f"{100 * W['fnr']:.0f} percent. Separation fails, ProPublica's finding. <bookmark mark='d'/> But among those "
            f"labelled high risk, {100 * B['ppv']:.0f} and {100 * W['ppv']:.0f} percent were rearrested: similar positive "
            f"predictive values, the company's reply."
        ) as vo:
            self.play(FadeIn(t[0]), FadeIn(t[1]), FadeIn(museum_tag(r"ProPublica's COMPAS data (the Museum)")))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(t[2]), FadeIn(t[3]), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(t[4]), FadeIn(t[5]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(t[6]), FadeIn(side[2]))
        self.wait(1.0)
        self.clear_scene()

    def calibration(self):
        d = load("compas")
        cal = d["cal"]
        xs = np.arange(1, 11)
        A = axes([0.5, 10.5], [0, 1], x_length=7.2, y_length=4.3, xlabel=r"COMPAS decile score",
                 ylabel=r"fraction rearrested within two years", xticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], yticks=[0, 0.25, 0.5, 0.75, 1],
                 center=[-2.4, 0.2, 0])
        ax = A.ax

        def line(g, color, dx):
            ys = cal[g]["rate"]
            ns = cal[g]["n"]
            dots = VGroup(*[Dot(ax.c2p(x + dx, y), radius=0.04 + 0.06 * np.sqrt(n / 605), color=color, fill_opacity=0.9)
                            for x, y, n in zip(xs, ys, ns)])
            return VGroup(polyline(ax, xs + dx, ys, color, 3), dots)
        b, w = line("Black", GRPA, -0.08), line("white", GRPB, 0.08)
        side = side_groups([
            [(r"orange: \ Black defendants", GRPA), (r"teal: \ white defendants", GRPB), (r"dot area: \ defendants per decile", GREY_A)],
            [(r"the curves nearly coincide:", S.ACCENT), (r"roughly calibrated within groups", S.ACCENT)],
            [(r"but the deciles are filled differently:", GREY_A), (rf"decile 10: \ {cal['Black']['n'][-1]} vs {cal['white']['n'][-1]}", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> Sufficiency, decile by decile: the fraction rearrested at each score, for each group, "
            f"with dots sized by the number of defendants. <bookmark mark='b'/> The two curves nearly coincide: the score "
            f"is roughly calibrated within groups, as Northpointe said, and as the criminologists Anthony Flores, Kristin "
            f"Bechtel and Christopher Lowenkamp also found. <bookmark mark='c'/> What differs is how the deciles are filled. "
            f"{cal['Black']['n'][-1]} Black defendants received a ten, against {cal['white']['n'][-1]} white defendants, "
            f"and most white defendants are in the lowest deciles. Same meaning of each score; different distributions of "
            f"scores; and so, as the next chapter proves, different error rates."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"ProPublica's COMPAS data (the Museum)")))
            vo.wait_until("a")
            self.play(Create(b[0]), FadeIn(b[1]), Create(w[0]), FadeIn(w[1]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Indicate(b[1][-1]), Indicate(w[1][-1]), FadeIn(side[2]))
        self.wait(1.0)
        self.clear_scene()

    def pairs(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Before COMPAS, a general fact: the criteria conflict in pairs. <bookmark mark='b'/> "
            "Independence and sufficiency cannot both hold if the group and the outcome are dependent, because a calibrated "
            "score must then track the different base rates. <bookmark mark='c'/> Independence and separation cannot both "
            "hold for a binary score when the base rates differ, unless the score is useless, independent of the outcome. "
            "<bookmark mark='d'/> And separation and sufficiency cannot both hold when the base rates differ, unless the "
            "prediction is perfect. That last one is the COMPAS dispute, and the next chapter proves it with one line of "
            "algebra.",
            [(r"\text{independence + sufficiency}", r":", r"\text{need } A \perp Y", 40),
             (r"\text{independence + separation}", r":", r"\text{need a useless score}", 40),
             (r"\text{separation + sufficiency}", r":", r"\text{need equal base rates, \ or perfection}", 40),
             (r"\text{COMPAS}", r":", r"\text{the third conflict}", 40)],
            [r"base rates", r"binary $R$", r"chapter 9", r"the dispute"],
            colors=[(2, BADC)])
