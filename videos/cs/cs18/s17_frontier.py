from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, draw_graph, grid_table, load,
                                   mono, words)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.dijkstra()
        self.barrier()
        self.flow()
        self.open_()

    def card(self):
        card = chapter_card(16, r"Research results: \ models and dates", r"Was Dijkstra the end of the story?",
                            lit=(2024,), extra=((2022, r"almost-linear max flow"), (2024, r"universal optimality"),
                                                (2025, r"the sorting barrier broken"), (2026, r"improved directed bound")), part=PART)
        with self.voiceover("Chapter sixteen. Selected research results, with their models and dates."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def dijkstra(self):
        head = label(r"Distance vector or distance order?",font_size=34).to_edge(UP,buff=.3)
        graph,_,_=draw_graph({'s':(-5.4,1.4),'a':(-3.6,2.3),'b':(-3.6,1.4),'c':(-3.6,.5)},
                            [('s','a'),('s','b'),('s','c')],directed=True,
                            weights={('s','a'):7,('s','b'):2,('s','c'):5})
        tab=grid_table([r"requested output",r"same distances, different order"],
                       [[r"distance vector",r"a: 7, b: 2, c: 5"],[r"distance ordering",r"b: 2, c: 5, a: 7"]],
                       widths=[2.8,4.5],row_h=.55,font_size=21,mono_cols=(),
                       colors=[[DATA,DATA],[HEAD,HEAD]]).move_to([2.2,1.45,0])
        steps=VGroup(
            label(r"standard Dijkstra also outputs a nondecreasing distance order",font_size=21,color=GREY_A),
            label(r"comparison lower bound: some graph families encode sorting; not every fixed graph",font_size=21,color=GREY_A),
            label(r"2024 universal optimality: fixed graph, worst arc lengths, distance-ordering task",font_size=21,color=YES),
            label(r"requires the specified working-set heap; our Python heap is an ordinary binary heap",font_size=21,color=LAM),
            label(r"distance-only algorithms have a different output requirement",font_size=22,color=HEAD),
        ).arrange(DOWN,buff=.2).move_to([0,-1.65,0])
        if steps.width>12.8:steps.scale_to_fit_width(12.8)
        with self.voiceover("First distinguish distance ordering from distance computation. <bookmark mark='a'/> Standard Dijkstra processes vertices in nondecreasing source distance, so its settlement order also sorts reachable distances. <bookmark mark='b'/> In the comparison model, some graph families encode a sorting problem; that is not a lower bound of n log n for every individual graph. <bookmark mark='c'/> Haeupler and colleagues' 2024 universal-optimality result concerns distance ordering on each fixed graph, compared against algorithms facing that graph's worst-case arc lengths in the specified model. <bookmark mark='d'/> It uses a heap with a working-set guarantee. Our ordinary Python binary heap is not an implementation of that specialized structure. <bookmark mark='e'/> Computing only the distances is a different output task, which is why the next results can improve sparse-graph bounds without contradicting this theorem.") as vo:
            self.play(FadeIn(head),FadeIn(graph))
            vo.wait_until('a');self.play(FadeIn(tab),FadeIn(steps[0]))
            for mark,line in zip('bcde',steps[1:]):
                vo.wait_until(mark);self.play(FadeIn(line))
        self.wait(.3);self.clear_scene()

    def barrier(self):
        head=label(r"Selected directed shortest-path bounds: 2025 and 2026",font_size=32).to_edge(UP,buff=.3)
        model=label(r"nonnegative real weights; deterministic; comparison-addition; distance-only output",
                    font_size=20,color=LAM).set_y(2.55)
        frame25=RoundedRectangle(width=12.4,height=1.05,corner_radius=.12,color=GREY_D,
                                 fill_color=BG,fill_opacity=1).set_y(1.55)
        name25=label(r"2025: Duan, Mao, Mao, Shu and Yin",font_size=21,color=DATA).move_to([-2.7,1.55,0])
        bound25=MathTex(r"O(m\log^{2/3}n)",font_size=34,color=YES).move_to([3.6,1.55,0])
        frame26=RoundedRectangle(width=12.4,height=1.6,corner_radius=.12,color=GREY_D,
                                 fill_color=BG,fill_opacity=1).set_y(-.05)
        name26=label(r"2026: Duan, Mao, Shu and Yin; ICALP",font_size=20,color=HEAD).set_y(.45)
        bound26=MathTex(r"O\!\left(m\sqrt{\log n}+\sqrt{mn\log n\log\log n}\right)",font_size=31,color=YES).set_y(-.05)
        sparse=MathTex(r"m=O(n):\quad O\!\left(m\sqrt{\log n\log\log n}\right)",font_size=27,color=HEAD).set_y(-.55)
        improved=VGroup(frame26,name26,bound26,sparse)
        idea=label(r"frontier reduction: limited relaxations plus selective ordering; research algorithms not implemented here",
                   font_size=19,color=GREY_A).set_y(-1.25)
        negative=VGroup(
            label(r"2022: Bernstein, Nanongkai and Wulff-Nilsen; randomized, integer weights",font_size=20,color=LAM),
            MathTex(r"O(m\log^8 n\log W)\qquad W:\text{ weight-magnitude parameter}",font_size=29,color=YES),
        ).arrange(DOWN,buff=.2).set_y(-2.4)
        with self.voiceover("These are selected dated results, not measurements of our city code. <bookmark mark='a'/> In 2025 Duan, Jiayi Mao, Xiao Mao, Shu and Yin gave a deterministic distance-only algorithm for directed graphs with nonnegative real weights. <bookmark mark='b'/> Its comparison-addition bound is m times log n to the two-thirds. <bookmark mark='c'/> A 2026 result by Duan, Xiao Mao, Shu and Yin improves the bound shown here; for sparse graphs it simplifies to m times the square root of log n times log log n. The bibliography identifies the ICALP publication and version. <bookmark mark='d'/> Frontier reduction combines limited relaxation with selective ordering. This episode does not implement either research algorithm. <bookmark mark='e'/> Negative weights need their own model: Bernstein, Nanongkai and Wulff-Nilsen's randomized result uses integer weights and includes a log W dependence, rather than covering arbitrary real weights at the same cost.") as vo:
            self.play(FadeIn(head),FadeIn(model),FadeIn(frame25),FadeIn(name25))
            vo.wait_until('a');self.play(Indicate(name25,color=DATA),run_time=.7)
            vo.wait_until('b');self.play(FadeIn(bound25))
            vo.wait_until('c');self.play(FadeIn(improved))
            vo.wait_until('d');self.play(FadeIn(idea))
            vo.wait_until('e');self.play(FadeIn(negative))
        self.wait(.3);self.clear_scene()

    def flow(self):
        head=label(r"An almost-linear flow theorem needs an input model",font_size=33).to_edge(UP,buff=.3)
        tab=grid_table([r"Chen et al., 2022",r"statement scope"],
                       [[r"problem",r"exact directed maximum flow and minimum-cost flow"],
                        [r"input",r"polynomially bounded integral capacities, costs and demands"],
                        [r"asymptotic time",r"$m^{1+o(1)}$ under the stated assumptions"]],
                       widths=[3.1,9.0],row_h=.55,font_size=22,mono_cols=(),
                       colors=[[GREY_A,YES],[GREY_A,HEAD],[GREY_A,YES]]).move_to(UP * 1.5)
        captions=[r"interior-point optimization",r"approximate minimum-ratio cycles",r"dynamic graph structures"]
        boxes=VGroup()
        for i,caption in enumerate(captions):
            frame=RoundedRectangle(width=3.55,height=1.0,corner_radius=.1,color=LAM,fill_color=BG,fill_opacity=1)
            text=label(caption,font_size=20,color=GREY_A)
            if text.width>3.2:text.scale_to_fit_width(3.2)
            boxes.add(VGroup(frame,text).move_to([-4.25+4.25*i,-.7,0]))
        arrows=VGroup(*[Arrow(boxes[i].get_right(),boxes[i+1].get_left(),buff=.08,color=HEAD) for i in range(2)])
        cost=label(r"amortized subpolynomial updates; not constant work for every update",font_size=22,color=LAM).set_y(-1.65)
        scope=VGroup(
            label(r"not an arbitrary-real-input or practical wall-time guarantee",font_size=23,color=HEAD),
            label(r"a cited theorem; this episode implements Edmonds--Karp",font_size=22,color=GREY_A),
        ).arrange(DOWN,buff=.2).set_y(-2.65)
        with self.voiceover("An almost-linear flow theorem also comes with conditions. <bookmark mark='a'/> Chen and colleagues' 2022 result gives exact directed maximum flow and minimum-cost flow in m to the one plus little o of one for polynomially bounded integral capacities, costs and demands in its stated setting. <bookmark mark='b'/> The method combines interior-point optimization with dynamic graph structures for approximate minimum-ratio cycles, whose update guarantee is amortized and subpolynomial. This is not a claim that every graph update costs constant time. <bookmark mark='c'/> Almost-linear describes asymptotic growth under those assumptions. It neither covers arbitrary real input for free nor promises that this implementation is as fast as reading a graph. The practical algorithm and its constants remain separate engineering questions.") as vo:
            self.play(FadeIn(head),FadeIn(tab))
            vo.wait_until('a');self.play(Indicate(tab,color=YES,scale_factor=1.02),run_time=.7)
            vo.wait_until('b');self.play(FadeIn(boxes),FadeIn(arrows),FadeIn(cost))
            vo.wait_until('c');self.play(FadeIn(scope))
        self.wait(.3);self.clear_scene()

    def open_(self):
        head=label(r"Open questions: specify weights, output and machine model",font_size=32).to_edge(UP,buff=.3)
        texts=[
            r"directed nonnegative-real distance-only SSSP in $O(m+n)$? comparison-addition model",
            r"practical almost-linear exact flow under useful integral-input assumptions?",
            r"general weighted APSP in $O(n^{3-\varepsilon})$ for a fixed $\varepsilon>0$?",
            r"classical general-weight TSP in $O^*((2-\varepsilon)^n)$ for fixed $\varepsilon>0$?",
        ]
        questions=VGroup()
        for i,text in enumerate(texts):
            frame=RoundedRectangle(width=12.6,height=.85,corner_radius=.1,color=GREY_D,fill_color=BG,fill_opacity=1)
            caption=label(text,font_size=22,color=GREY_A)
            if caption.width>12.0:caption.scale_to_fit_width(12.0)
            questions.add(VGroup(frame,caption).move_to([0,1.95-1.1*i,0]))
        star=label(r"$\bigstar$ research exercise: the first question; no sorted output required",font_size=22,color=HEAD).to_edge(DOWN,buff=.45)
        with self.voiceover("The model determines the open question. <bookmark mark='a'/> Can directed nonnegative-real single-source distances be computed in order m plus n in the comparison-addition model, without sorted output? The plus n accounts for vertices even when there are few edges. Thorup's classical linear bound concerns undirected positive integer weights in a different model. <bookmark mark='b'/> Can almost-linear exact flow methods become practical under useful input assumptions? <bookmark mark='c'/> For general weighted all-pairs shortest paths, is a fixed polynomial improvement below cubic possible in the stated model? <bookmark mark='d'/> For general weighted TSP, can a classical algorithm achieve a base strictly below two, ignoring polynomial factors? This differs from unweighted Hamiltonicity and quantum computation. <bookmark mark='e'/> The research exercise takes the first question and asks you to keep its weight, output and machine model explicit.") as vo:
            self.play(FadeIn(head),FadeIn(questions[0]))
            vo.wait_until('a');self.play(Indicate(questions[0],color=HEAD,scale_factor=1.02),run_time=.7)
            for mark,question in zip('bcd',questions[1:]):
                vo.wait_until(mark);self.play(FadeIn(question))
            vo.wait_until('e');self.play(FadeIn(star))
        self.wait(.3);self.clear_scene()
