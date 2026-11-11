from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (BAD, GOOD, HURDLE, MID_C, NET_C, OFI_C, PART, comma, load)


class Deep(VoiceoverScene):
    def construct(self):
        d = load("deep")
        self.card()
        self.literature()
        self.architecture()
        self.universal()
        self.benchmark()
        self.labels()
        self.design(d)
        self.results(d)
        self.why_high(d)
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(6, r"Deep order books", r"Can a network read the book better than a formula?", part=PART)
        with self.voiceover("Chapter six. The order book is a large, structured, fast-arriving stream of numbers: exactly "
                            "what deep learning is supposed to be good at. Since twenty seventeen, dozens of papers have "
                            "fed it to networks. What did they find, and what do we find?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def literature(self):
        cards = VGroup(
            desk_question(r"DeepLOB", r"Zhang, Zohren and Roberts (2019): convolutions over ten levels of prices and "
                          r"sizes, an inception module and an LSTM, predicting whether the smoothed mid rises, falls or "
                          r"stays; strong results on the FI-2010 benchmark and on London stocks", width=12.4, font_size=18),
            desk_question(r"universal features", r"Sirignano and Cont (2019): one LSTM trained on hundreds of US stocks "
                          r"together forecast the direction of the next move better than models fitted stock by stock, "
                          r"including on stocks it never saw: price formation looks universal", width=12.4, font_size=18),
            desk_question(r"order-flow inputs", r"Kolm, Turiel and Westray (2023): the same networks do better on "
                          r"order-flow imbalances than on raw book levels (Chapter 4)", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three results the field builds on. <bookmark mark='a'/> DeepLOB, by Zihao Zhang, Stefan Zohren and Stephen "
            "Roberts: convolutions over ten levels of prices and sizes, then a recurrent network, predicting whether a "
            "smoothed mid will rise, fall or stay. <bookmark mark='b'/> Justin Sirignano and Rama Cont trained one network "
            "on hundreds of American stocks together. It beat models fitted stock by stock, even on stocks it never saw: "
            "the mechanics of price formation look universal. <bookmark mark='c'/> And the input matters: the same "
            "networks do better when fed order-flow imbalances than raw book levels."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def architecture(self):
        rows = [cmath(r"x", r"\in", r"\mathbb R^{100 \times 40}", font_size=40, colors={r"x": NET_C}),
                cmath(r"\text{conv}", r":", r"\text{price with size, then bid with ask, then across levels}", font_size=30),
                cmath(r"\text{inception} \to \text{LSTM}", r":", r"\text{several time scales, then memory}", font_size=32),
                cmath(r"\hat y", r"\in", r"\{\text{down}, \text{flat}, \text{up}\}", font_size=38)]
        whys = [why(r"the last 100 book events, each with ten levels of price and size on both sides"),
                why(r"the first convolutions pair each level's price with its size, then each bid level with its ask "
                    r"level, then summarise the ten levels: the structure of a book, built into the filters"),
                why(r"parallel filters of different widths look at different time scales; a recurrent layer of 64 "
                    r"units carries information across the window"),
                why(r"a three-way classification of the coming mid move, scored by accuracy and F1")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "What DeepLOB sees, and how. <bookmark mark='a'/> The last hundred book events, each with ten levels of "
            "price and size on both sides: four thousand numbers. <bookmark mark='b'/> The first convolutions pair each "
            "level's price with its size, then each bid with its ask, then summarise the levels: the structure of a book "
            "built into the filters. <bookmark mark='c'/> Then parallel filters of different widths for different time "
            "scales, and a recurrent layer that carries memory across the window. <bookmark mark='d'/> The output is "
            "down, flat or up."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def universal(self):
        cards = VGroup(
            desk_question(r"universal", r"one model for all stocks beat a model per stock, on stocks in the sample and "
                          r"on stocks outside it: the network learned something about books, not about tickers",
                          width=12.4, font_size=19),
            desk_question(r"stationary", r"trained on earlier years, it kept its accuracy on later months without "
                          r"refitting: the relation between book and next move changed slowly", width=12.4, font_size=19),
            desk_question(r"path-dependent", r"longer histories of the book improved the forecast: price formation has "
                          r"memory, which a model of the current state alone cannot capture (the research chapter)",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"What Sirignano and Cont found, in more detail", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "What Sirignano and Cont found, in more detail, because it is the strongest positive result. "
            "<bookmark mark='a'/> Universality: one model for all stocks beat a model per stock, even on stocks it had "
            "never seen. <bookmark mark='b'/> Stationarity: trained on earlier years, it kept its accuracy on later "
            "months without refitting. <bookmark mark='c'/> And path-dependence: longer histories of the book improved "
            "the forecast. Price formation has memory, which a model of the current state alone cannot capture. The "
            "research chapter meets the same fact from the other side."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def benchmark(self):
        rows = [cmath(r"\text{FI-2010}", r":", r"\text{5 Finnish stocks},\ 10\ \text{days}", font_size=36),
                cmath(r"\text{LOBCAST}", r":", r"15\ \text{models, retrained and retested}", font_size=36,
                      colors={r"\text{LOBCAST}": HURDLE}),
                cmath(r"\text{new stocks}", r"\Rightarrow", r"\text{a large drop for every model}", font_size=36,
                      colors={r"\text{a large drop for every model}": BAD})]
        whys = [why(r"Ntakaris et al. (2018): the public benchmark most papers report on, from Nasdaq Nordic in 2010"),
                why(r"Prata et al. (2024): fifteen published deep order-book models, rerun in one open framework"),
                why(r"most overfitted FI-2010; on other stocks and periods all of them did markedly worse, which raises "
                    r"the question of their use in real markets")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Then the benchmark. <bookmark mark='a'/> Most papers report on one public data set, ten days of five "
            "Finnish stocks from twenty ten. <bookmark mark='b'/> Matteo Prata and colleagues reran fifteen published "
            "models in one open framework. <bookmark mark='c'/> On data the models had not been tuned on, every one of "
            "them did markedly worse; most had overfitted the benchmark. Part twenty-six's lesson, at the speed of "
            "milliseconds."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def labels(self):
        rows = [cmath(r"\ell_t", r"=", r"\frac{\bar m_{t+1..t+k} - m_t}{m_t}", font_size=40),
                cmath(r"\text{class}", r"=", r"\text{up if } \ell_t > \alpha,\ \text{down if } \ell_t < -\alpha,\ "
                      r"\text{else flat}", font_size=30),
                cmath('\\text{label accuracy}', r"\ne", '\\text{executable profit}', font_size=40, colors={'\\text{executable profit}': BAD})]
        whys = [why('one future-only smoothing variant; FI-2010/DeepLOB definitions can compare past and future average mids'),
                why(r"the threshold $\alpha$ sets how many examples are flat, and so what accuracy a constant guess gets"),
                why('smoothing, thresholds and overlapping windows change the task and dependence; label accuracy is not an executable return')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Specify the exact label before comparing models. <bookmark mark='a'/> The displayed equation is a future-average-versus-current-mid variant. Common FI-twenty-ten and DeepLOB definitions instead compare backward and forward average mids. Their normalization and window conventions must be stated. <bookmark mark='b'/> The threshold determines the flat class and the class base rates, changing a constant-class benchmark. <bookmark mark='c'/> Smoothing and overlapping windows alter noise, dependence and the prediction target; they are not universally easier in every information set. Label accuracy does not become an executable return. Our restored baseline uses a plain future mid change in ticks."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def design(self, d):
        ntr = d["1 s"]["n_train"]
        nte = d["1 s"]["n_test"]
        rows = [cmath(r"x_t", r"=", r"\big(\tfrac{\text{OFI}}{\text{depth}},\ \Delta M,\ I - \tfrac12\big)_{t-9..t}",
                      font_size=36, colors={r"x_t": OFI_C}),
                cmath(r"y_t", r"=", r"(M_{t+h} - M_t)/\text{tick},\quad h = 1\ \text{s},\ 10\ \text{s}", font_size=34),
                cmath(r"\text{models}", r":", r"I_t\ \text{alone};\ \text{linear};\ \text{network } 64{\times}32,\ 3\ "
                      r"\text{seeds}", font_size=30, colors={r"\text{models}": NET_C})]
        whys = [why(r"thirty numbers every second: ten seconds of scaled imbalance, mid changes and queue imbalance"),
                why(rf"the next mid change in ticks; {comma(ntr)} training seconds (16--17 May), {comma(nte)} test seconds "
                    r"(20--21 May)"),
                why('OLS fits all training data; network fits the first four fifths and validates on the last fifth; overlapping labels are not purged')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The comparison we actually run. <bookmark mark='a'/> Every nominal second, thirty inputs: ten lagged OFIs divided by current depth, ten mid changes, and ten imbalances. No spread feature enters this implementation. <bookmark mark='b'/> The target is a plain one- or ten-second mid change in ticks. The first two archive days train; the weekend days test. <bookmark mark='c'/> Linear fits use all training observations. The network fits the first eighty percent, validates on the last twenty, and averages three fixed seeds. Horizon labels can overlap the validation boundary; there is no purged split. Training scores therefore use unequal fitting samples and the setup is a small baseline, not a replication of DeepLOB."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def results(self, d):
        hx = [-4.6, -2.0, 0.4, 2.8, 5.2]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"horizon", r"model", r"train $R^2$", r"test $R^2$",
                                                                         r"test direction")])
        tab = VGroup(head)
        names = {"imbalance": r"imbalance alone", "linear": r"linear, 30 inputs", "network": r"network, 30 inputs"}
        for h in ("1 s", "10 s"):
            for k in ("imbalance", "linear", "network"):
                r = d[h][k]
                col = NET_C if k == "network" else (MID_C if k == "linear" else GREY_A)
                tab.add(VGroup(label(h, font_size=18), label(names[k], font_size=18, color=col),
                               MathTex(f"{100 * r['train_r2']:.1f}\\%", font_size=24),
                               MathTex(f"{100 * r['test_r2']:.1f}\\%", font_size=24),
                               MathTex(f"{100 * r['test_acc']:.1f}\\%", font_size=24, color=col)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.5 - 0.62 * j, 0])
        foot = wrapped_label(r"direction: the share of seconds with a mid move whose sign the model got right", 11.5, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        n1, l1 = d["1 s"]["network"]["test_acc"], d["1 s"]["linear"]["test_acc"]
        i1 = d["1 s"]["imbalance"]["test_acc"]
        n10, l10 = d["10 s"]["network"]["test_acc"], d["10 s"]["linear"]["test_acc"]
        r10 = d["10 s"]["linear"]["test_r2"]
        with self.voiceover(
            f"""Direction scores on nonzero future moves. <bookmark mark='a'/> At one second, imbalance alone scores {100 * i1:.0f} percent, the thirty-input linear fit {100 * l1:.0f}, and the network {100 * n1:.0f}. <bookmark mark='b'/> At ten seconds, the linear fit scores {100 * l10:.0f} and the network {100 * n10:.0f}. These particular network specifications do not win this direction comparison. The best displayed ten-second R squared is {100 * r10:.1f} percent. Accuracy is conditional on excluding flat targets, whereas R squared uses all targets. Neither statistic is a net-profit measure, and no robust comparison interval is estimated."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[4:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def why_high(self, d):
        e = load("edge")
        tr = d["1 s"]["linear"]["train_acc"]
        te = d["1 s"]["linear"]["test_acc"]
        big = e["by_size"][-1]
        t1 = e["trade"][1]
        per_bp = 1 / e["tick_bp"]
        cards = VGroup(
            desk_question(r"high accuracy, tiny $R^2$", rf"{100 * e['zero']:.0f}\% of seconds have no move; when the mid "
                          rf"does move, the linear rule calls the direction, even for jumps of five ticks or more "
                          rf"({100 * big['acc']:.0f}\%), but not the size", width=12.4, font_size=19),
            desk_question(r"not money", rf"trading the forecast's sign whenever it exceeds a tick captures "
                          rf"{t1['gain']:.1f} ticks of mid change per second traded; the spread costs a tick, and taker fees "
                          rf"of a few basis points cost far more: one basis point is about {per_bp:.0f} ticks",
                          width=12.4, font_size=19),
            desk_question('different sample conditions', f"training direction accuracy {100 * tr:.0f}\\%, test {100 * te:.0f}\\%; higher test scores coincide with different weekend conditions, without identifying their cause",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            f"""Interpret each statistic by its conditioning. <bookmark mark='a'/> About {100 * e['zero']:.0f} percent of future one-second targets are zero. The large-realized-move bin has {100 * big['acc']:.0f} percent sign accuracy, but future move size is unavailable at decision time: this is retrospective stratification, not a tradable filter. <bookmark mark='b'/> Selecting forecast magnitude above one tick gives signed mid-to-mid gain of {t1['gain']:.1f} ticks per selected observation. It omits executable entry and exit prices, inventory, overlap, latency and fees; one basis point is about {per_bp:.0f} ticks. Choosing among thresholds using these test scores would reuse the test sample. <bookmark mark='c'/> Test accuracy {100 * te:.0f} percent exceeds training accuracy {100 * tr:.0f}; a quieter weekend is one possible distribution change, not an identified explanation for the difference."""
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        rows = [cmath(r"\text{features}", r">", r"\text{architecture}", font_size=40, colors={r"\text{features}": GOOD}),
                cmath(r"\text{data}", r":", r"\text{many assets, many months}", font_size=38),
                cmath(r"\text{target}", r":", r"\text{after costs, at a horizon you can trade}", font_size=36,
                      colors={r"\text{target}": HURDLE})]
        whys = [why('this small comparison favors the linear sign baseline; capacity and generalization causes are not identified'),
                why('large multi-stock evidence does not guarantee a deep-model win in every setting'),
                why(r"smoothed three-class labels on a benchmark are not a strategy; score the trade, not the label")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Three bounded conclusions. <bookmark mark='a'/> In this short sample, simple book features and a linear baseline perform well on the chosen direction metric. That does not prove additional network capacity only fits noise. <bookmark mark='b'/> Large multi-stock studies offer evidence for other architectures and data scales; their results do not guarantee a deep-model win in every market. <bookmark mark='c'/> Report the label definition, nonzero conditioning, base rates, fitting split, all-target error and executable costs. A smoothed benchmark label, an accurate sign and a profitable strategy are different claims."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        head = label('Accuracy and execution costs answer different questions', font_size=29, color=QC.IDEA).to_edge(UP, buff=0.45)
        formula = MathTex('80/100\\ \\text{nonzero signs correct},\\quad G=1.5\\ \\text{ticks},\\quad s=1,\\quad f=3\\ \\text{ticks/side}', font_size=33).move_to(UP * 1.2)
        if formula.width > 12.4:
            formula.scale_to_fit_width(12.4)
        assumptions = wrapped_label('G is selected gross mid-to-mid gain; immediate market entry and exit each pay half-spread and a fee f.', 12.2, 20, GREY_A).move_to(DOWN * 0.1)
        question = wrapped_label('Compute conditional accuracy and the stipulated round-trip net gain. What does excluding flat targets change?', 12.2, 25, QC.IDEA).move_to(DOWN * 1.75)
        banner = label(r"Pause: derive the answer and check its assumptions and units.", font_size=19, color=QC.IDEA).to_edge(DOWN, buff=0.35)
        with self.voiceover('A model gets eighty of one hundred nonzero future signs correct, with flat targets excluded. Its selected gross mid-to-mid gain is one and a half ticks. Assume a one-tick spread at entry and exit and a three-tick fee per side. Compute conditional accuracy and net gain for immediate market entry and exit. Explain why flat-target conditioning and a fee-free mid markout answer different questions.'):
            self.play(FadeIn(head), FadeIn(formula), FadeIn(assumptions), FadeIn(question), FadeIn(banner))
        self.wait(6)
        self.clear_scene()
