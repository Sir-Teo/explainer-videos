from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Feedback(VoiceoverScene):
    def construct(self):
        card_section(self, 10, r"Measurement-based care", r"Do therapists know when a patient is getting worse?")
        self.lambert()
        self.rci()

    def lambert(self):
        rows_section(self, r"Routine outcome monitoring", [
            (r"therapists overestimate their patients' improvement, \ and rarely predict who will deteriorate", AUTH),
            (r"Michael Lambert's system: \ a short questionnaire every session, \ compared with the expected course "
             r"for similar patients", MODEL),
            (r"patients who are ``off track'' trigger a signal to the therapist, \ with suggestions", PERSON),
            (r"trials and meta-analyses: \ feedback improves outcomes, \ mostly for the off-track patients, \ and "
             r"reduces deterioration", GOOD),
            (r"Part 51's alarm, \ in a clinic: \ a signal is only useful if it is calibrated and someone acts on it", YOU),
        ], "Do therapists know when a patient is getting worse? <bookmark mark='a'/> Often not. Therapists "
           "overestimate their patients' improvement, and rarely predict who will deteriorate. <bookmark mark='b'/> "
           "Michael Lambert's system gives a short questionnaire every session and compares it with the expected "
           "course for similar patients. <bookmark mark='c'/> Patients who are off track trigger a signal to the "
           "therapist, with suggestions. <bookmark mark='d'/> Trials and meta-analyses find that feedback improves "
           "outcomes, mostly for the off-track patients, and reduces deterioration. <bookmark mark='e'/> It's Part "
           "51's alarm, in a clinic. A signal is only useful if it's calibrated and someone acts on it.",
           tag=published_tag(r"Lambert et al.\ (2018)"))
        chips_section(self, r"What measurement-based care needs", [
            (r"short, \ sensitive measures", r"questionnaires that change with recovery: \ Part 45's item response "
                                             r"theory keeps them short", MODEL),
            (r"expected trajectories", r"from thousands of earlier patients: \ Part 47's growth curves", PERSON),
            (r"a culture", r"therapists who see the data as help, \ not as an audit; \ otherwise it is ignored", GOOD),
            (r"honesty about noise", r"one bad week is not a trend: \ Part 47's single-case lessons", AUTH),
        ], "What does measurement-based care need? <bookmark mark='a'/> Short, sensitive measures, questionnaires that "
           "change with recovery, kept short by Part 45's item response theory. <bookmark mark='b'/> Expected "
           "trajectories, from thousands of earlier patients, which are Part 47's growth curves. "
           "<bookmark mark='c'/> A culture in which therapists see the data as help, not as an audit, or it's ignored. "
           "<bookmark mark='d'/> And honesty about noise. One bad week isn't a trend, which is Part 47's single-case "
           "lesson.", chip_w=4.0, text_w=8.2)

    def rci(self):
        sd, rel = 5.0, 0.85
        sem = sd * np.sqrt(1 - rel)
        sdiff = np.sqrt(2) * sem
        crit = 1.96 * sdiff
        rows_section(self, r"When is a change real?", [
            (r"Jacobson and Truax, \ 1991: \ a change between two scores is reliable if it is larger than the "
             r"measurement could produce by chance", WHITE),
            (rf"worked, \ illustrative: \ a depression scale with SD {sd:.0f} and reliability {rel:.2f}: \ the "
             rf"standard error of one score is {sem:.1f} points, \ of a difference {sdiff:.1f}", MODEL),
            (rf"a change of more than $1.96 \times {sdiff:.1f} \approx {crit:.1f}$ points is reliable; \ a patient "
             rf"four points worse might be noise, \ one six points worse is not", PERSON),
            (r"Part 3's reliability, \ at the bedside: \ the alert a monitoring system raises should use it", YOU),
        ], "When is a change real? <bookmark mark='a'/> In 1991 Neil Jacobson and Paula Truax defined a reliable "
           "change: one larger than the measurement could produce by chance. <bookmark mark='b'/> Work it through "
           "with illustrative numbers: a depression scale with a standard deviation of five and a reliability of "
           "zero point eight five. The standard error of one score is about one point nine, and of a difference "
           "about two point seven. <bookmark mark='c'/> So a change of more than about five point four points is "
           "reliable. A patient four points worse might be noise, and one six points worse isn't. "
           "<bookmark mark='d'/> That's Part 3's reliability at the bedside, and the alert a monitoring system "
           "raises should use it.")
