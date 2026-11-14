from __future__ import annotations

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class Score(VoiceoverScene):
    def construct(self):
        self.card()
        self.build()
        self.person()
        self.family()
        self.switches()

    def card(self):
        card = chapter_card(10, r"What a polygenic score can say", r"Thousands of tiny effects: what do they add up to?",
                            lit={2018: r"1.1 million people"}, part=PART, scale=("molecule", "person", "group"),
                            marr=("what",))
        with self.voiceover(
            "Chapter ten. What a polygenic score can say."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def build(self):
        d = load("score")
        lee = archive.LEE_2018.data
        head = heading(r"Add up the tiny effects: \ a polygenic score")
        A = axes([-3.2, 3.2], [-3.2, 3.2], x_length=4.2, y_length=3.8, xticks=[], yticks=[], xlabel=r"the score",
                 ylabel=r"the trait", center=[-4.3, -0.55, 0])
        s = (d["s"] - d["s"].mean()) / d["s"].std()
        pts = scatter(A.ax, s, d["y"], GENE, radius=0.025, opacity=0.5)
        rl = label(rf"predicts {pct(d['r2'])} in new people", font_size=28, color=GENE).next_to(A, UP, buff=0.12)
        B = axes([2.5, 6.5], [0, 0.55], x_length=4.3, y_length=2.6, xticks=[3, 4, 5, 6], yticks=[0, 0.25, 0.5],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: pct(v), xlabel=r"people in the discovery study",
                 ylabel=r"variation the score predicts", center=[0.7, -1.05, 0])
        cv = curve(B.ax, np.log10(d["ns"]), d["curve"], GENE, stroke_width=4)
        cap = DashedLine(B.ax.c2p(2.5, d["h2"]), B.ax.c2p(6.5, d["h2"]), color=WHITE, stroke_width=2)
        cl = label(r"the heritability", font_size=26, color=WHITE).next_to(B.ax.c2p(2.5, d["h2"]), UR, buff=0.06)
        here = Dot(B.ax.c2p(np.log10(d["train"]), d["expected"]), radius=0.09, color=WHITE)
        rows = rows_of([
            (r"for each person: \ copies at each position, \ times the estimated effect, \ summed", WHITE),
            (r"tested only in people who were not in the discovery study", P.ACCENT),
            (rf"years of schooling, real scores: \ {pct(lee['okbay_r2'][0])} to {pct(lee['okbay_r2'][1])} of the "
             r"variation", DATA),
        ], 3.9, 29, 0.3).move_to([5.05, 0.0, 0])
        keep_in_frame(rows)
        src = published_tag(archive.LEE_2018.cite)
        tag = psyche_tag(r"simulated: the miniature genome")
        with self.voiceover(
            "Thousands of tiny effects are useless one at a time. So add them up. <bookmark mark='a'/> For "
            "each person, go through the positions. Multiply the number of copies by the effect the big "
            "study estimated, and sum. The total is called a polygenic score. <bookmark mark='b'/> Then "
            "test it honestly: in people who weren't in the study. On our miniature genome, a score "
            f"built from {int(d['train']):,} people predicts {100 * d['r2']:.0f} percent of the variation in "
            f"{int(d['test']):,} new people. The trait's heritability is fifty percent. The score gets only "
            "part of the way, because each effect is estimated with error. <bookmark mark='c'/> The "
            "bigger the discovery study, the closer the score gets to that ceiling. <bookmark mark='d'/> "
            "For years of schooling, the real scores now predict "
            f"{100 * lee['okbay_r2'][0]:.0f} to {100 * lee['okbay_r2'][1]:.0f} percent of the variation. "
            "For one predictor of a behavioural trait, that's a large number. Now let's see what it "
            "buys."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts, lag_ratio=0.001), FadeIn(rl), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(B), Create(cap), FadeIn(cl), Create(cv), FadeIn(here), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def person(self):
        d = load("score")
        head = heading(rf"What {pct(d['real_r2'])} means, \ for groups and for one person")
        A = axes([0, 11], [-0.8, 0.8], x_length=4.6, y_length=3.6, xticks=[1, 10], yticks=[-0.5, 0, 0.5],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"tenth of the score, lowest to highest",
                 ylabel=r"average of the trait", center=[-4.25, -0.5, 0])
        bars = VGroup()
        unit = abs(A.ax.c2p(0, 1)[1] - A.ax.c2p(0, 0)[1])
        for k, v in enumerate(d["real_deciles"]):
            r = Rectangle(width=0.3, height=max(abs(float(v)) * unit, 0.01), stroke_width=0, fill_color=GENE, fill_opacity=0.9)
            r.move_to(A.ax.c2p(k + 1, float(v) / 2))
            bars.add(r)
        B = axes([-3.2, 3.2], [-3.2, 3.2], x_length=3.8, y_length=3.6, xticks=[], yticks=[], xlabel=r"one person's score",
                 ylabel=r"that person's trait", center=[0.75, -0.5, 0])
        cols = np.where(d["is_top"], 2, np.where(d["is_bottom"], 0, 1))
        cloud = VGroup(*[Dot(B.ax.c2p(float(a), float(b)), radius=0.025, color=(DZC, OWN, THRESH)[int(c)],
                             fill_opacity=0.45 if c == 1 else 0.9)
                         for a, b, c in zip(d["sc"], d["tr"], cols) if abs(a) < 3.1 and abs(b) < 3.1])
        mid = DashedLine(B.ax.c2p(-3.2, 0), B.ax.c2p(3.2, 0), color=WHITE, stroke_width=2)
        rows = rows_of([
            (r"groups: \ the averages climb steadily", GENE),
            (rf"top tenth of the score: \ {pct(d['top_above'])} are above the middle", THRESH),
            (rf"bottom tenth: \ {pct(d['bottom_above'])} are above the middle", DZC),
            (rf"the range left open for one person: \ $\pm {d['interval']:.1f}$ standard deviations, \ against "
             r"$\pm 1.96$ knowing nothing", WHITE),
        ], 3.7, 29, 0.28).move_to([5.15, -0.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(rf"simulated: a score that predicts {pct(d['real_r2'])} of a trait")
        with self.voiceover(
            f"What do twelve to sixteen percent mean? Take the middle, {100 * d['real_r2']:.0f}. "
            "<bookmark mark='a'/> Sort people by their score into ten groups. The averages of the groups "
            "climb steadily from the lowest to the highest. For comparing groups, the score works. "
            "<bookmark mark='b'/> Now one person. Someone in the top tenth of the score has a "
            f"{100 * d['top_above']:.0f} percent chance of being above the middle on the trait. "
            f"<bookmark mark='c'/> Someone in the bottom tenth has a {100 * d['bottom_above']:.0f} "
            "percent chance. So of the people the score ranks highest, one in four is below average, and "
            "of those it ranks lowest, one in four is above. <bookmark mark='d'/> And the range it leaves "
            f"open for a person is almost as wide as before: plus or minus {d['interval']:.1f} standard "
            "deviations, where knowing nothing at all gives one point nine six. A score like this is a "
            "tool for research on groups. As a statement about one person, it's a weak hint."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if v < 0 else UP) for b, v in zip(bars, d["real_deciles"])],
                                  lag_ratio=0.1), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(B), Create(mid), FadeIn(cloud, lag_ratio=0.001), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def family(self):
        d = load("score")
        k, y = archive.KONG_2018.data, archive.YENGO_2022.data
        head = heading(r"What is the score a score of?")
        A = axes([-2.2, 2.2], [-1.2, 1.2], x_length=4.6, y_length=3.7, xticks=[-2, 0, 2], yticks=[-1, 0, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"difference in score",
                 ylabel=r"difference in the trait", center=[-4.2, -0.4, 0])
        ax = A.ax
        pop = Line(ax.c2p(-2.2, -2.2 * d["population"]), ax.c2p(2.2, 2.2 * d["population"]), color=HOME, stroke_width=5)
        wit = Line(ax.c2p(-2.2, -2.2 * d["within"]), ax.c2p(2.2, 2.2 * d["within"]), color=GENE, stroke_width=5)
        pl = label(rf"between strangers: \ ${d['population']:.2f}$", font_size=28, color=HOME).next_to(
            ax.c2p(-2.1, 1.0), RIGHT, buff=0.0)
        wl = label(rf"between siblings: \ ${d['within']:.2f}$", font_size=28, color=GENE).next_to(
            ax.c2p(-2.1, 0.68), RIGHT, buff=0.0)
        hb = VGroup()
        for i, (name, v, col) in enumerate(((r"twins", y["twin_h2"], MZC), (r"all common variants", y["variance_all_common"], GENE))):
            bar = Rectangle(width=3.6 * v, height=0.4, stroke_width=0, fill_color=col, fill_opacity=0.9)
            bar.move_to([0.2 + 1.8 * v, -2.2 - 0.55 * i, 0])
            hb.add(VGroup(bar, label(rf"{name}: \ {pct(v)}", font_size=27, color=col).next_to(bar, RIGHT, buff=0.15)))
        hl = label(r"height: \ how much goes with genes", font_size=28, color=GREY_A).next_to(hb, UP, buff=0.15).align_to(hb, LEFT)
        rows = rows_of([
            (rf"between siblings the score's effect is about {pct(d['lee_smaller'])} smaller", GENE),
            (r"across families the score also picks up the parents, \ and the home their genes helped make", HOME),
            (rf"the gene versions parents did \emph{{not}} pass on still predict schooling, \ at {pct(k['share_of_transmitted'])} "
             r"of the strength: \ ``genetic nurture''", DATA),
        ], 6.6, 29, 0.28).move_to([3.4, 1.0, 0])
        keep_in_frame(rows)
        src = published_tag(archive.KONG_2018.cite + r"; \ " + archive.YENGO_2022.cite)
        tag = psyche_tag(r"lines: simulated families")
        with self.voiceover(
            "There's a second caution, about what the score is a score of. <bookmark mark='a'/> Compare "
            "unrelated people, and a difference of one unit in the score goes with "
            f"{d['population']:.2f} units of the trait. <bookmark mark='b'/> Now compare brothers and "
            "sisters, who have the same parents and the same home. Between siblings, the same difference "
            f"in score goes with {d['within']:.2f}: about {100 * d['lee_smaller']:.0f} percent less. "
            "That's what the study of a million people found for schooling. <bookmark mark='c'/> Why? "
            "Because across families the score also picks up the parents. Parents with higher scores "
            "make different homes, and their children get both the genes and the home. In Iceland, the "
            "gene versions that parents did not pass on still predicted their children's schooling, at "
            f"{100 * k['share_of_transmitted']:.0f} percent of the strength of the ones they did. It's "
            "been named genetic nurture. It's Galton's confound, found inside the genome. "
            f"<bookmark mark='d'/> And one more gap. For height, twin studies say "
            f"{100 * y['twin_h2']:.0f} percent. All the common variants together reach about "
            f"{100 * y['variance_all_common']:.0f}. The difference is called the missing heritability. "
            "Part of it is rarer variants that no chip reads. And part of it may be the twin design's "
            "own inflation, from chapter four."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(pop), FadeIn(pl))
            vo.wait_until("b")
            self.play(Create(wit), FadeIn(wl), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            self.wait(6.0)
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(hl), FadeIn(hb, lag_ratio=0.4))
        self.clear_scene()

    def switches(self):
        h = archive.HEIJMANS_2008.data
        head = heading(r"A word you will have heard: \ epigenetics")
        g = np.random.default_rng(12)
        dna = Line([-6.2, 2.0, 0], [6.2, 2.0, 0], color=GENE, stroke_width=8)
        tags_ = VGroup(*[Dot([x, 2.22, 0], radius=0.09, color=THRESH) for x in np.sort(g.uniform(-5.9, 5.9, 16))])
        dl = label(r"the same DNA in every cell; \ chemical tags help decide which genes are switched on", font_size=30,
                   color=WHITE).next_to(dna, DOWN, buff=0.25)
        rows = rows_of([
            (r"experience can move the tags: \ rat pups that were licked and groomed more grew up with fewer tags on a "
             r"stress-response gene, \ and a calmer response to stress", WHITE),
            (rf"in people: \ {h['people']} adults conceived in the Dutch famine of {h['famine'][0]}--{h['famine'][1] % 100}, "
             rf"\ six decades on, \ had fewer tags on a growth gene than their own brothers and sisters", DATA),
            (r"not established: \ that such marks are handed down the generations in humans", BAD),
        ], 12.4, 30, 0.28).move_to([0, -1.25, 0])
        src = published_tag(archive.HEIJMANS_2008.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Last, a word you'll have heard: epigenetics. <bookmark mark='a'/> Every cell in your body "
            "has the same DNA, yet a neuron isn't a liver cell. The difference is in which genes are "
            "switched on, and one of the switches is a chemical tag attached to the DNA. "
            "<bookmark mark='b'/> Experience can move the tags. Rat pups that were licked and groomed "
            "more by their mothers grew up with fewer tags on a gene that regulates the response to "
            "stress, and they handled stress more calmly. <bookmark mark='c'/> And in people: "
            f"{h['people']} men and women who were conceived during the Dutch famine of "
            f"{h['famine'][0]} had, six decades later, fewer tags on a growth gene than their own "
            "brothers and sisters. <bookmark mark='d'/> So the environment writes on the genome's "
            "switches. That's one way nurture gets into biology. What isn't established is the popular "
            "claim that such marks are handed down through the generations in people. Treat that one as "
            "open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), Create(dna))
            vo.wait_until("a")
            self.play(FadeIn(tags_, lag_ratio=0.1), FadeIn(dl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), *[t.animate.set_opacity(0.15) for t in tags_[::3]])
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()
