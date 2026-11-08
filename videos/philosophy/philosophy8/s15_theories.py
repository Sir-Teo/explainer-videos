from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Theories(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"What is truth?", r"What, if anything, do all truths have in common?", lit=(2020,),
                            part=PART)
        with self.voiceover("Chapter fourteen. What is truth?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.aristotle()
        self.views()
        self.davidson()
        self.slingshot()
        self.minimal()

    def aristotle(self):
        q = quote_card(r"To say of what is that it is not, or of what is not that it is, is false; while to say of "
                       r"what is that it is, and of what is not that it is not, is true.", r"Aristotle",
                       r"\textit{Metaphysics} $\Gamma$ 7", width=10.4, font_size=28).move_to([0, 1.0, 0])
        mo = label(r"the Later Mohists: \ a saying fits when name and actuality are paired", font_size=24,
                   color=GREY_A).next_to(q, DOWN, buff=0.5)
        t = label(r"Tarski called his T-schema an attempt to make this precise", font_size=24, color=GOAL).next_to(
            mo, DOWN, buff=0.3)
        with self.voiceover(
            "So far the question has been how truth behaves. Philosophers have also asked what it is. "
            "<bookmark mark='a'/>Aristotle's answer: to say of what is that it is, and of what is not that it is "
            "not, is true. <bookmark mark='b'/>The Later Mohists spoke of a saying fitting when its names are paired "
            "with actualities. <bookmark mark='c'/>And Tarski described his T-schema as an attempt to make "
            "Aristotle's idea precise."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(mo))
            vo.wait_until("c")
            self.play(FadeIn(t))
        self.clear_scene()

    def views(self):
        head = label(r"Five answers", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rows = [(r"correspondence", r"a truth fits a fact in the world", r"Russell 1912; \ Austin 1950; \ truthmakers"),
                (r"coherence", r"a truth fits a whole system of beliefs", r"Bradley; \ Blanshard 1939; \ Neurath"),
                (r"pragmatism", r"a truth is what inquiry would settle on, \ or what works", r"Peirce 1878; \ James "
                 r"1907; \ Dewey"),
                (r"identity", r"a true thought simply \textit{is} a fact", r"McDowell; \ Hornsby"),
                (r"deflationism", r"`true' adds nothing: \ `$p$' is true iff $p$, \ and that is all", r"Ramsey 1927; "
                 r"\ Quine; \ Horwich 1990")]
        tab = VGroup()
        for i, (a, b, c) in enumerate(rows):
            y = 1.9 - 0.95 * i
            tab.add(VGroup(label(a, font_size=26, color=GOAL).move_to([-6.3, y, 0], aligned_edge=LEFT),
                           label(b, font_size=22).move_to([-3.4, y + 0.15, 0], aligned_edge=LEFT),
                           label(c, font_size=19, color=GREY_B).move_to([-3.4, y - 0.25, 0], aligned_edge=LEFT)))
        survey = label(r"PhilPapers survey (2020): \ about half of philosophers favour correspondence, \ about a quarter "
                       r"deflationism", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "There are five main answers. <bookmark mark='a'/>Correspondence: a truth fits a fact. Bertrand Russell "
            "and J. L. Austin gave versions; today's truthmaker theories are its heirs. <bookmark mark='b'/>"
            "Coherence: a truth fits a whole system of beliefs, a view of F. H. Bradley, Brand Blanshard and Otto "
            "Neurath. <bookmark mark='c'/>Pragmatism: a truth is what inquiry would settle on in the long run, for "
            "Charles Sanders Peirce, or what works, in William James's more notorious version. "
            "<bookmark mark='d'/>The identity theory: a true thought does not match a fact; it is one. "
            "<bookmark mark='e'/>And deflationism, from Frank Ramsey to Paul Horwich: there is nothing for truth to "
            "be. 'Snow is white' is true if and only if snow is white, and that is all there is to say. In the "
            "survey of 2020, about half of philosophers favoured correspondence, and about a quarter deflationism."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            self.play(FadeIn(survey))
        self.clear_scene()


    def davidson(self):
        hc = history_card(1967, r"Donald Davidson", r"`Truth and meaning'", width=5.4, color=HIST).to_corner(UL,
                                                                                                         buff=0.35)
        t = MathTex(r"\text{`Schnee ist wei\ss' is true} \iff \text{snow is white}", font_size=40,
                    color=GOAL).move_to([0, 1.2, 0])
        rows = VGroup(
            label(r"read the T-sentences the other way: \ they state what the German sentence \textit{means}",
                  font_size=24),
            label(r"a Tarski-style truth theory for a language, \ with finitely many clauses, \ yields one for "
                  r"every sentence", font_size=24),
            label(r"so a finite mind can understand infinitely many sentences", font_size=24, color=OK),
            label(r"radical interpretation, \ and the principle of charity: \ Parts 27 and 28", font_size=22,
                  color=GREY_B)).arrange(DOWN, buff=0.3).next_to(t, DOWN, buff=0.55)
        with self.voiceover(
            "Tarski's work had a second life in the philosophy of language. <bookmark mark='a'/>Donald Davidson "
            "proposed in 1967 that T-sentences say what sentences mean. 'Schnee ist weiss' is true if and only if "
            "snow is white: that tells you what the German sentence means. <bookmark mark='b'/>A truth theory of "
            "Tarski's kind has finitely many clauses, one for each word and each way of combining them, and yet "
            "delivers a T-sentence for every one of infinitely many sentences. <bookmark mark='c'/>That, Davidson "
            "argued, is how a finite mind can understand an unbounded language. <bookmark mark='d'/>The program, "
            "and its principle of charity, return in Parts 27 and 28."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(t), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()


    def slingshot(self):
        hcs = VGroup(history_card(1943, r"Alonzo Church; \ Kurt Gödel (1944)", r"the slingshot", width=5.4,
                                  color=HIST),
                     history_card(1969, r"Donald Davidson", r"`True to the facts'", width=5.0, color=HIST)).arrange(
            RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        rows = [(r"p", r"a true sentence"),
                (r"\iota x\,(x = x \wedge p) = \iota x\,(x = x)", r"logically equivalent to $p$"),
                (r"\iota x\,(x = x \wedge q) = \iota x\,(x = x)", r"swap co-referring descriptions: \ same object"),
                (r"q", r"logically equivalent: \ any other truth")]
        tab = VGroup()
        for i, (f, why) in enumerate(rows):
            y = 1.1 - 0.75 * i
            tab.add(VGroup(MathTex(f, font_size=34).move_to([-5.6, y, 0], aligned_edge=LEFT),
                           label(why, font_size=21, color=GREY_A).move_to([-0.4, y, 0], aligned_edge=LEFT)))
        moral = VGroup(label(r"if sentences stand for facts, \ and these two moves keep the fact the same,",
                             font_size=24),
                       label(r"then every true sentence stands for one and the same Great Fact", font_size=26,
                             color=BAD),
                       label(r"replies: \ deny that descriptions are referring terms \ (Russell, Part 27); \ "
                             r"or that logical equivalents share facts", font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Correspondence theorists face a famous technical objection, called the slingshot, from Alonzo Church "
            "and Kurt Gödel in the 1940s, pressed by Donald Davidson in 1969. <bookmark mark='a'/>Start with any "
            "true sentence p. <bookmark mark='b'/>It is logically equivalent to: the object that is self-identical "
            "and such that p is the same as the object that is self-identical. <bookmark mark='c'/>If q is also "
            "true, both descriptions pick out the same object, so swap one for the other. <bookmark mark='d'/>And "
            "that is logically equivalent to q. <bookmark mark='e'/>If the fact a sentence stands for survives "
            "logical equivalence and swapping co-referring terms, then every true sentence stands for the same "
            "single fact, the Great Fact, and correspondence says nothing. The replies deny one of the moves: "
            "Russell's theory of descriptions, in Part 27, says the descriptions are not names at all."
        ) as vo:
            self.play(FadeIn(hcs))
            for mk, r in zip("abcd", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(m) for m in moral], lag_ratio=0.4), run_time=3)
        self.clear_scene()

    def minimal(self):
        head = label(r"Where the paradoxes bite", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"the deflationist's whole theory is the T-schema", font_size=26),
            label(r"but the liar shows the T-schema cannot hold for every sentence", font_size=26, color=BAD),
            label(r"so deflationists must say which instances to keep, \ and why that is not a substantive theory",
                  font_size=26, color=GOAL),
            label(r"Horwich: \ keep the instances that are not paradoxical; \ critics: \ that needs a theory of "
                  r"paradox", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.35).move_to([0, -0.1, 0])
        with self.voiceover(
            "This is where the two halves of the part meet. <bookmark mark='a'/>For the deflationist, the "
            "T-schema is the whole theory of truth. <bookmark mark='b'/>But the liar shows that the schema cannot "
            "hold for every sentence, on pain of contradiction. <bookmark mark='c'/>So the deflationist must say "
            "which instances to keep, and explain why that choice is not itself a substantial theory of truth. "
            "<bookmark mark='d'/>Horwich proposed keeping just the instances that do not generate paradox. Critics "
            "reply that saying which ones those are requires exactly the kind of theory deflationism hoped to do "
            "without."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=DOWN * 0.1))
        self.clear_scene()
