from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


def display(cue: str = "", target: str = "", center=(0, 1.3)):
    """Posner's display: a fixation cross between two boxes; a central arrow or a flash on one box; a target."""
    c = np.array([center[0], center[1], 0])
    lb = Square(1.0, color=GREY_B, stroke_width=3).move_to(c + LEFT * 2.4)
    rb = Square(1.0, color=GREY_B, stroke_width=3).move_to(c + RIGHT * 2.4)
    fix = VGroup(Line(c + LEFT * 0.15, c + RIGHT * 0.15), Line(c + UP * 0.15, c + DOWN * 0.15)).set_stroke(WHITE, 3)
    g = VGroup(lb, rb, fix)
    if cue == "arrow":
        g.add(Arrow(c + LEFT * 0.45, c + RIGHT * 0.5, buff=0, color=ATT, stroke_width=6,
                    max_tip_length_to_length_ratio=0.35).shift(UP * 0.4))
    if cue == "flash":
        g.add(Square(1.12, color=ATT, stroke_width=7).move_to(rb))
    if target:
        g.add(Star(5, outer_radius=0.22, color=WHITE, fill_opacity=1).move_to(rb if target == "right" else lb))
    return g


class Space(VoiceoverScene):
    def construct(self):
        self.card()
        self.posner()
        self.costs()
        self.two_cues()

    def card(self):
        card = chapter_card(3, r"A spotlight that moves without the eyes", r"Can you attend where you are not looking?",
                            lit={1980: r"Posner", 1984: r"Posner \& Cohen"}, part=PART, scale=("mind", "brain"),
                            marr=("what", "how"))
        with self.voiceover("Chapter three. A spotlight that moves without the eyes."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def posner(self):
        p = archive.POSNER_1980.data
        head = heading(r"Posner's cueing task")
        d0 = display()
        d1 = display("arrow")
        d2 = display("arrow", "right")
        d3 = display("arrow", "left")
        rows = rows_of([
            (r"keep your eyes on the cross; \ press a key the moment a star appears in either box", WHITE),
            (rf"an arrow first points to one box; \ it is right on {pct(p['valid_share'])} of trials", ATT),
            (r"valid: \ the star appears where the arrow pointed", GOOD),
            (r"invalid: \ it appears on the other side", BAD),
            (r"the eyes were checked: \ they stayed on the cross; \ attention moved by itself", CUE),
        ], 12.4, 27, 0.32).to_edge(DOWN, buff=0.75)
        tag = historical_tag(archive.POSNER_1980.cite)
        with self.voiceover(
            "Can you attend to a place without looking at it? <bookmark mark='a'/> Michael Posner's answer, in 1980, "
            "used a display of almost nothing: a cross to keep your eyes on, a box on each side, and a key to press "
            "the moment a star appears in either box. <bookmark mark='b'/> Before the star, an arrow at the centre "
            "points to one box, and it is right on eighty percent of trials. <bookmark mark='c'/> On valid trials the "
            "star appears where the arrow pointed. <bookmark mark='d'/> On invalid trials it appears on the other side. "
            "<bookmark mark='e'/> Posner checked that the eyes stayed on the cross. Whatever moved, it wasn't the eyes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(d0))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(d1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(d2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeOut(d2), FadeIn(d3), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def costs(self):
        d = load("cueing")
        head = heading(r"Benefits and costs")
        A = axes([0, 3], [240, 350], x_length=5.0, y_length=3.3, xticks=[], yticks=[250, 300, 350],
                 ylabel=r"mean RT, \ ms", center=[-3.2, 0.5, 0], font_size=18)
        ax = A.ax
        bars, labs = VGroup(), VGroup()
        for k, (key, name, col) in enumerate([("valid", r"valid", GOOD), ("neutral", r"neutral", GREY_B),
                                              ("invalid", r"invalid", BAD)]):
            lo, hi = ax.c2p(k + 0.5, 240), ax.c2p(k + 0.5, d[key])
            bars.add(Rectangle(width=0.9, height=hi[1] - lo[1], stroke_width=0, fill_color=col, fill_opacity=0.85)
                     .move_to([lo[0], (lo[1] + hi[1]) / 2, 0]))
            labs.add(VGroup(label(name, font_size=20, color=col).next_to(lo, DOWN, buff=0.15),
                            label(rf"{d[key]:.0f}", font_size=19, color=col).next_to(hi, UP, buff=0.08)))
        ben = BraceBetweenPoints(ax.c2p(1.05, d["valid"]), ax.c2p(1.05, d["neutral"]), direction=LEFT, color=GOOD)
        cost = BraceBetweenPoints(ax.c2p(1.95, d["neutral"]), ax.c2p(1.95, d["invalid"]), direction=RIGHT, color=BAD)
        rows = rows_of([
            (r"a neutral cue tells you nothing: \ the baseline", GREY_B),
            (r"benefit: \ faster where you were attending", GOOD),
            (r"cost: \ slower elsewhere, \ while attention is moved", BAD),
            (r"tens of milliseconds each way: \ small, \ but it reproduces in every laboratory", ATT),
            (r"Posner's image: \ a spotlight that moves, \ engaging and disengaging", CUE),
        ], 6.0, 25, 0.42).move_to([3.4, 0.0, 0])
        ptag = psyche_tag(r"\texttt{attention.posner\_rts}: \ a 400 ms cue, \ 400 trials a condition")
        tag = historical_tag(archive.POSNER_1980.cite)
        with self.voiceover(
            "A third kind of trial gives a baseline. <bookmark mark='a'/> On neutral trials the cue points both ways, "
            "or nowhere, and says nothing. <bookmark mark='b'/> Compared with neutral, valid trials are faster: a "
            "benefit, from already attending where the star appears. <bookmark mark='c'/> Invalid trials are slower: "
            "a cost, because attention has to be pulled away from the wrong place and moved. "
            "<bookmark mark='d'/> Each is a few tens of milliseconds, which sounds small. But it's one of the most "
            "reliable effects in experimental psychology, found in essentially every laboratory that has run the "
            "task. Psyche's version shows the shape. <bookmark mark='e'/> Posner's image was a spotlight that "
            "disengages from one place, moves, and engages at another, without the eyes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ptag), FadeIn(A))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(labs[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(labs[0]), FadeIn(ben), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(labs[2]), FadeIn(cost), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def two_cues(self):
        d = load("cueing")
        head = heading(r"Two ways to move it, \ and a rebound")
        dl = display("arrow", center=(-3.6, 2.25)).scale(0.5)
        dr = display("flash", center=(3.6, 2.25)).scale(0.5)
        tl = label(r"an arrow: \ voluntary", font_size=21, color=CUE).next_to(dl, DOWN, buff=0.1)
        tr = label(r"a flash: \ captured", font_size=21, color=ATT).next_to(dr, DOWN, buff=0.1)
        A = axes([0, 1000], [-40, 70], x_length=7.6, y_length=2.1, xticks=[0, 250, 500, 750, 1000],
                 yticks=[-25, 0, 25, 50], xlabel=r"time from cue to star, \ ms",
                 ylabel=r"invalid minus valid RT, \ ms", center=[0, -0.25, 0], font_size=17)
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(1000, 0), color=GREY_D, stroke_width=1.5)
        ce = curve(ax, d["soa"], d["endogenous"], CUE, 4)
        cx = curve(ax, d["soa"], d["exogenous"], ATT, 4)
        ior = label(r"inhibition of return: \ the flashed side is now slower", font_size=19, color=ATT)
        ior.move_to(ax.c2p(690, 22))
        rows = rows_of([
            (r"a predictive arrow: \ the effect builds over a few hundred ms and stays", CUE),
            (r"a flash, \ even an uninformative one, \ captures attention within 100 ms", ATT),
            (r"after about 300 ms the flashed place is inhibited: \ search does not go back", GREY_A),
        ], 12.4, 22, 0.16).to_edge(DOWN, buff=0.72)
        ptag = psyche_tag(r"\texttt{attention.cue\_effect}: \ the shapes, \ with Psyche's time constants")
        tag = historical_tag(r"Posner \& Cohen (1984)")
        with self.voiceover(
            "There turned out to be two ways to move the spotlight. <bookmark mark='a'/> An arrow is a voluntary "
            "instruction: you have to read it and decide to follow it, and its effect builds over a few hundred "
            "milliseconds, then stays as long as the arrow stays useful. <bookmark mark='b'/> A flash on one of the "
            "boxes works differently. It captures attention whether or not it predicts anything, and fast, within a "
            "tenth of a second. <bookmark mark='c'/> Then something odd happens. In 1984 Posner and Yoav Cohen found "
            "that a few hundred milliseconds after an uninformative flash, the flashed side becomes slower than the "
            "other. Attention has left, and is reluctant to return: inhibition of return. It is a sensible bias for "
            "a searcher, who should not keep checking the same place."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ptag), FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(dl), FadeIn(tl), Create(ce), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(dr), FadeIn(tr), Create(cx), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(ior), FadeIn(rows[2]))
        self.clear_scene()
