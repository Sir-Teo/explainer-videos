from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import (BAD, GOOD, HURDLE, MODEL_A, MODEL_B, MODEL_C, NEG, PART, POS, WORD, YLD, comma,
                                         load)

DESK = [
    (r"Your LLM signal backtests at a Sharpe ratio of 4 on 2015--2020 news. What is the first thing you check?",
     r"the model's training cut-off: if it read 2015--2020, the backtest can be memory. Then anonymise the firms and "
     r"re-run (Glasserman--Lin), and finally use a model dated before 2015"),
    (r"A dictionary's net tone explains 30\% of statement-day yield moves, measured from the prior close. Tradable?",
     r"no: the move happened in the minutes after release. Measure from just after the release, or predict a later "
     r"window, and the explanation must survive as a forecast"),
    (r"`Unemployment' is the most counted negative word in FOMC statements. Fix the dictionary?",
     r"remove mandate words for this genre, or better, learn the weights from outcomes (SESTM) and check that the "
     r"learned list beats chance out of sample"),
    None,  # built from the computed screen in Outro.desk
    (r"A satellite data set's buyers double every year. How long is it worth buying?",
     r"in a Kyle market each buyer's profit falls like $N^{-3/2}$: doubling cuts it by $2^{1.5} \approx 2.8$ a year. "
     r"Buy early, and measure the decay live"),
    (r"A general LLM beats your fine-tuned FinBERT on headlines in 2024 data. Switch?",
     r"only with a model dated before your test period, a fixed version, and costs; and keep the small model for "
     r"narrow labelled tasks, where specialists still win"),
]

