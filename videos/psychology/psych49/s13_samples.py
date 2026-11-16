from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


class Samples(VoiceoverScene):
    def construct(self):
        self.card()
        self.spread()
        self.reported()
        self.reliability()
        self.chip()

    def card(self):
        card = chapter_card(12, r"The sample-size reckoning", r"How many people does a brain-behaviour claim need?",
                            lit=(), part=PART, scale=("brain", "person"), marr=("what",))
        with self.voiceover("Chapter twelve. The sample-size reckoning."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def spread(self):
        d = load("bwas")
        head = heading(r"One correlation, \ five sample sizes")
        ns = np.asarray(d["n"])
        A = axes([0.3, 5.7], [-0.35, 0.55], x_length=6.2, y_length=3.2, xticks=None, yticks=[-0.2, 0, 0.2, 0.4],
                 yfmt=lambda v: f"{v:g}", ylabel=r"observed $r$ (middle 95\%)", center=[-3.0, 0.3, 0], font_size=12)
        truth = DashedLine(A.ax.c2p(0.3, d["true_r"]), A.ax.c2p(5.7, d["true_r"]), color=GOOD, stroke_width=2)
        zero = DashedLine(A.ax.c2p(0.3, 0), A.ax.c2p(5.7, 0), color=GREY_D, stroke_width=1)
        bars_ = VGroup(*[Line(A.ax.c2p(i + 1, lo), A.ax.c2p(i + 1, hi), color=MODEL, stroke_width=8)
                         for i, (lo, hi) in enumerate(zip(d["lo"], d["hi"]))])
        names = VGroup(*[label(num(n), font_size=14, color=GREY_A).next_to(A.ax.c2p(i + 1, -0.35), DOWN, buff=0.1)
                         for i, n in enumerate(ns)])
        nlab = label(r"people", font_size=13, color=GREY_A).next_to(names, DOWN, buff=0.1)
        rows = rows_of([
            (r"a true correlation of 0.1 between a brain measure and a behaviour: \ about as large as most "
             r"brain-wide associations turn out to be", WHITE),
            (rf"with 25 people, \ samples give anything from {d['lo'][0]:.2f} to {d['hi'][0]:.2f}", AUTH),
            (rf"with 4,000, \ {d['lo'][-1]:.2f} to {d['hi'][-1]:.2f}", GOOD),
            (r"Marek and colleagues, \ 2022: \ in samples of up to tens of thousands, \ brain-wide associations "
             r"were mostly this small; \ thousands of people are needed to estimate them", YOU),
        ], 5.4, 18, 0.34).move_to([3.7, -0.1, 0])
        tag = psyche_tag(r"\texttt{neurodata.bwas}, \ 4,000 studies per size")
        tag2 = published_tag(r"Marek et al.\ (2022)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Now the question that reorganized the field. <bookmark mark='a'/> Take a true correlation of zero point "
            "one between a brain measure and a behaviour. That's about as large as most brain-wide associations turn "
            "out to be. <bookmark mark='b'/> With twenty-five people, a study can find anything from minus zero point "
            "three to nearly zero point five. <bookmark mark='c'/> With four thousand, it lands near the truth. "
            "<bookmark mark='d'/> In 2022 Scott Marek and colleagues looked at samples of up to tens of thousands. "
            "Brain-wide associations were mostly this small, and thousands of people are needed to estimate them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(zero), FadeIn(truth), FadeIn(names),
                      FadeIn(nlab))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[Create(b) for b in bars_], lag_ratio=0.3), run_time=2.0)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def reported(self):
        d = load("bwas")
        t = load("thresholds")
        head = heading(r"What gets reported")
        ns = np.asarray(d["n"])
        A = axes([0.3, 5.7], [0, 1.05], x_length=6.2, y_length=3.0, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", center=[-3.0, 0.3, 0], font_size=12)
        x = np.arange(1, 6)
        c_rep = curve(A.ax, x, d["reported"], AUTH, stroke_width=4)
        c_pow = curve(A.ax, x, d["power"], GOOD, stroke_width=4)
        truth = DashedLine(A.ax.c2p(0.3, d["true_r"]), A.ax.c2p(5.7, d["true_r"]), color=GREY_B, stroke_width=1.5)
        names = VGroup(*[label(num(n), font_size=14, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1)
                         for i, n in enumerate(ns)])
        key = VGroup(label(r"average $|r|$ among significant results", font_size=13, color=AUTH),
                     label(r"share significant (power)", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.25)
        rows = rows_of([
            (rf"with 25 people, \ {100 * d['power'][0]:.0f}\% of studies are significant, \ and those report an "
             rf"average $|r|$ of {d['reported'][0]:.2f}: \ nearly five times the truth", AUTH),
            (rf"and a significant result replicates, \ in a new sample of the same size, \ {100 * d['replicate'][0]:.0f}\% "
             rf"of the time", AUTH),
            (rf"80\% power for $r = 0.1$ needs {num(t['n_r01'])} people", GOOD),
            (r"the literature of small studies was a literature of winners' curses: \ Part 4's arithmetic, \ in the brain",
             YOU),
        ], 5.4, 18, 0.34).move_to([3.7, -0.1, 0])
        with self.voiceover(
            "And here's what gets reported. <bookmark mark='a'/> With twenty-five people, about eight percent of "
            "studies are significant, and those report an average correlation near zero point four seven: nearly five "
            "times the truth. <bookmark mark='b'/> A significant result replicates, in a new sample of the same size, "
            "about six percent of the time. <bookmark mark='c'/> Eighty percent power for a correlation of zero point "
            "one needs about seven hundred and eighty people. <bookmark mark='d'/> The literature of small studies "
            "was a literature of winners' curses: Part 4's arithmetic, in the brain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(names), FadeIn(truth), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(c_rep), Create(c_pow))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def reliability(self):
        d = load("bwas")
        head = heading(r"A noisy ruler shrinks every correlation")
        eq = MathTex(r"r_{\text{observed}} = r_{\text{true}}\sqrt{\rho_{\text{brain}}\,\rho_{\text{behaviour}}}",
                     font_size=40, color=MODEL).move_to([0, 1.7, 0])
        rows = rows_of([
            (r"Spearman's attenuation, \ from Part 3: \ the reliabilities of both measures cap the correlation", WHITE),
            (r"Elliott and colleagues, \ 2020: \ across many studies, \ the test-retest reliability of common "
             r"task-fMRI measures averaged about 0.4", AUTH),
            (rf"a true correlation of 0.2, \ with a brain measure of reliability 0.4 and a behaviour of 0.8: \ observed "
             rf"about {d['attenuated']:.2f}", PERSON),
            (r"the remedies: \ longer scans per person, \ measures chosen for reliability, \ and samples of thousands",
             GOOD),
        ], 12.4, 22, 0.42).move_to([0, -1.1, 0])
        tag = published_tag(r"Elliott et al.\ (2020)")
        with self.voiceover(
            "Small samples are half the problem. The other half is the ruler. <bookmark mark='a'/> Spearman's "
            "attenuation, from Part 3: the reliabilities of both measures cap the correlation. "
            "<bookmark mark='b'/> In 2020 Maxwell Elliott and colleagues found that the test-retest reliability of "
            "common task-fMRI measures averaged about zero point four. <bookmark mark='c'/> So a true correlation of "
            "zero point two, with a brain measure of reliability zero point four and a behaviour of zero point eight, "
            "is observed at about zero point one one. <bookmark mark='d'/> The remedies are longer scans per person, "
            "measures chosen for their reliability, and samples of thousands."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def chip(self):
        head = heading(r"Could neuroscience understand a microprocessor?")
        rows = rows_of([
            (r"2017: \ Eric Jonas and Konrad Kording took a chip whose workings are fully known, \ running three "
             r"classic video games, \ and studied it as neuroscientists study brains", WHITE),
            (r"lesions: \ removing some transistors stopped one game but not the others, \ suggesting "
             r"``game-specific'' transistors", AUTH),
            (r"tuning curves, \ correlations between parts, \ and dimensionality reduction all produced plausible "
             r"findings", AUTH),
            (r"none revealed how the chip actually computes", PERSON),
            (r"the lesson: \ methods must be tested on systems where the answer is known, \ which is what this "
             r"part's synthetic brain is for", YOU),
        ], 12.4, 22, 0.4).move_to([0, -0.3, 0])
        tag = published_tag(r"Jonas \& Kording (2017)")
        with self.voiceover(
            "One more test of the methods themselves. <bookmark mark='a'/> In 2017 Eric Jonas and Konrad Kording took "
            "a chip whose workings are fully known, running three classic video games, and studied it the way "
            "neuroscientists study brains. <bookmark mark='b'/> Lesions: removing some transistors stopped one game "
            "but not the others, as if those transistors were for that game. <bookmark mark='c'/> Tuning curves, "
            "correlations between parts, and dimensionality reduction all produced plausible findings. "
            "<bookmark mark='d'/> None revealed how the chip actually computes. <bookmark mark='e'/> The lesson: "
            "methods have to be tested on systems where the answer is known. That's what this part's synthetic brain "
            "is for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
