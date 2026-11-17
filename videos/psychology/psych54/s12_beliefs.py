from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403


class Beliefs(VoiceoverScene):
    def construct(self):
        card_section(self, 11, r"Beliefs about ability", r"Can a lesson about the brain change grades?",
                     scale=("person", "society"))
        self.mindset()
        self.who()

    def mindset(self):
        head = heading(r"Growth mindset, \ at scale")
        A = axes([0.3, 3.7], [0, 0.6], x_length=5.0, y_length=3.0, xticks=None, yticks=[0, 0.2, 0.4, 0.6],
                 yfmt=lambda v: f"{v:.1f}", ylabel=r"effect (SD)", center=[-3.5, 0.3, 0], font_size=12)
        vals = [0.5, 0.08, 0.1]
        cols = [GREY_B, PERSON, GOOD]
        b = bars(A.ax, [1, 2, 3], vals, cols, width=0.6)
        names = VGroup(*[label(s, font_size=12, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, s in enumerate([r"early small studies", r"meta-analysis", r"national study, \ "
                                                                                          r"lower achievers"])])
        rows = rows_of([
            (r"the idea: \ students who believe ability can grow persist after setbacks; \ a short lesson can teach "
             r"the belief", WHITE),
            (r"early small studies reported large effects (illustrative bar); \ Sisk and colleagues' 2018 "
             r"meta-analysis found about 0.08 on achievement", PERSON),
            (r"Yeager and colleagues, \ 2019: \ a 50-minute online lesson for about 12,000 US ninth-graders, \ "
             r"randomized; \ grades rose by about 0.1 points among lower-achieving students, \ and little overall",
             GOOD),
            (r"small, \ real, \ and cheap: \ for a lesson under an hour, \ ``replicated, \ smaller''", YOU),
        ], 6.2, 19, 0.36).move_to([3.3, -0.1, 0])
        tag = published_tag(r"Yeager et al.\ (2019)")
        with self.voiceover(
            "Can a lesson about the brain change grades? <bookmark mark='a'/> The idea is that students who believe "
            "ability can grow persist after setbacks, and that a short lesson can teach the belief. "
            "<bookmark mark='b'/> Early small studies reported large effects; the first bar is illustrative. Victoria "
            "Sisk and colleagues' meta-analysis in 2018 found about zero point zero eight on achievement. "
            "<bookmark mark='c'/> Then David Yeager and colleagues ran a fifty-minute online lesson for about twelve "
            "thousand American ninth-graders, randomized. Grades rose by about a tenth of a grade point among "
            "lower-achieving students, and little overall. <bookmark mark='d'/> Small, real, and cheap. For a lesson "
            "under an hour, the Ledger says: replicated, smaller."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]), FadeIn(b[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def who(self):
        rows_section(self, r"For whom, \ and where", [
            (r"the national study found the effect only in schools whose peer norms supported challenge-seeking: \ "
             r"the lesson needed fertile soil", MODEL),
            (r"heterogeneity is the finding, \ not a footnote: \ an average of 0.08 can hide 0.2 for some and zero "
             r"for most (Part 47)", PERSON),
            (r"the risk: \ ``praise effort'' turned into slogans, \ without the lesson's content", AUTH),
            (r"how to read an intervention: \ size, \ for whom, \ at what cost, \ and against what alternative", YOU),
        ], "For whom, and where? <bookmark mark='a'/> The national study found the effect only in schools whose peer "
           "norms supported taking on challenges. The lesson needed fertile soil. <bookmark mark='b'/> "
           "Heterogeneity is the finding, not a footnote. An average of zero point zero eight can hide zero point "
           "two for some and nothing for most, which is Part 47's point. <bookmark mark='c'/> The risk is that praise "
           "effort turns into a slogan, without the lesson's content. <bookmark mark='d'/> So read an intervention "
           "by its size, for whom it works, at what cost, and against what alternative.")
