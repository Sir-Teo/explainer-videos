from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class Networks(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Network effects, \ tipping and lock-in", r"Can a worse technology win for good?",
             "Chapter seven. Network effects, tipping and lock-in.",
             lit={1985: r"David", 1989: r"Arthur", 1990: r"Liebowitz and Margolis"}, scale=("market", "world"),
             horizon=("a decade", "a century"))
        self.qwerty()
        self.paths()
        self.curve()
        self.reply()

    def qwerty(self):
        keys = VGroup()
        for r_, row in enumerate(("QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM")):
            g = VGroup(*[VGroup(RoundedRectangle(width=0.62, height=0.62, corner_radius=0.08, stroke_color=GREY_B,
                                                 stroke_width=1.6, fill_color="#141821", fill_opacity=1),
                                label(ch, font_size=22, color=BUS)) for ch in row])
            for k in g:
                k[1].move_to(k[0])
            g.arrange(RIGHT, buff=0.1)
            keys.add(g)
        keys.arrange(DOWN, buff=0.12)
        for k, g in enumerate(keys):
            g.shift(RIGHT * 0.25 * k)
        keys.move_to(UP * 0.7)
        cards = point_cards([
            (r"David, \ 1985", r"QWERTY was designed \\ for 1870s machines; \\ typists, \ schools and \\ "
                                r"makers kept it", BUS),
            (r"the mechanism", r"each typist's keyboard \\ is worth more when \\ others use the same", PATIENT),
            (r"the claim", r"a better layout \\ could not break in", LOSS),
        ], width=11.4, cols=3, font_size=18).move_to(DOWN * 2.0)
        tag = published_tag(tables.QWERTY.tag, corner=DR, font_size=11)
        with self.voiceover(
            "When a product is worth more because others use it too, the market can tip. "
            "<bookmark mark='a'/> In 1985 Paul David told the story of the QWERTY keyboard, laid out for the "
            "typewriters of the 1870s, and kept ever since. <bookmark mark='b'/> A typist trained on QWERTY is worth "
            "more to employers who use QWERTY, and a keyboard maker sells more of the layout typists know. "
            "<bookmark mark='c'/> David's claim was that a better layout, August Dvorak's, could never break in: "
            "history, not quality, had decided."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(k, scale=1.2) for g in keys for k in g], lag_ratio=0.03),
                      run_time=2.0)
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def paths(self):
        L = load("lockin")
        P = L["paths"]
        n = len(P[0])
        ax = plane([0, n], [0, 1], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 200, 400, 600], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"adopters so far",
                   ylabel=r"the older technology A's share", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        half = seg(ax, 0, 0.5, n, 0.5, GREY_B, 1.4, dashed=True)
        lines = VGroup(*[path(ax, np.arange(1, n + 1), p, (MYOPIC if p[-1] > 0.5 else PATIENT), 2.0, smooth=False)
                         for p in P])
        side = VGroup(
            label(rf"B is better: \ adopters \\ prefer it by {L['quality']} \\ on average \ (tastes vary)",
                  font_size=18, color=PATIENT),
            label(r"A came first, \ with \\ 20 users", font_size=18, color=MYOPIC),
            label(r"each user adds 0.02 \\ to everyone on the \\ same technology", font_size=18, color=BUS),
            label(rf"A wins {100 * L['at02']:.0f}\% of the \\ time", font_size=19, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island can run the story many times, as Brian Arthur did in theory. <bookmark mark='a'/> Two "
            f"technologies; adopters, on average, prefer B by {L['quality']}, though tastes vary. "
            "<bookmark mark='b'/> A came first and has twenty users. <bookmark mark='c'/> Each new user of a "
            "technology adds a little to its value for everyone else on it. Adopters arrive one by one and pick "
            f"what is best for them now. <bookmark mark='d'/> In {100 * L['at02']:.0f} percent of runs the worse "
            "technology, A, ends up with most users: its head start grows faster than B's quality can catch it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(half), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.1), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def curve(self):
        L = load("lockin")
        ax = plane([0, 0.04], [0, 1], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.01, 0.02, 0.03, 0.04], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"strength of the network effect, \ per user", ylabel=r"chance the worse technology wins",
                   xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ln = path(ax, L["network"], L["share"], LOSS, 3.4)
        side = VGroup(
            label(r"no network effect: \\ the better technology \\ always wins", font_size=18, color=PATIENT),
            label(r"strong effects: \ the \\ first mover always \\ wins", font_size=18, color=LOSS),
            label(r"in between, \ luck \\ and timing decide", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now vary the strength of the network effect. <bookmark mark='a'/> Without it, the better technology "
            "always wins. <bookmark mark='b'/> With strong effects, the first mover always wins. "
            "<bookmark mark='c'/> In between, luck and timing decide, and the market tips one way or the other and "
            "stays there. That is the theory of lock-in. Whether it describes QWERTY is another matter."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            for mk, s_ in zip("abc", side):
                vo.wait_until(mk)
                self.play(FadeIn(s_))
        self.clear_scene()

    def reply(self):
        cards = point_cards([
            (r"the evidence", r"the studies showing \\ Dvorak faster were \\ weak; \ later tests \\ found little gain",
             LOSS),
            (r"the market", r"if a layout were much \\ better, \ firms could \\ profit by switching \\ their typists",
             PATIENT),
            (r"Liebowitz and \\ Margolis, \ 1990", r"`The Fable of the \\ Keys': \ lock-in into \\ a worse standard "
                                                     r"\\ is unproven", BUS),
            (r"for policy", r"lock-in is possible; \\ whether it happened \\ is a question of \\ evidence", E.ACCENT),
        ], width=12.8, cols=4, font_size=17).move_to(DOWN * 0.1)
        head = label(r"the reply", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.QWERTY.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In 1990 Stan Liebowitz and Stephen Margolis replied. <bookmark mark='a'/> The studies that showed "
            "Dvorak's layout to be much faster were weak, and later tests found little advantage. "
            "<bookmark mark='b'/> And if a layout were much better, firms could profit by retraining their typists, "
            "so markets have ways out of bad standards. <bookmark mark='c'/> They called David's story the fable "
            "of the keys. <bookmark mark='d'/> The lesson for policy is that lock-in is possible in theory, as the "
            "Island shows, but whether it happened in a given market is a question of evidence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
