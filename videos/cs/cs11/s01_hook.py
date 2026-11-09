from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, COST, CTRL, DATA, FILE_COLORS, FUNC, HEAD, NO, PART, YES, code, load,
                                   region)


class Hook(VoiceoverScene):
    def construct(self):
        self.files()
        self.attack()
        self.preview()
        self.plan()

    # ------------------------------------------------------------------
    def files(self):
        pl = load("pebblelink")
        job = load("job")["rows"][1]
        head = label(r"The Job, \ as four files", font_size=36).to_edge(UP, buff=0.35)
        tiles = VGroup()
        for k, o in enumerate(pl["objects"]):
            c = FILE_COLORS[k]
            t = VGroup(region(2.6, 1.3, o["name"].replace(".o", ".s"), c, font_size=24),
                       label(rf"{o['text']} bytes of code \\ {len(o['relocs'])} holes to fill", font_size=17,
                             color=GREY_A))
            t[1].next_to(t[0], DOWN, buff=0.12)
            tiles.add(t)
        tiles.arrange(RIGHT, buff=0.45).shift(UP * 0.8)
        arrow = Arrow(UP * -0.5, DOWN * 1.3, color=HEAD, stroke_width=4)
        linked = region(8.0, 0.7, rf"one program: \ {pl['image']} bytes, \ entry at address 0", HEAD, font_size=22)
        linked.next_to(arrow, DOWN, buff=0.15)
        res = label(rf"chapter 1: \ the same top twenty as Part 6's program, \ "
                    rf"{job['v1']:,} instructions against {job['v0']:,}", font_size=22, color=YES).to_edge(DOWN,
                                                                                                    buff=0.35)
        with self.voiceover("Until now every Pebble program has been one file of assembly, written by hand, that the machine runs from address zero. Real programs are not like that. <bookmark mark='a'/> Here is the Job again, written the way a compiler would write it: four separate files. The main loop; the word table, now a linked list of nodes on a heap; a memory allocator; and the input and output routines. Each is assembled on its own, and each has holes in it: places where it uses a name, like lookup or alloc, whose address it cannot know. <bookmark mark='b'/> A linker fills the holes and joins the four into one program. <bookmark mark='c'/> It prints exactly the same twenty words as Part 6's program, and on the first chapter it is even a little faster.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in tiles], lag_ratio=0.25), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(GrowArrow(arrow), FadeIn(linked))
            vo.wait_until('c')
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def attack(self):
        sm = load("smash")
        head = label(r"And a program that does what its author never wrote", font_size=32).to_edge(UP, buff=0.35)
        prog = code(["greet: ask for a name, say hello", "  char buffer[64];", "  gets(buffer);      // no bound",
                     "  print(\"hello, \", buffer);"], size=20).shift(UP * 0.9)
        ok = VGroup(label(r"input \texttt{Ada}:", font_size=22, color=GREY_A),
                    Text("hello, Ada", font="DejaVu Sans Mono", font_size=22, color=YES)).arrange(RIGHT, buff=0.3)
        bad = VGroup(label(rf"an input of {len(sm['payload'])} carefully chosen bytes:", font_size=22, color=GREY_A),
                     Text("hello, ....pwned", font="DejaVu Sans Mono", font_size=22, color=NO)).arrange(RIGHT,
                                                                                               buff=0.3)
        VGroup(ok, bad).arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(prog, DOWN, buff=0.6)
        why = label(r"the input overwrote the return address on the stack, \ and the processor jumped into it",
                    font_size=22, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover("And here is a program that does something its author never wrote. <bookmark mark='a'/> It asks for a name and says hello, copying the name into a buffer of sixty-four bytes. <bookmark mark='b'/> Give it a name, and it greets you. <bookmark mark='c'/> Give it eighty-one carefully chosen bytes, and it prints pwned, a word that appears nowhere in the program. <bookmark mark='d'/> The input ran past the end of the buffer, overwrote the address the function was going to return to, and the processor returned into the input itself. To see how, and how to stop it, we need to know how a running program is laid out in memory.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(prog), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(ok))
            vo.wait_until('c')
            self.play(FadeIn(bad))
            vo.wait_until('d')
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def preview(self):
        head = label(r"By the end of this part", font_size=40).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"data in memory: \ bytes, \ alignment, \ arrays, \ pointers", font_size=27, color=DATA),
            label(r"procedures: \ the call stack, \ frames, \ calling conventions, \ recursion", font_size=27,
                  color=CTRL),
            label(r"the heap: \ five allocators on a real program's trace, \ and their theory", font_size=27,
                  color=YES),
            label(r"object files, \ linking, \ loading: \ Pebble's linker, \ and this machine's", font_size=27,
                  color=FUNC),
            label(r"undefined behaviour, \ and the stack smash: \ attack and defences", font_size=27, color=NO),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "The route through this part connects representation to behavior. <bookmark mark='a'/> Bytes, alignment, arrays and typed pointers explain where data goes. <bookmark mark='b'/> Calling conventions and frames explain how separately compiled functions cooperate. <bookmark mark='c'/> A recorded allocation trace lets us compare five simulated policies under explicit accounting rules. <bookmark mark='d'/> Object files, linking and loading connect Pebble's small implementation to compiled host examples. <bookmark mark='e'/> Finally, undefined behavior and a toy stack overwrite show why bounds, lifetime rules and defense coverage matter. Each measurement belongs to its stated program, model and build."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcde", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ The Running Program", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"a program's life: \ compiler, \ assembler, \ linker, \ loader",
            r"bytes, \ endianness, \ alignment; \ control flow and jump tables",
            r"the call stack, \ calling conventions, \ recursion and tail calls",
            r"the heap: \ free lists, \ coalescing, \ buddies; \ Knuth's rule, \ Robson's bound",
            r"object files, \ static and dynamic linking, \ the address space",
            r"undefined behaviour; \ the stack smash; \ the Job, \ linked",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 11 of Computer Science, Built, and the first part of Act Three, Speaking to the Machine. "
            "<bookmark mark='a'/> In this part: a program's life from source to process. Bytes, endianness and "
            "alignment, and control flow as machine code. The call stack, calling conventions, recursion and tail "
            "calls. The heap and its allocators, with Knuth's fifty-percent rule and Robson's bound. Object files, "
            "static and dynamic linking, and the address space. Undefined behaviour, the stack smash, and the Job, "
            "linked from four files."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
