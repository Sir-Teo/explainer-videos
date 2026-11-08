from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Dilemma(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Determinism, \ and luck", r"Is an undetermined act any more ours?", lit=(1814,),
                            part=PART)
        with self.voiceover("Chapter one. Determinism, and luck."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.demon()
        self.define()
        self.levels()
        self.horns()

    def demon(self):
        q = quote_card(r"An intellect which at a certain moment would know all forces that set nature in motion, \ "
                       r"and all positions of all items of which nature is composed, \dots\ for such an intellect "
                       r"nothing would be uncertain and the future just like the past would be present before its "
                       r"eyes.", r"Pierre-Simon Laplace", r"\textit{A Philosophical Essay on Probabilities} \ (1814)",
                       width=10.4, font_size=25).to_edge(UP, buff=0.5)
        rows = stack([(r"the state now, \ plus the laws, \ fixes every later state", LAW),
                      (r"including the state of your brain when you decide", WILL)], font_size=22,
                     buff=0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The modern worry has a famous image. <bookmark mark='a'/>In 1814 Pierre-Simon Laplace imagined an "
            "intellect that knew, at one moment, every force in nature and the position of every particle. For "
            "such an intellect, he wrote, nothing would be uncertain, and the future, like the past, would be "
            "present before its eyes. <bookmark mark='b'/>The state of the world now, together with the laws, "
            "would fix every later state, <bookmark mark='c'/>including the state of your brain at the moment you "
            "decide what to do."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def define(self):
        head = label(r"Determinism, \ defined \ (Part 24)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Arrow([-6.0, -0.9, 0], [6.0, -0.9, 0], buff=0, color=GREY_B)
        tl = label(r"time", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.1).shift(RIGHT * 5.4)
        t0 = DashedLine([-2.0, 2.4, 0], [-2.0, -0.9, 0], color=GREY_C)
        t0l = MathTex(r"t_0", font_size=24, color=GREY_A).next_to(t0, DOWN, buff=0.15)
        up = np.array([0, 0.5, 0])
        w1 = VMobject(color=LAW, stroke_width=4).set_points_smoothly(
            [np.array(p) + up for p in ([-6.0, 0.4, 0], [-4.0, 0.9, 0], [-2.0, 0.6, 0], [0.0, 1.1, 0], [2.5, 0.5, 0],
                                        [5.5, 1.2, 0])])
        w2a = VMobject(color=CHANCE, stroke_width=4).set_points_smoothly(
            [np.array(p) + up for p in ([-6.0, -0.6, 0], [-4.0, -0.1, 0], [-2.0, 0.6, 0])])
        w2b = VMobject(color=CHANCE, stroke_width=4).set_points_smoothly(
            [np.array(p) + up for p in ([-2.0, 0.6, 0], [0.0, 1.1, 0], [2.5, 0.5, 0], [5.5, 1.2, 0])]).shift(
            DOWN * 0.08)
        lab = stack([(r"two worlds with the same laws, \ alike at any one time, \ are alike at all times", LAW),
                     (r"so worlds that agree at $t_0$ never branch", GREY_A),
                     (r"a thesis about the laws, \ not about predictability: \ chaos is deterministic", GOAL)],
                    font_size=20, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Philosophers state determinism without the demon, as Part 24 did. <bookmark mark='a'/>The laws are "
            "deterministic if any two possible worlds that obey them, and agree completely at any one time, agree "
            "at all times. <bookmark mark='b'/>Two histories may differ in the past, but once they coincide at a "
            "time, they coincide for ever after: no branching. <bookmark mark='c'/>It is a thesis about the laws, "
            "not about what anyone could predict. A chaotic system is deterministic, though no one could ever "
            "measure it well enough to predict it."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(ax), FadeIn(tl))
            vo.wait_until("a")
            self.play(Create(w1), FadeIn(lab[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(t0), FadeIn(t0l), Create(w2a), run_time=1.5)
            self.play(Create(w2b), FadeIn(lab[1]))
            vo.wait_until("c")
            self.play(FadeIn(lab[2]))
        self.clear_scene()

    def levels(self):
        d = load("levels")
        head = label(r"Deterministic below, \ open above \ (List, \ 2019)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        pr = d["probs"]
        assert d["micro"] == 900 and d["fine_deterministic"] and d["deterministic_rows"] == []
        assert pr["deliberating"] == {"deliberating": 0.15, "tea": 0.45, "coffee": 0.4}
        assert pr["tea"]["tea"] == 0.9 and pr["coffee"]["coffee"] == 0.85
        cols = {"deliberating": SELF, "tea": CHANCE, "coffee": FUNC}
        sp = 0.15

        def at(i):
            return np.array([-5.8 + (i % 30) * sp, 1.6 - (i // 30) * sp, 0])
        dots = VGroup(*[Dot(at(i), radius=0.035, color=cols[d["macro"][i // 300]]) for i in range(900)])
        bands = VGroup(*[label(nm, font_size=16, color=cols[nm]).next_to(at(300 * k + 29) + DOWN * 0.65, RIGHT,
                                                                          buff=0.2)
                         for k, nm in enumerate(d["macro"])])
        arrows = VGroup()
        for e in d["examples"]:
            arrows.add(CurvedArrow(at(e["micro"]), at(e["next_micro"]), angle=-0.6, color=WHITE, stroke_width=1.6,
                                   tip_length=0.12))
        ml = label(r"each of 900 microstates has exactly one successor", font_size=17, color=LAW).next_to(
            dots, DOWN, buff=0.3)
        pos = {"deliberating": [3.2, 1.2, 0], "tea": [1.4, -1.6, 0], "coffee": [5.0, -1.6, 0]}
        nodes = {m: VGroup(Circle(radius=0.62, color=cols[m], fill_opacity=0.12),
                           label(m, font_size=17, color=cols[m])).move_to(p) for m, p in pos.items()}
        chain = VGroup()
        for a, b in (("deliberating", "tea"), ("deliberating", "coffee"), ("tea", "deliberating"),
                     ("coffee", "deliberating")):
            pa, pb = np.array(pos[a]), np.array(pos[b])
            u = (pb - pa) / np.linalg.norm(pb - pa)
            off = np.array([-u[1], u[0], 0]) * 0.14
            ar = Arrow(pa + u * 0.66 + off, pb - u * 0.66 + off, buff=0, color=GREY_B, stroke_width=3)
            chain.add(VGroup(ar, label(f"{pr[a][b]:.2f}", font_size=16, color=WHITE).move_to(
                (pa + pb) / 2 + off * 3.2)))
        loops = VGroup(*[label(f"stays: \\ {pr[m][m]:.2f}", font_size=15, color=cols[m]).next_to(
            nodes[m], DOWN if m != "deliberating" else UP, buff=0.12) for m in pos])
        side = label(r"agent level: \ from `deliberating', \ tea or coffee, \ not fixed", font_size=17,
                     color=GOAL).to_edge(DOWN, buff=0.3).shift(RIGHT * 3.2)
        with self.voiceover(
            "Christian List has argued that determinism and alternatives can both be real, at different levels. "
            "<bookmark mark='a'/>The Reasoner builds a small world of nine hundred microstates. Each has exactly one "
            "successor: the physics is deterministic. <bookmark mark='b'/>Now describe it the way psychology does, "
            "at the level of the agent. Group the microstates into three agent-level states: deliberating, choosing "
            "tea, and choosing coffee. <bookmark mark='c'/>From the agent-level state alone, what comes next? From "
            "deliberating: tea forty five percent of the time, coffee forty, and still deliberating fifteen. At "
            "that level the future is open, and the agent has alternatives. <bookmark mark='d'/>Refine the "
            "description down to single microstates and determinism returns. List's claim is that free will is a "
            "matter of the agential level, the level at which we describe choosers, and that its alternatives are "
            "as real as the categories of psychology. Critics answer that the openness is only in our description, "
            "not in the world; whether higher-level possibilities count is the question of the next chapters."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dots, lag_ratio=0.002), FadeIn(ml), run_time=2)
            self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(bands))
            vo.wait_until("c")
            self.play(*[FadeIn(n) for n in nodes.values()])
            self.play(LaggedStart(*[GrowArrow(c[0]) for c in chain], lag_ratio=0.2), FadeIn(VGroup(*[c[1] for c in
                                                                                                    chain])))
            self.play(FadeIn(loops), FadeIn(side))
            vo.wait_until("d")
            self.play(Indicate(dots, color=WHITE, scale_factor=1.02))
        self.clear_scene()

    def horns(self):
        head = label(r"The dilemma", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        left = VGroup(RoundedRectangle(width=5.4, height=2.6, corner_radius=0.2, color=LAW, fill_opacity=0.08),
                      VGroup(label(r"if determinism is true", font_size=24, color=LAW),
                             wrapped_label(r"every act was fixed before we were born, \ by the laws and the past, \ "
                                           r"neither of which is up to us", 4.8, 19, GREY_A)).arrange(DOWN, buff=0.25)
                      ).move_to([-3.2, 0.2, 0])
        right = VGroup(RoundedRectangle(width=5.4, height=2.6, corner_radius=0.2, color=CHANCE, fill_opacity=0.08),
                       VGroup(label(r"if it is false", font_size=24, color=CHANCE),
                              wrapped_label(r"an undetermined act is one nothing about us settled: \ how is that more "
                                            r"our doing than a coin toss?", 4.8, 19, GREY_A)).arrange(DOWN, buff=0.25)
                       ).move_to([3.2, 0.2, 0])
        foot = stack([(r"either way, \ freedom seems to vanish", BAD),
                      (r"the replies: \ compatibilism, \ libertarianism, \ or no free will: \ chapters 6 to 8", GOAL)],
                     font_size=21, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "This gives the problem the shape of a dilemma. <bookmark mark='a'/>If determinism is true, every act we "
            "perform was fixed before we were born, by the laws of nature and the distant past, and neither of "
            "those is up to us. <bookmark mark='b'/>If it is false, some acts are undetermined. But an undetermined "
            "act is one that nothing about us settled. How is that more our doing than the toss of a coin? "
            "<bookmark mark='c'/>Either way, freedom seems to vanish. <bookmark mark='d'/>The three main replies "
            "say that freedom survives determinism, that it needs indeterminism of the right kind, or that it does "
            "not exist. Chapters six to eight take them in turn."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()
