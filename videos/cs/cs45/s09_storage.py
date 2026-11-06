from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, mono,
                                   tag_box)


def sci(v: float, digits=1) -> str:
    """A number in TeX scientific notation (plain below a thousand)."""
    if v < 1000:
        return f"{v:.{digits}f}"
    e = math.floor(math.log10(v))
    m = v / 10 ** e
    return rf"${m:.{digits}f}\times 10^{{{e}}}$"


def frag(color, s=0.42):
    return Square(side_length=s, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=0.75)


class Storage(VoiceoverScene):
    def construct(self):
        self.card()
        self.shapes()
        self.consistency()
        self.scatter()
        self.markov()
        self.nines()

    def card(self):
        card = chapter_card(8, r"Object storage and eleven nines", r"How can data outlive every disk that holds it?",
                            lit=(2006, 2020), extra=((2006, r"Amazon S3"),
                                                     (2020, r"S3: \ strong read-after-write")), part=PART)
        with self.voiceover("Chapter eight. Object storage and eleven nines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def shapes(self):
        pr = load("serverless")["prices"]
        head = label(r"Block, \ file, \ object", font_size=36).to_edge(UP, buff=0.3)
        xs = (-4.6, 0.0, 4.6)
        # block: numbered blocks, one being written
        cells = VGroup()
        for i in range(12):
            sq = Square(side_length=0.68, stroke_color=DATA, stroke_width=1.5,
                        fill_color=HEAD if i == 7 else BG, fill_opacity=0.8 if i == 7 else 1)
            cells.add(VGroup(sq, mono(str(i), size=18, color=BLACK if i == 7 else DATA).move_to(sq)))
        cells.arrange_in_grid(rows=3, cols=4, buff=0.08)
        # file: a hierarchy
        tree = code_block(["/", "├── home/", "└── data/", "    └── novels/", "        ├── emma.txt",
                           "        └── persuasion.txt"], size=18, color=LAM)
        # object: a flat map from keys to whole objects
        keys = VGroup()
        for k in ("novels/emma.txt", "novels/persuasion.txt", "logs/2024-06-01"):
            t = tag_box(k, color=YES, size=16, w=2.95, h=0.5)
            blob = Rectangle(width=0.5, height=0.5, stroke_width=0, fill_color=YES, fill_opacity=0.55)
            keys.add(VGroup(t, Arrow(ORIGIN, RIGHT * 0.4, buff=0, stroke_width=2, color=GREY_B,
                                     max_tip_length_to_length_ratio=0.35), blob).arrange(RIGHT, buff=0.08))
        keys.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        bucket = SurroundingRectangle(keys, buff=0.18, corner_radius=0.1, color=YES, stroke_width=1.5)
        obj = VGroup(bucket, keys)
        pics = [cells, tree, obj]
        titles = [(r"block", DATA), (r"file", LAM), (r"object", YES)]
        ops = [r"read or write block 7, \ in place", r"open, \ seek, \ overwrite, \ rename, \ lock",
               r"PUT, \ GET or DELETE a whole object, \ by key, \ over HTTP"]
        notes = [r"a disk attached to one machine \ (Part 34), \ offered over the network",
                 r"names in a hierarchy, \ shared between machines, \ with locking to match",
                 r"no edits in place; \ the slashes in a key are only characters; \ scales almost without limit"]
        cols = []
        for x, pic, (t, c), op, nt in zip(xs, pics, titles, ops, notes):
            tl = label(t, font_size=26, color=c)
            pic.move_to([x, 0.9, 0])
            tl.move_to([x, 2.6, 0])
            o = wrapped_label(op, 4.0, font_size=21, color=c).move_to([x, -1.15, 0])
            n = wrapped_label(nt, 4.0, font_size=19, color=GREY_A).next_to(o, DOWN, buff=0.3)
            cols.append(VGroup(tl, pic, o, n))
        price = label(rf"S3 Standard: \ \${pr['s3 standard per GB-month']:.3f} per gigabyte-month \ "
                      rf"({pr['date']})", font_size=20, color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Clouds sell storage in three shapes. <bookmark mark='a'/> Block storage is a disk: "
            "numbered blocks, read and written in place, attached to one machine; Part 34's disk, "
            "over the network. <bookmark mark='b'/> File storage adds names in a hierarchy, and lets "
            "programs open a file, seek and overwrite bytes in the middle, with locking for sharing. "
            "<bookmark mark='c'/> Object storage gives most of that up. A bucket maps keys to whole "
            "objects, which you put, get or delete over HTTP. Nothing is edited in place, and the "
            "slashes in a key are just characters. <bookmark mark='d'/> In return it scales almost "
            "without limit, and it is cheap: about two point three cents a gigabyte a month, at "
            "Amazon's 2024 list price."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abc", cols):
                vo.wait_until(mk)
                self.play(FadeIn(c[0]), FadeIn(c[1]), FadeIn(c[2]))
                self.play(FadeIn(c[3]), run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(price))
        self.wait(0.4)
        self.clear_scene()

    def consistency(self):
        head = label(r"Read after write", font_size=36).to_edge(UP, buff=0.3)
        yw, yr = 2.0, 0.6
        lanes = VGroup(Line([-4.9, yw, 0], [6.6, yw, 0], color=GREY_D), Line([-4.9, yr, 0], [6.6, yr, 0],
                                                                           color=GREY_D))
        who = VGroup(label(r"writer", font_size=20, color=DATA).next_to([-4.9, yw, 0], LEFT, buff=0.2),
                     label(r"reader", font_size=20, color=LAM).next_to([-4.9, yr, 0], LEFT, buff=0.2))
        put = tag_box("PUT novels/emma.txt (v2)", color=DATA, size=17).move_to([-3.0, yw, 0])
        ok = label(r"succeeds", font_size=19, color=YES).next_to(put, RIGHT, buff=0.3)
        tick = DashedLine([ok.get_right()[0] + 0.25, yw + 0.35, 0], [ok.get_right()[0] + 0.25, yr - 2.2, 0],
                          color=GREY_B, dash_length=0.08)
        get = tag_box("GET novels/emma.txt", color=LAM, size=17).next_to([tick.get_x(), yr, 0], RIGHT, buff=0.4)
        old = VGroup(tag_box("v1", color=NO, size=17),
                     wrapped_label(r"2006--2020: \ after an overwrite, \ a read could still return the old "
                                   r"version for a while", 4.4, font_size=19, color=NO)).arrange(RIGHT, buff=0.25)
        new = VGroup(tag_box("v2", color=YES, size=17),
                     wrapped_label(r"since December 2020: \ every later GET and LIST sees the write", 4.4,
                                   font_size=19, color=YES)).arrange(RIGHT, buff=0.25)
        old.next_to(get, DOWN, buff=0.45).align_to(get, LEFT)
        new.next_to(old, DOWN, buff=0.35).align_to(get, LEFT)
        for g in (old, new):
            if g.get_right()[0] > 6.8:
                g.shift(LEFT * (g.get_right()[0] - 6.8))
        arr = VGroup(Arrow(get.get_bottom(), old[0].get_top(), buff=0.05, stroke_width=2, color=NO,
                           max_tip_length_to_length_ratio=0.25))
        lines = VGroup(
            wrapped_label(r"each update to one key is atomic; \ when two writers race, \ the later one wins; \ there "
                          r"are no transactions across keys", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"Part 46 builds tables, \ with snapshots and atomic commits, \ on exactly these "
                          r"guarantees", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "What does a read see? <bookmark mark='a'/> A writer's put succeeds, and then a reader "
            "asks for the object. <bookmark mark='b'/> For its first fourteen years, S3 showed a "
            "brand-new key at once in most cases, but an overwrite or delete could take a while to appear: eventual "
            "consistency, from Part 39. <bookmark mark='c'/> In December 2020, Amazon made every read "
            "strongly consistent: once a put or delete succeeds, every later get and listing reflects "
            "it. <bookmark mark='d'/> Each update to a key is atomic, the later of two racing writers "
            "wins, and there are no transactions across keys. Part 46 builds whole tables on exactly "
            "these guarantees."
        ) as vo:
            self.play(FadeIn(head), Create(lanes), FadeIn(who))
            vo.wait_until("a")
            self.play(FadeIn(put, shift=RIGHT * 0.2))
            self.play(FadeIn(ok), Create(tick))
            self.play(FadeIn(get, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(Create(arr), FadeIn(old))
            vo.wait_until("c")
            self.play(arr.animate.become(Arrow(get.get_bottom(), new[0].get_top(), buff=0.05, stroke_width=2,
                                               color=YES, max_tip_length_to_length_ratio=0.15)),
                      old.animate.set_opacity(0.35), FadeIn(new))
            vo.wait_until("d")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self):
        d = {r["name"]: r for r in load("durability")["schemes"]}
        c = load("correlated")
        rs, three = d["RS(10, 4)"], d["three copies"]
        n, k, racks = rs["n"], rs["k"], c["racks"]
        assert n % racks == 0
        head = label(r"Fragments across failure domains", font_size=36).to_edge(UP, buff=0.3)
        whole = Rectangle(width=6.0, height=0.42, stroke_width=0, fill_color=DATA, fill_opacity=0.75).move_to(
            [0, 2.45, 0])
        wl = label(r"one object", font_size=18, color=DATA).next_to(whole, LEFT, buff=0.2)
        frs = VGroup(*[frag(DATA if i < k else LAM) for i in range(n)]).arrange(RIGHT, buff=0.08).move_to(
            [-0.9, 1.75, 0])
        fl = VGroup(label(rf"{k} data fragments", font_size=17, color=DATA).next_to(frs[:k], UP, buff=0.1),
                    label(rf"{n - k} parity", font_size=17, color=LAM).next_to(frs[k:], UP, buff=0.1))
        rl = wrapped_label(rf"any {k} of the {n} rebuild the object \ (Reed--Solomon, \ Part 28)", 3.0,
                           font_size=19, color=GREY_A).next_to(frs, RIGHT, buff=0.3)
        boxes = VGroup(*[RoundedRectangle(width=1.5, height=2.1, corner_radius=0.08, stroke_color=GREY_B,
                                          stroke_width=1.5) for _ in range(racks)]).arrange(RIGHT, buff=0.3)
        boxes.move_to([0, -0.5, 0])
        names = VGroup(*[label(rf"rack {r + 1}", font_size=17, color=GREY_B).next_to(b, DOWN, buff=0.1)
                         for r, b in enumerate(boxes)])
        # fragment i goes to rack i mod racks, so parity and data mix
        slots = {i: boxes[i % racks].get_center() + UP * (0.45 - 0.9 * (i // racks)) for i in range(n)}
        moves = [frs[i].animate.scale(1.35).move_to(slots[i]) for i in range(n)]

        def x_over(i):
            return Cross(scale_factor=0.2, stroke_color=NO, stroke_width=5).move_to(slots[i])
        one = 1
        x1 = x_over(one)
        rack_down = 4
        lost_rack = [i for i in range(n) if i % racks == rack_down]
        extra_lost = [0, 13]
        lost = lost_rack + extra_lost
        assert len(lost) == n - k and len(set(lost)) == len(lost)
        rack_x = Cross(boxes[rack_down], stroke_color=NO, stroke_width=5)
        xs = VGroup(*[x_over(i) for i in extra_lost])
        left = label(rf"{n - len(lost)} of {n} fragments left: \ still readable", font_size=22, color=YES)
        lines = VGroup(
            wrapped_label(rf"{n - k} losses tolerated at {rs['overhead']:.1f}$\times$ the data, \ against "
                          rf"{three['n'] - three['k']} for three copies at {three['overhead']:.0f}$\times$", 12.4,
                          font_size=21, color=HEAD),
        ).to_edge(DOWN, buff=0.4)
        left.next_to(lines, UP, buff=0.3)
        with self.voiceover(
            "How can an object outlive its disks? <bookmark mark='a'/> Cut it into ten data fragments "
            "and compute four of parity with a Reed–Solomon code, from Part 28: any ten of the "
            "fourteen rebuild it. <bookmark mark='b'/> Then scatter the fragments across failure "
            "domains, here two to a rack in seven racks, so that no disk, rack or power feed holds "
            "too many. <bookmark mark='c'/> A disk fails; the system rebuilds its fragment elsewhere "
            "from ten survivors. <bookmark mark='d'/> Even a whole rack lost, with two more disks, "
            "leaves ten, and the object survives. <bookmark mark='e'/> Three full copies tolerate "
            "only two losses and store three times the data; this code tolerates four, at one point "
            "four times."
        ) as vo:
            self.play(FadeIn(head), FadeIn(whole), FadeIn(wl))
            vo.wait_until("a")
            self.play(ReplacementTransform(whole, frs), FadeOut(wl), FadeIn(fl), run_time=1.5)
            self.play(FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(boxes), FadeIn(names))
            self.play(LaggedStart(*moves, lag_ratio=0.12), FadeOut(fl), run_time=3)
            self.play(rl.animate.move_to([0, 1.75, 0]))
            vo.wait_until("c")
            self.play(Create(x1), frs[one].animate.set_opacity(0.15))
            self.play(FadeOut(x1), frs[one].animate.set_fill(opacity=0.75).set_stroke(WHITE, 3, opacity=1))
            self.play(frs[one].animate.set_stroke(DATA, 1.5))
            vo.wait_until("d")
            self.play(Create(rack_x), *[frs[i].animate.set_opacity(0.15) for i in lost_rack])
            self.play(Create(xs), *[frs[i].animate.set_opacity(0.15) for i in extra_lost])
            self.play(FadeIn(left))
            vo.wait_until("e")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def markov(self):
        dur = load("durability")
        d = {r["name"]: r for r in dur["schemes"]}
        three = d["three copies"]
        chk = dur["check"]
        head = label(r"Mean time to data loss", font_size=36).to_edge(UP, buff=0.3)
        xs = (-4.2, -1.4, 1.4, 4.2)
        y = 1.55
        states = VGroup()
        for i, x in enumerate(xs):
            col = NO if i == 3 else (YES if i == 0 else HEAD)
            c = Circle(radius=0.48, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.12)
            states.add(VGroup(c, label(str(i), font_size=26, color=col).move_to(c)).move_to([x, y, 0]))
        sl = VGroup(label(r"failed fragments", font_size=17, color=GREY_A).next_to(states[0], LEFT, buff=0.2),
                    label(r"data lost", font_size=17, color=NO).next_to(states[3], RIGHT, buff=0.2))
        fwd, back = VGroup(), VGroup()
        for i in range(3):
            a = CurvedArrow(states[i].get_top() + RIGHT * 0.2, states[i + 1].get_top() + LEFT * 0.2, angle=-0.9,
                            color=HEAD, stroke_width=2.5, tip_length=0.18)
            fwd.add(VGroup(a, MathTex(rf"{3 - i}\lambda", font_size=30, color=HEAD).next_to(a, UP, buff=0.08)))
        for i in (1, 2):
            a = CurvedArrow(states[i].get_bottom() + LEFT * 0.2, states[i - 1].get_bottom() + RIGHT * 0.2,
                            angle=-0.9, color=YES, stroke_width=2.5, tip_length=0.18)
            back.add(VGroup(a, MathTex(r"\mu", font_size=30, color=YES).next_to(a, DOWN, buff=0.08)))
        assume = label(r"three copies; \ each fails at 2\% a year, \ independently; \ one repair at a time, \ a day "
                       r"each \ (a model)", font_size=18, color=GREY_A).next_to(states, UP, buff=0.75)
        eq1 = MathTex(r"T_i = \frac{1 + \mu\, T_{i-1}}{(n-i)\,\lambda}", font_size=40, color=WHITE)
        eq2 = MathTex(r"\text{MTTDL} = \sum_{i=0}^{n-k} T_i", font_size=40, color=WHITE)
        eqs = VGroup(eq1, eq2).arrange(RIGHT, buff=1.4).move_to([0, -1.05, 0])
        why = label(r"$T_i$: \ expected time to go from $i$ failures to $i+1$; \ a repair first means climbing "
                    r"again", font_size=18, color=GREY_B).next_to(eqs, DOWN, buff=0.2)
        res = label(rf"three copies: \ about {three['mttdl_years'] / 1e9:.1f} billion years", font_size=24,
                    color=YES).next_to(why, DOWN, buff=0.3)
        mc = label(rf"Monte Carlo of the same chain, \ rates exaggerated: \ {chk[0]['simulated_years']:.0f} against "
                   rf"{chk[0]['exact_years']:.0f} years exact; \ {chk[1]['simulated_years']:.1f} against "
                   rf"{chk[1]['exact_years']:.1f} for any 4 of 6", font_size=17, color=GREY_B).to_edge(DOWN,
                                                                                               buff=0.3)
        with self.voiceover(
            "How long until data is lost? <bookmark mark='a'/> Model it as a Markov chain whose state "
            "counts the failed fragments. Each live one fails at rate lambda, two percent a year "
            "here, independently; a failed one is repaired at rate mu, in about a day. <bookmark "
            "mark='b'/> For three copies, the chain moves right at three lambda, then two lambda, "
            "then lambda, and the last state loses the data. <bookmark mark='c'/> From each damaged "
            "state, repair pulls it back. <bookmark mark='d'/> The expected time to climb each step, "
            "allowing for repairs that send us back, obeys this recurrence, and the mean time to data "
            "loss is the sum of the steps. <bookmark mark='e'/> For three copies: about 2.7 billion "
            "years. <bookmark mark='f'/> A simulation of the same chain, with exaggerated rates, "
            "agrees within two percent."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(states), FadeIn(sl), FadeIn(assume))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(f[0]) for f in fwd], lag_ratio=0.4), FadeIn(VGroup(*[f[1] for f in fwd])),
                      run_time=2)
            vo.wait_until("c")
            self.play(*[Create(b[0]) for b in back], FadeIn(VGroup(*[b[1] for b in back])))
            vo.wait_until("d")
            self.play(Write(eq1), FadeIn(why))
            self.play(Write(eq2))
            vo.wait_until("e")
            self.play(FadeIn(res, shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(mc))
        self.wait(0.4)
        self.clear_scene()

    def nines(self):
        rows_d = load("durability")["schemes"]
        head = label(r"Eleven nines", font_size=36).to_edge(UP, buff=0.3)
        nice = {"RS(6, 3)": r"6 data $+$ 3 parity", "RS(10, 4)": r"10 data $+$ 4 parity",
                "RS(10, 6)": r"10 data $+$ 6 parity"}
        rows, cols = [], []
        for r in rows_d:
            rows.append([nice.get(r["name"], r["name"]), rf"{r['overhead']:.1f}$\times$", f"{r['n'] - r['k']}",
                         sci(r["mttdl_years"]), f"{r['nines']:.1f}"])
            cols.append([YES if r["name"] == "RS(6, 3)" else WHITE] * 5)
        tab = grid_table([r"scheme", r"stored", r"losses survived", r"mean years to loss", r"nines a year"], rows,
                         widths=[3.2, 1.2, 2.1, 2.6, 1.6], row_h=0.6, font_size=21, mono_cols=(), colors=cols)
        tab.move_to([-1.0, 0.7, 0])
        bars = VGroup()
        x_b = tab.get_right()[0] + 0.25
        for i, r in enumerate(rows_d):
            w = r["nines"] / 20 * 1.7
            y_c = tab.cells[i + 1][0].get_y()
            col = YES if r["name"] == "RS(6, 3)" else (NO if r["n"] - r["k"] < 2 else DATA)
            bars.add(Rectangle(width=w, height=0.34, stroke_width=0, fill_color=col, fill_opacity=0.8)
                     .move_to([x_b + w / 2, y_c, 0]))
        eleven = DashedLine([x_b + 11 / 20 * 1.7, tab.cells[1][0].get_y() + 0.3, 0],
                            [x_b + 11 / 20 * 1.7, tab.cells[-1][0].get_y() - 0.3, 0], color=HEAD,
                            dash_length=0.06)
        el = label(r"11", font_size=16, color=HEAD).next_to(eleven, UP, buff=0.05)
        lines = VGroup(
            wrapped_label(r"S3 is designed for eleven nines a year: \ store ten million objects, \ and expect to lose "
                          r"one about every ten thousand years \ (AWS)", 12.4, font_size=19, color=HEAD),
            wrapped_label(r"every row assumes independent failures, \ 2\% a year and a day's repair: \ chapter 13 "
                          r"shows where the nines go when racks fail together", 12.4, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now compare schemes. <bookmark mark='a'/> One copy is lost with a two percent chance a "
            "year: under two nines. Each failure a scheme can absorb multiplies the mean time by "
            "thousands, because a repair takes a day and a disk lasts decades: two copies give about five "
            "point seven nines, three about nine point four. <bookmark mark='b'/> Erasure codes do "
            "better for less: six data fragments plus three of parity reach eleven nines, at one and "
            "a half times the data. <bookmark mark='c'/> Amazon designs S3 for eleven nines: store "
            "ten million objects, and expect to lose one about every ten thousand years. <bookmark "
            "mark='d'/> But all of this assumes independent failures. Chapter thirteen shows what "
            "happens when they are not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            vo.wait_until("a")
            for i in range(1, 4):
                self.play(FadeIn(VGroup(*tab.cells[i])), GrowFromEdge(bars[i - 1], LEFT), run_time=0.8)
            vo.wait_until("b")
            self.play(Create(eleven), FadeIn(el))
            for i in range(4, 7):
                self.play(FadeIn(VGroup(*tab.cells[i])), GrowFromEdge(bars[i - 1], LEFT), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM)
