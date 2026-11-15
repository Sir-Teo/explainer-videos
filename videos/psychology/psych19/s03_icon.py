from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403

GRID = ("RGBX", "KMTF", "LQZD")


def letter_grid(rows=GRID, font_size=58, color=WHITE, dx=0.95, dy=0.95) -> VGroup:
    g = VGroup()
    for i, r in enumerate(rows):
        for j, ch in enumerate(r):
            g.add(label(ch, font_size=font_size, color=color).move_to([(j - 1.5) * dx, (1 - i) * dy, 0]))
    return g


class Icon(VoiceoverScene):
    def construct(self):
        self.card()
        self.flash()
        self.partial()
        self.curve()

    def card(self):
        card = chapter_card(2, r"More than you can report", r"How much does one glance hold, \ and for how long?",
                            lit={1960: r"Sperling"}, part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter two. More than you can report."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def flash(self):
        p = archive.SPERLING_1960.data
        stage = demo_stage(8.4, 4.4, center=[0, 0.7, 0])
        grid = letter_grid().move_to(stage.box.get_center() + DOWN * 0.1)
        ask = label(r"which letters did you see?", font_size=30, color=YOU).move_to(grid)
        rows = rows_of([
            (r"1960: \ George Sperling flashes twelve letters for 50 ms", WHITE),
            (rf"whole report: \ write down all you can; \ about {p['whole_report']} letters, \ however long the flash",
             MEM),
            (r"yet people insisted they had seen more than they could name", GREY_A),
        ], 12.4, 26, 0.26).to_edge(DOWN, buff=0.8)
        tag = historical_tag(archive.SPERLING_1960.cite)
        with self.voiceover(
            "Here is a glance. <bookmark mark='a'/> Twelve letters, for a twentieth of a second. Ready. "
            "<bookmark mark='b'/>"
        ) as vo:
            self.play(FadeIn(stage), FadeIn(tag))
            vo.wait_until("b")
        self.add(grid)
        self.wait(0.12)
        self.remove(grid)
        self.wait(0.6)
        with self.voiceover(
            "How many could you name? <bookmark mark='a'/> In 1960 George Sperling, a graduate student at Harvard, "
            "ran this many thousands of times. <bookmark mark='b'/> Asked to write down every letter, people managed "
            f"about {p['whole_report']}, almost regardless of how many letters there were or how long the flash was. "
            "<bookmark mark='c'/> And yet they insisted they had seen more: that the letters had been there, clearly, "
            "and had faded while they were writing the first few down. Was that an illusion, or a store bigger than "
            "report could show?"
        ) as vo:
            self.play(FadeIn(ask))
            vo.wait_until("a")
            self.play(FadeOut(ask), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def partial(self):
        p = archive.SPERLING_1960.data
        head = heading(r"Partial report: \ a tone says which row")
        grid = letter_grid(font_size=48, dx=0.8, dy=0.78).move_to([-3.4, 1.0, 0])
        tones = VGroup(*[label(t, font_size=22, color=c).next_to(grid[4 * i + 3], RIGHT, buff=0.5)
                         for i, (t, c) in enumerate(((r"high tone", LOOP), (r"middle tone", MEM), (r"low tone", EXEC)))])
        box = SurroundingRectangle(VGroup(*grid[4:8]), color=MEM, buff=0.12)
        rows = rows_of([
            (r"right after the flash, \ a tone picks one row at random; \ report only that row", WHITE),
            (r"people got about three of its four letters, \ whichever row was cued", MEM),
            (r"so about three quarters of every row was available: \ about 9 of the 12 letters", MODEL),
            (rf"twice whole report's {p['whole_report']}: \ the limit was in the reporting, \ not the seeing", GREY_A),
        ], 6.4, 24, 0.34).move_to([3.3, 0.6, 0])
        tag = historical_tag(archive.SPERLING_1960.cite)
        with self.voiceover(
            "Sperling's answer was to sample. <bookmark mark='a'/> After the flash, a tone sounded: high for the top "
            "row, middle for the middle, low for the bottom, chosen at random, and people reported only that row. "
            "<bookmark mark='b'/> They got about three of its four letters. <bookmark mark='c'/> Since they couldn't "
            "know in advance which row would be asked for, about three quarters of every row must have been "
            "available when the tone sounded: about nine of the twelve letters. It is the logic of an exam that "
            f"tests a random chapter. <bookmark mark='d'/> That is twice the {p['whole_report']} letters of whole "
            "report. The limit on whole report was not in what was seen, but in getting it out before it faded."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(grid), FadeIn(tones))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(box), Indicate(tones[1], color=MEM))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def curve(self):
        d = load("sperling")
        p = archive.SPERLING_1960.data
        head = heading(r"Delay the tone, \ and the advantage melts")
        A = axes([0, 1000], [0, 12], x_length=7.4, y_length=3.6, xticks=[0, 250, 500, 750, 1000], yticks=[0, 4, 8, 12],
                 xlabel=r"delay of the tone after the flash, \ ms", ylabel=r"letters available \ (of 12)",
                 center=[-1.6, 0.55, 0], font_size=18)
        ax = A.ax
        c = curve_in(ax, d["delay"], d["available"], MODEL, 4)
        whole = DashedLine(ax.c2p(0, p["whole_report"]), ax.c2p(1000, p["whole_report"]), color=MEM, stroke_width=2)
        wl = label(r"whole report", font_size=19, color=MEM).next_to(ax.c2p(120, p["whole_report"]), DOWN, buff=0.1)
        wl.align_to(ax.c2p(20, 0), LEFT)
        dot = Dot(ax.c2p(0, p["partial_available_immediate"]), radius=0.08, color=DATA)
        dl = label(r"Sperling: \ about 9", font_size=19, color=DATA).next_to(dot, RIGHT, buff=0.15)
        notes = rows_of([
            (r"a large, \ brief visual store: \ Neisser named it iconic memory", WHITE),
            (r"a bright field after the flash wipes it; \ a dark one prolongs it", GREY_A),
            (r"the icon is not working memory: \ it holds more, \ for less than a second, \ before attention picks",
             MEM),
        ], 4.2, 22, 0.3).move_to([4.6, 0.6, 0])
        rows = rows_of([
            (r"$\text{available} = 12\,\big[\,i\,e^{-t/\tau} + (1 - i\,e^{-t/\tau})\,\tfrac{4.5}{12}\big]$: \ "
             r"read from the icon, \ or already moved to the store", MODEL),
        ], 12.4, 24, 0.2).to_edge(DOWN, buff=0.8)
        ptag = psyche_tag(r"\texttt{wm.partial\_report}: \ $i = 0.62$, \ $\tau = 250$ ms")
        tag = historical_tag(archive.SPERLING_1960.cite)
        with self.voiceover(
            "Then Sperling delayed the tone. <bookmark mark='a'/> Within a few hundred milliseconds the advantage "
            "melts away, and by about a second partial report is no better than whole report. "
            "<bookmark mark='b'/> The curve drawn here is Psyche's: a cued letter is read from a fading image with a "
            "probability that decays exponentially, with a time constant of a quarter of a second, or else it is "
            "reported only if it was among the four and a half letters already moved into a lasting store. "
            "<bookmark mark='c'/> Ulric Neisser named the fading image iconic memory. A bright field after the "
            "flash wipes it out; a dark one prolongs it. <bookmark mark='d'/> It is large and very brief, and it is "
            "not working memory. It is the raw material that attention selects from, the subject of the last part. "
            "What survives the selection is the subject of this one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(whole), FadeIn(wl), FadeIn(dot), FadeIn(dl))
            vo.wait_until("a")
            self.play(Create(c), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(ptag))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.clear_scene()
