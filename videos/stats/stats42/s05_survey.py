from __future__ import annotations

import numpy as np

from videos.stats.stats42.common import *  # noqa: F403

POS = {"A": (-3.6, 1.6), "D": (-1.2, 2.3), "I": (1.2, 2.3), "B": (3.6, 1.6), "T": (-2.6, -0.6), "K": (0.0, -0.6),
       "Y": (2.6, -0.6), "V": (0.0, -2.3)}
EDGES = [("A", "T"), ("A", "Y"), ("A", "D"), ("B", "T"), ("B", "Y"), ("B", "D"), ("I", "T"), ("I", "Y"), ("D", "T"), ("D", "Y"),
         ("T", "K"), ("K", "Y"), ("T", "V"), ("Y", "V")]
NAMES = {"A": r"age \ (and sex)", "B": r"BMI", "I": r"income", "D": r"told: \ high pressure", "T": r"uses the substitute",
         "K": r"potassium", "Y": r"pressure", "V": r"clinic visit"}


def graph(center=(-2.4, 0.1, 0), scale=0.78):
    cols = {"T": USERC, "Y": CASE2, "K": S.PRIOR, "V": S.RESID}
    return CausalGraph(POS, EDGES, center=center, scale=scale, font_size=26, radius=0.34, colors=cols)


