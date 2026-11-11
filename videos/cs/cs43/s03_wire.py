from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, grid_table, load, mono,
                                   tag_box)

FIELD_COLORS = (DATA, YES, HEAD, LAM, KERN, GREY_A)


def hexpairs(h: str) -> list[str]:
    return [h[i:i + 2] for i in range(0, len(h), 2)]


def split_fields(buf: bytes) -> list[bytes]:
    """Cut an encoded message into its fields, for display: a tag, then a varint or a length and that many bytes."""
    out, i = [], 0

    def varint_end(j):
        while buf[j] & 0x80:
            j += 1
        return j + 1
    while i < len(buf):
        start = i
        wt = buf[i] & 7
        i = varint_end(i)
        if wt == 0:
            i = varint_end(i)
        elif wt == 2:
            n, j, shift = 0, i, 0
            i = varint_end(i)
            while j < i:
                n |= (buf[j] & 0x7F) << shift
                shift += 7
                j += 1
            i += n
        out.append(buf[start:i])
    return out


def bitrow(bits: str, color, size=26, first=None):
    """A row of binary digits; ``first`` colours the leading digit (a continuation bit)."""
    g = VGroup(*[mono(b, size=size, color=color) for b in bits]).arrange(RIGHT, buff=0.06)
    if first is not None:
        g[0].set_color(first)
    return g


