from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403


class Load(VoiceoverScene):
    def construct(self):
        card_section(self, 6, r"Cognitive load", r"How much can a learner hold while learning?", marr=("how",))
        self.theory()
        self.budget()
        self.reversal()

    def theory(self):
        chips_section(self, r"Sweller's cognitive load theory", [
            (r"the limit", r"Part 19's working memory: \ a few elements at once, \ for new material", MODEL),
            (r"intrinsic load", r"how many elements the material makes the learner hold together", PERSON),
            (r"extraneous load", r"load added by the teaching itself: \ a diagram here, \ its labels over there, \ "
                                 r"search without guidance", AUTH),
            (r"the design goal", r"cut extraneous load so working memory can go to the material: \ worked examples, \ "
                                 r"integrated labels, \ one channel each for words and pictures", GOOD),
        ], "John Sweller's cognitive load theory starts from Part 19. <bookmark mark='a'/> Working memory holds a "
           "few elements at once, for new material. <bookmark mark='b'/> Intrinsic load is how many elements the "
           "material makes the learner hold together. <bookmark mark='c'/> Extraneous load is added by the teaching "
           "itself: a diagram here and its labels over there, or search without guidance. <bookmark mark='d'/> The "
           "design goal is to cut extraneous load so working memory can go to the material: worked examples, labels "
           "placed on the diagram, and one channel each for words and pictures.",
           tag=published_tag(r"Sweller (1988)"))

    def reversal(self):
        rows_section(self, r"Worked examples, \ and when they stop helping", [
            (r"the worked-example effect: \ novices who study solved problems learn more than those who solve the "
             r"same problems themselves", GOOD),
            (r"the expertise reversal effect: \ for learners who already know the method, \ the worked example is "
             r"redundant, \ and solving does better", AUTH),
            (r"so fade the support: \ full examples, \ then partial ones, \ then problems", MODEL),
            (r"the same design is wrong for different learners: \ Part 47's question, \ in the classroom", YOU),
        ], "Worked examples show the theory at work. <bookmark mark='a'/> Novices who study solved problems learn "
           "more than those who solve the same problems themselves. <bookmark mark='b'/> But for learners who "
           "already know the method, the worked example is redundant, and solving does better. That's the expertise "
           "reversal effect. <bookmark mark='c'/> So fade the support: full examples, then partial ones, then "
           "problems. <bookmark mark='d'/> The same design is wrong for different learners. It's Part 47's question, "
           "in the classroom.")

    def budget(self):
        head = heading(r"A load budget, \ schematic")
        A = axes([0.3, 4.7], [0, 6.2], x_length=5.6, y_length=3.2, xticks=None, yticks=[0, 2, 4, 6],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"elements held at once", center=[-3.3, 0.4, 0], font_size=12)
        cap = DashedLine(A.ax.c2p(0.3, 4), A.ax.c2p(4.7, 4), color=YOU, stroke_width=3)
        capl = label(r"capacity, \ about 4 (Part 19)", font_size=13, color=YOU).next_to(cap, UP, buff=0.08)
        # (intrinsic, extraneous) for: novice solving, novice studying an example, expert studying, expert solving
        cases = [(3.0, 2.2), (3.0, 0.5), (1.0, 1.4), (1.0, 0.4)]
        names = [r"novice, \ solves", r"novice, \ example", r"expert, \ example", r"expert, \ solves"]
        stacks = VGroup()
        for i, (a, b) in enumerate(cases):
            x = i + 1
            lo = Rectangle(width=0.62, height=A.ax.c2p(0, a)[1] - A.ax.c2p(0, 0)[1], fill_color=PERSON,
                           fill_opacity=0.85, stroke_width=0)
            lo.move_to(A.ax.c2p(x, 0), aligned_edge=DOWN)
            hi = Rectangle(width=0.62, height=A.ax.c2p(0, b)[1] - A.ax.c2p(0, 0)[1],
                           fill_color=AUTH if a + b > 4 else GREY_B, fill_opacity=0.85, stroke_width=0)
            hi.move_to(lo.get_top(), aligned_edge=DOWN)
            stacks.add(VGroup(lo, hi))
        lab = VGroup(*[label(t, font_size=12, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                       for i, t in enumerate(names)])
        key = VGroup(label(r"intrinsic", font_size=13, color=PERSON), label(r"extraneous", font_size=13, color=GREY_B),
                     label(r"over the limit", font_size=13, color=AUTH)).arrange(RIGHT, buff=0.35)
        key.next_to(A, UP, buff=0.55)
        rows = rows_of([
            (r"a novice solving a new kind of problem holds the goal, \ the givens and the search for a method: \ "
             r"over the limit, \ so little is left for learning the method", AUTH),
            (r"the same novice studying a worked example holds the steps, \ not the search", GOOD),
            (r"an expert has chunked the method (Part 24): \ the material costs one element, \ and reading a "
             r"redundant example is extra load", MODEL),
            (r"so the best format depends on what the learner already holds: \ the bars move as expertise grows", YOU),
            (r"the heights are illustrative; \ the theory's quantities are rarely measured this directly", GREY_B),
        ], 6.0, 18, 0.32).move_to([3.4, -0.2, 0])
        with self.voiceover(
            "Here is the theory as a budget, drawn schematically. <bookmark mark='a'/> A novice solving a new kind of "
            "problem has to hold the goal, the givens and the search for a method all at once. That's over the limit, "
            "so little capacity is left for learning the method itself. <bookmark mark='b'/> The same novice studying "
            "a worked example holds the steps, not the search, and fits. <bookmark mark='c'/> An expert has chunked "
            "the method, as Part 24 showed, so the material costs about one element, and reading a redundant example "
            "is extra load for no gain. <bookmark mark='d'/> So the best format depends on what the learner already "
            "holds, and the bars move as expertise grows. <bookmark mark='e'/> The heights are illustrative. The "
            "theory's quantities are rarely measured this directly, which is the main criticism of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(cap), FadeIn(capl), FadeIn(key), FadeIn(lab))
            for m, r, st in zip("abcd", rows[:4], stacks):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15), GrowFromEdge(st, DOWN))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
