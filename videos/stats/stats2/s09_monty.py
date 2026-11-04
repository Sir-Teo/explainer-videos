from __future__ import annotations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403


class Monty(VoiceoverScene):
    def construct(self):
        self.card()
        self.game()
        self.history()
        self.tree()
        self.simulate()
        self.protocols()

    def card(self):
        card = chapter_card(8, r"Monty Hall", r"What does an opened door tell you?", lit=(1763,), part=PART)
        with self.voiceover("Chapter eight. Monty Hall."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def doors(self):
        ds = VGroup(*[door(k, w=1.9, h=3.0) for k in (1, 2, 3)]).arrange(RIGHT, buff=0.9).move_to([0, 0.2, 0])
        return ds

    def game(self):
        ds = self.doors()
        behind = VGroup(prize("goat"), prize("car"), prize("goat"))
        for b, dr in zip(behind, ds):
            b.move_to(dr.body.get_center() + DOWN * 0.3)
        pick = SurroundingRectangle(ds[0], color=S.ACCENT, buff=0.12, corner_radius=0.1)
        you = label(r"your pick", font_size=26, color=S.ACCENT).next_to(pick, DOWN, buff=0.15)
        host = label(r"the host, who knows where the car is, \ opens a door with a goat", font_size=28, color=GREY_A)
        host.to_edge(UP, buff=0.5)
        q = label(r"stay with door 1, \ or switch to door 2?", font_size=36, color=S.ACCENT).to_edge(DOWN, buff=0.5)
        opened = Rectangle(width=1.9, height=3.0, stroke_color="#C9A27E", stroke_width=2, fill_color="#0B0F17",
                           fill_opacity=1).move_to(ds[2].body)
        goat3 = prize("goat").move_to(opened)
        with self.voiceover(
            "In 1990 a puzzle about a game show became one of the most argued-over questions in the history of "
            "probability. <bookmark mark='a'/> There are three doors. Behind one is a car; behind the other two, "
            "goats. <bookmark mark='b'/> You pick a door, say door one. <bookmark mark='c'/> The host, who knows "
            "where the car is, opens another door, door three, and shows you a goat. <bookmark mark='d'/> Then he "
            "asks: do you want to stay with door one, or switch to door two? Two doors left, one car. Does it "
            "matter?"
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dr, shift=UP * 0.2) for dr in ds], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Create(pick), FadeIn(you))
            vo.wait_until("c")
            self.play(FadeIn(host))
            self.play(FadeIn(opened), FadeIn(goat3))
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def history(self):
        h1 = history_card(1975, r"Steve Selvin, \ letters to \emph{The American Statistician}", r"the problem, its "
                          r"solution, \ and the name Monty Hall", color=S.MUSEUM, width=5.6, font_size=23)
        h2 = history_card(1990, r"Marilyn vos Savant, \ ``Ask Marilyn'', \ \emph{Parade}", r"``Yes; you should "
                          r"switch.'' \ About ten thousand letters followed, \ nearly a thousand from PhDs, \ most "
                          r"saying she was wrong", color=S.MUSEUM, width=5.6, font_size=23)
        VGroup(h1, h2).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([0, 1.2, 0])
        intuit = label(r"intuition: \ ``two doors, \ so it's fifty--fifty''", font_size=32, color=GREY_A)
        intuit.move_to([0, -1.6, 0])
        erd = label(r"Paul Erd\H{o}s, \ by his biographer's account, \ believed it only after a simulation",
                    font_size=24, color=GREY_B).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The puzzle was first posed and solved in 1975 by the statistician Steve Selvin, in two letters to The "
            "American Statistician. <bookmark mark='a'/> It became famous in 1990, when Marilyn vos Savant "
            "answered it in her magazine column: yes, you should switch; switching wins two times in three. "
            "<bookmark mark='b'/> She received about ten thousand letters, nearly a thousand of them from people "
            "with doctorates, most of them telling her she was wrong. <bookmark mark='c'/> The intuition is strong: "
            "two doors are left, so it must be fifty-fifty. <bookmark mark='d'/> Even Paul Erdős, one of the great "
            "mathematicians of the century, was convinced, by his biographer's account, only when he was shown a "
            "simulation. Let's not argue. Let's compute."
        ) as vo:
            self.play(FadeIn(h1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(h2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(intuit))
            vo.wait_until("d")
            self.play(FadeIn(erd))
        self.clear_scene()

    def tree(self):
        lv = ["", "", WHITE, [
            (r"\text{car } 1", r"\tfrac13", CAR, [(r"\text{opens } 2", r"\tfrac12", GREY_B, []),
                                                  (r"\text{opens } 3", r"\tfrac12", S.ACCENT, [])]),
            (r"\text{car } 2", r"\tfrac13", CAR, [(r"\text{opens } 3", r"1", S.ACCENT, [])]),
            (r"\text{car } 3", r"\tfrac13", CAR, [(r"\text{opens } 2", r"1", GREY_B, [])]),
        ]]
        tree = prob_tree(lv, x0=-6.0, dx=2.8, height=5.0, font_size=28).move_to([-3.4, -0.2, 0])
        title = label(r"you picked door 1; \ the host's rule decides the second branch", font_size=28,
                      color=GREY_A).to_edge(UP, buff=0.35)
        leaf_p = {(0, 1): r"\tfrac16", (1, 0): r"\tfrac13"}
        tags = VGroup(*[MathTex(t, font_size=32, color=S.ACCENT).next_to(tree.nodes[p], RIGHT, buff=0.3)
                        for p, t in leaf_p.items()])
        rows = [
            cmath(r"P(\text{car } 2 \mid \text{opens } 3)", r"=", r"\frac{\tfrac13}{\tfrac13 + \tfrac16}", r"=",
                  r"\tfrac23", font_size=34),
            cmath(r"P(\text{car } 1 \mid \text{opens } 3)", r"=", r"\frac{\tfrac16}{\tfrac13 + \tfrac16}", r"=",
                  r"\tfrac13", font_size=34),
        ]
        rows[0][4].set_color(EXACT)
        rows[1][4].set_color(EXACT)
        for r, y in zip(rows, (0.9, -0.9)):
            r.move_to([4.5, y, 0])
        why_ = label(r"when the car is behind door 1, \ the host could have opened either door: \ half the time he "
                     r"opens 2", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Draw the tree. <bookmark mark='a'/> The car is behind each door with probability a third. You picked "
            "door one. <bookmark mark='b'/> Now the host acts, and his rule decides the second branch. If the car is "
            "behind door one, he can open either of the others; say he picks at random, half and half. If it's "
            "behind door two, he must open door three. If it's behind door three, he must open door two. "
            "<bookmark mark='c'/> You saw him open door three. Two paths end there: car behind door one and he "
            "chose three, probability a third times a half, one sixth; and car behind door two, probability a "
            "third times one, one third. <bookmark mark='d'/> Renormalize. The car is behind door two with "
            "probability a third over a half: two thirds. <bookmark mark='e'/> Behind door one, one third. Switch. "
            "<bookmark mark='f'/> The asymmetry comes from the host's constraint: when you've picked a goat, he has "
            "no choice about which door to open, so his opening door three is twice as likely when the car is "
            "behind door two."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(FadeIn(tree.nodes[()]), *[FadeIn(tree.nodes[(i,)]) for i in range(3)],
                      *[Create(tree.edges[(i,)]) for i in range(3)], *[FadeIn(tree.probs[(i,)]) for i in range(3)])
            vo.wait_until("b")
            leaves = [p for p in tree.nodes if len(p) == 2]
            self.play(*[FadeIn(tree.nodes[p]) for p in leaves], *[Create(tree.edges[p]) for p in leaves],
                      *[FadeIn(tree.probs[p]) for p in leaves])
            vo.wait_until("c")
            self.play(*[tree.edges[p].animate.set_color(S.ACCENT).set_stroke(width=5) for p in ((0,), (0, 1), (1,), (1, 0))],
                      *[tree.nodes[p].animate.set_opacity(0.25) for p in ((0, 0), (2, 0))], FadeIn(tags))
            vo.wait_until("d")
            self.play(Write(rows[0]))
            vo.wait_until("e")
            self.play(Write(rows[1]))
            vo.wait_until("f")
            self.play(FadeIn(why_))
        self.clear_scene()

    def simulate(self):
        d = load("monty")
        run = np.asarray(d["running"])
        n = d["n"]
        A = axes([0, n], [0.3, 0.9], x_length=7.4, y_length=4.2, xlabel=r"games played", ylabel=r"fraction won by "
                 r"switching", xticks=[0, 1000, 2000, 3000], yticks=[0.33, 0.5, 0.67, 0.9],
                 xfmt=lambda v: fmt_int(v), yfmt=lambda v: f"{v:.2f}", center=[-2.6, -0.4, 0])
        ax = A.ax
        xs = np.arange(1, n + 1)
        idx = np.unique(np.geomspace(5, n, 300).astype(int)) - 1
        path = curve(ax, xs[idx], np.clip(run[idx], 0.3, 0.9), SIM, 3)
        gold = DashedLine(ax.c2p(0, 2 / 3), ax.c2p(n, 2 / 3), color=EXACT, stroke_width=3)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(n, 0.5), color=GREY_C, stroke_width=2)
        hl = label(r"``fifty--fifty''", font_size=22, color=GREY_B).next_to(ax.c2p(n, 0.5), RIGHT, buff=0.1)
        box = exact_sim(r"\tfrac23", 2 / 3, d["sim_switch"], n).move_to([4.6, 2.5, 0])
        eng = code_block(["car = Dist.uniform([1, 2, 3])", "tree = car.then(host)",
                          "tree.given(opened_3).P(car_2)   # 2/3"], font_size=18)
        eng.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.9)
        with self.voiceover(
            "Erdős wanted a simulation, so here's one. <bookmark mark='a'/> Three thousand games, the car placed at "
            "random, the host following his rule, the contestant always switching. <bookmark mark='b'/> The "
            f"fraction of wins settles at {d['sim_switch']:.3f}: two thirds, not one half. <bookmark mark='c'/> "
            "And in the engine the whole game is three lines: the car's door, the host's rule as a second stage of "
            "the tree, and the condition we observed."
        ) as vo:
            self.play(FadeIn(A), Create(gold), Create(half), FadeIn(hl))
            vo.wait_until("a")
            self.play(Create(path), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(box))
            vo.wait_until("c")
            self.play(FadeIn(eng, shift=UP * 0.2))
        self.clear_scene()

    def protocols(self):
        d = load("monty")
        pr = d["protocols"]
        rows = VGroup()
        table = [
            (r"knows, \ always opens a goat door, \ random when he can choose", frac(pr["standard"]["switch"])),
            (r"opens another door at random; \ it happened to hide a goat", frac(pr["ignorant"]["switch"])),
            (r"opens a door only when your first pick is the car", frac(pr["devil"]["switch"])),
            (r"knows; \ prefers door 3 with probability $q$ when he can choose", r"\tfrac{1}{1+q}"),
        ]
        head = VGroup(label(r"the host's rule", font_size=26, color=GREY_A),
                      label(r"$P(\text{switch wins})$", font_size=26, color=GREY_A))
        for txt, val in table:
            rows.add(VGroup(label(txt, font_size=24), MathTex(val, font_size=34, color=EXACT)))
        allrows = VGroup(head, *rows)
        y = 2.8
        for r in allrows:
            r[0].move_to([-6.5 + r[0].width / 2, y, 0])
            r[1].move_to([2.4, y, 0])
            y -= 0.85
        A = axes([0, 1], [0.4, 1.05], x_length=3.4, y_length=2.6, xlabel=r"$q$", xticks=[0, 0.5, 1],
                 yticks=[0.5, 1], center=[5.0, -1.9, 0])
        ax = A.ax
        cv = curve(ax, d["qs"], d["biased"], EXACT, 3)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(1, 0.5), color=GREY_C, stroke_width=1.5)
        cap = label(r"switching is never worse", font_size=22, color=EXACT).next_to(A, UP, buff=0.15)
        with self.voiceover(
            "But notice what the answer depended on: the host's rule. Change the rule and the same observation means "
            "something else. <bookmark mark='a'/> The standard host gives two thirds. <bookmark mark='b'/> Suppose "
            "instead the host doesn't know where the car is, and opens one of the other doors at random; this time, "
            "by luck, it hid a goat. Now the answer is a half: his door told you nothing about the others except "
            "that this one is empty. <bookmark mark='c'/> Suppose he's devious, and opens a door only when you've "
            "already picked the car, to tempt you away. Then switching always loses. <bookmark mark='d'/> And if "
            "he knows, but prefers door three whenever he has a choice, with probability q, then switching wins "
            "with probability one over one plus q: anywhere from a half to certainty, <bookmark mark='e'/> but "
            "never less than a half. <bookmark mark='f'/> So the data are not only what you saw, but how it came "
            "to be shown to you. The probability of the evidence under each hypothesis depends on the process that "
            "produced it; that probability is the likelihood, the central object of Parts 9 and 22."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(A), Create(half), Create(cv), FadeIn(cap))
            vo.wait_until("f")
            lesson = label(r"the data are not just \emph{what} you saw, \ but \emph{how it came to be shown}: \ the "
                           r"likelihood", font_size=26, color=S.ACCENT)
            if lesson.width > 8.6:
                lesson.width = 8.6
            lesson.move_to([-2.3, -2.4, 0])
            self.play(FadeIn(lesson, shift=UP * 0.2))
        self.clear_scene()
