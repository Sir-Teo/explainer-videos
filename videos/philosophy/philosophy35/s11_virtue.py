from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


class Virtue(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Virtue", r"Is ethics about acts, or about character?", lit=(-340, 1973),
                            part=PART)
        with self.voiceover("Chapter ten. Virtue."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.mean()
        self.particularism()
        self.confucius()
        self.situationism()

    def mean(self):
        head = label(r"Aristotle: \ the mean, \ eudaimonia, \ practical wisdom", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        hd = [r"\text{feeling or action}", r"\text{deficiency}", r"\text{virtue}", r"\text{excess}"]
        rows = [("fear and confidence", "cowardice", "courage", "rashness"),
                ("giving money", "stinginess", "generosity", "prodigality"),
                ("anger", "spiritlessness", "good temper", "irascibility"),
                ("truth about oneself", "self-deprecation", "truthfulness", "boastfulness")]
        cells = [[label(a, font_size=17, color=GREY_A), label(b, font_size=17, color=HARM), label(c, font_size=17,
                                                                                               color=VIRT),
                  label(e, font_size=17, color=HARM)] for a, b, c, e in rows]
        grid = ValueGrid(hd, cells, col_w=[3.2, 2.6, 2.4, 2.4], cell_h=0.52, font_size=16).move_to([0, 0.6, 0])
        foot = stack([(r"virtue: \ a settled disposition to feel and act at the right time, \ toward the right people, "
                       r"\ in the right way", VIRT),
                      (r"eudaimonia: \ the flourishing life, \ activity of the soul in accordance with virtue", GOOD),
                      (r"phronesis: \ practical wisdom, \ which sees what the situation requires", GOAL)],
                     font_size=18, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Virtue ethics begins with Aristotle's Nicomachean Ethics. <bookmark mark='a'/>For each kind of feeling "
            "and action there is a mean between two vices: courage between cowardice and rashness, generosity "
            "between stinginess and prodigality, good temper between spiritlessness and irascibility, truthfulness "
            "about oneself between self-deprecation and boastfulness. <bookmark mark='b'/>A virtue is a settled "
            "disposition to feel and act rightly: at the right time, toward the right people, in the right way. "
            "<bookmark mark='c'/>The aim is eudaimonia, the flourishing life, <bookmark mark='d'/>and what finds "
            "the mean in a given case is practical wisdom, not a rule. Elizabeth Anscombe's paper of 1958 and "
            "Rosalind Hursthouse's book of 1999 revived the view: right action is what a virtuous person would "
            "characteristically do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            for k in range(4):
                self.play(*[FadeIn(c) for c in grid.cell[k]], run_time=0.5)
            for mk, r in zip("bcd", foot):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def particularism(self):
        d = load("particularism")
        head = label(r"Particularism: \ is judgment a weighted sum of reasons?", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        a, f = d["atomistic"], d["with_defeaters"]
        assert (d["n_cases"], d["permissible"], len(d["atomistic_wrong"])) == (27, 15, 10)
        assert (a["acc"], a["weights"], a["threshold"], a["n_weightings"]) == (0.6296, [0, 0, -1], -0.5, 343)
        assert (f["acc"], f["weights"], f["threshold"], f["n_weightings"]) == (1.0, [1, -2, 1, -1, -2, 2], -0.5,
                                                                              117649)

        def reason(base, bw, defeat, dw):
            t1 = label(base, font_size=18, color=WHITE)
            v1 = label(bw, font_size=18, color=GOOD if bw.startswith("+") else HARM)
            t2 = label(defeat, font_size=16, color=GREY_A)
            v2 = label(dw, font_size=18, color=HARM if dw.startswith("-") else GREY_A)
            g = VGroup(VGroup(t1, v1).arrange(RIGHT, buff=0.2), VGroup(t2, v2).arrange(RIGHT, buff=0.2)).arrange(
                DOWN, buff=0.15)
            return VGroup(SurroundingRectangle(g, buff=0.18, color=GREY_B, stroke_width=1.5, corner_radius=0.08), g)

        cards = VGroup(reason(r"gives pleasure", r"+1", r"but the pleasure is cruel", r"-1"),
                       reason(r"keeps a promise", r"+1", r"but it was coerced", r"0"),
                       reason(r"tells a lie", r"-2", r"but inside a game", r"0")).arrange(RIGHT, buff=0.45).move_to(
            [0, 1.55, 0])
        rule = label(r"the judge: \ permissible iff the reasons sum to at least 0", font_size=17,
                     color=GREY_A).next_to(cards, DOWN, buff=0.22)
        wrong = {tuple(int(x[k]) for k in d["features"]) for x in d["atomistic_wrong"]}
        tiles = VGroup()
        for c in d["cases"]:
            col = GOOD if c["verdict"] else HARM
            tiles.add(Square(side_length=0.34, stroke_width=0, fill_color=col, fill_opacity=0.75))
        tiles.arrange(RIGHT, buff=0.06).move_to([0, 0.0, 0])
        cap = label(r"all 27 consistent cases: \ 15 permissible, \ 12 not", font_size=16, color=GREY_A).next_to(
            tiles, DOWN, buff=0.15)
        crosses = VGroup(*[Cross(t, stroke_color=WHITE, stroke_width=2.5, scale_factor=0.8)
                           for t, c in zip(tiles, d["cases"]) if tuple(c["f"]) in wrong])
        r1 = VGroup(label(r"fixed weights on the three reasons, \ best of 343 \ (Ross-style):", font_size=18,
                          color=DUTY),
                    MathTex(r"0\cdot\text{pleasure} + 0\cdot\text{promise} - 1\cdot\text{lie} > -\tfrac12", font_size=28,
                            color=DUTY),
                    label(r"17 of 27: \ ignore pleasure and promises, \ just do not lie", font_size=17, color=HARM)
                    ).arrange(DOWN, buff=0.12).move_to([-3.4, -2.0, 0])
        r2 = VGroup(label(r"weights for the defeaters too, \ best of 117,649:", font_size=18, color=VIRT),
                    MathTex(r"(+1, -2, +1, -1, -2, +2)", font_size=28, color=VIRT),
                    label(r"27 of 27 \ (McKeever and Ridge, \ 2006)", font_size=17, color=GOOD)
                    ).arrange(DOWN, buff=0.12).move_to([3.4, -2.0, 0])
        with self.voiceover(
            "Aristotle said that the decision rests with perception. Jonathan Dancy's Ethics Without Principles, of "
            "2004, turns this into a thesis about reasons. <bookmark mark='a'/>Holism: a feature that is a reason for "
            "an act in one case can be no reason, or a reason against, in another. That an act gives pleasure "
            "usually counts in its favour; that it gives a sadist pleasure counts against. A promise binds, unless it "
            "was coerced. A lie is wrong, unless it is a move in a game whose players expect it. "
            "<bookmark mark='b'/>The Reasoner builds a judge with exactly these views and asks it about all twenty "
            "seven consistent cases: fifteen permissible, twelve not. <bookmark mark='c'/>Can the judge be summed up "
            "as fixed weights on the basic reasons, in the manner of Ross's prima facie duties? Searching all three "
            "hundred and forty three integer weightings with every threshold, the best gets seventeen of the twenty "
            "seven right, by ignoring pleasure and promises altogether and saying only: do not lie. "
            "<bookmark mark='d'/>Sean McKeever and Michael Ridge's Principled Ethics, of 2006, answers that "
            "principles can carry their defeaters with them. Give each defeater a weight of its own, and a weighting "
            "from among a hundred and seventeen thousand fits every case: pleasure plus one, cruelty minus two, a "
            "promise plus one, coercion minus one, a lie minus two, a game plus two. <bookmark mark='e'/>So holism "
            "alone does not refute principles. The particularist's real claim is that the defeaters, and the "
            "defeaters of defeaters, never run out, so that no finite list can replace judgment. The same question "
            "now faces anyone who trains a machine on human moral verdicts."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.4), run_time=2)
            self.play(FadeIn(rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t, scale=0.5) for t in tiles], lag_ratio=0.05), FadeIn(cap))
            vo.wait_until("c")
            self.play(FadeIn(r1))
            self.play(LaggedStart(*[Create(x) for x in crosses], lag_ratio=0.1))
            vo.wait_until("d")
            self.play(FadeIn(r2), FadeOut(crosses))
        self.clear_scene()

    def confucius(self):
        head = label(r"Confucius and Mencius", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"ren \ (humaneness)", r"the virtue of caring for others, \ extending outward from family", VIRT),
                (r"li \ (ritual propriety)", r"the forms of conduct through which care is expressed and trained", DUTY),
                (r"the junzi", r"the exemplary person, \ whose character makes right action natural", GOAL),
                (r"Mencius 2A6", r"anyone who sees a child about to fall into a well feels alarm and compassion: \ "
                                 r"not for reward, \ not for reputation", GOOD),
                (r"four sprouts", r"compassion, \ shame, \ deference, \ and the sense of right and wrong: \ seeds of "
                                  r"ren, \ yi, \ li and zhi, \ to be cultivated", AGG)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.4)
        with self.voiceover(
            "Classical Chinese philosophy developed a virtue ethics of its own. <bookmark mark='a'/>Confucius made ren, "
            "humaneness, the central virtue: care for others, extending outward from the family. "
            "<bookmark mark='b'/>Li, ritual propriety, is the set of forms through which that care is expressed and "
            "trained. <bookmark mark='c'/>The ideal is the junzi, the exemplary person, whose character makes right "
            "action natural. <bookmark mark='d'/>Mencius argued that human nature is good: anyone who suddenly sees a "
            "child about to fall into a well feels alarm and compassion, not to win the parents' favour or a good "
            "name. <bookmark mark='e'/>Everyone has four sprouts, of compassion, shame, deference and a sense of right "
            "and wrong, which grow into the four virtues if they are cultivated."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def situationism(self):
        head = label(r"The situationist challenge \ (Harman, \ 1999; \ Doris, \ 2002)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        bars = VGroup()
        data = [(r"not in a hurry", 0.63, GOOD), (r"in a moderate hurry", 0.45, VIRT), (r"in a great hurry", 0.10, HARM)]
        for k, (n, v, col) in enumerate(data):
            h = 3.0 * v
            b = Rectangle(width=1.2, height=h, stroke_width=0, fill_color=col, fill_opacity=0.8).move_to(
                [-5.0 + 1.8 * k, -2.0 + h / 2, 0])
            bars.add(VGroup(b, label(f"{100 * v:.0f}\\%", font_size=18, color=col).next_to(b, UP, buff=0.08),
                            wrapped_label(n, 1.6, 15, GREY_A).next_to([-5.0 + 1.8 * k, -2.0, 0], DOWN, buff=0.12)))
        cap = label(r"seminarians who stopped to help a man slumped in a doorway \ (Darley and Batson, \ 1973)",
                    font_size=16, color=GREY_A).next_to(bars, UP, buff=1.2).align_to(bars, LEFT)
        side = stack([(r"small features of the situation predict behaviour better than character traits", HARM),
                      (r"Milgram \ (1963): \ 26 of 40 subjects gave the highest `shock'", HARM),
                      (r"if robust virtues are rare, \ is virtue ethics empirically false?", BAD),
                      (r"replies: \ virtue is an ideal, \ rarely reached \ (Annas; \ Kamtekar); \ local traits; \ "
                       r"replications are mixed", VIRT)], font_size=18, aligned_edge=LEFT, width=5.0,
                     buff=0.3).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "Social psychology raised a challenge. <bookmark mark='a'/>In 1973 John Darley and Daniel Batson sent "
            "seminary students to give a talk, some on the parable of the Good Samaritan, and on the way they passed "
            "a man slumped in a doorway. Sixty three percent of those not in a hurry stopped to help; forty five "
            "percent of those in a moderate hurry; only ten percent of those in a great hurry. "
            "<bookmark mark='b'/>Small features of the situation predicted behaviour better than character. "
            "<bookmark mark='c'/>In Stanley Milgram's experiment of 1963, twenty six of forty subjects gave what they "
            "believed was the strongest shock. <bookmark mark='d'/>Gilbert Harman and John Doris argued that robust "
            "character traits are rare, so virtue ethics rests on a false psychology. <bookmark mark='e'/>Virtue "
            "ethicists reply that virtue is an ideal few reach, which is what Aristotle said, and that the "
            "experiments are about local behaviour, some of it poorly replicated."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cap), LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.3),
                      *[FadeIn(b[1:]) for b in bars], run_time=2)
            for mk, r in zip("bcde", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
