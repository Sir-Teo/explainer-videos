from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403

SQUARES = [((-1.0, 0.6), 0.2), ((0.9, 0.9), 2.1), ((-0.3, -0.7), 3.6), ((1.2, -0.5), 4.6), ((-1.4, -0.3), 1.2),
           ((0.2, 0.2), 5.5)]


def squares(colours, center, scale=1.0, side=0.42):
    return VGroup(*[Square(side * scale, stroke_width=0, fill_color=hue(a), fill_opacity=1)
                    .move_to(np.array([center[0] + x * scale, center[1] + y * scale, 0]))
                    for (x, y), a in colours])


class Four(VoiceoverScene):
    def construct(self):
        self.card()
        self.task()
        self.derive()
        self.cowan()

    def card(self):
        card = chapter_card(6, r"Four, \ not seven", r"How many things can you hold, \ without rehearsing?",
                            lit={1997: r"Luck \& Vogel", 2001: r"Cowan"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter six. Four, not seven."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def task(self):
        d = load("change")
        p = archive.LUCK_VOGEL_1997.data
        head = heading(r"Change detection")
        sample = squares(SQUARES, (-5.0, 1.75), scale=0.78)
        test = squares([(xy, a if k != 2 else 0.9) for k, (xy, a) in enumerate(SQUARES)], (-1.4, 1.75), scale=0.78)
        f1 = SurroundingRectangle(sample, color=GREY_C, buff=0.3)
        f2 = SurroundingRectangle(test, color=GREY_C, buff=0.3)
        c1 = label(r"100 ms", font_size=18, color=GREY_B).next_to(f1, DOWN, buff=0.1)
        c2 = label(r"900 ms later: \ same or different?", font_size=18, color=GREY_B).next_to(f2, DOWN, buff=0.1)
        A = axes([0.5, 8.5], [0.5, 1.0], x_length=5.4, y_length=2.3, xticks=list(range(1, 9)), yticks=[0.5, 0.75, 1],
                 xlabel=r"squares in the display", ylabel=r"accuracy", center=[-2.9, -1.75, 0], font_size=17,
                 yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        c = VGroup(curve_in(ax, d["N"], d["accuracy"], MODEL, 4), scatter(ax, d["N"], d["accuracy"], MODEL, 0.06))
        rows = rows_of([
            (r"1997: \ Steven Luck and Edward Vogel; \ an array of coloured squares, \ a blank, \ the array again", WHITE),
            (r"too brief and too many to name: \ no verbal rehearsal", GREY_A),
            (rf"accuracy is near perfect up to 3 or 4 squares, \ then falls: \ capacity about {p['capacity']}", MEM),
            (r"objects with four features each are held as well as single colours: \ the unit is the object", EXEC),
        ], 5.4, 22, 0.3).move_to([3.9, -0.1, 0])
        ptag = psyche_tag(r"\texttt{wm.change\_detection}: \ $K = 3.5$ slots")
        tag = published_tag(archive.LUCK_VOGEL_1997.cite)
        with self.voiceover(
            "Digit span overestimates capacity, because people rehearse and chunk. To measure the raw limit you need "
            "a task that defeats both. <bookmark mark='a'/> In 1997 Steven Luck and Edward Vogel flashed an array of "
            "coloured squares for a tenth of a second, then a blank of nearly a second, then the array again, with "
            "one square perhaps changed. Same or different? <bookmark mark='b'/> The colours are too brief to name "
            "and there are too many to rehearse. <bookmark mark='c'/> Accuracy was nearly perfect with up to three or "
            f"four squares, then fell steadily: a capacity of about {p['capacity']}. <bookmark mark='d'/> And when "
            "each object had four features, a colour, an orientation, a size and a gap, people held four objects "
            "about as well as four colours. They concluded the limit counts objects, not features, though later "
            "work found the features are not quite free."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(f1), FadeIn(sample), FadeIn(c1))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(f2), FadeIn(test), FadeIn(c2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(A))
            vo.wait_until("c")
            self.play(Create(c), FadeIn(rows[2]), FadeIn(ptag), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def derive(self):
        d = load("change")
        head = heading(r"Derived: \ counting slots from hits and false alarms")
        eqs = VGroup(
            MathTex(r"H = \tfrac{K}{N} + \big(1 - \tfrac{K}{N}\big)\,g", font_size=40, color=GOOD),
            MathTex(r"F = \big(1 - \tfrac{K}{N}\big)\,g", font_size=40, color=LOST),
            MathTex(r"H - F = \tfrac{K}{N} \quad\Longrightarrow\quad K = N\,(H - F)", font_size=40, color=MEM),
        ).arrange(DOWN, buff=0.45).move_to([-2.9, 0.9, 0])
        notes = rows_of([
            (r"$K$ of the $N$ items are stored; \ if the changed one is among them, \ the change is seen", WHITE),
            (r"otherwise, \ guess ``different'' with probability $g$, \ on change and no-change trials alike", GREY_A),
            (r"the guessing cancels in $H - F$: \ Cowan's $K$, \ for a single probed item", MEM),
            (r"for a whole-display test, \ Pashler's version: \ $K = N\,(H - F) / (1 - F)$", EXEC),
        ], 5.6, 23, 0.3).move_to([3.7, 0.9, 0])
        A = axes([0.5, 8.5], [0, 5], x_length=6.0, y_length=1.9, xticks=list(range(1, 9)), yticks=[0, 2, 4],
                 xlabel=r"squares", ylabel=r"$K$", center=[-1.4, -2.15, 0], font_size=17)
        ax = A.ax
        kc = VGroup(curve_in(ax, d["N"], d["K"], MEM, 4), scatter(ax, d["N"], d["K"], MEM, 0.06))
        kl = label(r"$K = \min(N, 3.5)$: \ recovered", font_size=20, color=MEM).next_to(A, RIGHT, buff=0.3)
        ptag = psyche_tag(r"Psyche's hits and false alarms, \ 4,000 trials per set size")
        with self.voiceover(
            "How do you get a number from accuracy? With a model, and the model here is about as simple as they come. "
            "<bookmark mark='a'/> Suppose K of the N items are stored. On a change trial, if the changed item is among "
            "the stored ones, the change is detected; otherwise you guess different with some probability g. So the "
            "hit rate is K over N plus the rest times g. <bookmark mark='b'/> On a no-change trial, a stored item is "
            "correctly seen as the same, and otherwise you guess, so the false-alarm rate is the unstored share times "
            "g. <bookmark mark='c'/> Subtract, and the guessing cancels: K equals N times hits minus false alarms. "
            "That is Nelson Cowan's formula for a test that probes one item. <bookmark mark='d'/> When the whole "
            "display reappears, Harold Pashler's version divides by one minus the false-alarm rate. Applied to "
            "Psyche, whose true K is three and a half, the formula recovers it at every set size above three. "
            "Remember this derivation's assumption, that an item is either stored perfectly or not at all. The next "
            "chapter puts it on trial."
        ) as vo:
            self.play(FadeIn(head), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]), FadeIn(A), Create(kc), FadeIn(kl), FadeIn(ptag))
        self.clear_scene()

    def cowan(self):
        p = archive.COWAN_2001.data
        head = heading(r"The magical number four")
        rows = rows_of([
            (r"2001: \ Nelson Cowan reviews every task that blocks rehearsal and chunking", WHITE),
            (r"change detection, \ running span, \ the size of the recency effect, \ enumeration: \ about 3 to 5 chunks",
             MEM),
            (rf"his estimate: \ {p['capacity']} \ $\pm$ 1, \ in adults", MEM),
            (r"seven was a span with help: \ rehearsal, \ chunking, \ and long-term knowledge of the items", GREY_A),
            (r"subitizing: \ up to about four dots are counted at a glance; \ beyond, \ one by one", EXEC),
            (r"but a clean count of slots assumes slots exist: \ an item fully stored, \ or not at all", LOST),
        ], 12.0, 28, 0.38).move_to([0, -0.2, 0])
        tag = historical_tag(archive.COWAN_2001.cite)
        with self.voiceover(
            "Others had been finding the same number from different directions. <bookmark mark='a'/> In 2001 Nelson "
            "Cowan reviewed every task he could find that blocks rehearsal and chunking. <bookmark mark='b'/> Change "
            "detection, running span where a list stops unpredictably, the number of items in the recency part of a "
            "free-recall curve, how many dots can be counted at a glance: the estimates clustered between three and "
            f"five. <bookmark mark='c'/> Cowan's summary was {p['capacity']}, plus or minus one. <bookmark mark='d'/> "
            "Seven, on this view, was a span with help: rehearsal, chunking, and everything you know about digits. "
            "<bookmark mark='e'/> Even counting has a break near four: up to about four dots, the number is seen at a "
            "glance; beyond, you count. <bookmark mark='f'/> But every one of these estimates comes through a model in "
            "which an item is held perfectly or not at all. What if that's wrong?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
