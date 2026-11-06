from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class First(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Knowledge first", r"What if knowledge cannot be analysed?", lit=(2000,), part=PART)
        with self.voiceover("Chapter nine. Knowledge first."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.reverse()
        self.cold()
        self.brick()

    def reverse(self):
        hc = history_card(2000, r"Timothy Williamson", r"\textit{Knowledge and Its Limits}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        old = VGroup(MathTex(r"\text{belief} + \text{truth} + \text{justification} + X", font_size=30, color=GREY_A),
                     MathTex(r"\Downarrow", font_size=36, color=GREY_A),
                     MathTex(r"\text{knowledge}", font_size=34, color=GREY_A)).arrange(DOWN, buff=0.15).move_to(
            [-3.4, 0.2, 0])
        cross = Cross(old, stroke_color=BAD, stroke_width=5)
        new = VGroup(MathTex(r"\text{knowledge}", font_size=34, color=KNOW),
                     MathTex(r"\Downarrow", font_size=36, color=KNOW),
                     VGroup(label(r"evidence \ $E = K$", font_size=24, color=JUST),
                            label(r"belief: \ what aims at knowledge", font_size=24, color=BEL),
                            label(r"assertion: \ say only what you know", font_size=24, color=GREY_A)).arrange(
                         DOWN, buff=0.15)).arrange(DOWN, buff=0.15).move_to([3.3, 0.2, 0])
        foot = label(r"knowledge: \ the most general factive mental state \ (like seeing that, \ remembering that)",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "After forty years of counterexamples, Timothy Williamson proposed in 2000 to stop. <bookmark mark='a'/>"
            "The project assumed that knowledge is belief plus truth plus justification plus something, to be found. "
            "<bookmark mark='b'/>Williamson argued that knowledge has no such analysis, and that this is no "
            "embarrassment: most important concepts have none. <bookmark mark='c'/>Instead, put knowledge first, "
            "and explain the rest by it. Your evidence is exactly what you know: E equals K. Belief is the state "
            "that aims at knowledge, and falls short when it misses. And the rule of assertion is: say only what you "
            "know. <bookmark mark='d'/>Knowledge, on this view, is a mental state in its own right: the most general "
            "factive one, of which seeing that, remembering that and realizing that are special cases."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(old))
            vo.wait_until("b")
            self.play(Create(cross))
            vo.wait_until("c")
            self.play(FadeIn(new[0]), FadeIn(new[1]))
            self.play(LaggedStart(*[FadeIn(m) for m in new[2]], lag_ratio=0.5), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def cold(self):
        d = load("luminosity")
        n = len(d["feel"]) - 1
        head = label(r"Anti-luminosity: \ a cold morning", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, n, 4], y_range=[0, 1, 0.5], x_length=9.0, y_length=3.2, tips=False,
                  axis_config={"color": GREY_C, "stroke_width": 2}).move_to([-0.6, 0.15, 0])
        xl = label(r"dawn $\longrightarrow$ noon \ (25 moments)", font_size=20, color=GREY_B).next_to(ax, DOWN,
                                                                                                    buff=0.15)
        yl = label(r"feeling of cold", font_size=20, color=GREY_B).rotate(PI / 2).next_to(ax, LEFT, buff=0.15)
        thr = DashedLine(ax.c2p(0, 0.5), ax.c2p(n, 0.5), color=GREY_B)
        thl = label(r"`I feel cold' \ above this line", font_size=19, color=GREY_B).next_to(thr, RIGHT, buff=0.1)
        dots = VGroup()
        for t, f in enumerate(d["feel"]):
            col = KNOW if d["known"][t] else (LUCK if d["cold"][t] else GREY_C)
            dots.add(Dot(ax.c2p(t, f), radius=0.07, color=col))
        gap = d["gap"]
        band = Rectangle(width=ax.c2p(gap[-1] + 0.5, 0)[0] - ax.c2p(gap[0] - 0.5, 0)[0], height=3.2,
                         stroke_width=0, fill_color=LUCK, fill_opacity=0.12).move_to(
            [(ax.c2p(gap[0] - 0.5, 0)[0] + ax.c2p(gap[-1] + 0.5, 0)[0]) / 2, ax.get_center()[1], 0])
        keys = VGroup(
            VGroup(Dot(radius=0.07, color=KNOW), label(r"cold, \ and known to be", font_size=19, color=GREY_A)
                   ).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.07, color=LUCK), label(r"cold, \ not knowably so", font_size=19, color=GREY_A)
                   ).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.07, color=GREY_C), label(r"not cold", font_size=19, color=GREY_A)).arrange(
                RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.3, 1.3, 0])
        rows = VGroup(
            label(r"margin for error: \ to know I feel cold, \ I must feel cold in every case \textit{almost} like "
                  r"this one", font_size=22, color=JUST),
            label(rf"the Reasoner: \ moments {gap[0]} and {gap[-1]} \ are cold, \ but not knowably cold", font_size=22,
                  color=LUCK),
            label(r"luminosity (cold $\Rightarrow$ knowably cold) \ plus margins \ would carry `cold' all the way to "
                  r"noon", font_size=22, color=BAD)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Williamson's most famous argument is about what we can know of our own minds. Call a condition luminous "
            "if, whenever it obtains, you are in a position to know that it does. Surely feeling cold is luminous? "
            "<bookmark mark='a'/>Take a morning that warms very slowly, from freezing at dawn to warm at noon. The "
            "Reasoner divides it into twenty-five moments. At each, the feeling of cold is a little weaker than at "
            "the one before; above the line, you feel cold. <bookmark mark='b'/>Now, knowledge needs a margin for "
            "error. If at some moment you know that you feel cold, then you must feel cold at the next moment too, "
            "since your feelings then are almost exactly the same, and a belief that would have been false in a "
            "case so similar is not safe. <bookmark mark='c'/>The Reasoner applies the margin to every moment. Most "
            "cold moments are knowably cold. But the last two cold moments before the line are not: you feel cold, "
            "and you are in no position to know it. <bookmark mark='d'/>And luminosity must fail somewhere. If it "
            "held, then feeling cold at dawn would give knowledge of it, the margin would give feeling cold at the "
            "next moment, then knowledge of that, and so on, step by step, to feeling cold at noon. Which you do "
            "not. So no condition that can change gradually is luminous: not even your own sensations."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.05), Create(thr), FadeIn(thl),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(band), FadeIn(keys), FadeIn(rows[1]),
                      *[Indicate(dots[t], color=LUCK, scale_factor=1.8) for t in gap])
            vo.wait_until("d")
            self.play(LaggedStart(*[Flash(dots[t].get_center(), color=BAD, line_length=0.12) for t in
                                    range(d["first_warm"] + 1)], lag_ratio=0.15), run_time=3)
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def brick(self):
        w = wall(upto=11, current=11).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(11, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Two results like these go into the Wall. <bookmark mark='a'/>The eleventh brick. The dream: an "
            "analysis of knowledge, justified true belief plus X. <bookmark mark='b'/>The wall: Gettier's cases, with "
            "Zagzebski's recipe for making more whenever X falls short of truth; and Williamson's anti-luminosity "
            "argument, which shows that even our access to our own minds has margins. <bookmark mark='c'/>What it "
            "forces: perhaps knowledge cannot be analysed, and must be taken as basic; or, if it can, some condition "
            "must close the gap between justification and truth without making knowledge impossible."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.brick[11], color=P.CONCL, scale_factor=1.08), FadeIn(card[0]), FadeIn(card[1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1]))
            vo.wait_until("c")
            self.play(Indicate(card, color=P.WALL, scale_factor=1.02))
        self.clear_scene()
