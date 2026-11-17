from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403


class Societies(VoiceoverScene):
    def construct(self):
        self.card()
        self.fifteen()

    def card(self):
        card = chapter_card(6, r"Fifteen societies", r"Is fairness the same everywhere?",
                            lit={2001: r"Henrich et al."}, part=PART, scale=("group", "culture"), marr=("what",))
        with self.voiceover("Chapter six. Fifteen societies."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def fifteen(self):
        head = heading(r"The same game, \ far from campus")
        A = axes([0, 0.7], [0, 1.0], x_length=5.6, y_length=1.6, xticks=[0, 0.2, 0.4, 0.6], yticks=None,
                 xfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"average ultimatum offer", center=[-3.2, 0.6, 0],
                 font_size=15)
        rng_bar = Line(A.ax.c2p(0.26, 0.5), A.ax.c2p(0.58, 0.5), color=PERSON, stroke_width=10)
        lo = label(r"26\%", font_size=18, color=PERSON).next_to(A.ax.c2p(0.26, 0.5), UP, buff=0.15)
        hi = label(r"58\%", font_size=18, color=PERSON).next_to(A.ax.c2p(0.58, 0.5), UP, buff=0.15)
        ind = Dot(A.ax.c2p(0.44, 0.5), radius=0.1, color=CROWD)
        il = label(r"students: \ about 44\%", font_size=16, color=CROWD).next_to(ind, DOWN, buff=0.25)
        rows = rows_of([
            (r"Henrich, \ Boyd, \ Bowles, \ Camerer, \ Fehr, \ Gintis and McElreath, \ 2001: \ the ultimatum game "
             r"in 15 small-scale societies: \ foragers, \ horticulturalists, \ herders, \ farmers", WHITE),
            (r"average offers ranged from 26\% (the Machiguenga of Peru) to 58\%; \ in industrial societies they "
             r"are typically near 44\%", PERSON),
            (r"no society matched the selfish prediction", AUTH),
            (r"what predicted a group's offers was its economy: \ how much people cooperated in production, \ and "
             r"how integrated they were with markets; \ individual traits did not", GOOD),
            (r"fairness norms vary with the institutions people live in; \ Part 38 asks which other findings were "
             r"really findings about one kind of society", YOU),
        ], 12.4, 20, 0.28).move_to([0, -1.9, 0])
        tag = published_tag(r"Henrich et al.\ (2001)")
        with self.voiceover(
            "Almost all of these experiments were run with university students. <bookmark mark='a'/> In 2001 Joseph "
            "Henrich and colleagues took the ultimatum game to fifteen small-scale societies: foragers, "
            "horticulturalists, herders and farmers. <bookmark mark='b'/> Average offers ranged from twenty-six "
            "percent, among the Machiguenga of Peru, to fifty-eight percent. In industrial societies they're "
            "typically near forty-four. <bookmark mark='c'/> No society matched the selfish prediction. "
            "<bookmark mark='d'/> What predicted a group's offers was its economy: how much people cooperated in "
            "making a living, and how integrated they were with markets. Individual traits didn't. "
            "<bookmark mark='e'/> Fairness norms vary with the institutions people live in. Part 38 asks which other "
            "findings were really findings about one kind of society."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(rng_bar), FadeIn(lo), FadeIn(hi), FadeIn(ind), FadeIn(il), FadeIn(rows[1]))
            for m, r in zip("cde", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
