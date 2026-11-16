from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403


class Rate(VoiceoverScene):
    def construct(self):
        card_section(self, 5, r"Rate-distortion", r"What is the cheapest representation that is good enough?",
                     marr=("what",))
        self.theory()
        self.shepard()

    def theory(self):
        rows_section(self, r"Shannon's other theorem", [
            (r"rate: \ how many bits a representation carries about the stimulus; \ distortion: \ the expected "
             r"cost of the errors it allows", WHITE),
            (r"rate-distortion theory (Shannon, \ 1959): \ for each tolerated distortion, \ the least rate that "
             r"achieves it", MODEL),
            (r"minimize \ rate $+\ \beta \times$ distortion: \ $\beta$ is how much errors cost", PERSON),
            (r"Blahut and Arimoto's algorithm finds the best channel by alternating two simple updates", GOOD),
            (r"for a brain: \ perception and memory as channels that must be cheap, \ and errors that should be "
             r"cheap ones", YOU),
        ], "What's the cheapest representation that's good enough? <bookmark mark='a'/> Rate is how many bits a "
           "representation carries about the stimulus. Distortion is the expected cost of the errors it allows. "
           "<bookmark mark='b'/> Shannon's rate-distortion theory gives, for each tolerated distortion, the least "
           "rate that achieves it. <bookmark mark='c'/> Equivalently, minimize the rate plus beta times the "
           "distortion, where beta is how much errors cost. <bookmark mark='d'/> Richard Blahut and Suguru Arimoto's "
           "algorithm finds the best channel by alternating two simple updates. <bookmark mark='e'/> For a brain, "
           "perception and memory are channels that must be cheap, and their errors should be cheap ones.")

    def shepard(self):
        d = load("rd")
        head = heading(r"Shepard's law, \ derived")
        A = axes([0, 12], [0, 1.05], x_length=5.6, y_length=3.2, xticks=[0, 4, 8, 12], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"distance between stimuli",
                 ylabel=r"confusion (generalization)", center=[-3.3, 0.2, 0], font_size=12)
        dist = np.asarray(d["distance"])
        cols = [AUTH, PERSON, GOOD]
        cs = [curve(A.ax, dist[:13], d["gradients"][i][:13], cols[i], stroke_width=4) for i in range(3)]
        key = VGroup(*[label(rf"{r_:.1f} bits", font_size=13, color=c) for r_, c in zip(d["rates"], cols)])
        key.arrange(RIGHT, buff=0.4).next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"Part 22: \ Shepard, \ 1987: \ across species and stimuli, \ generalization falls off roughly "
             r"exponentially with psychological distance", WHITE),
            (r"Psyche's channel at three costs of error: \ a cheap code (low rate) confuses near stimuli broadly", AUTH),
            (r"a costly one generalizes narrowly; \ every gradient falls smoothly with distance", GOOD),
            (r"Sims, \ 2018: \ fitted to people's confusions, \ such a channel gives the law's shape, \ with no assumption about mental "
             r"space's geometry", MODEL),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{efficient.blahut\_arimoto}")
        tag2 = published_tag(r"Sims (2018)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Here's a law it derives. <bookmark mark='a'/> In Part 22, Roger Shepard's universal law of "
            "generalization: across species and stimuli, generalization falls off roughly exponentially with "
            "psychological distance. <bookmark mark='b'/> Here's Psyche's best channel at three costs of error. A "
            "cheap code, with a low rate, confuses nearby stimuli broadly. <bookmark mark='c'/> A costly one "
            "generalizes narrowly, and every gradient is a smooth fall. <bookmark mark='d'/> In 2018 Chris Sims "
            "showed that the law falls out of an efficient channel, without any assumption about the geometry of "
            "mental space."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cs[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(cs[1]), Create(cs[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
