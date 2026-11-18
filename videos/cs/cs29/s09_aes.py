from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, state_grid)


class Aes(WatchScene):
    def construct(self):
        self.card()
        self.steps()
        self.rounds()

    def card(self):
        self.chapter(8, r"AES", r"What is inside the cipher everyone uses?", lit=(1977, 1998, 2001), extra=((1977, r"DES"), (1998, r"Deep Crack"), (2001, r"AES")), part=PART, said="Chapter eight. The Advanced Encryption Standard.")


    def steps(self):
        self.ask(r"AES has four steps per round. \\ Which one is nonlinear?", [r"ShiftRows", r"MixColumns",
                 r"SubBytes"], 2,
                 say="AES runs four steps in each round. Which one is the only nonlinear step?",
                 reveal="SubBytes, the S-box: inversion in the field of bytes.")
        a = load("aes")
        st = dict(a["steps"])
        head = label(r"One round, \ on FIPS-197's example", font_size=34).to_edge(UP, buff=0.3)
        cell = 0.8
        g0 = state_grid(st["AddRoundKey 0"], cell=cell, font=23).next_to(head, DOWN, buff=0.7).to_edge(LEFT, buff=1.2)
        name = label(r"plaintext $\oplus$ key", font_size=20, color=GREY_A).next_to(g0, UP, buff=0.2)
        panel_x = 0.2
        notes = {
            "sub": VGroup(
                label(r"\textbf{SubBytes}: \ every byte through the S-box", font_size=22, color=DATA),
                label(r"$S(x)$ = the inverse of $x$ in GF(256) \ (Part 28, \ modulus \texttt{0x11b}), \ then a "
                      r"fixed affine map", font_size=19, color=WHITE),
                label(rf"$S(\texttt{{53}})$: \ inverse \texttt{{{a['inv53']:02x}}}, \ then $\to$ "
                      rf"\texttt{{{a['sbox53']:02x}}}: \ the only nonlinear step", font_size=19, color=GREY_A)),
            "shift": VGroup(
                label(r"\textbf{ShiftRows}: \ row $r$ rotates left by $r$", font_size=22, color=HEAD),
                label(r"each column now holds one byte from every column before", font_size=19, color=WHITE)),
            "mix": VGroup(
                label(r"\textbf{MixColumns}: \ each column times a matrix over GF(256)", font_size=22, color=LAM),
                MathTex(r"\begin{pmatrix} 2&3&1&1\\1&2&3&1\\1&1&2&3\\3&1&1&2 \end{pmatrix}", font_size=30,
                        color=LAM),
                label(r"MDS, \ like Reed--Solomon \ (Part 28): \ one changed byte changes all four", font_size=19,
                      color=WHITE)),
            "key": VGroup(
                label(r"\textbf{AddRoundKey}: \ XOR the round key", font_size=22, color=YES),
                label(r"11 round keys come from the key by rotation, \ the S-box and constants", font_size=19,
                      color=WHITE)),
        }
        for v in notes.values():
            v.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([panel_x, g0.get_y(), 0], aligned_edge=LEFT)
            v.set_x(panel_x + v.width / 2)
            if v.get_right()[0] > 6.9:
                v.width = 6.9 - panel_x
                v.set_x(panel_x + v.width / 2)
        seq = [("SubBytes 1", "sub", r"after SubBytes"), ("ShiftRows 1", "shift", r"after ShiftRows"),
               ("MixColumns 1", "mix", r"after MixColumns"), ("AddRoundKey 1", "key", r"after round 1")]
        grids = {k: state_grid(st[k], cell=cell, font=23).move_to(g0) for k, _, _ in seq}
        with self.voiceover(
            "AES works on a four by four grid of bytes, the state, filled column by column. Here is the example from "
            "the standard, after the key has been XORed in. A round has four steps. <bookmark mark='a'/> SubBytes "
            "replaces every byte by its S-box value. The S-box is the field of bytes from Part 28: take the byte's "
            "inverse in the field, then apply a fixed affine map. Fifty-three, inverted, is C A, and comes out as E "
            "D. Inversion is what makes AES nonlinear, and it was chosen because it is as far from linear as a "
            "function on bytes can be. <bookmark mark='b'/> ShiftRows rotates row one by one place, row two by two, "
            "row three by three. <bookmark mark='c'/> MixColumns multiplies each column by a fixed matrix over the "
            "same field. The matrix is maximum distance separable, the property of Reed-Solomon codes: change one "
            "byte of a column and all four output bytes change. <bookmark mark='d'/> Finally XOR the round key, "
            "derived from the cipher key by a small schedule. Substitution confuses; shifting and mixing diffuse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g0), FadeIn(name))
            cur = g0
            prev = None
            for (k, nk, nm), mk in zip(seq, "abcd"):
                vo.wait_until(mk)
                new = grids[k]
                newname = label(nm, font_size=20, color=GREY_A).next_to(new, UP, buff=0.2)
                out = [FadeOut(notes[prev])] if prev else []
                if nk == "shift":
                    anims = [cur.vals[r][c].animate.move_to(cur.cells[r][(c - r) % 4]) for r in range(4)
                             for c in range(4)]
                else:
                    anims = [Transform(cur.vals[r][c], new.vals[r][c]) for r in range(4) for c in range(4)]
                self.play(*out, FadeIn(notes[nk]), *anims, Transform(name, newname), run_time=1.5)
                self.remove(cur)
                self.add(new)
                cur = new
                prev = nk
        self.wait(0.3)
        self.clear_scene()

    def rounds(self):
        a = load("aes")
        head = label(r"Ten rounds, \ and the standard's answer", font_size=34).to_edge(UP, buff=0.3)
        keys = [(n, h) for n, h in a["steps"] if n.startswith("AddRoundKey")]
        g = state_grid(keys[0][1], cell=0.62, font=19).next_to(head, DOWN, buff=0.8).to_edge(LEFT, buff=1.4)
        rl = label(r"round 0", font_size=22, color=GREY_A).next_to(g, UP, buff=0.2)
        out = mono(" ".join(a["cipher"][i:i + 8] for i in range(0, 32, 8)), 22, YES)
        exp = mono(" ".join(a["expected"][i:i + 8] for i in range(0, 32, 8)), 22, DATA)
        pair = VGroup(VGroup(label(r"ours:", font_size=20, color=GREY_A), out).arrange(RIGHT, buff=0.3),
                      VGroup(label(r"FIPS-197, \ C.1:", font_size=20, color=GREY_A), exp).arrange(RIGHT, buff=0.3)
                      ).arrange(DOWN, aligned_edge=RIGHT, buff=0.2).next_to(g, RIGHT, buff=0.9)
        tick = label(r"\checkmark \ identical", font_size=24, color=YES).next_to(pair, DOWN, buff=0.25)
        lines = VGroup(
            label(r"the last round skips MixColumns; \ decryption runs the inverse steps in reverse", font_size=21,
                  color=WHITE),
            label(r"also checked: \ the standard's Appendix B, \ and decryption of random blocks", font_size=21,
                  color=GREY_A),
            label(r"\textbf{educational code: \ never use it for real} \ (it is slow, \ and leaks through timing: "
                  r"\ chapter 15)", font_size=21, color=NO),
            label(r"real CPUs: \ one instruction per round \ (AES-NI, \ 2010): \ about a byte per clock cycle",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now run all ten rounds. <bookmark mark='a'/> Here is the state after each one. Within two rounds, "
            "every byte depends on every byte of the input and the key. The last round leaves out MixColumns, which "
            "makes decryption, the inverse steps in reverse order, the same shape as encryption. <bookmark "
            "mark='b'/> After round ten: sixty-nine, C four, E zero, D eight. The standard's appendix gives "
            "the same sixteen bytes. Our AES also matches the standard's second example, and decrypts what it "
            "encrypts. <bookmark mark='c'/> This is code for learning. Never use it, or anything like it, for real: "
            "it is slow, and as chapter fifteen shows, its table lookups leak the key through timing. <bookmark "
            "mark='d'/> Since 2010 most processors have had AES instructions, one round per instruction, at about "
            "a byte per clock cycle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(rl))
            vo.wait_until("a")
            for r, (n, h) in enumerate(keys[1:], 1):
                new = state_grid(h, cell=0.62, font=19).move_to(g)
                nl = label(rf"round {r}", font_size=22, color=GREY_A).next_to(new, UP, buff=0.2)
                self.play(*[Transform(g.vals[i][j], new.vals[i][j]) for i in range(4) for j in range(4)],
                          Transform(rl, nl), run_time=0.6)
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(pair))
            self.play(FadeIn(tick), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()
