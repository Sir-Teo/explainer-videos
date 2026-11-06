from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (DATA, HEAD, NO, PART, YES, bit_row, grid_table, load, mono)


class Perfect(VoiceoverScene):
    def construct(self):
        self.card()
        self.pad()
        self.theorem()
        self.twotime()

    def card(self):
        card = chapter_card(4, r"Perfect secrecy", r"Can a cipher be unbreakable?", lit=(1917, 1943, 1949),
                            extra=((1917, r"Vernam's tape"), (1943, r"VENONA begins")), part=PART)
        with self.voiceover("Chapter four. Perfect secrecy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def pad(self):
        head = label(r"The one-time pad", font_size=34).to_edge(UP, buff=0.3)
        m = [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        k = [1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0]
        c = [a ^ b for a, b in zip(m, k)]
        rm, rk, rc = (bit_row(x, size=0.38, font=19, on=col) for x, col in ((m, DATA), (k, HEAD), (c, YES)))
        rows = VGroup(rm, rk, rc).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=1.4)
        tags = VGroup(*[label(t, font_size=19, color=col).next_to(r, LEFT, buff=0.25) for t, col, r in
                        ((r"$m$ \ (``HI'')", DATA, rm), (r"$k$", HEAD, rk), (r"$c = m \oplus k$", YES, rc))])
        tab = grid_table([r"$m$ \textbackslash\ $k$", "00", "01", "10", "11"],
                         [[f"{mm:02b}"] + [f"{mm ^ kk:02b}" for kk in range(4)] for mm in range(4)],
                         widths=[1.2, 0.7, 0.7, 0.7, 0.7], row_h=0.42, font_size=19, mono_cols=(0, 1, 2, 3, 4))
        tab.next_to(rows, RIGHT, buff=0.8).align_to(rows, UP)
        tl = label(r"two bits: \ every row \\ holds every ciphertext once", font_size=18, color=GREY_A).next_to(
            tab, DOWN, buff=0.15)
        lines = VGroup(
            label(r"Vernam \ (1917): \ XOR the message with a random key as long as itself, \ used \textbf{once}",
                  font_size=22, color=WHITE),
            label(r"Shannon's definition \ (1949): \ $\Pr[M = m \mid C = c] = \Pr[M = m]$ \ for every $m$ and $c$",
                  font_size=22, color=YES),
            label(r"proof: \ each $c$ comes from each $m$ under exactly one key, \ $k = m \oplus c$: \ "
                  r"$\Pr[C = c \mid M = m] = 2^{-n}$, \ whatever $m$ is", font_size=22, color=HEAD),
            label(r"the ciphertext tells an attacker with \textbf{unlimited} computing nothing at all", font_size=22,
                  color=DATA),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Is there a cipher no amount of cleverness can break? <bookmark mark='a'/> In 1917 Gilbert Vernam, at "
            "AT and T, combined each bit of a teleprinter message with a bit of a random key tape: exclusive or. "
            "Here is HI, sixteen bits, a key, and the ciphertext. Use the key once, and never again. <bookmark "
            "mark='b'/> In 1949 Shannon made secrecy precise. A cipher is perfectly secret if seeing the ciphertext "
            "does not change the probability of any message: what an attacker believes afterwards is what they "
            "believed before. <bookmark mark='c'/> The pad meets it. For two bits, look at the table: each row, one "
            "message, contains every ciphertext exactly once. So any ciphertext comes from any message under exactly "
            "one key, and with a uniform key every ciphertext is equally likely whatever the message was. <bookmark "
            "mark='d'/> Not hard to break: impossible. No computer, no amount of time, no quantum machine helps."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(tags[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(tags[1]), FadeIn(lines[0]))
            self.play(FadeIn(rows[2]), FadeIn(tags[2]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(tl), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def theorem(self):
        head = label(r"The price: \ $|K| \ge |M|$", font_size=34).to_edge(UP, buff=0.3)
        cnode = Circle(radius=0.38, color=YES, stroke_width=3).move_to([-4.6, 0.6, 0])
        ctext = MathTex("c", font_size=34, color=YES).move_to(cnode)
        keys = VGroup(*[MathTex(rf"k_{i + 1}", font_size=28, color=HEAD) for i in range(3)])
        msgs = VGroup(*[MathTex(rf"m_{i + 1}", font_size=28, color=DATA) for i in range(4)])
        keys.arrange(DOWN, buff=0.7).move_to([-1.8, 0.6, 0])
        msgs.arrange(DOWN, buff=0.5).move_to([1.6, 0.6, 0])
        arr_k = VGroup(*[Arrow(cnode.get_right(), k.get_left(), buff=0.12, stroke_width=2, color=GREY_B) for k in keys])
        dest = [0, 2, 1]
        arr_m = VGroup(*[Arrow(k.get_right(), msgs[d].get_left(), buff=0.15, stroke_width=2.5, color=HEAD)
                         for k, d in zip(keys, dest)])
        miss = SurroundingRectangle(msgs[3], color=NO, buff=0.1)
        cap = label(r"decrypt $c$ \\ under every key", font_size=18, color=GREY_A).next_to(arr_k, UP, buff=0.25)
        notes = VGroup(
            label(r"fix any ciphertext $c$; \ decrypting it under all $|K|$ keys gives at most $|K|$ messages",
                  font_size=21, color=WHITE),
            label(r"if $|K| < |M|$, \ some message $m_4$ is never among them: \ $\Pr[M = m_4 \mid C = c] = 0$",
                  font_size=21, color=NO),
            label(r"but before seeing $c$, \ $\Pr[M = m_4] > 0$: \ seeing $c$ taught something. \ Not perfect.",
                  font_size=21, color=HEAD),
            label(r"so perfect secrecy needs as many keys as messages: \ a key as long as everything you will ever "
                  r"send", font_size=21, color=YES),
            label(r"moving that key securely is the original problem again", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Shannon also proved the catch, and the proof is three lines. <bookmark mark='a'/> Take any ciphertext, "
            "and decrypt it under every possible key. You get at most one message per key. <bookmark mark='b'/> If "
            "there are fewer keys than messages, some message is missing from that list: given this ciphertext, its "
            "probability is zero. <bookmark mark='c'/> But before the ciphertext arrived, it was possible. Seeing "
            "the ciphertext changed what the attacker believes, so the cipher is not perfectly secret. <bookmark "
            "mark='d'/> Perfect secrecy needs at least as many keys as messages, so a key as long as everything you "
            "will ever send. <bookmark mark='e'/> And that key must reach the other side in secret. If you have a "
            "secure way to send a key that long, you could have sent the message instead."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cnode), FadeIn(ctext), FadeIn(keys), FadeIn(msgs))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arr_k], lag_ratio=0.2), FadeIn(cap), FadeIn(notes[0]))
            self.play(LaggedStart(*[GrowArrow(a) for a in arr_m], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Create(miss), msgs[3].animate.set_color(NO), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def twotime(self):
        o = load("otp")
        head = label(r"Use the pad twice, \ and it breaks", font_size=34).to_edge(UP, buff=0.3)
        n = o["n"]
        dx = 0.33
        m1, m2 = o["m1"], o["m2"]

        def row(s, color):
            return VGroup(*[mono("_" if c == " " else c, 18, color).move_to([dx * i, 0, 0]) for i, c in
                            enumerate(s)])
        hid1 = VGroup(*[mono("?", 18, GREY_D).move_to([dx * i, 0, 0]) for i in range(n)])
        hid2 = hid1.copy()
        rows = VGroup(hid1, hid2).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=1.6).set_x(0.3)
        r1, r2 = row(m1, DATA).move_to(rows[0]), row(m2, HEAD).move_to(rows[1])
        t1 = label(r"$m_1$", font_size=20, color=DATA).next_to(rows[0], LEFT, buff=0.3)
        t2 = label(r"$m_2$", font_size=20, color=HEAD).next_to(rows[1], LEFT, buff=0.3)
        x = label(r"$c_1 \oplus c_2 = (m_1 \oplus k) \oplus (m_2 \oplus k) = m_1 \oplus m_2$: \ the key cancels",
                  font_size=24, color=YES).next_to(head, DOWN, buff=0.45)
        reveal = VGroup()
        for i, frag in o["hits"][:3]:
            crib = " THE "
            if m1[i:i + 5] == crib:
                a, b = r1[i:i + 5], r2[i:i + 5]
            else:
                a, b = r2[i:i + 5], r1[i:i + 5]
            reveal.add(VGroup(*a, *b))
        lines = VGroup(
            label(r"guess a common word \ (\texttt{\_THE\_}) \ in one message, \ slide it along $m_1 \oplus m_2$, "
                  r"\ and read the other message there", font_size=21, color=WHITE),
            label(r"where the result is plain English, \ the guess was right: \ offsets 4, \ 17, \ 22", font_size=21,
                  color=YES),
            label(r"VENONA \ (1943--1980): \ Soviet pads printed twice in 1942; \ US codebreakers read parts of "
                  r"about 3{,}000 messages", font_size=21, color=HEAD),
            label(r"the pad is perfect only if every key bit is random, \ secret, \ and used \textbf{once}",
                  font_size=21, color=NO),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "And the pad must be used once. <bookmark mark='a'/> Encrypt two messages with the same key, and an "
            "eavesdropper who XORs the two ciphertexts gets the XOR of the two messages: the key cancels out. "
            "<bookmark mark='b'/> That is not yet either message, but English is redundant. Guess a common word, "
            "space T H E space, at some position in one message; XOR it in, and you read what the other message "
            "says there. Slide it along. <bookmark mark='c'/> At three offsets the result is English: code, under, "
            "and bridge. Each hit reveals a piece of both messages, and each piece suggests the next guess. "
            "<bookmark mark='d'/> This happened. In 1942 a Soviet factory under wartime pressure printed some pad "
            "pages twice. American codebreakers in the VENONA project noticed, and over the following decades read "
            "parts of about three thousand messages, exposing atomic spies. <bookmark mark='e'/> The pad's perfection "
            "has three conditions, and every one is fragile: random, secret, once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows), FadeIn(t1), FadeIn(t2))
            vo.wait_until("a")
            self.play(FadeIn(x))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            for grp in reveal:
                olds = VGroup(*[hid1[r1.submobjects.index(m)] if m in r1.submobjects else hid2[r2.submobjects.index(m)]
                                for m in grp])
                self.play(FadeOut(olds), FadeIn(grp), run_time=0.8)
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
            vo.wait_until("e")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()
