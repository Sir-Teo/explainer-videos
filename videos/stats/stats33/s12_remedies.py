from __future__ import annotations

from videos.stats.stats33.common import *  # noqa: F403


class Remedies(VoiceoverScene):
    def construct(self):
        self.card()
        self.prereg()
        self.registered()
        self.alpha005()
        self.bayes()
        self.abandon()
        self.asa()
        self.position()

    def card(self):
        card = chapter_card(11, r"Remedies argued", r"What should change, \ and who disagrees", lit=(2016,), part=PART)
        with self.voiceover("Chapter eleven. Remedies, argued."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def prereg(self):
        rows = fit_rows(VGroup(
            label(r"preregistration: \ hypotheses, \ outcomes, \ sample size and analysis, \ fixed in advance", font_size=26, color=BHC),
            label(r"clinical trials: \ required since 2005 \ (ICMJE; \ ClinicalTrials.gov)", font_size=26),
            label(r"Kaplan \& Irvin (2015): \ NHLBI trials with a positive primary outcome fell from 57\% to 8\% after 2000", font_size=26, color=SIGC),
            label(r"it closes the garden of forking paths; \ exploratory analysis stays allowed, \ labelled", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The first remedy is preregistration: write down the hypotheses, outcomes, sample size and "
            "analysis plan before collecting the data. <bookmark mark='b'/> Clinical trials have been required to register "
            "since 2005. <bookmark mark='c'/> Robert Kaplan and Veronica Irvin found that among large trials funded by the US "
            "heart, lung and blood institute, the share reporting a benefit on the primary outcome fell from fifty-seven "
            "percent before registration became mandatory in 2000 to eight percent after. <bookmark mark='d'/> Registration "
            "closes the garden of forking paths; exploratory analysis remains allowed, as long as it is labelled as such."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def registered(self):
        rows = fit_rows(VGroup(
            label(r"registered reports \ (Chambers 2013): \ peer review before the results exist", font_size=26, color=BHC),
            label(r"the journal commits to publish whatever the outcome", font_size=26),
            label(r"Scheel et al. (2021): \ 44\% positive results, \ against 96\% in the standard literature", font_size=26, color=SIGC),
            label(r"publication bias removed by design", font_size=26, color=TRUEC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Registered reports, championed by Chris Chambers from 2013, go further: the study is peer "
            "reviewed on its question and methods before any results exist, <bookmark mark='b'/> and the journal commits to "
            "publishing it whatever the outcome. <bookmark mark='c'/> Anne Scheel and colleagues found that forty-four "
            "percent of registered reports in psychology supported their first hypothesis, against ninety-six percent of "
            "comparable standard papers. <bookmark mark='d'/> The file drawer is removed by design."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def alpha005(self):
        rows = [
            cmath(r"\text{proposal}", r":", r"\text{call } p < 0.005 \text{ `significant', \ } p < 0.05 \text{ `suggestive'}", font_size=28),
            cmath(r"p = 0.05", r"\approx", r"\text{Bayes factor of only } 2.5\text{--}3.4 \text{ at best}", font_size=30),
            cmath(r"\text{PPV}", r"\uparrow", r"\text{fewer false positives for the same priors}", font_size=30),
            cmath(r"\text{objections}", r":", r"\text{larger samples, \ the same dichotomy, \ hacking at a new line}", font_size=28),
        ]
        rows[0][-1].set_color(BHC)
        whys = [why(r"Benjamin et al. (2018), \ 72 authors"), why(r"Part 26's bounds"), why(r"chapter nine's formula"),
                why(r"Lakens et al. (2018): \ `justify your alpha'")]
        with self.voiceover(
            "<bookmark mark='a'/> In 2018 seventy-two researchers, led by Daniel Benjamin, proposed redefining statistical "
            "significance: call p below point oh oh five significant, and between that and point oh five merely suggestive. "
            "<bookmark mark='b'/> Their argument: a p-value of point oh five corresponds at best to a Bayes factor of about "
            "two and a half to three and a half, weak evidence, by the bounds of Part 26. <bookmark mark='c'/> A stricter "
            "line raises the positive predictive value. <bookmark mark='d'/> Eighty-eight others, led by Daniël Lakens, "
            "replied: justify your alpha instead. A new line needs larger samples, keeps the false dichotomy, and invites "
            "hacking just below it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def abandon(self):
        rows = fit_rows(VGroup(
            label(r"McShane, \ Gal, \ Gelman, \ Robert \& Tackett (2019): \ abandon statistical significance", font_size=26),
            label(r"Amrhein, \ Greenland \& McShane in \emph{Nature} (2019), \ with 800 signatories", font_size=26, color=SIGC),
            label(r"report estimates and intervals; \ treat $p$ as continuous; \ no bright lines", font_size=26, color=BHC),
            label(r"critics: \ decisions are binary anyway; \ thresholds discipline the hopeful", font_size=26, color=FALSEC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Others want no line at all. Blakeley McShane, Andrew Gelman and colleagues argued in 2019 "
            "for abandoning statistical significance, <bookmark mark='b'/> and Valentin Amrhein, Sander Greenland and "
            "McShane's comment in Nature gathered eight hundred signatures. <bookmark mark='c'/> Report estimates with "
            "intervals, treat the p-value as one continuous measure among others, and draw no bright lines. "
            "<bookmark mark='d'/> Critics answer that many decisions are binary whatever we call them, and that a threshold "
            "fixed in advance disciplines the hopeful. The debate is not settled."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def asa(self):
        rows = fit_rows(VGroup(
            label(r"the ASA statement (Wasserstein \& Lazar 2016): \ six principles", font_size=26, color=BHC),
            label(r"a $p$-value is not the probability the hypothesis is true", font_size=24),
            label(r"scientific conclusions should not rest on $p$ passing a threshold", font_size=24),
            label(r"proper inference requires full reporting and transparency", font_size=24),
            label(r"$p$ does not measure the size or importance of an effect", font_size=24),
            label(r"by itself, \ $p$ is not a good measure of evidence", font_size=24, color=SIGC),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The American Statistical Association weighed in, for the first time in its history, with a "
            "statement on p-values in 2016, already met in Part 10. <bookmark mark='b'/> Among its six principles: a "
            "p-value is not the probability that the hypothesis is true; <bookmark mark='c'/> conclusions should not rest "
            "only on whether it passes a threshold; <bookmark mark='d'/> proper inference requires full reporting; "
            "<bookmark mark='e'/> the p-value does not measure the size of an effect; <bookmark mark='f'/> and by itself it "
            "is not a good measure of evidence."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def position(self):
        rows = fit_rows(VGroup(
            label(r"this course's position", font_size=28),
            label(r"count your questions, \ including the analyses you did not report", font_size=26, color=BHC),
            label(r"control an error rate that matches the use: \ FWER to confirm, \ FDR to discover", font_size=26, color=SIGC),
            label(r"report estimates with honest intervals, \ and register what you can", font_size=26, color=TRUEC),
            label(r"evidence you can check at every look: \ e-values, \ Part 58", font_size=26, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> This course's position, for what it is worth. <bookmark mark='b'/> Count your questions, "
            "including the analyses you tried and did not report. <bookmark mark='c'/> Control an error rate that matches "
            "the use: family-wise to confirm, false discovery to discover. <bookmark mark='d'/> Report estimates with honest "
            "intervals, and register what you can. <bookmark mark='e'/> And for evidence that stays valid however often you "
            "look, Part 58 builds e-values."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def bayes(self):
        rows = [
            cmath(r"\text{Bayes factor}", r":", r"\text{evidence, \ graded, \ for both hypotheses}", font_size=30),
            cmath(r"\text{estimation}", r":", r"\text{effect sizes with intervals; \ plan for precision}", font_size=30),
            cmath(r"\text{equivalence tests}", r":", r"\text{show an effect is negligibly small}", font_size=30),
            cmath(r"\text{all need}", r":", r"\text{the same honesty about forking paths}", font_size=30),
        ]
        rows[1][-1].set_color(BHC)
        whys = [why(r"Part 26"), why(r"Cumming (2014): \ the new statistics"), why(r"Schuirmann (1987); \ Lakens (2017)"), why(r"no method fixes selection")]
        with self.voiceover(
            "<bookmark mark='a'/> Other proposals replace the p-value's role. Bayes factors grade the evidence for "
            "both hypotheses, as in Part 26. <bookmark mark='b'/> Estimation-based reporting, Geoff Cumming's new "
            "statistics, puts effect sizes and their intervals first, and plans studies for precision rather than "
            "significance. <bookmark mark='c'/> Equivalence tests can show that an effect is too small to matter, "
            "something a non-significant p-value cannot. <bookmark mark='d'/> But every one of these needs the same "
            "honesty about the forking paths: no statistic is immune to selective reporting."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
