from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403


class WhatFor(VoiceoverScene):
    def construct(self):
        self.card()
        self.memory()
        self.pooled()
        self.dreams()

    def card(self):
        card = chapter_card(7, r"What sleep is for", r"One answer with experiments behind it, \ and one argument", lit=(),
                            part=PART, scale=("brain", "mind"), marr=("what",))
        with self.voiceover(
            "Chapter seven. What sleep is for."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def memory(self):
        head = heading(r"A reminder, \ delivered in deep sleep")
        g = np.random.default_rng(2)
        shown = set(g.choice(30, size=6, replace=False).tolist())
        cards = VGroup(*[RoundedRectangle(width=0.62, height=0.78, corner_radius=0.06, color=GREY_B, stroke_width=2,
                                          fill_color=THRESH if i in shown else GREY_D,
                                          fill_opacity=0.85 if i in shown else 0.35) for i in range(30)])
        cards.arrange_in_grid(rows=5, cols=6, buff=0.1).move_to([-4.6, 0.1, 0])
        ccap = wrapped_label(r"learn where the pairs lie, \ in a room that smells of roses", 4.4, 27, WHITE)
        ccap.next_to(cards, DOWN, buff=0.2)
        conds = [
            (r"roses while learning; \ again in deep sleep", r"more remembered", MODEL),
            (r"roses while learning; \ again in REM sleep", r"no gain", GREY_A),
            (r"roses while learning; \ again while awake", r"no gain", GREY_A),
            (r"no roses while learning; \ roses in deep sleep", r"no gain", GREY_A),
        ]
        table = VGroup()
        for i, (what, res, col) in enumerate(conds):
            y = 1.85 - 0.95 * i
            a = wrapped_label(what, 5.0, 28, WHITE)
            a.move_to([0, y, 0]).align_to(np.array([-1.9, 0, 0]), LEFT)
            b = label(res, font_size=30, color=col)
            b.move_to([0, y, 0]).align_to(np.array([3.75, 0, 0]), LEFT)
            table.add(VGroup(a, b))
        keep_in_frame(table)
        end = wrapped_label(r"Not the smell, \ and not sleep in general: \ a reminder in deep sleep. \ The idea: \ the "
                            r"hippocampus replays the day to the cortex, \ and the odour prompted the replay.", 8.6, 28,
                            THRESH).move_to([2.35, -2.35, 0])
        keep_in_frame(end)
        src = published_tag(archive.RASCH_2007.cite)
        with self.voiceover(
            "What is all this for? There are many proposals, and one of them has experiments behind it: "
            "memory. <bookmark mark='a'/> In 2007 Björn Rasch and Jan Born, in Germany, had volunteers "
            "learn where pairs of cards lay on a board, as in the children's game, in a room that smelled "
            "of roses. <bookmark mark='b'/> That night, in deep slow-wave sleep, some of them were given "
            "the smell of roses again. They didn't wake, and they didn't know. Next morning they "
            "remembered more of the card locations than sleepers who'd had no odour. "
            "<bookmark mark='c'/> Then the controls, which make it an experiment and not an anecdote. The "
            "odour in REM sleep: no gain. The odour while awake: no gain. The odour in deep sleep, when "
            "there had been none during learning: no gain. <bookmark mark='d'/> So it isn't the smell, "
            "and it isn't sleep in general. It's a reminder, delivered in deep sleep. The idea behind it "
            "is that during slow-wave sleep the hippocampus, from Part 7, replays the day's new memories "
            "to the cortex, and that the odour prompted the replay."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(cards, lag_ratio=0.02), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(ccap))
            vo.wait_until("b")
            self.play(FadeIn(table[0][0]))
            self.wait(6.0)
            self.play(FadeIn(table[0][1], scale=1.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in table[1:]], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def pooled(self):
        r = archive.RASCH_2007.data
        g, lo, hi = r["g"], r["g_lo"], r["g_hi"]
        head = heading(rf"{r['experiments']} experiments later")
        A = axes([-0.2, 0.6], [0, 3.6], x_length=6.4, y_length=2.4, xticks=[-0.2, 0, 0.2, 0.4, 0.6], yticks=[],
                 xfmt=lambda v: f"{v:.1f}", xlabel=r"effect of the cue, \ in standard deviations", ylabel=r"",
                 center=[-3.4, 1.15, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 3.6), color=GREY_C, stroke_width=2)
        whisk = VGroup(Line(ax.c2p(lo, 2.8), ax.c2p(hi, 2.8), color=MODEL, stroke_width=6),
                       Dot(ax.c2p(g, 2.8), radius=0.12, color=MODEL))
        wl = label(rf"deep and light sleep: \ ${g:.2f}$", font_size=27, color=MODEL).next_to(whisk, UP, buff=0.12)
        others = VGroup(*[VGroup(Dot(ax.c2p(0, y), radius=0.1, color=GREY_A),
                                 label(name, font_size=27, color=GREY_A).next_to(ax.c2p(0, y), RIGHT, buff=0.25))
                          for name, y in ((r"REM sleep: \ none", 1.7), (r"awake: \ none", 0.7))])
        B = axes([-3.5, 3.8], [0, 0.45], x_length=6.4, y_length=1.7, xticks=[], yticks=[], xlabel=r"", ylabel=r"",
                 center=[-3.4, -1.9, 0])
        x = np.linspace(-3.5, 3.8, 200)
        bell = lambda m: np.exp(-(x - m) ** 2 / 2) / np.sqrt(TAU)  # noqa: E731
        c0 = curve(B.ax, x, bell(0), GREY_A, stroke_width=4)
        c1 = curve(B.ax, x, bell(g), MODEL, stroke_width=4)
        bcap = label(rf"two groups, \ ${g:.2f}$ standard deviations apart", font_size=26, color=GREY_A).next_to(B, DOWN, buff=0.1)
        rows = rows_of([
            (rf"{r['experiments']} experiments, \ {num(r['people'])} people: \ memories cued in sleep with sounds or smells",
             WHITE),
            (rf"pooled: \ ${g:.2f}$, \ between ${lo:.2f}$ and ${hi:.2f}$; \ nothing in REM sleep or awake", MODEL),
            (r"real, and small: \ the two groups mostly overlap", GREY_A),
            (r"a neighbouring method, \ clicks timed to the slow waves: \ the reported effects have shrunk year by year",
             BAD),
            (r"sleep helps hold on to what was learned. \ Whether that is what sleep is for is another question", THRESH),
        ], 5.2, 28, 0.24).move_to([4.2, -0.3, 0])
        keep_in_frame(rows)
        src = published_tag(archive.RASCH_2007.cite)
        tag = note(r"the pooled estimate: Hu et al.\ (2020), in the same Archive entry").to_corner(DR, buff=0.3)
        with self.voiceover(
            f"One study is one study. By 2020 there were {r['experiments']} experiments of this kind, "
            "with two thousand people, cueing memories in sleep with sounds or smells. "
            f"<bookmark mark='a'/> Pooled, the effect in non-REM sleep is {g:.2f} of a standard "
            f"deviation, somewhere between {lo:.2f} and {hi:.2f}. In REM sleep, and in waking: nothing. "
            "<bookmark mark='b'/> So the finding holds. Now look at its size. These two curves are that "
            "far apart. Cueing in sleep moves the average a little, and the two groups mostly overlap. "
            "<bookmark mark='c'/> And for a neighbouring method, playing clicks timed to the slow waves "
            "to make them larger, the reported effects have shrunk year by year as the studies got "
            "bigger. Part 4 told you to expect that. <bookmark mark='d'/> So sleep helps hold on to what "
            "you learned. That much is as solid as anything in this part. Whether that's what sleep is "
            "for is another question, and it's waiting at the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A), FadeIn(zero), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(whisk), FadeIn(wl), FadeIn(others, lag_ratio=0.4), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(B), Create(c0), Create(c1), FadeIn(bcap), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4], shift=UP * 0.1))
        self.clear_scene()

    def dreams(self):
        head = heading(r"And dreams? \ Two accounts, \ and no agreement")

        def card(title, body, col, x):
            t = label(title, font_size=31, color=col)
            b = wrapped_label(body, 5.6, 28, WHITE)
            inner = VGroup(t, b).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            box = RoundedRectangle(width=6.3, height=inner.height + 0.5, corner_radius=0.14, color=col, stroke_width=2.5,
                                   fill_color=col, fill_opacity=0.07)
            g = VGroup(box, inner)
            inner.move_to(box)
            return g.move_to([x, 0, 0])

        left = card(r"1977: \ Hobson and McCarley", r"in REM sleep the brainstem fires signals up into the forebrain, \ more "
                    r"or less at random; \ the forebrain does what it always does with input: \ it makes a story", SLEEPC, -3.4)
        right = card(r"2000: \ Solms", r"in patients, \ brainstem damage that ends REM sleep can leave dreaming; \ damage in "
                     r"the forebrain can end dreaming and leave REM sleep", REMC, 3.4)
        VGroup(left, right).set_y(1.55)
        left.align_to(right, UP)
        cols = [r"brainstem damage", r"forebrain damage"]
        cells = [[(r"gone", BAD), (r"intact", MODEL)], [(r"intact", MODEL), (r"gone", BAD)]]
        frame, table = VGroup(), VGroup()
        xs, ys = [-0.2, 3.4], [-1.2, -1.95]
        for j, name in enumerate(cols):
            frame.add(label(name, font_size=29, color=GREY_A).move_to([xs[j], -0.45, 0]))
        for i, name in enumerate((r"REM sleep", r"dreaming")):
            frame.add(label(name, font_size=31, color=WHITE).move_to([-3.6, ys[i], 0]))
            for j in range(2):
                txt, col = cells[i][j]
                frame.add(Line([xs[j] - 0.5, ys[i] - 0.22, 0], [xs[j] + 0.5, ys[i] - 0.22, 0], color=GREY_D, stroke_width=2))
                table.add(label(txt, font_size=34, color=col).move_to([xs[j], ys[i], 0]))
        dd = label(r"a double dissociation \ (Part 7)", font_size=29, color=THRESH).move_to([0, -2.7, 0])
        end = label(r"what dreams are for, \ if anything: \ open", font_size=29, color=GREY_A).move_to([0, -3.25, 0])
        src = published_tag(archive.HOBSON_1977.cite)
        with self.voiceover(
            "And dreams? Here there's no agreement, so here are the two sides. <bookmark mark='a'/> In "
            "1977 Allan Hobson and Robert McCarley, at Harvard, proposed that a dream begins in the "
            "brainstem. During REM sleep it fires signals up into the forebrain, more or less at random, "
            "and the forebrain does what it always does with its input: it makes a story. On that view, "
            "the plot of a dream is the cortex making the best of noise. <bookmark mark='b'/> In 2000 the "
            "neuropsychologist Mark Solms answered with patients. Damage in the brainstem that abolishes "
            "REM sleep can leave dreaming intact. And damage in parts of the forebrain can abolish "
            "dreaming, and leave REM sleep untouched. <bookmark mark='c'/> That's the pattern Part 7 "
            "taught you to look for: a double dissociation. It says REM sleep and dreaming are run by "
            "different machinery, even though they usually keep company. And people woken from the other "
            "stages report dreams too, only less often. <bookmark mark='d'/> Hobson revised his theory, "
            "Solms pressed his, and the argument isn't over. What dreams are for, or whether they're for "
            "anything, nobody can yet say. So it goes on the screen as it is: open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(left[0]), FadeIn(right[0]), FadeIn(left[1][0]), FadeIn(right[1][0]),
                      FadeIn(frame))
            vo.wait_until("a")
            self.play(FadeIn(left[1][1]))
            vo.wait_until("b")
            self.play(FadeIn(right[1][1]))
            vo.wait_until("c")
            self.play(FadeIn(table, lag_ratio=0.1), FadeIn(dd), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()
