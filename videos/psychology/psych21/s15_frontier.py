from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.weaken()
        self.engrams()
        self.machines()

    def card(self):
        card = chapter_card(14, r"Frontier: \ editing memory", r"Can a memory be weakened, \ found again, \ or "
                            r"protected on purpose?",
                            lit={2009: r"Kindt et al.", 2015: r"Ryan et al.", 2017: r"Kirkpatrick et al."},
                            part=PART, scale=("molecule", "mind"), marr=("how",))
        with self.voiceover("Chapter fourteen. Frontier: editing memory."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def weaken(self):
        head = heading(r"Weakening a fear by reconsolidation?")
        rows = rows_of([
            (r"Kindt, \ Soeter and Vervliet, \ 2009: \ people learnt to fear a picture paired with a shock; \ a day "
             r"later, \ propranolol before a single reminder", WHITE),
            (r"the next day their startle response to the picture was gone, \ though they still knew the "
             r"picture had meant a shock", CUE),
            (r"Brunet and colleagues, \ 2018: \ a randomised trial in post-traumatic stress disorder, \ propranolol "
             r"before recalling the trauma, \ weekly: \ larger improvement than placebo", MODEL),
            (r"other attempts have failed, \ and the conditions under which a memory reopens are not known: \ "
             r"open", LOST),
            (r"and a question beyond the science: \ which memories should anyone be allowed to weaken?", FALSE),
        ], 12.4, 25, 0.36).move_to([0, -0.2, 0])
        tag = published_tag(r"Kindt, \ Soeter \& Vervliet (2009); \ Brunet et al.\ (2018)")
        with self.voiceover(
            "Three open questions. The first: if recalling a memory reopens it, can a harmful memory be weakened? "
            "<bookmark mark='a'/> In 2009 Merel Kindt, Marieke Soeter and Bram Vervliet taught people to fear a "
            "picture that came with a mild shock. A day later, some took propranolol, a common blood-pressure drug "
            "that blocks noradrenaline, before seeing the picture once as a reminder. <bookmark mark='b'/> The next "
            "day, their startle response to the picture was gone, though they could still say that it had predicted "
            "a shock. The feeling went; the knowledge stayed. <bookmark mark='c'/> In 2018 Alain Brunet and "
            "colleagues ran a randomised trial in post-traumatic stress disorder: propranolol before recalling the "
            "trauma, once a week, improved symptoms more than placebo. <bookmark mark='d'/> But other attempts have "
            "failed, and nobody yet knows reliably when a memory reopens and when it doesn't. "
            "<bookmark mark='e'/> And if it works, there's a question that isn't scientific: which memories should "
            "anyone be allowed to weaken?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def engrams(self):
        head = heading(r"Is a forgotten memory gone, \ or lost?")
        strip = trial_strip([
            (r"mice learn a fear", label(r"tag the cells", font_size=24, color=TRACE), r"active at learning"),
            (r"block consolidation", label(r"amnesia", font_size=26, color=LOST), r"no fear to the cue"),
            (r"switch the tagged cells on with light", label(r"fear returns", font_size=24, color=MODEL), ""),
        ], frame_w=3.4, frame_h=1.1, font_size=18).move_to([0, 1.5, 0])
        rows = rows_of([
            (r"Ryan, \ Roy, \ Pignatelli, \ Arons and Tonegawa, \ 2015: \ the memory was still stored in the cells; "
             r"\ what was lost was the way to reach it", WHITE),
            (r"the old question of chapter 2, \ decay or interference, \ asked of cells: \ is forgetting a loss of "
             r"storage or of access?", CUE),
            (r"open: \ how much ordinary forgetting is of this kind, \ and whether it can be reversed in people", LOST),
        ], 12.4, 25, 0.32).to_edge(DOWN, buff=0.65)
        tag = published_tag(r"Ryan et al.\ (2015)")
        with self.voiceover(
            "The second question goes back to chapter two: when a memory is forgotten, is it gone, or just lost? "
            "<bookmark mark='a'/> In 2015 Tomás Ryan, Dheeraj Roy, Michele Pignatelli, Autumn Arons and Susumu "
            "Tonegawa tagged the cells active as mice learnt a fear, the engram cells of Part 5. Then they gave the "
            "mice a drug that blocks consolidation, and the mice behaved as if they had forgotten. But switching the "
            "tagged cells on with light brought the fear right back. <bookmark mark='b'/> The memory was still "
            "stored. What had been lost was the route to it. <bookmark mark='c'/> It's the old question of decay "
            "or interference, now asked of cells: is forgetting a loss of storage, or of access? "
            "<bookmark mark='d'/> How much ordinary forgetting is of this kind, and whether it could ever be "
            "reversed in people, is open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(strip))
            vo.wait_until("a")
            self.play(Indicate(strip))
            for m, r in zip("bcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def machines(self):
        head = heading(r"Forgetting in machines")
        eq = MathTex(r"L(\theta) = L_{\text{new}}(\theta) + \sum_i \frac{\lambda}{2} F_i\,(\theta_i - "
                     r"\theta^{*}_{\text{old}, i})^2", font_size=36).move_to([0, 1.8, 0])
        eq[0][6:15].set_color(CUE)
        rows = rows_of([
            (r"chapter 4's penguin, \ at scale: \ a network trained on task after task forgets the earlier ones", LOST),
            (r"Kirkpatrick and colleagues, \ 2017: \ \emph{elastic weight consolidation}: \ make the weights that "
             r"mattered for old tasks stiff, \ in proportion to their Fisher information $F_i$", MODEL),
            (r"the brain's answer, \ replay, \ is the other main approach: \ keep or regenerate old examples, \ and "
             r"interleave them", TRACE),
            (r"and the reverse problem: \ \emph{unlearning}, \ removing what a model learnt from data it should not "
             r"keep, \ without retraining from scratch", FALSE),
            (r"open: \ whether the brain stiffens synapses as this penalty does, \ and whether forgetting on "
             r"purpose can be made reliable in either", CUE),
        ], 12.4, 24, 0.32).to_edge(DOWN, buff=0.65)
        tag = published_tag(r"Kirkpatrick et al.\ (2017)")
        with self.voiceover(
            "And the third question is about machines. <bookmark mark='a'/> Chapter four's penguin, at scale: a "
            "network trained on one task after another forgets the earlier ones. <bookmark mark='b'/> In 2017 James "
            "Kirkpatrick and colleagues at DeepMind proposed elastic weight consolidation. When learning a new task, "
            "add a penalty for moving the weights that mattered for old tasks, each in proportion to its Fisher "
            "information, the curvature of the old task's likelihood. It was explicitly inspired by synaptic "
            "consolidation in the brain. <bookmark mark='c'/> The brain's other answer, replay, is the other main "
            "approach in machine learning: keep or regenerate old examples and mix them in. "
            "<bookmark mark='d'/> And machines face the reverse problem too. Unlearning means removing what a model "
            "learnt from data it shouldn't keep, without retraining from the beginning. "
            "<bookmark mark='e'/> Open: whether real synapses stiffen the way this penalty does, and whether "
            "forgetting on purpose can be made reliable, in brains or machines."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(rows[1]))
            for m, r in zip("cde", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
