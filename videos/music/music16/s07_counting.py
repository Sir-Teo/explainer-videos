from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403


class Counting(SoundScene):
    def construct(self):
        chapter(self, 6, r"How many good lines?", r"How much freedom do the rules leave?")
        self.funnel()
        self.byhand()
        self.redundant()
        self.tune()

    # ------------------------------------------------------------------
    def funnel(self):
        d = load("counting")
        f = d["funnel"]
        g = axes([0, len(f) - 1], [2, 13], x_length=11.0, y_length=3.6, ylabel=r"lines that remain \ (powers of ten)", yticks=[3, 6, 9, 12], yfmt=lambda v: f"10^{{{int(v)}}}", font_size=20).move_to(DOWN * 0.6)
        xs = np.arange(len(f))
        ys = [np.log10(c) for _, c in f]
        dots = VGroup(*[Dot(g.ax.c2p(x, y), radius=0.07, color=TUNE) for x, y in zip(xs, ys)])
        line = curve_from(g, xs, ys, TUNE, stroke_width=3)
        names = VGroup(*[label(n.replace("no rules", "none"), font_size=16, color=GREY_B).rotate(0.6).next_to(g.ax.c2p(x, 2), DOWN, buff=0.35) for x, (n, _) in zip(xs, f)])
        top = label(rf"{d['total']:,} note sequences".replace(",", "{,}"), font_size=26, color=WHITE).next_to(dots[0], RIGHT, buff=0.2)
        end = label(rf"{d['valid']} good lines", font_size=30, color=TUNE).next_to(dots[-1], UP, buff=0.3)
        head = label(r"every first-species line over Fux's cantus firmus, \ counted", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "How much freedom do these rules leave? Monochord can count it exactly. Over Fux's cantus, "
            "the new voice may use fourteen notes in each bar, which gives "
            f"{say(d['total'] / 1e12, 1)} million million possible lines. <bookmark mark='a'/> Now add "
            "the rules one at a time and count what survives. Consonance alone removes all but one in "
            "four hundred. The rules for the beginning and the end remove most of the rest. The rules "
            "of melody cut deep. And when all twelve are in force, <bookmark mark='b'/> there are "
            f"{say(d['valid'])} good lines. Not one in thirty billion. The counting takes a fraction "
            "of a second, by dynamic programming: the rules only ever look one or two notes back, so "
            "the lines can be counted without being listed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(names), FadeIn(dots[0]), FadeIn(top))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(x) for x in dots[1:]], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("b")
            self.play(FadeIn(end))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def byhand(self):
        t = load("more")["toy"]
        cf, cells, edges = t["cf"], t["cells"], t["edges"]
        NAMES = ["C", "C$\\sharp$", "D", "E$\\flat$", "E", "F", "F$\\sharp$", "G", "G$\\sharp$", "A", "B$\\flat$", "B"]
        X = lambda i: -5.0 + 1.95 * i                                           # noqa: E731
        Y = lambda p: -2.35 + 0.235 * (p - 62)                                   # noqa: E731
        head = label(r"counting by hand: \ a five-note cantus, \ eight rules that look one note back", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        nodes, nums, names = {}, {}, VGroup()
        for i, col in enumerate(cells):
            for p, f, w in col:
                c = Circle(radius=0.25, stroke_color=GREY_B, stroke_width=2, fill_color=BLACK, fill_opacity=1).move_to([X(i), Y(p), 0])
                nodes[(i, p)] = c
                nums[(i, p)] = label(str(w), font_size=22, color=TUNE).move_to(c)
                names.add(label(NAMES[p % 12] + str(p // 12 - 1), font_size=16, color=GREY_B).next_to(c, LEFT, buff=0.08))
        links = VGroup(*[Line(nodes[(i, a)].get_center(), nodes[(i + 1, b)].get_center(), buff=0.27, color=DIM, stroke_width=2) for i, es in enumerate(edges) for a, b in es])
        cfl = VGroup(label(r"cantus:", font_size=22, color=CF_C).move_to([X(0) - 1.05, -3.25, 0]),
                     *[label(NAMES[p % 12], font_size=24, color=CF_C).move_to([X(i), -3.25, 0]) for i, p in enumerate(cf)])
        rule = VGroup(label(r"ways to finish from a note \\ = the sum of the ways \\ from the notes it may go to", font_size=24, color=WHITE),
                      label(rf"in all: \ {' + '.join(str(w) for _, _, w in cells[0])} = {t['total']}", font_size=26, color=TUNE)).arrange(DOWN, buff=0.4).move_to([5.0, 0.6, 0])
        rule[0].scale_to_fit_width(min(rule[0].width, 3.6))
        with self.voiceover(
            "How can anything count four million million lines without listing them? Here is the method, "
            "on a cantus of five notes, D, F, G, E, D, with eight of the rules: the ones that only compare a "
            "note with the note before it. <bookmark mark='a'/> Each column holds the notes the new voice "
            "may sing in that bar on some line that obeys the rules, and a line joins two notes when one "
            "may follow the other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cfl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in nodes.values()], lag_ratio=0.05), FadeIn(names), run_time=2.0)
            self.play(Create(links), run_time=2.0)
        cols = [[(i, p) for p, _, _ in col] for i, col in enumerate(cells)]
        with self.voiceover(
            "Now count backward, from the end. From each note of the last bar there is one way to "
            "finish: stop. <bookmark mark='a'/> Before it, the cadence allows only the leading note, C "
            "sharp: one way. <bookmark mark='b'/> In the middle bar, every note can go only to C sharp: "
            "one way each. <bookmark mark='c'/> In the second bar, each note can go to two of those: two "
            "ways each. <bookmark mark='d'/> And in the first bar, the number for each note is the sum of "
            "the numbers it can go to: four, four and six. <bookmark mark='e'/> Fourteen lines in all."
        ) as vo:
            self.play(*[FadeIn(nums[k]) for k in cols[4]])
            for mark, col in zip("abcd", cols[3::-1]):
                vo.wait_until(mark)
                self.play(*[FadeIn(nums[k]) for k in col], *[nodes[k].animate.set_stroke(TUNE) for k in col])
            vo.wait_until("e")
            self.play(FadeIn(rule))
        with self.voiceover(
            "Each number is found once and then reused. Add a bar, and the table grows by one column; "
            "the number of lines it counts is multiplied. Over Fux's cantus there are eleven columns, "
            "and since some rules look further back, a step back after a leap, no more than three "
            "parallel thirds, each cell also remembers the last move and the run of thirds. The method "
            "is the same, and it takes a fraction of a second."
        ):
            self.wait(0.5)
        pick = t["pick"]
        path = VGroup(*[Line(nodes[(i, a)].get_center(), nodes[(i + 1, b)].get_center(), buff=0.27, color=EAR, stroke_width=6) for i, (a, b) in enumerate(zip(pick, pick[1:]))])
        pr = t["probs"]
        chances = label(r"the first note, \ drawn: \\ " + r", \ ".join(rf"{NAMES[p % 12]}{p // 12 - 1} \ {round(q * t['total'])}/{t['total']}" for p, q in pr[0]), font_size=24, color=EAR).move_to([5.0, -2.0, 0])
        chances.scale_to_fit_width(min(chances.width, 3.7))
        with self.voiceover(
            "The same table draws a line at random with every good line equally likely, which is how "
            "the next chapter will take its samples. Choose the first note in proportion to its number: "
            "four chances in fourteen for the low D, four for A, six for the high D. <bookmark mark='a'/> Then "
            "each next note in proportion to its number, among the notes it may go to. This draw "
            "gives D in unison, A, E, C sharp, D. Over many draws, each of the fourteen lines comes up "
            "one time in fourteen."
        ) as vo:
            self.play(FadeIn(chances))
            vo.wait_until("a")
            self.play(*[nodes[(i, p)].animate.set_fill(EAR, opacity=0.35) for i, p in enumerate(pick)], Create(path), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def redundant(self):
        d = load("damage")
        rows = {r["rule"]: r for r in d["rows"]}
        t = VGroup(label(r"take away the rule against parallel fifths and octaves:", font_size=30, color=WHITE),
                   label(rf"still {d['full']} good lines. \ Not one more.", font_size=34, color=TUNE),
                   label(r"the stricter rule, \ no perfect consonance reached by similar motion, \ already forbids them all", font_size=26, color=GREY_A),
                   label(rf"take that one away instead: \ {rows['direct']['count']} lines", font_size=30, color=EAR)).arrange(DOWN, buff=0.35).move_to(UP * 0.2)
        with self.voiceover(
            "Counting also shows something no textbook mentions. Remove the most famous rule of all, "
            "the one against parallel fifths and octaves, and count again. <bookmark mark='a'/> Still "
            f"{say(d['full'])}. Not one line more. <bookmark mark='b'/> The reason is that a stricter "
            "rule is already in force: no perfect consonance may be reached by similar motion at all, "
            "and parallel motion is a kind of similar motion. <bookmark mark='c'/> Remove that rule "
            f"instead, and the number rises to {say(rows['direct']['count'])}. In first species, the "
            "famous rule does no work of its own. It is a special case, kept for its name."
        ) as vo:
            self.play(FadeIn(t[0]))
            vo.wait_until("a")
            self.play(FadeIn(t[1]))
            vo.wait_until("b")
            self.play(FadeIn(t[2]))
            vo.wait_until("c")
            self.play(FadeIn(t[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tune(self):
        d = load("counting")
        rows = VGroup(label(r"the whole Tune as a cantus firmus: \ 42 notes", font_size=30, color=WHITE),
                      label(rf"note sequences: \ a number with {d['tune_digits']} digits", font_size=28, color=GREY_A),
                      label(rf"good first-species lines: \ {d['tune_count']:,}".replace(",", "{,}"), font_size=34, color=TUNE),
                      label(rf"played one after another, \ day and night: \ {d['years']:,.0f} years".replace(",", "{,}"), font_size=28, color=GREY_A)).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        with self.voiceover(
            "And the rules still leave room for a lifetime of music. Take the whole Tune, forty-two "
            "notes, as a cantus firmus. <bookmark mark='a'/> The possible lines are a number with fifty "
            f"digits. <bookmark mark='b'/> The good ones number about {say(d['tune_count'] / 1e9)} "
            "billion. <bookmark mark='c'/> Played one after another without stopping, they would take "
            f"some {say(round(d['years'], -3))} years. The rules remove almost everything, and what "
            "they leave is still more than anyone will ever hear. That is why Fux's exercises could "
            "occupy a student for years: the rules rule out the bad, and leave the choosing to you."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()
