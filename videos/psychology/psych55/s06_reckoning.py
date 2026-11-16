from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Reckoning(VoiceoverScene):
    def construct(self):
        card_section(self, 5, r"The reckoning", r"How big is the average nudge?", scale=("society",))
        self.gap()
        self.size()
        self.meta()

    def gap(self):
        d = load("gap")
        head = heading(r"Published against practice")
        A = axes([0.3, 4.7], [0, 10], x_length=5.4, y_length=3.0, xticks=None, yticks=[0, 4, 8],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"average effect (points)", center=[-3.3, 0.3, 0], font_size=12)
        vals = [8.7, 1.4, 100 * d["academic"], 100 * d["units"]]
        cols = [GREY_B, GREY_B, AUTH, GOOD]
        b = bars(A.ax, [1, 2, 3.3, 4.3], vals, cols, width=0.6)
        names = VGroup(*[label(s, font_size=12, color=GREY_A).next_to(A.ax.c2p(x, 0), DOWN, buff=0.12)
                         for s, x in zip([r"journals", r"units", r"Psyche: \ published", r"Psyche: \ all"],
                                         [1, 2, 3.3, 4.3])])
        rows = rows_of([
            (r"DellaVigna and Linos, \ 2022: \ 126 trials by two US nudge units, \ every one, \ against the "
             r"published academic literature", WHITE),
            (r"about 8.7 percentage points in journals; \ about 1.4 across the units' trials", AUTH),
            (rf"Psyche, \ one distribution of true effects (mean {100 * d['truth']:.1f}): \ small academic trials "
             rf"published when significant average {100 * d['academic']:.1f}; \ large trials, \ all reported, \ "
             rf"{100 * d['units']:.1f}", MODEL),
            (r"selection alone triples the published average; \ the rest of the real gap came from what academic "
             r"trials tested, \ and on whom", PERSON),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.publication\_gap}")
        with self.voiceover(
            "How big is the average nudge? <bookmark mark='a'/> In 2022 Stefano DellaVigna and Elizabeth Linos "
            "collected one hundred and twenty-six trials by two American nudge units, every one of them, and compared "
            "them with the published academic literature. <bookmark mark='b'/> About eight point seven percentage "
            "points in journals. About one point four across the units' trials. <bookmark mark='c'/> In Psyche, with "
            "one distribution of true effects averaging one point four, small academic trials published when "
            "significant average almost five, and large trials, all reported, average one point four. "
            "<bookmark mark='d'/> Selection alone triples the published average. The rest of the real gap came from "
            "what academic trials tested, and on whom."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]), FadeIn(b[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[2]), FadeIn(b[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def meta(self):
        rows_section(self, r"The meta-analysis, \ and its correction", [
            (r"Mertens and colleagues, \ 2022: \ a meta-analysis of over 200 choice-architecture studies, \ an "
             r"average effect of about $d$ = 0.43", WHITE),
            (r"Maier and colleagues, \ 2022: \ corrected for publication bias, \ no evidence for an overall effect "
             r"remained", AUTH),
            (r"Szaszi and colleagues: \ the evidence is heterogeneous, \ and the question ``do nudges work?'' \ has "
             r"no single answer", MODEL),
            (r"the honest summary: \ some nudges, \ defaults above all, \ work reliably; \ the average published "
             r"nudge was smaller than it looked", YOU),
        ], "Then came the meta-analysis, and its correction. <bookmark mark='a'/> In 2022 Stephanie Mertens and "
           "colleagues pooled over two hundred choice-architecture studies, and found an average effect of about zero "
           "point four three standard deviations. <bookmark mark='b'/> Maximilian Maier and colleagues corrected the "
           "same data for publication bias, and no evidence for an overall effect remained. <bookmark mark='c'/> "
           "Barnabas Szaszi and colleagues argued that the evidence is heterogeneous, and that the question do "
           "nudges work has no single answer. <bookmark mark='d'/> The honest summary: some nudges, defaults above "
           "all, work reliably. The average published nudge was smaller than it looked.",
           tag=published_tag(r"Maier et al.\ (2022)"))

    def size(self):
        head = heading(r"What it takes to see 1.4 points")
        z = 1.959964 + 0.841621
        p0 = 0.30

        def n_arm(pts):
            p1 = p0 + pts / 100
            return z ** 2 * (p0 * (1 - p0) + p1 * (1 - p1)) / (pts / 100) ** 2

        xs = np.linspace(0.5, 10, 120)
        ys = np.log10([n_arm(x) for x in xs])
        A = axes([0, 10.5], [1.5, 5.6], x_length=5.6, y_length=3.2, xticks=[1, 2, 4, 6, 8, 10],
                 yticks=[2, 3, 4, 5], xfmt=lambda v: f"{v:.0f}",
                 yfmt=lambda v: {2: "100", 3: "1{,}000", 4: "10{,}000", 5: "100{,}000"}[int(round(v))],
                 xlabel=r"true effect (percentage points)", ylabel=r"people per arm, \ 80\% power",
                 center=[-3.3, 0.3, 0], font_size=12)
        c = curve(A.ax, xs, ys, MODEL, stroke_width=4)
        n_pub, n_unit = n_arm(8.7), n_arm(1.4)
        d_pub = Dot(A.ax.c2p(8.7, np.log10(n_pub)), radius=0.08, color=GREY_B)
        d_unit = Dot(A.ax.c2p(1.4, np.log10(n_unit)), radius=0.08, color=GOOD)
        rows = rows_of([
            (r"a two-arm trial on an outcome with a 30\% base rate; \ 5\% two-sided, \ 80\% power", WHITE),
            (rf"to detect the journals' average, \ 8.7 points: \ about {n_pub:,.0f} people per arm".replace(",", "{,}"),
             GREY_B),
            (rf"to detect the units' average, \ 1.4 points: \ about {n_unit:,.0f} per arm".replace(",", "{,}"), GOOD),
            (r"the required sample grows with the square of the shrinkage: \ a typical academic study of a few hundred "
             r"could only ever see the big effects, \ and those are the ones that reached print", AUTH),
            (r"nudge units can run trials of tens of thousands because the letters, \ texts and forms are already "
             r"being sent: \ the cheapest large experiments in social science", YOU),
        ], 6.0, 18, 0.32).move_to([3.4, -0.2, 0])
        with self.voiceover(
            "Why couldn't the academic studies see effects this small? <bookmark mark='a'/> Take a two-arm trial on an "
            "outcome with a thirty percent base rate, at the usual five percent and eighty percent power. "
            "<bookmark mark='b'/> To detect the journals' average, eight point seven points, takes about four "
            "hundred and sixty people per arm. <bookmark mark='c'/> To detect the units' average, one point four "
            "points, takes about seventeen thousand. <bookmark mark='d'/> The sample grows with the square of the "
            "shrinkage. A typical academic study of a few hundred could only ever see the big effects, and those are "
            "the ones that reached print. <bookmark mark='e'/> Nudge units can run trials of tens of thousands "
            "because the letters, texts and forms are being sent anyway. They're the cheapest large experiments in "
            "social science."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(c), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(d_pub, scale=1.5))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(d_unit, scale=1.5))
            for m, r in zip("de", rows[3:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
