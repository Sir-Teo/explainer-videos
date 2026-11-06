from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Function(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Function and teleology", r"What is a heart \textit{for}?", lit=(1973, 1984),
                            part=PART)
        with self.voiceover("Chapter eight. Function and teleology."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ancient()
        self.two()
        self.price()

    def two(self):
        head = label(r"Two theories of function", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        heart = VGroup(Circle(radius=0.55, color=BAD, fill_opacity=0.3).shift(LEFT * 0.35),
                       Circle(radius=0.55, color=BAD, fill_opacity=0.3).shift(RIGHT * 0.35),
                       Triangle(color=BAD, fill_opacity=0.3).scale(0.95).rotate(PI).shift(DOWN * 0.55)).move_to(
            [-5.0, 0.9, 0])
        a1 = Arrow(heart.get_right(), heart.get_right() + RIGHT * 1.4 + UP * 0.4, buff=0.1, color=OK, stroke_width=3)
        a2 = Arrow(heart.get_right(), heart.get_right() + RIGHT * 1.4 + DOWN * 0.4, buff=0.1, color=SELF,
                   stroke_width=3)
        l1 = label(r"pumps blood", font_size=18, color=OK).next_to(a1, RIGHT, buff=0.1)
        l2 = label(r"makes a thumping sound", font_size=18, color=SELF).next_to(a2, RIGHT, buff=0.1)
        rows = [
            (r"etiological \ (Wright, \ 1973)", r"the function of X is Z if X is there \textit{because} it does Z: \ "
                                                r"pumping explains why hearts exist; \ thumping does not", OK),
            (r"proper functions \ (Millikan, \ 1984)", r"what ancestors' hearts did that got them selected: \ so a "
                                                       r"diseased heart still has the function it fails to perform",
             GENE),
            (r"causal roles \ (Cummins, \ 1975)", r"the function is the contribution to a capacity of the containing "
                                                  r"system that we are analysing", ORG),
            (r"teleology tamed", r"`for' without a designer: \ the purpose is in the history, \ or in the analysis",
             GOAL),
        ]
        g = rows_table(rows, top=-0.4, gap=0.4, width=8.4, x_text=-2.0, label_size=20, text_size=19)
        with self.voiceover(
            "Biologists say the heart is for pumping blood. <bookmark mark='a'/>It also makes a thumping sound, "
            "which doctors use, but that is not what it is for. What is the difference? <bookmark mark='b'/>Larry "
            "Wright's etiological answer: the function of a trait is the effect that explains why it is there. "
            "Pumping explains why hearts exist; thumping does not. <bookmark mark='c'/>Ruth Millikan's proper "
            "functions make the history explicit: the effect for which ancestors' hearts were selected. That is why a "
            "diseased heart still has the function it fails to perform. <bookmark mark='d'/>Robert Cummins offered "
            "a different account: a function is a contribution to some capacity of a larger system that we are "
            "trying to explain, with no history required. <bookmark mark='e'/>Either way, teleology is tamed: the "
            "for lies in a selection history, or in an analysis, not in a designer's mind."
        ) as vo:
            self.play(FadeIn(head), FadeIn(heart))
            vo.wait_until("a")
            self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(l1), FadeIn(l2))
            for mk, r in zip("bcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def price(self):
        d = load("function")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mcs"] == [["F1"], ["F2"], ["F3"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.9, width=3.9, font_size=20,
                       center=[0, -0.5, 0], title=r"The Price List: \ Swampman's heart")
        positions = [(("F2",), r"Millikan", r"bite the bullet: \ Swampman's organs have no functions, \ until "
                                            r"selection acts on them"),
                     (("F1",), r"Cummins", r"functions are causal roles: \ Swampman's heart has one, \ history or not"),
                     (("F3",), r"Bigelow and Pargetter \ (1987)", r"forward-looking: \ a function is a disposition "
                                                                  r"that \textit{would} be favoured \ (history is not "
                                                                  r"needed)")]
        with self.voiceover(
            "Donald Davidson's Swampman makes a Price List. <bookmark mark='a'/>Lightning strikes a swamp and, by "
            "a vast coincidence, assembles a molecule-for-molecule duplicate of a man. Its functions, on the "
            "etiological theory, are effects with a selection history. Swampman's heart has no such history. Yet "
            "surely it has the function of pumping blood. <bookmark mark='b'/>The three cannot all stand. "
            "<bookmark mark='c'/>Millikan bites the bullet: Swampman's organs have no functions, strictly speaking, "
            "until selection gets to work on them. <bookmark mark='d'/>Cummins's causal-role account drops the "
            "history: the heart has a role in the system's capacity to circulate blood, however it came to be. "
            "<bookmark mark='e'/>John Bigelow and Robert Pargetter look forward instead: a function is a "
            "disposition that would be favoured by selection, so the heart qualifies with or without a past."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cde", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def ancient(self):
        head = label(r"Purposes in nature, \ before Darwin", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Aristotle", r"four causes: \ the eye's \textit{final} cause is seeing; \ nature does nothing in vain",
             GOAL),
            (r"Descartes; \ Bacon", r"final causes banished from physics: \ `like virgins consecrated to God, \ "
                                    r"barren'", BAD),
            (r"Kant \ (1790)", r"organisms are `natural purposes', \ parts both cause and effect of the whole; \ "
                               r"`no Newton of a blade of grass'", ORG),
            (r"Darwin \ (1859)", r"the Newton of the blade of grass: \ purpose-talk explained by history", GENE),
            (r"Mayr \ (1974)", r"\textit{teleonomy} \ (Pittendrigh's word): \ goal-directedness from a program shaped by "
                               r"selection", ALT),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.4, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Talk of purposes in nature is ancient. <bookmark mark='a'/>Aristotle distinguished four kinds of "
            "cause, and held that the final cause of the eye, what it is for, is seeing: nature, he said, does "
            "nothing in vain. <bookmark mark='b'/>The scientific revolution banished final causes from physics. "
            "Francis Bacon compared them to virgins consecrated to God: they bear nothing. "
            "<bookmark mark='c'/>Kant saw that organisms resist the banishment. In an organism the parts are both "
            "cause and effect of the whole, so we must judge it as a natural purpose. And he predicted that there "
            "would never be a Newton who could explain even a blade of grass by laws of nature alone. "
            "<bookmark mark='d'/>Darwin is often called that Newton: his theory explains purpose-talk by history. "
            "<bookmark mark='e'/>Ernst Mayr, borrowing a word coined by Colin Pittendrigh, called goal-directedness "
            "that comes from a program shaped by selection teleonomy, as opposed to teleology from a conscious aim."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
