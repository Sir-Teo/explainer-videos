from __future__ import annotations

import numpy as np

from videos.stats.stats18.common import *  # noqa: F403
from videos.stats.stats18.compute import adults, digest_returns

BANDS = [r"under 20", r"20--30", r"30--50", r"50--100", r"over 100"]


class WhatWentWrong(VoiceoverScene):
    def construct(self):
        self.card()
        self.frame()
        self.nonresponse()
        self.decompose()
        self.squire()
        self.gallup()
        self.total_error()

    def card(self):
        card = chapter_card(1, r"What went wrong", r"Two biases, \ and neither shrinks", lit=(1936,), part=PART)
        with self.voiceover("Chapter one. What went wrong."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def by_income(self):
        P = adults()
        v, L = P["vote"], P["listed"]
        R = digest_returns(P)
        b = np.digitize(P["income"], [20, 30, 50, 100])
        out = []
        for k in range(5):
            m = b == k
            out.append((m.sum(), L[m].mean(), v[m].mean(), R[m].sum() / max(1, L[m].sum())))
        return out

    def frame(self):
        d = load("digest")
        rows_ = self.by_income()
        A = axes([-0.6, 4.6], [0, 0.8], x_length=7.4, y_length=4.0, xlabel=r"", ylabel=r"share",
                 yticks=[0, 0.2, 0.4, 0.6, 0.8], center=[-2.0, 0.3, 0])
        ax = A.ax
        w = ax.c2p(0.35, 0)[0] - ax.c2p(0, 0)[0]
        lb = VGroup(*[Rectangle(width=w, height=max(0.01, ax.c2p(0, r[1])[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=FRAME,
                                fill_opacity=0.85).move_to(ax.c2p(k - 0.19, 0), aligned_edge=DOWN) for k, r in enumerate(rows_)])
        vb = VGroup(*[Rectangle(width=w, height=max(0.01, ax.c2p(0, r[2])[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=BLUE,
                                fill_opacity=0.85).move_to(ax.c2p(k + 0.19, 0), aligned_edge=DOWN) for k, r in enumerate(rows_)])
        names = VGroup(*[label(t, font_size=18, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.15) for k, t in enumerate(BANDS)])
        names.add(label(r"income band, \ thousands", font_size=20, color=GREY_A).next_to(ax.c2p(2, 0), DOWN, buff=0.55))
        rows = fit_rows(VGroup(
            label(r"teal: \ share on the registers", font_size=22, color=FRAME),
            label(r"blue: \ share voting Blue", font_size=22, color=BLUE),
            MathTex(rf"\text{{median income: all}}\ {d['income_all']:.0f}\text{{k}};\ \text{{listed}}\ {d['income_listed']:.0f}\text{{k}}", font_size=24),
            MathTex(rf"\text{{Blue among the listed}}: {100 * d['blue_listed']:.1f}\%", font_size=26, color=OBS),
            MathTex(rf"\text{{frame bias}}: +{100 * d['frame_bias']:.1f}\ \text{{points}}", font_size=26, color=RES),
        ), 4.4, 0.38, [4.6, 0.3, 0])
        with self.voiceover(
            "The Digest made two separate mistakes. The first was its list. <bookmark mark='a'/> In 1936 a telephone or a car "
            "was a sign of money. On the World's registers, the share of adults listed rises steeply with income: seven percent "
            "of the poorest band, two thirds of the richest. <bookmark mark='b'/> And support for Blue rises with income too. "
            "<bookmark mark='c'/> So the listed are richer: a median income of fifty-six thousand against thirty-nine. "
            "<bookmark mark='d'/> Among them Blue has forty-six point eight percent, <bookmark mark='e'/> eight point six points "
            "above the truth. That's frame bias, or coverage bias: the list from which the sample is drawn isn't the "
            "population."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in lb], lag_ratio=0.15), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in vb], lag_ratio=0.15), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def nonresponse(self):
        d = load("digest")
        rows_ = self.by_income()
        A = axes([-0.6, 4.6], [0, 0.25], x_length=7.4, y_length=4.0, xlabel=r"",
                 ylabel=r"share of the listed who returned a ballot", yticks=[0, 0.1, 0.2], center=[-2.0, 0.3, 0])
        ax = A.ax
        w = ax.c2p(0.5, 0)[0] - ax.c2p(0, 0)[0]
        rb = VGroup(*[Rectangle(width=w, height=max(0.01, ax.c2p(0, r[3])[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=RESP,
                                fill_opacity=0.85).move_to(ax.c2p(k, 0), aligned_edge=DOWN) for k, r in enumerate(rows_)])
        names = VGroup(*[label(t, font_size=18, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.15) for k, t in enumerate(BANDS)])
        names.add(label(r"income band, \ thousands", font_size=20, color=GREY_A).next_to(ax.c2p(2, 0), DOWN, buff=0.55))
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{returned: \ }}{100 * d['return_rate']:.1f}\%\ \text{{of the listed}}", font_size=26, color=RESP),
            MathTex(rf"\text{{Blue voters}}: {100 * d['resp_blue']:.1f}\%\qquad \text{{Red}}: {100 * d['resp_red']:.1f}\%", font_size=26),
            label(r"the keen, \ the angry, \ the challenger's side", font_size=22, color=GREY_A),
            MathTex(rf"\text{{Blue among returns}}: {100 * d['blue_returns']:.1f}\%", font_size=26, color=OBS),
            MathTex(rf"\text{{nonresponse bias}}: +{100 * d['nonresp_bias']:.1f}\ \text{{points}}", font_size=26, color=RES),
        ), 4.4, 0.38, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The second mistake was who answered. Only one in six of the listed sent a ballot back, and "
            "the rate rises with income. <bookmark mark='b'/> More importantly, it depends on the vote itself: twenty-one "
            "percent of Blue voters returned their ballots, thirteen percent of Red voters. <bookmark mark='c'/> People "
            "eager for change, angry with the government, were keener to have their say. <bookmark mark='d'/> Among the "
            "returns, Blue has fifty-eight percent: <bookmark mark='e'/> another eleven point two points of bias, this time "
            "from nonresponse."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in rb], lag_ratio=0.15), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def decompose(self):
        d = load("digest")
        A = axes([0.3, 0.62], [0, 3], x_length=9.0, y_length=2.4, xlabel=r"Blue's share", xticks=[0.35, 0.4, 0.45, 0.5, 0.55, 0.6],
                 center=[0.4, 0.4, 0], xfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        pts = [(d["truth"], r"the World", HIT), (d["blue_listed"], r"the listed", FRAME), (d["blue_returns"], r"the returns", RESP)]
        dots = VGroup()
        for k, (v, nm, col) in enumerate(pts):
            dt = Dot(ax.c2p(v, 1.2), radius=0.12, color=col)
            dots.add(VGroup(dt, label(nm, font_size=20, color=col).next_to(dt, UP, buff=0.15)))
        a1 = Arrow(ax.c2p(d["truth"], 0.7), ax.c2p(d["blue_listed"], 0.7), buff=0.05, color=FRAME, stroke_width=4)
        a2 = Arrow(ax.c2p(d["blue_listed"], 0.7), ax.c2p(d["blue_returns"], 0.7), buff=0.05, color=RESP, stroke_width=4)
        l1 = MathTex(rf"+{100 * d['frame_bias']:.1f}", font_size=24, color=FRAME).next_to(a1, DOWN, buff=0.1)
        l2 = MathTex(rf"+{100 * d['nonresp_bias']:.1f}", font_size=24, color=RESP).next_to(a2, DOWN, buff=0.1)
        rows = fit_rows(VGroup(
            MathTex(r"\text{error} = \underbrace{(\bar y_{\text{frame}} - \bar y)}_{\text{coverage}} + "
                    r"\underbrace{(\bar y_{\text{resp}} - \bar y_{\text{frame}})}_{\text{nonresponse}}", font_size=30),
            label(r"mailing more ballots to the same list changes neither term", font_size=24, color=RES),
        ), 12.4, 0.35, [0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Put together: the World's truth, thirty-eight percent; the listed, forty-seven; the returns, "
            "fifty-eight. <bookmark mark='b'/> The error splits exactly into a coverage term, <bookmark mark='c'/> and a "
            "nonresponse term. <bookmark mark='d'/> And here's the crux: sending more ballots to the same list, or waiting for "
            "more returns, changes neither term. The Digest's two point four million ballots weren't a large random sample. "
            "They were a large, very particular one."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, scale=1.4) for x in dots], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(l1), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(GrowArrow(a2), FadeIn(l2))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def squire(self):
        d = load("digest")
        rows = fit_rows(VGroup(
            label(r"Squire (1988): \ a 1937 Gallup survey asked who had received, \ and who had returned, \ a Digest ballot", font_size=24),
            label(r"both the list and the response were biased toward Landon", font_size=24, color=RES),
            label(r"even those who \emph{received} a ballot favoured Roosevelt", font_size=24, color=BLUE),
            label(r"had they all replied, \ the Digest would at least have picked the winner", font_size=24, color=OBS),
            MathTex(rf"\text{{the World: \ the listed are }}{100 * d['blue_listed']:.1f}\%\ \text{{Blue, \ still a Red majority}}", font_size=26,
                    color=FRAME),
        ), 12.4, 0.48, [0, 0, 0])
        tag = historical_tag(r"P. Squire, \ \emph{Public Opinion Quarterly} 52 (1988)", corner=DR)
        with self.voiceover(
            "Was it really both? <bookmark mark='a'/> In 1988 Peverill Squire found a Gallup survey from May 1937 that had asked "
            "people whether they'd received a Digest ballot, and whether they'd sent it back. <bookmark mark='b'/> Both "
            "the list and the response had leaned toward Landon. <bookmark mark='c'/> But even among those who received "
            "a ballot, Roosevelt had a majority. <bookmark mark='d'/> So had everyone who was mailed a ballot replied, the Digest "
            "would at least have picked the winner. Nonresponse turned a poor sample into a disaster. "
            "<bookmark mark='e'/> The World tells the same story: its listed adults are forty-seven percent Blue, still a Red "
            "majority, and it's the returns that flip it."
        ) as vo:
            self.add(tag)
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def gallup(self):
        P = adults()
        v = P["vote"]
        g = np.random.Generator(np.random.PCG64(1936))
        L = np.flatnonzero(P["listed"])
        k = g.choice(L, 3000, replace=False)
        r = k[g.random(3000) < P["prop"][k]]
        rows = fit_rows(VGroup(
            label(r"July 1936: \ Gallup predicted the \emph{Digest}'s answer before it was published", font_size=24),
            label(r"mail 3,000 postcards to names from the same lists", font_size=22, color=GREY_A),
            label(r"Gallup's forecast of the \emph{Digest}: \ Landon 56\%; \ it printed 57\%", font_size=24, color=OBS),
            MathTex(rf"\text{{the World}}: 3{{,}}000 \text{{ listed}} \to {len(r)} \text{{ replies}} \to \text{{Blue}}\ {100 * v[r].mean():.1f}\%",
                    font_size=28, color=RESP),
            label(r"a bias, \ once understood, \ can be predicted: \ it isn't noise", font_size=24, color=HIT),
        ), 12.4, 0.45, [0, 0, 0])
        with self.voiceover(
            "There's a coda that shows the Digest's error was systematic, not bad luck. <bookmark mark='a'/> In July 1936, "
            "before the Digest had mailed a single ballot, George Gallup published a prediction of what it would find. "
            "<bookmark mark='b'/> He'd mailed three thousand postcards to people drawn from the same kinds of lists. "
            "<bookmark mark='c'/> He forecast that the Digest would show Landon with fifty-six percent; it printed fifty-seven. "
            "<bookmark mark='d'/> The World's version: three thousand names from the registers bring four hundred and eighty-nine "
            "replies, fifty-nine percent Blue, the Digest's answer in miniature. <bookmark mark='e'/> A bias, once understood, "
            "can be reproduced with a tiny sample. Making the sample bigger only makes it more precisely wrong."
        ) as vo:
            for k_, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k_], shift=RIGHT * 0.2))
        self.clear_scene()

    def total_error(self):
        rows = [
            cmath(r"\text{sampling error}", r":", r"\text{shrinks like } 1/\sqrt n", font_size=30),
            cmath(r"\text{coverage error}", r":", r"\text{the frame misses part of the population}", font_size=30),
            cmath(r"\text{nonresponse error}", r":", r"\text{who answers depends on the answer}", font_size=30),
            cmath(r"\text{measurement error}", r":", r"\text{wording, \ order, \ the interviewer}", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"the only one Parts 8--11 measured"), why(r"telephones in 1936; \ landlines today"),
                why(r"the Digest's fatal error"), why(r"Part 41: \ measurement error")]
        with self.voiceover(
            "Survey researchers call this the total survey error. <bookmark mark='a'/> Sampling error is the part our intervals "
            "measure, and the only part that shrinks with sample size. <bookmark mark='b'/> Coverage error comes from a frame "
            "that misses part of the population: telephones in 1936, landlines in the 2000s, the internet today. "
            "<bookmark mark='c'/> Nonresponse error arises when who answers depends on the answer. <bookmark mark='d'/> And "
            "measurement error comes from the questions themselves, their wording and order, and the interviewer; that's for "
            "Part 41. An interval of plus or minus three points speaks only for the first line."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
