from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Depletion(VoiceoverScene):
    def construct(self):
        self.card()
        self.radishes()
        self.strength()
        self.funnel()
        self.pet()

    def card(self):
        card = chapter_card(8, r"Self-control as a resource", r"Does willpower run out?",
                            lit={1998: r"Baumeister et al.", 2007: r"Gailliot et al.", 2010: r"Hagger et al.",
                                 2015: r"Carter et al."},
                            part=PART, scale=("mind", "person"), marr=("what",))
        with self.voiceover("Chapter eight. Self-control as a resource."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def radishes(self):
        head = heading(r"Cookies and radishes")
        bowls = VGroup()
        for t, c in ((r"chocolate cookies", EXTR), (r"radishes", LOST)):
            b = Arc(radius=1.0, start_angle=PI, angle=PI, color=c, stroke_width=4)
            bowls.add(VGroup(b, label(t, font_size=18, color=c).next_to(b, DOWN, buff=0.15)))
        bowls.arrange(RIGHT, buff=0.8).move_to([-3.4, 0.6, 0])
        cookies = VGroup(*[Circle(radius=0.16, color=EXTR, fill_opacity=0.8).move_to(bowls[0][0].get_center()
                                                                                    + [x, 0.1, 0])
                           for x in (-0.4, 0.0, 0.4)])
        rad = VGroup(*[Circle(radius=0.13, color=LOST, fill_opacity=0.8).move_to(bowls[1][0].get_center()
                                                                                + [x, 0.08, 0])
                       for x in (-0.35, 0.0, 0.35)])
        rows = rows_of([
            (r"1998: \ hungry students sit beside a bowl of warm chocolate cookies", WHITE),
            (r"some may eat the cookies; \ others are told to eat only radishes, \ and resist", LOST),
            (r"then all get puzzles that, \ unknown to them, \ cannot be solved", WHITE),
            (r"the radish eaters give up much sooner, \ in less than half the time: \ resisting seemed to use "
             r"something up", WANT),
        ], 5.6, 22, 0.32).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Baumeister, \ Bratslavsky, \ Muraven \& Tice (1998)")
        with self.voiceover(
            "Now to self-control, and one of the most influential ideas in social psychology. "
            "<bookmark mark='a'/> In 1998 Roy Baumeister, Ellen Bratslavsky, Mark Muraven and Dianne Tice brought "
            "hungry students into a room that smelled of freshly baked chocolate cookies. <bookmark mark='b'/> Some "
            "were allowed to eat the cookies. Others were told to eat only the radishes from a second bowl, and "
            "left alone to resist. <bookmark mark='c'/> Then everyone was given puzzles that, unknown to them, had "
            "no solution, and the experimenters timed how long they kept trying. <bookmark mark='d'/> The radish "
            "eaters gave up much sooner, in less than half the time. Resisting the cookies seemed to have used "
            "something up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(bowls), FadeIn(cookies), FadeIn(rad))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(rad, color=LOST))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def strength(self):
        head = heading(r"The strength model")
        tank = RoundedRectangle(corner_radius=0.15, width=1.4, height=3.2, color=CTRL, stroke_width=3).move_to(
            [-4.6, 0.0, 0])
        fill = Rectangle(width=1.3, height=2.9, stroke_width=0, fill_color=CTRL, fill_opacity=0.6).move_to(tank)
        fill.align_to(tank, DOWN).shift(UP * 0.05)
        tl = label(r"willpower", font_size=18, color=CTRL).next_to(tank, DOWN, buff=0.2)
        rows = rows_of([
            (r"ego depletion: \ every act of self-control draws on one limited resource; \ a first act leaves less "
             r"for a second", CTRL),
            (r"hundreds of studies followed: \ Stroop tasks, \ handgrips, \ suppressed emotions, \ hard choices, "
             r"\ each depleting the next", WHITE),
            (r"2007: \ the resource was proposed to be blood glucose; \ a sugary drink seemed to restore it", EXTR),
            (r"critics: \ the brain's glucose use barely changes with mental effort; \ rinsing the mouth with sugar "
             r"seemed to work too", LOST),
            (r"2010: \ a meta-analysis of 198 tests found an average effect of about $d = 0.6$", WANT),
        ], 6.4, 22, 0.32).move_to([2.6, -0.1, 0])
        tag = published_tag(r"Baumeister et al.\ (1998); \ Gailliot et al.\ (2007); \ Kurzban (2010); \ "
                            r"Hagger et al.\ (2010)")
        with self.voiceover(
            "Baumeister's group gave the idea a name and a model. <bookmark mark='a'/> Ego depletion: every act of "
            "self-control draws on one limited resource, like a muscle that tires, so a first act leaves less for a "
            "second. <bookmark mark='b'/> Hundreds of studies followed, with many pairs of tasks: a Stroop task, "
            "then a handgrip; suppressing an emotion, then a puzzle; making hard choices, then anything at all. "
            "<bookmark mark='c'/> In 2007 Matthew Gailliot and colleagues proposed that the resource was blood "
            "glucose, since a sugary drink seemed to restore self-control. <bookmark mark='d'/> Critics such as "
            "Robert Kurzban pointed out that the brain's glucose use barely changes with mental effort, and later "
            "studies reported that merely rinsing the mouth with sugar water seemed to work too. "
            "<bookmark mark='e'/> Still, in 2010 Martin Hagger and colleagues pooled 198 tests in a meta-analysis "
            "and found an average effect of about six-tenths of a standard deviation, a medium-to-large effect, "
            "and very consistent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(tank), FadeIn(fill), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), fill.animate.stretch_to_fit_height(1.2).align_to(tank, DOWN).shift(UP * 0.05))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def funnel(self):
        d = load("literature")
        n_run = f"{int(d['k_run']):,}"
        head = heading(r"How a literature can find an effect that is not there")
        A = axes([-1.2, 2.0], [0, 0.65], x_length=5.8, y_length=3.8, xticks=[-1, 0, 1, 2], yticks=[0.2, 0.4, 0.6],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"effect found, \ $g$",
                 ylabel=r"standard error \ (smaller studies higher)", center=[-3.3, -0.2, 0], font_size=16)
        sa = scatter(A.ax, d["g_all"][::3], d["se_all"][::3], GREY_D, 0.03, 0.6)
        sp = scatter(A.ax, d["g"], d["se"], WANT, 0.035, 0.9)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, 0.65), color=GREY_B, stroke_width=2)
        se = np.linspace(0.2, 0.65, 30)
        sig = curve(A.ax, 1.96 * se, se, LOST, 2)
        sigl = label(r"$p = .05$", font_size=16, color=LOST).next_to(A.ax.c2p(1.96 * 0.62, 0.62), RIGHT, buff=0.08)
        rows = rows_of([
            (rf"Psyche's literature: \ {num(d['k_run'])} small studies \ (10 to 40 people a group) \ of an effect "
             r"that is exactly zero", MODEL),
            (r"significant results are published; \ 5\% of the rest escape the file drawer; \ 30\% of the rest are "
             r"nudged over the line by flexible analysis \ (Part 4)", LOST),
            (rf"{d['k_pub']} studies reach print, \ {pct(d['share_sig'])} of them significant", WANT),
            (rf"a meta-analysis of the published studies: \ $g = {d['re']:.2f}$ \ [{d['re_lo']:.2f}, "
             rf"{d['re_hi']:.2f}], \ precise and wrong", WANT),
        ], 5.6, 21, 0.3).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{evidence.literature}, \ \texttt{drive.random\_effects}: \ simulated")
        with self.voiceover(
            "But a consistent literature can be built from nothing, and Part 4's machinery shows how. "
            f"<bookmark mark='a'/> Psyche's literature has {n_run} small studies, ten "
            "to forty people a group, of an effect that is exactly zero. Each grey dot is a study: what it found, "
            "and how noisy it was, with the small studies higher up. <bookmark mark='b'/> Significant results are "
            "published. Five percent of the rest escape the file drawer, and thirty percent of the rest are nudged "
            "over the line by flexible analysis, the habits of Part 4. <bookmark mark='c'/> "
            f"{d['k_pub']} studies reach print, and {100 * d['share_sig']:.0f} percent of them are significant. They hug the red "
            "line, where p equals point oh five, and the small ones sit far to the right. <bookmark mark='d'/> A "
            f"meta-analysis of what was published finds an effect of {d['re']:.2f}, with a narrow interval: precise, "
            "and wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero))
            vo.wait_until("a")
            self.play(FadeIn(sa), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(sig), FadeIn(sigl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(sa.animate.set_opacity(0.15), FadeIn(sp), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def pet(self):
        d = load("literature")
        head = heading(r"Correcting for small-study bias")
        A = axes([0, 0.65], [-0.4, 2.0], x_length=5.8, y_length=3.8, xticks=[0, 0.2, 0.4, 0.6], yticks=[0, 1, 2],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"standard error",
                 ylabel=r"effect found, \ $g$", center=[-3.3, -0.2, 0], font_size=16)
        sp = scatter(A.ax, d["se"], d["g"], WANT, 0.035, 0.85)
        x = np.linspace(0, 0.65, 20)
        line = curve(A.ax, x, d["pet"] + d["pet_slope"] * x, INTR, 4)
        icpt = Dot(A.ax.c2p(0, d["pet"]), color=INTR, radius=0.09)
        eq = MathTex(r"g_i = \beta_0 + \beta_1\, \mathrm{SE}_i + \varepsilon_i, \quad w_i = 1/\mathrm{SE}_i^2",
                     font_size=32)
        rows = rows_of([
            (r"if small studies only reach print with big effects, \ effect grows with standard error", WHITE),
            (r"the precision-effect test: \ regress effect on standard error, \ and read off the intercept, \ the "
             r"effect of a study with no noise", INTR),
            (rf"here: \ intercept {d['pet']:.2f}, \ standard error {d['pet_se']:.2f}: \ nothing there", INTR),
            (r"2015: \ Carter, \ Kofler, \ Forster and McCullough applied such corrections to the depletion "
             r"literature, \ and found estimates near zero", LOST),
            (r"corrections can miss and mislead too; \ the only clean answer is a new test, \ planned in advance",
             MODEL),
        ], 5.6, 21, 0.3)
        right = VGroup(eq, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{drive.pet}: \ the published studies")
        with self.voiceover(
            "Can the bias be undone? <bookmark mark='a'/> If small studies only reach print when they find big "
            "effects, then the effects published grow with the standard error. <bookmark mark='b'/> The "
            "precision-effect test regresses each study's effect on its standard error and reads off the intercept, "
            "the effect predicted for a study with no noise at all. <bookmark mark='c'/> On Psyche's literature, "
            f"the intercept is {d['pet']:.2f}, give or take {d['pet_se']:.2f}: nothing there. "
            "<bookmark mark='d'/> In 2015 Evan Carter, Lilly Kofler, Daniel Forster and Michael McCullough applied "
            "corrections like this to the ego-depletion literature, and found estimates near zero. "
            "<bookmark mark='e'/> Corrections can mislead too; they rest on assumptions about how the bias arose. "
            "The only clean answer was a new test, planned and registered in advance, which is the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(sp), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(icpt), Indicate(icpt, color=INTR), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
