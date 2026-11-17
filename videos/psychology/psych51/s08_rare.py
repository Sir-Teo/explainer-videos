from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Rare(VoiceoverScene):
    def construct(self):
        card_section(self, 7, r"Rare targets", r"Why are rare things missed?")
        self.prevalence()
        self.gorilla()
        self.remedies()

    def prevalence(self):
        d = load("prevalence")
        head = heading(r"If you don't find it often, \ you often don't find it")
        A = axes([0.3, 4.7], [0, 1.0], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"targets missed", center=[-3.3, 0.3, 0], font_size=12)
        x = np.arange(1, 5)
        bo = bars(A.ax, x - 0.18, d["miss_opt"], GREY_B, width=0.34)
        bp = bars(A.ax, x + 0.18, d["miss_partial"], AUTH, width=0.34)
        names = VGroup(*[label(rf"{100 * p:g}\%", font_size=14, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN,
                                                                                        buff=0.1)
                         for i, p in enumerate(d["prev"])])
        nl = label(r"targets present in", font_size=13, color=GREY_A).next_to(names, DOWN, buff=0.1)
        key = VGroup(label(r"criterion shifted all the way", font_size=13, color=GREY_B),
                     label(r"a third of the way, \ like people", font_size=13, color=AUTH)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.25)
        rows = rows_of([
            (r"Part 12's row: \ Wolfe, \ Horowitz and Kenner, \ 2005: \ a search for tools in baggage images; \ at low "
             r"prevalence, \ observers miss far more", WHITE),
            (r"the signal-detection reason: \ when targets are rare, \ saying ``no'' is usually right, \ so the "
             r"criterion drifts up", MODEL),
            (rf"an observer who shifts a third of the way misses {100 * d['miss_partial'][0]:.0f}\% at a half and "
             rf"{100 * d['miss_partial'][-1]:.0f}\% at one in a hundred", AUTH),
            (r"airport screening and cancer screening are low-prevalence searches", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.prevalence}")
        tag2 = published_tag(r"Wolfe et al.\ (2005)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Rare targets bring a second problem. <bookmark mark='a'/> Part 12 entered the row: in 2005 Jeremy Wolfe, "
            "Todd Horowitz and Naomi Kenner had people search baggage images for tools, and at low prevalence they "
            "missed far more. <bookmark mark='b'/> The signal-detection reason: when targets are rare, saying no is "
            "usually right, so the criterion drifts up. <bookmark mark='c'/> An observer who shifts only a third of "
            "the way toward the optimum misses sixteen percent when half the bags hold a target, and over forty "
            "percent when one in a hundred does. Shifting all the way would miss even more. <bookmark mark='d'/> "
            "Airport screening and cancer screening are low-prevalence searches."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(names), FadeIn(nl), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(bo))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(bp))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def gorilla(self):
        rows_section(self, r"A gorilla in the lungs", [
            (r"2013: \ Trafton Drew, \ Melissa V\~o and Jeremy Wolfe inserted a small gorilla into a lung CT scan", WHITE),
            (r"radiologists searching for nodules looked straight at it, \ eye tracking showed, \ and most did not "
             r"report it", AUTH),
            (r"experts are not immune to Part 18's inattentional blindness: \ expertise tunes search to what is "
             r"expected", PERSON),
            (r"in a screening programme, \ the unexpected finding is the one with no one looking for it", YOU),
        ], "Expert eyes miss things too. <bookmark mark='a'/> In 2013 Trafton Drew, Melissa Vo and Jeremy Wolfe "
           "inserted a small gorilla into a lung scan. <bookmark mark='b'/> Radiologists searching for nodules looked "
           "straight at it, eye tracking showed, and most of them didn't report it. <bookmark mark='c'/> Experts aren't "
           "immune to Part 18's inattentional blindness. Expertise tunes search to what is expected. "
           "<bookmark mark='d'/> In a screening programme, the unexpected finding is the one no one is looking for.",
           tag=published_tag(r"Drew, \ V\~o \& Wolfe (2013)"))

    def remedies(self):
        chips_section(self, r"What helps", [
            (r"insert targets", r"add known fake targets so prevalence feels higher and the criterion stays low; \ "
                                r"airport systems do this", GOOD),
            (r"double reading", r"two independent readers, \ or a reader and an algorithm", MODEL),
            (r"breaks", r"short watches and rotations against the decrement", PERSON),
            (r"feedback", r"tell searchers what they missed, \ so expectations match the world", SYMP),
        ], "So what helps? <bookmark mark='a'/> Insert targets: add known fake targets so prevalence feels higher and "
           "the criterion stays low. Airport systems do this. <bookmark mark='b'/> Double reading: two independent "
           "readers, or a reader and an algorithm. <bookmark mark='c'/> Breaks: short watches and rotations against "
           "the decrement. <bookmark mark='d'/> And feedback: tell searchers what they missed, so their expectations "
           "match the world.")
