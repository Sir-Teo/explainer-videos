from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


class Time(VoiceoverScene):
    def construct(self):
        self.card()
        self.blink()
        self.bottleneck()

    def card(self):
        card = chapter_card(7, r"Attention in time", r"Can you attend to two things a moment apart?",
                            lit={1992: r"Raymond et al.", 1994: r"Pashler"}, part=PART, scale=("mind",),
                            marr=("what", "how"))
        with self.voiceover("Chapter seven. Attention in time."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def blink(self):
        d = load("blink")
        r = archive.RAYMOND_1992.data
        head = heading(r"The attentional blink")
        stream = VGroup()
        letters = "KPFTRZXBLMVH"
        for k, ch in enumerate(letters):
            col = TARGET if k == 3 else (ATT if k == 6 else GREY_B)
            stream.add(label(ch, font_size=34, color=col))
        stream.arrange(RIGHT, buff=0.32).move_to([0, 2.3, 0])
        t1 = label(r"T1: \ the odd colour", font_size=19, color=TARGET).next_to(stream[3], DOWN, buff=0.15)
        t2 = label(r"T2: \ was there an X?", font_size=19, color=ATT).next_to(stream[6], DOWN, buff=0.5)
        A = axes([0.5, 8.5], [0.3, 1.0], x_length=6.0, y_length=2.6, xticks=list(range(1, 9)), yticks=[0.4, 0.7, 1.0],
                 xlabel=r"lag: \ items from T1 to T2, \ 100 ms each", ylabel=r"P(T2 seen $\mid$ T1 seen)",
                 center=[-2.4, -0.9, 0], font_size=17)
        ax = A.ax
        win = Rectangle(width=ax.c2p(r["window_end_ms"] / 100, 0)[0] - ax.c2p(r["window_start_ms"] / 100, 0)[0],
                        height=ax.c2p(0, 1.0)[1] - ax.c2p(0, 0.3)[1], stroke_width=0, fill_color=CONFLICT,
                        fill_opacity=0.15)
        win.move_to(ax.c2p(r["window_start_ms"] / 100, 0.3), aligned_edge=DL)
        wl = wrapped_label(rf"{r['window_start_ms']} to {r['window_end_ms']} ms: \ the blink Raymond and colleagues "
                           r"found", 1.8, 15, CONFLICT).move_to(win.get_bottom() + UP * 0.3)
        c = VGroup(curve(ax, d["lags"], d["p"], ATT, 4), scatter(ax, d["lags"], d["p"], ATT, 0.07, 1))
        rows = rows_of([
            (r"letters at ten a second; \ name the one in an odd colour, \ then say whether an X followed", WHITE),
            (r"if T2 comes 200 to 500 ms after T1, \ it is often missed", ATT),
            (r"right after T1, \ at lag 1, \ it is spared", GOOD),
            (r"two stages: \ T1 occupies consolidation; \ T2 waits in a fragile buffer that the next letter overwrites",
             MODEL),
        ], 5.8, 23, 0.36).move_to([3.7, -0.85, 0])
        ptag = psyche_tag(r"\texttt{attention.attentional\_blink}: \ consolidation 300 ms, \ buffer decay 100 ms")
        tag = published_tag(archive.RAYMOND_1992.cite)
        with self.voiceover(
            "Attention has limits in time as well as in space. <bookmark mark='a'/> In rapid serial visual "
            "presentation, letters flash in one place, about ten a second. Your task: name the one letter in a "
            "different colour, the first target, and then say whether an X appeared afterwards. <bookmark mark='b'/> In 1992 Jane Raymond, "
            "Kimron Shapiro and Karen Arnell found that if the X came between about two hundred and five hundred "
            "milliseconds after the first target, people often missed it, though they saw it easily when they "
            "weren't also looking for the first target. They called it an attentional blink. <bookmark mark='c'/> The "
            "oddest part: an X that comes immediately after the first target is usually spared. "
            "<bookmark mark='d'/> A two-stage model explains the shape. Every letter is registered briefly. Turning a "
            "registration into something you can report takes a consolidation stage, which the first target occupies "
            "for a few hundred milliseconds. A second target that arrives meanwhile waits in a fragile buffer, and "
            "the next letter in the stream overwrites it. At lag one it slips into consolidation together with the "
            "first. Psyche's version reproduces the dip and the sparing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in stream], lag_ratio=0.15), FadeIn(rows[0]), run_time=1.5)
            self.play(FadeIn(t1), FadeIn(t2))
            vo.wait_until("b")
            self.play(FadeIn(win), FadeIn(wl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Create(c), FadeIn(ptag), run_time=2.0)
        self.clear_scene()

    def bottleneck(self):
        d = load("prp")
        head = heading(r"The psychological refractory period")
        y1, y2 = 2.4, 1.6
        sc = 0.009
        x0 = -6.2

        def bar(start, dur, y, col, txt):
            r = Rectangle(width=dur * sc, height=0.42, stroke_color=col, stroke_width=2, fill_color=col,
                          fill_opacity=0.35).move_to([x0 + (start + dur / 2) * sc, y, 0])
            return VGroup(r, label(txt, font_size=16, color=WHITE).move_to(r))

        soa = 50
        task1 = VGroup(bar(0, 100, y1, CUE, r"see"), bar(100, 150, y1, CONTROL, r"choose"), bar(250, 80, y1, GREY_B,
                                                                                              r"press"))
        wait = DashedLine([x0 + (soa + 100) * sc, y2, 0], [x0 + 250 * sc, y2, 0], color=BAD, stroke_width=3)
        task2 = VGroup(bar(soa, 100, y2, CUE, r"see"), bar(250, 150, y2, CONTROL, r"choose"), bar(400, 80, y2, GREY_B,
                                                                                                 r"press"))
        wl = label(r"waits", font_size=16, color=BAD).next_to(wait, DOWN, buff=0.05)
        names = VGroup(label(r"task 1", font_size=18, color=GREY_A).next_to(task1, LEFT, buff=0.15),
                       label(r"task 2", font_size=18, color=GREY_A).next_to(task2, LEFT, buff=0.15))
        A = axes([0, 1000], [300, 520], x_length=5.0, y_length=2.4, xticks=[0, 250, 500, 750, 1000],
                 yticks=[300, 400, 500], xlabel=r"SOA: \ time between the two stimuli, \ ms",
                 ylabel=r"RT to the second, \ ms", center=[3.6, 1.0, 0], font_size=16)
        ax = A.ax
        c = VGroup(curve(ax, d["soa"], d["rt2"], ATT, 4), scatter(ax, d["soa"], d["rt2"], ATT, 0.06, 1))
        slope = DashedLine(ax.c2p(0, d["rt2"][0]), ax.c2p(150, d["rt2"][0] - 150), color=GREY_B, stroke_width=2)
        sl = label(r"slope $-1$", font_size=17, color=GREY_B).next_to(ax.c2p(150, d["rt2"][0] - 150), RIGHT,
                                                                         buff=0.1)
        rows = rows_of([
            (r"two stimuli, \ two responses: \ a tone to answer by voice, \ a letter to answer by key", WHITE),
            (r"the closer together they come, \ the slower the second response", ATT),
            (r"perceiving overlaps; \ choosing a response does not: \ one decision at a time", CONTROL),
            (r"so at short SOAs every millisecond earlier the second stimulus arrives is a millisecond longer wait: "
             r"\ slope $-1$", MODEL),
            (r"Part 1's stage model, \ with one stage that cannot be shared", GREY_A),
        ], 12.4, 23, 0.16).to_edge(DOWN, buff=0.72)
        ptag = psyche_tag(r"\texttt{attention.prp}: \ gamma stages of 100, \ 150 and 80 ms")
        tag = published_tag(archive.PASHLER_1994.cite)
        with self.voiceover(
            "A second limit appears when you have to do two things, not just see them. <bookmark mark='a'/> Give "
            "people two stimuli in quick succession, each with its own response: a tone to answer by saying high or "
            "low, then a letter to answer with a key. <bookmark mark='b'/> The closer together the two arrive, the "
            "slower the response to the second, while the first is unaffected: the psychological refractory period. "
            "<bookmark mark='c'/> Harold Pashler's account, by 1994, was a central bottleneck. Perceiving the second "
            "stimulus can overlap with the first task, and so can pressing a key. But choosing a response cannot. "
            "The second task's choice waits until the first one's is done. <bookmark mark='d'/> That makes a sharp "
            "prediction. When the stimuli are close, each millisecond less between them is a millisecond more of "
            "waiting, so the second response time falls with a slope of exactly minus one, and then goes flat once "
            "there's no waiting at all. The data show that shape. <bookmark mark='e'/> It is Part 1's stage model "
            "again, with one stage that can only serve one task at a time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(names), FadeIn(task1))
            vo.wait_until("a")
            self.play(FadeIn(task2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), Create(c), FadeIn(rows[1]), FadeIn(ptag), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(wait), FadeIn(wl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(slope), FadeIn(sl), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
