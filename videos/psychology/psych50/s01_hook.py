from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


def pile(flags, pos, cols=10, cell=0.24, gap=0.05):
    """Squares stacked from the bottom: gold for a positive trial, grey for the rest."""
    g = VGroup()
    for i, f in enumerate(flags):
        r, c = divmod(i, cols)
        sq = Square(cell, stroke_width=0, fill_color=THRESH if f else "#4A505A", fill_opacity=1)
        sq.move_to([pos[0] + (c - (cols - 1) / 2) * (cell + gap), pos[1] + r * (cell + gap), 0])
        g.add(sq)
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.turner()
        self.simulated()
        self.question()
        self.objectives()

    def turner(self):
        head = heading(r"Two piles of trials")
        rows = rows_of([
            (r"2008: \ Erick Turner and colleagues compared 74 antidepressant trials registered with the US regulator "
             r"against what the journals printed", WHITE),
            (r"by the regulator's reading, \ about half the trials were positive", PERSON),
            (r"nearly all the positive trials were published; \ most of the others were not, \ or were written up as "
             r"if positive", AUTH),
            (r"in the journals, \ almost every trial looked positive, \ and the average effect looked about a third "
             r"larger", AUTH),
            (r"the drugs were not useless; \ the literature was filtered", YOU),
        ], 12.4, 23, 0.42).move_to([0, -0.4, 0])
        tag = published_tag(r"Turner et al.\ (2008)")
        with self.voiceover(
            "In 2008 Erick Turner and colleagues put two piles side by side. <bookmark mark='a'/> In one, the "
            "seventy-four antidepressant trials registered with the US regulator. In the other, what the journals "
            "printed. <bookmark mark='b'/> By the regulator's reading, about half the trials were positive. "
            "<bookmark mark='c'/> Nearly all of those were published. Most of the others were not published at all, "
            "or were written up as if they were positive. <bookmark mark='d'/> So in the journals, almost every trial "
            "looked positive, and the average effect looked about a third larger than it was. <bookmark mark='e'/> "
            "The drugs weren't useless. The literature was filtered."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def simulated(self):
        d = load("piles")
        head = heading(r"The filter, \ simulated")
        sig = np.asarray(d["sig"], bool)
        pub = np.asarray(d["pub"], bool)
        order = np.argsort(~sig)
        left = pile(sig[order], [-3.6, -2.2])
        right = pile(sig[pub][np.argsort(~sig[pub])], [3.6, -2.2])
        ll = label(rf"all {d['k']} registered trials: \ {d['k_sig']} positive", font_size=20, color=WHITE)
        ll.next_to(left, UP, buff=0.3)
        rl = label(rf"the {d['k_pub']} published: \ {d['k_pub_sig']} positive", font_size=20, color=WHITE)
        rl.next_to(right, UP, buff=0.3)
        rows = rows_of([
            (rf"Psyche: \ 74 trials of a drug with a real, \ modest effect (d = 0.3); \ every positive trial is "
             rf"published, \ about a third of the others", WHITE),
            (rf"pool all 74 and the effect comes out at {d['all_mu']:.2f}; \ pool the published {d['k_pub']}, \ "
             rf"{d['pub_mu']:.2f}", AUTH),
        ], 12.4, 20, 0.26).move_to([0, 2.1, 0])
        tag = psyche_tag(r"\texttt{meta.literature}, \ \texttt{random\_effects}")
        with self.voiceover(
            "Psyche can build the same two piles. <bookmark mark='a'/> Seventy-four trials of a drug with a real, "
            "modest effect. Every positive trial is published, and about a third of the others. "
            "<bookmark mark='b'/> On the left, all seventy-four, about half of them positive. On the right, the "
            "fifty-one that were published, three in four of them positive. <bookmark mark='c'/> Pool all the trials, "
            "and the effect comes out at about zero point three one. Pool only the published ones, and it's about "
            "zero point three seven. Nothing was faked. The filter alone did it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(ll), LaggedStart(*[FadeIn(s) for s in left], lag_ratio=0.01), run_time=1.5)
            self.play(FadeIn(rl), LaggedStart(*[FadeIn(s) for s in right], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ what does a whole literature say, \ and can it be trusted to say it?")
        rows = rows_of([
            (r"combining studies, \ and the moderators they hide", SYMP),
            (r"seeing the filter, \ and correcting for it", MODEL),
            (r"designs that remove it, \ and forensics that catch the impossible", PERSON),
            (r"many analysts, \ weak theories, \ and the Ledger audited by its own tools", GOOD),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks what a whole literature says, and whether it can be trusted to say it. "
            "<bookmark mark='a'/> Combining studies, and the moderators they hide. <bookmark mark='b'/> Seeing the "
            "filter, and correcting for it. <bookmark mark='c'/> Designs that remove the filter, and forensics that "
            "catch numbers that can't be. <bookmark mark='d'/> Many analysts, weak theories, and the series' own "
            "Ledger, audited with its own tools."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 50", font_size=34, color=GREY_B), label(r"The Weight of Evidence", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"fixed and random effects, \ heterogeneity and prediction intervals",
            r"meta-regression, \ and why moderators hide",
            r"funnels, \ Egger, \ PET-PEESE, \ trim-and-fill, \ selection models, \ p-curve",
            r"registered reports, \ and what they remove",
            r"GRIM, \ SPRITE and statcheck; \ fabrication detected",
            r"specification curves, \ Meehl's paradox, \ and the Ledger audited",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 50 of Psychology, Built: the weight of evidence. <bookmark mark='a'/> We'll combine studies "
            "by fixed and random effects, and draw prediction intervals. We'll see why moderators hide. We'll read "
            "funnel plots, and run every correction method on literatures where the truth is known. We'll see what "
            "registered reports remove. We'll test reported numbers with GRIM, SPRITE and statcheck, and see how "
            "fabricated data were caught. And we'll draw a specification curve, meet Meehl's paradox, and audit the "
            "Ledger with its own tools."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
