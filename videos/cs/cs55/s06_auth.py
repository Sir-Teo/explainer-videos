from __future__ import annotations

import hashlib
import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono

YEAR = 3.15e7          # seconds in a year, for reading guessing times


def say_time(s: float) -> str:
    """A guessing time as Tex: human_time below ten thousand years, a power of ten above."""
    yrs = s / YEAR
    if yrs >= 1e4:
        e = int(math.floor(math.log10(yrs)))
        return rf"${yrs / 10 ** e:.1f}\times10^{{{e}}}$ years"
    return human_time(s)


def lanes(names, xs, colors, top=2.35, bottom=-2.9, size=19):
    """The participants of a sequence diagram: a named box on top and a dashed lifeline down."""
    g = VGroup()
    for n, x, c in zip(names, xs, colors):
        box = RoundedRectangle(width=1.9, height=0.5, corner_radius=0.08, stroke_color=c, stroke_width=1.8,
                               fill_color=BG, fill_opacity=1).move_to([x, top, 0])
        t = label(n, font_size=size, color=c).move_to(box)
        if t.width > 1.75:
            t.width = 1.75
        life = DashedLine([x, top - 0.25, 0], [x, bottom, 0], color=GREY_D, stroke_width=1.5, dash_length=0.1)
        g.add(VGroup(box, t, life))
    return g


def message(x1, x2, y, tex, color, size=22, below=False):
    """One message of a sequence diagram: an arrow from x1 to x2 at height y, with its content above it."""
    a = Arrow([x1, y, 0], [x2, y, 0], buff=0.06, stroke_width=2.6, color=color, max_tip_length_to_length_ratio=0.07,
              max_stroke_width_to_length_ratio=8)
    t = MathTex(tex, font_size=size, color=color)
    t.next_to(a, DOWN if below else UP, buff=0.05)
    return VGroup(a, t)


def sha_prefix(s: str, n=10) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:n]


