from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403

RED, BLACK, YELLOW = "#E5534B", "#9AA5B8", "#F2D15C"


def urn(seed: int = 61) -> VGroup:
    """Ellsberg's urn: 30 red balls you can count, and 60 more, black or yellow in a proportion nobody tells you."""
    rng = np.random.default_rng(seed)
    body = RoundedRectangle(width=3.6, height=4.2, corner_radius=0.5, stroke_color=GREY_B, stroke_width=3)
    balls = VGroup()
    pts = []
    while len(pts) < 90:
        p = np.array([rng.uniform(-1.5, 1.5), rng.uniform(-1.8, 1.8), 0])
        if all(np.linalg.norm(p - q) > 0.3 for q in pts):
            pts.append(p)
    pts.sort(key=lambda p: (-p[1], p[0]))
    for i, p in enumerate(pts):
        if i < 30:
            balls.add(Dot(p, radius=0.13, color=RED))
        else:
            balls.add(VGroup(Dot(p, radius=0.13, color=GREY_D),
                             Text("?", font_size=12, color=GREY_A).move_to(p)))
    g = VGroup(body, balls)
    g.balls = balls
    return g


class Paradoxes(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Allais and Ellsberg in the triangle", r"What do the two famous paradoxes say expected utility "
             r"gets wrong?", "Chapter eight. Allais and Ellsberg in the triangle.",
             lit={1953: r"Allais", 1961: r"Ellsberg"})
        self.fanning()
        self.ellsberg()
        self.maxmin()
        self.prospect()

    def fanning(self):
        t = load("triangle")
        p = load("paradoxes")
        tr = triangle(center=LEFT * 3.2 + DOWN * 0.2, side=5.2)
        pts = {k: tr.p(*v) for k, v in t["points"].items()}
        dots = VGroup(*[Dot(pts[k], radius=0.08, color=SAFE if k.endswith("A") else RISKY) for k in pts])
        ch = VGroup(Line(pts["1A"], pts["1B"], color=E.ACCENT, stroke_width=4),
                    Line(pts["2A"], pts["2B"], color=E.ACCENT, stroke_width=4))
        fan = VGroup(*[tri_path(tr, l_, color=FAN, width=2.4) for l_ in p["lines"]])
        names = VGroup(label(r"1A, 1B", font_size=19, color=E.ACCENT).next_to(pts["1B"], RIGHT, buff=0.15),
                       label(r"2A, 2B", font_size=19, color=E.ACCENT).next_to(pts["2B"], UP, buff=0.15))
        side = VGroup(
            label(r"Machina (1982): \ indifference lines that \emph{fan out}", font_size=25, color=FAN),
            label(r"steeper toward the better corner: \\ more risk averse when the lottery is good", font_size=23),
            label(rf"slope at 1A: \ {p['slope_1']:.0f} \ $>$ 10: \ 1A beats 1B", font_size=24, color=SAFE),
            label(rf"slope at 2A: \ {p['slope_2']:.2f} \ $<$ 10: \ 2B beats 2A", font_size=24, color=RISKY),
            label(r"one model that does it: \ Chew's weighted utility, \\ $V = \sum p_i w_i u_i / \sum p_i w_i$ \ "
                  r"(illustrative weights)", font_size=21, color=GREY_A),
            label(r"independence is the casualty: \\ what the two options share \emph{does} matter", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Back to the triangle and Allais's pairs, with the two parallel moves from A to B. "
            "<bookmark mark='a'/> Expected utility's parallel lines can't produce the common pattern. Lines that fan "
            "out can. <bookmark mark='b'/> In 1982 Mark Machina suggested that this is what people's preferences look "
            "like: indifference lines steeper toward the top left of the triangle, where lotteries are better. "
            "People are more risk averse when they have more to lose. <bookmark mark='c'/> Near the sure million the "
            "lines are steeper than the move from 1A to 1B, so 1A wins. <bookmark mark='d'/> Down at the far right, "
            "near the corner for nothing, they're flatter than the move from 2A to 2B, so 2B wins. "
            "<bookmark mark='e'/> Here the fan comes from one particular alternative to expected utility, Soo Hong "
            "Chew's weighted utility, with weights chosen for illustration. Its lines are still straight, but they "
            "meet at a point outside the triangle instead of running parallel. <bookmark mark='f'/> What gives way is "
            "independence. The part the two options share does matter to people."
        ) as vo:
            self.play(FadeIn(tr), FadeIn(dots), Create(ch), FadeIn(names), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in fan], lag_ratio=0.15), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(dots[0], color=SAFE, scale_factor=2))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(dots[2], color=SAFE, scale_factor=2))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def ellsberg(self):
        e = tables.ELLSBERG_1961.data
        u = urn().to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        cap = VGroup(label(r"30 red", font_size=24, color=RED),
                     label(r"60 black or yellow: \\ in what proportion, \ nobody says", font_size=22,
                           color=GREY_A)).arrange(DOWN, buff=0.1).next_to(u, DOWN, buff=0.2)
        cols = [r"", r"red (30)", r"black", r"yellow"]
        bets = [(r"I: \ on red", (r"\$100", r"\$0", r"\$0")), (r"II: \ on black", (r"\$0", r"\$100", r"\$0")),
                (r"III: \ red or yellow", (r"\$100", r"\$0", r"\$100")),
                (r"IV: \ black or yellow", (r"\$0", r"\$100", r"\$100"))]
        tab = VGroup()
        xs = [0.6, 3.1, 4.6, 6.1]
        hdr = VGroup(*[label(c, font_size=22, color=[GREY_B, RED, BLACK, YELLOW][i]).move_to([xs[i], 2.6, 0])
                       for i, c in enumerate(cols)])
        for i, (name, pay) in enumerate(bets):
            y = 1.9 - 0.65 * i - (0.8 if i >= 2 else 0)
            row = VGroup(label(name, font_size=23).move_to([xs[0], y, 0]),
                         *[label(v, font_size=24, color=SAFE if v != r"\$0" else GREY_C).move_to([xs[j + 1], y, 0])
                           for j, v in enumerate(pay)])
            tab.add(row)
        q1 = label(r"which do you prefer: \ I or II?", font_size=24, color=E.ACCENT).move_to([3.4, 0.55, 0])
        q2 = label(r"and: \ III or IV?", font_size=24, color=E.ACCENT).move_to([3.4, -1.55, 0])
        pattern = VGroup(
            label(r"``A very frequent pattern of response is: \\ action I preferred to II, \ and IV preferred to "
                  r"III.''", font_size=23, color=AMBIG),
        ).move_to([3.4, -2.65, 0])
        tag = published_tag(r"Ellsberg, QJE (1961), pp.\ 653--654", corner=DR, font_size=14)
        with self.voiceover(
            "The second paradox is about something expected utility doesn't even have a word for. In 1961 Daniel "
            "Ellsberg, then an analyst at the RAND Corporation, described an urn. <bookmark mark='a'/> It holds "
            "thirty red balls, and sixty more that are black or yellow, in a proportion nobody tells you. One ball "
            "will be drawn. <bookmark mark='b'/> Bet one pays a hundred dollars if it's red. Bet two pays a hundred "
            "if it's black. Which would you rather have? <bookmark mark='c'/> Now bet three pays if the ball is red "
            "or yellow, and bet four if it's black or yellow. Which of those? Take your time, Ellsberg wrote. "
            "<bookmark mark='d'/> A very frequent pattern, he reported, is to prefer one to two, and four to three. "
            "You know the chance of red is a third; you know the chance of black or yellow is two thirds. People "
            "prefer the bets whose chances they know."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(u[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, scale=0.5) for b_ in u.balls], lag_ratio=0.02), FadeIn(cap),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(hdr), FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(q1))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]), FadeIn(q2))
            vo.wait_until("d")
            self.play(FadeIn(pattern))
            self.play(Indicate(tab[0], color=AMBIG, scale_factor=1.03), Indicate(tab[3], color=AMBIG,
                                                                                scale_factor=1.03))
        self.clear_scene()

    def maxmin(self):
        p = load("paradoxes")
        e = p["ellsberg"]
        rows = VGroup(
            label(r"no single probability of black can do it:", font_size=28),
            MathTex(r"\text{I} \succ \text{II} \;\Rightarrow\; p_{\text{red}} > p_{\text{black}}", font_size=36),
            MathTex(r"\text{IV} \succ \text{III} \;\Rightarrow\; p_{\text{black}} + p_{\text{yellow}} > "
                    r"p_{\text{red}} + p_{\text{yellow}} \;\Rightarrow\; p_{\text{black}} > p_{\text{red}}",
                    font_size=36),
            label(r"a contradiction: \ the choices are not expected utility for \emph{any} beliefs", font_size=26,
                  color=AMBIG),
        ).arrange(DOWN, buff=0.35).to_edge(UP, buff=0.6)
        mm = VGroup(
            label(r"maxmin expected utility \ (Gilboa and Schmeidler, 1989): \\ judge each bet by its worst chance, "
                  r"\ over every share of black from 0 to $\tfrac23$", font_size=24, color=AMBIG),
            label(rf"I: \ {e['I']:.2f} \qquad II: \ {e['II']:.2f} \qquad III: \ {e['III']:.2f} \qquad IV: \ "
                  rf"{e['IV']:.2f}", font_size=30),
            label(r"I $\succ$ II \ and \ IV $\succ$ III: \ Ellsberg's pattern, \ from aversion to \emph{ambiguity}",
                  font_size=26, color=E.ACCENT),
            label(r"risk: \ the chances are known; \ ambiguity: \ they are not \ (Knight, 1921: ``uncertainty'')",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(rows, DOWN, buff=0.55)
        with self.voiceover(
            "Why is this a paradox? <bookmark mark='a'/> If you prefer bet one to bet two, you must think red more "
            "likely than black. <bookmark mark='b'/> If you prefer four to three, you must think black or yellow more "
            "likely than red or yellow, which means black more likely than red. <bookmark mark='c'/> You can't believe "
            "both. Ellsberg's pattern isn't expected utility for any beliefs at all. <bookmark mark='d'/> One way to "
            "describe it came in 1989, from Itzhak Gilboa and David Schmeidler: maxmin expected utility. The chooser "
            "doesn't have one probability of black but a set of them, here anything from none of the sixty to all, "
            "and judges each bet by its worst case. <bookmark mark='e'/> Bet one wins with a third; bet two, in the "
            "worst case, never. Bet three, a third in the worst case; bet four, two thirds for sure. "
            "<bookmark mark='f'/> That's Ellsberg's pattern. It comes from aversion to ambiguity, to not knowing the "
            "chances, which is different from aversion to risk. <bookmark mark='g'/> Frank Knight had drawn the line "
            "in 1921: risk is when the chances are known, uncertainty when they aren't. Most of the economy's "
            "important gambles are the second kind."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(mm[0]))
            vo.wait_until("e")
            self.play(FadeIn(mm[1]))
            vo.wait_until("f")
            self.play(FadeIn(mm[2]))
            vo.wait_until("g")
            self.play(FadeIn(mm[3]))
        self.clear_scene()

    def prospect(self):
        p = load("paradoxes")
        xs, v = np.array(p["xs"]), np.array(p["value"])
        ps, w = np.array(p["ps"]), np.array(p["weight"])
        ax = plane([-100, 100], [-130, 70], center=LEFT * 4.1 + DOWN * 0.4, x_length=4.6, y_length=4.4,
                   xticks=[-100, -50, 0, 50, 100], yticks=[-100, -50, 0, 50], xlabel=r"gain or loss, \ \$",
                   ylabel=r"value", font_size=15)
        bx = plane([0, 1], [0, 1], center=RIGHT * 1.15 + DOWN * 0.4, x_length=3.3, y_length=3.3,
                   xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], xlabel=r"chance", ylabel=r"decision weight",
                   font_size=15)
        vc = path(ax, xs, v, color=FAN, width=3.5)
        axes0 = VGroup(DashedLine(ax.ax.c2p(-100, 0), ax.ax.c2p(100, 0), color=GREY_D, stroke_width=1.2),
                       DashedLine(ax.ax.c2p(0, -130), ax.ax.c2p(0, 70), color=GREY_D, stroke_width=1.2))
        wc = path(bx, ps, w, color=FAN, width=3.5)
        diag = DashedLine(bx.ax.c2p(0, 0), bx.ax.c2p(1, 1), color=GREY_C, stroke_width=1.5)
        side = VGroup(
            label(r"prospect theory, \ in one card", font_size=28, color=FAN),
            label(r"Kahneman and Tversky (1979, 1992):", font_size=21, color=GREY_B),
            label(r"value is of gains and losses \\ from a reference point, \\ not of wealth", font_size=21),
            label(r"losses loom larger: \\ about 2.25 times gains", font_size=21),
            label(r"small chances are overweighted, \\ large ones underweighted", font_size=21),
            label(r"the full account: \ \emph{Psychology, Built} \\ Part 26, \ and Part 45", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Tversky and Kahneman (1992): \ $\alpha = 0.88$, \ $\lambda = 2.25$, \ $\gamma = 0.61$",
                            corner=DR, font_size=14)
        with self.voiceover(
            "The best-known alternative to expected utility deserves a card here, though it has a part of its own "
            "later. <bookmark mark='a'/> In 1979 Daniel Kahneman and Amos Tversky proposed prospect theory. People "
            "value gains and losses from a reference point, usually where they stand now, not levels of wealth. "
            "<bookmark mark='b'/> The value function is concave for gains and convex for losses, and steeper for "
            "losses: in Tversky and Kahneman's 1992 estimates, a loss hurts about two and a quarter times as much as "
            "an equal gain pleases. <bookmark mark='c'/> And chances are weighted, not taken at face value: small "
            "chances count for more than they are, large ones for less. That weighting alone produces Allais's "
            "pattern. <bookmark mark='d'/> The psychology series takes this up in its Part twenty-six, and this "
            "series in Part forty-five."
        ) as vo:
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(axes0), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(Create(vc), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(bx), Create(diag), Create(wc), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(side[5]))
        self.clear_scene()
