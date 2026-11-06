from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


class Kant(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"The categorical imperative", r"Is there a law that binds every rational agent?",
                            lit=(1785,), part=PART)
        with self.voiceover("Chapter five. The categorical imperative."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.formulas()
        self.world()
        self.collapse()
        self.humanity()

    def formulas(self):
        hc = history_card(1785, r"Immanuel Kant", r"\textit{Groundwork of the Metaphysics of Morals}", width=6.6,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [(r"universal law", r"act only on that maxim through which you can at the same time will that it become "
                                   r"a universal law", KANT),
                (r"humanity", r"treat humanity, \ in your own person or another's, \ always as an end, \ never merely "
                              r"as a means", DUTY),
                (r"autonomy", r"the will is to be regarded as giving universal law", GOOD),
                (r"kingdom of ends", r"act as a member of a possible realm of ends, \ legislating for it", VIRT),
                (r"categorical", r"not `if you want X, \ do Y', \ but `do Y': \ binding on every rational agent, \ "
                                 r"whatever she wants", GOAL)]
        g = rows_table(rows, top=1.2, gap=0.42, width=8.0, x_text=-2.0)
        with self.voiceover(
            "Kant's Groundwork of the Metaphysics of Morals, of 1785, gave several formulations of one supreme "
            "principle. <bookmark mark='a'/>Act only on that maxim through which you can at the same time will that "
            "it become a universal law. <bookmark mark='b'/>Treat humanity, in your own person or in another's, always "
            "as an end, and never merely as a means. <bookmark mark='c'/>Regard your will as giving universal law. "
            "<bookmark mark='d'/>Act as a member of a possible kingdom of ends. <bookmark mark='e'/>The imperative is "
            "categorical: not if you want this, do that, but simply do it, binding on every rational agent whatever "
            "she happens to want."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def world(self):
        head = label(r"A world of promises, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the maxim", r"`when I need money, \ I will promise to repay it, \ though I know I never will'",
                 KANT),
                (r"its purpose", r"to get money by means of a promise", GREY_A),
                (r"the world", r"1000 agents; \ each round a tenth need money and promise to repay; \ a share $f$ of "
                               r"them follow the maxim", AGG),
                (r"lenders", r"lend only while more than half of past promises have been kept", DUTY),
                (r"universalize", r"set $f = 1$: \ can the maxim still achieve its purpose?", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.42, width=8.4)
        with self.voiceover(
            "Kant's own example of the universal law test is the lying promise, and the Reasoner can build it. "
            "<bookmark mark='a'/>The maxim: when I need money, I will promise to repay it, though I know I never "
            "will. <bookmark mark='b'/>Its purpose is to get money by means of a promise. <bookmark mark='c'/>The "
            "world: a thousand agents, of whom a tenth need money each round and promise to repay; a share f of them "
            "follow the maxim. <bookmark mark='d'/>Lenders lend only while more than half of the promises made so far "
            "have been kept. <bookmark mark='e'/>To universalize the maxim is to set f to one, and ask whether it can "
            "still achieve its purpose."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def collapse(self):
        d = load("promises")
        head = label(r"Universalized, \ the lie destroys itself", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = {r["f"]: r for r in d["rows"]}
        assert rows[0.0]["lent_rounds"] == 40 and rows[0.4]["lent_rounds"] == 40 and rows[0.5]["lent_rounds"] == 1
        assert rows[1.0]["final_trust"] == 0.008
        ax = Axes(x_range=[0, 40, 10], y_range=[0, 1, 0.5], x_length=6.4, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15, "include_numbers": True}).move_to([-2.4, -0.4, 0])
        xl = label(r"rounds", font_size=16, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"share of promises kept", font_size=16, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(40, 0.5), color=DUTY)
        hl = label(r"lenders stop below this", font_size=14, color=DUTY).next_to(ax.c2p(40, 0.5), UP, buff=0.08).shift(
            LEFT * 1.0)
        cols = {0.0: GOOD, 0.2: GOOD, 0.4: VIRT, 0.6: HARM, 1.0: BAD}
        curves = VGroup()
        for f, col in cols.items():
            tr = rows[f]["trust"]
            curves.add(VGroup(VMobject(color=col, stroke_width=3).set_points_as_corners(
                [ax.c2p(t, v) for t, v in enumerate(tr)]),
                label(f"$f = {f:g}$", font_size=14, color=col).next_to(ax.c2p(39, tr[-1]), RIGHT, buff=0.1)))
        side = stack([(r"$f$ up to 0.4: \ lenders keep lending all 40 rounds", GOOD),
                      (r"$f$ from 0.5: \ lending stops after the first round", HARM),
                      (r"$f = 1$: \ trust ends at 0.008; \ no one lends", BAD),
                      (r"the universalized maxim cannot achieve its own purpose: \ a contradiction in conception",
                       GOAL),
                      (r"the liar needs others to be honest: \ he makes an exception of himself", KANT)], font_size=18,
                     aligned_edge=LEFT, width=4.8, buff=0.28).move_to([4.1, -0.2, 0])
        with self.voiceover(
            "Here is what happens. <bookmark mark='a'/>The lines show the share of promises kept, round by round, for "
            "different shares of liars. <bookmark mark='b'/>Up to four tenths, lenders keep lending all forty rounds, "
            "and the liars do well. <bookmark mark='c'/>From a half, trust falls below the threshold at once, and "
            "lending stops after the first round. <bookmark mark='d'/>With everyone lying, trust ends near zero, and "
            "no one lends. <bookmark mark='e'/>The universalized maxim cannot achieve its own purpose: there is no "
            "money to be had by false promises in a world where all promises are false. That is Kant's contradiction "
            "in conception. <bookmark mark='f'/>The liar's success depends on others being honest: he wills a law "
            "for everyone, and an exception for himself."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), Create(half), FadeIn(hl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c[0]) for c in curves], lag_ratio=0.25), FadeIn(VGroup(*[c[1] for c in
                                                                                                   curves])),
                      run_time=2.5)
            for mk, r in zip("bcdef", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def humanity(self):
        d = load("humanity")
        head = label(r"Never merely as a means", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = d["rows"]
        assert len(rows) == 7 and (d["act_matches"], d["attitude_matches"]) == (7, 6)
        assert [r["act_test"] for r in rows] == ["permitted"] * 2 + ["forbidden"] * 4 + ["permitted"]
        assert rows[-1]["attitude_test"] == "forbidden" and not rows[-1]["wrong"]
        yes, no = r"yes", r"no"
        hd = [r"\text{act}", r"\text{deceives}", r"\text{forces}", r"\text{could consent}", r"\text{O'Neill's test}",
              r"\text{intuition}"]
        cells = []
        for r in rows:
            cells.append([label(r["act"], font_size=16, color=WHITE),
                          label(yes if r["deceives"] else no, font_size=16, color=HARM if r["deceives"] else GREY_B),
                          label(yes if r["coerces"] else no, font_size=16, color=HARM if r["coerces"] else GREY_B),
                          label(yes if r["could_consent"] else no, font_size=16,
                                color=GOOD if r["could_consent"] else HARM),
                          label(r["act_test"], font_size=16, color=GOOD if r["act_test"] == "permitted" else KANT),
                          label(r"wrong" if r["wrong"] else r"fine", font_size=16, color=HARM if r["wrong"] else GOOD)])
        grid = ValueGrid(hd, cells, col_w=[4.2, 1.5, 1.3, 2.0, 2.2, 1.6], cell_h=0.46, font_size=16).move_to(
            [0, 0.15, 0])
        foot = stack([(r"O'Neill \ (1985): \ merely as a means = involving others in a scheme they could not "
                       r"possibly consent to", KANT),
                      (r"Parfit's gangster regards the barista merely as a tool: \ an attitude, \ not a wrong act", HARM),
                      (r"Kant: \ only indirect duties to animals; \ Korsgaard \ (2018): \ they too are ends", VIRT)],
                     font_size=17, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Most Kantians now lead with the formula of humanity. <bookmark mark='a'/>Using people as means is "
            "everywhere and innocent: you use a taxi driver to get home, and she uses you to earn a living. What the "
            "formula forbids is treating anyone merely as a means. <bookmark mark='b'/>Onora O'Neill, in 1985, gave "
            "a test: you use someone merely as a means if you involve them in a scheme of action to which they could "
            "not possibly consent. Deception and coercion guarantee that, since the deceived cannot know what they "
            "would be agreeing to, and the coerced are given no say. <bookmark mark='c'/>The Reasoner runs the test "
            "on seven acts. The taxi ride and an honest sale pass. The lying promise, a confidence trick, a mugging "
            "and the push from the footbridge fail. Six of the seven verdicts match intuition on any reading. "
            "<bookmark mark='d'/>The seventh is Parfit's gangster, who regards the barista merely as a tool and "
            "would harm her if it suited him, and who buys a coffee. He treats her merely as a means in attitude, yet "
            "buying the coffee is not wrong: read as a test of attitudes the formula convicts him, read as O'Neill "
            "reads it, a test of acts, it does not. <bookmark mark='e'/>And the formula's circle stops at rational "
            "beings: Kant allowed only indirect duties to animals, a limit Christine Korsgaard's Fellow Creatures, "
            "of 2018, challenges from within Kant's own theory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            for k in range(1, 6):
                self.play(*[FadeIn(c) for c in grid.cell[k]], run_time=0.5)
            vo.wait_until("d")
            self.play(*[FadeIn(c) for c in grid.cell[6]], FadeIn(foot[1]))
            vo.wait_until("e")
            self.play(FadeIn(foot[2]))
        self.clear_scene()
