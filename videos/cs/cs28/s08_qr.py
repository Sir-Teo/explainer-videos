from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono, qr_grid)

LIGHT = "#e8e8e8"


def overlay(g, cells_xy, color, opacity=0.55):
    return VGroup(*[g.cells[y][x].copy().set_fill(color, opacity).set_stroke(width=0) for x, y in cells_xy])


class Qr(VoiceoverScene):
    def construct(self):
        self.card()
        self.anatomy()
        self.codewords()
        self.trace()
        self.scratches()

    def card(self):
        card = chapter_card(7, r"Our QR code", r"How much damage can a QR code take?", lit=(1994, 2000),
                            extra=((1994, r"Denso Wave"), (2000, r"ISO/IEC 18004")), part=PART)
        with self.voiceover("Chapter seven. Our QR code."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def anatomy(self):
        q = load("qr")
        head = label(r"Anatomy of a version-2 QR code", font_size=34).to_edge(UP, buff=0.3)
        g = qr_grid(q["matrix"], side=5.2).to_edge(LEFT, buff=0.8).shift(DOWN * 0.35)
        n = 25
        finder = [(x, y) for y in range(n) for x in range(n) if (x < 8 and y < 8) or (x > 16 and y < 8)
                  or (x < 8 and y > 16)]
        timing = [(6, i) for i in range(8, 17)] + [(i, 6) for i in range(8, 17)]
        align = [(x, y) for y in range(16, 21) for x in range(16, 21)]
        fmt = [(8, i) for i in range(9) if i != 6] + [(i, 8) for i in range(8) if i != 6] + \
              [(n - 1 - i, 8) for i in range(8)] + [(8, n - 7 + i) for i in range(7)]
        data = [(x, y) for y in range(n) for x in range(n) if q["owner"][y][x] >= 0]
        ov = [overlay(g, finder, HEAD), overlay(g, timing, LAM), overlay(g, align, CTRL), overlay(g, fmt, NO),
              overlay(g, data, DATA, 0.35)]
        lines = VGroup(
            label(r"\textbf{finder patterns}: \ three squares that fix position, \\ scale and rotation", font_size=21,
                  color=HEAD),
            label(r"\textbf{timing} and \textbf{alignment}: \ the module grid, \\ even when the paper is bent",
                  font_size=21, color=LAM),
            label(r"\textbf{format}: \ error level and mask, \ 15 bits, \\ stored twice with their own BCH code",
                  font_size=21, color=NO),
            label(rf"\textbf{{data}}: \ 44 bytes, \ placed in two-column zigzags \\ and XOR-ed with mask "
                  rf"{q['mask']} \ (chosen to avoid confusing patterns)", font_size=21, color=DATA),
            label(rf"level Q: \ 22 message bytes, \ 22 Reed--Solomon check bytes: \\ any 11 wrong bytes, \ or 22 "
                  r"known-missing ones, \ are repaired", font_size=21, color=YES),
            label(r"our encoder matches a standard library \\ bit for bit, \ for every mask: \ scan it", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.6).align_to(g, UP)
        fit_right(lines)
        with self.voiceover(
            "Masahiro Hara's team at Denso Wave designed the QR code in 1994 to track car parts. Ours is version "
            "two: twenty-five by twenty-five modules. <bookmark mark='a'/> Three finder squares let a camera find "
            "the code and its orientation. <bookmark mark='b'/> Timing stripes and an alignment square recover the "
            "grid even on a curved surface. <bookmark mark='c'/> Fifteen format bits record the error-correction "
            "level and the mask, stored twice and protected by a small code of their own. <bookmark mark='d'/> "
            "Everything else is data: forty-four bytes laid out in zigzags two columns wide, then XOR-ed with one of "
            "eight masks, chosen to avoid large blocks and patterns that look like finders. <bookmark mark='e'/> We "
            "chose level Q: twenty-two bytes of message and twenty-two Reed-Solomon check bytes, enough to repair "
            "any eleven wrong bytes, or twenty-two missing ones whose places are known. <bookmark mark='f'/> Our "
            "encoder produces exactly the same modules as a standard library for every mask, so your phone can read "
            "it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            for i, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(FadeIn(ov[i]), FadeIn(lines[i]))
                if i < 4:
                    self.play(FadeOut(ov[i]), run_time=0.6)
            vo.wait_until("f")
            self.play(FadeOut(ov[4]), FadeIn(lines[5]))
        self.wait(0.3)
        self.clear_scene()

    def codewords(self):
        q = load("qr")
        head = label(r"Where each byte lives", font_size=34).to_edge(UP, buff=0.3)
        g = qr_grid(q["matrix"], side=5.2).to_edge(LEFT, buff=0.8).shift(DOWN * 0.35)
        cols = [DATA, HEAD, YES, LAM, CTRL, NO]
        tint = VGroup()
        for y in range(25):
            for x in range(25):
                k = q["owner"][y][x]
                if k >= 0:
                    c = cols[k % len(cols)]
                    tint.add(g.cells[y][x].copy().set_fill(c, 0.55 if k < 22 else 0.3).set_stroke(width=0))
        nums = VGroup()
        for k in range(44):
            cells = [(x, y) for y in range(25) for x in range(25) if q["owner"][y][x] == k]
            cx = sum(x for x, _ in cells) / len(cells)
            cy = sum(y for _, y in cells) / len(cells)
            nums.add(label(str(k), font_size=13, color=WHITE).move_to(
                g.cells[0][0].get_center() + RIGHT * g.step * cx + DOWN * g.step * cy).set_stroke(BG, 2,
                                                                                               background=True))
        d = q["data"]
        lines = VGroup(
            label(r"each byte owns a 2 $\times$ 4 patch, \ snaking up and down", font_size=21, color=WHITE),
            label(rf"bytes 0--21: \ the message \\ \texttt{{0100}} (byte mode), \ length "
                  rf"{((d[0] & 15) << 4) | (d[1] >> 4)}, \ the text, \ padding", font_size=21, color=DATA),
            label(r"bytes 22--43: \ the remainder of the message \\ polynomial times $x^{22}$, \ divided by "
                  r"$\prod_{i<22} (x - \alpha^i)$", font_size=21, color=HEAD),
            label(r"so the 44 bytes are the coefficients of a polynomial \\ that vanishes at $\alpha^0, \ldots, "
                  r"\alpha^{21}$: \ the 22 \textbf{syndromes}", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.6).align_to(g, UP)
        fit_right(lines)
        with self.voiceover(
            "Here is where each of the forty-four bytes lives. <bookmark mark='a'/> Each one owns a patch of eight "
            "modules, two wide, snaking up and down the code from the bottom right. <bookmark mark='b'/> The first "
            "twenty-two hold the message: a mode marker, the length, the text and padding. <bookmark mark='c'/> The "
            "last twenty-two are the Reed-Solomon checks, in the generator form used in practice: the message "
            "polynomial is shifted up and divided by a polynomial with roots at the first twenty-two powers of "
            "alpha, and the remainder is appended. <bookmark mark='d'/> So the whole codeword vanishes at those "
            "twenty-two points. The decoder evaluates it there: the twenty-two syndromes are all zero when nothing "
            "is wrong, and otherwise they encode where and how the bytes were damaged."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(tint), FadeIn(lines[0]))
            self.play(FadeIn(nums))
            for mk, ln in zip("bcd", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def trace(self):
        t = load("qrtrace")
        head = label(r"The decoder at work, \ on the small scratch", font_size=34).to_edge(UP, buff=0.3)

        def hexrow(vals, color, per=11):
            rows = VGroup()
            for i in range(0, len(vals), per):
                rows.add(VGroup(*[mono(f"{v:02x}", 18, color if v else GREY_D) for v in vals[i:i + per]]).arrange(
                    RIGHT, buff=0.16))
            return rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        syn = hexrow(t["syndromes"], NO)
        loc = hexrow(t["locator"], HEAD, per=9)
        steps = VGroup(
            VGroup(label(r"1. \ 22 syndromes: \ the read bytes, \ as a polynomial, \ at $\alpha^0, \ldots, "
                         r"\alpha^{21}$; \ nonzero means damage", font_size=20, color=WHITE), syn).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(label(rf"2. \ Berlekamp--Massey: \ an error locator of degree {len(t['locator']) - 1}", font_size=20,
                         color=WHITE), loc).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            label(rf"3. \ Chien search: \ its roots point at bytes {', '.join(map(str, t['found']))}", font_size=20,
                  color=YES),
            label(rf"\ \ \ the bytes the paint actually changed: \ {', '.join(map(str, t['wrong']))}",
                  font_size=20, color=GREY_A),
            label(r"4. \ Forney's formula: \ the error value at each, \ XOR-ed off: \ "
                  + ("all 44 bytes restored" if t["ok"] else "failed"), font_size=20, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        with self.voiceover(
            "Here is the decoder working on the small scratch, step by step. <bookmark mark='a'/> It evaluates the "
            "forty-four bytes it read, as a polynomial, at the twenty-two powers of alpha. A clean code gives all "
            "zeros; these are not. <bookmark mark='b'/> The Berlekamp-Massey algorithm turns the syndromes into an "
            "error-locator polynomial, here of degree eight: the decoder now believes eight bytes are wrong. "
            "<bookmark mark='c'/> Chien's search tries every position and finds the eight roots, <bookmark "
            "mark='d'/> which are exactly the eight bytes the paint changed. <bookmark mark='e'/> Forney's formula "
            "gives the error value at each, and exclusive-or removes it. All forty-four bytes are back."
        ) as vo:
            self.play(FadeIn(head))
            for mk, st in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def scratches(self):
        q = load("qr")
        head = label(r"Three scratches", font_size=34).to_edge(UP, buff=0.3)
        grids = Group()
        caps = VGroup()
        for s in q["scratches"]:
            g = qr_grid(q["matrix"], side=3.6)
            x0, y0, x1, y1 = s["rect"]
            paint = VGroup(*[g.cells[y][x].copy().set_fill(LIGHT, 1).set_stroke(LIGHT, width=1.2) for y in range(y0, y1 + 1)
                             for x in range(x0, x1 + 1)])
            box = Rectangle(width=g.step * (x1 - x0 + 1), height=g.step * (y1 - y0 + 1), stroke_color=NO,
                            stroke_width=3).move_to(VGroup(g.cells[y0][x0], g.cells[y1][x1]))
            grids.add(Group(g, paint, box))
            r = s["result"]
            caps.add(VGroup(
                label(rf"{s['modules']} modules painted", font_size=19, color=GREY_A),
                label(rf"{len(s['wrong'])} bytes wrong, \ {len(s['touched'])} touched", font_size=19, color=WHITE),
                label(r"as errors: \ " + ("read" if r["errors"]["ok"] else "fails"), font_size=19,
                      color=YES if r["errors"]["ok"] else NO),
                label(r"as erasures: \ " + ("read" if r["erasures"]["ok"] else "fails"), font_size=19,
                      color=YES if r["erasures"]["ok"] else NO)).arrange(DOWN, buff=0.08))
        grids.arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.4)
        for c, g in zip(caps, grids):
            c.next_to(g, DOWN, buff=0.25)
        lines = VGroup(
            label(r"errors: \ the decoder must find the bad bytes itself: \ up to 11", font_size=21, color=WHITE),
            label(r"erasures: \ tell it which bytes the paint touched: \ up to 22 \ (chapter 2's rule)", font_size=21,
                  color=DATA),
            label(r"too much paint: \ more than 22 bytes touched, \ and no code of this rate can help", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now we damage it, three ways. <bookmark mark='a'/> A small scratch whitens fifty-six modules. Eight "
            "bytes come out wrong. That is within the eleven errors the code can find on its own, and the text comes "
            "back. <bookmark mark='b'/> A longer blot ruins fifteen bytes. As unknown errors that is too many: the "
            "decoder's locator polynomial has no consistent roots, and it gives up rather than guess. But a scanner "
            "can see where the damage is. Told which eighteen bytes the blot touched, the decoder treats them as "
            "erasures, and twenty-two erasures are allowed. The text comes back. <bookmark mark='c'/> Paint a whole "
            "stripe and twenty-four bytes are touched: more than the twenty-two check bytes can cover either way. "
            "Nothing helps, and the decoder correctly reports failure."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grids[0][0]))
            self.play(FadeIn(grids[0][1]), Create(grids[0][2]), FadeIn(caps[0]), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(grids[1][0]))
            self.play(FadeIn(grids[1][1]), Create(grids[1][2]), FadeIn(caps[1]), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(grids[2][0]))
            self.play(FadeIn(grids[2][1]), Create(grids[2][2]), FadeIn(caps[2]), FadeIn(lines[2]))
        self.wait(0.5)
        self.clear_scene()
