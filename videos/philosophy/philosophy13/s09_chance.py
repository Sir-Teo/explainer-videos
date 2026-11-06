from __future__ import annotations

import random

from videos.philosophy.philosophy13.common import *  # noqa: F403

FAIR, BENT = "#6FB7FF", "#F2A65A"


class Chance(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Chance and credence", r"How should beliefs about chances guide belief?",
                            lit=(1980, 1937), part=PART)
        with self.voiceover("Chapter eight. Chance and credence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.interpretations()
        self.principal()
        self.mixture()
        self.definetti()
        self.bug()

    def interpretations(self):
        head = label(r"What is probability? \ Five answers", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [label(r"interpretation", font_size=21, color=P.CLAIM), label(r"probability is", font_size=21,
                                                                           color=P.CLAIM),
              label(r"its hardest problem", font_size=21, color=P.CLAIM)]
        rows = [
            (r"classical \ (Laplace)", r"favourable cases over equipossible cases", r"`equipossible': \ Bertrand"),
            (r"frequency \ (Venn, \ von Mises)", r"relative frequency in a long run", r"the single case; \ which "
                                                                                   r"reference class?"),
            (r"propensity \ (Popper)", r"a disposition of a set-up", r"Humphreys: \ inverse probabilities"),
            (r"best system \ (Lewis)", r"what the simplest strong laws say", r"undermining futures \ (end of "
                                                                            r"chapter)"),
            (r"subjective \ (Ramsey, \ de Finetti)", r"a rational degree of belief", r"which prior? \ (Ch.\ 6)"),
        ]
        trs = [[label(a, font_size=20, color=CRED), label(b, font_size=20), label(c, font_size=19, color=GREY_A)]
               for a, b, c in rows]
        grid = ValueGrid(hd, trs, col_w=[3.8, 4.8, 4.2], cell_h=0.62, font_size=20).next_to(head, DOWN, buff=0.4)
        foot = label(r"two families: \ \textit{chance}, \ out in the world, \ and \textit{credence}, \ in the head",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So far probability has meant credence. But scientists speak of chances in the world: the chance that "
            "an atom decays, that a coin lands heads. What is probability? Five classic answers, surveyed in Alan "
            "Hájek's article on the interpretations of probability. <bookmark mark='a'/>The classical view: the ratio "
            "of favourable to equipossible cases, which runs straight into Bertrand. <bookmark mark='b'/>The "
            "frequency view: the long-run relative frequency. But what of a single case, and which reference class "
            "is yours? <bookmark mark='c'/>Karl Popper's propensities: a disposition of the experimental set-up. "
            "Paul Humphreys objected that propensities cannot run backwards, yet conditional probabilities do. "
            "<bookmark mark='d'/>Lewis's best-system view: chances are whatever the simplest and strongest summary "
            "of the world's history says. <bookmark mark='e'/>And the subjective view of this part. "
            "<bookmark mark='f'/>Most philosophers now accept two families: chance, out in the world, and credence, "
            "in the head. The question is how they connect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abcde", range(5)):
                vo.wait_until(mk)
                self.play(*[FadeIn(m) for m in grid.cell[r]])
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def principal(self):
        hc = history_card(1980, r"David Lewis", r"`A Subjectivist's Guide to Objective Chance'", width=6.0,
                          color=HIST).to_corner(UL, buff=0.35)
        pp = MathTex(r"C\bigl(A \mid \mathrm{ch}(A) = x \,\land\, E\bigr) \;=\; x", font_size=46, color=CRED).move_to(
            [0, 1.0, 0])
        cap = label(r"the Principal Principle", font_size=28, color=GOAL).next_to(pp, UP, buff=0.3)
        rows = stack([
            (r"credence, \ given the chance, \ should equal the chance", WHITE),
            (r"for any \textit{admissible} evidence $E$: \ the past, \ the laws", GREY_A),
            (r"inadmissible: \ a crystal ball that shows the outcome", BAD),
            (r"so: \ $C(A) = \sum_x C(\mathrm{ch}(A) = x)\cdot x$, \ \ credence is expected chance", COH),
        ], font_size=25).next_to(pp, DOWN, buff=0.5)
        with self.voiceover(
            "David Lewis gave the connection in 1980, and called it the Principal Principle, because it captures, "
            "he said, all we know about chance. <bookmark mark='a'/>Your credence in A, given that the chance of A "
            "is x, should be x. <bookmark mark='b'/>That holds whatever else you know, provided it is admissible: "
            "facts about the past, and the laws. <bookmark mark='c'/>A crystal ball that showed you the coin's "
            "landing would be inadmissible; knowing that, you should ignore the chance. "
            "<bookmark mark='d'/>A consequence: if you are unsure of the chance, your credence is your expectation "
            "of the chance."
        ) as vo:
            self.play(FadeIn(hc))
            self.play(FadeIn(cap), Write(pp))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def mixture(self):
        head = label(r"Two coins in a bag: \ learning a chance", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rnd = random.Random(1981)
        flips = [1 if rnd.random() < 0.9 else 0 for _ in range(12)]
        post = [0.5]
        for f in flips:
            a, b = post[-1] * (0.9 if f else 0.1), (1 - post[-1]) * (0.5)
            post.append(a / (a + b))
        setup = stack([(r"a fair coin \ (chance $0.5$) \ and a bent one \ (chance $0.9$)", WHITE),
                       (r"one is drawn at random and flipped, \ again and again", GREY_A)], font_size=24).next_to(
            head, DOWN, buff=0.3)
        ax = Axes(x_range=[0, 12, 2], y_range=[0, 1, 0.5], x_length=7.0, y_length=3.0, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 18}).move_to([-2.0, -1.4, 0])
        xl = label(r"flips seen", font_size=20, color=GREY_B).next_to(ax, DOWN, buff=0.35)
        bent_pts = [ax.c2p(i, p) for i, p in enumerate(post)]
        cred_pts = [ax.c2p(i, 0.9 * p + 0.5 * (1 - p)) for i, p in enumerate(post)]
        bent_line = VMobject(stroke_color=BENT, stroke_width=3).set_points_as_corners(bent_pts)
        cred_line = VMobject(stroke_color=CRED, stroke_width=3).set_points_as_corners(cred_pts)
        marks = VGroup(*[MathTex(r"H" if f else r"T", font_size=20, color=OK if f else BAD).move_to(
            ax.c2p(i + 1, 1.12)) for i, f in enumerate(flips)])
        legend = stack([(r"$C(\text{bent coin})$", BENT), (r"$C(\text{next flip heads})$", CRED),
                        (r"$= 0.9\,C(\text{bent}) + 0.5\,C(\text{fair})$", GREY_A)], font_size=22,
                       aligned_edge=LEFT).move_to([4.6, -0.6, 0])
        start = MathTex(r"C(\text{heads}) = \tfrac12 (0.9) + \tfrac12 (0.5) = 0.7", font_size=30, color=CRED).move_to(
            [4.2, 1.2, 0])
        with self.voiceover(
            "A small example. <bookmark mark='a'/>A bag holds a fair coin and a bent coin that lands heads nine "
            "times in ten. One is drawn at random and flipped, again and again. <bookmark mark='b'/>Before any flip, "
            "by the Principal Principle, your credence in heads is the expected chance: half of point nine plus half "
            "of point five, point seven. Notice that point seven is nobody's chance. <bookmark mark='c'/>Now the "
            "flips come in. Each one updates your credence about which coin it is, by Bayes, <bookmark mark='d'/>and "
            "your credence in the next heads follows, always the expected chance. Two early tails make the fair coin "
            "look likely. But the heads keep coming, and after a dozen flips you are over ninety percent sure it is "
            "the bent coin, and your credence in heads is close to point nine. This is how credence learns chance."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(setup))
            vo.wait_until("b")
            self.play(FadeIn(start))
            vo.wait_until("c")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(legend))
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.15), Create(bent_line), run_time=4)
            vo.wait_until("d")
            self.play(Create(cred_line), run_time=2.5)
        self.clear_scene()

    def definetti(self):
        hc = history_card(1937, r"Bruno de Finetti", r"the representation theorem", width=4.8, color=HIST).to_corner(
            UL, buff=0.35)
        ex = label(r"exchangeable: \ the order of the flips doesn't matter to you", font_size=26,
                   color=CRED).next_to(hc, DOWN, buff=0.5).set_x(0)
        eq = MathTex(r"P(x_1, \dots, x_n) \;=\; \int_0^1 \theta^{k} (1 - \theta)^{n - k}\, d\mu(\theta)", font_size=42)
        eq.next_to(ex, DOWN, buff=0.45)
        k = label(r"$k$ = number of heads", font_size=22, color=GREY_A).next_to(eq, DOWN, buff=0.2)
        rows = stack([
            (r"every exchangeable credence \textit{acts as if} there were an unknown chance $\theta$, \ with prior $\mu$",
             WHITE),
            (r"the subjectivist gets `unknown chances' without believing in them", GOAL),
            (r"and the prior's influence fades: \ the posterior on $\theta$ concentrates", GREY_A)],
            font_size=23, width=12.4).next_to(k, DOWN, buff=0.45)
        with self.voiceover(
            "De Finetti, who said that probability does not exist, had an answer to talk of unknown chances. "
            "<bookmark mark='a'/>Call your credences about a sequence of flips exchangeable if the order doesn't "
            "matter to you: any sequence with the same number of heads gets the same credence. "
            "<bookmark mark='b'/>His representation theorem: then your credences are exactly as if there were an "
            "unknown chance theta, with you holding a prior over it, and flips independent given theta. "
            "<bookmark mark='c'/>Every exchangeable credence acts as if there were a chance. "
            "<bookmark mark='d'/>So the subjectivist can talk of learning unknown chances without believing that "
            "they exist. <bookmark mark='e'/>And as the flips accumulate, the posterior over theta concentrates, "
            "which is the washing out of chapter six."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(ex))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(k))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def bug(self):
        head = label(r"The big bad bug", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"Humean chances depend on the whole history, \ future included", WHITE),
            (r"so some futures, \ if they happened, \ would change the chances: \ `undermining'", WHITE),
            (r"the present chance of such a future $F$ is positive", GREY_A),
            (r"but given the chances, \ $F$ is impossible: \ the Principal Principle says $C(F) > 0$ and $C(F) = 0$",
             BAD),
            (r"repair: \ the New Principle \ (Lewis; \ Hall; \ Thau, \ 1994)", OK),
            (r"$C(A \mid H_{t} T) = \mathrm{ch}(A \mid T)$: \ condition on the laws too", CRED),
        ], font_size=23, width=12.4).next_to(head, DOWN, buff=0.45)
        foot = label(r"Part 24 returns to chance, \ laws, \ and Humean supervenience", font_size=22,
                     color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Lewis's own theory of chance nearly broke his principle. He called the problem the big bad bug. "
            "<bookmark mark='a'/>For a Humean, chances supervene on the whole history of the world, the future "
            "included. <bookmark mark='b'/>So there are possible futures that, were they to happen, would make the "
            "chances different. Call them undermining. <bookmark mark='c'/>The present chances give such a future a "
            "small positive chance. <bookmark mark='d'/>Yet if the chances are what they are, the undermining "
            "future cannot happen. The Principal Principle demands a positive credence and a zero credence at once. "
            "<bookmark mark='e'/>The repair, found in 1994 by Lewis, Ned Hall and Michael Thau, is the New "
            "Principle: <bookmark mark='f'/>condition the chance on the laws as well. <bookmark mark='g'/>Part 24, "
            "on laws, returns to this."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("g")
            self.play(FadeIn(foot))
        self.clear_scene()
