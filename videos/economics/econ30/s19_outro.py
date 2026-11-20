from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403

PROBLEMS = [
    r"Calvo: \ if a price survives each quarter with probability $\theta$, \ show its mean life is $1/(1-\theta)$ "
    r"quarters; \ find $\theta$ for 9 months.",
    r"Bo's fare: \ with demand $p^{-\varepsilon}$ and cost 1, \ show a fare $g$ too high costs about "
    r"$\varepsilon(\varepsilon-1)g^2/2$ of profit \ and $\varepsilon g$ of sales.",
    r"Forward: \ solve $\pi_t = \beta \mathbb{E}_t \pi_{t+1} + \kappa x_t$ forward; \ with $x_t$ an AR(1) with "
    r"persistence $\rho$, \ show $\pi_t = \kappa x_t/(1-\beta\rho)$.",
    r"Determinacy: \ with $\phi_x = 0$, \ show the three-equation model has a unique bounded solution iff "
    r"$\phi_\pi > 1$.",
    r"A monetary shock: \ with $v_t$ an AR(1), \ find $x_t$ and $\pi_t$ by undetermined coefficients.",
    r"The divine coincidence: \ with $u_t = 0$, \ show $i_t = r^n_t + \phi_\pi \pi_t$ with $\phi_\pi > 1$ gives "
    r"$\pi_t = x_t = 0$.",
    r"Discretion: \ minimize $\pi_t^2 + \vartheta x_t^2$ subject to $\pi_t = \kappa x_t + v_t$; \ show "
    r"$x_t = -(\kappa/\vartheta)\pi_t$.",
    r"$\bigstar$ \ Forward guidance: \ with $\kappa = 0$, \ show a one-quarter cut promised $h$ quarters ahead "
    r"moves $x_0$ by the same for every $h$; \ why does $\kappa > 0$ make it grow?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 42, E.ACCENT).move_to(UP * 2.2)
        a = wrapped_label(r"Because many prices are set for months at a time, \ and changing them costs the seller "
                          r"little to postpone but the economy a lot, \ a change in money or interest rates moves "
                          r"spending and output before it moves prices. \ The best a central bank can do is move its "
                          r"rate with the natural rate, \ more than one for one with inflation, \ and commit to a "
                          r"path people believe; \ when the rate hits zero, \ promises are what it has left, \ and "
                          r"they are weaker in reality than in the model.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        S = load("sticky")
        t = np.array(S["t"])
        mini = plane([1968, 2027], [-4, 20], x_length=4.2, y_length=1.3)
        logo = VGroup(path(mini, t, np.clip(S["flex"], -4, 20), FLEX, 2, smooth=False),
                      path(mini, t, np.clip(S["sticky"], -4, 20), STICKY, 3, smooth=False)).next_to(a, DOWN,
                                                                                                    buff=0.35)
        with self.voiceover(
            "So: why does money move the real economy, and what is the best a central bank can do? "
            "<bookmark mark='a'/> Because many prices are set for months at a time, and leaving a price alone "
            "costs the seller little but the economy a lot, a change in money or interest rates moves spending and "
            "output before it moves prices. The best a central bank can do is move its rate with the natural "
            "rate, more than one for one with inflation, and commit to a path people believe. When its rate hits "
            "zero, promises are what it has left, and they are weaker in reality than in the model."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        M, C, T, D, O, S, Z, H = (load(x) for x in ("menu", "calvo", "taylor", "determinacy", "optimal", "setters",
                                                     "zlb", "hybrid"))
        items = [
            (r"100{,}000 prices a month; \ Bils and Klenow count how often they change", E.ACCENT),
            (r"Play it: \ 4.3 months with sales, \ 8--11 without", PRICE),
            (r"evidence: \ magazines, \ surveys, \ the records; \ sticky and flexible inflation", STICKY),
            (rf"menu costs: \ a 1\% error costs {100 * M['rows'][0]['profit_loss']:.2f}\% of profit, \ "
             rf"{100 * M['rows'][0]['output_loss']:.1f}\% of output", FLEX),
            (r"the markup: \ output set by demand at a stuck price", COST),
            (rf"Calvo: \ $\pi = \beta \mathbb{{E}}\pi' + \kappa x$, \ $\kappa = {C['base']['kappa']:.2f}$", INFL),
            (r"the dynamic IS curve; \ three equations, \ three shocks", OUTPUT),
            (rf"Taylor: \ {T['fit']['pi']:.2f} on inflation; \ the Taylor principle", CB),
            (r"the divine coincidence, \ and cost-push shocks that break it", OUTPUT),
            (rf"commitment: \ loss {O['loss_c']:.3f} against {O['loss_d']:.3f}; \ the price level comes back", CB),
            (rf"selection: \ menu costs pass money through in {S['half_menu']} month, \ Calvo in "
             rf"{S['half_calvo']}", PRICE),
            (rf"the zero bound, \ forward guidance and its puzzle; \ the hump at quarter {H['rich']['peak_x']}",
             HOLD),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 30, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del D, Z
        with self.voiceover(
            "Part thirty in twelve lines. <bookmark mark='a'/> The price collectors record a hundred thousand "
            "prices a month, and Bils and Klenow counted how often they change. You guessed the median life of a "
            "price: four months with sales, eight to eleven without. Magazines, surveys and the records agree "
            "that many prices stick, and sticky prices carry inflation's trend. Menu costs explain why: a small "
            "error costs the seller little and the economy a lot. A firm with a markup sells what is demanded at "
            "its stuck price. Calvo's fairy gives the New Keynesian Phillips curve; the Euler equation gives the "
            "IS curve; Taylor's rule closes the model, and the Taylor principle makes its solution unique. Demand "
            "shocks can be offset completely, cost shocks cannot. Commitment beats discretion and brings the price "
            "level back. Menu costs with selection make money weaker than Calvo says. And at the zero bound, "
            "forward guidance works in the model far better than in life, and frictions give the hump."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. Calvo's durations; Bo's fare and Mankiw's second-order loss; the Phillips curve solved "
            "forward; the Taylor principle; a monetary shock by undetermined coefficients; the divine coincidence; "
            "discretion; and a starred problem on the forward guidance puzzle. Full solutions are in the part's "
            "notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Jordi Gal\'i, \emph{Monetary Policy, Inflation, and the Business Cycle} (2nd ed., 2015), \ chs.\ 3--5",
             r"Michael Woodford, \emph{Interest and Prices} (2003)",
             r"David Romer, \emph{Advanced Macroeconomics} (5th ed., 2019), \ chs.\ 7 and 12",
             r"Carl Walsh, \emph{Monetary Theory and Policy} (4th ed., 2017)"],
            [r"Calvo (1983); \ Mankiw (1985); \ Akerlof and Yellen (1985); \ Taylor (1993)",
             r"Bils and Klenow (2004); \ Nakamura and Steinsson (2008); \ Golosov and Lucas (2007)",
             r"Clarida, \ Gal\'i and Gertler (1999, 2000); \ Blanchard and Gal\'i (2007)",
             r"Christiano, \ Eichenbaum and Evans (2005); \ Smets and Wouters (2007)",
             r"Eggertsson and Woodford (2003); \ Del Negro, \ Giannoni and Patterson (2012); \ McKay, \ Nakamura and "
             r"Steinsson (2016)"])
        with self.voiceover(
            "The reading: Jordi Galí's textbook, which this part follows; Michael Woodford's Interest and Prices, "
            "the treatise behind it; Romer's chapters on nominal rigidity and policy; and Carl Walsh's Monetary "
            "Theory and Policy. Then the papers, from Calvo to the forward guidance puzzle."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2012, r"Mario Draghi", r"in London, \ with the euro under attack, \ he adds a sentence: \ "
                          r"the ECB will do whatever it takes, \ ``and believe me, \ it will be enough''",
                          color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 31 \ $\cdot$ \ Act VI, \ Money and the Cycle", font_size=30, color=GREY_B),
                     label(r"The Central Bank", font_size=46),
                     label(r"what does a central bank actually do, \ and how do we know what it achieves?",
                           font_size=26, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ the model of policy; \ next: \ the policy itself", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part built the model central banks think with. The next looks at what they actually do. "
            "<bookmark mark='a'/> On the twenty-sixth of July 2012, with Spanish and Italian borrowing costs at levels "
            "that threatened the euro, Mario Draghi added a sentence to a speech in London: the European Central "
            "Bank would do whatever it takes, and believe me, it will be enough. The programme he announced was "
            "never used. <bookmark mark='b'/> Part "
            "thirty-one: the central bank. What does a central bank actually do, and how do we know what it "
            "achieves?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
