from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, code_block, grid_table, load,
                                   module_box, mono, tag_box)


# WCAG 2's relative luminance, written out so the derivation on screen is the one checked against the data
def _lin(v8: int) -> float:
    c = v8 / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lin_c(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _rgb(hexcol: str):
    h = hexcol.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def _lum(hexcol: str) -> float:
    r, g, b = (_lin(v) for v in _rgb(hexcol))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _ratio(a: str, b: str) -> float:
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


class Access(VoiceoverScene):
    def construct(self):
        self.card()
        self.tree()
        self.keyboard()
        self.contrast()
        self.palette()
        self.radio()
        self.ui_thread()
        self.platforms()

    def card(self):
        card = chapter_card(12, r"Accessibility and mobile", r"Who else must be able to use the page, and on what?",
                            lit=(2008, 2012, 2023), extra=((2008, r"WCAG 2.0"),
                                                           (2012, r"Huang et al.: \ LTE power"),
                                                           (2023, r"WCAG 2.2")), part=PART)
        with self.voiceover("Chapter twelve. Accessibility and mobile."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tree(self):
        head = label(r"The accessibility tree", font_size=36).to_edge(UP, buff=0.3)
        src = ['<nav><a href="/">Home</a></nav>', '<img src="cat.jpg" alt="A cat asleep">',
               '<label><input type=checkbox checked>', '  Gift wrap</label>', '<button>Buy</button>',
               '<div class="btn" onclick="buy()">Buy</div>']
        code = code_block(src, size=17, buff=0.38).move_to([-3.9, 0.45, 0]).to_edge(LEFT, buff=0.35)
        code[5].set_color(NO)

        def chip(text, col):
            return tag_box(text, color=col, size=16, h=0.42)

        def name(text):
            return mono(f'"{text}"', size=16, color=YES)

        def state(text, col=HEAD):
            return label(text, font_size=18, color=col)
        specs = [(0, [chip("navigation", DATA), chip("link", DATA), name("Home")]),
                 (1, [chip("image", DATA), name("A cat asleep")]),
                 (2.5, [chip("checkbox", DATA), name("Gift wrap"), state(r"checked")]),
                 (4, [chip("button", DATA), name("Buy"), state(r"focusable")]),
                 (5, [chip("generic", NO), mono('text "Buy"', size=16, color=GREY_A),
                      state(r"no role, \ no focus", NO)])]
        rows, links = VGroup(), VGroup()
        for li, parts in specs:
            y = (code[int(li)].get_y() + code[int(li + 0.5)].get_y()) / 2
            r = VGroup(*parts).arrange(RIGHT, buff=0.18).move_to([0, y, 0]).align_to([0.4, 0, 0], LEFT)
            src_line = code[int(li)] if li == int(li) else VGroup(code[int(li)], code[int(li + 0.5)])
            links.add(Line([src_line.get_right()[0] + 0.12, y, 0], [r.get_left()[0] - 0.12, y, 0], color=GREY_D,
                           stroke_width=1.5))
            rows.add(r)
        titles = VGroup(label(r"the DOM", font_size=20, color=GREY_A).next_to(code, UP, buff=0.25).align_to(code,
                                                                                                    LEFT),
                        label(r"the accessibility tree: \ role, \ name, \ state", font_size=20,
                              color=GREY_A).next_to(code, UP, buff=0.25).align_to(rows, LEFT))
        lines = VGroup(
            wrapped_label(r"the browser derives it from the DOM and hands it to the operating system, \ where screen "
                          r"readers and switch controls read it", 12.6, font_size=19, color=WHITE),
            wrapped_label(r"the \texttt{div} looks like a button but is only text: \ nothing to press, \ and Tab "
                          r"never reaches it", 12.6, font_size=19, color=NO),
            note(r"illustrative markup", font_size=17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A screen reader does not see pixels. <bookmark mark='a'/> From the DOM the browser derives a second tree,"
            " the accessibility tree, and hands it to the operating system: for everything a person can perceive or "
            "operate, a role, a name and a state. <bookmark mark='b'/> A button element becomes a button named Buy; a "
            "checkbox is named by its label, and is checked; an image is named by its alt text. <bookmark mark='c'/> "
            "But a div with a click handler is just generic text: nothing to press, and the keyboard cannot reach it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), FadeIn(titles[0]))
            vo.wait_until("a")
            self.play(FadeIn(titles[1]), FadeIn(lines[0]), FadeIn(lines[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(Create(links[i]), FadeIn(rows[i])) for i in range(4)],
                                  lag_ratio=0.4), run_time=2.4)
            vo.wait_until("c")
            self.play(Create(links[4]), FadeIn(rows[4]), FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def keyboard(self):
        head = label(r"Keyboard, \ focus and ARIA", font_size=36).to_edge(UP, buff=0.3)
        # what the screen shows (Menu first, moved there by CSS) against the DOM order that Tab follows
        visual = [("Menu", 4), ("Logo", 1), ("Search", 2), ("Cart", 3)]
        boxes = VGroup(*[tag_box(t, color=DATA, size=20, w=1.9, h=0.6) for t, _ in visual]).arrange(RIGHT, buff=0.7)
        nums = VGroup(*[label(rf"DOM \#{n}", font_size=17, color=GREY_B).next_to(b, DOWN, buff=0.12)
                        for b, (_, n) in zip(boxes, visual)])
        page = SurroundingRectangle(VGroup(boxes, nums), buff=0.25, corner_radius=0.1, color=GREY_C,
                                    stroke_width=1.5)
        bar = VGroup(page, boxes, nums).move_to([0, 1.75, 0])
        css = mono(".menu { order: -1 }", size=18, color=KERN).next_to(page, DOWN, buff=0.2).align_to(page, RIGHT)
        ring = SurroundingRectangle(boxes[1], buff=0.08, color=HEAD, stroke_width=5, corner_radius=0.1)
        tab_t = mono("Tab", size=18, color=HEAD).next_to(page, UP, buff=0.12).align_to(page, LEFT)
        order = sorted(range(4), key=lambda i: visual[i][1])
        aria = code_block(['<div role="button" tabindex="0"', '     aria-pressed="false">Mute</div>'], size=17)
        native = code_block(['<button aria-pressed="false">', '  Mute</button>'], size=17)
        a_t = wrapped_label(r"ARIA repairs the tree: \ a role, \ focus, \ a state; \ but Enter and Space are still "
                            r"yours to handle", 5.6, font_size=19, color=HEAD)
        n_t = wrapped_label(r"the native element: \ role, \ focus and keys for free; \ the first rule of ARIA is to "
                            r"prefer it", 5.6, font_size=19, color=YES)
        left = VGroup(aria, a_t).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        right = VGroup(native, n_t).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, -1.15, 0])
        rule = wrapped_label(r"focus follows the DOM, \ not the screen", 6.0, font_size=20,
                             color=WHITE).next_to(page, DOWN, buff=0.2).align_to(page, LEFT)
        with self.voiceover(
            "Many people use only a keyboard. <bookmark mark='a'/> Tab moves the focus in the order of the DOM, not "
            "the order on screen, so a layout rearranged by CSS sends the focus jumping. <bookmark mark='b'/> ARIA "
            "attributes can repair the accessibility tree with a role, a name or a state, but the keys are then yours "
            "to handle. The first rule of ARIA is to prefer the native element, which brings it all for free."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar), FadeIn(css))
            vo.wait_until("a")
            self.play(Create(ring), FadeIn(tab_t))
            for i in order[1:]:
                self.play(ring.animate.move_to(boxes[i]), Indicate(tab_t, color=HEAD, scale_factor=1.15),
                          run_time=0.8)
            self.play(FadeIn(rule))
            vo.wait_until("b")
            self.play(FadeIn(left))
            self.play(FadeIn(right))
        self.wait(0.4)
        self.clear_scene()

    def contrast(self):
        c = load("contrast")
        row = next(r for r in c["rows"] if r["name"] == "DATA")
        assert abs(_ratio(row["hex"], c["bg"]) - row["ratio"]) < 1e-9 and abs(_lum(c["bg"]) - c["lum_bg"]) < 1e-12
        assert abs(_ratio("#000000", "#ffffff") - c["black_white"]) < 1e-9
        head = label(r"The contrast ratio, \ derived", font_size=36).to_edge(UP, buff=0.3)
        f1 = MathTex(r"c_{\text{lin}} = \begin{cases} c / 12.92 & c \le 0.04045 \\ "
                     r"\left(\dfrac{c + 0.055}{1.055}\right)^{2.4} & \text{otherwise} \end{cases}"
                     r"\qquad c = \frac{v}{255}", font_size=30, color=WHITE)
        f2 = MathTex(r"L = 0.2126\,R + 0.7152\,G + 0.0722\,B", font_size=30, color=WHITE)
        f3 = MathTex(r"\text{ratio} = \frac{L_1 + 0.05}{L_2 + 0.05}", r"\qquad", r"\frac{1 + 0.05}{0 + 0.05} = 21",
                     font_size=30, color=WHITE)
        f3[2].set_color(HEAD)
        why = VGroup(
            label(r"undo sRGB's gamma: \ values become linear light", font_size=18, color=GREY_B),
            label(r"weight the primaries by how bright they look: \ mostly green", font_size=18, color=GREY_B),
            label(r"lighter over darker: \ from 1 \ (no contrast) \ to 21 \ (black on white)", font_size=18,
                  color=GREY_B))
        eqs = VGroup()
        for f, w in zip((f1, f2, f3), why):
            eqs.add(VGroup(f, w).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.4, 1.0, 0]).to_edge(LEFT, buff=0.4)
        ax = axes([0, 1, 0.5], [0, 1, 0.5], x_length=3.4, y_length=2.6, x_label=r"encoded value $c$",
                  xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], font=16)
        ax.move_to([4.6, 1.0, 0])
        curve = ax.ax.plot(_lin_c, x_range=[0, 1, 0.01], color=HEAD,
                           stroke_width=3)
        ident = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(1, 1), color=GREY_C, stroke_width=1.5)
        ylab = label(r"linear light", font_size=17, color=HEAD).next_to(ax.ax, UP, buff=0.1)
        # worked example: our blue on the background
        rgb = _rgb(row["hex"])
        lins = [_lin(v) for v in rgb]
        lum = _lum(row["hex"])
        tab = grid_table([rf"\texttt{{\{row['hex']}}}", r"R", r"G", r"B"],
                         [[r"8-bit $v$", *[f"{v}" for v in rgb]], [r"linear", *[f"{x:.3f}" for x in lins]]],
                         widths=[1.8, 1.1, 1.1, 1.1], row_h=0.42, font_size=19, mono_cols=())
        tab.cells[0][0].set_color(DATA)
        res = MathTex(rf"L = {lum:.3f}", r"\qquad", rf"\frac{{{lum:.3f} + 0.05}}{{{c['lum_bg']:.4f} + 0.05}} = "
                      rf"{row['ratio']:.2f}", font_size=30, color=WHITE)
        res[0].set_color(DATA)
        res[2].set_color(YES)
        bgnote = label(rf"background \texttt{{\{c['bg']}}}: \ $L = {c['lum_bg']:.4f}$", font_size=18,
                       color=GREY_B)
        ex = VGroup(tab, VGroup(res, bgnote).arrange(DOWN, aligned_edge=LEFT, buff=0.15)).arrange(RIGHT, buff=0.7)
        ex.to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Text must also be readable, and the Web Content Accessibility Guidelines, WCAG, make readable a number. "
            "<bookmark mark='a'/> sRGB values are gamma-encoded, so first undo it: a short straight piece near black, "
            "then a power of two point four. <bookmark mark='b'/> Weight the linear channels by how bright each "
            "primary looks, mostly green, to get the relative luminance. <bookmark mark='c'/> The contrast ratio is "
            "the lighter luminance plus five hundredths, over the darker plus five hundredths: one for equal colours, "
            "twenty-one for black on white. <bookmark mark='d'/> Our blue, on our background: point three seven "
            "against point zero zero eight six, a ratio of seven point one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]), FadeIn(ax), Create(ident), FadeIn(ylab))
            self.play(Create(curve), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab))
            self.play(FadeIn(res), FadeIn(bgnote))
        self.wait(0.4)
        self.clear_scene()

    def palette(self):
        c = load("contrast")
        grey = c["grey_on_white"]
        g_ratio = _ratio(grey, "#ffffff")
        v = int(grey[1:3], 16) + 1
        assert g_ratio >= 4.5 > _ratio(f"#{v:02x}{v:02x}{v:02x}", "#ffffff")
        head = label(r"Our palette, \ checked", font_size=36).to_edge(UP, buff=0.3)

        def white_tile(fg, text):
            r = Rectangle(width=3.4, height=0.7, stroke_width=0, fill_color=WHITE, fill_opacity=1)
            t = label(text, font_size=21, color=fg).move_to(r)
            return VGroup(r, t)
        tiles = VGroup(white_tile(BLACK, rf"black on white: \ {c['black_white']:.0f}:1"),
                       white_tile(grey, rf"\texttt{{\{grey}}} on white: \ {g_ratio:.2f}:1")).arrange(RIGHT, buff=0.5)
        th = label(r"pass marks: \ AA needs 4.5 \ (3 for large text); \ AAA needs 7", font_size=19, color=GREY_A)
        top = VGroup(tiles, th).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.35)

        def mark(ok):
            return MathTex(r"\checkmark" if ok else r"\times", font_size=30, color=YES if ok else NO)
        cols = VGroup()
        for r in c["rows"]:
            tile = Rectangle(width=1.3, height=1.0, stroke_color=GREY_D, stroke_width=1, fill_color=BG,
                             fill_opacity=1)
            aa = label(r"Aa", font_size=38, color=r["hex"]).move_to(tile)
            nm = mono(r["name"], size=17, color=r["hex"] if r["ratio"] >= 3 else GREY_A)
            hx = mono(r["hex"].upper(), size=17, color=GREY_B)
            ra = label(f"{r['ratio']:.2f}", font_size=25, color=WHITE)
            m1 = VGroup(label(r"AA", font_size=18, color=GREY_B), mark(r["AA text"])).arrange(RIGHT, buff=0.1)
            m2 = VGroup(label(r"AAA", font_size=18, color=GREY_B), mark(r["AAA text"])).arrange(RIGHT, buff=0.1)
            cols.add(VGroup(VGroup(tile, aa), nm, hx, ra, m1, m2).arrange(DOWN, buff=0.17))
        cols.arrange(RIGHT, buff=0.14).next_to(top, DOWN, buff=0.55)
        if cols.width > 13.2:
            cols.width = 13.2
        cols.set_x(0)
        bad = next(i for i, r in enumerate(c["rows"]) if not r["AA text"])
        aaa = [r["name"] for r in c["rows"] if r["AAA text"]]
        lines = VGroup(
            wrapped_label(rf"against the background \texttt{{\{c['bg']}}}: \ every colour but one passes AA; \ "
                          rf"{len(aaa)} pass AAA", 12.6, font_size=19, color=YES),
            wrapped_label(rf"\texttt{{GREY\_D}} fails at {c['rows'][bad]['ratio']:.2f}: \ it should carry lines, \ "
                          r"not words, \ yet the years on our own timeline strip use it", 12.6, font_size=19,
                          color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Normal text needs four and a half to one for level AA, large text three, and level AAA seven. <bookmark "
            "mark='a'/> On white, the lightest grey that passes AA is hex seven six seven six seven six. <bookmark "
            "mark='b'/> On our background, every colour of this series' palette but one passes AA, and four pass AAA. "
            "<bookmark mark='c'/> The darkest grey fails, at one point eight four. It should carry lines, not words, "
            "yet our own timeline strip prints its years in it: a fault this check has just found."
        ) as vo:
            self.play(FadeIn(head), FadeIn(th))
            vo.wait_until("a")
            self.play(FadeIn(tiles))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(col) for col in cols], lag_ratio=0.15), run_time=2)
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(Indicate(cols[bad], color=NO, scale_factor=1.06), FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def radio(self):
        d = load("radio")
        p = d["params"]
        head = label(r"The radio's tail", font_size=36).to_edge(UP, buff=0.3)
        x0, k, hk = -4.3, 0.0535, 0.65                     # seconds and watts -> scene units
        power = {"promote": p["promotion_w"], "active": p["active_w"], "tail": p["tail_w"]}
        color = {"promote": HEAD, "active": NO, "tail": KERN}

        def lane(segs, y):
            g = VGroup(Line([x0, y, 0], [x0 + 200 * k, y, 0], color=GREY_D, stroke_width=1.5))
            for kind, t0, t1 in segs:
                if t1 - t0 < 1e-9:
                    continue
                h = power[kind] * hk
                g.add(Rectangle(width=max(0.03, (t1 - t0) * k), height=h, stroke_width=0, fill_color=color[kind],
                                fill_opacity=0.85).move_to([x0 + (t0 + t1) / 2 * k, y + h / 2, 0]))
            return g
        y1, y2 = 0.95, -1.05
        l1, l2 = lane(d["spread"], y1), lane(d["batched"], y2)
        n_req = sum(1 for s in d["spread"] if s[0] == "active")
        gap = d["spread"][3][1] - d["spread"][0][1]
        names = VGroup(wrapped_label(rf"{n_req} requests\\{gap:.0f} s apart", 2.0, font_size=19, color=WHITE),
                       wrapped_label(rf"the same {n_req}\\batched", 2.0, font_size=19, color=WHITE))
        names[0].move_to([-5.6, y1 + 0.35, 0])
        names[1].move_to([-5.6, y2 + 0.35, 0])
        e1 = label(rf"about {d['spread_J']:.0f} J", font_size=24, color=NO).move_to([5.6, y1 + 1.15, 0])
        e2 = label(rf"about {d['batched_J']:.1f} J", font_size=24, color=YES).move_to([-0.5, y2 + 0.45, 0])
        ratio = label(rf"spread out, \ the same bytes cost {d['ratio']:.1f} times the energy", font_size=22,
                      color=HEAD).move_to([0, -1.85, 0])
        ticks = VGroup(*[label(rf"{t} s", font_size=16, color=GREY_B).move_to([x0 + t * k, y2 - 0.25, 0])
                         for t in range(0, 201, 50)])
        tr = d["spread"][1][2] - d["spread"][1][1]
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=color[kn], fill_opacity=0.85),
                                 label(t, font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.1)
                          for kn, t in (("promote", rf"waking up: \ {p['promotion_s']} s at {p['promotion_w']} W"),
                                        ("active", rf"transfer: \ {tr:.1f} s at {p['active_w']} W"),
                                        ("tail", rf"tail: \ {p['tail_s']} s at {p['tail_w']} W"))]
                        ).arrange(RIGHT, buff=0.5).move_to([0.3, 2.55, 0])
        src = wrapped_label(r"an LTE radio-state model with parameters rounded from Huang et al., \ MobiSys 2012; \ "
                            r"idle power is left out; \ heights are power", 12.6, font_size=18,
                            color=GREY_B).to_edge(DOWN, buff=0.35)
        batch = wrapped_label(r"hence background-work schedulers on both phone platforms, \ and sync that waits for "
                              r"the radio to be awake anyway", 12.6, font_size=19,
                              color=WHITE).next_to(src, UP, buff=0.15)
        with self.voiceover(
            "On a phone, the radio's cost depends on its state, not just on the bytes. <bookmark mark='a'/> In the LTE"
            " model measured by Huang and colleagues in 2012, waking the radio takes about a quarter of a second, and "
            "after a transfer it lingers in a high-power tail of about eleven and a half seconds. <bookmark mark='b'/>"
            " Ten small requests twenty seconds apart pay that tail ten times: about a hundred and thirty joules in "
            "our model. <bookmark mark='c'/> Sent together, they pay it once: about sixteen and a half joules, nearly "
            "eight times less. So phones batch background work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(legend), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(names[0]), Create(l1[0]), FadeIn(l1[1:4]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in l1[4:]], lag_ratio=0.1), run_time=2)
            self.play(FadeIn(e1))
            vo.wait_until("c")
            self.play(FadeIn(names[1]), Create(l2[0]), FadeIn(l2[1:]), FadeIn(ticks))
            self.play(FadeIn(e2), FadeIn(ratio), FadeIn(batch))
        self.wait(0.4)
        self.clear_scene()

    def ui_thread(self):
        head = label(r"The UI thread", font_size=36).to_edge(UP, buff=0.3)
        x0, k = -4.4, 0.21                                   # ms -> scene units

        def X(t):
            return x0 + t * k

        def block(t0, t1, y, col, text):
            r = Rectangle(width=(t1 - t0) * k, height=0.42, stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to([X((t0 + t1) / 2), y, 0])
            t = label(text, font_size=16, color=BLACK)
            if t.width > r.width - 0.08:
                return VGroup(r)
            return VGroup(r, t.move_to(r))
        ys = (1.55, 0.25, -0.4)
        vs = VGroup()
        for i, t in enumerate((0, 1000 / 60, 2000 / 60, 3000 / 60)):
            vs.add(DashedLine([X(t), 2.05, 0], [X(t), -0.75, 0], color=GREY_C, stroke_width=1.5))
            vs.add(label(rf"{t:.1f} ms" if i else r"0", font_size=16, color=GREY_B).move_to([X(t), -0.95, 0]))
        frame_t = label(r"a frame is due every 16.7 ms at 60 Hz, \ 8.3 ms at 120 Hz", font_size=18,
                        color=GREY_A).move_to([0.8, 2.4, 0])
        before = VGroup(block(1, 5, ys[0], DATA, r"input"), block(5, 11, ys[0], KERN, r"draw"),
                        block(17, 20, ys[0], DATA, r"input"), block(20, 44, ys[0], NO, r"read a file"),
                        block(44, 49, ys[0], KERN, r"draw"))
        miss = VGroup(Cross(scale_factor=0.18, stroke_color=NO, stroke_width=5).move_to([X(2000 / 60), ys[0] + 0.4,
                                                                                         0]),
                      label(r"frame missed", font_size=17, color=NO).move_to([X(2000 / 60) + 1.1, ys[0] + 0.45, 0]))
        after = VGroup(block(1, 5, ys[1], DATA, r"input"), block(5, 11, ys[1], KERN, r"draw"),
                       block(17, 20, ys[1], DATA, r"input"), block(20, 26, ys[1], KERN, r"draw"),
                       block(20, 44, ys[2], LAM, r"read a file"), block(44, 47, ys[1], KERN, r"draw"))
        lane_names = VGroup(label(r"UI thread", font_size=19, color=WHITE).move_to([-5.8, ys[0], 0]),
                            label(r"UI thread", font_size=19, color=WHITE).move_to([-5.8, ys[1], 0]),
                            label(r"worker", font_size=19, color=LAM).move_to([-5.8, ys[2], 0]))
        lines = VGroup(
            wrapped_label(r"the UI thread handles input and draws; \ disk and network work moves to other threads, "
                          r"\ as Chapter 5's frame budget demands", 12.6, font_size=19, color=WHITE),
            wrapped_label(r"Android offers to close an app that ignores input for five seconds: \ "
                          r"\textit{Application Not Responding}", 12.6, font_size=19, color=NO),
            note(r"illustrative timings", font_size=17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Native apps share the browser's problem. <bookmark mark='a'/> Each has one UI thread, which handles input"
            " and must deliver a frame every sixteen point seven milliseconds at sixty hertz, as in Chapter 5. A file "
            "read on that thread misses a frame. <bookmark mark='b'/> So disk and network work move to other threads, "
            "and Android offers to close an app that ignores input for five seconds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(vs), FadeIn(frame_t), FadeIn(lane_names[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in before], lag_ratio=0.5), run_time=2.4)
            self.play(FadeIn(miss), FadeIn(lines[2]))
            vo.wait_until("b")
            self.play(FadeIn(lane_names[1:]), LaggedStart(*[GrowFromEdge(b, LEFT) for b in after], lag_ratio=0.3),
                      run_time=2)
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def platforms(self):
        head = label(r"Native and cross-platform", font_size=36).to_edge(UP, buff=0.3)
        stacks = [(r"the platforms' own toolkits", GREY_A,
                   [(r"Swift \ or \ Kotlin", DATA), (r"UIKit, \ SwiftUI \ / \ Views, \ Compose", KERN),
                    (r"the platform's widgets", YES)]),
                  (r"React Native \ (Facebook, \ 2015)", DATA,
                   [(r"JavaScript and React", DATA), (r"React Native", KERN), (r"the platform's widgets", YES)]),
                  (r"Flutter \ (Google, \ 1.0 in 2018)", LAM,
                   [(r"Dart", DATA), (r"Flutter's widgets and renderer", KERN), (r"pixels it draws itself", LAM)])]
        cols = VGroup()
        for title, tcol, boxes in stacks:
            bx = VGroup(*[module_box(t, c, w=3.9, h=0.75, font=19) for t, c in boxes]).arrange(DOWN, buff=0.6)
            arr = VGroup(*[Arrow(bx[i].get_bottom(), bx[i + 1].get_top(), buff=0.04, stroke_width=2.5, color=GREY_B,
                                 max_tip_length_to_length_ratio=0.3) for i in range(2)])
            t = label(title, font_size=21, color=tcol).next_to(bx, UP, buff=0.25)
            cols.add(VGroup(t, bx, arr))
        cols.arrange(RIGHT, buff=0.35, aligned_edge=UP).next_to(head, DOWN, buff=0.5)
        lines = VGroup(
            wrapped_label(r"SwiftUI \ (2019) \ and Jetpack Compose \ (2021) \ are declarative, \ like Chapter 8's "
                          r"frameworks: \ the interface as a function of state", 12.6, font_size=19, color=WHITE),
            wrapped_label(r"one codebase for two platforms, \ against looking and behaving exactly like each", 12.6,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> Each platform has its own toolkit: UIKit and SwiftUI on iOS, Views and Jetpack "
            "Compose on Android, the newer ones declarative, like Chapter 8's frameworks. <bookmark mark='b'/> "
            "Cross-platform frameworks share one codebase. React Native, from 2015, drives the platform's own "
            "widgets from JavaScript; <bookmark mark='c'/> Flutter draws every pixel itself. The trade is one "
            "codebase against looking and behaving exactly like each platform."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(cols[1]))
            vo.wait_until("c")
            self.play(FadeIn(cols[2]), FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (grid_table, LAM)
