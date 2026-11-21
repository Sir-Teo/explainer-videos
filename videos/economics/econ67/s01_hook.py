from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.camel()
        self.first_tries()
        self.question()
        self.title()
        self.objectives()

    def camel_axes(self):
        C = load("camel")
        ax = plane([0, 6], [0, 6000], center=LEFT * 1.3 + DOWN * 0.45, x_length=9.6, y_length=4.9,
                   xticks=[0, 1, 1.96, 3, 4, 5, 6], yticks=[0, 2000, 4000, 6000],
                   xlabel=r"$|z|$, \ the estimate over its standard error",
                   ylabel=r"published results \ (per 0.1 of $|z|$)",
                   xfmt=lambda v: "1.96" if abs(v - 1.96) < 1e-9 else f"{v:.0f}", yfmt=lambda v: f"{v:,.0f}",
                   font_size=14)
        line = vline(ax, 1.96, 0, 6000, FAIL, 2.4)
        llab = label(r"$p = 0.05$", font_size=16, color=FAIL).next_to(ax.ax.c2p(1.96, 6000), UP, buff=0.08)
        return C, ax, line, llab

    def camel(self):
        hc = history_card(r"2016", r"Star Wars: \ the empirics strike back", r"Brodeur, \ L\'e, \ Sangnier and "
                          r"Zylberberg collect 50,000 test statistics from the AER, \ the JPE and the QJE, \ "
                          r"2005--2011", color=E.ACCENT, width=11.6, font_size=22).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"a valley: \ $p$ between 0.25 and 0.10 \ ($|z|$ from 1.15 to 1.65)", font_size=22, color=FIRST),
            label(r"a bump: \ $p$ just below 0.05 \ ($|z|$ just above 1.96)", font_size=22, color=PUB),
            label(r"the missing results: \ 10 to 20\% of those just significant", font_size=22, color=FAIL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(hc, DOWN, buff=0.6)
        tag = published_tag(r"Brodeur, \ L\'e, \ Sangnier and Zylberberg, \ \emph{AEJ: Applied} 8(1) (2016)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "In 2016 four economists, Abel Brodeur, Mathias Lé, Marc Sangnier and Yanos Zylberberg, did something "
            "simple. <bookmark mark='a'/> They collected fifty thousand test statistics from three of the most "
            "prestigious journals in economics, everything published between 2005 and 2011, and drew their "
            "distribution. If journals printed whatever researchers found, that distribution would be smooth. It "
            "was not. <bookmark mark='b'/> There was a valley where results are close to significant but not "
            "quite, p-values between a quarter and a tenth. <bookmark mark='c'/> And a bump just past the line of "
            "statistical significance, the famous five percent. <bookmark mark='d'/> They estimated that between a "
            "tenth and a fifth of the results that just clear the line should have fallen short of it. Results "
            "that were nearly significant had gone somewhere."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(hc, scale_factor=1.02))
            for mk, r_ in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def first_tries(self):
        C, ax, line, llab = self.camel_axes()
        bins = np.array(C["bins"], float)
        pub = histogram(ax, bins, C["published"], PUB, opacity=0.8)
        first = outline(ax, bins, C["first"], FIRST, scale=C["scale"], width=2.8)
        cal, cal0 = C["caliper"], C["caliper_first"]
        side = VGroup(
            legend_rows([(PUB, "published"), (FIRST, "every study's first try (rescaled)")], font_size=16),
            label(rf"just above 1.96 against just below: \\ published \ {cal['ratio']:.1f} to 1", font_size=17,
                  color=PUB),
            label(rf"first tries \ {cal0['ratio']:.1f} to 1", font_size=17, color=FIRST),
            label(r"the valley and the bump are made \\ by search and by selection", font_size=17,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax.ax, RIGHT, buff=0.3).shift(UP * 0.6)
        if side.get_right()[0] > 6.9:
            side.scale_to_fit_width(6.9 - side.get_left()[0])
        rules = VGroup(
            label(r"160,000 studies, \ true effects known \ (three in ten exactly zero)", font_size=16,
                  color=GREY_A),
            label(r"after an insignificant first try, \ some researchers search other specifications",
                  font_size=16, color=FIRST),
            label(r"journals publish every significant result \ and about a third of the rest", font_size=16,
                  color=PUB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rules.next_to(ax.ax.c2p(2.7, 6000), DR, buff=0.0)
        tag = island_tag(r"a simulated field: \ agora.field.mixed\_field \ (160,000 studies, \ true effects known)",
                         corner=DL, font_size=12)
        with self.voiceover(
            "This series cannot reach into those journals' files, but it can build a field in which the truth is "
            "known. <bookmark mark='a'/> A hundred and sixty thousand studies, each with a true effect, which for "
            "three in ten is exactly zero. <bookmark mark='a2'/> Each researcher runs a first analysis. If it is not "
            "significant, some try other reasonable specifications and report the first that works. <bookmark "
            "mark='a3'/> Journals then publish every significant result and about a third of the rest. <bookmark "
            "mark='b'/> Here is what gets published, "
            f"{C['n_pub']:,} results. The camel's valley and its bump are both there. <bookmark mark='c'/> And here, "
            "in blue, is what the same studies found on their first try, rescaled to the same total: smooth, no "
            "valley, no bump. <bookmark mark='d'/> Just above the line against just below it, the published "
            f"results run {cal['ratio']:.1f} to one; the first tries, {cal0['ratio']:.1f} to one. In this field "
            "we know exactly where the bump comes from, because we built it: from researchers who search and "
            "journals that select."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(line), FadeIn(llab), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rules[0], shift=RIGHT * 0.1))
            vo.wait_until("a2")
            self.play(FadeIn(rules[1], shift=RIGHT * 0.1))
            vo.wait_until("a3")
            self.play(FadeIn(rules[2], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeOut(rules), FadeIn(side[0][0]),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in pub], lag_ratio=0.02), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(first), FadeIn(side[0][1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 32, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"how often do published results replicate, \ and which ones?", font_size=26, color=TRUE),
            label(r"how do search and selection bend a literature, \ and can we correct for them?", font_size=26,
                  color=PUB),
            label(r"what changed when economics turned empirical?", font_size=26, color=STATE),
            label(r"what do the models leave out, \ and who decides what is published?", font_size=26,
                  color=FIRST),
            label(r"and what will machines change?", font_size=26, color=FAIL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "Sixty-six parts have told you what economics says. This one asks how much of it is true. <bookmark "
            "mark='a'/> How often do published results replicate, and can you tell in advance which ones will? "
            "<bookmark mark='b'/> How do search and selection bend a literature, and can we correct for them? "
            "<bookmark mark='c'/> What changed when economics turned from theory to data? <bookmark mark='d'/> What "
            "do its models leave out, and who decides what gets published? <bookmark mark='e'/> And what will "
            "machines change about how economists find things out?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        C = load("camel")
        ax = plane([0, 6], [0, 6000], x_length=5.2, y_length=1.5, xticks=[], yticks=[], font_size=12)
        ax.ax.set_opacity(0.0)
        bins = np.array(C["bins"], float)
        humps = histogram(ax, bins, C["published"], PUB, opacity=0.8)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 67 \ $\cdot$ \ The Next Economics", font_size=34, color=E.ACCENT)
        VGroup(humps, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part sixty-seven: the next economics."):
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in humps], lag_ratio=0.02), run_time=1.4)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act XII \ $\cdot$ \ The Frontier", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"replication and reproduction: \ what the large projects found, \ and why effects shrink",
            r"specification search and publication bias: \ how to see them, \ and how to correct for them",
            r"remedies: \ pre-analysis plans, \ registered reports, \ multiple testing",
            r"the empirical turn, \ many analysts, \ and the models' blind spots",
            r"the profession and the machines: \ who publishes, \ and what AI changes",
        ], color=E.ACCENT, font_size=28, width=13.0)
        with self.voiceover(
            "Part sixty-six asked what states do with trade. This part turns the series' tools on economics itself. "
            "By the end you will know <bookmark mark='a'/> what the large replication projects found, and why "
            "replicated effects are smaller; <bookmark mark='b'/> how to see specification search and publication "
            "bias in a literature, and how to correct for them; <bookmark mark='c'/> what pre-analysis plans, "
            "registered reports and multiple-testing rules can and cannot do; <bookmark mark='d'/> how the field "
            "turned empirical, why many analysts on one dataset disagree, and what equilibrium models leave out; "
            "<bookmark mark='e'/> and how the profession, and now machines, shape what economists find."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
