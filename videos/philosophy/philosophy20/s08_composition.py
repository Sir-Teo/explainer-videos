from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Composition(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"The special composition question", r"When do some things make up something?",
                            lit=(1987, 1990), part=PART)
        with self.voiceover("Chapter seven. The special composition question."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.question()
        self.count()
        self.organicism()
        self.boundaries()

    def question(self):
        hc = history_card(1990, r"Peter van Inwagen", r"\textit{Material Beings}", width=5.4, color=HIST).to_corner(
            UL, buff=0.35)
        q = MathTex(r"\text{When is it true that } \exists y \text{ such that the } x\text{s compose } y\,?",
                    font_size=34, color=GOAL).move_to([0.8, 1.4, 0])
        d = MathTex(r"\text{the } x\text{s compose } y \;:=\; \text{each is part of } y, \text{ and every part of } y "
                    r"\text{ overlaps one of them}", font_size=26, color=GREY_A).next_to(q, DOWN, buff=0.4)
        rows = stack([(r"never: \ \textit{nihilism} \ (only simples exist)", NOM),
                      (r"always: \ \textit{universalism} \ (every collection has a sum)", UNIV),
                      (r"sometimes: \ contact, \ fastening, \ cohesion, \ fusion, \ \textit{life}", WHOLE),
                      (r"the general question \ (what composition \textit{is}) \ he left aside", GREY_A)],
                     font_size=21, aligned_edge=LEFT, width=9.0).move_to([0.8, -1.4, 0])
        with self.voiceover(
            "Classical mereology says that any things whatever compose something. Peter van Inwagen asked whether "
            "that is true. <bookmark mark='a'/>His special composition question: when is it true that there is "
            "something the xs compose? <bookmark mark='b'/>Things compose y when each is part of y and every part of y "
            "overlaps one of them. <bookmark mark='c'/>One answer is never: only simples exist, the view called "
            "nihilism. <bookmark mark='d'/>Another is always: universalism, the classical theory. "
            "<bookmark mark='e'/>Between them lie moderate answers: when the things are in contact, or fastened "
            "together, or cohere, or fuse, or when their activity constitutes a life. <bookmark mark='f'/>What "
            "composition is, he left aside; the question is only when it happens."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(q))
            vo.wait_until("b")
            self.play(FadeIn(d))
            for mk, r in zip("cdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def count(self):
        d = load("compose")
        head = label(r"How many objects among six blocks?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        g0 = block_grid(2, 3, chosen=range(6), size=0.9, center=[-4.2, 1.0, 0])
        g1 = block_grid(2, 3, chosen=[0, 1, 4], size=0.9, center=[-4.2, -1.6, 0], on=WHOLE)
        g2 = block_grid(2, 3, chosen=d["scattered_example"], size=0.9, center=[-0.8, -1.6, 0], on=UNIV)
        l1 = label(r"a connected sum", font_size=16, color=WHOLE).next_to(g1, DOWN, buff=0.15)
        l2 = label(r"a scattered sum", font_size=16, color=UNIV).next_to(g2, DOWN, buff=0.15)
        hd = [r"\text{answer}", r"\text{objects}"]
        rows = [[MathTex(r"\text{nihilism}", font_size=24, color=NOM), MathTex(str(d["nihilism"]), font_size=28)],
                [MathTex(r"\text{contact}", font_size=24, color=WHOLE), MathTex(str(d["contact"]), font_size=28)],
                [MathTex(r"\text{universalism}", font_size=24, color=UNIV),
                 MathTex(str(d["universalism"]), font_size=28)]]
        grid = ValueGrid(hd, rows, col_w=[3.0, 1.6], cell_h=0.62, font_size=20).move_to([3.6, 1.0, 0])
        bys = d["contact_by_size"]
        sz = label(r"connected groups by size: \ " + ", \\ ".join(f"{bys[str(k)] if str(k) in bys else bys[k]}"
                                                              for k in sorted(int(x) for x in bys)),
                   font_size=17, color=GREY_A).next_to(grid, DOWN, buff=0.35)
        rows2 = stack([(r"$2^6 - 1 = 63$ \ on universalism: \ every nonempty group", UNIV),
                       (r"the same six simples, \ three different worlds", GOAL)], font_size=19,
                      aligned_edge=LEFT, width=6.0).move_to([3.4, -1.9, 0])
        with self.voiceover(
            "The Reasoner counts. <bookmark mark='a'/>Six blocks in a grid, each a simple. <bookmark mark='b'/>On "
            "nihilism there are six objects: the blocks themselves, and nothing they compose. "
            "<bookmark mark='c'/>On the contact view, a group composes something when its blocks are connected, "
            "edge to edge. The Reasoner checks every group: forty are connected, from single blocks to the whole "
            "array. <bookmark mark='d'/>On universalism every nonempty group composes something, including scattered "
            "ones like these two separated blocks: sixty-three objects. <bookmark mark='e'/>The same six simples, "
            "arranged the same way, and three answers to how many things there are."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g0))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), FadeIn(VGroup(*grid.cell[0])))
            vo.wait_until("c")
            self.play(FadeIn(g1), FadeIn(l1), FadeIn(VGroup(*grid.cell[1])), FadeIn(sz))
            vo.wait_until("d")
            self.play(FadeIn(g2), FadeIn(l2), FadeIn(VGroup(*grid.cell[2])), FadeIn(rows2[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows2[1]))
        self.clear_scene()

    def organicism(self):
        head = label(r"Van Inwagen's answer, \ and an argument for nihilism", font_size=30, color=CONN).to_edge(
            UP, buff=0.35)
        rows = [
            (r"organicism", r"the $x$s compose something iff their activity constitutes a life \ (Part 19): \ so there "
                            r"are organisms and simples, \ nothing else", WHOLE),
            (r"no tables", r"only `simples arranged table-wise': \ ordinary talk is true, \ loosely spoken", NOM),
            (r"why organisms", r"thinking: \ I exist, \ and my thinking is not just the simples' activity", GOAL),
            (r"Merricks \ (2001)", r"a baseball shatters a window; \ so do its atoms; \ the ball's causing it would be "
                                   r"overdetermination \ (Part 17): \ so no baseballs", BAD),
            (r"the reply", r"the ball's causal power just is its atoms' power, \ arranged: \ no double counting", UNIV),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Van Inwagen defended an unusual moderate answer. <bookmark mark='a'/>Things compose something only when "
            "their activity constitutes a life. So there are organisms, as Part 19 described them, and there are "
            "simples, and nothing else. <bookmark mark='b'/>There are no tables, only simples arranged table-wise. "
            "Ordinary talk of tables is true when loosely spoken. <bookmark mark='c'/>Why organisms? Because I exist, "
            "and my thinking is not just the activity of my simples. <bookmark mark='d'/>Trenton Merricks argued for "
            "eliminating even more. A baseball shatters a window. The ball's atoms, acting together, shatter it too. "
            "If the ball also caused it, the effect would be overdetermined, as in Part 17; so there are no "
            "baseballs. <bookmark mark='e'/>The reply is that the ball's power just is its atoms' power, arranged, so "
            "there is no double counting."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def boundaries(self):
        head = label(r"Touching, \ and who owns the boundary", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        a = Square(side_length=2.0, color=PARTC, fill_opacity=0.35).move_to([-4.6, 0.6, 0])
        b = Square(side_length=2.0, color=WHOLE, fill_opacity=0.35).move_to([-2.6, 0.6, 0])
        edge = Line([-3.6, -0.4, 0], [-3.6, 1.6, 0], color=GOAL, stroke_width=6)
        el = label(r"the line where they meet", font_size=16, color=GOAL).next_to(edge, DOWN, buff=0.15)
        rows = stack([(r"the contact answer needs a theory of touching: \ \textit{mereotopology}", WHITE),
                      (r"Whitehead; \ Clarke \ (1981): \ a primitive relation of connection, \ $C(x, y)$", UNIV),
                      (r"if regions are closed, \ touching ones overlap; \ if open, \ they touch at nothing", BAD),
                      (r"Bolzano: \ one is closed, \ the other open; \ \ Brentano: \ two boundaries, \ coinciding", ABS),
                      (r"Casati and Varzi \ (1999): \ \textit{Parts and Places}, \ the formal theory", GOAL)],
                     font_size=19, aligned_edge=LEFT, width=7.2).move_to([3.1, -0.4, 0])
        with self.voiceover(
            "The contact answer raises a question of its own: what is it for two things to touch? "
            "<bookmark mark='a'/>Mereology has no word for it; touching belongs to topology. The combined theory is "
            "called mereotopology. <bookmark mark='b'/>Alfred North Whitehead, and later Bowman Clarke, took a "
            "relation of connection as primitive. <bookmark mark='c'/>Now take two blocks that touch. Who owns the line "
            "where they meet? If both blocks include their boundaries, they overlap there, and do not merely touch. If "
            "neither does, there is a gap of nothing between them. <bookmark mark='d'/>Bernard Bolzano said one is "
            "closed and the other open, though nothing decides which. Franz Brentano said there are two boundaries, "
            "coinciding exactly. <bookmark mark='e'/>Roberto Casati and Achille Varzi built the formal theory in Parts "
            "and Places."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a), FadeIn(b))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(edge), FadeIn(el), FadeIn(rows[2]))
            for mk, r in zip("de", rows[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
