from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Pain(VoiceoverScene):
    def construct(self):
        card_section(self, 5, r"Chronic pain", r"When does pain outlast its injury?", scale=("person",))
        self.learned()
        self.treat()

    def learned(self):
        rows_section(self, r"Pain that stays", [
            (r"acute pain signals damage; \ chronic pain, \ lasting months, \ often persists after tissue has "
             r"healed", WHITE),
            (r"the fear-avoidance model: \ pain, \ then fear of movement, \ then avoidance, \ deconditioning and more "
             r"pain: \ Part 16's avoidance, \ maintained by relief", AUTH),
            (r"central sensitization: \ the nervous system's gain turns up, \ and Part 14's priors predict pain", MODEL),
            (r"psychological factors predict which back pain becomes chronic better than scans do", PERSON),
        ], "When does pain outlast its injury? <bookmark mark='a'/> Acute pain signals damage. Chronic pain, lasting "
           "months, often persists after the tissue has healed. <bookmark mark='b'/> The fear-avoidance model: pain, "
           "then fear of movement, then avoidance, deconditioning, and more pain. That's Part 16's avoidance, "
           "maintained by relief. <bookmark mark='c'/> Central sensitization: the nervous system's gain turns up, and "
           "Part 14's priors predict pain. <bookmark mark='d'/> Psychological factors predict which back pain becomes "
           "chronic better than scans do.")

    def treat(self):
        chips_section(self, r"Treating it", [
            (r"CBT and acceptance", r"modest, \ real effects on pain and disability, \ small on average (Cochrane "
                                    r"reviews)", MODEL),
            (r"graded activity", r"exposure for movement: \ the feared activity, \ step by step (Part 42's exposure)",
             GOOD),
            (r"pain education", r"explaining pain as a protective output of the brain reduces fear, \ with small "
                                r"effects", PERSON),
            (r"what to avoid", r"long-term opioids for chronic non-cancer pain: \ little benefit, \ and harm", AUTH),
        ], "How is it treated? <bookmark mark='a'/> Cognitive behavioural and acceptance-based therapies have modest, "
           "real effects on pain and disability, small on average. <bookmark mark='b'/> Graded activity is exposure "
           "for movement: the feared activity, step by step, like Part 42's exposure. <bookmark mark='c'/> Pain "
           "education explains pain as a protective output of the brain, which reduces fear, with small effects. "
           "<bookmark mark='d'/> And what to avoid: long-term opioids for chronic pain not caused by cancer, which "
           "bring little benefit and real harm.")
