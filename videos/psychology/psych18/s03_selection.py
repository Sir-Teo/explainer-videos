from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


class Selection(VoiceoverScene):
    def construct(self):
        self.card()
        self.name()
        self.attenuation()
        self.late()
        self.load_theory()

    def card(self):
        card = chapter_card(2, r"Early or late?", r"Does the ignored message reach meaning?",
                            lit={1959: r"Moray", 1960: r"Treisman", 1995: r"Lavie"}, part=PART, scale=("mind",),
                            marr=("what", "how"))
        with self.voiceover("Chapter two. Early or late?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def name(self):
        p = archive.MORAY_1959.data
        head = heading(r"Your own name gets through")
        rows = rows_of([
            (r"1959: \ Neville Moray repeats Cherry's shadowing task", WHITE),
            (r"a word list played many times in the ignored ear: \ afterwards, \ not recognized", CUE),
            (rf"but an instruction in the ignored ear, \ preceded by the listener's own name: \ about "
             rf"{pct(p['own_name_share'])} heard it", ATT),
            (r"a filter that blocks meaning cannot know which sounds are your name", BAD),
            (r"Wood and Cowan, \ 1995: \ about a third again; \ the cocktail party effect replicates", GREY_A),
        ], 12.4, 27, 0.32).move_to([0, -1.2, 0])
        headph = VGroup(Arc(radius=0.8, start_angle=0, angle=PI, color=GREY_B, stroke_width=4),
                        RoundedRectangle(width=0.28, height=0.55, corner_radius=0.1, color=CUE, fill_opacity=0.4)
                        .move_to([-0.8, -0.15, 0]),
                        RoundedRectangle(width=0.28, height=0.55, corner_radius=0.1, color=ATT, fill_opacity=0.4)
                        .move_to([0.8, -0.15, 0])).move_to([0, 2.0, 0])
        ign = VGroup(label(r"ignored, \ for example: \ ... \ table, \ river, \ table, \ river ...", font_size=22, color=CUE),
                     label(r"``\textbf{[your name]}, \ you may stop now''", font_size=22, color=ATT))
        ign.arrange(DOWN, aligned_edge=RIGHT, buff=0.15).next_to(headph, LEFT, buff=0.4)
        sh = label(r"shadowed: \ the story, \ word by word", font_size=22, color=GREY_A).next_to(headph, RIGHT, buff=0.4)
        tag = historical_tag(archive.MORAY_1959.cite)
        with self.voiceover(
            "The filter's first problem came a year later. <bookmark mark='a'/> In 1959 Neville Moray repeated "
            "Cherry's shadowing experiment. <bookmark mark='b'/> A short list of words was played over and over in "
            "the ignored ear, thirty-five times. Afterwards listeners did not recognize the words at all. "
            "<bookmark mark='c'/> But when an instruction in the ignored ear began with the listener's own name, "
            "about a third of them heard it. <bookmark mark='d'/> That is a problem for an early filter. To pass "
            "your name and nothing else, something must have recognized it as your name, and recognizing is "
            "exactly what the filter was supposed to come before. <bookmark mark='e'/> The effect replicates: in "
            "1995 Noelle Wood and Nelson Cowan found about a third again, the cocktail party effect proper."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(headph), FadeIn(sh))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "b":
                    self.play(FadeIn(ign[0]))
                if m == "c":
                    self.play(FadeIn(ign[1]))
        self.clear_scene()

    def attenuation(self):
        d = load("dichotic")
        head = heading(r"Treisman: \ an attenuator, \ not a wall")
        rows = rows_of([
            (r"1960: \ a story switches ears mid-sentence, \ and people follow it for a word or two", WHITE),
            (r"the ignored ear is turned down, \ not off", CUE),
            (r"words have thresholds: \ your name, \ or a word the sentence predicts, \ a low one", ATT),
            (r"so a turned-down signal still crosses a low threshold now and then", MODEL),
        ], 6.4, 25, 0.42).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        A = axes([0, 1], [0, 1], x_length=4.8, y_length=3.2, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xlabel=r"how much of the ignored ear gets through", ylabel=r"P(heard, \ ignored ear)",
                 center=[3.6, 0.35, 0], font_size=17)
        ax = A.ax
        cn = curve(ax, d["a"], d["sweep_name"], ATT, 4)
        cw = curve(ax, d["a"], d["sweep_word"], CUE, 3)
        mark = DashedLine(ax.c2p(0.4, 0), ax.c2p(0.4, 1), color=GREY_C, stroke_width=1.5)
        ml = label(r"0.4", font_size=16, color=GREY_B).next_to(ax.c2p(0.4, 1), UP, buff=0.05)
        lg = legend([(ATT, r"your own name"), (CUE, r"an ordinary word")], font_size=18)
        lg.next_to(ax.c2p(0, 1), RIGHT, buff=0.2).shift(DOWN * 0.75)
        k = d["words"].index("own name")
        res = label(rf"at 0.4: \ name {pct(d['attenuate'][k])}, \ ordinary word "
                    rf"{pct(d['attenuate'][d['words'].index('an ordinary word')], 1)}; \ with a filter, \ both 0",
                    font_size=18, color=MODEL).next_to(A, DOWN, buff=0.15)
        ptag = psyche_tag(r"\texttt{attention.dichotic}: \ signal plus noise against each word's threshold")
        tag = historical_tag(archive.TREISMAN_1960.cite)
        with self.voiceover(
            "Anne Treisman, then a graduate student at Oxford, proposed a repair. "
            "<bookmark mark='a'/> In 1960 she had people shadow a story in one ear while, mid-sentence, the story "
            "jumped to the other ear and a different text took its place. People often followed the story across "
            "for a word or two before catching themselves. Meaning was steering them from the ignored ear. "
            "<bookmark mark='b'/> Her proposal: the ignored channel isn't blocked, it's attenuated, turned down. "
            "<bookmark mark='c'/> And words have thresholds of recognition. Your name has a permanently low one; a "
            "word the sentence predicts has a temporarily low one. <bookmark mark='d'/> Psyche can make that "
            "precise. A word's signal is its strength, attenuated in the ignored ear, plus noise, and it is heard if "
            "it crosses the word's threshold. Turn the ignored ear down to forty percent, and your name gets through "
            "about a quarter of the time, near Moray's third, while an ordinary word almost never does. A true filter "
            "gives zero for both, which is what Moray's result rules out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15), FadeIn(ptag), Create(cw), Create(cn), FadeIn(lg),
                      run_time=2.0)
            self.play(Create(mark), FadeIn(ml), FadeIn(res))
        self.clear_scene()

    def late(self):
        head = heading(r"Or no early filter at all")
        early = VGroup(label(r"early selection", font_size=28, color=CUE),
                       label(r"senses $\to$ filter $\to$ meaning $\to$ response", font_size=24, color=GREY_A))
        late = VGroup(label(r"late selection", font_size=28, color=ATT),
                      label(r"senses $\to$ meaning, \ for everything $\to$ selection $\to$ response", font_size=24,
                            color=GREY_A))
        for g in (early, late):
            g.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        VGroup(early, late).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([0, 1.45, 0])
        rows = rows_of([
            (r"1963: \ Deutsch and Deutsch: \ every input is recognized; \ selection picks what to act on and remember",
             WHITE),
            (r"evidence each way: \ unattended words can prime meanings, \ yet people cannot report them", GREY_A),
            (r"two decades of argument, \ because the same task gave early results in some hands and late in others",
             CONFLICT),
        ], 12.4, 26, 0.34).move_to([0, -1.35, 0])
        tag = historical_tag(archive.TREISMAN_1960.cite)
        with self.voiceover(
            "Others went further. <bookmark mark='a'/> In 1963 J. Anthony Deutsch and Diana Deutsch proposed that "
            "there is no early filter at all. Everything is recognized, all the way to meaning, and selection comes "
            "late, deciding what to respond to and what to remember. Your name gets through because everything "
            "gets through; you just don't keep most of it. <bookmark mark='b'/> Experiments found support for both. "
            "Ignored words could prime related meanings, which suggests they were understood, yet people could not "
            "report them. <bookmark mark='c'/> The argument went on for two decades, because the same kind of task "
            "seemed to give early selection in some laboratories and late selection in others. The way out was to "
            "ask not where the filter is, but when it can afford to be late."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(early))
            vo.wait_until("a")
            self.play(FadeIn(late), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def load_theory(self):
        d = load("load")
        head = heading(r"Lavie's resolution: \ load")
        rows = rows_of([
            (r"a flanker: \ an irrelevant letter beside the target; \ does it slow you down?", WHITE),
            (r"easy search, \ low load: \ yes, \ the flanker is processed and interferes", CONFLICT),
            (r"hard search, \ high load: \ no, \ capacity is full and nothing spills over", CUE),
            (r"selection is late when there is spare capacity, \ early when there is none", ATT),
            (r"critics: \ load is hard to define without the result it explains", GREY_A),
        ], 6.4, 25, 0.42).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        A = axes([0.5, 6.5], [0, 70], x_length=4.8, y_length=3.0, xticks=[1, 2, 3, 4, 5, 6], yticks=[0, 30, 60],
                 xlabel=r"relevant items to process: \ the load", ylabel=r"flanker interference, \ ms",
                 center=[3.6, 0.35, 0], font_size=17)
        ax = A.ax
        bars = VGroup()
        for x, v in zip(d["load"], d["interference"]):
            lo, hi = ax.c2p(x, 0), ax.c2p(x, max(v, 0.3))
            bars.add(Rectangle(width=0.5, height=hi[1] - lo[1], stroke_width=0, fill_color=CONFLICT, fill_opacity=0.85)
                     .move_to([lo[0], (lo[1] + hi[1]) / 2, 0]))
        cap = DashedLine(ax.c2p(4, 0), ax.c2p(4, 70), color=CONTROL, stroke_width=2)
        cl = label(r"capacity", font_size=17, color=CONTROL).next_to(ax.c2p(4, 70), UP, buff=0.05)
        ptag = psyche_tag(r"\texttt{attention.flanker\_interference}: \ capacity 4, \ 60 ms when all is spare")
        tag = historical_tag(archive.LAVIE_1995.cite)
        with self.voiceover(
            "In 1995 Nilli Lavie offered a resolution. <bookmark mark='a'/> She used flankers: you look for a target "
            "letter, and an irrelevant letter appears off to the side. If the flanker is the letter of the other "
            "response, does it slow you down? <bookmark mark='b'/> When the search is easy, it does: the flanker gets "
            "processed and interferes. <bookmark mark='c'/> When the search is hard, with many similar items to sort "
            "through, the flanker stops mattering. <bookmark mark='d'/> Her account is that perception has a limited "
            "capacity which it always uses up. With little to process, the spare capacity spills over onto whatever "
            "else is there, and selection looks late. With a heavy load, nothing is left over, and selection looks "
            "early. In Psyche's version, interference is just the share of capacity left over. "
            "<bookmark mark='e'/> The critics' point is fair: if load is measured by whether distractors interfere, "
            "the theory explains itself. Good tests define load independently, by set size or by similarity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "d":
                    self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), Create(cap),
                              FadeIn(cl), FadeIn(ptag), run_time=2.0)
        self.clear_scene()
