from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403


class FDT(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Policies", r"Should you choose acts, or the procedure that produces them?",
                            lit=(1984, 2017), part=PART)
        with self.voiceover("Chapter twelve. Policies."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.hitchhiker()
        self.twins()
        self.fdt()
        self.critiques()

    def hitchhiker(self):
        d = load("hitchhiker")
        head = label(r"Parfit's hitchhiker \ (1984)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["accuracy"] == 0.99 and d["policy_pay"] == -10990.0 and d["policy_refuse"] == -990000.0
        assert (d["in_town_pay"], d["in_town_refuse"]) == (-1000.0, 0.0)
        story = stack([(r"you are dying in the desert", BAD),
                       (r"a driver will take you to town \ only if he predicts you will then pay him \$1,000", AGENT),
                       (r"he reads faces, \ and is right 99\% of the time", GREY_A)], font_size=19,
                      aligned_edge=LEFT, width=5.6, buff=0.25).move_to([-3.4, 1.4, 0])
        hd1 = [r"\text{in town, as an act}", r"\text{value}"]
        c1 = [[label(r"pay", font_size=19, color=MONEY), label(r"$-1{,}000$", font_size=20, color=BAD)],
              [label(r"refuse", font_size=19, color=MONEY), label(r"$0$", font_size=20, color=OK)]]
        g1 = ValueGrid(hd1, c1, col_w=[3.2, 1.8], cell_h=0.55, font_size=18).move_to([-3.4, -1.4, 0])
        hd2 = [r"\text{as a policy}", r"\text{expected value}"]
        c2 = [[label(r"pay once rescued", font_size=19, color=AGENT), label(r"$-10{,}990$", font_size=20,
                                                                            color=OK)],
              [label(r"refuse once rescued", font_size=19, color=AGENT), label(r"$-990{,}000$", font_size=20,
                                                                               color=BAD)]]
        g2 = ValueGrid(hd2, c2, col_w=[3.4, 2.2], cell_h=0.55, font_size=18).move_to([3.2, -1.4, 0])
        f = MathTex(r"0.99 \times (-1{,}000) + 0.01 \times (-10^6)", font_size=24, color=GREY_A).next_to(
            g2, UP, buff=0.35)
        foot = label(r"death counted as $-10^6$", font_size=16, color=GREY_A).next_to(g2, DOWN, buff=0.2)
        with self.voiceover(
            "Derek Parfit described this case in 1984. <bookmark mark='a'/>You are dying of thirst in the desert. "
            "A driver stops. He will take you to town only if he predicts that, once there, you will pay him a "
            "thousand dollars. He reads faces well: he is right ninety nine times in a hundred. "
            "<bookmark mark='b'/>Once you are in town, paying is a pure loss. You are safe; nothing you do now can "
            "undo the rescue. Causal decision theory says do not pay, and so does evidential decision theory, since "
            "you already know you were rescued. <bookmark mark='c'/>So the driver, reading you correctly, predicts "
            "that you will not pay, and leaves you to die. <bookmark mark='d'/>Compare the policies. Paying once "
            "rescued has an expected value of minus eleven thousand, counting death as minus a million; refusing has "
            "minus nine hundred and ninety thousand. An agent who reasons act by act does worse than one who can "
            "commit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in story], lag_ratio=0.4), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(g1.head), Create(g1.rule), *[FadeIn(c) for row in g1.cell for c in row])
            vo.wait_until("c")
            self.play(Indicate(story[0], color=WHITE))
            vo.wait_until("d")
            self.play(FadeIn(g2.head), Create(g2.rule), *[FadeIn(c) for row in g2.cell for c in row], FadeIn(f),
                      FadeIn(foot))
        self.clear_scene()

    def twins(self):
        d = load("twins")
        head = label(r"The prisoner's dilemma against your twin \ (Lewis, \ 1979)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        pay = d["payoffs"]
        assert pay == {"T": 5, "R": 3, "P": 1, "S": 0} and d["threshold"] == 0.7143
        assert d["dominance_gain"] == [2, 1]
        hd1 = [r"", r"\text{twin cooperates}", r"\text{twin defects}"]
        c1 = [[label(r"you cooperate", font_size=18, color=EVID), label(r"3", font_size=20), label(r"0", font_size=20)],
              [label(r"you defect", font_size=18, color=CAUSE), label(r"5", font_size=20), label(r"1", font_size=20)]]
        g1 = ValueGrid(hd1, c1, col_w=[2.2, 2.2, 2.0], cell_h=0.55, font_size=17).move_to([-3.8, 1.2, 0])
        dom = label(r"defecting gains 2 or 1, \ whatever the twin does", font_size=17, color=CAUSE).next_to(
            g1, DOWN, buff=0.25)
        ax = Axes(x_range=[0.5, 1, 0.1], y_range=[0, 3.5, 1], x_length=4.2, y_length=3.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15, "include_numbers": True},
                  x_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([2.7, 0.8, 0])
        xl = label(r"$r$: \ chance the twin moves as you do", font_size=15, color=GREY_A).next_to(ax.x_axis, DOWN,
                                                                                              buff=0.35)
        co = ax.plot(lambda r: 3 * r, x_range=[0.5, 1], color=EVID)
        de = ax.plot(lambda r: r + 5 * (1 - r), x_range=[0.5, 1], color=CAUSE)
        cross = Dot(ax.c2p(5 / 7, 15 / 7), radius=0.08, color=WHITE)
        cl = label(r"$r = 5/7 = 0.714$", font_size=16, color=WHITE).next_to(cross, UP, buff=0.12)
        ll = VGroup(label(r"cooperate: \ $3r$", font_size=15, color=EVID).next_to(ax.c2p(1, 3), RIGHT, buff=0.1),
                    label(r"defect: \ $r + 5(1-r)$", font_size=15, color=CAUSE).next_to(ax.c2p(1, 1), RIGHT,
                                                                                         buff=0.1))
        side = stack([(r"CDT: \ defect, \ by dominance, \ at every $r$", CAUSE),
                      (r"EDT: \ cooperate once $r > 0.714$", EVID),
                      (r"FDT: \ cooperate with an exact copy: \ you and it compute one function", AGENT),
                      (r"Part 34: \ what if the twin is only a stranger?", GOAL)], font_size=18, buff=0.2).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "David Lewis showed in 1979 that a famous game hides a Newcomb problem. <bookmark mark='a'/>In the "
            "prisoner's dilemma, each player cooperates or defects. Mutual cooperation pays three each; mutual "
            "defection one; a defector against a cooperator gets five, and the cooperator nothing. "
            "<bookmark mark='b'/>Whatever the other does, defecting pays more: two more against a cooperator, one "
            "more against a defector. That is dominance, and the causal theory defects. <bookmark mark='c'/>Now let "
            "the other player be your near-copy, whose move matches yours with probability r. Evidentially, "
            "cooperating is worth three r, and defecting r plus five times one minus r. <bookmark mark='d'/>The lines "
            "cross at five sevenths: above that, the evidential theory cooperates. <bookmark mark='e'/>Functional "
            "decision theory cooperates with an exact copy, since you and it compute one function. Whether real "
            "strangers ever resemble each other enough is the next part's question: Part 34 begins with this game."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g1.head), Create(g1.rule), *[FadeIn(c) for row in g1.cell for c in row])
            vo.wait_until("b")
            self.play(FadeIn(dom), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl))
            self.play(Create(co), Create(de), FadeIn(ll))
            vo.wait_until("d")
            self.play(FadeIn(cross), FadeIn(cl), FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def fdt(self):
        head = label(r"Functional decision theory \ (Yudkowsky and Soares, \ 2017)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"\mathrm{FDT}(P) \;=\; \arg\max_{a} \; \mathbb{E}\big[\,u \;\big|\; \mathrm{do}"
                    r"(\text{the procedure } P \text{ outputs } a)\big]", font_size=32, color=AGENT).move_to(
            [0, 1.9, 0])
        fl = label(r"intervene on the output of your decision procedure, \ wherever it is computed", font_size=19,
                   color=GREY_A).next_to(f, DOWN, buff=0.2)
        hd = [r"\text{case}", r"\text{EDT}", r"\text{CDT}", r"\text{FDT}"]
        rows = [(r"Newcomb", r"one box", r"two boxes", r"one box"),
                (r"smoking lesion", r"abstain", r"smoke", r"smoke"),
                (r"Parfit's hitchhiker", r"refuse", r"refuse", r"pay"),
                (r"transparent Newcomb \ (both boxes visible)", r"two boxes", r"two boxes", r"one box")]
        cells = [[label(a, font_size=18, color=WHITE), label(b, font_size=18, color=EVID),
                  label(c, font_size=18, color=CAUSE), label(e, font_size=18, color=AGENT)] for a, b, c, e in rows]
        grid = ValueGrid(hd, cells, col_w=[4.6, 2.0, 2.0, 2.0], cell_h=0.55, font_size=18).move_to([0, -0.9, 0])
        note = label(r"the predictor, \ the driver and your twin all run a model of your procedure", font_size=18,
                     color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Eliezer Yudkowsky and Nate Soares, working on the foundations of artificial agents, proposed "
            "functional decision theory in 2017. <bookmark mark='a'/>Treat your decision as the output of a "
            "procedure, a function, and ask which output would be best if you intervened on it, everywhere that "
            "function is computed: in your head, and in the predictor's model of you. <bookmark mark='b'/>In "
            "Newcomb's problem the predictor computes your procedure, so its output fixes both your choice and the "
            "box: take one. <bookmark mark='c'/>In the smoking lesion nothing computes your procedure except you; "
            "smoking does not change the lesion: smoke, as the causal theory says. <bookmark mark='d'/>In the "
            "desert, the driver's prediction is a model of your procedure, so the policy of paying gets you "
            "rescued: pay. <bookmark mark='e'/>And in transparent Newcomb, where you can see the million already "
            "in the box, it still says take only one box, since a procedure that would take both is predicted, and "
            "never sees the million. <bookmark mark='f'/>The predictor, the driver and a twin copy of you all run a "
            "model of your procedure; for an artificial agent that can be copied and simulated, that is no "
            "fantasy."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            self.play(FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("bcde", range(4)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.6)
            vo.wait_until("f")
            self.play(FadeIn(note))
        self.clear_scene()

    def critiques(self):
        head = label(r"The critiques", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"what is computed?", r"when does a physical system `compute' my procedure? \ the theory needs "
                                       r"counterfactuals about logic: \ `if this function output 1'", RISK),
                (r"the bomb", r"MacAskill \ (2019): \ a predictor who is almost always right left a note saying it "
                              r"put a bomb in the left box; \ FDT takes the left box anyway, \ and burns", BAD),
                (r"Schwarz \ (2018)", r"in blackmail and procreation cases its verdicts look arbitrary, \ and it "
                                     r"is not yet a formal theory", BAD),
                (r"the defence", r"judge a theory by how its agents fare across the problems they might face, \ not "
                                 r"in one problem after the fact", AGENT)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6)
        with self.voiceover(
            "Philosophers have pressed hard. <bookmark mark='a'/>First, the theory needs counterfactuals about "
            "logic: what would happen if a given mathematical function had a different output. When does a brain, "
            "or a predictor's model, compute my function? There is no settled account. <bookmark mark='b'/>William "
            "MacAskill's bomb case, of 2019: a predictor who errs once in a trillion trillion times leaves a note "
            "saying it predicted you would take the right box, and so put a bomb in the left. Taking the left box "
            "costs a hundred dollars less, and functional decision theory takes it: a policy of taking left makes "
            "such notes almost never appear, and so you burn. <bookmark mark='c'/>Wolfgang Schwarz argued in 2018 "
            "that its verdicts in some cases look arbitrary, and that it is not yet a formal theory. "
            "<bookmark mark='d'/>Its defenders answer that decision theories should be judged by how their agents "
            "fare across all the problems they might meet, not by what looks best in one problem after the fact. "
            "That disagreement, over what a theory of choice is for, is where the debate now stands."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
