from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


def kings_model():
    """A domain with no present king of France, and bald things: evaluate the two readings of `The present king of
    France is not bald' and the description itself, by brute force over the domain."""
    domain = ["Macron", "Charles III", "Yul Brynner"]
    king_fr = set()
    bald = {"Yul Brynner"}
    the_f = [x for x in domain if x in king_fr]
    exists_unique = len(the_f) == 1
    narrow = exists_unique and the_f[0] not in bald           # E!x (Kx & ~Bx)
    wide = not (exists_unique and the_f[0] in bald)           # ~ E!x (Kx & Bx)
    return {"domain": domain, "kings": sorted(king_fr), "bald": sorted(bald), "narrow": narrow, "wide": wide,
            "plain": exists_unique and the_f[0] in bald}


class Meinong(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Meinong's jungle and Russell's escape", r"Are there things that do not exist?",
                            lit=(1904, 1905), part=PART)
        with self.voiceover("Chapter two. Meinong's jungle and Russell's escape."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.jungle()
        self.russell()
        self.scope()
        self.neo()
        self.fiction()

    def jungle(self):
        hc = history_card(1904, r"Alexius Meinong", r"`On the Theory of Objects'", width=5.4, color=HIST).to_corner(
            UL, buff=0.35)
        mtn = Polygon([-5.8, -2.2, 0], [-4.4, 0.2, 0], [-3.0, -2.2, 0], color=GOAL, fill_opacity=0.45)
        sq = VGroup(Square(side_length=1.3, color=NOM, stroke_width=3), Circle(radius=0.65, color=NOM,
                                                                                stroke_width=3)).move_to(
            [-1.8, -1.4, 0])
        ml = label(r"the golden mountain", font_size=16, color=GOAL).next_to(mtn, DOWN, buff=0.12)
        sl = label(r"the round square", font_size=16, color=NOM).next_to(sq, DOWN, buff=0.12)
        rows = stack([(r"every thought is directed at an object, \ even when nothing answers to it", WHITE),
                      (r"\textit{Sosein} \ (being so) \ without \textit{Sein} \ (being): \ the golden mountain is "
                       r"golden, \ yet does not exist", GOAL),
                      (r"even impossible objects: \ the round square is round \textit{and} square", NOM),
                      (r"Russell: \ then the \textit{existent} golden mountain exists?", BAD),
                      (r"Meinong: \ it is existent, \ but does not exist", GREY_A)], font_size=20,
                     aligned_edge=LEFT, width=6.6).move_to([3.2, -0.4, 0])
        with self.voiceover(
            "Alexius Meinong took the opposite route from Quine. <bookmark mark='a'/>Every thought, he held, is "
            "directed at an object, even when nothing in the world answers to it. <bookmark mark='b'/>An object can "
            "have being-so without being. The golden mountain really is golden and a mountain; it simply does not "
            "exist. <bookmark mark='c'/>There are even impossible objects: the round square is round and square. "
            "<bookmark mark='d'/>Russell objected: then the existent golden mountain must exist, since it has every "
            "property in its description. <bookmark mark='e'/>Meinong replied that it is existent, but does not "
            "exist, a distinction few found reassuring. Quine, mocking a similar view, spoke of a slum of possibles."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(mtn), FadeIn(ml), Create(sq), FadeIn(sl))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def russell(self):
        hc = history_card(1905, r"Bertrand Russell", r"`On Denoting', \textit{Mind}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        s = label(r"`The present King of France is bald'", font_size=26, color=WHITE).move_to([1.6, 2.2, 0])
        f = MathTex(r"\exists x \, \big(", r"Kx", r"\;\land\;", r"\forall y \, (Ky \to y = x)", r"\;\land\;", r"Bx",
                    r"\big)", font_size=36).move_to([0.6, 0.9, 0])
        f[1].set_color(PARTC)
        f[3].set_color(UNIV)
        f[5].set_color(WHOLE)
        notes = VGroup(label(r"there is a king", font_size=16, color=PARTC).next_to(f[1], DOWN, buff=0.35),
                       label(r"at most one", font_size=16, color=UNIV).next_to(f[3], DOWN, buff=0.35),
                       label(r"he is bald", font_size=16, color=WHOLE).next_to(f[5], DOWN, buff=0.35))
        rows = stack([(r"`the F' is not a name: \ it vanishes on analysis into quantifiers", OK),
                      (r"no king, \ so the sentence is simply \textit{false}: \ no object needed", GOAL),
                      (r"`the golden mountain does not exist': \ $\lnot \exists x \, (Gx \land Mx \land "
                       r"\forall y \, ((Gy \land My) \to y = x))$", PARTC)], font_size=20, width=11.0).move_to(
            [0.6, -1.9, 0])
        with self.voiceover(
            "Russell's own escape came in 1905, in On Denoting. <bookmark mark='a'/>Take the sentence: the present "
            "King of France is bald. <bookmark mark='b'/>It looks like subject and predicate. Russell analysed it as "
            "three claims: there is a king of France; there is at most one; and he is bald. <bookmark mark='c'/>The "
            "definite description is not a name at all. It vanishes on analysis into quantifiers and predicates. "
            "<bookmark mark='d'/>Since France has no king, the first conjunct fails and the sentence is simply "
            "false. No object is needed for it to be about. <bookmark mark='e'/>And the golden mountain does not "
            "exist says only that nothing is uniquely golden and a mountain, which is true, and commits us to "
            "nothing."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(s))
            vo.wait_until("b")
            self.play(Write(f), FadeIn(notes))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def scope(self):
        d = kings_model()
        head = label(r"Scope: \ `The present King of France is not bald'", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        dom = VGroup(*[label(x, font_size=20, color=NOM if x in d["bald"] else GREY_A) for x in d["domain"]]).arrange(
            RIGHT, buff=0.8).move_to([0, 1.6, 0])
        dl = label(r"a model: \ no one is King of France; \ one person is bald", font_size=18,
                   color=GREY_A).next_to(dom, UP, buff=0.2)
        r1 = MathTex(r"\exists x \, (Kx \land \forall y (Ky \to y = x) \land \lnot Bx)", font_size=32, color=PARTC)
        r2 = MathTex(r"\lnot \exists x \, (Kx \land \forall y (Ky \to y = x) \land Bx)", font_size=32, color=UNIV)
        v1 = label(r"narrow scope: \ " + (r"true" if d["narrow"] else r"false"), font_size=20,
                   color=OK if d["narrow"] else BAD)
        v2 = label(r"wide scope: \ " + (r"true" if d["wide"] else r"false"), font_size=20,
                   color=OK if d["wide"] else BAD)
        g1 = VGroup(r1, v1).arrange(RIGHT, buff=0.5).move_to([0, 0.2, 0])
        g2 = VGroup(r2, v2).arrange(RIGHT, buff=0.5).move_to([0, -0.8, 0])
        rows = stack([(r"one sentence, \ two logical forms, \ two truth values", GOAL),
                      (r"`not' inside the description, \ or outside it: \ Russell's account explains the ambiguity",
                       WHITE),
                      (r"Strawson \ (1950): \ the sentence presupposes a king, \ and lacks a truth value \ (Part 27)",
                       BAD)], font_size=20, width=12.0).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Russell's analysis also explains an ambiguity. <bookmark mark='a'/>Take the negation: the present King "
            "of France is not bald. The Reasoner evaluates it in a model with three people, none of them King of "
            "France. <bookmark mark='b'/>Read with narrow scope, there is a unique king and he is not bald: false, "
            "since there is no king. <bookmark mark='c'/>Read with wide scope, it is not the case that there is a "
            "unique bald king: true. <bookmark mark='d'/>One sentence, two logical forms, two truth values, depending "
            "on whether the not sits inside the description or outside it. <bookmark mark='e'/>Peter Strawson "
            "objected that the sentence presupposes a king rather than asserting one, and so is neither true nor "
            "false. That dispute belongs to the philosophy of language, in Part 27."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dl), FadeIn(dom))
            vo.wait_until("b")
            self.play(Write(r1), FadeIn(v1))
            vo.wait_until("c")
            self.play(Write(r2), FadeIn(v2))
            for mk, r in zip("de", rows[:2]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def neo(self):
        head = label(r"Meinong's return", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Parsons \ (1980)", r"nuclear properties \ (golden, \ mountain) \ define objects; \ `existent' is "
                                  r"extranuclear: \ Russell's objection is blocked", GOAL),
            (r"Zalta \ (1983)", r"two modes of predication: \ abstract objects \textit{encode} properties, \ concrete "
                                r"ones \textit{exemplify} them: \ Sherlock Holmes encodes being a detective", UNIV),
            (r"Priest \ (2005)", r"noneism: \ `there is' does not mean `exists'; \ we can quantify over the "
                                 r"non-existent, \ inside a paraconsistent logic \ (Part 5)", NOM),
            (r"the cost", r"which non-existent objects are there? \ a comprehension principle, \ and its paradoxes",
             BAD),
            (r"the stakes", r"fiction, \ intentionality \ (Part 29), \ and negative existentials", GREY_A),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.8, x_text=-2.6, label_size=21)
        with self.voiceover(
            "Meinong did not stay dead. <bookmark mark='a'/>Terence Parsons divided properties into nuclear ones, "
            "like being golden or a mountain, which define an object, and extranuclear ones, like existing, which do "
            "not. The existent golden mountain then need not exist. <bookmark mark='b'/>Edward Zalta distinguished "
            "two ways of having a property: concrete objects exemplify properties, abstract ones encode them. "
            "Sherlock Holmes encodes being a detective without exemplifying it. <bookmark mark='c'/>Graham Priest's "
            "noneism separates the quantifier from existence: we can say there are things that do not exist, inside a "
            "paraconsistent logic like those of Part 5. <bookmark mark='d'/>The cost is a principle saying which "
            "non-existent objects there are, and the paradoxes that threaten it. <bookmark mark='e'/>The stakes "
            "include fiction, the intentionality of thought, and every true negative existential."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def fiction(self):
        head = label(r"Is there a Sherlock Holmes?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the datum", r"`Holmes is a detective' seems true; \ `Holmes does not exist' seems true too", WHITE),
            (r"pretence", r"Walton \ (1990): \ fiction is a game of make-believe; \ no Holmes, \ only pretending", NOM),
            (r"Meinongian", r"Holmes is a non-existent object who encodes being a detective \ (Zalta)", ABS),
            (r"creationism", r"van Inwagen \ (1977); \ Kripke; \ Thomasson \ (1999): \ Holmes is a real abstract "
                             r"artifact, \ created by Conan Doyle in 1887", UNIV),
            (r"the test", r"`Holmes is more famous than any real detective' is true: \ what is it about?", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Fiction sharpens the question. <bookmark mark='a'/>Holmes is a detective seems true, and so does Holmes "
            "does not exist. <bookmark mark='b'/>Kendall Walton says fiction is a game of make-believe: there is no "
            "Holmes, only our pretending that there is. <bookmark mark='c'/>A Meinongian says Holmes is a non-existent "
            "object, who encodes being a detective. <bookmark mark='d'/>Creationists, including Peter van Inwagen, "
            "Saul Kripke and Amie Thomasson, say Holmes really exists: an abstract artifact, created by Arthur Conan "
            "Doyle in 1887, as real as a law or a symphony. <bookmark mark='e'/>The test case: Holmes is more famous "
            "than any real detective. That seems simply true, and it is hard to read as pretence."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
