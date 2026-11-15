from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403


class Scale(VoiceoverScene):
    def construct(self):
        self.card()
        self.mental_age()
        self.deviation()
        self.error()

    def card(self):
        card = chapter_card(6, r"The scale", r"How does a test become an IQ?",
                            lit={1905: r"Binet \& Simon", 1912: r"Stern", 1939: r"Wechsler"}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter six. The scale."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def mental_age(self):
        d = load("scale")
        head = heading(r"Mental age, \ and a quotient")
        eq = label(r"$\mathrm{IQ} = 100 \times \dfrac{\text{mental age}}{\text{chronological age}}$", font_size=36)
        eq.move_to([0, 1.5, 0])
        rows = rows_of([
            (r"Binet and Simon's scale, \ 1905, \ revised in 1908: \ tasks grouped by the age at which most children pass them; \ a child who "
             r"passes the eight-year tasks has a mental age of eight", WHITE),
            (r"William Stern, \ 1912: \ divide mental age by actual age; \ Lewis Terman's Stanford--Binet, \ 1916, "
             r"\ multiplied by 100 and called it the IQ", VERB),
            (rf"a child of 8 with a mental age of 10: \ {d['ratio_child']:.0f}", G),
            (rf"but mental age stops growing in the late teens: \ a 40-year-old ``of mental age 16'' would score "
             rf"{d['ratio_adult']:.0f}, \ which is absurd", LOST),
        ], 12.4, 24, 0.38).move_to([0, -1.1, 0])
        tag = historical_tag(r"Binet \& Simon (1905); \ Stern (1912)")
        with self.voiceover(
            "Binet's scale, in its 1908 revision, gave a child a mental age. <bookmark mark='a'/> Tasks were grouped by the age at which "
            "most children pass them, so a child who passes the eight-year tasks has a mental age of eight. "
            "<bookmark mark='b'/> In 1912 William Stern divided mental age by actual age, and Lewis Terman's "
            "Stanford-Binet of 1916 multiplied by a hundred and called it the intelligence quotient. "
            f"<bookmark mark='c'/> A child of eight with a mental age of ten scores {d['ratio_child']:.0f}. "
            "<bookmark mark='d'/> But mental age stops growing in the late teens, so the ratio fails for adults. A "
            f"forty-year-old of mental age sixteen would score {d['ratio_adult']:.0f}, which is absurd."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def deviation(self):
        head = heading(r"Wechsler's deviation IQ, \ 1939")
        A = axes([40, 160], [0, 0.03], x_length=8.0, y_length=3.0, xticks=[55, 70, 85, 100, 115, 130, 145],
                 yticks=None, xfmt=lambda v: f"{v:.0f}", xlabel=r"IQ", center=[-1.5, 0.6, 0], font_size=15)
        x = np.linspace(40, 160, 300)
        y = np.exp(-0.5 * ((x - 100) / 15) ** 2) / (15 * np.sqrt(2 * np.pi))
        c = curve(A.ax, x, y, G, stroke_width=4)
        area = VGroup()
        for lo, hi, col, op in ((85, 115, G, 0.35), (70, 85, G, 0.18), (115, 130, G, 0.18)):
            xs = np.linspace(lo, hi, 40)
            pts = [A.ax.c2p(lo, 0)] + [A.ax.c2p(v, np.exp(-0.5 * ((v - 100) / 15) ** 2) / (15 * np.sqrt(2 * np.pi)))
                                       for v in xs] + [A.ax.c2p(hi, 0)]
            area.add(Polygon(*pts, stroke_width=0, fill_color=col, fill_opacity=op))
        pcts = VGroup(label(r"68\%", font_size=18, color=G).move_to(A.ax.c2p(100, 0.011)),
                      label(r"95\% within 70--130", font_size=17, color=GREY_A).move_to(A.ax.c2p(100, 0.031)))
        rows = rows_of([
            (r"David Wechsler, \ 1939: \ compare a person only with others of the same age in a norming sample", WHITE),
            (r"$\mathrm{IQ} = 100 + 15\, z$: \ the mean of the age group is 100, \ one standard deviation is 15 "
             r"points", G),
            (r"so an IQ is a rank, \ not an amount: \ 130 means the top 2\% of one's age group, \ in the year the "
             r"test was normed \ (Part 31's old norms)", VERB),
        ], 12.4, 23, 0.36).move_to([0, -2.2, 0])
        tag = historical_tag(r"Wechsler (1939)")
        with self.voiceover(
            "The fix came from David Wechsler. <bookmark mark='a'/> In 1939 he compared each person only with "
            "others of the same age, in a norming sample. <bookmark mark='b'/> A person's IQ is a hundred plus "
            "fifteen times their z-score: the mean of the age group is a hundred, and one standard deviation is "
            "fifteen points. About sixty-eight percent of people fall between eighty-five and a hundred and fifteen, "
            "and ninety-five percent between seventy and a hundred and thirty. <bookmark mark='c'/> So an IQ is a "
            "rank, not an amount. A hundred and thirty means the top two percent of one's age group, in the year "
            "the test was normed, which is why Part 31's old norms matter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(c))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(area), FadeIn(pcts), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def error(self):
        d = load("scale")
        head = heading(r"Every score has an error bar")
        A = axes([85, 115], [-0.5, 3.0], x_length=7.0, y_length=3.0, xticks=[90, 95, 100, 105, 110], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"IQ", center=[-2.4, 1.1, 0], font_size=15)
        bars_ = VGroup()
        for i, (rel, sem) in enumerate(zip(d["rel"], d["sem"])):
            y = 2.4 - 0.9 * i
            ln = Line(A.ax.c2p(100 - 1.96 * sem, y), A.ax.c2p(100 + 1.96 * sem, y), color=G, stroke_width=6)
            bars_.add(VGroup(ln, Dot(A.ax.c2p(100, y), radius=0.07, color=WHITE),
                             label(rf"reliability {rel:.2f}: \ $\pm${1.96 * sem:.1f}", font_size=17, color=G)
                             .next_to(ln, RIGHT, buff=0.2)))
        rows = rows_of([
            (r"Part 3: \ the standard error of measurement is $15\sqrt{1 - r}$, \ with $r$ the test's reliability",
             MODEL),
            (rf"at reliability 0.95, \ about $\pm${1.96 * d['sem'][2]:.0f} points around the score, \ 95\% of the "
             rf"time; \ at 0.80, \ $\pm${1.96 * d['sem'][0]:.0f}", G),
            (r"a score of 71 and a score of 69 are not different people", WHITE),
            (r"in 2014 the US Supreme Court, \ in \emph{Hall v.\ Florida}, \ ruled that a state may not treat 70 as "
             r"a hard line without the error around it", VERB),
        ], 12.4, 23, 0.34).move_to([0, -2.4, 0])
        tag = psyche_tag(r"\texttt{traits.sem\_interval}")
        with self.voiceover(
            "And every score has an error bar. <bookmark mark='a'/> Part 3 derived the standard error of "
            "measurement: fifteen times the square root of one minus the test's reliability. "
            f"<bookmark mark='b'/> At a reliability of 0.95, the interval is about plus or minus "
            f"{1.96 * d['sem'][2]:.0f} points around the score, ninety-five percent of the time; at 0.80, plus or "
            f"minus {1.96 * d['sem'][0]:.0f}. <bookmark mark='c'/> A score of seventy-one and a score of sixty-nine "
            "are not different people. <bookmark mark='d'/> In 2014, in Hall versus Florida, the United States "
            "Supreme Court ruled that a state may not treat seventy as a hard line without considering the error "
            "around it, in a case where a man's life depended on the answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars_], lag_ratio=0.4), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
