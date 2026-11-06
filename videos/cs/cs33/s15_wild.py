from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (HEAD, LAM, NO, PART, YES, load, mono, num)


class Wild(VoiceoverScene):
    def construct(self):
        self.card()
        self.cases()
        self.detectors()

    def card(self):
        card = chapter_card(14, r"Concurrency bugs in the wild", r"What happens when a race escapes?",
                            lit=(1985, 2003), extra=((1985, r"Therac-25"), (2003, r"the Northeast blackout")),
                            part=PART)
        with self.voiceover("Chapter fourteen. Concurrency bugs in the wild."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cases(self):
        head = label(r"Three races that escaped", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(*[VGroup(label(t, font_size=24, color=c), label(s, font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08) for t, s, c in (
            (r"Therac-25, \ 1985--87", r"a radiation machine: \ a fast operator's edit raced the task setting up the "
                                      r"beam; \ six massive overdoses \ (Leveson and Turner, 1993)", NO),
            (r"Mars Pathfinder, \ 1997", r"priority inversion through a shared lock: \ Part 31's watchdog resets, \ "
                                        r"fixed from Earth", LAM),
            (r"the Northeast blackout, \ 2003", r"a race in an alarm system's event handling silenced its alarms; \ "
                                                r"operators missed the cascade: \ 50 million people without power",
             HEAD),
            (r"what they share", r"rare schedules, \ invisible in testing, \ certain at scale", WHITE),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Races are not just lost increments. <bookmark mark='a'/> The Therac-25 radiation therapy machine, in the "
            "mid nineteen-eighties: an operator who edited the treatment settings quickly could race the software task "
            "that configured the beam, and the machine delivered massive overdoses. Six patients were harmed, and "
            "Nancy Leveson's investigation became required reading for engineers. <bookmark mark='b'/> Mars "
            "Pathfinder, which Part 31 met: priority inversion through a shared lock, and a rover that kept "
            "resetting itself. <bookmark mark='c'/> And in 2003, a race in the alarm software of an Ohio power "
            "company silenced its alarms; operators did not see the failures spreading, and fifty million people lost "
            "power. <bookmark mark='d'/> What these share: schedules too rare to show up in testing, and certain to "
            "occur in years of operation."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def detectors(self):
        d = load("tsan")
        head = label(r"Race detectors", font_size=36).to_edge(UP, buff=0.3)
        rep = VGroup(*[mono(t, 16, NO if "WARNING" in t else WHITE) for t in d["racy"]["lines"][:6]]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06)
        box = SurroundingRectangle(rep, color=GREY_D, buff=0.15, corner_radius=0.08)
        rl = label(r"ThreadSanitizer on the hook's program, \ on this machine:", font_size=19,
                   color=GREY_A).next_to(box, UP, buff=0.1).align_to(box, LEFT)
        rg = VGroup(rl, box, rep).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        aw = d["atomic_rw"]
        ai = d["atomic_inc"]
        notes = VGroup(
            label(r"how: \ a \textbf{vector clock} per thread and per variable \\ tracks happens-before \ (Part 38); "
                  r"\\ two accesses not ordered by it: \ a race", font_size=19, color=WHITE),
            label(rf"make \texttt{{count}} atomic but keep \\ \texttt{{count = count + 1}}: \ no warning, \\ yet it "
                  rf"printed {num(int(aw['printed']))} of 2{{,}}000{{,}}000", font_size=19, color=NO),
            label(rf"\texttt{{count += 1}} on the atomic: \\ {num(int(ai['printed']))}: \ correct", font_size=19,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rg, RIGHT, buff=0.5).align_to(rg, UP)
        lines = VGroup(
            label(r"a detector finds \textbf{data races}, \ not every \textbf{race}: \ atomic steps can still be "
                  r"combined wrongly", font_size=20, color=HEAD),
            label(r"Eraser \ (1997, \ locksets); \ FastTrack and ThreadSanitizer \ (2009); \ Go's \texttt{-race}; "
                  r"\ Rust rejects data races at compile time", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Tools now catch many of these. <bookmark mark='a'/> Here is ThreadSanitizer, built into the C compiler, "
            "run on the hook's program on this machine. It reports a data race on count, on line four, between a "
            "read in one thread and a write in another. <bookmark mark='b'/> It works by keeping a vector clock for "
            "every thread and every variable, Lamport's happens-before relation made concrete, which Part 38 builds. "
            "Two accesses that the clocks do not order are a race. <bookmark mark='c'/> But notice what happens if we "
            "make count an atomic variable and keep the same code. ThreadSanitizer is silent, because every load and "
            "every store is now atomic. And the program still loses updates: it printed one point two million, "
            "out of two million. <bookmark mark='d'/> Using the atomic increment, plus-equals, gives exactly two "
            "million. <bookmark mark='e'/> So a detector finds data races, not every race: atomic steps can still be "
            "combined wrongly, and only reasoning, or a model checker, finds that. <bookmark mark='f'/> Detectors go "
            "back to Eraser in 1997. Go has one built in, and Rust's type system rejects data races before the "
            "program even runs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rl), Create(box), LaggedStart(*[FadeIn(r) for r in rep], lag_ratio=0.15))
            for mk, n_ in zip("bcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
            for mk, ln in zip("ef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()
