from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


def glass(center, color=CPT, scale=1.0) -> VGroup:
    c = np.array(center, float)
    body = Polygon(c + np.array([-0.35, 0.45, 0]), c + np.array([0.35, 0.45, 0]), c + np.array([0.22, -0.45, 0]),
                   c + np.array([-0.22, -0.45, 0]), color=color, stroke_width=3, fill_opacity=0.15)
    return VGroup(body).scale(scale)


class Dispositions(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Dispositions, \ finks and masks", r"What makes a glass fragile?", lit=(1994, 1997),
                            part=PART)
        with self.voiceover("Chapter thirteen. Dispositions, finks and masks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.analysis()
        self.cases()
        self.table()
        self.powers()

    def analysis(self):
        head = label(r"The conditional analysis", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f = MathTex(r"x \text{ is fragile} \;\iff\; (x \text{ is struck} \;\Box\!\!\rightarrow\; x \text{ breaks})",
                    font_size=40, color=ABS).next_to(head, DOWN, buff=0.5)
        g = glass([0, 0.4, 0], scale=1.6)
        rows = stack([(r"Ryle \ (1949); \ Carnap's reduction sentences \ (1936): \ dispositions as conditionals", WHITE),
                      (r"with Lewis's counterfactual: \ true iff the closest struck-worlds are breaking-worlds", CPT),
                      (r"attractive: \ no mysterious powers, \ only what would happen", OK),
                      (r"C. B. Martin \ (1994): \ a fink can make the conditional false while the disposition is "
                       r"there", BAD)], font_size=21, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Possible worlds also promise to explain dispositions: fragility, solubility, the power of a drug to "
            "heal. <bookmark mark='a'/>The simple conditional analysis: x is fragile if and only if, were x "
            "struck, it would break. <bookmark mark='b'/>The idea goes back to Gilbert Ryle, and to Rudolf Carnap's "
            "reduction sentences for words like soluble. <bookmark mark='c'/>With Lewis's semantics for "
            "counterfactuals, the conditional is true when the closest worlds where x is struck are worlds where it "
            "breaks. <bookmark mark='d'/>It is attractive: no mysterious powers, only facts about what would happen. "
            "<bookmark mark='e'/>But in 1994 C. B. Martin described the fink."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(g))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def cases(self):
        head = label(r"Four objects, \ struck", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        xs = [-4.8, -1.6, 1.6, 4.8]
        names = [r"plain glass", r"finked glass", r"reverse-finked steel", r"masked glass"]
        notes = [r"breaks", r"a sorcerer hardens it at the moment of the blow", r"a sorcerer makes it brittle at the "
                 r"moment of the blow", r"packed in foam: \ the blow never reaches it"]
        objs = VGroup()
        for i, (x, n, t) in enumerate(zip(xs, names, notes)):
            col = GREY_A if i == 2 else CPT
            g = glass([x, 0.9, 0], color=col, scale=1.3)
            if i == 2:
                g = VGroup(Rectangle(width=0.6, height=1.2, color=GREY_A, fill_opacity=0.25).move_to([x, 0.9, 0]))
            if i == 3:
                g.add(RoundedRectangle(width=1.4, height=1.7, corner_radius=0.2, color=NAME, stroke_width=2,
                                       fill_opacity=0.08).move_to([x, 0.9, 0]))
            hammer = VGroup(Line([x + 1.0, 2.2, 0], [x + 0.45, 1.5, 0], color=GREY_B, stroke_width=5),
                            Rectangle(width=0.36, height=0.18, color=GREY_B, fill_opacity=0.8).rotate(0.9).move_to(
                                [x + 1.05, 2.25, 0]))
            nl = label(n, font_size=19, color=WHITE).move_to([x, -0.45, 0])
            tl = wrapped_label(t, 2.8, 16, GREY_A).next_to(nl, DOWN, buff=0.15)
            objs.add(VGroup(g, hammer, nl, tl))
        crack = VGroup(*[Line([xs[k] - 0.2, 1.2, 0], [xs[k] + 0.15, 0.6, 0], color=BAD, stroke_width=4)
                         for k in (0, 2)])
        rows = stack([(r"a fink removes the disposition exactly when the stimulus comes \ (Martin, \ 1994)", BAD),
                      (r"a reverse fink supplies it: \ the steel breaks, \ though steel is not fragile", GOAL),
                      (r"a mask stops the manifestation while the disposition stays \ (Johnston, \ 1992; \ Bird, \ "
                       r"1998)", NAME)], font_size=20, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The Reasoner sets up four objects and strikes each one. <bookmark mark='a'/>A plain glass: it breaks. "
            "<bookmark mark='b'/>A finked glass. A sorcerer watches it, and at the very moment it is struck, he "
            "makes it hard, so it does not break. The glass is fragile, yet it is false that it would break if "
            "struck. <bookmark mark='c'/>A reverse fink: a piece of steel, not fragile at all, which the sorcerer "
            "makes brittle at the moment of the blow, so it breaks. <bookmark mark='d'/>And a masked glass, packed "
            "in foam: it keeps its fragile structure, but the blow never reaches it. Mark Johnston and Alexander "
            "Bird called such interferers masks and antidotes."
        ) as vo:
            self.play(FadeIn(head))
            for mk, i in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(objs[i]))
                self.play(objs[i][1].animate.shift(DOWN * 0.35 + LEFT * 0.3), run_time=0.4)
                if i in (0, 2):
                    self.play(Create(crack[0 if i == 0 else 1]), run_time=0.4)
                if i >= 1:
                    self.play(FadeIn(rows[i - 1]))
        self.clear_scene()

    def table(self):
        d = load("disp")
        head = label(r"Two analyses, \ checked", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        hd = [r"\text{case}", r"\text{fragile?}", r"\text{simple analysis}", r"\text{Lewis's reformed analysis}"]
        rows = []
        for r in d["rows"]:
            rows.append([label(r["case"], font_size=20), mark(r["fragile"]),
                         VGroup(mark(r["simple"]), MathTex(r"\text{right}" if r["simple"] == r["fragile"] else
                                                           r"\text{wrong}", font_size=17,
                                                           color=OK if r["simple"] == r["fragile"] else BAD)).arrange(
                             RIGHT, buff=0.15),
                         VGroup(mark(r["reformed"]), MathTex(r"\text{right}" if r["reformed"] == r["fragile"] else
                                                             r"\text{wrong}", font_size=17,
                                                             color=OK if r["reformed"] == r["fragile"] else BAD)
                                ).arrange(RIGHT, buff=0.15)])
        grid = ValueGrid(hd, rows, col_w=[3.6, 1.8, 3.0, 3.8], cell_h=0.6, font_size=19).move_to([0, 0.6, 0])
        rows2 = stack([(r"Lewis \ (1997): \ fragile iff it has an intrinsic property that, \ if it were struck and "
                        r"\textit{kept} that property, \ would make it break", CPT),
                       (r"keeping the property defeats finks and reverse finks; \ masks still defeat it", GOAL)],
                      font_size=20, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now the two analyses, evaluated on all four. <bookmark mark='a'/>The simple analysis gets the plain "
            "glass right, and every other case wrong: it denies that the finked and masked glasses are fragile, and "
            "says the steel is. <bookmark mark='b'/>David Lewis's reformed analysis of 1997: x is fragile if it has "
            "some intrinsic property such that, if x were struck and kept that property, the striking and the "
            "property together would make it break. <bookmark mark='c'/>Holding the intrinsic property fixed "
            "defeats the fink and the reverse fink: the Reasoner's table turns right for both. But the mask is "
            "external; the foam stops the break while the glass keeps its structure, and the reformed analysis "
            "still says, wrongly, that the masked glass is not fragile."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule),
                      *[FadeIn(grid.cell[r][c]) for r in range(4) for c in (0, 1)])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][2]) for r in range(4)], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(rows2[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][3]) for r in range(4)], lag_ratio=0.25), FadeIn(rows2[1]))
        self.clear_scene()

    def powers(self):
        head = label(r"Powers first?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the reversal", r"Martin, \ Mumford, \ Bird \ (2007): \ dispositions are real, \ irreducible powers; "
                              r"\ conditionals are evidence of them", NAME),
            (r"laws", r"dispositional essentialism: \ a property's powers are its essence, \ so the laws of nature "
                      r"are necessary \ (Part 18)", ABS),
            (r"the price", r"powers point to manifestations that may never occur: \ a kind of intentionality in "
                           r"matter", BAD),
            (r"the Humean", r"Lewis: \ everything supervenes on the local arrangement of qualities; \ powers are "
                            r"patterns", WORLD),
        ]
        g = rows_table(rows, top=1.8, gap=0.5, width=8.8, x_text=-2.6, label_size=21)
        with self.voiceover(
            "Some philosophers drew the opposite moral. <bookmark mark='a'/>C. B. Martin, Stephen Mumford and "
            "Alexander Bird: dispositions are real and irreducible powers of things, and the conditionals are only "
            "evidence of them. <bookmark mark='b'/>On dispositional essentialism a property's powers are its essence, "
            "and then the laws of nature, which describe those powers, are necessary: the view from Part 18. "
            "<bookmark mark='c'/>The price is a strange directedness in matter: a power points at a manifestation "
            "that may never happen. <bookmark mark='d'/>On the other side stands Lewis's Humean supervenience: "
            "everything there is supervenes on the local arrangement of qualities, and powers are patterns in it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
