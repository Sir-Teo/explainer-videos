from __future__ import annotations

from videos.philosophy.philosophy41.common import *  # noqa: F403


class Privacy(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Differential privacy", r"Can data be useful and private at once?", lit=(2006,), part=PART)
        with self.voiceover("Chapter eight. Differential privacy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.anonymity()
        self.laplace()
        self.survey()
        self.models()
        self.reconstruct()

    def anonymity(self):
        head = history_card(2006, r"Dwork, \ McSherry, \ Nissim and Smith", r"``Calibrating Noise to Sensitivity''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"Sweeney \ (2000)", r"zip code, \ birth date and sex identify about 87\% of Americans; \ she found the governor of Massachusetts in `anonymous' hospital data", BAD),
                (r"Netflix \ (2008)", r"Narayanan and Shmatikov re-identified Netflix Prize users from a few ratings and dates", PRIV),
                (r"AOL \ (2006)", r"searches released under numbers: \ user 4417749 was found by reporters within days", RESP),
                (r"the lesson", r"removing names does not anonymize: \ any rich record is a fingerprint", GOAL)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Privacy first. The old method, removing names, fails. <bookmark mark='a'/>Latanya Sweeney showed that "
            "zip code, birth date and sex alone identify most Americans, about eighty seven percent in her 2000 "
            "study, and she found the governor of Massachusetts in supposedly anonymous hospital records. <bookmark "
            "mark='b'/>In 2008 Arvind Narayanan and Vitaly Shmatikov re-identified users of the Netflix Prize data "
            "from a handful of ratings and their dates. <bookmark mark='c'/>When AOL released search logs under "
            "numbers in 2006, reporters found user four four one seven seven four nine within days. <bookmark "
            "mark='d'/>Removing names does not anonymize: any rich enough record is a fingerprint."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def laplace(self):
        d = load("laplace")
        xs = d["x"]
        M = d["mechanisms"]
        assert [m["eps"] for m in M] == [0.1, 0.5, 1.0, 2.0] and all(abs(m["max_ratio"] - m["bound"]) < 1e-3 for m in M)
        head = label(r"The Laplace mechanism", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[-8, 8, 2], y_range=[0, 1.05, 0.25], x_length=7.6, y_length=4.0,
                  axis_config={"color": GREY_B, "include_tip": False, "font_size": 16},
                  x_axis_config={"numbers_to_include": [-8, -4, 0, 4, 8]}).move_to([-2.6, -0.5, 0])
        xl = label(r"noise added to the true count", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        cols = [GREY_B, FAIRC, PRIV, EXPL]
        curves = VGroup()
        for m, c in zip(M, cols):
            curves.add(VMobject(color=c, stroke_width=3.5).set_points_as_corners(
                [ax.c2p(x, y) for x, y in zip(xs, m["density"])]))
        m1 = M[2]
        sh = VMobject(color=PRIV, stroke_width=2.5).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, m1["shifted"])])
        sh.set_stroke(opacity=0.6)
        f = MathTex(r"\mathcal{M}(D) = \mathrm{count}(D) + \mathrm{Lap}(1/\varepsilon)", font_size=30).move_to([3.7, 2.2, 0])
        f2 = MathTex(r"\frac{P[\mathcal{M}(D) = o]}{P[\mathcal{M}(D') = o]} \;\le\; e^{\varepsilon}", font_size=32,
                     color=PRIV).move_to([3.7, 1.0, 0])
        leg = stack([(rf"$\varepsilon = {m['eps']:g}$: \ typical error {m['error']:g}", c) for m, c in zip(M, cols)],
                    font_size=19, buff=0.16, aligned_edge=LEFT).move_to([3.7, -0.7, 0])
        note = label(r"computed: \ the largest ratio of the two curves is exactly $e^{\varepsilon}$", font_size=19,
                     color=GOAL).move_to([3.7, -2.3, 0])
        with self.voiceover(
            "Differential privacy, defined by Cynthia Dwork, Frank McSherry, Kobbi Nissim and Adam Smith in 2006, "
            "makes privacy a precise promise. <bookmark mark='a'/>To release a count from a database, add random "
            "noise drawn from a Laplace distribution whose width is one over epsilon. <bookmark mark='b'/>Now compare "
            "two databases that differ in one person, whose true counts differ by one. The two output distributions, "
            "here for epsilon equal to one, are shifted copies of each other. <bookmark mark='c'/>At every possible "
            "output, the probabilities differ by a factor of at most e to the epsilon; the Reasoner checks that the "
            "largest ratio is exactly that. So whatever anyone learns from the output, they learn almost the same "
            "whether or not you are in the data. <bookmark mark='d'/>Smaller epsilon means wider noise: more privacy, "
            "and less accuracy. The typical error is one over epsilon: ten for epsilon a tenth, half for epsilon two."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(Write(f), Create(curves[2]))
            vo.wait_until("b")
            self.play(Create(sh))
            vo.wait_until("c")
            self.play(Write(f2), FadeIn(note))
            vo.wait_until("d")
            self.play(FadeOut(sh), *[Create(curves[i]) for i in (0, 1, 3)], FadeIn(leg))
        self.clear_scene()

    def survey(self):
        r = load("rr")
        c = load("compose")
        assert r["eps"] == 1.0986 and c["rows"][-1]["advanced"] == 27.14
        head = label(r"Randomized response, \ and the privacy budget", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        steps = stack([(r"Warner \ (1965): \ flip a coin; \ heads, \ answer truthfully; \ tails, \ flip again and say yes "
                        r"on heads", GREY_A),
                       (rf"simulated: \ {r['n']} people, \ true share {r['true_p']:.2f}; \ {r['share_yes'] * 100:.1f}\% "
                        rf"say yes", PRIV),
                       (rf"estimate $2 \times$ yes $- \tfrac12$ = {r['estimate']:.3f} \ ($\pm$ {r['se']:.3f}); \ each "
                        rf"answer is private with $\varepsilon = \ln 3 \approx 1.10$", FAIRC)],
                      font_size=21, buff=0.25).move_to([0, 1.7, 0])
        hd = [r"\text{queries}", r"\text{basic: } k\varepsilon", r"\text{advanced}"]
        cells = [[label(str(rw["k"]), font_size=19), label(f"{rw['basic']:g}", font_size=19),
                  label(f"{rw['advanced']:g}", font_size=19, color=EXPL)] for rw in c["rows"]]
        grid = ValueGrid(hd, cells, col_w=[2.0, 2.6, 2.6], cell_h=0.45, font_size=18).move_to([0, -1.3, 0])
        tl = label(r"total privacy loss, \ each query with $\varepsilon = 0.1$ \ ($\delta = 10^{-6}$)", font_size=19,
                   color=GREY_A).next_to(grid, UP, buff=0.15)
        with self.voiceover(
            "An older trick shows the idea at its simplest. <bookmark mark='a'/>Stanley Warner proposed in 1965 a way "
            "to ask embarrassing survey questions. Each respondent flips a coin: on heads, they answer truthfully; on "
            "tails, they flip again and say yes on heads, whatever the truth. <bookmark mark='b'/>The Reasoner "
            "simulates two thousand respondents, thirty percent of whom have the embarrassing trait; about forty two "
            "percent say yes. <bookmark mark='c'/>Since a yes comes with probability half the true share plus a "
            "quarter, the share can be estimated, here as point three four, give or take two hundredths, while every "
            "single answer is deniable: differentially private with epsilon the natural log of three. <bookmark "
            "mark='d'/>But privacy loss adds up. A hundred queries each with epsilon a tenth lose up to ten in total; "
            "a smarter accounting, advanced composition, gives about six. Privacy is a budget that every released "
            "statistic spends."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(tl), FadeIn(grid.head), Create(grid.rule), LaggedStart(*[FadeIn(VGroup(*rw)) for rw in grid.cell],
                                                                                     lag_ratio=0.3))
        self.clear_scene()

    def reconstruct(self):
        d = load("reconstruct")
        R = d["results"]
        assert d["n"] == 64 and R[2]["recovered"] == 1.0 and R[-1]["recovered"] == 0.719
        head = label(r"Too many accurate answers: \ reconstruction \ (Dinur and Nissim, \ 2003)", font_size=28,
                     color=CONN).to_edge(UP, buff=0.3)
        bars = VGroup()
        x0 = -4.6
        for k, r0 in enumerate(R):
            h = r0["recovered"] * 4.0
            b = Rectangle(width=1.0, height=h, fill_color=BAD if r0["recovered"] == 1.0 else PRIV, fill_opacity=0.7,
                          stroke_width=0).move_to([x0 + 1.5 * k, -2.4 + h / 2, 0])
            bars.add(VGroup(b, label(f"{r0['recovered'] * 100:.0f}\\%", font_size=18).next_to(b, UP, buff=0.08),
                            label(f"{r0['noise']:g}", font_size=18, color=GREY_A).next_to(b, DOWN, buff=0.15)))
        base = Line([x0 - 0.7, -2.4, 0], [x0 + 1.5 * 5 + 0.7, -2.4, 0], color=GREY_C)
        xl = label(r"size of the noise added to each answer", font_size=18, color=GREY_A).move_to([x0 + 3.75, -3.3, 0])
        side = stack([(r"64 secret bits; \ 256 random subset sums released", GREY_A),
                      (r"least squares, \ then rounding: \ every bit recovered when the noise is small", BAD),
                      (r"noise near $\sqrt{n} = 8$ is needed before the attack degrades", GOAL)],
                     font_size=19, buff=0.22, aligned_edge=LEFT)
        for s0 in side:
            if s0.width > 4.2:
                s0.width = 4.2
        side.move_to([4.7, 0.3, 0])
        with self.voiceover(
            "Why accept noise at all? Because without it, aggregates leak individuals. Irit Dinur and Kobbi Nissim "
            "showed in 2003 that answering too many questions too accurately lets an attacker rebuild the data. "
            "<bookmark mark='a'/>The Reasoner hides sixty four secret bits, one per person, and releases two hundred "
            "and fifty six sums over random subsets of people, each with some noise. <bookmark mark='b'/>An attacker "
            "solves for the bits by least squares and rounds. With noise up to two, every bit comes back. <bookmark "
            "mark='c'/>Only when the noise approaches the square root of the number of people, eight here, does the "
            "attack start to fail. This is the theorem that convinced the United States Census Bureau to adopt "
            "differential privacy for the 2020 census."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[:3]], lag_ratio=0.3), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[3:]], lag_ratio=0.3), FadeIn(side[2]))
        self.clear_scene()

    def models(self):
        head = label(r"Central, \ local, \ and learning in private", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"central", r"a trusted curator adds noise once: \ a count is off by about $1/\varepsilon$", PRIV),
                (r"local", r"each person randomizes before sending: \ no trust needed, \ but a count is off by about $\sqrt{n}/\varepsilon$", EXPL),
                (r"DP-SGD \ (Abadi et al., \ 2016)", r"train a network privately: \ clip each example's gradient, \ add Gaussian noise, \ and account for the privacy spent", FAIRC),
                (r"the cost", r"private models are less accurate, \ most of all on small groups \ (Bagdasaryan et al., \ 2019)", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Differential privacy comes in two architectures. <bookmark mark='a'/>In the central model, a trusted "
            "curator holds the raw data and adds noise once, to the answer; a count is then off by about one over "
            "epsilon, however many people are counted. <bookmark mark='b'/>In the local model, which is randomized "
            "response, each person adds noise before their data leave their device. No one need be trusted, but the "
            "noise adds up: a count over n people is off by about the square root of n over epsilon. <bookmark "
            "mark='c'/>Machine learning uses the central model. Martín Abadi and colleagues showed how to train a "
            "deep network privately: clip each training example's gradient so no one example can move the model much, "
            "add Gaussian noise, and keep an account of the privacy spent, using composition. <bookmark mark='d'/>The "
            "price falls unevenly. Eugene Bagdasaryan and colleagues found that private training costs the most "
            "accuracy on small and unusual groups, whose examples are exactly the ones clipping and noise suppress. "
            "Privacy and fairness are not independent goals."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
