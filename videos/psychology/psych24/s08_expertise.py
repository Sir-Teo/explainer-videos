from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403


def board(center=(0, 0, 0), size: float = 2.6, pieces=(), color=CONTENT) -> VGroup:
    """A small chess board with pieces as dots at (file, rank) squares 0..7."""
    c = np.array(center, float)
    s = size / 8
    sq = VGroup(*[Square(s, stroke_width=0, fill_color="#2B3240" if (i + j) % 2 else "#3A4354", fill_opacity=1)
                  .move_to(c + np.array([(i - 3.5) * s, (j - 3.5) * s, 0])) for i in range(8) for j in range(8)])
    ps = VGroup(*[Dot(c + np.array([(f - 3.5) * s, (r - 3.5) * s, 0]), radius=s * 0.32, color=col)
                  for f, r, col in pieces])
    return VGroup(sq, ps)


GAME = [(4, 0, WHITE), (5, 1, WHITE), (6, 1, WHITE), (7, 1, WHITE), (6, 0, WHITE), (5, 0, WHITE), (3, 1, WHITE),
        (2, 2, WHITE), (4, 3, WHITE), (0, 0, WHITE), (6, 7, GREY_B), (5, 6, GREY_B), (6, 6, GREY_B), (7, 6, GREY_B),
        (5, 7, GREY_B), (3, 6, GREY_B), (2, 5, GREY_B), (4, 4, GREY_B), (0, 7, GREY_B), (1, 6, GREY_B)]


