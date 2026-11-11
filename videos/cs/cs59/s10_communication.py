from __future__ import annotations

import math
import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs59.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, tag_box


def proc(name=None, color=GREY_B, r=0.27, size=20, fill=0.0):
    c = Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color if fill else BG,
               fill_opacity=fill if fill else 1)
    if name is None:
        return VGroup(c)
    return VGroup(c, MathTex(name, font_size=size, color=WHITE).move_to(c))


def polygon_pos(n, center, radius, start=90):
    return [np.array(center) + radius * np.array([math.cos(math.radians(start + 360 * k / n)),
                                                  math.sin(math.radians(start + 360 * k / n)), 0])
            for k in range(n)]


def pulses(pairs, color=DATA, r=0.05):
    """Messages as dots: returns the dots (placed at their sources) and the animations moving them to targets."""
    dots = VGroup(*[Dot(a, radius=r, color=color) for a, _ in pairs])
    return dots, [d.animate.move_to(b) for d, (_, b) in zip(dots, pairs)]


def toward(a, b, d):
    """The point at distance d from a towards b (so a message stops at a node's rim)."""
    v = np.array(b) - np.array(a)
    return np.array(a) + v / np.linalg.norm(v) * d


def cross(at, color=NO, s=0.15):
    return VGroup(Line(at + np.array([-s, -s, 0]), at + np.array([s, s, 0]), color=color, stroke_width=4),
                  Line(at + np.array([-s, s, 0]), at + np.array([s, -s, 0]), color=color, stroke_width=4))


def ladder(rows, whys, x_row, x_why, y_top, dy):
    for k, (r, w) in enumerate(zip(rows, whys)):
        y = y_top - k * dy
        r.move_to([0, y, 0]).align_to([x_row, 0, 0], LEFT)
        w.move_to([0, y, 0]).align_to([x_why, 0, 0], LEFT)
    return VGroup(*rows), VGroup(*whys)


def stacked(rows, whys, buff=0.22):
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


