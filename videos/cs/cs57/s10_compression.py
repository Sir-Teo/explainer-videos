from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs57.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load

M_PERCEPTRON = 2000          # the perceptron instrument's sample size (its default; chapter 3 quotes it)
DELTA = 0.05                 # the confidence used throughout the part (load("finite")["delta"])


def stacked(rows, whys, buff=0.2):
    """Derivation rows, each with its reason underneath in grey, as one left-aligned column."""
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


def fit_x(g, lo=-6.85, hi=6.85):
    if g.get_right()[0] > hi:
        g.shift(LEFT * (g.get_right()[0] - hi))
    if g.get_left()[0] < lo:
        g.shift(RIGHT * (lo - g.get_left()[0]))
    return g


def comp_bound(k, m, delta):
    """Littlestone and Warmuth: error at most (k ln m + ln 1/delta) / (m - k) for a size-k scheme."""
    return (k * math.log(m) + math.log(1 / delta)) / (m - k)


class Compression(VoiceoverScene):
    def construct(self):
        self.card()
        self.occam()
        self.scheme()
        self.perceptron()
        self.mdl()
        self.summary()

    def card(self):
        card = chapter_card(9, r"Learning is compression", r"Does a short description generalize?",
                            lit=(1978, 1986), extra=((1978, r"Rissanen: \ minimum description length"),
                                                     (1986, r"Littlestone and Warmuth: \ sample compression")),
                            part=PART)
        with self.voiceover("Chapter nine. Learning is compression."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ Occam's razor, as a theorem
    def occam(self):
        delta = load("finite")["delta"]
        head = label(r"Occam's razor, \ as a theorem", font_size=36).to_edge(UP, buff=0.3)
        codes = ["0", "10", "110", "1110", "1111"]
        # a prefix-free code drawn as a binary tree
        pos = {"": (0, 0), "0": (-1.0, -0.65), "1": (1.0, -0.65), "10": (0.35, -1.3), "11": (1.65, -1.3),
               "110": (1.0, -1.95), "111": (2.3, -1.95), "1110": (1.65, -2.6), "1111": (2.95, -2.6)}
        nodes = {k_: np.array([x, y, 0.0]) for k_, (x, y) in pos.items()}
        edges, leaves = VGroup(), VGroup()
        for c in pos:
            if c:
                edges.add(Line(nodes[c[:-1]], nodes[c], color=GREY_C, stroke_width=2))
        dots = VGroup(*[Dot(p, radius=0.06, color=GREY_B) for k, p in nodes.items() if k not in codes])
        for i, c in enumerate(codes):
            leaves.add(VGroup(Dot(nodes[c], radius=0.09, color=DATA),
                              label(rf"$h_{i + 1}$: \ \texttt{{{c}}}", font_size=17, color=DATA).next_to(
                                  nodes[c], DOWN, buff=0.1)))
        tree = VGroup(edges, dots, leaves)
        tree.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        W = 5.6
        segs = VGroup()
        for i, c in enumerate(codes):
            w = W * 2 ** -len(c)
            r = Rectangle(width=w, height=0.45, stroke_color=BG, stroke_width=2, fill_color=interpolate_color(
                ManimColor(HEAD), ManimColor(KERN), i / 4), fill_opacity=0.85)
            segs.add(r)
        segs.arrange(RIGHT, buff=0).next_to(tree, DOWN, buff=0.55).align_to(tree, LEFT)
        seg_l = VGroup(*[label(rf"$\delta/{2 ** len(c)}$", font_size=16, color=GREY_A).next_to(s, DOWN, buff=0.08)
                         for s, c in zip(segs[:3], codes[:3])])
        bar_t = label(rf"the failure budget $\delta = {delta:g}$, \ shared out by code length", font_size=17,
                      color=HEAD).next_to(segs, UP, buff=0.1).align_to(segs, LEFT)
        ill = note(r"illustrative code", font_size=16).next_to(seg_l, DOWN, buff=0.12).align_to(segs, LEFT)
        fs = 25
        rows = [
            MathTex(r"\sum_h 2^{-|h|}", r"\le", r"1", font_size=fs),
            MathTex(r"\delta_h", r"=", r"\delta\, 2^{-|h|}", font_size=fs),
            MathTex(r"\Pr\big[h \text{ fits all } m,\ \mathrm{err}(h) > \epsilon_h\big]", r"\le",
                    r"e^{-\epsilon_h m}", r"=", r"\delta_h", font_size=fs),
            MathTex(r"\epsilon_h", r"=", r"\frac{|h| \ln 2 + \ln(1/\delta)}{m}", font_size=fs + 3),
        ]
        rows[3][2].set_color(YES)
        whys = [
            label(r"Kraft's inequality: \ the codewords of a prefix-free code are leaves of a tree", font_size=17,
                  color=GREY_B),
            label(r"give each hypothesis a share of $\delta$: \ the shorter, \ the larger", font_size=17,
                  color=GREY_B),
            label(r"chapter 1, \ one hypothesis at a time; \ solve for $\epsilon_h$", font_size=17, color=GREY_B),
            label(r"the union bound spends at most $\sum_h \delta_h \le \delta$ \ (Blumer et al. \ 1987)",
                  font_size=17, color=YES),
        ]
        col = stacked(rows, whys, buff=0.3).next_to(head, DOWN, buff=0.45).to_edge(RIGHT, buff=0.4)
        foot = wrapped_label(r"a consistent hypothesis described in $b$ bits has error at most about $b/m$: \ "
                             r"chapter 1's bound is the case where every description has $\log_2|\mathcal H|$ bits",
                             col.width, font_size=18, color=WHITE).next_to(col, DOWN, buff=0.35).align_to(col, LEFT)
        with self.voiceover(
            "William of Ockham said not to multiply entities beyond necessity. Learning theory makes it a "
            "theorem. <bookmark mark='a'/> Describe each hypothesis in a prefix-free code, like the leaves of "
            "this tree. Kraft's inequality says two to the minus the lengths add up to at most one. "
            "<bookmark mark='b'/> So share out the failure probability delta in those proportions: a short "
            "hypothesis gets a large share. <bookmark mark='c'/> By chapter one's argument, a hypothesis with "
            "error above epsilon survives m examples with probability e to the minus epsilon m; set that equal "
            "to its share. <bookmark mark='d'/> Solve: its error is at most its length in bits, times log two, "
            "plus log of one over delta, all over m. The union bound spends at most delta. Anselm Blumer, "
            "Andrzej Ehrenfeucht, David Haussler and Manfred Warmuth called this Occam's razor, in 1987. Short descriptions generalize, not "
            "because nature is simple, but because there are few of them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(edges), FadeIn(dots), LaggedStart(*[FadeIn(lf) for lf in leaves], lag_ratio=0.2),
                      run_time=2)
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("b")
            self.play(FadeIn(bar_t), LaggedStart(*[GrowFromEdge(s, LEFT) for s in segs], lag_ratio=0.25),
                      FadeIn(seg_l), FadeIn(ill), Write(col[1][0]), FadeIn(col[1][1]))
            vo.wait_until("c")
            self.play(Write(col[2][0]), FadeIn(col[2][1]))
            vo.wait_until("d")
            self.play(Write(col[3][0]), FadeIn(col[3][1]))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ a compression scheme, and its bound
    def scheme(self):
        c = load("compress")
        r = {row["m"]: row for row in load("rect")["rows"]}
        m, kept = c["m"], c["kept"]
        k = len(kept)
        x0, x1, y0, y1 = c["box"]
        t0, t1, s0, s1 = c["target"]
        true_err = (t1 - t0) * (s1 - s0) - (x1 - x0) * (y1 - y0)
        eps = comp_bound(k, m, DELTA)
        head = label(r"Keep four, \ forget the rest", font_size=36).to_edge(UP, buff=0.3)
        side = 4.2
        frame = Square(side_length=side, stroke_color=GREY_C, stroke_width=1.5).next_to(head, DOWN, buff=0.45)
        frame.to_edge(LEFT, buff=0.7)
        o = frame.get_corner(DL)

        def at(x, y):
            return o + np.array([x * side, y * side, 0])
        dots = VGroup(*[Dot(at(*p), radius=0.035, color=YES if lab else GREY_B)
                        for p, lab in zip(c["points"], c["labels"])])
        kept_c = VGroup(*[Circle(radius=0.12, color=HEAD, stroke_width=3).move_to(at(*c["points"][i])) for i in kept])
        others = VGroup(*[d for i, d in enumerate(dots) if i not in kept])
        box = Polygon(at(x0, y0), at(x1, y0), at(x1, y1), at(x0, y1), color=HEAD, stroke_width=2.5)
        tgt = DashedVMobject(Polygon(at(t0, s0), at(t1, s0), at(t1, s1), at(t0, s1), color=GREY_A, stroke_width=1.5),
                             num_dashes=40)
        cap = label(rf"{m} points; \ dashed: \ the hidden target", font_size=17, color=GREY_A).next_to(
            frame, DOWN, buff=0.12).align_to(frame, LEFT)
        fs = 25
        rows = [
            MathTex(r"\kappa(S) \subseteq S,\ \ |\kappa(S)| = k", r",\qquad", r"\rho(\kappa(S)) \text{ fits all of } S",
                    font_size=fs),
            MathTex(r"\Pr\big[\mathrm{err}(h) > \epsilon,\ h \text{ fits the other } m - k\big]", r"\le",
                    r"(1 - \epsilon)^{m - k}", font_size=fs),
            MathTex(r"m^k\, e^{-\epsilon (m - k)}", r"\le", r"\delta", font_size=fs),
            MathTex(r"\epsilon", r"=", r"\frac{k \ln m + \ln(1/\delta)}{m - k}", font_size=fs + 2),
            MathTex(r"\epsilon", r"=", rf"\frac{{{k} \ln {m} + \ln {round(1 / DELTA)}}}{{{m - k}}}", r"=",
                    rf"{eps:.3f}", font_size=fs + 2),
        ]
        rows[3][2].set_color(YES)
        rows[4][4].set_color(YES)
        whys = [
            label(r"a scheme of size $k$: \ compress to $k$ examples, \ rebuild a consistent hypothesis",
                  font_size=17, color=GREY_B),
            label(r"for fixed indices, \ $h$ depends only on the kept points: \ the rest are fresh examples",
                  font_size=17, color=GREY_B),
            label(r"the union bound over at most $m^k$ choices of indices", font_size=17, color=GREY_B),
            label(r"solve for $\epsilon$ \ (Littlestone and Warmuth 1986)", font_size=17, color=YES),
            label(rf"$k = {k}$, \ $m = {m}$, \ $\delta = {DELTA:g}$", font_size=17, color=YES),
        ]
        col = stacked(rows[:4], whys[:4], buff=0.25).next_to(frame, RIGHT, buff=0.45).align_to(frame, UP)
        fit_x(col)
        rows[4].move_to(rows[3], aligned_edge=LEFT)
        whys[4].move_to(whys[3], aligned_edge=LEFT)
        cmp = wrapped_label(rf"this box's true error, \ exactly: \ target area minus box area $= {true_err:.4f}$; \ "
                            rf"chapter 1's rectangle bound at $m = {m}$: \ {r[m]['rect_bound']:.3f}; \ the VC bound: "
                            rf"{r[m]['vc_bound']:.3f}", col.width, font_size=18, color=GREY_A).next_to(
            col, DOWN, buff=0.3).align_to(col, LEFT)
        with self.voiceover(
            "Nick Littlestone and Manfred Warmuth turned this around in 1986. <bookmark mark='a'/> Two hundred "
            "points, labelled by a hidden rectangle. <bookmark mark='b'/> Keep only four: the extreme positive "
            "points. From them alone, rebuild the tightest box, and it labels all two hundred correctly. That is"
            " a compression scheme of size four. <bookmark mark='c'/> Why does it generalize? Fix which four "
            "positions are kept. The box depends only on those, so the other hundred and ninety-six are fresh "
            "examples it happened to fit. <bookmark mark='d'/> Take the union bound over at most m to the k "
            "choices, <bookmark mark='e'/> and solve: k log m plus log one over delta, over m minus k. "
            "<bookmark mark='f'/> Here that is point one two three. The box's true error is point zero one seven; "
            "the bound is safe, and of the same order as chapter one's."
        ) as vo:
            self.play(FadeIn(head), Create(frame))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.004), Create(tgt), FadeIn(cap),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(kc) for kc in kept_c], lag_ratio=0.2))
            self.play(others.animate.set_opacity(0.15), run_time=0.8)
            self.play(Create(box), Write(col[0][0]), FadeIn(col[0][1]))
            self.play(others.animate.set_opacity(1), run_time=0.8)
            vo.wait_until("c")
            self.play(Write(col[1][0]), FadeIn(col[1][1]), Indicate(others, color=WHITE, scale_factor=1.0))
            vo.wait_until("d")
            self.play(Write(col[2][0]), FadeIn(col[2][1]))
            vo.wait_until("e")
            self.play(Write(col[3][0]), FadeIn(col[3][1]))
            vo.wait_until("f")
            self.play(TransformMatchingTex(rows[3], rows[4]), FadeOut(whys[3]), FadeIn(whys[4]))
            self.play(FadeIn(cmp))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the perceptron compresses
    def perceptron(self):
        prs = load("perceptron")["rows"]
        m = M_PERCEPTRON
        gam = prs[0]["gamma"]
        nov = prs[0]["bound"]
        head = label(r"The perceptron is a compression scheme", font_size=36).to_edge(UP, buff=0.3)
        unit = 1.1
        base_y = -2.0
        groups = VGroup()
        for row in prs:
            vc = Rectangle(width=0.42, height=unit * math.log10(row["d"]), stroke_width=0, fill_color=NO,
                           fill_opacity=0.7)
            ks = Rectangle(width=0.42, height=unit * math.log10(row["mistakes"]), stroke_width=0, fill_color=YES,
                           fill_opacity=0.8)
            pair = VGroup(vc, ks).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
            vl = label(rf"{row['d']:,}".replace(",", "{,}"), font_size=16, color=NO).next_to(vc, UP, buff=0.05)
            kl = label(rf"{row['mistakes']}", font_size=16, color=YES).next_to(ks, UP, buff=0.05)
            dl = label(rf"$d = {row['d']:,}$".replace(",", "{,}"), font_size=17, color=GREY_A).next_to(pair, DOWN,
                                                                                                      buff=0.1)
            groups.add(VGroup(pair, vl, kl, dl))
        groups.arrange(RIGHT, buff=0.55, aligned_edge=DOWN)
        groups.move_to([-3.6, 0, 0]).align_to([0, base_y, 0], DOWN)
        for g_ in groups:
            g_[0].align_to([0, base_y + 0.45, 0], DOWN)
            g_[1].next_to(g_[0][0], UP, buff=0.05)
            g_[2].next_to(g_[0][1], UP, buff=0.05)
            g_[3].next_to(g_[0], DOWN, buff=0.1)
        y0 = base_y + 0.45
        axis = Line([groups.get_left()[0] - 0.2, y0, 0], [groups.get_right()[0] + 0.2, y0, 0], color=GREY_D)
        nl = DashedLine([groups.get_left()[0] - 0.2, y0 + unit * math.log10(nov), 0],
                        [groups.get_right()[0] + 0.2, y0 + unit * math.log10(nov), 0], color=HEAD, stroke_width=1.5)
        nll = label(rf"Novikoff: \ $(R/\gamma)^2 = {nov:.0f}$", font_size=17, color=HEAD).next_to(nl, UP, buff=0.06)
        nll.align_to(nl, LEFT)
        leg = VGroup(label(r"red: \ the VC dimension $d$", font_size=17, color=NO),
                     label(r"green: \ the scheme's size $k$, \ the mistakes", font_size=17, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).next_to(head, DOWN, buff=0.45).align_to(groups, LEFT)
        lg = note(r"log scale", font_size=16).next_to(leg, RIGHT, buff=0.4).align_to(leg, UP)
        hdr = [r"$d$", r"$k$", r"$\epsilon$ bound"]
        trs = [[rf"{row['d']:,}".replace(",", "{,}"), f"{row['mistakes']}",
                f"{comp_bound(row['mistakes'], m, DELTA):.3f}"] for row in prs]
        tab = grid_table(hdr, trs, widths=[1.0, 0.8, 1.4], row_h=0.4, font_size=19, mono_cols=())
        W = 5.8
        side = VGroup(
            wrapped_label(r"keep the examples it erred on, \ in order: \ run it on those alone and it makes the same "
                          r"mistakes, \ in the same order, \ and ends with the same weights", W, font_size=19,
                          color=WHITE),
            wrapped_label(rf"so $k$ = its mistakes $\le (R/\gamma)^2$: \ chapter 3's margin $\gamma = {gam:g}$, \ "
                          r"whatever the dimension", W, font_size=19, color=YES),
            tab,
            wrapped_label(rf"$m = {m:,}$".replace(",", "{,}") + rf" points on the sphere, \ $\delta = {DELTA:g}$; \ at "
                          r"$d = 1{,}000$ the VC dimension is half the sample and no VC bound says anything", W,
                          font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Compression explains chapter three's puzzle too. <bookmark mark='a'/> Keep only the examples the "
            "perceptron got wrong, in the order it met them. Run it on those alone: it makes the same mistakes "
            "in the same order and finishes with the same weights, which fit everything. "
            "<bookmark mark='b'/> So the perceptron is a compression scheme whose size is its number of "
            "mistakes, at most one over the margin squared, a hundred here, whatever the dimension. "
            "<bookmark mark='c'/> On two thousand points the VC dimension climbs to a thousand, <bookmark mark='d'/> "
            "while the scheme never needs more than thirty-eight. <bookmark mark='e'/> The compression bound stays"
            " under about a seventh, even in a thousand dimensions, where no VC bound says anything. "
            "Margins, not dimensions, decide, because a large margin means a short description."
        ) as vo:
            self.play(FadeIn(head), FadeIn(leg), FadeIn(lg), Create(axis))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Create(nl), FadeIn(nll))
            vo.wait_until("c")
            self.play(*[GrowFromEdge(g_[0][0], DOWN) for g_ in groups], *[FadeIn(g_[1]) for g_ in groups],
                      *[FadeIn(g_[3]) for g_ in groups])
            vo.wait_until("d")
            self.play(*[GrowFromEdge(g_[0][1], DOWN) for g_ in groups], *[FadeIn(g_[2]) for g_ in groups])
            vo.wait_until("e")
            self.play(FadeIn(tab), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ minimum description length
    def mdl(self):
        c = load("compress")
        m = c["m"]
        pos = sum(c["labels"])
        q = pos / m
        H = -(q * math.log2(q) + (1 - q) * math.log2(1 - q))
        k = len(c["kept"])
        bits = [(rf"send every label: \ 1 bit each", m, GREY_B),
                (rf"entropy-code them \ ({pos} of {m} positive): \ about $m\,H$", m * H, KERN),
                (rf"send the box: \ {k} indices of $\log_2 {m}$ bits, \ then nothing", k * math.log2(m), YES)]
        head = label(r"Minimum description length", font_size=36).to_edge(UP, buff=0.3)
        scale = 9.0 / m
        bars = VGroup()
        for t, v, col in bits:
            r = Rectangle(width=max(0.05, v * scale), height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.8)
            vl = label(rf"{v:.1f} bits" if v % 1 else rf"{v:.0f} bits", font_size=18, color=col).next_to(
                r, RIGHT, buff=0.15)
            tl = label(t, font_size=18, color=GREY_A).next_to(r, UP, buff=0.08).align_to(r, LEFT)
            bars.add(VGroup(r, vl, tl))
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        task = label(r"the receiver has the 200 points; \ we must tell it the labels", font_size=19,
                     color=WHITE).next_to(bars, UP, buff=0.25).align_to(bars, LEFT)
        bars.shift(DOWN * 0.3)
        task.shift(DOWN * 0.3)
        fs = 30
        rule = MathTex(r"\hat h", r"=", r"\arg\min_h", r"\Big[\, L(h)", r"+", r"L(\text{data} \mid h) \,\Big]",
                       font_size=fs)
        rule[3].set_color(YES)
        rule[5].set_color(KERN)
        rw = label(r"the model's bits, \ plus the bits of what it gets wrong \ (Rissanen 1978)", font_size=18,
                   color=GREY_B)
        VGroup(rule, rw).arrange(DOWN, buff=0.12).next_to(bars, DOWN, buff=0.55).to_edge(LEFT, buff=0.8)
        b = k * math.log2(m)
        occ = (b * math.log(2) + math.log(1 / DELTA)) / m
        cb = comp_bound(k, m, DELTA)
        oc = VGroup(
            MathTex(r"\frac{" + f"{b:.1f}" + r"\,\ln 2 + \ln " + f"{round(1 / DELTA)}" + r"}{" + f"{m}" + r"}", r"=",
                    f"{occ:.3f}", font_size=28),
            wrapped_label(rf"Occam's bound for these {b:.1f} bits; \ the compression bound gave {cb:.3f}", 4.0,
                          font_size=18, color=GREY_B),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        oc[0][2].set_color(YES)
        oc.next_to(rule, RIGHT, buff=0.9).align_to(rule, UP)
        fit_x(oc)
        p21 = wrapped_label(r"Part 21's bzip2 finds the structure in a text; \ a learner finds it in labels: \ both "
                            r"pay in bits for every regularity they claim", 12.2, font_size=19,
                            color=LAM).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "There is a third way to say the same thing, as a message. <bookmark mark='a'/> The receiver has "
            "the two hundred points and needs their labels. <bookmark mark='b'/> Sent one by one, that is two "
            "hundred bits. <bookmark mark='c'/> Coded by their frequency, forty-one positives in two hundred, "
            "about a hundred and forty-six. <bookmark mark='d'/> But send the four indices of the box's points, "
            "about thirty-one bits, and the receiver rebuilds the box and every label follows. Feed those "
            "thirty-one bits to Occam's bound and it says point one two one: the compression bound's answer, "
            "seen as a message. "
            "<bookmark mark='e'/> Jorma Rissanen's minimum description length principle, from 1978, chooses the"
            " hypothesis that minimizes the bits to describe it plus the bits to describe its exceptions. "
            "<bookmark mark='f'/> It is the bargain of Part 21's compressors: every regularity claimed must pay "
            "for itself in bits."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(task))
            for mk, b in zip("bcd", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[0], LEFT), FadeIn(b[2]), run_time=0.9)
                self.play(FadeIn(b[1]), run_time=0.4)
            vo.wait_until("e")
            self.play(Write(oc[0]), FadeIn(oc[1]))
            self.play(Write(rule), FadeIn(rw))
            vo.wait_until("f")
            self.play(FadeIn(p21))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ one idea, four measures
    def summary(self):
        head = label(r"One shape, \ four measures of complexity", font_size=36).to_edge(UP, buff=0.3)
        hdr = [r"measure", r"complexity", r"error after $m$ examples, \ consistent learner"]
        trs = [
            [r"finite class \ (chapter 1)", r"$\ln|\mathcal H|$", r"$\big(\ln|\mathcal H| + \ln\frac1\delta\big)/m$"],
            [r"Occam \ (this chapter)", r"$|h|$ bits", r"$\big(|h|\ln 2 + \ln\frac1\delta\big)/m$"],
            [r"compression \ (this chapter)", r"$k$ points", r"$\big(k\ln m + \ln\frac1\delta\big)/(m - k)$"],
            [r"VC dimension \ (chapter 2)", r"$d$", r"$O\big((d\ln m + \ln\frac1\delta)/m\big)$"],
        ]
        cols = [[GREY_A, WHITE, WHITE], [GREY_A, YES, YES], [GREY_A, HEAD, HEAD], [GREY_A, DATA, DATA]]
        tab = grid_table(hdr, trs, widths=[3.2, 1.8, 5.0], row_h=0.72, font_size=22, colors=cols, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6).set_x(0)
        brace = Brace(VGroup(*[tab.cells[r][2] for r in range(1, 5)]), RIGHT, color=GREY_B)
        bl = label(r"$\approx$ complexity $\times \log m \,/\, m$", font_size=22, color=GREY_A).next_to(
            brace, RIGHT, buff=0.1)
        fit_x(VGroup(tab, brace, bl))
        foot = wrapped_label(r"a scheme of size $k$ implies learnability; \ does learnability imply a scheme of size "
                             r"$O(d)$? \ That is the frontier, \ next", 12.0, font_size=21, color=LAM).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "Put the bounds side by side. <bookmark mark='a'/> The finite class of chapter one, the bits of "
            "Occam's razor, the kept points of a compression scheme, and the VC dimension of chapter two. "
            "<bookmark mark='b'/> Each says the same thing: error falls like the complexity, times a "
            "logarithm, over the number of examples. <bookmark mark='c'/> Compression implies learning. Does "
            "learning imply compression, with a scheme as small as the VC dimension? Littlestone and Warmuth "
            "asked in 1986, and it is still open. That is the frontier. Each measure, in the end, counts what "
            "the learner must remember."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(c_) for c_ in tab.cells[0]], FadeIn(tab.rule))
            vo.wait_until("a")
            for r in range(1, 5):
                self.play(*[FadeIn(c_) for c_ in tab.cells[r]], run_time=0.6)
            vo.wait_until("b")
            self.play(GrowFromCenter(brace), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, LAM)
