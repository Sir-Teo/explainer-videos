from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (BG, HEAD, LAM, NO, PART, T0C, T1C, T2C, YES, load, mono, num)


class Monitors(VoiceoverScene):
    def construct(self):
        self.card()
        self.monitor()
        self.mesa()

    def card(self):
        card = chapter_card(7, r"Monitors and condition variables", r"Why \texttt{while} and not \texttt{if}?",
                            lit=(1974, 1980), extra=((1974, r"Hoare: \ monitors"), (1980, r"Lampson and Redell: \ Mesa")),
                            part=PART)
        with self.voiceover("Chapter seven. Monitors and condition variables."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def monitor(self):
        head = label(r"A monitor: \ data, \ a lock, \ and conditions", font_size=34).to_edge(UP, buff=0.3)
        box = RoundedRectangle(width=6.2, height=3.6, corner_radius=0.15, stroke_color=HEAD, stroke_width=2,
                               fill_color=BG, fill_opacity=1).move_to([-3.0, 0.2, 0])
        inner = VGroup(label(r"the buffer's data", font_size=20, color=WHITE),
                       label(r"one lock: \ only one thread inside", font_size=20, color=HEAD),
                       label(r"condition \texttt{nonempty}: \ a queue of sleepers", font_size=20, color=LAM),
                       label(r"\texttt{wait(c)}: \ release the lock and sleep, \ \textbf{atomically}", font_size=20,
                             color=WHITE),
                       label(r"\texttt{signal(c)}: \ wake one sleeper", font_size=20, color=WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).move_to(box)
        side = VGroup(
            label(r"Hoare \ (1974) \ and Brinch Hansen \ (1975): \\ the compiler puts the lock around every \\ "
                  r"operation, \ so it cannot be forgotten", font_size=20, color=WHITE),
            label(r"Java's \texttt{synchronized}, \\ \texttt{wait} and \texttt{notify}; \\ pthreads' "
                  r"\texttt{pthread\_cond\_t}", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(box, RIGHT, buff=0.6).align_to(box, UP)
        with self.voiceover(
            "Hoare in 1974, and Brinch Hansen, proposed a structure instead: the monitor. <bookmark mark='a'/> A "
            "monitor bundles shared data with a lock, and the language itself takes the lock around every operation, "
            "so it cannot be forgotten. <bookmark mark='b'/> For waiting, it has condition variables. Wait releases "
            "the lock and goes to sleep, as one atomic step, so no signal can be lost between them. Signal wakes one "
            "sleeper. <bookmark mark='c'/> This is Java's synchronized methods with wait and notify, and the condition "
            "variables of every threads library."
        ) as vo:
            self.play(FadeIn(head), Create(box))
            vo.wait_until("a")
            self.play(FadeIn(inner[:2]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(inner[2:]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
        self.wait(0.3)
        self.clear_scene()

    def mesa(self):
        d = load("monitor")
        head = label(r"Mesa semantics: \ \texttt{if} is a bug", font_size=34).to_edge(UP, buff=0.3)
        code_if = VGroup(mono("lock(m)", 18, GREY_B), mono("if (count == 0)", 18, NO), mono("    wait(nonempty)", 18,
                                                                                              WHITE),
                         mono("count = count - 1", 18, WHITE), mono("unlock(m)", 18, GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06)
        code_wh = VGroup(mono("lock(m)", 18, GREY_B), mono("while (count == 0)", 18, YES),
                         mono("    wait(nonempty)", 18, WHITE), mono("count = count - 1", 18, WHITE),
                         mono("unlock(m)", 18, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        ci = VGroup(label(r"consumer, \ with \texttt{if}", font_size=19, color=NO), code_if).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        cw = VGroup(label(r"with \texttt{while}", font_size=19, color=YES), code_wh).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        codes = VGroup(ci, cw).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        story = VGroup(
            label(r"1. \ C1 finds the buffer empty and waits", font_size=19, color=T1C),
            label(r"2. \ the producer adds an item and signals: \ C1 is \textit{woken}, \ not yet running",
                  font_size=19, color=T0C),
            label(r"3. \ C2 arrives, \ takes the lock first, \ and takes the item", font_size=19, color=T2C),
            label(r"4. \ C1 gets the lock and, \ with \texttt{if}, \ takes from an empty buffer: \ count $= -1$",
                  font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(codes, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        res = VGroup(
            label(rf"checked: \ \texttt{{if}} breaks in {len(d['if']['trace'])} steps", font_size=20, color=NO),
            label(rf"\texttt{{while}}: \ safe in all {num(d['while']['states'])} states", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(codes, RIGHT, buff=0.7).align_to(codes, UP)
        lines = label(r"Hoare's signal hands the lock to the woken thread at once; \ Mesa's \ (Lampson and Redell, "
                      r"1980) \ only makes it runnable: \ re-check after waking", font_size=20,
                      color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "But there is a subtlety, and our checker finds it. <bookmark mark='a'/> A consumer takes the lock, finds "
            "the buffer empty, and waits. Written with if: <bookmark mark='b'/> one producer adds an item and "
            "signals. In Hoare's original monitors, the signal would hand the lock straight to the sleeper. But real "
            "systems, starting with Xerox's Mesa language in 1980, only make the sleeper runnable. <bookmark "
            "mark='c'/> In between, a second consumer can take the lock first, and take the item. <bookmark "
            "mark='d'/> When the first consumer finally runs, it does not look again, and takes from an empty buffer. "
            "The checker finds this in twenty-nine steps. <bookmark mark='e'/> Written with while, the consumer checks "
            "again after every wake-up, and the checker finds no violation at all. So the rule in every threads "
            "library is: wait in a while loop."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ci))
            vo.wait_until("a")
            self.play(FadeIn(story[0]))
            vo.wait_until("b")
            self.play(FadeIn(story[1]), FadeIn(lines))
            vo.wait_until("c")
            self.play(FadeIn(story[2]))
            vo.wait_until("d")
            self.play(FadeIn(story[3]), FadeIn(res[0]))
            vo.wait_until("e")
            self.play(FadeIn(cw), FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()
