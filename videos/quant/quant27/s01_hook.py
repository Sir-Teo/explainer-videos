from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import (BAD, COIN, COMPLEX, GOOD, HURDLE, LINEAR, MOM, NET, PART, TREE, era_strip,
                                         fit_right, illustration, load)


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.headline()
        self.paradox(load("snr"))
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Machine Learning for Returns")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty-seven. Machine learning for returns: what models with thousands or millions of parameters can "
            "learn from prices, what they cannot, and how to tell the difference."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def headline(self):
        head=label(r"Gu, Kelly and Xiu (2020): reported stock results",font_size=34,color=QC.FIRM).to_edge(UP,buff=.35)
        body=wrapped_label(r"About 30{,}000 U.S. stocks and 94 characteristics. Published monthly forecasts and gross long-short portfolios; this lecture does not replicate that stock experiment.",11.8,29).next_to(head,DOWN,buff=.55)
        stats=VGroup(*[definition_card(title,MathTex(value,font_size=44,color=QC.FIRM),width=3.8,font_size=26) for title,value in [(r"monthly OOS $R^2$",r"0.33\%\text{--}0.40\%"),(r"market-cap-weighted SR",r"1.35"),(r"equal-weighted SR",r"2.45")]]).arrange(RIGHT,buff=.35).move_to(DOWN*.3)
        foot=wrapped_label(r"Author-reported historical results, not an attainable-return promise. Zero-benchmark predictive $R^2$ is not literally a variance fraction. Source: official paper, Review of Financial Studies 33 (2020).",11.8,26,GREY_A).to_edge(DOWN,buff=.45)
        with self.voiceover("Gu, Kelly and Xiu's twenty twenty stock study used roughly thirty thousand companies and ninety-four characteristics. <bookmark mark='a'/> The paper reports monthly out-of-sample R squared around point three three to point four zero percent, against a zero forecast. This is not literally a fraction of variance explained. <bookmark mark='b'/> Its best neural-network portfolio has historical gross Sharpe ratios of one point three five with market-cap weights and two point four five with equal weights. These are the authors' stock results, not our crypto illustration, and not attainable-return promises.") as vo:
            self.play(FadeIn(head),FadeIn(body),FadeIn(foot))
            vo.wait_until("a");self.play(FadeIn(stats[0]))
            vo.wait_until("b");self.play(FadeIn(stats[1:]))
        self.clear_scene()

    def paradox(self,s):
        r2=np.asarray(s["r2"])*100
        ymax=float(max(max(s["single"]),*(max(v) for v in s["breadth"].values())))
        top=5*np.ceil(ymax/5)
        g=axes([0,5],[0,top],x_length=7.2,y_length=4.6,xlabel=r"population $R^2$, \% in the stated model",ylabel=r"idealised annual sign-strategy Sharpe",xticks=[0,1,2,3,4,5],yticks=list(np.arange(0,top+1,5)),font_size=14).to_edge(LEFT,buff=.5).shift(DOWN*.4)
        lines=[curve(g.ax,r2,s["single"],MOM,stroke_width=3)]
        for n,col in [("10",TREE),("100",NET),("1000",COMPLEX)]: lines.append(curve(g.ax,r2,s["breadth"][n],col,stroke_width=3))
        leg=legend([(MOM,r"one independent bet"),(TREE,r"10"),(NET,r"100"),(COMPLEX,r"1{,}000")],font_size=17)
        model=wrapped_label(r"Fixed idealisation: $S=\pm1$ equally likely, $r=aS+\varepsilon$, independent mean-zero noise with variance $\sigma^2$. Forecast $aS$; position $S$.",4.4,21,GREY_A)
        eq=MathTex(r"SR_n=\sqrt{12nR^2/(1-R^2)}",font_size=26,color=MOM)
        caution=wrapped_label(r"Population formula for this model. Arbitrary measured out-of-sample $R^2$ does not determine a tradable Sharpe ratio.",4.4,21,HURDLE)
        side=VGroup(model,eq,leg,caution).arrange(DOWN,aligned_edge=LEFT,buff=.28).to_edge(RIGHT,buff=.25)
        with self.voiceover(f"Use an explicit idealisation. A symmetric binary signal determines the conditional mean, with independent residual noise. Position by its sign. <bookmark mark='a'/> In this model, population R squared maps to the displayed annual Sharpe formula. One percent gives {s['sr_at_1pct']:.3f} for one bet. <bookmark mark='b'/> Independent equal-risk bets multiply it by the square root of their number. All saved curves are shown across their full range. Dependence, estimation, constraints and costs change the calculation. An arbitrary measured out-of-sample R squared alone does not determine a portfolio's attainable Sharpe ratio.") as vo:
            self.play(FadeIn(g),FadeIn(model),FadeIn(caution))
            vo.wait_until("a");self.play(Create(lines[0]),FadeIn(eq))
            vo.wait_until("b");self.play(*[Create(line) for line in lines[1:]],FadeIn(leg))
        self.clear_scene()

    def history(self):
        head=label(r"Tools, finance applications and current questions",font_size=34).to_edge(UP,buff=.4)
        items=[(r"1986--2017: core tools",r"1986: backpropagation\\1996: lasso\\2001: forests and boosting\\2007: random features\\2012: deep vision\\2017: transformers"),(r"2018--2020: finance",r"2018: practitioner toolkit\\2019: double descent\\2020: stock model zoo"),(r"2021--2025: directions",r"Conditional autoencoders\\Chart images\\Complexity and critiques\\Adversarial pricing\\Set models and market pretraining")]
        cards=VGroup(*[definition_card(title,Tex(body,font_size=25),width=4.0,font_size=25) for title,body in items]).arrange(RIGHT,buff=.3,aligned_edge=UP).move_to(DOWN*.25)
        with self.voiceover("The tools are older than the finance. Backpropagation was popularised in 1986; the lasso came in 1996; random forests and gradient boosting in 2001; random features in 2007; and in 2012 deep networks began winning at images, and in 2017 the transformer arrived. <bookmark mark='a'/> Marcos Lopez de Prado's practitioner's toolkit appeared in 2018, double descent was named in 2019, and in 2020 Gu, Kelly and Xiu brought the whole repertoire to the cross-section of stock returns. <bookmark mark='b'/> Since then: autoencoders, images of price charts, models with more parameters than observations, adversarial discount factors and transformers across assets; and, in 2025, a forceful critique and the first foundation models trained on market data.") as vo:
            self.play(FadeIn(head),FadeIn(cards[0]))
            vo.wait_until("a");self.play(FadeIn(cards[1]))
            vo.wait_until("b");self.play(FadeIn(cards[2]))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Why returns are a low signal-to-noise problem, and what that does to every model",
            r"The crypto model zoo: linear, trees, networks; data and execution limitations",
            r"The virtue of complexity, double descent, and the critique that reread them",
            r"For the researcher: Marchenko--Pastur and proportional-limit Gaussian ridge risk",
            r"Autoencoders, adversarial SDFs, attention across assets, images of prices",
            r"A pocket foundation model; the practitioner's toolkit; conformal intervals",
            r"Dated public firm records; registration and fair evaluation without sealed scores",
        ], color=QC.IDEA)
        with self.voiceover(
            'The plan is to examine weak return signals, a smaller crypto model illustration and its data limitations, random-feature complexity and its critics, and Gaussian proportional-limit risk. Then come autoencoders, discount-factor portfolios, attention, chart images, foundation-model protocols, practitioner tools and conformal assumptions. Public firm records illustrate governance. The registration chapter explains existing metadata and fair comparisons while leaving the panel and sealed experiment originals excluded.'
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("research",))
        with self.voiceover(
            'The research desk gains a model shop and an audit of what its examples support. The unchanged originals retain simplified training, period and calibration conventions. We explain those limitations, compare information sets and baselines, and preserve existing registrations. No new market trial is registered and no sealed experiment is opened or scored.'
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
