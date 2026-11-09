from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load)

KEEP = (".text", ".text.startup", ".data", ".bss", ".rodata.str1.1", ".data.rel.local", ".rela.text",
        ".rela.text.startup", ".symtab", ".strtab")


class Objects(VoiceoverScene):
    def construct(self):
        self.card()
        self.sources()
        self.sections()
        self.symbols()
        self.rules()

    def card(self):
        card = chapter_card(9, r"Object files", r"What does the assembler leave for the linker?", lit=(1988,),
                            extra=((1988, r"System V: \ ELF"),), part=PART)
        with self.voiceover("Chapter nine. Object files."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def sources(self):
        e = load("elf")
        head = label(r"Two C files, \ compiled separately on this machine", font_size=32).to_edge(UP, buff=0.3)
        a = VGroup(label(r"main.c", font_size=20, color=DATA), code(e["sources"]["main.c"].splitlines()[1:], size=14,
                                                                    color=YES)).arrange(DOWN, aligned_edge=LEFT)
        b = VGroup(label(r"lib.c", font_size=20, color=CTRL), code(e["sources"]["lib.c"].splitlines(), size=14,
                                                                   color=YES)).arrange(DOWN, aligned_edge=LEFT)
        VGroup(a, b).arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(head, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        cmd = code(["gcc -O2 -c main.c     # -> main.o", "gcc -O2 -c lib.c      # -> lib.o",
                    "gcc main.o lib.o -o prog", f"./prog                # prints: {e['run']}"], size=16).to_edge(
            RIGHT, buff=0.5).to_edge(DOWN, buff=0.4)
        with self.voiceover("Now the same story on a real machine. <bookmark mark='a'/> Two C files. main uses a function, count, and a variable, total, that live in the other file, and it has data of its own: a pointer to a string, and a counter private to the file. <bookmark mark='b'/> lib defines count and total, and one weak variable we will come back to. <bookmark mark='c'/> Each file is compiled on its own into an object file, and then the two are linked into a program. We compiled them on this computer and read the object files with the standard tool, readelf.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(a), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(b))
            vo.wait_until('c')
            self.play(FadeIn(cmd))
        self.wait(0.3)
        self.clear_scene()

    def sections(self):
        e = load("elf")["objects"]
        head = label(r"Sections of \texttt{main.o}", font_size=34).to_edge(UP, buff=0.3)
        meaning = {".text.startup": r"main's machine code", ".text": r"machine code",
                   ".data.rel.local": r"\texttt{greeting}: \ a pointer, \ still to be fixed up",
                   ".data": r"initialised variables", ".bss": r"\texttt{calls}: \ zeroed, \ takes no space in the file",
                   ".rodata.str1.1": r"the string constants, \ read-only",
                   ".rela.text.startup": r"the holes in the code, \ and what fills them",
                   ".rela.data.rel.local": r"the hole in the pointer", ".symtab": r"the symbol table",
                   ".strtab": r"the names"}
        rows = [[s["name"], f"{s['size']}", meaning.get(s["name"], "")] for s in e["main"]["sections"]
                if s["name"] in meaning]
        t = grid_table([r"section", r"bytes", r"holds"], rows, [3.6, 1.2, 7.0], row_h=0.45, font_size=19,
                       colors=[[CODE, GREY_A, GREY_A]] * len(rows), mono_cols=(0,)).move_to(DOWN * 0.1)
        elf = note(r"the format: \ ELF, \ the Executable and Linkable Format \ (System V, \ 1988): \ Linux, \ BSD, \ "
                   r"consoles, \ Pebble's own is a toy of it", font_size=17).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "An object file is a set of named sections. <bookmark mark='a'/> Here are main dot o's. The machine "
            "code is in one section, the string constants in a read-only one. The pointer greeting gets a section "
            "of its own, because its value, the address of the string, is not known yet. The private counter goes "
            "in bss: a section that records only its size, since it starts as zeros and needs no space in the file. "
            "Then two sections of relocations, the holes and what fills them, and the symbol table with its names. "
            "<bookmark mark='b'/> The format is ELF, from AT and T's System V in 1988, used today by Linux, the "
            "BSDs and most game consoles. Pebble's object files are a toy version of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.3),
                      run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(elf))
        self.wait(0.3)
        self.clear_scene()

    def symbols(self):
        e = load("elf")["objects"]
        head = label(r"Symbols and relocations", font_size=34).to_edge(UP, buff=0.3)
        syms = [s for s in e["main"]["symbols"] if s["type"] in ("FUNC", "OBJECT", "NOTYPE") and
                not s["name"].startswith(".")] + [s for s in e["lib"]["symbols"] if s["type"] in ("FUNC", "OBJECT")]
        rows = []
        for s in syms:
            where = "undefined" if s["ndx"] == "UND" else "defined"
            f = "main.o" if s in e["main"]["symbols"] else "lib.o"
            rows.append([f, s["name"], s["bind"].lower(), where])
        colors = [[GREY_B, CODE, YES if r[2] == "global" else (CTRL if r[2] == "weak" else GREY_B),
                   NO if r[3] == "undefined" else GREY_A] for r in rows]
        t = grid_table([r"file", r"symbol", r"binding", r""], rows, [1.6, 2.6, 1.6, 2.0], row_h=0.4, font_size=18,
                       colors=colors, mono_cols=(1,))
        t.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.5)
        rel = [[r["type"].replace("R_X86_64_", ""), r["symbol"]] for r in e["main"]["relocs"]]
        t2 = grid_table([r"relocation", r"for"], rel, [2.0, 2.6], row_h=0.4, font_size=18,
                        colors=[[FUNC, CODE]] * len(rel), mono_cols=(1,))
        t2.to_edge(RIGHT, buff=0.5).align_to(t, UP)
        kinds = note(r"PC32: \ a 32-bit distance from here; \ PLT32: \ a call, \ maybe through the PLT \ (chapter 11); "
                     r"\ 64: \ a whole address", font_size=16).to_edge(DOWN, buff=0.3)
        aside = note(r"\texttt{lib.o} calls \texttt{strlen}: \ gcc recognised the counting loop", font_size=16).next_to(
            kinds, UP, buff=0.1)
        with self.voiceover("The symbol table says what each file offers and what it needs. <bookmark mark='a'/> main dot o defines main and greeting as global symbols, visible to other files, and the counter as local. It lists total, count and the C library's printf as undefined: used here, defined elsewhere. lib dot o defines count and total, globally, and verbose as weak. And it needs strlen: the optimizer recognised count's loop as a string length and replaced it with a call to the library. <bookmark mark='b'/> The relocations say exactly which bytes depend on which symbol, and how: here, a 32-bit distance from the instruction to the target, a call that may go through a table we meet in chapter eleven, or a whole 64-bit address for the pointer.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule), LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.2), FadeIn(aside), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(t2), FadeIn(kinds))
        self.wait(0.3)
        self.clear_scene()

    def rules(self):
        e = load("elf")
        head = label(r"The linker's rules", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label("referenced strong symbols need a selected definition; unresolved weak symbols have special rules", font_size=22, color=GREY_A),
            label(r"two \textit{strong} definitions of one name: \ an error", font_size=22, color=NO),
            label(r"one strong and any number of \textit{weak}: \ the strong one wins", font_size=22, color=YES),
            label(r"only weak ones: \ any one of them \ (the first, \ in practice)", font_size=22, color=CTRL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.4)
        errs = VGroup(label(r"what this machine's linker said:", font_size=19, color=GREY_B))
        for k in ("undefined", "duplicate"):
            for line in e["errors"][k][:1]:
                errs.add(Text(line.split(";")[0][:78], font="DejaVu Sans Mono", font_size=14, color=NO))
        errs.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(pts, DOWN, buff=0.5)
        use = note(r"weak symbols let a library offer a default that a program may replace: \ a default "
                   r"\texttt{malloc}, \ a default handler", font_size=18).to_edge(DOWN, buff=0.35)
        with self.voiceover("For this static-link example, distinguish definitions from references and binding strength. <bookmark mark='a'/> An ordinary referenced strong symbol must resolve to a definition in the final link. Unresolved weak references have special platform rules and can resolve to zero. <bookmark mark='b'/> Multiple ordinary strong definitions are an error in this example. <bookmark mark='c'/> A selected strong definition takes precedence over weak definitions. <bookmark mark='d'/> If only weak definitions exist, the linker selects one under its rules; source code should not depend on an unspecified choice among differing implementations. <bookmark mark='e'/> Leaving out lib produces undefined references; including it twice produces duplicate strong definitions. Weak defaults are one override mechanism. Dynamic symbol interposition and library-specific hooks have related but different resolution rules.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, p in zip('abcd', pts):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until('e')
            self.play(FadeIn(errs), FadeIn(use))
        self.wait(0.3)
        self.clear_scene()
