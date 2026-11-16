from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Goodfit(VoiceoverScene):
    def construct(self):
        self.card()
        self.flexible()
        self.space()
        self.ppc()

    def card(self):
        card = chapter_card(7, r"A good fit can be bad", r"What does the model rule out?",
                            lit={2000: r"Roberts \& Pashler", 2017: r"Palminteri et al."}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter seven. A good fit can be bad."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def flexible(self):
        head = heading(r"How persuasive is a good fit?")
        rows = rows_of([
            (r"Roberts and Pashler, \ 2000: \ a fit is persuasive only if the model could have failed", WHITE),
            (r"ask what data the model cannot produce: \ a model that fits every possible outcome explains none of "
             r"them", AUTH),
            (r"ask how variable the data are: \ a fit inside the noise says little", PERSON),
            (r"and ask whether a plausible alternative fits as well", MODEL),
            (r"the strongest evidence is a prediction made before the data, \ of an effect the model must produce",
             GOOD),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        tag = published_tag(r"Roberts \& Pashler (2000)")
        with self.voiceover(
            "A model that fits well isn't therefore a good model. <bookmark mark='a'/> In 2000 Seth Roberts and Harold "
            "Pashler argued that a fit is persuasive only if the model could have failed. <bookmark mark='b'/> Ask "
            "what data the model can't produce. A model that fits every possible outcome explains none of them. "
            "<bookmark mark='c'/> Ask how variable the data are. A fit inside the noise says little. "
            "<bookmark mark='d'/> Ask whether a plausible alternative fits as well. <bookmark mark='e'/> And the "
            "strongest evidence is a prediction made before the data, of an effect the model must produce."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def ppc(self):
        d = load("ppc")
        head = heading(r"Does the model make the effect?")
        A = axes([0.3, 2.7], [0.5, 1.0], x_length=4.8, y_length=3.2, xticks=None, yticks=[0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{v:g}", ylabel=r"P(stay)", center=[-3.5, 0.3, 0], font_size=13)
        xs = np.array([1, 2])
        b0 = bars(A.ax, xs - 0.22, d["obs"], [WHITE] * 2, width=0.2)
        b1 = bars(A.ax, xs, d["pred_q"], [AUTH] * 2, width=0.2)
        b2 = bars(A.ax, xs + 0.22, d["pred_persev"], [GOOD] * 2, width=0.2)
        names = VGroup(label(r"after a win", font_size=14, color=GREY_A).next_to(A.ax.c2p(1, 0.5), DOWN, buff=0.1),
                       label(r"after a loss", font_size=14, color=GREY_A).next_to(A.ax.c2p(2, 0.5), DOWN, buff=0.1))
        key = VGroup(label(r"data", font_size=13, color=WHITE), label(r"Q-learner", font_size=13, color=AUTH),
                     label(r"with perseveration", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.3).next_to(A, UP, buff=0.3)
        rows = rows_of([
            (r"Psyche's learners have a pull toward repeating themselves; \ fit both models, \ then simulate from "
             r"each fit", WHITE),
            (rf"after a loss the learners stay {100 * d['obs'][1]:.0f}\% of the time; \ the plain Q-learner's "
             rf"simulations stay {100 * d['pred_q'][1]:.0f}\%: \ it cannot make the effect", AUTH),
            (rf"with perseveration, \ {100 * d['pred_persev'][1]:.0f}\%", GOOD),
            (r"Palminteri, \ Wyart and Koechlin, \ 2017: \ check that the winning model produces the data's "
             r"signature, \ not only that it scores best", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.posterior\_predictive}, \ 30 simulated learners")
        with self.voiceover(
            "Here's the check in practice. <bookmark mark='a'/> Psyche's learners have a pull toward repeating "
            "themselves. Fit both models, then simulate new data from each fit. <bookmark mark='b'/> After a loss, the "
            "learners stay with the same arm about eighty-five percent of the time. The plain Q-learner's simulations "
            "stay only seventy percent. Whatever its score, it can't make the effect. <bookmark mark='c'/> With "
            "perseveration, the simulations match. <bookmark mark='d'/> Stefano Palminteri, Valentin Wyart and Etienne "
            "Koechlin made this the rule in 2017: check that the winning model produces the data's signature, not "
            "only that it scores best."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(key), FadeIn(b0))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b1))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b2))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def space(self):
        d = load("flex")
        head = heading(r"What can each model produce?")
        A = axes([0, 1.02], [0, 1.02], x_length=4.0, y_length=4.0, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"stay after a loss",
                 ylabel=r"stay after a win", center=[-4.0, 0.0, 0], font_size=12)
        w = np.asarray(d["wsls"]); q = np.asarray(d["q"]); qp = np.asarray(d["q_persev"])
        dw = scatter(A.ax, w[:, 1], w[:, 0], SYMP, radius=0.05)
        dq = scatter(A.ax, q[:, 1], q[:, 0], MODEL, radius=0.05)
        dp = scatter(A.ax, qp[:, 1], qp[:, 0], PERSON, radius=0.05)
        rows = rows_of([
            (r"60 random parameter settings per model, \ simulated: \ each dot is one possible player", WHITE),
            (r"win-stay lose-shift lives in one corner: \ it can never stay after a loss more than its error rate "
             r"allows", SYMP),
            (r"Q-learning covers a band; \ with perseveration, \ almost the whole square", MODEL),
            (r"Roberts and Pashler's point: \ a model that can produce anything is not confirmed by producing this; \ "
             r"ask what it rules out", YOU),
        ], 7.0, 19, 0.36).move_to([2.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.simulate}, \ random parameters")
        with self.voiceover(
            "Roberts and Pashler's question can be drawn. <bookmark mark='a'/> Take sixty random parameter settings "
            "for each model, and simulate. Each dot is one possible player, placed by how often it stays after a "
            "loss and after a win. <bookmark mark='b'/> Win-stay lose-shift lives in one corner. It can never stay "
            "after a loss more than its error rate allows. <bookmark mark='c'/> Q-learning covers a band, and with "
            "perseveration added, almost the whole square. <bookmark mark='d'/> A model that can produce anything "
            "isn't confirmed by producing this. Ask what it rules out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(dw))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(dq), FadeIn(dp))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
