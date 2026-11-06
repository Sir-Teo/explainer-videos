from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, mono,
                                   module_box, tag_box)

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


def field_row(text, color, w, size=17):
    """One field of a schema, drawn as a box of monospace text, left-aligned."""
    t = mono(text, size=size, color=color)
    box = RoundedRectangle(width=w, height=0.5, corner_radius=0.08, stroke_color=color, stroke_width=1.6,
                           fill_color=BG, fill_opacity=1)
    t.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.18)
    return VGroup(box, t)


class Schemas(VoiceoverScene):
    def construct(self):
        self.card()
        self.rolling()
        self.subtyping()
        self.cases()
        self.trap()
        self.avro()
        self.zerocopy()

    def card(self):
        card = chapter_card(3, r"Schemas that evolve", r"How can a format change while old code still reads it?",
                            lit=(2009, 2016), extra=((2009, r"Avro"), (2016, r"proto3: \ no required fields")),
                            part=PART)
        with self.voiceover("Chapter three. Schemas that evolve."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rolling(self):
        head = label(r"Two versions at once", font_size=36).to_edge(UP, buff=0.3)
        servers = VGroup(*[module_box(r"v1", DATA, w=1.4, h=0.6, font=20) for _ in range(6)]).arrange(
            RIGHT, buff=0.45).move_to([0, 1.85, 0])
        upgraded = [module_box(r"v2", LAM, w=1.4, h=0.6, font=20).move_to(s) for s in servers]
        sc = label(r"servers, \ part-way through a rolling deploy", font_size=19, color=GREY_B).next_to(
            servers, UP, buff=0.2)
        log = VGroup(*[tag_box(v, color=DATA if v == "v1" else LAM, size=17, w=1.0) for v in
                       ["v1"] * 6 + ["v2"] * 3]).arrange(RIGHT, buff=0.12).move_to([0, 0.2, 0])
        lc = label(r"a log or a database: \ bytes written years ago, \ still read today", font_size=19,
                   color=GREY_B).next_to(log, DOWN, buff=0.2)

        def rule(reader, rc, data, dc, name, nc, text):
            a = module_box(reader, rc, w=1.8, h=0.55, font=18)
            b = tag_box(data, color=dc, size=17, w=1.6)
            arr = Arrow(RIGHT, LEFT, color=GREY_B, stroke_width=2, buff=0).scale(0.45)
            g = VGroup(a, arr, b).arrange(RIGHT, buff=0.15)
            t = VGroup(label(name, font_size=22, color=nc), label(text, font_size=20, color=WHITE)).arrange(
                RIGHT, buff=0.3)
            return VGroup(g, t).arrange(RIGHT, buff=0.5)
        rules = VGroup(
            rule(r"v2 code", LAM, r"v1 data", DATA, r"backward compatible:", YES, r"new code reads old data"),
            rule(r"v1 code", DATA, r"v2 data", LAM, r"forward compatible:", HEAD, r"old code reads new data"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "A schema is never changed everywhere at once. <bookmark mark='a'/> Servers are upgraded a few at a "
            "time, in a rolling deploy, so for a while old and new code run side by side and send each other "
            "messages. <bookmark mark='b'/> And data outlives code: a database or a log, which Part 46 takes up, "
            "holds bytes written years ago. <bookmark mark='c'/> So a change must be backward compatible: new code "
            "can read old data. <bookmark mark='d'/> And usually it must be forward compatible as well: old code, "
            "not yet upgraded, can read what new code writes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(servers), FadeIn(sc))
            self.play(LaggedStart(*[ReplacementTransform(servers[i], upgraded[i]) for i in range(3)],
                                  lag_ratio=0.5), run_time=2.4)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in log], lag_ratio=0.15), FadeIn(lc), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(rules[0]))
            vo.wait_until("d")
            self.play(FadeIn(rules[1]))
        self.wait(0.4)
        self.clear_scene()

    def subtyping(self):
        head = label(r"Compatibility is subtyping", font_size=36).to_edge(UP, buff=0.3)
        wf = VGroup(*[field_row(t, c, 3.3) for t, c in (("1 word:  string", DATA), ("2 count: int64", DATA),
                                                         ("3 novel: string", LAM))]).arrange(DOWN, buff=0.3)
        rf = VGroup(*[field_row(t, c, 3.9) for t, c in (("1 word:  string  required", GREY_A),
                                                         ("2 count: int64   optional", GREY_A))]).arrange(DOWN,
                                                                                                    buff=0.3)
        wf.move_to([-4.6, 1.0, 0])
        rf.move_to([-0.2, 0, 0]).align_to(wf, UP)
        wt = label(r"the writer \ (new code)", font_size=19, color=LAM).next_to(wf, UP, buff=0.18)
        rt = label(r"the reader \ (old code)", font_size=19, color=DATA).next_to(rf, UP, buff=0.18)
        links = VGroup(*[Line(wf[i].get_right(), rf[i].get_left(), color=YES, stroke_width=3) for i in range(2)])
        skip_t = label(r"unknown: \ skipped", font_size=19, color=GREY_B).move_to([rf.get_x(), wf[2].get_y(), 0])
        skip = DashedLine(wf[2].get_right(), skip_t.get_left() + LEFT * 0.1, color=GREY_B, stroke_width=2)
        sub = MathTex(r"\{\text{word},\ \text{count},\ \text{novel}\}\ <:\ \{\text{word},\ \text{count}\}",
                      font_size=34, color=WHITE).move_to([-2.4, -1.55, 0])
        subl = label(r"width subtyping \ (Part 14): \ a record with more fields goes wherever fewer are expected",
                     font_size=19, color=GREY_A).next_to(sub, DOWN, buff=0.2).set_x(0)
        side = VGroup(
            wrapped_label(r"fields are matched by number, \ and their types must agree", 4.2, font_size=19,
                          color=YES),
            wrapped_label(r"a field the reader does not know is skipped; \ protobuf keeps its bytes, \ so they "
                          r"survive being passed on", 4.2, font_size=19, color=GREY_A),
            wrapped_label(r"the rule: \ the reader accepts the writer's record if every field it \textbf{requires} "
                          r"is there, \ with a compatible type", 4.2, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.5, 1.0, 0])
        bad = wrapped_label(r"the other way round: \ a reader that requires \texttt{novel} rejects every old record",
                            12.4, font_size=20, color=NO).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part 14 has the answer. <bookmark mark='a'/> New code writes a record with three fields; old code "
            "expects two. <bookmark mark='b'/> The reader matches fields by number: word and count are there, "
            "with the types it expects. <bookmark mark='c'/> Novel is unknown, so it is skipped, though protobuf"
            " keeps its bytes to pass on. <bookmark mark='d'/> This is width subtyping: a record with more "
            "fields can go wherever fewer are expected. A reader accepts a writer's record when every field it "
            "requires is present, with a compatible type. <bookmark mark='e'/> Turn it round, and a reader that "
            "requires novel rejects every old record."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(wf), FadeIn(wt), FadeIn(rf), FadeIn(rt))
            vo.wait_until("b")
            self.play(Create(links), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(skip), FadeIn(skip_t), wf[2].animate.set_opacity(0.5), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(Write(sub), FadeIn(subl), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(bad))
        self.wait(0.4)
        self.clear_scene()

    def cases(self):
        ev = load("evolution")["cases"]
        head = label(r"Seven changes, \ checked", font_size=36).to_edge(UP, buff=0.3)
        v1 = label(r"version 1: \ \texttt{word} \ (field 1, \ string, \ required) \ and \texttt{count} \ (field 2, "
                   r"\ int64, \ optional)", font_size=19, color=GREY_A).next_to(head, DOWN, buff=0.25)

        def mark(ok):
            return r"$\checkmark$" if ok else r"$\times$"

        def prob(ps):
            if not ps:
                return r"none"
            return ps[0] + (r"; \ and the reverse" if len(ps) > 1 else "")
        rows = [[c["change"], mark(c["backward"]), mark(c["forward"]), prob(c["problems"])] for c in ev]
        tab = grid_table([r"change", r"backward", r"forward", r"problem our checker found"], rows,
                         widths=[3.6, 1.6, 1.6, 5.8], row_h=0.5, font_size=20, mono_cols=())
        tab.next_to(v1, DOWN, buff=0.3)
        for r, c in enumerate(ev, start=1):
            tab.cells[r][1].set_color(YES if c["backward"] else NO)
            tab.cells[r][2].set_color(YES if c["forward"] else NO)
            tab.cells[r][3].set_color(GREY_B if not c["problems"] else NO)
        idx = {c["change"]: r for r, c in enumerate(ev, start=1)}

        def row_box(name, color):
            r = idx[name]
            g = VGroup(*tab.cells[r])
            return SurroundingRectangle(g, buff=0.06, color=color, stroke_width=2.5).stretch_to_fit_width(
                tab.width + 0.15).set_x(tab.get_x())
        trap = row_box("renumber a field", HEAD)
        widen = row_box("widen int32 to int64", KERN)
        notes = VGroup(
            wrapped_label(r"our checker treats int32, \ int64, \ uint32, \ uint64 and bool as one varint family; \ "
                          r"protobuf agrees, \ but an old int32 reader truncates a value that no longer fits", 12.4,
                          font_size=19, color=KERN),
            wrapped_label(r"renumbering passes both ways: \ the checker's verdict, \ and a trap", 12.4, font_size=20,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(tab, DOWN, buff=0.45).set_x(0)
        groups = [VGroup(*line) for line in tab.cells]
        with self.voiceover(
            "Our checker applies that rule both ways to seven changes of a small schema: a required word, field "
            "one, and an optional count, field two. <bookmark mark='a'/> Adding or removing an optional field is"
            " safe both ways. <bookmark mark='b'/> Adding a required field breaks backward compatibility: old "
            "data never contains it. Removing one breaks forward compatibility: old readers still demand it. "
            "<bookmark mark='c'/> Changing a type breaks both. <bookmark mark='d'/> Widening a 32-bit integer to"
            " 64 bits passes, since both are varints, though an old reader truncates values that no longer fit. "
            "<bookmark mark='e'/> And renumbering a field passes, both ways. That verdict is wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(v1), FadeIn(groups[0]), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(groups[idx["add an optional field"]]), FadeIn(groups[idx["remove an optional field"]]))
            vo.wait_until("b")
            self.play(FadeIn(groups[idx["add a required field"]]), FadeIn(groups[idx["remove a required field"]]))
            vo.wait_until("c")
            self.play(FadeIn(groups[idx["change a field's type"]]))
            vo.wait_until("d")
            self.play(FadeIn(groups[idx["widen int32 to int64"]]), Create(widen), FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(groups[idx["renumber a field"]]), Create(trap), FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def trap(self):
        c = load("compare")
        fields = split_fields(bytes.fromhex(c["proto_hex"]))
        names = list(c["record"])
        cnt = fields[names.index("count")]
        count = c["record"]["count"]
        tag = format(2 << 3 | 0, "02x")                  # count as field 2, a varint
        hx = [tag] + hexpairs(cnt[1:].hex())
        head = label(r"The trap: \ renumbering", font_size=36).to_edge(UP, buff=0.3)
        x = -3.6
        w1 = VGroup(label(r"old writer", font_size=19, color=DATA),
                    mono("int64 count = 2;", size=19, color=DATA)).arrange(RIGHT, buff=0.3).move_to([x, 2.3, 0])
        bs = VGroup(*[tag_box(h, color=HEAD if i == 0 else DATA, size=19) for i, h in enumerate(hx)]).arrange(
            RIGHT, buff=0.12).move_to([x, 1.35, 0])
        bl = VGroup(label(r"field 2, \ varint", font_size=17, color=HEAD).next_to(bs[0], DOWN, buff=0.12),
                    label(rf"{count}", font_size=17, color=DATA).next_to(VGroup(*bs[1:]), DOWN, buff=0.12))
        bl[0].shift(LEFT * 0.4)
        r1 = VGroup(label(r"new reader", font_size=19, color=LAM),
                    mono("int64 count = 5;", size=19, color=LAM)).arrange(RIGHT, buff=0.3).move_to([x, -0.05, 0])
        a1 = Arrow([x, 0.75, 0], [x, 0.25, 0], buff=0, color=GREY_B, stroke_width=2)
        out = VGroup(
            label(r"field 2: \ unknown, \ skipped", font_size=20, color=GREY_B),
            label(r"field 5: \ absent, \ so count $= 0$", font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(r1, DOWN, buff=0.4)
        lost = label(rf"{count} lost, \ and nothing failed", font_size=21, color=NO).next_to(out, DOWN, buff=0.3)
        fix = code_block(["message Counts {", "  reserved 2;", '  reserved "count";', "  string word = 1;", "}"],
                         size=17)
        ff = SurroundingRectangle(fix, buff=0.18, color=GREY_C, stroke_width=1.5, corner_radius=0.08)
        side = VGroup(
            wrapped_label(r"both fields are optional, \ so a structural checker sees nothing to object to", 5.2,
                          font_size=19, color=HEAD),
            wrapped_label(r"a field's number \textbf{is} its identity: \ never change one, \ never reuse one; \ a "
                          r"deleted field's number and name are \texttt{reserved}", 5.2, font_size=19, color=YES),
            VGroup(ff, fix),
            wrapped_label(r"proto3 \ (2016) \ has no required fields: \ as the table showed, \ one can never be "
                          r"added or removed safely", 5.2, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.7, 0.1, 0])
        with self.voiceover(
            "Here is why. <bookmark mark='a'/> Old code writes the count, one thousand two hundred and twenty-"
            "six, as field two: the tag one zero, then a varint. <bookmark mark='b'/> New code expects the count"
            " in field five. <bookmark mark='c'/> To it, field two is unknown and is skipped, and field five is "
            "absent, so the count reads as zero. Nothing fails; every count is silently lost. <bookmark "
            "mark='d'/> The real rule: a field's number is its identity. Never change it, never reuse it, and "
            "reserve the number and name of a deleted field. <bookmark mark='e'/> And because a required field "
            "can never be safely added or removed, proto3 dropped required fields altogether."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(w1))
            self.play(LaggedStart(*[FadeIn(b) for b in bs], lag_ratio=0.3), FadeIn(bl))
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(r1))
            vo.wait_until("c")
            self.play(FadeIn(out[0]), bs[0].animate.set_opacity(0.4))
            self.play(FadeIn(out[1]), FadeIn(side[0]))
            self.play(FadeIn(lost))
            vo.wait_until("d")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def avro(self):
        rec = load("compare")["record"]
        head = label(r"Avro: \ the reader brings both schemas", font_size=36).to_edge(UP, buff=0.3)
        ws = VGroup(*[field_row(t, DATA, 3.0) for t in ("word:  string", "count: long")]).arrange(DOWN, buff=0.25)
        rs = VGroup(*[field_row(t, c, 4.6) for t, c in (("word:  string", LAM), ("count: long", LAM),
                                                         ('novel: string = "unknown"', HEAD))]).arrange(DOWN,
                                                                                                    buff=0.25)
        ws.move_to([-4.6, 1.25, 0])
        rs.move_to([1.2, 0, 0]).align_to(ws, UP)
        wt = label(r"writer's schema", font_size=19, color=DATA).next_to(ws, UP, buff=0.15)
        rt = label(r"reader's schema", font_size=19, color=LAM).next_to(rs, UP, buff=0.15)
        links = VGroup(*[Line(ws[i].get_right(), rs[i].get_left(), color=YES, stroke_width=3) for i in range(2)])
        dflt = label(r"missing: \ default", font_size=18, color=HEAD).next_to(rs[2], LEFT, buff=0.3)
        data = VGroup(tag_box(rec["word"], color=DATA, size=18), tag_box(f"{rec['count']}", color=DATA, size=18))
        data.arrange(RIGHT, buff=0.06).next_to(ws, DOWN, buff=0.75).align_to(ws, LEFT)
        dl = wrapped_label(r"the bytes: \ values only, \ in the writer's order; \ no tags, \ no names; \ integers "
                           r"are zigzag varints", 3.6, font_size=18, color=GREY_A)
        dl.next_to(data, DOWN, buff=0.2).align_to(data, LEFT)
        ill = note(r"illustrative schemas", font_size=17).to_corner(DR, buff=0.35)
        notes = VGroup(
            wrapped_label(r"the writer's schema travels in a file's header, \ or by number from a schema registry",
                          6.4, font_size=19, color=WHITE),
            wrapped_label(r"resolution matches fields by \textbf{name}: \ a field the writer lacks takes the reader's "
                          r"default; \ a field the reader lacks is skipped", 6.4, font_size=19, color=YES),
            wrapped_label(r"so in Avro the dangerous change is a rename, \ not a renumbering", 6.4, font_size=19,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, -2.05, 0])
        with self.voiceover(
            "Apache Avro, from the Hadoop project in 2009, makes a different trade. <bookmark mark='a'/> Its "
            "bytes carry no tags and no names, only values in the writer's order, with integers as zigzag "
            "varints. <bookmark mark='b'/> So the reader also needs the writer's schema, from a file's header or"
            " a schema registry. <bookmark mark='c'/> It resolves the two schemas, matching fields by name. "
            "<bookmark mark='d'/> A field the writer lacks takes the reader's default; a field the reader lacks "
            "is skipped. It is the same subtyping question, asked of whole schemas, and here the dangerous "
            "change is a rename."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(ws), FadeIn(wt), FadeIn(data), FadeIn(dl))
            vo.wait_until("b")
            self.play(FadeIn(rs), FadeIn(rt), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(Create(links), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(dflt), Indicate(rs[2], color=HEAD), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def zerocopy(self):
        c = load("compare")
        fields = split_fields(bytes.fromhex(c["proto_hex"]))
        names = list(c["record"])
        head = label(r"Reading without parsing", font_size=36).to_edge(UP, buff=0.3)
        cw = 0.3
        cells, starts = VGroup(), []
        for k, f in enumerate(fields):
            starts.append(len(cells))
            for _ in range(len(f)):
                cells.add(Square(side_length=cw, stroke_color=GREY_D, stroke_width=1,
                                 fill_color=FIELD_COLORS[k % len(FIELD_COLORS)], fill_opacity=0.7))
        cells.arrange(RIGHT, buff=0.03).move_to([0, 1.75, 0])
        pc = label(rf"protobuf: \ {c['proto_bytes']} bytes; \ to reach \texttt{{count}}, \ walk the tags from the "
                   r"start", font_size=19, color=GREY_A).next_to(cells, UP, buff=0.2)
        ci = names.index("count")
        cur = Triangle(color=HEAD, fill_color=HEAD, fill_opacity=1).scale(0.1).rotate(PI)
        cur.next_to(cells[0], DOWN, buff=0.08)
        hits = [starts[i] for i in range(ci + 1)]
        # an illustrative zero-copy layout: an offset table, then fixed-size fields, then the strings
        parts = [(r"offsets", 1.8, GREY_B), (r"word ref", 1.2, DATA), (r"count", 2.4, HEAD), (r"novel ref", 1.2, LAM),
                 (r"strings", 2.6, GREY_A)]
        zc = VGroup()
        for t, w, col in parts:
            r = Rectangle(width=w, height=0.55, stroke_color=col, stroke_width=1.8, fill_color=col, fill_opacity=0.15)
            zc.add(VGroup(r, label(t, font_size=18, color=col).move_to(r)))
        zc.arrange(RIGHT, buff=0.05).move_to([0, 0.0, 0])
        zl = label(r"zero-copy \ (illustrative layout): \ a table of offsets, \ then fields at fixed places",
                   font_size=19, color=GREY_A).next_to(zc, UP, buff=0.2)
        jump = CurvedArrow(zc[0].get_bottom() + DOWN * 0.05, zc[2].get_bottom() + DOWN * 0.05, angle=PI / 3,
                           color=HEAD, stroke_width=3)
        jl = label(r"base $+$ offset: \ one jump, \ read in place", font_size=19, color=HEAD).next_to(jump, DOWN,
                                                                                                    buff=0.12)
        notes = VGroup(
            wrapped_label(r"FlatBuffers \ (Google, \ 2014) \ and Cap'n Proto \ (Kenton Varda, \ 2013, \ after leading "
                          r"Protocol Buffers' second version): \ the bytes on the wire are the bytes in memory", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"the price: \ larger messages, \ padded for alignment; \ and a buffer from a stranger must "
                          r"be verified before its offsets are followed", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "One cost is left. <bookmark mark='a'/> To read one field of a protobuf message, a reader walks the "
            "tags from the start, decoding as it goes. <bookmark mark='b'/> Zero-copy formats lay the bytes out "
            "the way the program uses them. A table of offsets says where each field lives, <bookmark mark='c'/>"
            " so reading the count is one addition and one load, straight from the received buffer. <bookmark "
            "mark='d'/> FlatBuffers, from Google, and Cap'n Proto, by Kenton Varda, who had led Protocol "
            "Buffers' second version, work this way. <bookmark mark='e'/> The price is larger, padded messages, "
            "and a stranger's buffer must be verified before its offsets are followed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(pc), FadeIn(cur))
            for h in hits:
                self.play(cur.animate.next_to(cells[h], DOWN, buff=0.08), Indicate(cells[h], color=WHITE),
                          run_time=0.6)
            self.play(VGroup(*cells[starts[ci]:starts[ci] + len(fields[ci])]).animate.set_stroke(HEAD, width=3))
            vo.wait_until("b")
            self.play(FadeIn(zc), FadeIn(zl))
            vo.wait_until("c")
            self.play(Create(jump), FadeIn(jl))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG,)
