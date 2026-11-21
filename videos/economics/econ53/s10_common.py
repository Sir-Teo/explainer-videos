from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


class Common(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Common knowledge", r"Can two honest people agree to disagree?",
             "Chapter eight. Common knowledge.", lit={1976: r"Aumann", 1989: r"Rubinstein"}, scale=("person",),
             horizon=("a day",))
        self.aumann()
        self.dialogue()
        self.email()

    def aumann(self):
        rows = VGroup(
            label(r"two people with the same prior, \ who see different evidence", font_size=23, color=WHITE),
            label(r"if their beliefs about an event are common knowledge, \ the beliefs are equal", font_size=23,
                  color=BELIEF),
            label(r"common knowledge: \ both know, \ both know that both know, \ and so on, \ for ever", font_size=23,
                  color=THEORY),
            label(r"so persistent disagreement needs different priors, \ or someone who is not reasoning",
                  font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(UP * 0.2)
        tag = published_tag(r"Aumann, \ Annals of Statistics 4(6) (1976)", corner=DR, font_size=12)
        hc = history_card(1976, r"Robert Aumann", r"``Agreeing to disagree'': \ two people with a common prior "
                          r"cannot, once their beliefs are common knowledge", color=BELIEF, width=10.0,
                          font_size=24).move_to(UP * 0.4)
        with self.voiceover(
            "Everything so far assumed people share a prior and update by Bayes's rule. Robert Aumann drew a "
            "startling consequence in 1976. <bookmark mark='a'/> Take two people with the same prior who have seen "
            "different evidence. <bookmark mark='b'/> If their beliefs about some event are common knowledge, "
            "those beliefs must be equal. <bookmark mark='c'/> Common knowledge means that both know them, both "
            "know that both know, and so on without end. <bookmark mark='d'/> They cannot agree to disagree. "
            "Lasting disagreement between honest people needs different priors, or reasoning that is not "
            "Bayesian. That is a strong claim, so watch how it works."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                if mk == "a":
                    self.play(FadeOut(hc))
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def dialogue(self):
        A = load("agree")
        D = A["dialogue"]
        n = D["n"]
        boxes = VGroup(*[Square(side_length=0.8, stroke_color=GREY_B, stroke_width=1.5) for _ in range(n)]).arrange(
            RIGHT, buff=0.12).move_to(UP * 1.9)
        nums = VGroup(*[label(str(k + 1), font_size=20, color=WHITE).move_to(b) for k, b in enumerate(boxes)])
        ev = VGroup(*[boxes[k].copy().set_fill(GUILTY, 0.35).set_stroke(width=0) for k in D["event"]])
        true_ = boxes[D["state"]].copy().set_stroke(SENDER, 4)

        def bracket(part, color, y):
            g = VGroup()
            for cell in part:
                left = boxes[cell[0]].get_left()[0] + 0.04
                right = boxes[cell[-1]].get_right()[0] - 0.04
                g.add(Line([left, y, 0], [right, y, 0], color=color, stroke_width=5))
            return g

        ba = bracket(D["a"], RECEIVER, 1.2)
        bb = bracket(D["b"], SIGNAL, 0.95)
        la = label(r"Ann knows which blue group", font_size=17, color=RECEIVER).next_to(ba, LEFT, buff=0.2)
        lb = label(r"Bob, \ which pink group", font_size=17, color=SIGNAL).next_to(bb, LEFT, buff=0.2)
        ln = label(r"nine equally likely states; \ the event: \ 3 or 4 \ (red); \ the truth: \ 1 \ (gold)",
                   font_size=19, color=WHITE).next_to(boxes, UP, buff=0.3)
        hist = A["history"]
        names = {"A": ("Ann", RECEIVER), "B": ("Bob", SIGNAL)}
        lines = VGroup()
        for h in hist:
            nm, col = names[h["who"]]
            frac = {1 / 3: r"1/3", 1 / 2: r"1/2", 1 / 4: r"1/4"}
            f = next((v for k, v in frac.items() if abs(k - h["posterior"]) < 1e-9), f"{h['posterior']:.2f}")
            lines.add(label(rf"round {h['round'] + 1}: \ {nm} says {f}", font_size=22, color=col))
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 1.6)
        tag = published_tag(r"Geanakoplos and Polemarchakis, \ JET 28(1) (1982)", corner=DR, font_size=12)
        hc = history_card(1982, r"John Geanakoplos and Heraklis Polemarchakis", r"``We can't disagree forever'': "
                          r"\ announce beliefs back and forth, and they converge", color=THEORY, width=10.0,
                          font_size=24).move_to(UP * 0.4)
        with self.voiceover(
            "John Geanakoplos and Heraklis Polemarchakis showed how agreement arrives. <bookmark mark='a'/> Nine "
            "equally likely states. The question is whether the state is 3 or 4; the truth is 1. <bookmark "
            "mark='b'/> Ann knows only which of three blue groups the state is in; Bob knows which of the pink "
            "groups. <bookmark mark='c'/> Ann sees states 1 to 3, one of which is in the event: she says one third. "
            "<bookmark mark='d'/> Bob sees 1 to 4, two of which are in the event: he says one half. <bookmark "
            "mark='e'/> But Ann's announcement told Bob something: had the state been 4, 5 or 6, she would have "
            "said one third as well, while a 7, 8 or 9 would have made her say zero. Each announcement rules "
            "states out, for both of them. Ann now reasons from what Bob said and says one third again; "
            "<bookmark mark='f'/> Bob, knowing what Ann's repeat rules out, comes round to one third. They agree, "
            "having exchanged nothing but their beliefs."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(hc))
            self.play(FadeIn(boxes), FadeIn(nums), FadeIn(ev), FadeIn(true_), FadeIn(ln))
            vo.wait_until("b")
            self.play(Create(ba), FadeIn(la), Create(bb), FadeIn(lb))
            for mk, ln_ in zip("cdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln_, shift=RIGHT * 0.1))
        self.clear_scene()

    def email(self):
        A = load("agree")
        em = A["email"]
        eps = np.array(A["eps"])
        ax = plane([0, 0.5], [0.4, 0.7], center=RIGHT * 2.8 + DOWN * 0.6, x_length=5.4, y_length=3.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0.4, 0.5, 0.6, 0.7],
                   xlabel=r"chance a message is lost", ylabel=r"belief the other saw one fewer",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=13)
        z = path(ax, eps, A["z"], BELIEF, 3.0)
        half = DashedLine(ax.ax.c2p(0, 0.5), ax.ax.c2p(0.5, 0.5), color=GREY_B, stroke_width=1.4)
        steps = VGroup(
            label(r"two generals should attack together, \\ only in a rare state", font_size=19, color=WHITE),
            label(r"each email confirms the last; \\ each is lost with a small chance", font_size=19, color=SIGNAL),
            label(r"after any number of emails, \\ each thinks it more likely than not \\ that the other saw one "
                  r"fewer", font_size=19, color=BELIEF),
            label(r"the one who saw none will not attack, \\ so neither will the one who saw one, \\ nor two, \ "
                  r"\dots", font_size=19, color=ERR),
            label(r"almost common knowledge \\ is not enough", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.5)
        tag = published_tag(r"Rubinstein, \ AER 79(3) (1989)", corner=DR, font_size=12)
        with self.voiceover(
            "Common knowledge is demanding, and Ariel Rubinstein showed how much. <bookmark mark='a'/> Two generals "
            "should attack together, but only in a rare state of the world that one of them observes. <bookmark "
            "mark='b'/> He emails; the other's computer confirms automatically; that confirmation is confirmed, "
            "and so on, each email lost with a small chance, after which the exchange stops. <bookmark mark='c'/> "
            f"A general who has seen some number of emails knows the last one he sent may have been lost, and puts "
            f"probability {em['z']:.2f} on the other having seen one fewer: more likely than not, however many "
            "were exchanged. <bookmark mark='d'/> The general who saw none will not attack. So one who saw one "
            "email, thinking it likely the other saw none, will not either; nor one who saw two; and so on up. "
            "Nobody ever attacks, even after a hundred confirmations. <bookmark mark='e'/> Almost common knowledge "
            "is not common knowledge, and coordination can depend on the difference."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(ax), Create(half))
            for mk, s_ in zip("abcde", steps):
                vo.wait_until(mk)
                anims = [FadeIn(s_, shift=RIGHT * 0.1)]
                if mk == "c":
                    anims.append(Create(z))
                self.play(*anims)
        self.clear_scene()
