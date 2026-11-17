from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403


class Sequential(VoiceoverScene):
    def construct(self):
        card_section(self, 3, r"Simultaneous against sequential", r"Which line-up procedure is better?",
                     marr=("how",))
        self.history()
        self.roc()

    def history(self):
        rows_section(self, r"A reform, \ adopted", [
            (r"1985: \ Lindsay and Wells introduced the sequential line-up: \ one face at a time, \ a yes or no for "
             r"each, \ no going back", WHITE),
            (r"studies found fewer false identifications of innocent suspects, \ and fewer correct ones, \ but a higher "
             r"ratio of correct to false: \ the diagnosticity ratio", MODEL),
            (r"many US police departments adopted sequential line-ups", PERSON),
            (r"the ratio, \ though, \ depends on where the criterion sits, \ not only on how well a procedure "
             r"separates the guilty from the innocent", AUTH),
        ], "In 1985 a reform was proposed. <bookmark mark='a'/> Rod Lindsay and Gary Wells introduced the sequential "
           "line-up: one face at a time, a yes or no for each, and no going back. <bookmark mark='b'/> Studies found "
           "fewer false identifications of innocent suspects, and fewer correct ones, but a higher ratio of correct "
           "to false, called the diagnosticity ratio. <bookmark mark='c'/> Many American police departments adopted "
           "sequential line-ups. <bookmark mark='d'/> But that ratio depends on where the witness's criterion sits, "
           "not only on how well a procedure separates the guilty from the innocent.",
           tag=published_tag(r"Lindsay \& Wells (1985)"))

    def roc(self):
        d = load("roc")
        head = heading(r"The ROC reverses it")
        A = axes([0, 0.18], [0, 0.75], x_length=5.6, y_length=3.4, xticks=[0, 0.05, 0.1, 0.15], yticks=[0, 0.25, 0.5,
                                                                                                         0.75],
                 xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.2f}", xlabel=r"false IDs of innocent suspects",
                 ylabel=r"correct IDs of culprits", center=[-3.3, 0.2, 0], font_size=12)
        keep_s = np.asarray(d["s_fa"]) <= 0.18
        keep_q = np.asarray(d["q_fa"]) <= 0.18
        cs = curve(A.ax, np.asarray(d["s_fa"])[keep_s][::-1], np.asarray(d["s_hit"])[keep_s][::-1], GOOD,
                   stroke_width=4)
        cq = curve(A.ax, np.asarray(d["q_fa"])[keep_q][::-1], np.asarray(d["q_hit"])[keep_q][::-1], AUTH,
                   stroke_width=4)
        ps = Dot(A.ax.c2p(d["s_point"][0], d["s_point"][1]), radius=0.09, color=GOOD)
        pq = Dot(A.ax.c2p(d["q_point"][0], d["q_point"][1]), radius=0.09, color=AUTH)
        key = VGroup(label(r"simultaneous", font_size=13, color=GOOD), label(r"sequential", font_size=13, color=AUTH))
        key.arrange(RIGHT, buff=0.4).next_to(A, UP, buff=0.2)
        rows = rows_of([
            (rf"two typical operating points: \ simultaneous with diagnosticity {d['s_point'][2]:.1f}; \ sequential, \ "
             rf"more cautious, \ {d['q_point'][2]:.1f}: \ sequential looks better", PERSON),
            (rf"the curves: \ at every false-ID rate, \ simultaneous gives more correct IDs; \ partial areas "
             rf"{d['pauc_s']:.3f} against {d['pauc_q']:.3f}", GOOD),
            (r"Wixted and Mickes, \ 2014, \ and laboratory and field data since: \ sequential mostly shifts the "
             r"criterion, \ and loses a little discrimination", MODEL),
            (r"the 2020 recommendations no longer prefer sequential; \ a reform the field had championed was reversed "
             r"by its own better measurement", YOU),
        ], 6.0, 18, 0.34).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{work.lineup\_roc}, \ 100{,}000 simulated line-ups each")
        with self.voiceover(
            "The ROC curve reversed it. <bookmark mark='a'/> Here are two typical operating points. Simultaneous, "
            "with a diagnosticity ratio of about five. Sequential, more cautious, with about seven and a half. By the "
            "ratio, sequential looks better. <bookmark mark='b'/> Now the whole curves. At every rate of false "
            "identifications, the simultaneous line-up gives more correct ones. <bookmark mark='c'/> John Wixted and "
            "Laura Mickes made this argument in 2014, and laboratory and field data since agree: the sequential "
            "procedure mostly shifts the criterion, and loses a little discrimination. <bookmark mark='d'/> The 2020 "
            "recommendations no longer prefer sequential line-ups. A reform the field had championed was reversed by "
            "its own better measurement."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(ps, scale=1.5), FadeIn(pq, scale=1.5))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cs), Create(cq))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
