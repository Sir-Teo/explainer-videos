from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Mhp(VoiceoverScene):
    def construct(self):
        card_section(self, 2, r"The Model Human Processor", r"Can a person be drawn as an engineer's diagram?",
                     marr=("how",))
        self.diagram()
        self.predictions()

    def diagram(self):
        head = heading(r"Three processors, \ three memories")
        boxes = VGroup()
        specs = [(r"perceptual", r"$\tau_P$ = 100 ms (50 to 200)", SYMP, -4.4),
                 (r"cognitive", r"$\tau_C$ = 70 ms (25 to 170)", MODEL, 0.0),
                 (r"motor", r"$\tau_M$ = 70 ms (30 to 100)", PERSON, 4.4)]
        for name, t, col, x in specs:
            b = RoundedRectangle(width=3.4, height=1.4, corner_radius=0.15, color=col, fill_opacity=0.15)
            b.move_to([x, 1.2, 0])
            boxes.add(VGroup(b, label(name, font_size=24, color=col).move_to(b).shift(UP * 0.25),
                             label(t, font_size=17, color=WHITE).move_to(b).shift(DOWN * 0.3)))
        arrows = VGroup(Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.1, color=GREY_B),
                        Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.1, color=GREY_B))
        mems = VGroup(label(r"visual store: \ about 200 ms (Part 19's iconic memory)", font_size=17, color=SYMP),
                      label(r"working memory: \ about 7 chunks, \ fading in seconds (Part 19)", font_size=17,
                            color=MODEL),
                      label(r"long-term memory: \ unlimited, \ slow to write (Parts 20 and 21)", font_size=17,
                            color=GREY_A)).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([0, -0.5, 0])
        rows = rows_of([
            (r"Card, \ Moran and Newell, \ 1983: \ a person as three processors with cycle times, \ and memories with "
             r"capacities and decay rates", WHITE),
            (r"every number came from the experiments of Acts III and V, \ each given as typical, \ fast and slow", MODEL),
            (r"the claim was not that the mind is built this way, \ but that this is accurate enough to design with",
             YOU),
        ], 12.4, 20, 0.3).move_to([0, -2.5, 0])
        with self.voiceover(
            "In 1983 Stuart Card, Thomas Moran and Allen Newell drew a person as an engineer would. "
            "<bookmark mark='a'/> Three processors, perceptual, cognitive and motor, each with a cycle time, and "
            "memories with capacities and decay rates. <bookmark mark='b'/> Every number came from the experiments of "
            "Acts Three and Five, and each is given as typical, fast and slow. <bookmark mark='c'/> The claim wasn't "
            "that the mind is built this way. It was that this is accurate enough to design with."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3),
                      *[GrowArrow(a) for a in arrows])
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(mems))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def predictions(self):
        d = load("mhp")
        head = heading(r"Predictions by adding cycles")
        A = axes([0.3, 3.7], [0, 900], x_length=5.4, y_length=3.2, xticks=None, yticks=[0, 300, 600, 900],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"reaction time (ms)", center=[-3.3, 0.3, 0], font_size=12)
        kinds = ["simple", "physical", "name"]
        typ = [d[k]["typical"] for k in kinds]
        b = bars(A.ax, [1, 2, 3], typ, [SYMP, MODEL, PERSON], width=0.55)
        whisk = VGroup(*[Line(A.ax.c2p(i + 1, d[k]["fast"]), A.ax.c2p(i + 1, d[k]["slow"]), color=WHITE,
                              stroke_width=2) for i, k in enumerate(kinds)])
        names = VGroup(*[label(s, font_size=14, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, s in enumerate([r"simple", r"same shape?", r"same letter?"])])
        rows = rows_of([
            (r"a simple reaction: \ perceive, \ decide, \ move: \ $\tau_P + \tau_C + \tau_M$ = 240 ms (105 to 470)",
             SYMP),
            (r"``are these the same shape?'' \ adds one cognitive cycle: \ 310 ms", MODEL),
            (r"``same letter, \ A and a?'' \ adds two: \ 380 ms; \ Part 1's Posner and Donders, \ as arithmetic",
             PERSON),
            (r"the ranges are wide: \ the model predicts the order and the scale, \ not one person's millisecond", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.mhp\_reaction}")
        with self.voiceover(
            "The model predicts by adding cycles. <bookmark mark='a'/> A simple reaction is perceive, decide, move: "
            "two hundred and forty milliseconds, with a range from about a hundred to almost five hundred. "
            "<bookmark mark='b'/> Asking whether two shapes are the same adds one cognitive cycle: three hundred and "
            "ten. <bookmark mark='c'/> Asking whether A and small a are the same letter adds two: three hundred and "
            "eighty. That's Part 1's Posner and Donders, as arithmetic. <bookmark mark='d'/> The ranges are wide. The "
            "model predicts the order and the scale, not one person's millisecond."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            for i, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(rows[i]), FadeIn(b[i]), Create(whisk[i]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
