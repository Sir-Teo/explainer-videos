from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403

OLD = [(r"work sample", 0.54), (r"ability test", 0.51), (r"structured interview", 0.51), (r"job knowledge", 0.48),
       (r"unstructured interview", 0.38)]
NEW = [(r"structured interview", 0.42), (r"job knowledge", 0.40), (r"work sample", 0.33), (r"ability test", 0.31),
       (r"unstructured interview", 0.19)]


class Century(VoiceoverScene):
    def construct(self):
        card_section(self, 5, r"A century of evidence, \ revised", r"Which hiring methods predict, \ and how well?",
                     scale=("society",))
        self.compare()
        self.overcorrect()

    def compare(self):
        head = heading(r"1998 and 2022")
        A = axes([0, 0.62], [0.3, 5.7], x_length=4.2, y_length=3.6, xticks=[0, 0.2, 0.4, 0.6], yticks=None,
                 xfmt=lambda v: f"{v:.1f}", xlabel=r"validity", center=[-2.2, 0.4, 0], font_size=12)
        names = [r"structured interview", r"job knowledge", r"work sample", r"ability test", r"unstructured interview"]
        old = dict(OLD)
        new = dict(NEW)
        old_b, new_b, labs = VGroup(), VGroup(), VGroup()
        for i, nm in enumerate(names):
            y = 5 - i
            if nm in old:
                old_b.add(Rectangle(width=abs(A.ax.c2p(old[nm], 0)[0] - A.ax.c2p(0, 0)[0]), height=0.22, color=GREY_B,
                                    fill_opacity=0.6, stroke_width=0).move_to(A.ax.c2p(old[nm] / 2, y + 0.14)))
            new_b.add(Rectangle(width=abs(A.ax.c2p(new[nm], 0)[0] - A.ax.c2p(0, 0)[0]), height=0.22, color=MODEL,
                                fill_opacity=0.85, stroke_width=0).move_to(A.ax.c2p(new[nm] / 2, y - 0.14)))
            labs.add(label(nm, font_size=15, color=WHITE).next_to(A.ax.c2p(0, y), LEFT, buff=0.15))
        key = VGroup(label(r"Schmidt \& Hunter, \ 1998", font_size=14, color=GREY_B),
                     label(r"Sackett et al., \ 2022", font_size=14, color=MODEL)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.15)
        rows = rows_of([
            (r"1998: \ Frank Schmidt and John Hunter summarized 85 years of studies: \ ability tests and work samples "
             r"near 0.5", GREY_B),
            (r"2022: \ Paul Sackett and colleagues redid the range-restriction corrections, \ study design by study "
             r"design", MODEL),
            (r"nearly every estimate fell; \ ability tests most, \ to about 0.3; \ structured interviews now top the "
             r"list at about 0.4", PERSON),
            (r"the ranks moved less than the sizes: \ structure, \ job knowledge and samples of the work itself still "
             r"lead", YOU),
        ], 5.2, 18, 0.34).move_to([4.2, -0.2, 0])
        tag = published_tag(r"Schmidt \& Hunter (1998); \ Sackett et al.\ (2022)")
        with self.voiceover(
            "Which hiring methods predict, and how well? <bookmark mark='a'/> In 1998 Frank Schmidt and John Hunter "
            "summarized eighty-five years of studies. Ability tests and work samples came out near zero point five. "
            "<bookmark mark='b'/> In 2022 Paul Sackett and colleagues redid the range-restriction corrections, study "
            "design by study design. <bookmark mark='c'/> Nearly every estimate fell, ability tests most, to about "
            "zero point three. Structured interviews now top the list at about zero point four. "
            "<bookmark mark='d'/> The ranks moved less than the sizes. Structure, job knowledge, and samples of the "
            "work itself still lead."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(labs), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(b_) for b_ in old_b], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(b_) for b_ in new_b], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def overcorrect(self):
        d = load("overcorrect")
        rows_section(self, r"How a correction overshoots", [
            (r"the old practice: \ correct every study for range restriction with one typical ratio, \ borrowed from "
             r"other settings", WHITE),
            (r"but most validity studies are concurrent: \ the incumbents were never selected on the test being "
             r"studied, \ so their range is barely restricted", AUTH),
            (rf"Psyche: \ an unrestricted study observes {d['r_obs']:.2f}; \ the borrowed correction lifts it to "
             rf"{d['r_over']:.2f}, \ against a truth of {d['truth']:.2f}", MODEL),
            (r"a correction is a model of how the data were filtered; \ with the wrong model it adds bias rather than "
             r"removing it (Part 50's lesson, \ in hiring)", YOU),
        ], "How does a correction overshoot? <bookmark mark='a'/> The old practice corrected every study for range "
           "restriction with one typical ratio, borrowed from other settings. <bookmark mark='b'/> But most validity "
           "studies are concurrent. The incumbents were never selected on the test being studied, so their range is "
           "barely restricted. <bookmark mark='c'/> In Psyche, a study with no restriction observes zero point three "
           "nine. The borrowed correction lifts it to zero point seven eight, against a truth of zero point five. "
           "<bookmark mark='d'/> A correction is a model of how the data were filtered. With the wrong model it adds "
           "bias rather than removing it. It's Part 50's lesson, in hiring.",
           tag=psyche_tag(r"\texttt{work.case2} applied where it should not be"))
