from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class Screens(VoiceoverScene):
    def construct(self):
        card_section(self, 10, r"Screens and well-being", r"Are phones harming teenagers?", scale=("society",))
        self.dispute()
        self.curve()
        self.experiments()

    def dispute(self):
        chips_section(self, r"A dispute, \ with each side's best case", [
            (r"harm", r"teenagers' reported depression rose in several countries from about 2012, \ when "
                      r"smartphones spread; \ heavy users report worse well-being; \ the timing and mechanisms "
                      r"(sleep, \ comparison, \ displacement) are plausible", AUTH),
            (r"little harm", r"the associations are tiny, \ similar to wearing glasses or eating potatoes in one "
                             r"analysis; \ the trends differ by country and measure; \ the direction of cause is "
                             r"unknown", GOOD),
            (r"agreement", r"both sides call for causal designs, \ better measures of use, \ and data from "
                           r"platforms", MODEL),
        ], "Are phones harming teenagers? This is a live dispute, so here is each side's best case. "
           "<bookmark mark='a'/> The case for harm: teenagers' reported depression rose in several countries from "
           "about 2012, when smartphones spread. Heavy users report worse well-being, and the timing and the "
           "mechanisms, lost sleep, social comparison and displaced activities, are plausible. <bookmark mark='b'/> "
           "The case for little harm: the associations are tiny, similar in one analysis to wearing glasses or "
           "eating potatoes. The trends differ by country and by measure, and the direction of cause is unknown. "
           "<bookmark mark='c'/> And where they agree: both sides call for causal designs, better measures of use, "
           "and data from the platforms.", chip_w=2.6, text_w=9.6, font_size=20)

    def curve(self):
        d = load("spec")
        head = heading(r"A specification curve")
        n = len(d["beta"])
        A = axes([0, n], [-0.16, 0.02], x_length=5.6, y_length=3.2, xticks=None, yticks=[-0.15, -0.1, -0.05, 0],
                 yfmt=lambda v: f"{v:g}", ylabel=r"standardized effect", center=[-3.3, 0.2, 0], font_size=12)
        sig = np.asarray(d["p"]) < 0.05
        dots = VGroup(*[Dot(A.ax.c2p(i + 0.5, float(b)), radius=0.025, color=AUTH if s else GREY_B)
                        for i, (b, s) in enumerate(zip(d["beta"], sig))])
        z = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(n, 0), color=GREY_B, stroke_width=1.5)
        xl = label(rf"{n} defensible analyses, \ sorted", font_size=13, color=GREY_A).next_to(A, DOWN, buff=0.1)
        rows = rows_of([
            (r"Psyche's survey of 10,000 teenagers; \ a small true effect, \ and confounders (sleep, \ income, \ "
             r"school) that drive both", WHITE),
            (r"288 analyses: \ three measures of use, \ three of well-being, \ sixteen sets of controls, \ two "
             r"samples", MODEL),
            (rf"every effect is negative and small; \ {100 * d['share_sig']:.0f}\% are ``significant'' because the "
             rf"sample is large", AUTH),
            (rf"screen time explains about {100 * d['median_r2']:.0f}\% of the variance in well-being: \ your fourth "
             rf"number; \ Orben and Przybylski found at most 0.4\% in real data", GOOD),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{machines.specification\_curve}")
        tag2 = published_tag(r"Orben \& Przybylski (2019)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Amy Orben and Andrew Przybylski's tool for this is the specification curve: run every defensible "
            "analysis and show them all. <bookmark mark='a'/> Psyche's survey has ten thousand teenagers, a small "
            "true effect, and confounders, sleep, income and school, that drive both screen use and well-being. "
            "<bookmark mark='b'/> There are two hundred and eighty-eight analyses: three measures of use, three of "
            "well-being, sixteen sets of controls, and two samples. <bookmark mark='c'/> Every effect is negative and "
            "small, and most are significant only because the sample is large. <bookmark mark='d'/> Screen time "
            "explains about one percent of the variance in well-being. That's your fourth number. In real data, "
            "Orben and Przybylski found at most zero point four percent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), Create(z), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.005), run_time=2.5)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def experiments(self):
        rows_section(self, r"Experiments", [
            (r"Allcott and colleagues, \ 2020: \ paid to deactivate Facebook for four weeks before an election, \ "
             r"users reported slightly higher well-being, \ and spent the time on other activities", GOOD),
            (r"other deactivation and reduction experiments: \ mixed, \ mostly small effects, \ in adults", MODEL),
            (r"experiments on adolescents at scale are rare; \ natural experiments (broadband rollouts, \ school "
             r"phone bans) are being studied", PERSON),
            (r"the honest summary: \ small average effects; \ larger harms for some people and some uses are "
             r"possible and not yet measured well", YOU),
        ], "What do experiments say? <bookmark mark='a'/> In 2020 Hunt Allcott and colleagues paid people to "
           "deactivate Facebook for four weeks before an election. They reported slightly higher well-being, and "
           "spent the time on other activities. <bookmark mark='b'/> Other deactivation and reduction experiments "
           "are mixed, with mostly small effects, in adults. <bookmark mark='c'/> Experiments on adolescents at scale "
           "are rare, and natural experiments, broadband rollouts and school phone bans, are being studied. "
           "<bookmark mark='d'/> The honest summary: small average effects, and larger harms for some people and some "
           "uses are possible, and not yet measured well.", tag=published_tag(r"Allcott et al.\ (2020)"))
