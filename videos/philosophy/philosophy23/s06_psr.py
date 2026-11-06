from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class PSR(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"The principle of sufficient reason", r"Does everything have an explanation?",
                            lit=(1714, 1983), part=PART)
        with self.voiceover("Chapter five. The principle of sufficient reason."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.principle()
        self.collapse()
        self.computed()
        self.responses()

    def principle(self):
        head = label(r"Nothing without a reason", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Leibniz", r"`no fact can be real or existing, \ no statement true, \ unless there is a sufficient reason "
                         r"why it is so and not otherwise'", ABS),
            (r"its appeal", r"science, \ detective work and everyday life all assume that things have explanations",
             NAT),
            (r"Spinoza", r"took it all the way: \ `in nature there is nothing contingent' \ (\textit{Ethics} I, \ "
                         r"p29)", HUM),
            (r"the question", r"can the principle hold for \textit{every} truth, \ including the biggest one?", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=22)
        with self.voiceover(
            "Leibniz stated the principle in the Monadology. <bookmark mark='a'/>No fact can be real or existing, no "
            "statement true, unless there is a sufficient reason why it is so and not otherwise. "
            "<bookmark mark='b'/>Its appeal is obvious: science, detective work and ordinary life all assume that "
            "things have explanations, and we are rightly suspicious of anyone who says that something just happened, "
            "for no reason. <bookmark mark='c'/>Spinoza took it all the way: in nature, he wrote, there is nothing "
            "contingent. <bookmark mark='d'/>The question is whether the principle can hold for every truth, "
            "including the biggest one."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def collapse(self):
        hc = history_card(1983, r"Peter van Inwagen", r"\textit{An Essay on Free Will}", width=5.8,
                          color=HIST).to_corner(UL, buff=0.3)
        steps = stack([(r"1. \ let $p$ be the conjunction of every contingent truth: \ the big conjunctive "
                        r"contingent fact", WHITE),
                       (r"2. \ by the principle, \ some truth $q$ explains $p$; \ and an explanation entails what it "
                        r"explains", ABS),
                       (r"3. \ if $q$ is necessary, \ then $p$, \ which it entails, \ is necessary: \ contradiction",
                        BAD),
                       (r"4. \ if $q$ is contingent, \ it is a conjunct of $p$: \ then $p$ explains itself in part",
                        BAD),
                       (r"5. \ nothing explains itself: \ so if the principle holds, \ there are no contingent truths",
                        DIV)], font_size=21, aligned_edge=LEFT, width=12.2, buff=0.3).move_to([0, -0.5, 0])
        with self.voiceover(
            "Peter van Inwagen showed what the full principle costs. <bookmark mark='a'/>Let p be the conjunction of "
            "all contingent truths: the big conjunctive contingent fact. <bookmark mark='b'/>By the principle, some "
            "truth q explains it; and suppose, as Leibniz did, that a sufficient reason entails what it explains. "
            "<bookmark mark='c'/>If q is necessary, then p, which q entails, is necessary too, contradicting the fact "
            "that p is contingent. <bookmark mark='d'/>If q is contingent, then q is one of the contingent truths, a "
            "conjunct of p itself, and p would be explaining itself. <bookmark mark='e'/>Nothing explains itself. "
            "So if the principle holds without exception, there are no contingent truths at all: everything is "
            "necessary. The cosmological argument's best premise implies modal collapse, the same wall Gödel's proof "
            "ran into."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def computed(self):
        d = load("psr")
        head = label(r"On a finite space of worlds", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        cells = VGroup()
        for i in range(4):
            c = np.array([-5.0 + 1.7 * i, 1.4, 0])
            I = island(c, w=1.5, h=1.1, seed=320 + i, color=WARM if i == 0 else ARG,
                       name=r"actual" if i == 0 else rf"$w_{i}$", font_size=17)
            cells.add(I)
        p_hl = cells[0].shape.copy().set_stroke(DIV, 5)
        pl = label(r"$p = \{\text{actual}\}$: \ the conjunction of all truths", font_size=19, color=DIV).move_to(
            [-2.45, 0.2, 0])
        hd = [r"\text{worlds}", r"\text{true propositions}", r"\text{contingent truths}",
              r"\text{could explain } p"]
        rows = [[MathTex(str(r["worlds"]), font_size=22), MathTex(str(r["true_propositions"]), font_size=22),
                 MathTex(str(r["contingent_truths"]), font_size=22),
                 MathTex(str(r["explainers_of_bccf"]), font_size=22, color=BAD)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[1.4, 2.6, 2.6, 2.4], cell_h=0.45, font_size=19).move_to([-2.1, -1.65, 0])
        side = stack([(r"an explainer must be true, \ entail $p$, \ and not be $p$", WHITE),
                      (r"only $p$ itself entails $p$ and is true", BAD),
                      (r"so the principle holds only with one world", DIV)], font_size=20, aligned_edge=LEFT,
                     width=3.6).move_to([5.05, -1.4, 0])
        with self.voiceover(
            "The Reasoner checks the argument on finite spaces of worlds. <bookmark mark='a'/>Propositions are sets of "
            "worlds. The conjunction of all truths at the actual world is the proposition true there and nowhere "
            "else. <bookmark mark='b'/>An explanation of it must be true, must entail it, and must not be it. "
            "<bookmark mark='c'/>With one world there is nothing contingent to explain. With two, three or four "
            "worlds there are contingent truths, and the number of propositions that could explain the big fact is "
            "zero every time, because the only true proposition that entails it is itself. "
            "<bookmark mark='d'/>So the principle can hold only if there is one world: everything true is necessary."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(Create(p_hl), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def responses(self):
        head = label(r"Ways out", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"explanation without entailment", r"Pruss \ (2006): \ a free choice, \ or a chance event, \ explains "
                                                r"without necessitating", ABS),
            (r"restrict the principle", r"every \textit{contingent being} has a cause, \ not every truth an "
                                       r"explanation", ARG),
            (r"accept the collapse", r"Spinoza; \ Della Rocca \ (2010): \ rationalism all the way, \ and "
                                     r"necessitarianism", HUM),
            (r"brute facts", r"some truths have no explanation: \ the world just is this way", NAT),
            (r"the lesson", r"the price of the principle is the price of Gödel's proof: \ watch it", GOAL),
        ]
        g = rows_table(rows, top=1.9, gap=0.45, width=7.8, x_text=-1.6, label_size=21, text_size=21)
        with self.voiceover(
            "There are ways out. <bookmark mark='a'/>Alexander Pruss denies that explanation must entail: a free "
            "choice, or a chance event, can explain what follows without necessitating it. Then God's free choice "
            "could explain the world while the world stays contingent. <bookmark mark='b'/>Or restrict the "
            "principle: every contingent being has a cause, without every truth having an explanation. "
            "<bookmark mark='c'/>Or accept the collapse, as Spinoza did and as Michael Della Rocca defends: "
            "rationalism all the way down, and necessity everywhere. <bookmark mark='d'/>Or accept brute facts: some "
            "truths have no explanation; the world is just this way. <bookmark mark='e'/>The lesson is the one Gödel's "
            "proof taught: the strongest premises for theism often cost modal collapse, and the price has to be "
            "checked."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
