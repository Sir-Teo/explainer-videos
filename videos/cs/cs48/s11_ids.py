from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs48.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, module_box

MONO = "DejaVu Sans Mono"
# Snowflake's fields (explainer.cs.design.keys.snowflake): sign, milliseconds, machine, sequence
FIELDS = ((1, r"0", GREY_B), (41, r"41 bits: \ milliseconds since an epoch", DATA), (10, r"10: \ machine", KERN),
          (12, r"12: \ sequence", YES))


def sci(x: float) -> str:
    """A number as m x 10^e for Tex."""
    e = math.floor(math.log10(x))
    m = x / 10 ** e
    return rf"${m:.1f} \times 10^{{{e}}}$" if abs(m - 1) > 0.05 else rf"$10^{{{e}}}$"


def coloured(s: str, spans, size=16):
    """Monospaced text with character spans [(a, b, colour)] coloured."""
    return Text(s, font=MONO, font_size=size, color=GREY_A, t2c={f"[{a}:{b}]": c for a, b, c in spans})


class Ids(VoiceoverScene):
    def construct(self):
        self.card()
        self.counter()
        self.random()
        self.layout()
        self.skew()
        self.locality()

    def card(self):
        card = chapter_card(10, r"Unique IDs", r"How do many machines name things without asking each other?",
                            lit=(2010, 2024), extra=((2010, r"Twitter: \ Snowflake"),
                                                     (2024, r"RFC 9562: \ UUIDv7")), part=PART)
        with self.voiceover("Chapter ten. Unique IDs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ one counter
    def counter(self):
        head = label(r"Why not a counter?", font_size=36).to_edge(UP, buff=0.3)
        apps = VGroup(*[module_box(rf"server {i + 1}", DATA, w=1.6, h=0.5, font=18) for i in range(5)]).arrange(
            DOWN, buff=0.28).move_to([-5.3, 0.0, 0])
        db = module_box(r"one counter", KERN, w=2.0, h=0.7, font=19).move_to([-1.6, 0.0, 0])
        val = ValueTracker(1041)
        num = always_redraw(lambda: label(rf"next: \ {val.get_value():.0f}", font_size=18, color=KERN).next_to(
            db, DOWN, buff=0.15))
        asks = VGroup(*[Arrow(a.get_right(), db.get_left(), buff=0.08, stroke_width=1.8, color=GREY_B,
                              max_tip_length_to_length_ratio=0.1) for a in apps])
        dots = [Dot(a.get_right(), radius=0.07, color=HEAD) for a in apps for _ in range(2)]
        gens = VGroup(*[module_box(r"own IDs", YES, w=1.1, h=0.4, font=16).next_to(a, RIGHT, buff=0.15)
                        for a in apps])
        notes = VGroup(
            wrapped_label(r"every insert in the system asks one machine: \ a bottleneck, \ and a single point of "
                          r"failure", 5.4, font_size=19, color=NO),
            wrapped_label(r"split the counter: \ Flickr's two ticket servers \ (2010) \ handed out odd and even "
                          r"numbers", 5.4, font_size=19, color=HEAD),
            wrapped_label(r"or let each machine mint its own names, \ so that they never collide, \ without asking "
                          r"anyone", 5.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.7, 0.0, 0])
        foot = note(r"schematic", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Every record needs a name, and with many machines the obvious answer stops working. "
            "<bookmark mark='a'/> A single database counter hands out one, two, three. But then every insert in "
            "the system asks one machine: a bottleneck, and a single point of failure. <bookmark mark='b'/> "
            "Splitting the counter helps. Flickr, in 2010, ran two ticket servers, one handing out odd numbers "
            "and the other even. <bookmark mark='c'/> The other answer is to let each machine mint its own names, "
            "chosen so that they never collide, without asking anyone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(apps), FadeIn(db), FadeIn(num), FadeIn(foot))
            vo.wait_until("a")
            self.play(Create(asks))
            self.add(*dots)
            self.play(LaggedStart(*[d.animate.move_to(db) for d in dots], lag_ratio=0.15),
                      val.animate(rate_func=linear).set_value(1041 + len(dots)), FadeIn(notes[0]), run_time=3.0)
            self.remove(*dots)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeOut(asks), db.animate.fade(0.7), LaggedStart(*[FadeIn(g, shift=LEFT * 0.1) for g in gens],
                                                                       lag_ratio=0.15), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ UUIDv4 and the birthday bound
    def random(self):
        ids = load("ids")
        rows = load("birthday")["rows"]
        head = label(r"122 random bits", font_size=36).to_edge(UP, buff=0.3)
        u4 = VGroup(*[coloured(s, [(14, 15, HEAD), (19, 20, LAM)], size=20) for s in ids["uuid4"]]).arrange(
            DOWN, buff=0.18, aligned_edge=LEFT).move_to([-3.3, 2.0, 0])
        keyl = VGroup(label(r"version 4", font_size=18, color=HEAD), label(r"variant bits", font_size=18,
                                                                           color=LAM)).arrange(RIGHT, buff=0.5)
        keyl.next_to(u4, DOWN, buff=0.2)
        bits = label(r"128 bits \ $-$ \ 6 fixed \ $=$ \ 122 random", font_size=22, color=WHITE).next_to(
            keyl, DOWN, buff=0.3)
        formula = MathTex(r"P(\text{any collision among } n) \;\approx\; 1 - e^{-n^2 / 2^{123}}", font_size=32,
                          color=HEAD).move_to([-3.3, -1.0, 0])
        fl = label(r"the birthday bound \ (Part 17), \ with $2^{122}$ possible IDs", font_size=18,
                   color=GREY_A).next_to(formula, DOWN, buff=0.2)
        tab = grid_table([r"IDs made, \ $n$", r"chance of any collision"],
                         [[sci(r["n"]), sci(r["p"]) if r["p"] < 0.01 else rf"{100 * r['p']:.1f}\%"] for r in rows],
                         widths=[2.4, 3.2], row_h=0.6, font_size=22,
                         colors=[[WHITE, YES]] * (len(rows) - 1) + [[WHITE, NO]], mono_cols=())
        tab.move_to([3.8, 0.9, 0])
        tnote = wrapped_label(r"in practice, \ a broken random number generator is far likelier than bad luck", 5.4,
                              font_size=19, color=NO).next_to(tab, DOWN, buff=0.5).align_to(tab, LEFT)
        foot = note(r"probabilities computed; \ the three IDs are generated examples", font_size=16).to_edge(
            DOWN, buff=0.15)
        with self.voiceover(
            "The simplest way to need no one is to choose at random. <bookmark mark='a'/> A version four UUID has "
            "a hundred and twenty-eight bits, six of them fixed to mark its version and variant, leaving a hundred "
            "and twenty-two random. <bookmark mark='b'/> Part 17's birthday bound gives the chance that any two "
            "of n such IDs collide: about one minus e to the minus n squared over two to the hundred and "
            "twenty-three. <bookmark mark='c'/> A billion IDs: about one chance in ten to the nineteen. A million "
            "million: one in ten to the thirteen. Even at a thousand million million, about one in ten million. "
            "Only near two point seven billion billion are the odds even. <bookmark mark='d'/> In practice, a "
            "broken random number generator is far likelier than bad luck."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot), LaggedStart(*[FadeIn(u) for u in u4], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(keyl), FadeIn(bits))
            vo.wait_until("b")
            self.play(Write(formula), FadeIn(fl), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*r), shift=RIGHT * 0.15) for r in tab.cells[1:]], lag_ratio=0.6),
                      run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(tnote))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Snowflake and UUIDv7
    def layout(self):
        ids = load("ids")
        head = label(r"Time first", font_size=36).to_edge(UP, buff=0.3)
        spans, a = [], 0
        for n, _, c in FIELDS:
            spans.append((a, a + n, c))
            a += n
        bins = VGroup(*[coloured(b, spans, size=16) for b in ids["snowflake_bin"]]).arrange(
            DOWN, buff=0.12, aligned_edge=LEFT).move_to([0, 1.35, 0])
        bw = bins[0].width / 64
        x0 = bins[0].get_left()[0]
        bar, tags = VGroup(), VGroup()
        for (lo, hi, c), (_, txt, _) in zip(spans, FIELDS):
            r = Rectangle(width=bw * (hi - lo), height=0.32, stroke_color=BG, stroke_width=1.5, fill_color=c,
                          fill_opacity=0.75)
            r.move_to([x0 + bw * (lo + hi) / 2, 2.2, 0])
            bar.add(r)
            t = label(txt, font_size=18, color=c).next_to(r, UP, buff=0.1)
            if hi - lo == 1:
                t.next_to(r, LEFT, buff=0.1)
            tags.add(t)
        years = 2 ** 41 / 1000 / 86400 / 365.25
        derived = label(rf"$2^{{41}}$ ms $\approx$ {years:.1f} years; \ $2^{{12}} = {2 ** 12:,}$ IDs per "
                        rf"millisecond per machine; \ $2^{{10}} = {2 ** 10:,}$ machines", font_size=20,
                        color=WHITE).next_to(bins, DOWN, buff=0.3)
        sf = label(r"Snowflake \ (Twitter, \ 2010): \ three IDs, \ one millisecond apart, \ machine 7",
                   font_size=18, color=GREY_A).next_to(derived, DOWN, buff=0.2)
        u7 = VGroup(*[coloured(s, [(0, 8, DATA), (9, 13, DATA), (14, 15, HEAD)], size=20) for s in ids["uuid7"]])
        u7.arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([-3.2, -1.95, 0])
        u7t = label(r"UUIDv7 \ (RFC 9562, \ 2024)", font_size=21, color=DATA).next_to(u7, UP, buff=0.2).align_to(
            u7, LEFT)
        u7n = VGroup(
            wrapped_label(r"48 bits of Unix milliseconds first, \ then the version, \ then 74 random bits", 5.6,
                          font_size=19, color=DATA),
            wrapped_label(rf"sorted as strings, \ they are in creation order: \ "
                          rf"{'yes' if ids['sorted_uuid7'] else 'no'}; \ no machine numbers to assign", 5.6,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, -1.85, 0])
        with self.voiceover(
            "Random IDs scatter; often we want them to sort by time. <bookmark mark='a'/> Twitter's Snowflake, "
            "from 2010, packs sixty-four bits: forty-one bits of milliseconds since a chosen epoch, ten bits "
            "naming the machine, and twelve bits counting within the millisecond. <bookmark mark='b'/> Here are "
            "three, made one millisecond apart on machine seven: the time field ticks, and the sequence counts. "
            "<bookmark mark='c'/> Forty-one bits of milliseconds last about seventy years, and each machine can "
            "mint four thousand and ninety-six IDs a millisecond, with no coordination beyond handing out machine "
            "numbers. <bookmark mark='d'/> UUID version seven, standardised in RFC 9562 in 2024, does the same "
            "in a hundred and twenty-eight bits: forty-eight bits of Unix milliseconds first, then seventy-four "
            "random bits. The IDs sort by creation time, and need no machine numbers at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r, LEFT), FadeIn(t)) for r, t in zip(bar, tags)],
                                  lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(sf), LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in bins], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(derived))
            vo.wait_until("d")
            self.play(FadeIn(u7t), LaggedStart(*[FadeIn(u) for u in u7], lag_ratio=0.3), FadeIn(u7n[0]))
            self.play(FadeIn(u7n[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ clocks that step back
    def skew(self):
        head = label(r"When the clock steps back", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 12, 2], y_range=[996, 1008, 2], x_length=5.6, y_length=3.6,
                  axis_config={"color": GREY_D, "include_ticks": False}).move_to([-3.4, -0.1, 0])
        xl = label(r"true time", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"the machine's clock, \ ms", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(
            ax, LEFT)
        seg1 = Line(ax.c2p(0, 997), ax.c2p(7, 1004), color=DATA, stroke_width=3)
        step = DashedLine(ax.c2p(7, 1004), ax.c2p(7, 999), color=NO, stroke_width=2)
        seg2 = Line(ax.c2p(7, 999), ax.c2p(12, 1004), color=DATA, stroke_width=3)
        st = label(r"time daemon steps it back 5 ms", font_size=17, color=NO).next_to(step, RIGHT, buff=0.1).shift(
            UP * 0.6)
        lvl = DashedLine(ax.c2p(0, 1003), ax.c2p(12, 1003), color=HEAD, stroke_width=1.5)
        d1, d2 = Dot(ax.c2p(6, 1003), radius=0.08, color=HEAD), Dot(ax.c2p(11, 1003), radius=0.08, color=NO)
        l1 = label(r"ID (1003, \ 0)", font_size=17, color=HEAD).next_to(d1, UL, buff=0.08)
        l2 = label(r"ID (1003, \ 0) \ again", font_size=17, color=NO).next_to(d2, DOWN, buff=0.15).shift(LEFT * 0.4)
        code = code_block([
            "now = max(clock_ms(), last)   # never step back",
            "seq = seq + 1 if now == last else 0",
            "if seq == 4096:               # used up: wait",
            "    now, seq = next_ms(last), 0",
            "last = now",
        ], size=16).move_to([3.5, 1.4, 0])
        notes = VGroup(
            wrapped_label(r"remember the last timestamp issued, \ and never go below it", 5.8, font_size=19,
                          color=YES),
            wrapped_label(r"across machines, \ clocks disagree \ (Part 38): \ IDs are ordered only to within the "
                          r"skew; \ sort and page by them, \ never decide which write came first", 5.8,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(code, DOWN, buff=0.4).align_to(code, LEFT)
        foot = note(r"illustrative", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Time-ordered IDs inherit the troubles of clocks, Part 38's subject. <bookmark mark='a'/> Suppose the "
            "time daemon steps a machine's clock back five milliseconds. <bookmark mark='b'/> The generator sees a "
            "millisecond it has already used, restarts its sequence at zero, and mints an ID it minted before. "
            "<bookmark mark='c'/> The fix is to remember the last timestamp issued and never go below it: keep "
            "counting within that millisecond, and wait when the sequence runs out. <bookmark mark='d'/> Across "
            "machines, clocks disagree as well, so IDs from different machines are ordered only to within the skew "
            "between them. Sort and page by them, but never use them to decide which of two writes came first."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(foot))
            self.play(Create(seg1), run_time=1.5)
            self.play(FadeIn(lvl), FadeIn(d1), FadeIn(l1))
            vo.wait_until("a")
            self.play(Create(step), FadeIn(st))
            self.play(Create(seg2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(d2), FadeIn(l2), Indicate(d2, color=NO))
            vo.wait_until("c")
            self.play(FadeIn(code), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ index locality
    def locality(self):
        b = load("btree")
        R, O = b["random"], b["ordered"]
        head = label(r"Ordered keys and the index", font_size=36).to_edge(UP, buff=0.3)
        n_pages, pw, ph = 16, 0.46, 0.9
        # illustrative fill levels: random keys leave pages between half and full
        rnd_fill = [0.55, 0.8, 0.62, 0.95, 0.5, 0.7, 0.85, 0.6, 0.75, 0.52, 0.9, 0.66, 0.58, 0.82, 0.7, 0.6]

        def pages(fills, color):
            g = VGroup()
            for f in fills:
                frame = Rectangle(width=pw, height=ph, stroke_color=GREY_C, stroke_width=1.3)
                lvl = Rectangle(width=pw - 0.06, height=max(0.02, (ph - 0.06) * f), stroke_width=0,
                                fill_color=color, fill_opacity=0.7)
                lvl.align_to(frame, DOWN).shift(UP * 0.03)
                g.add(VGroup(frame, lvl))
            return g.arrange(RIGHT, buff=0.08)
        rp = pages(rnd_fill, NO)
        op = pages([1.0] * (n_pages - 1) + [0.3], YES)
        VGroup(rp, op).arrange(DOWN, buff=0.9).move_to([-2.2, 0.75, 0])
        rl = label(r"random keys \ (UUIDv4)", font_size=20, color=NO).next_to(rp, UP, buff=0.12).align_to(rp, LEFT)
        ol = label(r"time-ordered keys \ (UUIDv7, \ Snowflake)", font_size=20, color=YES).next_to(
            op, UP, buff=0.12).align_to(op, LEFT)
        targets = [3, 11, 7, 0, 14, 5, 9, 12]
        rdots = [Dot(rp.get_top() + UP * 0.6, radius=0.06, color=HEAD) for _ in targets]
        odots = [Dot(op.get_top() + UP * 0.5, radius=0.06, color=HEAD) for _ in targets]
        tab = grid_table([r"", r"random", r"time-ordered"],
                         [[r"leaf pages", f"{R['pages']:,}", f"{O['pages']:,}"],
                          [r"fill", rf"{100 * R['fill']:.0f}\%", rf"{100 * O['fill']:.0f}\%"],
                          [r"pages touched, \ last 10,000 inserts", f"{R['pages_touched_last_10000']:,}",
                           f"{O['pages_touched_last_10000']:,}"]],
                         widths=[4.0, 1.6, 2.0], row_h=0.5, font_size=20, colors=[[WHITE, NO, YES]] * 3,
                         mono_cols=())
        tab.move_to([-2.4, -2.45, 0])
        notes = VGroup(
            wrapped_label(r"a random insert needs its page in memory: \ the whole tree is the working set \ "
                          r"(Part 9, \ Part 35's buffer pool)", 4.4, font_size=19, color=WHITE),
            wrapped_label(r"the price: \ the rightmost page, \ or chapter 8's last range shard, \ is the hot spot; "
                          r"\ and every ID tells when it was made", 4.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.6, 0.2, 0])
        foot = note(r"200,000 inserts, \ 100 keys a page, \ computed; \ pages drawn illustrative", font_size=16)
        foot.to_edge(DOWN, buff=0.1).set_x(4.6)
        with self.voiceover(
            "Ordered IDs pay off in the index, Part 17's B-tree. <bookmark mark='a'/> Insert two hundred thousand "
            "keys into the leaf level of a B-plus tree, a hundred keys to a page. Random keys land all over the "
            "tree and split pages in half, leaving them sixty-nine percent full: two thousand eight hundred and "
            "eighty-nine pages. <bookmark mark='b'/> Time-ordered keys only ever touch the rightmost page, so "
            "every page fills completely: two thousand pages. <bookmark mark='c'/> The bigger difference is the "
            "working set. The last ten thousand random inserts touched two thousand seven hundred and thirty "
            "pages, nearly the whole tree, all of which must stay in memory; ordered inserts touched a hundred and "
            "one. <bookmark mark='d'/> The price: the rightmost page, or chapter eight's last range shard, becomes "
            "the hot spot, and every ID reveals when it was made."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rl), FadeIn(rp), FadeIn(ol), FadeIn(op), FadeIn(foot),
                      FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            vo.wait_until("a")
            self.add(*rdots)
            self.play(LaggedStart(*[d.animate.move_to(rp[t][0].get_center()) for d, t in zip(rdots, targets)],
                                  lag_ratio=0.2), run_time=2.5)
            self.play(*[FadeOut(d) for d in rdots], *[Indicate(rp[t], color=NO) for t in targets])
            self.play(FadeIn(tab.cells[1][0]), FadeIn(tab.cells[1][1]), FadeIn(tab.cells[2][0]),
                      FadeIn(tab.cells[2][1]))
            vo.wait_until("b")
            self.add(*odots)
            self.play(LaggedStart(*[d.animate.move_to(op[-1][0].get_center()) for d in odots], lag_ratio=0.2),
                      op[-1][1].animate.stretch_to_fit_height(ph - 0.06).align_to(op[-1][0], DOWN).shift(UP * 0.03),
                      run_time=2.5)
            self.play(*[FadeOut(d) for d in odots], FadeIn(tab.cells[1][2]), FadeIn(tab.cells[2][2]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[3])), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]), Indicate(op[-1], color=HEAD))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM)
