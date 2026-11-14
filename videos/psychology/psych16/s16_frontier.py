from __future__ import annotations

from videos.psychology.psych16.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.solid()
        self.propositions()
        self.causes()
        self.rewrite()

    def card(self):
        card = chapter_card(15, r"Frontier: \ links, \ beliefs and hidden causes", r"Is human conditioning reasoning?",
                            lit={2009: r"Mitchell et al.", 2010: r"Gershman, \ Blei \& Niv"}, part=PART,
                            scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter fifteen. The frontier: links, beliefs and hidden causes."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def solid(self):
        head = heading(r"What is solid, \ and what is argued")
        left = rows_of([
            (r"what is solid", MODEL),
            (r"acquisition, \ extinction, \ recovery and renewal", WHITE),
            (r"learning tracks contingency and prediction error", WHITE),
            (r"schedules, \ matching, \ and taste aversion", WHITE),
            (r"extinction is new learning, \ bound to context", WHITE),
        ], 5.6, 26, 0.3)
        right = rows_of([
            (r"what is argued", BAD),
            (r"how reliable blocking is", WHITE),
            (r"links or computed rates of reward", WHITE),
            (r"whether human conditioning is reasoning", WHITE),
            (r"whether a fear memory can be rewritten", WHITE),
        ], 5.6, 26, 0.3)
        g = VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.4, 0])
        with self.voiceover(
            "Here's where things stand. <bookmark mark='a'/> Solid: acquisition, extinction, spontaneous recovery and "
            "renewal; learning that follows contingency and prediction error; the signatures of schedules, the "
            "matching law and taste aversion; and extinction as new learning tied to its context. "
            "<bookmark mark='b'/> Argued: how dependable blocking is; whether animals learn links or compute rates; "
            "whether conditioning in people is really reasoning; and whether a fear memory can be rewritten. The last "
            "three are the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left[0]), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in left[1:]], lag_ratio=0.8), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in right[1:]], lag_ratio=0.8), run_time=5.0)
        self.clear_scene()

    def propositions(self):
        head = heading(r"Links, \ or beliefs?")
        rows = rows_of([
            (r"2009: \ Mitchell, \ De Houwer and Lovibond: \ in people, \ associative learning is propositional", WHITE),
            (r"tell people a tone will be followed by a shock, \ and they fear it before any pairing", INHIB),
            (r"blocking in people depends on whether they believe the causes add up", CS),
            (r"and people who cannot report the contingency show little conditioning", US),
            (r"the reply: \ automatic links exist too; \ the debate is about which system does what", GREY_A),
        ], 12.4, 28, 0.4).move_to([0, -0.1, 0])
        tag = published_tag(archive.MITCHELL_2009.cite)
        with self.voiceover(
            "The first question is what conditioning is, in people. <bookmark mark='a'/> In 2009 Chris Mitchell, Jan "
            "De Houwer and Peter Lovibond argued that human associative learning isn't the stamping-in of links at "
            "all, but reasoning: people form beliefs, propositions, about what causes what. "
            "<bookmark mark='b'/> Their evidence: tell someone that a tone will be followed by a shock, and they fear "
            "the tone before a single pairing. <bookmark mark='c'/> Blocking in people depends on whether they believe "
            "that two causes add up, which you can change with instructions. <bookmark mark='d'/> And people who can't "
            "say what predicts what show little conditioning. <bookmark mark='e'/> Defenders of links reply that "
            "automatic learning plainly exists too, in animals and in fast human responses. The live question is "
            "which system does what."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def causes(self):
        head = heading(r"Extinction as inference about hidden causes")
        rows = rows_of([
            (r"2010: \ Gershman, \ Blei and Niv: \ the animal asks which hidden cause is producing what it sees", WHITE),
            (r"a sudden change, \ shocks to none: \ probably a new cause, \ so a new memory; \ the old one survives",
             INHIB),
            (r"and when the old context returns, \ so can the old cause: \ renewal, \ recovery", CONTEXT),
            (r"a prediction: \ extinguish gradually, \ thinning the shocks, \ and the old memory is revised instead", YOU),
            (r"in rats, \ gradual extinction reduced the return of fear; \ tests in people are under way", CR),
        ], 12.4, 28, 0.4).move_to([0, -0.1, 0])
        tag = published_tag(archive.GERSHMAN_2010.cite)
        with self.voiceover(
            "The second is a new account of why extinction doesn't erase. <bookmark mark='a'/> In 2010 Sam Gershman, "
            "David Blei and Yael Niv proposed that an animal is always inferring which hidden cause is producing what "
            "it experiences, like the latent states of Part 14's perceptual inference. <bookmark mark='b'/> When "
            "shocks stop abruptly, the likeliest explanation is that the world has changed, a new cause, so a new "
            "memory is started and the old one is left intact. <bookmark mark='c'/> Bring back the old context, and "
            "the old cause becomes likely again: renewal and recovery. <bookmark mark='d'/> The theory makes an "
            "unusual prediction. Make the change gradual, thinning the shocks out slowly rather than stopping them, "
            "and the animal should conclude it's the same world, slowly changing, and revise the old memory instead "
            "of filing a new one. <bookmark mark='e'/> In rats, gradual extinction did reduce the return of fear. "
            "Whether it helps patients is being tested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def rewrite(self):
        head = heading(r"Can a fear memory be rewritten?")
        rows = rows_of([
            (r"a retrieved memory may become briefly changeable before it is stored again: \ reconsolidation", WHITE),
            (r"2010: \ remind people of a fear, \ then extinguish within hours, \ and the fear stayed gone a year "
             r"later", CR),
            (r"replications have been mixed: \ some labs find it, \ others not", INHIB),
            (r"if it holds, \ extinction could erase rather than compete; \ memory's rewriting is Part 21", YOU),
        ], 12.4, 28, 0.42).move_to([0, -0.1, 0])
        tag = published_tag(archive.SCHILLER_2010.cite)
        with self.voiceover(
            "The last question is the most hopeful. <bookmark mark='a'/> When a memory is retrieved, it may become "
            "briefly changeable before it's stored again, a process called reconsolidation. "
            "<bookmark mark='b'/> In 2010 Daniela Schiller and colleagues reminded people of a conditioned fear, then "
            "ran extinction within the next few hours, and reported that the fear didn't return, even a year later. "
            "<bookmark mark='c'/> Attempts to repeat it have been mixed: some laboratories find the effect, others "
            "don't, and nobody yet knows exactly when it works. <bookmark mark='d'/> If it holds up, extinction could "
            "rewrite a fear rather than compete with it. How memories are rewritten each time they're used is "
            "Part 21."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
