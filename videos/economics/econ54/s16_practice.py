from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ estimation as a job", r"Where are models estimated for a living?",
             "Chapter fourteen. In practice: estimation as a job.",
             lit={2007: r"Smets and Wouters", 2016: r"Cohen et al."}, scale=("firm", "nation"),
             horizon=("a year",))
        self.places()
        self.called()

    def places(self):
        rows = VGroup(
            label(r"transport appraisal: \ the value of time, \ from logit models of travellers' choices",
                  font_size=22, color=DATA),
            label(r"competition authorities: \ demand estimated, \ then a merger simulated \ (Part 43)",
                  font_size=22, color=EST),
            label(r"central banks: \ whole models of the economy, \ estimated with Bayesian priors", font_size=22,
                  color=PATIENCE),
            label(r"firms: \ demand and willingness to pay, \ from prices that vary or are varied on purpose",
                  font_size=22, color=CAUTION),
            label(r"UberX in 2015: \ demand estimated from surge prices, \ about \$2.9 billion of consumer surplus "
                  r"in four cities", font_size=22, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        if rows.width > 13.2:
            rows.width = 13.2
        head = label(r"estimation at work", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(r"Smets and Wouters, \ AER 97(3) (2007); \ Cohen, \ Hahn, \ Hall, \ Levitt and "
                            r"Metcalfe, \ NBER WP 22627 (2016)", corner=DR, font_size=12)
        with self.voiceover(
            "Where is this done for a living? <bookmark mark='a'/> In transport ministries, where the value of "
            "time from logit models like McFadden's decides which roads and railways get built. <bookmark "
            "mark='b'/> At competition authorities, which estimate demand and then simulate what a merger would do "
            "to prices, as in Part forty-three. <bookmark mark='c'/> At central banks, whose models of the whole "
            "economy are estimated, since Frank Smets and Rafael Wouters, with Bayesian methods: the outside "
            "evidence enters as priors, the compromise from Chapter nine. <bookmark mark='d'/> At firms, whose "
            "pricing teams estimate demand from prices that vary, or that they vary on purpose. <bookmark "
            "mark='e'/> And sometimes all of these at once: Peter Cohen and coauthors used the jumps in Uber's "
            "surge prices to trace out demand for rides, and estimated that in 2015 UberX gave its riders about "
            "two point nine billion dollars of consumer surplus in four American cities."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["google_flu"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17)
        cc.move_to(UP * 1.0)
        lesson = VGroup(
            label(r"a pattern with no model of why people search: \ it broke when the searching changed",
                  font_size=21, color=ERR),
            label(r"Chapter 1's line, \ with a billion data points", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(cc, DOWN, buff=0.6)
        tag = published_tag(r"Ginsberg et al., \ Nature 457 (2009); \ Lazer, \ Kennedy, \ King and Vespignani, \ "
                            r"Science 343 (2014)", corner=DR, font_size=12)
        with self.voiceover(
            "Called it? A forecast with more data than any in this part, and no model. <bookmark mark='a'/> In "
            "2008 Google's engineers, writing in Nature, showed that the share of searches for terms like flu "
            "symptoms tracked the share of doctor visits for flu-like illness, and could estimate it a week or two "
            "before the government's surveillance reports. The basis was a correlation fitted to past years, with "
            "no account of why people search. <bookmark mark='b'/> It worked, for a while. Its first version "
            "missed the 2009 pandemic, which arrived out of season. And in the 2012 to 2013 season it estimated "
            "about twice the doctor visits the Centers for Disease Control recorded; three-week-old official "
            "data forecast the present better. <bookmark mark='c'/> The verdict: partly right. <bookmark "
            "mark='d'/> David Lazer and colleagues traced much of the failure to changes in the search engine "
            "itself: the pattern was a product of conditions that changed. <bookmark mark='e'/> It is Chapter "
            "one's straight line, with a billion data points: the "
            "Lucas critique does not care how big the data are."
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
