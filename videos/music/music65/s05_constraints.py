from __future__ import annotations

from videos.music.music65.common import *  # noqa: F403


class Constraints(SoundScene):
    def construct(self):
        chapter(self, 4, r"Constraints", r"Can a chain be told where to end without losing its style?")
        self.problem()
        self.method()
        self.heard()

    # ------------------------------------------------------------------
    def problem(self):
        d = load("constrained")
        items = [
            (r"a chain draws one note at a time: \ it cannot plan an ending", WHITE),
            (r"ask for 32 notes ending on a long tonic under a fermata, \ with phrases ending on the tonic triad", WHITE),
            (rf"draw freely and check: \ only {100 * d['p_legal']:.2f}\% of draws pass", WHITE),
            (r"draw and throw away is Hiller's method: \ correct, \ and slow, \ and hopeless for harder constraints", WHITE),
            (r"better: \ change the chain so that it can only draw what passes, \ and otherwise keeps its odds", TUNE),
        ]
        rows_scene(self, r"the problem", items,
                   "A chain draws one note at a time, so it cannot plan an ending. <bookmark mark='b'/> Suppose we want thirty-two "
                   "notes that end, as a chorale does, on a long tonic under a fermata, with every phrase ending on a note of the "
                   "tonic chord. <bookmark mark='c'/> Draw freely and check: only "
                   f"{say(100 * d['p_legal'], 2)} per cent of draws pass. <bookmark mark='d'/> Drawing and throwing away is Hiller's "
                   "method from 1957: correct, slow, and hopeless when the constraints get harder. <bookmark mark='e'/> Better to "
                   "change the chain so that it can only draw what passes, while keeping its odds otherwise.", marks="bcde")

    # ------------------------------------------------------------------
    def method(self):
        lines = VGroup(
            label(r"count backwards first: \ for each state and each number of notes left,", font_size=20, color=WHITE),
            MathTex(r"\beta_k(s) = \sum_{x\ \text{allowed}} P(x \mid s)\, \beta_{k-1}(s')", font_size=38, color=TUNE),
            label(r"the probability that a legal ending can still be reached", font_size=19, color=GREY_A),
            label(r"then draw forwards in proportion to \ $P(x \mid s)\,\beta_{k-1}(s')$: \ never into a dead end", font_size=20, color=WHITE),
            label(r"exactly the chain's own distribution, \ conditioned on the constraints \ (Pachet and Roy, \ 2011)", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        head = label(r"Markov constraints", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The trick is to count backwards first. <bookmark mark='a'/> For every state of the chain and every number of "
            "notes still to come, <bookmark mark='b'/> compute the probability that a legal ending can still be reached from "
            "there. <bookmark mark='c'/> It needs only the chain's own probabilities, summed backwards from the end. "
            "<bookmark mark='d'/> Then draw forwards, weighting each candidate note by its probability times its chance of "
            "still ending well. The chain never walks into a dead end. <bookmark mark='e'/> And the result is exactly the "
            "chain's own distribution, conditioned on the constraints; François Pachet and Pierre Roy showed how in 2011."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("constrained")
        c = clip("constrained.two")
        r1 = tune_roll(d["free"], width=11.0, height=1.2).move_to(UP * 0.9)
        r2 = tune_roll(d["notes"], width=11.0, height=1.2).move_to(DOWN * 1.1)
        l1 = label(r"drawn freely: \ 32 notes, \ stopping wherever it stops", font_size=16, color=GREY_A).next_to(r1, UP, buff=0.12).align_to(r1, LEFT)
        l2 = label(r"drawn under the constraints", font_size=16, color=TUNE).next_to(r2, UP, buff=0.12).align_to(r2, LEFT)
        head = label(r"free and constrained, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover("Hear thirty-two notes from the same order-two chain, drawn freely, then under the constraints."):
            self.play(FadeIn(head), FadeIn(r1), FadeIn(l1), FadeIn(r2), FadeIn(l2))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"free, \ then constrained", kind="synthesized", detail=r"an order-2 chain", corner=DL, tag_corner=DR)
            snd.drive(r1, lambda m, t: m.set_opacity(1.0 if t < st["constrained"] else 0.35))
            snd.drive(r2, lambda m, t: m.set_opacity(1.0 if t >= st["constrained"] - 0.2 else 0.35))
        cp = d["copy"]
        res = label(rf"the constrained tune ends on a long C; \ its longest copied run: \ {cp['length']} notes", font_size=18, color=TUNE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The free draw stops in mid-air, on whatever note its thirty-second happened to be. The constrained one closes as "
            f"a chorale closes, on a long C, and its longest copied run is still only {say(cp['length'])} notes: the "
            "constraints shaped where it went without making it copy."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()
