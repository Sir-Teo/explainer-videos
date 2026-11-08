from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.table()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"A curious thing about the ontological problem is its simplicity. \ It can be put in three "
                       r"Anglo-Saxon monosyllables: \ `What is there?' \ It can be answered, \ moreover, \ in a word "
                       r"--- \ `Everything'.", r"W. V. O. Quine", r"`On What There Is' \ (1948)", width=10.4,
                       font_size=24).next_to(t, DOWN, buff=0.5)
        with self.voiceover(
            "Act Five of this series turns from how we know to what there is. Part 19 asked what life is; this part "
            "asks what anything is. <bookmark mark='a'/>Willard Van Orman Quine opened his most famous paper with a "
            "joke: the ontological question can be put in three words, what is there, and answered in one: "
            "everything. <bookmark mark='b'/>Everyone accepts that answer. The arguments begin when we ask what "
            "everything includes."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=GOAL, scale_factor=1.03))
        self.clear_scene()

    def table(self):
        head = label(r"How many things are on this table?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        top = Rectangle(width=4.6, height=0.18, color=GREY_B, fill_opacity=0.6).move_to([-3.6, -0.6, 0])
        legs = VGroup(*[Line([x, -0.7, 0], [x, -2.4, 0], color=GREY_B, stroke_width=5) for x in (-5.6, -1.6)])
        cup = VGroup(Polygon([-4.6, -0.5, 0], [-4.4, 0.6, 0], [-3.6, 0.6, 0], [-3.4, -0.5, 0], color=WHOLE,
                             fill_opacity=0.4),
                     Arc(radius=0.3, start_angle=-PI / 2, angle=PI, arc_center=[-3.45, 0.1, 0], color=WHOLE,
                         stroke_width=4))
        saucer = Ellipse(width=1.8, height=0.22, color=PARTC, fill_opacity=0.4).move_to([-4.0, -0.45, 0])
        apple = Circle(radius=0.32, color=BAD, fill_opacity=0.6).move_to([-2.3, -0.15, 0])
        rows = stack([(r"a cup, \ a saucer, \ an apple, \ a table: \ four?", WHITE),
                      (r"the cup's handle, \ the table's legs, \ the apple's core: \ parts are things too", PARTC),
                      (r"the cup-and-saucer; \ the apple-plus-the-Moon: \ sums of things?", WHOLE),
                      (r"the apple's redness; \ the cup's shape: \ properties?", UNIV),
                      (r"the number of cups: \ one; \ is the number one a thing?", ABS),
                      (r"or only $10^{27}$ particles, \ arranged table-wise and cup-wise?", BAD)],
                     font_size=21, aligned_edge=LEFT, width=6.8).move_to([3.2, -0.3, 0])
        with self.voiceover(
            "Here is a table. How many things are on it? <bookmark mark='a'/>A cup, a saucer and an apple; with the "
            "table, four. <bookmark mark='b'/>But the cup has a handle, the table has legs, the apple has a core. "
            "Parts are things too. <bookmark mark='c'/>Is the cup-and-saucer one more thing? What about the apple "
            "plus the Moon? <bookmark mark='d'/>The apple is red. Is its redness something it has, an entity of "
            "its own? <bookmark mark='e'/>There is one cup. Is the number one a thing? <bookmark mark='f'/>Or are "
            "there really only particles, some ten to the twenty-seven of them, arranged table-wise and cup-wise? "
            "Each answer is a serious position, and this part builds the tools to compare them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), Create(legs), FadeIn(saucer), FadeIn(cup), FadeIn(apple))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Quine's criterion of ontological commitment; \ plural quantification",
            r"Meinong's jungle and Russell's descriptions",
            r"universals, \ tropes and resemblance \ (Goodman's two troubles, \ computed)",
            r"abstract objects and the way of abstraction",
            r"mereology axiom by axiom: \ every poset on six elements, \ tested",
            r"when do parts make a whole? \ \ vagueness, \ the Wall, \ and the problem of the many",
            r"metaontology; \ grounding; \ is there a bottom level?",
            r"description logic, \ ontologies in industry, \ and what an embedding commits to",
        ], font_size=23)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Quine's criterion for what a theory says there is, and quantifiers that "
            "range over many things at once. <bookmark mark='b'/>Meinong's objects that do not exist, and Russell's "
            "escape. <bookmark mark='c'/>The ancient problem of universals, with resemblance nominalism tested on "
            "property tables. <bookmark mark='d'/>Abstract objects. <bookmark mark='e'/>The formal theory of parts "
            "and wholes, checked on every small model. <bookmark mark='f'/>When parts compose a whole: this part's "
            "brick in the Wall, and the problem of the many. <bookmark mark='g'/>Whether ontological disputes are "
            "substantive at all; grounding; and whether there is a bottom level. <bookmark mark='h'/>And ontology as "
            "engineering: description logic with a working reasoner, the ontologies of medicine and biology, and "
            "knowledge graphs."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
