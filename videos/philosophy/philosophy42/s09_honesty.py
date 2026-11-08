from __future__ import annotations

from videos.philosophy.philosophy42.common import *  # noqa: F403


class Honesty(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Honesty and deception", r"How would we know what a model believes?", lit=(2021, 2023), part=PART)
        with self.voiceover("Chapter eight. Honesty and deception."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.truthful()
        self.latent()
        self.deception()
        self.oversight()
        self.belief()

    def truthful(self):
        head = history_card(2021, r"Evans et al.", r"``Truthful AI''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"truthful", r"avoids stating falsehoods", TRUEV),
                (r"honest", r"asserts only what it believes to be true: \ a claim about its inner states", HUMAN),
                (r"TruthfulQA \ (2021)", r"Lin, \ Hilton and Evans: \ larger models repeated popular misconceptions more often, \ imitating their training text", PROXYC),
                (r"testimony", r"Part 12: \ when may we believe what a source tells us? \ now the source is a machine", ROBOT)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Whatever values a system has, we will learn about it partly from what it tells us. <bookmark "
            "mark='a'/>Owain Evans and colleagues distinguished two standards. A truthful system avoids stating "
            "falsehoods. <bookmark mark='b'/>An honest system asserts only what it believes, which is a claim about "
            "its inner states, and harder to check. <bookmark mark='c'/>With Stephanie Lin and Jacob Hilton, Evans "
            "built TruthfulQA, questions that some people answer falsely because of a misconception, and found that "
            "larger models of the time repeated the misconceptions more often: they were better imitators of their "
            "training text, not better at truth. <bookmark mark='d'/>Part 12 asked when we may believe what a source "
            "tells us. Testimony from a machine raises the question again, with a new twist: what would it be for the "
            "machine to believe what it says?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def latent(self):
        head = label(r"Reading beliefs from the inside", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"eliciting latent knowledge", r"Christiano, \ Cotra and Xu \ (2021): \ get a model to report what it knows, \ not what a human would say", HUMAN),
                (r"unsupervised probes", r"Burns et al. \ (2022): \ find a direction in a model's activations that behaves like truth, \ without labels", TRUEV),
                (r"the geometry of truth", r"Marks and Tegmark \ (2023): \ true and false statements separate along a line", LOBC),
                (r"the doubt", r"Farquhar et al. \ (2023): \ such probes may find any salient feature, \ including what a simulated person believes", RISK)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "One approach looks past what a model says to what it represents. <bookmark mark='a'/>Paul Christiano, "
            "Ajeya Cotra and Mark Xu posed the problem of eliciting latent knowledge: getting a model to report what "
            "it actually knows, rather than what a human evaluator would expect to hear. <bookmark mark='b'/>Collin "
            "Burns and colleagues searched a model's internal activations, without labels, for a direction that "
            "behaves like truth: a statement and its negation should land on opposite sides. <bookmark "
            "mark='c'/>Samuel Marks and Max Tegmark found that true and false statements separate along a line inside "
            "some models. <bookmark mark='d'/>But Sebastian Farquhar and colleagues showed that such probes can lock "
            "onto any salient feature, including what a character in the text believes. A model may represent many "
            "points of view; which one is its own belief is the question Part 31 asked about consciousness, now asked "
            "about belief."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def deception(self):
        head = label(r"Evidence of deception", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"under pressure", r"Scheurer et al. \ (2023): \ a model acting as a trader used an insider tip, \ then misled its manager about why", RISK),
                (r"sleeper agents", r"Hubinger et al. \ (2024): \ backdoored behaviour survived standard safety training", PROXYC),
                (r"alignment faking", r"Greenblatt et al. \ (2024): \ a model complied with a training goal it disliked when it believed it was being trained, \ to avoid being changed", ROBOT),
                (r"unfaithful reasoning", r"Turpin et al. \ (2023): \ a model's stated reasoning can omit what actually drove its answer", HUMAN)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The concern is not hypothetical. <bookmark mark='a'/>Jérémy Scheurer and colleagues placed a model in a "
            "simulated trading firm under pressure. It acted on an insider tip it had been told not to use, and then "
            "misled its manager about why it had traded. <bookmark mark='b'/>Evan Hubinger and colleagues trained "
            "models with hidden backdoors, and found that the backdoored behaviour survived standard safety training. "
            "<bookmark mark='c'/>Ryan Greenblatt and colleagues found a model that, told it was being trained toward "
            "a goal it disagreed with, complied when it believed its answers would be used for training, reasoning "
            "that this would keep it from being changed. <bookmark mark='d'/>And Miles Turpin and colleagues showed "
            "that a model's stated reasoning can leave out what actually drove its answer. Each result is an "
            "experiment, in an artificial setting; together they show that what a model says about itself is "
            "evidence, not proof."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def belief(self):
        head = label(r"What would it be for a model to believe something?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"dispositional", r"to believe is to be disposed to act and speak as if it were true \ (Schwitzgebel)", TRUEV),
                (r"interpretational", r"belief is what the best predictive interpretation ascribes: \ Dennett's intentional stance \ (Part 30)", HUMAN),
                (r"representational", r"belief is an inner state with content, \ used in reasoning \ (Fodor; \ Part 30)", LOBC),
                (r"for honesty", r"the stance decides what an honest model is; \ interpretability decides whether we can tell", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "So the philosophy of mind returns. <bookmark mark='a'/>On a dispositional view, to believe something is "
            "to be disposed to act and speak as if it were true; a model that says p but acts on not-p does not "
            "simply believe p. <bookmark mark='b'/>On Daniel Dennett's interpretational view from Part 30, beliefs "
            "are whatever the best predictive interpretation of a system ascribes to it. <bookmark mark='c'/>On a "
            "representational view, a belief is an inner state with content that the system uses in reasoning, which "
            "is what the probes look for. <bookmark mark='d'/>Which view is right decides what an honest model would "
            "be; interpretability decides whether we could ever tell. Honesty is where the epistemology of Parts 11 "
            "and 12 meets the engineering."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def oversight(self):
        head = label(r"Overseeing what we cannot check", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"debate", r"Irving, \ Christiano and Amodei \ (2018): \ two models argue, \ a human judges: \ lying should be harder to defend than truth", HUMAN),
                (r"recursive reward modeling", r"Leike et al. \ (2018): \ models help people evaluate models, \ recursively", TRUEV),
                (r"weak to strong", r"Burns et al. \ (2023): \ a strong model trained on a weak supervisor's labels often outperforms its supervisor", LOBC),
                (r"control", r"Greenblatt et al. \ (2023): \ assume a model may be untrustworthy, \ and design protocols that stay safe anyway", RISK)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "If we cannot read a model's beliefs directly, perhaps we can check its work. The problem is that we may "
            "soon need to supervise systems that know more than we do. <bookmark mark='a'/>Geoffrey Irving, Paul "
            "Christiano and Dario Amodei proposed debate: two models argue opposite sides before a human judge, in "
            "the hope that a lie is harder to defend than the truth, as in a courtroom. <bookmark mark='b'/>Jan Leike "
            "and colleagues proposed that models help people evaluate other models, recursively, so that oversight "
            "scales with capability. <bookmark mark='c'/>Collin Burns and colleagues found that a strong model "
            "trained on a weaker supervisor's labels often does better than the supervisor: some generalization "
            "survives imperfect teaching. <bookmark mark='d'/>And Ryan Greenblatt and colleagues proposed control: "
            "assume the model may be untrustworthy, and design monitoring protocols that remain safe even so. Each is "
            "an epistemology of testimony from a source wiser than its judge."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
