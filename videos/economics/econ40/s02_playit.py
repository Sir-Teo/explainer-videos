from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ four numbers", r"How unequal, \ and how mobile, \ is America?",
             "Chapter one. Play it: four numbers.", lit={2014: r"Chetty et al.", 2022: r"Saez"},
             scale=("household", "nation"), horizon=("a year", "a decade"))
        self.ask()
        self.reveal()

    def _cards(self):
        G = load("guess")
        qs = [(r"the richest 1\% of Americans: \\ what share of all income \\ did they receive in 2022?", TOP),
              (r"the richest 1\% of households: \\ what share of all wealth \\ do they hold?", WEALTH),
              (r"a child whose parents are in \\ the bottom fifth: \ the chance \\ of reaching the top fifth?",
               CHILD),
              (r"children born in 1984: \ what share \\ earn more at 30 than their \\ parents did, \ in real "
               r"terms?", MIDDLE)]
        ans = [(rf"{G['top1_income']:.1f}\%", r"of pre-tax income, \ tax records \\ (with capital gains: "
                rf"{G['top1_income_kg']:.1f}\%)"),
               (rf"{G['top1_wealth']:.1f}\%", r"of household net worth, \\ the Federal Reserve, \ 2026"),
               (rf"{100 * G['q5q1']:.1f}\%", r"children born 1980--82; \\ if birth did not matter: \ 20\%"),
               (rf"{100 * G['absmob1984']:.0f}\%", rf"born in 1940: \ {100 * G['absmob1940']:.0f}\%")]
        cards = VGroup()
        for (q, col), (a, sub) in zip(qs, ans):
            box = RoundedRectangle(width=6.1, height=2.9, corner_radius=0.12, stroke_color=col, stroke_width=2.2,
                                   fill_color="#141821", fill_opacity=1)
            qt = label(q, font_size=21, color=WHITE).move_to(box.get_top() + DOWN * 0.75)
            at = label(a, font_size=40, color=col).move_to(box.get_center() + DOWN * 0.55 + LEFT * 1.6)
            st = label(sub, font_size=16, color=GREY_A).next_to(at, RIGHT, buff=0.35)
            cards.add(VGroup(box, qt, at, st))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.3)).move_to(DOWN * 0.2)
        return cards

    def ask(self):
        cards = self._cards()
        head = label(r"Your turn: \ four guesses", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.3)
        ring = countdown().scale(0.6).next_to(head, RIGHT, buff=0.5)
        with self.voiceover(
            "Your turn. Four numbers about America, and a guess for each before the answers. <bookmark mark='a'/> "
            "First: of all the income Americans received in 2022, what share went to the richest one percent? "
            "<bookmark mark='b'/> Second: of all household wealth, what share do the richest one percent of "
            "households hold? <bookmark mark='c'/> Third: a child whose parents are in the bottom fifth of the "
            "income distribution. What is the chance that, as an adult, the child reaches the top fifth? "
            "<bookmark mark='d'/> And fourth: of Americans born in 1984, what share earn more at thirty than their "
            "parents did at the same age, after inflation? Pause, and write down your four guesses."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c[0]), FadeIn(c[1]))
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.cards, self.head = cards, head

    def reveal(self):
        G = load("guess")
        cards = self.cards
        tag = data_tag(r"Piketty and Saez (2022 update); \ Federal Reserve DFA via FRED; \ Chetty et al. (2014, "
                       r"2017)", corner=DR, font_size=11)
        with self.voiceover(
            "Here are the answers. <bookmark mark='a'/> The richest one percent received "
            f"{G['top1_income']:.1f} percent of all pre-tax income in 2022, about one dollar in five; counting capital "
            f"gains, {G['top1_income_kg']:.1f} percent. <bookmark mark='b'/> They hold {G['top1_wealth']:.1f} percent "
            "of all household wealth, about a third. <bookmark mark='c'/> A child from the bottom fifth has a "
            f"{100 * G['q5q1']:.1f} percent chance of reaching the top fifth; if parents did not matter at all, it "
            "would be twenty. <bookmark mark='d'/> And of children born in 1984, only "
            f"{100 * G['absmob1984']:.0f} percent out-earn their parents, against {100 * G['absmob1940']:.0f} percent "
            "of those born in 1940. Keep your guesses: each of these numbers has a chapter."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, c in zip("abcd", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c[2], scale=1.2), FadeIn(c[3]))
        self.clear_scene()
