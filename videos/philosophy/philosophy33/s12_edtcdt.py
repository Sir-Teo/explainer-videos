from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403


def node(txt, pos, col, r=0.55, fs=18):
    c = Circle(radius=r, color=col, fill_opacity=0.12).move_to(pos)
    return VGroup(c, label(txt, font_size=fs, color=col).move_to(c))


def edge(a, b, col=GREY_B):
    return Arrow(a[0].get_center(), b[0].get_center(), buff=0.6, color=col, stroke_width=3)


class EDTCDT(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Evidence or causation?", r"Does an act count for what it indicates, or for what it "
                                                           r"brings about?", lit=(1965, 1978, 1981), part=PART)
        with self.voiceover("Chapter eleven. Evidence or causation?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.formulas()
        self.lesion()
        self.button()
        self.damascus()
        self.wall_brick()

    def formulas(self):
        head = label(r"Two expected utilities", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f1 = MathTex(r"V(A) \;=\; \sum_S P(S \mid A)\,u(A, S)", font_size=36, color=EVID)
        l1 = label(r"evidential \ (Jeffrey, \ 1965): \ the news value of the act", font_size=19, color=EVID)
        f2 = MathTex(r"U(A) \;=\; \sum_S P(A \mathbin{\Box\!\!\to} S)\,u(A, S) \;=\; \sum_S P\big(S \mid "
                     r"\mathrm{do}(A)\big)\,u(A, S)", font_size=34, color=CAUSE)
        l2 = label(r"causal \ (Gibbard and Harper, \ 1978; \ Lewis, \ 1981; \ Joyce, \ 1999): \ what the act would "
                   r"bring about", font_size=19, color=CAUSE)
        g = VGroup(VGroup(f1, l1).arrange(DOWN, buff=0.15), VGroup(f2, l2).arrange(DOWN, buff=0.15)).arrange(
            DOWN, buff=0.6).move_to([0, 0.6, 0])
        foot = stack([(r"they agree whenever acts are no evidence about states they do not cause", GREY_A),
                      (r"$\mathrm{do}$: \ Pearl's intervention, \ from Part 17", HIST)], font_size=19,
                     buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Newcomb's problem divides two ways of computing expected utility. <bookmark mark='a'/>Richard "
            "Jeffrey's evidential decision theory, of 1965, weights each state by its probability given the act: "
            "the act's news value, how glad you would be to learn you had done it. <bookmark mark='b'/>Causal "
            "decision theory, from Allan Gibbard and William Harper in 1978, David Lewis in 1981 and James Joyce in "
            "1999, weights each state by the probability that it would obtain if you did the act: in Judea Pearl's "
            "terms from Part 17, conditioning on doing the act, not on observing it. Joyce computes it by imaging, an "
            "idea of Lewis's: moving each world's probability to the nearest worlds where the act is done. "
            "<bookmark mark='c'/>The two agree whenever your acts carry no evidence about states they do not "
            "cause. They come apart when acts are symptoms."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(g[0][0]), FadeIn(g[0][1]))
            vo.wait_until("b")
            self.play(Write(g[1][0]), FadeIn(g[1][1]))
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
        self.clear_scene()

    def lesion(self):
        d = load("lesion")
        head = label(r"The smoking lesion", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        a = d["acts"]
        assert a["smoke"]["p_lesion_given"] == 0.6585 and a["abstain"]["p_lesion_given"] == 0.0508
        assert (a["smoke"]["edt"], a["abstain"]["edt"], a["smoke"]["cdt"], a["abstain"]["cdt"]) == (
            -44.39, -8.814, -17.5, -27.5)
        assert d["edt_choice"] == "abstain" and d["cdt_choice"] == "smoke" and d["p_cancer_do"] == 0.275
        les = node(r"lesion", [-4.6, 1.2, 0], AGENT)
        smk = node(r"smoke", [-6.0, -0.9, 0], RISK)
        can = node(r"cancer", [-3.2, -0.9, 0], BAD)
        graph = VGroup(les, smk, can, edge(les, smk), edge(les, can))
        gl = label(r"no arrow from smoking to cancer", font_size=16, color=GREY_A).next_to(VGroup(smk, can), DOWN,
                                                                                          buff=0.3)
        nums = label(r"$P(\text{lesion}) = 0.3$; \ smoking is worth $+10$, \ cancer $-100$", font_size=16,
                     color=GREY_A).next_to(gl, DOWN, buff=0.15)
        hd = [r"", r"P(\text{lesion} \mid \text{act})", r"V \;(\text{EDT})", r"U \;(\text{CDT})"]
        cells = []
        for k, nm in (("smoke", r"smoke"), ("abstain", r"abstain")):
            cells.append([label(nm, font_size=20, color=RISK), label(f"{a[k]['p_lesion_given']:.3f}", font_size=20),
                          label(f"{a[k]['edt']:.1f}", font_size=20, color=EVID),
                          label(f"{a[k]['cdt']:.1f}", font_size=20, color=CAUSE)])
        grid = ValueGrid(hd, cells, col_w=[1.8, 2.6, 1.8, 1.8], cell_h=0.6, font_size=19).move_to([2.6, 0.9, 0])
        pick = VGroup(SurroundingRectangle(grid.cell[1][2], color=EVID, buff=0.06),
                      SurroundingRectangle(grid.cell[0][3], color=CAUSE, buff=0.06))
        side = stack([(r"EDT: \ abstain, \ because smoking is bad news", EVID),
                      (r"CDT: \ smoke; \ $P(\text{cancer} \mid \mathrm{do}(\text{smoke})) = 0.275$ either way", CAUSE),
                      (r"most judge CDT right here: \ abstaining only manages the news", GOAL),
                      (r"the tickle defence \ (Eells, \ 1982): \ if you can feel the urge, \ the act itself adds no "
                       r"evidence", HIST)], font_size=18, aligned_edge=LEFT, width=6.0, buff=0.25).move_to(
            [2.6, -1.8, 0])
        with self.voiceover(
            "The standard case against evidential decision theory is the smoking lesion. <bookmark mark='a'/>"
            "Suppose a lesion causes both a taste for smoking and cancer, and smoking itself is harmless. Thirty "
            "percent of people have the lesion; smoking is worth ten units of pleasure, cancer minus a hundred. "
            "<bookmark mark='b'/>Given that you smoke, the chance you have the lesion is sixty six percent; given "
            "that you abstain, five. So evidential expected utility is minus forty four for smoking and minus nine "
            "for abstaining. <bookmark mark='c'/>Evidential decision theory says abstain: smoking would be bad news. "
            "<bookmark mark='d'/>Causal decision theory intervenes. Doing the act leaves the lesion alone, so the "
            "chance of cancer is twenty seven and a half percent either way, and smoking adds its pleasure: smoke. "
            "<bookmark mark='e'/>Most people judge causal decision theory right here: abstaining manages the news, "
            "not the cancer. <bookmark mark='f'/>Ellery Eells replied for evidentialists with the tickle defence: if "
            "you can feel the urge that the lesion causes, then the act itself adds no further evidence, and the "
            "two theories agree."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(graph), FadeIn(gl), FadeIn(nums))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(2):
                self.play(*[FadeIn(c) for c in grid.cell[r][:3]], run_time=0.5)
            vo.wait_until("c")
            self.play(Create(pick[0]), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(*[FadeIn(grid.cell[r][3]) for r in range(2)])
            self.play(Create(pick[1]), FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
            vo.wait_until("f")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def button(self):
        d = load("button")
        head = label(r"The psychopath button \ (Egan, \ 2007)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["p_psycho"], d["p_if_press"]) == (0.05, 0.9)
        assert (d["cdt_press"], d["cdt_press_once_decided"], d["edt_press"]) == (4.5, -89.0, -89.0)
        assert d["cdt_choice"] == "press" and d["edt_choice"] == "refrain"
        btn = VGroup(Circle(radius=0.7, color=BAD, fill_opacity=0.7), label(r"press", font_size=20,
                                                                           color=WHITE)).move_to([-4.8, 0.6, 0])
        story = stack([(r"pressing kills every psychopath", BAD),
                       (r"Paul would like that, \ unless he is one", GREY_A),
                       (r"he is fairly sure he is not: \ $P = 0.05$", GREY_A),
                       (r"but only a psychopath would press: \ $P(\text{psychopath} \mid \text{press}) = 0.9$",
                        AGENT)], font_size=18, aligned_edge=LEFT, width=5.0, buff=0.22).next_to(btn, DOWN, buff=0.4)
        story.align_to(btn, LEFT).shift(LEFT * 0.6)
        f1 = MathTex(r"U(\text{press}) = 0.95 \times 10 + 0.05 \times (-100) = +4.5", font_size=28, color=CAUSE)
        f2 = MathTex(r"V(\text{press}) = 0.1 \times 10 + 0.9 \times (-100) = -89", font_size=28, color=EVID)
        f3 = MathTex(r"U(\text{press} \mid \text{decided to press}) = -89", font_size=28, color=CAUSE)
        fs = VGroup(f1, f2, f3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([2.6, 1.0, 0])
        side = stack([(r"CDT: \ press; \ EDT: \ refrain", GREY_A),
                      (r"almost everyone: \ refrain", GOAL),
                      (r"and CDT's verdict reverses once the choice is made: \ it is unstable", BAD)], font_size=19,
                     aligned_edge=LEFT, width=5.6, buff=0.22).move_to([2.6, -1.6, 0])
        with self.voiceover(
            "In 2007 Andy Egan turned the tables. <bookmark mark='a'/>Paul can press a button that will kill every "
            "psychopath. He would like that done, unless he is a psychopath himself. He is fairly sure he is not: "
            "five percent. But he is also sure that only a psychopath would press such a button. "
            "<bookmark mark='b'/>Causal decision theory uses his unconditional credence: pressing has expected "
            "utility plus four and a half. Press. <bookmark mark='c'/>Evidential decision theory conditions on "
            "pressing: ninety percent that he is a psychopath, minus eighty nine. Refrain. "
            "<bookmark mark='d'/>Almost everyone agrees with refraining. And once Paul has decided to press, his "
            "credence changes, and causal decision theory now says not to: its verdict is unstable. Here evidential "
            "decision theory gets it right, and the causal theory needs repair."
        ) as vo:
            self.play(FadeIn(head), FadeIn(btn))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in story], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(Write(f1))
            vo.wait_until("c")
            self.play(Write(f2), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(Write(f3), FadeIn(side[1]), FadeIn(side[2]))
        self.clear_scene()

    def damascus(self):
        d = load("damascus")
        head = label(r"Death in Damascus \ (Gibbard and Harper, \ 1978)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        assert d["ratifiable"] == []
        rows = d["rows"]
        assert [(r["plan"], r["stay"], r["switch"]) for r in rows] == [("Damascus", 0.01, 0.99),
                                                                       ("Aleppo", 0.01, 0.99)]
        dam = node(r"Damascus", [-4.4, 0.4, 0], RISK, r=0.8, fs=18)
        ale = node(r"Aleppo", [-1.2, 0.4, 0], RISK, r=0.8, fs=18)
        a1 = CurvedArrow(dam[0].get_top() + RIGHT * 0.2, ale[0].get_top() + LEFT * 0.2, angle=-PI / 3, color=CAUSE)
        a2 = CurvedArrow(ale[0].get_bottom() + LEFT * 0.2, dam[0].get_bottom() + RIGHT * 0.2, angle=-PI / 3,
                         color=CAUSE)
        al = label(r"each plan recommends the other", font_size=17, color=CAUSE).next_to(VGroup(dam, ale), DOWN,
                                                                                         buff=0.9)
        hd = [r"\text{if you plan}", r"\text{survive by staying}", r"\text{survive by going}"]
        cells = [[label(r["plan"], font_size=19, color=RISK), label(f"{r['stay']:.2f}", font_size=20, color=BAD),
                  label(f"{r['switch']:.2f} \\ (to {r['switch_to']})", font_size=19, color=OK)] for r in rows]
        grid = ValueGrid(hd, cells, col_w=[2.4, 2.6, 3.0], cell_h=0.6, font_size=18).move_to([3.0, 1.0, 0])
        side = stack([(r"ratifiable: \ still best once you have chosen it \ (Jeffrey, \ 1983)", GOAL),
                      (r"neither city is ratifiable", BAD),
                      (r"responses: \ mixed acts; \ deliberational dynamics \ (Skyrms, \ 1990; \ Arntzenius, \ "
                       r"2008); \ Joyce's equilibrium \ (2012)", HIST)], font_size=18, aligned_edge=LEFT, width=5.6,
                     buff=0.25).move_to([3.0, -1.5, 0])
        with self.voiceover(
            "Causal decision theory has an older instability problem. <bookmark mark='a'/>A man meets Death in "
            "Damascus. Death says: I am coming for you tomorrow. The man thinks of fleeing to Aleppo. But Death is "
            "a reliable predictor, and will be wherever he predicts the man will be. <bookmark mark='b'/>If the man "
            "plans to stay in Damascus, then Death is probably waiting in Damascus, and going to Aleppo would save "
            "him with probability ninety nine percent. If he plans Aleppo, Death is probably in Aleppo, and Damascus "
            "is the place to be. <bookmark mark='c'/>Jeffrey called a choice ratifiable if it is still best once "
            "you have chosen it. <bookmark mark='d'/>Neither city is ratifiable: each plan, once made, recommends "
            "the other. <bookmark mark='e'/>Brian Skyrms and Frank Arntzenius modelled deliberation as a process "
            "that settles on a mixed state of mind, and Joyce proposed choosing at the equilibrium. Whether that "
            "rescues the theory is open."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dam), FadeIn(ale))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            self.play(*[FadeIn(c) for c in grid.cell[0]], Create(a1))
            self.play(*[FadeIn(c) for c in grid.cell[1]], Create(a2), FadeIn(al))
            vo.wait_until("c")
            self.play(FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=33, current=33).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(33, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the thirty third brick in the Wall. <bookmark mark='a'/>The dream was one theory of rational "
            "choice: expected utility, with probabilities and utilities read off preferences. Allais and Ellsberg "
            "showed common, defensible preferences that no expected utility represents. Newcomb's problem split "
            "the theory into two, evidential and causal, and each has cases it gets wrong. "
            "<bookmark mark='b'/>What it forces is a choice: keep expected utility and call those preferences "
            "mistakes, adopt one of its rivals, or accept that rational choice needs more than one theory."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[33], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()
