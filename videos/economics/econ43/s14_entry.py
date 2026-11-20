from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class Entry(VoiceoverScene):
    def construct(self):
        card(self, 12, r"How many dentists does a town need?", r"What does the number of firms reveal?",
             "Chapter twelve. How many dentists does a town need?", lit={1991: r"Bresnahan and Reiss"},
             scale=("city", "market"), horizon=("a decade",))
        self.idea()
        self.towns()
        self.estimate()
        self.zipf()

    def idea(self):
        E_ = load("entry")
        S = np.array(E_["true_S"])
        lines = VGroup(
            MathTex(r"N \text{ firms enter while}\quad \text{population} \times \frac{v_N}{N} \;\ge\; F", font_size=38),
            MathTex(r"S_N \;=\; \frac{N\,F}{v_N}, \qquad \frac{S_{N+1}/(N+1)}{S_N/N} \;=\; \frac{v_N}{v_{N+1}}",
                    font_size=40, color=E.ACCENT),
        ).arrange(DOWN, buff=0.5).move_to(UP * 1.8)
        notes = VGroup(
            label(r"$v_N$: \ the market's profit per resident before fixed costs when $N$ firms compete", font_size=19,
                  color=GREY_A),
            label(r"if entry makes competition fiercer, \ each new firm needs more people than the last", font_size=20,
                  color=PRICE),
            label(r"if not \ (a cartel, \ or competition already complete), \ the ratio is one", font_size=20,
                  color=DEMAND),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=1.2)
        tag = published_tag(tables.BR_1991.tag, corner=DR, font_size=11)
        intro = point_cards([
            (r"about 200 towns", r"isolated, \\ in the western \\ United States", DEMAND),
            (r"local trades", r"doctors, \ dentists, \\ plumbers and \\ other businesses", PRICE),
            (r"one count", r"how many firms \\ each town \\ supports", GAIN),
        ], width=11.4, cols=3, font_size=19).move_to(DOWN * 0.2)
        with self.voiceover(
            "Sometimes market power can be read from the simplest data of all: how many firms there are. In 1991 "
            "Timothy Bresnahan and Peter Reiss studied about two hundred isolated towns in the western United States, "
            "far enough from cities that their residents bought locally, and counted the doctors, dentists, plumbers "
            "and other businesses in each. <bookmark mark='a'/> A town supports N firms while its population, times "
            "each firm's profit per resident, covers the fixed cost of opening. <bookmark mark='b'/> So the "
            "population needed for N firms is N times the fixed cost over the market's profit per resident. "
            "<bookmark mark='c'/> If each entrant makes competition fiercer, margins fall, and every additional "
            "firm needs more people per firm than the one before. <bookmark mark='d'/> If entry changes nothing, "
            "the population per firm stays the same. The ratio of successive thresholds measures how competition "
            "changes with each entrant."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in intro.cards], lag_ratio=0.5),
                      run_time=2.5)
            vo.wait_until("a")
            self.play(FadeOut(intro.cards), Write(lines[0]), FadeIn(notes[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Write(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        del S
        self.clear_scene()

    def towns(self):
        E_ = load("entry")
        T = TRUTH["towns"]
        pop = np.array(E_["pop"])
        n = np.array(E_["n"])
        K = len(T["margins"])
        rng = np.random.default_rng(5)
        ax = plane([np.log10(0.5), np.log10(40)], [-0.5, K + 0.5], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2,
                   y_length=4.6, xticks=[np.log10(v) for v in (0.5, 1, 2, 5, 10, 20, 40)],
                   yticks=list(range(K + 1)), xlabel=r"town population, \ thousands \ (log scale)",
                   ylabel=r"firms in town", xfmt=lambda v: f"{10 ** v:g}", yfmt=lambda v: f"{v:.0f}"
                   + (r"+" if v == K else ""), font_size=14)
        pts = VGroup(*[dot(ax, np.log10(p), k + rng.uniform(-0.22, 0.22), DEMAND, 0.04) for p, k in zip(pop, n)])
        S = np.array(E_["true_S"])
        steps = VGroup(*[vline(ax, np.log10(s), -0.5, K + 0.5, PRICE, 1.6) for s in S])
        side = VGroup(
            label(rf"{T['n']} Island towns", font_size=19, color=WHITE),
            label(r"each firm pays a \\ fixed cost; \ towns \\ differ in theirs a little", font_size=18,
                  color=GREY_A),
            label(r"gold: \ the planted \\ thresholds $S_1, \ldots, S_5$", font_size=18, color=PRICE),
            label(r"the margin per resident: \\ "
                  + r", \ ".join(f"{m:.2f}" for m in T["margins"]), font_size=17, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"The Island has {T['n']} isolated towns of different sizes. <bookmark mark='a'/> Each dot is a town: "
            "its population across, the number of dentists up. Small towns have none or one; large ones have "
            "five or more. <bookmark mark='b'/> The pattern is noisy, because towns differ a little in what opening "
            "costs. <bookmark mark='c'/> Behind it are the thresholds planted on the Island. <bookmark mark='d'/> "
            "The market's profit per resident falls from one with a single firm to 0.6 with two and 0.48 with three, "
            "then hardly at all: competition arrives with the second and third firm."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.004), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(s_) for s_ in steps], lag_ratio=0.2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def estimate(self):
        E_ = load("entry")
        tr = np.array(E_["true_ratio"])
        es = np.array(E_["est"]["ratio"])
        co = np.array(E_["cournot_ratio"])
        ax = plane([0.5, 4.5], [0.8, 2.0], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[1, 2, 3, 4], yticks=[0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
                   xlabel=r"entrant", ylabel=r"people per firm needed, \ relative to one firm fewer",
                   xfmt=lambda v: ("", r"\text{2nd}", r"\text{3rd}", r"\text{4th}", r"\text{5th}")[int(v)]
                   if 1 <= v <= 4 else "",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        one = seg(ax, 0.5, 1.0, 4.5, 1.0, DEMAND, 2.0, dashed=True)
        xs = np.arange(1, 5)
        tl = VGroup(path(ax, xs, tr, TRUTH_C, 3.0, smooth=False), *[dot(ax, x, y, TRUTH_C, 0.08)
                                                                    for x, y in zip(xs, tr)])
        el = VGroup(path(ax, xs, es, BLP_C, 3.0, smooth=False), *[dot(ax, x, y, BLP_C, 0.08)
                                                                  for x, y in zip(xs, es)])
        cl = VGroup(path(ax, xs, co, GREY_B, 2.0, smooth=False))
        side = VGroup(
            label(r"green: \ the truth", font_size=18, color=TRUTH_C),
            label(rf"teal: \ estimated from the \\ towns alone \ ({', '.join(f'{v:.2f}' for v in es)})",
                  font_size=17, color=BLP_C),
            label(r"grey: \ Cournot with \\ straight-line demand", font_size=17, color=GREY_B),
            label(r"dashed: \ a cartel, \ or \\ competition already \\ complete", font_size=17, color=DEMAND),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.BR_1991.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Bresnahan and Reiss estimated the thresholds with an ordered probit: the chance that a town has at "
            "least N firms rises with its population relative to the N-th threshold. <bookmark mark='a'/> On the "
            f"Island the truth says the second firm needs {tr[0]:.2f} times as many people per firm as the first, "
            f"the third {tr[1]:.2f} times as many as the second, and after that about one. "
            f"<bookmark mark='b'/> Estimated from nothing but populations and counts, the ratios are "
            f"{es[0]:.2f}, {es[1]:.2f}, {es[2]:.2f} and {es[3]:.2f}. <bookmark mark='c'/> For comparison, Cournot "
            "competition with straight-line demand would keep the ratio between 1.1 and 1.2, "
            "<bookmark mark='d'/> and a cartel would hold it at one. <bookmark mark='e'/> In America's towns "
            "Bresnahan and Reiss found the Island's "
            "pattern: competitive conduct changes quickly as the number of incumbents rises, most of the change "
            "comes with the second and third firms, and once a town has three to five, another entrant changes "
            "little."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(tl), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(el), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(cl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(one), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Indicate(VGroup(tl, el), color=WHITE, scale_factor=1.02))
        self.clear_scene()

    def zipf(self):
        A = tables.AXTELL_2001.data
        f = facts.BY_KEY["zipf_firms"]
        data_m = label(rf"about {A['firms']} million \\ American firms, \ {A['year']}: \\ an exponent close \\ to one",
                       font_size=18, color=WHITE)
        theory_m = label(r"random proportional \\ growth with entry \\ and exit \ (Gibrat)", font_size=18,
                         color=THEORY)
        agora_m = label(r"Part 52 \\ builds it", font_size=18, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, THEORY, None)).move_to(UP * 0.3)
        tag = published_tag(tables.AXTELL_2001.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Counting firms reveals another of the series' facts, at the scale of the whole economy. "
            "<bookmark mark='a'/> In 2001 Robert Axtell plotted the sizes of about five and a half million American "
            "firms and found Zipf's law: the number of firms larger than a given size falls in proportion to that "
            "size, with an exponent close to one, the same law that governed cities in Part thirty-seven. "
            "<bookmark mark='b'/> The usual theory is proportional random growth, with firms entering and exiting. "
            "<bookmark mark='c'/> Agora builds that economy of firms in Part fifty-two."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(fc.cols[k][2:]))
        self.clear_scene()
