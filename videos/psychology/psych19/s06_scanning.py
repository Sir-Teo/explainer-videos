from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403


class Scanning(VoiceoverScene):
    def construct(self):
        self.card()
        self.task()
        self.serial()
        self.mimicry()

    def card(self):
        card = chapter_card(5, r"Searching what you hold", r"How do you check whether 7 is in your list?",
                            lit={1966: r"Sternberg", 1972: r"Townsend"}, part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter five. Searching what you hold."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def task(self):
        p = archive.STERNBERG_1966.data
        d = load("sternberg")
        head = heading(r"Sternberg's memory scanning")
        strip = trial_strip([
            (r"a memory set, \ 1 to 6 digits", label(r"3 \ 8 \ 1 \ 6", font_size=40, color=MEM), r"1.2 s each"),
            (r"a pause", None, r"2 s"),
            (r"a probe digit", label(r"8", font_size=48), ""),
            (r"in the set? \ yes or no", label(r"yes", font_size=40, color=GOOD), r"RT"),
        ], frame_w=2.6, frame_h=1.2, font_size=19).move_to([0, 2.0, 0])
        A = axes([0.5, 6.5], [350, 700], x_length=6.2, y_length=3.0, xticks=[1, 2, 3, 4, 5, 6],
                 yticks=[400, 500, 600, 700], xlabel=r"digits in the memory set", ylabel=r"RT, \ ms",
                 center=[-2.8, -1.2, 0], font_size=18)
        ax = A.ax
        k = d["k"]
        yes = VGroup(curve_in(ax, k, d["serial_yes"], GOOD, 4), scatter(ax, k, d["serial_yes"], GOOD, 0.07))
        no = VGroup(DashedVMobject(curve_in(ax, k, d["serial_no"], LOST, 3), num_dashes=20),
                    scatter(ax, k, d["serial_no"], LOST, 0.06))
        key = legend([(GOOD, r"yes"), (LOST, r"no")], font_size=18).arrange(RIGHT, buff=0.4)
        key.next_to(ax.c2p(1, 690), RIGHT, buff=0.1).align_to(ax.c2p(1, 690), UP)
        eq = MathTex(rf"\text{{RT}} = {p['intercept_ms']:.0f} + {p['slope_ms']:.0f}\,s \ \text{{ms}}", font_size=34,
                     color=DATA)
        rows = rows_of([
            (r"1966: \ Saul Sternberg, \ Bell Labs", WHITE),
            (rf"RT rises in a straight line: \ about {p['slope_ms']:.0f} ms per digit held; \ $r^2 = "
             rf"{p['r2']:.3f}$", DATA),
            (r"and the slope is the same for yes and for no", MEM),
        ], 5.0, 23, 0.3)
        right = VGroup(eq, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.9, -1.0, 0])
        ptag = psyche_tag(r"\texttt{wm.sternberg\_rts}: \ exhaustive serial comparison")
        tag = published_tag(archive.STERNBERG_1966.cite)
        with self.voiceover(
            "Once something is held, how do you use it? <bookmark mark='a'/> In 1966 Saul Sternberg at Bell Labs gave "
            "people a short list of digits to hold, then a single probe digit, and asked: was it in the list? Yes or "
            "no, as fast as you can. <bookmark mark='b'/> Reaction time rose in a perfectly straight line with the "
            f"number of digits held, about {p['slope_ms']:.0f} milliseconds for each extra digit, starting from about "
            f"{p['intercept_ms']:.0f} milliseconds. A straight line through the means explained "
            f"{100 * p['r2']:.1f} percent of their variance. <bookmark mark='c'/> And the surprising part: the slope "
            "was the same whether the answer was yes or no."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(strip))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(A))
            vo.wait_until("b")
            self.play(Create(yes), FadeIn(eq), FadeIn(rows[1]), FadeIn(ptag), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(no), FadeIn(key), FadeIn(rows[2]), run_time=1.5)
        self.clear_scene()

    def serial(self):
        d = load("sternberg")
        head = heading(r"Why the same slope means \ ``check everything''")
        A = axes([0.5, 6.5], [350, 700], x_length=6.6, y_length=3.6, xticks=[1, 2, 3, 4, 5, 6],
                 yticks=[400, 500, 600, 700], xlabel=r"digits in the memory set", ylabel=r"RT, \ ms",
                 center=[-2.6, 0.35, 0], font_size=18)
        ax = A.ax
        k = d["k"]
        ex = curve_in(ax, k, d["serial_yes"], MEM, 4)
        st = curve_in(ax, k, d["self_yes"], SLOT, 4)
        st_no = DashedVMobject(curve_in(ax, k, d["self_no"], SLOT, 3), num_dashes=20)
        key = legend([(MEM, r"exhaustive: \ yes and no alike"), (SLOT, r"self-terminating: \ yes"),
                      (SLOT, r"dashed: \ self-terminating, \ no")], font_size=18).next_to(A, DOWN, buff=0.3)
        rows = rows_of([
            (r"serial: \ compare the probe with one digit at a time", WHITE),
            (r"if you stop at a match, \ a yes needs half the comparisons on average: \ half the slope", SLOT),
            (r"a no always needs all of them: \ the full slope", LOST),
            (r"equal slopes: \ the search is exhaustive; \ you check every digit, \ even after a match", MEM),
            (r"odd, \ but quick: \ deciding after each comparison may cost more than finishing", GREY_A),
        ], 5.4, 23, 0.3).move_to([3.85, 0.3, 0])
        ptag = psyche_tag(r"\texttt{wm.sternberg\_rts}: \ 38 ms comparisons, \ exponential")
        with self.voiceover(
            "Sternberg's interpretation was elegant. <bookmark mark='a'/> Suppose the probe is compared with the "
            "held digits one at a time. <bookmark mark='b'/> If you stop as soon as you find a match, a yes needs, on "
            "average, only half of the comparisons, so the yes line should rise at half the slope of the no line. "
            "<bookmark mark='c'/> A no always requires checking everything. <bookmark mark='d'/> The slopes were "
            "equal, so Sternberg concluded that the search is serial and exhaustive: every digit is checked, even "
            "after a match has been found. <bookmark mark='e'/> That sounds wasteful, but at forty milliseconds a "
            "comparison, it may be cheaper to finish than to stop and decide after each one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(st), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(st_no), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(ex), FadeIn(key), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def mimicry(self):
        d = load("sternberg")
        head = heading(r"Derived: \ a parallel search that looks serial")
        A = axes([0.5, 6.5], [350, 700], x_length=5.4, y_length=3.0, xticks=[1, 2, 3, 4, 5, 6],
                 yticks=[400, 550, 700], xlabel=r"digits held", ylabel=r"mean RT, \ ms", center=[-3.6, 0.65, 0],
                 font_size=17)
        ax = A.ax
        k = d["k"]
        par = curve_in(ax, k, d["parallel_yes"], LOOP, 4)
        lim = DashedVMobject(curve_in(ax, k, d["limited_yes"], MODEL, 4), num_dashes=20)
        ser = curve_in(ax, k, d["serial_yes"], MEM, 4)
        B = axes([200, 1200], [0, 0.004], x_length=5.4, y_length=3.0, xticks=[200, 700, 1200], yticks=[],
                 xlabel=r"RT with 4 digits, \ ms", ylabel=r"share of trials", center=[3.3, 0.65, 0], font_size=17)
        hs = hist(B.ax, d["edges"], d["hist_serial"], MEM, opacity=0.45)
        hl = hist(B.ax, d["edges"], d["hist_limited"], MODEL, opacity=0.45)
        key = legend([(MEM, r"serial"), (LOOP, r"parallel, \ unlimited"), (MODEL, r"parallel, \ shared capacity")],
                     font_size=18).arrange(RIGHT, buff=0.5).move_to([0, -1.55, 0])
        eq = MathTex(r"j \text{ comparisons left, each at rate } \tfrac{1}{j\,c}: \quad "
                     r"\min \text{ of } j \text{ exponentials} \sim \text{Exp}\big(\tfrac{1}{c}\big)",
                     font_size=32, color=MODEL).move_to([0, -2.3, 0])
        rows = rows_of([
            (r"unlimited parallel: \ the slowest of $s$ comparisons; \ RT grows like $1 + \frac12 + \dots + \frac1s$, "
             r"\ curved", LOOP),
            (r"shared capacity, \ reallocated as each finishes: \ the same distribution as serial, \ exactly "
             r"\ (Townsend, \ 1972)", MODEL),
        ], 12.4, 23, 0.18).to_edge(DOWN, buff=0.7)
        ptag = psyche_tag(r"\texttt{wm.sternberg\_rts}: \ 40,000 trials a model")
        with self.voiceover(
            "There is a catch, and it is one of the deepest lessons of reaction-time modelling. "
            "<bookmark mark='a'/> Suppose instead that all the comparisons run at once, in parallel, and you answer "
            "when the slowest finishes. With unlimited capacity each comparison runs at full speed, and the time of "
            "the slowest grows like one plus a half plus a third and so on: a curve, not a line. That model is "
            "ruled out. <bookmark mark='b'/> But suppose the comparisons share a fixed capacity. With j left, each "
            "runs at one j-th of the full rate, and the first of them finishes after the minimum of j exponential "
            "times, which is exponential at the full rate. Then the freed capacity is shared among the rest. "
            "<bookmark mark='c'/> Add it up, and every stage is identical to one serial comparison. The parallel model "
            "predicts the same line, and not just the same means: the same distribution of reaction times. James "
            "Townsend proved this in 1972. A straight line, even a perfect one, cannot tell serial from parallel. "
            "Part 48 returns to models that mimic one another."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(ptag), Create(ser))
            vo.wait_until("a")
            self.play(Create(par), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(eq))
            vo.wait_until("c")
            self.play(Create(lim), FadeIn(key), FadeIn(hs), FadeIn(hl), FadeIn(rows[1]))
        self.clear_scene()
