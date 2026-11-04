from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import COST, CTRL, DATA, HEAD, INF, NO, PART, YES, load, step_counter, tape_from

PHASE = {"copy": r"copy the input onto tape 2", "rewind": r"rewind tape 1", "compare":
         r"compare: \ tape 1 forwards, \ tape 2 backwards", "accept": r"accept"}


class Robust(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_tapes()
        self.race()
        self.simulation()
        self.variants()
        self.nondeterminism()

    def card(self):
        card = chapter_card(6, r"More tapes, same power", r"Does a more elaborate machine compute more?",
                            lit=(1936,), part=PART)
        with self.voiceover("Chapter six. More tapes, same power."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def two_tapes(self):
        d = load("palindrome")
        hist = d["run2_0110"]
        lo = -1
        head = label(r"Two tapes, \ two heads, \ one table", font_size=40).to_edge(UP, buff=0.35)
        v1 = tape_from(hist[0], lo, tape=0, cell=0.66, font_size=30).move_to(UP * 0.9)
        v2 = tape_from(hist[0], lo, tape=1, cell=0.66, font_size=30, show_state=False).move_to(DOWN * 1.0)
        l1 = label(r"tape 1", font_size=26, color=GREY_B).next_to(v1, LEFT, buff=0.35)
        l2 = label(r"tape 2", font_size=26, color=GREY_B).next_to(v2, LEFT, buff=0.35)
        phase = label(PHASE["copy"], font_size=30, color=CTRL).to_edge(DOWN, buff=0.9)
        rule = label(r"a rule now reads a symbol from \textit{each} tape, \ writes to each, \ moves each head",
                     font_size=26, color=GREY_A).next_to(head, DOWN, buff=0.25)
        cnt = step_counter().to_corner(DR, buff=0.4)
        with self.voiceover(
            "Give the machine a second tape, with its own head. A rule now reads the symbols under both heads, writes "
            "on both tapes, and moves both heads, each left or right. <bookmark mark='a'/> Palindromes become easy. "
            "Copy the input onto tape two. Rewind tape one. Then compare: tape one read forwards, tape two read "
            "backwards, both at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rule), FadeIn(v1), FadeIn(v2), FadeIn(l1), FadeIn(l2))
            vo.wait_until("a")
            self.play(FadeIn(phase), FadeIn(cnt))
        with self.voiceover(
            f"On zero one one zero it takes {len(hist) - 1} steps, the same as one tape. But the zig-zag is gone: each "
            f"head crosses the input a fixed number of times."
        ):
            for i in range(len(hist) - 1):
                a, b = hist[i], hist[i + 1]
                anims = []
                for k, v in enumerate((v1, v2)):
                    new = b["tapes"][k][a["heads"][k] - lo]
                    mv = b["heads"][k] - a["heads"][k]
                    anims.append(v.step(new, mv, b["state"] if k == 0 else v.state, run_time=0.7))
                if b["state"] != a["state"] and b["state"] in PHASE:
                    np_ = label(PHASE[b["state"]], font_size=30, color=YES if b["state"] == "accept" else CTRL)
                    anims.append(Transform(phase, np_.move_to(phase)))
                self.play(*anims, cnt.tracker.animate(run_time=0.7).set_value(i + 1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        d = load("palindrome")
        ns, one, two = (np.array(d[k], float) for k in ("n", "one", "two"))
        ax = CornerAxes(x_range=[0, 60, 10], y_range=[0, 1900, 500], x_length=8.4, y_length=4.8, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_numbers": True, "font_size": 20})
        ax.move_to(DOWN * 0.4)
        xl = label(r"length of the input, $n$", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yl = label(r"steps", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        c1 = curve(ax, ns, one, COST, 3)
        c2 = curve(ax, ns, two, DATA, 3)
        l1 = label(r"one tape: \ $\approx n^2/2$", font_size=28, color=COST).next_to(ax.c2p(46, one[45]), LEFT, buff=0.3)
        l2 = label(r"two tapes: \ $3n + 3$", font_size=28, color=DATA).next_to(ax.c2p(56, two[55]), UP, buff=0.3)
        assert all(two[i] == 3 * ns[i] + 3 for i in range(len(ns)))
        with self.voiceover(
            "Measured on every length up to sixty: with one tape the steps grow like n squared over two. With two tapes, "
            "exactly three n plus three. <bookmark mark='a'/> So a second tape makes the machine faster, and Hennie's "
            "theorem says no one-tape program can catch up. Does it also make the machine more powerful: can two tapes "
            "compute something one tape cannot?"
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(c1), FadeIn(l1), run_time=1.6)
            self.play(Create(c2), FadeIn(l2), run_time=1.2)
            vo.wait_until("a")
            self.play(Indicate(l2, color=DATA))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def simulation(self):
        thm = theorem_card(r"one tape simulates many", r"For every $k$-tape machine there is a one-tape machine that "
                           r"computes the same thing; \ $t$ steps of the $k$-tape machine take $O(t^2)$ steps on one tape.",
                           width=11.4, font_size=26).to_edge(UP, buff=0.35)
        # the two tapes of a mid-run configuration
        t1, t2 = list("0110"), list("011_")
        top = TapeView(t1, head=2, state="cmp", cell=0.55, font_size=26, ellipsis=False).move_to(UP * 0.7 + LEFT * 2.6)
        bot = TapeView(t2, head=1, state=None, cell=0.55, font_size=26, ellipsis=False).move_to(DOWN * 0.7 + LEFT * 2.6)
        # one tape: # 0 1 1 0 # 0 1 1 _ #, with the two virtual heads marked
        syms = ["#"] + t1 + ["#"] + t2 + ["#"]
        one = TapeView(syms, head=None, state=None, cell=0.55, font_size=26).move_to(DOWN * 0.1 + RIGHT * 0.0)
        marks = VGroup()
        for idx in (1 + 2, 6 + 1):
            dot = Dot(radius=0.07, color=HEAD).next_to(one.cells[idx], DOWN, buff=0.08)
            marks.add(dot)
        mark_l = label(r"dots: \ where each tape's head is", font_size=24, color=HEAD).next_to(one, DOWN, buff=0.5)
        sweep = Triangle(color=C.CS_HEAD, fill_opacity=1, stroke_width=0).rotate(PI).scale_to_fit_width(0.24)
        sweep.next_to(one.cells[0], UP, buff=0.08)
        how = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"sweep right: \ read the marked symbols \ (remember them in the state)", DATA),
            (r"sweep left: \ write, \ and move each dot", CTRL),
            (r"a dot reaching a \# \ shifts everything right by one cell", GREY_A),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "No. Here is why. <bookmark mark='a'/> Take any configuration of a two-tape machine. <bookmark mark='b'/> "
            "Write both tapes onto a single tape, side by side, separated by a marker symbol. Mark where each head is "
            "with a dot: a dotted zero is just one more symbol in a bigger alphabet. <bookmark mark='c'/> To simulate "
            "one step, the single head sweeps right across everything, collecting the dotted symbols in its state, "
            "<bookmark mark='d'/> then sweeps back, writing the new symbols and moving the dots. If a dot runs into a "
            "separator, the tape is shifted along to make room."
        ) as vo:
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(top), FadeIn(bot))
            vo.wait_until("b")
            self.play(ReplacementTransform(VGroup(top.cells, top.syms), VGroup(*one.cells[1:5], *one.syms[1:5])),
                      ReplacementTransform(VGroup(bot.cells, bot.syms), VGroup(*one.cells[6:10], *one.syms[6:10])),
                      FadeOut(top.head), FadeOut(bot.head), run_time=1.6)
            self.play(FadeIn(VGroup(one.cells[0], one.cells[5], one.cells[10], one.syms[0], one.syms[5], one.syms[10],
                                    one.dots)), FadeIn(marks), FadeIn(mark_l))
            vo.wait_until("c")
            self.play(FadeIn(sweep), FadeIn(how[0]))
            self.play(sweep.animate.next_to(one.cells[-1], UP, buff=0.08), run_time=2.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(how[1]))
            self.play(sweep.animate.next_to(one.cells[0], UP, buff=0.08), marks[0].animate.shift(RIGHT * 0.55),
                      marks[1].animate.shift(LEFT * 0.55), run_time=2.0, rate_func=linear)
            self.play(FadeIn(how[2]))
        d = load("palindrome")
        ns, two, sim = (np.array(d[k], float) for k in ("n", "two", "sim"))
        ax = CornerAxes(x_range=[0, 60, 10], y_range=[0, 60000, 20000], x_length=7.6, y_length=3.9, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_numbers": True, "font_size": 20})
        ax.move_to(DOWN * 1.05)
        xl = label(r"length of the input, $n$", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yl = label(r"steps", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        cs = curve(ax, ns, sim, INF, 3)
        c2 = curve(ax, ns, two, DATA, 3)
        ls = label(r"two tapes, simulated on one", font_size=26, color=INF).next_to(ax.c2p(40, sim[39]), LEFT, buff=0.3)
        l2 = label(r"two tapes", font_size=26, color=DATA).next_to(ax.c2p(58, two[57]), UP, buff=0.2)
        ratio = sim[-1] / two[-1] ** 2
        with self.voiceover(
            f"Each simulated step costs a sweep over everything written so far, and after t steps that is at most "
            f"about t cells. So t steps become about t squared. <bookmark mark='a'/> Here is the simulation, run for "
            f"real on the palindrome machine: its steps grow quadratically, about {ratio:.1f} times the square of the "
            f"two-tape step count at length sixty. Slower, much slower; but it computes exactly the same answers."
        ) as vo:
            self.play(*[FadeOut(m) for m in (one, marks, mark_l, sweep, how)])
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(c2), FadeIn(l2))
            self.play(Create(cs), FadeIn(ls), run_time=1.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def variants(self):
        head = label(r"Every reasonable variation computes the same things", font_size=36).to_edge(UP, buff=0.4)
        rows = [
            (r"a tape infinite in both directions", r"fold it in half: \ two tracks", r"constant"),
            (r"more symbols", r"write each in binary", r"constant"),
            (r"a ``stay'' move", r"move right and back", r"constant"),
            (r"$k$ tapes", r"tracks and dots, \ as above", r"quadratic"),
            (r"a 2-dimensional tape", r"store the grid row by row", r"polynomial"),
            (r"random access memory", r"a tape of (address, value) pairs", r"polynomial"),
        ]
        hdr = VGroup(*[label(t, font_size=24, color=GREY_B) for t in
                       (r"the extra feature", r"how one tape simulates it", r"slowdown")])
        tab = VGroup(hdr, *[VGroup(label(a, font_size=26), label(b, font_size=26, color=GREY_A),
                                   label(c, font_size=26, color=COST)) for a, b, c in rows])
        for r in tab:
            r[0].move_to([-3.6, 0, 0], aligned_edge=LEFT).shift(LEFT * 0.0)
        tab.arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.2)
        for r in tab:
            r[0].set_x(-6.4 + r[0].width / 2)
            r[1].set_x(-0.6 + r[1].width / 2)
            r[2].set_x(4.9 + r[2].width / 2)
        line = Line([-6.4, 0, 0], [6.6, 0, 0], color=GREY_D).next_to(hdr, DOWN, buff=0.15)
        line.set_x(0.1)
        with self.voiceover(
            "The same trick works for every variation anyone proposed. <bookmark mark='a'/> A tape infinite in both "
            "directions: fold it into two tracks. More symbols: write each one as a few binary digits. A stay-put move: "
            "step right and back. Several tapes: tracks and dots. A two-dimensional tape, or memory you can jump around "
            "in by address: lay it out in a row. <bookmark mark='b'/> Each extra feature can be simulated by the plain "
            "machine, at worst with a polynomial slowdown. The set of things that can be computed does not move."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), Create(line))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[1:]], lag_ratio=0.35), run_time=3.0)
            vo.wait_until("b")
            self.play(*[Indicate(r[2], color=COST) for r in tab[1:]])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nondeterminism(self):
        head = label(r"Nondeterminism: \ several possible moves", font_size=38).to_edge(UP, buff=0.35)
        # a computation tree: depth 4, branching 2, one accepting leaf
        rng = np.random.default_rng(4)
        levels = 5
        nodes = {}
        tree = VGroup()
        for lv in range(levels):
            k = 2 ** lv
            for i in range(k):
                x = (i + 0.5) / k * 11.0 - 5.5
                y = 2.2 - lv * 1.05
                acc = lv == levels - 1 and i == 11
                rej = lv == levels - 1 and not acc
                c = YES if acc else (NO if rej else GREY_B)
                dot = Dot([x, y, 0], radius=0.09 if lv < levels - 1 else 0.1, color=c)
                nodes[(lv, i)] = dot
                tree.add(dot)
                if lv:
                    par = nodes[(lv - 1, i // 2)]
                    tree.add(Line(par.get_center(), dot.get_center(), color=GREY_D, stroke_width=1.5).set_z_index(-1))
        path = VGroup()
        i = 11
        for lv in range(levels - 1, 0, -1):
            path.add(Line(nodes[(lv - 1, i // 2)].get_center(), nodes[(lv, i)].get_center(), color=YES, stroke_width=4))
            i //= 2
        acc_l = label(r"accept \ if \textit{some} branch accepts", font_size=28, color=YES).to_edge(DOWN, buff=1.0)
        cost = label(r"a deterministic machine can try every branch, \ breadth first: \ up to $2^t$ of them for $t$ steps",
                     font_size=26, color=COST).to_edge(DOWN, buff=0.4)
        schem = schematic_tag(UR)
        with self.voiceover(
            "One more variation, and the most important. Let the table offer several possible moves in some "
            "configurations, and let the machine take any of them. A run is no longer a line but a tree of "
            "possibilities. <bookmark mark='a'/> Say the machine accepts if any branch accepts. <bookmark mark='b'/> "
            "This still computes nothing new: a deterministic machine can explore the tree, level by level, until it "
            "finds an accepting branch. But the tree can have two to the t branches after t steps, and the obvious "
            "simulation takes exponential time. Whether that exponential can always be avoided is the most famous open "
            "question in computer science, P versus NP: Part 26."
        ) as vo:
            self.play(FadeIn(head), FadeIn(schem))
            self.play(LaggedStart(*[FadeIn(m) for m in tree], lag_ratio=0.01), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(path), FadeIn(acc_l))
            vo.wait_until("b")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()
