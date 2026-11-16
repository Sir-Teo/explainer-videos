from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


class Control(VoiceoverScene):
    def construct(self):
        self.card()
        self.triadic()

    def card(self):
        card = chapter_card(7, r"Helplessness and control", r"What is learned when nothing works?",
                            lit={1967: r"Seligman \& Maier", 2016: r"Maier \& Seligman"}, part=PART,
                            scale=("circuit", "person"), marr=("how",))
        with self.voiceover("Chapter seven. Helplessness and control."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def triadic(self):
        d = load("helpless")
        head = heading(r"The triadic design, \ computed")
        A = axes([0.5, 10.5], [0, 1.05], x_length=5.4, y_length=3.2, xticks=[1, 5, 10], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"test trial in the shuttle box",
                 ylabel=r"share escaping", center=[-3.3, -0.1, 0], font_size=14)
        t = np.arange(1, 11)
        cols = {"escapable": GOOD, "none": GREY_A, "inescapable": AUTH}
        lines = VGroup(*[curve(A.ax, t, d[k], c, stroke_width=4) for k, c in cols.items()])
        key = legend([(GOOD, r"escapable first"), (GREY_A, r"no shock first"), (AUTH, r"inescapable first")],
                     font_size=14).move_to(A.ax.c2p(7.5, 0.45))
        rows = rows_of([
            (r"Psyche: \ a learner believes, \ to some degree, \ that its actions control shock, \ and tries to "
             r"escape as often as it believes; \ trying updates the belief", WHITE),
            (r"with escapable shock first, \ the belief in control is strong, \ and it escapes at once", GOOD),
            (r"with inescapable shock first, \ trying never worked, \ so it rarely tries, \ and never finds out the "
             r"new box is different", AUTH),
            (r"Maier and Seligman, \ 2016: \ in rats, \ prolonged shock triggers passivity by default; \ detecting "
             r"control, \ in prefrontal cortex, \ switches it off: \ control is what is learned", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.helplessness}; \ Maier \& Seligman (2016)")
        with self.voiceover(
            "Psyche runs the triadic design as a belief about control. <bookmark mark='a'/> A learner believes, to "
            "some degree, that its actions control the shock, and tries to escape as often as it believes. Trying "
            "updates the belief. <bookmark mark='b'/> With escapable shock first, the belief in control is strong, "
            "and it escapes at once. <bookmark mark='c'/> With inescapable shock first, trying never worked, so it "
            "rarely tries, and never finds out that the new box is different. The learner with no shock first sits "
            "between, and learns. <bookmark mark='d'/> The 2016 revision puts the default the other way round: in "
            "rats, prolonged shock triggers passivity by default, and detecting control, in prefrontal cortex, "
            "switches it off. Control is what's learned. In depression, the question becomes what makes people "
            "stop detecting control."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(lines[2]), Create(lines[1]), FadeIn(key))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
