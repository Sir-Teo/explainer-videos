from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Effort(VoiceoverScene):
    def construct(self):
        self.card()
        self.avoid()
        self.evc_reward()
        self.evc_difficulty()
        self.why()

    def card(self):
        card = chapter_card(12, r"Effort as a cost", r"Why does thinking hard feel like something?",
                            lit={1989: r"Brehm \& Self", 2010: r"Kool et al.", 2013: r"Shenhav et al.",
                                 2018: r"Inzlicht et al."},
                            part=PART, scale=("mind", "brain"), marr=("what", "how"))
        with self.voiceover("Chapter twelve. Effort as a cost."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def avoid(self):
        head = heading(r"People avoid mental effort")
        decks = VGroup()
        for t, c in ((r"deck A: \ the task rarely switches", INTR), (r"deck B: \ the task switches often", LOST)):
            r_ = RoundedRectangle(corner_radius=0.12, width=2.4, height=1.6, color=c, fill_opacity=0.15)
            decks.add(VGroup(r_, wrapped_label(t, 2.1, 18, c).move_to(r_)))
        decks.arrange(RIGHT, buff=0.6).move_to([-3.4, 0.4, 0])
        rows = rows_of([
            (r"Kool, \ McGuire, \ Rosen and Botvinick, \ 2010: \ choose a deck, \ then do the task it gives; "
             r"\ the decks differ only in how often the task switches", WHITE),
            (r"most people drift toward the easier deck, \ without being told the difference, \ and often without "
             r"noticing it", INTR),
            (r"Westbrook, \ Kester and Braver, \ 2013: \ people will give up money to do an easier version of a "
             r"memory task; \ the price of effort can be measured, \ like a discount", WANT),
            (r"effort is a cost, \ weighed against rewards like any other", MODEL),
        ], 5.6, 22, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Kool et al.\ (2010); \ Westbrook, \ Kester \& Braver (2013)")
        with self.voiceover(
            "If self-control isn't a fuel, why does it feel like it runs out? A different answer starts from a "
            "simple observation. <bookmark mark='a'/> In 2010 Wouter Kool, Joseph McGuire, Zev Rosen and Matthew "
            "Botvinick let people choose between two decks of cards. Each card set a small task, and the decks "
            "differed only in how often the task switched. <bookmark mark='b'/> Most people drifted toward the "
            "deck with fewer switches, without being told the difference, and often without noticing it. "
            "<bookmark mark='c'/> In 2013 Andrew Westbrook, Daria Kester and Todd Braver showed that people will "
            "give up money to do an easier version of a memory task, so the price of mental effort can be measured, "
            "much like a discount rate. <bookmark mark='d'/> Effort, on this view, is a cost, weighed against "
            "rewards like any other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(decks))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def evc_reward(self):
        d = load("effort")
        head = heading(r"Derivation: \ the expected value of control")
        eqs = VGroup(
            MathTex(r"\mathrm{EVC}(u) = P(\text{success} \mid u)\, R - c\, u^2", font_size=36),
            MathTex(r"P(\text{success} \mid u) = \Phi\big(3\,(u - \text{difficulty})\big)", font_size=30),
            MathTex(r"u^* = \arg\max_{u \ge 0} \mathrm{EVC}(u)", font_size=32),
        ).arrange(DOWN, buff=0.3)
        A = axes([0, 8], [0, 1.8], x_length=5.6, y_length=3.6, xticks=[0, 2, 4, 6, 8], yticks=[0, 0.5, 1.0, 1.5],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"reward for success, \ $R$",
                 ylabel=r"control chosen, \ $u^*$", center=[-3.3, -0.2, 0], font_size=16)
        c = curve(A.ax, d["reward"], d["u"], WANT, 4)
        rows = rows_of([
            (r"Shenhav, \ Botvinick and Cohen, \ 2013: \ the brain chooses how much control to exert, \ trading "
             r"the chance of success against a cost that grows with intensity", WHITE),
            (rf"below a reward of about {d['jump']:.2f}, \ the best choice is not to try at all", LOST),
            (r"above it, \ control jumps, \ then grows slowly: \ more reward buys a little more effort", WANT),
        ], 5.6, 21, 0.3)
        right = VGroup(eqs, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{drive.evc\_curve}: \ difficulty 1, \ cost 1")
        with self.voiceover(
            "Amitai Shenhav, Botvinick and Jonathan Cohen turned that into a model in 2013, the expected value of "
            "control. <bookmark mark='a'/> The brain chooses an intensity of control, u. More control raises the "
            "chance of success; control has a cost that grows with its square. The best intensity maximizes the "
            "difference. <bookmark mark='b'/> Psyche solves it for a task of fixed difficulty, across rewards. "
            f"Below a reward of about {d['jump']:.2f}, the best choice is not to try at all. "
            "<bookmark mark='c'/> Above it, control jumps up, and then grows only slowly. More reward buys a little "
            "more effort, not a lot."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Write(eqs))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def evc_difficulty(self):
        d = load("effort")
        head = heading(r"Effort against difficulty")
        A = axes([0, 2.6], [0, 2.2], x_length=5.8, y_length=3.6, xticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5],
                 yticks=[0, 1, 2], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"difficulty",
                 ylabel=r"control chosen, \ $u^*$", center=[-3.3, -0.2, 0], font_size=16)
        cl = curve(A.ax, d["difficulty"], d["u_lo"], BODY, 4)
        ch = curve(A.ax, d["difficulty"], d["u_hi"], WANT, 4)
        key = legend([(BODY, r"reward 4"), (WANT, r"reward 8")], font_size=17).move_to(A.ax.c2p(0.45, 1.9))
        rows = rows_of([
            (r"as the task gets harder, \ control rises to meet it", WHITE),
            (rf"until success costs more than it is worth: \ then effort drops to nothing, \ at difficulty "
             rf"{d['quit_lo']:.2f} for a reward of 4, \ {d['quit_hi']:.2f} for 8", LOST),
            (r"Brehm's motivational intensity theory, \ 1989: \ effort tracks difficulty until success is "
             r"impossible or not worth it, \ then collapses", INTR),
            (r"measured in the heart's pre-ejection period and the pupil, \ effort shows this rise and fall", BODY),
        ], 5.6, 21, 0.3).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{drive.intensity}")
        with self.voiceover(
            "Now vary the difficulty instead. <bookmark mark='a'/> As the task gets harder, control rises to meet "
            "it. <bookmark mark='b'/> Until success costs more than it's worth: then effort drops to nothing, at "
            f"difficulty {d['quit_lo']:.2f} for a reward of four, and {d['quit_hi']:.2f} for a reward of eight. A "
            "larger reward keeps you trying on harder tasks, but not forever. <bookmark mark='c'/> Jack Brehm's "
            "motivational intensity theory said this in 1989, without the equation: effort follows difficulty "
            "until success is impossible or not worth it, and then collapses. <bookmark mark='d'/> Measures of "
            "effort in the body, such as how hard the heart contracts and how wide the pupils open, show this rise "
            "and fall."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cl), Create(ch), FadeIn(key), FadeIn(rows[0]), run_time=2.5)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def why(self):
        head = heading(r"Why should effort cost anything?")
        rows = rows_of([
            (r"not fuel: \ the brain uses about the same energy whether it is solving a hard problem or idling", CTRL),
            (r"opportunity cost: \ control is a limited channel, \ and using it on one thing means not using it "
             r"on another \ (Kurzban, \ Duckworth, \ Kable and Myers, \ 2013)", WANT),
            (r"the feeling of effort, \ and of boredom, \ may be the brain's estimate of what else it could be "
             r"doing", INTR),
            (r"the effort paradox: \ people also seek effort out, \ climbing mountains and doing crosswords; \ "
             r"effort can add value as well as cost \ (Inzlicht, \ Shenhav and Olivola, \ 2018)", LIKE),
        ], 12.2, 26, 0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Kurzban et al.\ (2013); \ Inzlicht, \ Shenhav \& Olivola (2018)")
        with self.voiceover(
            "But why should effort cost anything? <bookmark mark='a'/> Not because it burns fuel. The brain uses "
            "about the same energy whether it's solving a hard problem or idling. <bookmark mark='b'/> Robert "
            "Kurzban, Angela Duckworth, Joseph Kable and Justus Myers proposed in 2013 that the cost is an "
            "opportunity cost. Control is a limited channel, and using it on one task means not using it on "
            "another. <bookmark mark='c'/> On that view the feeling of effort, and the feeling of boredom, are the "
            "brain's running estimate of what else it could be doing, which explains why they grow with time on a "
            "task without anything being used up. <bookmark mark='d'/> And there is a paradox. People also seek "
            "effort out: they climb mountains, do crosswords, and value what they worked for. Michael Inzlicht, "
            "Shenhav and Christopher Olivola call it the effort paradox. Effort can add value as well as cost it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
