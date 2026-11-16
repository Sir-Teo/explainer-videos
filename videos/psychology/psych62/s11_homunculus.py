from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403


class Homunculus(VoiceoverScene):
    def construct(self):
        card_section(self, 10, r"The Homunculus, \ last drawing", r"What is still a little person?",
                     scale=("person",), marr=("how",))
        self.drawing()

    def drawing(self):
        hm = homunculus_map(done=PART, height=6.4).move_to([-3.6, -0.1, 0])
        rows = rows_of([
            (r"mechanism now: \ the neuron and the synapse, \ thresholds and signal detection, \ early vision, \ "
             r"conditioning and reward prediction, \ decision as accumulation", GOOD),
            (r"partly mechanism: \ attention, \ working memory, \ episodic memory, \ language comprehension, \ "
             r"emotion", MODEL),
            (r"still a little person: \ consciousness (Part 27); \ open-ended thought; \ a unified architecture "
             r"(Part 58); \ the individual case (Parts 47 and 59)", AUTH),
            (r"the parts still drawn as a person are the syllabus of the next fifty years", YOU),
        ], 6.4, 19, 0.38).move_to([3.0, -0.1, 0])
        with self.voiceover(
            "In Part 1 the Homunculus was a little person inside the head, doing all the work. Each part replaced a "
            "piece of it with mechanism. Here it is, drawn one last time. <bookmark mark='a'/> Mechanism now: the "
            "neuron and the synapse, thresholds and signal detection, early vision, conditioning and reward "
            "prediction, and decision as the accumulation of evidence. <bookmark mark='b'/> Partly mechanism: "
            "attention, working memory, episodic memory, language comprehension and emotion. <bookmark mark='c'/> "
            "Still a little person: consciousness, from Part 27; open-ended thought; a unified architecture, from "
            "Part 58; and the individual case, from Parts 47 and 59. <bookmark mark='d'/> The parts still drawn as "
            "a person are the syllabus of the next fifty years."
        ) as vo:
            self.play(FadeIn(hm))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
