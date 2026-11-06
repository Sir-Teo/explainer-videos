from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Common(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Common knowledge", r"What did the father's sentence add?", lit=(1969, 1976),
                            part=PART)
        with self.voiceover("Chapter four. Common knowledge."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.tower()
        self.reach()
        self.convention()
        self.ritual()

    def tower(self):
        d = load("common")
        head = label(r"Everyone knows, \ everyone knows that everyone knows, \ \dots", font_size=30,
                     color=CONN).to_edge(UP, buff=0.35)
        defs = VGroup(MathTex(r"E\,\varphi = K_{\text{Ann}}\varphi \land K_{\text{Bob}}\varphi \land K_{\text{Cy}}"
                              r"\varphi", font_size=32),
                      MathTex(r"E^{2}\varphi = E\,E\,\varphi, \qquad E^{3}\varphi = E\,E\,E\,\varphi, \quad \dots",
                              font_size=32),
                      MathTex(r"C\,\varphi = E\varphi \land E^{2}\varphi \land E^{3}\varphi \land \cdots", font_size=36,
                              color=COMMON)).arrange(DOWN, buff=0.3).move_to([0, 1.2, 0])
        hd = [label(r"muddy children", font_size=21, color=P.CLAIM),
              label(r"`someone is muddy': \ deepest $E^k$ before the father speaks", font_size=21, color=P.CLAIM),
              label(r"common?", font_size=21, color=P.CLAIM)]
        rows = []
        for key, name in (("100", r"one \ (100)"), ("110", r"two \ (110)"), ("111", r"three \ (111)")):
            r = d[key]
            rows.append([label(name, font_size=21), label(rf"$E^{{{r['depth']}}}$" if r["depth"] else r"not even $E$",
                                                          font_size=22),
                         mark(r["common"], 26)])
        grid = ValueGrid(hd, rows, col_w=[2.8, 6.4, 1.8], cell_h=0.52, font_size=21).move_to([0, -1.5, 0])
        foot = label(r"with $k$ muddy children, \ $E^{k-1}$ held already: \ the father added the rest, \ all the way "
                     r"up", font_size=23, color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "So what did the father's sentence add? <bookmark mark='a'/>Say that everyone knows phi when each child "
            "knows it. Everyone knows that everyone knows is E twice, and so on. <bookmark mark='b'/>Common knowledge "
            "is the whole infinite tower at once: everyone knows, and everyone knows that everyone knows, and so on "
            "for ever. <bookmark mark='c'/>The Reasoner measures how high the tower stood before the father spoke. "
            "With one muddy child, not even everyone knew that someone was muddy: the muddy child saw only clean "
            "faces. With two, everyone knew it, but not that everyone knew it. With three, E squared held, but not "
            "E cubed. In no case was it common knowledge. <bookmark mark='d'/>With k muddy children, the tower "
            "already stood k minus one storeys high. The father's sentence added every storey above."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defs[0]), FadeIn(defs[1]))
            vo.wait_until("b")
            self.play(FadeIn(defs[2]))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(3)], lag_ratio=0.6), run_time=5)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def reach(self):
        head = label(r"Common knowledge as reachability", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        g = muddy_cube(scale=2.0, center=[-2.8, -0.5, 0], radius=0.32, font_size=20)
        act = Circle(radius=0.42, color=COMMON, stroke_width=3).move_to(g.world[(1, 1, 0)])
        bad = Circle(radius=0.42, color=BAD, stroke_width=4).move_to(g.world[(0, 0, 0)])
        path = VGroup(Line(g.pos[(1, 1, 0)], g.pos[(0, 1, 0)], color=COMMON, stroke_width=8, stroke_opacity=0.6),
                      Line(g.pos[(0, 1, 0)], g.pos[(0, 0, 0)], color=COMMON, stroke_width=8, stroke_opacity=0.6))
        rows = VGroup(
            label(r"$C\varphi$ at $w$: \ $\varphi$ holds at every world reachable from $w$", font_size=23),
            label(r"by any chain of steps, \ along any agent's lines", font_size=23, color=GREY_A),
            label(r"from 110: \ Ann's line to 010, \ Bob's line to 000", font_size=23, color=COMMON),
            label(r"at 000 nobody is muddy: \ so not common knowledge", font_size=23, color=BAD),
            label(r"the father deletes 000: \ now every world reachable from 110 has a muddy child", font_size=23,
                  color=OK),
            VGroup(label(r"Aumann (1976): \ common knowledge = the event contains", font_size=20, color=GREY_B),
                   label(r"the actual cell of the \textit{meet} of the partitions", font_size=20, color=GREY_B)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08)).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        for r in rows:
            if r.width > 6.6:
                r.width = 6.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "There is a picture of common knowledge. <bookmark mark='a'/>Phi is common knowledge at a world when phi "
            "holds at every world you can reach from it, <bookmark mark='b'/>by any chain of steps, along anyone's "
            "lines. Each step is one more storey of 'knows that'. <bookmark mark='c'/>From one one zero, Ann's line "
            "leads to zero one zero, and from there Bob's line leads to zero zero zero. <bookmark mark='d'/>At zero "
            "zero zero, nobody is muddy. So before the father spoke, 'someone is muddy' was not common knowledge: "
            "Ann thinks Bob might think that nobody is muddy. <bookmark mark='e'/>The father's announcement deletes "
            "zero zero zero, and with it every chain that reached it. <bookmark mark='f'/>Robert Aumann gave the "
            "definition its exact form in 1976, in terms of partitions: an event is common knowledge when it contains "
            "the whole cell of the actual world in the finest partition coarser than everyone's, the meet."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(act))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(path[0]), FadeIn(rows[2]))
            self.play(Create(path[1]))
            vo.wait_until("d")
            self.play(Create(bad), FadeIn(rows[3]))
            vo.wait_until("e")
            gone = [e for k, e in g.edge.items() if (0, 0, 0) in (k[1], k[2])]
            self.play(FadeOut(g.world[(0, 0, 0)]), FadeOut(bad), FadeOut(path[1]), *[FadeOut(e) for e in gone],
                      FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def convention(self):
        hc = history_card(1969, r"David Lewis", r"\textit{Convention}", width=4.4, color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            label(r"why does everyone drive on the left in Britain?", font_size=25),
            label(r"each drives on the left because she expects the others to,", font_size=23, color=GREY_A),
            label(r"and expects them to expect her to, \ and so on", font_size=23, color=GREY_A),
            label(r"a convention: \ a regularity sustained by common knowledge of expectations", font_size=25,
                  color=COMMON),
            label(r"so too: \ money, \ language, \ meeting times, \ a public announcement in a crowded square",
                  font_size=22, color=GREY_B),
            label(r"and anything that needs it must find a way to create it", font_size=24,
                  color=GOAL)).arrange(DOWN, buff=0.3).move_to([0, -0.5, 0])
        with self.voiceover(
            "The idea first came from philosophy. <bookmark mark='a'/>David Lewis, in his book Convention of 1969, "
            "asked why everyone in Britain drives on the left. <bookmark mark='b'/>Not because a law makes each driver "
            "want to; because each expects the others to, <bookmark mark='c'/>and expects them to expect her to, and "
            "so on up. <bookmark mark='d'/>A convention, Lewis argued, is a regularity sustained by common knowledge "
            "of such expectations. <bookmark mark='e'/>Money, language, meeting times, and the power of saying "
            "something in public all work the same way. <bookmark mark='f'/>And anything that needs common "
            "knowledge must find a way to create it. The next chapter shows that, in one important setting, no way "
            "exists."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def ritual(self):
        hc = history_card(2001, r"Michael Chwe", r"\textit{Rational Ritual}", width=4.6, color=HIST).to_corner(UL,
                                                                                                          buff=0.35)
        circle_ = VGroup(*[Dot(1.4 * np.array([np.cos(a), np.sin(a), 0]) + np.array([-3.6, -0.6, 0]), radius=0.12,
                               color=COMMON) for a in np.linspace(0, TAU, 13)[:-1]])
        cl = label(r"facing inward: \ each sees that all see", font_size=20, color=GREY_A).next_to(circle_, DOWN,
                                                                                                  buff=0.3)
        rows = VGroup(
            label(r"rituals, \ rallies, \ town meetings \ make information common knowledge", font_size=23),
            label(r"you hear the message, \ and see everyone else hear it", font_size=23, color=GREY_A),
            label(r"Chwe: \ goods that people buy because others do \ advertise on the most-watched broadcasts",
                  font_size=22, color=GOAL),
            label(r"where an audience knows that it is an audience", font_size=22, color=GREY_A),
            label(r"and a revolt needs it: \ everyone may hate the ruler, \ but nobody moves first", font_size=22,
                  color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        for r in rows:
            if r.width > 6.0:
                r.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([2.9, -0.5, 0])
        with self.voiceover(
            "Common knowledge also explains some puzzling social behaviour. <bookmark mark='a'/>Michael Chwe, in "
            "Rational Ritual, argued that rituals, rallies and town meetings exist to make things common knowledge. "
            "People often gather in a circle, facing inward, so that each can see that everyone else sees. "
            "<bookmark mark='b'/>You hear the message, and you see everyone hear it. <bookmark mark='c'/>Chwe "
            "found that products people buy because others buy them tend to be advertised on the most-watched "
            "broadcasts, <bookmark mark='d'/>where the audience knows that it is an audience. "
            "<bookmark mark='e'/>And a revolt needs common knowledge: everyone may privately hate the ruler, but "
            "nobody wants to be the first to move, until something public makes the shared hatred common knowledge."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in circle_], lag_ratio=0.1), FadeIn(cl), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

