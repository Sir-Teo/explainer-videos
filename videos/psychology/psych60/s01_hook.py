from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.question()
        self.objectives()

    def story(self):
        rows_section(self, r"A psychologist's machine", [
            (r"1958: \ the Perceptron, \ a learning machine, \ published in \emph{Psychological Review} by a "
             r"psychologist, \ Frank Rosenblatt", WHITE),
            (r"reinforcement learning came from Pavlov and Thorndike (Parts 16 and 17); \ for decades AI borrowed "
             r"from psychology", MODEL),
            (r"1966: \ ELIZA, \ a script that turned statements into questions; \ Weizenbaum was dismayed by how "
             r"readily its users confided in it", PERSON),
            (r"now the debt runs both ways: \ language models sit psychology's tests, \ are proposed as models of "
             r"the mind, \ and are used as advisers, \ helpers and stand-in participants", AUTH),
            (r"each of those uses is a psychological claim; \ this part tests each with the tools of the previous "
             r"fifty-nine", YOU),
        ], "In 1958 a learning machine called the Perceptron was published in Psychological Review, by a "
           "psychologist, Frank Rosenblatt. <bookmark mark='a'/> That's where this part begins. <bookmark mark='b'/> "
           "Reinforcement learning came from Pavlov and Thorndike, Parts 16 and 17. For decades artificial "
           "intelligence borrowed from psychology. <bookmark mark='c'/> In 1966 Joseph Weizenbaum's ELIZA turned "
           "people's statements into questions with a simple script, and Weizenbaum was dismayed by how readily its "
           "users confided in it. <bookmark mark='d'/> Now the debt runs both ways. Language models sit psychology's "
           "tests, are proposed as models of the mind, and are used as advisers, helpers and stand-in participants. "
           "<bookmark mark='e'/> Each of those uses is a psychological claim, and this part tests each one with the "
           "tools of the previous fifty-nine.", tag=historical_tag(r"Rosenblatt (1958)"))

    def question(self):
        rows_section(self, r"Today: \ what can psychology and artificial intelligence now tell each other?", [
            (r"machines as models of minds, \ and as subjects of psychology's tests", SYMP),
            (r"the traps: \ contamination, \ prompts, \ one model is not a sample", MODEL),
            (r"people with machines: \ trust, \ persuasion, \ care, \ stand-in participants", PERSON),
            (r"screens and well-being, \ and what machines lack", GOOD),
        ], "So this part asks: what can psychology and artificial intelligence now tell each other? "
           "<bookmark mark='a'/> Machines as models of minds, and as subjects of psychology's tests. "
           "<bookmark mark='b'/> The traps: contamination, prompts, and the fact that one model is not a sample. "
           "<bookmark mark='c'/> People with machines: trust, persuasion, care, and stand-in participants. "
           "<bookmark mark='d'/> And screens and well-being, and what machines lack.", font_size=27, buff=0.48)

    def objectives(self):
        head = VGroup(label(r"Part 60", font_size=34, color=GREY_B), label(r"Minds and Machines", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"judge a network as a model of the mind: \ behaviour matched is not mechanism shared",
            r"test a machine without contamination or pseudo-replication",
            r"treat a benchmark as a test: \ validity, \ item response theory, \ sample size",
            r"predict how people rely on, \ trust and are persuaded by machines",
            r"say where silicon samples fail, \ and weigh the screens dispute",
            r"state what a science of machine behaviour needs from psychology",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 60 of Psychology, Built: minds and machines. <bookmark mark='a'/> We'll judge a network as "
            "a model of the mind, and see why behaviour matched is not mechanism shared. We'll test a machine "
            "without contamination or pseudo-replication. We'll treat a benchmark as a test, with validity, item "
            "response theory and sample size. We'll predict how people rely on, trust and are persuaded by machines. "
            "We'll say where silicon samples fail, and weigh the dispute about screens. And we'll state what a "
            "science of machine behaviour needs from psychology."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
