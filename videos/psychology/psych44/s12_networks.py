from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403
from videos.psychology.psych44.diagrams import arrow, node

SYMPTOMS = (r"worry", r"poor sleep", r"fatigue", r"poor focus")


class Networks(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_pictures()
        self.same()
        self.decide()

    def card(self):
        card = chapter_card(11, r"Factors or networks?", r"A hidden cause, \ or symptoms that cause each other?",
                            lit={2013: r"Borsboom \& Cramer", 2016: r"Kruis \& Maris"}, part=PART,
                            scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter eleven. Factors or networks?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def two_pictures(self):
        head = heading(r"Two pictures of a disorder")
        F = node(r"F", MODEL, latent=True, r=0.45).move_to([-3.4, 1.4, 0])
        xs = VGroup(*[node(s_, SYMP, r=0.42) for s_ in (r"1", r"2", r"3", r"4")]).arrange(RIGHT, buff=0.45)
        xs.move_to([-3.4, -0.6, 0])
        fa = VGroup(*[arrow(F, x, color=MODEL) for x in xs])
        left_l = label(r"a common cause", font_size=17, color=MODEL).next_to(xs, DOWN, buff=0.35)
        pos = [[2.0, 1.2, 0], [4.8, 1.2, 0], [2.0, -1.0, 0], [4.8, -1.0, 0]]
        ns = VGroup(*[node(s_, SYMP, r=0.42).move_to(p) for s_, p in zip((r"1", r"2", r"3", r"4"), pos)])
        edges = VGroup(*[Line(ns[i].get_center(), ns[j].get_center(), color=GOOD, stroke_width=3, buff=0.45)
                         for i in range(4) for j in range(i + 1, 4)])
        right_l = label(r"symptoms that cause each other", font_size=17, color=GOOD).next_to(ns, DOWN, buff=0.35)
        key = VGroup(*[label(rf"{k + 1}: \ {s_}", font_size=15, color=GREY_A) for k, s_ in enumerate(SYMPTOMS)])
        key.arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.9)
        foot = wrapped_label(r"Borsboom and Cramer, \ 2013: \ poor sleep causes fatigue, \ fatigue causes poor focus, \ "
                             r"poor focus causes worry; \ no hidden ``depression'' needed", 12.4, 19, GOOD)
        foot.next_to(key, DOWN, buff=0.2)
        tag = published_tag(r"Borsboom \& Cramer (2013)")
        with self.voiceover(
            "Two pictures of a disorder. <bookmark mark='a'/> In the first, a hidden cause, the disorder, produces "
            "each symptom, the way a diagnostic category assumes. <bookmark mark='b'/> In the second, Part 39's "
            "symptom network, there's no hidden cause. The symptoms cause each other. <bookmark mark='c'/> Denny Borsboom and Angélique Cramer argued for "
            "the second in 2013: poor sleep causes fatigue, fatigue causes poor focus, poor focus causes worry. No "
            "hidden depression needed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(F), FadeIn(xs), FadeIn(fa), FadeIn(left_l))
            vo.wait_until("b")
            self.play(FadeIn(ns), Create(edges), FadeIn(right_l))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def same(self):
        d = load("network")
        head = heading(r"The same covariances")
        R = heatmap(d["R"], names=[r"1", r"2", r"3", r"4"], cell=0.62, font_size=15, lo=0.0, hi=0.6)
        Pm = heatmap(d["partial"], names=[r"1", r"2", r"3", r"4"], cell=0.62, font_size=15, lo=0.0, hi=0.6)
        R.move_to([-4.4, 0.4, 0])
        Pm.move_to([-0.8, 0.4, 0])
        rl = label(r"correlations from one factor", font_size=14, color=MODEL).next_to(R, UP, buff=0.15)
        pl = label(r"the network's edges", font_size=14, color=GOOD).next_to(Pm, UP, buff=0.15)
        rows = rows_of([
            (r"Psyche: \ one factor, \ loadings 0.8, 0.7, 0.6 and 0.5; \ the correlations follow", WHITE),
            (r"the partial correlations are a network: \ every pair joined, \ the strongest edges where the loadings "
             r"are largest", GOOD),
            (rf"the network reproduces the correlations exactly (largest error {d['max_err']:.0e}): \ any covariance "
             rf"matrix has a network that fits it perfectly", MODEL),
            (r"Kruis and Maris, \ 2016: \ for yes-or-no symptoms, \ the network, \ a latent-variable model and a "
             r"common-cause model are the same distribution", YOU),
        ], 4.6, 18, 0.36).move_to([4.2, -0.1, 0])
        tag = psyche_tag(r"\texttt{sem.factor\_as\_network}")
        with self.voiceover(
            "Can data decide between the pictures? <bookmark mark='a'/> Psyche writes down a single factor, with "
            "loadings of zero point eight, seven, six and five. The correlations follow. <bookmark mark='b'/> Now "
            "compute the partial correlations. They're a network: every pair joined, the strongest edges where the "
            "loadings are largest. <bookmark mark='c'/> The network reproduces the correlations exactly. Any "
            "covariance matrix has a network that fits it perfectly. <bookmark mark='d'/> Joost Kruis and Gunter Maris "
            "proved the stronger result in 2016. For yes-or-no symptoms, the network, a latent-variable model and a "
            "common-cause model are the same distribution. Part 39 stated it; this is the simplest case, computed. The fit can't decide."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(R), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(Pm), FadeIn(pl))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def decide(self):
        head = heading(r"What could decide")
        data = (
            (r"intervene", r"treat sleep alone: \ in a network, \ fatigue and focus should improve too; \ under a "
                           r"common cause, \ they should not", GOOD),
            (r"follow time", r"within-person data over weeks (Part 47): \ does sleep today predict fatigue tomorrow, \ "
                             r"in the same person?", SYMP),
            (r"check stability", r"a network estimated from a few hundred people can change from sample to sample; \ "
                                 r"bootstrap its edges before reading them", AUTH),
            (r"both", r"a common cause and direct links can coexist; \ the question is how much of each", YOU),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=18, width=3.0), wrapped_label(how, 8.8, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "So what could decide? <bookmark mark='a'/> Intervention. Treat sleep alone. In a network, fatigue and "
            "focus should improve too; under a common cause, they shouldn't. <bookmark mark='b'/> Time. With data "
            "within each person over weeks, as in Part 47, does sleep today predict fatigue tomorrow in the same "
            "person? <bookmark mark='c'/> And stability. A network estimated from a few hundred people can change from "
            "sample to sample, so bootstrap its edges before reading them. <bookmark mark='d'/> And the answer may be "
            "both: a common cause and direct links together. The question is how much of each."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
