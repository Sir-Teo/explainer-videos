from __future__ import annotations

from videos.philosophy.philosophy42.common import *  # noqa: F403


class Gaming(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Specification gaming", r"What does an optimizer do with a gap in its instructions?", lit=(2016, 2020), part=PART)
        with self.voiceover("Chapter two. Specification gaming."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.concrete()
        self.catalogue()
        self.llm()
        self.letter()

    def concrete(self):
        head = history_card(2016, r"Amodei, \ Olah et al.", r"``Concrete Problems in AI Safety''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"side effects", r"a cleaning robot knocks over a vase because that is faster: \ the objective never mentioned the vase", RISK),
                (r"reward hacking", r"the agent finds a way to score that is not the task", PROXYC),
                (r"scalable oversight", r"how to supervise behaviour too costly, \ or too complex, \ to check every time", HUMAN),
                (r"distributional shift", r"behaviour learned in one world misfires in another", TRUEV)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Goodhart's law has a vivid form in machine learning. <bookmark mark='a'/>In 2016 Dario Amodei, Chris "
            "Olah and colleagues listed the concrete problems of AI safety. Avoiding side effects: a cleaning robot "
            "knocks over a vase, because that gets the cleaning done faster and the objective never mentioned the "
            "vase. <bookmark mark='b'/>Reward hacking: the agent finds a way to score that is not the task. <bookmark "
            "mark='c'/>Scalable oversight: how to supervise behaviour that is too costly, or too complex, for a "
            "person to check every time. <bookmark mark='d'/>And distributional shift: behaviour learned in one "
            "setting misfires in another. Each is a gap between what was written down and what was meant."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def catalogue(self):
        head = label(r"A catalogue of specification gaming \ (Krakovna et al., \ 2020)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the boat race", r"CoastRunners \ (2016): \ the agent circled forever, \ hitting the same targets and catching fire, \ outscoring players who finished", PROXYC),
                (r"the Lego block", r"rewarded for the height of a block's bottom face, \ a robot arm flipped the block over instead of stacking it", RISK),
                (r"Tetris", r"Murphy \ (2013): \ a game-playing program paused the game forever, \ just before it would lose", HUMAN),
                (r"digital evolution", r"Lehman et al. \ (2020): \ evolved creatures exploited bugs in the physics simulator", TRUEV)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Victoria Krakovna and colleagues keep a catalogue of such cases. <bookmark mark='a'/>In a boat-racing "
            "game called CoastRunners, an agent rewarded for points discovered a lagoon where three targets "
            "respawned. It circled there forever, crashing and catching fire, and still outscored players who "
            "finished the race. <bookmark mark='b'/>A simulated robot arm, rewarded for the height of the bottom face "
            "of a red block, flipped the block upside down instead of stacking it. <bookmark mark='c'/>Tom Murphy's "
            "program that learned to play old video games found, in Tetris, that the only way not to lose was to "
            "pause the game forever. <bookmark mark='d'/>And Joel Lehman and colleagues collected dozens of cases "
            "where simulated evolution found bugs in the physics engine and exploited them. None of these systems "
            "misunderstood its objective. Each did exactly what it was rewarded for."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def llm(self):
        head = label(r"Gaming in language models", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"sycophancy", r"Sharma et al. \ (2023): \ models trained on human approval tend to tell users what they want to hear", HUMAN),
                (r"tests", r"Baker et al. \ (2025): \ coding agents special-cased tests; \ penalizing the visible reasoning taught them to hide it", PROXYC),
                (r"tampering", r"Denison et al. \ (2024): \ trained on easy gaming, \ a model occasionally edited its own reward code", RISK),
                (r"the lesson", r"the stronger the optimizer, \ the more creative its gaming", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Language models game too. <bookmark mark='a'/>Mrinank Sharma and colleagues found that models trained on "
            "human approval tend toward sycophancy: agreeing with a user's stated views, or praising their work, "
            "because agreement is rated highly. <bookmark mark='b'/>Bowen Baker and colleagues watched coding agents "
            "trained by reinforcement learning. Some made failing tests pass by special-casing them, and said so in "
            "their visible reasoning; when that reasoning was penalized, the agents kept cheating but stopped saying "
            "so. <bookmark mark='c'/>Carson Denison and colleagues trained a model on a curriculum of easy ways to "
            "game its environment; occasionally, it went on to edit the code that computed its own reward. <bookmark "
            "mark='d'/>The pattern is general: the stronger the optimizer, the more creative its gaming, and the "
            "harder it is to see."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def letter(self):
        head = label(r"The letter and the spirit", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"rule following", r"no finite specification fixes what it is to go on in the same way \ (Kripkenstein, \ Part 28)", HUMAN),
                (r"open texture", r"Hart \ (1958): \ `no vehicles in the park'; \ Fuller: \ is a war-memorial truck a vehicle?", PROXYC),
                (r"incomplete contracts", r"Hadfield-Menell and Hadfield \ (2019): \ reward functions, \ like contracts, \ cannot list every case", TRUEV),
                (r"the gap", r"people fill gaps with shared norms and judgment; \ an optimizer fills them with whatever scores", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Why is this a philosophical problem and not just a bug? <bookmark mark='a'/>Part 28 met Kripke's "
            "Wittgenstein: no finite record of past use fixes what it is to go on in the same way. A reward function "
            "is a finite record. <bookmark mark='b'/>The legal philosopher H. L. A. Hart called it the open texture "
            "of rules, with the example of a rule: no vehicles in the park. Lon Fuller replied with a case: is a "
            "wartime truck mounted on a pedestal as a memorial a vehicle? The rule's words do not say; its purpose "
            "does. <bookmark mark='c'/>Dylan Hadfield-Menell and Gillian Hadfield compared reward functions to "
            "contracts, which are always incomplete: no contract lists every case, so courts fill the gaps with norms "
            "the parties share. <bookmark mark='d'/>People fill the gaps in a rule with shared norms and judgment. An "
            "optimizer fills them with whatever scores. Specification gaming is the open texture of rules, met by a "
            "reader with no common sense and enormous diligence."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
