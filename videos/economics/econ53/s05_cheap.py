from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


class CheapTalk(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Cheap talk", r"Can words that cost nothing carry information?",
             "Chapter four. Cheap talk.", lit={1982: r"Crawford and Sobel"}, scale=("person", "firm"),
             horizon=("a day",))
        self.setup_()
        self.partitions()
        self.bias()

    def setup_(self):
        rows = VGroup(
            label(r"an adviser sees the state, \ a number between 0 and 1", font_size=23, color=SENDER),
            label(r"she sends a message: \ any words, \ free, \ unverifiable", font_size=23, color=SIGNAL),
            label(r"a decision maker hears it and acts; \ he wants the action to match the state", font_size=23,
                  color=RECEIVER),
            label(r"the adviser wants the action a little higher: \ the state plus a bias $b$", font_size=23,
                  color=ERR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(UP * 0.3)
        q = label(r"if she would exaggerate, \ why should he listen at all?", font_size=24,
                  color=E.ACCENT).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Crawford and Sobel, \ Econometrica 50(6) (1982)", corner=DR, font_size=12)
        hc = history_card(1982, r"Vincent Crawford and Joel Sobel", r"``Strategic information transmission'': \ an "
                          r"adviser who knows more, \ a listener who decides, \ and interests that differ",
                          color=E.ACCENT, width=10.0, font_size=24).move_to(UP * 0.4)
        with self.voiceover(
            "The prosecutor's investigation was a commitment: once designed, it reported what it found. What if "
            "there is no commitment, only talk? Vincent Crawford and Joel Sobel posed it in 1982. <bookmark "
            "mark='a'/> An adviser sees the state of the world, a number between zero and one. <bookmark "
            "mark='b'/> She sends a message: any words she likes, free and unverifiable. <bookmark mark='c'/> A "
            "decision maker hears it and acts, and wants his action to match the state. <bookmark mark='d'/> The "
            "adviser wants the action a little higher than the state, by a bias b: a financial adviser who earns "
            "more when you buy more, an agency that wants a bigger budget. <bookmark mark='e'/> If she would always "
            "exaggerate, why should he listen at all?"
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                if mk == "a":
                    self.play(FadeOut(hc))
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(q, shift=UP * 0.1))
        self.clear_scene()

    def partitions(self):
        Ct = load("cheap")
        rows = Ct["rows"]
        width = 10.0
        lines = VGroup()
        for i, r in enumerate(rows):
            y = 1.9 - 1.15 * i
            base = Line([-width / 2, y, 0], [width / 2, y, 0], color=GREY_B, stroke_width=2)
            ticks = VGroup(*[Line([-width / 2 + width * x, y - 0.18, 0], [-width / 2 + width * x, y + 0.18, 0],
                                  color=SIGNAL, stroke_width=3) for x in r["bounds"]])
            acts = VGroup(*[Triangle(color=RECEIVER, fill_opacity=1).scale(0.08).rotate(PI).move_to(
                [-width / 2 + width * x, y + 0.3, 0]) for x in r["actions"]])
            name = label(rf"$b = {r['b']}$: \ {r['N']} message" + ("s" if r["N"] > 1 else ""), font_size=19,
                         color=WHITE).next_to(base, LEFT, buff=0.3)
            lines.add(VGroup(base, ticks, acts, name))
        lines.move_to(DOWN * 0.1)
        if lines.width > 13.4:
            lines.width = 13.4
        key = label(r"pink ticks: \ where the message changes \qquad blue: \ the action each message brings",
                    font_size=18, color=GREY_A).to_edge(DOWN, buff=0.45)
        r05 = next(r for r in rows if abs(r["b"] - 0.05) < 1e-9)
        with self.voiceover(
            "The answer is that he listens, but to coarse messages. <bookmark mark='a'/> In equilibrium the "
            "adviser does not report the state; she reports which of a few intervals it falls in, and the decision "
            "maker takes the action best for that interval. <bookmark mark='b'/> With a bias of 0.05, three "
            f"messages: the state is below {r05['bounds'][1]:.2f}, between {r05['bounds'][1]:.2f} and "
            f"{r05['bounds'][2]:.2f}, or above. Notice that the intervals widen as the state rises: at the top, "
            "where she most wants to exaggerate, her words are least precise. <bookmark mark='c'/> With a smaller "
            "bias, more messages; with a larger one, fewer, <bookmark mark='d'/> and at a bias of a quarter or "
            "more, only one: nothing she says can be believed, and the talk is babble."
        ) as vo:
            self.play(FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(lines[1][0]), FadeIn(lines[1][3]))
            vo.wait_until("b")
            self.play(Create(lines[1][1]), FadeIn(lines[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.clear_scene()

    def bias(self):
        Ct = load("cheap")
        bs = np.array(Ct["bs"])
        ax = plane([0, 0.3], [0, 0.09], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.6, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3], yticks=[0, 0.03, 0.06, 0.09], xlabel=r"the adviser's bias $b$",
                   ylabel=r"the decision maker's expected loss", xfmt=lambda v: f"{v:.1f}",
                   yfmt=lambda v: f"{v:.2f}", font_size=14)
        loss = path(ax, bs, Ct["loss"], RECEIVER, 3.0, smooth=False)
        bab = seg(ax, 0, Ct["babbling"], 0.3, Ct["babbling"], ERR, 2.0, dashed=True)
        side = VGroup(
            label(r"blue: \ the best equilibrium's \\ loss, \ by bias", font_size=19, color=RECEIVER),
            label(r"red: \ no information at all", font_size=19, color=ERR),
            label(r"the more aligned the interests, \\ the more talk can carry", font_size=21, color=E.ACCENT),
            label(r"the kinks: \ each time a message \\ is lost", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Here is the decision maker's expected loss in the most informative equilibrium, for every bias. "
            "<bookmark mark='a'/> It rises with the bias, with a kink each time one more message is lost, "
            "<bookmark mark='b'/> until it reaches the dashed line, what he would lose with no information at all. "
            "<bookmark mark='c'/> The more aligned the interests, the more talk can carry. That is why we ask "
            "about an adviser's incentives before we weigh her advice, and why commitment, the subject of the next "
            "chapter, can be worth so much."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(loss), FadeIn(side[0]), FadeIn(side[3]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(bab), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()
