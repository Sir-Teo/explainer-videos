from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono)


class DiscreteLogs(VoiceoverScene):
    def construct(self):
        self.card()
        self.bsgs()
        self.pohlig()
        self.index()

    def card(self):
        card = chapter_card(8, r"Discrete logarithms", r"How hard is it to undo $g^x$?", lit=(1971, 1978, 2015),
                            extra=((1971, r"Shanks: \ baby-step giant-step"), (1978, r"Pohlig--Hellman; \ rho"),
                                   (2015, r"Logjam")), part=PART)
        with self.voiceover("Chapter eight. Discrete logarithms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def bsgs(self):
        d = load("dlog")
        head = label(r"Baby steps, \ giant steps", font_size=34).to_edge(UP, buff=0.3)
        m = 6
        baby = VGroup(*[VGroup(Square(side_length=0.6, stroke_color=DATA, fill_color=DATA, fill_opacity=0.2),
                               ).add(label(rf"$g^{{{j}}}$", font_size=18).move_to([0, 0, 0])) for j in range(m)])
        for j, b in enumerate(baby):
            b[1].move_to(b[0])
        baby.arrange(RIGHT, buff=0.08).next_to(head, DOWN, buff=0.7).to_edge(LEFT, buff=1.0)
        bl = label(r"baby steps: \ a table of $g^0 \ldots g^{m-1}$", font_size=19, color=DATA).next_to(baby, UP,
                                                                                                   buff=0.15)
        giant = VGroup(*[label(t, font_size=20, color=HEAD) for t in
                         (r"$h$", r"$h g^{-m}$", r"$h g^{-2m}$", r"$h g^{-3m}$")]).arrange(RIGHT, buff=0.7)
        giant.next_to(baby, DOWN, buff=0.9).align_to(baby, LEFT)
        gl = label(r"giant steps: \ until one lands in the table", font_size=19, color=HEAD).next_to(giant, DOWN,
                                                                                                buff=0.15)
        hit = SurroundingRectangle(giant[3], color=YES, buff=0.08)
        hl = label(r"$h g^{-3m} = g^{j}$ \ $\Rightarrow$ \ $x = 3m + j$", font_size=22, color=YES).next_to(gl, DOWN,
                                                                                                      buff=0.3)
        rows = d["rows"]
        ax = Axes(x_range=[22, 42, 4], y_range=[0, 4, 1], x_length=4.4, y_length=2.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(RIGHT, buff=0.8).shift(UP * 0.4)
        lg = lambda s: math.log10(s) + 4     # noqa: E731
        line = VMobject(color=HEAD, stroke_width=3).set_points_as_corners([ax.c2p(r["bits"], lg(r["seconds"]))
                                                                           for r in rows])
        dts = VGroup(*[Dot(ax.c2p(r["bits"], lg(r["seconds"])), radius=0.05, color=HEAD) for r in rows])
        xt = VGroup(*[label(str(x), font_size=14, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (24, 32, 40)])
        yt = VGroup(*[label(t, font_size=14, color=GREY_A).next_to(ax.c2p(22, y), LEFT, buff=0.08)
                      for y, t in ((1, "1 ms"), (3, "0.1 s"))])
        axl = label(r"bits of $p$; \ time \ (ours)", font_size=16, color=GREY_A).next_to(ax, DOWN, buff=0.4)
        note = label(r"$m = \lceil\sqrt{n}\rceil$: \ about $2\sqrt{n}$ work and $\sqrt{n}$ memory: \ every 2 bits of $p$ "
                     r"double the time", font_size=21, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Chapter three left a question: how fast can g to the x be undone? Trying every x takes p steps. Daniel "
            "Shanks found a square root in 1971. <bookmark mark='a'/> Write the unknown x as i times m plus j, with m "
            "about the square root of p. First take baby steps: store g to the j for every j below m. <bookmark "
            "mark='b'/> Then take giant steps from the target: h, h divided by g to the m, by g to the two m, and so "
            "on, looking each one up in the table. <bookmark mark='c'/> When one matches, x is read off. About two "
            "square roots of p operations, and a square root's worth of memory. <bookmark mark='d'/> Our runs: each "
            "four more bits of p multiply the time by about five, close to the four a square root predicts. Pollard's rho does the same "
            "with almost no memory."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in baby], lag_ratio=0.2), FadeIn(bl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g_) for g_ in giant], lag_ratio=0.4), FadeIn(gl))
            vo.wait_until("c")
            self.play(Create(hit), FadeIn(hl), FadeIn(note))
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(axl), Create(line), FadeIn(dts))
        self.wait(0.3)
        self.clear_scene()

    def pohlig(self):
        d = load("dlog")
        head = label(r"Pohlig--Hellman: \ the shape of $p - 1$ matters", font_size=34).to_edge(UP, buff=0.3)
        fac = r" \cdot ".join(sorted(d["smooth_factors"], key=int))
        lines = VGroup(
            label(r"a discrete log mod $p$ splits into one log per prime factor of $p - 1$ \ (and the CRT puts them "
                  r"together)", font_size=22, color=WHITE),
            label(rf"a {d['smooth_bits']}-bit prime with $p - 1 = {fac}$", font_size=22, color=NO),
            label(rf"largest factor 109: \ the whole log in {d['ph_seconds'] * 1000:.1f} ms \ "
                  rf"({'correct' if d['ph_ok'] else 'wrong'})", font_size=22, color=NO),
            label(rf"a \textbf{{safe prime}} \ $p = 2q + 1$, \ $q$ prime \ ({d['safe_bits']} bits): \ no shortcut, \ "
                  r"the full $\sqrt{q}$", font_size=22, color=YES),
            label(r"so Diffie--Hellman groups use safe primes, \ or a prime-order subgroup \ (the DDH condition again)",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "The square root is of the group's order, and the order's structure matters. <bookmark mark='a'/> Stephen "
            "Pohlig and Martin Hellman showed in 1978 that a discrete logarithm splits into one smaller logarithm for "
            "each prime factor of p minus one, glued back together by the Chinese remainder theorem. <bookmark "
            "mark='b'/> Here is an eighty-four-bit prime whose p minus one is a product of small primes. <bookmark "
            "mark='c'/> The largest is a hundred and nine, so every piece is tiny, and the whole logarithm takes under "
            "a millisecond. <bookmark mark='d'/> A safe prime is twice a prime plus one. Then p minus one has a huge "
            "prime factor, and nothing beats the full square root. <bookmark mark='e'/> So Diffie-Hellman groups are "
            "built from safe primes, or work in a subgroup of large prime order."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def index(self):
        d = load("dlog")
        head = label(r"Index calculus, \ and Logjam", font_size=34).to_edge(UP, buff=0.3)
        tries = f"{d['ic_tries']:,}".replace(",", "{,}")
        lines = VGroup(
            label(r"in $Z_p^*$, \ numbers \textbf{factor}: \ if $g^k = 2^a 3^b 5^c \cdots$, \ then $k \equiv a \log 2 "
                  r"+ b \log 3 + \cdots \pmod{p-1}$", font_size=22, color=WHITE),
            label(rf"collect enough smooth powers, \ solve the linear system: \ logs of all small primes \ "
                  rf"(ours: \ {d['ic_base']} primes, \ {d['ic_relations']} relations from {tries} tries)",
                  font_size=22, color=DATA),
            label(rf"then one smooth $h g^s$ gives $\log h$: \ ours, \ for a 30-bit $p$, \ in {d['ic_seconds']:.2f} s, "
                  rf"\ {'correct' if d['ic_ok'] else 'wrong'}", font_size=22, color=YES),
            label(r"sub-exponential, \ like the sieves: \ finite-field Diffie--Hellman needs 2048-bit primes", font_size=22,
                  color=HEAD),
            label(r"the expensive part depends only on $p$: \ precompute once, \ then break every exchange that uses it",
                  font_size=22, color=NO),
            label(r"Logjam \ (2015): \ 512-bit `export' groups broken in minutes; \ a few shared 1024-bit primes in "
                  r"reach of a nation", font_size=22, color=NO),
            label(r"elliptic curves have no `small primes' to factor into: \ only rho works \ (next chapter)",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "For the numbers modulo p there is something better than square roots, because numbers can be factored. "
            "<bookmark mark='a'/> If some power of g happens to factor into small primes, its exponent is a linear "
            "combination of the logarithms of those primes. <bookmark mark='b'/> Collect enough such smooth powers and "
            "solve the linear system, and you know the logarithm of every small prime. <bookmark mark='c'/> Then "
            "multiply the target by random powers of g until the product is smooth, and its logarithm falls out. Ours "
            "works on a thirty-bit prime in a tenth of a second. <bookmark mark='d'/> Index calculus is "
            "sub-exponential, like the sieves, which is why Diffie-Hellman over integers needs primes of two thousand "
            "bits. <bookmark mark='e'/> Worse, the expensive first stage depends only on the prime, not on the "
            "exchange. <bookmark mark='f'/> In 2015 the Logjam researchers showed that servers still accepting old "
            "five-hundred-and-twelve-bit export groups could be broken in minutes after one precomputation, and that a "
            "handful of shared thousand-bit primes were within reach of a national agency. <bookmark mark='g'/> "
            "Elliptic curve points cannot be factored into small pieces. There, only the generic square-root attacks "
            "are known."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
