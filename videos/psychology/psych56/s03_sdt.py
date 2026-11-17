from __future__ import annotations

from scipy import stats

from videos.psychology.psych56.common import *  # noqa: F403


class Sdt(VoiceoverScene):
    def construct(self):
        card_section(self, 2, r"The line-up as signal detection", r"What is a witness deciding?", marr=("how",))
        self.model()
        self.estimator()

    def model(self):
        x = np.linspace(-3.5, 5, 300)
        head = heading(r"Six faces, \ one criterion")
        A = axes([-3.5, 5], [0, 0.45], x_length=6.0, y_length=2.8, xticks=[-2, 0, 1.5, 3], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"memory match", center=[-3.0, 0.6, 0], font_size=12)
        cn = curve(A.ax, x, stats.norm.pdf(x), GREY_B, stroke_width=3)
        cc = curve(A.ax, x, stats.norm.pdf(x, 1.5), PERSON, stroke_width=4)
        crit = DashedLine(A.ax.c2p(1.0, 0), A.ax.c2p(1.0, 0.45), color=AUTH)
        lab = VGroup(label(r"innocent faces", font_size=14, color=GREY_B).move_to(A.ax.c2p(-1.6, 0.42)),
                     label(r"the culprit", font_size=14, color=PERSON).move_to(A.ax.c2p(2.6, 0.42)),
                     label(r"criterion", font_size=14, color=AUTH).next_to(A.ax.c2p(1.0, 0.45), UP, buff=0.05))
        rows = rows_of([
            (r"each face gives a memory-match signal: \ innocent faces around 0, \ the culprit higher (here $d'$ = "
             r"1.5)", WHITE),
            (r"the witness picks the best match if it passes a criterion: \ Clark's and Wixted and Mickes's model", MODEL),
            (r"a lax criterion: \ more culprits picked, \ and more innocent suspects; \ a strict one: \ fewer of both",
             PERSON),
            (r"so a procedure must be judged by the trade-off, \ an ROC (Part 12), \ not by one pair of rates", YOU),
        ], 6.4, 19, 0.36).move_to([3.2, -0.4, 0])
        tag = psyche_tag(r"Part 21's line-up observer")
        with self.voiceover(
            "What is a witness deciding? <bookmark mark='a'/> Each face gives a memory-match signal. Innocent faces "
            "cluster around zero, and the culprit higher, here by one and a half standard deviations. "
            "<bookmark mark='b'/> The witness picks the best match, if it passes a criterion. That's the model of "
            "Steven Clark, and of John Wixted and Laura Mickes. <bookmark mark='c'/> A lax criterion picks more "
            "culprits, and more innocent suspects. A strict one picks fewer of both. <bookmark mark='d'/> So a "
            "procedure has to be judged by the whole trade-off, an ROC curve as in Part 12, not by one pair of rates."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(cn), Create(cc), FadeIn(lab[0]), FadeIn(lab[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(crit), FadeIn(lab[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), crit.animate.shift(RIGHT * 0.5), lab[2].animate.shift(RIGHT * 0.5))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def estimator(self):
        chips_section(self, r"What lowers $d'$", [
            (r"viewing conditions", r"distance, \ light, \ duration: \ a glimpse at 30 metres is not a look at 3", PERSON),
            (r"stress and weapons", r"attention drawn to a weapon (``weapon focus'') leaves less for the face (Part 18)",
             AUTH),
            (r"cross-race effect", r"faces of other groups are recognized less accurately, \ with more false "
                                   r"identifications", MODEL),
            (r"delay", r"Part 21's forgetting: \ weeks between the crime and the line-up", SYMP),
        ], "Gary Wells divided the factors into two kinds. Estimator variables lower d prime, and the justice system "
           "can't control them. <bookmark mark='a'/> Viewing conditions: distance, light and duration. A glimpse at "
           "thirty metres isn't a look at three. <bookmark mark='b'/> Stress and weapons: attention drawn to a weapon "
           "leaves less for the face. That's weapon focus, and Part 18's attention. <bookmark mark='c'/> The "
           "cross-race effect: faces of other groups are recognized less accurately, with more false "
           "identifications. <bookmark mark='d'/> And delay: Part 21's forgetting, over the weeks between the crime "
           "and the line-up.")