class Expertise(VoiceoverScene):
    def construct(self):
        self.card()
        self.chess()
        self.practice()

    def card(self):
        card = chapter_card(7, r"Expertise", r"What does an expert know that a novice does not?",
                            lit={1946: r"de Groot", 1973: r"Chase \& Simon", 1993: r"Ericsson et al.",
                                 2014: r"Macnamara et al."},
                            part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter seven. Expertise."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def chess(self):
        head = heading(r"Five seconds of a chess position")
        rng = np.random.default_rng(73)
        sq = rng.choice(64, len(GAME), replace=False)
        RANDOM = [(int(k % 8), int(k // 8), col) for k, (_, _, col) in zip(sq, GAME)]
        b1 = board((-4.6, 0.9, 0), 2.6, GAME)
        b2 = board((-1.6, 0.9, 0), 2.6, RANDOM)
        l1 = label(r"from a game", font_size=21, color=GREY_A).next_to(b1, DOWN, buff=0.15)
        l2 = label(r"the same pieces, \ scrambled", font_size=21, color=GREY_A).next_to(b2, DOWN, buff=0.15)
        A = axes([0, 2], [0, 1], x_length=4.2, y_length=1.9, xticks=[], yticks=[], ylabel=r"pieces recalled",
                 center=[-3.1, -2.1, 0], font_size=15)
        vals = [(0.5, 0.82, LOGIC, -1), (0.5, 0.25, GREY_B, 1), (1.5, 0.2, LOGIC, -1), (1.5, 0.15, GREY_B, 1)]
        bs = VGroup(*[bars(A.ax, [x + 0.18 * side], [v], c, 0.33) for x, v, c, side in vals])
        bl = VGroup(label(r"game", font_size=16, color=GREY_A).next_to(A.ax.c2p(0.5, 0), DOWN, buff=0.08),
                    label(r"random", font_size=16, color=GREY_A).next_to(A.ax.c2p(1.5, 0), DOWN, buff=0.08))
        key = legend([(LOGIC, r"master"), (GREY_B, r"beginner")], font_size=15).next_to(A, RIGHT, buff=0.2)
        sch = label(r"schematic of the reported pattern", font_size=15, color=GREY_B).next_to(key, DOWN, buff=0.1)
        rows = rows_of([
            (r"de Groot, \ 1946: \ grandmasters do not search more moves than club players; \ they consider better "
             r"ones, \ and remember a position after a glance", WHITE),
            (r"Chase \& Simon, \ 1973: \ a master, \ a strong amateur and a beginner rebuilt positions seen for "
             r"five seconds", LOGIC),
            (r"from real games, \ the master recalled far more; \ scrambled, \ the advantage nearly vanished", CONTENT),
            (r"what the master stores are \emph{chunks}: \ familiar groups, \ perhaps tens of thousands of them", MODEL),
            (r"Gobet \& Simon, \ 1996: \ a small edge survives even on random boards", GREY_A),
        ], 5.2, 22, 0.32).move_to([4.0, 0.0, 0])
        tag = published_tag(r"de Groot (1946); \ Chase \& Simon (1973); \ Gobet \& Simon (1996)")
        with self.voiceover(
            "What makes an expert? Chess has been the laboratory. <bookmark mark='a'/> In the 1940s the Dutch "
            "psychologist and chess master Adriaan de Groot found that grandmasters don't search more moves ahead "
            "than good club players. They consider better moves, and they can rebuild a position after a glance. "
            "<bookmark mark='b'/> In 1973 William Chase and Herbert Simon showed a master, a strong amateur and a "
            "beginner a position for five seconds, and asked them to rebuild it. <bookmark mark='c'/> From real "
            "games, the master recalled far more pieces. With the same pieces scrambled at random, the master's "
            "advantage nearly vanished. <bookmark mark='d'/> The master wasn't remembering pieces, but chunks: "
            "familiar groups, like a castled king, of which a master might know tens of thousands. "
            "<bookmark mark='e'/> Later work found that a small advantage survives even on random boards, as "
            "chunks would predict, since a few familiar groups turn up by chance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(b1), FadeIn(l1))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Circumscribe(b1, color=LOGIC), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(b2), FadeIn(l2), FadeIn(A), FadeIn(bs), FadeIn(bl), FadeIn(key), FadeIn(sch),
                      FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def practice(self):
        head = heading(r"Ten thousand hours?")
        dom = [(r"games", 0.26), (r"music", 0.21), (r"sports", 0.18), (r"education", 0.04), (r"professions", 0.01)]
        A = axes([0, 5], [0, 0.3], x_length=5.6, y_length=3.0, xticks=[], yticks=[0, 0.1, 0.2, 0.3],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"differences explained by practice",
                 center=[-3.1, 0.2, 0], font_size=16)
        bs = VGroup(*[bars(A.ax, [k + 0.5], [v], MODEL, 0.6) for k, (_, v) in enumerate(dom)])
        names = VGroup(*[label(t, font_size=18, color=GREY_A).next_to(A.ax.c2p(k + 0.5, 0), DOWN, buff=0.12)
                         for k, (t, _) in enumerate(dom)])
        nums = VGroup(*[label(r"$<$1\%" if v < 0.02 else pct(v), font_size=18).next_to(b, UP, buff=0.06)
                        for b, (_, v) in zip(bs, dom)])
        rows = rows_of([
            (r"Ericsson, \ Krampe \& Tesch-R\"omer, \ 1993: \ Berlin violinists; \ the best had practised alone "
             r"most, \ an estimated 10{,}000 hours by twenty", WHITE),
            (r"Gladwell, \ 2008: \ the ``10{,}000-hour rule''; \ not a claim Ericsson made", GREY_A),
            (r"Macnamara, \ Hambrick \& Oswald, \ 2014: \ 88 studies, \ 11{,}135 people: \ practice matters, \ but "
             r"explains a minority of the differences", MODEL),
            (r"a 2019 replication with violinists found the best and the good had practised about equally", LOST),
        ], 5.6, 22, 0.32).move_to([3.6, 0.1, 0])
        tag = published_tag(r"Ericsson et al. (1993); \ Macnamara et al. (2014); \ Macnamara \& Maitra (2019)")
        with self.voiceover(
            "So how do you build a library of chunks? <bookmark mark='a'/> In 1993 Anders Ericsson and colleagues "
            "studied violinists at a Berlin music academy. The best had spent the most time in deliberate practice, "
            "alone, working on what they couldn't yet do: an estimated ten thousand hours by the age of twenty. "
            "<bookmark mark='b'/> Malcolm Gladwell turned this into the ten-thousand-hour rule, a claim Ericsson "
            "himself rejected. <bookmark mark='c'/> How much does practice explain? In 2014 Brooke Macnamara, David "
            "Hambrick and Frederick Oswald pooled eighty-eight studies of more than eleven thousand people. Practice "
            "explained about a quarter of the differences in games, a fifth in music and sport, four percent in "
            "education, and under one percent in professions. <bookmark mark='d'/> And a 2019 replication of the "
            "violin study found that the best and the good violinists had practised about equally. Practice matters, "
            "but it isn't the whole story, and the Ledger records the rule as a story the record doesn't support."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b) for b in bs], lag_ratio=0.3), FadeIn(nums), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
