from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403


class FirstTheorem(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The first welfare theorem", r"Why is a competitive equilibrium efficient, and what does that "
             r"need?", "Chapter five. The first welfare theorem.")
        self.claim()
        self.proof()
        self.assumptions()

    def claim(self):
        b = load("box")
        w = load("welfare")
        box = box_from(b, center=LEFT * 2.6 + DOWN * 0.1, width=6.2, height=5.4)
        cc = box.curve(b["cc_x"], b["cc_y"], color=CC, width=3)
        E_ = Dot(box.c2p(*b["xA"]), radius=0.1, color=WHITE)
        line = price_line(box, b["xA"], b["p"])
        side = VGroup(
            label(r"in equilibrium each trader faces the same price \\ and sets her rate of substitution equal to it",
                  font_size=22),
            MathTex(rf"MRS_{{\text{{Ana}}}} = {w['mrsA']:.3f} = MRS_{{\text{{Bo}}}}", font_size=34, color=CC),
            label(r"equal rates: \ no swap left that helps both", font_size=23, color=CC),
            label(r"the theorem: \ every competitive equilibrium \\ is Pareto efficient", font_size=26,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "In the box, the equilibrium landed on the contract curve. That wasn't luck. <bookmark mark='a'/> At "
            "the equilibrium both traders face the same price, and each trades until her own rate of substitution "
            "equals it. <bookmark mark='b'/> So their rates of substitution are equal to each other: one point oh "
            "one eight baskets a fish for both. <bookmark mark='c'/> And equal rates mean there is no swap left "
            "that both would want. <bookmark mark='d'/> That is the first fundamental theorem of welfare "
            "economics: every competitive equilibrium is Pareto efficient. Adam Smith's invisible hand, stated "
            "precisely, for any number of goods and traders."
        ) as vo:
            self.play(FadeIn(box), FadeIn(cc), FadeIn(E_))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def proof(self):
        steps = VGroup(
            label(r"suppose prices $p$ and allocation $x$ are an equilibrium, \ and some feasible $x'$ is better "
                  r"for someone \\ and worse for nobody", font_size=24),
            MathTex(r"\text{1. whoever prefers } x'_i:\quad p \cdot x'_i > p \cdot \omega_i", font_size=32),
            MathTex(r"\text{2. whoever is indifferent:}\quad p \cdot x'_i \ge p \cdot \omega_i", font_size=32),
            MathTex(r"\text{3. add them up:}\quad p \cdot \textstyle\sum_i x'_i > p \cdot \sum_i \omega_i",
                    font_size=32),
            MathTex(r"\text{4. but } x' \text{ is feasible:}\quad \textstyle\sum_i x'_i = \sum_i \omega_i", font_size=32),
            label(r"5. a contradiction: \ no such $x'$, \ so $x$ is Pareto efficient", font_size=26, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(LEFT * 0.4 + DOWN * 0.3)
        head = label(r"the proof, \ in five lines", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.4)
        why = VGroup(
            label(r"1: \ she could have afforded it \\ and didn't choose it", font_size=19, color=GREY_A),
            label(r"2: \ otherwise something a little \\ better was affordable", font_size=19, color=GREY_A),
        )
        why[0].next_to(steps[1], RIGHT, buff=0.4)
        why[1].next_to(steps[2], RIGHT, buff=0.4)
        with self.voiceover(
            "The proof takes five lines. <bookmark mark='a'/> Suppose the prices p and the allocation x are an "
            "equilibrium, and some other feasible allocation, x prime, is better for someone and worse for nobody. "
            "<bookmark mark='b'/> Anyone who strictly prefers their bundle in x prime must find it too expensive "
            "at the prices p: if they could have afforded it, they would have chosen it. <bookmark mark='c'/> "
            "Anyone who likes x prime just as well can't find it any cheaper than what they own: if they could, "
            "they could have afforded something a little better. That step needs one assumption, that people "
            "always want a little more of something. <bookmark mark='d'/> Add up over everyone: x prime costs "
            "more than everything the economy owns. <bookmark mark='e'/> But x prime is feasible: it shares out "
            "exactly what the economy owns, so it costs exactly that much. <bookmark mark='f'/> That's a "
            "contradiction, so there is no such allocation, and the equilibrium is efficient."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(why[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), FadeIn(why[1]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
            vo.wait_until("f")
            self.play(FadeIn(steps[5]))
        self.clear_scene()

    def assumptions(self):
        head = label(r"what the proof used, \ and where each fails", font_size=30, color=E.ACCENT).to_edge(UP,
                                                                                                    buff=0.4)
        rows = (
            (r"a price for everything that matters to anyone", r"smoke, \ noise, \ ideas: \ Part 15"),
            (r"everyone takes prices as given", r"market power: \ Parts 10 and 12"),
            (r"everyone knows what they are buying", r"lemons and signals: \ Part 13"),
            (r"markets for every date and every risk", r"chapter 12, \ and Part 23"),
            (r"efficient is not fair", r"who should get what: \ Parts 18 and 41"),
        )
        grid = VGroup()
        for a, b_ in rows:
            grid.add(VGroup(label(a, font_size=24), label(b_, font_size=22, color=HOLD)))
        for r in grid:
            r[1].next_to(r[0], RIGHT, buff=0.6)
        grid.arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.55)
        for r in grid:
            r[1].align_to(grid[0][1], LEFT)
        col = max(r[0].get_right()[0] for r in grid) + 0.6
        for r in grid:
            r[1].set_x(col + r[1].width / 2)
        grid.move_to(DOWN * 0.3)
        foot = label(r"Act IV is about what happens when they fail", font_size=24, color=GREY_A).to_edge(DOWN,
                                                                                                  buff=0.45)
        with self.voiceover(
            "Read the proof again for what it assumed, because each assumption is a part of this series. "
            "<bookmark mark='a'/> It used a price for everything anyone cares about. Smoke from a neighbour's "
            "fire has no price, and nothing in the proof covers it: that's Part fifteen. <bookmark mark='b'/> It "
            "assumed everyone takes prices as given. A seller who sets the price is Part ten. "
            "<bookmark mark='c'/> It assumed everyone knows what they're buying; the used-car market of Part "
            "thirteen does not. <bookmark mark='d'/> It needs markets for goods at every date and in every "
            "circumstance, which is chapter twelve. <bookmark mark='e'/> And efficient is not the same as fair: "
            "the theorem holds at whatever starting point you give it, however unequal. Who should get what is "
            "Parts eighteen and forty-one. <bookmark mark='f'/> The first welfare theorem is less a description of "
            "any economy than a list of the ways an economy can go wrong."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            for mk, r in zip("abcde", grid):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()
