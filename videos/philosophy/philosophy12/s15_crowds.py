from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Crowds(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"The wisdom of crowds", r"When is a crowd wiser than its members?", lit=(1907,),
                            part=PART)
        with self.voiceover("Chapter fourteen. The wisdom of crowds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ox()
        self.theorem()
        self.bias()
        self.markets()

    def ox(self):
        d = load("crowds")
        hc = history_card(1907, r"Francis Galton", r"`Vox Populi', \ \textit{Nature}", width=4.6,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(label(r"Plymouth, \ 1906: \ 787 tickets guess an ox's weight", font_size=23),
                      label(r"the middlemost guess: \ 1,207 lb", font_size=23, color=COMMON),
                      label(r"the dressed weight: \ 1,198 lb", font_size=23, color=OK),
                      label(r"within one percent, \ better than almost every guesser", font_size=23,
                            color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, 1.1, 0])
        hist = d["hist"]
        ax = Axes(x_range=[900, 1500, 100], y_range=[0, max(c for _, c in hist) * 1.15, 50], x_length=7.0,
                  y_length=3.0, tips=False, axis_config={"color": GREY_C, "include_numbers": True, "font_size": 18}
                  ).move_to([-2.6, -1.3, 0])
        bars = VGroup()
        for b, c in hist:
            x0 = 900 + 25 * b
            if x0 < 900 or x0 + 25 > 1500:
                continue
            p0, p1 = ax.c2p(x0, 0), ax.c2p(x0 + 25, c)
            bars.add(Rectangle(width=p1[0] - p0[0] - 0.01, height=p1[1] - p0[1], stroke_width=0,
                               fill_color=AG["A"], fill_opacity=0.6).move_to((p0 + p1) / 2))
        tl = DashedLine(ax.c2p(d["truth"], 0), ax.c2p(d["truth"], max(c for _, c in hist) * 1.1), color=OK)
        cl = DashedLine(ax.c2p(d["plain"]["crowd"], 0), ax.c2p(d["plain"]["crowd"], max(c for _, c in hist) * 1.1),
                        color=COMMON)
        note = label(rf"a toy fair of {d['n']} guesses \ (Galton's tickets survive only as his summary)",
                     font_size=19, color=GREY_B).next_to(ax, DOWN, buff=0.35)
        nums = VGroup(label(rf"crowd's average: \ {d['plain']['crowd']:.0f} lb", font_size=21, color=COMMON),
                      label(rf"truth: \ {d['truth']} lb", font_size=21, color=OK)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1).move_to(
            [3.4, -1.4, 0])
        with self.voiceover(
            "Sometimes, many fallible minds together know more than any of them. <bookmark mark='a'/>In 1906 Francis "
            "Galton went to a livestock fair in Plymouth, where 787 people paid sixpence each to guess the weight of "
            "an ox. <bookmark mark='b'/>The middlemost guess was one thousand two hundred and seven pounds. "
            "<bookmark mark='c'/>The ox, dressed, weighed one thousand one hundred and ninety-eight. "
            "<bookmark mark='d'/>The crowd was within one percent, closer than almost every individual guess. "
            "<bookmark mark='e'/>Galton's tickets do not survive, so the Reasoner builds a toy fair, each guesser "
            "with her own bias and noise. Their guesses spread widely; their average lands within a few pounds of "
            "the truth."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(Create(ax), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=3)
            self.play(Create(tl), Create(cl), FadeIn(nums), FadeIn(note))
        self.clear_scene()

    def theorem(self):
        d = load("crowds")["plain"]
        head = label(r"The diversity prediction theorem", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        who = label(r"Scott Page, \textit{The Difference} \ (2007)", font_size=21, color=GREY_B).next_to(head, DOWN,
                                                                                                    buff=0.15)
        f = MathTex(r"(c - \theta)^2", r"\;=\;", r"\frac{1}{n}\sum_i (s_i - \theta)^2", r"\;-\;",
                    r"\frac{1}{n}\sum_i (s_i - c)^2", font_size=40).next_to(who, DOWN, buff=0.45)
        f[0].set_color(COMMON)
        f[2].set_color(BAD)
        f[4].set_color(KNOW)
        labs = VGroup(label(r"crowd error", font_size=21, color=COMMON).next_to(f[0], DOWN, buff=0.25),
                      label(r"average error", font_size=21, color=BAD).next_to(f[2], DOWN, buff=0.25),
                      label(r"diversity", font_size=21, color=KNOW).next_to(f[4], DOWN, buff=0.25))
        proof = label(r"proof: \ expand $(s_i - \theta)^2 = ((s_i - c) + (c - \theta))^2$ \ and average; \ the cross "
                      r"term vanishes, \ since the $s_i - c$ sum to zero", font_size=21, color=GREY_A).move_to(
            [0, -0.5, 0])
        nums = MathTex(rf"{d['crowd_error']:.1f}", r"\;=\;", rf"{d['average_error']:.1f}", r"\;-\;",
                       rf"{d['diversity']:.1f}", font_size=38).move_to([0, -1.6, 0])
        nums[0].set_color(COMMON)
        nums[2].set_color(BAD)
        nums[4].set_color(KNOW)
        nl = label(r"the toy fair: \ squared errors in lb$^2$", font_size=20, color=GREY_B).next_to(nums, DOWN,
                                                                                                  buff=0.2)
        foot = label(r"a crowd is as wise as its members are accurate, \ plus as diverse as they are", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.4)
        assert d["identity"]
        with self.voiceover(
            "Why does it work? Scott Page's diversity prediction theorem is an identity. <bookmark mark='a'/>The "
            "crowd's squared error equals the average squared error of its members, minus their diversity, the "
            "average squared distance of each guess from the crowd's. <bookmark mark='b'/>The proof is two lines: "
            "expand each member's error around the crowd's average, and average; the cross term vanishes because "
            "the deviations from the average sum to zero. <bookmark mark='c'/>On the toy fair, the Reasoner checks "
            "it: the crowd's error of about five square pounds is the average error, over five thousand, minus a "
            "diversity of almost the same size. <bookmark mark='d'/>So a crowd is as wise as its members are "
            "accurate, plus however diverse they are. Diversity is not a bonus. It is the whole effect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(who))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(labs))
            vo.wait_until("b")
            self.play(FadeIn(proof))
            vo.wait_until("c")
            self.play(Write(nums), FadeIn(nl))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def bias(self):
        d = load("crowds")
        head = label(r"When the crowd shares a bias", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        hd = [label(r"", font_size=20), label(r"crowd error", font_size=21, color=COMMON),
              label(r"average error", font_size=21, color=BAD), label(r"diversity", font_size=21, color=KNOW)]
        rows = []
        for name, key in ((r"independent guesses", "plain"), (r"everyone 60 lb too heavy", "shared")):
            r = d[key]
            rows.append([label(name, font_size=21), label(f"{r['crowd_error']:,.0f}", font_size=21),
                         label(f"{r['average_error']:,.0f}", font_size=21),
                         label(f"{r['diversity']:,.0f}", font_size=21)])
        grid = ValueGrid(hd, rows, col_w=[4.2, 2.4, 2.6, 2.2], cell_h=0.56, font_size=21).move_to([0, 0.8, 0])
        rows2 = VGroup(
            label(r"the same diversity cannot cancel an error everyone shares", font_size=24, color=BAD),
            label(r"so crowds fail when members copy each other, \ or share a source, \ or a prejudice", font_size=23,
                  color=GREY_A),
            label(r"Condorcet's jury theorem has the same moral: \ independence \ (Part 39)", font_size=22,
                  color=GREY_B)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The theorem also says when crowds fail. <bookmark mark='a'/>The Reasoner adds sixty pounds to every "
            "guess at the toy fair, as if everyone had seen the same misleading sign. The diversity is exactly what "
            "it was. But the crowd's error is now nearly four thousand square pounds: the average error went up, and "
            "diversity cannot cancel an error that everyone shares. <bookmark mark='b'/>So crowds fail when their "
            "members copy one another, or share a single source, or a common prejudice. "
            "<bookmark mark='c'/>Condorcet's jury theorem, which we meet in Part 39, has the same moral: the wisdom "
            "of many depends on their independence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg),
                      FadeIn(VGroup(*grid.cell[0])))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*grid.cell[1])), FadeIn(rows2[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows2[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows2[2]))
        self.clear_scene()

    def markets(self):
        hc = history_card(1945, r"Friedrich Hayek", r"`The Use of Knowledge in Society'", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            label(r"the knowledge an economy needs is dispersed: \ no planner has it", font_size=23),
            label(r"a price sums it up: \ a mine closes, \ tin gets dearer, \ and users economize", font_size=23,
                  color=GREY_A),
            label(r"without anyone knowing why", font_size=23, color=GREY_A),
            label(r"prediction markets: \ contracts that pay \$1 if an event happens", font_size=23, color=GOAL),
            label(r"the price reads as a probability; \ the Iowa Electronic Markets, \ since 1988", font_size=22,
                  color=GREY_A),
            label(r"they aggregate well \ when traders are diverse and independent: \ the same moral again",
                  font_size=23, color=OK)).arrange(DOWN, buff=0.26).move_to([0, -0.5, 0])
        with self.voiceover(
            "Markets are crowds of another kind. <bookmark mark='a'/>Friedrich Hayek argued in 1945 that the knowledge "
            "an economy needs is scattered among millions of people, and no planner could ever collect it. "
            "<bookmark mark='b'/>A price sums it up. If a tin mine closes, tin becomes dearer, and every user of tin "
            "economizes, <bookmark mark='c'/>without anyone needing to know why. <bookmark mark='d'/>Prediction "
            "markets apply the idea directly: trade contracts that pay a dollar if some event happens, "
            "<bookmark mark='e'/>and the price can be read as the crowd's probability. The Iowa Electronic Markets "
            "have forecast elections this way since 1988. <bookmark mark='f'/>Like any crowd, they aggregate well "
            "when the traders are diverse and independent, and fail when everyone is following everyone else."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

