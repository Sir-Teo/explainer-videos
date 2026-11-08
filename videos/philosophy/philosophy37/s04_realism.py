from __future__ import annotations

from videos.philosophy.philosophy37.common import *  # noqa: F403


class Realism(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Moral realism", r"Are there moral facts, \ and what are they?", lit=(1991,), part=PART)
        with self.voiceover("Chapter three. Moral realism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.kinds()
        self.cornell()
        self.railton()
        self.supervenience()
        self.knowing()
        self.twin()

    def kinds(self):
        sv = load("tetrad")["survey"]
        assert sv["moral realism"] == 0.621
        head = label(r"Two kinds of realism", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the realist's claims", r"moral sentences state facts; \ some are true; \ their truth does not "
                                          r"depend on what anyone thinks of them", REAL),
                (r"non-naturalism", r"moral facts are sui generis, \ like the facts of logic or mathematics: \ "
                                    r"Shafer-Landau \ (2003), \ Enoch \ (2011), \ Parfit \ (2011)", OUGHT),
                (r"naturalism", r"moral properties are natural properties, \ found by inquiry: \ Boyd \ (1988), \ "
                                r"Brink \ (1989), \ Sturgeon \ (1985): \ the Cornell realists", IS),
                (r"PhilPapers 2020", r"62\% accept or lean toward moral realism", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.1, label_size=20, text_size=20)
        with self.voiceover(
            "Moral realism holds three things. <bookmark mark='a'/>Moral sentences state facts; some of them are true; "
            "and their truth does not depend on what anyone thinks of them. <bookmark mark='b'/>Non-naturalists, "
            "Moore's heirs, say the moral facts are sui generis, like the facts of logic or mathematics: Russ "
            "Shafer-Landau, David Enoch, and Derek Parfit, who argued in On What Matters that normative truths need "
            "no metaphysics at all. <bookmark mark='c'/>Naturalists say moral properties are natural properties, found "
            "by inquiry, as water was found to be H two O: Richard Boyd, David Brink and Nicholas Sturgeon, the "
            "Cornell realists. <bookmark mark='d'/>Realism is the majority view: sixty two percent of philosophers in "
            "the 2020 survey accept or lean toward it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def cornell(self):
        head = label(r"Moral facts that explain \ (Sturgeon, \ 1985)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Harman's challenge", r"we need physics to explain why the physicist sees a vapour trail; \ we "
                                        r"need no moral facts to explain why you judge the boys' cruelty wrong \ "
                                        r"(Harman, \ 1977)", ANTI),
                (r"Sturgeon's reply", r"Hitler's depravity explains what he did: \ remove it, \ and the explanation "
                                      r"fails", REAL),
                (r"causal regulation", r"`good' refers to whatever property causally regulates our use of it, \ as "
                                       r"`water' refers to H$_2$O \ (Boyd)", IS),
                (r"the test", r"a moral property earns its place if it figures in our best explanations", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.1, label_size=20, text_size=20)
        with self.voiceover(
            "The naturalists answered a challenge from Gilbert Harman. <bookmark mark='a'/>Harman argued in 1977 that "
            "we need physical facts to explain why a physicist sees a vapour trail in a cloud chamber, but we need no "
            "moral facts to explain why you judge it wrong when you see boys setting a cat on fire: your upbringing "
            "explains that. <bookmark mark='b'/>Nicholas Sturgeon replied that moral facts do explain. Hitler's "
            "depravity explains what he did; remove it, and the explanation fails. <bookmark mark='c'/>Richard Boyd "
            "added a theory of reference: good refers to whatever property causally regulates our use of the word, "
            "as water refers to H two O. <bookmark mark='d'/>On this view a moral property earns its place, like any "
            "other, by figuring in our best explanations."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def railton(self):
        head = label(r"A reforming definition \ (Railton, \ 1986)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"non-moral good", r"what you would want yourself to want, \ if you were fully informed and rational", IS),
                (r"moral rightness", r"what would be approved from a social point of view, \ taking everyone's interests equally", REAL),
                (r"reforming", r"not an analysis of what the words mean, \ but a revision that keeps their point", OUGHT),
                (r"the test", r"it is earned if it explains moral history: \ why unjust arrangements tend to generate unrest", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Peter Railton offered naturalism a different strategy in 1986. <bookmark mark='a'/>A person's non-moral "
            "good is what she would want herself to want, if she were fully informed and fully rational. <bookmark "
            "mark='b'/>Moral rightness is what would be approved from a social point of view, taking everyone's "
            "interests into account equally. <bookmark mark='c'/>This is not an analysis of what the words mean, "
            "which Moore's argument would test, but a reforming definition: a revision that keeps their point. "
            "<bookmark mark='d'/>It earns its place, Railton argued, if it helps explain moral history, for instance "
            "why social arrangements that neglect some people's interests tend to generate discontent and change."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def supervenience(self):
        head = label(r"The supervenience challenge \ (Blackburn, \ 1971)", font_size=30, color=CONN).to_edge(UP,
                                                                                                             buff=0.35)
        f = MathTex(r"\Box\,\forall x\,\forall y\,\big(x \text{ and } y \text{ are naturally alike} \;\to\; "
                    r"x \text{ and } y \text{ are morally alike}\big)", font_size=30, color=OUGHT).move_to([0, 1.6, 0])
        rows = stack([(r"no two acts can differ in rightness without differing in some natural respect: \ everyone "
                       r"accepts this", GREY_A),
                      (r"but if moral properties are distinct from natural ones, \ why must they covary, \ of "
                       r"necessity?", BAD),
                      (r"the realist owes an explanation of a necessary connection between distinct existences", BAD),
                      (r"Blackburn: \ the expressivist explains it: \ consistency in attitudes requires treating "
                       r"alike what is alike", EXPR)],
                     font_size=20, aligned_edge=LEFT, width=11.6, buff=0.3).move_to([0, -0.8, 0])
        with self.voiceover(
            "Simon Blackburn posed a problem for the non-naturalist in 1971. <bookmark mark='a'/>Moral properties "
            "supervene on natural ones: necessarily, two acts alike in every natural respect are alike morally. No "
            "two acts can differ in rightness without differing in something else. Everyone accepts this. "
            "<bookmark mark='b'/>But if moral properties are distinct from natural ones, why must they covary, as a "
            "matter of necessity? <bookmark mark='c'/>The non-naturalist owes an explanation of a necessary connection "
            "between distinct existences, the kind of thing Hume said there cannot be. <bookmark mark='d'/>Blackburn "
            "thought his own view explains it easily: if moral judgments express attitudes, consistency in our "
            "attitudes requires treating alike what is alike."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def knowing(self):
        head = label(r"How could we know?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"intuitionism", r"some moral truths are self-evident to a mature mind: \ Ross \ (1930); \ Audi; \ "
                                  r"Huemer, \ \textit{Ethical Intuitionism} \ (2005)", REAL),
                (r"seemings", r"if it seems to you that torturing for fun is wrong, \ you have a reason to believe it, "
                              r"\ unless defeated", GREY_A),
                (r"moral perception", r"we can see that an act is cruel, \ as we see that a face is angry \ "
                                      r"(McGrath, \ 2019)", REAL),
                (r"the puzzle of testimony", r"deferring to experts about geography is fine; \ about whether eating "
                                             r"meat is wrong, \ it seems odd \ (Hills, \ 2009)", BAD),
                (r"the question", r"why should moral knowledge, \ if there is any, \ need understanding rather than "
                                  r"trust?", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.42, width=8.4, x_text=-2.0, label_size=20, text_size=19)
        with self.voiceover(
            "A realist also owes an account of moral knowledge. <bookmark mark='a'/>Intuitionists say some moral "
            "truths are self-evident to a mature and attentive mind: W. D. Ross's prima facie duties of Part 35, and, "
            "more recently, Robert Audi and Michael Huemer. <bookmark mark='b'/>On Huemer's view, if it seems to you "
            "that torturing for fun is wrong, you thereby have a reason to believe it, unless something defeats the "
            "seeming. <bookmark mark='c'/>Others speak of moral perception: we can see that an act is cruel, as we see "
            "that a face is angry. <bookmark mark='d'/>A puzzle about testimony tests all of this. Deferring to an "
            "expert about geography is fine; deferring about whether eating meat is wrong seems odd, as Alison Hills "
            "and others have noted. <bookmark mark='e'/>Why should moral knowledge, if there is any, require your "
            "own understanding rather than trust? Anti-realists think the oddity is a clue."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def twin(self):
        head = label(r"Moral twin earth \ (Horgan and Timmons, \ 1991)", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.35)
        e = VGroup(Circle(radius=0.7, color=IS, fill_opacity=0.15), label(r"Earth", font_size=20, color=IS))
        t = VGroup(Circle(radius=0.7, color=OUGHT, fill_opacity=0.15), label(r"Twin Earth", font_size=20, color=OUGHT))
        e.move_to([-4.0, 1.0, 0])
        t.move_to([-1.0, 1.0, 0])
        le = wrapped_label(r"`good' regulated by consequentialist properties", 2.7, 17, IS).next_to(
            e, DOWN, buff=0.2)
        lt = wrapped_label(r"`good' regulated by deontological properties", 2.7, 17, OUGHT).next_to(
            t, DOWN, buff=0.2)
        side = stack([(r"`water' and `twater': \ different meanings, \ no real disagreement \ (Putnam)", GREY_A),
                      (r"`good' and `twin good': \ the two peoples still seem to disagree when they argue", OUGHT),
                      (r"so the meaning of `good' is not fixed by what causally regulates it", BAD),
                      (r"a problem for Cornell realism, \ and a point for expressivism: \ disagreement in attitude",
                       EXPR)],
                     font_size=19, aligned_edge=LEFT, width=5.6, buff=0.3).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "Terry Horgan and Mark Timmons answered Boyd with a thought experiment in 1991. <bookmark mark='a'/>On "
            "Putnam's twin earth, a liquid like water is made of XYZ; their word water means something different from "
            "ours, and there is no real disagreement between us about it. <bookmark mark='b'/>Now imagine a moral "
            "twin earth, where the word good is causally regulated by deontological properties, while ours is "
            "regulated by consequentialist ones. On Boyd's theory, the two words mean different things. "
            "<bookmark mark='c'/>But when an earther and a twin earther argue over whether to break a promise for the "
            "greater good, they seem to disagree, not to talk past each other. <bookmark mark='d'/>So the meaning of "
            "good is not fixed by what causally regulates it, and the disagreement looks like a clash of attitudes: a "
            "point for the expressivists."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(e), FadeIn(t), FadeIn(le), FadeIn(lt), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
