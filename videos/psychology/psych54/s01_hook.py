from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.since()
        self.question()
        self.objectives()

    def story(self):
        rows_section(self, r"The two sigma problem", [
            (r"1984: \ Benjamin Bloom reports studies by his students in which pupils tutored one to one scored about "
             r"two standard deviations above pupils taught in a class of thirty", WHITE),
            (r"the average tutored pupil outperformed 98\% of the class", PERSON),
            (r"no school can give every child a tutor: \ Bloom challenged education to find group methods as good", MODEL),
            (r"the challenge became the founding promise of educational technology", GOOD),
        ], "In 1984 the educational psychologist Benjamin Bloom published a challenge. <bookmark mark='a'/> In studies "
           "by his students, pupils tutored one to one scored about two standard deviations above pupils taught in a "
           "class of thirty. <bookmark mark='b'/> The average tutored pupil outperformed ninety-eight percent of the "
           "class. <bookmark mark='c'/> No school can give every child a tutor, so Bloom challenged education to "
           "find group methods as good. <bookmark mark='d'/> The challenge became the founding promise of educational "
           "technology.", tag=published_tag(r"Bloom (1984)"))

    def since(self):
        rows_section(self, r"Forty years on", [
            (r"the original studies were small, \ short, \ and used tests built for the material taught", WHITE),
            (r"Kurt VanLehn's 2011 review of human tutoring: \ about 0.8 SD, \ not 2; \ the best computer tutors came "
             r"close to that", MODEL),
            (r"large trials of school tutoring programmes find gains of a few tenths of an SD, \ more for intensive, \ "
             r"daily, \ in-school tutoring", PERSON),
            (r"and the methods with the strongest evidence are ones students rate as less effective than rereading", AUTH),
            (r"memory research (Parts 20 and 21) becomes an engineering problem: \ when should the next review be?", YOU),
        ], "Forty years on, the two sigma has shrunk. <bookmark mark='a'/> The original studies were small and short, "
           "and used tests built for the material taught. <bookmark mark='b'/> Kurt VanLehn's 2011 review of human "
           "tutoring found about zero point eight standard deviations, not two, and the best computer tutors came "
           "close to that. <bookmark mark='c'/> Large trials of school tutoring find gains of a few tenths of a "
           "standard deviation, more for intensive, daily tutoring in school. <bookmark mark='d'/> And the study "
           "methods with the strongest evidence are ones students rate as less effective than rereading. "
           "<bookmark mark='e'/> Parts 20 and 21's memory research becomes an engineering problem: when should the "
           "next review be?", tag=published_tag(r"VanLehn (2011)"))

    def question(self):
        rows_section(self, r"Today: \ what is the best way to learn, \ and why do learners choose the opposite?", [
            (r"retrieval, \ spacing and interleaving, \ and why they feel worse", SYMP),
            (r"ten techniques ranked, \ cognitive load, \ and the myths", MODEL),
            (r"tutors and schedulers that model the learner", PERSON),
            (r"reading, \ beliefs and feedback", GOOD),
        ], "So this part asks: what's the best way to learn something, and why do learners choose the opposite? "
           "<bookmark mark='a'/> Retrieval, spacing and interleaving, and why they feel worse. <bookmark mark='b'/> "
           "Ten techniques ranked, cognitive load, and the myths. <bookmark mark='c'/> Tutors and schedulers that "
           "model the learner. <bookmark mark='d'/> And reading, beliefs, and feedback.", font_size=27, buff=0.48)

    def objectives(self):
        head = VGroup(label(r"Part 54", font_size=34, color=GREY_B), label(r"The Science of Learning", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"retrieval practice, \ spacing and interleaving",
            r"learning against performance, \ and the illusion of fluency",
            r"which study techniques work, \ and cognitive load",
            r"learning styles and other myths, \ tested",
            r"tutoring, \ and a review scheduler raced on Psyche",
            r"reading, \ mindsets and feedback at scale",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 54 of Psychology, Built: the science of learning. <bookmark mark='a'/> We'll put retrieval "
            "practice, spacing and interleaving into classrooms. We'll separate learning from performance, and meet "
            "the illusion of fluency. We'll rank ten study techniques, and design for cognitive load. We'll test "
            "learning styles and other myths. We'll measure tutoring honestly, and race review schedulers on Psyche. "
            "And we'll look at reading, mindsets and feedback at scale."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
