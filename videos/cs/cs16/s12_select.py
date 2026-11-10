from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono,
                                   words)


class Select(VoiceoverScene):
    def construct(self):
        self.card()
        self.quickselect()
        self.mom()
        self.five()

    def card(self):
        card = chapter_card(11, r"Selection and the median of medians", r"Can we find the median without sorting?",
                            lit=(1973,), extra=((1973, r"Blum, Floyd, Pratt, Rivest and Tarjan"),), part=PART)
        with self.voiceover("Chapter eleven. Selection and the median of medians."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def quickselect(self):
        d = load("select")
        head = label(r"Quickselect: \ recurse on one side only", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"to find the $k$-th smallest: \ partition, \ then continue only where $k$ lies", font_size=22,
                  color=GREY_A),
            MathTex(r"\mathbb{E}[C] \le n + \tfrac34 n + (\tfrac34)^2 n + \cdots = 4n \quad\text{(a crude bound)}",
                    font_size=30),
            label(r"median, distinct keys: \ $\mathbb E[C_n]=(2+2\ln2)n+o(n)$ \ (leading term)", font_size=22,
                  color=YES),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.5)
        rows = [[words(r["n"]), words(round(r["quick"])), f"{r['quick'] / r['n']:.2f}", words(round(r["sort"]))]
                for r in d["rows"]]
        tab = grid_table([r"$n$", r"quickselect, \ mean", r"per element", r"sorting: \ $n \lg n$"], rows,
                         widths=[2.0, 3.2, 2.2, 3.0], row_h=0.44, font_size=19,
                         colors=[[WHITE, YES, YES, GREY_B]] * len(rows)).next_to(pts, DOWN, buff=0.4)
        with self.voiceover(
            (
            "Selection needs one rank, not every rank. <bookmark mark='a'/> Quickselect partitions around a pivot "
            "and continues only in the side containing the requested rank. Our count charges one logical "
            "partition comparison per nonpivot key. <bookmark mark='b'/> For distinct keys and a uniform pivot, "
            "the expected larger side is at most three quarters of the current size. Bounding the chosen side by "
            "that larger side gives a crude linear bound, about four n; it is an expectation argument, not a "
            "guaranteed shrink at each step. <bookmark mark='c'/> For the median, the leading expected term is "
            "two plus two natural log two, times n, with lower-order corrections. The finite sample means need "
            "not equal that asymptotic coefficient exactly."
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(Write(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]), FadeIn(tab))
        self.wait(0.3)
        self.clear_scene()

    def five(self):
        head = label(r"Why groups of five?", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(label(r"groups of 3", font_size=22, color=NO),
                   MathTex(r"T(n)\le T(n/3+O(1))+T(2n/3+O(1))+O(n)\;\Rightarrow\;O(n\log n)", font_size=28,
                           color=NO),
                   label(r"$\tfrac13+\tfrac23=1$: this elementary bound does not close with linear induction", font_size=19,
                         color=GREY_B)).arrange(DOWN, buff=0.1),
            VGroup(label(r"groups of 5", font_size=22, color=YES),
                   MathTex(r"T(n)\le T(n/5+O(1))+T(7n/10+O(1))+O(n)\;\Rightarrow\;O(n)", font_size=28, color=YES),
                   label(r"$\tfrac15 + \tfrac{7}{10} = \tfrac{9}{10}$: \ the levels shrink", font_size=19,
                         color=GREY_B)).arrange(DOWN, buff=0.1),
            VGroup(label(r"groups of 7", font_size=22, color=DATA),
                   MathTex(r"T(n)\le T(n/7+O(1))+T(5n/7+O(1))+O(n)\;\Rightarrow\;O(n)", font_size=28, color=DATA),
                   label(r"$\tfrac17 + \tfrac57 = \tfrac67$: \ also linear, \ larger constant per group", font_size=19,
                         color=GREY_B)).arrange(DOWN, buff=0.1),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.5)
        note = label(r"for these linear-toll recurrences: \ fractions summing below one give a linear upper bound",
                     font_size=21, color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            (
            "The group size changes what this proof can establish. <bookmark mark='a'/> With groups of three, the "
            "elementary upper-bound recurrence has fractions one third and two thirds. Their sum is one, giving "
            "an O of n log n bound by this argument. An upper-bound recurrence does not prove a matching lower "
            "bound for the algorithm. <bookmark mark='b'/> With five, one fifth plus seven tenths is less than "
            "one, so a linear toll gives a linear upper bound after accounting for rounding. <bookmark mark='c'/> "
            "Seven also gives a sum below one, with a different small-group cost. <bookmark mark='d'/> This "
            "shrinking-sum test applies to these linear-toll recurrences. It is not a universal characterization "
            "of all divide-and-conquer algorithms."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def mom(self):
        d=load("select")
        head=label(r"Median of medians: a pivot with protected ranks",font_size=32).to_edge(UP,buff=0.3)
        groups=[[1,2,5,17,22],[3,6,8,18,23],[4,9,13,19,24],[7,10,15,20,25],[11,12,16,21,26]]
        grid=VGroup();cells={}
        for col,values in enumerate(groups):
            for row,value in enumerate(values):
                box=RoundedRectangle(width=0.72,height=0.43,corner_radius=0.05,stroke_color=GREY_D,stroke_width=1.5,fill_color=BG,fill_opacity=1)
                text=mono(str(value),20,WHITE).move_to(box)
                cell=VGroup(box,text).move_to([-5.3+col*1.12,1.5-row*0.62,0]);grid.add(cell);cells[col,row]=cell
        title=label(r"five sorted groups of five distinct keys",font_size=20,color=GREY_A).next_to(grid,UP,buff=0.3)
        medians=VGroup(*[cells[c,2] for c in range(5)])
        pivot=SurroundingRectangle(cells[2,2],color=HEAD,buff=0.07,stroke_width=3)
        pl=label(r"pivot 13",font_size=20,color=HEAD).next_to(grid,DOWN,buff=0.25)
        counts=VGroup(label(r"9 protected keys $\le$ pivot",font_size=20,color=YES),
                      label(r"9 protected keys $\ge$ pivot",font_size=20,color=CTRL),
                      label(r"the pivot belongs to both counts",font_size=17,color=GREY_B)).arrange(DOWN,buff=0.12).next_to(pl,DOWN,buff=0.2)
        steps=VGroup(
            label(r"1. sort small groups; count actual comparisons",font_size=20,color=GREY_A),
            label(r"2. recursively select the median of group medians",font_size=20,color=DATA),
            VGroup(label(r"3. three keys per protected full group",font_size=20,color=YES),
                   label(r"exclude pivot/incomplete groups: $3n/10-O(1)$ per side",font_size=19,color=GREY_A)).arrange(DOWN,buff=0.1),
            MathTex(r"\begin{aligned}T(n)\le{}&T(\lceil n/5\rceil)\\&+T(7n/10+O(1))+cn\end{aligned}",font_size=29,color=HEAD),
            label(r"$1/5+7/10=9/10<1$: a linear upper bound closes",font_size=20,color=HEAD),
        ).arrange(DOWN,buff=0.3).move_to(RIGHT*3.0+UP*0.15)
        if steps.width>6.2:steps.scale_to_fit_width(6.2)
        r=d['rows'][-1]
        measured=label(rf"this implementation, $n={words(r['n'])}$: {r['mom']/r['n']:.2f} comparisons/key; quickselect sample mean {r['quick']/r['n']:.2f}",font_size=19,color=GREY_A).to_edge(DOWN,buff=0.3)
        with self.voiceover("We can guarantee linear worst-case work. <bookmark mark='a'/> Divide distinct keys into groups of five and sort each small group to find its median. Every less-than comparison in that routine is now counted. <bookmark mark='b'/> Recursively select the median of those medians as the pivot. In the picture, at least half the group medians lie on either side. <bookmark mark='c'/> Each such full group contributes three keys on the corresponding side, apart from the pivot group and a possible incomplete group. This gives three n over ten minus a constant protected on each side. <bookmark mark='d'/> The recurrence therefore uses a ceiling for the medians call and seven n over ten plus a constant for the remaining side. <bookmark mark='e'/> The fractions sum to nine tenths, so a sufficiently large linear bound closes by induction. The displayed finite implementation count is an example, not a universal comparison constant.") as vo:
            self.play(FadeIn(head),FadeIn(title))
            vo.wait_until("a")
            self.play(FadeIn(grid),FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(*[m[0].animate.set_stroke(DATA,3) for m in medians],Create(pivot),FadeIn(pl),FadeIn(steps[1]))
            vo.wait_until("c")
            protected=[]
            for col in range(5):
                for row in range(5):
                    if col<=2 and row<=2:protected.append(cells[col,row][0].animate.set_fill(YES,0.3))
                    elif col>=2 and row>=2:protected.append(cells[col,row][0].animate.set_fill(CTRL,0.3))
            self.play(*protected,FadeIn(counts),FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]),FadeIn(measured))
        self.wait(0.3);self.clear_scene()
