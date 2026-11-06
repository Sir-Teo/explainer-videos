from __future__ import annotations

from videos.philosophy.philosophy13.common import *  # noqa: F403

SMALL, BIG, YOU = "#F2A65A", "#6FB7FF", "#FFD166"


def people(n: int, cols: int, center, size=0.14, gap=0.04, color=GREY_B) -> VGroup:
    g = VGroup()
    for i in range(n):
        r, c = divmod(i, cols)
        g.add(Square(side_length=size, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to(
            [c * (size + gap), -r * (size + gap), 0]))
    return g.move_to(center)


class Anthropic(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Observers and doom", r"What does your own existence tell you?", lit=(1983,),
                            part=PART)
        with self.voiceover("Chapter twelve. Observers and doom."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.selection()
        self.toy()
        self.doomsday()
        self.sia()
        self.presumptuous()
        self.finetuning()

    def selection(self):
        head = label(r"Observation selection", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        net = VGroup(*[Line([-4.0 + i * 0.5, 1.6, 0], [-4.0 + i * 0.5, -1.6, 0], color=GREY_C, stroke_width=2)
                       for i in range(9)],
                     *[Line([-4.0, 1.6 - i * 0.5, 0], [0.0, 1.6 - i * 0.5, 0], color=GREY_C, stroke_width=2)
                       for i in range(7)])
        fish = VGroup(*[Ellipse(width=0.8, height=0.3, color=BET, fill_opacity=0.6).move_to(p)
                        for p in ([-3.2, 0.9, 0], [-1.5, -0.4, 0], [-0.8, 1.1, 0])])
        small = VGroup(*[Ellipse(width=0.25, height=0.1, color=GREY_B, fill_opacity=0.6).move_to(p)
                         for p in ([-3.3, -2.1, 0], [-2.2, -2.5, 0], [-1.1, -2.2, 0], [-0.3, -2.6, 0])])
        rows = stack([(r"Eddington's net: \ every fish caught is over 2 inches", WHITE),
                      (r"so the sea has no small fish?", BAD),
                      (r"no: \ the net could catch nothing smaller", OK),
                      (r"we are the catch: \ every observer finds conditions fit for observers", GOAL),
                      (r"Carter \ (1974): \ the anthropic principle", GREY_A)], font_size=22, aligned_edge=LEFT,
                     width=5.8).move_to([3.9, 0.0, 0])
        with self.voiceover(
            "Evidence can be filtered by the way it reaches us. <bookmark mark='a'/>Arthur Eddington's example: a "
            "fisherman's net has a two-inch mesh, and every fish he catches is longer than two inches. "
            "<bookmark mark='b'/>Should he conclude that the sea has no small fish? <bookmark mark='c'/>No: his net "
            "could not have caught them. <bookmark mark='d'/>We are in the same position about our own existence. "
            "Every observer finds herself in conditions that allow observers. <bookmark mark='e'/>Brandon Carter "
            "called this the anthropic principle. How should it enter our credences?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(net), FadeIn(fish), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(small), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            for mk, r in zip("de", rows[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def toy(self):
        head = label(r"Two toy universes", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sm = people(10, 5, [-4.2, 1.0, 0], color=SMALL)
        bg = people(1000, 50, [2.4, 0.4, 0], size=0.1, gap=0.03, color=BIG)
        sl = label(r"small: \ 10 people", font_size=22, color=SMALL).next_to(sm, DOWN, buff=0.3)
        bl = label(r"big: \ 1{,}000 people", font_size=22, color=BIG).next_to(bg, DOWN, buff=0.25)
        coin = label(r"a fair coin decides which universe exists", font_size=24, color=BET).next_to(head, DOWN,
                                                                                                    buff=0.25)
        you = label(r"you learn: \ your birth rank is 7", font_size=24, color=YOU).to_edge(DOWN, buff=0.4)
        rings = VGroup(SurroundingRectangle(sm[6], color=YOU, buff=0.03),
                       SurroundingRectangle(bg[6], color=YOU, buff=0.02))
        with self.voiceover(
            "A toy model makes the question exact. <bookmark mark='a'/>A fair coin decides which of two universes "
            "exists. <bookmark mark='b'/>The small one will contain ten people in all; <bookmark mark='c'/>the big "
            "one a thousand. <bookmark mark='d'/>You find yourself existing, and you learn that you are the seventh "
            "person ever born. Which universe are you in?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(coin))
            vo.wait_until("b")
            self.play(FadeIn(sm), FadeIn(sl))
            vo.wait_until("c")
            self.play(FadeIn(bg, lag_ratio=0.001), FadeIn(bl), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(you), Create(rings))
        self.clear_scene()

    def doomsday(self):
        d = load("doomsday")
        head = label(r"The self-sampling assumption, \ and doom", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ssa = label(r"SSA: \ reason as if you were a random sample from the observers in your world", font_size=24,
                    color=CRED).next_to(head, DOWN, buff=0.3)
        toy = MathTex(r"P(\text{small} \mid \text{rank } 7) = \frac{\tfrac12 \cdot \tfrac{1}{10}}{\tfrac12 \cdot "
                      r"\tfrac{1}{10} + \tfrac12 \cdot \tfrac{1}{1000}} \approx 0.990", font_size=32).next_to(
            ssa, DOWN, buff=0.4)
        real = VGroup(
            label(r"now humanity: \ about $10^{11}$ people born so far", font_size=24),
            label(r"doom soon: \ $2 \times 10^{11}$ ever; \ \ doom late: \ $2 \times 10^{14}$ ever; \ \ prior "
                  r"$\tfrac12$ each", font_size=22, color=GREY_A),
            MathTex(rf"P(\text{{doom soon}} \mid \text{{your rank}}) = {d['ssa_soon']:.3f}", font_size=34,
                    color=BAD)).arrange(DOWN, buff=0.22).next_to(toy, DOWN, buff=0.5)
        bars = bar_row([d["prior_soon"], d["ssa_soon"]], [r"prior: \ doom soon", r"after SSA"], [GREY_B, BAD],
                       width=4.0, font_size=22, vmax=1.0, fmt=lambda v: f"{v:.3f}").to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "One answer is the self-sampling assumption, set out by Nick Bostrom. <bookmark mark='a'/>Reason as if "
            "you were a random sample from the observers in your world. <bookmark mark='b'/>Then being seventh is "
            "a one in ten chance in the small universe and a one in a thousand chance in the big one, and you should "
            "be ninety nine percent sure that you are in the small one. <bookmark mark='c'/>Now replace the toys "
            "with humanity. About a hundred billion people have been born. Suppose humanity will total either two "
            "hundred billion, doom soon, or two hundred trillion, doom late, and give each a half. "
            "<bookmark mark='d'/>The same calculation makes doom soon ninety nine point nine percent likely. "
            "<bookmark mark='e'/>This is the Doomsday argument of Brandon Carter and John Leslie: from your birth "
            "rank alone, it seems, you can predict that humanity will end soon."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ssa))
            vo.wait_until("b")
            self.play(Write(toy))
            vo.wait_until("c")
            self.play(FadeIn(real[0]), FadeIn(real[1]))
            vo.wait_until("d")
            self.play(FadeIn(real[2]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r) for r in bars], lag_ratio=0.3))
        self.clear_scene()

    def sia(self):
        d = load("doomsday")
        head = label(r"The self-indication assumption", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sia = label(r"SIA: \ that you exist at all favours worlds with more observers, \ in proportion", font_size=24,
                    color=CRED).next_to(head, DOWN, buff=0.3)
        steps = VGroup(
            MathTex(r"\text{1. existing:}\quad \tfrac12 \cdot 10 \;:\; \tfrac12 \cdot 1000 \;\Rightarrow\; "
                    r"P(\text{small}) \approx 0.0099", font_size=30),
            MathTex(r"\text{2. rank } 7:\quad 0.0099 \cdot \tfrac{1}{10} \;:\; 0.9901 \cdot \tfrac{1}{1000} "
                    r"\;\Rightarrow\; P(\text{small}) = \tfrac12", font_size=30),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(sia, DOWN, buff=0.45)
        bars = bar_row([d["prior_soon"], d["sia_prior_soon"], d["sia_soon"]],
                       [r"prior: \ doom soon", r"after existing (SIA)", r"after your rank"], [GREY_B, BIG, OK],
                       width=4.0, font_size=22, vmax=1.0, fmt=lambda v: f"{v:.3f}").next_to(steps, DOWN, buff=0.5)
        foot = label(r"under SIA the Doomsday shift cancels exactly", font_size=25, color=GOAL).to_edge(DOWN,
                                                                                                    buff=0.35)
        with self.voiceover(
            "The rival is the self-indication assumption. <bookmark mark='a'/>The fact that you exist at all is "
            "evidence for worlds with more observers in them, in proportion to their number. "
            "<bookmark mark='b'/>First, update on existing: the big universe has a hundred times as many people, "
            "so it becomes a hundred times likelier. <bookmark mark='c'/>Then update on being seventh, by the "
            "self-sampling rule. The two factors of a hundred cancel, and you are back at a half. "
            "<bookmark mark='d'/>For humanity's numbers the Reasoner gets the same: doom soon falls to a tenth of a "
            "percent on existing, then returns to exactly a half on learning your rank. "
            "<bookmark mark='e'/>Under the self-indication assumption, the Doomsday argument vanishes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sia))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in bars], lag_ratio=0.3))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def presumptuous(self):
        d = load("doomsday")
        head = label(r"The presumptuous philosopher \ (Bostrom, \ 2002)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        rows = stack([
            (r"two cosmologies, \ equally supported by physics", WHITE),
            (r"$T_1$: \ a trillion observers; \ \ $T_2$: \ a thousand times more", WHITE),
            (r"the physicists plan an experiment to decide", GREY_A),
            (rf"the philosopher: \ `no need: \ by SIA, \ $T_2$ is {d['presumptuous_factor']:,.0f} times likelier'"
             .replace(",", "{,}"), BAD),
            (r"SIA wins against Doomsday, \ and seems absurd here", GOAL),
            (r"SSA's own trouble: \ which observers count, \ the \textit{reference class}?", GREY_A),
        ], font_size=24, buff=0.3, width=12.4).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "But the self-indication assumption has a price of its own, which Bostrom called the presumptuous "
            "philosopher. <bookmark mark='a'/>Physics leaves two cosmological theories equally well supported. "
            "<bookmark mark='b'/>On the first there are a trillion observers; on the second a thousand times more. "
            "<bookmark mark='c'/>The physicists propose an expensive experiment to decide between them. "
            "<bookmark mark='d'/>The philosopher says: don't bother; by the self-indication assumption, the second "
            "theory is a thousand times likelier already. <bookmark mark='e'/>That seems absurd. So the assumption "
            "that disarms Doomsday makes armchair cosmology too easy. <bookmark mark='f'/>And the self-sampling "
            "assumption has its own problem: random among which observers? Humans, mammals, minds? The answer "
            "changes the prediction. This is the reference class problem, again."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def finetuning(self):
        head = label(r"Fine-tuning", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"if the constants of physics were slightly different, \ there would be no chemistry, \ no observers",
             WHITE),
            (r"three explanations: \ chance, \ design, \ or many universes with varied constants", GREY_A),
            (r"SIA: \ existence favours many universes \ (more observers)", BIG),
            (r"White \ (2000): \ `this universe is fit for life' is not made likelier by others existing", SMALL),
            (r"Hacking: \ the inverse gambler's fallacy", GREY_A),
            (r"the same tools, \ the same open question", GOAL),
        ], font_size=23, buff=0.3, width=12.4).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The same reasoning meets cosmology's biggest question. <bookmark mark='a'/>If several constants of "
            "physics were slightly different, there would be no chemistry and no observers. <bookmark mark='b'/>Is "
            "that luck, design, or a sign of many universes with varied constants, of which ours is one of the few "
            "that can be observed? <bookmark mark='c'/>The self-indication assumption favours many universes, since "
            "they hold more observers. <bookmark mark='d'/>Roger White argued that the existence of other universes "
            "does not make it any likelier that this universe is fit for life, <bookmark mark='e'/>and that to "
            "think so is what Ian Hacking called the inverse gambler's fallacy. <bookmark mark='f'/>The tools of "
            "this part make the question precise. They do not yet settle it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
