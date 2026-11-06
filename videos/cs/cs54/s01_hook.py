from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono


def card_(title, when, what, col, w=4.2, h=3.0):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    g = VGroup(label(title, font_size=24, color=col), label(when, font_size=17, color=GREY_B),
               wrapped_label(what, w - 0.4, font_size=17, color=GREY_A)).arrange(DOWN, buff=0.2).move_to(frame)
    return VGroup(frame, g)


class Hook(VoiceoverScene):
    def construct(self):
        self.bugs()
        self.midpoint()
        self.plan()

    def bugs(self):
        head = label(r"Three bugs", font_size=36).to_edge(UP, buff=0.3)
        cards = VGroup(
            card_(r"Ariane 5", r"4 June 1996", r"a 64-bit floating-point value converted to a 16-bit integer "
                  r"overflowed in reused code; \ the rocket destroyed itself 37 seconds after launch", NO),
            card_(r"Therac-25", r"1985--1987", r"race conditions in a radiation-therapy machine's software gave "
                  r"massive overdoses; \ patients died", HEAD),
            card_(r"Heartbleed", r"2014", r"one missing bounds check in OpenSSL let anyone read up to 64 kB of a "
                  r"server's memory, \ keys included", LAM),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.5)
        quote = wrapped_label(r"``Program testing can be used to show the presence of bugs, \ but never to show "
                              r"their absence.'' \ --- Edsger Dijkstra, \ 1970", 12.0, font_size=21,
                              color=WHITE).next_to(cards, DOWN, buff=0.5)
        src = note(r"inquiry board report \ (1996); \ Leveson and Turner \ (1993); \ CVE-2014-0160", font_size=16
                   ).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Three bugs. <bookmark mark='a'/> In 1996 the first Ariane 5 rocket destroyed itself thirty-seven "
            "seconds after launch, because reused code converted a sixty-four-bit floating-point number to a "
            "sixteen-bit integer, and it overflowed. <bookmark mark='b'/> Between 1985 and 1987 race conditions in "
            "the software of the Therac-25 radiation machine gave patients massive overdoses, and some died. "
            "<bookmark mark='c'/> In 2014 a single missing bounds check in OpenSSL let anyone read secrets out of a "
            "server's memory. <bookmark mark='d'/> All three programs had been tested. Edsger Dijkstra said it in "
            "1970: testing can show that bugs are present, never that they are absent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for mk, c in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(quote))
        self.wait(0.4)
        self.clear_scene()

    def midpoint(self):
        m = load("hoare")["midpoints"]
        bad, good = m[0], m[4]
        ce = bad["counterexample"]
        head = label(r"A bug in a textbook algorithm, \ found by a SAT solver", font_size=36).to_edge(UP, buff=0.3)
        code = VGroup(mono("mid = (lo + hi) >> 1", size=26, color=NO),
                      mono("mid = lo + ((hi - lo) >>> 1)", size=26, color=YES)).arrange(DOWN, buff=0.8,
                                                                                         aligned_edge=LEFT)
        code.next_to(head, DOWN, buff=0.7).to_edge(LEFT, buff=1.0)
        need = label(r"must hold: \ $lo \le mid < hi$", font_size=24, color=WHITE).next_to(code, UP, buff=0.35).align_to(
            code, LEFT)
        s = ce["lo"] + ce["hi"]
        wrapped = s - 65536 if s >= 32768 else s
        r1 = wrapped_label(rf"SAT, \ in {bad['seconds']:.2f} s: \ $lo = {ce['lo']:,}$, \ $hi = {ce['hi']:,}$; \ "
                           rf"their sum {s:,} wraps to {wrapped:,} in 16 bits", 6.2, font_size=20,
                           color=NO).next_to(code[0], RIGHT, buff=0.6)
        r2 = wrapped_label(rf"UNSAT: \ proved for every 16-bit $lo < hi$ \ ({good['vars']:,} variables, \ "
                           rf"{good['clauses']:,} clauses)", 6.2, font_size=20, color=YES).next_to(code[1], RIGHT,
                                                                                                buff=0.6)
        foot = wrapped_label(r"Joshua Bloch \ (2006): \ the overflow sat in Java's binary search for nine years; \ "
                             r"Rice's theorem \ (Part 25) \ forbids deciding correctness in general, \ so this part "
                             r"goes around it three ways", 12.4, font_size=19, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is a bug of the famous kind. <bookmark mark='a'/> Binary search needs the midpoint to lie between "
            "low and high. The textbook line adds them and halves the sum. <bookmark mark='b'/> We turned that "
            "requirement into a logical formula over sixteen-bit integers and handed it to our own SAT solver from "
            f"Part 26. In {bad['seconds']:.1f} seconds it found a counterexample: their sum overflows, wraps to a "
            "negative number, and the midpoint falls outside the range. <bookmark mark='c'/> The repaired line, "
            "which shifts the difference without a sign, makes the formula unsatisfiable: correct for every "
            "sixteen-bit input, a proof, not a test. <bookmark mark='d'/> Joshua Bloch reported in 2006 that this "
            "overflow had sat in Java's binary search for nine years. Rice's theorem says correctness cannot be "
            "decided in general, so this part goes around it three ways."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(need), FadeIn(code[0]))
            vo.wait_until("b")
            self.play(FadeIn(r1))
            vo.wait_until("c")
            self.play(FadeIn(code[1]), FadeIn(r2))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Proving Programs Correct", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"Floyd--Hoare logic, \ invariants and variants",
            r"weakest preconditions, \ checked by our SAT solver",
            r"separation logic for the heap",
            r"model checking, \ explicit, \ symbolic and bounded",
            r"abstract interpretation and proof assistants",
            r"verified systems; \ fuzzing our own compiler",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 54 of Computer Science, Built. <bookmark mark='a'/> The three ways around Rice's theorem "
            "are to write the invariants ourselves, to exhaust a finite state space, or to approximate soundly. We "
            "will prove programs with Hoare logic and weakest preconditions; reason about the heap with separation "
            "logic; model-check protocols explicitly, symbolically and with SAT; analyse programs by abstract "
            "interpretation; meet the proof assistants that check mathematics and the systems proved with them; and "
            "fuzz our own compiler until it confesses."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM, NO, YES)