class Communication(VoiceoverScene):
    def construct(self):
        self.card()
        self.count()
        self.bound()
        self.proof()
        self.linear()
        self.worst()
        self.randomness()

    def card(self):
        card = chapter_card(9, r"The cost of agreement", r"How many messages must agreement cost?",
                            lit=(1985, 1999, 2019),
                            extra=((1985, r"Dolev and Reischuk: \ $\Omega(n^2)$"), (1999, r"PBFT"),
                                   (2019, r"HotStuff")), part=PART)
        with self.voiceover("Chapter nine. The cost of agreement."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ counting
    def count(self):
        head = label(r"Counting messages", font_size=36).to_edge(UP, buff=0.3)
        n = 7
        C = np.array([-3.9, -0.45, 0])
        P = polygon_pos(n, C, 1.8)
        ps = VGroup(*[proc(rf"p_{k + 1}").move_to(P[k]) for k in range(n)])
        links = VGroup(*[Line(P[i], P[j], color=GREY_D, stroke_width=1, buff=0.28)
                         for i in range(n) for j in range(i + 1, n)])
        pairs = [(P[i], toward(P[j], P[i], 0.3)) for i in range(n) for j in range(n) if i != j]
        cnt = label(rf"one round: \ {len(pairs)} messages", font_size=22, color=HEAD).move_to([-3.9, -2.85, 0])
        ill = note(r"illustrative: \ $n = 7$", font_size=16).next_to(cnt, DOWN, buff=0.1)
        fs = 30
        rows = [MathTex(r"M_1", r"=", r"n(n-1)", font_size=fs),
                MathTex(r"M", r"=", r"(f+1)", r"n(n-1)", font_size=fs),
                MathTex(r"M", r"\approx", r"\tfrac{1}{3}n^{3}", font_size=fs),
                MathTex(r"M_{\mathrm{OM}}", r"\sim", r"n^{f+1}", font_size=fs)]
        rows[3][2].set_color(NO)
        whys = [label(r"one round, \ everyone to everyone", font_size=18, color=GREY_B),
                label(r"FloodSet's $f + 1$ rounds \ (Chapter 4)", font_size=18, color=GREY_B),
                label(r"with $f$ close to $n/3$", font_size=18, color=GREY_B),
                label(r"Lamport, \ Shostak and Pease: \ relay every chain of names", font_size=18, color=NO)]
        col = stacked(rows, whys, buff=0.3).move_to([3.4, 0.55, 0]).align_to([0.9, 0, 0], LEFT)
        q = wrapped_label(r"count messages sent by correct processes, \ or the \textbf{words} they carry \ (a value "
                          r"or a signature): \ which of this is necessary?", 5.8, font_size=19,
                          color=HEAD).next_to(col, DOWN, buff=0.4).align_to(col, LEFT)
        with self.voiceover(
            "How expensive is agreement? Count the messages. <bookmark mark='a'/> In one all-to-all round, each "
            "of n processes sends to the n minus one others: forty-two messages for seven processes. "
            "<bookmark mark='b'/> The flooding protocol of chapter four repeats that for f plus one rounds. "
            "<bookmark mark='c'/> Against a third of the processes failing, that is about a third of n cubed. "
            "<bookmark mark='d'/> The original Byzantine protocol of Lamport, Shostak and Pease is far worse: "
            "processes relay every chain of names, and the count grows like n to the power f plus one. "
            "<bookmark mark='e'/> We count the messages correct processes send, or the words they carry, a value "
            "or a signature each. Which of this cost is necessary?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(links), FadeIn(ps))
            vo.wait_until("a")
            dots, anims = pulses(pairs)
            self.add(dots)
            self.play(*anims, run_time=1.6)
            self.play(FadeOut(dots), FadeIn(cnt), FadeIn(ill), FadeIn(col[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            for _ in range(2):
                dots, anims = pulses(pairs)
                self.add(dots)
                self.play(*anims, run_time=0.9)
                self.remove(dots)
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(col[3]))
            vo.wait_until("e")
            self.play(FadeIn(q))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the bound
    def bound(self):
        head = label(r"Dolev and Reischuk's lower bound", font_size=36).to_edge(UP, buff=0.3)
        n, s = 25, 0.15
        cells = VGroup()
        for r in range(n):
            for c in range(n):
                sq = Square(side_length=s * 0.86, stroke_width=0, fill_color=GREY_D if r != c else BG,
                            fill_opacity=0.35)
                sq.move_to([c * s, -r * s, 0])
                cells.add(sq)
        cells.move_to([-3.7, -0.55, 0])
        frame = SurroundingRectangle(cells, buff=0.05, color=GREY_C, stroke_width=1.4)
        to = label(r"to", font_size=18, color=GREY_B).next_to(frame, UP, buff=0.12)
        fr = label(r"from", font_size=18, color=GREY_B).rotate(PI / 2).next_to(frame, LEFT, buff=0.12)
        vcols = list(range(n - 4, n))
        rng = random.Random(3)
        block = VGroup()
        for c in vcols:
            for r in sorted(rng.sample(range(n - 4), 4)):
                block.add(cells[r * n + c])
        vcells = VGroup(*[cells[r * n + c] for r in range(n) for c in vcols])
        br = Brace(VGroup(*[cells[c] for c in vcols]), UP, buff=0.08, color=HEAD)
        bl = MathTex(r"V", font_size=26, color=HEAD).next_to(br, UP, buff=0.06)
        ill = note(r"illustrative: \ $n = 25$, \ $f = 8$", font_size=16).next_to(frame, DOWN, buff=0.15)
        thm = wrapped_label(r"\textbf{Dolev and Reischuk \ (1985)}: \ every deterministic Byzantine agreement "
                            r"protocol has runs in which correct processes send $\Omega(n + f^2)$ messages, \ "
                            r"\textit{even with signatures}", 6.2, font_size=20, color=WHITE)
        tb = VGroup(SurroundingRectangle(thm, buff=0.2, color=HEAD, corner_radius=0.1, stroke_width=2), thm)
        tb.move_to([3.35, 1.75, 0])
        fs = 34
        d = [MathTex(r"M", r"\ge", r"\left(\tfrac{f}{2}\right)^{2}", font_size=fs),
             MathTex(r"M", r"\ge", r"\tfrac{f^{2}}{4}", font_size=fs),
             MathTex(r"M", r"\ge", r"\tfrac{1}{4}\left(\tfrac{n-1}{3}\right)^{2}", font_size=fs),
             MathTex(r"M", r"\approx", r"\tfrac{n^{2}}{36}", font_size=fs),
             MathTex(r"M", r"=", r"\Omega(n^{2})", font_size=fs)]
        d[4][2].set_color(YES)
        for m in d:
            m.move_to([3.35, -0.25, 0])
        w = [label(r"each of $f/2$ processes in $V$ must hear $f/2$ messages", font_size=19, color=GREY_B),
             label(r"allow the most faults: \ $f = (n-1)/3$", font_size=19, color=GREY_B),
             label(r"quadratic, \ whatever the protocol", font_size=19, color=YES)]
        for m in w:
            m.move_to([3.35, -1.05, 0])
        sig = wrapped_label(r"they also proved that authenticated protocols need $\Omega(nf)$ signatures", 6.2,
                            font_size=19, color=GREY_A).move_to([3.35, -2.2, 0])
        with self.voiceover(
            "In 1985 Danny Dolev and Rüdiger Reischuk showed that much of it is. <bookmark mark='a'/> Every "
            "deterministic Byzantine agreement protocol has runs in which the correct processes send on the order "
            "of n plus f squared messages, and signatures do not help. <bookmark mark='b'/> Draw who sends to "
            "whom as a matrix; all-to-all fills it. <bookmark mark='c'/> The proof finds a set V of f over two "
            "processes, each of which must hear about f over two messages: <bookmark mark='d'/> at least f "
            "squared over four. <bookmark mark='e'/> Allow the most faults, a third of n, and that is about n "
            "squared over thirty-six: quadratic, whatever the protocol. <bookmark mark='f'/> They also showed "
            "that authenticated protocols need on the order of n times f signatures."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tb))
            vo.wait_until("b")
            self.play(FadeIn(frame), FadeIn(to), FadeIn(fr), FadeIn(ill))
            self.play(LaggedStart(*[cells[r * n:(r + 1) * n].animate.set_fill(DATA, opacity=0.55)
                                    for r in range(n)], lag_ratio=0.08), run_time=2.0)
            self.play(cells[0::n + 1].animate.set_fill(BG, opacity=1), run_time=0.3)
            vo.wait_until("c")
            self.play(vcells.animate.set_fill(GREY_D, opacity=0.35), FadeIn(br), FadeIn(bl))
            self.play(block.animate.set_fill(HEAD, opacity=1), FadeIn(d[0]), FadeIn(w[0]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(d[0], d[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(d[1], d[2]), ReplacementTransform(w[0], w[1]))
            self.play(TransformMatchingTex(d[2], d[3]))
            self.play(TransformMatchingTex(d[3], d[4]), ReplacementTransform(w[1], w[2]))
            vo.wait_until("f")
            self.play(FadeIn(sig))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the proof
    def proof(self):
        head = label(r"Why: \ starve one process", font_size=36).to_edge(UP, buff=0.3)
        others = [np.array([-5.9 + 0.9 * k, 2.3, 0]) for k in range(6)]
        ops = VGroup(*[proc(r"s" if k == 0 else None, color=HEAD if k == 0 else GREY_B).move_to(p)
                       for k, p in enumerate(others)])
        vx = [0.6, 1.8, 3.0, 4.2]
        vy = 1.0
        V = [np.array([x, vy, 0]) for x in vx]
        vps = VGroup(*[proc(rf"q_{k + 1}", color=NO).move_to(p) for k, p in enumerate(V)])
        vbox = SurroundingRectangle(vps, buff=0.22, color=NO, corner_radius=0.12, stroke_width=1.8)
        vl = label(r"$V$: \ $f/2$ faulty, \ each ignores the first $f/2$ messages it receives", font_size=18,
                   color=NO)
        ins = [5, 3, 2, 4]
        rng = random.Random(1)
        senders = [sorted(rng.sample(range(6), k)) for k in ins]
        arrows = VGroup()
        per = []
        for j, ss in enumerate(senders):
            g = VGroup(*[Line(others[i], V[j], buff=0.3, color=DATA, stroke_width=1.3, stroke_opacity=0.7)
                         for i in ss])
            per.append(g)
            arrows.add(g)
        inl = VGroup(*[MathTex(rf"\mathrm{{in}} = {k}", font_size=22, color=GREY_A).next_to(vps[j], DOWN,
                                                                                            buff=0.34)
                       for j, k in enumerate(ins)])
        vl.next_to(inl, DOWN, buff=0.15).set_x(vbox.get_x())
        thr = label(r"$f/2 = 4$", font_size=18, color=HEAD).next_to(vbox, RIGHT, buff=0.15)
        ill = note(r"illustrative: \ $f = 8$", font_size=16).next_to(thr, DOWN, buff=0.1).align_to(thr, LEFT)
        p_ = 2
        ring = Circle(radius=0.36, color=HEAD, stroke_width=3).move_to(V[p_])
        bad = VGroup(*[ops[i][0].copy().set_stroke(NO, width=3) for i in senders[p_]])
        fs = 28
        rows = [MathTex(r"\textstyle\sum_{q \in V} \mathrm{in}(q)", r"<", r"\left(\tfrac{f}{2}\right)^{2}",
                        font_size=fs),
                MathTex(r"\mathrm{in}(p)", r"<", r"\tfrac{f}{2}", r"\text{ for some } p \in V", font_size=fs),
                MathTex(r"|V \setminus \{p\}|", r"+", r"\mathrm{in}(p)", r"<", r"f", font_size=fs),
                MathTex(r"p\text{ decides } b", r"\ne", r"1 - b", font_size=fs)]
        rows[3][1].set_color(NO)
        whys = [label(r"suppose fewer messages than the bound", font_size=19, color=GREY_B),
                label(r"pigeonhole: \ $p$ ignores everything it is sent", font_size=19, color=GREY_B),
                label(r"world 2: \ $p$ honest, \ its senders corrupt and silent to it", font_size=19, color=GREY_B),
                label(r"the others see world 1 and decide the sender's $1 - b$", font_size=19, color=NO)]
        rg, wg = ladder(rows, whys, -6.3, -1.1, -0.95, 0.7)
        src = note(r"the argument as retold by Abraham et al. \ (2019)", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Here is the heart of it, as Ittai Abraham and colleagues retold it in 2019. <bookmark mark='a'/> "
            "Suppose a protocol always sends fewer than f over two, squared, messages. Corrupt a set V of f over "
            "two processes, which behave honestly but ignore the first f over two messages each receives. "
            "<bookmark mark='b'/> With so few messages, some member p of V receives fewer than f over two: it "
            "ignores everything. <bookmark mark='c'/> Now a second world: p is honest, and the few processes that "
            "wrote to p are corrupted instead, silent towards it. Still fewer than f faults. <bookmark mark='d'/> "
            "Everyone else sees the first world again. p, hearing nothing, decides some fixed value b; give the "
            "sender the other value, and validity makes the rest decide it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ops), FadeIn(vps), Create(vbox))
            vo.wait_until("a")
            self.play(FadeIn(vl), FadeIn(rows[0]), FadeIn(whys[0]))
            self.play(LaggedStart(*[Create(g) for g in per], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(inl), FadeIn(thr), FadeIn(ill))
            vo.wait_until("b")
            self.play(Create(ring), inl[p_].animate.set_color(HEAD))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(vps[p_][0].animate.set_stroke(YES), FadeIn(bad), per[p_].animate.set_stroke(NO, opacity=0.25))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ quadratic and linear
    def linear(self):
        head = label(r"Votes to everyone, \ or through the leader", font_size=36).to_edge(UP, buff=0.3)
        n = 7
        CL, CR = np.array([-3.5, 0.5, 0]), np.array([3.5, 0.5, 0])
        PL = polygon_pos(n, CL, 1.4)
        psl = VGroup(*[proc().move_to(p) for p in PL])
        linksl = VGroup(*[Line(PL[i], PL[j], color=GREY_D, stroke_width=1, buff=0.28)
                          for i in range(n) for j in range(i + 1, n)])
        PR = polygon_pos(n - 1, CR, 1.5)
        lead = proc(r"L", color=HEAD).move_to(CR)
        psr = VGroup(*[proc().move_to(p) for p in PR])
        linksr = VGroup(*[Line(CR, p, color=GREY_D, stroke_width=1, buff=0.28) for p in PR])
        capl = label(r"PBFT \ (1999): \ every vote to every replica", font_size=20, color=DATA).move_to([-3.5, 2.4, 0])
        capr = label(r"HotStuff \ (2019): \ votes to the leader", font_size=20, color=HEAD).move_to([3.5, 2.4, 0])
        fs = 30
        cl = [MathTex(r"n(n-1)", r"\text{ per phase}", font_size=fs),
              MathTex(r"O(n^2)", r"\text{ per decision}", font_size=fs)]
        cr = [MathTex(r"2(n-1)", r"\text{ per phase}", font_size=fs),
              MathTex(r"O(n)", r"\text{ per decision}", font_size=fs)]
        for m in cl:
            m.move_to([-3.5, -1.62, 0])
        for m in cr:
            m.move_to([3.5, -1.62, 0])
        cl[1][0].set_color(NO)
        cr[1][0].set_color(YES)
        qc = tag_box(r"QC", color=HEAD, size=18, w=0.7, h=0.42).move_to(CR + DOWN * 0.55)
        notes = VGroup(
            wrapped_label(r"a \textbf{quorum certificate}: \ $2f + 1$ votes combined into one threshold signature, "
                          r"\ the size of one word", 12.4, font_size=19, color=HEAD),
            wrapped_label(r"HotStuff \ (Yin, \ Malkhi, \ Reiter, \ Gueta and Abraham) \ stays linear when the leader "
                          r"is replaced; \ by its authors' count, \ PBFT's view change costs $O(n^3)$ words", 12.4,
                          font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Practical protocols meet this cost in different ways. <bookmark mark='a'/> PBFT, Miguel Castro and "
            "Barbara Liskov's protocol of 1999, has every replica send its vote to every other: n times n minus "
            "one messages in each phase. <bookmark mark='b'/> HotStuff, from Maofan Yin, Dahlia Malkhi, Michael "
            "Reiter, Guy Golan Gueta and Ittai Abraham in 2019, sends the votes to the leader instead. "
            "<bookmark mark='c'/> The leader combines two f plus one votes into one threshold signature, a quorum "
            "certificate, and sends that single word back: two times n minus one messages a phase. "
            "<bookmark mark='d'/> Linear instead of quadratic, and it stays linear when a leader is replaced, "
            "where PBFT's view change costs on the order of n cubed words."
        ) as vo:
            self.play(FadeIn(head), FadeIn(linksl), FadeIn(psl), FadeIn(linksr), FadeIn(psr), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(capl), FadeIn(cl[0]))
            for _ in range(2):
                dots, anims = pulses([(PL[i], toward(PL[j], PL[i], 0.28)) for i in range(n) for j in range(n)
                                      if i != j])
                self.add(dots)
                self.play(*anims, run_time=1.0)
                self.remove(dots)
            vo.wait_until("b")
            self.play(FadeIn(capr))
            dots, anims = pulses([(p, toward(CR, p, 0.3)) for p in PR], color=DATA)
            self.add(dots)
            self.play(*anims, run_time=1.0)
            vo.wait_until("c")
            self.play(ReplacementTransform(dots, qc), run_time=0.8)
            dots2, anims2 = pulses([(CR, toward(p, CR, 0.28)) for p in PR], color=HEAD)
            self.add(dots2)
            self.play(*anims2, FadeIn(cr[0]), run_time=1.0)
            self.remove(dots2)
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(cl[0], cl[1]), TransformMatchingTex(cr[0], cr[1]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the worst case
    def worst(self):
        head = label(r"Linear per view, \ quadratic in the worst case", font_size=36).to_edge(UP, buff=0.3)
        k = 5
        xs = [-4.2 + 2.1 * i for i in range(k)]
        views = VGroup()
        for i, x in enumerate(xs):
            good = i == k - 1
            col = YES if good else NO
            fr = RoundedRectangle(width=1.75, height=1.25, corner_radius=0.1, stroke_color=col, stroke_width=2,
                                  fill_color=BG, fill_opacity=1).move_to([x, 1.55, 0])
            t = label(rf"view {i + 1}", font_size=18, color=GREY_A).next_to(fr.get_top(), DOWN, buff=0.12)
            ld = proc(r"L", color=col, r=0.22, size=18).move_to(fr.get_center() + DOWN * 0.15)
            st = label(r"decides" if good else r"silent", font_size=16, color=col).next_to(fr, DOWN, buff=0.08)
            views.add(VGroup(fr, t, ld, st))
        unit = 2.1
        y_bar = -0.25
        segs = VGroup(*[Rectangle(width=unit * 0.94, height=0.32, stroke_width=0, fill_color=NO if i < k - 1 else YES,
                                  fill_opacity=0.8).move_to([xs[i], y_bar, 0]) for i in range(k)])
        segl = label(r"$\approx n$ words each", font_size=18, color=GREY_A).next_to(segs[0], DOWN, buff=0.1)
        ill = note(r"illustrative: \ $f = 4$ silent leaders in a row", font_size=16).next_to(segs[-1], DOWN,
                                                                                              buff=0.1)
        fs = 34
        d = [MathTex(r"W", r"=", r"f \cdot O(n)", r"+", r"O(n)", font_size=fs),
             MathTex(r"W", r"=", r"O(fn)", font_size=fs),
             MathTex(r"W", r"=", r"O(n^2)", font_size=fs)]
        for m in d:
            m.move_to([0, -1.45, 0])
        d[2][2].set_color(HEAD)
        w = [label(r"$f$ wasted views, \ then a good one", font_size=19, color=GREY_B),
             label(r"$f$ up to $n/3$: \ exactly Dolev and Reischuk's bound", font_size=19, color=HEAD)]
        for m in w:
            m.move_to([0, -2.15, 0])
        tight = wrapped_label(r"and the bound is \textbf{tight}: \ protocols quadratic in the worst case, \ Momose "
                              r"and Ren \ (2021, \ synchrony with signatures) \ and Civit et al. \ (2022, \ partial "
                              r"synchrony)", 12.4, font_size=19, color=YES).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Does that beat Dolev and Reischuk? No. <bookmark mark='a'/> A faulty leader can simply stay silent; "
            "its view is wasted, and HotStuff moves on to the next leader. <bookmark mark='b'/> With f bad "
            "leaders in a row, each view costs about n words, <bookmark mark='c'/> so the total is f times n, and "
            "with f a third of n that is quadratic again. The lower bound is about the worst case, and the worst "
            "case is a run of bad leaders. <bookmark mark='d'/> And the bound is tight. Protocols that are "
            "quadratic in the worst case were found for synchrony by Atsuki Momose and Ling Ren in 2021, and for "
            "partial synchrony by Pierre Civit and colleagues in 2022."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(views[0]))
            self.play(GrowFromEdge(segs[0], LEFT), FadeIn(segl))
            vo.wait_until("b")
            for i in range(1, k):
                self.play(FadeIn(views[i]), GrowFromEdge(segs[i], LEFT), run_time=0.6)
            self.play(FadeIn(ill), FadeIn(d[0]), FadeIn(w[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(d[0], d[1]))
            self.play(TransformMatchingTex(d[1], d[2]), ReplacementTransform(w[0], w[1]))
            vo.wait_until("d")
            self.play(FadeIn(tight))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ randomness
    def randomness(self):
        head = label(r"What randomness buys", font_size=36).to_edge(UP, buff=0.3)
        cols, rws = 6, 5
        pos = [np.array([-6.1 + 0.62 * c, 2.35 - 0.62 * r, 0]) for r in range(rws) for c in range(cols)]
        rng = random.Random(7)
        faulty = set(rng.sample(range(30), 8))
        comm = sorted(rng.sample(range(30), 7))
        dots = VGroup(*[Circle(radius=0.15, stroke_color=NO if i in faulty else GREY_B, stroke_width=2,
                               fill_color=BG, fill_opacity=1).move_to(p) for i, p in enumerate(pos)])
        rings = VGroup(*[Circle(radius=0.22, color=HEAD, stroke_width=3).move_to(pos[i]) for i in comm])
        fills = [dots[i].animate.set_fill(HEAD, opacity=0.6) for i in comm]
        inner = VGroup(*[Line(pos[a], pos[b], color=HEAD, stroke_width=1.2, stroke_opacity=0.7, buff=0.16)
                         for x, a in enumerate(comm) for b in comm[x + 1:]])
        rest = [i for i in range(30) if i not in comm]
        tell, tanims = pulses([(pos[comm[i % len(comm)]], pos[j]) for i, j in enumerate(rest)], color=HEAD,
                              r=0.045)
        leg = VGroup(label(r"red rim: \ faulty", font_size=17, color=NO),
                     label(r"filled: \ the random committee", font_size=17, color=HEAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(dots, DOWN, buff=0.25).align_to(dots, LEFT)
        ill = note(r"illustrative: \ $n = 30$, \ $c = 7$; \ a sketch", font_size=16).next_to(
            leg, DOWN, buff=0.08).align_to(leg, LEFT)
        fs = 28
        rows = [MathTex(r"M", r"=", r"c^2", r"+", r"c\,n", font_size=fs),
                MathTex(r"\Pr[\text{half the committee faulty}]", r"\le", r"e^{-\Omega(c)}", font_size=fs),
                MathTex(r"c", r"=", r"\Theta(\log n)", font_size=fs),
                MathTex(r"M", r"=", r"O(n \log n)", font_size=fs)]
        rows[3][2].set_color(YES)
        whys = [label(r"the committee agrees, \ then tells everyone", font_size=18, color=GREY_B),
                label(r"under a third faulty overall: \ a Chernoff bound", font_size=18, color=GREY_B),
                label(r"failure probability polynomially small", font_size=18, color=GREY_B),
                label(r"below the deterministic $\Omega(n^2)$", font_size=18, color=YES)]
        col = stacked(rows, whys, buff=0.22).move_to([3.0, 0.75, 0]).align_to([-1.2, 0, 0], LEFT)
        notes = VGroup(
            wrapped_label(r"the catch: \ an adaptive adversary corrupts the committee once it is known; \ Algorand "
                          r"\ (Chen and Micali, \ 2019) \ lets members select themselves secretly and speak once", 12.4,
                          font_size=19, color=HEAD),
            wrapped_label(r"if the adversary can also erase messages already sent, \ $\Omega(f^2)$ holds even with "
                          r"randomness \ (Abraham et al., \ 2019)", 12.4, font_size=19, color=NO),
            wrapped_label(r"randomness also buys time: \ constant expected rounds \ (Feldman and Micali) \ against "
                          r"$f + 1$", 12.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The bound is for deterministic protocols. What does randomness buy? <bookmark mark='a'/> Choose a "
            "small random committee, let it agree among itself, and have it tell everyone: c squared plus c times "
            "n messages. <bookmark mark='b'/> If under a third of all processes are faulty, a random committee is "
            "half faulty only with probability exponentially small in its size, <bookmark mark='c'/> so a "
            "committee of logarithmic size will do, <bookmark mark='d'/> and the cost falls to about n log n. "
            "<bookmark mark='e'/> The catch is an adaptive adversary, who corrupts the committee once it is "
            "known. Algorand, by Jing Chen and Silvio Micali, lets members select themselves secretly and speak "
            "only once. <bookmark mark='f'/> But against an adversary who can also erase messages already sent, "
            "Abraham and colleagues showed that even randomized protocols need f squared. <bookmark mark='g'/> "
            "Randomness also buys time: Pesech Feldman and Silvio Micali reached a constant expected number of "
            "rounds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots))
            vo.wait_until("a")
            self.play(Create(rings), *fills, FadeIn(leg), FadeIn(ill))
            self.play(Create(inner), run_time=1.2)
            self.add(tell)
            self.play(*tanims, run_time=1.2)
            self.remove(tell)
            self.play(FadeIn(col[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[0]))
            vo.wait_until("f")
            self.play(FadeIn(notes[1]))
            vo.wait_until("g")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM, load)
