from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403

ABC = {"a": "#F2C14E", "b": "#F2788F", "c": "#7EC8F5"}


def column(ranking, x, y=0.6, font_size=30, head=None, color=GREY_B):
    """A ballot of three, best on top, as a column of letters in a box."""
    letters = VGroup(*[label(c, font_size=font_size, color=ABC[c]) for c in ranking]).arrange(DOWN, buff=0.28)
    box = RoundedRectangle(width=0.9, height=letters.height + 0.45, corner_radius=0.1, stroke_color=color,
                           stroke_width=2)
    letters.move_to(box)
    g = VGroup(box, letters).move_to([x, y, 0])
    if head:
        g.add(label(head, font_size=17, color=GREY_A).next_to(box, UP, buff=0.12))
    return g


class ArrowTheorem(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Arrow's theorem", r"Is there any fair way to turn everyone's rankings into one ranking for "
             r"society?", "Chapter three. Arrow's theorem.",
             lit={1950: r"Arrow", 1972: r"Arrow's Nobel", 2005: r"Geanakoplos's proofs"}, scale=("nation",),
             horizon=("a decade",))
        self.conditions()
        self.proof()
        self.rest()

    def conditions(self):
        rows = VGroup(
            label(r"a rule takes everyone's ranking of three or more options, \ and returns a ranking for society",
                  font_size=24),
            label(r"1. \ any rankings allowed \ (unrestricted domain)", font_size=24, color=RULE),
            label(r"2. \ if everyone prefers x to y, \ so does society \ (Pareto)", font_size=24, color=RULE),
            label(r"3. \ society's x against y depends only on how people rank x against y \ (independence)",
                  font_size=24, color=RULE),
            label(r"4. \ no one whose ranking always becomes society's \ (no dictator)", font_size=24, color=RULE),
            label(r"Arrow: \ no rule satisfies all four", font_size=30, color=CYCLE),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Arrow, \emph{Social Choice and Individual Values} (1951)", corner=DR, font_size=13)
        with self.voiceover(
            "Arrow asked for very little. <bookmark mark='a'/> A rule takes everyone's ranking of three or more "
            "options, and returns a ranking for society, complete and consistent. <bookmark mark='b'/> First, people "
            "may rank the options any way they like. <bookmark mark='c'/> Second, if everyone prefers x to y, so "
            "does society: the Pareto condition. <bookmark mark='d'/> Third, society's verdict on x against y depends "
            "only on how people rank x against y, not on where they put other options: independence, the condition "
            "Borda's count broke. <bookmark mark='e'/> Fourth, there is no dictator, no one person whose ranking "
            "always becomes society's. <bookmark mark='f'/> Arrow proved that no rule satisfies all four."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def proof(self):
        pv = load("pivot")
        n = pv["n"]
        base = [("a", "c", "b") if k % 2 == 0 else ("c", "a", "b") for k in range(n)]
        xs = [-5.6 + 1.5 * k for k in range(n)]
        cols = [column(base[k], xs[k], head=rf"voter {k + 1}") for k in range(n)]
        soc_rank = lambda pos: ("a", "c", "b") if pos == 2 else ("b", "a", "c")  # noqa: E731
        soc = column(soc_rank(pv["positions"][0]), 4.6, head=r"society", color=E.ACCENT)
        head = label(r"Geanakoplos's proof: \ move b from bottom to top, \ one voter at a time", font_size=25,
                     color=E.ACCENT).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"step 1: \ when everyone puts b at the top or bottom, \ so does society", font_size=21),
            label(r"start: \ everyone puts b last, \ so society does too \ (Pareto)", font_size=21),
            label(r"at the end everyone puts b first, \ so society does too: \ somewhere it jumps", font_size=21),
            label(r"the voter at whom it jumps is pivotal", font_size=22, color=CYCLE),
            label(r"step 3: \ independence makes the pivotal voter decide every other pair: \ a dictator",
                  font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "John Geanakoplos gave a short proof in 2005, and it can be watched. Take three options, a, b and c, "
            "and five voters. <bookmark mark='a'/> First a lemma: if every voter puts b either at the very top or at "
            "the very bottom, then society must too. If society put b in the middle, independence would let us raise "
            "c above a for everyone without changing any vote about b, and the social ranking would contradict "
            "itself. <bookmark mark='b'/> Now start with everyone putting b last. By Pareto, society puts b last. "
            "<bookmark mark='c'/> Move b to the top of the first voter's ranking, then the second's, and so on. When "
            "all have moved it, Pareto puts b first for society. So somewhere it jumps from bottom to top. "
            "<bookmark mark='d'/> Here it jumps at the third voter. That voter is pivotal. "
            "<bookmark mark='e'/> The rest of the proof uses independence to show that the pivotal voter alone "
            "decides how society ranks every pair: a dictator. Any rule that keeps the first three conditions has "
            "one."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(c) for c in cols], FadeIn(soc))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            for k in range(n):
                new = column(("b",) + tuple(x for x in base[k] if x != "b"), xs[k], head=rf"voter {k + 1}")
                jump = pv["positions"][k + 1] != pv["positions"][k]
                anims = [Transform(cols[k], new)]
                if jump:
                    anims.append(Transform(soc, column(soc_rank(pv["positions"][k + 1]), 4.6, head=r"society",
                                                       color=E.ACCENT)))
                self.play(*anims, run_time=1.0)
                if jump:
                    self.play(Indicate(soc, color=CYCLE, scale_factor=1.08), run_time=0.8)
                if k == pv["pivot"]:
                    vo.wait_until("d")
                    self.play(FadeIn(steps[3]), cols[k][0].animate.set_stroke(CYCLE, width=5))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.clear_scene()

    def rest(self):
        rows = VGroup(
            label(r"so something must give", font_size=27, color=E.ACCENT),
            label(r"restrict the rankings people may hold: \ single peaks, \ chapter four", font_size=24, color=RULE),
            label(r"drop independence: \ Borda and its cousins, \ open to manipulation, \ chapter five", font_size=24,
                  color=RULE),
            label(r"use more information than rankings: \ how much each gains, \ compared across people, \ chapter six",
                  font_size=24, color=RULE),
            label(r"the theorem is not that democracy is impossible, \ but that no procedure is neutral", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Geanakoplos, Econ.\ Theory 26(1) (2005)", corner=DR, font_size=13)
        with self.voiceover(
            "So something must give. <bookmark mark='a'/> One way out is to restrict the rankings people may hold, "
            "as chapter four does. <bookmark mark='b'/> Another is to drop independence, as Borda's count does, at "
            "the price of manipulation, the subject of chapter five. <bookmark mark='c'/> The third is to use more "
            "information than rankings: how much each person gains or loses, compared across people, which chapter "
            "six takes up. <bookmark mark='d'/> Arrow's theorem does not say that democracy is impossible. It says "
            "that no procedure for adding people up is neutral: every one builds in a choice."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
