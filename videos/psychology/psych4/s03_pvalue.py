from __future__ import annotations

import numpy as np

from videos.psychology.psych4.common import *  # noqa: F403

NOT = [
    r"the chance that the result is a fluke",
    r"the chance that the hypothesis is false",
    r"one minus the chance that the effect is real",
    r"a measure of how big the effect is",
    r"the chance that a repeat would fail",
    r"evidence of no effect, when it is large",
]


class PValue(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.is_not()

    def card(self):
        card = chapter_card(2, r"What a p-value is", r"What question does a p-value answer?",
                            lit={1925: r"Fisher's \emph{Statistical Methods}"}, part=PART, scale=("group",),
                            marr=("what",))
        with self.voiceover(
            "Chapter two. What a p-value is."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def definition(self):
        d = load("pvalue")
        head = heading(r"One study, and the world in which the treatment does nothing")
        edges, dens = np.asarray(d["edges"]), np.asarray(d["density"])
        top = float(dens.max()) * 1.2
        A = axes([-14, 14], [0, top], x_length=8.2, y_length=3.6, xticks=[-12, -8, -4, 0, 4, 8, 12],
                 xlabel=r"difference between the groups if the game did nothing (ms)", center=[-2.3, -0.5, 0])
        ax = A.ax
        obs = d["observed"]
        centre = (edges[:-1] + edges[1:]) / 2
        body = hist(ax, edges, np.where(np.abs(centre) < abs(obs), dens, 0), NULLC, 0.6)
        tails = hist(ax, edges, np.where(np.abs(centre) >= abs(obs), dens, 0), SIG, 0.95)
        mark = DashedLine(ax.c2p(obs, 0), ax.c2p(obs, top * 0.9), color=TRUTH, stroke_width=3)
        mlab = label(rf"this study: \ ${obs:.1f}$ ms", font_size=24, color=TRUTH).next_to(mark, UP, buff=0.06)
        mirror = DashedLine(ax.c2p(-obs, 0), ax.c2p(-obs, top * 0.55), color=SIG, stroke_width=2)
        side = VGroup(
            wrapped_label(rf"{d['n']} people, shuffled into two groups; \ the game group is {abs(obs):.1f} ms "
                          r"faster", 4.6, 26, WHITE),
            wrapped_label(rf"suppose the game did nothing, and reshuffle {fmt_int(d['shuffles'])} times", 4.6, 26,
                          NULLC),
            wrapped_label(rf"a difference this large, in either direction: \ {d['as_extreme']} times", 4.6, 26, SIG),
            label(rf"$p = {p_text(d['p'])}$", font_size=54, color=SIG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([4.6, 0.3, 0])
        defn = label(r"p: \ how often a result at least this extreme would turn up, \emph{if nothing were going on}",
                     font_size=28, color=P.ACCENT).to_edge(DOWN, buff=0.75)
        tag = simulated_tag()
        # the opening picture: Part 2's deck, dealt into two groups and dealt again
        rng_ = np.random.default_rng(4)
        deck = VGroup(*[RoundedRectangle(width=0.5, height=0.72, corner_radius=0.07, stroke_width=0,
                                         fill_color=(TRUTH if i < 8 else NULLC), fill_opacity=0.9) for i in range(16)])
        slots = [np.array([-5.2 + 0.72 * (i % 8), 0.55 - 1.1 * (i // 8), 0]) for i in range(16)]
        for c_, s_ in zip(deck, slots):
            c_.move_to(s_)
        deck_l = VGroup(label(r"played the game", font_size=24, color=TRUTH).next_to(slots[7], RIGHT, buff=0.5),
                        label(r"did not", font_size=24, color=NULLC).next_to(slots[15], RIGHT, buff=0.5))
        deals = [rng_.permutation(16) for _ in range(3)]
        with self.voiceover(
            "You met this picture in Part 2, with a deck of cards. It's worth one more look, because everything "
            f"in this part hangs on it. <bookmark mark='a'/> Two hundred people, shuffled into two groups. The "
            f"group that played the game is {abs(obs):.1f} milliseconds faster. Is that the game, or the luck of "
            "the shuffle? <bookmark mark='b'/> Imagine a world in which the game does nothing at all. In that "
            "world each person's score would be the same whichever group they'd landed in. So reshuffle the "
            "labels, twenty thousand times, and see what differences that world produces. <bookmark mark='c'/> "
            f"A difference as large as ours, in either direction, turns up {d['as_extreme']} times. That share, "
            f"{d['p']:.3f}, is the p-value. <bookmark mark='d'/> Read the definition slowly. It's a statement "
            "about the data, made inside an imaginary world where nothing is going on. It says: in that world, "
            "a result like this would be rare. It doesn't say that world is unlikely."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(deck, lag_ratio=0.05), FadeIn(deck_l), run_time=1.5)
            for perm in deals:
                self.play(*[c_.animate.move_to(slots[j]) for c_, j in zip(deck, perm)], run_time=1.6)
            vo.wait_until("a")
            self.play(FadeOut(deck), FadeOut(deck_l), FadeIn(A), run_time=0.8)
            self.play(FadeIn(side[0]), Create(mark), FadeIn(mlab))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(body, lag_ratio=0.03), FadeIn(tails, lag_ratio=0.03), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(mirror), FadeIn(side[2]))
            self.play(FadeIn(side[3], scale=1.2))
            vo.wait_until("d")
            self.play(FadeIn(defn, shift=UP * 0.15))
        self.clear_scene()

    def is_not(self):
        head = heading(r"Six things a p-value is not")
        rows = VGroup()
        for i, t in enumerate(NOT):
            x = VGroup(Line(UL * 0.13, DR * 0.13, color=BAD, stroke_width=5), Line(UR * 0.13, DL * 0.13, color=BAD,
                                                                              stroke_width=5))
            rows.add(VGroup(x, label(t, font_size=32, color=WHITE)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.45, 0])
        end = VGroup(
            label(r"It is the probability of data like these, given no effect.", font_size=30, color=P.ACCENT),
            label(r"What you want is the probability of an effect, given these data. \ That needs more than p.",
                  font_size=28, color=WHITE),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "It's easier to say what a p-value isn't, because it's misread constantly, by students and by working "
            "researchers. <bookmark mark='a'/> It isn't the chance that the result is a fluke. "
            "<bookmark mark='b'/> It isn't the chance that your hypothesis is false. <bookmark mark='c'/> One "
            "minus p isn't the chance that the effect is real. <bookmark mark='d'/> It isn't a measure of size, "
            "as you just saw. <bookmark mark='e'/> It doesn't tell you how often a repeat of the study would "
            "fail. <bookmark mark='f'/> And a large p-value isn't evidence that there's no effect. It may only "
            "mean the study was too small to see one. <bookmark mark='g'/> All six mistakes come from turning "
            "the sentence round. The p-value is the probability of data like these, given that there's no effect. "
            "What everyone wants is the probability that there's an effect, given these data. To get from one to "
            "the other you need to know how likely the effect was to begin with, and how likely the study was to "
            "find it. Those are the next two chapters. The derivations are in Statistics, Built, Part 10."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15), run_time=0.7)
            vo.wait_until("g")
            self.play(FadeIn(end[0], shift=UP * 0.15))
            self.play(FadeIn(end[1]))
        self.clear_scene()
