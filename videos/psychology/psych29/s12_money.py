from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class Money(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_findings()
        self.world()
        self.resolution()
        self.easterlin()

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

    def easterlin(self):
        head = heading(r"Richer people, \ richer countries, \ richer years")
        rng = np.random.default_rng(1974)
        titles = [(r"within a country, \ one year", COG), (r"across countries", PLEAS),
                  (r"one country, \ over time", UNPL)]
        panels = VGroup()
        for i, (t, c) in enumerate(titles):
            A = axes([0, 1], [0, 1], x_length=3.3, y_length=2.1, xticks=None, yticks=None,
                     xlabel=(r"log income" if i < 2 else r"year"), ylabel=r"happiness", font_size=17,
                     center=[-4.45 + 4.45 * i, 1.0, 0])
            ttl = label(t, font_size=21, color=c).next_to(A, UP, buff=0.12)
            panels.add(VGroup(A, ttl))
        xs = rng.uniform(0.05, 0.95, 70)
        people = scatter(panels[0][0].ax, xs, np.clip(0.25 + 0.45 * xs + rng.normal(0, 0.14, 70), 0.03, 0.97),
                         COG, radius=0.035)
        xc = rng.uniform(0.08, 0.92, 26)
        nations = scatter(panels[1][0].ax, xc, np.clip(0.15 + 0.7 * xc + rng.normal(0, 0.07, 26), 0.03, 0.97),
                          PLEAS, radius=0.055)
        ax3 = panels[2][0].ax
        yrs = np.linspace(0.05, 0.95, 25)
        inc = curve(ax3, yrs, 0.18 + 0.7 * yrs, GREY_B, 3)
        hap = curve(ax3, yrs, 0.5 + 0.03 * np.sin(9 * yrs), UNPL, 4)
        inc_l = label(r"income", font_size=17, color=GREY_B).next_to(ax3.c2p(0.95, 0.88), LEFT, buff=0.1)
        hap_l = label(r"happiness", font_size=17, color=UNPL).next_to(ax3.c2p(0.95, 0.5), DOWN, buff=0.12)
        hap_l.align_to(inc_l, RIGHT)
        why = point_cards([
            (r"comparison", r"income is judged against other people's; \ when everyone grows richer, \ nobody "
             r"moves up", COG),
            (r"adaptation", r"like chapter ten's lottery winners, \ last year's raise becomes this year's normal",
             BODY),
        ], width=12.4, font_size=20)
        why.move_to([0, -2.05, 0])
        checks = verdict_row([
            (r"within and across countries, \ happiness rises with log income \ (Deaton; \ Stevenson and "
             r"Wolfers, \ 2008)", "replicated"),
            (r"over ten years or more, \ faster growth does not bring faster-rising happiness \ (Easterlin et "
             r"al., \ 2010)", "contested"),
        ], width=12.4, font_size=20)
        checks.move_to([0, -2.05, 0])
        stamp = label(r"schematic: \ the shapes the studies reported", font_size=17, color=GREY_B)
        stamp.move_to([0, -0.62, 0])
        tag = published_tag(r"Easterlin (1974); \ Deaton (2008); \ Stevenson \& Wolfers (2008); \ "
                            r"Easterlin et al.\ (2010)")
        with self.voiceover(
            "The question is older than these studies, and it began with nations. <bookmark mark='a'/> In 1974 the "
            "economist Richard Easterlin gathered surveys that asked people how happy they were. Within a country, "
            "in any one year, richer people said they were happier. <bookmark mark='b'/> But in the United States, "
            "from 1946 to 1970, income per head rose a long way, and reported happiness did not rise with it. If "
            "money buys happiness for each person, why not for a nation? It became known as the Easterlin paradox. "
            "<bookmark mark='c'/> His answer had two parts. People judge their income against other people's, so "
            "when everyone grows richer together, nobody moves up. And people adapt, like the lottery winners of "
            "chapter ten: last year's raise becomes this year's normal. <bookmark mark='d'/> In 2008 came replies "
            "from larger data. Angus Deaton, with the Gallup World Poll, and Betsey Stevenson and Justin Wolfers, "
            "with many surveys, found that across countries life satisfaction rises steadily with the logarithm of "
            "income, with no point where it stops, and they argued that the short, noisy series over time were "
            "consistent with the same slope. <bookmark mark='e'/> Easterlin and his colleagues replied in 2010 "
            "that over ten years or more, countries whose incomes grew faster did not become happier faster, even "
            "where income doubled within twenty years. <bookmark mark='f'/> So the slope across people and across "
            "countries is settled. Whether growth makes a nation happier is still argued, and the answer turns on "
            "which surveys, which countries, and how long a run."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(stamp))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]), LaggedStart(*[FadeIn(p) for p in people], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(panels[2]), Create(inc), FadeIn(inc_l), run_time=1.6)
            self.play(Create(hap), FadeIn(hap_l), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(why.cards[0], shift=UP * 0.15))
            self.play(FadeIn(why.cards[1], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeOut(why), FadeIn(panels[1]), LaggedStart(*[FadeIn(p) for p in nations], lag_ratio=0.05),
                      FadeIn(checks.rows[0], shift=RIGHT * 0.15), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(checks.rows[1], shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(Indicate(checks.rows[1].chip, color=STATUS_COLOR["contested"], scale_factor=1.1),
                      Indicate(panels[2][1], color=UNPL, scale_factor=1.06))
        self.clear_scene()
