from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats13.common import *  # noqa: F403


class Online(VoiceoverScene):
    def construct(self):
        self.card()
        self.bing()
        self.anatomy()
        self.cuped_scatter()
        self.cuped_math()
        self.cuped_reps()
        self.srm()
        self.pitfalls()
        self.board()

    def card(self):
        card = chapter_card(13, r"Online experiments", r"Fisher's field, \ a billion plots at a time", lit=(2013,), part=PART)
        with self.voiceover("Chapter thirteen. Online experiments."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def bing(self):
        hc = history_card(2012, r"Bing, \ Microsoft's search engine", r"an engineer's idea, \ shelved for months as low priority: \ "
                          r"show more of each ad's text in its headline. \ A two-week online experiment: \ revenue up 12\%, \ worth over "
                          r"\$100 million a year in the United States", color=S.ALT, width=10.6, font_size=22).move_to([0, 1.4, 0])
        rows = fit_rows(VGroup(
            label(r"told by Kohavi, \ Tang \& Xu, \ \emph{Trustworthy Online Controlled Experiments} (2020)", font_size=22, color=GREY_A),
            label(r"most ideas, \ tested, \ do nothing or harm: \ the experiment is the only judge", font_size=24),
            label(r"large companies now run tens of thousands of controlled experiments a year", font_size=24, color=OBS),
        ), 12.4, 0.3, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Around 2012, an engineer at Bing, Microsoft's search engine, suggested a small change to how "
            "ads were shown: move some of each ad's text up into its headline. The idea sat on a list for months, judged low "
            "priority. When someone finally tested it, in a two-week online experiment, revenue rose twelve percent: worth more "
            "than a hundred million dollars a year in the United States alone. <bookmark mark='b'/> The story is told by Ron "
            "Kohavi, Diane Tang and Ya Xu in their book on online experiments. <bookmark mark='c'/> Their broader point is "
            "humbling: most ideas, when tested, do nothing or do harm, and nobody can tell in advance which. "
            "<bookmark mark='d'/> So large technology companies now run tens of thousands of randomized experiments a year. "
            "They're Fisher's experiments, with users as plots."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def anatomy(self):
        rows = [
            cmath(r"\text{unit}", r":", r"\text{a user, \ assigned by an experiment-specific salted hash}", font_size=30),
            cmath(r"\text{arms}", r":", r"\text{A (control) and B (the change), \ usually 50/50}", font_size=30),
            cmath(r"\text{metric}", r":", r"\text{revenue, \ clicks, \ time, \ \ldots\ per user}", font_size=30),
            cmath(r"\hat\tau", r"=", r"\bar y_B - \bar y_A,\qquad \mathrm{SE} = \sqrt{s_A^2/n_A + s_B^2/n_B}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"the same user always sees the same arm"), why(r"Bernoulli assignment; realized counts can differ"),
                why(r"decided before the experiment"), why(r"Welch's comparison, \ Part 10")]
        intro = label('Specify the unit, assignment and metric before running', font_size=36)
        with self.voiceover(
            "The anatomy of an A/B test. <bookmark mark='a'/> The unit is a user, assigned by an experiment-specific randomized hash of their ID, so the same "
            "person always sees the same version. <bookmark mark='b'/> Two arms, the control and the change, usually split fifty "
            "fifty: a Bernoulli-randomized design with millions of plots. <bookmark mark='c'/> A metric chosen in advance, like "
            "revenue per user. <bookmark mark='d'/> And the estimate is the difference in means, with Welch's standard error "
            "from Part 10. Everything in this part applies. The one new problem is that the effects are tiny, a fraction of a "
            "percent, and the metrics are noisy. Even with millions of users, precision is precious."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def cuped_scatter(self):
        d = load("online")
        x, y, t = np.asarray(d["x_show"]), np.asarray(d["y_show"]), np.asarray(d["t_show"], bool)
        A = axes([-3, 24], [-7, 26], x_length=6.2, y_length=4.6, xlabel=r"last month's spend, \ $x$", ylabel=r"this month's spend, \ $y$",
                 xticks=[0, 10, 20], yticks=[0, 10, 20], center=[-3.0, 0.0, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=S.TREAT if tt else S.CTRL, fill_opacity=0.75) for a, b, tt in zip(x, y, t)])
        th = d["theta"]
        b0 = float(np.mean(y) - th * np.mean(x))
        ln = Line(ax.c2p(-3, b0 - 3 * th), ax.c2p(24, b0 + 24 * th), color=FIT, stroke_width=3)
        rows = fit_rows(VGroup(
            label(r"20,000 users; \ the change truly adds 0.15 per user", font_size=24),
            label(r"but most of the variation in $y$ was there before the experiment", font_size=24),
            MathTex(rf"\mathrm{{corr}}(x, y) = {d['rho']:.2f}", font_size=30),
            label(r"subtract the part of $y$ that $x$ predicts", font_size=24, color=FIT),
            label(r"$x$ was measured before randomization: \ it cannot be affected by B; inference must account for fitting", font_size=22, color=OBS),
        ), 4.8, 0.34, [4.4, 0.2, 0])
        tag = simulated_tag(r"simulated A/B test", corner=DR)
        with self.voiceover(
            "Here's a simulated test with twenty thousand users. <bookmark mark='a'/> The change truly adds point one five to "
            "each user's monthly spend, about one and a half percent. <bookmark mark='b'/> Plot each user's spend this month "
            "against their spend last month, before the experiment began. Most of the variation in this month's spend was "
            "already there: big spenders stay big spenders. <bookmark mark='c'/> The correlation is point eight. "
            "<bookmark mark='d'/> So subtract the part of each user's spend that last month predicts, and compare what's left. "
            "<bookmark mark='e'/> Using a pre-treatment covariate avoids adjusting away treatment effects, because the change cannot "
            "have affected last month. This is regression adjustment using a baseline covariate, rather than design-stage blocking; fitted adjustment can have small finite-sample bias."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots, lag_ratio=0.003), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(ln), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def cuped_math(self):
        d = load("online")
        rows = [
            cmath(r"\tilde y_i", r"=", r"y_i - \theta\,(x_i - \bar x),\qquad \theta = \frac{\mathrm{cov}(x, y)}{\mathrm{var}(x)}", font_size=30),
            cmath(r"\mathrm{Var}(Y-\theta X)", r"=", rf"(1 - \rho^2)\,\mathrm{{Var}}(y) = {1 - d['rho'] ** 2:.2f}\,\mathrm{{Var}}(y)", font_size=30),
            cmath(r"\text{plain}", r":", rf"\hat\tau = {d['plain']:.3f},\ \ \mathrm{{SE}}\ {d['se_plain']:.3f},\ \ p = {d['p_plain']:.3f}", font_size=30),
            cmath(r"\text{CUPED}", r":", rf"\hat\tau = {d['cuped']:.3f},\ \ \mathrm{{SE}}\ {d['se_cuped']:.3f},\ \ p = 3.9\times10^{{-5}}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        rows[2][2].set_color(RES)
        whys = [why(rf"Deng, \ Xu, \ Kohavi \& Walker (2013); \ $\hat\theta = {d['theta']:.2f}$"), why(r"the variance left after the regression"),
                why(r"not significant"), why(rf"the same users: \ worth {d['users_equiv']:.1f}$\times$ as many")]
        with self.voiceover(
            "<bookmark mark='a'/> In 2013 Alex Deng, Ya Xu, Ron Kohavi and Toby Walker named it CUPED: replace each user's "
            "metric by the metric minus theta times their centred pre-experiment value, with theta the regression slope of y on "
            "x. <bookmark mark='b'/> For a fixed population-optimal coefficient, the residual variance is one minus rho squared times the original: here, about thirty-six "
            "percent of it. <bookmark mark='c'/> The plain comparison estimates point one oh four, with a standard error of "
            "point zero five six: p point zero six five, not significant. <bookmark mark='d'/> CUPED, on the same users, "
            "estimates point one four, with a standard error of point zero three four: p of four in a hundred thousand. Cutting "
            "the variance to thirty-six percent is worth two point eight times as many users. Statisticians will recognize "
            "Fisher's analysis of covariance from 1932, adapted at scale. The fitted-coefficient standard error and z-test here are large-sample approximations."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cuped_reps(self):
        d = load("online")
        r = np.asarray(d["reps"])
        A = axes([-0.05, 0.35], [0, 110], x_length=9.0, y_length=3.6, xlabel=r"estimated effect, \ 600 of 2,000 experiments shown", ylabel=r"",
                 xticks=[0, 0.1, 0.15, 0.2, 0.3], yticks=[0, 50, 100], center=[0, 0.6, 0])
        ax = A.ax
        e = np.linspace(-0.05, 0.35, 61)
        b1 = hist_bars(ax, e, np.histogram(r[:, 0], e)[0], color=RES, opacity=0.45)
        b2 = hist_bars(ax, e, np.histogram(r[:, 1], e)[0], color=OBS, opacity=0.75)
        tl = DashedLine(ax.c2p(0.15, 0), ax.c2p(0.15, 105), color=EXACT, stroke_width=3)
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{SD of the estimate: plain}}\ {d['sd_plain']:.3f}\ \to\ \text{{CUPED}}\ {d['sd_cuped']:.3f}", font_size=30),
            label(r"SDs use all 2,000 runs; fitted adjustment can have small finite-sample bias", font_size=24, color=OBS),
            label(r"Freedman (2008), \ Lin (2013): \ regression adjustment is safe in randomized experiments, \ with care", font_size=22, color=GREY_A),
        ), 12.4, 0.3, [0, -2.3, 0])
        with self.voiceover(
            "Is that one experiment typical? <bookmark mark='a'/> Repeat the whole experiment two thousand times; the histogram shows the first six hundred. The plain "
            "estimates, in red, spread widely around the truth; the CUPED estimates, in gold, cluster tightly: their standard "
            "deviation falls from point zero five seven to point zero three three. <bookmark mark='b'/> Both are centred on the "
            "true point one five. The estimates show little bias in this large simulation. Fitting theta on these same data can introduce small finite-sample bias, even with a pre-treatment covariate. The covariate was measured before the coin "
            "was tossed. <bookmark mark='c'/> David Freedman worried in 2008 that regression adjustment could mislead in "
            "experiments; Winston Lin showed in 2013 that with an interaction and robust standard errors, under regularity conditions it is at least "
            "as precise, asymptotically. It's now routine."
        ) as vo:
            self.play(FadeIn(A), Create(tl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b1], lag_ratio=0.01), run_time=1.5)
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b2], lag_ratio=0.01), FadeIn(rows[0]), run_time=1.5)
            for k, m_ in enumerate("bc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def srm(self):
        d = load("online")["srm"]
        W = 10.0
        tot = d["a"] + d["b"]
        ra = Rectangle(width=W * d["a"] / tot, height=0.8, stroke_width=0, fill_color=S.CTRL, fill_opacity=0.8)
        rb = Rectangle(width=W * d["b"] / tot, height=0.8, stroke_width=0, fill_color=S.TREAT, fill_opacity=0.8)
        bar = VGroup(ra, rb).arrange(RIGHT, buff=0).move_to([0, 1.6, 0])
        half = DashedLine(bar.get_top() + UP * 0.2, bar.get_bottom() + DOWN * 0.2, color=WHITE, stroke_width=2).set_x(bar.get_left()[0] + W / 2)
        la = label(rf"A: \ {d['a']:,}", font_size=26, color=S.CTRL).next_to(ra, UP, buff=0.2)
        lb = label(rf"B: \ {d['b']:,}", font_size=26, color=S.TREAT).next_to(rb, UP, buff=0.2)
        rows = fit_rows(VGroup(
            label(r"designed as 50/50; \ B has 1.6\% more recorded users than A", font_size=26),
            MathTex(rf"\chi^2_1\ \text{{test of the split:}}\ p = {d['p']:.4f}", font_size=32, color=RES),
            label(r"a sample-ratio mismatch flag: \ investigate assignment and logging", font_size=24, color=RES),
            label(r"bots filtered differently, \ a crash in one arm, \ a redirect that loses users", font_size=24),
            label(r"a flag is evidence, not proof of a bug: \ audit before interpreting metrics", font_size=24, color=OBS),
        ), 12.4, 0.32, [0, -1.2, 0])
        intro = label('Check the allocation counts before interpreting outcomes', font_size=36)
        with self.voiceover(
            "The most important check in online experiments costs nothing. <bookmark mark='a'/> This experiment was designed as a "
            "fifty-fifty split. The arms received fifty thousand and fifty thousand eight hundred and twenty users. "
            "<bookmark mark='b'/> A chi-squared test of the split, Part 10's goodness of fit, gives p equals point zero zero "
            "nine eight. A fair coin rarely misses by this much. <bookmark mark='c'/> That's a sample-ratio mismatch, and it "
            "is evidence of an assignment or logging problem, although a valid randomized test can occasionally flag by chance. <bookmark mark='d'/> Bots filtered differently in "
            "the two arms; a bug that crashes the new version for some browsers, so their users vanish from the logs; a "
            "redirect that loses people. <bookmark mark='e'/> If selection or logging depends on the arm, comparability can fail and "
            "the original randomization guarantee no longer applies to the recorded comparison. Check the split before reading any metric."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(GrowFromEdge(ra, LEFT), GrowFromEdge(rb, LEFT), FadeIn(la), FadeIn(lb), Create(half), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1], shift=RIGHT * 0.2))
        self.clear_scene()

    def pitfalls(self):
        rows = fit_rows(VGroup(
            label(r"peeking at the $p$-value every day and stopping when it dips: \ Part 10's broken promise", font_size=24, color=RES),
            label(r"novelty: \ users react to anything new, \ then settle", font_size=24),
            label(r"interference: \ on a social network, \ one user's treatment reaches their friends", font_size=24),
            label(r"many metrics, \ many segments: \ chapter four's multiplicity", font_size=24),
            label(r"A/A tests: \ run the platform against itself, \ and check that 5\% means 5\%", font_size=24, color=OBS),
        ), 12.4, 0.44, [0, 0, 0])
        intro = label('An online experiment still needs a valid design', font_size=36)
        with self.voiceover(
            "The old pitfalls come back at scale. <bookmark mark='a'/> Watching the p-value every day and stopping when it dips "
            "below five percent breaks the test, as Part 10 showed; Part 58 builds tests that allow it. "
            "<bookmark mark='b'/> Novelty effects: users react to anything new, then settle, so a two-day test can mislead. "
            "<bookmark mark='c'/> Interference: on a social network, treating one user changes what their friends see, so the "
            "control group isn't untreated. Parts 35 and 62 take this up. <bookmark mark='d'/> Dozens of metrics and segments: "
            "chapter four's multiplicity. <bookmark mark='e'/> And A/A tests, where both arms get the same version, check that "
            "the platform's five percent really is five percent."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=13) if r.part == 13]
        b = coverage_board(rows, lit_part=13, placeholders=0, font_size=20, row_h=0.55)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "The Coverage Board, with seven new rows, all tests whose promise is a five percent false-rejection rate. "
            "<bookmark mark='a'/> The randomization test on skewed data, ten plots against ten: five point two percent, kept. "
            "Its validity came from the coin. <bookmark mark='b'/> A t-test on the tidy systematic layout of chapter one, with no "
            "real difference between varieties: it rejects every single time. The soil's gradient is confounded with the "
            "varieties. <bookmark mark='c'/> All ten pairwise t-tests among five groups, unadjusted: at least one false "
            "rejection twenty-seven percent of the time, broken. Tukey's method: four point nine five percent, kept. "
            "<bookmark mark='d'/> The split plot analysed as a completely randomized design: twenty-six percent, broken. With "
            "the whole-plot error: five point oh one, kept. <bookmark mark='e'/> And the CUPED test in ten thousand A/A "
            "experiments: five point two, kept. Every broken row in this part is a design ignored by its analysis."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]))
            vo.wait_until("c")
            self.play(FadeIn(b.body[2]), FadeIn(b.body[3]))
            vo.wait_until("d")
            self.play(FadeIn(b.body[4]), FadeIn(b.body[5]))
            vo.wait_until("e")
            self.play(FadeIn(b.body[6]))
        self.wait(1.0)
        self.clear_scene()
