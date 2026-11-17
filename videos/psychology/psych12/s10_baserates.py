from __future__ import annotations

import numpy as np

from videos.psychology.psych12.common import *  # noqa: F403


class BaseRates(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.tree()
        self.odds()
        self.curve_()

    def card(self):
        card = chapter_card(9, r"Base rates", r"A good test says yes. \ How likely is it that something is there?",
                            lit={1995: r"Gigerenzer and Hoffrage"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter nine. Base rates."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def problem(self):
        d = load("baserates")
        head = heading(r"The mammogram problem")
        rows = rows_of([
            (r"1\% of women screened have breast cancer", SIGNALC),
            (r"if a woman has it, \ the mammogram is positive 80\% of the time: \ the hit rate", HIT),
            (r"if she does not, \ it is still positive 9.6\% of the time: \ the false-alarm rate", FA),
            (r"a woman's mammogram is positive. \ How likely is it that she has cancer?", THRESH),
        ], 11.6, 32, 0.38).move_to([0, 0.6, 0])
        ans = label(rf"about {pct(d['nf_ppv'])}", font_size=60, color=THRESH).move_to([0, -2.3, 0])
        tags = VGroup(published_tag(archive.GIGERENZER_HOFFRAGE_1995.cite),
                      note(r"the problem's numbers, \ as posed in the studies").to_corner(DR, buff=0.3))
        with self.voiceover(
            "Detection theory describes the test. It doesn't, on its own, tell you what a yes means. Here's a "
            "problem that has been put to doctors and students for decades, with these numbers. "
            "<bookmark mark='a'/> One percent of the women screened have breast cancer. <bookmark mark='b'/> If a "
            "woman has it, the mammogram is positive eighty percent of the time: that's the hit rate. "
            "<bookmark mark='c'/> If she doesn't, it's still positive nine point six percent of the time: the "
            "false-alarm rate. <bookmark mark='d'/> A woman's mammogram is positive. How likely is it that she has "
            "cancer? Take a moment. <bookmark mark='e'/> The answer is about eight percent. Most people, doctors "
            "included, guess far higher."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags), FadeIn(rows[0]))
            for i, m in enumerate("bcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[i + 1]))
            vo.wait_until("e")
            self.play(FadeIn(ans, scale=0.8))
        self.clear_scene()

    def tree(self):
        d = load("baserates")
        head = heading(r"The same problem in natural frequencies")

        def box(txt, col, w=2.6, fs=26):
            r = RoundedRectangle(width=w, height=0.8, corner_radius=0.12, color=col, stroke_width=2.5, fill_color=col,
                                 fill_opacity=0.1)
            return VGroup(r, label(txt, font_size=fs, color=col).move_to(r))
        top = box(r"1{,}000 women", WHITE).move_to([-2.6, 2.2, 0])
        sick = box(r"10 have cancer", SIGNALC).move_to([-4.6, 0.7, 0])
        well = box(r"990 do not", NOISEC).move_to([-0.3, 0.7, 0])
        tp = box(r"8 test positive", HIT, 2.2, 23).move_to([-5.6, -0.9, 0])
        fn = box(r"2 negative", MISS, 1.7, 23).move_to([-3.55, -0.9, 0])
        fp = box(rf"{d['nf_false_positive']:.0f} test positive", FA, 2.3, 23).move_to([-1.4, -0.9, 0])
        tn = box(r"895 negative", HIT, 1.9, 23).move_to([0.75, -0.9, 0])

        def arr(a, b):
            return Arrow(a.get_bottom(), b.get_top(), buff=0.06, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        arrows = VGroup(arr(top, sick), arr(top, well), arr(sick, tp), arr(sick, fn), arr(well, fp), arr(well, tn))
        frac = MathTex(rf"\frac{{8}}{{8 + {d['nf_false_positive']:.0f}}} = \frac{{8}}{{{d['nf_positives']:.0f}}}"
                       rf"\approx {100 * d['nf_ppv']:.1f}\%", font_size=46, color=THRESH).move_to([-2.4, -2.6, 0])
        rows = rows_of([
            (r"count people instead of multiplying probabilities", WHITE),
            (r"of 103 positive tests, \ 8 are cancers: \ the false alarms swamp the hits", FA),
            (rf"Gigerenzer and Hoffrage (1995): \ correct answers rose from {pct(d['correct_prob'])} with "
             rf"probabilities to {pct(d['correct_freq'])} with frequencies", DATA),
            (r"still fewer than half: \ base rates are hard, \ but the format helps", GREY_A),
        ], 4.0, 26, 0.3).move_to([4.8, 0.3, 0])
        keep_in_frame(rows)
        tag = published_tag(archive.GIGERENZER_HOFFRAGE_1995.cite)
        with self.voiceover(
            "Here's the same problem told in counts instead of percentages. <bookmark mark='a'/> Picture a thousand "
            "women. Ten have cancer, and nine hundred and ninety don't. <bookmark mark='b'/> Of the ten, eight test "
            "positive. Of the nine hundred and ninety, about ninety-five test positive too, because nine point six "
            "percent of a large number is a large number. <bookmark mark='c'/> So of a hundred and three positive "
            "tests, eight are cancers. Eight percent. The false alarms swamp the hits, because there are so many "
            "more healthy women to make them. <bookmark mark='d'/> In 1995 Gerd Gigerenzer and Ulrich Hoffrage "
            "showed that this way of telling it, natural frequencies, roughly tripled the share of people who got "
            f"the right answer: from about {100 * d['correct_prob']:.0f} percent to {100 * d['correct_freq']:.0f}. "
            "<bookmark mark='e'/> Still fewer than half. Base rates are hard for minds, and the format of the "
            "numbers matters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(top), GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(sick), FadeIn(well), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[GrowArrow(a) for a in arrows[2:]], FadeIn(tp), FadeIn(fn), FadeIn(fp), FadeIn(tn))
            vo.wait_until("c")
            self.play(Write(frac), FadeIn(rows[1]), Indicate(tp), Indicate(fp))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def odds(self):
        d = load("odds")
        head = heading(r"Bayes's rule in one line: \ odds times the likelihood ratio")
        eqs = VGroup(
            MathTex(r"\text{odds after} \;=\; \text{odds before} \times \frac{H}{F}", font_size=44, color=THRESH),
            MathTex(rf"\frac{{1}}{{99}} \times \frac{{0.8}}{{0.096}} = \frac{{1}}{{99}} \times {d['lr']:.1f}"
                    rf"\approx \frac{{{d['post_odds'] * 100:.1f}}}{{100}}", font_size=40, color=WHITE),
            MathTex(rf"P = \frac{{{d['post_odds']:.3f}}}{{1 + {d['post_odds']:.3f}}} \approx {100 * d['post_p']:.1f}\%",
                    font_size=40, color=FA),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([-2.4, 0.9, 0])
        rows = rows_of([
            (r"$H/F$ is the likelihood ratio of a positive test: \ chapter 5's $\ell$, \ for a yes", MODEL),
            (rf"a second, \ independent positive multiplies again: \ {pct(d['second_p'])}", HIT),
            (rf"a negative test: \ ratio $(1-H)/(1-F) = {d['lr_neg']:.2f}$, \ cancer {pct(d['neg_p'], 2)}", NOISEC),
            (r"the test supplies the ratio; \ the population supplies the odds", THRESH),
        ], 11.6, 28, 0.3).to_edge(DOWN, buff=0.7)
        tag = psyche_tag(r"computed: \ the mammogram's rates")
        with self.voiceover(
            "The same arithmetic fits on one line, and it ties this chapter to chapter five. "
            "<bookmark mark='a'/> The odds of cancer after a positive test are the odds before it, times the hit "
            "rate over the false-alarm rate. <bookmark mark='b'/> One in ninety-nine, times "
            f"{d['lr']:.1f}, gives odds of about eight in a hundred, which is a probability of about "
            f"{100 * d['post_p']:.0f} percent. <bookmark mark='c'/> And that ratio, hits over false alarms, is the "
            "likelihood ratio of a positive result: chapter five's quantity, for a yes. <bookmark mark='d'/> If a "
            "second, independent test is also positive, multiply again: the probability rises to "
            f"{100 * d['second_p']:.0f} percent. <bookmark mark='e'/> A negative test has a ratio below one and "
            "brings the probability down to about one in five hundred. <bookmark mark='f'/> The test supplies the "
            "ratio. The population supplies the odds. You need both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eqs[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]), FadeIn(eqs[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
            vo.wait_until("f")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def curve_(self):
        d = load("baserates")
        head = heading(r"The same test, \ different populations")
        A = axes([-3, -0.3], [0, 1], x_length=6.6, y_length=4.0, xticks=[-3, -2, -1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: {-3: r"0.1\%", -2: r"1\%", -1: r"10\%"}[int(v)], yfmt=lambda v: f"{v:g}",
                 xlabel=r"how common the disease is (log scale)", ylabel=r"share of positives that are real",
                 center=[-2.9, -0.2, 0])
        ax = A.ax
        c = curve(ax, np.log10(d["prevalence"]), d["ppv"], THRESH, stroke_width=5)
        p1 = Dot(ax.c2p(-2, d["ppv_at_01"]), radius=0.08, color=FA)
        p10 = Dot(ax.c2p(-1, d["ppv_at_10"]), radius=0.08, color=HIT)
        rows = rows_of([
            (rf"the test is the same everywhere: \ $d' = {d['d']:.1f}$, \ the same criterion", MODEL),
            (rf"screening, \ 1\% ill: \ {pct(d['ppv_at_01'])} of positives are real", FA),
            (rf"a clinic where 10\% are ill: \ {pct(d['ppv_at_10'])}", HIT),
            (r"$d'$ and $c$ describe the test; \ what a ``yes'' means also depends on who is tested", THRESH),
        ], 4.8, 27, 0.3).move_to([4.3, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ the mammogram's two rates, \ at every prevalence")
        with self.voiceover(
            "Now keep the test fixed and change who is tested. <bookmark mark='a'/> The hit and false-alarm rates "
            f"stay the same, d prime of about {d['d']:.1f} with the same criterion. <bookmark mark='b'/> In "
            f"screening, where one woman in a hundred is ill, {100 * d['ppv_at_01']:.0f} percent of positives are "
            f"real. <bookmark mark='c'/> In a clinic where one in ten is ill, it's {100 * d['ppv_at_10']:.0f} "
            "percent. <bookmark mark='d'/> Same machine, same reader, different meaning. d prime and c describe the "
            "test. What a yes means depends also on the population. That's the arithmetic underneath every "
            "argument about who should be screened."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(c), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(p1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(p10), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
