from __future__ import annotations

import numpy as np
from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import PART, RISKY, BAD, GOOD, LOGIT, GBMC, load, lesson_cards


class Defaults(VoiceoverScene):
    def construct(self):
        self.records()
        self.target()
        self.availability()
        self.answer()

    def records(self):
        title, cards = lesson_cards('7. What does a bankruptcy filing count?', [
            ('A public reporting event', 'Form 8-K Item 1.03: bankruptcy or receivership; reporting date differs from the event date'),
            ('Coverage and duplicates', 'Private issuers, reporting exemptions, repeat filings and entity identifiers change the count'),
            ('Counts need a denominator', 'A filing count divided by no defined population is not a default probability'),
            ('This reconstruction', 'The SEC search failed twice. No annual count or correlation is certified here.'),
        ])
        with self.voiceover("Chapter seven. Before fitting a default model, define what a label means. Item one point zero three of Form eight K reports bankruptcy or receivership. Its filing date can differ from the legal event date. A bankruptcy filing is also narrower than many credit definitions of default, which can include missed payments or distressed exchanges. <bookmark mark='a'/> Searching filings requires coverage checks and deduplication. One company can submit several reports about the same episode, while separate legal entities can share an economic parent. Some companies never file this form. <bookmark mark='b'/> A count has no at-risk denominator and cannot by itself estimate an annual default probability. The original search failed, and one retry after a successful endpoint diagnostic also failed. We retain both failures and show no reconstructed annual counts or spread correlations. Public access alone would not validate the search or turn the resulting labels into a complete population.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()

    def target(self):
        title, cards = lesson_cards('A forecast target needs an observation clock', [
            ('Population', 'Identify obligors alive and at risk at the forecast date; document entry, exit and censoring'),
            ('Event and horizon', 'Choose bankruptcy, payment default or another event; define the next twelve months precisely'),
            ('Information set', 'Use actual publication dates and historical versions, with missingness known at that date'),
            ('Assessment', 'Temporal separation, issuer dependence, event counts and uncertainty belong beside every score'),
        ])
        with self.voiceover("A usable prediction problem has a population, an event, a horizon and an information set. Specify which obligors are alive and at risk at the forecast date, and how mergers, delistings, repeat defaults and incomplete follow-up are handled. <bookmark mark='a'/> Then define the event and its window. A twelve-month bankruptcy filing label is a different target from a bond payment default within a year. Delayed reports near the boundary can change which window contains an event. <bookmark mark='b'/> Every feature needs a publication date and a historical version. Later restatements and accounts published after the forecast date cannot enter that forecast. Assessment also needs chronological separation and a method for uncertainty that respects repeated issuers and shared macroeconomic shocks. A large row count is not the same as a large number of independent defaults.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()

    def availability(self):
        title, cards = lesson_cards('Accounts are not automatically point in time', [
            ('Current-vintage XBRL frames', 'A convenient cross-section can contain later revisions and fiscal/calendar mismatches'),
            ('A three-month lag', 'An assumed delay is not evidence of the actual filing date or historical availability'),
            ('Public float', 'Non-affiliate market value differs from total equity market capitalization'),
            ('Example boundary', 'The legacy joined firm-year experiment stays closed; the next lesson uses invented samples'),
        ])
        with self.voiceover("An accounting database needs an availability audit. Current XBRL frames make it convenient to collect one accounting concept across companies, but convenience does not establish what was known historically. Restatements, fiscal-year differences and tagging choices matter. <bookmark mark='a'/> Adding a fixed three-month lag does not prove the annual report was public on the assumed day. The actual release and filing timestamps must be checked, with the version that was available then. Public float measures shares held by non-affiliates at a specified date; it is not automatically the total market value of equity at the fiscal year end. <bookmark mark='b'/> This review does not access the legacy joined firm-year experiment or report its model scores. We will use independent samples from a declared synthetic population to demonstrate fitting, model selection, ranking and calibration. Those results teach a procedure and provide no evidence about real issuer forecasting.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()

    def answer(self):
        title, cards = lesson_cards('Pause, then check the label', [
            ('Question', 'Why can an 8-K search undercount defaults and overcount bankruptcies?'),
            ('Undercount', 'Coverage gaps, missed matches, non-reporting obligors and non-bankruptcy default events'),
            ('Overcount', 'Repeated reports, amendments, multiple entities and keyword false positives'),
            ('Repair', 'Validate a sample against legal event records; define episodes and the at-risk population'),
        ])
        with self.voiceover("Pause and predict. Why can a search of bankruptcy filings undercount defaults and overcount bankruptcies? <bookmark mark='a'/> It can miss non-reporting companies, poorly matched reports and credit events that never become bankruptcy cases. <bookmark mark='b'/> It can also count repeated reports, amendments or several entities from one economic group, and a keyword search can return false positives. The repair is an explicit event rule, a deduplication rule, a validated sample and a defined population at risk. Do not divide a filing count by a convenient but unrelated issuer count and call it a probability.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()