PROBLEMS = [
    r"Show that cosine similarity of tf-idf rows does not change when every count in a document is doubled.",
    r"Zipf with frequency $\propto 1/r$ over $V = 10{,}000$ words: what share of tokens do the top 100 words cover?",
    r"A 300-word statement has 6 negative and 3 positive words. Its net tone? And if `unemployment' (2 of the 6) is "
    r"dropped from the negative list?",
    r"300 words each appear in exactly 10 statements; the labels are fair coin flips. How many pass $|f_j - \frac12| "
    r"\ge 0.2$?",
    r"Show that SESTM's penalty $\lambda\log p(1 - p)$ is a $\text{Beta}(\lambda + 1, \lambda + 1)$ prior on $p$.",
    r"Show that $\mathrm{PMI}(w, c) = \log P(c \mid w)/P(c)$ is zero for independent words, and why PPMI drops negatives.",
    r"Compute the fog index of: `The Committee decided today to keep its target for the federal funds rate unchanged.'",
    r"A model's loss is 3.5 nats per token, with 4.2 characters per token. Bits per character?",
    r"In sample, named headlines give a Sharpe ratio of 1.2 and anonymised ones 1.5. What does Glasserman--Lin's "
    r"decomposition say?",
    r"Kyle with $N$ informed buyers: from 4 to 9 buyers, by what factor does each one's profit fall, and the total?",
    r"(qual) For increasing $g, q$ on $[0, 1]$ and $p$ any distribution, prove $\operatorname{Cov}(g(p), q(p)) \ge 0$. "
    r"Deduce the limits of $f_j$ for positive, negative and neutral words in SESTM's model.",
    r"(qual) Kyle (1985) with $N$ symmetric insiders sharing $v$: derive $\beta$, $\lambda$, each insider's profit, and "
    r"show $\operatorname{Var}(v \mid p) = \sigma_v^2/(N + 1)$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("corpus"), load("tone"), load("form"), load("sestm"), load("topics"), load("embed"),
                   load("lookahead"), load("altdata"), load("envelope"), load("theory"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, c, t, f, s, tp, e, la, a, env, th):
        items = [
            (rf"words as numbers: {c['n_statements']} statements and {c['n_minutes']} minutes, Zipf's slope "
             rf"{c['zipf_slope']:.2f}", WORD),
            (r"dictionaries: Harvard misread 10-Ks; Loughran--McDonald misreads a central bank's mandate", NEG),
            (rf"tone against the two-year yield: $t = {t['regs']['net']['t']:.2f}$; words move yields through the path "
             r"of policy, not their mood", YLD),
            (rf"the statement grew from {f['first5']:.0f} to {f['last5']:.0f} words; its phrases about the future "
             r"carry the news", WORD),
            (rf"SESTM on statements: {s['rho_train']:.2f} in sample, {s['rho']:.2f} out", HURDLE),
            (r"topics in thirty years of minutes are eras: aggregates, firming, facilities, purchases, repo", WORD),
            (rf"embeddings: tightening $-$ raise $+$ lower $=$ {e['analogies'][0]['best'][0] if e['analogies'] else '?'}",
             GOOD),
        ]
        items2 = [
            (r"FinBERT and transformers read context; a pocket LM learns the committee's prose on a CPU", MODEL_A),
            (r"LLMs read headlines and statements; only large models predict", WORD),
            (r"look-ahead: memory and distraction; tests that catch leaks; dated models", BAD),
            (rf"the time-sliced experiment: bits per character on 2008--12, A {la['A']['bpc_test']:.2f}, "
             rf"C {la['C']['bpc_test']:.2f}, B {la['B']['bpc_test']:.2f}", MODEL_C),
            (r"agents: an org chart of prompts, with thin evidence", GREY_A),
            (r"alternative data: each buyer's profit falls like $N^{-3/2}$; satellites widened the gap", GOOD),
            (rf"the statement score on 2021--25: {env['row']['holdout']['sharpe']:.2f} $\pm$ "
             rf"{env['row']['holdout']['sharpe_se']:.2f}; the counter {comma(env['trials'])}", QC.HOUSE),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 28 in fourteen lines")
        with self.voiceover(
            "Part twenty-eight in fourteen lines. Words become counts in a matrix, and their frequencies follow Zipf's "
            "law. Dictionaries are fitted to a genre: the psychologists' list misread annual reports, and the finance "
            "list misreads a central bank, whose mandate words count as bad news. The dictionary's tone said nothing "
            "about the bond market's reaction, because statements move yields through what they imply about the path "
            "of policy. The statement grew from a paragraph into the policy instrument, and its phrases about the "
            "future carry the news. Words learned from outcomes fitted the past and did not travel. Topic models found "
            "eras, and embeddings learned that easing is the opposite of tightening."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 28 in fourteen lines")
        with self.voiceover(
            "Transformers read words in context, and a small one learned the committee's prose on an ordinary "
            "computer. Large language models read headlines and financial statements well, and only the large ones. "
            "But a model that read the future can remember it; tests can catch some leaks, and dated models avoid "
            "them. Our own experiment measured the gap. Trading agents are an organisation chart of prompts, with "
            "little evidence yet. A data set's value falls fast as it spreads. And the statement score, opened on the "
            "sealed years, was a coin, honestly counted."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        d = load("theory")["data"]
        DESK[3] = (rf"Your screen keeps {d['n_real']} words from {d['n']} documents. How do you know they are not noise?",
                   rf"shuffle the labels and screen again: here {d['null_mean']:.0f} words on average, $p = {d['p_perm']:.2f}$. "
                   r"Or use a word-by-word threshold $z\sqrt{\pi(1 - \pi)/k_j}$ with $z \approx \sqrt{2\log m}$")

        def page(qs):
            cards = VGroup(*[desk_question(q, a_, width=12.4, font_size=20) for q, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. A language-model signal with a Sharpe ratio of four on 2015 to 2020 news: check the "
            "model's training cut-off first, then anonymise, then use a model dated before 2015. "
            "<bookmark mark='a'/> A tone score that explains the day's move from the prior close is explaining, not "
            "forecasting. <bookmark mark='b'/> And a mandate word counted as negative calls for a genre-specific "
            "list, or better, weights learned from outcomes and checked out of sample."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        cards = page(DESK[3:])
        with self.voiceover(
            f"{d['n_real']} words from {d['n']} documents: shuffle the labels and screen again before "
            "believing any of them. <bookmark mark='a'/> A data set whose buyers double each year loses almost two "
            "thirds of each buyer's edge every year. <bookmark mark='b'/> And a general model that beats your "
            "specialist on recent data must be dated before the test before you switch. Full solutions are in the "
            "notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: tf-idf and document length; how much of a corpus Zipf's head covers; net tone and a "
            "mandate word; how many words pass a screen by chance; SESTM's penalty as a prior; pointwise mutual "
            "information; a fog index by hand; bits per character; reading Glasserman and Lin's decomposition; and the "
            "arithmetic of a shared data set. Then two qualifying-exam problems: Chebyshev's association inequality "
            "and the screening limits, and Kyle's market with many insiders. Solutions, in English and Chinese, are in "
            "the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"LLM agents as alpha miners, against the counter", [29]),
            (r"text features in the portfolio and the risk model", [30, 31]),
            (r"Kyle's informed traders, derived; who trades with whom", [35]),
            (r"the finale: the statement score's row, deflated by the full count", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part twenty-nine turns language models into alpha miners, and counts every formula "
            "they try. Parts thirty and thirty-one put text features into portfolios and risk models. Part thirty-five "
            "derives Kyle's informed trader, whose crowding we used here. And the finale deflates the statement "
            "score's row with everything else."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Gentzkow, Kelly and Taddy, `Text as data', \textit{Journal of Economic Literature} (2019); Kelly and Xiu, "
             r"\textit{Financial Machine Learning} (2023), the text chapter; Jurafsky and Martin, \textit{Speech and "
             r"Language Processing}"],
            [r"Stone et al.\ (1966); Gunning (1952); Kyle (1985); Admati and Pfleiderer (1988); Kuttner (2001); "
             r"Antweiler and Frank (2004); Tetlock, Saar-Tsechansky and Macskassy (2008); Meade and Stasavage (2008); "
             r"Araci (2019); Zhu (2019); Cohen, Malloy and Nguyen (2020); Shapiro and Wilson (2022); Gorodnichenko, Pham "
             r"and Talavera (2023); Hansen and Kazinnik (2023); Cao, Jiang, Wang and Yang (2024); "
             r"G\"urkaynak, Sack and Swanson (2005); Tetlock (2007); Loughran and McDonald (2011, 2014); Mikolov et al.\ "
             r"(2013); Levy and Goldberg (2014); Vaswani et al.\ (2017); Hansen, McMahon and Prat (2018); Ke, Kelly and "
             r"Xiu (2019); Chen, Kelly and Xiu (2022)",
             r"Huang, Wang and Yang (2023); Wu et al.\ (2023); Li et al.\ (2023); Lopez-Lira and Tang (2023); Glasserman "
             r"and Lin (2023); Bybee, Kelly, Manela and Xiu (2024); Kim, Muhn and Nikolaev (2024); Sarkar and Vafa "
             r"(2024); Xiao et al.\ (2024); He, Lv, Manela and Wu (2025); Katona, Painter, Patatoukas and Zeng (2025). "
             r"Data: the Federal Reserve Board; FRED; the Loughran--McDonald dictionary (sraf.nd.edu)"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from the General Inquirer in 1966 to the "
            "first chronologically consistent language models. Every number on screen was computed by the House's code "
            "from public documents and yields, with simulations labelled as such."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("research",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 29, Alpha Mining and Automated Research", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House now has a reading room: tools to turn the committee's words into features, a rule that stamps "
            "every word with the moment it became public, and the habit of asking what a model has already read. "
            "<bookmark mark='a'/> Next, Part twenty-nine: alpha mining and automated research. Machines that search "
            "millions of formulas for signals, language models that write their own research, and a trial counter "
            "that has to keep up."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
