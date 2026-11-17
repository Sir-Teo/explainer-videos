from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403


class Bias(VoiceoverScene):
    def construct(self):
        self.card()
        self.turner()
        self.filtered()
        self.eysenck_again()

    def card(self):
        card = chapter_card(7, r"How big is it really?", r"What did the unpublished trials find?",
                            lit={2008: r"Turner et al.", 2015: r"Driessen et al.", 2019: r"Cuijpers et al."},
                            part=PART, scale=("person", "society"), marr=("what",))
        with self.voiceover("Chapter seven. How big is it really?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def turner(self):
        head = heading(r"Two piles of trials")
        A = axes([0.3, 2.7], [0, 100], x_length=4.6, y_length=3.0, xticks=None, yticks=[0, 50, 100],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"positive", center=[-3.6, 0.5, 0], font_size=13)
        b = bars(A.ax, [1, 2], [51, 94], [GREY_B, AUTH], width=0.6)
        names = VGroup(wrapped_label(r"at the regulator", 1.8, 13, GREY_B).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15),
                       wrapped_label(r"in the journals", 1.8, 13, AUTH).next_to(A.ax.c2p(2, 0), DOWN, buff=0.15))
        rows = rows_of([
            (r"Turner and colleagues, \ 2008: \ the 74 trials of twelve antidepressants registered with the US "
             r"regulator", WHITE),
            (r"by the regulator's own reading, \ about half were positive; \ in the journals, \ 94\% appeared "
             r"positive", AUTH),
            (r"negative trials went unpublished, \ or were published as if positive; \ the apparent effect grew by "
             r"about a third", PERSON),
            (r"Part 4's file drawer, \ in an industry; \ and the same question applies to psychotherapy", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Turner et al.\ (2008)")
        with self.voiceover(
            "How big is the effect really? Drug trials show the problem most clearly. <bookmark mark='a'/> In 2008 "
            "Erick Turner and colleagues compared the seventy-four trials of twelve antidepressants registered with "
            "the American regulator against what was published. <bookmark mark='b'/> By the regulator's own reading, "
            "about half were positive. In the journals, ninety-four percent appeared positive. "
            "<bookmark mark='c'/> Negative trials went unpublished, or were written up as if they were positive, and "
            "the apparent effect grew by about a third. <bookmark mark='d'/> It's Part 4's file drawer, in an "
            "industry. And the same question applies to psychotherapy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def filtered(self):
        d = load("bias")
        head = heading(r"A filtered literature, \ computed")
        A = axes([-0.8, 1.6], [0, 0.55], x_length=5.4, y_length=3.6, xticks=[-0.5, 0, 0.5, 1, 1.5],
                 yticks=[0, 0.2, 0.4], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.1f}", xlabel=r"effect $d$",
                 ylabel=r"standard error", center=[-3.3, 0.3, 0], font_size=13)
        se = np.sqrt(d["v"])
        pub = np.asarray(d["published"]) > 0
        hidden = scatter(A.ax, d["d"][~pub], se[~pub], GREY_D, radius=0.035)
        shown = scatter(A.ax, d["d"][pub], se[pub], PERSON, radius=0.04)
        truth = DashedLine(A.ax.c2p(0.3, 0), A.ax.c2p(0.3, 0.55), color=GOOD, stroke_width=2)
        sig = curve(A.ax, 1.96 * np.linspace(0.05, 0.55, 50), np.linspace(0.05, 0.55, 50), AUTH, stroke_width=2)
        rows = rows_of([
            (r"Psyche: \ 400 trials of a therapy whose true effect is 0.3, \ small and large", WHITE),
            (rf"significant ones are published, \ and a fifth of the rest: \ {d['n_pub']} appear, \ "
             rf"{pct(d['share_sig_pub'])} of them significant", PERSON),
            (rf"a random-effects meta-analysis of the published trials finds {d['mu_pub']:.2f}; \ of all of them, \ "
             rf"{d['mu_all']:.2f}", AUTH),
            (r"the missing trials are the small, \ unlucky ones: \ the gap in the funnel (Part 50's tools)", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.publication\_filter}, \ \texttt{random\_effects}")
        with self.voiceover(
            "Psyche shows what a filter does. <bookmark mark='a'/> Four hundred trials of a therapy whose true effect "
            "is zero point three, some small and some large. <bookmark mark='b'/> The significant ones are published, "
            "and a fifth of the rest. <bookmark mark='c'/> A random-effects meta-analysis of the published trials "
            "finds an effect near zero point four three. Of all of them, close to the truth. "
            "<bookmark mark='d'/> The missing trials are the small, unlucky ones, which leaves a gap in the funnel. "
            "Part 50 builds the tools that see it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(truth))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(hidden), FadeIn(shown))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeOut(hidden), Create(sig))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(hidden))
        self.clear_scene()

    def eysenck_again(self):
        head = heading(r"Was Eysenck right after all?")
        rows = rows_of([
            (r"Driessen and colleagues, \ 2015: \ of the psychotherapy trials for depression funded by the US "
             r"National Institutes of Health, \ about a quarter were never published; \ adding them shrank the effect",
             PERSON),
            (r"Cuijpers and colleagues, \ 2019: \ all trials of therapy for adult depression average near $g = 0.7$; "
             r"\ restricted to trials at low risk of bias, \ without waiting lists, \ and adjusted for bias, \ the "
             r"effect is considerably smaller", AUTH),
            (r"their answer to their own title: \ no, \ therapy works; \ but the effect is smaller than the literature "
             r"suggests", GOOD),
            (r"the Ledger: \ therapy against no treatment, \ replicated; \ the published size, \ replicated, \ "
             r"smaller", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        tag = published_tag(r"Driessen et al.\ (2015); \ Cuijpers et al.\ (2019)")
        with self.voiceover(
            "And for psychotherapy? <bookmark mark='a'/> In 2015 Ellen Driessen and colleagues tracked the "
            "psychotherapy trials for depression funded by the American National Institutes of Health. About a "
            "quarter had never been published, and adding them shrank the effect. <bookmark mark='b'/> In 2019 Pim "
            "Cuijpers and colleagues asked, in the title of their paper, whether Eysenck was right after all. All "
            "trials of therapy for adult depression averaged near zero point seven. Restricted to trials at low risk "
            "of bias, without waiting lists, and adjusted for publication bias, the effect was considerably smaller. "
            "<bookmark mark='c'/> Their answer to their own question: no. Therapy works. But the effect is smaller "
            "than the literature suggests. <bookmark mark='d'/> The Ledger: therapy against no treatment, replicated. "
            "The published size, replicated, and smaller."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
