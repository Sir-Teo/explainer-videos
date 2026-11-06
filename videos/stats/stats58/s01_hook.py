from __future__ import annotations

import numpy as np

from videos.stats.stats58.common import *  # noqa: F403


class Hook(LectureMixin, VoiceoverScene):
    def construct(self):
        self.story()
        self.idea()
        self.numbers()
        self.peeking()
        self.board()
        self.turn()
        self.upgrade()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1943, 1945)).to_edge(UP, buff=0.35)
        hc = history_card(1943, r"the Statistical Research Group, \ Columbia",
                          r"a Navy officer complains that a test of two alternative methods ran on long after a seasoned "
                          r"observer could see the answer; \ W. Allen Wallis and Milton Friedman ask whether a test can "
                          r"stop as soon as the evidence suffices, \ and take the question to Abraham Wald", color=SPRTC,
                          width=11.4, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"Wald's answer: \ the sequential probability ratio test", font_size=26, color=SPRTC),
            label(r"classified until 1945; \ published in the \emph{Annals} that year, \ and as a book in 1947", font_size=24, color=GREY_A),
            label(r"Wallis (1980): \ one of the most seminal statistical ideas of its time", font_size=24, color=WEALTHC),
        ), 12.4, 0.35, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1943, at the Statistical Research Group at Columbia University, a Navy officer "
            "complained about a test comparing two alternative methods. It had to run its full planned length, though a "
            "seasoned observer could have called the answer long before. W. Allen Wallis and Milton Friedman wondered "
            "whether a test could stop as soon as the evidence sufficed, and took the question to Abraham Wald. <bookmark "
            "mark='b'/> Wald's answer was the sequential probability ratio test. <bookmark mark='c'/> It was classified "
            "until 1945, then published, and in 1947 became a book. <bookmark mark='d'/> Wallis, writing the group's history "
            "in 1980, counted it among the most seminal statistical ideas of its time."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def idea(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The idea fits in one line. After each observation, compute the likelihood ratio of the "
            "alternative against the null. <bookmark mark='b'/> If it climbs above a threshold A, stop and reject the null. "
            "<bookmark mark='c'/> If it falls below a threshold B, stop and accept it. <bookmark mark='d'/> Otherwise take "
            "another observation. Wald showed that A equal to one minus beta over alpha, and B equal to beta over one minus "
            "alpha, give error rates close to alpha and beta, whatever the data turn out to be.",
            [(r"\Lambda_n", r"=", r"\prod_{i \le n} \frac{f_1(X_i)}{f_0(X_i)}", 38),
             (r"\Lambda_n \ge A", r":", r"\text{stop; \ reject } H_0", 38),
             (r"\Lambda_n \le B", r":", r"\text{stop; \ accept } H_0", 38),
             (r"\text{else}", r":", r"\text{one more observation; \ } A = \tfrac{1 - \beta}{\alpha}, \ B = \tfrac{\beta}{1 - \alpha}", 36)],
            [r"the evidence so far", r"enough against $H_0$", r"enough for it", r"Wald's thresholds"],
            colors=[(0, SPRTC), (1, FIXEDC), (2, CSC)])

    def numbers(self):
        d = load("hook")
        fx = d["fixed"]
        self.lad_voiceover(
            f"<bookmark mark='a'/> Wald's own kind of example: lots of shells, where a defective rate of ten percent is "
            f"acceptable and twenty percent is not, with alpha five percent and beta ten. <bookmark mark='b'/> The best "
            f"fixed-sample test needs {fx['n']} shells, rejecting with {fx['c']} or more defectives. <bookmark mark='c'/> The "
            f"sequential test, computed exactly, needs on average {d['asn0']:.0f} shells when the rate is ten percent and "
            f"{d['asn1']:.0f} when it is twenty: <bookmark mark='d'/> a saving of about {100 * d['saving0']:.0f} percent, with "
            f"its error rates at {100 * d['size']:.1f} and {100 * (1 - d['power']):.1f} percent, inside the targets.",
            [(r"p_0 = 0.1, \ p_1 = 0.2", r":", r"\alpha = 0.05, \ \beta = 0.10", 38),
             (r"\text{fixed sample}", r":", rf"n = {fx['n']}, \ \text{{reject if }} \ge {fx['c']} \text{{ defective}}", 36),
             (r"\text{SPRT}", r":", rf"E_{{p_0}} N = {d['asn0']:.1f}, \ \ E_{{p_1}} N = {d['asn1']:.1f}", 36),
             (r"\text{saving}", r":", rf"\approx {100 * d['saving0']:.0f}\%, \ \text{{errors }} {100 * d['size']:.1f}\%, \ {100 * (1 - d['power']):.1f}\%", 36)],
            [r"lot acceptance", r"the exact binomial test", r"exact, \ by the lattice", r"and errors on target"],
            colors=[(1, FIXEDC), (2, SPRTC), (3, CSC)])

    def peeking(self):
        d = load("ville")
        ns, cv = d["ns"], d["curve"]
        lab = {n: c for n, c in zip(ns, cv)}
        self.lad_voiceover(
            f"<bookmark mark='a'/> But the SPRT is the disciplined way to look early. The undisciplined way is to run an "
            f"ordinary five percent test, and check it after every new observation. <bookmark mark='b'/> If there is no "
            f"effect at all, the chance of having rejected somewhere within a hundred looks is {100 * lab[100]:.0f} "
            f"percent; <bookmark mark='c'/> within five thousand, {100 * lab[5000]:.0f} percent, and it goes to one. <bookmark "
            f"mark='d'/> The law of the iterated logarithm guarantees it: a random walk crosses every fixed multiple of "
            f"root n infinitely often.",
            [(r"\text{peeking}", r":", r"|Z_n| \ge 1.96 \text{ at any } n \le N?", 38),
             (r"N = 100", r":", rf"P_{{H_0}}(\text{{reject}}) = {lab[100]:.2f}", 38),
             (r"N = 5{,}000", r":", rf"{lab[5000]:.2f} \ \to 1", 38),
             (r"\text{why}", r":", r"\limsup Z_n/\sqrt{2\log\log n} = 1", 36)],
            [r"Part 35's peeking, \ every visit", r"simulated, \ 20{,}000 nulls", r"sure to reject, \ eventually", r"Part 44's LIL: \ every fixed line is crossed"],
            colors=[(1, FIXEDC), (2, FIXEDC)])

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("checked every visit", "betting confidence"),
                   f"<bookmark mark='a'/> On the Board, a conversion rate of twelve percent watched from the twentieth "
                   f"visitor to the two-thousandth. The ordinary ninety-five percent interval, checked at every visit, holds "
                   f"the truth at every check in only {100 * br[0]['achieved']:.0f} percent of streams: broken. <bookmark "
                   f"mark='b'/> The betting confidence sequence of chapter six holds it throughout in "
                   f"{100 * br[1]['achieved']:.0f} percent: kept.", [("a", [0]), ("b", [1])])

    def turn(self):
        self.list_voiceover(
            "<bookmark mark='a'/> So there are two questions. <bookmark mark='b'/> The first is how to test so that you may "
            "look whenever you like, and stop whenever you like, and keep your error rate. <bookmark mark='c'/> The answer "
            "will be a single inequality from 1939, Jean Ville's, and the idea of betting against the null. <bookmark "
            "mark='d'/> The second is how to experiment when you choose what to collect as you go, as an A/B platform or an "
            "adaptive trial does. <bookmark mark='e'/> Then the data are no longer independent of the design, and inference "
            "needs its own tools.",
            [(r"two questions:", GREY_A),
             (r"1. \ test so that you may look, \ and stop, \ whenever you like", WEALTHC),
             (r"answer: \ Ville's inequality (1939), \ betting, \ e-values, \ confidence sequences", CSC),
             (r"2. \ experiment when you choose what to collect as you go", BANDITC),
             (r"answer: \ adaptive designs, \ and inference that knows how the data were chosen", BANDITC)])

    def upgrade(self):
        cards = [
            upgrade_card(10, r"a $p$-value is computed once, \ at a fixed $n$", r"you look once",
                         r"chapters 3--7: \ e-values and test martingales, \ valid at every look"),
            upgrade_card(35, r"group-sequential boundaries for planned looks", r"looks planned in advance",
                         r"chapters 2 and 6: \ the Brownian picture, \ and looks at any time"),
        ]
        VGroup(*cards).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Two promises come due. Part ten computed a p-value once, at a sample size fixed in "
            "advance, and assumed you look once. Chapters three to seven build e-values and test martingales, valid at every "
            "look. <bookmark mark='b'/> Part thirty-five gave group-sequential boundaries for looks planned in advance. "
            "Chapter two puts them in the Brownian picture, and chapter six allows a look at any time."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 58", font_size=34, color=GREY_B), label(r"Anytime-Valid Inference", font_size=56),
                      label(r"and Adaptive Experiments", font_size=40, color=GREY_A)).arrange(DOWN, buff=0.2)
        obj = objectives_card([
            r"the SPRT, \ exactly; \ group-sequential theory; \ estimation after stopping",
            r"test martingales and Ville; \ testing by betting; \ e-values; \ composite nulls",
            r"confidence sequences; \ CAST as a betting test; \ e-BH; \ change detection on the Nile",
            r"bandits, \ adaptive designs and the inference they need; \ off-policy evaluation; \ open problems",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 35, \ 44, \ 46").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.sequential}, \ the confidence funnel").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-eight: anytime-valid inference and adaptive experiments. <bookmark mark='b'/> "
            "The sequential probability ratio test, computed exactly; group-sequential theory and estimation after stopping; "
            "test martingales and Ville's inequality; testing by betting and e-values, for simple and composite nulls; "
            "confidence sequences; the CAST trial as a betting test; multiple testing with e-values; change detection on the "
            "Nile; and bandits, adaptive designs, and the inference they need, with off-policy evaluation and open problems."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
