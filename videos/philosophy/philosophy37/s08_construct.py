from __future__ import annotations

from videos.philosophy.philosophy37.common import *  # noqa: F403


class Construct(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Relativism and construction", r"Is morality made, \ and by whom?", lit=(1975, 1980),
                            part=PART)
        with self.voiceover("Chapter seven. Relativism and construction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.relativism()
        self.disagreement()
        self.peers()
        self.constructivism()
        self.dworkin()

    def relativism(self):
        head = label(r"Moral relativism", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"descriptive", r"moral codes differ across societies and ages: \ Herodotus's Greeks and Callatians, "
                                 r"\ on the treatment of the dead", GREY_A),
                (r"metaethical", r"moral claims are true or false only relative to a framework: \ Harman, \ "
                                 r"``Moral Relativism Defended'' \ (1975)", ANTI),
                (r"Harman's idea", r"morality as implicit agreement: \ an `ought' judgment presupposes that the agent "
                                   r"shares the relevant agreement", ANTI),
                (r"pluralistic", r"Wong \ (2006): \ more than one morality is true, \ but not every one: \ all must "
                                 r"serve the needs of social cooperation", REAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The oldest anti-realism is relativism. <bookmark mark='a'/>Descriptively, it is plainly true that moral "
            "codes differ: Herodotus tells how the Greeks, who burned their dead, were horrified to hear of the "
            "Callatians, who ate theirs, and how the Callatians were horrified in turn. <bookmark mark='b'/>The "
            "metaethical thesis says more: moral claims are true or false only relative to a framework. Gilbert "
            "Harman defended it in 1975. <bookmark mark='c'/>On his view morality rests on implicit agreements, and "
            "an inner ought judgment about someone presupposes that she shares the relevant agreement; so it is odd to "
            "say that Hitler ought not to have done what he did, though not odd to call him evil. "
            "<bookmark mark='d'/>David Wong's pluralistic relativism, of 2006, says more than one morality is true, "
            "but not every one: each must serve the needs of social cooperation in creatures like us."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def disagreement(self):
        head = label(r"The problem of disagreement", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        hd = [r"\text{speaker}", r"\text{says}", r"\text{relativist content}", r"\text{true?}"]
        cells = [[label(r"Ana", font_size=20, color=IS), label(r"`eating meat is wrong'", font_size=19),
                  label(r"wrong by Ana's standards", font_size=19, color=EXPR), mark(True, 22)],
                 [label(r"Ben", font_size=20, color=OUGHT), label(r"`eating meat is not wrong'", font_size=19),
                  label(r"not wrong by Ben's standards", font_size=19, color=EXPR), mark(True, 22)]]
        grid = ValueGrid(hd, cells, col_w=[1.6, 4.0, 4.4, 1.2], cell_h=0.6, font_size=18).move_to([0, 1.1, 0])
        foot = stack([(r"both claims true: \ so they do not contradict each other", GREY_A),
                      (r"but Ana and Ben seem to disagree, \ and to argue about something", BAD),
                      (r"replies: \ disagreement in attitude \ (Stevenson); \ assessment-sensitivity \ "
                       r"(MacFarlane, \ 2014): \ truth relative to the judge, \ not the speaker", EXPR)],
                     font_size=20, buff=0.22).move_to([0, -1.3, 0])
        with self.voiceover(
            "Relativism faces the problem of disagreement. <bookmark mark='a'/>Ana says eating meat is wrong; Ben says "
            "it is not. If what Ana says is that it is wrong by her standards, and what Ben says is that it is not "
            "wrong by his, then both are true, and they do not contradict each other. <bookmark mark='b'/>But they "
            "seem to disagree, and to argue about something. <bookmark mark='c'/>Relativists reply that the "
            "disagreement is in attitude, as Stevenson said, or, with John MacFarlane, that truth is relative to the "
            "one who assesses a claim rather than the one who makes it, so that each can rightly call the other "
            "wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for row in grid.cell for c in row], FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def peers(self):
        head = label(r"Disagreement as evidence", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the argument", r"persistent disagreement among informed, \ careful people is evidence that there is no fact to be found", ANTI),
                (r"the parallel", r"philosophers disagree about everything: \ is there no fact about free will, \ or about Part 2's logic?", GOAL),
                (r"peer disagreement", r"Part 12's question: \ should you lower your confidence when an equally informed peer disagrees?", IS),
                (r"the moral case", r"conciliationism about morality leaves very few moral beliefs standing", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Disagreement can also be treated as evidence. <bookmark mark='a'/>If informed, careful people go on "
            "disagreeing about morality, perhaps that is because there is no fact to be found. <bookmark "
            "mark='b'/>But philosophers disagree about almost everything; is there no fact about free will, or about "
            "logic? <bookmark mark='c'/>Part 12 asked whether you should lower your confidence when an equally "
            "informed peer disagrees. <bookmark mark='d'/>Applied to morality, the conciliatory answer would leave "
            "very few moral beliefs standing, which some take as a reason to reject it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def constructivism(self):
        head = label(r"Constructivism", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Rawls \ (1980)", r"``Kantian Constructivism in Moral Theory'': \ principles of justice are those "
                                    r"that would be chosen by a suitable procedure: \ Part 38's original position", REAL),
                (r"Korsgaard \ (1996)", r"\textit{The Sources of Normativity}: \ obligation comes from the reflective "
                                        r"structure of agency itself", OUGHT),
                (r"Street \ (2010)", r"Humean constructivism: \ normative truths are what follows from within the "
                                     r"practical point of view of a valuing creature", EXPR),
                (r"between", r"not discovered like stars, \ nor merely felt: \ made, \ but by constraints no one is "
                             r"free to ignore", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Constructivists look for a path between discovery and feeling. <bookmark mark='a'/>John Rawls's lectures "
            "on Kantian constructivism, of 1980, said that principles of justice are those that would be chosen by a "
            "suitably designed procedure, the original position of Part 38. <bookmark mark='b'/>Christine Korsgaard's "
            "The Sources of Normativity, of 1996, located obligation in the reflective structure of agency itself: to "
            "act at all, you must value your own humanity, and so, she argued, everyone's. "
            "<bookmark mark='c'/>Sharon Street's Humean constructivism says normative truths are whatever follows "
            "from within the practical point of view of a creature that values things. <bookmark mark='d'/>On each "
            "view moral truths are not discovered like stars, nor merely felt; they are made, but under constraints "
            "no agent is free to ignore."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def dworkin(self):
        head = label(r"Does metaethics matter? \ (Dworkin, \ 1996)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the challenge", r"``Objectivity and Truth: \ You'd Better Believe It'': \ there is no neutral standpoint outside morality from which to judge it", REAL),
                (r"the claim", r"`slavery is wrong, \ and would be wrong whatever anyone thought' is itself a moral claim", OUGHT),
                (r"the upshot", r"Archimedean skepticism is either a first-order moral view, \ to be argued as such, \ or nothing", BAD),
                (r"the reply", r"Blackburn; \ Street: \ the metaethicist asks a different question, \ about what moral claims are, \ not which ones are true", EXPR)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Ronald Dworkin argued in 1996 that the whole enterprise is confused. <bookmark mark='a'/>There is, he "
            "said, no neutral standpoint outside morality from which to assess it. <bookmark mark='b'/>The claim that "
            "slavery is wrong, and would be wrong whatever anyone thought, is itself a moral claim, made from inside. "
            "<bookmark mark='c'/>So a skeptic who denies it is making a moral claim too, which must be argued as "
            "such, or is saying nothing at all. <bookmark mark='d'/>Blackburn and Street replied that the "
            "metaethicist asks a different question: not which moral claims are true, but what it is for one to be."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
