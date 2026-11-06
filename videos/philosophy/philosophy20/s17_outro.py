from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Quine's criterion; \ Plato's beard; \ the Geach--Kaplan sentence, \ checked; \ gavagai",
            r"Meinong's objects; \ Russell's descriptions and their scope; \ Sherlock Holmes",
            r"universals, \ tropes, \ Bradley's regress; \ resemblance and Goodman's two troubles, \ computed",
            r"abstract objects; \ directions and Hume's principle; \ classes as sums of singletons",
            r"mereology: \ every poset on six elements tested; \ CEM models are Boolean algebras minus zero",
            r"composition counted; \ boundaries; \ vagueness \ (the Wall); \ the problem of the many",
            r"Carnap, \ Putnam's 3 or 7; \ grounding as a strict order, \ and Fine's logic; \ gunk and monism",
            r"an ALC tableau reasoner and an open-world ABox; \ OntoClean; \ what an embedding commits to",
        ]
        card = objectives_card(items, title=r"What we built", font_size=23)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Quine's criterion of ontological commitment, and a "
            "sentence that quantifies over pluralities, checked by brute force. <bookmark mark='b'/>Meinong's "
            "non-existent objects and Russell's theory of descriptions. <bookmark mark='c'/>Universals, tropes and "
            "resemblance, with Goodman's two troubles computed on property tables. <bookmark mark='d'/>Abstract objects "
            "and the way of abstraction. <bookmark mark='e'/>Mereology, with every small model tested and the theorem "
            "that its models are Boolean algebras without a bottom. <bookmark mark='f'/>The special composition "
            "question, counted on six blocks; the argument from vagueness, this part's brick in the Wall; and the "
            "problem of the many. <bookmark mark='g'/>Metaontology, grounding as a strict order, and the question of a "
            "bottom level. <bookmark mark='h'/>And ontology as engineering: a working description-logic reasoner, "
            "OntoClean, and an embedding that answers everything."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{mereo.geach\_kaplan, resemblance\_classes}", r"commitment; \ resemblance"),
                (r"\texttt{mereo.ground\_tree, immediate\_grounds}", r"the logic of ground"),
                (r"\texttt{mereo.Poset: wsp, ssp, uf, fusion}", r"the axioms"),
                (r"\texttt{mereo.posets\_up\_to\_iso, mereology\_census}", r"every small model"),
                (r"\texttt{mereo.composition\_counts, putnam\_world, gunk}", r"composition"),
                (r"\texttt{mereo.grounding\_check}", r"grounding"),
                (r"\texttt{dl.satisfiable, subsumes, msc, instance}", r"description logic"),
                (r"\texttt{dl.ontoclean, transe}", r"engineering"),
                (r"\texttt{evo.*}, \ \texttt{science.*}, \ \dots", r"Parts 1--19")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.55
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.49
            if a.width > 7.6:
                a.width = 7.6
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.2:
                b.width = 4.2
            b.move_to([1.9 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_mereo.py}, \ \texttt{test\_dl.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=20, current=20).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has two new modules. <bookmark mark='a'/>Mereo checks plural sentences and resemblance "
            "classes, tests the axioms of parthood on every small partial order, counts objects on rival answers to "
            "the composition question, checks that grounding is an order and unfolds Fine's logic of ground. Dl is a "
            "description-logic reasoner, with a tableau that returns proofs or counter-models and open-world answers "
            "about individuals, an OntoClean checker, and a small embedding. "
            "<bookmark mark='b'/>And the Wall has its twentieth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[20], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Regiment `every critic admires some novelist' and `there is a novelist every critic admires'. \ What does "
            r"each commit to?",
            r"Evaluate `the present King of France is not bald' in a model with one bald King, \ on both scopes.",
            r"Show that in the imperfect community, \ no property is shared by all three objects.",
            r"Show that a poset with exactly two elements cannot satisfy both supplementation and unrestricted fusion.",
            r"Count the connected groups among four blocks in a row. \ How many objects exist on each answer?",
            r"Run the tableau by hand: \ is every \textit{Grandmother} a \textit{Parent}?",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Regiment two sentences and "
            "read off their commitments; evaluate a description on both scopes; verify the imperfect community; show "
            "that no two-element model satisfies classical mereology; count objects among four blocks; and run a "
            "tableau by hand. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"persistence: \ endurance, \ perdurance, \ the statue and the clay", [21]),
            (r"possible worlds and what possibilia are", [22]),
            (r"substantivalism: \ is spacetime a thing?", [25]),
            (r"entanglement and priority monism", [26]),
            (r"descriptions, \ names and reference", [27]),
            (r"grounding the mental: \ physicalism", [30, 31]),
            (r"what a model represents", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 21, \textit{Identity and Persistence}", font_size=26, color=P.CONCL).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Persistence, and the statue and its clay, in Part 21. Possible "
            "worlds, in Part 22. Whether spacetime is a thing, in Part 25. Entanglement and monism, in Part 26. "
            "Descriptions and reference, in Part 27. Grounding the mental, in Parts 30 and 31. And what a model "
            "represents, in the finale. <bookmark mark='b'/>Next, Part 21: identity and persistence."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Loux and Crisp, \textit{Metaphysics: A Contemporary Introduction} (4th ed. 2017); \ van Inwagen, "
             r"\textit{Material Beings} (1990)",
             r"Simons, \textit{Parts} (1987); \ Armstrong, \textit{Universals: An Opinionated Introduction} (1989); "
             r"\ Lewis, \textit{Parts of Classes} (1991)",
             r"Chalmers, Manley and Wasserman (eds.), \textit{Metametaphysics} (2009); \ Sider, \textit{Writing the "
             r"Book of the World} (2011)",
             r"Baader et al., \textit{The Description Logic Handbook} (2003); \ Rodriguez-Pereyra, "
             r"\textit{Resemblance Nominalism} (2002)"],
            [r"Meinong 1904; Russell 1905; Leśniewski 1916; Quine 1948; Carnap 1950; Goodman 1951; Williams 1953",
             r"Boolos 1984; Putnam 1987; Baxter 1988; Unger 1980; Geach 1980; Lewis 1986, 1993; Sider 2001, 2007",
             r"Fine 2001, 2012; Schaffer 2003, 2009, 2010; Rosen 2010; Wilson 2014; Hirsch 2011; Thomasson 2015",
             r"Schmidt-Schauß and Smolka 1991; Guarino and Welty 2002; Bordes et al. 2013; Li et al. 2023"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