class SurveyGraph(VoiceoverScene):
    def construct(self):
        self.card()
        self.naive()
        self.users()
        self.dag()
        self.backdoor()
        self.bad_controls()
        self.numbers()

    def card(self):
        card = chapter_card(4, r"Case 2: \ the survey and its graph", r"Users have higher pressure: \ so what?", part=PART)
        with self.voiceover("Chapter four. The second case: an observational survey, and the graph that has to come before any estimate."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def naive(self):
        o = load("obs")
        r = o["res"]["naive"]
        A = axes([80, 180], [0, 0.03], x_length=7.4, y_length=4.4, xlabel=r"systolic pressure, \ mm Hg", ylabel=r"density",
                 xticks=[80, 100, 120, 140, 160, 180], yticks=[0, 0.01, 0.02, 0.03], center=[-2.5, 0.2, 0])
        ax = A.ax
        M = World().ministry
        y, t = np.asarray(M["sbp"]), np.asarray(M["uptake"], bool)
        bins = np.linspace(80, 180, 41)
        c, w = (bins[:-1] + bins[1:]) / 2, bins[1] - bins[0]
        hu, _ = np.histogram(y[t], bins=bins, density=True)
        hn, _ = np.histogram(y[~t], bins=bins, density=True)
        cn = bars_at(ax, c, np.minimum(hn, 0.03), w, GREY_B, opacity=0.45)
        cu = bars_at(ax, c, np.minimum(hu, 0.03), w, USERC, opacity=0.55)
        mu = DashedLine(ax.c2p(o["y_mean_users"], 0), ax.c2p(o["y_mean_users"], 0.027), color=USERC, stroke_width=2.5)
        mn = DashedLine(ax.c2p(o["y_mean_non"], 0), ax.c2p(o["y_mean_non"], 0.027), color=GREY_B, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(rf"{o['n']:,} adults; \ {o['n_users']} use the substitute", font_size=24),
            label(rf"users: \ mean {o['y_mean_users']:.1f} mm Hg", font_size=24, color=USERC),
            label(rf"non-users: \ mean {o['y_mean_non']:.1f}", font_size=24, color=GREY_A),
            label(rf"difference: \ $+{r[0]:.1f}$ \ [{r[2]:.1f}, \ {r[3]:.1f}]", font_size=26, color=NAIVEC),
            label(r"``Salt substitute raises blood pressure''", font_size=22, color=GREY_B),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The ministry's survey reached {o['n']:,} adults a year after the substitute went on sale; "
            f"{o['n_users']} of them use it. <bookmark mark='b'/> Their mean pressure is {say(o['y_mean_users'], 1)}, "
            f"<bookmark mark='c'/> against {say(o['y_mean_non'], 1)} for everyone else. <bookmark mark='d'/> A difference of "
            f"{say(r[0], 1)} millimetres, with a ninety percent interval from {say(r[2], 1)} to {say(r[3], 1)}: far from zero, "
            f"and in the wrong direction. <bookmark mark='e'/> The headline writes itself. Our job is to ask what the "
            f"difference means."
        ) as vo:
            self.play(FadeIn(A), FadeIn(survey_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(cu), Create(mu), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(cn), Create(mn), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def users(self):
        o = load("obs")
        rows = [[r"", r"users", r"non-users", r"SMD"]]
        fmt = {"age": "{:.1f}", "male": "{:.0%}", "BMI": "{:.1f}", "log income": "{:.2f}", "told high": "{:.0%}"}
        for (nm, a, b), smd in zip(o["table"], o["smd_raw"]):
            rows.append([nm, fmt[nm].format(a).replace("%", r"\%"), fmt[nm].format(b).replace("%", r"\%"), f"{smd:+.2f}"])
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.22).move_to([0, 0.6, 0])
        msg = fit_rows(VGroup(
            label(r"users are older and heavier, \ and three times as likely to have been told their pressure is high", font_size=26, color=USERC),
            label(r"confounding by indication: \ the people at risk are the ones who switched", font_size=26, color=S.ACCENT),
        ), 12.4, 0.3, [0, -2.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Who are the users? Compare them with everyone else. They are older, by about "
            f"{o['table'][0][1] - o['table'][0][2]:.0f} years; heavier; slightly richer; <bookmark mark='b'/> and "
            f"{100 * o['table'][4][1]:.0f} percent of them had been told by a doctor that their pressure was high, against "
            f"{100 * o['table'][4][2]:.0f} percent of non-users. The standardized differences in the last column are far "
            f"beyond the tenth that Part thirty-six called balanced. <bookmark mark='c'/> This is confounding by indication: "
            f"the substitute was taken up by exactly the people whose pressure was already high, often on their doctor's "
            f"advice. The raw comparison mixes the substitute's effect with the reason for using it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(msg[0]))
            vo.wait_until("c")
            self.play(FadeIn(msg[1]))
        self.clear_scene()

    def dag(self):
        G = graph()
        legend = fit_rows(VGroup(*[label(rf"${k}$: \ {v}", font_size=24, color=GREY_A if k not in "TYKV" else
                                         {"T": USERC, "Y": CASE2, "K": S.PRIOR, "V": S.RESID}[k]) for k, v in NAMES.items()]),
                          4.6, 0.32, [4.6, 0.2, 0])
        common = [n for n in "ABID"]
        with self.voiceover(
            "<bookmark mark='a'/> Before any estimate, a graph, written from what is known about blood pressure rather than "
            "read off the data. <bookmark mark='b'/> Age and sex, BMI and income each affect both whether someone switches "
            "and their pressure. Age and BMI also make a diagnosis of high pressure likelier, and the diagnosis affects both "
            "switching and pressure, through medicines and advice. <bookmark mark='c'/> The substitute works through "
            "potassium: users excrete thirty millimoles a day more, and potassium lowers pressure. <bookmark mark='d'/> And "
            "the survey also recorded whether each person visited a clinic this year, which both switching and high pressure "
            "make likelier."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(G.node("T")), FadeIn(G.node("Y")), FadeIn(legend[4]), FadeIn(legend[6]))
            vo.wait_until("b")
            self.play(*[FadeIn(G.node(n)) for n in common], *[GrowArrow(G.arrows[e]) for e in EDGES if e[0] in common],
                      *[FadeIn(legend[i]) for i in range(4)])
            vo.wait_until("c")
            self.play(FadeIn(G.node("K")), GrowArrow(G.arrows[("T", "K")]), GrowArrow(G.arrows[("K", "Y")]), FadeIn(legend[5]))
            vo.wait_until("d")
            self.play(FadeIn(G.node("V")), GrowArrow(G.arrows[("T", "V")]), GrowArrow(G.arrows[("Y", "V")]), FadeIn(legend[7]))
        self.wait(1.0)
        self.clear_scene()

    def backdoor(self):
        G = graph()
        p1 = G.path(["T", "D", "Y"], S.ACCENT)
        p2 = G.path(["T", "A", "D", "Y"], S.ACCENT)
        p3 = G.path(["T", "I", "Y"], S.ACCENT)
        box = G.condition(["A", "B", "I", "D"], GOODC)
        side = fit_rows(VGroup(
            label(r"back-door paths into $T$:", font_size=24),
            label(r"$T \leftarrow D \rightarrow Y$", font_size=26, color=S.ACCENT),
            label(r"$T \leftarrow A \rightarrow D \rightarrow Y$, \ $T \leftarrow I \rightarrow Y$, \ ...", font_size=24, color=S.ACCENT),
            label(r"adjust for $\{A, B, I, D\}$: \ every one blocked", font_size=24, color=GOODC),
            label(r"none of them is caused by $T$", font_size=24, color=GOODC),
        ), 4.6, 0.42, [4.6, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The back-door criterion of Part thirty-six finds the adjustment set. Every path that enters "
            "the substitute through an arrowhead is a back door. <bookmark mark='b'/> Switching, back to diagnosis, forward to "
            "pressure. <bookmark mark='c'/> Switching, back to age, through diagnosis, to pressure; switching, back to income, "
            "to pressure; and so on. <bookmark mark='d'/> Conditioning on age and sex, BMI, income and diagnosis blocks every "
            "one, <bookmark mark='e'/> and none of those is a descendant of switching, so the set satisfies the criterion: the "
            "effect is identified, if the graph is right."
        ) as vo:
            self.play(FadeIn(G))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(p1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeOut(p1), FadeIn(p2), FadeIn(p3), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeOut(p2), FadeOut(p3), Create(box), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def bad_controls(self):
        G = graph()
        med = G.path(["T", "K", "Y"], S.PRIOR)
        col = G.path(["T", "V", "Y"], S.RESID)
        bk = G.condition(["K"], S.PRIOR)
        bv = G.condition(["V"], S.RESID)
        side = fit_rows(VGroup(
            label(r"$K$, \ a mediator: \ adjusting removes the effect itself", font_size=24, color=S.PRIOR),
            label(r"$V$, \ a collider: \ adjusting opens $T \rightarrow V \leftarrow Y$", font_size=24, color=S.RESID),
            label(r"among visitors, \ users with low pressure are over-represented", font_size=22, color=GREY_A),
            label(r"more data is not always better: \ more \emph{variables} can be worse", font_size=24, color=S.ACCENT),
        ), 4.6, 0.42, [4.6, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The graph also says what not to adjust for, and the survey offers two tempting variables. "
            "Potassium lies on the causal path: adjusting for it compares users and non-users with the same potassium, which "
            "asks what the substitute does apart from its mechanism. The answer, nothing, is not the question. <bookmark "
            "mark='b'/> The clinic visit is a collider: both switching and high pressure cause it. Conditioning on it opens a "
            "path that was closed. <bookmark mark='c'/> Among people who visited a clinic, users had a reason to be there that "
            "non-users lacked, so the non-users who visited were the ones with high pressure, and the comparison is distorted. "
            "<bookmark mark='d'/> An exam answer that adjusts for everything in the data set fails here twice."
        ) as vo:
            self.play(FadeIn(G))
            vo.wait_until("a")
            self.play(FadeIn(med), Create(bk), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(col), Create(bv), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def numbers(self):
        o = load("obs")
        r = o["res"]
        items = [("naive", r"nothing: \ the raw difference", NAIVEC), ("regress", r"$\{A, B, I, D\}$", GOODC),
                 ("mediator", r"$\{A, B, I, D\} + K$", S.PRIOR), ("collider", r"$\{A, B, I, D\} + V$", S.RESID)]
        A = axes([-6, 9], [0, 4.5], x_length=7.4, y_length=4.4, xlabel=r"estimated effect of the substitute, \ mm Hg",
                 xticks=[-6, -3, 0, 3, 6, 9], yticks=[], center=[-2.5, 0.2, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 4.5), color=GREY_B, stroke_width=2)
        rowsg = VGroup()
        for i, (k, nm, c) in enumerate(items):
            yv = 4 - i
            est, _, lo, hi = r[k]
            rowsg.add(VGroup(Line(ax.c2p(lo, yv), ax.c2p(hi, yv), color=c, stroke_width=5), Dot(ax.c2p(est, yv), color=c, radius=0.09)))
        side = fit_rows(VGroup(*[label(rf"{nm}: \ ${r[k][0]:+.2f}$", font_size=24, color=c) for k, nm, c in items],
                               label(r"regressions on 40 imputed data sets, \ 90\% intervals", font_size=20, color=GREY_B)),
                        4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here are the four answers, each with a ninety percent interval. Adjusting for nothing, plus "
            f"{say(r['naive'][0], 1)}. <bookmark mark='b'/> Adjusting for the back-door set, minus {say(-r['regress'][0], 1)}: "
            f"the sign has flipped. <bookmark mark='c'/> Adding potassium, the mediator, the effect disappears: "
            f"{'plus' if r['mediator'][0] > 0 else 'minus'} {say(abs(r['mediator'][0]), 2)}. <bookmark mark='d'/> Adding the "
            f"clinic visit, the collider, it is exaggerated to minus {say(-r['collider'][0], 1)}. Three analyses of the same "
            f"survey, three different stories, and only the graph says which to believe. Income, meanwhile, is missing for "
            f"more than a third of the sample; these regressions used imputed values, which is the next chapter."
        ) as vo:
            self.play(FadeIn(A), FadeIn(zero), FadeIn(survey_tag()))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rowsg[k]), FadeIn(side[k]))
            self.play(FadeIn(side[4]))
        self.clear_scene()
