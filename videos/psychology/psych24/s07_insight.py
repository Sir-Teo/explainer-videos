from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403


def dots_grid(center=(0, 0, 0), step: float = 0.9) -> VGroup:
    c = np.array(center, float)
    return VGroup(*[Dot(c + np.array([(i - 1) * step, (j - 1) * step, 0]), radius=0.11, color=WHITE)
                    for j in range(3) for i in range(3)])


def to_scene(pt, center, step: float = 0.9):
    return np.array(center, float) + np.array([(pt[0] - 1) * step, (pt[1] - 1) * step, 0])


class Insight(VoiceoverScene):
    def construct(self):
        self.card()
        self.apes()
        self.candle()
        self.jars()
        self.ninedots()
        self.warmth()

    def card(self):
        card = chapter_card(6, r"Insight", r"Why is the answer obvious only afterwards?",
                            lit={1945: r"Duncker", 1987: r"Metcalfe \& Wiebe", 2001: r"MacGregor et al."},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter six. Insight."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def apes(self):
        head = heading(r"K\"ohler's apes")
        # the stick problem, seen from the side: Sultan behind the bars, the fruit on the ground outside
        pa = panel(6.0, 2.55, center=[-3.65, 1.45, 0])
        floor_a = Line([-6.45, 0.45, 0], [-0.85, 0.45, 0], color=GREY_C, stroke_width=2)
        bars = VGroup(*[Line([x, 0.45, 0], [x, 2.45, 0], color=GREY_B, stroke_width=4) for x in (-4.55, -4.35)])
        sultan = little_person(0.95, color=CONTENT).move_to([-5.7, 0.95, 0])
        name = label(r"Sultan", font_size=19, color=CONTENT).next_to(sultan, UP, buff=0.1)

        def banana(at):
            return ArcBetweenPoints(np.array(at) + LEFT * 0.28, np.array(at) + RIGHT * 0.28, angle=PI / 2.4,
                                    color="#F2C14E", stroke_width=9)
        fruit = banana([-1.35, 0.62, 0])
        s1 = Line([-5.25, 0.62, 0], [-3.65, 0.62, 0], color=CONTENT, stroke_width=6)
        s2 = Line([-5.25, 0.8, 0], [-3.75, 0.8, 0], color="#C9A227", stroke_width=8)
        joined = VGroup(Line([-5.2, 0.62, 0], [-3.3, 0.62, 0], color="#C9A227", stroke_width=8),
                        Line([-3.3, 0.62, 0], [-1.6, 0.62, 0], color=CONTENT, stroke_width=6))
        cap_a = label(r"two short sticks; \ one fits inside the other", font_size=19, color=GREY_A)
        cap_a.move_to([-3.65, 0.05, 0])
        # the box problem: fruit hung from the roof, boxes on the floor
        pb = panel(6.0, 2.55, center=[-3.65, -1.55, 0])
        floor_b = Line([-6.45, -2.55, 0], [-0.85, -2.55, 0], color=GREY_C, stroke_width=2)
        roof = Line([-6.45, -0.45, 0], [-0.85, -0.45, 0], color=GREY_C, stroke_width=2)
        string = Line([-2.6, -0.45, 0], [-2.6, -0.85, 0], color=GREY_B, stroke_width=2)
        hung = banana([-2.6, -0.95, 0])
        ape_b = little_person(0.8, color=CONTENT).move_to([-5.8, -2.15, 0])
        box1 = Square(0.62, stroke_color=SEARCH, fill_color=SEARCH, fill_opacity=0.35).move_to([-4.4, -2.24, 0])
        box2 = Square(0.62, stroke_color=SEARCH, fill_color=SEARCH, fill_opacity=0.35).move_to([-1.5, -2.24, 0])
        cap_b = label(r"boxes dragged under the fruit, \ then stacked", font_size=19, color=GREY_A)
        cap_b.move_to([-3.65, -2.95, 0])
        card_ = theory_card(r"Insight as restructuring", r"Wolfgang K\"ohler, \ 1917; \ the Gestalt school",
                            r"a problem is solved when the situation is suddenly seen anew, \ not by the slow "
                            r"trial and error of Thorndike's cats", r"the jump is real; \ what it joins was learned "
                            r"before", "contested", width=6.2, font_size=20, color=INSIGHT)
        card_.move_to([3.45, 1.35, 0])
        checks = verdict_row([
            (r"solutions can come all at once, \ and feel that way \ (Metcalfe and Wiebe, \ 1987: \ this "
             r"chapter's last screen)", "replicated"),
            (r"insight owes little to past learning: \ Birch, \ 1945, \ chimpanzees new to sticks; \ Epstein "
             r"et al., \ 1984, \ pigeons", "failed"),
        ], width=6.2, font_size=19)
        checks.next_to(card_, DOWN, buff=0.3)
        tag = historical_tag(r"Thorndike (1898); \ K\"ohler (1917/1925); \ Birch (1945); \ Epstein et al.\ (1984)")
        with self.voiceover(
            "The idea that some thinking isn't step-by-step search is older than the computer. "
            "<bookmark mark='a'/> From 1913 Wolfgang Köhler, one of the Gestalt psychologists of Part 14, ran a "
            "research station for chimpanzees on Tenerife, and set them problems with fruit out of reach. "
            "<bookmark mark='b'/> Sultan, his ablest chimpanzee, had two hollow sticks, each too short to reach a "
            "banana outside the bars. After about an hour of failing, playing with them, he found he had pushed one "
            "into the other, and at once went to the bars and pulled the fruit in. <bookmark mark='c'/> Others "
            "dragged a box under fruit hung from the roof, and later stacked two or more. <bookmark mark='d'/> "
            "Köhler's book appeared in 1917, and in English as The Mentality of Apes. Against Edward Thorndike's "
            "cats, which escaped from puzzle boxes by slow trial and error, he argued for insight: a sudden change "
            "in how the situation is seen, so that a stick becomes part of a longer arm. The Gestalt word was "
            "restructuring. <bookmark mark='e'/> The record keeps the suddenness and adds a history. In 1945 "
            "Herbert Birch found that young chimpanzees with no experience of sticks mostly failed such problems, "
            "and solved them readily after a few days of playing with sticks. In 1984 Robert Epstein and "
            "colleagues trained pigeons, separately, to push a box and to climb onto one; given a toy banana out of "
            "reach, they put the two together. <bookmark mark='f'/> Insight is real as an experience, but it's "
            "built from what was learned before. Karl Duncker, who trained in Köhler's Berlin institute, took the "
            "question to people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(pa), FadeIn(pb), FadeIn(floor_a), FadeIn(bars), FadeIn(sultan), FadeIn(name),
                      FadeIn(fruit))
            vo.wait_until("b")
            self.play(FadeIn(s1), FadeIn(s2), FadeIn(cap_a))
            self.play(ReplacementTransform(VGroup(s2, s1), joined), run_time=1.2)
            self.play(fruit.animate.move_to([-1.85, 0.75, 0]), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(floor_b), FadeIn(roof), FadeIn(string), FadeIn(hung), FadeIn(ape_b), FadeIn(box1),
                      FadeIn(box2), FadeIn(cap_b))
            self.play(box1.animate.move_to([-2.6, -2.24, 0]), box2.animate.move_to([-2.6, -1.62, 0]), run_time=1.4)
            self.play(ape_b.animate.scale(0.8).next_to(box2, UP, buff=0.0).shift(LEFT * 0.05), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(card_.box), FadeIn(card_.name), FadeIn(card_.claim))
            vo.wait_until("e")
            self.play(FadeIn(checks.rows[0], shift=RIGHT * 0.15))
            self.play(FadeIn(checks.rows[1], shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(card_.verdict), FadeIn(card_.status))
        self.clear_scene()

    def candle(self):
        head = heading(r"Duncker's candle")
        wall = Rectangle(width=4.6, height=3.4, stroke_color=GREY_B, fill_color="#20262F", fill_opacity=1)
        wall.move_to([-3.6, 0.6, 0])
        candle = VGroup(Rectangle(width=0.22, height=1.0, fill_color=CONTENT, fill_opacity=1, stroke_width=0),
                        Ellipse(width=0.16, height=0.3, fill_color="#FF9F43", fill_opacity=1, stroke_width=0)
                        .shift(UP * 0.66)).move_to([-4.8, -0.6, 0])
        box = VGroup(Rectangle(width=1.2, height=0.55, stroke_color=SEARCH, fill_color=SEARCH, fill_opacity=0.3),
                     *[Dot([-0.35 + 0.18 * k, 0.05 * (k % 2), 0], radius=0.05, color=GREY_A) for k in range(5)]
                     ).move_to([-3.4, -0.75, 0])
        matches = VGroup(*[Line([0, 0, 0], [0.55, 0.12, 0], color=GREY_A, stroke_width=3).shift(DOWN * 0.08 * k)
                           for k in range(3)]).move_to([-2.2, -0.8, 0])
        ll = wrapped_label(r"a candle, \ a box of tacks, \ matches: \ fix the candle to the wall so it can burn "
                           r"without dripping on the table", 4.8, 22, GREY_A).next_to(wall, DOWN, buff=0.2)
        shelf = box[0].copy().set_fill(SEARCH, 0.6).move_to([-3.6, 0.9, 0])
        candle2 = candle.copy().next_to(shelf, UP, buff=0.0)
        tacks = VGroup(*[Dot(shelf.get_corner(UL) + RIGHT * (0.2 + 0.4 * k) + DOWN * 0.1, radius=0.05,
                             color=WHITE) for k in range(3)])
        rows = rows_of([
            (r"Duncker, \ 1945: \ the answer is to empty the box, \ tack it to the wall, \ and stand the candle in "
             r"it", WHITE),
            (r"\emph{functional fixedness}: \ the box is seen as a container, \ not as a shelf", INSIGHT),
            (r"Adamson, \ 1952: \ the problem is easier when the box is given empty, \ beside the tacks", GREY_A),
        ], 5.6, 24, 0.36).move_to([3.5, 0.3, 0])
        tag = historical_tag(r"Duncker (1945); \ Adamson (1952)")
        with self.voiceover(
            "Some problems aren't solved by search at all, or not by any search you can report. "
            "<bookmark mark='a'/> Karl Duncker gave people a candle, a box of tacks and some matches, and asked them "
            "to fix the candle to the wall so it could burn without dripping on the table. People try to tack the "
            "candle to the wall, or glue it with melted wax. <bookmark mark='b'/> The answer is to empty the box, "
            "tack it to the wall, and stand the candle in it. <bookmark mark='c'/> Duncker called the obstacle "
            "functional fixedness: the box is seen as a container for tacks, not as a shelf. "
            "<bookmark mark='d'/> Robert Adamson found in 1952 that the problem is easier when the box is given "
            "empty, beside the tacks, not filled with them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(wall), FadeIn(candle), FadeIn(box), FadeIn(matches), FadeIn(ll))
            vo.wait_until("b")
            self.play(TransformFromCopy(box[0], shelf), FadeIn(tacks), Transform(candle, candle2), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def jars(self):
        d = load("jars")
        J = d["jars"]
        head = heading(r"Luchins's water jars")
        A, B, C, goal = (int(v) for v in J[1])
        scale_ = 2.2 / B

        def jar(cap, name, col, x):
            h = max(cap * scale_, 0.3)
            body = Rectangle(width=0.62 if cap > 10 else 0.42, height=h, stroke_color=col, stroke_width=2.5)
            body.move_to([x, 0.35 + h / 2, 0])
            water = Rectangle(width=body.width - 0.06, height=0.001, stroke_width=0, fill_color=SEARCH,
                              fill_opacity=0.75).move_to(body.get_bottom() + UP * 0.003)
            t = label(rf"{name}: \ {cap}", font_size=21, color=col).next_to(body, DOWN, buff=0.15)
            g = VGroup(body, water, t)
            g.body, g.water = body, water
            return g
        jA, jB, jC = jar(A, "A", CONTENT, -5.9), jar(B, "B", SEARCH, -4.75), jar(C, "C", LOGIC, -3.75)
        want = label(rf"measure out exactly {goal}", font_size=23, color=WHITE).move_to([-1.15, 2.1, 0])

        def fill_to(j, amount):
            h = amount * scale_
            return j.water.animate.stretch_to_fit_height(max(h, 0.001)).move_to(
                j.body.get_bottom() + UP * max(h, 0.001) / 2)
        formula = MathTex(r"B - A - 2C = " + str(goal), font_size=40, color=SEARCH).move_to([-1.15, 1.2, 0])

        def row(k, y):
            a, b, c, g = (int(v) for v in J[k])
            ok = bool(d["practised_works"][k])
            mark = r"\checkmark" if ok else r"\times"
            short = (MathTex(str(d["shortest"][k]), font_size=28, color=MODEL) if d["shortest_steps"][k] < 4
                     else VectorizedPoint())
            r_ = VGroup(label(rf"{k + 1}.", font_size=21, color=GREY_B),
                        label(rf"{a}, \ {b}, \ {c} \ $\to$ \ {g}", font_size=22, color=WHITE),
                        MathTex(rf"B - A - 2C \ {mark}", font_size=28, color=SEARCH if ok else LOST), short)
            for m, x in zip(r_, (-6.35, -4.9, -2.75, -0.85)):
                m.move_to([x, y, 0])
            r_[0].align_to([-6.6, 0, 0], LEFT)
            return r_
        assert list(d["shortest"][[6, 8]]) == ["A - C", "A - C"] and not d["practised_works"][8]
        practice = VGroup(*[row(k, y) for k, y in ((1, -0.55), (2, -0.97), (3, -1.39))])
        dots = label(r"$\vdots$ \ five in a row", font_size=19, color=GREY_B).move_to([-4.9, -1.8, 0])
        crit = VGroup(row(6, -2.3), row(8, -2.75))
        checks = verdict_row([
            (r"Luchins, \ 1942: \ after five problems solved one way, \ most kept the long way when a short one "
             r"was there; \ on problem 9 many were stuck", "replicated"),
            (r"Bilali\'c, \ McLeod and Gobet, \ 2008: \ strong chess players miss a shorter mate, \ their eyes "
             r"held by the familiar one", "replicated"),
        ], width=5.6, font_size=20)
        checks.move_to([3.75, 0.55, 0])
        name = label(r"\emph{Einstellung}: \ a mental set", font_size=26, color=INSIGHT).next_to(checks, DOWN,
                                                                                                     buff=0.45)
        tag = published_tag(r"Luchins (1942); \ Bilali\'c, \ McLeod \& Gobet (2008)")
        with self.voiceover(
            "Duncker's obstacle lay in how an object is seen. Abraham Luchins found one in a method. "
            "<bookmark mark='a'/> In 1942 he gave people imaginary water jars. With jars that hold twenty-one, a "
            "hundred and twenty-seven and three cups, measure out exactly a hundred. <bookmark mark='b'/> The "
            "answer is to fill the big jar, pour off once into the first, and twice into the small one: B minus A "
            "minus two C. <bookmark mark='c'/> Five problems in a row yield to the same formula. "
            "<bookmark mark='d'/> Then come problems like the seventh: twenty-three, forty-nine and three, to "
            "measure twenty. The old formula works, but so does A minus C, in two steps. Most of those who had "
            "practised used the long way; groups who began at the critical problems almost always saw the short "
            "one. <bookmark mark='e'/> On the ninth, where the old formula fails and A minus C is the answer, many "
            "of the practised were stuck. Luchins called it Einstellung, a mental set: a way of working that hides "
            "a better one. <bookmark mark='f'/> Experts aren't immune. In 2008 Merim Bilalić, Peter McLeod and "
            "Fernand Gobet showed chess players a position with a familiar mate and a shorter one. Strong players "
            "missed the shorter mate, and their eyes kept going back to the familiar one even while they said they "
            "were looking for something better. Fixedness and set are obstacles with names. The most famous "
            "insight problem is harder to diagnose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(jA), FadeIn(jB), FadeIn(jC), FadeIn(want))
            vo.wait_until("b")
            self.play(fill_to(jB, B), run_time=0.8)
            self.play(fill_to(jB, B - A), fill_to(jA, A), run_time=0.8)
            self.play(fill_to(jB, B - A - C), fill_to(jC, C), run_time=0.6)
            self.play(fill_to(jC, 0), run_time=0.4)
            self.play(fill_to(jB, goal), fill_to(jC, C), run_time=0.6)
            self.play(Write(formula), Indicate(jB.body, color=SEARCH))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in practice], lag_ratio=0.4),
                      FadeIn(dots))
            vo.wait_until("d")
            self.play(FadeIn(crit[0], shift=RIGHT * 0.1))
            self.play(FadeIn(checks.rows[0], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(crit[1], shift=RIGHT * 0.1), FadeIn(name))
            vo.wait_until("f")
            self.play(FadeIn(checks.rows[1], shift=RIGHT * 0.15))
        self.clear_scene()

    def ninedots(self):
        d = load("ninedots")
        head = heading(r"The nine dots, \ by brute force")
        cA, cB = (-4.3, 0.6, 0), (-0.6, 0.6, 0)
        gA, gB = dots_grid(cA), dots_grid(cB)
        box = SurroundingRectangle(gA, color=GREY_B, buff=0.25, stroke_width=2)
        tA = label(r"turning only inside the square", font_size=21, color=GREY_A).next_to(box, DOWN, buff=0.3)
        nA = label(rf"{d['n_inside']} \ solutions", font_size=30, color=LOST).next_to(tA, DOWN, buff=0.15)
        path = d["classic"]
        pts = [to_scene(p, cB) for p in path]
        line = VMobject(color=MODEL, stroke_width=5).set_points_as_corners(pts)
        tB = label(r"allowed to turn outside it", font_size=21, color=GREY_A).move_to([cB[0], tA.get_y(), 0])
        nB = label(rf"{d['n_outside']} \ solutions", font_size=30, color=MODEL).next_to(tB, DOWN, buff=0.15)
        assert d["n_inside"] == 0 and d["n_outside"] == d["n_wider"]
        rows = rows_of([
            (r"four straight lines, \ without lifting the pen, \ through all nine dots", WHITE),
            (r"Psyche tries every path of four lines turning at grid points: \ inside the square there is none", LOST),
            (rf"outside it, \ {d['n_outside']} distinct drawings, \ and no more however far the grid goes", MODEL),
            (r"but telling people to go outside the square helps only a minority \ (Weisberg \& Alba, \ 1981): \ "
             r"the obstacle is not just one assumption", GREY_A),
        ], 4.6, 23, 0.36).move_to([4.4, 0.2, 0])
        tag = psyche_tag(r"\texttt{reason.nine\_dots}")
        with self.voiceover(
            "Here is the most famous insight problem. <bookmark mark='a'/> Join all nine dots with four straight "
            "lines, without lifting your pen. <bookmark mark='b'/> Psyche tries every path of four lines that turns "
            "only at points of the grid. Inside the square, there is no solution at all. <bookmark mark='c'/> Allow "
            f"it to turn outside the square, and there are {d['n_outside']} distinct drawings, and no more however "
            "far the grid extends. So the puzzle really does require leaving the box. <bookmark mark='d'/> Yet when "
            "Robert Weisberg and Joseph Alba told people that the lines could go outside the square, only a minority "
            "then solved it. The obstacle isn't just one hidden assumption, and that's part of what makes insight "
            "hard to explain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(gA), FadeIn(gB))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(box), FadeIn(tA), FadeIn(nA), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(tB), FadeIn(nB), FadeIn(rows[2]), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def warmth(self):
        head = heading(r"Is insight special?")
        A = axes([0, 4], [0, 7], x_length=5.6, y_length=3.2, xticks=[0, 1, 2, 3, 4], yticks=[1, 4, 7],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"time to the answer, \ quarters",
                 ylabel=r"feeling of warmth", center=[-3.2, 0.3, 0], font_size=16)
        x = np.linspace(0, 4, 50)
        alg = curve(A.ax, x, 1.5 + 1.3 * x, SEARCH, 3)
        ins = curve(A.ax, x, np.where(x < 3.6, 1.6 + 0.08 * x, 1.9 + 4.5 * (x - 3.6) / 0.4), INSIGHT, 3)
        key = legend([(SEARCH, r"algebra problems"), (INSIGHT, r"insight problems")], font_size=18).move_to(
            A.ax.c2p(1.2, 6.0))
        sch = label(r"schematic of the pattern reported, \ not data", font_size=18, color=GREY_B).next_to(
            A, DOWN, buff=0.4)
        rows = rows_of([
            (r"Metcalfe \& Wiebe, \ 1987: \ every 15 seconds, \ people rated how close they felt to the answer", WHITE),
            (r"on algebra problems, \ warmth rose steadily; \ on insight problems, \ it stayed low until the "
             r"answer came", INSIGHT),
            (r"people could predict which algebra problems they would solve, \ not which insight problems", GREY_A),
            (r"the other side: \ insight may be ordinary search, \ with progress you cannot monitor \ (MacGregor, "
             r"\ Ormerod \& Chronicle, \ 2001)", SEARCH),
        ], 5.8, 23, 0.36).move_to([3.5, 0.0, 0])
        tag = published_tag(r"Metcalfe \& Wiebe (1987); \ MacGregor, \ Ormerod \& Chronicle (2001)")
        with self.voiceover(
            "Is insight a different kind of thinking, or ordinary search that you can't see? "
            "<bookmark mark='a'/> In 1987 Janet Metcalfe and David Wiebe asked people, every fifteen seconds while "
            "they worked, how close they felt to the answer. <bookmark mark='b'/> On algebra problems the feeling "
            "of warmth rose steadily. On insight problems it stayed low, and then the answer came all at once. "
            "<bookmark mark='c'/> People could also predict which algebra problems they would solve, but not which "
            "insight problems. <bookmark mark='d'/> The other side argues that insight is ordinary search after all: "
            "James MacGregor and colleagues modelled the nine dots as a search guided by how much progress each line "
            "seems to make, and predicted when people would get stuck. Both may be right: the search is ordinary, "
            "and what changes suddenly is the space being searched."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(alg), Create(ins), FadeIn(key), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
