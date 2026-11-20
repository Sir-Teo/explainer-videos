from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ setting pay and minimums", r"Who does this for a living?",
             "Chapter fourteen. In practice: setting pay and minimums.", lit={1979: r"a survey of economists"},
             scale=("firm", "nation"), horizon=("a year",))
        self.jobs()
        self.called()

    def jobs(self):
        rows = VGroup(
            label(r"the people who do this", font_size=27, color=E.ACCENT),
            label(r"minimum-wage commissions: \ how high, \ how fast, \ for whom", font_size=21, color=NJ),
            label(r"labour ministries and statistical offices: \ wages, \ hours, \ the effects of rules",
                  font_size=21, color=SUPPLY),
            label(r"compensation analysts: \ pay bands, \ market surveys, \ what it takes to hire", font_size=21,
                  color=WAGE),
            label(r"people analytics: \ pay gaps, \ turnover, \ the return to training", font_size=21,
                  color=SCHOOL),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Card and Krueger (1994); \ Cengiz et al.\ (2019)", corner=DR, font_size=12)
        with self.voiceover(
            "Who does this for a living? <bookmark mark='a'/> Many countries set their minimum wage on the advice of "
            "a standing commission, Britain's Low Pay Commission among them, whose economists study each rise's "
            "effects before recommending the next. <bookmark mark='b'/> Labour ministries and statistical offices "
            "measure wages and hours and evaluate the rules. <bookmark mark='c'/> Inside firms, compensation analysts "
            "set pay bands from market surveys: in effect they estimate the supply curve the firm faces. "
            "<bookmark mark='d'/> And people-analytics teams study pay gaps, turnover and what training is worth, "
            "with the selection problems of chapter eleven at every turn."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["survey_1979"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17).move_to(UP * 0.3)
        tag = published_tag(tables.KEARL_1979.tag + r"; \ Cengiz et al.\ (2019); \ Jardim et al.\ (2022)",
                            corner=DR, font_size=11)
        foot = label(r"the sign was right somewhere; \ the size, \ for moderate minimums, \ was not", font_size=20,
                     color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In a survey published in 1979, ninety percent of 211 economists agreed, "
            "at least with provisos, that a minimum wage increases unemployment among young and unskilled workers. "
            "<bookmark mark='b'/> For the moderate increases studied since, from New Jersey's restaurants to 138 "
            "state increases, the average effect on employment has been close to zero; losses appear where minimums "
            "are high relative to local pay, as in Seattle's hours. Later surveys found the agreement falling. "
            "<bookmark mark='c'/> The verdict: partly right. <bookmark mark='d'/> The direction can be right at some "
            "level; the size, for the minimums most places choose, was not."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
