from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, GOOD, NET, PART, load


class Production(VoiceoverScene):
    def construct(self):
        self.card()
        self.record()
        self.validation(load("calib"), load("hedge"))

    def card(self):
        c = chapter_card(11, r"Production and model risk", r"What has to be true before a network trades?", part=PART)
        with self.voiceover("Chapter eleven. Production and model risk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def record(self):
        cards = VGroup(
            firm_card(r"J.P. Morgan", r"Hans Buehler's team put data-driven hedging into production, starting in 2018 with "
                      r"vanilla index option books. By 2022, Risk.net reported, about 70\% of the bank's Euro Stoxx flow "
                      r"options were quoted and hedged by machine, with traders reviewing the orders, and deep hedging of "
                      r"Euro Stoxx 50 cliquets had gone live. Buehler was Risk's quant of the year for 2022.",
                      source=r"as reported by Risk.net, 2022", width=6.1, font_size=20),
            firm_card(r"Danske Bank", r"Brian Huge and Antoine Savine developed differential machine learning (chapter 4) "
                      r"at the bank, where adjoint differentiation already ran in production: the pathwise derivatives it "
                      r"computed became training labels. Risk.net reported the bank using the method to speed up its XVA "
                      r"calculations.", source=r"Huge and Savine (2020); as reported by Risk.net", width=6.1, font_size=20),
        ).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 0.6)
        sr = history_card(2026, r"SR 26-2, Federal Reserve, OCC and FDIC",
                          r"US supervisory guidance on model risk, replacing SR 11-7 (2011) in April 2026. Every model is "
                          r"challenged by people independent of its builders (``effective challenge''), validated for "
                          r"conceptual soundness, monitored, tested on outcomes and kept in an inventory, with effort scaled "
                          r"to the model's materiality. A pricing or hedging network is a model like any other.",
                          color=QC.HOUSE, width=12.4, font_size=20)
        sr.next_to(cards, DOWN, buff=0.35)
        with self.voiceover(
            "What has reached real desks? The clearest public case is J.P. Morgan. Hans Buehler's team began hedging "
            "vanilla index option books with a data-driven engine in 2018. By 2022, as Risk.net reported, about seventy "
            "percent of the bank's Euro Stoxx flow options were quoted and hedged by machine, with traders reviewing "
            "the orders, and deep hedging of Euro Stoxx cliquets had gone live. <bookmark mark='a'/> At Danske Bank, "
            "Brian Huge and Antoine Savine built differential machine learning where adjoint differentiation already "
            "ran in production: the derivatives it computed became training labels, and Risk.net reported the method "
            "speeding up the bank's valuation adjustments. <bookmark mark='b'/> And over all of "
            "it sits the regulator. American banking supervisors' guidance on model risk, SR 11-7 from 2011, revised in April "
            "2026 as SR 26-2, says that every model must be challenged by people who did not build it, checked for "
            "conceptual soundness, monitored, and tested on outcomes, with more scrutiny the more it matters. A neural "
            "network that prices or hedges is a model like any other."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(sr, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def validation(self, c, h):
        held = c["held_rmse"]
        noise = c["label_noise_rmse"]
        ev = h["nocost"]["eval"]
        bsd = h["nocost"]["bs_eval"]
        rows = [
            (r"inside the box it learned", rf"the calibrator's error on held-out parameter sets: {held:.2f} vol points, "
             rf"against Monte Carlo noise of {noise:.2f} in its own labels", GOOD),
            (r"outside the box, silence", r"a network extrapolates without warning: inputs are checked against the training "
             r"ranges, and anything outside falls back to the slow engine", BAD),
            (r"against a known answer", rf"with no costs the deep hedger must reproduce Black--Scholes: its price "
             rf"{ev['price']:.2f} against {bsd['price']:.2f} for delta hedging on the same paths", NET),
            (r"the simulator is the model", r"a hedger trained on one market generator is tested on others and on "
             r"replayed history; the generator gets validated too (chapter 10)", BAD),
            (r"every night", r"each network re-checked against the pricing engine of Part 16 on fresh samples; drift beyond "
             r"tolerance takes it out of service", GOOD),
        ]
        tab = VGroup()
        for a, b, col in rows:
            tab.add(VGroup(label(a, font_size=23, color=col), wrapped_label(b, 7.6, 20, GREY_A)).arrange(RIGHT, buff=0.5,
                                                                                                       aligned_edge=UP))
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 4.6)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        for r_ in tab:
            r_[1].set_x(r_[0].get_left()[0] + 4.6 + r_[1].width / 2)
        head = label(r"Validating a network, the SR 26-2 way", font_size=32).to_edge(UP, buff=0.5)
        tab.next_to(head, DOWN, buff=0.45)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        tab.set_x(0)
        with self.voiceover(
            "What does that mean for the networks of this part? First, they are checked where they were trained: the "
            f"calibrator's error on parameters it never saw is {held:.2f} vol points, below the noise of its own "
            "Monte Carlo labels. <bookmark mark='a'/> Second, outside that region they are not trusted at all: a "
            "network extrapolates without any warning, so inputs are checked against the training ranges, and "
            "anything outside goes back to the slow engine. <bookmark mark='b'/> Third, they must reproduce known "
            "answers: with no costs, the deep hedger has to rediscover Black–Scholes, and it does. "
            "<bookmark mark='c'/> Fourth, for a hedger the simulator is the model, so it is tested on other generators "
            "and on replayed history. And every night, each network is checked against the engine of Part sixteen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
        self.wait(0.5)
        self.clear_scene()
