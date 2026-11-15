from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403

NAMES = {"slots": r"slots", "averaging": r"slots + averaging", "equal": r"equal precision",
         "variable": r"variable precision"}
COLS = {"slots": SLOT, "averaging": EXEC, "equal": LOOP, "variable": MODEL}
MODELS = ("slots", "averaging", "equal", "variable")


def deg(x):
    return float(np.degrees(x))


class Precision(VoiceoverScene):
    def construct(self):
        self.card()
        self.task()
        self.errors()
        self.mixture()
        self.swaps()
        self.models()
        self.verdict()
        self.mimic()

    def card(self):
        card = chapter_card(7, r"Slots or resources", r"Is the limit a number of things, \ or a quantity of precision?",
                            lit={2008: r"Zhang \& Luck; \ Bays \& Husain", 2012: r"van den Berg et al."}, part=PART,
                            scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter seven. Slots or resources."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def task(self):
        b = load("bays")
        head = heading(r"Continuous report: \ not whether, \ but how well")
        w = wheel(1.25, 0.26).move_to([-3.6, 0.6, 0])
        locs = [(-0.45, 0.45), (0.45, 0.45), (-0.45, -0.45), (0.45, -0.45)]
        cols = [0.4, 2.2, 3.9, 5.3]
        items = VGroup(*[Square(0.34, stroke_width=0, fill_color=hue(a), fill_opacity=1).move_to(
            w.get_center() + np.array([x, y, 0])) for (x, y), a in zip(locs, cols)])
        probe = Square(0.34, stroke_color=WHITE, stroke_width=3, fill_opacity=0).move_to(items[1])
        target = Dot(w.get_center() + 1.12 * np.array([np.cos(cols[1]), np.sin(cols[1]), 0]), radius=0.09, color=WHITE)
        resp_a = cols[1] + 0.45
        resp = Dot(w.get_center() + 1.12 * np.array([np.cos(resp_a), np.sin(resp_a), 0]), radius=0.09, color=MEM)
        arc = Arc(radius=1.55, start_angle=cols[1], angle=0.45, color=MEM, stroke_width=4).move_arc_center_to(
            w.get_center())
        el = label(r"error", font_size=20, color=MEM).next_to(arc, UL, buff=0.05)
        rows = rows_of([
            (r"a few coloured squares, \ a delay, \ then one location is marked", WHITE),
            (r"click its colour on a wheel: \ the error is an angle, \ from $-180^\circ$ to $180^\circ$", MEM),
            (rf"open data: \ Bays, \ Catalao and Husain, \ 2009: \ {b['observers']} observers, \ "
             rf"{num(b['trials'])} trials, \ 1, \ 2, \ 4 or 6 squares", DATA),
            (r"shared by its first author on the Open Science Framework; \ every fit below is to these trials", GREY_A),
        ], 6.4, 24, 0.34).move_to([3.0, 0.4, 0])
        tag = published_tag(archive.BAYS_2009.cite)
        with self.voiceover(
            "Change detection asks whether you remember an item. In 2004 Patrick Wilken and Wei Ji Ma, and then many "
            "others, asked how well. <bookmark mark='a'/> Show a few coloured squares, take them away, then mark one "
            "of the locations. <bookmark mark='b'/> The observer clicks the colour they remember on a wheel, and the "
            "error is an angle: zero for perfect, a hundred and eighty degrees for the opposite colour. Every trial "
            "gives a number, not a yes or no. <bookmark mark='c'/> We'll use one dataset throughout: Paul Bays, Raquel "
            f"Catalao and Masud Husain's experiment from 2009, {b['observers']} observers and {b['trials']} trials, "
            "with one, two, four or six squares. <bookmark mark='d'/> Bays has shared the trial-by-trial data "
            "openly, and every model in this chapter is fitted to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(items))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(probe))
            vo.wait_until("b")
            self.play(FadeIn(w), FadeIn(target), FadeIn(rows[1]))
            self.play(FadeIn(resp), Create(arc), FadeIn(el))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def _panels(self, b, center_y=0.5, fits=None, font_size=16):
        panels = VGroup()
        for i, n in enumerate(b["set_sizes"]):
            A = axes([-np.pi, np.pi], [0, 1.6], x_length=2.9, y_length=2.4, xticks=[-np.pi, 0, np.pi], yticks=[],
                     xfmt=lambda v: {-180: r"-180^\circ", 0: r"0^\circ", 180: r"180^\circ"}[round(np.degrees(v))],
                     xlabel=r"error", center=[-5.0 + 3.35 * i, center_y, 0], font_size=font_size)
            h = hist(A.ax, b["edges"], np.minimum(b[f"hist_{int(n)}"], 1.6), LOOP, opacity=0.6)
            t = label(rf"{int(n)} square{'s' if n > 1 else ''}", font_size=22, color=WHITE).next_to(A, UP, buff=0.12)
            panels.add(VGroup(A, h, t))
        return panels

    def errors(self):
        b = load("bays")
        head = heading(r"The errors spread as more is held")
        panels = self._panels(b, 0.9)
        sds = [deg(np.mean(b[f"sd_{int(n)}"])) for n in b["set_sizes"]]
        sl = VGroup(*[label(rf"spread {s:.0f}$^\circ$", font_size=20, color=MEM).next_to(p[0], DOWN, buff=0.15)
                      for p, s in zip(panels, sds)])
        rows = rows_of([
            (r"one square: \ a narrow peak at zero; \ six: \ a low hump on a wide base", WHITE),
            (r"a slot model reads the base as guessing: \ items that were never stored", SLOT),
            (r"a resource model reads the whole shape as one item's memory, \ spread thin", LOOP),
            (r"both can be written down exactly, \ and fitted", MEM),
        ], 12.4, 25, 0.24).to_edge(DOWN, buff=0.8)
        tag = published_tag(archive.BAYS_2009.cite)
        with self.voiceover(
            "Here are the errors, pooled over observers. <bookmark mark='a'/> With one square, a narrow peak at zero: "
            f"a circular spread of about {sds[0]:.0f} degrees. With two, {sds[1]:.0f}; with four, {sds[2]:.0f}; with "
            f"six, {sds[3]:.0f}, a low hump on a wide base. <bookmark mark='b'/> There are two ways to read the six. A "
            "slot model says the hump is the items that got a slot and the flat base is guessing, for the items that "
            "didn't. <bookmark mark='c'/> A resource model says there are no guesses at all: a fixed resource is "
            "spread over six items, each is remembered imprecisely, and imprecision can be very large. "
            "<bookmark mark='d'/> Both ideas can be written down as probability distributions and fitted to every "
            "trial. That's how the argument has been fought."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(p[0]) for p in panels], *[FadeIn(p[2]) for p in panels])
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(p[1]), FadeIn(s)) for p, s in zip(panels, sl)],
                                  lag_ratio=0.6), FadeIn(rows[0]), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def mixture(self):
        b = load("bays")
        head = heading(r"The mixture model: \ a description")
        eq = MathTex(r"p(\varepsilon) = (1 - g)\,\text{VM}(\varepsilon;\, 0, \kappa) + g\,\tfrac{1}{2\pi}",
                     font_size=40).move_to([0, 2.35, 0])
        eq[0][7:20].set_color(MEM)
        n = b["set_sizes"]
        g = np.array([b[f"mix_{int(k)}"][0] for k in n])
        sd = np.degrees([b[f"mix_{int(k)}"][1] for k in n])
        A = axes([0, 7], [0, 0.6], x_length=4.8, y_length=2.3, xticks=[1, 2, 4, 6], yticks=[0, 0.3, 0.6],
                 xlabel=r"squares", ylabel=r"guess rate $g$", center=[-3.6, 0.3, 0], font_size=17)
        B = axes([0, 7], [0, 40], x_length=4.8, y_length=2.3, xticks=[1, 2, 4, 6], yticks=[0, 20, 40],
                 xlabel=r"squares", ylabel=r"s.d. of remembered items, \ degrees", center=[2.6, 0.3, 0],
                 font_size=17)
        gc = VGroup(curve_in(A.ax, n, g, LOST, 4), scatter(A.ax, n, g, LOST, 0.07))
        sc = VGroup(curve_in(B.ax, n, sd, MEM, 4), scatter(B.ax, n, sd, MEM, 0.07))
        rows = rows_of([
            (r"Zhang and Luck, \ 2008: \ a von Mises bump for stored items, \ a flat floor for guesses", WHITE),
            (rf"fitted here: \ $g$ = {g[0]:.2f}, \ {g[1]:.2f}, \ {g[2]:.2f}, \ {g[3]:.2f}; \ "
             rf"s.d. = {sd[0]:.0f}, \ {sd[1]:.0f}, \ {sd[2]:.0f}, \ {sd[3]:.0f} degrees", DATA),
            (r"the s.d. rises up to four squares, \ then levels off: \ the shape slots predict, \ with spare slots "
             r"averaged below capacity", SLOT),
            (rf"and $N(1 - g)$, \ the number stored, \ comes out near {6 * (1 - g[3]):.1f} at six: \ a capacity of "
             r"about three", MEM),
        ], 12.4, 24, 0.22).to_edge(DOWN, buff=0.75)
        ptag = psyche_tag(r"\texttt{wm.fit\_mixture}: \ maximum likelihood, \ pooled over observers")
        tag = published_tag(archive.ZHANG_LUCK_2008.cite)
        with self.voiceover(
            "The first tool is a description, not a theory. <bookmark mark='a'/> Weiwei Zhang and Steven Luck, in "
            "2008, fitted each set size with a mixture: with probability one minus g, a von Mises distribution, the "
            "circular cousin of the normal, centred on the true colour; with probability g, a flat floor of guesses. "
            "<bookmark mark='b'/> Fitted by maximum likelihood to the Bays data, the guess rate is "
            f"{g[0]:.2f}, {g[1]:.2f}, {g[2]:.2f} and {g[3]:.2f}, and the spread of the remembered items is "
            f"{sd[0]:.0f}, {sd[1]:.0f}, {sd[2]:.0f} and {sd[3]:.0f} degrees. <bookmark mark='c'/> Read as slots, "
            "this is a tidy picture. The spread grows from one square to four and then stops: once the items "
            "outnumber the slots, each stored item has one slot and a fixed precision. Below capacity, spare slots "
            "can hold extra copies of the same item and average them, which is Zhang and Luck's slots-plus-averaging "
            "model. <bookmark mark='d'/> And the number of items stored, N times one minus g, comes out near "
            f"{6 * (1 - g[3]):.1f} with six squares: a capacity of about three. It all looks like slots. Hold that "
            "thought."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Indicate(eq, color=MEM, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(B), Create(gc), Create(sc), FadeIn(rows[1]), FadeIn(ptag), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def swaps(self):
        b = load("bays")
        head = heading(r"Some guesses are not guesses")
        n = b["set_sizes"]
        sw = np.array([b[f"swap_{int(k)}"] for k in n])
        A = axes([0, 7], [0, 0.4], x_length=6.0, y_length=3.2, xticks=[1, 2, 4, 6], yticks=[0, 0.2, 0.4],
                 xlabel=r"squares", ylabel=r"share of responses", center=[-2.8, 0.45, 0], font_size=18)
        ax = A.ax
        pn = VGroup(curve_in(ax, n, sw[:, 1], SLOT, 4), scatter(ax, n, sw[:, 1], SLOT, 0.07))
        pu = VGroup(curve_in(ax, n, sw[:, 2], GREY_B, 4), scatter(ax, n, sw[:, 2], GREY_B, 0.07))
        key = legend([(SLOT, r"around another square's colour: \ swaps"), (GREY_B, r"uniform: \ true guesses")],
                     font_size=19).next_to(A, DOWN, buff=0.3)
        rows = rows_of([
            (r"Bays, \ Catalao and Husain: \ add a third component, \ responses centred on the other squares' colours",
             WHITE),
            (r"right colour, \ wrong place: \ a failure of binding, \ not of storage", SLOT),
            (rf"fitted here, \ with six squares: \ {pct(sw[3, 1])} swaps, \ {pct(sw[3, 2])} uniform", DATA),
            (r"part of what looked like forgetting is confusion", GREY_A),
        ], 5.4, 23, 0.32).move_to([3.85, 0.3, 0])
        ptag = psyche_tag(r"\texttt{wm.fit\_swap}: \ maximum likelihood, \ pooled")
        tag = published_tag(archive.BAYS_2009.cite)
        with self.voiceover(
            "Bays and his colleagues noticed something about the guesses. <bookmark mark='a'/> Many of them weren't "
            "random. They landed near the colour of one of the other squares. So they added a third component to the "
            "mixture, centred on the non-target colours. <bookmark mark='b'/> These are swaps: the right colour, "
            "reported for the wrong place. Not a failure of storage, but of binding colour to location, the problem "
            f"from the last part. <bookmark mark='c'/> Fitted to these data, with six squares about {pct(sw[3, 1])} "
            f"of responses are swaps and about {pct(sw[3, 2])} are uniform. <bookmark mark='d'/> Some of what the "
            "two-component mixture called forgetting is confusion."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(ptag))
            vo.wait_until("b")
            self.play(Create(pn), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(pu), FadeIn(key), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def models(self):
        head = heading(r"Four process models, \ one likelihood each")
        cards = VGroup()
        texts = {
            "slots": (r"$K$ slots: \ an item is stored with probability $\min(1, K/N)$, \ precision $J$; \ else a "
                      r"guess", r"$K, \ J$"),
            "averaging": (r"$K$ slots shared out: \ an item with $s$ slots has precision $s\,J$; \ extra items "
                          r"guessed", r"$K, \ J$"),
            "equal": (r"no slots: \ every item stored, \ precision $J_1 N^{-\alpha}$", r"$J_1, \ \alpha$"),
            "variable": (r"no slots: \ precision itself varies, \ gamma with mean $J_1 N^{-\alpha}$ and scale $\tau$",
                         r"$J_1, \ \alpha, \ \tau$"),
        }
        for mo in MODELS:
            t, ps = texts[mo]
            name = label(NAMES[mo], font_size=26, color=COLS[mo])
            body = wrapped_label(t, 5.6, 21, GREY_A)
            par = label(rf"parameters: \ {ps}", font_size=20, color=COLS[mo])
            inner = VGroup(name, body, par).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            box = RoundedRectangle(width=6.2, height=inner.height + 0.4, corner_radius=0.12, stroke_color=COLS[mo],
                                   stroke_width=2, fill_color="#05070B", fill_opacity=1)
            inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
            cards.add(VGroup(box, inner))
        cards.arrange_in_grid(2, 2, buff=(0.35, 0.3)).move_to([0, 0.75, 0])
        J = MathTex(r"J = \kappa\,\frac{I_1(\kappa)}{I_0(\kappa)}", font_size=34, color=MEM)
        jl = label(r"precision: \ the Fisher information of a von Mises", font_size=21, color=MEM)
        jrow = VGroup(J, jl).arrange(RIGHT, buff=0.3).move_to([0, -2.0, 0])
        rows = rows_of([
            (r"each is fitted to each observer separately, \ by maximum likelihood; \ compared by AIC", WHITE),
        ], 12.4, 24, 0.2).to_edge(DOWN, buff=0.8)
        ptag = psyche_tag(r"\texttt{wm.fit\_model}, \ \texttt{wm.model\_pdf}")
        with self.voiceover(
            "To get past descriptions, write down processes. <bookmark mark='a'/> Four of them. Slots: K slots, an "
            "item gets one with probability K over N and is then remembered with a fixed precision; otherwise it's a "
            "guess. Slots plus averaging: the K slots are shared out, and an item with s slots has s times the "
            "precision. <bookmark mark='b'/> Equal precision: no slots, every item is stored, and a fixed resource "
            "divided among N items gives each a precision that falls as a power of N. Variable precision, from Ronald "
            "van den Berg, Wei Ji Ma and colleagues in 2012: the same, except that precision itself varies from item "
            "to item and trial to trial, drawn from a gamma distribution. <bookmark mark='c'/> Precision has a "
            "precise meaning here: the Fisher information that a noisy memory carries about the true colour, which "
            "for a von Mises is kappa times a ratio of Bessel functions. <bookmark mark='d'/> Each model is fitted "
            "separately to each of the twelve observers, by maximum likelihood over every trial, and compared with "
            "the Akaike information criterion, which charges two points per parameter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(cards[0]), FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]), FadeIn(cards[3]))
            vo.wait_until("c")
            self.play(FadeIn(jrow))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
        self.clear_scene()

    def verdict(self):
        b = load("bays")
        head = heading(r"The verdict on these data")
        daic = b["daic"]
        n_obs = daic.shape[0]
        A = axes([0.3, n_obs + 0.7], [0, 220], x_length=7.4, y_length=3.4, xticks=list(range(1, n_obs + 1)),
                 yticks=[0, 100, 200], xlabel=r"observer", ylabel=r"AIC worse than the best model",
                 center=[-2.2, 0.6, 0], font_size=17)
        ax = A.ax
        dots = VGroup()
        for j, mo in enumerate(MODELS):
            off = (j - 1.5) * 0.17
            dots.add(VGroup(*[Dot(ax.c2p(i + 1 + off, min(float(daic[i, j]), 218)), radius=0.065, color=COLS[mo])
                              for i in range(n_obs)]))
        key = legend([(COLS[m], NAMES[m]) for m in MODELS], font_size=18).arrange(RIGHT, buff=0.45)
        key.next_to(A, DOWN, buff=0.35)
        wins, tot = b["wins"], b["daic_total"]
        rows = rows_of([
            (rf"variable precision is best for {int(wins[3])} of {n_obs} observers", MODEL),
            (rf"summed over observers, \ AIC worse by: \ slots + averaging {tot[1]:.0f}, \ slots {tot[0]:.0f}, \ "
             rf"equal precision {tot[2]:.0f}", GREY_A),
            (r"van den Berg and colleagues found the same across ten datasets", DATA),
            (r"but none of these models has swaps, \ and hybrids with a few slots and variable precision fit too", LOST),
        ], 4.6, 22, 0.32).move_to([4.3, 0.55, 0])
        ptag = psyche_tag(r"12 observers \ $\times$ \ 4 models, \ fitted to every trial")
        tag = published_tag(archive.VANDENBERG_2012.cite)
        with self.voiceover(
            "Here is the result, observer by observer. Each dot is how much worse a model's AIC is than the best "
            "model for that observer; zero is the winner. <bookmark mark='a'/> Variable precision wins for "
            f"{int(wins[3])} of the {n_obs} observers. <bookmark mark='b'/> Summed over observers, slots plus "
            f"averaging is worse by {tot[1]:.0f} points, slots by {tot[0]:.0f}, and equal precision by "
            f"{tot[2]:.0f}. Differences of ten are usually called decisive. <bookmark mark='c'/> Van den Berg, Awh "
            "and Ma reached the same conclusion across ten datasets from six laboratories in 2014: the resource "
            "models with variable precision fit best. <bookmark mark='d'/> Two caveats keep the argument open. None "
            "of these four models includes swaps, which we just saw are real. And hybrid models, with a small number "
            "of slots holding variable-precision memories, fit nearly as well. The winner is a family, not a "
            "single answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key), FadeIn(ptag))
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(dots[3], color=MODEL))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def mimic(self):
        m = load("mimic")
        b = load("bays")
        head = heading(r"Why the mixture's guesses can mislead")
        n = m["set_sizes"]
        A = axes([-np.pi, np.pi], [0, 0.6], x_length=5.4, y_length=3.0, xticks=[-np.pi, 0, np.pi], yticks=[],
                 xfmt=lambda v: {-180: r"-180^\circ", 0: r"0^\circ", 180: r"180^\circ"}[round(np.degrees(v))],
                 xlabel=r"error, \ six squares", center=[-3.5, 0.6, 0], font_size=17)
        h = hist(A.ax, m["edges"], np.minimum(m["hist_6"], 0.6), MODEL, opacity=0.55)
        x = b["x"]
        B = axes([0, 7], [0, 0.5], x_length=4.6, y_length=3.0, xticks=[1, 2, 4, 6], yticks=[0, 0.25, 0.5],
                 xlabel=r"squares", ylabel=r"the mixture's guess rate $g$", center=[3.0, 0.6, 0], font_size=17)
        gc = VGroup(curve_in(B.ax, n, m["g"], LOST, 4), scatter(B.ax, n, m["g"], LOST, 0.07))
        p = m["params"]
        rows = rows_of([
            (rf"a variable-precision observer who never guesses: \ the median observer's fit \ "
             rf"($J_1 = {p[0]:.0f}$, \ $\alpha = {p[1]:.2f}$, \ $\tau = {p[2]:.0f}$)", MODEL),
            (rf"fit the mixture to its errors: \ ``guess rates'' of {m['g'][2]:.2f} and {m['g'][3]:.2f} at four and six",
             LOST),
            (rf"and a ``capacity'' $N(1 - g)$ of about {m['K'][3]:.1f}: \ slots read off a model with none", MEM),
            (r"a low-precision memory and a guess look alike in the tails: \ parameters are not processes", GREY_A),
        ], 12.4, 24, 0.22).to_edge(DOWN, buff=0.75)
        ptag = psyche_tag(r"\texttt{wm.simulate\_report}: \ 20,000 trials per set size")
        with self.voiceover(
            "One more experiment, on Psyche, shows why the descriptions couldn't settle the question. "
            "<bookmark mark='a'/> Take the variable-precision model fitted to the median observer, and let Psyche "
            "be that observer. By construction, Psyche never guesses: every item is stored, just with a precision "
            "that varies. <bookmark mark='b'/> Fit the mixture model to Psyche's errors, and it reports guess rates "
            f"of {m['g'][2]:.2f} with four squares and {m['g'][3]:.2f} with six. <bookmark mark='c'/> Turn those into a "
            f"capacity, N times one minus g, and you get about {m['K'][3]:.1f} slots, read off a model that has none, "
            "and the spread of the 'stored' items levels off, just as it did in the real data. The picture that "
            "looked like slots is what a slotless observer produces. <bookmark mark='d'/> A memory held with very low precision is nearly flat, and in the tails it looks "
            "exactly like a guess. A parameter in a descriptive model is not a process in the head. Part 48 makes "
            "this a general method: simulate from each model, fit the others, and see what can be told apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(h))
            vo.wait_until("b")
            self.play(Create(gc), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
