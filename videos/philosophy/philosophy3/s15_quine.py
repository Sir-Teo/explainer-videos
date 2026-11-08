from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403


class Quine(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"To be is to be the value of a variable", r"What does a theory say there is?",
                            lit=(1948,), part=PART)
        with self.voiceover("Chapter fourteen. To be is to be the value of a variable."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.question()
        self.beard()
        self.exits()
        self.criterion()
        self.numbers()
        self.carnap()

    def question(self):
        q = quote_card(r"A curious thing about the ontological problem is its simplicity. It can be put in three "
                       r"Anglo-Saxon monosyllables: `What is there?' It can be answered, moreover, in a word---"
                       r"`Everything'---and everyone will accept this answer as true.",
                       r"Quine, `On What There Is' (1948)", width=11.0, font_size=28).move_to([0, 0.6, 0])
        rest = label(r"the disagreement is over cases: \ numbers? \ properties? \ possible worlds? \ Pegasus?",
                     font_size=26, color=GOAL).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "In 1948 W. V. Quine published a short paper that set the agenda for metaphysics in English for half "
            "a century. <bookmark mark='a'/>A curious thing about the ontological problem, he wrote, is its "
            "simplicity. It can be put in three monosyllables: what is there? And it can be answered in a word: "
            "everything. <bookmark mark='b'/>The disagreement is over cases. Are there numbers? Properties? "
            "Possible worlds? And what about Pegasus?"
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(q[1] if len(q) > 1 else q, color=GOAL, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(rest))
        self.clear_scene()

    def beard(self):
        s = label(r"`Pegasus does not exist.'", font_size=40).move_to([0, 2.2, 0])
        puzzle = VGroup(label(r"if it is true, \ it is true \textit{of} something", font_size=28),
                        label(r"so Pegasus must in some sense \textit{be}", font_size=28),
                        label(r"and then what is it that does not exist?", font_size=28, color=BAD)).arrange(
            DOWN, buff=0.3).move_to([0, 0.2, 0])
        nm = label(r"Quine: \ `Plato's beard', \ tough enough to dull Occam's razor", font_size=26,
                   color=GOAL).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Take a sentence that is plainly true. <bookmark mark='a'/>Pegasus does not exist. "
            "<bookmark mark='b'/>An old argument says: if it is true, it is true of something, namely Pegasus. So "
            "Pegasus must in some sense be. <bookmark mark='c'/>But then what is it that does not exist? "
            "<bookmark mark='d'/>Quine called this riddle Plato's beard: historically, he said, it has proved "
            "tough, frequently dulling the edge of Occam's razor."
        ) as vo:
            self.play(FadeIn(s))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(puzzle[0]), FadeIn(puzzle[1]))
            vo.wait_until("c")
            self.play(FadeIn(puzzle[2]))
            vo.wait_until("d")
            self.play(FadeIn(nm))
        self.clear_scene()

    def exits(self):
        d = load("beard")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.65, width=3.8, font_size=22,
                       center=[0, -0.45, 0], title=r"The Price List: \ Plato's beard")
        positions = [
            (("A",), r"Russell, Quine", r"the sentence is not about Pegasus: \ `nothing pegasizes', \ "
                                        r"$\lnot \exists x\, \mathrm{Pegasizes}(x)$"),
            (("E",), r"Meinong", r"Pegasus has being but lacks existence \ (1904; \ Parsons 1980, Priest 2005)"),
            (("B",), r"Free logic", r"names may be empty, \ and some sentences with empty names are true "
                                    r"\ (Lambert)"),
            (("N",), r"Fictional realism", r"Pegasus exists, \ as an abstract character made by a story \ "
                                           r"(Kripke, van Inwagen 1977)"),
        ]
        assert sorted(tuple(m) for m in d["mcs"]) == sorted(p[0] for p in positions)
        with self.voiceover(
            "Four claims, one conflict. <bookmark mark='a'/>The sentence 'Pegasus does not exist' is true. It is "
            "about Pegasus. A true sentence about something needs that thing to have being, in some sense. And "
            "whatever has being exists. <bookmark mark='b'/>The Reasoner finds one minimal conflict and four "
            "exits, and each exit is a school. <bookmark mark='c'/>Russell and Quine deny that the sentence is about "
            "Pegasus. 'Pegasus' abbreviates a description, 'the thing that pegasizes', and the sentence says that "
            "nothing pegasizes. It is Chapter four's theory of descriptions. <bookmark mark='d'/>Alexius Meinong "
            "denied that whatever has being exists: Pegasus is an object, with being of a kind, but without "
            "existence. <bookmark mark='e'/>Free logic denies the third claim: names may be empty, and some "
            "sentences containing them are true anyway. <bookmark mark='f'/>And fictional realists deny the first. "
            "Pegasus exists, as an abstract object created by a story, like a novel or a law; what does not exist "
            "is a flying horse."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if mk != "c":
                    self.play(*pl.reset(), run_time=0.6)
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def criterion(self):
        q = quote_card(r"To be assumed as an entity is, purely and simply, to be reckoned as the value of a variable.",
                       r"Quine, `On What There Is' (1948)", width=10.0, font_size=30).to_edge(UP, buff=0.4)
        f = MathTex(r"\exists x\, (\mathrm{Dog}(x) \land \mathrm{White}(x))", font_size=44).move_to([-2.6, 0.2, 0])
        fl = label(r"`some dogs are white'", font_size=24, color=GREY_A).next_to(f, DOWN, buff=0.2)
        dom = Ellipse(width=4.2, height=2.6, stroke_color=OBJ, stroke_width=2).move_to([3.6, -0.3, 0])
        dl = label(r"what $x$ must range over", font_size=22, color=OBJ).next_to(dom, UP, buff=0.1)
        dogs = VGroup(*[label(t, font_size=24, color=WHITE) for t in (r"a dog", r"a white dog", r"another dog")])
        dogs.arrange(DOWN, buff=0.2).move_to(dom)
        ar = Arrow(f[0][1].get_bottom(), dom.get_left(), buff=0.2, color=QUANT, path_arc=0.6)
        com = label(r"committed to dogs; \ not to whiteness: \ `White' is a predicate, not a value of $x$",
                    font_size=24, color=GOAL).to_edge(DOWN, buff=0.9)
        sp = label(r"but `some species are cross-fertile' quantifies over species: \ abstract objects",
                   font_size=24, color=BAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Quine's own answer was a test for what a theory says there is. <bookmark mark='a'/>To be assumed as an "
            "entity is, purely and simply, to be reckoned as the value of a variable. <bookmark mark='b'/>Write the "
            "theory in first-order logic. 'Some dogs are white' says there is an x that is a dog and is white. "
            "<bookmark mark='c'/>For it to be true, the variable must range over dogs. So the sentence is committed "
            "to dogs. <bookmark mark='d'/>It is not committed to whiteness: 'white' is a predicate, not something a "
            "variable takes as a value. <bookmark mark='e'/>But 'some zoological species are cross-fertile' "
            "quantifies over species, so whoever asserts it is committed to species, which are abstract objects. "
            "Quine's slogan: to be is to be the value of a variable."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("c")
            self.play(Create(dom), FadeIn(dl), FadeIn(dogs), Create(ar))
            vo.wait_until("d")
            self.play(FadeIn(com))
            vo.wait_until("e")
            self.play(FadeIn(sp))
        self.clear_scene()

    def numbers(self):
        f = MathTex(r"\exists x\, (\mathrm{Prime}(x) \land x > 10^{100})", font_size=44, color=GOAL).move_to(
            [0, 2.0, 0])
        steps = VGroup(
            label(r"our best science is written in mathematics, \ and mathematics quantifies over numbers and sets",
                  font_size=24),
            label(r"we should believe what our best science says there is", font_size=24),
            label(r"so we should believe in numbers and sets", font_size=26, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.2, 0])
        nm = label(r"the Quine--Putnam indispensability argument: \ Part 9", font_size=24, color=GREY_A).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "The test has teeth. <bookmark mark='a'/>'There is a prime number bigger than ten to the hundred' is a "
            "theorem, and its variable ranges over numbers. <bookmark mark='b'/>Physics is written in mathematics, "
            "and mathematics quantifies over numbers, functions and sets. <bookmark mark='c'/>If we believe what our "
            "best science says there is, <bookmark mark='d'/>then we are committed to numbers and sets: abstract "
            "objects, outside space and time. This is the indispensability argument of Quine and Hilary Putnam, and "
            "it is one of the main arguments of Part 9."
        ) as vo:
            self.play(Write(f))
            vo.wait_until("a")
            for mk, st in zip("bcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=RIGHT * 0.2))
            self.play(FadeIn(nm))
        self.clear_scene()

    def carnap(self):
        hc = history_card(1950, r"Rudolf Carnap", r"`Empiricism, Semantics, and Ontology'", width=5.6,
                          color=HIST).to_corner(UL, buff=0.4)
        two = VGroup(
            VGroup(label(r"internal questions", font_size=28, color=P.CLAIM),
                   label(r"`is there a prime above 100?' \ asked inside the language of numbers", font_size=22,
                         color=GREY_A),
                   label(r"answered by proof: \ trivially yes", font_size=22, color=OK)).arrange(DOWN, buff=0.15),
            VGroup(label(r"external questions", font_size=28, color=P.AGENT),
                   label(r"`do numbers really exist?' \ asked about the language itself", font_size=22,
                         color=GREY_A),
                   label(r"a practical choice of framework, \ not a matter of fact", font_size=22,
                         color=BAD)).arrange(DOWN, buff=0.15)).arrange(RIGHT, buff=1.0).move_to([0, -0.3, 0])
        fwd = label(r"Quine rejected the distinction (1951); \ the debate over `metaontology' is Part 20",
                    font_size=24, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Rudolf Carnap thought the whole enterprise was confused. <bookmark mark='a'/>Inside a language with "
            "number words, 'is there a prime above a hundred?' is an internal question, answered by proof: "
            "trivially, yes. <bookmark mark='b'/>But 'do numbers really exist?', asked about the language itself, "
            "is not a question of fact at all. It is a practical choice of which framework to use. "
            "<bookmark mark='c'/>Quine rejected the distinction in 1951, in 'Two Dogmas of Empiricism', and the "
            "dispute between them is still the starting point of metaontology, in Part 20."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(two[0]))
            vo.wait_until("b")
            self.play(FadeIn(two[1]))
            vo.wait_until("c")
            self.play(FadeIn(fwd))
        self.clear_scene()
