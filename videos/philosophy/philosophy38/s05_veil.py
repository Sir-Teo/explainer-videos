from __future__ import annotations

from videos.philosophy.philosophy38.common import *  # noqa: F403


class Veil(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Choosing behind the veil", r"Maximin, \ or the average?", lit=(1975,), part=PART)
        with self.voiceover("Chapter four. Choosing behind the veil."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.harsanyi()
        self.societies()
        self.stakes()

    def harsanyi(self):
        head = label(r"Harsanyi against Rawls", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Harsanyi \ (1953; \ 1975)", r"behind the veil, \ give each position an equal chance and maximize expected utility: \ the result is average utilitarianism", MKT),
                (r"his objection", r"maximin would refuse any gain to all but the worst off, \ however large, \ for the smallest gain to them", BAD),
                (r"Rawls's reply", r"the conditions for maximin hold behind the veil; \ and utilitarianism ignores the separateness of persons", FAIR),
                (r"the stakes", r"the same veil, \ two different principles: \ the disagreement is about rational choice under uncertainty", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "John Harsanyi had used the same device before Rawls, with a different result. <bookmark mark='a'/>Behind "
            "a veil, he argued in 1953 and again in 1975, a rational chooser would give herself an equal chance of "
            "being anyone, and maximize expected utility: and that is average utilitarianism, the theorem of Part 35. "
            "<bookmark mark='b'/>Harsanyi objected that maximin would refuse any gain to everyone else, however "
            "large, for the smallest gain to the worst off. <bookmark mark='c'/>Rawls replied that the conditions "
            "for maximin hold behind the veil, and added a deeper charge: utilitarianism treats society as one big "
            "person, adding up gains and losses across lives, and so ignores the separateness of persons. <bookmark "
            "mark='d'/>So the same veil yields two principles, and the disagreement is really about rational choice "
            "under uncertainty, the subject of Part 33."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def societies(self):
        d = load("veil")
        head = label(r"Two hundred societies, \ chosen", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["n"], d["classes"], d["avg_choice"], d["maximin_choice"]) == (200, 5, 140, 173)
        assert d["avg"] == {"average": 54.0, "minimum": 5.148} and d["maximin"] == {"average": 42.959, "minimum": 33.301}
        be = {b["eta"]: b for b in d["by_eta"]}
        assert (be[0]["choice"], be[2]["choice"], be[8]["choice"], be[20]["choice"]) == (140, 128, 173, 173)
        assert (be[2]["average"], be[2]["minimum"]) == (50.658, 29.82)
        ax = Axes(x_range=[0, 60, 10], y_range=[0, 40, 10], x_length=6.0, y_length=4.2, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15, "include_numbers": True}).move_to([-3.3, -0.5, 0])
        xl = label(r"average income", font_size=16, color=MKT).next_to(ax.x_axis, DOWN, buff=0.42)
        yl = label(r"income of the worst-off class", font_size=16, color=FAIR).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(a, m), radius=0.035, color=GREY_B) for a, m in d["points"]])
        mark_ = lambda k, c: Circle(radius=0.13, color=c, stroke_width=3).move_to(ax.c2p(*d["points"][k]))  # noqa: E731
        m_avg, m_mid, m_max = mark_(140, MKT), mark_(128, COM), mark_(173, FAIR)
        side = stack([(r"each dot: \ a society of five equal classes", GREY_A),
                      (r"average utility \ (Harsanyi): \ average 54.0, \ worst off 5.1", MKT),
                      (r"maximin \ (Rawls): \ average 43.0, \ worst off 33.3", FAIR),
                      (r"expected utility with risk aversion $\eta$ from 0.5 to 5: \ average 50.7, \ worst off 29.8",
                       COM),
                      (r"from $\eta = 8$ on, \ the maximin society: \ maximin is the limit of infinite risk "
                       r"aversion", GOAL)],
                     font_size=18, aligned_edge=LEFT, width=4.8, buff=0.3).move_to([4.2, -0.3, 0])
        with self.voiceover(
            "The Reasoner puts the two rules to work. <bookmark mark='a'/>It draws two hundred societies, each with "
            "five equally large classes; richer societies tend to be more unequal. Each dot is a society, placed by "
            "its average income and the income of its worst-off class. <bookmark mark='b'/>A chooser who maximizes "
            "average utility, as Harsanyi recommended, picks the richest on average: fifty four, with a worst-off "
            "class at five. <bookmark mark='c'/>Maximin picks the society whose worst-off class is best off: thirty "
            "three, with an average of forty three. <bookmark mark='d'/>Between them lies expected utility with risk "
            "aversion. With a curvature eta anywhere from half to five, the choice is a third society: average fifty "
            "point seven, worst off twenty nine point eight. <bookmark mark='e'/>From eta eight upward, it is the "
            "maximin society. Maximin is what expected utility becomes as risk aversion grows without limit."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.005, run_time=2), FadeIn(side[0]))
            for mk, (m, s) in zip("bcde", ((m_avg, side[1]), (m_max, side[2]), (m_mid, side[3]), (None, side[4]))):
                vo.wait_until(mk)
                anims = [FadeIn(s)] + ([Create(m)] if m is not None else [Indicate(m_max, color=FAIR)])
                self.play(*anims)
        self.clear_scene()

    def stakes(self):
        head = label(r"What the veil leaves out", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"risk attitude", r"the choice depends on the risk aversion we build into the chooser: \ that is a moral choice in disguise", COM),
                (r"strains of commitment", r"Rawls: \ choose principles you could live with in any position, \ and keep in good faith", FAIR),
                (r"Sen \ (2009)", r"\textit{The Idea of Justice}: \ compare real alternatives; \ no blueprint of a perfectly just society is needed", LIB),
                (r"Cohen \ (2008)", r"\textit{Rescuing Justice and Equality}: \ the incentives behind the difference principle are demands the talented choose to make", POW)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "What does the veil leave out? <bookmark mark='a'/>First, the verdict depends on the attitude to risk we "
            "give the chooser, and that is a moral decision made in advance. <bookmark mark='b'/>Rawls added the "
            "strains of commitment: the parties must choose principles they could live with, and keep in good faith, "
            "whatever position they turn out to occupy. <bookmark mark='c'/>Amartya Sen's The Idea of Justice, of 2009, "
            "objected to the search for a perfectly just society: what we need are comparisons between real "
            "alternatives, and we can know that ending a famine is more just without knowing what perfect justice "
            "is. <bookmark mark='d'/>And G. A. Cohen's Rescuing Justice and Equality, of 2008, attacked the incentive "
            "argument behind the difference principle. The talented demand higher pay to work harder; but in a "
            "society whose members really accepted the principle, they would not demand it, so the inequality it "
            "licenses reflects their choices, not a constraint on what is possible."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
