from __future__ import annotations

from videos.philosophy.philosophy37.common import *  # noqa: F403


class Moore(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"The open question", r"Can goodness be defined?", lit=(1903,), part=PART)
        with self.voiceover("Chapter two. The open question."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.argument()
        self.fallacy()
        self.ideal()
        self.analysis()
        self.thick()

    def argument(self):
        hc = history_card(1903, r"G. E. Moore", r"\textit{Principia Ethica}", width=5.0, color=HIST).to_corner(
            UL, buff=0.3)
        q1 = label(r"``Is pleasure pleasure?''", font_size=30, color=GREY_A).move_to([-2.6, 0.6, 0])
        q2 = label(r"``Is pleasure good?''", font_size=30, color=OUGHT).move_to([2.6, 0.6, 0])
        c1 = label(r"closed: \ a competent speaker cannot wonder", font_size=19, color=GREY_A).next_to(q1, DOWN,
                                                                                                   buff=0.25)
        c2 = label(r"open: \ a competent speaker can wonder", font_size=19, color=OUGHT).next_to(q2, DOWN, buff=0.25)
        foot = stack([(r"if `good' meant `pleasant', \ the two questions would be the same", GREY_A),
                      (r"the same test, \ for any natural property $N$: \ `is $N$ good?' \ stays open", OUGHT),
                      (r"so `good' names a simple, \ non-natural property, \ known by intuition", REAL)],
                     font_size=20, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "G. E. Moore's Principia Ethica, of 1903, gave the twentieth century its starting point. "
            "<bookmark mark='a'/>Ask: is pleasure pleasure? The question is closed: no competent speaker can wonder "
            "about it. <bookmark mark='b'/>Now ask: is pleasure good? That question is open; a competent speaker can "
            "sensibly wonder. <bookmark mark='c'/>But if good simply meant pleasant, the two questions would be the "
            "same question. <bookmark mark='d'/>Run the test for any natural property you like, what we desire to "
            "desire, what maximizes survival: the question whether it is good stays open. "
            "<bookmark mark='e'/>So, Moore concluded, good names a simple property that is not natural, and that we "
            "know by intuition."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q1), FadeIn(c1))
            vo.wait_until("b")
            self.play(FadeIn(q2), FadeIn(c2))
            for mk, r in zip("cde", foot):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def fallacy(self):
        head = label(r"The naturalistic fallacy", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Moore's charge", r"identifying goodness with any natural property: \ pleasure \ (Bentham), \ "
                                    r"what is more evolved \ (Spencer)", OUGHT),
                (r"not a fallacy of inference", r"it is a claim about meaning: \ that the definition is false", GREY_A),
                (r"Frankena \ (1939)", r"the argument assumes what it sets out to prove: \ that goodness is not "
                                       r"identical with the natural property", BAD),
                (r"its legacy", r"a century of non-naturalism, \ intuitionism and, \ in reaction, \ noncognitivism",
                 EXPR)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.1, label_size=20, text_size=20)
        with self.voiceover(
            "Moore called the mistake he had found the naturalistic fallacy. <bookmark mark='a'/>It is the error, he "
            "said, of identifying goodness with some natural property: with pleasure, as Bentham did, or with what is "
            "more evolved, as Herbert Spencer did. <bookmark mark='b'/>It is not a fallacy of inference, but a claim "
            "about meaning: that every such definition is false. <bookmark mark='c'/>William Frankena replied in 1939 "
            "that the argument assumes what it sets out to prove: that goodness is not identical with the natural "
            "property. A naturalist will say that the question only seems open. <bookmark mark='d'/>Even so, Moore's "
            "argument shaped a century: the non-naturalists and intuitionists who followed him, and, in reaction, "
            "the noncognitivists of chapter five."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def ideal(self):
        head = label(r"Moore's ideal", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"intuition", r"what is good in itself cannot be proved, \ only seen: \ the isolation test: \ would it be good if it existed quite alone?", REAL),
                (r"organic unities", r"the value of a whole need not be the sum of the values of its parts", OUGHT),
                (r"the greatest goods", r"\textit{Principia}, \ chapter 6: \ the pleasures of human intercourse and the enjoyment of beautiful objects", GOAL),
                (r"its influence", r"read as a manifesto by the Bloomsbury Group: \ Keynes, \ Woolf, \ Forster", GREY_A)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Moore's positive view was as influential as his argument. <bookmark mark='a'/>What is good in itself "
            "cannot be proved, only seen; his test was isolation: would this be good if it existed quite alone? "
            "<bookmark mark='b'/>Wholes, he added, are organic unities: the value of a whole need not be the sum of "
            "the values of its parts. <bookmark mark='c'/>And the greatest goods, the last chapter of Principia said, "
            "are the pleasures of human intercourse and the enjoyment of beautiful objects. <bookmark mark='d'/>The "
            "young Keynes, Virginia Woolf and E. M. Forster of the Bloomsbury Group read it as a manifesto."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def analysis(self):
        head = label(r"The paradox of analysis, \ and water", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        a1 = label(r"`a brother is a male sibling'", font_size=24, color=GREY_A).move_to([-3.4, 1.4, 0])
        a2 = label(r"`water is H$_2$O'", font_size=24, color=IS).move_to([3.4, 1.4, 0])
        t1 = label(r"if correct, \ uninformative; \ if informative, \ incorrect?", font_size=19, color=BAD).next_to(
            a1, DOWN, buff=0.25)
        t2 = label(r"true, \ necessary, \ and discovered: \ `is water H$_2$O?' \ was an open question", font_size=19,
                   color=IS).next_to(a2, DOWN, buff=0.25)
        foot = stack([(r"Langford \ (1942): \ the paradox of analysis: \ the open question test proves too much", BAD),
                      (r"Putnam; \ Kripke \ (Part 22): \ identities can be necessary and a posteriori", IS),
                      (r"so `goodness is $N$' might be true, \ and still sound open: \ the opening for naturalism", REAL)],
                     font_size=20, buff=0.22).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Two replies changed the debate. <bookmark mark='a'/>The first is the paradox of analysis, put by Cooper "
            "Harold Langford in 1942. A correct analysis, like a brother is a male sibling, seems uninformative; an "
            "informative one seems incorrect. The open question test would condemn every interesting analysis "
            "of anything. <bookmark mark='b'/>The second came from the philosophy of language of Part 22. Water is H "
            "two O is true, necessary, and was discovered: is water H two O? was once an open question. "
            "<bookmark mark='c'/>So goodness might be identical with some natural property, though the identity "
            "sounds open, because it is known a posteriori, not by analysing a concept. <bookmark mark='d'/>That is "
            "the opening for the naturalist realism of the next chapter."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a1), FadeIn(t1), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(a2), FadeIn(t2), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
            vo.wait_until("d")
            self.wait(0.5)
        self.clear_scene()

    def thick(self):
        head = label(r"Thin and thick", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"thin concepts", r"good, \ right, \ ought: \ evaluation with little descriptive content", OUGHT),
                (r"thick concepts", r"cruel, \ courageous, \ lewd, \ tactful: \ description and evaluation at once \ (Williams, \ 1985)", IS),
                (r"the disentangling debate", r"Hare: \ a neutral description plus a thin verdict; \ McDowell \ (1981): \ the extension cannot be grasped without the evaluative point", REAL),
                (r"Foot \ (1958)", r"`rude' applies only where offence is given: \ facts fix whether the word applies", EXPR),
                (r"V\"{a}yrynen \ (2013)", r"\textit{The Lewd, \ the Rude and the Nasty}: \ the evaluation may be a pragmatic implication, \ not part of the meaning", ANTI)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Moore's question concerns thin concepts. <bookmark mark='a'/>Good, right and ought evaluate while saying "
            "very little about what their objects are like. <bookmark mark='b'/>Bernard Williams, in Ethics and the "
            "Limits of Philosophy, of 1985, drew attention to thick concepts such as cruel, courageous, lewd and "
            "tactful, which seem to describe and evaluate at once. If they do, the line between is and ought runs "
            "through the middle of our vocabulary. <bookmark mark='c'/>Hare held that a thick term can be "
            "disentangled into a neutral description plus a thin verdict. John McDowell replied that one cannot learn "
            "which acts count as cruel without grasping the evaluative point of the word, so no neutral description "
            "picks out the same acts. <bookmark mark='d'/>Philippa Foot had argued in 1958 that a word like rude "
            "applies only where offence is given, so facts settle whether it applies. <bookmark mark='e'/>And Pekka "
            "Väyrynen's The Lewd, the Rude and the Nasty, of 2013, argued that the evaluation carried by thick terms "
            "is often a pragmatic implication rather than part of their meaning, which would restore the gap."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
