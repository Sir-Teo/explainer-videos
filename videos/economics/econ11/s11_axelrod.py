from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

NAMES = {"ALLC": r"always cooperate", "ALLD": r"always defect", "TFT": r"tit for tat", "GRIM": r"grim trigger",
         "TF2T": r"tit for two tats", "WSLS": r"win-stay, lose-shift", "GTFT": r"generous tit for tat",
         "RANDOM": r"random", "JOSS": r"Joss (sneaky)"}
NICE = {"ALLC", "TFT", "GRIM", "TF2T", "WSLS", "GTFT"}


def strip(moves, y, size=0.22):
    g = VGroup(*[Square(side_length=size, stroke_width=0, fill_color=COOP if m else DEFECT, fill_opacity=0.9)
                 for m in moves]).arrange(RIGHT, buff=0.04)
    return g.move_to(UP * y)


class Axelrod(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Axelrod's tournaments", r"Which strategy does best when the game is played again and again?",
             "Chapter nine. Axelrod's tournaments.", lit={1980: r"Axelrod's tournaments"}, scale=("person",),
             horizon=("a year",))
        self.history()
        self.agora()
        self.noise()

    def history(self):
        ax_ = load("tournament")["axelrod"]
        hc = history_card(1980, r"Robert Axelrod", rf"a computer tournament: \ {ax_['first_entries']} programs, \ "
                          rf"each meeting every other for {ax_['first_rounds']} rounds of the prisoner's dilemma",
                          color=COOP, width=11.4, font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"the winner was the shortest program entered: \ tit for tat, \ by Anatol Rapoport", font_size=24,
                  color=COOP),
            label(r"cooperate first; \ then do whatever the other did last round", font_size=24),
            label(r"a second tournament, \ with more than sixty entries who knew the result: \ tit for tat again",
                  font_size=23, color=COOP),
            label(r"Axelrod's reading: \ be nice, \ retaliate, \ forgive, \ be clear", font_size=25, color=EQ),
            label(r"and a warning: \ tit for two tats would have won the first, \ had anyone entered it", font_size=23,
                  color=HOLD),
        ).arrange(DOWN, buff=0.35).next_to(hc, DOWN, buff=0.55)
        tag = published_tag(r"Axelrod, Journal of Conflict Resolution 24 (1980); \ \emph{The Evolution of "
                            r"Cooperation} (1984)", corner=DR, font_size=13)
        with self.voiceover(
            "If the game goes on, which strategy is best? It depends on what the others play, so in 1980 Robert "
            "Axelrod asked people to submit programs and let them fight it out. <bookmark mark='a'/> Fourteen "
            "programs met each other for two hundred rounds each. The winner was the shortest one entered: tit for "
            "tat, sent in by the psychologist Anatol Rapoport. <bookmark mark='b'/> It cooperates in the first round, "
            "and then does whatever the other did in the round before. <bookmark mark='c'/> Axelrod ran a second "
            "tournament, with more than sixty entries from people who knew the first result. Tit for tat won again. "
            "<bookmark mark='d'/> His reading: successful strategies are nice, never defecting first; they "
            "retaliate; they forgive; and they are clear enough that others learn how to deal with them. "
            "<bookmark mark='e'/> He also noted that a more forgiving rule, tit for two tats, would have won the first "
            "tournament if anyone had entered it. Who wins depends on who else plays."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def agora(self):
        t = load("tournament")
        field = t["field"]
        sc = np.array(t["clean"]["score"])
        order = np.argsort(-sc)
        bars = VGroup()
        for rank, i in enumerate(order):
            k = field[i]
            col = COOP if k in NICE else DEFECT
            g = VGroup(label(NAMES[k], font_size=18, color=col),
                       Rectangle(width=2.0 * (sc[i] - 1.5), height=0.26, stroke_width=0, fill_color=col,
                                 fill_opacity=0.8),
                       label(f"{sc[i]:.2f}", font_size=16, color=col))
            bars.add(g)
        for g in bars:
            g[0].set_width(min(g[0].width, 2.4))
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        x0 = max(g[0].get_right()[0] for g in bars) + 0.2
        for g in bars:
            g[1].align_to(np.array([x0, 0, 0]), LEFT)
            g[2].next_to(g[1], RIGHT, buff=0.1)
        bars.to_edge(LEFT, buff=0.5).shift(UP * 0.4)
        bh = label(r"points per round, \ Agora's round robin", font_size=18, color=GREY_A).next_to(bars, UP, buff=0.2)
        eco = np.array(t["eco"])
        ax = plane([0, 150], [0, 0.25], center=RIGHT * 3.3 + DOWN * 0.2, x_length=5.2, y_length=4.0,
                   xticks=[0, 50, 100, 150], yticks=[0, 0.1, 0.2], xlabel=r"generations", ylabel=r"share of the "
                   r"population", font_size=15)
        gens = np.arange(len(eco))
        curves = VGroup(*[path(ax, gens, eco[:, i], color=COOP if k in NICE else DEFECT, width=2.5, smooth=False)
                          for i, k in enumerate(field)])
        notes = VGroup(
            label(r"nice strategies take over; \\ the exploiters starve", font_size=19, color=COOP),
        ).next_to(ax, DOWN, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Agora reruns the idea with nine classic strategies, each meeting every other, and a copy of itself, for "
            "two hundred rounds. <bookmark mark='a'/> In this field tit for two tats comes first and tit for tat "
            "fifth, just as Axelrod warned: the ranking depends on the field. But look at the pattern. The nice "
            "strategies, in green, take the top six places; always defecting comes last. "
            "<bookmark mark='b'/> Axelrod also ran an ecological version: let each strategy's share of the "
            "population grow in proportion to its score, generation after generation. "
            "<bookmark mark='c'/> Generation after generation the exploiters shrink, because the strategies they feed "
            "on are outnumbered by ones that punish them, and the nice strategies take over."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(bh), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars],
                                                         lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(ax))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.1), FadeIn(notes), run_time=3)
        self.clear_scene()

    def noise(self):
        t = load("tournament")
        n = 30
        a, b = t["tft_moves"]
        c, d = t["wsls_moves"]
        s1, s2 = strip(a[:n], 2.0), strip(b[:n], 1.65)
        s3, s4 = strip(c[:n], 0.2), strip(d[:n], -0.15)
        l1 = label(r"tit for tat against itself, \ one mistake in round 5", font_size=20, color=GREY_A).next_to(
            s1, UP, buff=0.2)
        l2 = label(r"win-stay, lose-shift against itself, \ the same mistake", font_size=20, color=GREY_A).next_to(
            s3, UP, buff=0.2)
        noisy = t["noisy"]["ranking"]
        rows = VGroup(
            label(r"one slip, \ and tit for tat echoes it: \ punish, \ be punished, \ round after round", font_size=22,
                  color=DEFECT),
            label(r"win-stay, lose-shift: \ repeat what worked, \ change what didn't; \ it repairs a slip in two "
                  r"rounds", font_size=22, color=COOP),
            label(rf"with 5\% of moves mistaken, \ Agora's round robin is won by {NAMES[noisy[0]]}; \ tit for tat is "
                  rf"{noisy.index('TFT') + 1}th", font_size=22, color=EQ),
            label(r"Nowak and Sigmund (1993): \ in noisy worlds, \ forgiveness and repair beat strict reciprocity",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Nowak and Sigmund, Nature 364 (1993)", corner=DR, font_size=13)
        with self.voiceover(
            "Real relationships have accidents: a misunderstanding, a missed delivery. <bookmark mark='a'/> Here is "
            "tit for tat against itself, with one move in round five coming out wrong. One slip, and tit for tat "
            "echoes it: each punishes the other's punishment, round after round, for ever, unless another accident "
            "breaks the cycle. "
            "<bookmark mark='b'/> A different rule, win-stay, lose-shift, repeats its move if the last round went "
            "well and switches if it didn't. After the slip, both defect once, both switch back, and cooperation is "
            "repaired in two rounds. <bookmark mark='c'/> Run the whole round robin with five percent of moves "
            "mistaken, and win-stay, lose-shift comes first, with tit for tat fifth. <bookmark mark='d'/> Martin Nowak and Karl Sigmund showed "
            "in 1993 that in a noisy world, strategies that forgive and repair beat strict reciprocity."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(l1), FadeIn(s1), FadeIn(s2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(l2), FadeIn(s3), FadeIn(s4), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
