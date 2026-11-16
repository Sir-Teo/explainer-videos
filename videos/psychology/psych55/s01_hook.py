from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.donors()
        self.downstream()
        self.question()
        self.objectives()

    def donors(self):
        head = heading(r"One sentence on a form")
        A = axes([0.3, 2.7], [0, 1.05], x_length=4.2, y_length=3.0, xticks=None, yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"consent to be a donor", center=[-3.8, 0.3, 0],
                 font_size=12)
        b = bars(A.ax, [1, 2], [0.15, 0.95], [AUTH, GOOD], width=0.7)
        names = VGroup(label(r"opt in", font_size=14, color=AUTH).next_to(A.ax.c2p(1, 0), DOWN, buff=0.12),
                       label(r"opt out", font_size=14, color=GOOD).next_to(A.ax.c2p(2, 0), DOWN, buff=0.12))
        rows = rows_of([
            (r"Johnson and Goldstein, \ 2003: \ European countries where people had to opt in to organ donation had "
             r"low consent rates; \ where they had to opt out, \ nearly everyone was a donor", WHITE),
            (r"one sentence on a form: \ the default", PERSON),
            (r"an online experiment agreed: \ the same choice, \ framed as opt-in or opt-out, \ roughly doubled "
             r"consent", MODEL),
            (r"the bars are approximate country averages, \ as usually quoted", YOU),
        ], 6.8, 19, 0.36).move_to([3.0, -0.1, 0])
        tag = published_tag(r"Johnson \& Goldstein (2003)")
        with self.voiceover(
            "Here's one sentence on a form. <bookmark mark='a'/> In 2003 Eric Johnson and Daniel Goldstein compared "
            "European countries. Where people had to opt in to organ donation, consent rates were low. Where they had "
            "to opt out, nearly everyone was a donor. <bookmark mark='b'/> The difference was a default. "
            "<bookmark mark='c'/> An online experiment agreed: the same choice, framed as opting in or opting out, "
            "roughly doubled consent. <bookmark mark='d'/> The bars are approximate country averages, as they're "
            "usually quoted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def downstream(self):
        rows_section(self, r"And then the accounting", [
            (r"consent on a register is not organs donated: \ families, \ hospitals and logistics decide that, \ "
             r"and opt-out countries do not uniformly donate more", AUTH),
            (r"still, \ the nudge became policy: \ Thaler and Sunstein's 2008 book, \ and ``nudge units'' in "
             r"governments around the world", MODEL),
            (r"in published papers, \ the average nudge moved behaviour by almost nine percentage points", PERSON),
            (r"across everything two government units actually ran, \ by about one and a half (DellaVigna and Linos, "
             r"\ 2022)", GOOD),
            (r"this part is that gap: \ what changes behaviour at scale, \ by how much, \ and how we know", YOU),
        ], "Then the accounting arrived. <bookmark mark='a'/> Consent on a register isn't organs donated. Families, "
           "hospitals and logistics decide that, and opt-out countries don't uniformly donate more. "
           "<bookmark mark='b'/> Still, the nudge became policy: Richard Thaler and Cass Sunstein's book in 2008, "
           "and nudge units in governments around the world. <bookmark mark='c'/> In published papers, the average "
           "nudge moved behaviour by almost nine percentage points. <bookmark mark='d'/> Across everything two "
           "government units actually ran, it moved it by about one and a half, as Stefano DellaVigna and Elizabeth "
           "Linos found in 2022. <bookmark mark='e'/> This part is that gap: what changes behaviour at scale, by how "
           "much, and how we know.", tag=published_tag(r"DellaVigna \& Linos (2022)"))

    def question(self):
        rows_section(self, r"Today: \ how much can the way a choice is presented change what millions do?", [
            (r"defaults, \ the toolbox, \ and a megastudy", SYMP),
            (r"the reckoning: \ published against practice, \ and for whom", MODEL),
            (r"incentives, \ backfires, \ persuasion and misinformation", PERSON),
            (r"a retraction, \ and the ethics of steering people", GOOD),
        ], "So this part asks: how much can the way a choice is presented change what millions of people do? "
           "<bookmark mark='a'/> Defaults, the toolbox, and a megastudy. <bookmark mark='b'/> The reckoning: "
           "published against practice, and for whom. <bookmark mark='c'/> Incentives, backfires, persuasion and "
           "misinformation. <bookmark mark='d'/> And a retraction, and the ethics of steering people.",
           font_size=27, buff=0.48)

    def objectives(self):
        head = VGroup(label(r"Part 55", font_size=34, color=GREY_B), label(r"Behaviour Change at Scale",
                                                                           font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"why defaults work, \ and the inertia algebra",
            r"the toolbox: \ framing, \ reminders, \ commitment, \ norms",
            r"megastudies, \ the winner's curse and shrinkage",
            r"published nudges against nudge units, \ and heterogeneity",
            r"incentives, \ backfires, \ persuasion and misinformation",
            r"sludge, \ autonomy, \ and changing the system",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 55 of Psychology, Built: behaviour change at scale. <bookmark mark='a'/> We'll see why "
            "defaults work, and solve their algebra. We'll open the toolbox of framing, reminders, commitment and "
            "norms. We'll run a megastudy, and correct its winner. We'll set published nudges against what nudge "
            "units found, and ask for whom. We'll look at incentives, backfires, persuasion and misinformation. And "
            "we'll weigh sludge, autonomy, and changing the system instead of the person."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
