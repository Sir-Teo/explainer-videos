from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.smoking()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"The law of causality, I believe, like much that passes muster among philosophers, is a relic "
                       r"of a bygone age, surviving, like the monarchy, only because it is erroneously supposed to do "
                       r"no harm.", r"Bertrand Russell", r"`On the Notion of Cause' \ (1913)", width=10.4,
                       font_size=24).next_to(t, DOWN, buff=0.5)
        with self.voiceover(
            "Part 16 ended with a lesson from Simpson's paradox: statistics alone cannot tell us which table to "
            "trust, because that depends on what causes what. This part is about causes. "
            "<bookmark mark='a'/>In 1913 Bertrand Russell argued that physics had no use for the notion: the law of "
            "causality, he said, is a relic of a bygone age, surviving, like the monarchy, only because it is "
            "erroneously supposed to do no harm. <bookmark mark='b'/>A century later, causation is a branch of "
            "mathematics, and a Turing Award."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=GOAL, scale_factor=1.03))
        self.clear_scene()

    def smoking(self):
        head = label(r"Does smoking cause lung cancer?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        g = CausalGraph({"smoking": [-3.2, 0.4, 0], "cancer": [0.2, 0.4, 0], "gene": [-1.5, 2.0, 0]},
                        [("smoking", "cancer"), ("gene", "smoking"), ("gene", "cancer")], hidden=("gene",),
                        colors={"smoking": CAUSE, "cancer": EFFECT}, radius=0.62, font_size=19,
                        dashed=(("gene", "smoking"), ("gene", "cancer")))
        rows = stack([
            (r"Doll and Hill \ (1950, \ 1954): \ heavy smokers, \ lung cancer about 20 times as often", WHITE),
            (r"Fisher \ (1958): \ perhaps a gene inclines people both to smoke and to cancer", BAD),
            (r"Cornfield \ (1959): \ to explain a 9-fold risk away, \ the gene must be 9 times commoner in "
             r"smokers", OK),
            (r"no such gene was found; \ the Surgeon General \ (1964); \ Hill's criteria \ (1965)", GREY_A),
            (r"but what, \ exactly, \ had been shown? \ And how?", GOAL),
        ], font_size=21, aligned_edge=LEFT, width=7.2).move_to([2.8, -1.6, 0])
        with self.voiceover(
            "The most consequential causal question of the twentieth century. <bookmark mark='a'/>Richard Doll and "
            "Austin Bradford Hill found that heavy smokers developed lung cancer many times as often as "
            "non-smokers. <bookmark mark='b'/>Ronald Fisher, the founder of modern statistics, and himself a smoker, "
            "objected that correlation is not causation: perhaps a gene inclines people both to smoke and to get "
            "cancer. <bookmark mark='c'/>Jerome Cornfield answered with an inequality: to explain away a nine-fold "
            "risk, such a gene would have to be at least nine times as common among smokers, and nothing like it "
            "was ever found. <bookmark mark='d'/>The Surgeon General's report of 1964 settled the policy. "
            "<bookmark mark='e'/>But what, exactly, had been shown, and by what logic? Fisher's own method, the "
            "randomized experiment, was impossible here. This part builds the logic that settles such questions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g.node["smoking"]), FadeIn(g.node["cancer"]), GrowArrow(g.edge[("smoking", "cancer")]),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(g.node["gene"]), Create(g.edge[("gene", "smoking")]), Create(g.edge[("gene", "cancer")]),
                      FadeIn(rows[1]))
            for mk, r in zip("cde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Hume's two definitions; \ al-Ghazālī's cotton; \ Mill's methods; \ INUS conditions",
            r"Lewis's counterfactuals: \ preemption, \ trumping, \ overdetermination",
            r"probability-raising; \ Russell's challenge; \ interventions",
            r"structural models, \ graphs, \ d-separation; \ seeing and doing; \ the do-calculus",
            r"the ladder: \ counterfactuals, \ necessity and sufficiency; \ actual causation, \ computed",
            r"Markov, \ faithfulness, \ the common cause; \ discovery by PC \ (the Wall)",
            r"potential outcomes, \ instruments, \ difference in differences; \ causes at work; \ the mind",
        ], font_size=24)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>The classical analyses: Hume's two definitions, al-Ghazālī's challenge "
            "eight centuries earlier, Mill's methods and Mackie's conditions. <bookmark mark='b'/>Lewis's "
            "counterfactual theory, and the cases that break it. <bookmark mark='c'/>Probabilities, Russell's "
            "challenge, and the idea of intervention. <bookmark mark='d'/>Structural models and their graphs, the "
            "difference between seeing and doing, and Pearl's do-calculus. <bookmark mark='e'/>The ladder of "
            "causation, and actual causation, computed on the classic cases. <bookmark mark='f'/>The assumptions "
            "that let us discover causes from data, and the theorem that limits it: this part's brick in the Wall. "
            "<bookmark mark='g'/>And the statistician's rival framework, causes at work in industry, and whether a "
            "thought can cause anything at all."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
