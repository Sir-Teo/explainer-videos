from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load

DESK = [
    (r"Brownian motion starts at 0. What is the expected time until it leaves $(-a, b)$?",
     r"$ab$: by Dynkin with $f = x^2$, $\mathbb{E}\tau = \mathbb{E}W_\tau^2 = b^2\tfrac{a}{a+b} + a^2\tfrac{b}{a+b}$"),
    (r"What is the probability that Brownian motion hits $+1$ before $-2$?",
     r"$2/3$: $W$ is a martingale, so $1 \cdot p - 2(1 - p) = 0$"),
    (r"Price a digital call (pays 1 if $S_T > K$) in Black--Scholes, using Girsanov.",
     r"$e^{-rT} Q(S_T > K) = e^{-rT} N(d_2)$: under $Q$, $\log S_T$ is normal with mean "
     r"$\log S_0 + (r - \tfrac12\sigma^2)T$"),
]

PROBLEMS = [
    r"Show that $\sum |\Delta W|$ over a grid of $n$ steps on $[0, 1]$ has mean $\sqrt{2n/\pi}$, and $\sum (\Delta W)^2$ has "
    r"mean 1 and variance $2/n$.",
    r"Compute $\int_0^T W\,dW$ as a limit of left-point sums, and then of midpoint sums. Which one is a martingale in $T$?",
    r"Derive Milstein's correction for $dX = a\,dt + b(X)\,dW$ from It\^o's lemma applied to $b(X)$ over one step.",
    r"For Vasicek, show that $r_T$ is Gaussian and find its mean and variance. What is the long-run probability of a "
    r"negative rate with the fitted $\kappa = 0.099$, $\theta = 4.1\%$, $\sigma = 1.4\%$?",
    r"A Hawkes process has $\mu = 0.1$, $\alpha = 0.8$, $\beta = 2$ (per day). What is its long-run rate? What fraction of "
    r"events are triggered by earlier ones?",
    r"From the first-passage density $f_{\tau_a}(t) = \frac{a}{\sqrt{2\pi t^3}}e^{-a^2/2t}$, show that "
    r"$\mathbb{E}\,\tau_a = \infty$ although $P(\tau_a < \infty) = 1$.",
    r"Compute the Clark--Ocone integrand of $F = W_T^3$, and check it with It\^o's lemma.",
    r"(qual) For $dX = \sigma_t dW$ with deterministic $\sigma_t$, prove $\sqrt n(\mathrm{RV}_n - \int\sigma^2) \Rightarrow "
    r"N(0, 2\int\sigma^4)$ by the Lindeberg CLT.",
    r"(qual) With iid noise $\varepsilon$ of variance $\omega^2$ added to each price, show $\mathbb E\,\mathrm{RV}_n(Y) = "
    r"\mathrm{IV} + 2n\omega^2$ and $\mathrm{RV}_n(Y)/2n \to \omega^2$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.s = load("signature")
        self.m = load("cir_mle")
        self.env = load("envelope2")
        self.j = load("jumps")
        self.h = load("hawkes")
        self.r = load("rough")
        self.recap()
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self):
        items = [
            (r"Brownian motion: the universal limit of walks, and L\'evy's construction; reflection doubles the tail", BM),
            (r"quadratic variation is time: proved, and measured on Bitcoin through the microstructure noise", BM),
            (r"the It\^o integral is a completed ledger of bets: an isometry, a martingale; smooth noise is Stratonovich",
             ITO),
            (r"It\^o's lemma: the misses above the tangent plane pile up to $\tfrac12 f_{xx}\,dt$; Picard, Euler, "
             r"Milstein", ITO),
            (rf"OU and CIR solved and fitted: exact likelihood puts CIR's Feller ratio at {self.m['best']['feller']:.2f}",
             DRIFT),
            (r"Fokker--Planck pushes densities forward, Feynman--Kac pulls prices back", DRIFT),
            (r"Girsanov re-weights paths: drift changes, volatility cannot; importance sampling", STRAT),
            (r"martingale representation: every Brownian payoff is a hedge; a second noise or jumps break it", STRAT),
            (r"local time: the free stop-loss hedge loses the option's whole time value", JUMP),
            (rf"jumps: {self.j['n_jumps']} Bitcoin hours beyond 5 sd; Hawkes branching {self.h['fit']['branching']:.2f}, "
             r"passed the time-rescaling test", JUMP),
            (rf"roughness: $H \approx {self.r['hurst']['H']:.2f}$ on Bitcoin, but a smooth OU can look rough; "
             r"signatures read order and area", ITO),
        ]
        rows = VGroup()
        for i, (t, c) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=c), label(t, font_size=22)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        title = label(r"Part 5 in eleven lines", font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(title, DOWN, buff=0.35)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        with self.voiceover(
            "Part five in eleven lines. Brownian motion is the universal limit of random walks, and Lévy built it "
            "directly; the reflection principle doubles its tail. Its quadratic variation is time, proved and "
            "measured. The Itô integral is a completed ledger of bets, an isometry and a martingale, while smooth "
            "noise leads to Stratonovich. Itô's lemma is the misses above a tangent plane, piling up. Stochastic "
            "differential equations exist by Picard iteration and are simulated at known orders. Mean-reverting rates "
            "can be solved and fitted exactly, and their densities and prices obey partial differential equations. "
            "Girsanov re-weights paths: drift changes, volatility cannot. Every Brownian payoff is a hedge, until a "
            "second noise or a jump arrives. Local time is why the free hedge costs the option's price. Jumps are "
            "real, and they cluster. And volatility looks rough, though a fast but smooth process can look rough too, "
            "and signatures read what a path did, in order."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=20))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=25) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions, all classics. Brownian motion leaves an interval from minus a to b after an "
            "expected time a times b, by Dynkin's formula. <bookmark mark='a'/> The chance that Brownian motion hits plus one before minus two is two "
            "thirds, by optional stopping, exactly as for the walk in Part four. <bookmark mark='b'/> And a digital "
            "call in Black and Scholes is worth the discounted risk-neutral probability of finishing in the money: "
            "N of d two. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "And nine problems: the variations of Brownian motion, the two integrals of W against itself, Milstein's "
            "correction, the Vasicek distribution, a Hawkes process's long-run rate, the infinite mean of a first "
            "passage time, a Clark-Ocone integrand, and two at the level of a qualifying exam: realized variance's "
            "central limit theorem, and the bias that noise adds to it. Solutions, in English and Chinese, are in the "
            "notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(6)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"Girsanov, representation and the risk-neutral measure", [9, 10]),
            (r"local time, jumps and hedging errors", [11, 12, 13]),
            (r"mean reversion and term-structure models", [19]),
            (r"Hawkes, rough volatility and the order book", [14, 36]),
            (r"the simulation library, schemes and signatures", [15, 16, 17, 42]),
        ])
        with self.voiceover(
            "Where this comes back. Girsanov and martingale representation are the step from the real world to the "
            "pricing world in Parts nine and ten. Local time and jumps explain hedging errors in eleven to thirteen. "
            "Mean reversion returns in the rates part, nineteen. Hawkes processes and rough volatility return in "
            "fourteen and thirty-six. And the simulation library, the schemes and signatures power the computing "
            "parts, fifteen to seventeen, and the machines of forty-two."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Shreve, \textit{Stochastic Calculus for Finance II}, ch.\ 3--11",
             r"\O ksendal, \textit{Stochastic Differential Equations}; Karatzas and Shreve, \textit{Brownian Motion and "
             r"Stochastic Calculus}",
             r"Cont and Tankov, \textit{Financial Modelling with Jump Processes}, ch.\ 2--8; Bj\"ork, \textit{Arbitrage "
             r"Theory in Continuous Time}, ch.\ 4--5",
             r"Kloeden and Platen, \textit{Numerical Solution of Stochastic Differential Equations}; Glasserman, "
             r"\textit{Monte Carlo Methods in Financial Engineering}"],
            [r"Bachelier (1900); Wiener (1923); It\^o (1944, 1951); Cameron and Martin (1944); Kac (1949); L\'evy (1948); "
             r"Donsker (1951); Feller (1951); Girsanov (1960); Tanaka (1963); Wong and Zakai (1965); Stratonovich (1966)",
             r"Clark (1970); Novikov (1972); Vasicek (1977); Ocone (1984); Cox, Ingersoll and Ross (1985); Carr and "
             r"Jarrow (1990); Broadie, Glasserman and Kou (1997); Rogers (1997)",
             r"Merton (1976); Hawkes (1971); Ogata (1981); Barndorff-Nielsen and Shephard (2004); Hardiman, Bercot and "
             r"Bouchaud (2013); Andersen, Bollerslev, Diebold and Labys (2000); Zhang, Mykland and A\"it-Sahalia (2005)",
             r"Mandelbrot and Van Ness (1968); Gatheral, Jaisson and Rosenbaum (2018); Cont and Das (2024); Chen (1957); "
             r"Lyons (1998); Chevyrev and Kormilitzin (2016); Issa et al.\ (2023); Cuchiero et al.\ (2025)",
             r"Industry: CFTC 8432-21 (2021); CME Clearing 20-171 (2020); SEC Release 34-90763 (OCC STANS); "
             r"Demeterfi, Derman, Kamal and Zou (1999); Fed, OCC and FDIC SR 26-2 (2026)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. Every number was computed by the "
            "series' own code: Bitcoin by the minute and by the hour from Binance, and Treasury bill yields and the "
            "oil price from the St. Louis Fed. One command rebuilds them all."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 6, Financial Econometrics", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House can now simulate almost anything, and its sixth rule stands: no desk prices with a simulator "
            f"that has not first reproduced a known answer. The trial counter reads {self.env['trials']}. "
            "<bookmark mark='a'/> Next, Part six: financial econometrics. "
            "How to estimate the parameters of these models from data that is short, noisy and overlapping, and how "
            "not to fool yourself while doing it."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
