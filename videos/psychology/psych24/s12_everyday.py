from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403


class Everyday(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.rules()
        self.bounded()

    def card(self):
        card = chapter_card(11, r"Everyday predictions, \ and bounded rationality",
                            r"Are ordinary guesses good inferences?",
                            lit={1955: r"Simon", 2006: r"Griffiths \& Tenenbaum", 2008: r"Mozer et al."},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter eleven. Everyday predictions, and bounded rationality."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def derive(self):
        d = load("everyday")
        head = heading(r"Derivation: \ predicting a total from a part")
        q = label(r"A film has taken \$40 million so far. \ How much will it take in all?", font_size=30,
                  color=CONTENT).move_to([0, 2.3, 0])
        eqs = VGroup(
            MathTex(r"p(t_{\text{total}} \mid t) \;\propto\; p(t \mid t_{\text{total}})\; p(t_{\text{total}})",
                    font_size=30, color=LOGIC),
            MathTex(r"p(t \mid t_{\text{total}}) = \frac{1}{t_{\text{total}}}, \quad 0 < t < t_{\text{total}}",
                    font_size=28, color=GREY_A),
            MathTex(r"\text{guess: the median of } p(t_{\text{total}} \mid t)", font_size=28, color=MODEL),
        ).arrange(DOWN, buff=0.25).move_to([-3.3, 0.85, 0])
        A = axes([0, 300], [0, 1.05], x_length=5.8, y_length=1.9, xticks=[0, 40, 80, 150, 300], yticks=[],
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"total takings, \ \$ million", center=[-3.3, -1.75, 0],
                 font_size=15)
        T = d["film_T"]
        pri = curve_in(A.ax, T, d["film_prior"], CONTENT, 3)
        lik = curve_in(A.ax, T[T >= d["film_seen"]], d["film_like"][T >= d["film_seen"]], LOGIC, 3)
        post = curve_in(A.ax, T[T >= d["film_seen"]], d["film_post"][T >= d["film_seen"]], MODEL, 4)
        g = d["film_guess"]
        assert abs(g - 2 * d["film_seen"]) < 1e-9
        gl = DashedLine(A.ax.c2p(g, 0), A.ax.c2p(g, 1.0), color=MODEL, stroke_width=2)
        gt = label(rf"guess: \ \${g:.0f} million", font_size=18, color=MODEL).next_to(A.ax.c2p(g, 1.0), UP,
                                                                                       buff=0.06)
        key = legend([(CONTENT, r"prior: \ a power law"), (LOGIC, r"likelihood: \ $1/t_{\text{total}}$, \ above 40"),
                      (MODEL, r"posterior")], font_size=15).move_to(A.ax.c2p(225, 0.62))
        rows = rows_of([
            (r"Griffiths \& Tenenbaum, \ 2006: \ you meet a quantity at a random moment of its course, \ and "
             r"know how such totals are spread in the world", WHITE),
            (r"the likelihood favours small totals: \ any $t$ is less surprising if the total is short", LOGIC),
            (r"the prior is what you know about films, \ lives, \ cakes, \ reigns", CONTENT),
            (rf"the best single guess is the posterior median: \ for the film, \ \${g:.0f} million, \ twice what it "
             rf"has taken", MODEL),
        ], 5.6, 24, 0.36).move_to([3.7, -0.3, 0])
        tag = published_tag(r"Griffiths \& Tenenbaum (2006), \ \emph{Psychological Science}")
        with self.voiceover(
            "Reasoning in daily life is mostly guessing well. <bookmark mark='a'/> A film has taken forty million "
            "dollars so far. How much will it take in all? <bookmark mark='b'/> In 2006 Tom Griffiths and Josh "
            "Tenenbaum treated this as inference. You meet the film at a random moment of its run, so the chance of "
            "seeing any particular amount so far is one over the total. <bookmark mark='c'/> Small totals make what "
            "you saw less surprising, so the likelihood pulls the guess down. Your knowledge of how such totals are "
            "spread, the prior, pulls it the other way. <bookmark mark='d'/> Combine them, and the best single "
            "guess is the median of the posterior. For the film, it's eighty million dollars: twice what it has "
            "taken so far."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(A))
            vo.wait_until("b")
            self.play(Write(eqs[0]), Write(eqs[1]), Create(lik), FadeIn(key[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(pri), FadeIn(key[0]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Write(eqs[2]), Create(post), FadeIn(key[2]), FadeIn(rows[3]))
            self.play(Create(gl), FadeIn(gt))
        self.clear_scene()

    def rules(self):
        d = load("everyday")
        head = heading(r"Three priors, \ three rules")
        t = d["t"]
        specs = [
            (r"power law \ (film takings)", "power_1.0", CONTENT, r"multiply: \ $\times 2$ for $\gamma = 1$"),
            (r"Erlang \ (a typical length)", "erlang", INSIGHT, r"add: \ a roughly constant amount"),
            (r"normal \ (life spans)", "gauss", MODEL, r"regress to the mean, \ then a little more"),
        ]
        A = axes([0, 100], [0, 200], x_length=5.6, y_length=3.6, xticks=[0, 50, 100], yticks=[0, 100, 200],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"$t$, \ seen so far",
                 ylabel=r"predicted total", center=[-3.1, 0.2, 0], font_size=16)
        diag = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(100, 100), color=GREY_D)
        cs = VGroup(*[curve_in(A.ax, t, np.minimum(d[k], 200), c, 3) for _, k, c, _ in specs])
        key = legend([(c, n) for n, _, c, _ in specs], font_size=17).move_to(A.ax.c2p(30, 175))
        life = (d["ex_life_18"], d["ex_life_39"], d["ex_life_90"])
        rows = rows_of([
            (r"a power-law prior gives a multiplicative rule: \ with $\gamma = 1$, \ guess twice what you have seen", CONTENT),
            (r"an Erlang prior adds a roughly constant amount", INSIGHT),
            (rf"a normal prior for lives \ (mean 75, \ sd 16, \ illustrative): \ at 18, \ about {life[0]:.0f}; \ at "
             rf"39, \ {life[1]:.0f}; \ at 90, \ {life[2]:.0f}", MODEL),
            (r"people's median guesses fell close to the optimal curves for films, \ lives, \ poems and cakes", DATA),
            (r"Mozer, \ Pashler \& Homaei, \ 2008: \ group medians that good can come from people who each recall "
             r"only a couple of examples", LOST),
        ], 5.6, 22, 0.34).move_to([3.6, 0.0, 0])
        tag = psyche_tag(r"\texttt{reason.predict\_total}; \ Griffiths \& Tenenbaum (2006)")
        with self.voiceover(
            "Different priors give different rules. <bookmark mark='a'/> Film takings follow a power law: a few "
            "films take enormous sums. Then the optimal guess is a multiple of what you've seen; for the simplest "
            "power law, twice. <bookmark mark='b'/> If totals cluster around a typical length, an Erlang prior, the "
            "rule is to add a roughly constant amount. <bookmark mark='c'/> And for life spans, roughly normal, the "
            f"guess sits near the average until you're old: about {life[0]:.0f} for someone who is eighteen, "
            f"{life[1]:.0f} at thirty-nine, and {life[2]:.0f} for someone already ninety. <bookmark mark='d'/> "
            "Griffiths and Tenenbaum found that people's median guesses fell close to the optimal curves for films, "
            "lives, poems and baking times, as if each had the right prior. <bookmark mark='e'/> But Michael Mozer "
            "and colleagues showed that group medians that good could come from people who each recall only a couple "
            "of examples. The group is well calibrated; whether each mind holds a whole distribution is contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(diag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(Create(cs[k]), FadeIn(key[k]), FadeIn(rows[k]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def bounded(self):
        sel = load("selection")
        head = heading(r"Rational, \ irrational, \ or bounded?")
        items = [
            (r"logic as the yardstick", LOST, r"people fail: \ the selection task, \ syllogisms, \ belief bias"),
            (r"probability as the yardstick", MODEL, r"people often do well: \ choosing informative evidence, \ "
                                                    r"guessing totals from parts"),
            (r"bounded rationality", SEARCH, r"Simon, \ 1955: \ a mind with little time and memory "
                                             r"\emph{satisfices}: \ it stops at the first option that is good enough"),
        ]
        cols = VGroup()
        for k, (t, c, w) in enumerate(items):
            box = RoundedRectangle(corner_radius=0.15, width=4.1, height=4.9, stroke_color=c, stroke_width=2,
                                   fill_color=c, fill_opacity=0.06).move_to([-4.35 + 4.35 * k, 0.05, 0])
            body = VGroup(label(t, font_size=25, color=c), wrapped_label(w, 3.6, 21, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.18)
            body.move_to(box.get_top() + DOWN * 0.25, aligned_edge=UP).align_to(box, LEFT).shift(RIGHT * 0.25)
            cols.add(VGroup(box, body))
        # 1: the four cards, logic's answer against the common one
        cards = VGroup()
        for j, (face, pick) in enumerate((("E", "both"), ("K", ""), ("4", "people"), ("7", "logic"))):
            r = RoundedRectangle(corner_radius=0.06, width=0.62, height=0.86, stroke_color=GREY_B, stroke_width=2,
                                 fill_color="#20262F", fill_opacity=1)
            cards.add(VGroup(r, label(face, font_size=26)).move_to([-5.4 + 0.72 * j, -1.05, 0]))
            if pick in ("both", "logic"):
                cards[-1][0].set_stroke(MODEL, 4)
            if pick == "people":
                cards[-1][0].set_stroke(LOST, 4)
        ck = VGroup(label(r"logic: \ E and 7", font_size=17, color=MODEL),
                    label(r"most people: \ E, \ or E and 4", font_size=17, color=LOST)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(cards, DOWN, buff=0.2).align_to(cards, LEFT)
        v1 = VGroup(cards, ck)
        # 2: expected information per card, rare p and q
        eig = sel["eig"]
        names = [r"p", r"q", r"not-q", r"not-p"]
        x0, base = -1.17, -1.85
        bars2 = VGroup(*[Rectangle(width=0.5, height=max(0.02, 2.0 * v / eig.max()), stroke_width=0, fill_color=MODEL,
                                   fill_opacity=0.85).move_to([x0 + 0.78 * j, base, 0], aligned_edge=DOWN)
                         for j, v in enumerate(eig)])
        bn = VGroup(*[label(n, font_size=17, color=GREY_A).next_to(bars2[j], DOWN, buff=0.08).set_y(base - 0.18)
                      for j, n in enumerate(names)])
        bt = label(r"expected information, \ rare $p$ and $q$", font_size=16, color=GREY_B).move_to(
            [x0 + 1.17, base + 2.3, 0])
        assert list(eig) == sorted(eig, reverse=True)
        v2 = VGroup(bars2, bn, bt)
        # 3: satisficing, options examined in turn until one clears the bar
        hs = [0.7, 1.1, 0.55, 1.75, 2.0, 0.9, 1.5]
        thr = 1.55
        x3, base3 = 2.85, -1.85
        bars3 = VGroup(*[Rectangle(width=0.36, height=h, stroke_width=0, fill_color=SEARCH, fill_opacity=0.85)
                         .move_to([x3 + 0.48 * j, base3, 0], aligned_edge=DOWN) for j, h in enumerate(hs)])
        first = next(j for j, h in enumerate(hs) if h >= thr)
        assert first == 3
        bars3[first].set_fill(INSIGHT, 1)
        for j in range(first + 1, len(hs)):
            bars3[j].set_fill(GREY_D, 0.5)
        tl = DashedLine([x3 - 0.3, base3 + thr, 0], [x3 + 0.48 * (len(hs) - 1) + 0.3, base3 + thr, 0],
                        color=GREY_A, stroke_width=2)
        tt = label(r"good enough", font_size=16, color=GREY_A).next_to(tl, UP, buff=0.06).align_to(tl, LEFT)
        st = label(r"stop here; \ the best goes unseen", font_size=16, color=INSIGHT).next_to(bars3, DOWN, buff=0.12)
        v3 = VGroup(bars3, tl, tt, st)
        nxt = label(r"the argument continues in Part 26: \ judgement, \ heuristics, \ and biases", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.75)
        tag = historical_tag(r"Simon (1955, \ 1956)")
        with self.voiceover(
            "So are people logical? It depends on the yardstick. <bookmark mark='a'/> Measured against logic, people "
            "fail: the selection task, syllogisms, belief bias. <bookmark mark='b'/> Measured against probability and "
            "the world people actually live in, they often do well: choosing informative evidence, guessing totals "
            "from parts. <bookmark mark='c'/> Herbert Simon offered a third view in 1955: bounded rationality. A mind "
            "with little time and limited memory can't optimize. It satisfices, stopping at the first option that's "
            "good enough. The search of chapter four, the chunks of chapter seven, and the shortcuts of chapter two "
            "are all ways of being good enough. <bookmark mark='d'/> The argument about what counts as rational "
            "returns in Part 26, on judgement and its biases."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, col, v in zip("abc", cols, (v1, v2, v3)):
                vo.wait_until(m)
                self.play(FadeIn(col, shift=UP * 0.15), FadeIn(v))
            vo.wait_until("d")
            self.play(FadeIn(nxt))
        self.clear_scene()
