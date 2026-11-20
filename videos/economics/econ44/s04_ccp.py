from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class CCP(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Faster: \ conditional choice probabilities", r"Can you skip solving the model?",
             "Chapter three. Faster: conditional choice probabilities.", lit={1993: r"Hotz and Miller"},
             scale=("firm",), horizon=("a month",))
        self.idea()
        self.real()
        self.fleets()

    def idea(self):
        lines = VGroup(
            MathTex(r"\ln \frac{P(\text{rebuild}\mid x)}{P(\text{keep}\mid x)} \;=\; v_{\text{rebuild}} - "
                    r"v_{\text{keep}}(x)", font_size=38),
            MathTex(r"v_{\text{keep}}(x) - v_{\text{rebuild}} \;=\; -\theta x + RC + \beta \sum_j p_j \big[\ln "
                    r"\hat P_1(j) - \ln \hat P_1(x+j)\big]", font_size=34, color=E.ACCENT),
        ).arrange(DOWN, buff=0.6).move_to(UP * 1.4)
        cards = point_cards([
            (r"step 1", r"estimate the chance \\ of a rebuild at each \\ mileage, \ straight \\ from the data", CCP_C),
            (r"the trick", r"a rebuild resets every \\ bus to zero, \ so the \\ future cancels into \\ those chances",
             PATIENT),
            (r"step 2", r"one logit, \\ no fixed point \\ to solve", GAIN),
        ], width=11.4, cols=3, font_size=19).move_to(DOWN * 1.6)
        tag = published_tag(tables.RUST_1987.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Solving the fixed point for every trial value is costly when the state is large, say in a market with "
            "many firms. In 1993 Joseph Hotz and Robert Miller found a short cut. <bookmark mark='a'/> With logit "
            "surprises, the log odds of rebuilding equal the difference between the two values. So the choice "
            "probabilities, which can be estimated straight from the data, carry the values in them. "
            "<bookmark mark='b'/> In Rust's model a rebuild returns every bus to zero miles, whatever its history. "
            "That makes the future cancel: the difference in values can be written using only the estimated "
            "chances of a rebuild, at mileage x plus j and at j. <bookmark mark='c'/> So the recipe has two steps: "
            "estimate those chances directly, then fit the costs with a single logit. No fixed point is ever "
            "solved."
        ) as vo:
            self.play(FadeIn(tag), Write(lines[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(Write(lines[1]), FadeIn(cards.cards[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cards.cards[2], shift=UP * 0.1))
        self.clear_scene()

    def real(self):
        C = load("ccp")
        R = load("rust")
        rows = [(r"NFXP", R["nfxp"]["RC"], PATIENT)] + [
            (rf"CCP, \ first step a degree-{k} \\ polynomial in mileage", C["real"][k]["RC"], CCP_C) for k in "123"]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(rows):
            y = 1.3 - 1.0 * k
            w = v * 0.35
            r = Rectangle(width=w, height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-0.6 + w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=18, color=col).next_to(np.array([-0.75, y, 0]), LEFT, buff=0.1), r,
                            label(rf"$RC$ = {v:.1f}", font_size=19, color=WHITE).next_to(r, RIGHT, buff=0.15)))
        head = label(r"on Zurcher's buses: \ the rebuild cost, \ estimated four ways", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(rf"only {R['n_repl']} rebuilds: \ the first step's guesses at low mileage, \ where rebuilds never "
                     r"happened, \ swing the answer", font_size=19, color=HOLD).to_edge(DOWN, buff=0.7)
        tag = data_tag(r"Rust's data; \ estimated here", corner=DR, font_size=11)
        with self.voiceover(
            "Try it on Zurcher's buses. <bookmark mark='a'/> The nested fixed point gave a rebuild cost of "
            f"{R['nfxp']['RC']:.1f}. <bookmark mark='b'/> The short cut needs a first step: the chance of a rebuild "
            "at each mileage, smoothed by a polynomial. With a straight line, it gives "
            f"{C['real']['1']['RC']:.1f}; <bookmark mark='c'/> with a quadratic, {C['real']['2']['RC']:.1f}; "
            f"<bookmark mark='d'/> with a cubic, {C['real']['3']['RC']:.1f}. <bookmark mark='e'/> The reason is the "
            f"sample. There are only {R['n_repl']} rebuilds, none at low mileage, so the first step must guess the "
            "chances there, and the formula leans on those guesses. The short cut trades computation for "
            "statistical precision."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(b_[0]) for b_ in bars])
            for mk, b_ in zip("abcd", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b_[1], LEFT), FadeIn(b_[2]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def fleets(self):
        C = load("ccp")
        tr = C["truth"]
        ax = plane([9.0, 10.5], [2.2, 2.8], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[9.0, 9.25, 9.5, 9.75, 10.0, 10.25, 10.5], yticks=[2.2, 2.4, 2.6, 2.8],
                   xlabel=r"rebuild cost, \ $RC$", ylabel=r"upkeep, \ $\theta$", xfmt=lambda v: f"{v:.2f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        t = VGroup(dot(ax, tr[0], tr[1], GAIN, 0.12),
                   label(r"the truth", font_size=17, color=GAIN).next_to(ax.ax.c2p(tr[0], tr[1]), UP, buff=0.14))
        pts = VGroup()
        for nb, sz in (("104", 0.08), ("1000", 0.11)):
            s_ = C["sims"][nb]
            a = dot(ax, s_["nfxp"][0], s_["nfxp"][1], PATIENT, sz)
            b = dot(ax, s_["ccp"][0], s_["ccp"][1], CCP_C, sz)
            la = label(rf"NFXP, \ {nb} buses", font_size=15, color=PATIENT).next_to(a, RIGHT, buff=0.12)
            lb = label(rf"CCP, \ {nb} buses", font_size=15, color=CCP_C).next_to(b, LEFT, buff=0.12)
            pts.add(VGroup(a, la, b, lb))
        s1, s2 = C["sims"]["104"], C["sims"]["1000"]
        side = VGroup(
            label(r"Island fleets with \\ Zurcher's costs planted", font_size=18, color=WHITE),
            label(rf"104 buses: \ {s1['replacements']} rebuilds", font_size=18, color=GREY_A),
            label(rf"1,000 buses: \ {s2['replacements']:,} rebuilds", font_size=18, color=GREY_A),
            label(r"with enough data \\ the two agree", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "On the Island we can plant Zurcher's costs in simulated fleets and compare. "
            f"<bookmark mark='a'/> With 104 buses for ten years, {s1['replacements']} rebuilds, both estimators land "
            f"near the truth: the nested fixed point at {s1['nfxp'][0]:.2f} and {s1['nfxp'][1]:.2f}, the short cut "
            f"at {s1['ccp'][0]:.2f} and {s1['ccp'][1]:.2f}. <bookmark mark='b'/> With a thousand buses, they agree "
            "more closely still. <bookmark mark='c'/> The lesson is the trade-off: the short cut is cheap to "
            "compute, which matters most when the model is a dynamic game among many firms, but it needs data rich "
            "enough to estimate the choice probabilities well, everywhere they will be used."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(t), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(pts[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()
