from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def open_bin(w, h, color=GREY_B, width=2):
    """A machine drawn as an open-topped bin of capacity 1 (height h)."""
    return VGroup(Line([-w / 2, h, 0], [-w / 2, 0, 0], color=color, stroke_width=width),
                  Line([-w / 2, 0, 0], [w / 2, 0, 0], color=color, stroke_width=width),
                  Line([w / 2, 0, 0], [w / 2, h, 0], color=color, stroke_width=width))


def item(size, h, w, color=DATA, text=None, font=16, min_h=0.0):
    r = Rectangle(width=w, height=max(size * h, min_h), stroke_color=BG, stroke_width=1.5, fill_color=color,
                  fill_opacity=0.85)
    if text and size * h > 0.28:
        return VGroup(r, label(text, font_size=font, color=BLACK).move_to(r))
    return VGroup(r)


def stack(bin_, sizes, h, w, color=DATA, texts=None, min_h=0.0):
    """Items stacked from the bottom of a bin."""
    g, y = VGroup(), bin_.get_bottom()[1]
    for k, s in enumerate(sizes):
        it = item(s, h, w, color, texts[k] if texts else None, min_h=min_h)
        it.move_to([bin_.get_x(), y + it.height / 2, 0])
        y += it.height
        g.add(it)
    return g


def pct(r):
    return rf"+{100 * (r - 1):.0f}\%"


