from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403


class Fit(VoiceoverScene):
    def construct(self):
        self.card()
        self.chisq()
        self.indices()
        self.dynamic()

    def card(self):
        card = chapter_card(5, r"Does it fit?", r"How close is close enough?",
                            lit={1999: r"Hu \& Bentler", 2023: r"McNeish \& Wolf"}, part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter five. Does it fit?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def chisq(self):
        d = load("hs")
        head = heading(r"The chi-square test")
        A = axes([0, 100], [0, 0.07], x_length=5.6, y_length=2.8, xticks=[0, 24, 50, 85], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"$\chi^2$ on 24 df", center=[-3.3, 0.6, 0], font_size=13)
        from scipy import stats
        x = np.linspace(0.5, 100, 300)
        dens = curve(A.ax, x, stats.chi2.pdf(x, 24), GREY_A, stroke_width=3)
        mark = DashedLine(A.ax.c2p(d["t3_T"], 0), A.ax.c2p(d["t3_T"], 0.06), color=AUTH, stroke_width=2)
        m_l = label(r"Holzinger and Swineford", font_size=12, color=AUTH).next_to(A.ax.c2p(d["t3_T"], 0.06), UP, buff=0.05)
        rows = rows_of([
            (r"if the model were exactly right, \ $T$ would come from this curve, \ around 24", WHITE),
            (rf"the data give {d['t3_T']:.1f}: \ the model is rejected, \ $p < 10^{{-7}}$", AUTH),
            (rf"the one-factor model is far worse: \ $\chi^2 = {d['t1_T']:.0f}$ on {d['t1_df']:.0f} df", PERSON),
            (r"but no model is exactly right; \ with enough people, \ the test rejects every one: \ it answers a "
             r"question nobody asked", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        with self.voiceover(
            "First, the chi-square test of exact fit. <bookmark mark='a'/> If the model were exactly right, the "
            "statistic would come from this curve, centred near twenty-four. <bookmark mark='b'/> The data give "
            "eighty-five. The model is rejected, decisively. <bookmark mark='c'/> A single general factor does far "
            "worse. <bookmark mark='d'/> But no model of real people is exactly right, and with enough people the "
            "test rejects every one. It answers a question nobody really asked."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(dens))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(mark), FadeIn(m_l))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def indices(self):
        d = load("hs")
        head = heading(r"Approximate fit")
        data = (
            (r"RMSEA", rf"{d['t3_rmsea']:.3f}", r"misfit per degree of freedom, \ per person: \ $\sqrt{\max(T - "
                                                 r"df, 0)/(df\,n)}$", PERSON),
            (r"CFI", rf"{d['t3_cfi']:.3f}", r"how much better than a model of no correlations at all", MODEL),
            (r"TLI", rf"{d['t3_tli']:.3f}", r"the same comparison, \ penalized for complexity", SYMP),
            (r"SRMR", rf"{d['t3_srmr']:.3f}", r"the average residual correlation", GOOD),
        )
        rows = VGroup()
        for name, val, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=18, width=1.8), label(val, font_size=22, color=c),
                            wrapped_label(how, 7.6, 18, WHITE)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.5, 0])
        foot = rows_of([
            (r"Hu and Bentler, \ 1999: \ cut-offs of CFI at least 0.95, \ RMSEA at most 0.06 and SRMR at most 0.08, \ "
             r"from simulations of a few model types", PERSON),
            (r"by them this model fails; \ and the cut-offs became rules in thousands of papers", AUTH),
        ], 12.4, 20, 0.3).move_to([0, -2.4, 0])
        tag = published_tag(r"Hu \& Bentler (1999)")
        with self.voiceover(
            "So people use approximate fit. <bookmark mark='a'/> RMSEA measures misfit per degree of freedom and per "
            "person. <bookmark mark='b'/> CFI asks how much better the model is than a model with no correlations at "
            "all. <bookmark mark='c'/> TLI asks the same, with a penalty for complexity. <bookmark mark='d'/> And "
            "SRMR is the average residual correlation. <bookmark mark='e'/> In 1999 Li-tze Hu and Peter Bentler "
            "proposed cut-offs, from simulations of a few model types: CFI at least zero point nine five, RMSEA at "
            "most zero point oh six. By them this model fails. And the cut-offs became rules in thousands of papers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def dynamic(self):
        d = load("cutoffs")
        head = heading(r"Cut-offs that depend on the model")
        bins = np.linspace(0, 0.12, 25)
        top = 1.1 * max(np.histogram(np.clip(d[k], 0, 0.1199), bins)[0].max() for k in ("ok_rmsea", "miss_rmsea"))
        A = axes([0, 0.12], [0, top], x_length=5.6, y_length=3.0, xticks=[0, 0.03, 0.06, 0.09, 0.12], yticks=None,
                 xfmt=lambda v: f"{v:.2f}", xlabel=r"RMSEA in 200 samples of 301", center=[-3.3, 0.5, 0],
                 font_size=13)
        hist = VGroup()
        for key, c in (("ok_rmsea", GOOD), ("miss_rmsea", AUTH)):
            h, _ = np.histogram(np.clip(d[key], 0, 0.1199), bins)
            hist.add(bars(A.ax, (bins[:-1] + bins[1:]) / 2, h, c, width=0.0045, opacity=0.6))
        cut = DashedLine(A.ax.c2p(0.06, 0), A.ax.c2p(0.06, 0.97 * top), color=YOU, stroke_width=2)
        c_l = label(r"0.06", font_size=12, color=YOU).next_to(A.ax.c2p(0.06, 0.97 * top), UP, buff=0.05)
        key = VGroup(label(r"the model is right", font_size=13, color=GOOD),
                     label(r"one cross-loading of 0.4 left out", font_size=13, color=AUTH)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(A, DOWN, buff=0.3)
        q = lambda a, p: float(np.quantile(a, p))  # noqa: E731
        rows = rows_of([
            (r"Psyche draws 200 samples of 301 from the fitted model, \ and 200 from the same model with one "
             r"cross-loading left out", WHITE),
            (rf"the right model: \ 95\% of RMSEAs below {q(d['ok_rmsea'], 0.95):.3f}", GOOD),
            (rf"the misspecified one: \ RMSEA below 0.06 in {pct(np.mean(d['miss_rmsea'] <= 0.06))} of samples, \ "
             rf"CFI above 0.95 in {pct(np.mean(d['miss_cfi'] >= 0.95))}: \ the fixed cut-offs pass a wrong model", AUTH),
            (r"McNeish and Wolf, \ 2023: \ simulate from your own model to set the cut-off; \ a fixed 0.06 can be far "
             r"too strict or far too lenient", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{sem.fit\_cfa}, \ 400 simulated samples; \ McNeish \& Wolf (2023)")
        with self.voiceover(
            "But a cut-off only means something for a particular model. <bookmark mark='a'/> Psyche draws two hundred "
            "samples of three hundred and one children from the fitted model, and two hundred from the same model "
            "with one cross-loading left out. <bookmark mark='b'/> When the model is right, almost all the RMSEAs fall "
            "low. <bookmark mark='c'/> When it's wrong, they spread higher, but most still fall below the conventional "
            "cut-off, and nearly every CFI passes too. The fixed cut-offs pass a model that's wrong. "
            "<bookmark mark='d'/> In 2023 Daniel McNeish and Melissa Wolf proposed dynamic cut-offs: simulate from "
            "your own model to set them. A fixed zero point oh six can be far too strict, or far too lenient."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(cut), FadeIn(c_l), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(hist[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(hist[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
