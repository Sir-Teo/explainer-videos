from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403


class Bias(VoiceoverScene):
    def construct(self):
        card_section(self, 4, r"Efficiency explains biases", r"Does an efficient code see the world straight?")
        self.tilt()
        self.wei()
        self.more()

    def tilt(self):
        d = load("tilt")
        head = heading(r"The tilt after-effect, \ predicted")
        A = axes([-48, 48], [-5.5, 5.5], x_length=5.6, y_length=3.2, xticks=[-40, -20, 0, 20, 40],
                 yticks=[-4, 0, 4], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"test minus adapter (degrees)", ylabel=r"perceived shift (degrees)", center=[-3.3, 0.2, 0],
                 font_size=12)
        c = curve(A.ax, d["tests"], d["shift"], PERSON, stroke_width=4)
        zero = DashedLine(A.ax.c2p(-48, 0), A.ax.c2p(48, 0), color=GREY_B, stroke_width=1.5)
        i20 = int(np.argmin(abs(np.asarray(d["tests"]) - 20)))
        pk = Dot(A.ax.c2p(d["tests"][i20], d["shift"][i20]), radius=0.08, color=AUTH)
        rows = rows_of([
            (r"Psyche's population: \ 72 units tuned to orientation; \ adaptation lowers the gain of those tuned "
             r"near the adapter", WHITE),
            (r"the readout still assumes the old gains, \ so every test is pushed away from the adapter", MODEL),
            (rf"largest 10 to 25 degrees away: \ about {d['shift'][i20]:.0f} degrees at 20, \ your first number "
             rf"(people report a few degrees)", AUTH),
            (r"why adapt at all? \ re-centring the code on the recent input keeps it efficient when the world "
             r"changes; \ the illusion is the price", GOOD),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{efficient.tilt\_aftereffect}")
        with self.voiceover(
            "Start with the after-effect you just saw. <bookmark mark='a'/> Psyche's population has seventy-two "
            "units tuned to orientation. Adaptation lowers the gain of the units tuned near the adapter. "
            "<bookmark mark='b'/> The readout still assumes the old gains, so every test is pushed away from the "
            "adapter. <bookmark mark='c'/> The shift is largest ten to twenty-five degrees away: about four degrees "
            "at twenty, your first number. People report a few degrees. <bookmark mark='d'/> Why adapt at all? "
            "Re-centring the code on recent input keeps it efficient when the world changes. The illusion is the "
            "price."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(pk, scale=1.5))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def wei(self):
        d = load("bias")
        head = heading(r"Anti-Bayesian, \ and efficient")
        th = np.asarray(d["theta"])
        A1 = axes([0, 180], [0, 1.6], x_length=4.4, y_length=2.0, xticks=[0, 45, 90, 135, 180], yticks=[0, 1.0],
                  xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", ylabel=r"how common", center=[-4.0, 1.7, 0],
                  font_size=11)
        A2 = axes([0, 180], [-3, 3], x_length=4.4, y_length=2.0, xticks=[0, 45, 90, 135, 180], yticks=[-2, 0, 2],
                  xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"orientation (degrees)",
                  ylabel=r"bias", center=[-4.0, -1.2, 0], font_size=11)
        p = np.asarray(d["prior"])
        cp = curve(A1.ax, th, p / p.max() * 1.4, CROWD, stroke_width=3)
        cb = curve(A2.ax, th, d["bias"], AUTH, stroke_width=3)
        z = DashedLine(A2.ax.c2p(0, 0), A2.ax.c2p(180, 0), color=GREY_B, stroke_width=1.5)
        rows = rows_of([
            (r"a plain Bayesian observer is pulled toward what is common: \ toward vertical and horizontal", WHITE),
            (r"but people judge near-cardinal lines as pushed away from cardinal", AUTH),
            (r"Wei and Stocker, \ 2015: \ if the encoder spends its precision where the prior is high, \ the "
             r"likelihood is lopsided, \ and the posterior lands on the far side: \ repulsion", MODEL),
            (r"Psyche's efficient observer: \ biases of about 2.5 degrees away from 0 and 90, \ your second "
             r"number", GOOD),
            (r"their 2017 rule, \ bias proportional to the slope of discrimination thresholds squared, \ held across "
             r"many published data sets", PERSON),
        ], 6.4, 18, 0.32).move_to([3.0, -0.1, 0])
        tag = psyche_tag(r"\texttt{efficient.efficient\_bias}")
        tag2 = published_tag(r"Wei \& Stocker (2015)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Now a bias that seemed to break the Bayesian story. <bookmark mark='a'/> Vertical and horizontal are "
            "the commonest orientations, so a plain Bayesian observer should be pulled toward them. "
            "<bookmark mark='b'/> But people judge lines near vertical as pushed away from vertical. "
            "<bookmark mark='c'/> In 2015 Xue-Xin Wei and Alan Stocker showed why. If the encoder spends its "
            "precision where the prior is high, the likelihood becomes lopsided, and the posterior lands on the far "
            "side. The result is repulsion. <bookmark mark='d'/> Psyche's efficient observer is biased about two and "
            "a half degrees away from vertical and horizontal. That's your second number. <bookmark mark='e'/> Their "
            "2017 rule, that the bias is proportional to the slope of the squared discrimination threshold, held "
            "across many published data sets."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A1), FadeIn(A2), Create(z))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(cp))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(cb), run_time=2.0)
            for m, r in zip("de", rows[3:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def more(self):
        chips_section(self, r"What else efficiency explains", [
            (r"Weber's law", r"a code whose resources follow a heavy-tailed distribution of intensities gives "
                             r"thresholds proportional to intensity (Part 11; \ Ganguli and Simoncelli)", MODEL),
            (r"capacity limits", r"working memory as a channel with limited information (Part 19): \ precision "
                                 r"falls as items are added", PERSON),
            (r"value", r"neurons coding value normalize by the options on offer (Part 26), \ which can produce "
                       r"context effects in choice", AUTH),
            (r"the warning", r"almost any bias can be fitted by some prior and some resource limit; \ the test is a "
                             r"prior measured independently", YOU),
        ], "What else does efficiency explain? <bookmark mark='a'/> Weber's law: a code whose resources follow a "
           "heavy-tailed distribution of intensities gives thresholds proportional to intensity, as Deep Ganguli and "
           "Eero Simoncelli showed. That's Part 11. <bookmark mark='b'/> Capacity limits: working memory as a "
           "channel with limited information, Part 19, where precision falls as items are added. "
           "<bookmark mark='c'/> Value: neurons that code value normalize by the options on offer, which can "
           "produce context effects in choice, Part 26. <bookmark mark='d'/> And the warning: almost any bias can be "
           "fitted by some prior and some resource limit. The real test is a prior that's measured independently, as "
           "Laughlin measured his fly's world.")
