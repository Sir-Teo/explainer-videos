from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ this is the job", r"What does an economist reading the economy do all "
             r"week?", "Chapter fourteen. In practice: this is the job.", lit={2014: r"GDPNow"},
             scale=("firm", "nation"), horizon=("a day",))
        self.week()
        self.called()

    def week(self):
        chain = flow_chain([(r"the calendar: \ what is released this week, \ and what is expected", SPF),
                            (r"each release: \ the surprise, \ against the consensus", NOW),
                            (r"the nowcast: \ revised, \ with the news in each number", GB),
                            (r"the note: \ the number, \ the range, \ what would change it", LATEST),
                            (r"the record: \ every forecast kept and scored", BENCH)], direction=DOWN, box_w=3.6,
                           box_h=0.8, buff=0.3, font_size=19,
                           notes=[r"payrolls on the first Friday, \ inflation mid-month, \ GDP a month after the "
                                  r"quarter",
                                  r"markets move on the surprise, \ not on the number",
                                  r"the Atlanta Fed's GDPNow and the New York Fed's nowcast publish theirs",
                                  r"Chapter 12's rule",
                                  r"Chapter 6's scoring, \ applied to yourself"], note_size=18)
        chain.move_to(DOWN * 0.3)
        head = label(r"a week on a forecasting desk", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "This part is the job of thousands of economists, in central banks, ministries, banks and firms. "
            "<bookmark mark='a'/> The week starts with the calendar: which numbers come out, and what everyone "
            "expects them to be. <bookmark mark='b'/> Each release is read as a surprise against that consensus, "
            "because markets move on the surprise, not the number. <bookmark mark='c'/> The nowcast is revised, "
            "and the revision is explained by the news in each release. <bookmark mark='d'/> The note to the "
            "decision-maker gives the number, the range, and what would change it. <bookmark mark='e'/> And the "
            "good desks keep every forecast and score it, against a benchmark, which is the habit this part has "
            "been teaching."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                anims = [FadeIn(chain.boxes[k], shift=DOWN * 0.1), FadeIn(chain.notes[k], shift=RIGHT * 0.1)]
                if k:
                    anims.append(GrowArrow(chain.arrows[k - 1]))
                self.play(*anims)
        self.clear_scene()

    def called(self):
        c = calls.CALLS["sahm_2024"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17)
        cc.move_to(UP * 1.0)
        lesson = VGroup(
            label(r"a rule fitted to past recessions, \ read by someone who knew why it might fail", font_size=21,
                  color=LATEST),
            label(r"the rule's own author, \ arguing against its signal", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(cc, DOWN, buff=0.6)
        tag = published_tag(r"Sahm, \ Bloomberg Opinion, \ 7 August 2024; \ CRS Insight IN12410 (2024)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In August 2024 the Sahm rule fired. Claudia Sahm, its author, wrote "
            "that the United States was not in a recession: unemployment had risen partly because more people were "
            "looking for work, not only because people were losing jobs, so her rule's signal could be false. "
            "<bookmark mark='b'/> No recession followed; output kept growing, and no business-cycle peak has been "
            "dated since 2020. <bookmark mark='c'/> The verdict: right. <bookmark mark='d'/> It is the best lesson "
            "of this part in one episode: a rule is a summary of the past, <bookmark mark='e'/> and the person "
            "best placed to know when it might fail was the one who understood why it had worked."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(cc.left, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(lesson[0]))
            vo.wait_until("e")
            self.play(FadeIn(lesson[1]))
        self.clear_scene()
