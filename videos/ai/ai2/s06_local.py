from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import (COLD, FAIL, FCOL, GCOST, HEUR, HIST, HOT, LEARN, PART, PATH, load, queens_board,
                                  tour_mob)


def landscape(x):
    return (1.2 * np.exp(-((x - 1.5) ** 2) / 0.5) + 2.2 * np.exp(-((x - 5.2) ** 2) / 0.8)
            + 0.9 * np.exp(-((x - 3.3) ** 2) / 0.25) + 0.15 * np.sin(3 * x) + 0.4)


def temp_color(T, T0, T1):
    t = float(np.clip((np.log(T) - np.log(T1)) / (np.log(T0) - np.log(T1)), 0, 1))
    return interpolate_color(ManimColor(COLD), ManimColor(HOT), t)


class Local(VoiceoverScene):
    def construct(self):
        self.card()
        self.hills()
        self.queens()
        self.metropolis()
        self.cooling()
        self.budgets()
        self.genetic()

    def card(self):
        card = chapter_card(5, r"Climbing and cooling", r"What if the path doesn't matter, only where you end up?",
                            lit=(1983,), part=PART)
        with self.voiceover("Chapter five. Climbing and cooling."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def hills(self):
        ax = Axes(x_range=[0, 7, 1], y_range=[0, 3, 1], x_length=10.0, y_length=3.9, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to(DOWN * 0.75)
        graph = ax.plot(landscape, x_range=[0, 7], color=GCOST, stroke_width=4)
        area = ax.get_area(graph, x_range=[0, 7], color=GCOST, opacity=0.12)
        xl = label(r"states", font_size=22, color=GREY_B).next_to(ax, DOWN, buff=0.1)
        yl = label(r"how good \ (minus the cost)", font_size=22, color=GREY_B).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        xs = [0.3]
        for _ in range(40):  # steepest ascent on the curve, small steps
            x = xs[-1]
            best = max([x - 0.15, x, x + 0.15], key=lambda v: landscape(np.clip(v, 0, 7)))
            if best == x:
                break
            xs.append(best)
        ball = glow_dot(ax.c2p(xs[0], landscape(xs[0])), color=FCOL, radius=0.1)
        tr = ValueTracker(0)
        ball.add_updater(lambda m: m.move_to(ax.c2p(np.interp(tr.get_value(), range(len(xs)), xs),
                                                    landscape(np.interp(tr.get_value(), range(len(xs)), xs)))))
        loc = label(r"a local maximum: \ every neighbour is worse", font_size=22, color=FAIL)
        loc.next_to(ax.c2p(1.5, landscape(1.5)), UP, buff=0.35)
        glob = label(r"the global maximum", font_size=22, color=PATH).next_to(ax.c2p(5.2, landscape(5.2)), UP, buff=0.25)
        dc = definition_card(r"hill climbing", r"keep one state; \ move to the best neighbour; \ stop when none is "
                             r"better", width=4.6, font_size=21, color=FCOL).to_corner(UL, buff=0.3)
        with self.voiceover(
            "Often the path doesn't matter, only the final state: a schedule, a chip layout, a tour. Then keep a single state "
            "and improve it step by step. <bookmark mark='a'/> Picture the states as a landscape, height meaning quality. Hill "
            "climbing always steps to the best neighbour. <bookmark mark='b'/> It is fast and needs almost no memory. "
            "<bookmark mark='c'/> And it stops on the first peak it reaches, a local maximum, while the highest peak is "
            "somewhere else."
        ) as vo:
            self.play(Create(ax), Create(graph), FadeIn(area), FadeIn(xl), FadeIn(yl), FadeIn(tag), FadeIn(dc))
            vo.wait_until("a")
            self.add(ball)
            vo.wait_until("b")
            self.play(tr.animate.set_value(len(xs) - 1), run_time=3.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(loc), FadeIn(glob))
        ball.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def queens(self):
        d = load("queens")
        runs = d["runs"]
        cell = 0.48
        boards = {}
        for k, x in (("stuck", -3.6), ("solved", 3.6)):
            boards[k] = queens_board(runs[k]["boards"][0], cell=cell, center=[x, 0.5, 0])
        heads = VGroup(label(r"stuck", font_size=28, color=FAIL).next_to(boards["stuck"], UP, buff=0.25),
                       label(r"solved", font_size=28, color=PATH).next_to(boards["solved"], UP, buff=0.25))

        def hlab(k, i):
            h = runs[k]["h"][i]
            return label(rf"step ${i}$: \ ${h}$ attacking pairs", font_size=24,
                         color=(PATH if h == 0 else GREY_A)).next_to(boards[k], DOWN, buff=0.25)

        hl = {k: hlab(k, 0) for k in boards}
        p, s = d["plain"], d["sideways"]
        stats = VGroup(
            label(rf"from ${d['n_starts']:,}$ random starts:".replace(",", "{,}"), font_size=22, color=GREY_A),
            label(rf"steepest ascent solves ${100 * p['success']:.0f}\%$, \ in ${p['steps_ok']:.1f}$ steps; \ "
                  rf"stuck after ${p['steps_fail']:.1f}$", font_size=22, color=FCOL),
            label(rf"allowing $100$ sideways moves: \ ${100 * s['success']:.0f}\%$", font_size=22, color=HEUR),
            label(rf"random restarts: \ solved for certain, \ about ${p['restart_steps']:.0f}$ steps in all",
                  font_size=22, color=PATH),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).to_edge(DOWN, buff=0.2)
        intro = label(r"eight queens, \ one per column: \ move one queen within its column", font_size=24,
                      color=GREY_A).to_edge(UP, buff=0.25)
        with self.voiceover(
            "The classic test: eight queens on a chessboard, none attacking another. One queen per column; a move shifts a "
            "queen within its column; the height is the number of attacking pairs. <bookmark mark='a'/> Two runs of steepest "
            "descent. On the left, the attacks fall, then stop: no move helps. <bookmark mark='b'/> On the right, the same rule "
            f"reaches a solution. <bookmark mark='c'/> Over {d['n_starts']:,} random starts it solves "
            f"{100 * p['success']:.0f} percent, in {p['steps_ok']:.0f} steps on average; the rest get stuck after "
            f"{p['steps_fail']:.0f}. <bookmark mark='d'/> Allow sideways moves across plateaus, and it solves "
            f"{100 * s['success']:.0f} percent. Or restart whenever stuck: about {1 / p['success']:.0f} tries, around "
            f"{p['restart_steps']:.0f} steps in all."
        ) as vo:
            self.play(FadeIn(intro), FadeIn(boards["stuck"]), FadeIn(boards["solved"]), FadeIn(heads),
                      FadeIn(hl["stuck"]), FadeIn(hl["solved"]))
            for k, mk in (("stuck", "a"), ("solved", "b")):
                vo.wait_until(mk)
                for i in range(1, len(runs[k]["boards"])):
                    nb = queens_board(runs[k]["boards"][i], cell=cell, center=boards[k].get_center())
                    nl = hlab(k, i)
                    self.play(Transform(boards[k], nb), Transform(hl[k], nl), run_time=0.7)
                    self.wait(0.15)
            vo.wait_until("c")
            self.play(FadeIn(stats[0]), FadeIn(stats[1]))
            vo.wait_until("d")
            self.play(FadeIn(stats[2]), FadeIn(stats[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def metropolis(self):
        rule = cmath(r"P(\text{accept a change } \Delta E > 0)", r"=", r"e^{-\Delta E / T}", font_size=40)
        rule[2].set_color(HOT)
        rule.to_edge(UP, buff=0.5)
        hc = history_card(1983, r"Kirkpatrick, Gelatt \& Vecchi, \textit{Optimization by Simulated Annealing}, "
                          r"\textit{Science}", r"the Metropolis rule of $1953$, from statistical physics, \ with a "
                          r"temperature lowered slowly, \ as when metal is annealed", width=6.0, color=HIST,
                          font_size=20).to_corner(DL, buff=0.25)
        rows = [
            cmath(r"\pi(s)\, P(s \to s')", r"=", r"\pi(s')\, P(s' \to s)", font_size=36),
            cmath(r"\pi(s)\, q\, e^{-\Delta E/T}", r"=", r"\pi(s')\, q", font_size=36),
            cmath(r"\frac{\pi(s')}{\pi(s)}", r"=", r"e^{-(E(s') - E(s))/T}", font_size=36),
            cmath(r"\pi(s)", r"\propto", r"e^{-E(s)/T}", font_size=40),
        ]
        whys = [why(r"balance: \ as much flow each way"), why(r"uphill accepted w.p. $e^{-\Delta E/T}$, \ downhill always"),
                why(r"divide"), why(r"Boltzmann's distribution")]
        rows[3][2].set_color(HOT)
        step = ladder(self, rows, whys, keep=4, top=1.7, x=1.2)
        concl = label(r"$T \to 0$: \ all the probability piles onto the lowest states", font_size=24, color=COLD)
        concl.to_corner(DR, buff=0.3)
        with self.voiceover(
            "Simulated annealing escapes local optima by sometimes going the wrong way. <bookmark mark='a'/> Propose a random "
            "change. If it lowers the cost, take it; if it raises the cost by delta E, take it anyway with probability e to "
            "the minus delta E over T, where T is a temperature. <bookmark mark='b'/> Why that rule? At a fixed temperature, in "
            "equilibrium, the flow from s to s prime equals the flow back. <bookmark mark='c'/> Uphill moves are accepted with "
            "that probability, downhill always, and proposals are symmetric. <bookmark mark='d'/> Divide, "
            "<bookmark mark='e'/> and the time spent in each state follows Boltzmann's distribution. <bookmark mark='f'/> As T "
            "falls toward zero, it concentrates on the lowest-cost states."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Write(rule))
            for i, mk in enumerate("bcde"):
                vo.wait_until(mk)
                step(i)
            vo.wait_until("f")
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cooling(self):
        d = load("tsp")
        xy = np.asarray(d["xy"], float)
        snaps = np.asarray(d["sa_snaps"])
        tr = np.asarray(d["sa_trace"])
        every = int(d["sa_snap_every"])
        n_snaps = int(min(len(snaps), len(tr) // every))
        T0, T1 = tr[0, 0], tr[-1, 0]
        ax = Axes(x_range=[0, 1800, 300], y_range=[0, 1200, 300], x_length=6.6, y_length=4.4, tips=False,
                  axis_config={"stroke_opacity": 0}).move_to([-3.2, -0.2, 0])
        cities = VGroup(*[Dot(ax.c2p(*p), radius=0.05, color=WHITE) for p in xy])
        frame = SurroundingRectangle(ax, buff=0.1, color=GREY_D, stroke_width=1.5)
        k = ValueTracker(0)

        def tour():
            i = int(np.clip(k.get_value(), 0, n_snaps - 1))
            T = tr[i * every, 0]
            return tour_mob(ax, xy, snaps[i], color=temp_color(T, T0, T1), width=3)

        live = always_redraw(tour)
        # the length and the temperature against time
        steps = np.arange(len(tr))
        g = axes([0, len(tr)], [7000, max(26000, tr[:, 1].max() + 1000)], x_length=5.0, y_length=3.0,
                 xlabel=r"temperature steps (cooling $\to$)", ylabel=r"tour length", xticks=[0, len(tr)],
                 yticks=[10000, 20000], yfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), center=[3.9, 0.9, 0])
        cur = curve(g.ax, steps, tr[:, 1], GREY_B, 2)
        opt = DashedLine(g.ax.c2p(0, d["opt"]), g.ax.c2p(len(tr), d["opt"]), color=PATH, dash_length=0.08)
        ol = label(rf"optimum ${d['opt']:,}$".replace(",", "{,}"), font_size=18, color=PATH).next_to(opt, UP, buff=0.05)
        ol.align_to(opt, RIGHT)
        dot = always_redraw(lambda: Dot(g.ax.c2p(int(np.clip(k.get_value(), 0, n_snaps - 1)) * every,
                                                 tr[int(np.clip(k.get_value(), 0, n_snaps - 1)) * every, 1]),
                                        radius=0.07, color=FCOL))
        tnum = DecimalNumber(T0, num_decimal_places=1, font_size=30, color=HOT)
        tnum.add_updater(lambda m: m.set_value(tr[int(np.clip(k.get_value(), 0, n_snaps - 1)) * every, 0]))
        tlab = VGroup(MathTex("T =", font_size=30, color=GREY_A), tnum).arrange(RIGHT, buff=0.15).move_to([3.0, -1.6, 0])
        tnum.add_updater(lambda m: m.set_color(temp_color(m.get_value() + 1e-9, T0, T1)).next_to(tlab[0], RIGHT, buff=0.15))
        lnum = DecimalNumber(tr[0, 1], num_decimal_places=0, group_with_commas=True, font_size=30, color=FCOL)
        lnum.add_updater(lambda m: m.set_value(tr[int(np.clip(k.get_value(), 0, n_snaps - 1)) * every, 1]))
        llab = VGroup(label(r"length", font_size=24, color=GREY_A), lnum).arrange(RIGHT, buff=0.2).move_to([5.3, -1.6, 0])
        lnum.add_updater(lambda m: m.next_to(llab[0], RIGHT, buff=0.2))
        acc = label(rf"$2$-opt moves: \ reverse a stretch of the tour; \\ ${d['sa_per_temp']:,}$ evaluated moves per temperature"
                    .replace(",", "{,}"), font_size=20, color=GREY_A).move_to([3.9, -2.5, 0])
        acc.set_x(min(acc.get_x(), 6.9 - acc.width / 2))
        tag = note(r"computed: \ berlin52 (TSPLIB), \ $52$ places in Berlin").to_corner(DL, buff=0.2)
        best = int(d["sa_best"])
        hit = best == int(d["opt"])
        a0, a_end = 100 * tr[0, 3], 100 * tr[-1, 3]
        end = (f"It ends at {best:,}: the proven optimum, {int(d['opt']):,}." if hit else
               f"It ends at {best:,}, against the proven optimum of {int(d['opt']):,}.")
        with self.voiceover(
            "Here it is on a travelling-salesman problem: the shortest round trip through fifty-two places in Berlin, a "
            "standard test whose optimum is known. A move reverses a stretch of the tour. <bookmark mark='a'/> Hot, at first, "
            f"{a0:.0f} percent of proposed changes are accepted, and the tour is a tangle. <bookmark mark='b'/> As it cools, "
            "fewer bad moves get through; crossing edges disappear, and the tour pulls into loops around the city's clusters. "
            f"<bookmark mark='c'/> At the end, {a_end:.1f} percent are accepted: annealing has become hill climbing, from a "
            "very good place. " + end
        ) as vo:
            self.add(live)
            self.play(FadeIn(cities), Create(frame), FadeIn(g), Create(opt), FadeIn(ol), FadeIn(tlab), FadeIn(llab),
                      FadeIn(acc), FadeIn(tag))
            self.add(dot)
            vo.wait_until("a")
            self.play(Create(cur), k.animate.set_value(n_snaps * 0.25), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(k.animate.set_value(n_snaps * 0.8), run_time=7.0, rate_func=linear)
            vo.wait_until("c")
            self.play(k.animate.set_value(n_snaps - 1), run_time=3.0, rate_func=linear)
            for m in (live, dot, tnum, lnum):
                m.clear_updaters()
            # the run's last step: its best tour, length and temperature
            fin = tour_mob(ax, xy, d["sa_best_tour"], color=temp_color(T1, T0, T1), width=3)
            self.play(Transform(live, fin), ChangeDecimalToValue(lnum, best), ChangeDecimalToValue(tnum, T1),
                      dot.animate.move_to(g.ax.c2p(len(tr) - 1, tr[-1, 1])), run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def budgets(self):
        d = load("tsp")
        opt = int(d["opt"])
        items = [
            (r"nearest neighbour \ (best start)", [min(d["nn_lengths"])], GREY_B),
            (r"nearest neighbour, \ then $2$-opt", [min(d["nn2opt_lengths"])], GCOST),
            (r"$2$-opt hill climbing, \ restarts", d["eq_restarts"], FCOL),
            (r"simulated annealing", d["eq_anneal"], HOT),
            (r"genetic algorithm", d["eq_ga"], LEARN),
        ]
        lo = opt * 0.95
        hi = max(max(v) for _, v, _ in items) * 1.03
        g = axes([lo, hi], [0, len(items)], x_length=6.0, y_length=4.0, xlabel=r"tour length", xticks=[opt],
                 xfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), center=[1.8, -0.3, 0])
        names = VGroup()
        bars = VGroup()
        for i, (nm, vals, col) in enumerate(items):
            y = len(items) - i - 0.5
            m, a, b = float(np.mean(vals)), float(np.min(vals)), float(np.max(vals))
            bar = Line(g.ax.c2p(lo, y), g.ax.c2p(m, y), color=col, stroke_width=16)
            rng_ = Line(g.ax.c2p(a, y), g.ax.c2p(b, y), color=WHITE, stroke_width=2.5) if b > a else VectorizedPoint()
            val = MathTex(f"{m:,.0f}".replace(",", "{,}"), font_size=24, color=col).next_to(g.ax.c2p(max(m, b), y), RIGHT,
                                                                                          buff=0.15)
            bars.add(VGroup(bar, rng_, val))
            names.add(label(nm, font_size=20, color=col).next_to(g.ax.c2p(lo, y), LEFT, buff=0.2))
        optl = DashedLine(g.ax.c2p(opt, 0), g.ax.c2p(opt, len(items)), color=PATH, dash_length=0.08)
        tag = note(rf"computed: \ the last three on an equal budget of ${d['budget']:,}$ candidate-cost evaluations, \ "
                   rf"${len(d['eq_anneal'])}$ seeds; \ bar = mean, \ line = range".replace(",", "{,}")).to_corner(DR,
                                                                                                                buff=0.2)
        sa, rs, ga = (float(np.mean(d[k])) for k in ("eq_anneal", "eq_restarts", "eq_ga"))
        n_opt = sum(1 for v in d["eq_anneal"] if v == opt)
        order = sorted([("annealing", sa), ("restarted hill climbing", rs), ("the genetic algorithm", ga)],
                       key=lambda t: t[1])
        verdict = (f"On the same budget of {d['budget']:,} candidate-cost evaluations, {order[0][0]} does best, averaging "
                   f"{order[0][1]:,.0f}; {order[1][0]} averages {order[1][1]:,.0f}, and {order[2][0]}, {order[2][1]:,.0f}.")
        hits = (f"Annealing found the optimum itself in {n_opt} of {len(d['eq_anneal'])} runs." if n_opt else
                "Annealing never found the optimum itself.")
        with self.voiceover(
            "Is the cooling worth it? Limit all three methods to the same number of candidate-cost evaluations, including "
            "initialization. A two-opt delta counts once, like scoring one genetic child; this is not equal CPU time. "
            "<bookmark mark='a'/> The "
            "greedy tour, always to the nearest unvisited place, is "
            f"{100 * (min(d['nn_lengths']) / opt - 1):.0f} percent too long even from its best start; 2-opt hill climbing "
            f"polishes it to {min(d['nn2opt_lengths']):,}. <bookmark mark='b'/> " + verdict + " <bookmark mark='c'/> " + hits
        ) as vo:
            self.play(FadeIn(g), Create(optl), FadeIn(tag))
            vo.wait_until("a")
            for i in range(2):
                self.play(FadeIn(names[i]), Create(bars[i][0]), FadeIn(bars[i][2]), run_time=0.8)
            vo.wait_until("b")
            for i in range(2, len(items)):
                self.play(FadeIn(names[i]), Create(bars[i][0]), FadeIn(bars[i][1]), FadeIn(bars[i][2]), run_time=0.8)
            vo.wait_until("c")
            self.play(Indicate(VGroup(names[3], bars[3]), color=HOT, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def genetic(self):
        d = load("tsp")
        p1 = [0, 1, 2, 3, 4, 5, 6, 7]
        p2 = [3, 7, 0, 6, 2, 5, 1, 4]
        i, j = 2, 5
        child = [-1] * 8
        child[i:j] = p1[i:j]
        rest = [c for c in p2[j:] + p2[:j] if c not in child]
        pos = j
        for c in rest:
            child[pos % 8] = c
            pos += 1

        def strip(seq, col, keep=()):
            g = VGroup()
            for k, c in enumerate(seq):
                box = Square(0.5, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.35 if k in keep else 0.08)
                g.add(VGroup(box, Text(chr(65 + c), font_size=24, color=WHITE).move_to(box)))
            return g.arrange(RIGHT, buff=0.06)

        s1 = strip(p1, GCOST, keep=range(i, j))
        s2 = strip(p2, HEUR)
        sc = strip(child, LEARN, keep=range(i, j))
        rows = VGroup(VGroup(label(r"parent 1", font_size=22, color=GCOST), s1).arrange(RIGHT, buff=0.3),
                      VGroup(label(r"parent 2", font_size=22, color=HEUR), s2).arrange(RIGHT, buff=0.3),
                      VGroup(label(r"child", font_size=22, color=LEARN), sc).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, buff=0.3, aligned_edge=RIGHT).move_to([-3.2, 1.2, 0])
        ox = label(r"order crossover: \ keep a stretch of parent 1, \\ fill in the rest in parent 2's order",
                   font_size=20, color=GREY_A).next_to(rows, DOWN, buff=0.25)
        tag = note(r"illustrative").next_to(rows, UP, buff=0.15)
        hc = history_card(1975, r"John Holland, \textit{Adaptation in Natural and Artificial Systems}",
                          r"a population; \ the fitter reproduce; \ children mix their parents and mutate",
                          width=5.6, color=HIST, font_size=20).move_to([3.6, 1.6, 0])
        bp = np.asarray(d["ga_best_per_gen"])
        G = max(1, len(bp) - 1)
        ga_gap = 100 * (bp[-1] / d["opt"] - 1)
        gg = axes([0, G], [6000, bp[0] * 1.05], x_length=5.2, y_length=2.4, xlabel=r"generations",
                  ylabel=r"best tour in the population", xticks=[0, G], yticks=[10000, 20000],
                  yfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), center=[3.6, -1.6, 0])
        gc = curve(gg.ax, np.arange(len(bp)), bp, LEARN, 3)
        optl = DashedLine(gg.ax.c2p(0, d["opt"]), gg.ax.c2p(G, d["opt"]), color=PATH, dash_length=0.08)
        new = VGroup(history_card(2023, r"FunSearch", r"a language model proposes the mutations: \ new results in "
                                  r"combinatorics", width=4.4, color=LEARN, font_size=18),
                     history_card(2025, r"AlphaEvolve", r"evolves code with Gemini: \ $4 \times 4$ complex matrices "
                                  r"multiplied with $48$ multiplications", width=4.4, color=LEARN, font_size=18))
        new.arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.15).set_x(-3.6)
        with self.voiceover(
            "A third idea keeps a whole population. <bookmark mark='a'/> John Holland's genetic algorithms, from 1975, let the "
            "fitter states reproduce: a child takes pieces of two parents, plus a random mutation. <bookmark mark='b'/> On our "
            f"budget, a plain version ends {ga_gap:.0f} percent above the optimum: most children of two good tours are worse "
            "than either. <bookmark mark='c'/> Population search has a second "
            "life. DeepMind's FunSearch, in 2023, let a language model propose the mutations; in 2025 AlphaEvolve evolved "
            "programs that way, and found how to multiply four-by-four complex matrices with forty-eight multiplications, one "
            "fewer than Strassen's 1969 method."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(rows[:2]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]), FadeIn(ox))
            vo.wait_until("b")
            self.play(FadeIn(gg), Create(optl), Create(gc), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeOut(ox), LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in new], lag_ratio=0.5))
        self.wait(0.3)
        self.clear_scene()
