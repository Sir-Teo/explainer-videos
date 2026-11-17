from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403

WORLDS = (("common", r"one common cause", G), ("sampling", r"Thomson's sampling", VERB),
          ("mutualism", r"mutualism", VIS))


class Worlds(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.same()
        self.experiment()

    def card(self):
        card = chapter_card(5, r"What $g$ is not shown to be", r"Does a factor prove a cause?",
                            lit={1916: r"Thomson", 2006: r"van der Maas et al."}, part=PART,
                            scale=("brain", "person", "group"), marr=("what", "how"))
        with self.voiceover("Chapter five. What g is not shown to be."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def three(self):
        head = heading(r"Three worlds")
        icons = VGroup()
        # common cause: one node feeding eight
        c0 = Dot([0, 0.6, 0], radius=0.16, color=G)
        c_tests = VGroup(*[Dot([-1.05 + 0.3 * i, -0.4, 0], radius=0.07, color=WHITE) for i in range(8)])
        c_arrows = VGroup(*[Line(c0.get_center(), t.get_center(), color=G, stroke_width=1.5) for t in c_tests])
        icons.add(VGroup(c_arrows, c0, c_tests))
        # sampling: many small bonds, tests drawing overlapping subsets
        rng = np.random.default_rng(4)
        bonds = VGroup(*[Dot([x, y, 0], radius=0.025, color=GREY_B) for x, y in zip(rng.uniform(-1.1, 1.1, 90),
                                                                                     rng.uniform(0.1, 0.9, 90))])
        s_tests = VGroup(*[Dot([-1.05 + 0.3 * i, -0.4, 0], radius=0.07, color=WHITE) for i in range(8)])
        s_lines = VGroup()
        for i, t in enumerate(s_tests):
            for b in rng.choice(90, 6, replace=False):
                s_lines.add(Line(bonds[b].get_center(), t.get_center(), color=VERB, stroke_width=0.8,
                                 stroke_opacity=0.6))
        icons.add(VGroup(s_lines, bonds, s_tests))
        # mutualism: eight abilities in a ring, each helping the others
        ring = VGroup(*[Dot([0.75 * np.cos(2 * PI * i / 8), 0.2 + 0.6 * np.sin(2 * PI * i / 8), 0], radius=0.08,
                            color=WHITE) for i in range(8)])
        m_lines = VGroup(*[Line(ring[i].get_center(), ring[j].get_center(), color=VIS, stroke_width=1)
                           for i in range(8) for j in range(i + 1, 8)])
        icons.add(VGroup(m_lines, ring))
        for i, ic in enumerate(icons):
            ic.move_to([-4.4 + 4.4 * i, 1.0, 0])
        names = VGroup(*[label(t, font_size=24, color=c).next_to(icons[i], DOWN, buff=0.3)
                         for i, (_, t, c) in enumerate(WORLDS)])
        texts = VGroup(*[wrapped_label(t, 3.9, 19, GREY_A).next_to(names[i], DOWN, buff=0.2) for i, t in enumerate((
            r"a single latent ability, \ $g$, \ raises every score; \ each test adds something specific",
            r"Godfrey Thomson, \ 1916: \ each test draws on a random sample of many independent elementary "
            r"abilities; \ tests correlate because their samples overlap; \ there is no $g$",
            r"Han van der Maas and colleagues, \ 2006: \ abilities start independent and help each other grow, \ "
            r"vocabulary helping reading helping memory; \ there is no $g$"))])
        tag = psyche_tag(r"\texttt{traits.common\_cause, \ sampling, \ mutualism}")
        with self.voiceover(
            "Spearman read the positive manifold as one underlying ability. It isn't the only way to get one. "
            "Psyche builds three worlds of eight tests each. <bookmark mark='a'/> In the first, a single latent "
            "ability, g, raises every score, and each test adds something specific. <bookmark mark='b'/> The second "
            "is Godfrey Thomson's, from 1916. Each test draws on a random sample of many independent elementary "
            "abilities, and tests correlate because their samples overlap. There's no g. Thomson made his point with "
            "dice. <bookmark mark='c'/> The third is Han van der Maas and colleagues' mutualism, from 2006. "
            "Abilities start out independent and help each other grow, vocabulary helping reading helping memory. "
            "Again there's no g."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, i in zip("abc", range(3)):
                vo.wait_until(m)
                self.play(FadeIn(icons[i]), FadeIn(names[i]), FadeIn(texts[i]))
        self.clear_scene()

    def same(self):
        d = load("worlds")
        head = heading(r"The same correlations")
        hms = VGroup()
        for i, (k, t, c) in enumerate(WORLDS):
            hm = heatmap(d[f"R_{k}"], cell=0.34, values=False)
            nm = label(t, font_size=21, color=c).next_to(hm, UP, buff=0.2)
            stat = VGroup(label(rf"smallest $r$ = {d[f'min_{k}']:.2f}", font_size=17),
                          label(rf"one factor rejected in {pct(d[f'reject_{k}'])} of samples", font_size=17,
                                color=GOOD)).arrange(DOWN, buff=0.1).next_to(hm, DOWN, buff=0.25)
            hms.add(VGroup(hm, nm, stat).move_to([-4.4 + 4.4 * i, 0.4, 0]))
        rows = rows_of([
            (rf"300 simulated people per sample, \ {d['reps']} samples per world: \ every world has a positive "
             r"manifold, \ and a one-factor model fits it", WHITE),
            (r"the test of one factor rejects in 4 to 8\% of samples, \ close to the 5\% that chance alone gives when "
             r"one factor is true", GOOD),
            (r"so a good factor model shows that the correlations could come from one cause, \ not that they do",
             YOU),
        ], 12.4, 22, 0.32).move_to([0, -2.6, 0])
        tag = psyche_tag(r"\texttt{traits.one\_factor}: \ 200 samples per world")
        with self.voiceover(
            "Now give each world's tests to three hundred people and factor-analyse the results. "
            f"<bookmark mark='a'/> Psyche does it {d['reps']} times per world. Every world has a positive manifold, "
            "and a one-factor model fits it. <bookmark mark='b'/> The test of one factor rejects in four to eight "
            "percent of samples, close to the five percent that chance alone gives when one factor is true. "
            "<bookmark mark='c'/> So a good factor model shows that the correlations could come from one cause, not "
            "that they do. A factor is a summary of covariation, and three quite different machines produce it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(h) for h in hms], lag_ratio=0.4), run_time=3.0)
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def experiment(self):
        d = load("worlds")
        head = heading(r"An experiment can tell them apart")
        A = axes([-0.6, 7.6], [-0.05, 0.55], x_length=6.2, y_length=3.6, xticks=list(range(8)),
                 yticks=[0, 0.25, 0.5], xfmt=lambda v: f"{int(v) + 1}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"ability", ylabel=r"change (SD)", center=[-3.0, -0.4, 0], font_size=15)
        bc = bars(A.ax, np.arange(8) - 0.18, d["train_common"], G, width=0.34)
        bm = bars(A.ax, np.arange(8) + 0.18, d["train_mutualism"], VIS, width=0.34)
        key = legend([(G, r"common cause"), (VIS, r"mutualism")], font_size=17).move_to(A.ax.c2p(5.0, 0.45))
        rows = rows_of([
            (r"train ability 1 alone: \ raise its resource, \ and let everything settle", WHITE),
            (r"in the common-cause world, \ only ability 1 moves: \ training a test's specific part leaves $g$, \ "
             r"and the other tests, \ where they were", G),
            (rf"in the mutualism world, \ the others rise too, \ by about {np.mean(d['train_mutualism'][1:]):.2f} "
             r"SD, \ through the coupling", VIS),
            (r"so the question is causal, \ and it needs interventions and development, \ not more factor analysis: "
             r"\ the frontier of chapter fifteen", YOU),
        ], 5.6, 21, 0.36).move_to([3.6, -0.2, 0])
        tag = psyche_tag(r"\texttt{traits.train\_one}")
        with self.voiceover(
            "What can tell the worlds apart is an experiment. <bookmark mark='a'/> Train ability one alone: raise "
            "its resource, and let everything settle. <bookmark mark='b'/> In the common-cause world only ability "
            "one moves. Training a test's specific part leaves g, and the other tests, where they were. "
            "<bookmark mark='c'/> In the mutualism world the other abilities rise too, by about "
            f"{np.mean(d['train_mutualism'][1:]):.2f} of a standard deviation, through the coupling. "
            "<bookmark mark='d'/> So whether g is a thing is a causal question. It needs interventions and the study "
            "of development, not more factor analysis, and it's on the frontier in chapter fifteen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bc), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(bm), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
