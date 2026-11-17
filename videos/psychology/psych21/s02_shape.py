from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403

WHO = (("ebbinghaus", r"Ebbinghaus, \ 1885", TRACE), ("mack", r"Mack, \ 1991", CUE), ("seitz", r"Seitz, \ 1991", CTX),
       ("dros", r"Dros, \ 2015", FALSE))
LAW_TEX = {
    "power": (r"S = a\,t^{-b}", r"power"),
    "exponential": (r"S = a\,e^{-t/\tau}", r"exponential"),
    "log": (r"S = a - b \ln t", r"logarithmic \ (Ebbinghaus's own)"),
    "wickelgren": (r"S = \lambda (1 + \beta t)^{-\psi}", r"Wickelgren's"),
}
LAW_COL = {"power": MODEL, "exponential": LOST, "log": CUE, "wickelgren": CTX}
SHORT = {"power": "pow.", "exponential": "exp.", "log": "log", "wickelgren": "Wick."}
TICKS = {np.log10(20): r"20\,\text{min}", np.log10(60): r"1\,\text{h}", np.log10(526): r"9\,\text{h}",
         np.log10(1440): r"1\,\text{d}", np.log10(8640): r"6\,\text{d}", np.log10(44640): r"31\,\text{d}"}


def time_axes(center, x_length=7.0, y_length=3.6, font_size=18, ymax=0.6):
    return axes([np.log10(15), np.log10(60000)], [0, ymax], x_length=x_length, y_length=y_length,
                xticks=list(TICKS), yticks=[0, 0.2, 0.4, 0.6][: int(round(ymax / 0.2)) + 1],
                xfmt=lambda v: TICKS[min(TICKS, key=lambda k: abs(k - v))], yfmt=lambda v: f"{100 * v:.0f}\\%",
                xlabel=r"time since learning", ylabel=r"savings", center=center, font_size=font_size)


