from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class Answers(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Four answers to the skeptic", r"Which claim should go?", lit=(1939, 1996),
                            part=PART)
        with self.voiceover("Chapter twelve. Four answers to the skeptic."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.moore()
        self.dretske()
        self.context()
        self.putnam()

    def moore(self):
        hc = history_card(1939, r"G.\ E.\ Moore", r"`Proof of an External World'", width=5.2,
                          color=HIST).to_corner(UL, buff=0.35)
        hands = VGroup(*[VGroup(RoundedRectangle(width=0.55, height=0.8, corner_radius=0.2, color=JUST,
                                                 fill_opacity=0.3),
                                *[RoundedRectangle(width=0.12, height=0.42, corner_radius=0.05, color=JUST,
                                                   fill_opacity=0.3).move_to([-0.2 + 0.13 * k, 0.6, 0])
                                  for k in range(4)]) for _ in range(2)]).arrange(RIGHT, buff=1.0).scale(1.6).move_to(
            [3.6, 1.7, 0])
        rows = VGroup(
            label(r"`Here is one hand, \ and here is another': \ so external things exist", font_size=25, color=JUST),
            label(r"the premise is more certain \ than any premise of the skeptic's argument", font_size=24),
            label(r"so run the argument backwards: \ I know I have hands, \ so I know I'm not envatted",
                  font_size=24, color=OK),
            label(r"Wittgenstein, \textit{On Certainty} (1969): \ such propositions are `hinges' \ on which doubt "
                  r"itself turns", font_size=23, color=GREY_A)).arrange(DOWN, buff=0.3).move_to([0, -1.0, 0])
        with self.voiceover(
            "First, the answer of G. E. Moore. <bookmark mark='a'/>In a lecture of 1939 he held up his hands and said: "
            "here is one hand, and here is another. So there are at least two external things, and so an external "
            "world. <bookmark mark='b'/>This sounds like cheating, but Moore's point was about certainty. He is more "
            "certain that he has hands than he could ever be of any premise in a skeptical argument. "
            "<bookmark mark='c'/>One person's modus ponens is another's modus tollens: run the skeptic's argument "
            "backwards. I know I have hands; so, by closure, I know I am not a brain in a vat. "
            "<bookmark mark='d'/>Ludwig Wittgenstein, in notes written in the last eighteen months of his life and "
            "published as On Certainty, gave this a deeper form. Propositions like here is a hand are not known on "
            "evidence. They are hinges: the questions we raise and our doubts depend on some propositions being "
            "exempt from doubt."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(hands, shift=UP * 0.2), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def dretske(self):
        head = label(r"Give up closure", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        z = VGroup(*[Line([x, -0.25, 0], [x + 0.18, 0.25, 0], color=WHITE, stroke_width=6) for x in
                     np.arange(-0.9, 0.9, 0.3)])
        zbox = SurroundingRectangle(z, buff=0.2, color=GREY_B, corner_radius=0.1)
        zebra = VGroup(zbox, z).move_to([-3.6, 1.0, 0])
        zl = label(r"in the zebra pen at the zoo", font_size=21, color=GREY_A).next_to(zebra, DOWN, buff=0.15)
        rows = VGroup(
            label(r"Dretske (1970): \ I know `that is a zebra'", font_size=24, color=OK),
            label(r"it implies `that is not a mule cleverly painted to look like a zebra'", font_size=22),
            label(r"which I have not checked, \ and do not know", font_size=24, color=BAD),
            label(r"knowledge does not pass along every known implication", font_size=24, color=GOAL),
            label(r"the price: \ `I know it's a zebra, \ but not that it's not a painted mule' \ "
                  r"(an abominable conjunction again)", font_size=22, color=LUCK)).arrange(DOWN, buff=0.25).move_to(
            [0, -1.3, 0])
        with self.voiceover(
            "The second answer gives up closure. <bookmark mark='a'/>Fred Dretske's example, from 1970: at the zoo "
            "I see a striped animal in the zebra pen, and I know that it is a zebra. <bookmark mark='b'/>Being a "
            "zebra implies not being a mule cleverly painted to look like one. <bookmark mark='c'/>But I have not "
            "checked for paint, and I would believe it was a zebra even if it were a painted mule. So I do not know "
            "that it is not a painted mule. <bookmark mark='d'/>Knowledge, Dretske concluded, does not pass along "
            "every known implication, and Nozick's sensitivity gave the same verdict, as the Reasoner found in "
            "chapter six. <bookmark mark='e'/>The price is sentences like: I know it's a zebra, but I don't know it "
            "isn't a painted mule. To most ears, that sounds absurd."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(zebra), FadeIn(zl), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def context(self):
        d = load("bank")
        hc = history_card(1996, r"David Lewis", r"`Elusive Knowledge'", width=4.6, color=HIST).to_corner(UL, buff=0.35)
        q = quote_card(r"S knows that P iff P holds in every possibility left uneliminated by S's evidence---Psst!---"
                       r"except for those possibilities that we are properly ignoring.", r"David Lewis", "",
                       width=8.0, font_size=22).move_to([2.4, 2.3, 0])
        poss = d["possibilities"]
        hd = [label(r"possibility", font_size=20, color=P.CLAIM), label(r"bank open?", font_size=20, color=P.CLAIM),
              label(r"Friday, \ no rush", font_size=20, color=P.CLAIM),
              label(r"rent due Monday", font_size=20, color=P.CLAIM)]
        rows = []
        for i, p in enumerate(poss):
            if p["p"]:
                lo = label(r"actual, \ as far as I know", font_size=19, color=GREY_A)
                hi = label(r"actual, \ as far as I know", font_size=19, color=GREY_A)
            else:
                lo = label(r"properly ignored", font_size=19, color=OK)
                hi = label(r"not eliminated", font_size=19, color=BAD)
            rows.append([label(p["name"], font_size=19), mark(p["p"], 22), lo, hi])
        grid = ValueGrid(hd, rows, col_w=[5.2, 1.6, 2.6, 2.6], cell_h=0.52, font_size=19).move_to([0, -0.6, 0])
        assert d["careless"][0] and not d["careful"][0]
        verdict = VGroup(
            VGroup(label(r"`I know it's open Saturday'", font_size=20, color=OK),
                   label(r"true", font_size=22, color=OK)).arrange(DOWN, buff=0.08).move_to(
                [grid.cell[0][2].get_x(), -2.35, 0]),
            VGroup(label(r"`I know it's open Saturday'", font_size=20, color=BAD),
                   label(r"false", font_size=22, color=BAD)).arrange(DOWN, buff=0.08).move_to(
                [grid.cell[0][3].get_x(), -2.35, 0]))
        foot = VGroup(label(r"contextualism: \ the standard for `knows' shifts with the speaker's context \ (DeRose 1992)",
                            font_size=20, color=GREY_A),
                      label(r"subject-sensitive invariantism: \ with the subject's stakes \ (Hawthorne 2004, \ Stanley "
                            r"2005)", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "The third answer is contextualism. <bookmark mark='a'/>David Lewis put it in one sentence: S knows that "
            "P if and only if P holds in every possibility left uneliminated by S's evidence, psst, except for those "
            "possibilities that we are properly ignoring. <bookmark mark='b'/>Keith DeRose's bank case. On a Friday "
            "afternoon I want to deposit a cheque, but the queues are long. I was at the bank two Saturdays ago, so "
            "I say: I know it's open on Saturday. <bookmark mark='c'/>The Reasoner applies Lewis's rule. My evidence "
            "eliminates nothing beyond what I saw. In the relaxed context, the possibilities that the bank has "
            "changed its hours, or that a pipe will burst, are properly ignored. Every not-P possibility is "
            "accounted for: I know. <bookmark mark='d'/>Now the rent is due on Monday, and my partner asks: banks "
            "do change their hours; do you know? Once mentioned, those possibilities cannot be properly ignored, and "
            "my evidence does not eliminate them. Now it is false to say I know. <bookmark mark='e'/>For the "
            "contextualist, the skeptic does not refute ordinary knowledge; she changes the context, by making the "
            "vat a live possibility. A related view, subject-sensitive invariantism, lets the subject's own stakes, "
            "not the speaker's context, set the standard."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg),
                      *[FadeIn(VGroup(*grid.cell[r][:2])) for r in range(len(rows))])
            vo.wait_until("c")
            self.play(*[FadeIn(grid.cell[r][2]) for r in range(len(rows))])
            self.play(FadeIn(verdict[0]))
            vo.wait_until("d")
            self.play(*[FadeIn(grid.cell[r][3]) for r in range(len(rows))])
            self.play(FadeIn(verdict[1]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def putnam(self):
        hc = history_card(1981, r"Hilary Putnam", r"\textit{Reason, Truth and History}, \ ch.\ 1", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        steps = VGroup(
            label(r"words refer to what causes their use \ (semantic externalism)", font_size=24, color=JUST),
            label(r"a brain in a vat has never been in causal contact with brains or vats", font_size=23),
            label(r"so its word `vat' refers to vat-images, \ or to features of the program", font_size=23),
            label(r"so when it thinks `I am a brain in a vat', \ the thought is false", font_size=24, color=BAD),
            label(r"and when I think it, \ it is false too: \ so I am not a brain in a vat", font_size=24, color=OK),
            label(r"the limit: \ it rules out only the permanently envatted, \ not a brain envatted last night",
                  font_size=22, color=GREY_A)).arrange(DOWN, buff=0.27).move_to([0, -0.5, 0])
        with self.voiceover(
            "The last answer is Hilary Putnam's, and it is the strangest. <bookmark mark='a'/>Putnam held that our "
            "words refer to what we are causally connected with in the right way. <bookmark mark='b'/>A brain that "
            "has always been in a vat has never been in contact with real brains or vats. <bookmark mark='c'/>So in "
            "its language, vat refers to vat-images, or to features of the program that produces them. "
            "<bookmark mark='d'/>Then when it thinks, I am a brain in a vat, it says something false: it is not in "
            "an image of a vat. <bookmark mark='e'/>And when I think it, in my language, where vat means vat, it is "
            "false if I am not envatted, and false if I am. Either way it is false, so I am not a brain in a vat. "
            "<bookmark mark='f'/>The argument works only against a brain that has always been in a vat. It says "
            "nothing against one that was envatted last night, whose words still refer to real vats."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, s_ in zip("abcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=UP * 0.1))
        self.clear_scene()
