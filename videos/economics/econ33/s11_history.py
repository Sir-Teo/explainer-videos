from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403


class History(VoiceoverScene):
    def construct(self):
        card(self, 9, r"A hundred and fifty years, \ eighteen countries", r"Do credit booms predict crises?",
             "Chapter nine. A hundred and fifty years, eighteen countries.",
             lit={2012: r"Schularick and Taylor", 2013: r"Jord\`a, \ Schularick and Taylor"},
             scale=("nation", "world"), horizon=("a decade", "a century"))
        self.odds()
        self.predictor()
        self.recessions()

    def odds(self):
        P = load("panel")
        O = P["odds"]
        ax = plane([0.4, 7.6], [0, 0.42], center=LEFT * 1.6 + DOWN * 0.4, x_length=9.0, y_length=4.6,
                   xticks=[], yticks=[0, 0.1, 0.2, 0.3, 0.4], ylabel=r"chance of a crisis within three years",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        vals = O["by_quintile"] + [O["neither"], O["both"]]
        names = [r"lowest \\ fifth", r"2nd", r"3rd", r"4th", r"highest \\ fifth", r"neither \\ booming",
                 r"credit and \\ houses both \\ in top fifth"]
        cols = [interpolate_color(ManimColor(CALM), ManimColor(CRISIS), k / 4) for k in range(5)] + [CALM, CRISIS]
        bars, labs, nms = VGroup(), VGroup(), VGroup()
        for k, (v, n, c) in enumerate(zip(vals, names, cols)):
            x = k + 1 if k < 5 else k + 1.4
            p0, p1 = ax.ax.c2p(x - 0.35, 0), ax.ax.c2p(x + 0.35, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=c, fill_opacity=0.85,
                               stroke_width=0).move_to((p0 + p1) / 2))
            labs.add(label(rf"{100 * v:.0f}\%", font_size=18, color=c).next_to(bars[-1], UP, buff=0.06))
            nms.add(wrapped_label(n, 1.3, 14, GREY_A).next_to(ax.ax.c2p(x, 0), DOWN, buff=0.12))
        k1 = label(r"the rise in bank loans to GDP over the past three years, \ by fifths", font_size=17,
                   color=CREDIT).next_to(ax, UP, buff=0.12)
        side = VGroup(
            label(rf"{P['countries']} countries, \ {P['first']}--{P['last']}, \\ war years left out", font_size=18,
                  color=GREY_A),
            label(r"Greenwood, \ Hanson, \ Shleifer \\ and S\o rensen (2022), \\ 42 countries since 1950: \\ "
                  r"about 40\% after booms \\ in credit and asset prices, \\ 7\% otherwise", font_size=18,
                  color=HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.25)
        tag = data_tag(r"Jord\`a, \ Schularick and Taylor, \ Macrohistory Database R6; \ this film", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Is there a pattern in the numbers, or only in the stories? Moritz Schularick and Alan Taylor, later "
            "with Oscar Jorda, assembled bank lending, house prices and the dates of banking crises for eighteen "
            f"rich countries back to 1870. <bookmark mark='a'/> Here are their data, {P['crises_all']} crises in "
            "all. Sort every peacetime year by how much bank lending rose relative to GDP over the "
            "three years before, and count how often a crisis started within the next three. In the fifth with the "
            f"slowest credit growth, {100 * O['by_quintile'][0]:.0f} percent. In the fifth with the fastest, "
            f"{100 * O['by_quintile'][-1]:.0f} percent. <bookmark mark='b'/> When house prices were booming as "
            f"well, {100 * O['both']:.0f} percent; when neither was, {100 * O['neither']:.0f}. "
            "<bookmark mark='c'/> Robin Greenwood, Samuel Hanson, Andrei Shleifer and Jakob Sorensen found nearly "
            "the same in forty-two countries since 1950: about forty percent after booms in credit and asset "
            "prices, seven percent otherwise. Crises are not bolts from the blue."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(k1), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[k], DOWN), FadeIn(labs[k]), FadeIn(nms[k]))
                                    for k in range(5)], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(*[AnimationGroup(GrowFromEdge(bars[k], DOWN), FadeIn(labs[k]), FadeIn(nms[k]))
                        for k in (5, 6)])
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def predictor(self):
        P = load("panel")
        RL, CG = P["real_loans"], P["credit_gdp"]
        ax = plane([0, 1], [0, 1], center=LEFT * 3.0 + DOWN * 0.4, x_length=4.8, y_length=4.8,
                   xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], xlabel=r"calm years flagged", ylabel=r"crises caught",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        diag = seg(ax, 0, 0, 1, 1, GREY_C, 1.5, dashed=True)
        r_in = path(ax, RL["roc_in"]["fpr"], RL["roc_in"]["tpr"], CREDIT, 3.2, smooth=False)
        r_oos = path(ax, RL["roc_oos"]["fpr"], RL["roc_oos"]["tpr"], CRISIS, 3.2, smooth=False)
        r_cg = path(ax, CG["roc_oos"]["fpr"], CG["roc_oos"]["tpr"], HOUSE, 3.2, smooth=False)
        side = VGroup(
            label(r"a logit: \ the chance of a crisis next year \\ from bank-loan growth in each of the \\ five years "
                  r"before, \ with country effects", font_size=19, color=WHITE),
            label(rf"purple: \ in sample, \ 1870--2020: \ AUC {RL['auc_in']:.2f}", font_size=19, color=CREDIT),
            label(rf"red: \ out of sample, \ each year from 1950 \\ predicted by a model fitted on the years "
                  rf"before: \\ AUC {RL['auc_oos']:.2f} \ ({RL['crises_oos']} crises)", font_size=19, color=CRISIS),
            label(rf"gold: \ the five-year rise in loans to GDP, \\ out of sample: \ AUC {CG['auc_oos']:.2f}",
                  font_size=19, color=HOUSE),
            label(r"but I tried two measures and kept the better: \\ that choice flatters it", font_size=18,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Jord\`a, \ Schularick and Taylor, \ Macrohistory Database R6; \ after Schularick and Taylor, "
                       r"\ \emph{AER} 102(2) (2012)", corner=DR, font_size=12)
        with self.voiceover(
            "Can that be turned into a forecast? Schularick and Taylor's model predicts a crisis next year from the "
            "growth of bank lending in each of the five years before. <bookmark mark='a'/> Fitted on all the data, "
            "this curve shows how many crises it catches against how many calm years it raises false alarms in. A "
            "useless model lies on the diagonal; the area under the curve is the chance it ranks a crisis year "
            f"above a calm one. In sample, {RL['auc_in']:.2f}. <bookmark mark='b'/> But a forecaster in 1990 did "
            "not have the data from after 1990. Refit the model each year on the years before it, and predict the "
            f"next: since 1950, the area falls to {RL['auc_oos']:.2f}, barely better than a coin. "
            "<bookmark mark='c'/> A simpler measure does better: the rise in lending relative to GDP over five "
            f"years, out of sample, {CG['auc_oos']:.2f}. <bookmark mark='d'/> A warning about that number: I tried "
            "two measures and am showing you the better one, which flatters it. Credit booms raise the odds of a "
            "crisis several times over. But most booms do not end in crises, and the timing is hard."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(diag), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(r_in), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(r_oos), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(r_cg), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def recessions(self):
        R = load("recessions")
        post = R["post"]
        h = np.array(post["h"])
        ax = plane([0, 6], [-6, 11], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.6, y_length=4.6,
                   xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[-5, 0, 5, 10], xlabel=r"years after the peak",
                   ylabel=r"real GDP per head, \ \% of the peak", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=14)
        zero = seg(ax, 0, 0, 6, 0, GREY_C, 1.2)
        res = {}
        for k, c in (("normal", CALM), ("financial", CRISIS)):
            m, se = np.array(post[k]), np.array(post[f"se_{k}"])
            res[k] = (band(ax, h, m - 1.96 * se, m + 1.96 * se, c, 0.18), path(ax, h, m, c, 3.5, smooth=False))
        side = VGroup(
            label(rf"teal: \ {post['n_normal']} normal recessions \\ since 1948", font_size=19, color=CALM),
            label(rf"red: \ {post['n_financial']} with a banking crisis \\ within two years of the peak",
                  font_size=19, color=CRISIS),
            label(rf"five years on: \ {post['normal'][5]:+.1f}\% \\ against {post['financial'][5]:+.1f}\%",
                  font_size=21, color=WHITE),
            label(rf"since 1870 the gap is smaller: \\ {R['gap5_all']:.1f} points", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Jord\`a, \ Schularick and Taylor, \ Macrohistory Database R6; \ after Jord\`a, \ Schularick "
                       r"and Taylor, \ \emph{JMCB} 45(s2) (2013)", corner=DR, font_size=12)
        with self.voiceover(
            "There is a second regularity, and it is about cost. <bookmark mark='a'/> Take every business-cycle "
            "peak in these countries since 1948, and follow real GDP per head for six years. After a normal "
            "recession, output dips, and in two years it is back above the peak. <bookmark mark='b'/> After a "
            "recession that comes with a banking crisis, it falls further and stays down. <bookmark mark='c'/> "
            f"Five years on, the normal recession has left output {post['normal'][5]:.1f} percent above its old "
            f"peak; the financial one, {post['financial'][5]:.1f}. The bands show the uncertainty in each average. "
            "<bookmark mark='d'/> Over the whole period since 1870 the gap is smaller, about "
            f"{R['gap5_all']:.0f} points, and Jorda, Schularick and Taylor found that within each kind, the bigger "
            "the credit boom before, the deeper the recession after."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(res["normal"][0]), Create(res["normal"][1]), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(res["financial"][0]), Create(res["financial"][1]), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
