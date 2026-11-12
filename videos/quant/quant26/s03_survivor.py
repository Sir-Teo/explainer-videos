"""Survivorship mechanisms and fixed arithmetic; the unavailable SEC original is excluded."""
from __future__ import annotations
from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import BAD, GOOD, PART, ask

class Survivor(VoiceoverScene):
    def construct(self):
        self.card()
        self.fixed_outcomes()
        self.conditioning()
        self.delisting()
        self.data_protocol()
        self.question()

    def card(self):
        c=chapter_card(2,r"Survivorship and conditioning",r"Who is missing from the report?",lit=(1992,1997),part=PART)
        with self.voiceover("Chapter two. Survivorship and conditioning. A database can exclude closed funds, failed companies or abandoned strategies. We study the mechanism with fixed arithmetic. The original SEC snapshot comparison is unavailable because its recorded data hash does not match; no replacement historical result is generated."):
            self.play(FadeIn(c[0],shift=UP*.2),FadeIn(c[1]))
        self.play(FadeOut(c))

    def fixed_outcomes(self):
        head=label(r"Four fabricated one-year outcomes",font_size=32).to_edge(UP,buff=.4)
        vals=[-20,-10,10,20]
        g=axes([0,5],[-25,25],x_length=6.6,y_length=3.5,yticks=[-20,-10,0,10,20],yfmt=lambda v:rf"{v:+g}\%" if v else r"0\%",font_size=18).move_to(LEFT*2.3+UP*.55)
        ax=g.ax
        zero=Line(ax.c2p(0,0),ax.c2p(5,0),color=GREY_C,stroke_width=2)
        bars=VGroup(*[Polygon(ax.c2p(i+.62,0),ax.c2p(i+1.38,0),ax.c2p(i+1.38,v),ax.c2p(i+.62,v),stroke_width=0).set_fill(BAD if v<0 else GOOD,opacity=.85) for i,v in enumerate(vals)])
        names=VGroup(*[label(n,font_size=25).next_to(ax.c2p(i+1,0),UP if v<0 else DOWN,buff=.12) for i,(n,v) in enumerate(zip("ABCD",vals))])
        nums=VGroup(*[MathTex(rf"{v:+d}\%",font_size=22,color=BAD if v<0 else GOOD).next_to(bars[i],DOWN if v<0 else UP,buff=.06) for i,v in enumerate(vals)])
        key=VGroup(label(r"excluded by the chosen filter",font_size=21,color=BAD),label(r"retained",font_size=21,color=GOOD)).arrange(DOWN,aligned_edge=LEFT,buff=.25).next_to(g,RIGHT,buff=.7).shift(UP*.5)
        # the mean of whatever the report includes: a line across the bars, with its value at the right end
        mean=DashedLine(ax.c2p(.3,0),ax.c2p(4.7,0),color=WHITE,stroke_width=3,dash_length=.1)
        tag=MathTex(r"0\%",font_size=30).next_to(mean,RIGHT,buff=.12)
        all_mean=MathTex(r"\text{all four mean}=(-20-10+10+20)/4=0\%",font_size=27).to_edge(DOWN,buff=1.05)
        kept=MathTex(r"\text{retained mean}=(10+20)/2=15\%",font_size=27,color=GOOD).next_to(all_mean,DOWN,buff=.28)
        with self.voiceover("Here are four explicitly fabricated one-year outcomes: minus twenty, minus ten, plus ten and plus twenty percent. <bookmark mark='a'/> Their equally weighted arithmetic mean is zero. Now impose a reporting filter that retains only the two nonnegative outcomes. <bookmark mark='b'/> The reported mean becomes fifteen percent. Nothing about the four outcomes improved. Conditioning changed the group that appears in the report. This example is fixed arithmetic, not a market simulation, strategy backtest or estimate of an actual fund population.") as vo:
            self.play(FadeIn(head),FadeIn(g),FadeIn(zero),LaggedStart(*[GrowFromEdge(bars[i],UP if vals[i]<0 else DOWN) for i in range(4)],lag_ratio=.25),FadeIn(names))
            self.play(FadeIn(nums))
            vo.wait_until('a');self.play(Create(mean),FadeIn(tag),FadeIn(all_mean))
            vo.wait_until('b')
            self.play(bars[0].animate.set_fill(opacity=.18),bars[1].animate.set_fill(opacity=.18),nums[0].animate.set_opacity(.3),nums[1].animate.set_opacity(.3),FadeIn(key))
            up=DashedLine(ax.c2p(2.3,15),ax.c2p(4.7,15),color=GOOD,stroke_width=3,dash_length=.1)
            self.play(Transform(mean,up),Transform(tag,MathTex(r"15\%",font_size=30,color=GOOD).next_to(up,RIGHT,buff=.12)),FadeIn(kept))
        self.clear_scene()

    def conditioning(self):
        rows=[cmath(r"\mathbb E[r\mid S=1]",r"\ne",r"\mathbb E[r]\quad\text{in general}",font_size=37),
              cmath(r"\text{observed sample}",r"=",r"\text{outcomes selected by an inclusion rule}",font_size=32)]
        whys=[why(r"$S$ records inclusion. The direction and size of bias depend on its relation to outcomes; upward bias is not an unconditional mathematical law"),why(r"Brown, Goetzmann, Ibbotson and Ross (1992) study fund survivorship. Merger, closure, backfill and reporting rules require separate accounting")]
        step=ladder(self,rows,whys,keep=2,top=2.3,x=-.3,buff=.7,edge=6.8)
        with self.voiceover("The general lesson is conditional sampling. <bookmark mark='a'/> The return distribution among included records can differ from the distribution in the target population. The direction and size of that difference depend on the inclusion rule. Positive survivorship bias is not a universal identity. <bookmark mark='b'/> Fund closures, mergers, voluntary reporting, backfill and abandoned strategies can create different filters. Brown and coauthors studied fund survivorship in 1992. A historical universe must be defined using information available at the relevant date, with exits and identifier changes retained.") as vo:
            step(0);vo.wait_until('a');self.wait(.1);vo.wait_until('b');step(1)
        self.clear_scene()

    def delisting(self):
        eq=MathTex(r"1+r_{\rm combined}=(1+r_{\rm regular})(1+r_{\rm exit})",font_size=35).to_edge(UP,buff=.8)
        fixed=MathTex(r"(1+0.10)(1-0.50)-1=-0.45",font_size=41,color=BAD).next_to(eq,DOWN,buff=.65)
        foot=wrapped_label(r"Fixed arithmetic for compatible sequential return intervals. Check a provider's definitions to avoid omitted or double-counted exit returns. Missing does not automatically mean zero. Shumway (1997); Shumway and Warther (1999).",12,22,GREY_A).to_edge(DOWN,buff=.7)
        with self.voiceover("Exits also require return accounting. <bookmark mark='a'/> For compatible sequential intervals, compound a regular return and an exit return. In a fixed example, plus ten percent followed by minus fifty percent gives minus forty-five percent. Simply adding the two would give the wrong result. <bookmark mark='b'/> Provider definitions matter: do not omit an exit payment or count the same interval twice. A missing delisting return is not automatically zero. Shumway and later Shumway with Warther document why exit records matter; no delisting-return dataset is reconstructed here.") as vo:
            self.play(FadeIn(eq));vo.wait_until('a');self.play(FadeIn(fixed));vo.wait_until('b');self.play(FadeIn(foot))
        self.clear_scene()

    def data_protocol(self):
        cards=VGroup(
            desk_question(r"original SEC comparison unavailable",r"The current cached ticker file failed the protected recorded-source hash check. Original computation and failure log are preserved; its numerical output is not displayed.",width=12,font_size=21),
            desk_question(r"membership is not corporate survival",r"Even a matching later CIK/ticker snapshot would measure an intersection of reporting universes, with mergers, identifier changes and incomplete coverage.",width=12,font_size=21),
            desk_question(r"a historical-data protocol",r"Prespecify the universe clock; retain exits and closed records; document reporting/backfill rules and return definitions before estimating performance.",width=12,font_size=21),
        ).arrange(DOWN,buff=.28)
        with self.voiceover("The original SEC example remains blocked. <bookmark mark='a'/> Its public ticker snapshot fails the recorded-source hash check. The computation and error are preserved, and its unavailable numbers are withheld. The manifest is unchanged. <bookmark mark='b'/> Even with matching bytes, membership in a later ticker file would not be a literal corporate-survival rate. Public-float frames and bankruptcy-report searches select particular reporting universes. <bookmark mark='c'/> Define the historical universe clock, retain exits and closed records, and document backfill, identifiers and return definitions before estimating performance.") as vo:
            for i,mk in enumerate(('a','b','c')):
                if i:vo.wait_until(mk)
                self.play(FadeIn(cards[i],shift=UP*.2))
        self.clear_scene()

    def question(self):
        q=ask(r"The four fixed outcomes average 0\%, while the chosen retained pair averages 15\%. Does the higher reported mean establish manager skill? What population should the report describe?")
        with self.voiceover("Pause and predict. Four fixed outcomes average zero percent, while the selected retained pair averages fifteen percent. Does the higher reported mean establish manager skill? State the target population and identify the selection rule before interpreting the difference."):
            self.play(FadeIn(q))
        self.clear_scene()
