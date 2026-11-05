from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, load, mono,
                                   sawtooth, words)


class Hook(VoiceoverScene):
    def construct(self):
        self.question()
        self.heap()
        self.preview()
        self.plan()

    def question(self):
        h = load("hook")
        head = label(r"The Job, \ run by a machine we build", font_size=34).to_edge(UP, buff=0.3)
        src = code(["let rec bump w table =", "  match table with", "    [] -> [(w, 1)]",
                    "  | p :: rest -> if fst p = w then (w, snd p + 1) :: rest", "                else p :: bump w rest"],
                   size=19, color=CODE).to_edge(LEFT, buff=0.6).shift(UP * 1.2)
        notes = VGroup(
            label(r"every \texttt{::} builds a new cell; \ every \texttt{(w, 1)} a new pair", font_size=22,
                  color=GREY_A),
            label(r"nothing in the program ever frees one", font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(src, DOWN, buff=0.5).align_to(src, LEFT)
        stats = VGroup(
            label(rf"Part 7's chapter: \ {words(h['bytes'])} bytes of text", font_size=24, color=WHITE),
            label(rf"{words(h['allocated_words'])} words allocated: \ {h['words_per_byte']:.0f} per byte",
                  font_size=24, color=COST),
            label(rf"at most {words(h['peak_live'])} of them in use at once", font_size=24, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.6).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            "In Part 14 the Job was written in the lambda core, a language of functions, lists and pairs. A "
            "language is not a program you can run, though. Something has to run it. <bookmark mark='a'/> Look "
            "at bump. Every double colon builds a new list cell, and every pair builds a new pair. <bookmark "
            "mark='b'/> And nothing in the program ever gives one back. There is no free. <bookmark mark='c'/> On "
            "the chapter of Part 7, four thousand seven hundred bytes of text, the Job allocates three hundred and "
            "seventy thousand words of memory, seventy-nine words for every byte it reads. <bookmark mark='d'/> "
            "Yet at any moment it is using at most twenty-seven thousand of them. The rest is garbage, and "
            "someone has to take it away."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(stats[:2]))
            vo.wait_until("d")
            self.play(FadeIn(stats[2]))
        self.wait(0.3)
        self.clear_scene()

    def heap(self):
        h = load("hook")
        head = label(r"The heap, \ filling and emptying", font_size=34).to_edge(UP, buff=0.3)
        ax, curve, drops = sawtooth(h["log"], h["semispace"], h["allocated_words"])
        ax.move_to(DOWN * 0.1)
        top = DashedLine(ax.c2p(0, h["semispace"]), ax.c2p(h["allocated_words"], h["semispace"]), color=NO,
                         stroke_width=1.5, dash_length=0.08)
        lab_top = label(rf"the heap: \ {words(h['semispace'])} words", font_size=19, color=NO).next_to(
            top, UP, buff=0.08).align_to(top, RIGHT)
        xl = label(r"words allocated so far", font_size=19, color=GREY_B).next_to(ax, DOWN, buff=0.25)
        yl = label(r"words in use", font_size=19, color=GREY_B).next_to(ax, LEFT, buff=0.2).rotate(PI / 2)
        cap = VGroup(
            label(rf"{h['gcs']} collections: \ each finds what is still reachable, \ and keeps only that",
                  font_size=22, color=YES),
            label(r"the program never notices: \ this part builds the machine that does it", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "This is the Job's heap as it runs, on the virtual machine this part builds. <bookmark mark='a'/> "
            "Memory fills as the program allocates. <bookmark mark='b'/> When the heap is full, the garbage "
            "collector stops the program, finds every object it can still reach, and keeps only those. The heap "
            "drops back to the live data, and the program carries on, never knowing. <bookmark mark='c'/> Eight "
            "times on this text. How the collector finds what is live, how fast it can do it, and how it can do "
            "it while the program keeps running, is half of this part."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), Create(top), FadeIn(lab_top))
            vo.wait_until("a")
            self.play(Create(curve), run_time=5, rate_func=linear)
            vo.wait_until("b")
            self.play(LaggedStart(*[Flash(d, color=YES, flash_radius=0.18) for d in drops], lag_ratio=0.15),
                      FadeIn(drops))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def preview(self):
        head = label(r"By the end of this part", font_size=40).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"closures: \ how a function remembers where it was made", font_size=27, color=LAM),
            label(r"continuations: \ the call stack, \ turned into data", font_size=27, color=CTRL),
            label(r"a bytecode machine, \ written in the Pebble language, \ running on Pebble", font_size=27,
                  color=DATA),
            label(r"four garbage collectors, \ and the invariant that lets one run concurrently", font_size=27,
                  color=YES),
            label(r"how a JIT makes a dynamic language fast, \ measured on this machine", font_size=27, color=HEAD),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is where we are going. <bookmark mark='a'/> Closures: how a function remembers the place where "
            "it was made, long after that place is gone. <bookmark mark='b'/> Continuations: the call stack, "
            "turned into a value you can hold. <bookmark mark='c'/> A bytecode virtual machine for the lambda "
            "core, written in the Pebble language and running on Pebble itself. <bookmark mark='d'/> Four garbage "
            "collectors, and the three-colour invariant that lets a collector run while the program is still "
            "changing the heap. <bookmark mark='e'/> And just-in-time compilers, which make dynamic languages fast, "
            "measured on real runtimes on this machine."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcde", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Runtimes", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"interpreters, \ environments and closures",
            r"continuations, \ CPS and tail calls",
            r"bytecode virtual machines and dispatch",
            r"reference counting, \ tracing, \ copying and generational collection",
            r"incremental collection: \ the tri-color invariant",
            r"JITs, \ dynamic dispatch, \ exceptions, \ WebAssembly",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 15 of Computer Science, Built: Runtimes, the last part of Act Three. We have a machine, a "
            "compiler, and a language with types. Now we give the language somewhere to live. <bookmark "
            "mark='a'/> In this part: interpreters, environments and closures; continuations and tail calls; "
            "bytecode machines and the cost of dispatch; reference counting, tracing, copying and generational "
            "collection; collecting while the program runs; and just-in-time compilers, dynamic dispatch, "
            "exceptions and WebAssembly."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
