from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, GOOD, NET, OPT, PART, REF, ask, load


class Production(VoiceoverScene):
    def construct(self):
        self.card()
        self.record()
        self.more()
        self.validation(load("calib"), load("hedge"), load("calib_noise"))
        self.known(load("bsde_seeds"), load("stopping"), load("hedge"), load("drift"))

    def card(self):
        c = chapter_card(17, r"Production and model risk", r"What has to be true before a network trades?", part=PART)
        with self.voiceover("Chapter seventeen. Production and model risk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def record(self):
        cards = VGroup(
            firm_card(r"J.P. Morgan", r"Hans Buehler's team has hedged vanilla index option books on the S\&P 500 and "
                      r"the Euro Stoxx with a data-driven engine since 2018, and later priced a large share of its "
                      r"Euro Stoxx vanilla book with deep hedging and extended it to cliquets. Buehler was Risk's quant of "
                      r"the year for 2022, and later moved to XTX Markets.",
                      source=r"as reported by Risk.net", width=6.1, font_size=20),
            firm_card(r"Danske Bank", r"Brian Huge and Antoine Savine developed differential machine learning (chapter 4) "
                      r"at the bank, where adjoint differentiation already ran in production: the pathwise derivatives it "
                      r"computed became training labels. Risk.net reported the bank using the method to speed up its XVA "
                      r"calculations.", source=r"Huge and Savine (2020); as reported by Risk.net", width=6.1, font_size=20),
        ).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 0.6)
        sr = history_card(2026, r"SR 26-2, Federal Reserve, OCC and FDIC",
                          r"US supervisory guidance on model risk, 17 April 2026, superseding SR 11-7 (2011) and SR 21-8. Every model is "
                          r"challenged by people independent of its builders (``effective challenge''), validated for "
                          r"conceptual soundness, monitored, tested on outcomes and kept in an inventory, with effort scaled "
                          r"to the model's materiality. Generative and agentic AI are outside its scope; a pricing or hedging network "
                          r"is a model like any other.",
                          color=QC.HOUSE, width=12.4, font_size=20)
        sr.next_to(cards, DOWN, buff=0.35)
        with self.voiceover(
            "What has reached real desks? The clearest public case is J.P. Morgan. As Risk.net reported, Hans "
            "Buehler's team has hedged vanilla index option books on the S&P 500 and the Euro Stoxx with a data-driven "
            "engine since 2018; the bank later priced a large share of its Euro Stoxx vanilla book with a version of "
            "deep hedging, and extended the programme to cliquets. <bookmark mark='a'/> At Danske Bank, "
            "Brian Huge and Antoine Savine turned the derivatives that adjoint differentiation already computed in "
            "production into training labels; Risk.net reported the method speeding up the bank's valuation "
            "adjustments. <bookmark mark='b'/> And over all of "
            "it sits the regulator. On the seventeenth of April 2026 the Federal Reserve, the OCC and the FDIC "
            "replaced SR 11-7, the model risk guidance of 2011, with SR 26-2: every model challenged by people who did "
            "not build it, checked for soundness, monitored, tested on outcomes and kept in an inventory. Generative "
            "and agentic AI are outside its scope; a network that prices or hedges is squarely inside it."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(sr, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def more(self):
        cs = VGroup(
            firm_card(r"Quantum deep hedging", r"Cherrat, Raj, Kerenidis, \dots, Wood, \dots, Pistoia (2023), with J.P. "
                      r"Morgan researchers: deep hedging with quantum networks on a trapped-ion processor, circuits of up "
                      r"to 16 qubits; comparable performance with fewer trainable parameters", source=r"\textit{Quantum} 7, "
                      r"1191", width=4.1, font_size=16, kind=r"Method"),
            firm_card(r"Deeply learning derivatives", r"Ferguson and Green (2018): a network trained on randomly generated "
                      r"basket-call valuations, ``a million times faster'' than the traditional model, as the authors "
                      r"claim", source=r"arXiv 1809.02233", width=4.1, font_size=16, kind=r"Method"),
            firm_card(r"PRA SS1/23", r"UK model risk principles for banks with internal-model approval: published 17 May "
                      r"2023, in force 17 May 2024, revised 23 April 2026; covers the use of artificial intelligence and "
                      r"machine learning in models", source=r"Bank of England", width=4.1, font_size=16, kind=r"Rule"),
        ).arrange(RIGHT, buff=0.2).shift(UP * 0.3)
        for c_ in cs:
            c_[0].set_stroke(GREY_C)
        with self.voiceover(
            "Three more entries. In 2023 a team including J.P. Morgan researchers ran deep hedging with quantum "
            "networks on a trapped-ion processor: comparable performance with fewer parameters, research, not "
            "deployment. <bookmark mark='a'/> In 2018 Ryan Ferguson and Andrew Green reported a network valuing basket "
            "calls a million times faster than the traditional model, as the authors claim. <bookmark mark='b'/> And in Britain, the Prudential Regulation Authority's "
            "supervisory statement SS1/23, in force since May 2024 and revised in April 2026, sets model risk "
            "principles for banks with internal-model approval, and names artificial intelligence and machine "
            "learning explicitly."
        ) as vo:
            self.play(FadeIn(cs[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cs[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cs[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def validation(self, c, h, nz):
        ev = h["nocost"]["eval"]
        bsd = h["nocost"]["bs_eval"]
        rows = [
            (r"conceptual soundness", r"every method derived before it is trained: indifference prices, BSDEs, the "
             r"bang-bang rule, the band (chapters 8, 10, 11, 13)", GOOD),
            (r"inside the box it learned", rf"the calibrator against fresh simulation: {nz['net_fresh']['rmse']:.2f} vol "
             rf"points on parameter sets it never saw (chapter 3)", GOOD),
            (r"outside the box, silence", r"a network extrapolates without warning; inputs are checked against the "
             r"training ranges and anything outside goes to the slow engine (chapters 4 and 5)", BAD),
            (r"outcomes against known answers", rf"no costs: the deep hedger's price {ev['price']:.2f} against delta "
             rf"hedging's {bsd['price']:.2f}; the BSDE's linear check (chapters 9 and 11)", NET),
            (r"the simulator is the model", r"hedgers tested on other generators and on replayed history (chapter 19); "
             r"the generator is validated too (chapter 16)", BAD),
            (r"monitoring and inventory", r"every network re-checked nightly against Part 16's engine; each one listed, "
             r"with its owner, its box and its materiality", GOOD),
        ]
        tab = VGroup()
        for a, b, col in rows:
            tab.add(VGroup(label(a, font_size=22, color=col), wrapped_label(b, 7.6, 19, GREY_A)).arrange(RIGHT, buff=0.5,
                                                                                                       aligned_edge=UP))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        for r_ in tab:
            r_[1].set_x(r_[0].get_left()[0] + 4.6 + r_[1].width / 2)
        head = label(r"SR 26-2's checklist, applied to this part's networks", font_size=32).to_edge(UP, buff=0.4)
        tab.next_to(head, DOWN, buff=0.35)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        if tab.height > 6.3:
            tab.scale_to_fit_height(6.3)
        tab.set_x(0)
        with self.voiceover(
            "Take the guidance's checklist, line by line. Conceptual soundness: every method here was derived before "
            "it was trained. <bookmark mark='a'/> Performance where it "
            f"was trained: the calibrator sits {nz['net_fresh']['rmse']:.2f} vol points from fresh simulations of "
            "parameters it never saw. <bookmark mark='b'/> Outside that region it is not trusted: inputs are checked "
            "against the training ranges, and anything outside goes to the slow engine. <bookmark mark='c'/> Outcomes against known answers: with no costs, the "
            "deep hedger must rediscover Black–Scholes, and it does; the BSDE solver must reproduce Monte Carlo when "
            "default is switched off, and it does. <bookmark mark='d'/> For a hedger, the simulator is part of the "
            "model, so the hedger is tested on other generators and on history, which is chapter nineteen. And every "
            "network is monitored, checked each night against the engine of Part sixteen, and kept in the inventory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
            vo.wait_until("d")
            self.play(FadeIn(tab[4]), FadeIn(tab[5]))
        self.wait(0.5)
        self.clear_scene()

    def known(self, bs, st, h, d):
        t0 = bs["tail0"]
        tl = bs["tail_lin"]
        n = h["nocost"]
        devs = [r["dev"] for r in d["rows"]]
        rows = [
            (r"deep BSDE, with default", rf"{t0['mean']:.2f} \pm {t0['sd']:.2f}", rf"{bs['reference']:.3f}",
             r"multilevel Picard"),
            (r"deep BSDE, no default", rf"{tl['mean']:.2f} \pm {tl['sd']:.2f}", rf"{bs['no_default_mc']:.2f}", r"Monte Carlo"),
            (r"deep stopping, two assets", rf"{st['2']['lower']:.3f}", rf"{st['2']['reference']['binomial']:.3f}",
             r"binomial tree"),
            (r"deep hedger, no costs", rf"{n['eval']['price']:.3f}", rf"{n['bs_eval']['price']:.3f}", r"delta hedging"),
            (r"drift hedger, extra shares", rf"{np.mean(devs):.3f}", rf"{d['merton_atm']:.3f}", r"Merton (1969)"),
        ]
        head = VGroup(label(r"network", font_size=21, color=GREY_A), label(r"it says", font_size=21, color=GREY_A),
                      label(r"known answer", font_size=21, color=GREY_A), label(r"from", font_size=21, color=GREY_A))
        tab = VGroup(head)
        for a, b, c_, e in rows:
            tab.add(VGroup(label(a, font_size=22), MathTex(b, font_size=30, color=NET), MathTex(c_, font_size=30, color=REF),
                           label(e, font_size=20, color=GREY_B)))
        xs = [-4.4, -0.6, 2.4, 5.0]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.2 - 0.8 * i, 0])
        ttl = label(r"The part's known-answer scoreboard", font_size=30).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Here is the part's scoreboard of known answers, all from this part's own runs. The deep BSDE against "
            "multilevel Picard, and against Monte Carlo without default. Deep stopping against a binomial tree. The "
            "deep hedger against delta hedging. And the drift-trained hedger's extra shares against Merton's formula. "
            "<bookmark mark='a'/> Every network here earns its trust the same way: by agreeing with a slower, "
            "independent engine wherever such an engine exists."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.5, run_time=6))
            vo.wait_until("a")
        q = ask(r"under SR 26-2, is the market generator a model?")
        with self.voiceover(
            "A question: under the new guidance, is the market generator a model? Think about what the hedger is "
            "validated on."
            " Yes. It produces the paths the hedger is validated on, so it is part of the model and must be validated too: its stylized facts, held-out history, and more than one generator. Next: the frontier."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
