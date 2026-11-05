from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.pebble.asm import _li_parts
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FILE_COLORS, FUNC, HEAD, NO, PART, YES, code, grid_table,
                                   load, region)


class Linking(VoiceoverScene):
    def construct(self):
        self.card()
        self.resolve()
        self.layout()
        self.patch()
        self.archive()

    def card(self):
        card = chapter_card(10, r"Linking, \ step by step", r"How do four files become one program?", part=PART)
        with self.voiceover("Chapter ten. Linking, step by step."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def resolve(self):
        pl = load("pebblelink")
        head = label(r"Step 1: \ resolve every name", font_size=34).to_edge(UP, buff=0.3)
        cols = VGroup()
        for k, o in enumerate(pl["objects"]):
            c = FILE_COLORS[k]
            g = VGroup(region(2.6, 0.6, o["name"], c, font_size=22))
            defs = [d[0] for d in o["defined"] if d[3] == "global"]
            g.add(label(r"defines: \ " + (r", \ ".join(rf"\texttt{{{d.replace('_', chr(92) + '_')}}}" for d in defs)
                                          or r"---"), font_size=16, color=YES))
            g.add(label(r"needs: \ " + (r", \ ".join(rf"\texttt{{{u}}}" for u in o["undefined"]) or r"---"),
                        font_size=16, color=NO))
            g.arrange(DOWN, buff=0.15)
            cols.add(g)
        cols.arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=0.5)
        if cols.width > 13:
            cols.scale_to_fit_width(13)
        res = VGroup(label(r"every need meets exactly one global definition:", font_size=21, color=GREY_A))
        for name, addr in sorted(pl["symbols"].items(), key=lambda kv: kv[1]):
            res.add(Text(f"{name:<9} {addr:>4}", font="DejaVu Sans Mono", font_size=16, color=CODE))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(cols, DOWN, buff=0.5).to_edge(LEFT, buff=1.2)
        err = VGroup(label(r"and when it does not, \ Pebble's linker says so:", font_size=19, color=GREY_B),
                     Text(pl["errors"]["undefined"].replace(" in ", "\n  in "), font="DejaVu Sans Mono", font_size=15,
                          color=NO),
                     Text(pl["errors"]["duplicate"].replace(": ", ":\n  "), font="DejaVu Sans Mono", font_size=15,
                          color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(res, RIGHT, buff=0.8).align_to(res, UP)
        if err.get_right()[0] > 6.8:
            err.scale_to_fit_width(6.8 - err.get_left()[0])
        with self.voiceover(
            "Now our own linker, on the Job's four object files. <bookmark mark='a'/> Each file says what it "
            "defines and what it needs. main defines start and needs getc, lookup and report. The table defines "
            "lookup and report and needs alloc, putc and printnum. alloc and io need nothing. <bookmark mark='b'/> "
            "The first job is to match every need to exactly one definition. Here, every name is defined once, so "
            "each gets an address. <bookmark mark='c'/> Leave out the allocator, or include it twice, and Pebble's "
            "linker refuses, with the same two complaints this machine's linker gave."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(res))
            vo.wait_until("c")
            self.play(FadeIn(err))
        self.wait(0.3)
        self.clear_scene()

    def layout(self):
        pl = load("pebblelink")
        head = label(r"Step 2: \ decide where everything goes", font_size=34).to_edge(UP, buff=0.3)
        names = [o["name"] for o in pl["objects"]]
        rows = []
        for f, sec, start, size in pl["layout"]:
            if size == 0:
                continue
            rows.append((f, sec, start, size))
        blocks = VGroup()
        for f, sec, start, size in rows:
            c = FILE_COLORS[names.index(f)]
            h = 0.55 if sec != ".bss" else 0.75
            txt = rf"{f} \ \texttt{{{sec}}} \ ({size:,} bytes)"
            blocks.add(VGroup(region(5.6, h, txt, c, font_size=17,
                                     fill=0.12 if sec == ".bss" else 0.3),
                              Text(f"{start:>6}", font="DejaVu Sans Mono", font_size=15, color=GREY_B)))
        for b in blocks:
            b[1].next_to(b[0], LEFT, buff=0.2)
        blocks.arrange(DOWN, buff=0.05).move_to(DOWN * 0.15).to_edge(LEFT, buff=0.5)
        legend = VGroup(
            label(r"all the code first, \ in file order", font_size=19, color=DATA),
            label(r"then all the data", font_size=19, color=CTRL),
            label(r"then \texttt{.bss}: \ addresses only, \\ zeros at load time \ (the heap's 384 KB)", font_size=19,
                  color=FUNC),
            label(rf"the file: \ {pl['image']} bytes; \ the program in memory: \ {pl['bss'][1]:,}", font_size=19,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        legend.next_to(blocks, RIGHT, buff=0.5)
        for k, sec in enumerate((".text", ".data", ".bss")):
            idx = [i for i, r in enumerate(rows) if r[1] == sec]
            if idx:
                legend[k].set_y(VGroup(*[blocks[i] for i in idx]).get_y())
        legend[3].next_to(legend[2], DOWN, buff=0.6).align_to(legend[2], LEFT)
        with self.voiceover(
            "Step two: decide where everything goes. <bookmark mark='a'/> The linker lays out all the files' code "
            "first, one after another in the order the files were given, each aligned to sixteen bytes. Then all "
            "their data. <bookmark mark='b'/> Then the bss sections, which take addresses but no bytes in the file: "
            "here, the allocator's three hundred and eighty-four kilobytes of heap. <bookmark mark='c'/> So the "
            "program file is eight hundred and sixty-four bytes, but the program in memory is almost four hundred "
            "kilobytes. Now that every section has an address, so does every symbol."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in blocks[:-1]], lag_ratio=0.3),
                      FadeIn(legend[0]), FadeIn(legend[1]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(blocks[-1]), FadeIn(legend[2]))
            vo.wait_until("c")
            self.play(FadeIn(legend[3]))
        self.wait(0.3)
        self.clear_scene()

    def patch(self):
        pl = load("pebblelink")
        head = label(r"Step 3: \ fill every hole", font_size=34).to_edge(UP, buff=0.3)
        ps = pl["patches"]
        rows = [[p["file"], f"{p['at']}", p["kind"], p["symbol"], f"{p['target']}"] for p in ps]
        t = grid_table([r"file", r"at", r"kind", r"symbol", r"its address"], rows, [1.7, 1.0, 1.3, 1.6, 1.8],
                       row_h=0.3, font_size=15, colors=[[GREY_B, GREY_A, FUNC, CODE, HEAD]] * len(rows),
                       mono_cols=(2, 3)).to_edge(LEFT, buff=0.4).shift(DOWN * 0.3)
        if t.height > 6.2:
            t.scale_to_fit_height(6.2)
        t.next_to(head, DOWN, buff=0.3).to_edge(LEFT, buff=0.4)
        hl = next(p for p in ps if p["kind"] == "hi_lo")
        hi, lo = _li_parts(hl["target"])
        ex = VGroup(
            label(rf"\texttt{{la t0, {hl['symbol']}}} \ in {hl['file']}:", font_size=20, color=GREY_A),
            Text(f"lui  t0, 0          ->  lui  t0, {hi}", font="DejaVu Sans Mono", font_size=16, color=CODE),
            Text(f"ori  t0, t0, 0      ->  ori  t0, t0, {lo}", font="DejaVu Sans Mono", font_size=16, color=CODE),
            label(rf"${hi} \times 1024 + {lo} = {hl['target']}$: \ the address of \texttt{{{hl['symbol']}}}",
                  font_size=19, color=HEAD),
            label(r"a call: \ the distance in instructions, \\ into the jump's 22-bit field", font_size=19, color=FUNC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        done = label(r"then run it: \ the same twenty words as Part 6's program", font_size=21, color=YES).to_edge(
            DOWN, buff=0.3).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            f"Step three: fill the holes. <bookmark mark='a'/> There are {len(ps)} relocations across the four "
            "files. Each says where the hole is, what kind of hole, and which symbol's address belongs in it. "
            "<bookmark mark='b'/> Take one: the table code loads the address of its list head with la, which the "
            f"assembler emitted as a lui and an ori with zeros. head now lives at {hl['target']}. The linker splits "
            f"that into its top twenty-two bits, {hi}, and its low ten, {lo}, and writes them into the two "
            "instructions. <bookmark mark='c'/> For a call, it writes the distance from the call to the function, "
            "counted in instructions, into the jump's 22-bit field. <bookmark mark='d'/> That is all a static linker "
            "does. Load the result and run it, and the four files behave as one program."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule),
                      LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.1),
                      run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in ex[:4]], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(ex[4]))
            vo.wait_until("d")
            self.play(FadeIn(done))
        self.wait(0.3)
        self.clear_scene()

    def archive(self):
        ar = load("archive")
        L = ar["links"]
        kb_ar, kb_obj = round(L["archive"]["bytes"] / 1024), round(L["objects"]["bytes"] / 1024)
        head = label(r"Libraries, \ and why order matters", font_size=34).to_edge(UP, buff=0.3)
        cmd1 = code([r"gcc main.o libjob.a"], size=18, color=YES)
        cmd2 = code([r"gcc libjob.a main.o"], size=18, color=NO)

        def scan(first_lib):
            mo = region(1.5, 0.7, r"main.o", FILE_COLORS[0], font_size=20)
            co = region(1.4, 0.55, r"count.o", FILE_COLORS[1], font_size=17)
            uo = region(1.4, 0.55, r"unused.o \\ (100 KB table)", GREY_B, font_size=14, fill=0.08)
            mem = VGroup(co, uo).arrange(RIGHT, buff=0.15)
            lib = VGroup(SurroundingRectangle(mem, buff=0.15, color=CTRL, stroke_width=1.5, corner_radius=0.08), mem)
            lt = label(r"libjob.a", font_size=17, color=CTRL).next_to(lib, UP, buff=0.08)
            lib.add(lt)
            row = VGroup(lib, mo) if first_lib else VGroup(mo, lib)
            row.arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
            return row, mo, co, uo

        row1, mo1, co1, uo1 = scan(False)
        cmd1.next_to(row1, UP, buff=0.55).align_to(row1, LEFT)
        g1 = VGroup(cmd1, row1).move_to(UP * 1.35)
        und1 = label(r"undefined so far: \ \texttt{count}", font_size=19, color=NO).next_to(row1, DOWN, buff=0.3)
        und1.align_to(row1, LEFT)
        took = VGroup(label(rf"takes \texttt{{count.o}}, \ leaves \texttt{{unused.o}}: \ {kb_ar} KB", font_size=19,
                            color=YES),
                      label(rf"(all three object files listed directly: \ {kb_obj} KB)", font_size=17, color=GREY_B)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(und1, DOWN, buff=0.12).align_to(und1, LEFT)
        row2, mo2, co2, uo2 = scan(True)
        cmd2.next_to(row2, UP, buff=0.55).align_to(row2, LEFT)
        g2 = VGroup(cmd2, row2).move_to(UP * 1.35)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0, aligned_edge=UP).next_to(head, DOWN, buff=0.45)
        und1.next_to(row1, DOWN, buff=0.3).align_to(row1, LEFT)
        took.next_to(und1, DOWN, buff=0.12).align_to(und1, LEFT)
        und2 = label(r"undefined so far: \ nothing, \ so it takes nothing", font_size=19, color=GREY_B).next_to(
            row2, DOWN, buff=0.3).align_to(row2, LEFT)
        err = VGroup(label(r"then \texttt{main.o} needs \texttt{count}, \ too late:", font_size=19, color=NO),
                     Text(L["archive first"]["error"][0], font="DejaVu Sans Mono", font_size=15, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(und2, DOWN, buff=0.12).align_to(und2, LEFT)
        rule = label(r"the rule: \ libraries after the files that use them, \ in dependency order", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Real programs also link against libraries, and a static library is simply an archive of object files. "
            "<bookmark mark='a'/> Here is one we built, lib job dot a, holding two members: count dot o, and unused "
            "dot o, which carries a hundred-kilobyte table. <bookmark mark='b'/> The linker reads its inputs left "
            "to right, keeping a list of the names still undefined. After main dot o, that list holds count. "
            "<bookmark mark='c'/> In the archive it takes only the members that define a name on the list: count "
            f"dot o comes in, unused dot o stays out. The program is {kb_ar} kilobytes; listing all three object "
            f"files instead gives {kb_obj}. <bookmark mark='d'/> Now put the library first. When the linker reads "
            "it, nothing is undefined yet, so it takes nothing; then main dot o needs count, too late. Undefined "
            "reference to count. <bookmark mark='e'/> That is why, on a command line, libraries go after the files "
            "that use them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cmd1), FadeIn(row1))
            vo.wait_until("b")
            self.play(Indicate(mo1, color=FILE_COLORS[0]), FadeIn(und1))
            vo.wait_until("c")
            self.play(co1[0].animate.set_fill(YES, opacity=0.45), uo1.animate.set_opacity(0.3))
            self.play(FadeIn(took))
            vo.wait_until("d")
            self.play(FadeIn(cmd2), FadeIn(row2))
            self.play(FadeIn(und2), co2.animate.set_opacity(0.3), uo2.animate.set_opacity(0.3))
            self.play(FadeIn(err))
            vo.wait_until("e")
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()
