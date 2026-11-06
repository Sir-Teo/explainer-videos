from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Illusion(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Illusionism and the meta-problem", r"Why do we think experience is so strange?",
                            lit=(1991, 2018), part=PART)
        with self.voiceover("Chapter six. Illusionism, and the meta-problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.illusionism()
        self.meta()
        self.selfmodel()
        self.schema()

    def illusionism(self):
        head = label(r"Illusionism", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Dennett \ (1988)", r"`Quining Qualia': \ nothing is ineffable, \ intrinsic, \ private and "
                                     r"directly known all at once", FUNC),
                (r"Dennett \ (1991)", r"\textit{Consciousness Explained}: \ multiple drafts; \ "
                                      r"heterophenomenology, \ chapter 15 of Part 29", FUNC),
                (r"Frankish \ (2016)", r"experiences seem to have phenomenal properties; \ they do not: \ the "
                                       r"seeming is a representation", SELF),
                (r"the task", r"explain why it seems so: \ the illusion problem, \ an easy problem", GOAL),
                (r"the cost", r"Strawson: \ `the silliest claim ever made'; \ can the seeming itself be an "
                              r"illusion?", BAD)]
        g = rows_table(rows, top=1.6, gap=0.45)
        with self.voiceover(
            "The type-A answer has a modern name: illusionism. <bookmark mark='a'/>In 1988 Daniel Dennett argued, in "
            "Quining Qualia, that nothing has all the properties philosophers give qualia at once: ineffable, "
            "intrinsic, private, and directly known. <bookmark mark='b'/>His book of 1991 replaced the inner theatre "
            "with multiple drafts of content, studied from the outside, as Part 29 described. "
            "<bookmark mark='c'/>Keith Frankish's illusionism of 2016 says it directly: experiences seem to have "
            "phenomenal properties, but they do not. The seeming is a representation, a model the brain has of its "
            "own states. <bookmark mark='d'/>The hard problem is replaced by the illusion problem: explain why it "
            "seems this way, which is an easy problem. <bookmark mark='e'/>The cost is high. Galen Strawson called "
            "the denial of experience the silliest claim ever made, and many ask how a seeming could itself be an "
            "illusion, since seeming is already experience."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def meta(self):
        hc = history_card(2018, r"David Chalmers", r"`The Meta-Problem of Consciousness'", width=5.8,
                          color=HIST).to_corner(UL, buff=0.3)
        reports = VGroup(*[label(s, font_size=21, color=SELF) for s in (
            r"`I know I am conscious, \ whatever else I doubt'",
            r"`no physical story could explain this redness'",
            r"`my experience is simple, \ intrinsic, \ indescribable'",
            r"`a robot could do all this without feeling anything'")]).arrange(DOWN, buff=0.3, aligned_edge=LEFT
                                                                               ).move_to([0, 0.2, 0])
        foot = stack([(r"problem intuitions: \ reports, \ so behaviour: \ an easy problem", FUNC),
                      (r"any solution constrains every theory: \ whatever explains the reports must relate to "
                       r"experience somehow", GOAL)], font_size=20, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 2018 Chalmers found common ground with the illusionists, and called it the meta-problem. "
            "<bookmark mark='a'/>We say things like: I know I am conscious, whatever else I doubt. No physical story "
            "could explain this redness. My experience is simple and indescribable. A robot could do all this "
            "without feeling anything. <bookmark mark='b'/>These are problem intuitions. They are reports, and "
            "reports are behaviour, so explaining them is an easy problem: find the mechanism that produces them. "
            "<bookmark mark='c'/>Chalmers argued that any solution constrains every theory. If the mechanism that "
            "makes us say these things has nothing to do with experience, our belief in experience would be "
            "unjustified. If it does, the solution tells us something about experience itself."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in reports], lag_ratio=0.5), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def selfmodel(self):
        d = load("introspection")
        head = label(r"A self-model that cannot say what it can tell apart \ (an analogy)", font_size=28,
                     color=CONN).to_edge(UP, buff=0.3)
        assert (d["shades"], d["words"], d["bits_seen"], d["bits_said"]) == (4096, 11, 12.0, 3.46)
        assert d["same_word_pairs"] == 933278 and d["share_unsayable"] == 0.1113
        # a slice of the shade cube, coloured, and the same slice as the self-model sees it
        protos = {k: np.array(v) for k, v in C.FOCAL.items()}
        n = 16
        vals = np.linspace(0, 255, n)
        size = 0.2
        def cell(rgb, at):
            return Square(side_length=size, stroke_width=0, fill_color=rgb_to_color(rgb / 255.0),
                          fill_opacity=1).move_to(at)
        seen, said = VGroup(), VGroup()
        for i, r in enumerate(vals):
            for j, gch in enumerate(vals):
                rgb = np.array([r, gch, 96.0])
                x, y = -6.2 + size * j, 1.9 - size * i
                seen.add(cell(rgb, [x, y, 0]))
                name = min(protos, key=lambda k: ((protos[k] - rgb) ** 2).sum())
                said.add(cell(protos[name].astype(float), [x + 4.0, y, 0]))
        sl = label(r"what it tells apart", font_size=18, color=GREY_A).next_to(seen, DOWN, buff=0.15)
        al = label(r"what its self-model says", font_size=18, color=GREY_A).next_to(said, DOWN, buff=0.15)
        side = stack([(r"$16^3 = 4096$ shades told apart: \ 12 bits", SIG),
                      (r"11 basic colour words \ (Berlin and Kay, \ 1969): \ 3.46 bits", SELF),
                      (r"of 8\,386\,560 pairs it can tell apart, \ 933\,278 get the same word", FEEL),
                      (r"asked how they differ: \ `they just do; \ it's like \textit{this}'", GOAL)], font_size=19,
                     aligned_edge=LEFT, width=4.6, buff=0.3).move_to([4.4, 0.3, 0])
        foot = label(r"it would report its states as simple, \ intrinsic and ineffable; \ whether that explains "
                     r"anything more is the question", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The Reasoner builds a toy version of the meta-problem, labelled as an analogy. "
            "<bookmark mark='a'/>A perceiver tells apart sixteen levels of each of three colour channels: four "
            "thousand and ninety six shades, twelve bits of discrimination. Here is one slice of its colour space. "
            "<bookmark mark='b'/>But its model of its own states keeps only which of eleven basic colour words a "
            "state falls under, the eleven that Brent Berlin and Paul Kay found across languages: three and a half "
            "bits. <bookmark mark='c'/>Of the eight point four million pairs of shades it can tell apart, nine "
            "hundred and thirty three thousand fall under the same word. <bookmark mark='d'/>Ask it how two of those "
            "differ, and its self-model has nothing to offer but: they just do; it is like this. "
            "<bookmark mark='e'/>Such a system would report that its experiences are simple, intrinsic, and "
            "ineffable, which is just what our problem intuitions say. For the illusionist, that is the whole "
            "story. For Chalmers, it explains the reports and leaves the redness."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(seen), FadeIn(sl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(said), FadeIn(al), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def schema(self):
        hc = history_card(2013, r"Michael Graziano", r"\textit{Consciousness and the Social Brain}", width=6.2,
                          color=HIST).to_corner(UL, buff=0.3)
        att = VGroup(RoundedRectangle(width=3.6, height=1.0, corner_radius=0.2, color=FUNC, fill_opacity=0.1),
                     label(r"attention: \ a messy competition", font_size=19, color=FUNC)).move_to([-3.0, -1.4, 0])
        sch = VGroup(RoundedRectangle(width=3.6, height=1.0, corner_radius=0.2, color=SELF, fill_opacity=0.1),
                     label(r"its model: \ `an inner awareness'", font_size=19, color=SELF)).move_to([-3.0, 0.6, 0])
        arr = Arrow(att.get_top(), sch.get_bottom(), buff=0.1, color=SELF)
        rows = stack([(r"the brain controls its attention with a simplified model of it, \ as it controls the arm "
                       r"with a body schema", GREY_A),
                      (r"the model leaves out the mechanism, \ so it depicts something ghostly: \ awareness", SELF),
                      (r"we report what the model says: \ the attention schema theory", GOAL),
                      (r"one of the fourteen indicators of chapter 15: \ \texttt{AST-1}", FUNC)], font_size=19,
                     aligned_edge=LEFT, width=6.4, buff=0.3).move_to([3.2, -0.3, 0])
        with self.voiceover(
            "A scientific version of this idea has a name. <bookmark mark='a'/>In 2013 the neuroscientist Michael "
            "Graziano proposed that the brain controls its own attention, a messy competition between signals, "
            "using a simplified model of it, as it controls an arm with a model of the body. "
            "<bookmark mark='b'/>The model leaves out the mechanism, the neurons and their competition. What it "
            "depicts instead is something simpler and stranger: an inner awareness that takes hold of things. "
            "<bookmark mark='c'/>When we report being aware, on this view, we report what the model says. That is "
            "the attention schema theory, the meta-problem solved by a mechanism. <bookmark mark='d'/>It returns in "
            "chapter fifteen as one of the indicators that a machine might be conscious: a model of its own "
            "attention."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(att), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(sch), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
