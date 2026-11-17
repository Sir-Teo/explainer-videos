from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403

CAP_COL = [LOST, SPEED, VERB, GOOD]


class Raven(VoiceoverScene):
    def construct(self):
        self.card()
        self.carpenter()
        self.solver()
        self.rests_on()

    def card(self):
        card = chapter_card(8, r"What it rests on", r"What does a matrix item actually ask of a mind?",
                            lit={1938: r"Raven", 1990: r"Carpenter, \ Just \& Shell"}, part=PART,
                            scale=("brain", "mind", "person"), marr=("how",))
        with self.voiceover("Chapter eight. What it rests on."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def carpenter(self):
        d = load("matrices")
        head = heading(r"What one intelligence test measures")
        panel = matrix_panel(d["grid3"], cell=0.7).move_to([-4.0, 0.2, 0])
        rows = rows_of([
            (r"Patricia Carpenter, \ Marcel Just and Peter Shell, \ 1990: \ students solving Raven's Advanced "
             r"Progressive Matrices, \ with eye tracking and thinking aloud", WHITE),
            (r"people solved an item by finding rules attribute by attribute, \ comparing along rows, \ one rule at a "
             r"time", VERB),
            (r"the number of rules an item contained explained 57\% of the variation in how hard items were", G),
            (r"two programs: \ FAIRAVEN, \ which solved items as well as a median student, \ and BETTERAVEN, \ as well "
             r"as the best, \ by managing more rules and goals at once", MODEL),
        ], 7.6, 22, 0.36).move_to([2.6, -0.2, 0])
        tag = published_tag(r"Carpenter, \ Just \& Shell (1990)")
        with self.voiceover(
            "If g is real, what is it made of? One way in is to ask what the purest test of it actually demands. "
            "<bookmark mark='a'/> In 1990 Patricia Carpenter, Marcel Just and Peter Shell watched students solve "
            "Raven's Advanced Progressive Matrices, tracking their eyes and recording them thinking aloud. "
            "<bookmark mark='b'/> People solved an item by finding the rules attribute by attribute, comparing "
            "along the rows, one rule at a time. <bookmark mark='c'/> The number of rules an item contained "
            "explained fifty-seven percent of the variation in how hard the items were. <bookmark mark='d'/> They "
            "wrote two programs. FAIRAVEN solved items about as well as a median student; BETTERAVEN, as well as "
            "the best, and the difference was its ability to manage more rules and goals at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(panel))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def solver(self):
        d = load("matrices")
        head = heading(r"Psyche's solver: \ rules held at once")
        A = axes([-0.3, 4.3], [0, 1.05], x_length=6.2, y_length=4.2, xticks=[0, 1, 2, 3, 4],
                 yticks=[0, 0.25, 0.5, 0.75, 1.0], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"rules in the item", ylabel=r"accuracy", center=[-2.9, -0.4, 0], font_size=15)
        ks = np.arange(5)
        curves = VGroup(*[curve(A.ax, ks, d[f"acc_cap{c}"], CAP_COL[i], stroke_width=3) for i, c in enumerate((1, 2, 3, 4))])
        pop = curve(A.ax, ks, d["acc_pop"], WHITE, stroke_width=6)
        pop_dots = scatter(A.ax, ks, d["acc_pop"], WHITE, radius=0.07)
        key = legend([(CAP_COL[i], rf"holds {c} rule{'s' if c > 1 else ''}") for i, c in enumerate((1, 2, 3, 4))] +
                     [(WHITE, r"a population")], font_size=16).move_to(A.ax.c2p(0.9, 0.3))
        rows = rows_of([
            (r"items generated from rules: \ constant, \ a step along the row, \ or three values cycling", WHITE),
            (r"the solver infers each attribute's rule and rejects options that break it, \ but can track only so many "
             r"rules; \ for the rest it guesses", MODEL),
            (rf"a population with mixed capacities: \ {pct(d['acc_pop'][1])} of one-rule items, \ "
             rf"{pct(d['acc_pop'][3])} of three-rule items, \ {pct(d['acc_pop'][4])} of four", G),
            (r"difficulty set by how many rules must be held at once: \ working memory, \ Part 19", VERB),
        ], 5.6, 21, 0.36).move_to([3.6, -0.2, 0])
        tag = psyche_tag(r"\texttt{traits.matrix\_item, \ solve}")
        with self.voiceover(
            "Psyche builds the same idea. <bookmark mark='a'/> Its items are generated from rules: an attribute is "
            "constant, steps along the row, or cycles through three values. <bookmark mark='b'/> Its solver infers "
            "each attribute's rule and rejects the options that break it, but it can keep track of only so many "
            "rules; for the rest, it guesses. Each coloured line is a solver of one capacity. "
            "<bookmark mark='c'/> A population with mixed capacities gets "
            f"{spct(d['acc_pop'][1])} of one-rule items right, {spct(d['acc_pop'][3])} of three-rule items, and "
            f"{spct(d['acc_pop'][4])} of four. <bookmark mark='d'/> Difficulty is set by how many rules must be "
            "held at once, which is working memory, the subject of Part 19."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(key), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(pop), FadeIn(pop_dots), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def rests_on(self):
        head = heading(r"Three foundations, \ none of them the whole")
        cols = VGroup()
        for t, body, c in (
            (r"working memory", r"holding and updating several things at once; \ working-memory capacity and fluid "
             r"reasoning correlate strongly, \ though not perfectly \ (Part 19)", VERB),
            (r"speed", r"simple reaction and inspection times correlate modestly with IQ; \ a slower system runs out "
             r"of time \ (Part 31's speed theory)", SPEED),
            (r"the brain", r"total brain volume and the efficiency of networks correlate modestly with scores; \ the "
             r"associations are small, \ and need large samples \ (Part 8)", VIS)):
            cols.add(VGroup(word_chip(t, color=c, font_size=26, width=3.8), wrapped_label(body, 3.9, 23, WHITE))
                     .arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to([0, 0.5, 0])
        foot = wrapped_label(r"each explains part of the variance in $g$; \ none reduces it: \ $g$ is a summary of "
                             r"many processes, \ not yet a mechanism", 12.0, 22, YOU).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Three foundations are usually proposed. <bookmark mark='a'/> Working memory: holding and updating "
            "several things at once. Working-memory capacity and fluid reasoning correlate strongly, though not "
            "perfectly. <bookmark mark='b'/> Speed: simple reaction times and inspection times correlate modestly "
            "with IQ, and a slower system runs out of time. <bookmark mark='c'/> And the brain: total brain volume "
            "and the efficiency of brain networks correlate modestly with scores, though the associations are small "
            "and need large samples, as Part 8 warned. <bookmark mark='d'/> Each explains part of the variance in g. "
            "None reduces it. For now g is a summary of many processes, not yet a mechanism."
        ) as vo:
            self.play(FadeIn(head))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
