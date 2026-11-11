from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (BG, DATA, HEAD, LAM, NO, PART, YES, code, load, mono)


class SideChannels(VoiceoverScene):
    def construct(self):
        self.card()
        self.timing()
        self.caches()
        self.randomness()

    def card(self):
        card = chapter_card(15, r"Side channels and bad randomness", r"What leaks besides the ciphertext?",
                            lit=(1996, 2008), extra=((1996, r"Kocher: \ timing attacks"), (1999, r"power analysis"),
                                                     (2005, r"cache attacks on AES"), (2008, r"Debian's OpenSSL")),
                            part=PART)
        with self.voiceover("Chapter fifteen. Side channels, and bad randomness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def timing(self):
        t = load("timing")["rows"]
        head = label(r"A comparison that leaks", font_size=34).to_edge(UP, buff=0.3)
        early = code(["def equal(a, b):", "    for x, y in zip(a, b):", "        if x != y:",
                      "            return False", "    return True"], size=17)
        const = code(["def equal(a, b):", "    d = 0", "    for x, y in zip(a, b):", "        d |= x ^ y",
                      "    return d == 0"], size=17)
        el = label(r"early exit", font_size=19, color=NO)
        cl = label(r"fixed-work Python loop", font_size=19, color=YES)
        codes = VGroup(VGroup(el, early).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
                       VGroup(cl, const).arrange(DOWN, aligned_edge=LEFT, buff=0.12)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        ymax = max(800, math.ceil(max(max(r["early_ns"], r["constant_ns"]) for r in t) / 200) * 200)
        ax = Axes(x_range=[0, 16, 4], y_range=[0, ymax, ymax / 4], x_length=5.0, y_length=3.2,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(codes, RIGHT, buff=1.2).align_to(
            codes, UP).shift(DOWN * 0.3)
        e = VMobject(color=NO, stroke_width=3).set_points_as_corners([ax.c2p(r["correct"], r["early_ns"]) for r in t])
        c = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(r["correct"], r["constant_ns"])
                                                                        for r in t])
        ed = VGroup(*[Dot(ax.c2p(r["correct"], r["early_ns"]), radius=0.05, color=NO) for r in t])
        cd = VGroup(*[Dot(ax.c2p(r["correct"], r["constant_ns"]), radius=0.05, color=YES) for r in t])
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (0, 4, 8, 12, 16)])
        yt = VGroup(*[label(str(y), font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (0, ymax / 2, ymax)])
        xl = label(r"correct leading bytes in the guess", font_size=16, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"nanoseconds per comparison", font_size=16, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(
            ax, LEFT)
        slope = (t[-1]["early_ns"] - t[0]["early_ns"]) / 16
        lines = VGroup(
            label(rf"measured average prefix slope: \ {slope:.0f} ns/byte; \\ timing can expose correct prefixes",
                  font_size=20, color=NO),
            label(r"with reliable timing: \ about $16 \times 256$ candidates; \\ repeated measurements may be needed", font_size=20,
                  color=HEAD),
            label(r"Kocher \ (1996): \ timing recovered RSA and Diffie--Hellman keys; \ use "
                  r"\texttt{hmac.compare\_digest}", font_size=20, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Everything so far attacked the mathematics. Real systems also leak through how long they take, how "
            "much power they draw, what they leave in the cache. <bookmark mark='a'/> Here is the obvious way to "
            "check a MAC tag: compare byte by byte, and stop at the first difference. <bookmark mark='b'/> We timed "
            "it against guesses with more correct leading bytes. The measured times depend on this machine and "
            "Python runtime. <bookmark mark='c'/> If an attacker can distinguish prefix lengths reliably, it can "
            "guess one byte at a time: roughly sixteen times two hundred and fifty-six candidate guesses. Real "
            "timing attacks generally require repeated measurements and statistical analysis, not one query per "
            "guess. <bookmark mark='d'/> The second loop visits every pair of bytes, ORs the XORs, and decides at "
            "the end. This illustrates removing early exit; Python does not guarantee its running time is "
            "independent of secrets. Kocher's 1996 work demonstrated timing attacks on RSA and Diffie-Hellman. "
            "For tag comparisons use the standard hmac.compare_digest implementation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(codes[0]))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            self.play(Create(e), FadeIn(ed), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(codes[1]), Create(c), FadeIn(cd), FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def caches(self):
        head = label(r"Table lookups leave footprints", font_size=34).to_edge(UP, buff=0.3)
        lines_ = VGroup()
        hot = 0xA
        for i in range(16):
            r = Rectangle(width=0.62, height=1.3, stroke_color=GREY_B, stroke_width=1.2,
                          fill_color=NO if i == hot else BG, fill_opacity=0.6 if i == hot else 1)
            lines_.add(VGroup(r, mono(f"{i:X}", 15, WHITE).move_to(r)))
        lines_.arrange(RIGHT, buff=0.05).next_to(head, DOWN, buff=1.2)
        tl = label(r"a 1 KB AES table \ (``T-table''): \ 16 cache lines of 64 bytes \ (Part 9)", font_size=19,
                   color=GREY_A).next_to(lines_, UP, buff=0.2)
        idx = MathTex(r"T[\,p_0 \oplus k_0\,]", font_size=36, color=HEAD).next_to(lines_, DOWN, buff=0.5)
        arr = Arrow(idx.get_top(), lines_[hot].get_bottom(), buff=0.1, color=NO, stroke_width=3)
        notes = VGroup(
            label(r"fast AES software looks up tables indexed by plaintext $\oplus$ key bytes", font_size=21,
                  color=WHITE),
            label(r"another process on the same core times its own memory: \ the line AES touched is now cached",
                  font_size=21, color=NO),
            label(r"which line \ = \ the top 4 bits of $p_0 \oplus k_0$: \ with known $p_0$, \ half of each key byte",
                  font_size=21, color=HEAD),
            label(r"Bernstein \ (2005), \ Osvik, \ Shamir and Tromer \ (2006): \ full AES keys, \ across processes",
                  font_size=21, color=NO),
            label(r"fixes: \ AES instructions in hardware, \ or bitsliced code with no secret-dependent addresses",
                  font_size=21, color=YES),
            label(r"power and EM analysis \ (Kocher et al., 1999): \ smart cards read through their power supply",
                  font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Timing leaks through memory too. <bookmark mark='a'/> Fast software AES replaces the S-box and "
            "MixColumns with lookups in four tables of a kilobyte each, indexed by bytes of the plaintext XORed "
            "with the key. A kilobyte is sixteen cache lines, Part 9's unit. <bookmark mark='b'/> An attacker "
            "running on the same machine fills the cache with its own data, lets AES run, then times its own "
            "accesses: the line AES used is now slow for the attacker, because AES evicted it. <bookmark mark='c'/> "
            "Which line was used reveals the top four bits of the plaintext byte XOR the key byte. With known "
            "plaintexts, that is half of every key byte, and later rounds give the rest. <bookmark mark='d'/> Daniel "
            "Bernstein, and then Dag Arne Osvik, Adi Shamir and Eran Tromer, recovered full AES keys this way across "
            "process boundaries in 2005 and 2006, the same mechanism Spectre would exploit in 2018. <bookmark "
            "mark='e'/> The fixes: hardware AES instructions, or bitsliced code that touches the same addresses "
            "whatever the key. <bookmark mark='f'/> And power analysis reads keys from smart cards through their "
            "power consumption, one trace at a time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines_), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(idx), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(notes[1]))
            for mk, n_ in zip("cdef", notes[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def randomness(self):
        d = load("debian")
        head = label(r"Keys from bad randomness", font_size=34).to_edge(UP, buff=0.3)
        n = 64
        cells = VGroup(*[Square(side_length=0.16, stroke_width=0, fill_color=GREY_D, fill_opacity=1)
                         for _ in range(n * 16)]).arrange_in_grid(rows=16, cols=n, buff=0.03)
        cells.next_to(head, DOWN, buff=0.5)
        frac = d["found"] / d["space"]
        k = int(frac * len(cells))
        found = cells[k].copy().set_fill(YES, 1).scale(1.6)
        cap = label(rf"all {d['space']:,} possible process IDs \ (each square: \ 32 of them)".replace(",", "{,}"),
                    font_size=18, color=GREY_A).next_to(cells, DOWN, buff=0.15)
        lines = VGroup(
            label(r"Debian, \ 2006--2008: \ a line removed from OpenSSL left the process ID as the \textbf{only} "
                  r"randomness", font_size=21, color=WHITE),
            label(r"so every key generated on Debian and Ubuntu came from a list of 32{,}767 per key type: \ SSH keys, "
                  r"\ TLS certificates", font_size=21, color=NO),
            label(rf"our toy: \ a {d['key_bits']}-bit AES key seeded by PID {d['pid']}: \ found after "
                  rf"{d['tried']:,} tries, \ {d['seconds']:.0f} seconds".replace(",", "{,}"), font_size=21,
                  color=YES),
            label(r"Dual\_EC\_DRBG \ (NIST, 2006--2014): \ a generator whose constants could hide a back door", font_size=21,
                  color=HEAD),
            label(r"use the operating system's generator: \ \texttt{os.urandom}, \ \texttt{secrets}, \ "
                  r"\texttt{getrandom()}", font_size=21, color=DATA),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The last failure is the most basic: the key was never random. <bookmark mark='a'/> In 2006 a Debian "
            "maintainer, silencing a warning from a memory-checking tool, removed a line from OpenSSL that mixed "
            "entropy into its random number generator. What remained was the process ID: at most thirty-two "
            "thousand seven hundred and sixty-seven values. <bookmark mark='b'/> For two years, every SSH key and "
            "certificate generated on Debian and Ubuntu came from a short list, and attackers simply generated the "
            "whole list. <bookmark mark='c'/> Here is the same mistake in miniature: a hundred-and-twenty-eight-bit "
            "AES key, seeded from a process ID. We tried every ID in turn, and found the key after twenty-three "
            "thousand tries. The measured runtime is displayed. A hundred and twenty-eight bits of key, fifteen bits of randomness. "
            "<bookmark mark='d'/> And randomness can be sabotaged deliberately. Dual EC DRBG, a generator "
            "standardised in 2006, used two elliptic-curve constants of unexplained origin; whoever knew the "
            "relation between them could predict its output. It was withdrawn in 2014. <bookmark mark='e'/> The "
            "rule: take random numbers from the operating system's generator, which collects real entropy and runs "
            "it through a cipher like ChaCha20, and nowhere else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[c.animate.set_fill(GREY_B, 1) for c in cells[:k]], lag_ratio=0.002),
                      run_time=2.5)
            self.play(FadeIn(found, scale=2), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()
