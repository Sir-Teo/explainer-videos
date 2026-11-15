from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403

# log10(minutes) of a few landmarks, for a log-time axis
TICKS = {1.0: r"10\,\text{min}", np.log10(60): r"1\,\text{h}", np.log10(1440): r"1\,\text{d}",
         np.log10(10080): r"1\,\text{wk}", np.log10(43200): r"1\,\text{mo}"}


def _tick(v):
    for k, s in TICKS.items():
        if abs(v - k) < 1e-6:
            return s
    return ""


class Savings(VoiceoverScene):
    def construct(self):
        self.card()
        self.curve()
        self.activation()
        self.environment()

    def card(self):
        card = chapter_card(1, r"Savings and the first curve", r"How fast is a memory lost, \ and by what law?",
                            lit={1885: r"Ebbinghaus", 1991: r"Anderson \& Schooler", 1998: r"ACT-R"},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter one. Savings and the first curve."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def curve(self):
        d = load("forgetting")
        e = archive.EBBINGHAUS_1885.data
        head = heading(r"Ebbinghaus's retention table, \ with three laws fitted")
        A = axes([1, 4.8], [0, 70], x_length=7.0, y_length=4.0, xticks=sorted(TICKS), yticks=[0, 20, 40, 60],
                 xlabel=r"time since learning \ (log scale)", ylabel=r"savings", center=[-2.6, 0.2, 0], font_size=18,
                 xfmt=_tick, yfmt=lambda v: f"{v:.0f}\\%")
        ax = A.ax
        lt, ltt = np.log10(d["t"]), np.log10(d["tt"])
        pts = scatter(ax, lt, d["y"], DATA, radius=0.09, opacity=1.0)
        ce = curve_in(ax, ltt, d["ebb"], MODEL, 4)
        cp = curve_in(ax, ltt, d["pow"], WORD, 4)
        cx = curve_in(ax, ltt, d["exp"], LOST, 4)
        k, c = d["params_ebb"]
        a, b = d["params_pow"]
        a2, tau = d["params_exp"]
        sse = d["sse"]
        eqs = VGroup(
            MathTex(rf"b = \frac{{100\,k}}{{(\log_{{10}} t)^c + k}}", font_size=30, color=MODEL),
            MathTex(rf"b = a\,t^{{-\beta}}", font_size=30, color=WORD),
            MathTex(rf"b = a\,e^{{-t/\tau}}", font_size=30, color=LOST),
        )
        fits = VGroup(
            label(rf"$k = {k:.2f}, \ c = {c:.2f}$: \ residual SS {sse[0]:.0f}", font_size=20, color=MODEL),
            label(rf"$a = {a:.0f}, \ \beta = {b:.3f}$: \ residual SS {sse[1]:.0f}", font_size=20, color=WORD),
            label(rf"$\tau = {tau / 1440:.1f}$ days: \ residual SS {sse[2]:.0f}", font_size=20, color=LOST),
        )
        block = VGroup(*[VGroup(q, f).arrange(DOWN, aligned_edge=LEFT, buff=0.12) for q, f in zip(eqs, fits)])
        block.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.3, 0.6, 0])
        note = rows_of([
            (rf"his own formula: \ $k = {e['k']}$, \ $c = {e['c']}$; \ refitted here, \ "
             rf"$k = {k:.2f}$, \ $c = {c:.2f}$", MODEL),
            (r"the loss is fast, \ then slow: \ on a log scale of time it is nearly a straight line", WORD),
            (r"an exponential, \ which loses a fixed share per hour, \ cannot bend both ways", LOST),
        ], 12.6, 23, 0.2).to_edge(DOWN, buff=0.6)
        tag = historical_tag(archive.EBBINGHAUS_1885.cite)
        ptag = psyche_tag(r"\texttt{memory.fit\_forgetting}: \ least squares")
        with self.voiceover(
            "Here are Ebbinghaus's seven numbers, the savings after twenty minutes, an hour, nine hours, a day, two "
            "days, six days and a month, plotted against time on a logarithmic scale. <bookmark mark='a'/> After "
            f"twenty minutes he saved {e['saving'][0]:.0f} percent of the work, after an hour only "
            f"{e['saving'][1]:.0f}; by a month {e['saving'][-1]:.0f} percent remained, and that remainder was "
            "going very slowly. <bookmark mark='b'/> Ebbinghaus fitted his "
            "own formula, in which savings fall with a power of the logarithm of time. Refitted by least squares "
            f"its two constants come out close to his, {k:.2f} and {c:.2f}. <bookmark mark='c'/> A plain power law, "
            "savings proportional to time raised to a small negative power, does nearly as well with two constants "
            "of its own. <bookmark mark='d'/> An exponential, which loses the same share of what's left in every "
            "hour, cannot. It has to choose between the fast early loss and the slow late one, and gets both "
            "wrong. <bookmark mark='e'/> That shape, fast and then ever slower, is the first law of memory, and it "
            "has been found again and again, most recently by Jaap Murre's own replication of Ebbinghaus in 2015. "
            "Part 21 looks at why the curve has that shape."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(ptag))
            self.play(FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(note[0]))
            vo.wait_until("b")
            self.play(Create(ce), FadeIn(block[0]))
            vo.wait_until("c")
            self.play(Create(cp), FadeIn(block[1]))
            vo.wait_until("d")
            self.play(Create(cx), FadeIn(block[2]), FadeIn(note[2]))
            vo.wait_until("e")
            self.play(FadeIn(note[1]))
        self.clear_scene()

    def activation(self):
        d = load("forgetting")
        head = heading(r"ACT-R: \ a memory's activation is the sum of its past uses")
        eq = MathTex(r"B", r"=", r"\ln \sum_{j=1}^{n} t_j^{-d}", r"\qquad", r"P(\text{recall}) = "
                     r"\frac{1}{1 + e^{-(B - \theta)/s}}", font_size=40).move_to([0, 2.15, 0])
        eq[0].set_color(MODEL)
        eq[4].set_color(WORD)
        A = axes([0, 60], [0, 1], x_length=6.4, y_length=3.0, xticks=[0, 15, 30, 45, 60], yticks=[0, 0.5, 1],
                 xlabel=r"days since the last use", ylabel=r"probability of recall", center=[-2.7, -1.0, 0],
                 font_size=18, yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        cs = VGroup(*[curve_in(ax, d["days"], d[k], col, 4) for k, col in
                      (("act1", LOST), ("act3", WORD), ("act10", MODEL))])
        key = legend([(LOST, r"used once"), (WORD, r"used 3 times"), (MODEL, r"used 10 times")],
                     font_size=19)
        key.move_to(ax.c2p(46, 0.6))
        rows = rows_of([
            (r"each use $j$, \ $t_j$ ago, \ adds a trace that fades as a power of its age, \ $d = 0.5$", MODEL),
            (r"practice adds traces; \ time shrinks them: \ the power law falls out of the sum", WORD),
            (r"recall is a threshold on activation, \ blurred by noise", GREY_A),
        ], 5.2, 22, 0.28).move_to([4.3, -1.55, 0])
        ptag = psyche_tag(r"\texttt{memory.actr\_activation}: \ time in hours, \ $d = 0.5$, \ $\theta = -2$, \ "
                          r"$s = 0.5$; \ uses spread over two days")
        with self.voiceover(
            "Ebbinghaus's curve has a modern descendant inside a whole theory of the mind. "
            "<bookmark mark='a'/> In ACT-R, John Anderson's cognitive architecture, every memory has an activation. "
            "Each time the memory was used, it left a trace, and each trace fades as a power of its age. The "
            "activation is the logarithm of the sum of the traces. <bookmark mark='b'/> The probability of recall is "
            "a threshold on activation, softened by noise. <bookmark mark='c'/> A fact used once fades within days. "
            "Used three times it lasts longer, and used ten times longer still, and the same equation gives both "
            "the practice curve and the forgetting curve. <bookmark mark='d'/> The power law of forgetting isn't "
            "put in by hand here. It comes from summing traces that each fade as a power of their age."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq[:3]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eq[3:]), FadeIn(rows[2]), FadeIn(ptag))
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(key))
            self.play(LaggedStart(*[Create(c) for c in cs], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def environment(self):
        head = heading(r"Why would memory fade like that?")
        rows = rows_of([
            (r"Anderson and Schooler, \ 1991: \ look at the world, \ not the mind", WHITE),
            (r"the chance that a word appears in a \emph{New York Times} headline tomorrow, \ against the days since "
             r"it last did", CUE),
            (r"the same for the words in parents' speech to children, \ and for the senders of one researcher's email",
             CUE),
            (r"in every case, \ the odds of being needed fall as a power of the time since the last use", WORD),
            (r"so a memory that fades like the odds of its being needed is not failing: \ it is keeping the right "
             r"things ready", MODEL),
            (r"the rational analysis of memory: \ ask what problem memory solves, \ then how well", GREY_A),
        ], 12.4, 27, 0.36).move_to([0, -0.3, 0])
        tag = published_tag(r"Anderson \& Schooler (1991)")
        with self.voiceover(
            "Why should memory fade as a power of time, rather than any other way? <bookmark mark='a'/> In 1991 "
            "Anderson and Lael Schooler looked for the answer outside the head. <bookmark mark='b'/> They took the "
            "headlines of the New York Times and asked, for each word, how likely it was to appear tomorrow, given "
            "how many days ago it had last appeared. <bookmark mark='c'/> They did the same for the words parents "
            "say to young children, and for the senders of the email one researcher received. <bookmark mark='d'/> In all "
            "three, the odds that an item will be needed fall as a power of the time since it was last needed. "
            "<bookmark mark='e'/> So a memory that fades like a power law is matched to the world it serves. "
            "Forgetting is not simply failure: it keeps ready the things most likely to be wanted. "
            "<bookmark mark='f'/> Anderson called this the rational analysis of memory. Ask first what problem "
            "memory is solving, and then how well it solves it. We'll meet the same style of argument again, in "
            "vision and in decision making."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
