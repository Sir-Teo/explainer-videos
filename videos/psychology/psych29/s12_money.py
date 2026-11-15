from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class Money(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_findings()
        self.world()
        self.resolution()

    def card(self):
        card = chapter_card(11, r"Happiness and income", r"Does money buy happiness, \ and up to what point?",
                            lit={2010: r"Kahneman \& Deaton", 2021: r"Killingsworth",
                                 2023: r"adversarial collaboration"},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter eleven. Happiness and income."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def two_findings(self):
        head = heading(r"Two findings that disagreed")
        left = VGroup(label(r"2010: \ a plateau", font_size=26, color=UNPL), rows_of([
            (r"Daniel Kahneman and Angus Deaton: \ about 450{,}000 answers to a daily Gallup survey", WHITE),
            (r"life evaluation rose with log income all the way up", WHITE),
            (r"yesterday's emotional well-being stopped rising at about \$75{,}000 a year", UNPL),
        ], 5.4, 21, 0.25)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right = VGroup(label(r"2021: \ no plateau", font_size=26, color=PLEAS), rows_of([
            (r"Matthew Killingsworth: \ 1{,}725{,}994 moments sampled by smartphone from 33{,}391 employed US "
             r"adults", WHITE),
            (r"``how do you feel right now?'', \ at random times of day", WHITE),
            (r"happiness rose with log income, \ with no plateau above \$75{,}000", PLEAS),
        ], 5.4, 21, 0.25)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.2, 0])
        foot = wrapped_label(r"different measures and samples; \ both careful; \ both widely reported", 12.0, 23,
                             COG).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Kahneman \& Deaton (2010); \ Killingsworth (2021)")
        with self.voiceover(
            "Does money buy happiness? Two careful studies gave different answers. <bookmark mark='a'/> In 2010 "
            "Daniel Kahneman and Angus Deaton analysed about four hundred and fifty thousand answers to a daily "
            "Gallup survey. People's evaluation of their lives rose with the logarithm of income all the way up. But "
            "yesterday's emotional well-being, whether they had felt enjoyment, stress or sadness, stopped rising at "
            "about seventy-five thousand dollars a year. <bookmark mark='b'/> In 2021 Matthew Killingsworth used a "
            "smartphone app that asked people how they felt right now, at random moments: 1,725,994 reports from "
            "33,391 employed adults in the United States. Happiness rose with log income, with no plateau above "
            "seventy-five thousand. <bookmark mark='c'/> Different measures, different samples, both careful, both "
            "widely reported."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def world(self):
        d = load("income")
        head = heading(r"One world, \ both findings")
        x = np.log2(np.asarray(d["income"]) / 1000.0)
        ticks = [np.log2(v) for v in (25, 50, 100, 200, 400)]
        A = axes([np.log2(15), np.log2(500)], [-2.6, 0.7], x_length=5.8, y_length=3.8, xticks=ticks,
                 yticks=[-2, -1, 0], xfmt=lambda v: rf"{2 ** v:.0f}\text{{k}}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"household income, \ log scale", ylabel=r"momentary happiness", center=[-3.3, -0.2, 0],
                 font_size=16)
        cm = curve(A.ax, x, d["mean"], PLEAS, 4)
        c10 = curve(A.ax, x, d["p10"], UNPL, 4)
        ref = DashedLine(A.ax.c2p(np.log2(100), -2.6), A.ax.c2p(np.log2(100), 0.7), color=GREY_B, stroke_width=2)
        key = legend([(PLEAS, r"everyone's average"), (UNPL, r"the least happy tenth")], font_size=17)
        key.move_to(A.ax.c2p(np.log2(40), 0.45))
        rows = rows_of([
            (r"Psyche's simulated population: \ for most people, \ happiness rises steadily with log income", MODEL),
            (r"for a fifth of people, \ unhappiness has sources money does not touch: \ illness, \ grief, \ "
             r"loneliness; \ money helps them only up to about \$100{,}000", UNPL),
            (r"the average keeps rising; \ the least happy tenth flattens", WHITE),
            (r"a measure driven by the unhappiest people \ (felt sad or stressed yesterday?) \ shows a plateau; \ "
             r"a measure of everyone's average does not", COG),
        ], 5.6, 21, 0.3).move_to([3.4, -0.1, 0])
        tag = simulated_tag(r"simulated: \ \texttt{emotion.income\_world}, \ 200{,}000 people")
        with self.voiceover(
            "How can both be right? Psyche can build a world where they are. <bookmark mark='a'/> In this simulated "
            "population, happiness rises steadily with the logarithm of income for most people. "
            "<bookmark mark='b'/> But for a fifth of people, unhappiness has sources that money does not touch, "
            "such as illness, grief or loneliness, and money helps them only up to about a hundred thousand dollars. "
            "<bookmark mark='c'/> The average keeps rising. The least happy tenth flattens. "
            "<bookmark mark='d'/> A measure driven by the unhappiest people, such as whether you felt sad or "
            "stressed yesterday, will show a plateau. A measure of everyone's average will not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(ref))
            vo.wait_until("a")
            self.play(Create(cm), FadeIn(key[0]), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c10), FadeIn(key[1]), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def resolution(self):
        head = heading(r"An adversarial collaboration, \ 2023")
        rows = rows_of([
            (r"Killingsworth and Kahneman, \ with Barbara Mellers as arbiter, \ reanalysed Killingsworth's data "
             r"together, \ agreeing in advance what would count", WHITE),
            (r"for the least happy fifth, \ happiness rose with income up to about \$100{,}000, \ then stopped", UNPL),
            (r"for everyone else it kept rising, \ and for the happiest it rose faster above \$100{,}000", PLEAS),
            (r"the 2010 plateau was real for the unhappiest; \ the measure it used was sensitive mainly to them", COG),
            (r"what it shows about method: \ two rival findings settled by working together, \ as in Part 27's "
             r"test of theories of consciousness", WHITE),
        ], 12.2, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Killingsworth, \ Kahneman \& Mellers (2023)")
        with self.voiceover(
            "That is close to what the authors themselves found. <bookmark mark='a'/> In 2023 Killingsworth and "
            "Kahneman, with Barbara Mellers as an arbiter, reanalysed Killingsworth's data together, having agreed "
            "in advance what would count. <bookmark mark='b'/> For the least happy fifth of people, happiness rose "
            "with income up to about a hundred thousand dollars, and then stopped. <bookmark mark='c'/> For "
            "everyone else it kept rising, and for the happiest it rose faster above a hundred thousand. "
            "<bookmark mark='d'/> The 2010 plateau was real for the unhappiest people, and the measure it used was "
            "sensitive mainly to them. <bookmark mark='e'/> It's a lesson in method as well: two rival findings, "
            "settled by their authors working together, like the test of theories of consciousness in Part 27."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
