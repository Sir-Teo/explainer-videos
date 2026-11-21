from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403


def _sci(x: float) -> str:
    m, e = f"{x:.0e}".split("e")
    return rf"{m} \times 10^{{{int(e)}}}"


class Jacobians(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Sequence-space Jacobians", r"How do you solve a HANK model in a second?",
             "Chapter ten. Sequence-space Jacobians.",
             lit={2009: r"Reiter", 2021: r"Auclert, Bardóczy, Rognlie, Straub"},
             scale=("household", "nation"), horizon=("a decade",))
        self.idea()
        self.matrix()
        self.fakenews()
        self.speed()

    def idea(self):
        rows = VGroup(
            label(r"the old way: \ linearize in the distribution, \ thousands of state variables", font_size=22,
                  color=GREY_A),
            label(r"the new way: \ linearize in the paths of a few aggregates", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(UP, buff=0.7)
        ins = VGroup(*[label(t, font_size=22, color=c) for t, c in (
            (r"$r_0, r_1, \dots, r_{T-1}$", DIRECT), (r"$Z_0, Z_1, \dots, Z_{T-1}$", INDIRECT))]).arrange(
            DOWN, buff=0.5)
        box = RoundedRectangle(width=3.6, height=2.2, corner_radius=0.15, stroke_color=MANY, fill_color=MANY,
                               fill_opacity=0.12)
        blab = label(r"every household: \\ rules backward, \\ distribution forward", font_size=19,
                     color=WHITE).move_to(box)
        outs = label(r"$C_0, C_1, \dots, C_{T-1}$", font_size=22, color=WHITE)
        VGroup(ins, VGroup(box, blab), outs).arrange(RIGHT, buff=1.0).move_to(DOWN * 0.6)
        a1 = Arrow(ins.get_right(), box.get_left(), color=GREY_B, buff=0.15)
        a2 = Arrow(box.get_right(), outs.get_left(), color=GREY_B, buff=0.15)
        jac = MathTex(r"\mathbf{J}^{C,Z}_{t,s} = \frac{\partial C_t}{\partial Z_s}", font_size=38,
                      color=THEORY).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Solving a model like this one used to be hard: after a shock the distribution moves, and the old "
            "approach linearized the economy in thousands of numbers that describe it. <bookmark mark='a'/> "
            "Adrien Auclert, Bence Bardóczy, Matthew Rognlie and Ludwig Straub turned the problem sideways. "
            "<bookmark mark='b'/> Treat the households as a single block. Feed it whole paths: the interest rate in "
            "each of the next three hundred quarters, and incomes in each quarter. <bookmark mark='c'/> Inside, "
            "every household solves its rules backward from the end and the distribution moves forward from today. "
            "<bookmark mark='d'/> Out comes the path of total spending. <bookmark mark='e'/> Linearize that map, "
            "and it is a matrix: how spending in quarter t responds to income in quarter s. A Jacobian, in the "
            "space of sequences."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(ins), GrowArrow(a1))
            vo.wait_until("c")
            self.play(FadeIn(box), FadeIn(blab))
            vo.wait_until("d")
            self.play(GrowArrow(a2), FadeIn(outs))
            vo.wait_until("e")
            self.play(Write(jac))
        self.clear_scene()

    def matrix(self):
        J = load("jacobian")
        M = np.array(J["J"])
        n = M.shape[0]
        size = 4.6
        cell = size / n
        top = float(np.percentile(np.abs(M), 99.5))
        sq = VGroup()
        for i in range(n):
            for j in range(n):
                v = float(np.clip(M[i, j] / top, 0, 1)) ** 0.5
                sq.add(Square(side_length=cell, stroke_width=0, fill_color=interpolate_color(
                    ManimColor("#0E1117"), ManimColor(INDIRECT), v), fill_opacity=1.0).move_to(
                    [(j - n / 2 + 0.5) * cell, (n / 2 - i - 0.5) * cell, 0]))
        frame = Square(side_length=size, stroke_color=GREY_B, stroke_width=1.2)
        mat = VGroup(sq, frame).move_to(LEFT * 3.3 + DOWN * 0.3)
        xl = label(r"income in quarter $s$ \ $\rightarrow$", font_size=17, color=GREY_A).next_to(mat, UP, buff=0.15)
        yl = label(r"spending in quarter $t$ \ $\rightarrow$", font_size=17, color=GREY_A).rotate(-PI / 2).next_to(
            mat, LEFT, buff=0.15)
        ax = plane([0, 20], [0, 0.3], center=RIGHT * 3.4 + UP * 0.6, x_length=5.2, y_length=3.0,
                   xticks=[0, 5, 10, 15, 20], yticks=[0, 0.1, 0.2, 0.3], xlabel=r"quarter $t$",
                   ylabel=r"$\partial C_t / \partial Z_s$", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=13)
        cols = (INDIRECT, MANY, DIST)
        curves = VGroup(*[path(ax, np.arange(20), np.array(J["col_fake"][str(s)])[:20], c, 2.6, smooth=False)
                          for s, c in zip(J["cols"][:2], cols)])
        side = VGroup(
            label(r"gold: \ income today, \ spent \\ mostly at once, \ then less", font_size=17, color=INDIRECT),
            label(r"green: \ income announced for \\ quarter 10: \ some spent before \\ it arrives", font_size=17,
                  color=MANY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, DOWN, buff=0.5).align_to(ax, LEFT)
        with self.voiceover(
            "Here is that matrix for the Island's households, the first forty quarters. <bookmark mark='a'/> Each "
            "column is the path of spending after a one-off rise in income in one quarter; each row, a quarter's "
            "spending. The bright diagonal says that income is spent mostly when it arrives. <bookmark mark='b'/> "
            "Take the first column: income today. Spending jumps at once, then decays over the following quarters, "
            "the intertemporal marginal propensities to consume. <bookmark mark='c'/> Take the column for income "
            "announced today but paid in quarter ten. Households who can borrow or draw on savings spend some of "
            "it before it arrives; those at their limit cannot, so the jump comes when the money does."
        ) as vo:
            self.play(FadeIn(frame), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(sq, lag_ratio=0.002), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(ax), Create(curves[0]), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(curves[1]), FadeIn(side[1]), run_time=1.6)
        self.clear_scene()

    def fakenews(self):
        steps = flow_chain([(r"one backward pass: \ how news about quarter s changes today's rules", DIRECT),
                            (r"one forward pass: \ how a change in tomorrow's distribution shows up later",
                             DIST),
                            (r"the fake-news matrix", INDIRECT),
                            (r"a running sum down the diagonals: \ the Jacobian", THEORY)], box_w=2.9, box_h=1.5,
                           font_size=18, buff=0.45).move_to(UP * 1.2)
        eq = MathTex(r"\mathbf{J}_{t,s} = \mathbf{F}_{t,s} + \mathbf{J}_{t-1,s-1}", font_size=42,
                     color=THEORY).next_to(steps, DOWN, buff=0.8)
        why = label(r"news about quarter $s$, \ heard at 0, \ acts like news about $s - 1$ heard at 1, \ shifted",
                    font_size=20, color=GREY_A).next_to(eq, DOWN, buff=0.4)
        with self.voiceover(
            "Building the matrix one column at a time would mean solving the economy three hundred times. The "
            "authors found a shortcut they called the fake-news algorithm. <bookmark mark='a'/> One backward pass "
            "records how news about each future quarter changes households' rules today. <bookmark mark='b'/> One "
            "forward pass records how a change in next quarter's distribution shows up in spending later. "
            "<bookmark mark='c'/> Combined, they give a matrix of the effects of news, <bookmark mark='d'/> and a "
            "running sum down its diagonals turns that into the Jacobian. The trick rests on time being the same "
            "everywhere: hearing today about quarter s is like hearing next quarter about s minus one, shifted by "
            "a quarter."
        ) as vo:
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                an = [FadeIn(steps.boxes[k], shift=UP * 0.1)]
                if k > 0:
                    an.append(Create(steps.arrows[k - 1]))
                self.play(*an)
            self.play(Write(eq), FadeIn(why))
        self.clear_scene()

    def speed(self):
        J = load("jacobian")
        ax = plane([0, 40], [0, 0.3], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.0, y_length=4.4,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 0.1, 0.2, 0.3], xlabel=r"quarter $t$",
                   ylabel=r"$\partial C_t / \partial Z_s$", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=13)
        fake = VGroup()
        brute = VGroup()
        for s, c in zip(J["cols"], (INDIRECT, MANY, DIST)):
            fake.add(path(ax, np.arange(40), J["col_fake"][str(s)], c, 3.0, smooth=False))
            brute.add(VGroup(*[dot(ax, t, v, WHITE, 0.035) for t, v in enumerate(J["col_brute"][str(s)])
                               if t % 2 == 0]))
        side = VGroup(
            label(r"lines: \ the fake-news algorithm", font_size=19, color=WHITE),
            label(r"dots: \ brute force, \ the economy \\ solved again for each column", font_size=19, color=GREY_A),
            label(r"largest difference: \ $" + _sci(J["max_error"]) + "$", font_size=18, color=WHITE),
            label(rf"all {2 * J['T']} columns: \\ fake news {J['fake_seconds']:.2f} s \\ brute force about "
                  rf"{J['brute_seconds_all']:.0f} s \\ (estimated from three)", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Auclert, \ Bardóczy, \ Rognlie and Straub, \ Econometrica 89(5) (2021)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Does it work? <bookmark mark='a'/> The lines are three columns from the fake-news algorithm. "
            "<bookmark mark='b'/> The dots are the same columns computed by brute force, solving the whole "
            "economy again with income raised in one quarter. <bookmark mark='c'/> They agree to the fifth decimal "
            "place, the error of the small step both use. <bookmark mark='d'/> The difference is the "
            f"time. All {2 * J['T']} columns, for interest rates and incomes, took {J['fake_seconds']:.2f} "
            f"seconds; by brute force, an estimated {J['brute_seconds_all']:.0f}. Once the Jacobians are in hand, "
            "solving the economy's response to any shock is a single linear solve: the equations of chapter nine, "
            "each one a matrix."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(f) for f in fake], lag_ratio=0.3), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in brute], lag_ratio=0.3), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()
