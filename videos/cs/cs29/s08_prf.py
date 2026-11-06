from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (BG, DATA, HEAD, NO, PART, YES, flow_box, grid_table, load, mono)


class Prf(VoiceoverScene):
    def construct(self):
        self.card()
        self.ggm()
        self.feistel()
        self.switching()

    def card(self):
        card = chapter_card(7, r"Pseudorandom functions and permutations", r"Can a key choose a random-looking "
                            r"function?", lit=(1973, 1986, 1988),
                            extra=((1973, r"Feistel's networks"), (1986, r"Goldreich--Goldwasser--Micali"),
                                   (1988, r"Luby--Rackoff")), part=PART)
        with self.voiceover("Chapter seven. Pseudorandom functions and permutations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ggm(self):
        g = load("ggm")
        head = label(r"A random-looking function from a tree", font_size=34).to_edge(UP, buff=0.3)
        nodes = g["nodes"]
        pos = {}
        for p in nodes:
            d = len(p)
            idx = int(p, 2) if p else 0
            n = 2 ** d
            pos[p] = np.array([-5.6 + 11.2 * (idx + 0.5) / n, 1.9 - 1.15 * d, 0])
        path = [g["input"][:i] for i in range(len(g["input"]) + 1)]
        mobs = {}
        for p, h in nodes.items():
            on = p in path
            box = RoundedRectangle(width=1.25, height=0.48, corner_radius=0.08, stroke_color=YES if on else GREY_B,
                                   stroke_width=2.5 if on else 1.2, fill_color=BG, fill_opacity=1).move_to(pos[p])
            mobs[p] = VGroup(box, mono(h[:8], 15, WHITE if on else GREY_A).move_to(box))
        edges = VGroup()
        for p in nodes:
            if p:
                on = p in path
                e = Line(pos[p[:-1]] + DOWN * 0.25, pos[p] + UP * 0.25, color=YES if on else GREY_D,
                         stroke_width=3 if on else 1.4)
                edges.add(VGroup(e, mono(p[-1], 15, YES if on else GREY_C).move_to(e.get_center() + LEFT * 0.18)))
        seed = label(r"key $k$", font_size=17, color=HEAD).next_to(mobs[""], LEFT, buff=0.2)
        lines = VGroup(
            label(r"a \textbf{PRF} $F_k$: \ even with queries $x$ of its choice, \ no efficient attacker tells $F_k$ "
                  r"from a truly random function", font_size=21, color=WHITE),
            label(r"Goldreich, \ Goldwasser, \ Micali \ (1986): \ $G(s) = G_0(s) \,\|\, G_1(s)$; \ walk the bits of "
                  r"$x$ down the tree", font_size=21, color=DATA),
            label(rf"here $G$ is SHA-256 cut to two 8-byte halves; \ $F_k(\texttt{{{g['input']}}}) = "
                  rf"\texttt{{{g['output'][:8]}}}\ldots$", font_size=21, color=YES),
            label(r"proof: \ a \textbf{hybrid argument}: \ replace one level at a time by true randomness; \ each "
                  r"swap is invisible if $G$ is a PRG", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.17).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A generator gives one long random-looking string. Often we need more: a function that gives a "
            "random-looking answer for any input we ask about, the same answer each time. <bookmark mark='a'/> A "
            "pseudorandom function is a keyed function that no efficient attacker can tell from a truly random one, "
            "even choosing the inputs. <bookmark mark='b'/> Oded Goldreich, Shafi Goldwasser and Silvio Micali built "
            "one from any generator in 1986. Take a generator that doubles its input, and split the output into a "
            "left half and a right half. Start from the key at the root, and walk down a tree, following the bits of "
            "the input: zero means take the left half, one the right. <bookmark mark='c'/> With SHA-256 as the "
            "generator, input one, zero, one leads here, and this leaf is the output. <bookmark mark='d'/> The proof "
            "is a hybrid argument. Replace the top level with true randomness; then the next; and so on, one level "
            "at a time. If any step could be noticed, that would break the generator. After n steps the function is "
            "truly random."
        ) as vo:
            self.play(FadeIn(head), FadeIn(mobs[""]), FadeIn(seed))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(e, mobs[p])) for e, p in zip(edges, [p for p in nodes if p])],
                                  lag_ratio=0.15), FadeIn(lines[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(lines[2]), Indicate(mobs[g["input"]], color=YES))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def feistel(self):
        f = load("feistel")
        head = label(r"Feistel networks: \ permutations from functions", font_size=34).to_edge(UP, buff=0.3)
        Lb = flow_box(r"$L$", DATA, w=1.3, h=0.6, font=24)
        Rb = flow_box(r"$R$", HEAD, w=1.3, h=0.6, font=24)
        top = VGroup(Lb, Rb).arrange(RIGHT, buff=1.6).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        Lo = flow_box(r"$R$", HEAD, w=1.3, h=0.6, font=24)
        Ro = flow_box(r"$L \oplus f(R)$", DATA, w=1.6, h=0.6, font=22)
        bot = VGroup(Lo, Ro).arrange(RIGHT, buff=1.3).next_to(top, DOWN, buff=2.0).align_to(top, LEFT)
        fbox = flow_box(r"$f$", YES, w=0.8, h=0.6, font=24).move_to([Rb.get_x(), top.get_y() - 1.0, 0])
        xo = MathTex(r"\oplus", font_size=40, color=WHITE).move_to([Lb.get_x(), fbox.get_y(), 0])
        wires = VGroup(
            Arrow(Rb.get_bottom(), fbox.get_top(), buff=0.05, stroke_width=2.5, color=GREY_B),
            Arrow(fbox.get_left(), xo.get_right(), buff=0.08, stroke_width=2.5, color=GREY_B),
            Arrow(Lb.get_bottom(), xo.get_top(), buff=0.08, stroke_width=2.5, color=GREY_B),
            Arrow(xo.get_bottom(), Ro.get_top(), buff=0.08, stroke_width=2.5, color=GREY_B),
            Arrow(fbox.get_bottom() + RIGHT * 0.25, Lo.get_top(), buff=0.08, stroke_width=2.5, color=GREY_B),
        )
        tab = grid_table([r"rounds", r"our test fires", r"random permutation"],
                         [[str(r["rounds"]), f"{100 * r['feistel']:.0f}%", f"{100 * r['random']:.0f}%"]
                          for r in f["rows"]], widths=[1.2, 2.6, 2.4], row_h=0.48, font_size=20, mono_cols=(1, 2))
        tab.next_to(top, RIGHT, buff=1.2).align_to(top, UP)
        tnote = label(rf"{f['trials']:,} trials each, \ 16-bit halves, \\ random round functions".replace(",", "{,}"),
                      font_size=17, color=GREY_A).next_to(tab, DOWN, buff=0.2)
        lines = VGroup(
            label(r"one round: \ $(L, R) \mapsto (R, \ L \oplus f(R))$: \ invertible for \textbf{any} $f$: \ run it "
                  r"backwards", font_size=21, color=WHITE),
            label(r"two rounds fail: \ inputs $(L_1, R)$ and $(L_2, R)$ give left outputs that XOR to $L_1 \oplus "
                  r"L_2$, \ always", font_size=21, color=NO),
            label(r"Luby and Rackoff \ (1988): \ \textbf{three} rounds of a PRF give a pseudorandom permutation; "
                  r"\ four resist decryption queries too", font_size=21, color=YES),
            label(r"DES: \ 16 Feistel rounds \ (IBM, 1977)", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.17).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A block cipher must be a permutation: every ciphertext must decrypt to one plaintext. A random-looking "
            "function need not be invertible. Horst Feistel, at IBM, found the bridge. <bookmark mark='a'/> Split the "
            "block into halves. The right half goes through any function f, the result is XORed into the left half, "
            "and the halves swap. Whatever f is, the round can be undone: you know R, so you can compute f of R again "
            "and XOR it back off. <bookmark mark='b'/> How many rounds make it look random? Two are not enough. Feed "
            "in two inputs with the same right half: the left halves of the outputs always differ by exactly the "
            "difference of the inputs. Our test catches one and two rounds every time. <bookmark mark='c'/> Michael "
            "Luby and Charles Rackoff proved in 1988 that three rounds with pseudorandom round functions give a "
            "pseudorandom permutation, and four give one that stays secure even when the attacker can also ask for "
            "decryptions. On three rounds, our test never fires. <bookmark mark='d'/> The Data Encryption Standard "
            "of 1977 is sixteen Feistel rounds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(fbox), FadeIn(xo), LaggedStart(*[GrowArrow(w) for w in wires], lag_ratio=0.2),
                      FadeIn(bot), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), FadeIn(tab.cells[0][2]), FadeIn(tab.rule),
                      FadeIn(VGroup(*tab.cells[1], *tab.cells[2])), FadeIn(tnote), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[3])), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def switching(self):
        head = label(r"Function or permutation? \ The birthday again", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 40, 8], y_range=[0, 1.0, 0.25], x_length=6.4, y_length=3.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.6).to_edge(
            LEFT, buff=1.0)
        import math
        n = 64
        pts = [ax.c2p(e, 1 - math.exp(-(2.0 ** e) ** 2 / 2 ** (n + 1))) for e in [x / 4 for x in range(0, 161)]]
        cur = VMobject(color=NO, stroke_width=3).set_points_as_corners(pts)
        xt = VGroup(*[MathTex(rf"2^{{{e}}}", font_size=20, color=GREY_A).next_to(ax.c2p(e, 0), DOWN, buff=0.1)
                      for e in (0, 8, 16, 24, 32, 40)])
        yt = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.1)
                      for y, t in ((0, "0"), (0.5, "0.5"), (1, "1"))])
        xl = label(r"blocks encrypted under one key \ (64-bit blocks)", font_size=17, color=GREY_A).next_to(
            xt, DOWN, buff=0.12)
        yl = label(r"chance a random \textbf{function} would have repeated", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        mark = DashedLine(ax.c2p(32, 0), ax.c2p(32, 1), color=HEAD, stroke_width=1.5)
        notes = VGroup(
            label(r"a permutation never repeats an output; \\ a random function does, \ after about \\ "
                  r"$2^{n/2}$ queries \ (Part 17's birthday)", font_size=20, color=WHITE),
            label(r"so a PRP is a PRF, \\ up to an advantage of $q^2 / 2^{n+1}$", font_size=20, color=DATA),
            label(r"for 64-bit blocks \ (3DES, \ Blowfish): \\ $2^{32}$ blocks is only 32 GB", font_size=20,
                  color=NO),
            label(r"Sweet32 \ (2016): \ colliding blocks in \\ long HTTPS sessions leaked cookies", font_size=20,
                  color=HEAD),
            label(r"so AES has 128-bit blocks, \\ and keys are changed long before $2^{64}$", font_size=20,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        with self.voiceover(
            "Is a pseudorandom permutation also a pseudorandom function? Almost, and the difference matters. "
            "<bookmark mark='a'/> A permutation never gives the same output twice. A random function does, by the "
            "birthday paradox of Part 17, after about the square root of the number of possible outputs. <bookmark "
            "mark='b'/> Until then the two look the same: the advantage of telling them apart is at most q squared "
            "over two to the n plus one, for q queries. <bookmark mark='c'/> For a sixty-four-bit block, as in "
            "triple DES or Blowfish, the square root is two to the thirty-two blocks: just thirty-two gigabytes. "
            "<bookmark mark='d'/> In 2016 the Sweet32 attack used exactly this. In long-lived HTTPS connections "
            "with sixty-four-bit ciphers, colliding ciphertext blocks revealed the XOR of two plaintext blocks, and "
            "eventually a secret cookie. <bookmark mark='e'/> This is why AES has a hundred-and-twenty-eight-bit "
            "block, and why protocols change keys long before the birthday bound."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(cur), FadeIn(notes[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(mark), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()
