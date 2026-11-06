from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, curve, load)


def era(year, name, lines, color, w=2.5, h=4.3):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=color, stroke_width=2, fill_color=BG,
                         fill_opacity=1)
    yr = label(str(year), font_size=34, color=color).move_to(r.get_top() + DOWN * 0.4)
    nm = label(name, font_size=25, color=WHITE).next_to(yr, DOWN, buff=0.14)
    body = VGroup(*[label(t, font_size=19, color=GREY_A) for t in lines]).arrange(DOWN, buff=0.14)
    if body.width > w - 0.25:
        body.scale_to_fit_width(w - 0.25)
    body.next_to(nm, DOWN, buff=0.22)
    return VGroup(r, yr, nm, body)


class History(VoiceoverScene):
    def construct(self):
        self.card()
        self.eras()
        self.model()

    def card(self):
        card = chapter_card(1, r"From batch to time-sharing", r"How did one computer come to serve many people?",
                            lit=(1956, 1961, 1965, 1969, 1991),
                            extra=((1956, r"GM-NAA I/O: \ batch"), (1961, r"CTSS"), (1965, r"Multics"),
                                   (1969, r"Unix"), (1991, r"Linux")), part=PART)
        with self.voiceover("Chapter one. From batch to time-sharing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def eras(self):
        head = label(r"Five systems", font_size=36).to_edge(UP, buff=0.3)
        cards = VGroup(
            era(1956, r"GM-NAA I/O", [r"General Motors and", r"North American Aviation,", r"IBM 704", r"a \textbf{batch}"
                                      r" monitor:", r"load the next job,", r"run it, print"], GREY_B),
            era(1961, r"CTSS", [r"Corbat\'o, \ MIT", r"IBM 709, \ then 7094", r"\textbf{time-sharing}:",
                                r"a slice each, \ in turn", r"up to 30 users", r"a timer and protection"], YES),
            era(1965, r"Multics", [r"MIT, \ Bell Labs, \ GE", r"a computer utility", r"rings of protection",
                                   r"a tree of files", r"dynamic linking", r"ambitious, \ late"], LAM),
            era(1969, r"Unix", [r"Thompson and Ritchie,", r"Bell Labs, \ PDP-7", r"rewritten in C, \ 1973",
                                r"processes, \ pipes,", r"files as bytes", r"CACM paper, \ 1974"], HEAD),
            era(1991, r"Linux", [r"Torvalds, \ Helsinki", r"a Unix-like kernel", r"for the 386, \ free",
                                 r"now: \ most servers,", r"Android phones,", r"all of the TOP500"], DATA),
        ).arrange(RIGHT, buff=0.18).next_to(head, DOWN, buff=0.4)
        line = label(r"the ideas of 1961--1974 \ (the mode bit, \ the process, \ the system call, \ the scheduler) "
                     r"\ are the ones in your phone", font_size=21, color=WHITE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Five systems tell the story. <bookmark mark='a'/> In 1956, General Motors and North American Aviation "
            "wrote a monitor for the IBM 704 that loaded the next job as soon as the last one finished: batch "
            "processing, and arguably the first operating system. <bookmark mark='b'/> In 1961, Fernando Corbató's "
            "group at MIT demonstrated CTSS, the Compatible Time-Sharing System. A clock interrupted each user's "
            "program after a short slice and moved to the next, and memory protection kept the programs apart. It "
            "eventually served about thirty users at once. <bookmark mark='c'/> Multics, begun in 1965 by MIT, Bell "
            "Labs and General Electric, aimed at a computer utility, like the electricity grid, with rings of "
            "protection and a tree of files. It was ambitious and late, and Bell Labs withdrew. <bookmark mark='d'/> "
            "Two of the Bell Labs people, Ken Thompson and Dennis Ritchie, then wrote something smaller on a spare "
            "PDP-7 in 1969: Unix. They rewrote it in C in 1973 and described it in 1974. <bookmark mark='e'/> In 1991 "
            "a Finnish student, Linus Torvalds, announced a free Unix-like kernel for his PC. Today Linux runs most "
            "servers, every Android phone, and every one of the five hundred fastest supercomputers. <bookmark "
            "mark='f'/> The ideas in this part were all settled between 1961 and 1974, and they are the ones in the "
            "phone in your pocket."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcde", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(line))
        self.wait(0.3)
        self.clear_scene()

    def model(self):
        h = load("history")
        head = label(r"How many users can share one machine?", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 60, 10], y_range=[0, 22, 5], x_length=6.4, y_length=3.9,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in range(0, 61, 10)])
        yt = VGroup(*[label(str(y), font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in range(0, 21, 5)])
        xl = label(r"users $N$", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"response time, \ seconds", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        rows = h["rows"]
        sim = curve(ax, [r["N"] for r in rows], [r["R"] for r in rows], YES)
        S, Z = h["S"], h["Z"]
        flat = DashedLine(ax.c2p(0, S), ax.c2p(60, S), color=GREY_B, stroke_width=1.5)
        slope = DashedLine(ax.c2p((S + Z) / S, S), ax.c2p(60, 60 * S - Z), color=NO, stroke_width=2)
        knee = Dot(ax.c2p(h["nstar"], S), color=HEAD, radius=0.07)
        kl = label(rf"$N^* = (S + Z)/S = {h['nstar']:.0f}$", font_size=19, color=HEAD).next_to(knee, DOWN + RIGHT,
                                                                                               buff=0.12)
        notes = VGroup(
            label(rf"each user: \ think $Z = {Z:.0f}$ s, \\ then ask for $S = {S}$ s of processor", font_size=20,
                  color=WHITE),
            label(r"simulated: \ the processor shared equally \\ among the waiting jobs", font_size=20, color=YES),
            label(r"few users: \ nobody waits; \ $R \approx S$", font_size=20, color=GREY_A),
            label(r"past $N^*$: \ the processor is always busy; \\ each extra user adds $S$ for \textbf{everyone}: "
                  r"\ $R = NS - Z$", font_size=20, color=NO),
            label(rf"the law $R = N/X - Z$ holds: \\ at $N = 40$, \ ${rows[8]['R']:.2f}$ against "
                  rf"${rows[8]['law']:.2f}$", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.55).align_to(ax, UP)
        for n_ in notes:
            if n_.width > 5.6:
                n_.scale_to_fit_width(5.6)
        with self.voiceover(
            "How many users can share one machine? Treat each user as a loop. <bookmark mark='a'/> Think for ten "
            "seconds, then ask for half a second of processor time, and wait for the answer. <bookmark mark='b'/> We "
            "simulated this, with the processor shared equally among everyone waiting, which is what fast "
            "time-slicing approximates. <bookmark mark='c'/> With a few users, nobody waits: the response time is the "
            "half second of work. <bookmark mark='d'/> But the processor can only do two jobs per second, and twenty "
            "users thinking ten seconds each ask for about two per second. Past twenty-one users, the machine is "
            "always busy, and each additional user adds half a second to everybody's response. <bookmark mark='e'/> "
            "The knee sits where the two straight lines meet, and the simulation follows them. <bookmark mark='f'/> "
            "This is the interactive response time law, from the theory of closed queues: response equals users "
            "over throughput, minus think time. We will come back to queues in chapter twelve."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(sim), FadeIn(notes[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(flat), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(Create(slope), FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(knee), FadeIn(kl))
            vo.wait_until("f")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()
