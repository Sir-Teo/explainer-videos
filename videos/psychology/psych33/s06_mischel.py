from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403

COMP_COL = [PERSON, SITUATION, O_, GREY_B]
COMP_NAME = [r"the person's trait", r"the situation's pull", r"the person's own if-then signature",
             r"noise on the occasion"]


class Mischel(VoiceoverScene):
    def construct(self):
        self.card()
        self.deceit()
        self.coefficient()
        self.world()

    def card(self):
        card = chapter_card(5, r"The person and the situation", r"Does a trait predict what someone will do?",
                            lit={1928: r"Hartshorne \& May", 1968: r"Mischel"}, part=PART, scale=("person", "group"),
                            marr=("what",))
        with self.voiceover("Chapter five. The person and the situation."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def deceit(self):
        head = heading(r"Studies in Deceit, \ 1928")
        chips = VGroup(*[word_chip(w, color=LOST, font_size=22, width=2.0) for w in
                         (r"copying", r"stealing", r"lying", r"faking", r"peeping")]).arrange(RIGHT, buff=0.2)
        chips.move_to([0, 1.8, 0])
        rows = rows_of([
            (r"Hugh Hartshorne and Mark May, \ the Character Education Inquiry at Teachers College, \ Columbia: \ "
             r"schoolchildren were given chances to cheat that they thought nobody could detect", WHITE),
            (r"a child who cheated on one test tended to cheat when the same test was repeated", PERSON),
            (r"but cheating on one kind of test predicted cheating on a different kind only weakly; \ the more "
             r"different the situations, \ the weaker the link", SITUATION),
            (r"their conclusion: \ honesty is specific to situations, \ not a general trait; \ later reanalyses "
             r"found more generality than they claimed", YOU),
        ], 12.4, 22, 0.36).move_to([0, -0.9, 0])
        tag = historical_tag(r"Hartshorne \& May (1928)")
        with self.voiceover(
            "The doubt is older than the five factors. <bookmark mark='a'/> In the 1920s Hugh Hartshorne and Mark "
            "May, of the Character Education Inquiry at Teachers College in New York, gave schoolchildren chances "
            "to cheat that they thought nobody could detect: copying answers, taking money, lying, faking a score, "
            "peeping. <bookmark mark='b'/> A child who cheated on one test tended to cheat again when the same test "
            "was repeated. <bookmark mark='c'/> But cheating on one kind of test predicted cheating on a different "
            "kind only weakly, and the more different the situations, the weaker the link. <bookmark mark='d'/> "
            "They concluded, in 1928, that honesty is specific to situations rather than a general trait. Later "
            "reanalyses of their data found more generality than they claimed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.15))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def coefficient(self):
        head = heading(r"The ``personality coefficient''")
        big = label(r"$r \approx .30$", font_size=72, color=LOST).move_to([-3.6, 0.6, 0])
        sub = label(r"the ceiling Mischel saw", font_size=22, color=GREY_A).next_to(big, DOWN, buff=0.25)
        rows = rows_of([
            (r"Walter Mischel, \ \emph{Personality and Assessment}, \ 1968: \ correlations between a trait measure "
             r"and behaviour in a particular situation, \ or between behaviour in two situations, \ rarely rose above "
             r"about .30", WHITE),
            (r"a correlation of .30 explains 9\% of the variance: \ was the rest the situation?", LOST),
            (r"the book was read as saying that personality does not exist; \ Mischel later protested that reading", GREY_A),
            (r"two decades of argument followed: \ the person-situation debate", YOU),
        ], 6.6, 22, 0.38).move_to([3.0, -0.2, 0])
        tag = historical_tag(r"Mischel (1968)")
        with self.voiceover(
            "Forty years later the doubt became a crisis. <bookmark mark='a'/> In 1968, in Personality and "
            "Assessment, Walter Mischel reviewed the evidence and found that correlations between a trait measure "
            "and behaviour in a particular situation, or between behaviour in two situations, rarely rose above "
            "about point three. It became known as the personality coefficient. <bookmark mark='b'/> A correlation "
            "of point three explains nine percent of the variance. Was the rest the situation? "
            "<bookmark mark='c'/> The book was read as saying that personality doesn't exist, a reading Mischel "
            "later protested. <bookmark mark='d'/> Two decades of argument followed: the person-situation debate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(big), FadeIn(sub))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def world(self):
        d = load("acts")
        head = heading(r"Psyche's world of people and situations")
        A = axes([-5, 5], [-5, 5], x_length=4.0, y_length=4.0, xticks=None, yticks=None, xlabel=r"act in situation 1",
                 ylabel=r"act in situation 2", center=[-4.4, -0.4, 0], font_size=14)
        dots = scatter(A.ax, d["x"], d["y"], PERSON, radius=0.025, opacity=0.5)
        r_l = label(rf"$r = {d['single']:.2f}$", font_size=26, color=PERSON).next_to(A, UP, buff=0.1)
        pie = VGroup()
        start = PI / 2
        for share, c in zip(d["comp"], COMP_COL):
            ang = TAU * share
            pie.add(AnnularSector(inner_radius=0.0, outer_radius=1.2, angle=-ang, start_angle=start, color=c,
                                  fill_opacity=0.85, stroke_width=1, stroke_color=BLACK))
            start -= ang
        pie.move_to([0.3, 0.9, 0])
        key = VGroup(*[label(rf"{pct(s)} \ {n}", font_size=16, color=c) for s, n, c in
                       zip(d["comp"], COMP_NAME, COMP_COL)]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        key.next_to(pie, RIGHT, buff=0.35)
        rows = rows_of([
            (r"each act is a stable trait, \ a situation everyone responds to, \ the person's own way of responding to "
             r"that situation, \ and noise", WHITE),
            (rf"one act in one situation predicts one act in another at {d['single']:.2f}: \ Mischel's ceiling, \ "
             r"with a real and stable trait in every person", PERSON),
            (rf"the same situation on another occasion: \ {d['same']:.2f}; \ higher, \ because the signature repeats",
             O_),
        ], 7.6, 20, 0.32).move_to([2.6, -2.2, 0])
        tag = simulated_tag(r"\texttt{personality.act\_world}")
        with self.voiceover(
            "Psyche can show why a real trait produces such small correlations. <bookmark mark='a'/> In its world, "
            "each act is the sum of four things: a stable trait, the pull of the situation on everyone, the "
            "person's own way of responding to that situation, and noise on the occasion. Here are their shares of "
            "the variance in one act. <bookmark mark='b'/> One act in one situation predicts one act in another "
            f"at {d['single']:.2f}. That's Mischel's ceiling, in a world where every person has a real and stable "
            "trait, and it answers your first number. <bookmark mark='c'/> The same situation met again does "
            f"better, {d['same']:.2f}, because the person's own response to it repeats."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pie], lag_ratio=0.3), FadeIn(key), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots), FadeIn(r_l), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
