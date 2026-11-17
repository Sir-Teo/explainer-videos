from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403


class StageOne(VoiceoverScene):
    def construct(self):
        card_section(self, 4, r"The registered report, \ Stage 1", r"What must be fixed before the data are "
                     r"analysed?", marr=("what",))
        self.theory()
        self.plan()

    def theory(self):
        rows_section(self, r"Theory and hypotheses", [
            (r"theory: \ Part 59's reliability paradox: \ an effect almost everyone shows may leave little "
             r"difference between people to measure; \ a slope, \ like a difference, \ doubles trial noise", WHITE),
            (r"H1, \ the risky prediction: \ the split-half reliability of a person's rotation slope is below 0.70",
             AUTH),
            (r"H2, \ the corollary: \ a person's mean time on the same trials is more reliable than the slope", MODEL),
            (r"the alternative: \ rotation speed is a stable spatial ability (Part 32): \ reliability 0.70 or more",
             GOOD),
        ], "What must be fixed before the data are analysed? First the theory and hypotheses. <bookmark mark='a'/> "
           "The theory is Part 59's reliability paradox: an effect almost everyone shows may leave little "
           "difference between people to measure, and a slope, like a difference, doubles trial noise. "
           "<bookmark mark='b'/> H1, the risky prediction: the split-half reliability of a person's rotation slope "
           "is below zero point seven. <bookmark mark='c'/> H2, the corollary: a person's mean time on the same "
           "trials is more reliable than the slope. <bookmark mark='d'/> And the alternative: rotation speed is a "
           "stable spatial ability, Part 32's subject, with a reliability of zero point seven or more.")

    def plan(self):
        d = load("plan")
        rows_section(self, r"The plan, \ as code", [
            (r"data: \ Ganis and Kievit's open study, \ 54 people, \ 96 trials each, \ already public, \ its "
             r"reliability never computed in this series", WHITE),
            (rf"trials: \ correct ``same'' trials from 200 to 10,000 ms; \ people with at least "
             rf"{d['registered_min']} usable trials per angle in each half", MODEL),
            (r"analysis: \ each person's slope in odd and even trials; \ correlate the halves; \ Spearman-Brown; \ "
             r"a bootstrap interval over people", PERSON),
            (r"decision: \ supported if the interval lies below 0.70, \ refuted if above, \ otherwise "
             r"inconclusive", GOOD),
            (rf"the plan's fingerprint, \ recorded before the analysis ran: \ SHA-256 \texttt{{{d['hash'][:16]}}}...",
             YOU),
        ], "Then the plan, written as code. <bookmark mark='a'/> The data: Ganis and Kievit's open study, fifty-four "
           "people with ninety-six trials each, already public, and its reliability never computed in this series. "
           "<bookmark mark='b'/> The trials: correct same trials between two hundred milliseconds and ten seconds, "
           "from people with at least four usable trials per angle in each half. <bookmark mark='c'/> The analysis: "
           "each person's slope in odd and in even trials, the correlation of the halves, the Spearman-Brown "
           "correction, and a bootstrap interval over people. <bookmark mark='d'/> The decision: supported if the "
           "interval lies below zero point seven, refuted if it lies above, and otherwise inconclusive. "
           "<bookmark mark='e'/> And the plan's fingerprint, a SHA-256 hash recorded before the analysis ran. Any "
           "change afterwards would show.", tag=published_tag(r"Ganis \& Kievit (2015)"))
