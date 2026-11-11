from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (BG, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono)

TRAIL = [{1: (0xB, 0x2)}, {2: (0x4, 0x6)}, {1: (0x2, 0x5), 2: (0x2, 0x5)}]   # round -> {S-box: (in, out)}


def perm(i):
    return (i % 4) * 4 + i // 4


def spn_diagram(dx=0.34, top=2.4, rh=1.25):
    """Heys' SPN: 16 wires, three full rounds and a last S-box layer; returns the group and the trail's pieces."""
    xs = [-2.55 + dx * i + 0.12 * (i // 4) for i in range(16)]
    g, trail = VGroup(), VGroup()
    y = top
    active = {i for i in range(16) if (0x0B00 >> (15 - i)) & 1}
    for r in range(4):
        key = Line([xs[0] - 0.25, y, 0], [xs[-1] + 0.25, y, 0], color=HEAD, stroke_width=2)
        g.add(key, label(rf"$K_{r + 1}$", font_size=16, color=HEAD).next_to(key, LEFT, buff=0.1))
        sy = y - 0.4
        for s in range(4):
            box = Rectangle(width=dx * 3.6, height=0.36, stroke_color=DATA, stroke_width=1.5, fill_color=BG,
                            fill_opacity=1).move_to([(xs[4 * s] + xs[4 * s + 3]) / 2, sy, 0])
            on = r < 3 and s in TRAIL[r]
            if on:
                trail.add(box.copy().set_stroke(NO, width=3).set_fill(opacity=0))
            g.add(box, label(rf"$S_{{{r + 1}{s + 1}}}$", font_size=13, color=GREY_A).move_to(box))
        for i in range(16):
            seg = Line([xs[i], y + 0.25, 0] if r == 0 else [xs[i], y + 0.05, 0], [xs[i], sy + 0.18, 0], color=GREY_D,
                       stroke_width=1)
            g.add(seg)
            if i in active:
                trail.add(seg.copy().set_stroke(NO, width=2.5))
        if r == 3:
            fk = Line([xs[0] - 0.25, sy - 0.5, 0], [xs[-1] + 0.25, sy - 0.5, 0], color=HEAD, stroke_width=2)
            g.add(fk, label(r"$K_5$", font_size=16, color=HEAD).next_to(fk, LEFT, buff=0.1))
            for i in range(16):
                g.add(Line([xs[i], sy - 0.18, 0], [xs[i], sy - 0.7, 0], color=GREY_D, stroke_width=1))
            break
        out = set()
        for s, (a, b) in TRAIL[r].items():
            for k in range(4):
                if (b >> (3 - k)) & 1:
                    out.add(4 * s + k)
        ny = y - rh
        for i in range(16):
            on = i in out
            ln = Line([xs[i], sy - 0.18, 0], [xs[perm(i)], ny + 0.05, 0], color=GREY_D, stroke_width=1)
            g.add(ln)
            if on:
                trail.add(ln.copy().set_stroke(NO, width=2.5))
        active = {perm(i) for i in out}
        y = ny
    return g, trail


class Cryptanalysis(VoiceoverScene):
    def construct(self):
        self.card()
        self.trail()
        self.attack()
        self.mitm()

    def card(self):
        card = chapter_card(14, r"Cryptanalysis", r"How are real ciphers attacked?", lit=(1990, 1993),
                            extra=((1990, r"Biham--Shamir: \ differential"), (1993, r"Matsui: \ linear")), part=PART)
        with self.voiceover("Chapter fourteen. Cryptanalysis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def trail(self):
        s = load("spn")
        head = label(r"Following a difference", font_size=34).to_edge(UP, buff=0.3)
        g, tr = spn_diagram()
        VGroup(g, tr).scale(0.9).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.9)
        t = s["table"]
        cells = VGroup()
        cs = 0.2
        hi = {(0xB, 0x2), (0x4, 0x6), (0x2, 0x5)}
        for a in range(16):
            for b in range(16):
                v = t[a][b]
                sq = Square(side_length=cs, stroke_width=0.4, stroke_color=GREY_D,
                            fill_color=NO if (a, b) in hi else DATA, fill_opacity=min(1.0, v / 8) if a else 0.1)
                sq.move_to([b * cs, -a * cs, 0])
                cells.add(sq)
        cells.center()
        tl = VGroup(label(r"S-box difference table", font_size=17, color=GREY_A),
                    label(r"row: \ $\Delta$in, \ column: \ $\Delta$out", font_size=15, color=GREY_B)).arrange(
            DOWN, buff=0.05)
        tab = VGroup(tl, cells).arrange(DOWN, buff=0.12).next_to(g, RIGHT, buff=0.6).align_to(g, UP)
        notes = VGroup(
            label(r"Heys' toy cipher: \ 16 bits, \ 4-bit S-boxes, \ a bit permutation, \ 4 rounds", font_size=19,
                  color=WHITE),
            label(r"$\Delta$in \texttt{B} $\to$ $\Delta$out \texttt{2} \ for 8 of 16 inputs: \ a hot cell", font_size=19,
                  color=NO),
            label(r"trail: \ \texttt{B}$\to$\texttt{2} $(\tfrac{8}{16})$, \ \texttt{4}$\to$\texttt{6} "
                  r"$(\tfrac{6}{16})$, \ \texttt{2}$\to$\texttt{5} $(\tfrac{6}{16})^2$", font_size=19, color=HEAD),
            label(rf"total $\tfrac{{27}}{{1024}}$: \ of {s['pairs']:,} pairs, \ about {s['expected_right']:.0f} "
                  r"follow it".replace(",", "{,}", 1), font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(tab, DOWN, buff=0.35).align_to(tab, LEFT)
        fit_right(notes)
        with self.voiceover(
            "How are ciphers like AES attacked, and how are they designed to resist? We use a teaching cipher by "
            "Howard Heys, small enough to break. <bookmark mark='a'/> Sixteen bits, four rounds, each a key XOR, "
            "four four-bit S-boxes, and a permutation of the wires. <bookmark mark='b'/> Eli Biham and Adi Shamir's "
            "differential cryptanalysis, published in 1990, follows not values but differences: pairs of inputs "
            "that differ by a fixed XOR. The key XOR leaves a difference unchanged. Only the S-boxes change it, and "
            "not uniformly: this table counts, for each input difference, how often each output difference occurs. "
            "Input difference B gives output difference two in eight of the sixteen cases. <bookmark mark='c'/> "
            "Chain likely cells through three rounds, following the wires, and you have a trail: a difference that "
            "survives with probability eight sixteenths, times six sixteenths, times six sixteenths squared. "
            "<bookmark mark='d'/> Twenty-seven in a thousand and twenty-four. Of five thousand chosen pairs, about a "
            "hundred and thirty should follow it all the way to the last round."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(tr), FadeIn(notes[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def attack(self):
        s = load("spn")
        head = label(r"Counting the right pairs", font_size=34).to_edge(UP, buff=0.3)
        counts = s["counts"]
        keys = s["guesses"]
        true = s["true_subkey"]
        ax = Axes(x_range=[0, 256, 32], y_range=[0, 160, 40], x_length=7.4, y_length=3.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.6).to_edge(
            LEFT, buff=1.0)
        bars = VGroup()
        for i, (k, c) in enumerate(zip(keys, counts)):
            if c == 0:
                continue
            base, top = ax.c2p(i + 0.5, 0), ax.c2p(i + 0.5, c)
            bars.add(Rectangle(width=0.024, height=top[1] - base[1], stroke_width=0,
                               fill_color=YES if k == true else DATA, fill_opacity=1).move_to(base, aligned_edge=DOWN))
        ti = keys.index(true)
        tl = label(rf"\texttt{{{true >> 8:X}}}, \ \texttt{{{true & 15:X}}}: \ {counts[ti]} pairs", font_size=18,
                   color=YES).next_to(ax.c2p(ti + 0.5, counts[ti]), LEFT, buff=0.15)
        yt = VGroup(*[label(str(y), font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (0, 40, 80, 120, 160)])
        xl = label(r"the 256 guesses for the last-round key bits under $S_{42}$ and $S_{44}$", font_size=17,
                   color=GREY_A).next_to(ax, DOWN, buff=0.2)
        second = s["top"][1][1]
        notes = VGroup(
            label(r"for each guess: \ undo the last S-boxes \\ on both ciphertexts; \ count pairs \\ showing "
                  r"$\Delta$ = \texttt{0606}", font_size=19, color=WHITE),
            label(rf"right key: \ {counts[ti]} \ (expected {s['expected_right']:.0f}) \\ best wrong guess: \ {second}",
                  font_size=19, color=YES),
            label(rf"{s['seconds']:.2f} seconds; \ then peel off \\ the rest of the key", font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        lines = VGroup(
            label(r"DES's S-boxes were tuned against this in 1974, \ and kept secret: \ IBM and the NSA knew \ "
                  r"(Coppersmith, 1994)", font_size=20, color=WHITE),
            label(r"\textbf{linear} cryptanalysis \ (Matsui, 1993): \ biased XORs of bits instead; \ DES from $2^{43}$ "
                  r"known plaintexts", font_size=20, color=LAM),
            label(r"AES's design \textbf{proves} every 4-round trail has at least 25 active S-boxes: \ probability "
                  r"$\le 2^{-150}$", font_size=20, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now the attack. We encrypt five thousand pairs of chosen plaintexts with that input difference, under "
            "an unknown key. <bookmark mark='a'/> The trail predicts the difference just before the last S-boxes. "
            "Guess the eight key bits that feed the two active S-boxes; undo those S-boxes on both ciphertexts; and "
            "count how many pairs show the predicted difference. <bookmark mark='b'/> For the right guess, the "
            "trail's pairs show up: a hundred and forty-six, against the hundred and thirty-two expected. Wrong "
            "guesses see only chance: the best wrong one gets eighty. <bookmark mark='c'/> A third of a second, "
            "and eight key bits are known; the rest of the key follows the same way. <bookmark mark='d'/> IBM's "
            "designers knew this technique in 1974, as Don Coppersmith revealed twenty years later, and chose DES's "
            "S-boxes to resist it. <bookmark mark='e'/> Mitsuru Matsui's linear cryptanalysis tracks biased XORs of "
            "bits instead of differences, and broke DES with two to the forty-three known plaintexts. <bookmark "
            "mark='f'/> AES was designed with proofs against both: its mixing guarantees at least twenty-five active "
            "S-boxes in any four-round trail, so no trail is likelier than two to the minus one hundred and fifty."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.005), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(tl), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            for mk, ln in zip("def", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def mitm(self):
        s = load("spn")["mitm"]
        head = label(r"Meet in the middle", font_size=34).to_edge(UP, buff=0.3)
        p = mono("p", 26, WHITE).move_to([-5.6, 1.2, 0])
        e1 = RoundedRectangle(width=1.4, height=0.7, corner_radius=0.1, stroke_color=DATA).move_to([-3.4, 1.2, 0])
        e2 = RoundedRectangle(width=1.4, height=0.7, corner_radius=0.1, stroke_color=HEAD).move_to([1.0, 1.2, 0])
        t1 = label(r"$E_{k_1}$", font_size=24).move_to(e1)
        t2 = label(r"$E_{k_2}$", font_size=24).move_to(e2)
        c = mono("c", 26, WHITE).move_to([3.4, 1.2, 0])
        mid = Dot([-1.2, 1.2, 0], color=YES, radius=0.1)
        wires = VGroup(Arrow(p.get_right(), e1.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5),
                       Arrow(e1.get_right(), mid.get_left(), buff=0.05, color=GREY_B, stroke_width=2.5),
                       Arrow(mid.get_right(), e2.get_left(), buff=0.05, color=GREY_B, stroke_width=2.5),
                       Arrow(e2.get_right(), c.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5))
        f1 = label(r"table: \ $E_{k_1}(p)$ \\ for all $2^{16}$ keys $k_1$", font_size=19, color=DATA).next_to(
            e1, DOWN, buff=0.4)
        f2 = label(r"$D_{k_2}(c)$ for all $2^{16}$ $k_2$: \\ look each up in the table", font_size=19,
                   color=HEAD).next_to(e2, DOWN, buff=0.4)
        meet = label(r"they meet here", font_size=19, color=YES).next_to(mid, UP, buff=0.3)
        bad = [k for k in s["found"] if k != s["keys"]]
        lines = VGroup(
            label(r"double encryption with two 16-bit keys: \ is it a 32-bit key?", font_size=21, color=WHITE),
            label(rf"meet in the middle \ (Diffie and Hellman, 1977): \ {s['work']:,} cipher calls instead of "
                  rf"{s['brute']:,}".replace(",", "{,}"), font_size=21, color=YES),
            label(rf"two known plaintext pairs leave {len(s['found'])} candidates: \ the true pair and "
                  rf"{len(bad)} impostor; \ a third pair decides", font_size=21, color=HEAD),
            label(r"so 2DES has the strength of about one DES key: \ hence \textbf{triple} DES, \ 112-bit security, \ "
                  r"retired in 2023", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "One more attack, on a tempting idea. <bookmark mark='a'/> If one key is too short, encrypt twice with "
            "two keys. With our toy cipher's sixteen-bit keys, does that make a thirty-two-bit key? <bookmark "
            "mark='b'/> No. Given a plaintext and its ciphertext, encrypt the plaintext under every first key and "
            "store the results. Then decrypt the ciphertext under every second key, and look each result up. Where "
            "they match, the two halves meet in the middle. Whitfield Diffie and Martin Hellman pointed this out in "
            "1977: a hundred and thirty-one thousand cipher calls instead of four billion. <bookmark mark='c'/> "
            "With a second plaintext pair, two candidate key pairs survive: the true one, and one impostor that "
            "happens to fit both. A third pair would settle it. <bookmark mark='d'/> So double DES is barely "
            "stronger than DES, which is why the banks' long-lived workaround was triple DES, at about a hundred "
            "and twelve bits of security, finally retired by the standards institute in 2023."
        ) as vo:
            self.play(FadeIn(head), FadeIn(p), FadeIn(e1), FadeIn(t1), FadeIn(e2), FadeIn(t2), FadeIn(c),
                      FadeIn(wires), FadeIn(mid))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(f1))
            self.play(FadeIn(f2), FadeIn(meet), mid.animate.scale(1.6))
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()
