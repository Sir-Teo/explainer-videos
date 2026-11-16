from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403


class Code(VoiceoverScene):
    def construct(self):
        card_section(self, 8, r"Theory as code", r"What would it take for a theory to be derivable?", marr=("what",))
        self.verbal()
        self.worked()
        self.method()

    def verbal(self):
        chips_section(self, r"Verbal theories, \ and their problem", [
            (r"vague", r"``anxiety biases attention to threat'' predicts a direction, \ not a size, \ a time course "
                       r"or a boundary", AUTH),
            (r"flexible", r"almost any result can be reconciled with it after the fact", AUTH),
            (r"formal", r"a model written as code makes predictions you can compute, \ including surprising ones", GOOD),
            (r"this series", r"Psyche is that idea: \ every chapter's claim computed from a model whose code you can "
                             r"read", MODEL),
        ], "What would it take for a theory to be derivable? <bookmark mark='a'/> Verbal theories are vague. "
           "Anxiety biases attention to threat predicts a direction, not a size, a time course, or a boundary. "
           "<bookmark mark='b'/> They're flexible: almost any result can be reconciled with them after the fact. "
           "<bookmark mark='c'/> A model written as code makes predictions you can compute, including surprising "
           "ones. <bookmark mark='d'/> And this series is that idea: Psyche computes every chapter's claim from a "
           "model whose code you can read.")

    def method(self):
        rows_section(self, r"Theory construction, \ as a method", [
            (r"Borsboom and colleagues, \ 2021: \ start from robust phenomena, \ build a formal model that would "
             r"produce them, \ check that it does", WHITE),
            (r"van Rooij and Baggio, \ 2021: \ theory before the test: \ ask whether a theory can even produce the "
             r"behaviour, \ before testing it on data", MODEL),
            (r"then the risky prediction: \ a result the theory forbids, \ written down before the study (Part 62's "
             r"registered report)", GOOD),
            (r"what counts as a derivation: \ another person runs the code and gets the prediction", YOU),
        ], "Theory construction can be a method. <bookmark mark='a'/> Denny Borsboom and colleagues propose starting "
           "from robust phenomena, building a formal model that would produce them, and checking that it does. "
           "<bookmark mark='b'/> Iris van Rooij and Giosue Baggio argue for theory before the test: ask whether a "
           "theory can even produce the behaviour, before testing it on data. <bookmark mark='c'/> Then comes the "
           "risky prediction: a result the theory forbids, written down before the study. That's Part 62's "
           "registered report. <bookmark mark='d'/> And what counts as a derivation? Another person runs the code "
           "and gets the prediction.", tag=published_tag(r"Borsboom et al.\ (2021)"))

    def worked(self):
        rows_section(self, r"One sentence, \ written as code", [
            (r"verbal: \ ``practice makes people faster, \ with diminishing returns''", WHITE),
            (r"as code, \ the sentence must choose: \ a power law $T = a + b N^{-c}$, \ or an exponential $T = a + "
             r"b e^{-cN}$ (Part 48's law that was an average)", MODEL),
            (r"the two predict the same early trials and different late ones: \ the power law keeps improving after "
             r"a thousand trials, \ the exponential has stopped", PERSON),
            (r"writing it down exposes the choice the sentence hid, \ and names the experiment that settles it: \ "
             r"long practice, \ fitted person by person", GOOD),
        ], "Here is what writing a theory as code does. <bookmark mark='a'/> The verbal version: practice makes "
           "people faster, with diminishing returns. <bookmark mark='b'/> As code, the sentence has to choose. A "
           "power law, or an exponential? That was Part 48's law that turned out to be an average. "
           "<bookmark mark='c'/> The two predict the same early trials and different late ones. The power law keeps "
           "improving after a thousand trials, and the exponential has stopped. <bookmark mark='d'/> Writing it down "
           "exposes the choice the sentence hid, and names the experiment that settles it: long practice, fitted "
           "person by person.")
