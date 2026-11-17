from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403


class Growth(VoiceoverScene):
    def construct(self):
        self.card()
        self.trajectories()
        self.split()

    def card(self):
        card = chapter_card(6, r"Growth", r"Does a predictor that changes over time change the person?",
                            lit=(), part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter six. Growth."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def trajectories(self):
        head = heading(r"Trajectories, \ and what changes with them")
        eqs = VGroup(
            MathTex(r"y_{pt} = (\alpha + u_p) + (\beta + v_p)\,t + \gamma\,z_{pt} + \varepsilon_{pt}", font_size=36,
                    color=MODEL),
            MathTex(r"z_{pt} = \bar z_p + (z_{pt} - \bar z_p)", font_size=36, color=GOOD),
        ).arrange(DOWN, buff=0.45).move_to([0, 1.5, 0])
        rows = rows_of([
            (r"Part 31's growth curves and Part 44's latent slopes are this model: \ each person's own start and "
             r"rate", WHITE),
            (r"now add a predictor that changes too: \ sleep, \ stress, \ or practice on each occasion", MODEL),
            (r"its single coefficient $\gamma$ mixes two questions: \ do people who sleep more do better, \ and does "
             r"a person do better on nights they sleep more?", AUTH),
            (r"split it into the person's average and the occasion's departure, \ and give each its own coefficient: "
             r"\ the next two chapters", GOOD),
        ], 12.4, 21, 0.38).move_to([0, -1.5, 0])
        with self.voiceover(
            "Growth is the same model, with time as the predictor. <bookmark mark='a'/> Part 31's growth curves and "
            "Part 44's latent slopes are this model: each person's own start and rate. <bookmark mark='b'/> Now add a "
            "predictor that changes too: sleep, stress, or practice on each occasion. <bookmark mark='c'/> Its single "
            "coefficient mixes two questions. Do people who sleep more do better? And does a person do better on the "
            "nights they sleep more? <bookmark mark='d'/> Split the predictor into the person's average and the "
            "occasion's departure from it, and give each its own coefficient. The next two chapters show why."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eqs[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(eqs[1]))
        self.clear_scene()

    def split(self):
        d = load("growth")
        head = heading(r"Practice, \ week by week")
        A = axes([0.3, 3.7], [-0.6, 0.7], x_length=4.6, y_length=3.0, xticks=None, yticks=[-0.5, 0, 0.5],
                 yfmt=lambda v: f"{v:g}", ylabel=r"coefficient of practice", center=[-3.6, 0.3, 0], font_size=13)
        b = bars(A.ax, [1, 2, 3], [d["mixed"], d["within"], d["between"]], [GREY_B, GOOD, AUTH], width=0.6)
        names = VGroup(*[wrapped_label(t, 1.4, 12, c).next_to(A.ax.c2p(i + 1, -0.6), DOWN, buff=0.1) for i, (t, c) in
                         enumerate(((r"entered once", GREY_B), (r"week's departure", GOOD), (r"child's average", AUTH)))])
        rows = rows_of([
            (r"Psyche: \ 200 children, \ 5 weeks; \ children who practise more on average are those who struggle, \ "
             r"but any child does better in a week they practise more", WHITE),
            (rf"entered once, \ practice gets one coefficient, \ {d['mixed']:.2f}: \ a blend of two opposite "
             rf"effects", AUTH),
            (rf"split, \ the week's departure gets {d['within']:+.2f} (planted +0.5) and the child's average "
             rf"{d['between']:+.2f} (planted -0.4)", GOOD),
            (r"advice for a child (``practise more this week'') needs the first number; \ the blend would understate "
             r"it by more than half", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.growth\_split}; \ statkit's \texttt{lmm}")
        with self.voiceover(
            "Here's what goes wrong if you don't split. <bookmark mark='a'/> Psyche makes two hundred children, "
            "measured for five weeks. Children who practise more on average are the ones who struggle, but any child "
            "does better in a week they practise more. <bookmark mark='b'/> Entered once, practice gets a single "
            "coefficient, a blend of two opposite effects. <bookmark mark='c'/> Split, the week's departure gets about "
            "plus zero point four, a little short of the planted half, since five weeks pin down each child's average only roughly; and the child's average gets about minus zero point four, as planted. "
            "<bookmark mark='d'/> Advice for a child, practise more this week, needs the first number. The blend "
            "would understate it by more than half."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