class Wire(VoiceoverScene):
    def construct(self):
        self.card()
        self.doubles()
        self.varint()
        self.tags()
        self.zigzag()
        self.compare()

    def card(self):
        card = chapter_card(2, r"Bytes on the wire", r"What does a message look like as bytes?",
                            lit=(2006, 2008), extra=((2006, r"JSON: \ RFC 4627"),
                                                     (2008, r"Protocol Buffers open-sourced")), part=PART)
        with self.voiceover("Chapter two. Bytes on the wire."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def doubles(self):
        d = load("doubles")
        rows = d["rows"][:4]
        two53 = 2 ** 53
        head = label(r"JSON's numbers are doubles", font_size=36).to_edge(UP, buff=0.3)
        xs = [-4.5, -1.5, 1.5, 4.5]
        y = 1.75
        line = Line([-6.0, y, 0], [6.0, y, 0], color=GREY_C, stroke_width=2)
        reps = {r["received"] for r in d["rows"]}
        dots, names = VGroup(), VGroup()
        for x, r in zip(xs, rows):
            ok = r["sent"] in reps
            dots.add(Dot([x, y, 0], radius=0.1, color=YES) if ok else
                     Circle(radius=0.1, color=NO, stroke_width=3).move_to([x, y, 0]))
            off = r["sent"] - two53
            t = r"$2^{53}$" + (rf"$\,{'+' if off > 0 else '-'}\,{abs(off)}$" if off else "")
            names.add(label(t, font_size=22, color=YES if ok else NO).next_to([x, y, 0], DOWN, buff=0.25))
        spans = VGroup(
            label(r"up to $2^{53}$: \ every integer", font_size=18, color=GREY_A).move_to([(xs[0] + xs[1]) / 2,
                                                                                       y - 0.95, 0]),
            label(r"beyond: \ every second one", font_size=18, color=GREY_A).move_to([(xs[2] + xs[3]) / 2,
                                                                                    y - 0.95, 0]),
        )
        sent = Dot([xs[2], y + 0.7, 0], radius=0.12, color=HEAD)
        sl = label(r"sent", font_size=18, color=HEAD).next_to(sent, RIGHT, buff=0.12)
        ex = d["example"]
        s, r_ = str(ex["sent"]), str(ex["received"])
        k = next(i for i in range(len(s)) if s[i] != r_[i])
        ulp = 2 ** (ex["sent"].bit_length() - 53)

        def num(txt, col):
            return VGroup(mono(txt[:k], size=24, color=WHITE), mono(txt[k:], size=24, color=col)).arrange(
                RIGHT, buff=0.02)
        idrow = VGroup(
            VGroup(label(r"an id, \ sent:", font_size=21, color=GREY_A), num(s, YES)).arrange(RIGHT, buff=0.3),
            VGroup(label(r"read by JavaScript:", font_size=21, color=GREY_A), num(r_, NO)).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.2).move_to([-1.6, -0.55, 0])
        ul = label(rf"doubles there are {ulp} apart", font_size=19, color=NO).next_to(idrow, RIGHT, buff=0.4)
        notes = VGroup(
            wrapped_label(r"JSON says nothing about precision; \ JavaScript reads every number as a 64-bit double "
                          r"\ (Part 4): \ 53 significant bits", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"so large ids travel as strings, \ as text the reader parses itself; \ RFC 8259 \ (2017) \ "
                          r"warns that integers beyond $\pm(2^{53}-1)$ may not survive", 12.4, font_size=20,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Start with the most common format of all. JSON writes numbers as decimal text and says nothing "
            "about precision, but JavaScript reads every number as a double, Part 4's sixty-four-bit float, with"
            " fifty-three significant bits. <bookmark mark='a'/> Up to two to the fifty-three, every integer is "
            "exact; above it, doubles are two apart. <bookmark mark='b'/> So two to the fifty-three plus one "
            "arrives as two to the fifty-three: it lies halfway, and rounds to the even neighbour. <bookmark "
            "mark='c'/> A nineteen-digit id is worse. Near a billion billion, doubles are two hundred and fifty-"
            "six apart, and the last digits change. <bookmark mark='d'/> So APIs send large ids as strings, and "
            "the JSON standard warns that larger integers may not survive."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dd) for dd in dots], lag_ratio=0.2), FadeIn(names), FadeIn(spans))
            vo.wait_until("b")
            self.play(FadeIn(sent, scale=1.4), FadeIn(sl))
            self.play(sent.animate.move_to([xs[2], y, 0]), FadeOut(sl))
            self.play(sent.animate.move_to([xs[1], y, 0]), run_time=1.2)
            self.play(Indicate(names[1], color=HEAD))
            vo.wait_until("c")
            self.play(FadeIn(idrow[0]))
            self.play(TransformFromCopy(idrow[0][1], idrow[1][1]), FadeIn(idrow[1][0]))
            self.play(FadeIn(ul))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def varint(self):
        p = {k: v for k, v, _, _ in load("published")["encodings"]}
        ok = {k: m for k, _, _, m in load("published")["encodings"]}
        g = {k: w for k, _, w, _ in load("published")["encodings"]}
        sz = load("sizes")["unsigned"]
        v = 150
        bits = format(v, "b")
        lo, hi = format(v & 0x7F, "07b"), format(v >> 7, "07b")
        head = label(r"Varints: \ seven bits at a time", font_size=36).to_edge(UP, buff=0.3)
        cx = -3.5
        r1 = VGroup(label(rf"{v} \ $=$", font_size=30, color=WHITE), bitrow(bits, DATA)).arrange(RIGHT, buff=0.3)
        r1.move_to([cx, 2.25, 0])
        ghi, glo = bitrow(hi, LAM), bitrow(lo, DATA)
        VGroup(ghi, glo).arrange(RIGHT, buff=0.6).move_to([cx, 1.25, 0])
        gl = VGroup(label(r"high seven", font_size=16, color=LAM).next_to(ghi, DOWN, buff=0.1),
                    label(r"low seven", font_size=16, color=DATA).next_to(glo, DOWN, buff=0.1))
        b1, b2 = bitrow("1" + lo, DATA, first=HEAD), bitrow("0" + hi, LAM, first=HEAD)
        bytes_ = VGroup(b1, b2).arrange(RIGHT, buff=0.6).move_to([cx, -0.05, 0])
        frames = VGroup(*[SurroundingRectangle(b, buff=0.08, color=GREY_C, stroke_width=1.5) for b in bytes_])
        hx = hexpairs(p["varint 150"])
        hexes = VGroup(*[mono(h, size=26, color=YES).next_to(f, DOWN, buff=0.2) for h, f in zip(hx, frames)])
        cont = label(r"top bit: \ another byte follows?", font_size=17, color=HEAD).next_to(frames, UP, buff=0.12)
        cont.align_to(frames, LEFT)
        mark = r"$\checkmark$" if ok["varint 150"] else r"$\times$"
        guide = " ".join(hexpairs(g["varint 150"]))
        check = label(r"the encoding guide: \ \texttt{" + guide + r"} \ " + mark, font_size=20,
                      color=YES if ok["varint 150"] else NO).next_to(hexes, DOWN, buff=0.35)
        vals = [r for r in sz if r["value"] not in (1, 300)]

        def vname(n):
            if n > 16384 and n & (n - 1) == 0:
                return rf"$2^{{{n.bit_length() - 1}}}$"
            return f"{n}"
        chart = bar_chart([r["bytes"] for r in vals], [vname(r["value"]) for r in vals],
                          [YES if r["bytes"] == 1 else (HEAD if r["bytes"] < 10 else NO) for r in vals],
                          height=2.6, bar_w=0.4, gap=0.26, vmax=10, fmt_=lambda b: f"{b}", font_size=18)
        chart.move_to([3.75, -1.15, 0])
        ct = label(r"bytes for a value \ (computed)", font_size=19, color=GREY_A).next_to(chart, UP, buff=0.25)
        foot = wrapped_label(r"one byte up to 127, \ one more for every seven bits, \ ten for the largest 64-bit "
                             r"values", 6.0, font_size=19, color=WHITE).next_to(chart, DOWN, buff=0.3)
        with self.voiceover(
            "Protocol Buffers, which Google open-sourced in 2008, write integers another way, as varints. "
            "<bookmark mark='a'/> Take a hundred and fifty. In binary it needs eight bits. <bookmark mark='b'/> Cut "
            "them into groups of seven, starting from the low end. <bookmark mark='c'/> Write the low group first, "
            "and give every byte a top bit that says whether another byte follows: one for the first byte, zero for "
            "the last. <bookmark mark='d'/> In hexadecimal that is nine six, zero one, exactly the bytes the "
            "encoding guide gives. <bookmark mark='e'/> So small numbers cost one byte, every further seven bits "
            "cost one more, and the very largest sixty-four-bit values need ten."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(r1))
            vo.wait_until("b")
            self.play(TransformFromCopy(r1[1][1:], glo), TransformFromCopy(r1[1][:1], ghi[-1:]),
                      FadeIn(ghi[:-1]), FadeIn(gl))
            vo.wait_until("c")
            self.play(TransformFromCopy(glo, b1[1:]), TransformFromCopy(ghi, b2[1:]), run_time=1.4)
            self.play(FadeIn(b1[0], scale=1.6), FadeIn(b2[0], scale=1.6), Create(frames), FadeIn(cont))
            vo.wait_until("d")
            self.play(FadeIn(hexes, shift=DOWN * 0.1))
            self.play(FadeIn(check))
            vo.wait_until("e")
            self.play(FadeIn(ct), FadeIn(chart), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def tags(self):
        enc = load("published")["encodings"]
        ours = {k: v for k, v, _, _ in enc}
        head = label(r"Tags: \ a field number and a wire type", font_size=36).to_edge(UP, buff=0.3)
        form = mono("tag = field << 3 | wire type", size=21, color=HEAD).move_to([2.2, 2.35, 0])

        def row(h, y, colors):
            bs = VGroup(*[tag_box(b, color=c, size=18) for b, c in zip(hexpairs(h), colors)]).arrange(RIGHT, buff=0.1)
            return bs.move_to([0, y, 0]).to_edge(LEFT, buff=0.6)
        ha = ours["message {a: 150}"]
        ra = row(ha, 2.35, [HEAD, DATA, DATA])
        fa = int(ha[:2], 16)
        aa = VGroup(
            VGroup(label(rf"field {fa >> 3}", font_size=16, color=HEAD), label(rf"type {fa & 7}", font_size=16,
                                                                                 color=HEAD)).arrange(DOWN, buff=0.05),
            label(r"150", font_size=18, color=DATA),
        )
        aa[0].next_to(ra[0], DOWN, buff=0.12)
        aa[1].next_to(VGroup(ra[1], ra[2]), DOWN, buff=0.15)
        hb = ours['message {b: "testing"}']
        pb = hexpairs(hb)
        rb = row(hb, 0.95, [HEAD, KERN] + [YES] * (len(pb) - 2))
        fb = int(pb[0], 16)
        ab = VGroup(
            VGroup(label(rf"field {fb >> 3}", font_size=16, color=HEAD), label(rf"type {fb & 7}", font_size=16,
                                                                                 color=HEAD)).arrange(DOWN, buff=0.05),
            VGroup(label(rf"{int(pb[1], 16)}", font_size=16, color=KERN), label(r"bytes", font_size=16,
                                                                               color=KERN)).arrange(DOWN, buff=0.05),
            *[mono(bytes.fromhex(b).decode(), size=18, color=YES) for b in pb[2:]],
        )
        for a, b in zip(ab, rb):
            a.next_to(b, DOWN, buff=0.12)
        types = VGroup(label(r"wire types", font_size=19, color=GREY_B),
                       *[label(t, font_size=18, color=GREY_A) for t in
                         (r"0: \ varint", r"1: \ 8 fixed bytes", r"2: \ length, \ then bytes", r"5: \ 4 fixed bytes")]
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.9, 0.85, 0])
        keys = ["varint 150", "message {a: 150}", 'message {b: "testing"}', "message {c: {a: 150}}",
                "packed [3, 270, 86942]"]
        by = {k: (o, w, m) for k, o, w, m in enc}
        rows = [[k, " ".join(hexpairs(by[k][0])), " ".join(hexpairs(by[k][1])),
                 r"$\checkmark$" if by[k][2] else r"$\times$"] for k in keys]
        tab = grid_table([r"example", r"our encoder", r"the encoding guide", r""], rows, widths=[3.4, 3.7, 3.7, 0.6],
                         row_h=0.4, font_size=19, mono_cols=(0, 1, 2))
        tab.move_to([0, -1.6, 0])
        for r in range(1, len(rows) + 1):
            tab.cells[r][3].set_color(YES if by[keys[r - 1]][2] else NO)
        with self.voiceover(
            "A message is a sequence of fields, and each field begins with a tag. <bookmark mark='a'/> The tag is "
            "the field number shifted left by three bits, combined with a wire type: zero for a varint, one and "
            "five for eight and four fixed bytes, two for anything with a length. <bookmark mark='b'/> So field "
            "one holding a varint has the tag zero eight, and the message a equals a hundred and fifty is zero "
            "eight, nine six, zero one. <bookmark mark='c'/> A string is wire type two: field two gives the tag one "
            "two, then the length, seven, then the seven bytes of the word testing. <bookmark mark='d'/> Nested "
            "messages and packed lists are length-delimited too. Our encoder reproduces every example in the "
            "guide, byte for byte."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(form), FadeIn(types))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in ra], lag_ratio=0.3), FadeIn(aa))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b) for b in rb], lag_ratio=0.12), run_time=1.6)
            self.play(LaggedStart(*[FadeIn(a) for a in ab], lag_ratio=0.12), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(tab.rule), LaggedStart(*[FadeIn(VGroup(*line)) for line in tab.cells], lag_ratio=0.3),
                      run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def zigzag(self):
        pub = load("published")
        enc = {k: (o, w, m) for k, o, w, m in pub["encodings"]}
        zz = pub["zigzag"]
        neg = load("sizes")["negative"]
        head = label(r"Negative numbers, \ and zigzag", font_size=36).to_edge(UP, buff=0.3)

        def brow(name, h, color):
            n = label(name, font_size=21, color=color)
            bs = VGroup(*[tag_box(b, color=color, size=17) for b in hexpairs(h)]).arrange(RIGHT, buff=0.08)
            return VGroup(n, bs)
        ri = brow(r"int32 $-2$:", enc["int32 -2"][0], NO)
        rs = brow(r"sint32 $-2$:", enc["sint32 -2"][0], YES)
        for r_, y in ((ri, 2.3), (rs, 1.55)):
            r_[0].move_to([-5.6, y, 0])
            r_[1].next_to([-4.6, y, 0], RIGHT, buff=0)
        cnt = VGroup(label(rf"{len(hexpairs(enc['int32 -2'][0]))} bytes", font_size=19, color=NO).next_to(ri[1], RIGHT,
                                                                                                         buff=0.3),
                     label(rf"{len(hexpairs(enc['sint32 -2'][0]))} byte", font_size=19, color=YES).next_to(
                         rs[1], RIGHT, buff=0.3))
        why = wrapped_label(r"two's complement sets the top bit, \ so all 64 bits must be sent", 3.6, font_size=18,
                            color=GREY_A).next_to(ri[1], DOWN, buff=0.15).align_to(ri[1], RIGHT)
        small = [r for r in zz if abs(r[0]) <= 2][:4]
        xs = {n: -5.2 + i * 1.15 for i, n in enumerate(sorted(r[0] for r in small))}
        top = VGroup(*[mono(f"{n}", size=21, color=DATA).move_to([xs[n], 0.35, 0]) for n, _, _, _ in small])
        bot = VGroup(*[mono(f"{z}", size=21, color=YES).move_to([-5.2 + z * 1.15, -0.85, 0]) for _, z, _, _ in small])
        arrs = VGroup(*[Arrow([xs[n], 0.15, 0], [-5.2 + z * 1.15, -0.65, 0], buff=0.05, color=GREY_B, stroke_width=2,
                              tip_length=0.16) for n, z, _, _ in small])
        rl = VGroup(label(r"$n$", font_size=20, color=DATA).move_to([-6.3, 0.35, 0]),
                    label(r"code", font_size=18, color=YES).move_to([-6.3, -0.85, 0]))
        form = mono("(n << 1) ^ (n >> 31)", size=19, color=HEAD).move_to([-3.5, -1.6, 0])
        big = VGroup(*[mono(f"{n} -> {z}", size=16, color=GREY_A) for n, z, _, ok in zz if abs(n) > 2])
        big.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(form, DOWN, buff=0.25)
        allok = all(r[3] for r in zz)
        bl = label(r"as in the guide's table \ $\checkmark$" if allok else r"differs from the guide", font_size=17,
                   color=YES if allok else NO).next_to(big, DOWN, buff=0.15)
        rows = [[rf"${r['value']}$", f"{r['int']}", f"{r['sint']}"] for r in neg]
        tab = grid_table([r"value", r"as int32", r"as sint32"], rows, widths=[1.8, 1.8, 1.8], row_h=0.4,
                         font_size=19, mono_cols=())
        tab.move_to([3.8, -0.9, 0])
        for r in range(1, len(rows) + 1):
            tab.cells[r][1].set_color(NO)
            tab.cells[r][2].set_color(YES)
        tl = label(r"bytes on the wire \ (computed)", font_size=18, color=GREY_B).next_to(tab, UP, buff=0.2)
        with self.voiceover(
            "Negative numbers expose a flaw. <bookmark mark='a'/> In two's complement, minus two has its top bit "
            "set, so as a varint all sixty-four bits must be sent, and it takes ten bytes. <bookmark mark='b'/> The "
            "sint types fix this with zigzag encoding, which interleaves the signs. Zero becomes zero, minus one "
            "becomes one, one becomes two, minus two becomes three. <bookmark mark='c'/> In code, shift left by one "
            "and exclusive-or with the sign bit copied across the word. Our version matches the guide's table, "
            "even at the extremes. <bookmark mark='d'/> Now minus two is the single byte zero three, and small "
            "numbers of either sign stay small: minus a thousand takes two bytes rather than ten."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ri[0]), LaggedStart(*[FadeIn(b) for b in ri[1]], lag_ratio=0.15), run_time=1.5)
            self.play(FadeIn(cnt[0]), FadeIn(why))
            vo.wait_until("b")
            self.play(FadeIn(top), FadeIn(rl))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(b) for b in bot], lag_ratio=0.3), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(form))
            self.play(FadeIn(big), FadeIn(bl))
            vo.wait_until("d")
            self.play(FadeIn(rs), FadeIn(cnt[1]))
            self.play(FadeIn(tl), FadeIn(tab))
        self.wait(0.4)
        self.clear_scene()

    def compare(self):
        c = load("compare")
        js = c["json"]
        cut = js.index(',"novel"') + 1
        head = label(r"One record, \ two encodings", font_size=36).to_edge(UP, buff=0.3)
        jt = label(rf"JSON, \ {c['json_bytes']} bytes", font_size=22, color=NO)
        jl = VGroup(mono(js[:cut], size=19, color=WHITE), mono(js[cut:], size=19, color=WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        jg = VGroup(jt, jl).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(LEFT, buff=0.6).set_y(1.95)
        fields = split_fields(bytes.fromhex(c["proto_hex"]))
        names = list(c["record"])
        groups = VGroup()
        for k, (f, nm) in enumerate(zip(fields, names)):
            col = FIELD_COLORS[k % len(FIELD_COLORS)]
            h = mono(" ".join(hexpairs(f.hex())), size=19, color=col)
            groups.add(VGroup(h, label(rf"field {k + 1}: \ {nm}", font_size=17, color=col).next_to(h, DOWN,
                                                                                               buff=0.1)))
        l1 = VGroup(*groups[:3]).arrange(RIGHT, buff=0.35, aligned_edge=UP)
        l2 = VGroup(*groups[3:]).arrange(RIGHT, buff=0.35, aligned_edge=UP)
        pt = label(rf"Protocol Buffers, \ {c['proto_bytes']} bytes", font_size=22, color=YES)
        VGroup(pt, l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(jg, DOWN, buff=0.4).align_to(
            jg, LEFT)
        k = 0.1
        bars = VGroup()
        for i, (nm, n, col) in enumerate(((r"JSON", c["json_bytes"], NO),
                                          (r"protobuf", c["proto_bytes"], YES))):
            r = Rectangle(width=n * k, height=0.36, stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to([-4.6 + n * k / 2, -1.75 - i * 0.6, 0])
            bars.add(VGroup(label(nm, font_size=19, color=col).next_to(r, LEFT, buff=0.2).align_to([-4.8, 0, 0], RIGHT),
                            r, label(rf"{n} bytes", font_size=19, color=col).next_to(r, RIGHT, buff=0.15)))
        foot = wrapped_label(r"the bytes mean nothing without the schema: \ \texttt{08} says ``field 1, \ a varint'', "
                             r"\ not ``id''", 12.4, font_size=20, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Put it together on one record: an id, a word, its count, its novel, a score and three tags. "
            f"<bookmark mark='a'/> As compact JSON it is {c['json_bytes']} bytes. <bookmark mark='b'/> As "
            f"Protocol Buffers it is {c['proto_bytes']}, with the score as a zigzag sint and the tags as a packed"
            " list. <bookmark mark='c'/> The saving comes mostly from names: JSON repeats every field name in "
            "every record, and writes numbers as decimal text, where protobuf sends a one-byte tag and a varint."
            " <bookmark mark='d'/> The price is that the bytes mean nothing without the schema: zero eight says "
            "field one, not id. Both sides must agree on the schema, and keep agreeing as it changes: the next "
            "chapter."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(jg), FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(FadeIn(pt), LaggedStart(*[FadeIn(g_) for g_ in groups], lag_ratio=0.3), FadeIn(bars[1]),
                      run_time=2)
            vo.wait_until("c")
            self.play(Indicate(jl, color=NO, scale_factor=1.03))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM)
