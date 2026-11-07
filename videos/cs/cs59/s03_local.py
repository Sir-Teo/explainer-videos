from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs59.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono

PAL = [YES, DATA, HEAD, NO, LAM, KERN, TEAL_C, PINK]


def colour_of(v):
    return PAL[v] if v < len(PAL) else GREY_C


def cv_step(a, b):
    """One Cole-Vishkin step for a node of colour a whose successor has colour b: (i, bit, new colour)."""
    x = a ^ b
    i = (x & -x).bit_length() - 1
    bit = (a >> i) & 1
    return i, bit, 2 * i + bit


def bits_row(v, width, size=20, color=WHITE):
    """The binary digits of v, most significant first, one mobject per digit (index 0 is the rightmost)."""
    s = format(v, f"0{width}b")
    g = VGroup(*[mono(ch, size=size, color=color) for ch in s]).arrange(RIGHT, buff=0.06)
    for ch in g:
        ch.align_to(g, DOWN)
    return g


def stacked(rows, whys, buff=0.22):
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


class Local(VoiceoverScene):
    def construct(self):
        self.card()
        self.view()
        self.trick()
        self.proper()
        self.shrink()
        self.ring()
        self.scale()

    def card(self):
        card = chapter_card(2, r"Locality: \ colouring a ring", r"How far must a node look to choose its colour?",
                            lit=(1986, 2000), extra=((1986, r"Cole and Vishkin: \ deterministic coin tossing"),
                                                     (2000, r"Peleg: \ a locality-sensitive approach")), part=PART)
        with self.voiceover("Chapter two. Locality: colouring a ring."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def view(self):
        head = label(r"What a node knows after $t$ rounds", font_size=36).to_edge(UP, buff=0.3)
        N, R = 16, 2.35
        c0 = np.array([-3.4, -0.45, 0])
        ang = [PI / 2 - k * TAU / N for k in range(N)]
        P = [c0 + R * np.array([np.cos(a), np.sin(a), 0]) for a in ang]
        ring = Circle(radius=R, color=GREY_D, stroke_width=2).move_to(c0).set_z_index(-1)
        nodes = VGroup(*[Circle(radius=0.2, stroke_color=GREY_B, stroke_width=1.6, fill_color=BG, fill_opacity=1)
                         .move_to(p) for p in P])
        nodes[0].set_stroke(HEAD, width=3)
        vl = label(r"$v$", font_size=22, color=HEAD).next_to(nodes[0], UP, buff=0.1)
        tl = label(r"$t = 0$", font_size=24, color=HEAD).move_to(c0)
        fs = 32
        eqs = [MathTex(r"\mathrm{out}(v)", r"=", r"A\big(", r"B(v, t)", r"\big)", font_size=fs),
               MathTex(r"\mathrm{out}(v)", r"=", r"A\big(", r"x_{-t}, \dots, x_0, \dots, x_t", r"\big)",
                       font_size=fs)]
        eqs[0][3].set_color(HEAD)
        eqs[1][3].set_color(HEAD)
        whys = [label(r"$B(v, t)$: \ everything within $t$ hops", font_size=18, color=GREY_B),
                label(r"on an oriented ring: \ $2t + 1$ ids in a row", font_size=18, color=GREY_B)]
        col = stacked(eqs, whys, buff=0.35).move_to([3.4, 1.5, 0])
        notes = VGroup(
            wrapped_label(r"in LOCAL nothing is lost by forwarding everything you know each round, \ so a $t$-round "
                          r"algorithm \textit{is} a function from radius-$t$ views to outputs", 5.9, font_size=19,
                          color=WHITE),
            wrapped_label(r"without ids, \ identical nodes on a ring see identical views forever: \ no deterministic "
                          r"algorithm can even 2-colour them, \ so ids, \ a proper $n$-colouring, \ are where we "
                          r"start", 5.9, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -1.75, 0])
        with self.voiceover(
            "The LOCAL model turns distance into time. <bookmark mark='a'/> Put sixteen nodes on an oriented ring, "
            "where each knows which neighbour is its successor, and watch one node, v. <bookmark mark='b'/> Each "
            "round, every node tells both neighbours everything it knows. After one round v knows the identifiers "
            "one hop away; after t rounds, its whole neighbourhood of radius t, and nothing beyond. <bookmark "
            "mark='c'/> So a t-round algorithm is just a function from such views to outputs, and on a ring a view "
            "is two t plus one identifiers in a row. <bookmark mark='d'/> Identifiers matter: on an anonymous ring "
            "every node sees the same thing forever, and no deterministic algorithm can colour it. With them we "
            "start from a proper colouring with n colours, and must shrink it to three."
        ) as vo:
            self.play(FadeIn(head), Create(ring), FadeIn(nodes), FadeIn(vl))
            vo.wait_until("a")
            self.play(FadeIn(tl))
            vo.wait_until("b")
            for t in range(1, 4):
                dots = VGroup()
                targets = []
                for k in range(N):
                    for d in (1, -1):
                        dots.add(Dot(P[k], radius=0.07, color=DATA).set_z_index(3))
                        targets.append(P[(k + d) % N])
                self.play(FadeIn(dots, run_time=0.15))
                self.play(*[dd.animate.move_to(tp) for dd, tp in zip(dots, targets)], run_time=0.8)
                lit = [k % N for k in range(-t, t + 1)]
                ntl = label(rf"$t = {t}$", font_size=24, color=HEAD).move_to(c0)
                self.play(FadeOut(dots, run_time=0.15), Transform(tl, ntl),
                          *[nodes[k].animate.set_fill(HEAD, opacity=0.45) for k in lit], run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(col[0]))
            self.play(TransformMatchingTex(eqs[0].copy(), eqs[1]), FadeIn(whys[1]))
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def trick(self):
        c = load("cv")
        tr = c["trace"]
        head = label(r"The bit-position trick", font_size=36).to_edge(UP, buff=0.3)
        a, b = tr[0][0], tr[0][1]
        W = max(tr[0]).bit_length()
        i, bit, new = cv_step(a, b)
        assert new == tr[1][0]
        ra, rb = bits_row(a, W, color=DATA), bits_row(b, W, color=LAM)
        sa, sb = f"{a:,}".replace(",", "{,}"), f"{b:,}".replace(",", "{,}")
        la = label(rf"$c(v) = {sa}$", font_size=21, color=DATA)
        lb = label(rf"$c(\mathrm{{succ}}\,v) = {sb}$", font_size=21, color=LAM)
        la.next_to([-2.1, 2.25, 0], LEFT, buff=0)
        lb.next_to([-2.1, 1.65, 0], LEFT, buff=0)
        ra.next_to([-1.9, 2.25, 0], RIGHT, buff=0)
        rb.next_to([-1.9, 1.65, 0], RIGHT, buff=0)
        k = W - 1 - i
        hl = SurroundingRectangle(VGroup(ra[k], rb[k]), color=HEAD, buff=0.06, stroke_width=2.5)
        il = label(rf"lowest differing bit: \ $i = {i}$", font_size=18, color=HEAD).next_to(hl, DOWN, buff=0.12)
        il.align_to(hl, RIGHT)
        fs = 32
        eqs = [MathTex(r"c'(v)", r"=", r"2i", r"+", r"c_v[i]", font_size=fs),
               MathTex(r"c'(v)", r"=", r"2 \cdot " + str(i), r"+", str(bit), font_size=fs),
               MathTex(r"c'(v)", r"=", str(new), font_size=fs)]
        for e in eqs:
            e[0].set_color(HEAD)
        eqs[2][2].set_color(YES)
        VGroup(*eqs).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.9, 1.65, 0])
        trows = []
        for r in (1, 2):
            x, y = tr[r][0], tr[r][1]
            w = max(x, y).bit_length()
            ii, bb, nn = cv_step(x, y)
            assert nn == tr[r + 1][0]
            trows.append([f"{r + 1}", format(x, f"0{w}b"), format(y, f"0{w}b"), f"{ii}", f"{bb}", f"{nn}"])
        tab = grid_table([r"round", r"$c(v)$", r"$c(\mathrm{succ}\,v)$", r"$i$", r"bit", r"$c'(v)$"], trows,
                         widths=[1.1, 1.3, 1.9, 0.7, 0.8, 1.1], row_h=0.48, font_size=19, mono_cols=(1, 2))
        tab.move_to([-3.2, -0.75, 0])
        src = note(rf"node 0 of the {c['n']:,}-node ring, \ rounds 1 to 3, \ from our run".replace(",", "{,}"),
                   font_size=16).next_to(tab, DOWN, buff=0.15)
        side = VGroup(
            wrapped_label(r"the new colour is a pair: \ \textit{where} $v$ first differs from its successor, \ and "
                          r"\textit{what} $v$ has there", 5.4, font_size=19, color=WHITE),
            wrapped_label(rf"a {W}-bit id has positions 0 to {W - 1}, \ so after one round at most "
                          rf"$2 \times {W} = {2 * W}$ colours remain; \ the run used {c['colours'][1]}", 5.4,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -1.1, 0])
        foot = note(r"Cole and Vishkin \ (1986) \ called it deterministic coin tossing, \ for parallel list ranking",
                    font_size=18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is Richard Cole and Uzi Vishkin's trick of 1986, on numbers from our run. <bookmark mark='a'/> "
            "Node v's identifier is one million, nine hundred and ninety-nine thousand, five hundred and "
            "ninety-one; its successor's is one million, six hundred and sixty-four thousand, two hundred. Write "
            "both in binary. <bookmark mark='b'/> Find the lowest bit where they differ: here, bit zero. <bookmark "
            "mark='c'/> The new colour is twice that position plus v's own bit there: two times zero, plus one, is "
            "one. <bookmark mark='d'/> Every node does this at once, and the next rounds work on the new, shorter "
            "colours; in round three v finds its first difference at position two and becomes four. <bookmark "
            "mark='e'/> A twenty-one-bit identifier has only twenty-one positions, so after one round at most "
            "forty-two colours remain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(la), FadeIn(lb))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in ra], lag_ratio=0.04),
                      LaggedStart(*[FadeIn(d) for d in rb], lag_ratio=0.04), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(hl), FadeIn(il))
            vo.wait_until("c")
            self.play(FadeIn(eqs[0]))
            self.play(TransformMatchingTex(eqs[0].copy(), eqs[1]))
            self.play(TransformMatchingTex(eqs[1].copy(), eqs[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.5), FadeIn(src))
            vo.wait_until("e")
            self.play(FadeIn(side[0]))
            self.play(FadeIn(side[1]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def proper(self):
        head = label(r"Why neighbours still differ", font_size=36).to_edge(UP, buff=0.3)
        names = [r"$v$", r"$w = \mathrm{succ}\,v$", r"$\mathrm{succ}\,w$"]
        circs = VGroup(*[Circle(radius=0.32, stroke_color=c, stroke_width=2.2, fill_color=BG, fill_opacity=1)
                         for c in (DATA, LAM, GREY_B)]).arrange(DOWN, buff=1.05).move_to([-5.3, -0.1, 0])
        nl = VGroup(*[label(n, font_size=20, color=WHITE).next_to(cc, RIGHT, buff=0.15) for n, cc in zip(names, circs)])
        arr = VGroup(*[Arrow(circs[k].get_bottom(), circs[k + 1].get_top(), buff=0.05, stroke_width=2.5,
                             color=GREY_B, max_tip_length_to_length_ratio=0.25) for k in range(2)])
        al = VGroup(label(r"$i_v$: \ $v$ against $w$", font_size=17, color=DATA),
                    label(r"$i_w$: \ $w$ against its successor", font_size=17, color=LAM))
        for a_, t in zip(arr, al):
            t.next_to(a_, RIGHT, buff=0.25).shift(DOWN * 0.05)
        fs = 30
        rows = [
            MathTex(r"c'(v)", r"=", r"2 i_v + c_v[i_v]", r",\quad", r"c'(w)", r"=", r"2 i_w + c_w[i_w]", font_size=fs),
            MathTex(r"c'(v)", r"=", r"c'(w)", r"\;\Longrightarrow\;", r"i_v = i_w = i", r",\;", r"c_v[i] = c_w[i]",
                    font_size=fs),
            MathTex(r"i", r"=", r"i_v", r"\;\Longrightarrow\;", r"c_v[i] \neq c_w[i]", font_size=fs),
            MathTex(r"c'(v)", r"\neq", r"c'(w)", font_size=fs),
        ]
        rows[1][6].set_color(NO)
        rows[2][4].set_color(YES)
        rows[3].set_color(YES)
        whys = [label(r"each new colour is (position, bit), \ written as one number", font_size=18, color=GREY_B),
                label(r"$2i + b$ determines $i$ and $b$, \ since $b \in \{0, 1\}$", font_size=18, color=GREY_B),
                label(r"but $i_v$ was chosen as a bit where $c_v$ and $c_w$ differ: \ contradiction", font_size=18,
                      color=GREY_B),
                label(r"so the new colouring is proper, \ whatever the ids", font_size=18, color=GREY_B)]
        col = stacked(rows, whys, buff=0.3).move_to([2.4, -0.1, 0])
        with self.voiceover(
            "Why can neighbours never collide? <bookmark mark='a'/> Take v, its successor w, and w's successor. "
            "Node v chose its position by comparing itself with w, but w compared itself with its own successor. "
            "<bookmark mark='b'/> Suppose v and w get the same new colour. Two i plus a bit determines both the "
            "position and the bit, so they chose the same position i and have the same bit there. <bookmark "
            "mark='c'/> But v chose i precisely as a position where its colour and w's differ, a contradiction. "
            "<bookmark mark='d'/> The new colouring is proper whatever the identifiers were, so the step can be "
            "repeated, and because each node has a single successor to compare with, all nodes act at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(circs), FadeIn(nl))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a_), FadeIn(t)) for a_, t in zip(arr, al)],
                                  lag_ratio=0.6), FadeIn(col[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
        self.wait(0.4)
        self.clear_scene()

    def shrink(self):
        c = load("cv")
        head = label(r"How fast the colours shrink", font_size=36).to_edge(UP, buff=0.3)
        fs = 30
        rows = [
            MathTex(r"c", r"<", r"2^b", font_size=fs),
            MathTex(r"c'", r"=", r"2i + \text{bit}", r"\le", r"2(b - 1) + 1", r"<", r"2b", font_size=fs),
            MathTex(r"b'", r"=", r"\lceil \log_2 2b \rceil", r"=", r"1 + \lceil \log_2 b \rceil", font_size=fs),
        ]
        rows[2][4].set_color(HEAD)
        whys = [label(r"a colour of $b$ bits", font_size=18, color=GREY_B),
                label(r"positions run from 0 to $b - 1$", font_size=18, color=GREY_B),
                label(r"bits needed for the new colour: \ about $\log b$", font_size=18, color=GREY_B)]
        col = stacked(rows, whys, buff=0.3).move_to([-3.3, 0.9, 0])
        b = [max(c["trace"][0]).bit_length()]
        while True:
            nb = 1 + math.ceil(math.log2(b[-1]))
            if nb >= b[-1]:
                break
            b.append(nb)
        trows = [[r"0", rf"{b[0]}", r"---", rf"{c['colours'][0]:,}".replace(",", "{,}")]]
        for r in range(1, len(b) + 1):
            bound = 2 * b[r - 1]
            trows.append([f"{r}", f"{b[r]}" if r < len(b) else f"{b[-1]}", f"{bound}", f"{c['colours'][r]}"])
        tab = grid_table([r"round", r"bits $b$", r"bound $2b$", r"colours used"], trows, widths=[1.1, 1.3, 1.6, 2.0],
                         row_h=0.45, font_size=19, mono_cols=())
        tab.move_to([3.6, 1.0, 0])
        for row in tab.cells[1:]:
            row[3].set_color(YES)
        chain = MathTex(*[x for k, v in enumerate(b) for x in ((str(v),) if k == 0 else (r"\to", str(v)))],
                        r"\to", str(b[-1]), font_size=36, color=HEAD)
        chain[-1].set_color(NO)
        cl = label(rf"stuck at {b[-1]} bits: \ $2i + \text{{bit}} < {2 * b[-1]}$ again", font_size=19, color=NO)
        VGroup(chain, cl).arrange(DOWN, buff=0.2).move_to([-3.3, -2.2, 0])
        foot = wrapped_label(rf"each round takes a logarithm of the length, \ so about $\log^* n$ rounds reach "
                             rf"{2 * b[-1]} colours; \ three more rounds finish the job", 5.8, font_size=19,
                             color=WHITE).move_to([3.6, -2.2, 0])
        with self.voiceover(
            "How quickly do the colours shrink? <bookmark mark='a'/> If every colour fits in b bits, the position "
            "i is at most b minus one, so the new colour, two i plus a bit, is less than two b. <bookmark "
            "mark='b'/> Writing it takes one plus the logarithm of b bits: a colour's length collapses to roughly "
            "its own logarithm in one round. <bookmark mark='c'/> In our run: twenty-one bits, then six, four, "
            "three. The bound allows forty-two colours after round one and the run used thirty-eight; then twelve, "
            "eight and six, exactly at the bound. <bookmark mark='d'/> At three bits the trick stops helping: two "
            "i plus a bit is again below six. <bookmark mark='e'/> Since each round takes a logarithm, reaching "
            "six colours takes about as many rounds as the logarithms needed to bring n down to a constant."
        ) as vo:
            self.play(FadeIn(head), FadeIn(col[0]))
            vo.wait_until("a")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), FadeIn(VGroup(*tab.cells[1])))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[2:]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("d")
            self.play(Write(chain), FadeIn(cl))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def ring(self):
        c = load("cv")
        tr = c["trace"]
        head = label(r"A million colours collapse", font_size=36).to_edge(UP, buff=0.3)
        n = len(tr[0])
        c0 = np.array([-3.3, -0.45, 0])
        R = 2.75
        span = 300 * DEGREES
        ang = [-PI / 2 + 30 * DEGREES + k * span / (n - 1) for k in range(n)]
        P = [c0 + R * np.array([np.cos(a), np.sin(a), 0]) for a in ang]
        arc = Arc(radius=R, start_angle=ang[0], angle=span, color=GREY_D, stroke_width=2).move_arc_center_to(c0)
        gap = DashedVMobject(Arc(radius=R, start_angle=ang[-1], angle=TAU - span, color=GREY_D, stroke_width=2)
                             .move_arc_center_to(c0), num_dashes=5)
        more = label(rf"{c['n'] - n:,} more nodes".replace(",", "{,}"), font_size=16,
                     color=GREY_B).next_to(c0 + DOWN * R, DOWN, buff=0.1)
        nodes = VGroup(*[Circle(radius=0.25, stroke_color=GREY_B, stroke_width=1.5, fill_color=BG, fill_opacity=1)
                         .move_to(p) for p in P])
        orient = Arc(radius=R + 0.5, start_angle=ang[3], angle=ang[5] - ang[3], color=GREY_B,
                     stroke_width=2).move_arc_center_to(c0).add_tip(tip_length=0.12)
        um = np.array([np.cos(ang[4]), np.sin(ang[4]), 0])
        ol = label(r"successor", font_size=16, color=GREY_B).next_to(c0 + (R + 0.65) * um, RIGHT, buff=0.05)

        def nums(vals):
            return VGroup(*[label(str(v), font_size=18, color=BLACK if v < len(PAL) else WHITE).move_to(p)
                            for v, p in zip(vals, P)])

        def counter(r):
            return VGroup(label(rf"round {r}", font_size=24, color=HEAD),
                          label(rf"{c['colours'][r]:,} colours".replace(",", "{,}"), font_size=22, color=WHITE)
                          ).arrange(DOWN, buff=0.12).move_to(c0)
        cnt = counter(0)
        steps = [r"ids"] + [r"bit trick"] * (len(c["colours"]) - 4) + [rf"remove {k}" for k in (5, 4, 3)]
        trows = [[f"{r}", rf"{v:,}".replace(",", "{,}"), s] for r, (v, s) in enumerate(zip(c["colours"], steps))]
        tab = grid_table([r"round", r"colours", r"step"], trows, widths=[1.1, 1.7, 2.0], row_h=0.4, font_size=19,
                         mono_cols=())
        tab.move_to([3.9, 1.0, 0])
        k4 = len(c["colours"]) - 4
        for r in range(1, len(trows) + 1):
            tab.cells[r][2].set_color(DATA if 1 <= r - 1 <= k4 else (KERN if r > 1 else GREY_A))
        note_ = wrapped_label(r"to remove colour 5: \ its nodes are never neighbours, \ so all of them at once take "
                              r"the smallest of 0, 1, 2 that their two neighbours do not use; \ then 4, \ then 3",
                              5.6, font_size=19, color=KERN).next_to(tab, DOWN, buff=0.35)
        done = label(rf"{c['rounds']} rounds, \ proper: \ {'yes' if c['proper'] else 'no'}", font_size=21,
                     color=YES).next_to(note_, DOWN, buff=0.3)
        with self.voiceover(
            "Now watch it run. <bookmark mark='a'/> Twenty-four consecutive nodes of our million-node ring, each "
            "starting with its twenty-one-bit identifier: a million colours. <bookmark mark='b'/> One round of the "
            "bit trick, and the ring is down to thirty-eight colours; then twelve, eight, six. <bookmark "
            "mark='c'/> Then a different step takes over. Nodes of colour five are never neighbours, so all of "
            "them recolour at once, each taking the smallest of zero, one and two that neither neighbour uses. "
            "Then colour four goes, then three. <bookmark mark='d'/> Seven rounds, and our instrument checked "
            "every edge of the million: no two neighbours share a colour."
        ) as vo:
            self.play(FadeIn(head), Create(arc), Create(gap), FadeIn(more), FadeIn(nodes), FadeIn(orient),
                      FadeIn(ol))
            vo.wait_until("a")
            self.play(FadeIn(cnt), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), FadeIn(VGroup(*tab.cells[1])))
            cur = None
            for r in range(1, len(tr)):
                if r == k4 + 1:
                    vo.wait_until("c")
                    self.play(FadeIn(note_))
                elif r == 1:
                    vo.wait_until("b")
                vals = tr[r]
                new = nums(vals)
                anims = [nd.animate.set_fill(colour_of(v), opacity=1 if v < len(PAL) else 0.3)
                         for nd, v in zip(nodes, vals)]
                anims.append(Transform(cnt, counter(r)))
                anims.append(FadeIn(VGroup(*tab.cells[r + 1])))
                if cur is None:
                    cur = new
                    anims.append(FadeIn(cur))
                else:
                    anims.append(Transform(cur, new))
                changed = [k for k in range(n) if tr[r - 1][k] != vals[k]] if r > k4 else []
                self.play(*anims, run_time=1.0)
                if changed:
                    self.play(*[Indicate(nodes[k], color=WHITE, scale_factor=1.3) for k in changed], run_time=0.6)
                else:
                    self.wait(0.6)
            vo.wait_until("d")
            self.play(FadeIn(done))
        self.wait(0.4)
        self.clear_scene()

    def scale(self):
        ls = load("logstar")["rows"]
        sc = load("cvscale")["rows"]
        head = label(r"$\log^* n$: \ the number of logarithms to reach 1", font_size=36).to_edge(UP, buff=0.3)
        fs = 32
        eqs = [MathTex(r"\log^* n", r"=", r"\min\{\, k : \log_2^{(k)} n \le 1 \,\}", font_size=fs),
               MathTex(r"65536", r"\to", r"16", r"\to", r"4", r"\to", r"2", r"\to", r"1", font_size=fs),
               MathTex(r"\log^* 65536", r"=", r"4", font_size=fs)]
        eqs[2][2].set_color(HEAD)
        col = VGroup(*eqs).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.6, 1.7, 0])
        nl = [rf"${r['n'].replace(',', '{,}').replace('^65536', '^{65536}')}$" for r in ls]
        lt = grid_table([r"$n$", r"$\log^* n$"], [[x, f"{r['log_star']}"] for x, r in zip(nl, ls)], widths=[2.2, 1.4],
                        row_h=0.42, font_size=19, mono_cols=())
        lt.next_to(col, DOWN, buff=0.45).align_to(col, LEFT)
        st = grid_table([r"ring size $n$", r"rounds", r"$\log^* n$"],
                        [[rf"{r['n']:,}".replace(",", "{,}"), f"{r['rounds']}", f"{r['log_star']}"] for r in sc],
                        widths=[2.2, 1.3, 1.3], row_h=0.42, font_size=19, mono_cols=())
        st.move_to([3.7, 1.35, 0])
        for row in st.cells[1:]:
            row[1].set_color(YES)
        sl = note(r"Cole--Vishkin, \ run by our instrument", font_size=16).next_to(st, DOWN, buff=0.12)
        side = wrapped_label(r"rounds $= \log^* n + O(1)$: \ the difference stays at two or three; \ $2^{65536}$, "
                             r"\ far more than the atoms in the universe, \ has $\log^* = 5$", 5.4, font_size=19,
                             color=WHITE).next_to(sl, DOWN, buff=0.35)
        q = wrapped_label(r"is $\log^* n$ necessary, \ or could a cleverer rule do it in a constant number of rounds?",
                          5.4, font_size=19, color=HEAD).next_to(side, DOWN, buff=0.3)
        with self.voiceover(
            "The count of rounds has a name. <bookmark mark='a'/> Log star of n is the number of times you take "
            "the base-two logarithm before reaching one: sixty-five thousand five hundred and thirty-six becomes "
            "sixteen, four, two, one; four logarithms. <bookmark mark='b'/> It grows absurdly slowly: two to the "
            "power sixty-five thousand five hundred and thirty-six, vastly more than the atoms in the universe, "
            "has log star five. <bookmark mark='c'/> Cole and Vishkin's rounds track it: from ten nodes to a "
            "million, our instrument needs log star of n plus two or three. <bookmark mark='d'/> So "
            "three-colouring a ring takes almost constant time. Could a cleverer rule do it in constant time? The "
            "next chapter's answer is no."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]))
            self.play(FadeIn(eqs[1], lag_ratio=0.2), run_time=1.5)
            self.play(TransformMatchingTex(eqs[1].copy(), eqs[2]))
            vo.wait_until("b")
            self.play(FadeIn(lt))
            vo.wait_until("c")
            self.play(FadeIn(st), FadeIn(sl))
            self.play(FadeIn(side))
            vo.wait_until("d")
            self.play(FadeIn(q))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM, NO, YES)