class Packing(VoiceoverScene):
    def construct(self):
        self.card()
        self.puzzle()
        self.hard()
        self.heuristics()
        self.bounds()
        self.vector()
        self.preempt()

    def card(self):
        card = chapter_card(5, r"Scheduling as bin packing", r"How few machines can hold this work?",
                            lit=(1973, 2007), extra=((1973, r"Johnson: \ first fit decreasing analysed"),
                                                     (2007, r"D\'osa: \ the tight bound")), part=PART)
        with self.voiceover("Chapter five. Scheduling as bin packing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def puzzle(self):
        head = label(r"Containers into machines", font_size=36).to_edge(UP, buff=0.3)
        sizes = [0.5, 0.3, 0.6, 0.2, 0.4, 0.3, 0.5, 0.2]
        H, W = 2.6, 0.75
        queue = VGroup(*[item(s, H, W, DATA, f"{s:.1f}") for s in sizes]).arrange(RIGHT, buff=0.12,
                                                                                 aligned_edge=DOWN)
        queue.move_to([-2.95, 0, 0]).align_to([0, 1.0, 0], DOWN)
        ql = label(r"CPU each container requests \ (a machine holds 1)", font_size=18, color=GREY_A).next_to(
            queue, UP, buff=0.12).align_to(queue, LEFT)
        bins = VGroup(*[open_bin(0.9, H) for _ in range(4)]).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        bins.move_to([-3.95, 0, 0]).align_to([0, -3.3, 0], DOWN)
        names = VGroup(*[label(rf"m{i + 1}", font_size=16, color=GREY_A).next_to(b, DOWN, buff=0.06)
                         for i, b in enumerate(bins)])
        bins.shift(UP * 0.25)
        names.shift(UP * 0.25)
        ill = note(r"illustrative", font_size=16).next_to(bins, RIGHT, buff=0.3).align_to(bins, DOWN)
        loads, moves = [0.0] * 4, []
        for it, s in zip(queue, sizes):                 # first fit: the first machine with room
            k = next(i for i in range(4) if loads[i] + s <= 1 + 1e-9)
            y = bins[k].get_bottom()[1] + (loads[k] + s / 2) * H
            moves.append(it.animate.move_to([bins[k].get_x(), y, 0]))
            loads[k] += s
        used = sum(1 for x in loads if x > 0)
        notes = VGroup(
            wrapped_label(r"\textbf{bin packing}: \ items of sizes between 0 and 1, \ bins of size 1; \ use as few "
                          r"bins as possible", 5.4, font_size=20, color=WHITE),
            wrapped_label(r"\textbf{first fit}: \ put each item in the first machine where it fits; \ open a new "
                          r"one only when none has room", 5.4, font_size=20, color=YES),
            wrapped_label(rf"here {used} machines, \ every one full; \ the fourth can be switched off or rented "
                          r"to someone else", 5.4, font_size=20, color=HEAD),
            wrapped_label(r"a real scheduler first \textbf{filters} the machines a container fits on, \ then "
                          r"\textbf{scores} them: \ one rule spreads work out, \ another packs machines full", 5.4,
                          font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.75, -0.3, 0])
        with self.voiceover(
            "Once a pod has no machine, the scheduler must choose one. <bookmark mark='a'/> This is bin "
            "packing: items of sizes between zero and one, bins of size one, and as few bins as possible. "
            "<bookmark mark='b'/> The simplest sensible rule is first fit: each item goes into the first "
            "machine with room. <bookmark mark='c'/> Here it fills three machines exactly, and the fourth can "
            "be switched off. <bookmark mark='d'/> A real scheduler filters out the machines that cannot take "
            "the container, then scores the rest: one rule spreads work out, another packs machines full."
        ) as vo:
            self.play(FadeIn(head), FadeIn(queue), FadeIn(ql), FadeIn(bins), FadeIn(names), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            for m in moves:
                self.play(m, run_time=0.55)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), bins[3].animate.set_color(GREY_D), names[3].animate.set_color(GREY_D))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def hard(self):
        p = load("partition")
        head = label(r"NP-hard, \ by way of partition", font_size=36).to_edge(UP, buff=0.3)
        H, W = 2.3, 0.8

        def side(case, color, title, cx):
            ic = DATA
            nums = case["numbers"]
            tags = VGroup(*[label(f"{x}", font_size=24, color=color) for x in nums]).arrange(RIGHT, buff=0.35)
            t = label(title, font_size=20, color=color)
            half = label(rf"total {sum(nums)}, \ half {case['half']:g}: \ item sizes $x / {case['half']:g}$",
                         font_size=18, color=GREY_A)
            top = VGroup(t, tags, half).arrange(DOWN, buff=0.18)
            nb = case["bins_needed"]
            bins = VGroup(*[open_bin(1.0, H, color=NO if k >= 2 else GREY_B) for k in range(nb)]).arrange(
                RIGHT, buff=0.35, aligned_edge=DOWN)
            # place the items: the two-bin split when it exists, otherwise first fit decreasing
            xs = case["items"]
            order = sorted(range(len(xs)), key=lambda i: -xs[i])
            groups = [[] for _ in range(nb)]
            loads = [0.0] * nb
            if case["partition_exists"]:
                n = len(xs)
                pick = next(m for m in range(1, 2 ** n) if abs(sum(xs[i] for i in range(n) if m >> i & 1) - 1) < 1e-9)
                groups = [[i for i in range(n) if pick >> i & 1], [i for i in range(n) if not pick >> i & 1]]
            else:
                for i in order:
                    k = next(b for b in range(nb) if loads[b] + xs[i] <= 1 + 1e-9)
                    groups[k].append(i)
                    loads[k] += xs[i]
            VGroup(top, bins).arrange(DOWN, buff=0.4).move_to([cx, 0.15, 0])
            fill = VGroup(*[stack(bins[k], [xs[i] for i in g], H, W - 0.1, ic,
                                  [f"{nums[i]}" for i in g]) for k, g in enumerate(groups)])
            return top, bins, fill
        yes = side(p["yes"], YES, r"splits into two halves", -3.4)
        no = side(p["no"], NO, r"cannot be split evenly", 3.4)
        res = VGroup(
            label(rf"{p['yes']['bins_needed']} bins", font_size=20, color=YES).next_to(yes[1], DOWN, buff=0.15),
            label(rf"{p['no']['bins_needed']} bins", font_size=20, color=NO).next_to(no[1], DOWN, buff=0.15))
        line = wrapped_label(r"two bins suffice exactly when the numbers can be split into equal halves: \ "
                             r"partition is NP-complete \ (Part 26), \ so bin packing is NP-hard, \ and no fast "
                             r"algorithm can promise fewer than $\tfrac{3}{2}$ times the optimum unless P = NP",
                             12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Recall partition, from Part 26: can some numbers be split into two halves with equal sums? "
            "<bookmark mark='a'/> Divide each by half the total, and ask whether the items fit in two bins. "
            "Three, one, one, two, two and one total ten; three, one and one make five, and so do two, two and one. "
            "<bookmark mark='b'/> Three, three, three and one also total ten, but nothing makes five: a third "
            "bin is needed. <bookmark mark='c'/> So a fast packer would solve partition, and bin packing is NP-"
            "hard. Telling two bins from three is already hard, so no fast algorithm can promise better than "
            "one and a half times the optimum, unless P equals NP."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(yes[0]), FadeIn(yes[1]))
            self.play(LaggedStart(*[FadeIn(i, shift=DOWN * 0.3) for g in yes[2] for i in g], lag_ratio=0.15),
                      FadeIn(res[0]))
            vo.wait_until("b")
            self.play(FadeIn(no[0]), FadeIn(no[1]))
            self.play(LaggedStart(*[FadeIn(i, shift=DOWN * 0.3) for g in no[2] for i in g], lag_ratio=0.2),
                      FadeIn(res[1]))
            vo.wait_until("c")
            self.play(FadeIn(line))
        self.wait(0.4)
        self.clear_scene()

    def heuristics(self):
        p = load("packing")
        u, s = p["uniform"], p["structured"]
        head = label(r"Four heuristics against the optimum", font_size=36).to_edge(UP, buff=0.3)
        rules = {"next fit": r"only the newest machine",
                 "first fit": r"the first machine with room",
                 "best fit": r"the fullest machine it fits in",
                 "first fit decreasing": r"sort largest first, \ then first fit"}
        names = list(rules)
        rows = [[k, rules[k], rf"{pct(u['mean_ratio'][k])} \ / \ {pct(u['worst_ratio'][k])}",
                 rf"{pct(s['mean_ratio'][k])} \ / \ {pct(s['worst_ratio'][k])}"] for k in names]
        tab = grid_table([r"heuristic", r"where each item goes", r"random sizes", r"clustered sizes"], rows,
                         widths=[3.0, 4.9, 2.3, 2.3], row_h=0.62, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6).set_x(0)
        for i, c in enumerate((NO, HEAD, LAM, YES), 1):
            tab.cells[i][0].set_color(c)
            tab.cells[i][1].set_color(GREY_A)
        sub = label(r"bins used above the exact optimum: \ mean \ / \ worst", font_size=17, color=GREY_B).next_to(
            tab, UP, buff=0.1).align_to(tab, RIGHT)
        cap = wrapped_label(rf"{u['n']} items per instance; \ {u['trials']} instances with sizes drawn uniformly at "
                            rf"random, \ {s['trials']} with sizes clustered near values that almost pair "
                            r"up; \ the optimum by branch and bound", 12.4, font_size=18,
                            color=GREY_A).next_to(tab, DOWN, buff=0.4)
        line = wrapped_label(r"sorting first is worth most: \ big items placed early leave gaps that small ones "
                             r"fill, \ instead of small items scattered everywhere leaving no room for a big one",
                             12.4, font_size=20, color=YES).next_to(cap, DOWN, buff=0.3)
        with self.voiceover(
            "We packed random instances with four classic rules, and compared each with the exact optimum, "
            "found by branch and bound. <bookmark mark='a'/> Next fit, which keeps only one machine open, used "
            "about a quarter more machines than needed on average, and half as many again at worst. <bookmark "
            "mark='b'/> First fit and best fit, which look back at every machine, came within about eight "
            "percent. <bookmark mark='c'/> First fit decreasing, which sorts the work largest first, came "
            "within one percent. <bookmark mark='d'/> Sorting wins, because large items placed early leave gaps"
            " that small ones can fill."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(sub), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[2])), FadeIn(VGroup(*tab.cells[3])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[4])))
            vo.wait_until("d")
            self.play(FadeIn(line), Indicate(VGroup(*tab.cells[4]), color=YES, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    def bounds(self):
        nf = load("nextfit")["rows"]
        ex = next(r for r in nf if r["items"] == 16)
        head = label(r"What can be guaranteed", font_size=36).to_edge(UP, buff=0.3)
        H, W = 1.45, 0.52
        k = ex["next_fit"]
        nbins = VGroup(*[open_bin(0.6, H) for _ in range(k)]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        nfill = VGroup(*[stack(b, [0.5, 0.01], H, W, DATA, ["0.5", None], min_h=0.045) for b in nbins])
        for g in nfill:
            g[1][0].set_fill(HEAD)
        obins = VGroup(*[open_bin(0.6, H) for _ in range(ex["optimum"])]).arrange(RIGHT, buff=0.12,
                                                                                   aligned_edge=DOWN)
        pairs = ex["optimum"] - 1
        ofill = VGroup(*[stack(b, [0.5, 0.5], H, W, DATA) for b in obins[:pairs]],
                       stack(obins[pairs], [0.01] * k, H, W, HEAD, min_h=0.045))
        nl = label(rf"next fit: \ {ex['next_fit']} machines", font_size=19, color=NO)
        ol = label(rf"optimum: \ {ex['optimum']}", font_size=19, color=YES)
        top = VGroup(nl, VGroup(nbins, nfill)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        bot = VGroup(ol, VGroup(obins, ofill)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        VGroup(top, bot).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.6, 0.6, 0])
        fam = label(r"halves alternating with tiny items", font_size=17, color=GREY_A).next_to(top, UP, buff=0.12)
        fam.align_to(top, LEFT)
        rows = [[f"{r['items']}", f"{r['next_fit']}", f"{r['optimum']}", f"{r['ratio']:.2f}"] for r in nf]
        tab = grid_table([r"items", r"next fit", r"optimum", r"ratio"], rows, widths=[1.3, 1.4, 1.5, 1.3],
                         row_h=0.42, font_size=19, mono_cols=())
        tab.move_to([3.6, 1.0, 0])
        for i in range(1, len(rows) + 1):
            tab.cells[i][3].set_color(NO)
        proof = VGroup(
            wrapped_label(r"any two neighbouring bins of next fit hold more than 1 \ (else the second's first item "
                          r"would have fitted), \ so $\mathrm{NF} \le 2\,\mathrm{OPT} - 1$: \ the factor 2 is "
                          r"proved, \ and the family above shows it cannot be improved", 12.4, font_size=19,
                          color=WHITE),
            MathTex(r"\mathrm{FFD} \le \tfrac{11}{9}\,\mathrm{OPT} + \tfrac{6}{9}", font_size=34, color=YES),
            wrapped_label(r"Johnson \ (1973) \ proved $\tfrac{11}{9}\,\mathrm{OPT} + 4$; \ D\'osa \ (2007) \ found "
                          r"the tight constant", 6.0, font_size=19, color=GREY_A),
        )
        proof[0].to_edge(DOWN, buff=1.05)
        VGroup(proof[1], proof[2]).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A proof says how badly a rule can do. <bookmark mark='a'/> Give next fit halves alternating with "
            "tiny items. Each half closes the machine before it, so sixteen items take eight machines; the "
            "optimum pairs the halves and gathers the tiny items, in five. <bookmark mark='b'/> As the family "
            "grows, the ratio climbs towards two. <bookmark mark='c'/> It can never pass two: any two "
            "neighbouring machines hold more than one machine's worth, or the second's first item would have "
            "fitted. <bookmark mark='d'/> For first fit decreasing, David Johnson proved in 1973 a bound of "
            "eleven ninths of the optimum plus four; in 2007 György Dósa found the tight constant, six ninths."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fam))
            vo.wait_until("a")
            self.play(FadeIn(nl), FadeIn(nbins), LaggedStart(*[FadeIn(g) for g in nfill], lag_ratio=0.1))
            self.play(FadeIn(ol), FadeIn(obins), LaggedStart(*[FadeIn(g) for g in ofill], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(proof[0]))
            vo.wait_until("d")
            self.play(FadeIn(proof[1]), FadeIn(proof[2]))
        self.wait(0.4)
        self.clear_scene()

    def vector(self):
        v = load("vector")
        head = label(r"Two resources at once", font_size=36).to_edge(UP, buff=0.3)
        vals = [(r"lower bound: \ total demand", v["lower_bound"], GREY_B, f"{v['lower_bound']:.1f}"),
                (r"first fit, \ sorted by each job's larger demand", v["ffd_max_dim"], YES, f"{v['ffd_max_dim']}"),
                (r"first fit, \ sorted by CPU alone", v["ffd_cpu_only"], NO, f"{v['ffd_cpu_only']}")]
        bars = VGroup()
        for k, (t, x, col, txt) in enumerate(vals):
            w = x / 70 * 6.0
            b = Rectangle(width=w, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-6.2 + w / 2, 1.75 - 1.05 * k, 0])
            bars.add(VGroup(b, label(rf"{txt} machines", font_size=19, color=col).next_to(b, RIGHT, buff=0.15),
                            label(t, font_size=18, color=GREY_A).next_to(b, UP, buff=0.07).align_to(b, LEFT)))

        def gauges(util, col, title):
            g = VGroup()
            for name, x in zip((r"CPU", r"memory"), util):
                frame = Rectangle(width=0.6, height=2.0, stroke_color=GREY_B, stroke_width=1.5)
                fill = Rectangle(width=0.6, height=2.0 * x, stroke_width=0, fill_color=col, fill_opacity=0.8)
                fill.align_to(frame, DOWN)
                g.add(VGroup(frame, fill, label(name, font_size=16, color=GREY_A).next_to(frame, DOWN, buff=0.08),
                             label(rf"{100 * x:.0f}\%", font_size=17, color=col).next_to(frame, UP, buff=0.06)))
            g.arrange(RIGHT, buff=0.35)
            return VGroup(label(title, font_size=17, color=col), g).arrange(DOWN, buff=0.15)
        ga = gauges(v["util_max_dim"], YES, r"larger demand")
        gb = gauges(v["util_cpu_only"], NO, r"CPU alone")
        gg = VGroup(ga, gb).arrange(RIGHT, buff=0.7, aligned_edge=DOWN).move_to([4.3, 0.85, 0])
        gt = label(r"average machine, \ share used", font_size=17, color=GREY_B).next_to(gg, UP, buff=0.15)
        lines = VGroup(
            wrapped_label(rf"{v['jobs']} containers, \ some CPU-heavy, \ some memory-heavy, \ some balanced; \ a "
                          r"machine is full when \textit{either} resource is: \ \textbf{vector bin packing}", 12.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"sorted by CPU alone, \ the memory-hungry jobs come last, \ when early machines have "
                          r"memory but no CPU to spare; \ mixing the two kinds on one machine is where the saving "
                          r"is", 12.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Real containers ask for more than one thing. <bookmark mark='a'/> Our two hundred containers each "
            "need some processor and some memory, and a machine is full when either runs out: this is vector "
            "bin packing. The total demand says at least thirty-nine machines. <bookmark mark='b'/> First fit, "
            "sorting by each job's larger demand, used forty-three, about nine-tenths busy in both resources. "
            "<bookmark mark='c'/> Sorted by processor alone, it used sixty-three, about sixty percent busy: the"
            " memory-hungry jobs came last, when machines had memory but no processor to spare. Packing well "
            "means mixing the two kinds."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), GrowFromEdge(bars[0][0], LEFT), FadeIn(bars[0][1:]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], LEFT), FadeIn(bars[1][1:]), FadeIn(gt), FadeIn(ga))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[2][0], LEFT), FadeIn(bars[2][1:]), FadeIn(gb))
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def preempt(self):
        head = label(r"Priorities and preemption", font_size=36).to_edge(UP, buff=0.3)
        H, W = 3.0, 1.1
        b = open_bin(1.3, H).move_to([-4.6, -0.2, 0])
        batch = stack(b, [0.3, 0.25, 0.3], H, W, LAM, [r"batch", r"batch", r"batch"])
        prod = item(0.4, H, W, HEAD, r"prod").move_to([-2.2, 2.05, 0])
        pl = label(r"a production task arrives", font_size=18, color=HEAD).next_to(prod, RIGHT, buff=0.2)
        free = label(r"room left: \ too little", font_size=17, color=GREY_A).next_to(b, RIGHT, buff=0.15)
        free.set_y(b.get_top()[1] - 0.2)
        queue = label(r"evicted: \ waits to be placed elsewhere", font_size=17, color=NO).move_to([-1.4, -2.3, 0])
        ill = note(r"illustrative", font_size=16).next_to(b, DOWN, buff=0.15)
        notes = VGroup(
            wrapped_label(r"Borg gives every job a priority: \ \textbf{production} \ (serving users) \ and "
                          r"\textbf{batch} \ (everything that can wait)", 5.2, font_size=19, color=WHITE),
            wrapped_label(r"a higher-priority task may \textbf{preempt} lower ones: \ they are killed and "
                          r"rescheduled; \ Kubernetes has priority classes that do the same", 5.2, font_size=19,
                          color=HEAD),
            wrapped_label(r"batch work also runs in capacity that production reserved but is not using, \ and is "
                          r"the first to go when it is wanted back", 5.2, font_size=19, color=LAM),
            wrapped_label(r"Verma et al. \ (2015): \ running the two kinds on separate machines would need "
                          r"20--30\% more machines in the median cell", 5.2, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -0.2, 0])
        with self.voiceover(
            "The other half of scheduling is deciding who gives way. <bookmark mark='a'/> Borg gives every job "
            "a priority: production work that serves users, and batch work that can wait. <bookmark mark='b'/> "
            "Here a full machine of batch tasks meets a production task. <bookmark mark='c'/> The scheduler "
            "preempts the lowest-priority task, which goes back into the queue to be placed elsewhere; "
            "Kubernetes' priority classes do the same. <bookmark mark='d'/> Batch work also fills capacity that"
            " production reserved but is not using. <bookmark mark='e'/> The payoff: in the Borg paper, keeping"
            " the two kinds on separate machines would have needed twenty to thirty percent more of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(b), FadeIn(batch), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(prod), FadeIn(pl), FadeIn(free))
            vo.wait_until("c")
            self.play(batch[2].animate.move_to(queue.get_top() + UP * (batch[2].height / 2 + 0.1)).set_fill(
                NO, 0.6), FadeIn(queue), FadeOut(free))
            target = [b.get_x(), b.get_bottom()[1] + (0.55 + 0.2) * H, 0]
            self.play(prod.animate.move_to(target), FadeOut(pl), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, PART)
