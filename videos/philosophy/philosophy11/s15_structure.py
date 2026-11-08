from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class Structure(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"The structure of justification", r"Where do reasons end?", lit=(), part=PART)
        with self.voiceover("Chapter fourteen. The structure of justification."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.price()
        self.shapes()
        self.coherence()

    def price(self):
        d = load("regress")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.4, width=3.6, font_size=21,
                       center=[0, -0.45, 0], title=r"The Price List: \ Agrippa's regress")
        assert d["mcs"] == [["R1"], ["R2"], ["R3"], ["R4"]]
        positions = [(("R1",), r"foundationalism", r"some beliefs are basic"),
                     (("R2",), r"coherentism", r"a web of mutual support"),
                     (("R3",), r"infinitism", r"reasons without end (Klein)"),
                     (("R4",), r"skepticism", r"nothing is justified")]
        with self.voiceover(
            "Agrippa's trilemma, from the start of Part 10, returns as a Price List. <bookmark mark='a'/>Four claims. "
            "Every justified belief is justified by another belief. No belief is justified by a circle of reasons. "
            "No infinite chain of reasons justifies. And some of our beliefs are justified. <bookmark mark='b'/>The "
            "Reasoner confirms they cannot all be true, and that each one alone can be given up. Four positions. "
            "<bookmark mark='c'/>Foundationalism gives up the first: some beliefs are basic, justified without resting "
            "on others. <bookmark mark='d'/>Coherentism gives up the second: beliefs support one another, as a web. "
            "<bookmark mark='e'/>Infinitism, defended by Peter Klein, gives up the third: the chain of reasons is "
            "endless, and that is fine. <bookmark mark='f'/>And the skeptic gives up the last."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=2.4)
                self.play(*anims)
        self.clear_scene()

    def shapes(self):
        head = label(r"Three shapes of reasons", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        # foundations: a pyramid of support resting on basic beliefs
        base = VGroup(*[Square(side_length=0.4, color=JUST, fill_opacity=0.6) for _ in range(4)]).arrange(
            RIGHT, buff=0.1)
        mid = VGroup(*[Square(side_length=0.4, color=BEL, fill_opacity=0.3) for _ in range(3)]).arrange(RIGHT,
                                                                                                    buff=0.1)
        top = VGroup(*[Square(side_length=0.4, color=BEL, fill_opacity=0.3) for _ in range(2)]).arrange(RIGHT,
                                                                                                    buff=0.1)
        pyr = VGroup(top, mid, base).arrange(DOWN, buff=0.1).move_to([-4.6, 0.5, 0])
        pl = VGroup(label(r"foundations", font_size=24, color=JUST),
                    label(r"basic: \ experience, \ self-evidence", font_size=19, color=GREY_A)).arrange(
            DOWN, buff=0.1).next_to(pyr, DOWN, buff=0.3)
        # coherence: a web
        pts = [np.array([np.cos(a), np.sin(a), 0]) * 1.0 + np.array([0, 0.5, 0]) for a in
               np.linspace(0, TAU, 7)[:-1]]
        web = VGroup(*[Line(pts[i], pts[j], color=BEL, stroke_width=1.5) for i in range(6) for j in range(i + 1, 6)
                       if (j - i) in (1, 2, 5)], *[Dot(p, radius=0.09, color=BEL) for p in pts])
        wl = VGroup(label(r"a web", font_size=24, color=BEL),
                    label(r"Neurath's boat: \ rebuilt at sea, \ plank by plank", font_size=19,
                          color=GREY_A)).arrange(DOWN, buff=0.1).next_to(web, DOWN, buff=0.3)
        # infinitism: a chain fading out
        chain = VGroup(*[Dot([4.0 + 0.0 * k, 1.6 - 0.45 * k, 0], radius=0.09, color=SKEP).set_opacity(1 - 0.17 * k)
                         for k in range(6)])
        arrows = VGroup(*[Arrow(chain[k + 1].get_center(), chain[k].get_center(), buff=0.1, color=SKEP,
                                stroke_width=2, max_tip_length_to_length_ratio=0.3).set_opacity(1 - 0.17 * k)
                          for k in range(5)])
        dots = label(r"$\vdots$", font_size=28, color=SKEP).next_to(chain, DOWN, buff=0.05).set_opacity(0.4)
        il = VGroup(label(r"an endless chain", font_size=24, color=SKEP),
                    label(r"each reason has a reason", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.1).move_to(
            [4.2, pl.get_y(), 0])
        foot = VGroup(label(r"foundations: \ how can experience, \ not itself a belief, \ justify a belief?",
                            font_size=21, color=GREY_A),
                      label(r"coherence: \ a consistent fairy tale coheres too: \ why should coherence track truth?",
                            font_size=21, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Picture the three answers that keep justification. <bookmark mark='a'/>Foundationalism is a pyramid: "
            "most beliefs rest on others, but at the bottom lie basic beliefs, justified by experience or by being "
            "self-evident. Descartes was one kind of foundationalist; most empiricists were another. "
            "<bookmark mark='b'/>Coherentism is a web. Otto Neurath compared us to sailors who must rebuild their "
            "ship on the open sea, plank by plank, never able to put it in dry dock and start from the bottom. "
            "<bookmark mark='c'/>Infinitism is an endless chain, each reason backed by another, receding forever. "
            "<bookmark mark='d'/>Each has its classic problem. Foundations: how can an experience, which is not "
            "itself a belief, justify one? Coherence: a consistent fairy tale coheres as well as the truth. Why "
            "should coherence be a guide to truth at all? The Reasoner can test that last question."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(FadeIn(base), FadeIn(mid), FadeIn(top), lag_ratio=0.4), FadeIn(pl))
            vo.wait_until("b")
            self.play(Create(web), FadeIn(wl), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(c, a)) for c, a in zip(chain, arrows)], lag_ratio=0.3),
                      FadeIn(dots), FadeIn(il), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def coherence(self):
        d = load("coherence")
        head = label(r"Does coherence track truth?", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        ms = VGroup(MathTex(r"C_{\text{Shogenji}} = \frac{P(A_1 \land A_2 \land A_3)}{P(A_1)P(A_2)P(A_3)}",
                            font_size=28),
                    MathTex(r"C_{\text{overlap}} = \frac{P(A_1 \land A_2 \land A_3)}{P(A_1 \lor A_2 \lor A_3)}",
                            font_size=28)).arrange(DOWN, buff=0.25).move_to([-3.9, 1.8, 0])
        hd = [label(r"", font_size=20), label(r"Shogenji", font_size=20, color=P.CLAIM),
              label(r"overlap", font_size=20, color=P.CLAIM)]
        rows = [[label(r"set A", font_size=21, color=LUCK), label(f"{d['shogenji'][0]:.2f}", font_size=21),
                 label(f"{d['overlap'][0]:.2f}", font_size=21)],
                [label(r"set B", font_size=21, color=BEL), label(f"{d['shogenji'][1]:.2f}", font_size=21),
                 label(f"{d['overlap'][1]:.2f}", font_size=21)]]
        tab = ValueGrid(hd, rows, col_w=[1.4, 1.5, 1.5], cell_h=0.45, font_size=20).move_to([-4.0, -0.2, 0])
        same = label(r"same prior: \ $P(\text{all true}) = 0.1$ \ for both", font_size=19, color=GREY_A).next_to(
            tab, DOWN, buff=0.2)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1, 0.25], x_length=5.6, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "stroke_width": 2, "include_numbers": True, "font_size": 18}).move_to(
            [2.8, -0.2, 0])
        xl = label(r"$x = P(\text{report}\mid\text{false}) / P(\text{report}\mid\text{true})$ \ (left: good witnesses)",
                   font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.15)
        yl = label(r"$P(\text{all three true} \mid \text{reports})$", font_size=18, color=GREY_B).next_to(ax, UP,
                                                                                                         buff=0.1)
        ca = ax.plot_line_graph([c[0] for c in d["curve"]], [c[1] for c in d["curve"]], line_color=LUCK,
                                add_vertex_dots=False, stroke_width=3)
        cb = ax.plot_line_graph([c[0] for c in d["curve"]], [c[2] for c in d["curve"]], line_color=BEL,
                                add_vertex_dots=False, stroke_width=3)
        x0 = d["cross"]
        cross_y = [c for c in d["curve"] if abs(c[0] - 0.5) < 1e-9][0][1]
        cd = Dot(ax.c2p(x0, cross_y), color=GOAL, radius=0.08)
        cl = label(rf"they cross at $x = {x0:.2f}$", font_size=19, color=GOAL).next_to(cd, UR, buff=0.1)
        p = d["probe"]
        notes = VGroup(label(rf"good witnesses ($x = 0.25$): \ A {p[0][1]:.2f}, \ B {p[0][2]:.2f}", font_size=20,
                             color=BEL),
                       label(rf"poor witnesses ($x = 0.75$): \ A {p[1][1]:.3f}, \ B {p[1][2]:.3f}", font_size=20,
                             color=LUCK)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        foot = VGroup(label(r"A is more coherent on both measures; \ which set is more likely true depends on the "
                            r"witnesses,", font_size=22, color=GOAL),
                      label(r"which no measure of coherence can see \ (Bovens and Hartmann 2003; \ Olsson 2005)",
                            font_size=22, color=GOAL)).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.2)
        notes.next_to(ms, DOWN, buff=0.2).align_to(ms, LEFT)
        notes.move_to([-3.9, -2.0, 0])
        with self.voiceover(
            "Bayesians have tried to make coherence precise. <bookmark mark='a'/>Two measures. Tomoji Shogenji's: "
            "the probability that all the propositions are true together, divided by the product of their separate "
            "probabilities. Erik Olsson's overlap measure: the probability that all are true, divided by the "
            "probability that at least one is. <bookmark mark='b'/>The Reasoner builds two sets of three reports, "
            "each from an independent witness, with the same prior chance of all being true. Set A is more coherent "
            "than set B on both measures. <bookmark mark='c'/>Now it computes how likely each set is to be true, "
            "given the reports, for witnesses of every quality. On the left the witnesses are good; on the right, "
            "barely better than chance. <bookmark mark='d'/>The curves cross. With good witnesses, the less coherent "
            "set B is more likely true; with poor ones, A. <bookmark mark='e'/>Which set is more likely true depends "
            "on the witnesses, and no measure of the sets' coherence alone can see that. Luc Bovens and Stephan "
            "Hartmann, in 2003, and Olsson, in 2005, proved that no measure of coherence is truth-conducive in this "
            "sense."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ms[0]))
            self.play(FadeIn(ms[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab.head), FadeIn(tab.rule), FadeIn(tab.rows_bg),
                      *[FadeIn(VGroup(*tab.cell[r])) for r in range(2)], FadeIn(same))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(ca), Create(cb), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(cd), FadeIn(cl))
            self.play(FadeIn(notes))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
