from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (DATA, HEAD, NO, PART, T0C, T1C, YES, grid_table, load, mono, num)


def stack_pic(nodes, x, y_top=1.4, owned=None, color=DATA):
    """A stack drawn top-down: ``nodes`` names, top first; ``owned``: nodes a thread has popped (drawn red)."""
    g = VGroup()
    top = mono("top", 18, HEAD).move_to([x, y_top + 0.55, 0])
    g.add(top)
    prev = top
    for k, n in enumerate(nodes):
        bad = owned and n in owned
        c = NO if bad else color
        b = VGroup(RoundedRectangle(width=1.0, height=0.55, corner_radius=0.08, stroke_color=c, stroke_width=2,
                                    fill_color=c, fill_opacity=0.2), mono(n, 20, WHITE))
        b[1].move_to(b[0])
        b.move_to([x, y_top - 0.85 * k, 0])
        g.add(Arrow(prev.get_bottom(), b.get_top(), buff=0.04, color=GREY_B, stroke_width=2,
                    max_tip_length_to_length_ratio=0.35), b)
        prev = b
    return g


class LockFree(VoiceoverScene):
    def construct(self):
        self.card()
        self.treiber()
        self.aba()
        self.fixes()

    def card(self):
        card = chapter_card(11, r"Lock-free data structures", r"Can threads share a stack without a lock?",
                            lit=(1986, 1996, 2001), extra=((1986, r"Treiber stack"), (1996, r"Michael--Scott queue"),
                                                           (2001, r"RCU in Linux")), part=PART)
        with self.voiceover("Chapter eleven. Lock-free data structures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def treiber(self):
        head = label(r"Treiber's stack, \ 1986", font_size=36).to_edge(UP, buff=0.3)
        code = VGroup(mono("pop():", 20, HEAD),
                      mono("  do {", 20, WHITE),
                      mono("    t = top;", 20, WHITE),
                      mono("    if (t == NULL) return EMPTY;", 20, GREY_B),
                      mono("    n = t->next;", 20, WHITE),
                      mono("  } while (!CAS(&top, t, n));", 20, YES),
                      mono("  return t;", 20, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        box = SurroundingRectangle(code, color=GREY_D, buff=0.2, corner_radius=0.08)
        VGroup(box, code).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        st = stack_pic(["A", "B", "C"], 3.2)
        notes = VGroup(
            label(r"read the top, \ read its successor, \ then swing \texttt{top} with one CAS", font_size=21,
                  color=WHITE),
            label(r"if another thread changed \texttt{top} meanwhile, \ the CAS fails: \ retry", font_size=21,
                  color=HEAD),
            label(r"\textbf{lock-free}: \ some thread always makes progress; \ a stalled thread holds nothing up",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "With an atomic compare-and-swap, a stack needs no lock at all. Kent Treiber described this one at IBM in "
            "1986. <bookmark mark='a'/> To pop, read the top, read the node below it, and then, with one "
            "compare-and-swap, change top from the node you read to its successor. <bookmark mark='b'/> If another "
            "thread changed top in the meantime, the compare-and-swap fails, and you simply try again. <bookmark "
            "mark='c'/> This is lock-free: at any moment, some thread is making progress, and a thread that is "
            "descheduled halfway through holds nothing that others wait for. A thread holding a lock, descheduled, "
            "blocks everyone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(st))
            vo.wait_until("a")
            self.play(Create(box), FadeIn(code), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Indicate(code[5], color=YES), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def aba(self):
        d = load("aba")
        head = label(r"The ABA problem, \ found by the checker", font_size=34).to_edge(UP, buff=0.3)
        s0 = stack_pic(["A", "B", "C"], -4.6)
        c0 = label(r"T1 reads: \\ \texttt{t = A}, \ \texttt{n = B}, \\ and stalls", font_size=19, color=T0C).next_to(
            s0, DOWN, buff=0.3)
        s1 = stack_pic(["A", "C"], -0.9)
        c1 = label(r"T2 pops A, \ pops B, \\ and pushes A back", font_size=19, color=T1C).next_to(s1, DOWN, buff=0.3)
        s1.align_to(s0, UP)
        c1.align_to(c0, UP)
        s2 = stack_pic(["B", "C"], 2.8, owned={"B"})
        c2 = label(r"T1: \ \texttt{CAS(top, A, B)} \\ \textbf{succeeds}, \ since top is A again: \\ now B, \ which T2 "
                   r"owns, \ is the top", font_size=19, color=NO).next_to(s2, DOWN, buff=0.3)
        s2.align_to(s0, UP)
        c2.align_to(c0, UP)
        arr = VGroup(Arrow(s0.get_right() + RIGHT * 0.2, s1.get_left() + LEFT * 0.2, color=GREY_B, stroke_width=2),
                     Arrow(s1.get_right() + RIGHT * 0.2, s2.get_left() + LEFT * 0.2, color=GREY_B, stroke_width=2))
        n = len(d["plain"]["trace"])
        lines = VGroup(
            label(rf"the checker's schedule: \ {n} steps; \ of the {num(d['plain']['states'])} states, \ one final "
                  rf"stack contains a popped node", font_size=20, color=NO),
            label(r"the CAS compares \textit{values}: \ A came back, \ so it could not tell that the stack had "
                  r"changed underneath", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "But the checker finds a flaw, the famous ABA problem. <bookmark mark='a'/> Thread one starts a pop. It "
            "reads top, A, and A's successor, B, and then it is descheduled. <bookmark mark='b'/> Thread two pops A, "
            "pops B, and then pushes A back, reusing the node, as a memory allocator would. The stack is now A, then "
            "C. <bookmark mark='c'/> Thread one wakes, and its compare-and-swap checks that top is still A. It is, so "
            "it succeeds, and sets top to B. But B was popped by thread two, which may be using it for something else "
            "entirely. The stack is corrupted. <bookmark mark='d'/> The checker found the schedule. <bookmark "
            "mark='e'/> The compare-and-swap compares values, and the value came back, so it cannot see that "
            "everything underneath has changed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(s0), FadeIn(c0))
            vo.wait_until("b")
            self.play(GrowArrow(arr[0]), FadeIn(s1), FadeIn(c1))
            vo.wait_until("c")
            self.play(GrowArrow(arr[1]), FadeIn(s2), FadeIn(c2))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def fixes(self):
        d = load("aba")
        head = label(r"Fixing ABA, \ and freeing memory safely", font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"remedy", r"how", r"where"], [
            [r"tagged pointers", r"a version number beside \texttt{top}, \ bumped by every CAS",
             rf"checked: \ {num(d['tagged']['states'])} states, \ no corruption"],
            [r"hazard pointers \ (Michael 2004)", r"announce the node you are reading; \ nobody frees it",
             r"C++26's \texttt{std::hazard\_pointer}"],
            [r"epochs \ (Fraser 2004)", r"free a node only after every thread has moved on", r"Rust's crossbeam"],
            [r"RCU \ (McKenney 2001)", r"readers take no lock at all; \ writers copy, \ publish, \ wait, \ then free",
             r"Linux: \ over 10{,}000 uses"],
        ], widths=[3.6, 5.8, 3.6], row_h=0.62, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45)
        lines = VGroup(
            label(r"the Michael--Scott queue \ (1996) \ uses two CAS-ed pointers: \ Java's "
                  r"\texttt{ConcurrentLinkedQueue}", font_size=20, color=WHITE),
            label(r"progress: \ \textbf{wait-free} \ (every thread finishes in bounded steps) \ $\supset$ "
                  r"\textbf{lock-free} \ $\supset$ \textbf{obstruction-free}", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.15).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "There are several cures. <bookmark mark='a'/> Tag the pointer with a version number that every "
            "successful compare-and-swap increments. Then a top that comes back is still different. Our checker "
            "confirms that the tagged stack is never corrupted. <bookmark mark='b'/> Underneath ABA is a harder "
            "problem: when is it safe to free a node another thread might be reading? Hazard pointers let each thread "
            "announce the nodes it is reading, so nobody frees them. <bookmark mark='c'/> Epochs free a node only "
            "after every thread has passed a point where it could still hold one. <bookmark mark='d'/> And read-copy-"
            "update, used more than ten thousand times inside Linux, lets readers take no lock at all: a writer copies "
            "the data, publishes the new version, waits for every reader that might see the old one, and only then "
            "frees it. <bookmark mark='e'/> The Michael and Scott queue of 1996 applies the same ideas to a queue, and "
            "Java's concurrent queue is built on it. <bookmark mark='f'/> These designs are classified by the "
            "progress they guarantee: wait-free, the strongest, means every thread finishes in a bounded number of "
            "its own steps."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for mk, r in zip("abcd", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r)))
            vo.wait_until("e")
            self.play(FadeIn(lines[0]))
            vo.wait_until("f")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()
