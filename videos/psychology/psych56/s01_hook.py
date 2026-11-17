from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.question()
        self.objectives()

    def story(self):
        rows_section(self, r"A certain witness", [
            (r"a witness picks a man from a line-up, \ and is certain; \ the jury believes her; \ he goes to prison",
             WHITE),
            (r"years later, \ DNA testing shows the crime was committed by someone else", AUTH),
            (r"Brandon Garrett's study of the first 250 DNA exonerations in the United States: \ about three "
             r"quarters involved a mistaken eyewitness identification", PERSON),
            (r"the psychology of the courtroom is Part 12's signal detection and Part 21's memory, \ with a person's "
             r"liberty attached", MODEL),
            (r"for once, \ research changed practice; \ then it changed its own mind about one of its reforms", YOU),
        ], "A witness picks a man from a line-up, and she's certain. <bookmark mark='a'/> The jury believes her, and "
           "he goes to prison. <bookmark mark='b'/> Years later, DNA testing shows the crime was committed by someone "
           "else. <bookmark mark='c'/> When Brandon Garrett studied the first two hundred and fifty DNA exonerations "
           "in the United States, about three quarters involved a mistaken eyewitness identification. "
           "<bookmark mark='d'/> The psychology of the courtroom is Part 12's signal detection and Part 21's memory, "
           "with a person's liberty attached. <bookmark mark='e'/> For once, research changed practice. Then it "
           "changed its own mind about one of its reforms.", tag=published_tag(r"Garrett (2011)"))

    def question(self):
        rows_section(self, r"Today: \ how much should a court trust a memory, \ a confession or an expert?", [
            (r"the line-up: \ detection, \ procedure and confidence", SYMP),
            (r"confessions and lie detection", MODEL),
            (r"experts, \ children and juries", PERSON),
            (r"risk tools and numbers in court", GOOD),
        ], "So this part asks: how much should a court trust a memory, a confession or an expert? "
           "<bookmark mark='a'/> The line-up: detection, procedure and confidence. <bookmark mark='b'/> Confessions "
           "and lie detection. <bookmark mark='c'/> Experts, children and juries. <bookmark mark='d'/> And risk tools "
           "and numbers in court.", font_size=27, buff=0.48)

    def objectives(self):
        head = VGroup(label(r"Part 56", font_size=34, color=GREY_B), label(r"Psychology and Law", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the line-up as signal detection, \ with ROC curves",
            r"why sequential line-ups were adopted, \ and abandoned",
            r"when a witness's confidence can be trusted",
            r"false confessions and the limits of lie detection",
            r"context and bias in forensic experts; \ suggestible memories",
            r"risk tools, \ fairness's impossibility, \ and an IQ score's error",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 56 of Psychology, Built: psychology and law. <bookmark mark='a'/> We'll treat the line-up "
            "as signal detection, with ROC curves. We'll see why sequential line-ups were adopted, and then "
            "abandoned. We'll ask when a witness's confidence can be trusted. We'll look at false confessions and the "
            "limits of lie detection. We'll see context bias in forensic experts, and memories that suggestion can "
            "create. And we'll meet risk tools, the impossibility result for fairness, and the error around an IQ "
            "score that became constitutional law."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
