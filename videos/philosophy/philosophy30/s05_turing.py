from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403


class Turing(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"The imitation game", r"Can machines think?", lit=(1950,), part=PART)
        with self.voiceover("Chapter four. The imitation game."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.game()
        self.objections()
        self.since()

    def game(self):
        hc = history_card(1950, r"Alan Turing", r"`Computing Machinery and Intelligence', \textit{Mind}", width=7.2,
                          color=HIST).to_corner(UL, buff=0.3)
        wall_ = Line([0, 1.6, 0], [0, -2.2, 0], color=GREY_B, stroke_width=6)
        judge = VGroup(Circle(radius=0.35, color=BEHAV), label(r"C", font_size=22, color=BEHAV)).move_to([-4.0, -0.3, 0])
        jl = label(r"the interrogator", font_size=17, color=BEHAV).next_to(judge, DOWN, buff=0.15)
        a = VGroup(Square(side_length=0.7, color=FUNC), label(r"A", font_size=22, color=FUNC)).move_to([3.4, 0.6, 0])
        b = VGroup(Circle(radius=0.35, color=FEEL), label(r"B", font_size=22, color=FEEL)).move_to([3.4, -1.2, 0])
        al = label(r"a machine", font_size=17, color=FUNC).next_to(a, RIGHT, buff=0.2)
        bl = label(r"a person", font_size=17, color=FEEL).next_to(b, RIGHT, buff=0.2)
        lines = VGroup(DashedLine(judge.get_right(), a.get_left(), color=GREY_C),
                       DashedLine(judge.get_right(), b.get_left(), color=GREY_C))
        tt = label(r"typed messages only", font_size=17, color=GREY_A).move_to([-1.6, 0.9, 0])
        rows = stack([(r"if C cannot reliably tell which is the machine, \ the machine wins", OK),
                      (r"Turing's forecast: \ by 2000, \ an average interrogator would have no more than a 70\% chance "
                       r"of being right after five minutes", HIST)], font_size=20, aligned_edge=LEFT, width=12.0,
                     buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Turing thought the question can machines think too vague to answer, and replaced it with a game. "
            "<bookmark mark='a'/>An interrogator, C, talks by typed messages with two players hidden from view. "
            "<bookmark mark='b'/>One, A, is a machine; the other, B, is a person. C may ask anything. "
            "<bookmark mark='c'/>If C cannot reliably tell which is the machine, the machine has won. "
            "<bookmark mark='d'/>Turing forecast that by the year 2000 computers would play so well that an average "
            "interrogator would have no more than a seventy percent chance of making the right identification after "
            "five minutes of questioning."
        ) as vo:
            self.play(FadeIn(hc), Create(wall_))
            vo.wait_until("a")
            self.play(FadeIn(judge), FadeIn(jl), Create(lines), FadeIn(tt))
            vo.wait_until("b")
            self.play(FadeIn(a), FadeIn(b), FadeIn(al), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def objections(self):
        head = label(r"Turing's nine objections, \ answered", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        objs = [
            (r"theological", r"thinking is a function of the soul", r"God could give a soul to a machine"),
            (r"heads in the sand", r"the consequences would be too dreadful", r"consolation, \ not refutation"),
            (r"mathematical", r"G\"odel: \ a machine cannot see the truth of its G\"odel sentence", r"nor can we, \ "
                                                                                                      r"of ours"),
            (r"consciousness", r"Jefferson: \ only when it writes a sonnet because of thoughts felt", r"then we cannot "
                                                                                                    r"know other "
                                                                                                    r"minds either"),
            (r"disabilities", r"it will never be kind, \ enjoy strawberries, \ fall in love \dots", r"induction from "
                                                                                                 r"the machines we "
                                                                                                 r"have seen"),
            (r"Lady Lovelace", r"it can only do what we order it to do", r"machines often surprise their makers"),
            (r"continuity", r"the nervous system is not discrete", r"a discrete machine can imitate a continuous one"),
            (r"informality", r"no rules could cover every circumstance", r"no \textit{rules of conduct}, \ perhaps; \ "
                                                                         r"\textit{laws of behaviour} still"),
            (r"extrasensory perception", r"telepathy would spoil the test", r"use a telepathy-proof room"),
        ]
        hd = [r"\text{objection}", r"\text{the claim}", r"\text{Turing's reply}"]
        cells = [[label(a, font_size=19, color=BAD), label(b, font_size=17, color=GREY_A),
                  label(c, font_size=17, color=OK)] for a, b, c in objs]
        grid = ValueGrid(hd, cells, col_w=[3.1, 5.7, 4.9], cell_h=0.57, font_size=20).move_to([0, -0.4, 0])
        with self.voiceover(
            "Turing then answered nine objections. <bookmark mark='a'/>The theological objection: thinking is a "
            "function of the soul. Turing: God could give a soul to a machine if he chose. "
            "<bookmark mark='b'/>The heads in the sand objection: the consequences would be too dreadful. That is a "
            "consolation, not a refutation. <bookmark mark='c'/>The mathematical objection: by Gödel's theorem, a "
            "machine cannot see the truth of its own Gödel sentence, from Part 7. Nor, Turing replied, has anyone "
            "shown that we can see ours. <bookmark mark='d'/>The argument from consciousness: Geoffrey Jefferson said "
            "no machine equals a brain until it writes a sonnet because of thoughts and emotions felt. Turing: then "
            "we cannot know that other people think either. <bookmark mark='e'/>Arguments from disabilities: it will "
            "never be kind, enjoy strawberries and cream, or fall in love. These are inductions from the machines we "
            "happen to have seen. <bookmark mark='f'/>Lady Lovelace's objection: a machine can only do what we order "
            "it to do. Turing: machines surprise him all the time. <bookmark mark='g'/>Continuity: the nervous system "
            "is not a discrete machine. But a discrete machine can imitate a continuous one well enough. "
            "<bookmark mark='h'/>Informality: no set of rules could cover every circumstance. Perhaps no rules of "
            "conduct, Turing said, but there may still be laws of behaviour. <bookmark mark='i'/>And extrasensory "
            "perception, which Turing took surprisingly seriously: put the players in a telepathy-proof room."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abcdefghi", range(9)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.6)
        self.clear_scene()

    def since(self):
        head = label(r"The test since", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"ELIZA \ (1966)", r"Weizenbaum's pattern-matching therapist: \ some users confided in it, \ to his "
                                r"dismay", HIST),
            (r"competitions", r"the Loebner Prize \ (1991--2019): \ chatbots that won by evasion and typos", BEHAV),
            (r"Jones and Bergen \ (2025)", r"in three-party tests, \ GPT-4.5 with a persona prompt was judged the human "
                                           r"73\% of the time", FUNC),
            (r"what it shows", r"a test of indistinguishability in conversation, \ not a definition of thinking: \ the "
                               r"next two chapters ask what it leaves out", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "The test has had a long afterlife. <bookmark mark='a'/>In 1966 Joseph Weizenbaum's ELIZA imitated a "
            "therapist by matching patterns in what users typed; to his dismay, some confided in it as if it "
            "understood. <bookmark mark='b'/>Competitions like the Loebner Prize, from 1991 to 2019, were often won by "
            "programs that dodged questions and faked typing errors. <bookmark mark='c'/>In 2025 Cameron Jones and "
            "Benjamin Bergen reported three-party tests, in Turing's own format, in which GPT-4.5, prompted to adopt "
            "a persona, was judged to be the human seventy-three percent of the time, more often than the real "
            "humans were. <bookmark mark='d'/>What would that show? The test measures indistinguishability in "
            "conversation. Whether that is thinking is the question of the next two chapters."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