class Auth(VoiceoverScene):
    def construct(self):
        self.card()
        self.entropy()
        self.guessing()
        self.storage()
        self.codes()
        self.passkeys()
        self.lowe()

    def card(self):
        card = chapter_card(5, r"Who are you? \ Authentication", r"How can a machine tell that it is really you?",
                            lit=(1978, 1995, 2019), extra=((1978, r"Needham--Schroeder"), (1995, r"Lowe's attack"),
                                                           (2019, r"WebAuthn")), part=PART)
        with self.voiceover("Chapter five. Who are you? Authentication."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def entropy(self):
        tab = load("passwords")["table"]
        pick = [("digits", 6, r"6 digits"), ("lowercase", 8, r"8 lowercase letters"),
                ("alphanumeric", 8, r"8 letters and digits"), ("lowercase", 16, r"16 lowercase letters"),
                ("with symbols", 12, r"12 of all 95 printable")]
        rows = [next(r for r in tab if r["alphabet"] == a and r["length"] == n) | {"name": nm} for a, n, nm in pick]
        fast = "fast unsalted (1e10/s)"
        head = label(r"What a password is worth", font_size=36).to_edge(UP, buff=0.3)
        e1 = MathTex(r"\#\,\text{passwords}", r"=", r"N^{L}", font_size=42)
        e2 = MathTex(r"H", r"=", r"\log_2", r"N^{L}", font_size=42)
        e3 = MathTex(r"H", r"=", r"L", r"\log_2", r"N", font_size=42)
        e4 = MathTex(r"T", r"=", r"\frac{2^{H}}{2R}", font_size=42)
        for e in (e1, e2, e3, e4):
            e.move_to([0, 2.2, 0])
        whys = [label(r"$L$ symbols, \ each from an alphabet of $N$", font_size=20, color=GREY_A),
                label(r"entropy in bits: \ the log of the count", font_size=20, color=GREY_A),
                label(r"a log turns the power into a product", font_size=20, color=GREY_A),
                label(r"expected time: \ half the space, \ at $R$ guesses a second", font_size=20, color=GREY_A)]
        for w in whys:
            w.move_to([0, 1.5, 0])
        bars = VGroup()
        unit = 6.0 / 110
        for k, r in enumerate(rows):
            y = 0.8 - k * 0.68
            nm = label(r["name"], font_size=21, color=WHITE)
            nm.move_to([-4.6, y, 0]).align_to([-6.6, 0, 0], LEFT)
            b = Rectangle(width=r["entropy_bits"] * unit, height=0.42, stroke_width=0,
                          fill_color=NO if r["seconds"][fast] < 1e5 else YES, fill_opacity=0.8)
            b.move_to([-2.6, y, 0], aligned_edge=LEFT)
            bits = label(rf"{r['entropy_bits']:.0f} bits", font_size=17, color=BLACK).move_to(b)
            inside = bits.width <= b.width - 0.1
            if not inside:
                bits.set_color(WHITE).next_to(b, RIGHT, buff=0.1)
            tt = label(say_time(r["seconds"][fast]), font_size=21, color=HEAD)
            tt.next_to(bits if not inside else b, RIGHT, buff=0.2)
            bars.add(VGroup(nm, b, bits, tt))
        bars.set_x(0)
        cap = label(r"expected time to guess at $R = 10^{10}$ per second \ (a fast, \ unsalted hash)", font_size=18,
                    color=GREY_B).next_to(bars, DOWN, buff=0.35).set_x(0)
        with self.voiceover(
            "Start with the oldest answer: something you know. <bookmark mark='a'/> A password of L symbols, each "
            "from an alphabet of N, is one of N to the L. <bookmark mark='b'/> Its entropy in bits is the base-two "
            "logarithm of that count, <bookmark mark='c'/> which is L times log two of N. <bookmark mark='d'/> "
            "Testing R guesses a second, an attacker expects to search half the space: two to the H over two R. "
            "<bookmark mark='e'/> At ten billion guesses a second, a fast hash on one graphics card, eight lowercase "
            "letters last about ten seconds; sixteen last some seventy thousand years."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(e1), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(e1, e2), FadeTransform(whys[0], whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(e2, e3), FadeTransform(whys[1], whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(e3, e4), FadeTransform(whys[2], whys[3]))
            vo.wait_until("e")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(g[0]), GrowFromEdge(g[1], LEFT), FadeIn(g[2]), FadeIn(g[3]))
                                    for g in bars], lag_ratio=0.3), FadeIn(cap), run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def guessing(self):
        z = load("passwords")["zipf"]
        H = z["normaliser"]
        head = label(r"People do not choose at random", font_size=36).to_edge(UP, buff=0.3)
        base_y, hmax = -2.3, 3.6
        bars = VGroup()
        for k, r in enumerate(z["rows"]):
            x = -5.7 + k * 0.85
            h = r["share_cracked"] * hmax
            b = Rectangle(width=0.6, height=h, stroke_width=0, fill_color=NO, fill_opacity=0.8)
            b.move_to([x, base_y, 0], aligned_edge=DOWN)
            v = label(rf"{100 * r['share_cracked']:.0f}\%", font_size=18, color=NO).next_to(b, UP, buff=0.08)
            n = MathTex(rf"10^{{{k + 1}}}", font_size=24, color=GREY_A).next_to([x, base_y, 0], DOWN, buff=0.15)
            bars.add(VGroup(b, v, n))
        axis = Line([-6.2, base_y, 0], [-0.9, base_y, 0], color=GREY_C, stroke_width=1.5)
        xl = label(r"guesses, \ most popular first", font_size=17, color=GREY_A).next_to(axis, DOWN, buff=0.55)
        yl = label(r"share of users guessed", font_size=17, color=GREY_A).next_to(bars, UP, buff=0.25).set_x(-3.55)
        ill = label(rf"illustrative model: \ Zipf, \ $10^{{7}}$ distinct passwords \ (after Bonneau, \ 2012)",
                    font_size=16, color=GREY_B).next_to(xl, DOWN, buff=0.12).set_x(-3.55)
        rows = [MathTex(r"p_r", r"=", r"\frac{1}{r\,H_N}", font_size=31),
                MathTex(r"\text{share}(k)", r"=", r"\frac{H_k}{H_N}", font_size=31),
                MathTex(r"\text{share}(k)", r"\approx", r"\frac{\ln k + \gamma}{H_N}", font_size=31),
                MathTex(r"\text{share}(10k) - \text{share}(k)", r"\approx", r"\frac{\ln 10}{H_N}", font_size=31),
                MathTex(r"\frac{\ln 10}{H_N}", r"=", rf"\frac{{2.303}}{{{H:.2f}}}", r"=", rf"{math.log(10) / H:.3f}",
                        font_size=31)]
        whys = [r"the $r$-th most popular password; \ $H_N = \sum_{r \le N} 1/r$ normalises",
                r"the first $k$ guesses cover the $k$ most popular",
                r"a harmonic number is a logarithm, \ plus Euler's $\gamma$",
                r"so each tenfold more guesses adds the same slice",
                r"with our $N = 10^{7}$: \ about 14 points per decade"]
        ladder = VGroup()
        for r, w in zip(rows, whys):
            ladder.add(VGroup(r, wrapped_label(w, 5.6, font_size=18, color=GREY_A)).arrange(DOWN, buff=0.1))
        ladder.arrange(DOWN, buff=0.22)
        if ladder.height > 6.1:
            ladder.scale_to_fit_height(6.1)
        ladder.move_to([3.6, -0.4, 0])
        with self.voiceover(
            "But entropy assumes a random choice, and people do not choose at random. <bookmark mark='a'/> Large "
            "studies, Joseph Bonneau's in 2012 among them, found choices close to a Zipf law: the r-th most popular "
            "password is chosen with probability proportional to one over r. <bookmark mark='b'/> In our illustrative "
            "model of ten million passwords, ten guesses cover eighteen percent of users, and a million cover "
            "eighty-six. <bookmark mark='c'/> The share is a ratio of harmonic numbers, and a harmonic number is a "
            "logarithm, <bookmark mark='d'/> so every tenfold increase in guesses adds the same slice, about fourteen "
            "points."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(xl), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(ladder[0]), FadeIn(yl))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(g[0], DOWN), FadeIn(g[1]), FadeIn(g[2]))
                                    for g in bars], lag_ratio=0.3), run_time=3)
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(ladder[1][1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(ladder[2][1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(ladder[3][1]))
            self.play(TransformMatchingTex(rows[3].copy(), rows[4]), FadeIn(ladder[4][1]))
        self.wait(0.4)
        self.clear_scene()

    def storage(self):
        tab = load("passwords")["table"]
        r8 = next(r for r in tab if r["alphabet"] == "lowercase" and r["length"] == 8)
        fast, slow = r8["seconds"]["fast unsalted (1e10/s)"], r8["seconds"]["slow salted (10/s/core)"]
        head = label(r"Storing a password \ (Part 29)", font_size=36).to_edge(UP, buff=0.3)
        pw = "letmein1"
        same = sha_prefix(pw)
        t1 = grid_table([r"user", r"stored: \ $h(\text{pw})$"], [["alice", same + "..."], ["bob", same + "..."]],
                        widths=[1.6, 3.8], row_h=0.52, font_size=22, mono_cols=(0, 1))
        salts = ["q7Fz", "M2kd"]
        t2 = grid_table([r"user", r"salt", r"stored: \ $h(\text{salt}\,\|\,\text{pw})$"],
                        [["alice", salts[0], sha_prefix(salts[0] + pw) + "..."],
                         ["bob", salts[1], sha_prefix(salts[1] + pw) + "..."]],
                        widths=[1.6, 1.3, 3.8], row_h=0.52, font_size=22, mono_cols=(0, 1, 2))
        l1 = label(r"no salt: \ the same password, \ the same hash", font_size=21, color=NO)
        l2 = label(r"a random salt per user: \ every hash different", font_size=21, color=YES)
        left = VGroup(VGroup(l1, t1).arrange(DOWN, buff=0.2, aligned_edge=LEFT),
                      VGroup(l2, t2).arrange(DOWN, buff=0.2, aligned_edge=LEFT)).arrange(DOWN, buff=0.8,
                                                                                          aligned_edge=LEFT)
        left.next_to(head, DOWN, buff=0.6).to_edge(LEFT, buff=0.35)
        for r in (1, 2):
            t1.cells[r][1].set_color(NO)
            t2.cells[r][2].set_color(YES)
        ill = label(r"both users chose \texttt{letmein1} \ (illustrative); \ $h$ = SHA-256, \ first 10 hex digits",
                    font_size=16, color=GREY_B).next_to(left, DOWN, buff=0.35).align_to(left, LEFT)
        f1 = MathTex(r"T", r"=", r"\frac{2^{H}}{2R}", font_size=36)
        f2 = MathTex(r"\frac{T_{\text{slow}}}{T_{\text{fast}}}", r"=", r"\frac{R_{\text{fast}}}{R_{\text{slow}}}",
                     font_size=36)
        f3 = MathTex(r"\frac{T_{\text{slow}}}{T_{\text{fast}}}", r"=", r"\frac{10^{10}}{10}", r"=", r"10^{9}",
                     font_size=36)
        right = VGroup(f1, f2, f3).arrange(DOWN, buff=0.3).move_to([4.0, 1.25, 0])
        res = VGroup(
            VGroup(label(r"fast hash, \ $10^{10}$/s:", font_size=19, color=NO),
                   label(say_time(fast), font_size=19, color=NO)).arrange(RIGHT, buff=0.2),
            VGroup(label(r"slow hash, \ 10/s per core:", font_size=19, color=YES),
                   label(say_time(slow), font_size=19, color=YES)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(right, DOWN, buff=0.75)
        rl = label(r"8 lowercase letters, \ expected:", font_size=17, color=GREY_A).next_to(res, UP, buff=0.12)
        rl.align_to(res, LEFT)
        names = wrapped_label(r"bcrypt \ (1999), \ scrypt \ (2009), \ Argon2 \ (2015): \ a tunable cost, \ and "
                              r"for the last two a memory cost too", 5.4, font_size=20,
                              color=HEAD).next_to(res, DOWN, buff=0.4).set_x(4.0)
        with self.voiceover(
            "Assume the password file will be stolen, and make the theft buy little. <bookmark mark='a'/> Store only "
            "a hash. Unsalted, equal passwords give equal hashes, and one precomputed table cracks them all. "
            "<bookmark mark='b'/> A random salt per user makes every entry different, so each user must be attacked "
            "alone. <bookmark mark='c'/> Then make the hash slow on purpose: time is inversely proportional to rate, "
            "<bookmark mark='d'/> so going from ten billion guesses a second to ten is a factor of a billion: eight "
            "lowercase letters now take over three hundred years per core. <bookmark mark='e'/> These are Part 29's "
            "bcrypt, scrypt and Argon2, the last two also demanding memory."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left[0]))
            self.play(Indicate(t1.cells[1][1], color=NO), Indicate(t1.cells[2][1], color=NO))
            vo.wait_until("b")
            self.play(FadeIn(left[1]), FadeIn(ill))
            vo.wait_until("c")
            self.play(Write(f1))
            self.play(TransformMatchingTex(f1.copy(), f2))
            vo.wait_until("d")
            self.play(TransformMatchingTex(f2.copy(), f3))
            self.play(FadeIn(rl), FadeIn(res))
            vo.wait_until("e")
            self.play(FadeIn(names))
        self.wait(0.4)
        self.clear_scene()

    def codes(self):
        t = load("totp")
        sha1 = [r for r in t["totp"] if r["algorithm"] == "sha1"]
        hotp1 = next(r["hotp"] for r in t["hotp"] if r["counter"] == 1)
        head = label(r"One-time codes: \ an HMAC over the clock", font_size=36).to_edge(UP, buff=0.3)
        f1 = MathTex(r"C", r"=", r"\left\lfloor \frac{t - T_0}{X} \right\rfloor", font_size=34)
        f2 = MathTex(r"\text{code}", r"=", r"\text{Trunc}\big(\text{HMAC}_K(C)\big)", r"\bmod 10^{d}", font_size=34)
        VGroup(f1, f2).arrange(RIGHT, buff=0.9).next_to(head, DOWN, buff=0.35)
        steps = [(r"$t$", r"$t = 59$"), (r"$\lfloor (t - T_0)/30 \rfloor$", r"$C = 1$"),
                 (r"HMAC-SHA-1$(K, C)$", r"20 bytes"), (r"truncate", r"31-bit integer"),
                 (r"$\bmod 10^{8}$", rf"\texttt{{{sha1[0]['totp']}}}")]
        pipe, vals = VGroup(), VGroup()
        for s, v in steps:
            box = RoundedRectangle(width=2.15, height=0.6, corner_radius=0.08, stroke_color=KERN, stroke_width=1.6,
                                   fill_color=BG, fill_opacity=1)
            tt = label(s, font_size=18, color=WHITE).move_to(box)
            if tt.width > 2.0:
                tt.width = 2.0
            pipe.add(VGroup(box, tt))
            vals.add(label(v, font_size=18, color=HEAD))
        pipe.arrange(RIGHT, buff=0.42).next_to(VGroup(f1, f2), DOWN, buff=0.4)
        arrows = VGroup(*[Arrow(pipe[i].get_right(), pipe[i + 1].get_left(), buff=0.04, stroke_width=2,
                                color=GREY_B, max_tip_length_to_length_ratio=0.3) for i in range(len(pipe) - 1)])
        for v, p in zip(vals, pipe):
            v.next_to(p, DOWN, buff=0.15)
        rows = [[f"{r['time']:,}", f"{r['time'] // 30:,}", r["totp"]] for r in sha1]
        tab = grid_table([r"time $t$ (s)", r"counter $C$", r"code (8 digits)"], rows, widths=[2.6, 2.2, 2.2],
                         row_h=0.42, font_size=19, mono_cols=(0, 1, 2))
        tab.next_to(vals, DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        for r in range(1, len(rows) + 1):
            tab.cells[r][2].set_color(YES)
        tl = label(r"RFC 6238's SHA-1 test values: \ ours match all six", font_size=17,
                   color=YES).next_to(tab, DOWN, buff=0.12).align_to(tab, LEFT)
        notes = VGroup(
            wrapped_label(rf"HOTP \ (RFC 4226, \ 2005) \ at counter 1: \ \texttt{{{hotp1}}} \ --- \ the last six "
                          rf"digits of the code at $t = 59$: \ the same HMAC, \ the same counter", 5.2, font_size=18,
                          color=LAM),
            wrapped_label(r"still a secret you type: \ a look-alike login page can relay it within its 30 seconds",
                          5.2, font_size=18, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, RIGHT, buff=0.6).align_to(tab, UP)
        with self.voiceover(
            "A second factor proves something you have. <bookmark mark='a'/> Authenticator codes follow RFC 6238, "
            "from 2011. Phone and server share a key, and each divides the time by thirty seconds, rounding down, to "
            "get a counter. <bookmark mark='b'/> Each takes an HMAC of the counter, cuts four bytes from it where the "
            "hash itself points, and keeps the last six or eight digits. <bookmark mark='c'/> Ours reproduces the "
            "standard's test values exactly. <bookmark mark='d'/> At fifty-nine seconds the counter is one, and the "
            "code ends in the same six digits as the older counter-based code at counter one: the same computation. "
            "<bookmark mark='e'/> But it is still typed, so a fake page can relay it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(pipe[:2]), GrowArrow(arrows[0]))
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(pipe[2:]), *[GrowArrow(a) for a in arrows[1:]])
            self.play(LaggedStart(*[FadeIn(v, shift=DOWN * 0.1) for v in vals], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(tl))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]), Indicate(vals[-1], color=LAM))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def passkeys(self):
        head = label(r"Passkeys: \ a signature bound to the site \ (Part 30)", font_size=36).to_edge(UP, buff=0.3)
        xs = [-5.4, -2.4, 0.6]
        ln = lanes([r"device", r"browser", r"bank.example"], xs, [YES, DATA, KERN], top=2.3, bottom=-2.0)
        m = [message(xs[2], xs[1], 1.45, r"c \;(\text{random})", KERN),
             message(xs[1], xs[0], 0.65, r"c,\ \text{origin}", DATA),
             message(xs[0], xs[1], -0.15, r"\sigma = \text{Sign}_{sk}(c,\ \text{origin})", YES, size=20),
             message(xs[1], xs[2], -0.95, r"\sigma", YES)]
        ok = label(r"verify $\sigma$ with $pk$: \ \checkmark", font_size=19, color=YES)
        ok.next_to([xs[2], -1.45, 0], LEFT, buff=0.15)
        reg = label(r"at sign-up: \ a key pair for this site; \ the server keeps only $pk$", font_size=19,
                    color=GREY_A).move_to([-2.4, -2.5, 0])
        notes = VGroup(
            wrapped_label(r"nothing secret is typed, \ and the server stores nothing that logs anyone in", 4.3,
                          font_size=19, color=WHITE),
            wrapped_label(r"the browser writes the origin it really talks to: \ a look-alike site gets a signature "
                          r"over the wrong origin, \ or none at all", 4.3, font_size=19, color=YES),
            wrapped_label(r"schematic, \ after WebAuthn \ (W3C Recommendation, \ 2019)", 4.3, font_size=16,
                          color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.6, -0.2, 0])
        with self.voiceover(
            "Passkeys drop the shared secret, using Part 30's signatures. <bookmark mark='a'/> At sign-up the device "
            "makes a key pair for this one site and gives the server only the public half. <bookmark mark='b'/> To "
            "log in, the server sends a random challenge, the browser adds the origin it is really talking to, and "
            "the device signs both. <bookmark mark='c'/> The server checks the signature. Nothing secret is typed, "
            "and a stolen database logs no one in. <bookmark mark='d'/> A look-alike site gets a signature over the "
            "wrong origin, or none. This is WebAuthn, a W3C Recommendation since 2019."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ln))
            vo.wait_until("a")
            self.play(FadeIn(reg))
            vo.wait_until("b")
            for g in m[:3]:
                self.play(GrowArrow(g[0]), FadeIn(g[1]), run_time=0.8)
            vo.wait_until("c")
            self.play(GrowArrow(m[3][0]), FadeIn(m[3][1]), run_time=0.8)
            self.play(FadeIn(ok), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def lowe(self):
        ns = load("ns")
        fl, fx = ns["flawed"], ns["fixed"]
        head = label(r"Needham--Schroeder \ (1978), \ and Lowe's attack \ (1995)", font_size=36).to_edge(UP, buff=0.3)
        xs = [-5.6, -3.1, -0.6]
        ln = lanes([r"Alice", r"Intruder", r"Bob"], xs, [DATA, NO, LAM], top=2.45, bottom=-1.6)
        ys = [1.75, 1.15, 0.55, -0.05, -0.65, -1.25]
        m = [message(xs[0], xs[1], ys[0], r"\{N_a,\, A\}_{I}", DATA),
             message(xs[1], xs[2], ys[1], r"\{N_a,\, A\}_{B}", NO),
             message(xs[2], xs[1], ys[2], r"\{N_a,\, N_b\}_{A}", LAM),
             message(xs[1], xs[0], ys[3], r"\{N_a,\, N_b\}_{A}", NO),
             message(xs[0], xs[1], ys[4], r"\{N_b\}_{I}", DATA),
             message(xs[1], xs[2], ys[5], r"\{N_b\}_{B}", NO)]
        key = label(r"$\{m\}_X$: \ $m$ sealed with $X$'s public key", font_size=16,
                    color=GREY_B).move_to([-3.1, -2.1, 0])
        res = label(r"Bob believes he spoke to Alice; \ the intruder knows $N_b$", font_size=18,
                    color=NO).move_to([-3.1, -2.55, 0])
        fixm = MathTex(r"\{N_a,\, N_b", r"\}_{A}", font_size=24, color=YES)
        fixm2 = MathTex(r"\{N_a,\, N_b", r",\, B", r"\}_{A}", font_size=24, color=YES)
        fixm2[1].set_color(HEAD)
        found = "found" if fl["attack_found"] else "none"
        none = "none" if not fx["attack_found"] else "found"
        rows = [[r"original", f"{fl['states_explored']}", found, f"{len(fl['trace'])} steps"],
                [r"Lowe's fix", f"{fx['states_explored']}", none, r"---"]]
        tab = grid_table([r"protocol", r"states", r"attack", r"trace"], rows, widths=[1.7, 1.0, 1.0, 1.1],
                         row_h=0.42, font_size=18, mono_cols=())
        tab.cells[1][2].set_color(NO)
        tab.cells[2][2].set_color(YES)
        notes = VGroup(
            wrapped_label(r"our model checker \ (Part 54): \ breadth-first over every interleaving, \ against an "
                          r"intruder that owns the network \ (Dolev--Yao)", 4.9, font_size=18, color=WHITE),
            tab,
            wrapped_label(r"the fix: \ Bob names himself inside message 2", 4.9, font_size=18, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.15, 0.2, 0])
        fixm2.next_to(notes[2], DOWN, buff=0.15).align_to(notes[2], LEFT)
        fixm.move_to(fixm2, aligned_edge=LEFT)
        with self.voiceover(
            "Across a network, logging in is a protocol. <bookmark mark='a'/> In 1978 Roger Needham and Michael "
            "Schroeder proposed this one: Alice sends Bob a nonce and her name, sealed for Bob; he returns her nonce "
            "with one of his own; she returns his. <bookmark mark='b'/> In 1995 Gavin Lowe ran it through a model "
            "checker. Alice opens an honest session with the intruder, who re-seals her message for Bob. Bob's reply "
            "is sealed for Alice, so the intruder forwards it unread, and Alice returns Bob's nonce, to the intruder. "
            "<bookmark mark='c'/> Bob believes he is talking to Alice, and the intruder holds his secret. <bookmark "
            "mark='d'/> Our checker from Part 54 finds the same attack among nineteen states. <bookmark mark='e'/> "
            "Lowe's fix is a single name: Bob puts his own in the reply, and no attack remains."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ln), FadeIn(key))
            vo.wait_until("a")
            self.play(Indicate(ln[0][0], color=DATA), Indicate(ln[2][0], color=LAM))
            vo.wait_until("b")
            for g in m[:5]:
                self.play(GrowArrow(g[0]), FadeIn(g[1]), run_time=0.9)
            vo.wait_until("c")
            self.play(GrowArrow(m[5][0]), FadeIn(m[5][1]), run_time=0.9)
            self.play(FadeIn(res), Indicate(m[5][1], color=NO))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]), FadeIn(tab.cells[0][0]), *[FadeIn(c) for c in tab.cells[0][1:]],
                      FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[1]])
            vo.wait_until("e")
            self.play(FadeIn(notes[2]), FadeIn(fixm))
            self.play(TransformMatchingTex(fixm, fixm2), *[FadeIn(c) for c in tab.cells[2]])
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES, PART, mono)
