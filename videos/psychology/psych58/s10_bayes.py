from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403


class Bayes(VoiceoverScene):
    def construct(self):
        card_section(self, 9, r"The Bayesian brain and its critics", r"Optimal against what?")
        self.successes()
        self.critics()
        self.test()

    def successes(self):
        rows_section(self, r"Where the Bayesian account earned its place", [
            (r"cue combination: \ vision and touch weighted by their reliabilities, \ as the optimum requires "
             r"(Ernst and Banks, \ 2002; \ Part 14)", GOOD),
            (r"motor control: \ people learn the distribution of perturbations and their own noise, \ and plan "
             r"accordingly (K\"ording and Wolpert, \ 2004)", MODEL),
            (r"illusions as optimal guesses: \ slow-motion priors explain speed misperception at low contrast "
             r"(Weiss, \ Simoncelli and Adelson, \ 2002)", PERSON),
            (r"the strength: \ quantitative predictions from measured noise, \ with no free weights", YOU),
        ], "Optimal against what? First, where the Bayesian account earned its place. <bookmark mark='a'/> Cue "
           "combination: vision and touch are weighted by their reliabilities, as the optimum requires. That was Marc "
           "Ernst and Martin Banks in 2002, and Part 14. <bookmark mark='b'/> Motor control: people learn the "
           "distribution of perturbations and their own noise, and plan accordingly, as Konrad Kording and Daniel "
           "Wolpert showed. <bookmark mark='c'/> Illusions as optimal guesses: a prior for slow motion explains why "
           "things look slower at low contrast. <bookmark mark='d'/> The strength is quantitative predictions from "
           "measured noise, with no free weights.")

    def critics(self):
        chips_section(self, r"The critics", [
            (r"just-so stories", r"Bowers and Davis, \ 2012: \ with priors and likelihoods chosen after the fact, \ "
                                 r"any behaviour can be called optimal", AUTH),
            (r"theory or tool", r"Jones and Love, \ 2011: \ ``Bayesian fundamentalism'' fits data without asking "
                                r"how the computation is done", MODEL),
            (r"suboptimality", r"Rahnev and Denison, \ 2018: \ people are reliably suboptimal in many tasks; \ the "
                               r"useful question is how", PERSON),
            (r"the defence", r"used as a model with measured priors, \ it predicts; \ used as a description of "
                             r"everything, \ it does not", GOOD),
        ], "Now the critics. <bookmark mark='a'/> Jeffrey Bowers and Colin Davis called many Bayesian accounts "
           "just-so stories: with priors and likelihoods chosen after the fact, any behaviour can be called optimal. "
           "<bookmark mark='b'/> Matt Jones and Bradley Love warned against Bayesian fundamentalism, which fits data "
           "without asking how the computation is done. <bookmark mark='c'/> Dobromir Rahnev and Rachel Denison "
           "showed that people are reliably suboptimal in many tasks, and argued the useful question is how. "
           "<bookmark mark='d'/> The defence: used as a model with measured priors, the Bayesian account predicts. "
           "Used as a description of everything, it doesn't.", tag=published_tag(r"Bowers \& Davis (2012)"))

    def test(self):
        rows_section(self, r"How to keep it honest", [
            (r"measure the prior independently: \ from the environment's statistics (Laughlin's fly), \ or from "
             r"training", WHITE),
            (r"measure the noise independently: \ from discrimination thresholds", MODEL),
            (r"then predict a new task with no parameters left to fit", GOOD),
            (r"compare against a named alternative, \ not against no model at all (Part 48's model comparison)",
             PERSON),
        ], "So how do you keep it honest? <bookmark mark='a'/> Measure the prior independently: from the "
           "environment's statistics, like Laughlin's fly, or from training. <bookmark mark='b'/> Measure the noise "
           "independently, from discrimination thresholds. <bookmark mark='c'/> Then predict a new task with no "
           "parameters left to fit. <bookmark mark='d'/> And compare against a named alternative, not against no "
           "model at all. That's Part 48's model comparison.")
