from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403
from videos.economics.econ63.s01_hook import web

PROBLEMS = [
    r"Leontief: \ with input shares $\Omega$ and consumption shares $\beta$, \ show that sales over GDP are "
    r"$\lambda' = \beta'(I - \Omega)^{-1}$, \ and that $\sum_i \lambda_i \geq 1$, \ with equality only without "
    r"intermediate inputs.",
    r"Hulten: \ in a competitive economy with Cobb-Douglas technologies, \ show that $d\log Y / d\log A_i = "
    r"\lambda_i$, \ whatever the network.",
    r"Granularity: \ with Zipf sizes $s_i \propto 1/i$, \ show that $\sqrt{\sum s_i^2}$ falls like $1/\log n$, \ "
    r"not $1/\sqrt{n}$.",
    r"Clearing: \ three banks in a ring each owe the next 10 and hold nothing else; \ show that every "
    r"$(p, p, p)$ with $0 \le p \le 10$ clears, \ and say which one Eisenberg and Noe's algorithm picks, \ and why.",
    r"Key player: \ for a star of one hub and $k$ leaves with $x = (I - \delta G)^{-1}\mathbf{1}$, \ compute the "
    r"hub's effort and the loss from removing it.",
    r"$\bigstar$ \ Jackson and Wolinsky: \ for $n$ players, \ show that the star is efficient for "
    r"$\delta - \delta^2 < c < \delta + \frac{(n-2)}{2}\delta^2$, \ and pairwise stable only for $c < \delta$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).move_to(UP * 2.4)
        a = wrapped_label(r"To a first approximation, \ when the firm or sector is large: \ it matters by its "
                          r"sales, \ and with firms as unequal as real ones, \ their own shocks do not cancel. \ "
                          r"Beyond that, \ when the shock is large and the input hard to replace, \ when the "
                          r"network is lopsided, \ and when links are specific or debts concentrated, \ a local "
                          r"shock travels along the links and grows. \ Dense links absorb small shocks and spread "
                          r"large ones.", 11.6, 26, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        links, nodes, _ = web(width=4.6, height=2.0, node_r=0.035)
        fl = VGroup(links, nodes).next_to(a, DOWN, buff=0.45)
        with self.voiceover(
            "So: when does a shock to one firm become a shock to everyone? <bookmark mark='a'/> To a first "
            "approximation, when the firm or sector is large: it matters by its sales, and with firms as unequal "
            "as real ones, their own shocks do not cancel out. Beyond that, when the shock is large and the input "
            "hard to replace, when the network is lopsided, and when links are specific or debts concentrated, a "
            "local shock travels along the links and grows. And dense links are a double-edged insurance: they "
            "absorb small shocks and spread large ones."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(fl), run_time=1.5)
        self.clear_scene()

    def recap(self):
        T, P, Gr, R, Q, O, B, D, K, Dl = (load(x) for x in (
            "table", "playit", "granular", "response", "quake", "oring", "banks", "diffusion", "keyplayer", "dials"))
        Rw = {r["sector"]: r for r in P["rows"]}
        e_loss, e_h = 100 * (1 - np.exp(Rw["energy"]["loss"])), 100 * (1 - np.exp(Rw["energy"]["hulten"]))
        thr = next(s for s, d in zip(B["contagion"]["shocks"], B["contagion"]["complete"]["defaults"]) if d == 10)
        kd = np.array(K["drop"]) / K["total"]
        items = [
            (rf"Leontief's paths: \ sales add to {T['sum_domar']:.2f} times GDP; \ metals 3.4 steps upstream", NODE),
            (r"Hulten: \ a small shock matters by sales over GDP, \ and nothing else", GDP),
            (rf"Play it: \ services cost most; \ energy {e_loss:.1f}\% against Hulten's {e_h:.1f}\%", LINK),
            (rf"granular: \ 10,000 Zipf firms still swing {100 * Gr['rows'][-1]['zipf']:.1f}\%; \ a star never calms"
             .replace(",", "{,}"), SHOCK),
            (rf"beyond Hulten: \ energy's share climbs from 0.25 towards "
             rf"{np.gradient(R['theta_0.15'], R['shocks'])[0]:.2f} as it fails", SHOCK),
            (rf"supply chains: \ {100 * Q['direct_only']:.0f}\% lost at the hit firms, \ "
             rf"{100 * Q['total_loss']:.1f}\% with the links; \ specific inputs carry it", SEED),
            (rf"the O-ring: \ one weak link costs two fifths; \ sorting adds {100 * O['gain']:.0f}\%", PEOPLE),
            (rf"banks: \ the complete network absorbs small losses, \ and fails whole past {thr:.0f}", BANK),
            (r"weak ties: \ moderately weak ties find jobs; \ Called it? \ right", PEOPLE),
            (rf"diffusion: \ central seeds reach {100 * D['most central'][-1]:.0f}\%, \ peripheral "
             rf"{100 * D['least central'][-1]:.0f}\%", SEED),
            (rf"key player: \ the bridge, \ {100 * kd[K['key']]:.0f}\% of effort, \ not the hub's "
             rf"{100 * kd[K['most_links']]:.0f}\%", SEED),
            (r"formation: \ the efficient star is unstable when links cost more than $\delta$", LINK),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=27, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 63, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part sixty-three in twelve lines. <bookmark mark='r1'/> An input-output table is a network, and "
            "Leontief's inverse sums its paths. <bookmark mark='r2'/> To first order, a sector matters by its "
            "sales. <bookmark mark='r3'/> The biggest seller is the biggest risk, with a premium for essential "
            "inputs. <bookmark mark='r4'/> Firms' own shocks do not cancel when firms are unequal or networks "
            "lopsided. <bookmark mark='r5'/> Large shocks to inputs nobody can replace cost more than their "
            "sales. <bookmark mark='r6'/> Disasters travel along supply chains, through specific inputs. "
            "<bookmark mark='r7'/> One weak link can sink a team, so skills sort. <bookmark mark='r8'/> Dense "
            "banking networks are robust yet fragile. <bookmark mark='r9'/> Weak ties carry news of jobs. "
            "<bookmark mark='r10'/> Where news starts decides how far it goes. <bookmark mark='r11'/> The key "
            "player is not the most popular. <bookmark mark='r12'/> And the networks people choose are not "
            "always the ones that would be best."
        ) as vo:
            self.play(FadeIn(head))
            for i, r_ in enumerate(rows):
                vo.wait_until(f"r{i + 1}")
                self.play(FadeIn(r_, shift=RIGHT * 0.15), run_time=0.8)
            self.play(Indicate(rows, color=WHITE, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems: Leontief's inverse and why sales add to more than GDP; Hulten's theorem for "
            "Cobb-Douglas economies; why Zipf's law slows the law of large numbers; a clearing vector by hand; the "
            "key player in a star; and a starred problem on when the efficient star is stable. Full solutions are "
            "in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Matthew O. Jackson, \emph{Social and Economic Networks} (2008)",
             r"Vasco Carvalho and Alireza Tahbaz-Salehi, \ ``Production Networks: \ A Primer'', \emph{Annual "
             r"Review of Economics} (2019)",
             r"Sanjeev Goyal, \emph{Connections: \ An Introduction to the Economics of Networks} (2007)"],
            [r"Leontief (1936); \ Domar (1961); \ Hulten (1978); \ Lucas (1977); \ Granovetter (1973); \ Kremer "
             r"(1993)",
             r"Jackson and Wolinsky (1996); \ Eisenberg and Noe (2001); \ Ballester, \ Calvó-Armengol and Zenou "
             r"(2006); \ Gabaix (2011)",
             r"Acemoglu et al.\ (2012, \ 2015); \ Banerjee et al.\ (2013); \ Elliott, \ Golub and Jackson (2014); \ "
             r"Barrot and Sauvagnat (2016)",
             r"Baqaee and Farhi (2019); \ Boehm et al.\ (2019); \ Carvalho et al.\ (2021); \ Elliott, \ Golub and "
             r"Leduc (2022); \ Rajkumar et al.\ (2022)"])
        with self.voiceover(
            "The reading: Matthew Jackson's Social and Economic Networks; Vasco Carvalho and Alireza Tahbaz-Salehi's "
            "primer on production networks; and Sanjeev Goyal's Connections. Then the papers, from Leontief to the "
            "experiments on weak ties."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(r"every day", r"a judge's desk", r"for each person arrested, \ a judge in the United States "
                          r"decides whether to hold them before trial, \ by guessing who will not come back; \ could "
                          r"an algorithm guess better, \ and how would we know?", color=E.ACCENT, width=10.4,
                          font_size=23)
        nxt = VGroup(label(r"Next: \ Part 64 \ $\cdot$ \ Act XII, \ The Frontier", font_size=30, color=GREY_B),
                     label(r"Machines that Learn", font_size=46),
                     label(r"what does machine learning change in how economics is done?", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from networks to the machines that read them", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        steps_ = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                  stroke_width=2.0), label(t_, font_size=18, color=c_))
                          for t_, c_ in ((r"prediction policy", LINK), (r"selective labels", SHOCK),
                                         (r"double machine learning", GDP), (r"language models", PEOPLE))])
        for s_ in steps_:
            s_[1].move_to(s_[0])
        steps_.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps_, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, from the networks to the machines that learn from them. <bookmark mark='a'/> Every day, "
            "judges in the United States decide whether people who have been arrested should wait for trial at "
            "home or in jail, by guessing who would not come back. Could an algorithm trained on the same facts "
            "guess better? And how would we know, when we never see what the jailed would have done? <bookmark "
            "mark='b'/> Prediction policy problems, selective labels, double machine learning, and language "
            "models as subjects and assistants. <bookmark mark='c'/> Part sixty-four: machines that learn."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps_], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
