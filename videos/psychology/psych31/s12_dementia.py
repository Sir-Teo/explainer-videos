from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403

R_COL = [LOST, PERIOD, GOOD]


class Dementia(VoiceoverScene):
    def construct(self):
        self.card()
        self.normal()
        self.reserve()
        self.fractions()
        self.trial()
        self.neurons()

    def card(self):
        card = chapter_card(11, r"Dementia and reserve", r"What is normal ageing, \ and what can be prevented?",
                            lit={1998: r"Eriksson et al.", 2015: r"FINGER", 2024: r"Lancet Commission"},
                            part=PART, scale=("cell", "brain", "person", "society"), marr=("how",))
        with self.voiceover("Chapter eleven. Dementia and reserve."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def normal(self):
        head = heading(r"Ageing is not dementia")
        rows = rows_of([
            (r"normal ageing: \ slower, \ more trouble finding a name, \ but daily life intact", AGE),
            (r"dementia: \ a decline in memory or other thinking severe enough to disrupt independent daily life, "
             r"\ caused by disease, \ most often Alzheimer's", LOST),
            (r"in between: \ mild cognitive impairment, \ a decline beyond what age predicts, \ with daily life "
             r"still managed; \ some progress, \ some do not", PERIOD),
            (r"telling them apart is a measurement problem: \ a test score against norms for age and education, \ "
             r"and a change against the person's own past", YOU),
        ], 12.4, 25, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "First, a line that matters to every family. <bookmark mark='a'/> Normal ageing means slower thinking "
            "and more trouble finding a name, with daily life intact. <bookmark mark='b'/> Dementia is a decline in "
            "memory or other thinking severe enough to disrupt independent daily life, and it's caused by disease, "
            "most often Alzheimer's. <bookmark mark='c'/> In between is mild cognitive impairment: a decline beyond "
            "what age predicts, with daily life still managed. Some people with it progress to dementia, and some "
            "don't. <bookmark mark='d'/> Telling these apart is a measurement problem: a test score compared with "
            "norms for age and education, and a change compared with the person's own past."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def reserve(self):
        d = load("reserve")
        head = heading(r"Cognitive reserve: \ a threshold model")
        A = axes([50, 95], [-4.4, 0.6], x_length=6.4, y_length=4.4, xticks=[50, 60, 70, 80, 90], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"age", ylabel=r"cognition", center=[-2.9, -0.4, 0], font_size=16)
        cs = VGroup(*[curve(A.ax, d["age"], d[f"cog{i}"], R_COL[i], stroke_width=5) for i in range(3)])
        ons = VGroup(*[DashedLine(A.ax.c2p(d[f"onset{i}"], 0.5), A.ax.c2p(d[f"onset{i}"], -4.4), color=R_COL[i],
                                  stroke_width=2) for i in range(3)])
        key = legend([(R_COL[i], rf"reserve {r:g}") for i, r in enumerate(d["reserves"])], font_size=17)
        key.move_to(A.ax.c2p(60, -3.0))
        rows = rows_of([
            (r"pathology accumulates with age, \ the same for everyone here; \ symptoms begin when it exceeds the "
             r"person's reserve", WHITE),
            (rf"more reserve, \ later onset: \ at ages {d['onset0']:.0f}, \ {d['onset1']:.0f} and "
             rf"{d['onset2']:.0f}", GOOD),
            (r"and, \ past the threshold, \ a steeper decline to the same end: \ the disease was further along when "
             r"it showed", LOST),
            (r"reserve is inferred, \ not measured: \ education, \ work and activity are its usual proxies, \ and "
             r"each is confounded", YOU),
        ], 5.6, 21, 0.36).move_to([3.6, -0.2, 0])
        tag = psyche_tag(r"\texttt{lifespan.reserve}")
        with self.voiceover(
            "Why do two people with the same disease in the brain show it so differently? One answer, developed by "
            "Yaakov Stern, is cognitive reserve. <bookmark mark='a'/> In Psyche's version, pathology accumulates "
            "with age, the same for everyone, and symptoms begin when it exceeds the person's reserve. "
            f"<bookmark mark='b'/> More reserve means later onset: here at {d['onset0']:.0f}, {d['onset1']:.0f} and "
            f"{d['onset2']:.0f}. <bookmark mark='c'/> And past the threshold, the person with more reserve declines "
            "faster to the same end, because the disease was further along when it finally showed. "
            "<bookmark mark='d'/> Reserve is inferred, not measured. Education, work and activity are its usual "
            "proxies, and each is confounded with much else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in cs], lag_ratio=0.4), FadeIn(ons), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def fractions(self):
        d = load("reserve")
        head = heading(r"Fourteen risk factors, \ and an attributable fraction")
        eq = label(r"$\mathrm{PAF} = \dfrac{p\,(\mathrm{RR} - 1)}{1 + p\,(\mathrm{RR} - 1)}$", font_size=40)
        eq.move_to([-3.4, 1.0, 0])
        ex = label(rf"$p = 0.3, \ \mathrm{{RR}} = 1.9$: \ PAF $= {d['paf_example']:.2f}$", font_size=26, color=MODEL)
        ex.next_to(eq, DOWN, buff=0.4)
        comb = label(rf"$1 - \prod_i (1 - \mathrm{{PAF}}_i)$: \ 7, 7, 5, 5\% \ $\to$ \ "
                     rf"{100 * d['paf_combined']:.0f}\%, \ not {100 * d['paf_sum']:.0f}\%", font_size=24, color=YOU)
        comb.next_to(ex, DOWN, buff=0.4)
        rows = rows_of([
            (r"the 2024 Lancet Commission: \ 14 modifiable risk factors across life, \ from less education in "
             r"childhood to untreated vision loss late in life, \ with hearing loss, \ high blood pressure, \ "
             r"smoking, \ inactivity and high LDL cholesterol among them", WHITE),
            (r"together, \ about 45\% of dementia potentially preventable; \ untreated hearing loss and high LDL "
             r"about 7\% each", OLD),
            (r"the fraction assumes each factor is a cause, \ and that removing it removes its risk; \ for most, "
             r"\ the evidence is observational", LOST),
        ], 5.6, 21, 0.36).move_to([3.6, -0.2, 0])
        tag = published_tag(r"Livingston et al.\ (2024)")
        with self.voiceover(
            "In 2024 a Lancet Commission listed fourteen modifiable risk factors for dementia. "
            "<bookmark mark='a'/> They run across life, from less education in childhood to untreated vision loss "
            "late in life, with hearing loss, high blood pressure, smoking, inactivity and high LDL cholesterol among them. "
            "<bookmark mark='b'/> Together, it estimated, about forty-five percent of dementia is potentially "
            "preventable, with untreated hearing loss and high LDL contributing about seven percent each. "
            "<bookmark mark='c'/> Those numbers are population attributable fractions. For a factor with prevalence "
            "p and relative risk RR, the fraction is p times RR minus one, over one plus the same. A prevalence of "
            f"0.3 and a relative risk of 1.9 give {d['paf_example']:.2f}. <bookmark mark='d'/> Fractions for "
            "several factors don't add, because one case can be attributed to several; for independent factors you "
            f"multiply the complements. Seven, seven, five and five percent make {100 * d['paf_combined']:.0f}, not "
            f"{100 * d['paf_sum']:.0f}. <bookmark mark='e'/> And every fraction assumes the factor is a cause, and "
            "that removing it removes its risk. For most of these, the evidence is observational."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(eq), FadeIn(ex))
            vo.wait_until("d")
            self.play(FadeIn(comb))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def trial(self):
        head = heading(r"Testing prevention: \ FINGER")
        rows = rows_of([
            (r"Tiia Ngandu, \ Miia Kivipelto and colleagues, \ 2015: \ 1{,}260 Finns aged 60 to 77 at raised risk, "
             r"\ randomized", WHITE),
            (r"two years of diet advice, \ exercise, \ cognitive training and monitoring of heart risk, \ against "
             r"general health advice", AGE),
            (r"a battery of tests, \ in standard units: \ improved by 0.20 with the programme, \ 0.16 without: \ "
             r"a small difference, \ in the right direction", GOOD),
            (r"a randomized test of the Commission's logic: \ change several risks at once, \ and see whether "
             r"thinking changes; \ dementia itself was not the outcome", YOU),
        ], 12.4, 24, 0.4).move_to([0, -0.3, 0])
        tag = published_tag(r"Ngandu et al.\ (2015)")
        with self.voiceover(
            "Can prevention be tested? <bookmark mark='a'/> In the FINGER trial, Tiia Ngandu, Miia Kivipelto and "
            "colleagues randomized twelve hundred and sixty Finns aged sixty to seventy-seven at raised risk. "
            "<bookmark mark='b'/> Half got two years of diet advice, exercise, cognitive training and monitoring of "
            "heart risk; half got general health advice. <bookmark mark='c'/> On a battery of tests in standard "
            "units, the programme group improved by 0.20 and the control group by 0.16: a small difference, in the "
            "right direction. <bookmark mark='d'/> It's a randomized test of the Commission's logic: change several "
            "risks at once and see whether thinking changes. Dementia itself, which takes longer, wasn't the "
            "outcome."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def neurons(self):
        head = heading(r"New neurons in the adult brain?")
        rows = rows_of([
            (r"Peter Eriksson, \ Fred Gage and colleagues, \ 1998: \ five cancer patients had been given a marker "
             r"of dividing cells; \ after death, \ new neurons were found in the hippocampus", WHITE),
            (r"Shawn Sorrells and colleagues, \ 2018: \ new neurons fell steeply through childhood, \ and none were "
             r"detectable in adults", LOST),
            (r"Maura Boldrini and colleagues, \ 2018, \ and Elena Moreno-Jim\'enez and colleagues, \ 2019: \ "
             r"immature neurons in adults into their seventies and beyond", GOOD),
            (r"much of the disagreement is method: \ how quickly tissue is preserved after death, \ and which "
             r"markers count", PERIOD),
            (r"so the popular promise, \ grow new neurons and stay young, \ rests on a contested finding", YOU),
        ], 12.4, 24, 0.4).move_to([0, -0.3, 0])
        tag = published_tag(r"Eriksson et al.\ (1998); \ Sorrells et al.\ (2018); \ Boldrini et al.\ (2018)")
        with self.voiceover(
            "One last question about the ageing brain. Does it make new neurons? <bookmark mark='a'/> In 1998 Peter "
            "Eriksson, Fred Gage and colleagues studied five cancer patients who had been given a marker of dividing "
            "cells for diagnosis. After their deaths, new neurons were found in the hippocampus. "
            "<bookmark mark='b'/> In 2018 Shawn Sorrells and colleagues reported that new neurons fell steeply "
            "through childhood, and that none were detectable in adults. <bookmark mark='c'/> The same year Maura Boldrini and colleagues, "
            "and in 2019 Elena Moreno-Jimenez and colleagues, found immature neurons in adults into their seventies "
            "and beyond. <bookmark mark='d'/> Much of the disagreement is about method: how quickly the tissue was "
            "preserved after death, and which markers count. <bookmark mark='e'/> So the popular promise, grow new "
            "neurons and stay young, rests on a contested finding."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
