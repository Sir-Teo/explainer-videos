from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403


class Kant(VoiceoverScene):
    def construct(self):
        card_section(self, 11, r"The verdict on Kant", r"Was he right?", scale=("person", "society"))
        self.three()
        self.right()
        self.fourth()

    def three(self):
        chips_section(self, r"Three objections, \ answered", [
            (r"1. mathematics", r"answered: \ Weber's and Fechner's laws, \ Hick's logarithm, \ signal detection, "
                                r"\ the diffusion model, \ the Rescorla-Wagner rule: \ equations about the mind that "
                                r"predict measurements", GOOD),
            (r"2. experiment", r"answered: \ minds are randomized, \ manipulated and recombined every day, \ from "
                               r"Donders's subtraction (Part 1) to registered reports", GOOD),
            (r"3. observation", r"right, \ and answered: \ observing does disturb (demand characteristics, \ "
                                r"Clever Hans, \ placebo, \ introspection's limits), \ and the field learned to "
                                r"measure and control the disturbance", PERSON),
        ], "So, was Kant right? <bookmark mark='a'/> On mathematics: answered. Weber's and Fechner's laws, Hick's "
           "logarithm, signal detection, the diffusion model and the Rescorla-Wagner rule are equations about the "
           "mind that predict measurements. <bookmark mark='b'/> On experiment: answered. Minds are randomized, "
           "manipulated and recombined every day, from Donders's subtraction in Part 1 to the registered report you "
           "just saw. <bookmark mark='c'/> On observation, Kant was right, and it was answered anyway. Observing "
           "does disturb: demand characteristics, Clever Hans, placebo, and the limits of introspection. And the "
           "field learned to measure the disturbance and control it, with blinding, control groups and "
           "behavioural measures.", chip_w=3.0, text_w=9.4, font_size=20)

    def fourth(self):
        rows_section(self, r"The objection Kant did not make", [
            (r"the observer's incentives: \ researchers rewarded for positive, \ new, \ striking results (Parts 4, "
             r"\ 50 and 61)", AUTH),
            (r"it produced the failed rows of the Ledger, \ not because minds cannot be studied, \ but because "
             r"studiers are people", MODEL),
            (r"it too is being answered: \ registered reports, \ open data, \ big teams, \ and a Ledger with dates",
             GOOD),
            (r"the verdict: \ a science of the mind is possible; \ it is hard; \ and it is a science of its own "
             r"scientists too", YOU),
        ], "There's a fourth objection Kant didn't make. <bookmark mark='a'/> The observer's incentives: researchers "
           "are rewarded for positive, new and striking results, as Parts 4, 50 and 61 showed. "
           "<bookmark mark='b'/> It produced the failed rows of the Ledger, not because minds can't be studied, but "
           "because the people studying them are people. <bookmark mark='c'/> It too is being answered, with "
           "registered reports, open data, big teams, and a Ledger with dates. <bookmark mark='d'/> So here's the "
           "verdict. A science of the mind is possible. It's hard. And it has to be a science of its own scientists "
           "too.")

    def right(self):
        rows_section(self, r"What Kant got right", [
            (r"that measurement is the hard part: \ sixty-two parts later, \ reliability and validity are still where "
             r"most findings live or die", WHITE),
            (r"that observing changes the observed: \ demand, \ expectation and the Hawthorne story's grain of truth "
             r"are designed around, \ not wished away", MODEL),
            (r"that a science of mind needs more than introspection: \ every chapter here rests on behaviour, \ "
             r"physiology or models scored against data", GOOD),
            (r"his error was to treat these as reasons it could not be done, \ rather than as the problems the "
             r"methods would have to solve", AUTH),
        ], "Before the verdict, what Kant got right. <bookmark mark='a'/> That measurement is the hard part. Sixty-two "
           "parts later, reliability and validity are still where most findings live or die. <bookmark mark='b'/> "
           "That observing changes the observed. Demand, expectation, and the grain of truth in the Hawthorne story "
           "are designed around, not wished away. <bookmark mark='c'/> That a science of mind needs more than "
           "introspection. Every chapter here rests on behaviour, physiology, or models scored against data. "
           "<bookmark mark='d'/> His error was to treat these as reasons it couldn't be done, rather than as the "
           "problems the methods would have to solve.")
