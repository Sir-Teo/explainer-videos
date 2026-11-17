from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Model(VoiceoverScene):
    def construct(self):
        self.card()
        self.program()
        self.zoo()
        self.signatures()

    def card(self):
        card = chapter_card(2, r"What a cognitive model is", r"What turns parameters into behaviour?",
                            lit={2018: r"Farrell \& Lewandowsky", 2019: r"Wilson \& Collins"}, part=PART,
                            scale=("person",), marr=("how",))
        with self.voiceover("Chapter two. What a cognitive model is."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def program(self):
        head = heading(r"A program that makes behaviour")
        box = RoundedRectangle(width=7.0, height=3.8, corner_radius=0.12, stroke_color=MODEL, stroke_width=1.5,
                               fill_color=BLACK, fill_opacity=0.5).move_to([-3.0, 0.2, 0])
        code = [r"def q_learner(alpha, beta, rewards):", r"    q = [0.5, 0.5]", r"    for trial in trials:",
                r"        p = softmax(beta * q)", r"        choice = sample(p)", r"        r = reward(choice)",
                r"        q[choice] += alpha * (r - q[choice])", r"        yield choice"]
        lines = VGroup(*[Text(l, font="DejaVu Sans Mono", font_size=14, color=GREY_A) for l in code])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(box)
        rows = rows_of([
            (r"a cognitive model is a generative program: \ parameters in, \ trial-by-trial behaviour out", WHITE),
            (r"run forward, \ it simulates people; \ run backward, \ its likelihood says how probable each observed "
             r"choice was", MODEL),
            (r"the likelihood of the data is the product, \ over trials, \ of the probability the model gave to what "
             r"the person actually did", PERSON),
            (r"Wilson and Collins, \ 2019: \ ten simple rules, \ starting with simulate before you fit", GOOD),
        ], 5.6, 19, 0.38).move_to([3.6, -0.1, 0])
        tag = published_tag(r"Wilson \& Collins (2019)")
        with self.voiceover(
            "What is a cognitive model? <bookmark mark='a'/> A program that generates behaviour: parameters in, "
            "choices out, trial by trial. Here's Part 17's learner in eight lines. <bookmark mark='b'/> Run forward, "
            "it simulates people. Run backward, its likelihood says how probable each observed choice was. "
            "<bookmark mark='c'/> The likelihood of the data is the product, over trials, of the probability the "
            "model gave to what the person actually did. <bookmark mark='d'/> Robert Wilson and Anne Collins wrote "
            "ten simple rules for this craft in 2019. The first is: simulate before you fit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(box), FadeIn(lines))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def zoo(self):
        head = heading(r"Four models of one task")
        data = (
            (r"biased coin", r"chooses right with a fixed probability: \ 1 parameter", GREY_B),
            (r"win-stay, \ lose-shift", r"repeats after a win, \ switches after a loss, \ with some noise: \ 1 "
                                        r"parameter", SYMP),
            (r"Q-learner", r"learns each arm's value at rate $\alpha$, \ chooses by softmax with $\beta$: \ 2 "
                           r"parameters", MODEL),
            (r"Q-learner with perseveration", r"the same, \ plus a pull $\kappa$ toward the last choice: \ 3 "
                                              r"parameters", PERSON),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=17, width=4.2), wrapped_label(how, 8.0, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.2, 0])
        foot = wrapped_label(r"each is a hypothesis about how the choices were made; \ the rest of this part asks how "
                             r"to tell them apart, \ and how far to trust the winner", 12.0, 21, YOU).move_to([0, -2.5, 0])
        with self.voiceover(
            "Here are four models of the same bandit. <bookmark mark='a'/> A biased coin, with one parameter. "
            "<bookmark mark='b'/> Win-stay, lose-shift, with some noise. <bookmark mark='c'/> The Q-learner, with a "
            "learning rate and an inverse temperature. <bookmark mark='d'/> And the Q-learner with perseveration, a "
            "pull toward repeating the last choice. <bookmark mark='e'/> Each is a hypothesis about how the choices "
            "were made. The rest of this part asks how to tell them apart, and how far to trust the winner."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def signatures(self):
        d = load("signatures")
        head = heading(r"Simulate before you fit")
        A = axes([0.3, 4.7], [0, 1.05], x_length=6.0, y_length=3.0, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"probability of staying", center=[-3.1, 0.3, 0],
                 font_size=12)
        xs = np.arange(1, 5)
        bw = bars(A.ax, xs - 0.18, d["win"], GOOD, width=0.32)
        bl = bars(A.ax, xs + 0.18, d["loss"], AUTH, width=0.32)
        names = VGroup(*[wrapped_label(t, 1.3, 11, WHITE).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1) for i, t in
                         enumerate((r"random", r"win-stay lose-shift", r"Q-learning", r"Q + perseveration"))])
        key = VGroup(label(r"after a win", font_size=13, color=GOOD),
                     label(r"after a loss", font_size=13, color=AUTH)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.25)
        rows = rows_of([
            (r"before fitting anything, \ run each model and look at what it does: \ 40 simulated players each", WHITE),
            (r"a simple signature: \ how often a player repeats a choice after a win, \ and after a loss", MODEL),
            (rf"win-stay lose-shift almost never stays after a loss ({100 * d['loss'][1]:.0f}\%); \ Q-learning stays "
             rf"{100 * d['loss'][2]:.0f}\% of the time; \ add perseveration, \ {100 * d['loss'][3]:.0f}\%", PERSON),
            (r"the models disagree where it can be seen: \ that is what makes them testable (Wilson and Collins's "
             r"first rules)", YOU),
        ], 5.6, 18, 0.34).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.simulate}, \ \texttt{fit.stay\_after}")
        with self.voiceover(
            "Before fitting anything, simulate. <bookmark mark='a'/> Run each model and look at what it does: forty "
            "simulated players each. <bookmark mark='b'/> A simple signature is how often a player repeats a choice "
            "after a win, and after a loss. <bookmark mark='c'/> Win-stay lose-shift almost never stays after a loss. "
            "Q-learning stays about three times in five, and with perseveration added, nearly nine times in ten. "
            "<bookmark mark='d'/> The models disagree where it can be seen, and that's what makes them testable. "
            "Simulating first is among Wilson and Collins's ten rules for a reason."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(bw), FadeIn(bl))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
