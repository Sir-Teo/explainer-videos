from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Classical(VoiceoverScene):
    def construct(self):
        self.card()
        self.sample()
        self.one_se()

    def card(self):
        card = chapter_card(2, r"What classical theory cannot do", r"Why is a score not a measurement?",
                            lit={1968: r"Lord \& Novick"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter two. What classical theory cannot do."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def sample(self):
        d = load("classical")
        head = heading(r"Difficulty depends on who answers")
        A = axes([0.5, 10.5], [0, 1], x_length=5.6, y_length=3.2, xticks=list(range(1, 11)), yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"item, \ easiest to hardest",
                 ylabel=r"proportion correct", center=[-3.3, 0.4, 0], font_size=13)
        xs = np.arange(1, 11)
        pw = VGroup(*[Dot(A.ax.c2p(x, p), radius=0.07, color=AUTH) for x, p in zip(xs, d["p_weak"])])
        ps = VGroup(*[Dot(A.ax.c2p(x, p), radius=0.07, color=GOOD) for x, p in zip(xs, d["p_strong"])])
        key = VGroup(label(r"weaker group", font_size=14, color=AUTH), label(r"stronger group", font_size=14,
                                                                             color=GOOD)).arrange(RIGHT, buff=0.5)
        key.next_to(A, UP, buff=0.1)
        rows = rows_of([
            (r"classical difficulty is the proportion who get an item right", WHITE),
            (rf"the same ten items, \ given to a weaker and a stronger group: \ item 5 is answered by "
             rf"{100 * d['p_weak'][4]:.0f}\% of one and {100 * d['p_strong'][4]:.0f}\% of the other", PERSON),
            (r"so an item's difficulty depends on the sample, \ and a person's score on the test: \ neither is a "
             r"property of the item or the person alone", AUTH),
            (r"the items' Rasch difficulties are the same in both groups: \ they were set once, \ for Psyche", MODEL),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.simulate}, \ 2{,}000 simulated people per group")
        with self.voiceover(
            "Classical test theory, from Part 3, has three blind spots. <bookmark mark='a'/> The first: an item's "
            "difficulty is the proportion who get it right. <bookmark mark='b'/> Give the same ten items to a weaker "
            "and a stronger group. The middle item is answered by about four in ten of one group, and seven in ten of "
            "the other. <bookmark mark='c'/> So an item's difficulty depends on the sample, and, as the hook showed, a "
            "person's score depends on the test. Neither belongs to the item or the person alone. "
            "<bookmark mark='d'/> Yet these items have one difficulty each, set once when Psyche made them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(p) for p in pw], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(p) for p in ps], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def one_se(self):
        d = load("classical")
        head = heading(r"One error for everyone?")
        A = axes([-3, 3], [0, 1.6], x_length=5.6, y_length=3.2, xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[0, 0.5, 1, 1.5],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"ability", ylabel=r"standard error",
                 center=[-3.3, 0.4, 0], font_size=13)
        se = curve(A.ax, d["th"], d["se_irt"], MODEL, stroke_width=4)
        flat_v = d["sem_raw"] / d["sd_raw"]
        flat = DashedLine(A.ax.c2p(-3, flat_v), A.ax.c2p(3, flat_v), color=GREY_B, stroke_width=2)
        f_l = label(r"classical: \ one number, \ in SD units", font_size=13, color=GREY_B).next_to(A.ax.c2p(-3, flat_v), UP,
                                                                                    buff=0.05, aligned_edge=LEFT)
        rows = rows_of([
            (rf"classical theory gives one standard error of measurement for everyone: \ "
             rf"$\mathrm{{SD}}\sqrt{{1 - \alpha}}$, \ here {d['sem_raw']:.1f} points with $\alpha = {d['alpha']:.2f}$", WHITE),
            (r"but a test of middling items measures middling people well and the extremes badly", MODEL),
            (r"item response theory gives a standard error for each ability, \ from the items' information "
             r"(chapter 5): \ smallest in the middle, \ growing at both ends", GOOD),
            (r"three things to fix: \ sample-free items, \ test-free scores, \ and an error for each person", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.fixed\_form\_se}, \ ten simulated items")
        with self.voiceover(
            "The third blind spot. <bookmark mark='a'/> Classical theory gives one standard error of measurement for "
            "everyone: the standard deviation times the square root of one minus reliability. <bookmark mark='b'/> "
            "But a test of middling items measures middling people well, and people at the extremes badly. "
            "<bookmark mark='c'/> Item response theory gives a standard error for each ability, from how much the "
            "items tell us there. It's smallest in the middle, and grows at both ends. <bookmark mark='d'/> So there "
            "are three things to fix: items whose difficulty doesn't depend on the sample, scores that don't depend on "
            "the test, and an error for each person."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(flat), FadeIn(f_l))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(se))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
