from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)

X0, UNIT = -6.3, 0.36


def bar(iv, y, color, h=0.26, op=0.75):
    s, f = iv
    return Rectangle(width=(f - s) * UNIT, height=h, stroke_color=color, stroke_width=1.5, fill_color=color,
                     fill_opacity=op).move_to([X0 + (s + f) / 2 * UNIT, y, 0])


class Greedy(VoiceoverScene):
    def construct(self):
        self.card()
        self.schedule()
        self.exchange()
        self.rules()
        self.huffman()

    def card(self):
        card = chapter_card(1, r"Greedy, \ and the exchange argument", r"When is the best-looking step safe?",
                            lit=(1952,), extra=((1952, r"Huffman codes"),), part=PART)
        with self.voiceover("Chapter one. Greedy, and the exchange argument."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def schedule(self):
        d = load("greedy")
        head = label(r"One room, \ many meetings", font_size=34).to_edge(UP, buff=0.3)
        ivs = sorted(map(tuple, d["ivs"]), key=lambda iv: iv[1])
        pick = set(map(tuple, d["pick"]))
        bars = VGroup(*[bar(iv, 2.2 - 0.38 * i, GREY_B, op=0.35) for i, iv in enumerate(ivs)])
        axis = NumberLine(x_range=[0, 22, 2], length=22 * UNIT, include_numbers=False, color=GREY_D).move_to(
            [X0 + 11 * UNIT, -2.2, 0])
        ticks = VGroup(*[label(str(t), font_size=15, color=GREY_B).next_to(axis.n2p(t), DOWN, buff=0.1)
                         for t in range(0, 23, 4)])
        pts = VGroup(
            label(r"choose as many non-overlapping meetings as possible", font_size=21, color=GREY_A),
            label(r"greedy rule: \\ take the one that \textbf{finishes first}, \\ drop everything it overlaps, \\ "
                  r"repeat", font_size=21, color=YES),
            label(rf"here: \ {len(pick)} meetings, \ the most possible", font_size=22, color=HEAD),
            label(r"sort once, \ scan once: \ $O(n \log n)$", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            'Each meeting has a start and an end; every meeting counts equally, and touching endpoints are allowed. '
            "<bookmark mark='a'/> Choose the largest nonoverlapping subset. <bookmark mark='b'/> Sort by finishing "
            'time and accept the next meeting whose start is at least the last accepted finish. Checking that one '
            "boundary is enough because the accepted meetings are ordered. <bookmark mark='c'/> This instance admits "
            "four meetings, matching the independently computed optimum. <bookmark mark='d'/> Sorting costs n log n "
            'comparisons; the finish-rule scan is linear. Other plausible rules will fail.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), Create(axis), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            last = -1
            for i, iv in enumerate(ivs):
                if iv in pick:
                    self.play(bars[i].animate.set_fill(YES, 0.9).set_stroke(YES), run_time=0.45)
                    for j, jv in enumerate(ivs):
                        if jv not in pick and jv[0] < iv[1] and iv[0] < jv[1] and j > last:
                            bars[j].set_fill(GREY_D, 0.15).set_stroke(GREY_D)
                    last = i
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def exchange(self):
        head = label(r"The exchange argument", font_size=34).to_edge(UP, buff=0.3)
        g = [(0, 5), (7, 10), (12, 15), (17, 20)]
        o = [(1, 6), (8, 11), (12, 16), (17, 22)]           # an abstract best schedule, first meeting different
        gb = VGroup(*[bar(iv, 1.6, YES) for iv in g])
        ob = VGroup(*[bar(iv, 0.4, LAM) for iv in o])
        gl = label(r"greedy", font_size=20, color=YES).next_to(gb, UP, buff=0.15).align_to(gb, LEFT)
        ol = label(r"any best schedule", font_size=20, color=LAM).next_to(ob, UP, buff=0.15).align_to(gb, LEFT)
        new = bar(g[0], 0.4, YES)
        steps = VGroup(
            label(r"greedy's first meeting $g_1$ ends no later than any other meeting", font_size=21, color=GREY_A),
            label(r"in a best schedule, \ swap its first meeting for $g_1$: \ nothing new overlaps, \ the count is "
                  r"unchanged", font_size=21, color=YES),
            label(r"so some best schedule starts with $g_1$; \ repeat the argument on what is left", font_size=21,
                  color=GREY_A),
            label(r"by induction greedy is never behind: \ it stays ahead at every step", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The proof is called an exchange argument. <bookmark mark='a'/> Greedy's first meeting finishes no "
            "later than any meeting at all. <bookmark mark='b'/> Take any best schedule and swap its first meeting "
            "for greedy's. Greedy's ends earlier, so it cannot clash with anything that came after; the schedule "
            "is still valid and just as large. <bookmark mark='c'/> So some best schedule begins with greedy's "
            "choice, and the rest of it is a best schedule for the meetings that start later, where the same "
            "argument applies. <bookmark mark='d'/> By induction, greedy is never behind. That is the shape of "
            "nearly every greedy proof: show that a best solution can be changed, one step at a time, into the "
            "greedy one without getting worse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gb), FadeIn(ob), FadeIn(gl), FadeIn(ol))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), Indicate(gb[0], color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), Transform(ob[0], new))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
        self.wait(0.3)
        self.clear_scene()

    def rules(self):
        d = load("greedy")
        head = label(r"Plausible rules that fail", font_size=34).to_edge(UP, buff=0.3)
        st = d["stats"]
        T = d["trials"]
        rows = [[r"finishes first", f"{st['finish']:,} of {T:,}", r"always \ (proved)"],
                [r"fewest overlaps", f"{st['fewest']:,} of {T:,}", rf"fails on {len(d['bad']['fewest']['ivs'])} "
                                                                    r"meetings"],
                [r"shortest", f"{st['shortest']:,} of {T:,}", r"fails on 3 meetings"],
                [r"starts first", f"{st['start']:,} of {T:,}", r"fails on 4 meetings"]]
        tab = grid_table([r"greedy rule", r"optimal on random cases", r"counterexample"], rows,
                         widths=[3.4, 3.8, 3.8], row_h=0.5, font_size=21, mono_cols=(),
                         colors=[[YES] * 3, [HEAD] * 3, [LAM] * 3, [NO] * 3]).next_to(head, DOWN, buff=0.5)
        ex = d["bad"]["shortest"]["ivs"]
        exb = VGroup(*[bar(tuple(iv), y, c) for iv, y, c in ((ex[0], -1.3, GREY_B), (ex[1], -1.7, NO),
                                                              (ex[2], -1.3, GREY_B))]).shift(RIGHT * 1.4)
        exl = label(r"shortest first takes the middle one, \\ and blocks two", font_size=19,
                    color=GREY_A).next_to(exb, RIGHT, buff=0.5)
        coins = VGroup(
            label(r"coins $\{1, 3, 4\}$: \ greedy pays 6 as $4 + 1 + 1$, \ the best is $3 + 3$", font_size=21,
                  color=NO),
            label(rf"amounts 1--99: greedy fails {d['coins134_fail_n']} times for 1,3,4; none for 1,5,10,25", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A plausible rule still needs a proof. <bookmark mark='a'/> These four rules run on two thousand fixed "
            'random instances. Earliest finish matches the optimum throughout; that experiment illustrates the '
            "theorem. Fewest conflicts still fails on the displayed fifteen-meeting witness. <bookmark mark='b'/> "
            'Shortest first chooses the middle interval and loses two compatible intervals. Starting first can lose '
            "many. <bookmark mark='c'/> With coin values one, three and four, greedy pays six using three coins, "
            'while dynamic programming finds two. The displayed failure count covers amounts one through ninety-nine.'
            ' The one-five-ten-twenty-five system passes that finite range; the experiment alone does not prove '
            'canonicality for all amounts.'
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(exb), FadeIn(exl))
            vo.wait_until("c")
            self.play(FadeIn(coins))
        self.wait(0.3)
        self.clear_scene()

    def huffman(self):
        d = load("greedy")
        head = label(r"Huffman's code, \ greedy too \ (1952)", font_size=34).to_edge(UP, buff=0.3)
        codes = d["codes"]
        rows = [[(r"space" if s == " " else s), f"{100 * p:.1f}\\%", str(L)] for s, L, p in codes[:9]]
        rows.append([r"\ldots", "", ""])
        rows += [[s, f"{100 * p:.2f}\\%", str(L)] for s, L, p in codes[-3:]]
        tab = grid_table([r"symbol", r"share", r"bits"], rows, widths=[1.6, 1.8, 1.2], row_h=0.36, font_size=19,
                         mono_cols=(), colors=[[WHITE, GREY_A, YES]] * len(rows)).next_to(head, DOWN, buff=0.4).to_edge(
            LEFT, buff=0.8)
        pts = VGroup(
            label(r"repeatedly merge the two rarest symbols \\ into one; \ the merges build the code tree", font_size=21,
                  color=GREY_A),
            label(r"exchange argument: \ some optimal tree has the two rarest \\ as deepest siblings", font_size=21,
                  color=HEAD),
            label(rf"on the thirty novels' {d['symbols']} symbols: \\ {d['avg_bits']:.2f} bits each, \ against "
                  rf"{d['fixed_bits']} for a fixed code", font_size=22, color=YES),
            label(rf"Shannon's bound, \ the entropy: \ {d['entropy']:.2f} bits \\ (\textit{{AI, Built}}, \ Part 1)",
                  font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            'Huffman coding minimizes the weighted length of a binary prefix code for known symbol frequencies. '
            "<bookmark mark='a'/> Repeatedly merge the two lightest symbols or subtrees. <bookmark mark='b'/> Some "
            'optimal binary code tree puts two least-frequent symbols as deepest siblings; contracting that pair '
            "gives a smaller instance and the exchange proof. <bookmark mark='c'/> These frequencies come from "
            "letters and single spaces between words in thirty novels. We check the complete code's Kraft sum and "
            "weighted length against an independent merge-cost calculation. <bookmark mark='d'/> Entropy is a real-"
            'valued lower bound, not necessarily an attainable average for a one-symbol binary prefix code. Block '
            'coding can approach it under the corresponding source assumptions.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
