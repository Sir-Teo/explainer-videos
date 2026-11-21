from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403

PROBLEMS = [
    r"The prosecutor: \ with a prior of 0.4 and a judge who convicts at 0.6, \ design the best investigation. \ What "
    r"share is convicted?",
    r"Concavification: \ a sender gets 1 if the receiver's belief is at least 0.75 and nothing otherwise. \ Find her "
    r"best value at a prior of 0.3, \ and the split that achieves it.",
    r"Cheap talk: \ with $b = 0.1$, \ find the boundaries of the two-message equilibrium, \ and the decision maker's "
    r"expected loss.",
    r"Bayes--Nash: \ in the Cournot example, \ show that firm 1's quantity is $(a - 2c_1 + \mathbb{E}c_2)/3$.",
    r"Beer or quiche: \ explain why the quiche equilibrium fails the intuitive criterion.",
    r"Common knowledge: \ in the nine-state dialogue, \ show what Ann's first announcement tells Bob.",
    r"The global game: \ show that the marginal speculator's belief about the share attacking is uniform, \ and "
    r"derive $\theta^* = 1 - c$.",
    r"$\bigstar$ \ Cascades: \ with hints right with probability $q$, \ show that a cascade on the better choice "
    r"eventually forms with probability $q^2/(q^2 + (1-q)^2)$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).move_to(UP * 2.2)
        a = wrapped_label(r"By choosing what others will learn, \ and committing to it: \ splitting their beliefs "
                          r"so that, \ on average, \ they stay right, \ but land where the receivers act as she "
                          r"wants. \ Without commitment, \ talk carries only as much as interests are aligned; \ "
                          r"with many receivers, \ she coordinates them; \ and everything rests on what people "
                          r"infer, \ which is less than the theory assumes.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([F["t"][0], F["t"][-1]], [0, 1], x_length=4.2, y_length=1.3)
        v = np.array(F["expected"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, BELIEF, 2.4, smooth=False).next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: how does someone who controls only what others learn get them to do what she wants? <bookmark "
            "mark='a'/> By choosing what they will learn, and committing to it. An investigation splits the "
            "audience's beliefs so that, on average, they remain right, but they land where the audience acts as "
            "the designer wants: just past the threshold, never wasted beyond it. Without commitment, talk "
            "carries only as much information as interests are aligned. With many receivers, the designer can "
            "coordinate them. And everything rests on what people infer from what they see, which in practice is "
            "less, and less reliable, than the theory assumes."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=14.0, rate_func=linear)
            self.play(Indicate(a, color=E.ACCENT, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def recap(self):
        Pr, C, Ct, Bq, D, Cs, Ch, G, R, Bg = (load(x) for x in (
            "prosecutor", "concav", "cheap", "beer", "design", "cascade", "chain", "global", "relational", "bargain"))
        r05 = next(r for r in Ct["rows"] if abs(r["b"] - 0.05) < 1e-9)
        items = [
            (rf"the prosecutor: \ 30\% guilty, \ {100 * Pr['optimal']:.0f}\% convicted, \ nobody fooled", SENDER),
            (r"Bayesian games: \ each type's best response, \ on average over the others", RECEIVER),
            (r"off the path: \ the intuitive criterion keeps beer, \ drops quiche", BELIEF),
            (rf"cheap talk: \ a bias of 0.05 allows {r05['N']} messages; \ a quarter, \ none", SIGNAL),
            (rf"persuasion: \ the concave closure at the prior: \ {C['at_prior']:.1f}", SENDER),
            (rf"many receivers: \ {D['best']:.1f} investors by design, \ {D['full']:.1f} by full disclosure", THEORY),
            (r"Blackwell: \ better for everyone only if the other is a garbling", BELIEF),
            (r"common knowledge: \ no agreeing to disagree; \ almost is not enough", RECEIVER),
            (rf"global games: \ the regime falls below {G['flat']['theta']:.1f}; \ sharp public news, \ three "
             r"equilibria", ERR),
            (rf"cascades: \ {100 * Cs['limit_wrong']:.1f}\% of queues wrong for ever", LOSS),
            (rf"reputation: \ entry only in the last {Ch['k_star']} towns; \ Coase: \ delay "
             rf"{Bg['coase']['best']['delay']:.1f}", WEAK),
            (rf"relational contracts: \ as good as a contract from $\delta = {R['delta_star']:.1f}$", GAIN),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 53, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del Bq
        with self.voiceover(
            "Part fifty-three in twelve lines. <bookmark mark='r1'/> A prosecutor who cannot lie can double the "
            "convictions by designing the investigation. <bookmark mark='r2'/> In a Bayesian game each type plays "
            "its best response, on average over the others. <bookmark mark='r3'/> Off the equilibrium path, "
            "beliefs must be sensible, and the intuitive criterion says which are. <bookmark mark='r4'/> Cheap "
            "talk carries as much as interests are aligned. <bookmark mark='r5'/> A sender who commits gets the "
            "concave closure of her value at the prior. <bookmark mark='r6'/> With many receivers, obedient "
            "recommendations can coordinate them. <bookmark mark='r7'/> One source is better for everyone only if "
            "the other is a garbling of it. <bookmark mark='r8'/> People with a common prior cannot agree to "
            "disagree, and almost common knowledge is not enough. <bookmark mark='r9'/> A little private noise "
            "picks one equilibrium; sharp public news brings back several. <bookmark mark='r10'/> Herds can lock "
            "onto the wrong choice with nobody making a mistake. <bookmark mark='r11'/> Reputations make threats "
            "credible, and private values make bargains slow. <bookmark mark='r12'/> And promises no court will "
            "enforce are kept when the future matters enough."
        ) as vo:
            self.play(FadeIn(head))
            for i, r_ in enumerate(rows):
                vo.wait_until(f"r{i + 1}")
                self.play(FadeIn(r_, shift=RIGHT * 0.15), run_time=0.8)
            self.play(Indicate(rows, color=WHITE, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. Design another prosecutor's investigation; find a concave closure; derive the two-message "
            "equilibrium of cheap talk; Bayes-Nash quantities; the intuitive criterion; what an announcement reveals; "
            "the global game's threshold; and a starred problem on the odds that a cascade is right. Full solutions "
            "are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Drew Fudenberg and Jean Tirole, \emph{Game Theory} (1991), \ chapters 6 to 10",
             r"Emir Kamenica, \ `Bayesian persuasion and information design', \emph{Annual Review of Economics} "
             r"(2019)",
             r"Dirk Bergemann and Stephen Morris, \ `Information design: a unified perspective', \emph{JEL} (2019)",
             r"Stephen Morris and Hyun Song Shin, \ `Global games: theory and applications' (2003)"],
            [r"Harsanyi (1967--68); \ Nash (1950); \ Blackwell (1953); \ Coase (1972); \ Aumann (1976)",
             r"Selten (1978); \ Crawford and Sobel (1982); \ Geanakoplos and Polemarchakis (1982); \ Rubinstein (1982)",
             r"Kreps and Wilson (1982); \ Milgrom and Roberts (1982); \ Cho and Kreps (1987); \ Bull (1987)",
             r"Rubinstein (1989); \ Banerjee (1992); \ Bikhchandani, Hirshleifer and Welch (1992); \ Carlsson and van "
             r"Damme (1993)",
             r"Morris and Shin (1998); \ Levin (2003); \ DellaVigna and Kaplan (2007); \ Kamenica and Gentzkow (2011)"])
        with self.voiceover(
            "The reading: Fudenberg and Tirole's chapters on games of incomplete information; Emir Kamenica's "
            "survey of Bayesian persuasion; Bergemann and Morris's unified view of information design; and Morris "
            "and Shin on global games. Then the papers, from Harsanyi to the prosecutor."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1973, r"Daniel McFadden and the Bay Area's new railway",
                          r"the official forecast: \ about 15\% of work trips; \ a model estimated from commuters' "
                          r"own choices: \ 6.3\%; \ in 1975, \ 6.2\%", color=E.ACCENT, width=10.4, font_size=23)
        nxt = VGroup(label(r"Next: \ Part 54 \ $\cdot$ \ Act X, \ The Graduate Core", font_size=30, color=GREY_B),
                     label(r"Estimating Models", font_size=46),
                     label(r"how is a model's hidden machinery measured from the choices it predicts?", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from what people know \ to what we can measure", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        steps = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                 stroke_width=2.0), label(t_, font_size=18, color=c_))
                         for t_, c_ in ((r"likelihood", RECEIVER), (r"moments", SENDER),
                                        (r"simulation", BELIEF), (r"identification", SIGNAL))])
        for s_ in steps:
            s_[1].move_to(s_[0])
        steps.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, the models meet the data. <bookmark mark='a'/> In the early 1970s the San Francisco Bay "
            "Area was building a railway. The official forecast said about fifteen percent of commuters would use "
            "it; Daniel McFadden's model, estimated from commuters' own choices, said 6.3 percent, and in 1975 it "
            "was 6.2. <bookmark mark='b'/> Part fifty-four is about estimating models: likelihood, moments, "
            "simulation, <bookmark mark='c'/> and the question beneath them all, what in the data identifies "
            "what in the model."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
