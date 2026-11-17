from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class Tom(VoiceoverScene):
    def construct(self):
        card_section(self, 4, r"Theory of mind in machines", r"Does a model know what others believe?",
                     scale=("person",))
        self.claim()
        self.worked()
        self.valid()

    def claim(self):
        rows_section(self, r"A claim, \ its perturbations, \ and a comparison", [
            (r"Kosinski, \ 2023: \ large language models pass false-belief tasks (Part 35's Sally-Anne) at the "
             r"level of school-age children", WHITE),
            (r"Ullman, \ 2023: \ trivial alterations (a transparent bag, \ a person told the truth) break the "
             r"answers: \ pattern matching on the task's familiar form", AUTH),
            (r"Strachan and colleagues, \ 2024: \ models against about 1,900 people on a battery of theory-of-mind "
             r"tests: \ at or above people on some, \ below on others (faux pas), \ with a cautious style", MODEL),
            (r"the claim is contested; \ the method has improved", PERSON),
        ], "Does a model know what others believe? <bookmark mark='a'/> In 2023 Michal Kosinski reported that large "
           "language models pass false-belief tasks, Part 35's Sally-Anne, at the level of school-age children. "
           "<bookmark mark='b'/> Tomer Ullman showed that trivial alterations, like a transparent bag, or a person "
           "who's been told the truth, break the answers. That's pattern matching on the task's familiar form. "
           "<bookmark mark='c'/> In 2024 James Strachan and colleagues tested models against about nineteen hundred "
           "people on a battery of theory-of-mind tests. Models were at or above people on some, below on others, "
           "like detecting a faux pas, with a cautious style of answer. <bookmark mark='d'/> The claim is contested, "
           "and the method has improved.", tag=published_tag(r"Strachan et al.\ (2024)"))

    def valid(self):
        chips_section(self, r"What a valid test would need", [
            (r"new items", r"stories never published, \ in forms the model has not seen", MODEL),
            (r"controls", r"true-belief versions, \ so that tracking the story's facts alone fails", PERSON),
            (r"converging tasks", r"several measures that should agree, \ as Part 30 asked of infants' looking", GOOD),
            (r"a human baseline", r"the same items, \ the same scoring, \ for people", SYMP),
            (r"Part 30's lesson", r"infants' theory of mind was argued over looking times for decades; \ claims "
                                  r"about a new kind of subject deserve the same care", YOU),
        ], "What would a valid test need? <bookmark mark='a'/> New items: stories never published, in forms the model "
           "hasn't seen. <bookmark mark='b'/> Controls: true-belief versions, so that tracking the story's facts alone "
           "fails. <bookmark mark='c'/> Converging tasks: several measures that should agree, as Part 30 asked of "
           "infants' looking. <bookmark mark='d'/> A human baseline: the same items and the same scoring, for people. "
           "<bookmark mark='e'/> That's Part 30's lesson. Infants' theory of mind was argued over looking times for "
           "decades, and claims about a new kind of subject deserve the same care.")

    def worked(self):
        rows_section(self, r"One item, \ perturbed", [
            (r"the classic: \ Sam puts chocolate in a box and leaves; \ Ana moves it to a bag; \ where will Sam look? "
             r"\ (the box: \ he did not see it moved)", WHITE),
            (r"perturbed: \ the bag is transparent, \ and Sam can see the chocolate through it when he returns", MODEL),
            (r"now the right answer changes: \ a reader who tracks what Sam can see says the bag; \ one matching the "
             r"familiar story says the box", AUTH),
            (r"Ullman, \ 2023: \ small changes like this broke models that passed the originals; \ later models "
             r"pass more of them, \ which is why the test set must keep changing", PERSON),
            (r"the same logic as Part 30's infant studies: \ a capacity is shown by the cases where only it gives the "
             r"right answer", YOU),
        ], "Here's one item, perturbed. <bookmark mark='a'/> The classic: Sam puts chocolate in a box and leaves. Ana "
           "moves it to a bag. Where will Sam look? In the box, because he didn't see it moved. "
           "<bookmark mark='b'/> Now perturb it. The bag is transparent, and Sam can see the chocolate through it "
           "when he comes back. <bookmark mark='c'/> The right answer changes. A reader who tracks what Sam can see "
           "says the bag. One matching the familiar story says the box. <bookmark mark='d'/> In 2023 Tomer Ullman "
           "showed that small changes like this broke models that passed the originals. Later models pass more of "
           "them, which is why the test set has to keep changing. <bookmark mark='e'/> It's the same logic as Part "
           "30's infant studies: a capacity is shown by the cases where only it gives the right answer.")
