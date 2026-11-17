from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403


class Mood(VoiceoverScene):
    def construct(self):
        card_section(self, 5, r"Mood as computation", r"What is a mood, \ computationally?", scale=("person",))
        self.rutledge()
        self.simulate()

    def rutledge(self):
        rows_section(self, r"Happiness, \ moment to moment", [
            (r"Rutledge and colleagues, \ 2014: \ in a gambling task, \ momentary happiness was predicted by recent "
             r"expected rewards and reward prediction errors (Part 17), \ not by total winnings", WHITE),
            (r"the same model fitted the ratings of about 18,000 smartphone app users", GOOD),
            (r"Eldar and Niv: \ mood as momentum, \ an integral of recent prediction errors that biases how new "
             r"outcomes are perceived; \ a loop that could tip into mania or depression", MODEL),
            (r"the promise: \ mood disorders as mis-set integrators; \ the evidence so far is from healthy samples and "
             r"models, \ not patients", AUTH),
        ], "What is a mood, computationally? <bookmark mark='a'/> In 2014 Robb Rutledge and colleagues found that in a "
           "gambling task, momentary happiness was predicted by recent expected rewards and reward prediction errors, "
           "Part 17's signal, not by total winnings. <bookmark mark='b'/> The same model fitted the ratings of about "
           "eighteen thousand smartphone app users. <bookmark mark='c'/> Eran Eldar and Yael Niv proposed mood as "
           "momentum: an integral of recent prediction errors that biases how new outcomes are perceived. It's a loop "
           "that could tip into mania or depression. <bookmark mark='d'/> The promise is mood disorders as mis-set "
           "integrators. The evidence so far is from healthy samples and models, not patients.",
           tag=published_tag(r"Rutledge et al.\ (2014)"))
        chips_section(self, r"Testing a computational account of mood", [
            (r"prediction", r"does the integrator's time constant, \ fitted in a week of ratings, \ predict the next "
                            r"month's course?", MODEL),
            (r"reliability", r"is it stable across weeks in the same person?", PERSON),
            (r"intervention", r"do treatments that help mood change the parameter, \ and does the change come first?",
             GOOD),
            (r"the bar", r"each step is a separate study; \ few have been done", AUTH),
        ], "How would a computational account of mood be tested? <bookmark mark='a'/> Prediction: does the "
           "integrator's time constant, fitted from a week of ratings, predict the next month's course? "
           "<bookmark mark='b'/> Reliability: is it stable across weeks in the same person? <bookmark mark='c'/> "
           "Intervention: do treatments that help mood change the parameter, and does the change come first? "
           "<bookmark mark='d'/> Each step is a separate study, and few have been done.")

    def simulate(self):
        d = load("mood")
        T = len(d["rpe"])
        t = np.arange(1, T + 1)
        head = heading(r"Two integrators, \ one run of luck")
        A = axes([0, T + 1], [0, 1.05], x_length=6.2, y_length=2.4, xticks=[1, 10, 20, 30, 40], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", ylabel=r"happiness", center=[-2.9, 1.2, 0],
                 font_size=12)
        B = axes([0, T + 1], [-1.1, 1.1], x_length=6.2, y_length=1.3, xticks=[1, 10, 20, 30, 40], yticks=[-1, 0, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"trial", ylabel=r"RPE",
                 center=[-2.9, -2.0, 0], font_size=11)
        rp = VGroup(*[Line(B.ax.c2p(i, 0), B.ax.c2p(i, float(r)), color=GOOD if r > 0 else AUTH, stroke_width=5)
                      for i, r in zip(t, d["rpe"])])
        cf = curve(A.ax, t, d["fast"], PERSON, stroke_width=4)
        cs = curve(A.ax, t, d["slow"], MODEL, stroke_width=4)
        key = VGroup(label(r"errors fade fast", font_size=13, color=PERSON),
                     label(r"errors fade slowly", font_size=13, color=MODEL)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.15)
        lo_f, lo_s = float(d["fast"][16:26].min()), float(d["slow"][16:26].min())
        rows = rows_of([
            (r"forty gambles, \ with a run of losses in the middle; \ the bars are the prediction errors", WHITE),
            (r"two simulated people with the same weights, \ differing only in how slowly past errors fade", MODEL),
            (rf"the slow integrator swings higher in good times and lower in the run: \ {lo_s:.2f} against "
             rf"{lo_f:.2f}", AUTH),
            (r"one parameter, \ a time constant, \ separates a resilient mood from a sticky one: \ the kind of "
             r"target the programme wants, \ if it can be measured reliably (chapter six)", YOU),
        ], 4.6, 17, 0.3).move_to([4.4, -0.2, 0])
        tag = psyche_tag(r"Rutledge's model, \ illustrative weights")
        with self.voiceover(
            "Here's the idea run forward. <bookmark mark='a'/> Forty gambles, with a run of losses in the middle. The "
            "bars are the prediction errors. <bookmark mark='b'/> Two simulated people have the same weights, and "
            "differ only in how slowly past errors fade. <bookmark mark='c'/> The slow integrator swings higher in "
            "good times, and much lower in the losing run: about zero point one five against zero point three one. "
            "<bookmark mark='d'/> One parameter, a time constant, separates a resilient mood from a sticky one. "
            "That's the kind of target the programme wants, if it can be measured reliably, which is chapter six's "
            "question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[Create(l) for l in rp], lag_ratio=0.05), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cf), Create(cs), run_time=2)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