class Shape(VoiceoverScene):
    def construct(self):
        self.card()
        self.replications()
        self.laws()
        self.jost()
        self.averaging()

    def card(self):
        card = chapter_card(1, r"The shape of forgetting", r"What law does forgetting follow?",
                            lit={1885: r"Ebbinghaus", 1897: r"Jost", 1991: r"Wixted \& Ebbesen",
                                 2015: r"Murre \& Dros"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter one. The shape of forgetting."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def replications(self):
        d = load("laws")
        s = archive.SAVINGS_REPLICATIONS.data
        head = heading(r"One curve, \ four people, \ 130 years")
        A = time_axes([-1.7, -0.25, 0], x_length=8.2, y_length=4.4)
        x = np.log10(d["t"])
        pts = VGroup()
        lines = VGroup()
        for who, _, col in WHO:
            lines.add(curve(A.ax, x, d[who], col, stroke_width=2))
            pts.add(scatter(A.ax, x, d[who], col, radius=0.07, opacity=1.0))
        key = legend([(col, name) for _, name, col in WHO], font_size=22).move_to([4.6, 1.0, 0])
        rows = rows_of([
            (rf"Jaap Dros, \ 2015: \ {s['dros_hours']} hours of learning syllable lists, \ "
             r"Ebbinghaus's method to the letter", FALSE),
            (r"the same shape every time: \ fast at first, \ then slower and slower", WHITE),
            (r"not quite smooth: \ at one day the curves rise or pause, \ after the first night's sleep", CTX),
        ], 4.1, 21, 0.3).move_to([4.75, -1.4, 0])
        tag = historical_tag(archive.SAVINGS_REPLICATIONS.cite)
        with self.voiceover(
            "In the last part we met Ebbinghaus's curve. Is it a fact about memory, or a fact about Ebbinghaus? "
            "<bookmark mark='a'/> It has been checked. In 1991 a German study by Otto Heller and colleagues repeated "
            "the experiment with two subjects, Mack and Seitz. And in 2015 Jaap Murre and his student Joeri Dros "
            "did it again in Amsterdam: Dros spent about seventy hours learning and relearning lists of nonsense "
            "syllables, at Ebbinghaus's seven intervals, from twenty minutes to a month. <bookmark mark='b'/> Here "
            "are all four. The levels differ a little; the shape does not. Forgetting is fast at first, then "
            "slower, and slower again. <bookmark mark='c'/> And the curves are not quite smooth. Between nine hours "
            "and a day, where they should keep falling, two of them rise and the others pause. A day is the first "
            "interval with a night's sleep in it. That irregularity in Ebbinghaus's table is what led John Jenkins "
            "and Karl Dallenbach to study sleep and forgetting in 1924, and Murre and Dros's fits find a jump at a "
            "day. Whether sleep causes it, they say, this kind of experiment has yet to show. We'll come back to "
            "sleep."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(key[3]), Create(lines[3]), FadeIn(pts[3]))
            vo.wait_until("b")
            self.play(*[Create(lines[i]) for i in range(3)], *[FadeIn(pts[i]) for i in range(3)],
                      *[FadeIn(key[i]) for i in range(3)], FadeIn(rows[1]))
            vo.wait_until("c")
            k = list(np.log10(d["t"]))
            box = Rectangle(width=abs(A.ax.c2p(k[4], 0)[0] - A.ax.c2p(k[1], 0)[0]) + 0.3,
                            height=abs(A.ax.c2p(0, 0.45)[1] - A.ax.c2p(0, 0.18)[1]), color=CTX, stroke_width=2)
            box.move_to(A.ax.c2p((k[2] + k[3]) / 2, 0.315))
            self.play(Create(box), FadeIn(rows[2]))
        self.clear_scene()

    def laws(self):
        d = load("laws")
        names = [str(n) for n in d["names"]]
        head = heading(r"Four laws, \ fitted")
        A = time_axes([-3.0, 0.1, 0], x_length=6.8, y_length=3.9)
        x = np.log10(d["t"])
        xx = np.log10(d["tt"])
        pts = scatter(A.ax, x, d["ebbinghaus"], TRACE, radius=0.08, opacity=1.0)
        cs = VGroup(*[curve_in(A.ax, xx, d[f"ebbinghaus_{n}"], LAW_COL[n], 3) for n in names])
        eqs = VGroup(*[VGroup(MathTex(LAW_TEX[n][0], font_size=30, color=LAW_COL[n]),
                              label(LAW_TEX[n][1], font_size=20, color=GREY_A)).arrange(DOWN, buff=0.08,
                                                                                         aligned_edge=LEFT)
                       for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.2, 1.0, 0])
        # AIC table: rows = people, columns = laws, the best in each row marked
        hdr = VGroup(label(r"AIC", font_size=20, color=GREY_B),
                     *[label(SHORT[n], font_size=20, color=LAW_COL[n]) for n in names])
        table = VGroup(hdr)
        best = []
        for who, name, col in WHO:
            a = d[who + "_aic"]
            best.append(names[int(np.argmin(a))])
            table.add(VGroup(label(name.split(",")[0], font_size=20, color=col),
                             *[label(f"{v:.0f}", font_size=20, color=WHITE if v == a.min() else GREY_C)
                               for v in a]))
        for r in table:
            for j, cell in enumerate(r):
                cell.move_to([2.2 + (0 if j == 0 else 0.55 + 0.9 * j), 0, 0])
        table.arrange(DOWN, buff=0.15).move_to([4.4, -2.2, 0])
        for r in table:
            for j, cell in enumerate(r):
                cell.set_x(2.3 + (0 if j == 0 else 0.45 + 0.8 * j))
        winners = {n: best.count(n) for n in names}
        assert winners == {"power": 3, "exponential": 0, "log": 1, "wickelgren": 0}, winners  # the narration says so
        note = label(r"lower is better; \ Wickelgren's law has a third parameter", font_size=19,
                     color=GREY_B).next_to(table, DOWN, buff=0.15)
        note.set_x(table.get_x())
        ptag = psyche_tag(r"\texttt{memory.fit\_law}: \ least squares, \ AIC")
        pw = d["ebbinghaus_power_params"]
        with self.voiceover(
            "What law is it? Four have been proposed. <bookmark mark='a'/> A power function, a times t to the minus "
            "b. An exponential, the law of radioactive decay. A logarithm, which is what Ebbinghaus himself "
            "fitted. And Wickelgren's, a power function with one more parameter that keeps it finite at time zero. "
            "<bookmark mark='b'/> Fitted to Ebbinghaus's seven points, the exponential is plainly wrong: it can't "
            "fall fast and then flatten. The other three are hard to tell apart by eye. "
            "<bookmark mark='c'/> So compare them by Akaike's criterion, which charges for parameters. The power "
            "law wins for three of the four people, the logarithm for Dros, whose last point falls steeply, and the "
            "exponential for none. "
            "<bookmark mark='d'/> With seven points each, that's not a verdict, and the reason the power law is "
            "believed is larger datasets: John Wixted and Ebbe Ebbesen in 1991, and many since, found power-like "
            "forgetting across materials, measures and species."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(pts), FadeIn(ptag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(e, shift=LEFT * 0.1) for e in eqs], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in cs], lag_ratio=0.3), run_time=3.0)
            self.play(Indicate(eqs[names.index("exponential")], color=LOST))
            vo.wait_until("c")
            self.play(eqs.animate.scale(0.8).move_to([4.4, 1.6, 0]))
            self.play(FadeIn(table), FadeIn(note))
            vo.wait_until("d")
            self.play(Indicate(eqs[names.index("power")], color=MODEL))
        self.clear_scene()
        _ = pw

    def jost(self):
        j = load("jost")
        head = heading(r"Jost's law: \ of two equal memories, \ the older lasts longer")
        A = axes([0, 20000], [0, 0.5], x_length=6.2, y_length=3.2, xticks=[0, 10080, 20160],
                 yticks=[0, 0.25, 0.5], xfmt=lambda v: {0: "0", 10080: r"1\,\text{wk}", 20160: r"2\,\text{wk}"}
                 .get(int(v), ""), yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"from now", ylabel=r"strength",
                 center=[-3.5, -0.2, 0], font_size=18)
        B = axes([0, 20000], [0, 0.5], x_length=6.2, y_length=3.2, xticks=[0, 10080, 20160],
                 yticks=[0, 0.25, 0.5], xfmt=lambda v: {0: "0", 10080: r"1\,\text{wk}", 20160: r"2\,\text{wk}"}
                 .get(int(v), ""), yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"from now", ylabel=r"strength",
                 center=[3.5, -0.2, 0], font_size=18)
        h = j["h"]
        g = VGroup(curve(A.ax, h, j["power_young"], TRACE, 4), curve(A.ax, h, j["power_old"], CTX, 4),
                   curve(B.ax, h, j["exp_young"], TRACE, 4), DashedVMobject(curve(B.ax, h, j["exp_old"], CTX, 4),
                                                                            num_dashes=40))
        tA = label(r"power law", font_size=24, color=MODEL).next_to(A, UP, buff=0.1)
        tB = label(r"exponential", font_size=24, color=LOST).next_to(B, UP, buff=0.1)
        key = legend([(TRACE, r"learnt an hour ago"), (CTX, r"learnt two days ago, \ just as strong now")],
                     font_size=20).arrange(RIGHT, buff=0.6).move_to([0, 2.65, 0])
        eqs = VGroup(MathTex(r"-\frac{d \ln S}{dt} = \frac{b}{t}", font_size=34, color=MODEL),
                     MathTex(r"-\frac{d \ln S}{dt} = \frac{1}{\tau}", font_size=34, color=LOST))
        eqs[0].move_to(A.ax.c2p(13000, 0.1))
        eqs[1].move_to(B.ax.c2p(13000, 0.1))
        rows = rows_of([
            (r"the rate of loss of a power-law memory falls with its age: \ an old memory is a survivor", MODEL),
            (r"an exponential has no memory of its age: \ two equal traces fade alike, \ which Jost's law denies",
             LOST),
        ], 12.6, 22, 0.15).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "There's a deeper reason to prefer the power law, found by Adolf Jost in 1897. "
            "<bookmark mark='a'/> Take two memories that are equally strong right now, one learnt an hour ago and "
            "one learnt two days ago and since refreshed to the same strength. Which will you still have next week? "
            "Jost's law says the older one. <bookmark mark='b'/> Under the power law, that's what happens. The rate "
            "at which a memory is lost, the slope of the log of its strength, is b over t: it falls as the memory "
            "ages. A memory that has lasted is one that will last. <bookmark mark='c'/> An exponential can't do "
            "this. Its rate of loss is constant, one over tau, whatever the memory's age, so the two memories fade "
            "identically, the dashed line on top of the solid one. Forgetting is not radioactive decay. "
            "<bookmark mark='d'/> Jost's law is one reason the power law isn't just a good fit but a good idea: it "
            "says the memory system treats age as evidence of need, the argument of Anderson and Schooler from the "
            "last part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(tA), FadeIn(tB), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(g[0]), Create(g[2]))
            vo.wait_until("b")
            self.play(Create(g[1]), Write(eqs[0]), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(g[3]), Write(eqs[1]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Indicate(tA, color=MODEL))
        self.clear_scene()

    def averaging(self):
        m = load("mixture")
        head = heading(r"Derivation: \ a power law from exponentials")
        A = axes([0, 30], [0, 1], x_length=6.0, y_length=3.2, xticks=[0, 10, 20, 30], yticks=[0, 0.5, 1],
                 xlabel=r"time", ylabel=r"retained", center=[-3.6, 0.2, 0], font_size=18)
        t = m["t"]
        each = VGroup(*[curve(A.ax, t, e, GREY_B, 1.5) for e in m["each"]])
        avg = curve(A.ax, t, m["average"], TRACE, 5)
        pw = DashedVMobject(curve(A.ax, t, m["power"], MODEL, 3), num_dashes=40)
        eq = MathTex(r"\int_0^\infty e^{-\lambda t}\, \frac{\lambda^{k-1} e^{-\lambda/\theta}}{\Gamma(k)\,\theta^k}"
                     r"\, d\lambda", r"=", r"(1 + \theta t)^{-k}", font_size=34).move_to([3.4, 1.2, 0])
        eq[2].set_color(MODEL)
        rows = rows_of([
            (r"let each memory fade exponentially, \ each at its own rate $\lambda$", GREY_A),
            (rf"if the rates vary as a gamma distribution, \ shape $k = {m['shape']:g}$, \ the average of the "
             r"exponentials is exactly a power function", TRACE),
            (r"so a power law in averaged data does not show that any one memory follows it \ "
             r"(Anderson and Tweney, \ 1997)", LOST),
            (r"but Ebbinghaus's curve is one person's: \ the averaging is over syllables, \ and the argument still "
             r"applies", CUE),
        ], 6.4, 21, 0.25).move_to([3.4, -1.45, 0])
        ptag = psyche_tag(r"\texttt{memory.gamma\_mixture}: \ 20{,}000 exponentials averaged")
        with self.voiceover(
            "But here's a warning that every model fitter should know. <bookmark mark='a'/> Suppose every single "
            "memory fades exponentially, but each at its own rate, lambda: some fast, some slow. "
            "<bookmark mark='b'/> Average them, and the average is not an exponential. If the rates follow a "
            "gamma distribution, the integral can be done exactly, and it's one plus theta t, to the power minus "
            "k: a power function, Wickelgren's form. Twenty thousand exponentials, averaged, sit right on the "
            "dashed curve. <bookmark mark='c'/> So a power law in averaged data does not show that any single memory "
            "obeys it. Richard Anderson and Ryan Tweney made this point in 1997. <bookmark mark='d'/> And it applies "
            "even to Ebbinghaus, one person, because his savings are averaged over syllables and lists. The shape of "
            "the curve is a fact. What it says about one memory is a question for the models of the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e in each], lag_ratio=0.1), run_time=2.5)
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(rows[1]))
            self.play(Create(avg), Create(pw), FadeIn(ptag))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
