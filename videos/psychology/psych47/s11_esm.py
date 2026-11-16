from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403


class Esm(VoiceoverScene):
    def construct(self):
        self.card()
        self.diaries()
        self.inertia()
        self.relmean()

    def card(self):
        card = chapter_card(10, r"Intensive longitudinal data", r"What does a month of a life look like as data?",
                            lit={1983: r"Csikszentmihalyi", 2010: r"Kuppens et al."}, part=PART, scale=("person",),
                            marr=("what", "how"))
        with self.voiceover("Chapter ten. Intensive longitudinal data."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def diaries(self):
        head = heading(r"Experience sampling")
        A = axes([0, 60], [-3, 3], x_length=11.0, y_length=2.0, xticks=[0, 20, 40, 60], yticks=[-2, 0, 2],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"prompt", ylabel=r"mood",
                 center=[0, 1.3, 0], font_size=12)
        rng = np.random.default_rng(47)
        x = np.zeros(60)
        for t in range(1, 60):
            x[t] = 0.5 * x[t - 1] + rng.normal(0, 0.8)
        c = curve(A.ax, np.arange(60), x, PERSON, stroke_width=3)
        rows = rows_of([
            (r"a phone asks, \ several times a day for weeks: \ how do you feel, \ where are you, \ what are you doing?",
             WHITE),
            (r"each person becomes a time series: \ their own mean, \ their own spread, \ and how much each moment "
             r"carries over to the next", MODEL),
            (r"the carry-over is the autoregression, \ or inertia: \ a mood that lingers", PERSON),
            (r"from many series, \ a network of how one person's states predict each other: \ person-specific, \ "
             r"not population-average", GOOD),
        ], 12.4, 20, 0.34).move_to([0, -1.7, 0])
        tag = label(r"one illustrative series", font_size=13, color=GREY_B).to_corner(DR, buff=0.3)
        with self.voiceover(
            "To study a person, measure a person often. <bookmark mark='a'/> In experience sampling, a phone asks "
            "several times a day, for weeks: how do you feel, where are you, what are you doing? "
            "<bookmark mark='b'/> Each person becomes a time series, with their own mean, their own spread, and how "
            "much each moment carries over to the next. <bookmark mark='c'/> That carry-over is the autoregression, "
            "or inertia: a mood that lingers. <bookmark mark='d'/> From several series, a network of how one person's "
            "states predict each other: person-specific, not a population average."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(c), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def inertia(self):
        d = load("inertia")
        head = heading(r"Inertia, \ and its estimate")
        A = axes([0, 210], [0, 0.45], x_length=5.6, y_length=3.0, xticks=[10, 50, 100, 200], yticks=[0, 0.2, 0.4],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"occasions per person",
                 ylabel=r"average estimate", center=[-3.3, 0.3, 0], font_size=13)
        truth = DashedLine(A.ax.c2p(0, d["phi"]), A.ax.c2p(210, d["phi"]), color=GOOD, stroke_width=2)
        c = curve(A.ax, d["T"], d["mean_est"], AUTH, stroke_width=4)
        dots = VGroup(*[Dot(A.ax.c2p(t, e), radius=0.07, color=AUTH) for t, e in zip(d["T"], d["mean_est"])])
        rows = rows_of([
            (r"Kuppens, \ Allen and Sheeber, \ 2010: \ emotions that linger, \ high inertia, \ go with depressive "
             r"symptoms", WHITE),
            (rf"but inertia estimated around a person's own mean is biased toward zero: \ with a true 0.4, \ 20 "
             rf"occasions give {d['mean_est'][1]:.2f} on average, \ 10 give {d['mean_est'][0]:.2f}", AUTH),
            (r"the bias is about $(1 + 3\phi)/T$: \ people with fewer answers look less inert, \ a confound if "
             r"compliance differs between groups", PERSON),
            (r"and inertia adds little beyond a person's mean and spread (the Ledger)", MODEL),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.inertia\_bias}, \ 2{,}000 series per point")
        with self.voiceover(
            "Inertia became a measure of risk. <bookmark mark='a'/> In 2010 Peter Kuppens, Nicholas Allen and Lisa "
            "Sheeber reported that emotions that linger go with depressive symptoms. <bookmark mark='b'/> But inertia "
            "estimated around a person's own mean is biased toward zero. With a true value of zero point four, twenty "
            "occasions give about zero point three on average, and ten give less than half the truth. "
            "<bookmark mark='c'/> The bias is about one plus three phi, over the number of occasions. People who "
            "answer fewer prompts look less inert: a confound if compliance differs between groups. "
            "<bookmark mark='d'/> And inertia turns out to add little beyond a person's mean and spread. That's in "
            "the Ledger."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(truth))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), FadeIn(dots))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def relmean(self):
        d = load("relmean")
        head = heading(r"How many prompts?")
        A = axes([0, 60], [0, 1.05], x_length=5.6, y_length=3.0, xticks=[1, 14, 28, 56], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"prompts averaged",
                 ylabel=r"reliability of a person's average", center=[-3.3, 0.3, 0], font_size=13)
        c = curve(A.ax, d["k"], d["rel"], MODEL, stroke_width=4)
        dots = VGroup(*[Dot(A.ax.c2p(k, v), radius=0.07, color=PERSON) for k, v in zip(d["k"], d["rel_sim"])])
        i7, i28 = list(d["k"]).index(7), list(d["k"]).index(28)
        rows = rows_of([
            (r"one prompt's mood is 40\% the person, \ 60\% the moment", WHITE),
            (r"average $k$ prompts, \ and Spearman-Brown (Part 3) gives the reliability of the person's mean", MODEL),
            (rf"a week of daily prompts: \ {d['rel'][i7]:.2f}; \ four weeks: \ {d['rel'][i28]:.2f}", PERSON),
            (r"but the moments are not noise: \ their spread, \ their inertia and their reaction to events are what "
             r"experience sampling is for", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"500 simulated people (dots) \ against Spearman-Brown")
        with self.voiceover(
            "How many prompts does a diary need? <bookmark mark='a'/> Say one prompt's mood is forty percent the "
            "person and sixty percent the moment. <bookmark mark='b'/> Average k prompts, and Spearman and Brown's "
            "formula, from Part 3, gives the reliability of the person's mean. <bookmark mark='c'/> A week of daily "
            "prompts gives about zero point eight. Four weeks, about zero point nine five. <bookmark mark='d'/> But the "
            "moments aren't noise. Their spread, their inertia, and their reaction to events are what experience "
            "sampling is for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), FadeIn(dots))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
