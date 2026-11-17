from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card_section(self, 14, r"In practice: \ evaluating a model", r"A team says its new model reasons better. \ "
                     r"How would you check?", scale=("society",))
        self.where()
        self.plan()

    def where(self):
        chips_section(self, r"Where this is a job", [
            (r"AI evaluation", r"designing benchmarks and studies of model behaviour, \ with psychometrics", MODEL),
            (r"human-AI interaction", r"how people rely on, \ trust and work with systems; \ calibrated reliance",
             PERSON),
            (r"safety and alignment", r"red-teaming, \ sycophancy, \ persuasion and deception tests", AUTH),
            (r"products and research", r"mental-health products under clinical standards; \ market research with "
                                       r"synthetic respondents, \ validated against people", GOOD),
        ], "Where is this a job? <bookmark mark='a'/> In AI evaluation: designing benchmarks and studies of model "
           "behaviour, with psychometrics. <bookmark mark='b'/> In human-AI interaction: how people rely on, trust "
           "and work with systems, and how to calibrate that reliance. <bookmark mark='c'/> In safety and alignment: "
           "red-teaming, and tests of sycophancy, persuasion and deception. <bookmark mark='d'/> And in products and "
           "research: mental-health products held to clinical standards, and market research with synthetic "
           "respondents, validated against people.")

    def plan(self):
        d = load("separate")
        rows_section(self, r"A worked evaluation plan", [
            (r"construct: \ write down what ``reasons better'' means, \ and which tasks would show it (Part 3)", WHITE),
            (r"items: \ new, \ written after both models' training, \ with perturbed twins of each", MODEL),
            (rf"size: \ a 3-point gain near 70\%, \ paired on the same items, \ needs about "
             rf"{num(round(d['paired'], -2))} items; \ more with fewer", PERSON),
            (r"prompts: \ several phrasings, \ fixed in advance, \ the same for both models", GOOD),
            (r"report: \ a preregistered primary score with its interval, \ every phrasing's result, \ and the "
             r"items where the models differ", YOU),
        ], "Here's a worked evaluation plan. <bookmark mark='a'/> The construct: write down what reasons better "
           "means, and which tasks would show it. That's Part 3. <bookmark mark='b'/> The items: new ones, written "
           "after both models' training, with perturbed twins of each. <bookmark mark='c'/> The size: a three-point "
           "gain near seventy percent, paired on the same items, needs about eighteen hundred items, and more if the "
           "items are less correlated. <bookmark mark='d'/> The prompts: several phrasings, fixed in advance, the "
           "same for both models. <bookmark mark='e'/> And the report: a preregistered primary score with its "
           "interval, every phrasing's result, and the items where the models differ.", font_size=21, buff=0.38)
