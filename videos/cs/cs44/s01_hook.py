from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


class Hook(VoiceoverScene):
    def construct(self):
        self.demo()
        self.lineage()
        self.measured()
        self.plan()

    def demo(self):
        head = label(r"San Francisco, \ 9 December 1968", font_size=38).to_edge(UP, buff=0.35)
        # a schematic of the demo: a screen, a keyboard, a chord keyset and a mouse
        screen = RoundedRectangle(width=4.2, height=2.8, corner_radius=0.12, stroke_color=GREY_B, fill_color=BG,
                                  fill_opacity=1).move_to([-3.4, 0.6, 0])
        lines = VGroup(*[Line([-5.1, 1.5 - 0.35 * k, 0], [-5.1 + w, 1.5 - 0.35 * k, 0], color=GREY_C,
                              stroke_width=3) for k, w in enumerate((2.6, 3.1, 1.8, 2.9, 2.2))])
        link = Line([-4.3, 0.45, 0], [-3.4, 0.45, 0], color=DATA, stroke_width=4)
        cursor = Triangle(color=WHITE, fill_opacity=1).scale(0.09).rotate(-0.5).move_to([-2.3, -0.1, 0])
        mouse = VGroup(RoundedRectangle(width=0.55, height=0.8, corner_radius=0.12, stroke_color=HEAD),
                       Line([0, 0.4, 0], [0, 0.75, 0], color=HEAD)).move_to([-1.3, -1.7, 0])
        kb = RoundedRectangle(width=3.0, height=0.5, corner_radius=0.08, stroke_color=GREY_B).move_to([-4.0, -1.7,
                                                                                                    0])
        caps = VGroup(label(r"the mouse \ (Engelbart and English, \ 1964)", font_size=17, color=HEAD).next_to(
            mouse, DOWN, buff=0.15))
        items = VGroup(*[label(t, font_size=22, color=c) for t, c in (
            (r"a mouse and a pointer on a screen", HEAD),
            (r"text linked to other text: \ hypertext", DATA),
            (r"two people editing one document, \ live", YES),
            (r"video of a colleague thirty miles away", LAM),
            (r"one system: \ NLS, \ from Douglas Engelbart's lab at SRI", GREY_A))]).arrange(DOWN, aligned_edge=LEFT,
                                                                                     buff=0.32)
        items.move_to([3.4, 0.2, 0])
        with self.voiceover(
            "On the ninth of December 1968, in San Francisco, Douglas Engelbart sat on a stage with a screen, a "
            "keyboard and a small wooden box with wheels underneath. <bookmark mark='a'/> For ninety minutes he "
            "showed a thousand engineers what a computer could be for a person. A pointer on the screen that "
            "followed his hand, through the box his lab had invented: the mouse. <bookmark mark='b'/> Words linked "
            "to other words, so that clicking one opened another: hypertext. <bookmark mark='c'/> A colleague "
            "thirty miles away, editing the same document at the same time, <bookmark mark='d'/> his face in a "
            "window on the screen. <bookmark mark='e'/> It was one working system, called NLS, from Engelbart's lab "
            "at the Stanford Research Institute. It came to be called the mother of all demos."
        ) as vo:
            self.play(FadeIn(head), Create(screen), FadeIn(kb), FadeIn(mouse))
            vo.wait_until("a")
            self.play(FadeIn(cursor), FadeIn(caps), FadeIn(items[0]))
            self.play(cursor.animate.move_to([-3.8, 0.55, 0]), mouse.animate.shift(LEFT * 0.4 + UP * 0.2),
                      run_time=1.2)
            vo.wait_until("b")
            self.play(Create(lines), FadeIn(items[1]))
            self.play(Create(link))
            vo.wait_until("c")
            self.play(FadeIn(items[2]))
            vo.wait_until("d")
            self.play(FadeIn(items[3]))
            vo.wait_until("e")
            self.play(FadeIn(items[4]))
        self.wait(0.4)
        self.clear_scene()

    def lineage(self):
        head = label(r"From a demo to everyone's desk", font_size=36).to_edge(UP, buff=0.3)
        events = [(1968, r"NLS demo", HEAD), (1973, r"Xerox Alto: \ windows, \ icons, \ a mouse", DATA),
                  (1979, r"Jobs visits PARC", GREY_A), (1984, r"Macintosh", YES),
                  (1985, r"Windows 1.0", LAM), (1991, r"the web", KERN), (2007, r"iPhone: \ multi-touch", NO)]
        x0, x1 = -6.0, 6.0
        axis = Line([x0, 0, 0], [x1, 0, 0], color=GREY_C)

        def X(y):
            return x0 + (y - 1965) / (2010 - 1965) * (x1 - x0)
        marks = VGroup()
        for k, (y, t, c) in enumerate(events):
            up = k % 2 == 0
            d = Dot([X(y), 0, 0], radius=0.08, color=c)
            stem = Line([X(y), 0, 0], [X(y), 0.9 if up else -0.9, 0], color=c, stroke_width=1.5)
            lb = VGroup(label(f"{y}", font_size=18, color=c), wrapped_label(t, 2.3, font_size=17, color=GREY_A))
            lb.arrange(DOWN, buff=0.06).next_to(stem, UP if up else DOWN, buff=0.08)
            marks.add(VGroup(d, stem, lb))
        foot = wrapped_label(r"each step was an argument about people: \ what they can see, \ reach, \ remember "
                             r"and decide, \ and how fast", 12.4, font_size=21, color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The ideas took fifteen years to reach ordinary desks. <bookmark mark='a'/> At Xerox PARC, the Alto of "
            "1973 put windows, icons and a mouse on a personal machine. In 1979 Steve Jobs visited, and the "
            "Macintosh followed in 1984, Windows a year later. The web arrived in 1991, and multi-touch phones in "
            "2007. <bookmark mark='b'/> Each step was an argument about people: what they can see, reach, "
            "remember and decide, and how quickly. This part treats those arguments as science."
        ) as vo:
            self.play(FadeIn(head), Create(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.35), run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def measured(self):
        f = load("fitts")
        pk = load("peeking")
        head = label(r"People, \ and products, \ can be measured", font_size=36).to_edge(UP, buff=0.3)

        def chart(xs, ys, color, xlab, ylab, x0, y0, w=5.2, h=3.0, ymin=None, ymax=None):
            ymin = min(ys) if ymin is None else ymin
            ymax = max(ys) if ymax is None else ymax
            xmin, xmax = min(xs), max(xs)
            ax = VGroup(Line([x0, y0, 0], [x0 + w, y0, 0], color=GREY_C), Line([x0, y0, 0], [x0, y0 + h, 0],
                                                                                color=GREY_C))
            pts = [[x0 + (x - xmin) / (xmax - xmin) * w, y0 + (y - ymin) / (ymax - ymin) * h, 0]
                   for x, y in zip(xs, ys)]
            lb = VGroup(label(xlab, font_size=17, color=GREY_B).next_to(ax[0], DOWN, buff=0.15),
                        label(ylab, font_size=17, color=GREY_B).next_to(ax[1], UP, buff=0.1))
            return ax, pts, lb
        rows = sorted(f["rows"], key=lambda r: r["ID"])
        ax1, p1, l1 = chart([r["ID"] for r in rows], [r["MT"] for r in rows], DATA, r"difficulty, \ bits",
                            r"movement time, \ s", -6.4, -1.9)
        dots = VGroup(*[Dot(p, radius=0.05, color=DATA) for p in p1])
        fit = Line(p1[0], p1[-1], color=HEAD, stroke_width=2)
        days = list(range(1, len(pk["fpr_peeking"]) + 1))
        ax2, p2, l2 = chart(days, pk["fpr_peeking"], NO, r"days of daily checking", r"false positives",
                            0.9, -1.9, ymin=0, ymax=0.3)
        curve = VMobject(color=NO, stroke_width=3).set_points_as_corners(p2)
        five = DashedLine([0.9, -1.9 + 0.05 / 0.3 * 3.0, 0], [6.1, -1.9 + 0.05 / 0.3 * 3.0, 0], color=YES)
        cap1 = label(rf"Fitts's law: \ $R^2 = {f['r2']:.2f}$", font_size=20, color=HEAD).next_to(ax1, UP, buff=0.5)
        cap2 = label(rf"an A/A test checked daily: \ {100 * pk['fpr_peeking'][-1]:.0f}\% false positives", font_size=20,
                     color=NO).next_to(ax2, UP, buff=0.5)
        with self.voiceover(
            "Two kinds of measurement run through this part. <bookmark mark='a'/> The first is of people. The time "
            "to point at a target grows with the logarithm of its distance over its width, so precisely that the "
            "points fall on a line. That is Fitts's law, and it comes from Shannon's channel capacity. "
            "<bookmark mark='b'/> The second is of products: controlled experiments that compare two versions with "
            "real users. They have their own traps. Here, two identical versions are compared and checked every "
            f"day for a month; {100 * pk['fpr_peeking'][-1]:.0f} percent of these experiments declare a winner "
            "where there is none, against the five percent the test promises."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax1), FadeIn(l1), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05))
            self.play(Create(fit), FadeIn(cap1))
            vo.wait_until("b")
            self.play(Create(ax2), FadeIn(l2), Create(five))
            self.play(Create(curve), run_time=2)
            self.play(FadeIn(cap2))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ People and Products", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"Fitts's law from channel capacity; \ Hick's law as entropy",
            r"predicting task times; \ the thresholds of perception",
            r"colour: \ sRGB, \ OKLab, \ contrast and colour blindness",
            r"how many users a usability test needs",
            r"the A/B test, \ its power, \ and the peeking problem",
            r"CUPED, \ false discoveries, \ bandits and Goodhart",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 44 of Computer Science, Built, the last part of Act Eight. <bookmark mark='a'/> We will "
            "derive Fitts's law from channel capacity and Hick's law from entropy; predict how long a task takes "
            "before anyone does it; turn colour into formulas and check this series' own palette for colour-blind "
            "viewers; and then run experiments on products, deriving their power, and seeing why looking at the "
            "results every morning breaks them, and how to look safely."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (KERN, LAM, YES)
