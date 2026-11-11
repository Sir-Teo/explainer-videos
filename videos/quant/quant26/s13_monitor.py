from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import BAD, GOOD, HURDLE, IS_C, NOISE, OOS_C, PART, RULE, ask, illustration, load


def _years(ym):
    ym = np.asarray(ym)
    return ym // 100 + (ym % 100 - 0.5) / 12


class Monitor(VoiceoverScene):
    def construct(self):
        m = load("monitor")
        self.card()
        self.peeking()
        self.bet()
        self.example(m["examples"]["flagged"], BAD)
        self.example(m["examples"]["kept"], GOOD)
        self.zoo(m)
        self.question()

    def card(self):
        c = chapter_card(12, r"Retrospective monitoring diagnostics", r"What null makes a betting guarantee valid?",
                         lit=(2016,), part=PART)
        with self.voiceover("Chapter twelve. Betting monitors and retrospective diagnostics. We examine what the original paths show, and the stronger bounded-process assumptions needed for an anytime guarantee."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def peeking(self):
        cards=VGroup(
            desk_question(r"repeated fixed-horizon tests",r"repeated nominal 5\% tests can inflate the probability of at least one false rejection; the amount depends on their joint law",width=12.2,font_size=20),
            desk_question(r"a prespecified decision process",r"fix the claim, data, scaling, bets and error budget using available information; do not reinterpret a fitted historical path as a prospectively calibrated test",width=12.2,font_size=20),
            desk_question(r"testing by betting",r"a valid nonnegative supermartingale starting at one obeys Ville's bound at $1/\alpha$ under its own null; the theorem does not establish that a proposed financial null is valid",width=12.2,font_size=20),
        ).arrange(DOWN,buff=.25)
        with self.voiceover("Repeated looks require a decision process. <bookmark mark='a'/> Reusing a nominal five-percent fixed-horizon test can inflate the chance of at least one false rejection. Its exact size depends on dependence between looks. <bookmark mark='b'/> Fix the claim, data, scaling, betting choices and error budget from available information. A fitted historical path does not automatically become a prospectively calibrated test. <bookmark mark='c'/> Testing by betting gives a useful theorem: a valid nonnegative supermartingale starting at one obeys Ville's bound. We must separately justify why its null holds for the financial increments.") as vo:
            for k,mk in enumerate(('a','b','c')):
                if k:vo.wait_until(mk)
                self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def bet(self):
        rows=[cmath(r"x_t",r"=",r"\operatorname{clip}\!\left({m-r_t\over4\hat\sigma},-.99,.99\right)",font_size=35,colors={r"x_t":RULE}),
              cmath(r"H_0^{\rm clipped}",r":",r"\mathbb E[x_t\mid\mathcal F_{t-1}]\le0",font_size=36,colors={r"H_0^{\rm clipped}":BAD}),
              cmath(r"E_t",r"=",r"{1\over K}\sum_{j=1}^K\prod_{s\le t}(1+\lambda_jx_s),\quad0\le\lambda_j<1",font_size=33,colors={r"E_t":HURDLE}),
              cmath(r"\Pr_{H_0^{\rm clipped}}(\sup_t E_t\ge20)",r"\le",r"1/20",font_size=36,colors={r"\Pr_{H_0^{\rm clipped}}(\sup_t E_t\ge20)":GOOD})]
        whys=[why(r"the unchanged implementation clips scaled shortfalls; target, scale and betting grid must be fixed using available past information"),
              why(r"this bounded conditional-mean null is stronger than a claim about the raw return mean: nonlinear clipping need not preserve the sign of a mean"),
              why(r"under the stated clipped null, each positive predictable bet is a nonnegative supermartingale; their fixed mixture starts at one"),
              why(r"Ville's bound applies only under that valid process null; the retrospective raw-return examples below do not establish these assumptions")]
        step=ladder(self,rows,whys,keep=4,top=3.2,x=-.5,buff=.3,edge=6.9)
        with self.voiceover("The implementation and its necessary null must be distinguished. <bookmark mark='a'/> The original code clips the scaled shortfall between minus point nine nine and point nine nine. The target, scale and betting grid must be chosen from information already available. <bookmark mark='b'/> For the guarantee, the clipped increment must have conditional mean at most zero. A raw return mean above the target does not imply this after clipping. <bookmark mark='c'/> Under that bounded conditional null, every positive predictable bet is a nonnegative supermartingale; a fixed mixture starts at one. <bookmark mark='d'/> Ville bounds its chance of ever reaching twenty by five percent. Our retrospective raw-return examples do not verify this null, so their threshold counts remain diagnostics.") as vo:
            step(0);vo.wait_until('a');self.wait(.1);vo.wait_until('b');step(1);vo.wait_until('c');step(2);vo.wait_until('d');step(3)
        self.clear_scene()

    def example(self, ex, col):
        x = _years(ex["ym"])
        cum = np.asarray(ex["cum"])
        bt = ex["m_in"] * np.arange(1, len(cum) + 1)
        path = np.asarray(ex["path"])
        lo1, hi1 = float(min(cum.min(), bt.min(), 0) - 1), float(max(cum.max(), bt.max()) + 1)
        g1 = axes([x[0], x[-1]], [lo1, hi1], x_length=5.6, y_length=3.4, xlabel=r"after publication",
                  ylabel=r"cumulative return, \%", xticks=[], yticks=[0], font_size=13).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.4)
        ax1 = g1.ax
        l_bt = DashedLine(ax1.c2p(x[0], bt[0]), ax1.c2p(x[-1], bt[-1]), color=IS_C, stroke_width=2)
        l_cum = curve(ax1, x, cum, OOS_C, stroke_width=3)
        lo2 = min(-2.0, float(path.min()) - 0.15)
        hi2 = max(2.5, float(path.max()) + 0.3)
        g2 = axes([x[0], x[-1]], [lo2, hi2], x_length=5.4, y_length=3.4, xlabel=r"after publication",
                  ylabel=r"clipped diagnostic, $\log_{10} E_t$", xticks=[], yticks=[-2, 0, 2], font_size=13).to_edge(
            RIGHT, buff=0.5).shift(DOWN * 0.4)
        ax2 = g2.ax
        thr = DashedLine(ax2.c2p(x[0], np.log10(20)), ax2.c2p(x[-1], np.log10(20)), color=HURDLE, stroke_width=2)
        thr_l = label(r"20", font_size=14, color=HURDLE).next_to(ax2.c2p(x[-1], np.log10(20)), RIGHT, buff=0.08)
        l_e = curve(ax2, x, path, col, stroke_width=3)
        flag = None
        if ex.get("flag_full"):
            fy = ex["flag_full"] // 100 + (ex["flag_full"] % 100 - 0.5) / 12
            flag = Dot(ax2.c2p(fy, np.log10(20)), color=BAD, radius=0.08)
        name = ex["long"]
        head = VGroup(label(rf"{name}", font_size=26, color=col),
                      MathTex(rf"\text{{published}}\ {ex['year']},\ \ t = {ex['t_in']:.1f}\ \text{{in its paper's sample}}",
                              font_size=24, color=GREY_A)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.35)
        foot = MathTex(rf"\text{{backtest}}\ {ex['m_in']:.2f}\%\ \text{{a month}};\ \ \text{{after}}\ {ex['m_post']:.2f}\%"
                       rf"\ \text{{over}}\ {ex['n_post']}\ \text{{months}}", font_size=24).to_edge(DOWN, buff=0.65)
        flagged = flag is not None
        with self.voiceover(
            ("An originally selected flagged example from the published-predictor panel. <bookmark mark='a'/> The dashed curve extrapolates its estimated in-sample monthly mean; the solid curve adds the available postpublication returns. Their gap is a descriptive comparison in a later public data vintage. <bookmark mark='b'/> The original clipped-shortfall product crosses twenty. That is a threshold crossing of this fitted diagnostic, not proof of a raw-return decline with a certified five-percent error rate. The target is estimated and selected, and the required clipped conditional-mean null has not been established.") if flagged else ("An originally selected unflagged example from the same published-predictor panel. <bookmark mark='a'/> Its available postpublication cumulative return is compared with an extrapolation of its in-sample mean. This is a retrospective comparison in a later public vintage. <bookmark mark='b'/> The original clipped diagnostic does not cross twenty. Non-crossing does not prove that a return promise is true, establish equivalence, or certify future performance. Both examples were selected after their historical paths were available.")
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), FadeIn(g2), Create(thr), FadeIn(thr_l))
            vo.wait_until("a")
            self.play(Create(l_bt), Create(l_cum), FadeIn(foot), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(l_e), run_time=2.5)
            if flag is not None:
                self.play(FadeIn(flag, scale=1.5))
        self.add(illustration(r"Open Source Asset Pricing 2024.10; the House's \texttt{martingale.EProcess}"))
        self.wait(0.4)
        self.clear_scene()

    def zoo(self,m):
        f,h=m['full'],m['half'];yrs=np.asarray(f['years_to_flag'])
        rows=VGroup(
            MathTex(rf"{m['n']}\ \text{{published predictors; retrospective clipped diagnostics through 2020}}",font_size=26),
            MathTex(rf"\text{{original full target}}:\ {f['flagged']}\ \text{{ever crossed 20}};\ {f['ebh']}\ \text{{terminal e-BH rule}}",font_size=27,color=BAD),
            MathTex(rf"\text{{original half target}}:\ {h['flagged']}\ \text{{ever crossed 20}};\ {h['ebh']}\ \text{{terminal e-BH rule}}",font_size=27,color=HURDLE),
            MathTex(rf"\text{{median publication-year to flag-year difference}}:\ {np.median(yrs):.0f}\ \text{{years}}",font_size=25,color=GREY_A),
        ).arrange(DOWN,buff=.35).shift(UP*.5)
        foot=wrapped_label(r"Counts are unchanged descriptive outputs, not certified raw-return discoveries. Terminal e-BH controls expected FDR under arbitrary dependence only when its inputs are valid unit-mean-bounded e-values under their nulls. Clipping, selected estimated targets and retrospective data do not establish this validity; running maxima are not substituted for terminal e-values.",12,18,GREY_A).to_edge(DOWN,buff=.4)
        with self.voiceover("The original whole-panel calculations remain visible. <bookmark mark='a'/> These are published predictors with positive estimated in-sample means. The first row counts full-target diagnostic paths that ever cross twenty and the terminal e-BH rule's selections. <bookmark mark='b'/> The second row uses half the fitted target. The time summary is a difference of calendar years, among flagged cases, not a universal speed of evidence. <bookmark mark='c'/> Terminal e-BH can control expected false-discovery rate under any cross-predictor dependence if its inputs are valid e-values under their stated nulls. The fitted clipped paths here do not establish those premises for raw-return claims. Published-universe selection, revised histories and estimated targets remain material limitations.") as vo:
            self.play(FadeIn(rows[0]));vo.wait_until('a');self.play(FadeIn(rows[1]));vo.wait_until('b');self.play(FadeIn(rows[2]),FadeIn(rows[3]));vo.wait_until('c');self.play(FadeIn(foot))
        self.clear_scene()

    def question(self):
        q=ask(r"A separately justified valid e-process stands at 12. Can a chosen threshold of 10 retain a 5\% anytime error bound? What bound follows from Ville at 10?")
        with self.voiceover("Pause and predict. In a separate mathematical example, a valid e-process stands at twelve. A colleague wants to lower the threshold from twenty to ten. That cannot retain the original five-percent anytime bound. Ville gives a ten-percent bound at ten. Restarting monitors also requires justified claims and an overall error budget; it is not a source of free repeated five-percent tests."):
            self.play(FadeIn(q))
        self.clear_scene()
