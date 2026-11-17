from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403


class Games(VoiceoverScene):
    def construct(self):
        self.card()
        self.five()
        self.dilemma()

    def card(self):
        card = chapter_card(2, r"Games as experiments", r"What does ``rational'' predict, \ and what do people do?",
                            lit={1982: r"G\"uth et al."}, part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter two. Games as experiments."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def five(self):
        head = heading(r"Five games")
        data = (
            (r"dictator", r"one person divides a sum; \ the other has no say", r"give nothing",
             r"many give something", CROWD),
            (r"ultimatum", r"the responder can reject, \ and then both get nothing", r"offer the minimum; \ accept "
             r"it", r"offers near 40\%; \ low offers rejected", PERSON),
            (r"trust", r"an investor sends money, \ which is multiplied; \ the trustee may send some back",
             r"send nothing", r"many send, \ and many repay", GOOD),
            (r"prisoner's dilemma", r"each cooperates or defects; \ defecting pays more whatever the other does",
             r"defect", r"many cooperate, \ at least at first", MODEL),
            (r"public goods", r"each puts some of an endowment into a pot that is multiplied and shared",
             r"contribute nothing", r"about half at first, \ then decline", AUTH))
        lefts, widths = (-6.5, -3.4, 1.3, 4.0), (2.7, 4.4, 2.4, 2.6)
        rows = VGroup()
        for k, (name, rule, pred, real, c) in enumerate(data):
            y = 1.5 - 0.95 * k
            cells = [word_chip(name, color=c, font_size=18, width=widths[0]), wrapped_label(rule, widths[1], 17, WHITE),
                     wrapped_label(pred, widths[2], 17, GREY_A), wrapped_label(real, widths[3], 17, c)]
            for cell, x0 in zip(cells, lefts):
                cell.move_to([x0, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(*cells))
        hdr = VGroup(*[label(t, font_size=16, color=GREY_B).move_to([x0, 2.25, 0], aligned_edge=LEFT)
                       for t, x0 in zip((r"the rule", r"selfish prediction", r"what people do"), lefts[1:])])
        with self.voiceover(
            "Economists turned simple games into experiments, with real money. <bookmark mark='a'/> In the dictator "
            "game, one person divides a sum and the other has no say. A selfish player gives nothing. Many give "
            "something. <bookmark mark='b'/> In the ultimatum game the responder can reject, and offers sit near "
            "forty percent. <bookmark mark='c'/> In the trust game, an investor sends money that is multiplied, and "
            "the trustee may send some back. Selfish players send nothing; many people send, and many repay. "
            "<bookmark mark='d'/> In the prisoner's dilemma, defecting pays more whatever the other does, yet many "
            "people cooperate, at least at first. <bookmark mark='e'/> And in the public-goods game, everyone puts "
            "some money into a pot that is multiplied and shared. People start by contributing about half, and then "
            "it declines. The theory of these games is in Philosophy, Built, Part 34."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def dilemma(self):
        head = heading(r"The prisoner's dilemma")
        cells = VGroup()
        pays = {(0, 0): (r"3, \ 3", GOOD), (0, 1): (r"0, \ 5", AUTH), (1, 0): (r"5, \ 0", AUTH),
                (1, 1): (r"1, \ 1", GREY_A)}
        for (i, j), (t, c) in pays.items():
            sq = Square(side_length=1.5, stroke_color=GREY_D, fill_color="#14181F", fill_opacity=1)
            sq.move_to([-4.2 + 1.5 * j, 0.9 - 1.5 * i, 0])
            cells.add(VGroup(sq, label(t, font_size=24, color=c).move_to(sq)))
        top = VGroup(label(r"cooperate", font_size=16, color=GREY_A).move_to([-4.2, 1.95, 0]),
                     label(r"defect", font_size=16, color=GREY_A).move_to([-2.7, 1.95, 0]))
        side = VGroup(label(r"cooperate", font_size=16, color=GREY_A).move_to([-5.6, 0.9, 0]),
                      label(r"defect", font_size=16, color=GREY_A).move_to([-5.6, -0.6, 0]))
        rows = rows_of([
            (r"payoffs per move (yours, \ theirs): \ both cooperate, \ 3 each; \ both defect, \ 1 each", WHITE),
            (r"whatever the other does, \ defecting pays more: \ 5 instead of 3, \ or 1 instead of 0", AUTH),
            (r"so two rational players defect and get 1 each, \ when both could have had 3", PERSON),
            (r"played once with a stranger, \ the logic is airtight; \ played again and again, \ it is not", GOOD),
        ], 6.4, 20, 0.38).move_to([3.0, -0.2, 0])
        with self.voiceover(
            "The prisoner's dilemma is the cleanest of them. <bookmark mark='a'/> Here are the points per move. If "
            "both cooperate, three each. If both defect, one each. <bookmark mark='b'/> Whatever the other player "
            "does, defecting pays more: five instead of three, or one instead of nothing. <bookmark mark='c'/> So "
            "two rational players defect and get one each, when both could have had three. "
            "<bookmark mark='d'/> Played once with a stranger, the logic is airtight. Played again and again with "
            "the same person, it isn't."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(top), FadeIn(side))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(cells[0]), Indicate(cells[3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(cells[2]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
