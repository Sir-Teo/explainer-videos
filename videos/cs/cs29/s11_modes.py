from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (BG, DATA, HEAD, NO, PART, YES, load, mono, pixel_image)


class Modes(VoiceoverScene):
    def construct(self):
        self.card()
        self.four()
        self.oracle_idea()
        self.oracle_run()

    def card(self):
        card = chapter_card(10, r"Modes of operation", r"How do you encrypt more than 16 bytes?", lit=(1980, 2002),
                            extra=((1980, r"FIPS 81: \ ECB, CBC, \ldots"), (2002, r"Vaudenay's padding oracle"),
                                   (2014, r"POODLE")), part=PART)
        with self.voiceover("Chapter ten. Modes of operation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def four(self):
        p = load("penguin")
        head = label(r"The logo, \ four ways", font_size=34).to_edge(UP, buff=0.3)
        imgs = Group(*[pixel_image(p[k], p["w"], p["h"], height=2.1) for k in ("plain", "ecb", "cbc", "ctr")])
        imgs.arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=0.4)
        names = [(r"plaintext", GREY_A), (r"ECB", NO), (r"CBC", YES), (r"CTR", YES)]
        forms = [r"P_i", r"C_i = E_k(P_i)", r"C_i = E_k(P_i \oplus C_{i-1})", r"C_i = P_i \oplus E_k(N \,\|\, i)"]
        caps = VGroup()
        for im, (n, c), f in zip(imgs, names, forms):
            caps.add(VGroup(label(n, font_size=21, color=c), MathTex(f, font_size=22, color=WHITE)).arrange(
                DOWN, buff=0.1).next_to(im, DOWN, buff=0.15))
        lines = VGroup(
            label(rf"ECB: \ each block alone: \ {p['distinct_ecb']} distinct ciphertext blocks of {p['blocks']}, \ "
                  r"the same as the picture: \ deterministic, \ so not even CPA-secure", font_size=20, color=NO),
            label(rf"CBC \ (1976): \ XOR in the previous ciphertext \ (a random IV first): \ {p['distinct_cbc']} "
                  r"distinct blocks", font_size=20, color=YES),
            label(r"CTR: \ encrypt a counter, \ XOR it in: \ a stream cipher from a block cipher, \ parallel, \ "
                  r"random access", font_size=20, color=DATA),
            label(r"CTR's rule: \ never reuse a nonce under one key, \ or it is the two-time pad of chapter 4",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A block cipher encrypts sixteen bytes. A mode of operation says how to encrypt a message of any length. "
            "<bookmark mark='a'/> The obvious mode, electronic codebook, encrypts each block on its own. It is "
            "deterministic, so by chapter five it cannot be secure, and our logo shows why: the eighty-five distinct "
            "blocks of the picture become eighty-five distinct blocks of ciphertext, in the same places. <bookmark "
            "mark='b'/> Cipher block chaining, from 1976, XORs each plaintext block with the previous ciphertext "
            "block before encrypting, starting from a random initial value. Now every block is different. <bookmark "
            "mark='c'/> Counter mode encrypts a nonce followed by a block counter and XORs the result into the "
            "plaintext. It turns the block cipher into a stream cipher, like chapter six's: blocks can be done in "
            "parallel, or any one decrypted alone. <bookmark mark='d'/> Its one rule is absolute. Never encrypt two "
            "messages under one key with the same nonce, or you have made a two-time pad."
        ) as vo:
            self.play(FadeIn(head), FadeIn(imgs[0]), FadeIn(caps[0]))
            vo.wait_until("a")
            self.play(FadeIn(imgs[1]), FadeIn(caps[1]), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(imgs[2]), FadeIn(caps[2]), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(imgs[3]), FadeIn(caps[3]), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def oracle_idea(self):
        head = label(r"A server that says too much", font_size=34).to_edge(UP, buff=0.3)
        pad = VGroup(*[mono(t, 20, c) for t, c in (("... 41 54 21", WHITE), ("05 05 05 05 05", HEAD))]).arrange(
            RIGHT, buff=0.15)
        pl = label(r"PKCS\#7: \ fill the last block with $n$ bytes of value $n$", font_size=21, color=WHITE)
        top = VGroup(pl, pad).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.4)
        f = MathTex(r"P_i = D_k(C_i) \oplus C_{i-1}", font_size=40, color=YES).next_to(top, DOWN, buff=0.45)
        steps = VGroup(
            label(r"1. \ the server decrypts, \ checks the padding, \ and answers \textit{bad padding} or "
                  r"\textit{bad MAC}: \ an \textbf{oracle}", font_size=21, color=WHITE),
            label(r"2. \ the attacker changes the last byte of $C_{i-1}$ by XOR with a guess $g \oplus "
                  r"\texttt{01}$, \ and sends $C_{i-1}' \, C_i$", font_size=21, color=DATA),
            label(r"3. \ padding is valid only if the last byte of $P_i$ became \texttt{01}: \ that is, \ the guess "
                  r"$g$ was the byte", font_size=21, color=HEAD),
            label(r"4. \ at most 256 tries per byte; \ then aim for \texttt{02 02}, \ and so on, \ right to left",
                  font_size=21, color=YES),
            label(r"Vaudenay \ (2002); \ in SSL and TLS: \ Lucky Thirteen \ (2013), \ POODLE \ (2014)",
                  font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(f, DOWN, buff=0.45)
        with self.voiceover(
            "CBC has its own trap, and it shows how a single bit of leaked information can unravel everything. "
            "<bookmark mark='a'/> Messages are padded to a whole number of blocks; the usual rule fills the last "
            "block with n bytes, each of value n. <bookmark mark='b'/> Decryption of a block is the block cipher's "
            "inverse, XORed with the previous ciphertext block. So whatever the attacker XORs into the previous "
            "block appears, bit for bit, in the decrypted plaintext. <bookmark mark='c'/> Now suppose the server "
            "decrypts, checks the padding, and reports a padding error differently from any other error, by message "
            "or just by timing. <bookmark mark='d'/> The attacker sends a doctored previous block, changing its last "
            "byte by a guess. <bookmark mark='e'/> The padding is valid only when the plaintext's last byte has "
            "become one, and that happens exactly when the guess was right. <bookmark mark='f'/> At most two hundred "
            "and fifty-six tries reveal one byte; then the attacker aims for two twos, then three threes, working "
            "right to left. <bookmark mark='g'/> Serge Vaudenay described it in 2002, and versions of it broke SSL "
            "and TLS more than once in the following decade."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top))
            vo.wait_until("b")
            self.play(FadeIn(f))
            for mk, st in zip("cdefg", steps):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def oracle_run(self):
        d = load("padding")
        head = label(r"The attack, \ run", font_size=34).to_edge(UP, buff=0.3)
        msg = d["message"]
        nblk = d["blocks"]
        blocks = VGroup()
        for b in range(nblk):
            r = Rectangle(width=4.0, height=0.7, stroke_color=DATA, stroke_width=2, fill_color=BG, fill_opacity=1)
            blocks.add(VGroup(r, label(rf"$C_{b + 1}$", font_size=20, color=DATA).next_to(r, UP, buff=0.08)))
        blocks.arrange(RIGHT, buff=0.25).next_to(head, DOWN, buff=0.7)
        dx = 4.0 / 16
        chars = VGroup()
        order = []
        for b in range(nblk):
            for j in range(16):
                i = 16 * b + j
                ch = msg[i] if i < len(msg) else "·"
                m = mono("_" if ch == " " else ch, 20, YES if i < len(msg) else GREY_C)
                m.move_to(blocks[b][0].get_left() + RIGHT * dx * (j + 0.5))
                chars.add(m)
        for b in range(nblk):
            for j in range(15, -1, -1):
                order.append(16 * b + j)
        counter = Integer(0, font_size=36, color=HEAD)
        ql = label(r"queries to the oracle:", font_size=22, color=GREY_A)
        cg = VGroup(ql, counter).arrange(RIGHT, buff=0.3).next_to(blocks, DOWN, buff=0.7)
        lines = VGroup(
            label(rf"recovered: \ \texttt{{{msg.replace(' ', '~')}}}", font_size=21, color=YES),
            label(rf"{d['queries']:,} queries, \ {d['per_byte']:.0f} per byte, \ {d['seconds']:.1f} seconds; \ no "
                  r"key, \ only \textit{valid} or \textit{invalid}".replace(",", "{,}", 1), font_size=21, color=WHITE),
            label(r"against $2^{128}$ for the key: \ the cipher was never touched", font_size=21, color=HEAD),
            label(r"the lesson: \ check integrity \textbf{before} decrypting: \ encrypt-then-MAC, \ or an AEAD "
                  r"mode \ (next chapter)", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "We built the server and ran the attack. <bookmark mark='a'/> Three blocks of ciphertext, encrypted under "
            "AES with a key the attacker never sees. Each query asks only: is the padding valid? Watch the plaintext "
            "appear, byte by byte, from the right of each block. <bookmark mark='b'/> It reads: PIN equals four nine "
            "two one; transfer approved by the bank. <bookmark mark='c'/> Six thousand four hundred and twelve "
            "queries, about a hundred and thirty-four per byte, two seconds. Recovering the key instead would take "
            "two to the hundred and twenty-eight tries. AES was never attacked at all. <bookmark mark='d'/> The "
            "flaw is decrypting data before checking that it is genuine. The fix is integrity, which is the next "
            "chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(blocks), FadeIn(cg))
            vo.wait_until("a")
            anims = []
            for k, i in enumerate(order):
                anims.append(FadeIn(chars[i]))
            self.play(LaggedStart(*anims, lag_ratio=1.0), ChangeDecimalToValue(counter, d["queries"]),
                      run_time=6.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()
