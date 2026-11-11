from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono)


class Oracle(VoiceoverScene):
    def construct(self):
        self.card()
        self.padding()
        self.attack()

    def card(self):
        card = chapter_card(6, r"Bleichenbacher's oracle", r"Can one bit of feedback reveal a whole message?",
                            lit=(1998, 2017), extra=((1998, r"Bleichenbacher"), (2017, r"ROBOT")), part=PART)
        with self.voiceover("Chapter six. Bleichenbacher's oracle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def padding(self):
        head = label(r"PKCS \#1 v1.5, \ and a server that complains", font_size=34).to_edge(UP, buff=0.3)
        parts = [("00", GREY_B, 0.6), ("02", HEAD, 0.6), ("random nonzero bytes", GREY_A, 5.4), ("00", GREY_B, 0.6),
                 ("message", YES, 2.4)]
        boxes = VGroup()
        for t, c, w in parts:
            r = Rectangle(width=w, height=0.7, stroke_color=c, stroke_width=2, fill_color=BG, fill_opacity=1)
            boxes.add(VGroup(r, label(t, font_size=20, color=c).move_to(r)))
        boxes.arrange(RIGHT, buff=0).next_to(head, DOWN, buff=0.7)
        lines = VGroup(
            label(r"RSA encryption in TLS until 2018: \ pad the message like this, \ then $c = m^e \bmod n$",
                  font_size=22, color=WHITE),
            label(r"the server decrypts, \ and if the first two bytes aren't \texttt{00 02}, \ says so: \ an "
                  r"\textbf{oracle}", font_size=22, color=NO),
            label(r"RSA is malleable: \ send $c \cdot s^e$, \ and the server checks $m \cdot s$ instead", font_size=22,
                  color=HEAD),
            label(r"each `valid' answer means $2B \le m s \bmod n < 3B$, \ with $B = 2^{8(k-2)}$: \ a narrow window",
                  font_size=22, color=DATA),
            label(r"each window narrows the interval that must hold $m$; \ repeat until one number is left",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.22).next_to(boxes, DOWN, buff=0.6)
        with self.voiceover(
            "For twenty years, TLS used RSA to send the session key, with a padding format called PKCS one version "
            "one point five. <bookmark mark='a'/> The padded message starts with the bytes zero and two, then random "
            "nonzero bytes, a zero, and the message. <bookmark mark='b'/> A server decrypting a ciphertext checks "
            "this format, and early servers sent a different error when it was wrong. That is an oracle, like Part "
            "29's padding oracle. <bookmark mark='c'/> Combine it with malleability. Multiply the ciphertext by s to "
            "the e, and the server is checking m times s. <bookmark mark='d'/> Whenever it says the padding is valid, "
            "the attacker learns that m times s, modulo n, lies in a narrow window. <bookmark mark='e'/> Each answer "
            "cuts down the set of possible messages. Daniel Bleichenbacher showed in 1998 how to choose the s values "
            "so the set shrinks to a single number."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3), FadeIn(lines[0]))
            for mk, ln in zip("bcde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def attack(self):
        o = load("oracle")
        head = label(r"The interval, \ shrinking", font_size=34).to_edge(UP, buff=0.3)
        r0, r1 = o["runs"]
        ax = Axes(x_range=[0, 140000, 20000], y_range=[0, 400, 100], x_length=6.6, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.6).to_edge(
            LEFT, buff=1.0)
        cols = {256: DATA, 384: HEAD}
        curves = VGroup()
        for run in (r0, r1):
            pts = [ax.c2p(0, run["bits"] - 16)] + [ax.c2p(q, w) for q, w in run["trace"]]
            curves.add(VMobject(color=cols[run["bits"]], stroke_width=3).set_points_as_corners(pts))
        xt = VGroup(*[label(f"{x // 1000}k", font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (0, 40000, 80000, 120000)])
        yt = VGroup(*[label(str(y), font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (0, 100, 200, 300, 400)])
        xl = label(r"queries to the oracle", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yl = label(r"bits of uncertainty about $m$", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(
            ax, LEFT)
        keys = VGroup(*[label(rf"{r['bits']}-bit key", font_size=18, color=cols[r['bits']]) for r in (r0, r1)]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.c2p(80000, 150))
        notes = VGroup(
            label(rf"256-bit key: \\ {r0['queries']:,} queries, \ {r0['seconds']:.0f} s".replace(",", "{,}"),
                  font_size=20, color=DATA),
            label(rf"384-bit key: \\ {r1['queries']:,} queries, \ {r1['seconds']:.0f} s".replace(",", "{,}"),
                  font_size=20, color=HEAD),
            label(rf"recovered: \ \texttt{{{r0['recovered']}}}", font_size=20, color=YES),
            label(r"real keys: \ about a million \\ queries: \ ``the million-message \\ attack''", font_size=20,
                  color=WHITE),
            label(r"ROBOT \ (2017): \ still alive \\ on major websites", font_size=20, color=NO),
            label(r"TLS 1.3 dropped RSA key \\ transport entirely", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "We built a server that answers only valid or invalid, and ran the attack. <bookmark mark='a'/> The curve "
            "shows how many bits of uncertainty remain about the message. For a two-hundred-and-fifty-six-bit key it "
            "falls slowly while the attacker searches for the first valid s, then steeply, about a bit per query. "
            "<bookmark mark='b'/> Thirty-three thousand queries in all; for a three-hundred-and-eighty-four-bit key, a "
            "hundred and twenty-nine thousand. <bookmark mark='c'/> Out comes the message, with no key and no "
            "factoring. <bookmark mark='d'/> Against real key sizes the attack takes around a million queries, which "
            "gave it its name. <bookmark mark='e'/> Servers kept leaking the bit, through error messages and timing: "
            "in 2017 the ROBOT study found it still working against major websites. <bookmark mark='f'/> TLS 1.3 "
            "removed RSA key transport altogether, and uses only Diffie-Hellman."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(keys[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(curves[1]), FadeIn(keys[1]), FadeIn(notes[0]), FadeIn(notes[1]), run_time=2.0)
            for mk, n_ in zip("cdef", notes[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
