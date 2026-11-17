from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403


class Stimulation(VoiceoverScene):
    def construct(self):
        card_section(self, 10, r"New interventions", r"What do stimulation and psychedelics show?", scale=("brain",))
        self.stimulation()
        self.drugs()
        self.standards()

    def stimulation(self):
        chips_section(self, r"Stimulating the brain", [
            (r"TMS", r"magnetic pulses over the prefrontal cortex; \ cleared in the United States for depression in "
                     r"2008; \ modest benefit over sham in meta-analyses", MODEL),
            (r"accelerated TMS", r"many sessions a day, \ aimed by each person's connectivity map; \ Cole and "
                                 r"colleagues, \ 2022: \ a large benefit over sham in a trial of 29 people", GOOD),
            (r"deep brain stimulation", r"electrodes in the subgenual cingulate: \ striking open results in a few "
                                        r"patients (2005), \ then a larger sham-controlled trial stopped for futility", AUTH),
            (r"the lesson", r"small open studies of devices overestimate; \ sham control and size decide", YOU),
        ], "What do new interventions show? First, stimulating the brain. <bookmark mark='a'/> Transcranial magnetic "
           "stimulation sends magnetic pulses over the prefrontal cortex. It was cleared in the United States for "
           "depression in 2008, and meta-analyses find a modest benefit over sham. <bookmark mark='b'/> Accelerated "
           "protocols give many sessions a day, aimed by each person's connectivity map. In 2022 Eleanor Cole and "
           "colleagues reported a large benefit over sham, in a trial of twenty-nine people. <bookmark mark='c'/> "
           "Deep brain stimulation puts electrodes in the subgenual cingulate. It gave striking open results in a few "
           "patients in 2005, and then a larger sham-controlled trial was stopped for futility. <bookmark mark='d'/> "
           "The lesson: small open studies of devices overestimate. Sham control and size decide.",
           tag=published_tag(r"Cole et al.\ (2022)"))

    def drugs(self):
        chips_section(self, r"Fast-acting drugs", [
            (r"ketamine", r"a single infusion lifts depressive symptoms within hours in some patients; \ an "
                          r"esketamine nasal spray was approved in 2019; \ effects fade over days", MODEL),
            (r"psilocybin", r"Goodwin and colleagues, \ 2022: \ 233 patients, \ 25 mg against 1 mg; \ a larger fall "
                            r"in symptoms at three weeks, \ smaller and uncertain by twelve", PERSON),
            (r"blinding", r"people usually know whether they had a psychedelic: \ expectation (Part 57) is part of "
                          r"every result", AUTH),
            (r"mechanism", r"proposed accounts (relaxed priors, \ plasticity) are computational, \ and still to be "
                           r"tested", YOU),
        ], "Second, fast-acting drugs. <bookmark mark='a'/> A single infusion of ketamine lifts depressive symptoms "
           "within hours in some patients. A nasal spray of esketamine was approved in 2019. The effects fade over "
           "days. <bookmark mark='b'/> Psilocybin: in 2022 Guy Goodwin and colleagues gave two hundred and "
           "thirty-three patients a dose of twenty-five milligrams or one milligram. There was a larger fall in "
           "symptoms at three weeks, smaller and uncertain by twelve. <bookmark mark='c'/> The problem is blinding. "
           "People usually know whether they had a psychedelic, so expectation, Part 57's subject, is part of every "
           "result. <bookmark mark='d'/> The proposed mechanisms, relaxed priors and plasticity, are computational, "
           "and still to be tested.", tag=published_tag(r"Goodwin et al.\ (2022)"))

    def standards(self):
        rows_section(self, r"Judged by Part 2's standards", [
            (r"randomization and a credible control: \ sham coils, \ active placebos, \ low doses", WHITE),
            (r"blinding checked, \ not assumed: \ ask patients and raters what they think was given", AUTH),
            (r"outcomes that last: \ months, \ not days", MODEL),
            (r"size: \ enough patients that the estimate is not one lucky sample (Part 4)", PERSON),
            (r"replication by groups without a stake in the treatment", GOOD),
        ], "So judge them by Part 2's standards. <bookmark mark='a'/> Randomization and a credible control: sham "
           "coils, active placebos, or low doses. <bookmark mark='b'/> Blinding checked, not assumed: ask patients "
           "and raters what they think was given. <bookmark mark='c'/> Outcomes that last months, not days. "
           "<bookmark mark='d'/> Enough patients that the estimate isn't one lucky sample, as in Part 4. "
           "<bookmark mark='e'/> And replication by groups without a stake in the treatment.")
