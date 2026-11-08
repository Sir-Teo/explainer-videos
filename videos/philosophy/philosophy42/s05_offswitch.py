from __future__ import annotations

from videos.philosophy.philosophy42.common import *  # noqa: F403


class OffSwitch(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"The off-switch game", r"Will a machine let us switch it off?", lit=(2016, 2017), part=PART)
        with self.voiceover("Chapter four. The off-switch game."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.russell()
        self.tree()
        self.heat()
        self.information()
        self.corrigible()

    def russell(self):
        head = history_card(2019, r"Stuart Russell", r"\textit{Human Compatible}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"1", r"the machine's only objective is to maximize the realization of human preferences", TRUEV),
                (r"2", r"the machine is initially uncertain about what those preferences are", ROBOT),
                (r"3", r"the ultimate source of information about human preferences is human behaviour", HUMAN),
                (r"assistance games", r"Hadfield-Menell, \ Dragan, \ Abbeel and Russell \ (2016): \ cooperative inverse RL, \ a game of two players with one reward that only the human knows", PROXYC)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Stuart Russell proposed a different design in Human Compatible. <bookmark mark='a'/>First, the machine's "
            "only objective is to realize human preferences. <bookmark mark='b'/>Second, and crucially, it is "
            "initially uncertain what those preferences are. <bookmark mark='c'/>Third, its evidence about them is "
            "human behaviour. <bookmark mark='d'/>With Dylan Hadfield-Menell, Anca Dragan and Pieter Abbeel he made "
            "this a game: cooperative inverse reinforcement learning, in which a human and a robot share one reward "
            "that only the human knows. The robot does well only by helping the human, and learns what helps by "
            "watching. The payoff of this design appears in the simplest possible game."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def tree(self):
        d = load("offswitch")
        ex, exn = d["example"], d["example_noisy"]
        assert abs(ex["wait"] - ex["exact_wait"]) < 1e-3 and ex["incentive"] > 0 and exn["incentive"] < 0
        head = label(r"The off-switch game \ (Hadfield-Menell, \ Dragan, \ Abbeel and Russell, \ 2017)",
                     font_size=28, color=CONN).to_edge(UP, buff=0.3)
        R = LabeledDot(MathTex(r"R", font_size=30, color=BLACK), radius=0.3, color=ROBOT).move_to([-1.5, 1.9, 0])
        H = LabeledDot(MathTex(r"H", font_size=30, color=BLACK), radius=0.3, color=HUMAN).move_to([1.6, 0.2, 0])
        leaves = {"act": [-4.4, 0.2, 0], "off": [-1.5, 0.2, 0], "allow": [0.4, -1.5, 0], "hoff": [2.8, -1.5, 0]}
        vals = {"act": r"u", "off": r"0", "allow": r"u", "hoff": r"0"}
        lv = {k: MathTex(vals[k], font_size=34).move_to(p) for k, p in leaves.items()}
        edges = VGroup(
            Line(R.get_center(), lv["act"].get_center(), buff=0.35, color=GREY_B),
            Line(R.get_center(), lv["off"].get_center(), buff=0.35, color=GREY_B),
            Line(R.get_center(), H.get_center(), buff=0.35, color=GREY_B),
            Line(H.get_center(), lv["allow"].get_center(), buff=0.35, color=GREY_B),
            Line(H.get_center(), lv["hoff"].get_center(), buff=0.35, color=GREY_B))
        el = VGroup(label(r"act", font_size=19, color=ROBOT).next_to(edges[0].get_center(), UL, buff=0.08),
                    label(r"switch off", font_size=19, color=ROBOT).next_to(edges[1].get_center(), LEFT, buff=0.1),
                    label(r"wait", font_size=19, color=ROBOT).next_to(edges[2].get_center(), UR, buff=0.08),
                    label(r"allow", font_size=19, color=HUMAN).next_to(edges[3].get_center(), LEFT, buff=0.1),
                    label(r"switch off", font_size=19, color=HUMAN).next_to(edges[4].get_center(), RIGHT, buff=0.1))
        belief = MathTex(r"\text{the robot's belief: } u \sim N(\mu, \sigma^2) = N(0.5,\ 1)", font_size=26,
                         color=ROBOT).move_to([0, -2.4, 0])
        eqs = VGroup(
            MathTex(rf"\text{{act: }}\ \mathbb{{E}}[u] = \mu = {ex['act']:.2f}", font_size=26),
            MathTex(r"\text{switch off: }\ 0", font_size=26),
            MathTex(rf"\text{{wait: }}\ \mathbb{{E}}[\max(u, 0)] = \mu\,\Phi(\mu/\sigma) + \sigma\,\varphi(\mu/\sigma) "
                    rf"= {ex['wait']:.2f}", font_size=26, color=TRUEV),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.9, 2.2, 0])
        for e in eqs:
            if e.width > 6.4:
                e.width = 6.4
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, 2.35, 0])
        noisy = MathTex(rf"\text{{a noisy human, }} P(\text{{allow}}) = \frac{{1}}{{1 + e^{{-\beta u}}}},\ \beta = 0.5:"
                        rf"\ \ \text{{wait}} = {exn['wait']:.2f} < {exn['act']:.2f}", font_size=24,
                        color=RISK).move_to([0, -3.2, 0])
        with self.voiceover(
            "Here is the game. <bookmark mark='a'/>A robot, R, is about to take an action whose value to the human "
            "is u. It can act, and get u; switch itself off, and get zero; or wait, and let the human, H, decide. "
            "<bookmark mark='b'/>If it waits, the human either allows the action or switches the robot off. "
            "<bookmark mark='c'/>The robot does not know u. It believes u is normally distributed, with mean point "
            "five and spread one: probably good, possibly harmful. <bookmark mark='d'/>Acting is worth the mean, "
            "point five. Switching off is worth zero. Waiting is worth the expected value of the larger of u and "
            "zero, because a rational human will block the action exactly when it is harmful: point seven zero. "
            "Waiting wins. The robot wants to keep the off switch in the human's hands, because the human's "
            "decision carries information the robot lacks. <bookmark mark='e'/>But suppose the human is noisy, "
            "allowing harmful actions and blocking good ones at random, with a rationality of one half. Now waiting "
            "is worth only point four zero, less than acting, and the robot acts without asking."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(R), Create(edges[0:3]), FadeIn(el[0:3]), FadeIn(lv["act"]), FadeIn(lv["off"]))
            vo.wait_until("b")
            self.play(FadeIn(H), Create(edges[3:]), FadeIn(el[3:]), FadeIn(lv["allow"]), FadeIn(lv["hoff"]))
            vo.wait_until("c")
            self.play(FadeIn(belief))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(e) for e in eqs], lag_ratio=0.5))
            self.play(Indicate(eqs[2], color=TRUEV, scale_factor=1.05))
            vo.wait_until("e")
            self.play(FadeIn(noisy))
        self.clear_scene()

    def heat(self):
        d = load("offswitch")
        mus, sigmas, G = d["mus"], d["sigmas"], d["grids"]
        frac = {k: float(np.mean(np.array(v) < -1e-9)) for k, v in G.items()}
        assert frac["rational"] == 0.0 and 0.3 < frac["beta=2"] < 0.35 and 0.6 < frac["beta=0.5"] < 0.65
        head = label(r"When does the robot defer?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        panels = VGroup()
        for i, (key, title) in enumerate((("rational", r"a rational human"), ("beta=0.5", r"a noisy human, \ $\beta = 0.5$"))):
            grid = np.array(G[key])
            cells = VGroup()
            w, h = 5.2 / 21, 3.9 / 16
            for si in range(0, len(sigmas), 2):
                for mi in range(0, len(mus), 2):
                    v = grid[si][mi]
                    col = TRUEV if v > 1e-9 else (RISK if v < -1e-9 else GREY_D)
                    op = min(1.0, 0.15 + abs(v) * 1.2) if abs(v) > 1e-9 else 0.5
                    cells.add(Rectangle(width=w, height=h, stroke_width=0, fill_color=col, fill_opacity=op).move_to(
                        [-6.1 + 6.6 * i + (mi // 2 + 0.5) * w, -2.5 + (si // 2 + 0.5) * h, 0]))
            box = SurroundingRectangle(cells, buff=0, color=GREY_C, stroke_width=1)
            xl = VGroup(*[label(f"{m:g}", font_size=14, color=GREY_B).next_to(box, DOWN, buff=0.08).set_x(
                box.get_left()[0] + (m + 2) / 4 * box.width) for m in (-2, -1, 0, 1, 2)])
            yl = VGroup(*[label(f"{s:g}", font_size=14, color=GREY_B).next_to(box, LEFT, buff=0.08).set_y(
                box.get_bottom()[1] + s / 3 * box.height) for s in (0, 1, 2, 3)])
            xt = label(r"robot's mean belief $\mu$", font_size=16, color=GREY_A).next_to(xl, DOWN, buff=0.1)
            yt = label(r"its uncertainty $\sigma$", font_size=16, color=GREY_A).rotate(PI / 2).next_to(yl, LEFT,
                                                                                                         buff=0.1)
            tt = label(title, font_size=21, color=HUMAN).next_to(box, UP, buff=0.15)
            ft = label(rf"wants to act or switch off in {frac[key] * 100:.0f}\% of the grid", font_size=17,
                       color=RISK if frac[key] > 0 else TRUEV).next_to(xt, DOWN, buff=0.12)
            panels.add(VGroup(cells, box, xl, yl, xt, yt, tt, ft))
        key_ = stack([(r"teal: \ prefers to wait, \ and leave the switch with the human", TRUEV),
                      (r"pink: \ prefers to act, \ or to switch itself off", RISK)], font_size=18, buff=0.15,
                     aligned_edge=LEFT).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "The Reasoner solves the game everywhere. <bookmark mark='a'/>Across, the robot's mean belief about "
            "the action; up, its uncertainty. Teal means the robot prefers to wait and leave the switch with the "
            "human; pink means it prefers to act or to switch itself off. <bookmark mark='b'/>With a rational "
            "human, the robot always weakly prefers to wait. The advantage is largest when it is most uncertain, and "
            "it vanishes along the bottom edge, where the robot is certain: a robot sure of its objective has no "
            "reason to listen. <bookmark mark='c'/>With a noisy human, the region of deference shrinks: in sixty "
            "two percent of the grid the robot would rather act on its own judgment or switch itself off; with a "
            "less noisy human, thirty two percent. <bookmark mark='d'/>The theorem's lesson has two sides. "
            "Deference comes from the robot's uncertainty about what we want, and lasts only as long as that "
            "uncertainty does; and it depends on the robot's belief that we are rational enough to be worth "
            "obeying."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(panels[0][1:7]), FadeIn(key_))
            vo.wait_until("b")
            self.play(FadeIn(panels[0][0]), FadeIn(panels[0][7]))
            vo.wait_until("c")
            self.play(FadeIn(panels[1]))
            vo.wait_until("d")
            self.wait(0.5)
        self.clear_scene()

    def corrigible(self):
        head = label(r"Corrigibility", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Soares et al. \ (2015)", r"`Corrigibility': \ an agent should not resist correction, \ nor manipulate us into or out of pressing the button", ROBOT),
                (r"utility indifference", r"Armstrong: \ make the agent indifferent to the button; \ but indifference is fragile", PROXYC),
                (r"Carey \ (2018)", r"with a misspecified prior, \ an assistance-game robot can ignore the off switch", RISK),
                (r"the open problem", r"no known objective makes a capable agent reliably correctable", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The property the off-switch game is after has a name. <bookmark mark='a'/>Nate Soares, Benja "
            "Fallenstein, Eliezer Yudkowsky and Stuart Armstrong called it corrigibility in 2015: an agent that does "
            "not resist correction or shutdown, and does not manipulate its overseers into pressing the button or "
            "into leaving it alone. <bookmark mark='b'/>One proposal, utility indifference, makes the agent exactly "
            "indifferent to whether the button is pressed; but the indifference is fragile, and the agent has no "
            "reason to preserve the button for its successors. <bookmark mark='c'/>Ryan Carey showed that the "
            "assistance-game robot loses its deference if its prior over our preferences is wrong, which in practice "
            "it will be. <bookmark mark='d'/>Corrigibility remains an open problem: no known objective makes a "
            "capable optimizer reliably correctable."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def information(self):
        head = label(r"Deference is the value of information", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Good \ (1967)", r"a Bayesian never expects free evidence to make its decision worse", HUMAN),
                (r"the off switch", r"$\mathbb{E}[\max(u, 0)] - \max(\mathbb{E}[u], 0)$: \ the expected value of learning the sign of $u$", TRUEV),
                (r"noisy evidence", r"a noisy human is a noisy signal: \ worth less, \ and sometimes worth less than nothing to act on", RISK),
                (r"Part 13", r"the robot is a Bayesian deciding whether to look before it leaps", ROBOT)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "There is a simpler way to see the result. <bookmark mark='a'/>In 1967 I. J. Good proved that a Bayesian "
            "agent never expects free evidence to make its decisions worse: looking before you leap cannot hurt, on "
            "average. <bookmark mark='b'/>The robot's incentive to wait, the expected value of the larger of u and "
            "zero, minus the larger of the expected u and zero, is exactly the expected value of learning the sign of "
            "u. The human's choice is that evidence. <bookmark mark='c'/>A noisy human is a noisy signal. It is worth "
            "less, and if the robot must obey it rather than merely observe it, it can be worth less than acting "
            "alone. <bookmark mark='d'/>So the off-switch game is the Bayesian decision theory of Parts 13 and 33 in "
            "a new setting: a robot deciding whether to look before it leaps, where the looking is done by us."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
