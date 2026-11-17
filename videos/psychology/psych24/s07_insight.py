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
        self.candle()
        self.ninedots()
        self.warmth()

    def card(self):
        card = chapter_card(6, r"Insight", r"Why is the answer obvious only afterwards?",
                            lit={1945: r"Duncker", 1987: r"Metcalfe \& Wiebe", 2001: r"MacGregor et al."},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter six. Insight."):
            self.play(FadeIn(card, shift=UP * 0.2))
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
