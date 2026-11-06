from __future__ import annotations

import random

from videos.philosophy.philosophy13.common import *  # noqa: F403

HC, TC, AWAKE, ASLEEP = "#FFD166", "#6FB7FF", "#5EE6D0", "#3A4250"


def node(text: str, col, pos, w=1.7, h=0.6, fill=0.2) -> VGroup:
    b = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=col, stroke_width=3, fill_color=col,
                         fill_opacity=fill).move_to(pos)
    return VGroup(b, label(text, font_size=20).move_to(pos))


class Beauty(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Sleeping Beauty", r"What should you believe about when you are?", lit=(2000,),
                            part=PART)
        with self.voiceover("Chapter eleven. Sleeping Beauty."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.week()
        self.answers()
        self.simulate()
        self.bets()
        self.monday()
        self.selflocating()

    def tree(self):
        sun = node(r"Sunday: \ sleep; \ toss a coin", WHITE, [-4.6, 0.3, 0], w=2.9)
        h = node(r"heads", HC, [-1.6, 1.5, 0], w=1.4)
        t = node(r"tails", TC, [-1.6, -0.9, 0], w=1.4)
        hm = node(r"Monday: \ woken", AWAKE, [1.4, 1.5, 0], w=2.3)
        ht = node(r"Tuesday: \ asleep", ASLEEP, [4.4, 1.5, 0], w=2.3, fill=0.6)
        tm = node(r"Monday: \ woken", AWAKE, [1.4, -0.9, 0], w=2.3)
        tt = node(r"Tuesday: \ woken", AWAKE, [4.4, -0.9, 0], w=2.3)
        ar = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.1, color=GREY_B, stroke_width=3,
                            max_tip_length_to_length_ratio=0.15)
                      for a, b in ((sun, h), (sun, t), (h, hm), (hm, ht), (t, tm), (tm, tt))])
        erase = label(r"memory erased", font_size=18, color=BAD).next_to(ar[5], DOWN, buff=0.42)
        return VGroup(sun, h, t, hm, ht, tm, tt, ar, erase)

    def week(self):
        hc = history_card(2000, r"Adam Elga", r"`Self-locating belief and the Sleeping Beauty problem'",
                          width=6.2, color=HIST).to_corner(UL, buff=0.35)
        tr = self.tree().shift(DOWN * 0.5)
        sun, h, t, hm, ht, tm, tt, ar, erase = tr
        q = label(r"woken, \ with no idea what day it is: \ how likely is it that the coin landed heads?",
                  font_size=24, color=BET).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Adam Elga's puzzle, from 2000, came to him from the decision theorists. <bookmark mark='a'/>On Sunday "
            "Beauty is put to sleep, and a fair coin is tossed. <bookmark mark='b'/>If it lands heads, she is woken "
            "on Monday, and sleeps through Tuesday. <bookmark mark='c'/>If tails, she is woken on Monday, put back to "
            "sleep with the memory of the waking erased, and woken again on Tuesday. <bookmark mark='d'/>She knows "
            "all this. Now she wakes, with no idea what day it is. How likely is it, for her, that the coin landed "
            "heads?"
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(sun))
            self.play(GrowArrow(ar[0]), GrowArrow(ar[1]), FadeIn(h), FadeIn(t))
            vo.wait_until("b")
            self.play(GrowArrow(ar[2]), FadeIn(hm))
            self.play(GrowArrow(ar[3]), FadeIn(ht))
            vo.wait_until("c")
            self.play(GrowArrow(ar[4]), FadeIn(tm))
            self.play(GrowArrow(ar[5]), FadeIn(tt), FadeIn(erase))
            vo.wait_until("d")
            self.play(FadeIn(q))
        self.clear_scene()

    def answers(self):
        tr = self.tree().scale(0.62).to_edge(UP, buff=0.35)
        half = VGroup(label(r"halfer: \ $\tfrac12$ \ \ (Lewis, \ 2001)", font_size=26, color=HC),
                      label(r"she knew she would wake; \ she has learned nothing new", font_size=21),
                      label(r"so her credence should stay at the coin's chance", font_size=21, color=GREY_A)).arrange(
            DOWN, buff=0.18)
        third = VGroup(label(r"thirder: \ $\tfrac13$ \ \ (Elga, \ 2000)", font_size=26, color=TC),
                       label(r"three wakings she cannot tell apart", font_size=21),
                       label(r"the tails ones are equally likely; \ and if told `it is Monday',", font_size=21),
                       label(r"a coin not yet tossed should get $\tfrac12$: \ so each waking gets $\tfrac13$",
                             font_size=21, color=GREY_A)).arrange(DOWN, buff=0.18)
        VGroup(half, third).arrange(RIGHT, buff=1.0, aligned_edge=UP).to_edge(DOWN, buff=0.6)
        foot = label(r"the coin may be tossed on Monday night: \ nothing changes for Beauty", font_size=19,
                     color=GREY_B).next_to(third, DOWN, buff=0.15)
        with self.voiceover(
            "Two answers, both defended by excellent philosophers. <bookmark mark='a'/>The halfer, David Lewis: on "
            "Sunday her credence in heads was a half, and when she wakes she learns nothing she didn't know would "
            "happen. So it should still be a half. <bookmark mark='b'/>The thirder, Elga: there are three wakings "
            "she cannot tell apart. The two tails wakings should be equally likely. And if she were told that it is "
            "Monday, her credence in heads should be one half, because the coin could just as well be tossed on "
            "Monday night, after she wakes. <bookmark mark='c'/>Put those together, and each of the three wakings "
            "gets a third. So heads gets a third."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in half], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in third[:3]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(third[3]), FadeIn(foot))
        self.clear_scene()

    def simulate(self):
        d = load("beauty")
        head = label(r"The Reasoner runs the experiment", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rnd = random.Random(12)
        strip = VGroup()
        x = -6.4
        tosses = [rnd.random() < 0.5 for _ in range(16)]
        for hd in tosses:
            k = 1 if hd else 2
            for _ in range(k):
                strip.add(Square(side_length=0.32, stroke_width=0, fill_color=HC if hd else TC,
                                 fill_opacity=0.9).move_to([x, 1.6, 0]))
                x += 0.37
            x += 0.16
        strip.set_x(0)
        strip_l = label(r"each square is a waking: \ yellow after heads, \ blue after tails", font_size=20,
                        color=GREY_A).next_to(strip, DOWN, buff=0.2).set_x(0)
        rows = VGroup(
            VGroup(label(r"experiments:", font_size=24), MathTex(rf"{d['runs']:,}".replace(",", "{,}"),
                                                                font_size=30)).arrange(RIGHT, buff=0.2),
            VGroup(label(r"heads, \ per experiment:", font_size=24, color=HC),
                   MathTex(rf"{d['heads_per_experiment']:.4f}", font_size=34, color=HC)).arrange(RIGHT, buff=0.2),
            VGroup(label(r"heads, \ per waking:", font_size=24, color=TC),
                   MathTex(rf"{d['heads_per_awakening']:.4f}", font_size=34, color=TC)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([0, -1.0, 0])
        foot = label(r"both numbers are right: \ they answer different questions", font_size=25,
                     color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The Reasoner runs the experiment a hundred thousand times. <bookmark mark='a'/>Here are the first "
            "sixteen, one square per waking: one square after heads, two after tails. <bookmark mark='b'/>Count the "
            "experiments in which the coin landed heads: half of them. <bookmark mark='c'/>Count the wakings that "
            "follow heads: a third of them, because tails produces twice as many wakings. <bookmark mark='d'/>Both "
            "numbers are right. They answer different questions: how often the coin lands heads, and how often a "
            "waking follows heads. The puzzle is which of those Beauty's credence should track."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in strip], lag_ratio=0.05), FadeIn(strip_l), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def bets(self):
        d = load("beauty")
        head = label(r"What the bets say", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        left = VGroup(label(r"offered at every waking", font_size=24, color=TC),
                      label(r"a ticket paying \$1 if heads, \ at price $x$", font_size=21),
                      MathTex(r"\tfrac12(1 - x) + \tfrac12(-2x) = 0", font_size=30),
                      MathTex(rf"x = {d['breakeven_per_awakening']:.3f}", font_size=34, color=TC),
                      label(r"the thirder's price", font_size=21, color=GREY_A)).arrange(DOWN, buff=0.25).move_to(
            [-3.4, -0.2, 0])
        right = VGroup(label(r"settled once per experiment", font_size=24, color=HC),
                       label(r"the same ticket, \ but only one counts", font_size=21),
                       MathTex(r"\tfrac12(1 - x) + \tfrac12(-x) = 0", font_size=30),
                       MathTex(rf"x = {d['breakeven_per_experiment']:.3f}", font_size=34, color=HC),
                       label(r"the halfer's price", font_size=21, color=GREY_A)).arrange(DOWN, buff=0.25).move_to(
            [3.4, -0.2, 0])
        foot = label(r"bets don't settle it: \ the betting setup decides which count matters", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Can betting settle it, as it settled coherence? <bookmark mark='a'/>Offer Beauty a ticket paying a "
            "dollar if heads, at price x, at every waking. After heads she buys one ticket and wins; after tails she "
            "buys two and loses both. Her break-even price is a third: the thirder's credence. "
            "<bookmark mark='b'/>But if only one purchase per experiment counts, the break-even price is a half: the "
            "halfer's. <bookmark mark='c'/>So bets reveal what is being counted. They don't decide what Beauty "
            "should believe."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in left], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in right], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def monday(self):
        head = label(r"Then she is told: \ `today is Monday'", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [label(r"view", font_size=22, color=P.CLAIM), label(r"on waking", font_size=22, color=P.CLAIM),
              label(r"told `Monday'", font_size=22, color=P.CLAIM), label(r"the cost", font_size=22, color=P.CLAIM)]
        rows = [
            (r"thirder", r"$\tfrac13$", r"$\tfrac12$", r"credence moves without new evidence about the coin?", TC),
            (r"halfer", r"$\tfrac12$", r"$\tfrac23$", r"$\tfrac23$ for a fair coin not yet tossed", HC),
            (r"double halfer", r"$\tfrac12$", r"$\tfrac12$", r"gives up conditionalization \ (Meacham, \ 2008)",
             COH),
        ]
        trs = [[label(a, font_size=22, color=c), label(b, font_size=24), label(x, font_size=24),
                label(z, font_size=20, color=GREY_A)] for a, b, x, z, c in rows]
        grid = ValueGrid(hd, trs, col_w=[2.6, 1.8, 2.2, 6.2], cell_h=0.7, font_size=22).next_to(head, DOWN, buff=0.6)
        foot = label(r"every answer pays somewhere: \ self-locating belief strains the rules of updating",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Each answer has a price, which shows when Beauty is told that today is Monday. "
            "<bookmark mark='a'/>For the thirder, her credence in heads rises from a third to a half: she has "
            "learned what day it is, and wakings are what she was uncertain among. <bookmark mark='b'/>For Lewis's "
            "halfer it rises from a half to two thirds. So she should be two-thirds confident that a fair coin, to "
            "be tossed tonight, will land heads. Few can accept that. <bookmark mark='c'/>The double halfer, "
            "Christopher Meacham's view, says a half both times, which means she does not conditionalize on what "
            "she learns. <bookmark mark='d'/>Every answer pays somewhere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(*[FadeIn(m) for m in grid.cell[r]])
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def selflocating(self):
        head = label(r"Belief about where, \ and when, \ you are", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"ordinary credence: \ over possible worlds", WHITE),
            (r"self-locating credence: \ over \textit{centred} worlds \ (Lewis, \ 1979): \ a world, \ a person, "
             r"\ a time", CRED),
            (r"Beauty's three centres: \ heads--Monday, \ tails--Monday, \ tails--Tuesday", GREY_A),
            (r"learning `it is Monday' is not learning which world you are in", WHITE),
            (r"conditionalization was built for worlds; \ for centres it needs revising \ (Titelbaum, \ 2013)", GOAL),
            (r"next: \ the same question, \ asked about all of humanity", BET),
        ], font_size=24, buff=0.3, width=12.4).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "What makes Beauty hard is that her uncertainty is not about the world. <bookmark mark='a'/>Ordinary "
            "credence is spread over possible worlds. <bookmark mark='b'/>Self-locating credence, in Lewis's phrase, "
            "is spread over centred worlds: a world together with a person and a time. <bookmark mark='c'/>Beauty "
            "has three centres to choose among. <bookmark mark='d'/>Learning that it is Monday is learning which "
            "centre you occupy, not which world. <bookmark mark='e'/>Conditionalization was designed for "
            "uncertainty about worlds, and Michael Titelbaum and others have had to rebuild it for centres. "
            "<bookmark mark='f'/>Next, the same question, about all of humanity."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
