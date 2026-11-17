from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Marshmallow(VoiceoverScene):
    def construct(self):
        self.card()
        self.test()
        self.confound()
        self.reliable()
        self.waiting()

    def card(self):
        card = chapter_card(10, r"The marshmallow test", r"Does a four-year-old's patience predict a life?",
                            lit={1972: r"Mischel et al.", 1990: r"Shoda et al.", 2013: r"Kidd et al.",
                                 2018: r"Watts et al."},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter ten. The marshmallow test."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def test(self):
        head = heading(r"One now, \ or two later")
        table = Line([-5.6, -0.6, 0], [-1.4, -0.6, 0], color=GREY_B, stroke_width=4)
        m1 = RoundedRectangle(corner_radius=0.08, width=0.45, height=0.38, color=WHITE, fill_opacity=0.9).move_to(
            [-4.2, -0.4, 0])
        m2 = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.45, height=0.38, color=WHITE,
                                       fill_opacity=0.9).move_to([x, -0.4, 0]) for x in (-2.9, -2.35)])
        l1 = label(r"now", font_size=18, color=EXTR).next_to(m1, DOWN, buff=0.35)
        l2 = label(r"if you wait", font_size=18, color=INTR).next_to(m2, DOWN, buff=0.35)
        bell = label(r"ring the bell to end the wait", font_size=18, color=GREY_B).move_to([-3.5, 1.4, 0])
        rows = rows_of([
            (r"late 1960s, \ Stanford's nursery school: \ Walter Mischel's children choose a small treat now or a "
             r"bigger one when the experimenter returns", WHITE),
            (r"the studies were about how children wait: \ covering the treat, \ thinking of it as a cloud, \ "
             r"singing, \ all lengthened the wait", INTR),
            (r"follow-ups years later: \ the children who had waited longer had higher test scores and were rated "
             r"more competent as adolescents", WANT),
            (r"those follow-ups had a few dozen children each, \ from one university's families", LOST),
        ], 5.6, 22, 0.32).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Mischel, \ Ebbesen \& Zeiss (1972); \ Shoda, \ Mischel \& Peake (1990)")
        with self.voiceover(
            "The most famous test of self-control was given to four-year-olds. <bookmark mark='a'/> In the late "
            "1960s and early 1970s, at the nursery school on Stanford's campus, Walter Mischel and his colleagues "
            "offered children a choice: one treat now, a marshmallow or a pretzel, or two if they could wait until "
            "the experimenter came back. Ringing a bell ended the wait. <bookmark mark='b'/> The studies were about "
            "how children manage to wait. Covering the treat helped; so did thinking of the marshmallow as a "
            "puffy cloud, or singing to oneself. <bookmark mark='c'/> Years later, follow-ups found that the children "
            "who had waited longer had higher test scores and were rated by their parents as more competent "
            "adolescents. That became the famous claim: a preschooler's patience predicts a life. "
            "<bookmark mark='d'/> But each follow-up had a few dozen children, all from the families of one "
            "university."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(table), FadeIn(m1), FadeIn(m2), FadeIn(l1), FadeIn(l2),
                      FadeIn(bell))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def confound(self):
        d = load("confound")
        head = heading(r"Derivation: \ what controls take away")
        g = VGroup()
        nodes = {"B": ([-3.1, 1.4, 0], r"family background", BODY), "A": ([-3.1, -1.8, 0], r"early ability", BODY),
                 "W": ([-5.0, -0.2, 0], r"waiting at 4", CTRL), "Y": ([-1.2, -0.2, 0], r"scores at 15", WANT)}
        pos = {}
        for k, (p, t, c) in nodes.items():
            box = RoundedRectangle(corner_radius=0.12, width=1.9, height=0.7, color=c, fill_opacity=0.12).move_to(p)
            g.add(VGroup(box, label(t, font_size=17, color=c).move_to(box)))
            pos[k] = box
        def arr(a, b, col=GREY_B, w=3):
            return Arrow(pos[a].get_center(), pos[b].get_center(), buff=0.5, color=col, stroke_width=w,
                         max_tip_length_to_length_ratio=0.15)
        arrows = VGroup(arr("B", "W"), arr("A", "W"), arr("B", "Y", BODY, 4), arr("A", "Y", BODY, 4),
                        arr("W", "Y", CTRL, 2))
        eq = MathTex(r"\hat\beta_{\text{alone}} = \beta_W + \underbrace{\beta_B \gamma_B + \beta_A \gamma_A}"
                     r"_{\text{through the background}}", font_size=30)
        rows = rows_of([
            (r"Psyche's Pool: \ background and early ability shape both how long a child waits and later "
             r"scores; \ waiting itself adds a little", MODEL),
            (rf"waiting alone predicts the scores: \ $r = {d['r']:.2f}$", WANT),
            (rf"with background and ability controlled, \ the slope falls from {d['alone']:.2f} to "
             rf"{d['controlled']:.2f}: \ {pct(d['shrink'])} smaller, \ and now right", CTRL),
            (r"Watts, \ Duncan and Quan, \ 2018: \ about 900 children from many backgrounds; \ the association was "
             r"about half the original size, \ and two-thirds smaller again with background controlled", LOST),
        ], 5.6, 21, 0.3)
        right = VGroup(eq, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.5, -0.1, 0])
        tag = simulated_tag(r"simulated: \ \texttt{drive.confounded\_delay}, \ 20{,}000 children")
        with self.voiceover(
            "Why might a small, privileged sample mislead? Draw what else could be going on. "
            "<bookmark mark='a'/> In this simulated pool, family background and early ability shape both how long "
            "a child waits at four and how well the child scores at fifteen. Waiting itself adds only a little. "
            f"<bookmark mark='b'/> Waiting alone predicts the scores, with a correlation of {d['r']:.2f}. The "
            "regression slope on waiting alone is the true effect plus everything that flows through the "
            "background. <bookmark mark='c'/> Control for background and ability, and the slope falls from "
            f"{d['alone']:.2f} to {d['controlled']:.2f}, {100 * d['shrink']:.0f} percent smaller, which here is the truth. "
            "<bookmark mark='d'/> In 2018 Tyler Watts, Greg Duncan and Haonan Quan repeated the follow-up in about "
            "nine hundred children from many backgrounds. The association was about half the size of the "
            "original, and shrank by about two-thirds more once family background and early ability were "
            "controlled. Those numbers aren't the simulation's; the simulation only shows how that can happen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(g), FadeIn(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), arrows[2].animate.set_opacity(0.25), arrows[3].animate.set_opacity(0.25))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def reliable(self):
        head = heading(r"Waiting is a bet on the world")
        rows = rows_of([
            (r"Kidd, \ Palmeri and Aslin, \ 2013: \ before the marshmallow, \ the experimenter promises children "
             r"better art supplies, \ and either brings them or comes back saying there are none", WHITE),
            (r"children who had met a reliable adult waited about four times as long as those who had met an "
             r"unreliable one", INTR),
            (r"a child who expects the promise to be broken is not failing at self-control; \ they are reading "
             r"their world", WANT),
            (r"which raises the question: \ when is giving up the rational thing to do?", MODEL),
        ], 12.2, 27, 0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Kidd, \ Palmeri \& Aslin (2013)")
        with self.voiceover(
            "There is a second reason to doubt that waiting measures a trait. <bookmark mark='a'/> In 2013 Celeste "
            "Kidd, Holly Palmeri and Richard Aslin added a step before the marshmallow. The experimenter promised "
            "the children better art supplies, and then either brought them, or came back empty-handed with an "
            "apology. <bookmark mark='b'/> Children who had just met a reliable adult waited for the second "
            "marshmallow about four times as long as children who had met an unreliable one. "
            "<bookmark mark='c'/> A child who expects promises to be broken is not failing at self-control. "
            "They're reading their world correctly. <bookmark mark='d'/> Which raises a sharper question: when is "
            "giving up the rational thing to do?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def waiting(self):
        d = load("waiting")
        head = heading(r"Derivation: \ when to stop waiting")
        A = axes([0, 20], [0, 110], x_length=5.6, y_length=3.6, xticks=[0, 5, 10, 15, 20], yticks=[0, 25, 50, 75, 100],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"minutes waited so far",
                 ylabel=r"expected further wait, \ minutes", center=[-3.3, -0.2, 0], font_size=16)
        cn = curve(A.ax, d["t"], d["normal_wait"], INTR, 4)
        cp = curve(A.ax, d["t"], d["pareto_wait"], LOST, 4)
        key = legend([(INTR, r"a reliable return \ (normal)"), (LOST, r"an unreliable one \ (heavy tail)")],
                     font_size=17).move_to(A.ax.c2p(13.5, 25))
        eq = MathTex(r"\mathbb{E}[T - t \mid T > t] = \frac{\int_t^\infty S(u)\,du}{S(t)}", font_size=34)
        rows = rows_of([
            (r"both return times have a median of 5 minutes; \ only their tails differ", WHITE),
            (rf"reliable: \ the longer you have waited, \ the sooner the end: \ {d['normal_at5']:.1f} more minutes "
             r"at minute 5", INTR),
            (rf"unreliable: \ the longer you have waited, \ the longer still to go: \ {d['pareto_at5']:.0f} more "
             rf"minutes at minute 5, \ {d['pareto_at10']:.0f} at minute 10", LOST),
            (rf"maximizing treats per minute: \ wait it out when the return is reliable; \ give up after about "
             rf"{d['pareto_best']:.1f} minutes when it is not \ (McGuire and Kable, \ 2013)", WANT),
        ], 5.6, 21, 0.3)
        right = VGroup(eq, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{drive.remaining\_wait}, \ \texttt{give\_up\_time}")
        with self.voiceover(
            "Joseph McGuire and Joseph Kable gave the answer in 2013, and it can be derived. "
            "<bookmark mark='a'/> Having waited t minutes, the expected further wait is the area under the "
            "survival curve beyond t, divided by the chance of having got this far. Compare two worlds where the "
            "experimenter's return has the same median, five minutes, and only the tails differ. "
            "<bookmark mark='b'/> If returns are reliable, the longer you've waited, the sooner the end: at five "
            f"minutes, about {d['normal_at5']:.1f} more. <bookmark mark='c'/> If they're unreliable, with a heavy "
            "tail, the longer you've waited, the longer you should expect still to wait: about "
            f"{d['pareto_at5']:.0f} more minutes at minute five, {d['pareto_at10']:.0f} at minute ten. Each minute "
            "without a return is evidence that this is one of the long ones. <bookmark mark='d'/> A chooser who "
            "maximizes treats per minute should wait it out in the first world, and give up after about "
            f"{d['pareto_best']:.1f} minutes in the second. McGuire and Kable showed that adults adjust their "
            "persistence to exactly this kind of difference. Giving up can be intelligence, not weakness."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cn), FadeIn(key[0]), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(cp), FadeIn(key[1]), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
