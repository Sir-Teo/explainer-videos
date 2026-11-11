from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, num)


class Phy(VoiceoverScene):
    def construct(self):
        self.card()
        self.shannon()
        self.qam()
        self.gap()
        self.light()

    def card(self):
        card = chapter_card(3, r"Bits on a wire", r"How many bits can a channel carry?", lit=(1928, 1948),
                            extra=((1928, r"Nyquist"), (1948, r"Shannon: \ channel capacity")), part=PART)
        with self.voiceover("Chapter three. Bits on a wire."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def shannon(self):
        p = load("phy")
        head = label(r"Two limits", font_size=36).to_edge(UP, buff=0.3)
        ny = MathTex(r"\text{symbols per second} \le 2B", font_size=36, color=DATA)
        sh = MathTex(r"C = B \log_2\!\left(1 + \frac{S}{N}\right)", font_size=44, color=HEAD)
        VGroup(ny, sh).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.45)
        rows = []
        for c in p["channels"]:
            C = c["C"]
            cs = f"{C / 1e6:.0f} Mb/s" if C > 1e6 else f"{C / 1e3:.0f} kb/s"
            B = c["B"]
            bs = f"{B / 1e6:.0f} MHz" if B >= 1e6 else f"{B / 1e3:.1f} kHz"
            rows.append([c["name"], bs, rf"{c['snr_db']} dB", cs])
        tab = grid_table([r"channel", r"bandwidth $B$", r"$S/N$", r"capacity $C$"], rows,
                         widths=[3.8, 2.2, 1.4, 2.2], row_h=0.42, font_size=19, mono_cols=())
        tab.next_to(sh, DOWN, buff=0.5).set_x(0)
        for r in range(1, 4):
            tab.cells[r][3].set_color(YES)
        lines = VGroup(
            label(r"Nyquist \ (1928): \ a channel of bandwidth $B$ hertz carries at most $2B$ independent pulses a "
                  r"second", font_size=19, color=DATA),
            label(r"Shannon \ (1948): \ with noise, \ at most $C$ bits a second \textit{can} be sent with as few "
                  r"errors as you like; \ above $C$, \ none can", font_size=19, color=HEAD),
            label(r"a dial-up modem reached 33.6 kb/s on a 36 kb/s line: \ the limit is real, \ and engineering "
                  r"reaches it", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "The physical layer turns bits into a signal: a voltage on copper, light in glass, a radio wave. Two "
            "results bound what it can do. <bookmark mark='a'/> Harry Nyquist showed in 1928 that a channel of "
            "bandwidth B can carry at most two B independent pulses each second. <bookmark mark='b'/> And Claude "
            "Shannon showed in 1948, the theorem we met in Part 28, that with noise the capacity is B times the "
            "logarithm of one plus the signal-to-noise ratio. Below that rate, coding can make errors as rare as you "
            "like. Above it, nothing can. <bookmark mark='c'/> For a telephone line, thirty-six kilobits a second; "
            "for an eighty-megahertz Wi-Fi channel, eight hundred megabits; <bookmark mark='d'/> and the last dial-up "
            "modems reached thirty-three point six kilobits on such a line. The bound is not just theory: "
            "engineering gets close to it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ny), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(sh), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def qam(self):
        p = load("phy")
        head = label(r"QAM: \ bits as points in a plane", font_size=36).to_edge(UP, buff=0.3)
        panels = VGroup()
        for key, title in (("16@24", r"16-QAM, \ 24 dB"), ("16@14", r"16-QAM, \ 14 dB"), ("64@24", r"64-QAM, \ 24 dB")):
            cl = p["clouds"][key]
            ax = Square(3.2, stroke_color=GREY_D, stroke_width=1)
            dots = VGroup()
            for (x, y), t in zip(cl["pts"], cl["tx"]):
                if abs(x) < 1.5 and abs(y) < 1.5:
                    dots.add(Dot([x * 1.05, y * 1.05, 0], radius=0.018, color=[DATA, HEAD, LAM, KERN][t % 4]))
            dots.move_to(ax)
            cap = label(title, font_size=19, color=WHITE).next_to(ax, UP, buff=0.12)
            ser = label(rf"symbol errors {cl['ser']:.1%}".replace("%", r"\%"), font_size=17,
                        color=YES if cl["ser"] < 0.01 else NO).next_to(ax, DOWN, buff=0.12)
            panels.add(VGroup(ax, dots, cap, ser))
        panels.arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.5)
        lines = VGroup(
            label(r"each symbol is one of $M$ points \ (amplitude and phase): \ $\log_2 M$ bits; \ Gray-coded, \ so "
                  r"a near miss costs one bit", font_size=20, color=WHITE),
            label(r"noise scatters the points; \ the receiver picks the nearest; \ errors when clouds overlap",
                  font_size=20, color=NO),
            label(r"more points, \ more bits, \ but each needs more signal: \ 64-QAM needs about 6 dB more than 16-QAM",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How do real systems approach the limit? <bookmark mark='a'/> By sending, in each symbol, one of M "
            "points in a plane: an amplitude and a phase, which together encode log two of M bits. Sixteen points, "
            "four bits a symbol. The labels are Gray-coded, so neighbouring points differ in one bit. "
            "<bookmark mark='b'/> Noise scatters each received point into a cloud, and the receiver picks the nearest "
            "point. At twenty-four decibels the clouds are tight; at fourteen they touch, and several percent of "
            "symbols are wrong. <bookmark mark='c'/> Sixty-four points carry six bits, but packed closer, they need about six "
            "decibels more signal for the same error rate."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(panels[2]), FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def gap(self):
        p = load("phy")
        head = label(r"Measured against Shannon", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[4, 36, 4], y_range=[-6, 0, 1], x_length=6.6, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to([-2.6, -0.2, 0])
        xt = VGroup(*[label(str(x), font_size=16, color=GREY_B).next_to(ax.c2p(x, -6), DOWN, buff=0.1)
                      for x in range(8, 37, 8)])
        yt = VGroup(*[MathTex(rf"10^{{{y}}}", font_size=18, color=GREY_B).next_to(ax.c2p(4, y), LEFT, buff=0.1)
                      for y in range(-6, 1, 2)])
        xl = label(r"$E_s/N_0$, \ dB", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"bit error rate", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        cols = {4: DATA, 16: HEAD, 64: LAM, 256: KERN}
        curves = VGroup()
        for q in p["qam"]:
            pts = [(m["snr_db"], np.log10(m["ber"])) for m in q["curve"] if m["ber"] > 0]
            if len(pts) > 1:
                curves.add(VMobject(color=cols[q["M"]], stroke_width=3).set_points_as_corners(
                    [ax.c2p(x, max(y, -6)) for x, y in pts]))
        rows = [[f"{q['M']}-QAM", str(q["bits"]), f"{q['snr_needed']:.1f} dB", f"{q['shannon']:.1f} dB",
                 f"{q['gap']:.1f} dB"] for q in p["qam"]]
        tab = grid_table([r"", r"bits", r"needs \ ($10^{-6}$)", r"Shannon", r"gap"], rows,
                         widths=[1.4, 0.8, 1.5, 1.4, 1.0], row_h=0.42, font_size=18, mono_cols=())
        tab.move_to([3.6, 0.6, 0])
        for r, q in enumerate(p["qam"], start=1):
            tab.cells[r][0].set_color(cols[q["M"]])
            tab.cells[r][4].set_color(NO)
        lines = VGroup(
            wrapped_label(r"measured symbol errors match \\ the textbook formula", 6.4, font_size=19, color=WHITE),
            wrapped_label(r"uncoded QAM sits about 8.6 dB \\ from Shannon's limit, \ at every size", 6.4, font_size=19, color=NO),
            wrapped_label(r"error-correcting codes \ (Part 28: \ LDPC, \\ turbo, \ polar) \ close all but a fraction \\ of a "
                  r"decibel", 6.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(tab, DOWN, buff=0.5).align_to(tab, LEFT)
        with self.voiceover(
            "We sent two hundred thousand random symbols for each size and signal level, and counted errors. "
            "<bookmark mark='a'/> The measured rates fall on the textbook formula's curves, and each curve sits "
            "further right, needing more signal, as the points multiply. <bookmark mark='b'/> Now compare with "
            "Shannon. To carry four bits a symbol, Shannon needs a signal-to-noise ratio of fifteen, under twelve "
            "decibels; uncoded 16-QAM needs twenty to reach one error in a million bits. The gap is about eight and "
            "a half decibels, whatever the size. <bookmark mark='c'/> Closing it is the job of Part 28's "
            "error-correcting codes. Modern links with LDPC or polar codes run within a fraction of a decibel of the "
            "limit."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(lines[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def light(self):
        p = load("phy")
        head = label(r"The speed of light is a budget", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r["name"], f"{r['km']:,.0f} km", f"{r['rtt_ms']:.0f} ms"] for r in p["rtts"]]
        tab = grid_table([r"route", r"fibre", r"round trip, \ at best"], rows, widths=[4.2, 2.0, 2.6], row_h=0.42,
                         font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for r in range(1, len(rows) + 1):
            tab.cells[r][2].set_color(HEAD)
        bd = [[(f"{b['rate'] / 1e9:.0f} Gb/s" if b["rate"] >= 1e9 else f"{b['rate'] / 1e6:.0f} Mb/s"),
               (f"{b['bytes'] / 1e6:.0f} MB" if b["bytes"] >= 1e6 else f"{b['bytes'] / 1e3:.1f} kB")] for b in p["bdp"]]
        tab2 = grid_table([r"rate, \ New York--London", r"bytes in flight"], bd, widths=[4.0, 2.6], row_h=0.42,
                          font_size=19, mono_cols=())
        tab2.next_to(tab, DOWN, buff=0.5).set_x(0)
        for r in range(1, 4):
            tab2.cells[r][1].set_color(YES)
        lines = VGroup(
            label(r"light in glass: \ about 204{,}000 km a second, \ two thirds of $c$", font_size=20, color=WHITE),
            label(r"\textbf{bandwidth--delay product}: \ to keep a long fat pipe full, \ this much must be sent "
                  r"before any reply can return \ (Part 37)", font_size=20, color=YES),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Capacity is one limit; distance is the other. <bookmark mark='a'/> Light in glass travels about two "
            "hundred thousand kilometres a second, two thirds of its speed in vacuum. A round trip from New York to "
            "London takes at least fifty-five milliseconds; to Singapore and back from London, a hundred and "
            "eighteen. No engineering can lower these. <bookmark mark='b'/> Multiply the rate by the round trip and "
            "you get the bandwidth-delay product, the bytes that must be in flight to keep the pipe full. At a "
            "hundred gigabits a second across the Atlantic, six hundred and eighty-eight megabytes are in the cable "
            "at once. Part 37's TCP has to manage exactly that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(*[Indicate(c, color=HEAD) for c in [tab.cells[r][2] for r in range(1, len(rows) + 1)]])
            vo.wait_until("b")
            self.play(FadeIn(tab2), FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()


_ = (num,)
