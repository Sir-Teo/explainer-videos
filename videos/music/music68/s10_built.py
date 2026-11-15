from __future__ import annotations

from videos.music.music68.common import *  # noqa: F403


class Built(SoundScene):
    def construct(self):
        chapter(self, 9, r"What was built", r"What is Monochord now, and how do we know it works?")
        self.counts()
        self.layers()
        self.checks()
        self.skills()

    # ------------------------------------------------------------------
    def counts(self):
        b = load("built")
        cells = [(f"{b['modules']}", r"modules of Monochord"), (f"{b['lines']:,}".replace(",", "{,}"), r"lines of code"),
                 (f"{b['tests']}", rf"tests, \ in {b['test_files']} files"), (f"{b['clips']}", r"sounds computed by Parts 1 to 67"),
                 (f"{b['hours']:.1f}", r"hours of those sounds"), (f"{b['labs']}", r"labs, \ one per part")]
        grid = VGroup()
        for big, small in cells:
            grid.add(VGroup(label(big, font_size=44, color=TUNE), label(small, font_size=17, color=GREY_A)).arrange(DOWN, buff=0.15))
        grid.arrange_in_grid(rows=2, cols=3, buff=(1.2, 0.8)).move_to(DOWN * 0.1)
        head = label(r"Monochord, \ counted", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Monochord began in Part 1 as one simulated string. Here it is, counted from the repository. "
            f"<bookmark mark='a'/> {say(b['modules'])} modules, <bookmark mark='b'/> about {say(round(b['lines'], -2))} lines "
            f"of code, <bookmark mark='c'/> and {say(b['tests'])} tests that hold it to account. <bookmark mark='d'/> Parts 1 "
            f"to 67 computed {say(b['clips'])} sounds with it, <bookmark mark='e'/> about {say(b['hours'], 1)} hours of them, "
            f"every one made by the code and none recorded. <bookmark mark='f'/> And there is a lab for every part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.copy().set_opacity(0.15)))   # a ghost of what is coming
            for m, c in zip("abcdef", grid):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15), run_time=0.5)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def layers(self):
        b = load("built")["layers"]
        order = ["the core", "the physics", "the theory", "the styles", "the craft and the mind", "the electronics", "the studio",
                 "the listeners and makers"]
        what = {"the core": r"sounds, \ clips, \ the Tune, \ the corpora", "the physics": r"strings, \ air, \ the ear, \ instruments, \ tunings",
                "the theory": r"pitch to grammar: \ scales, \ chords, \ keys, \ voices, \ forms", "the styles": r"eras and the world's musics",
                "the craft and the mind": r"orchestras, \ composers, \ performers, \ listeners",
                "the electronics": r"sampling, \ filters, \ effects, \ synthesizers, \ the DAW",
                "the studio": r"microphones, \ rooms, \ mixing, \ mastering, \ codecs, \ the business",
                "the listeners and makers": r"transcription to generation, \ research tools"}
        top = max(b[k]["lines"] for k in order)
        rows_ = VGroup()
        for k in order:
            bar = Rectangle(width=max(0.05, 5.0 * b[k]["lines"] / top), height=0.32, stroke_width=0, fill_color=TUNE, fill_opacity=0.8)
            rows_.add(VGroup(label(k, font_size=18, color=WHITE), bar, label(rf"{b[k]['modules']} modules, \ {b[k]['lines']:,} lines".replace(",", "{,}"), font_size=14, color=GREY_B),
                             label(what[k], font_size=14, color=GREY_A)))
        for r in rows_:
            r[0].move_to([-6.6, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-3.1, 0, 0], aligned_edge=LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.15)
            r[3].next_to(r[0], DOWN, buff=0.06, aligned_edge=LEFT)
        rows_.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(DOWN * 0.25)
        head = label(r"its layers, \ in lines of code", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Its layers, each the size of the code it takes. <bookmark mark='a'/> The core holds the sounds, the clips, the "
            "Tune and the corpora. The physics: strings, air, the ear, the instruments and their tunings. The theory, from "
            "pitch to grammar. The styles: eras, and the world's other musics. <bookmark mark='b'/> The craft and the mind. "
            "The electronics, from sampling to the workstation. The studio. And last the machines that listen and make. The "
            "theory and the styles are as large as the physics: much of music's knowledge is about structure, not sound."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r) for r in rows_[:4]], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_[4:]], lag_ratio=0.25), run_time=2.0)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def checks(self):
        items = [
            (r"against closed forms: \ d'Alembert's solution for the string, \ Bessel's functions, \ Sabine's formula, \ the binomial", WHITE),
            (r"against other people's code: \ \texttt{scipy.signal}, \ and \texttt{ffmpeg}'s loudness meter beside our BS.1770 meter", WHITE),
            (r"against published numbers: \ Krumhansl and Kessler's key profiles, \ measured tunings and rooms", WHITE),
            (r"against scores whose analysis is known: \ Bach's chorales, \ for the harmonizer and the generators", WHITE),
            (r"and where there was nothing independent, \ each part says so in its notes", TUNE),
        ]
        rows_scene(self, r"how we know it works", items,
                   "How do we know it works? Each layer was checked against something that does not share its code. "
                   "<bookmark mark='b'/> Against closed forms: d'Alembert's solution for the string, Bessel's functions, Sabine's "
                   "formula, the binomial distribution. <bookmark mark='c'/> Against other people's code: SciPy's signal "
                   "processing, and ffmpeg's loudness meter beside the series' own. <bookmark mark='d'/> Against published "
                   "numbers, like Krumhansl and Kessler's key profiles. <bookmark mark='e'/> Against scores whose analysis is "
                   "known, Bach's chorales above all. <bookmark mark='f'/> And where there was nothing independent to check "
                   "against, each part says so in its notes.", marks="bcdef")

    # ------------------------------------------------------------------
    def skills(self):
        items = [
            (r"simulate a string, \ a pipe, \ a membrane, \ a room; \ and say what an ear will make of them", WHITE),
            (r"tune a scale, \ spell a chord, \ find a key, \ check a counterpoint, \ parse a phrase", WHITE),
            (r"read a style, \ or a tradition, \ by its own rules: \ a talea, \ a tihai, \ a maqam's moves", WHITE),
            (r"filter, \ synthesize, \ mix, \ master and code a sound, \ and measure what each step did", WHITE),
            (r"build a machine that listens or writes, \ split its data honestly, \ and audit its verdicts", TUNE),
        ]
        rows_scene(self, r"what you can now do", items,
                   "And what can you now do, with it or without it? <bookmark mark='b'/> Simulate a string, a pipe, a membrane, "
                   "a room, and say what an ear will make of them. <bookmark mark='c'/> Tune a scale, spell a chord, find a key, "
                   "check a counterpoint, parse a phrase. <bookmark mark='d'/> Read a style or a tradition by its own rules: a "
                   "talea, a tihai, the moves of a maqam. <bookmark mark='e'/> Filter, synthesize, mix, master and code a sound, "
                   "and measure what each step did. <bookmark mark='f'/> And build a machine that listens or writes, split its "
                   "data honestly, and audit its verdicts.", marks="bcdef")
