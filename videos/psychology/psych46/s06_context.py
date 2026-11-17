from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


def option_plot(center, opts, colors, names, x_length=4.0, y_length=3.0):
    A = axes([0, 10], [0, 10], x_length=x_length, y_length=y_length, xticks=[0, 5, 10], yticks=[0, 5, 10],
             xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"quality", ylabel=r"value for money",
             center=center, font_size=12)
    dots = VGroup(*[Dot(A.ax.c2p(*o), radius=0.1, color=c) for o, c in zip(opts, colors)])
    labs = VGroup(*[label(n, font_size=14, color=c).next_to(d, UR, buff=0.05) for n, c, d in zip(names, colors, dots)])
    return A, dots, labs


class Context(VoiceoverScene):
    def construct(self):
        self.card()
        self.redbus()
        self.decoy()

    def card(self):
        card = chapter_card(5, r"Where the axiom fails", r"Can an option nobody picks change what they pick?",
                            lit={1972: r"Tversky", 1982: r"Huber et al.", 1989: r"Simonson"}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter five. Where the axiom fails."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def redbus(self):
        d = load("redbus")
        head = heading(r"The red bus and the blue bus")
        A = axes([0.3, 3.7], [0, 0.6], x_length=4.8, y_length=3.0, xticks=None, yticks=[0, 0.25, 0.5],
                 yfmt=lambda v: f"{v:g}", ylabel=r"share", center=[-3.4, 0.3, 0], font_size=13)
        xs = np.array([1, 2, 3])
        b1 = bars(A.ax, xs - 0.17, d["logit3"], [AUTH] * 3, width=0.3)
        b2 = bars(A.ax, xs + 0.17, d["truth3"], [GOOD] * 3, width=0.3)
        names = VGroup(*[label(t, font_size=14, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, t in enumerate((r"car", r"red bus", r"blue bus"))])
        key = VGroup(label(r"logit", font_size=13, color=AUTH), label(r"two identical buses", font_size=13,
                                                                      color=GOOD)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.05)
        rows = rows_of([
            (r"a commuter is indifferent between a car and a red bus: \ half and half", WHITE),
            (r"add a blue bus, \ identical except in colour; \ the axiom keeps car to red bus at 1:1, \ so each gets "
             r"a third", AUTH),
            (r"but the blue bus only splits the bus riders: \ the car keeps half, \ each bus a quarter", GOOD),
            (r"the axiom fails when options are similar: \ their random parts are correlated, \ not independent; \ "
             r"nested and mixed logits allow it", MODEL),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{scaling.normal\_choice\_shares}, \ correlated noise")
        with self.voiceover(
            "The axiom's most famous failure. <bookmark mark='a'/> A commuter is indifferent between a car and a red "
            "bus: half and half. <bookmark mark='b'/> Add a blue bus, identical except in colour. The axiom keeps the "
            "odds of car to red bus at one to one, so each option gets a third. <bookmark mark='c'/> But the blue "
            "bus only splits the bus riders. The car keeps half, and each bus gets a quarter. "
            "<bookmark mark='d'/> The axiom fails when options are similar, because their random parts are "
            "correlated, not independent. Nested and mixed logit models allow for it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b1))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b2))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def decoy(self):
        head = heading(r"Decoys and compromises")
        A1, d1, l1 = option_plot([-4.6, 0.4, 0], [[6, 4], [4, 6], [5.5, 3.5]], [PERSON, SYMP, GREY_B],
                                 [r"A", r"B", r"decoy"], 3.6, 2.8)
        A2, d2, l2 = option_plot([-0.6, 0.4, 0], [[6, 4], [4, 6], [8, 2]], [PERSON, SYMP, GREY_B],
                                 [r"A", r"B", r"extreme"], 3.6, 2.8)
        t1 = label(r"attraction", font_size=17, color=PERSON).next_to(A1, UP, buff=0.1)
        t2 = label(r"compromise", font_size=17, color=PERSON).next_to(A2, UP, buff=0.1)
        rows = rows_of([
            (r"Huber, \ Payne and Puto, \ 1982: \ a decoy slightly worse than A on both attributes raises A's share; "
             r"\ no one picks the decoy, \ yet it matters", PERSON),
            (r"Simonson, \ 1989: \ add an extreme option and A, \ now in the middle, \ gains: \ the compromise effect",
             MODEL),
            (r"Tversky, \ 1972: \ a new option takes most from the options it resembles: \ the similarity effect", SYMP),
            (r"each breaks Luce's axiom: \ the menu changes the odds between the same two options", AUTH),
        ], 12.4, 19, 0.3).move_to([0, -2.3, 0])
        rows.shift(RIGHT * 0)
        side = wrapped_label(r"two attributes, \ more is better; \ A and B trade one off against the other", 3.4, 16,
                             GREY_A).move_to([4.9, 0.6, 0])
        tag = published_tag(r"Huber, Payne \& Puto (1982); \ Simonson (1989); \ Tversky (1972)")
        with self.voiceover(
            "Menus also bend preferences in ways that similarity can't explain. Take two options, A and B, each better "
            "on one attribute. <bookmark mark='a'/> In 1982 Joel Huber, John Payne and Christopher Puto added a decoy "
            "slightly worse than A on both attributes. A's share went up. No one picks the decoy, yet it matters. "
            "<bookmark mark='b'/> In 1989 Itamar Simonson added an extreme option instead, and A, now in the middle, "
            "gained. It's the compromise effect. <bookmark mark='c'/> And Amos Tversky had shown in 1972 that a new "
            "option takes most from the options it resembles. <bookmark mark='d'/> Each one breaks Luce's axiom: the "
            "menu changes the odds between the same two options."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(side), FadeIn(A1), FadeIn(A2), FadeIn(t1), FadeIn(t2),
                      FadeIn(d1[:2]), FadeIn(l1[:2]), FadeIn(d2[:2]), FadeIn(l2[:2]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(d1[2]), FadeIn(l1[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(d2[2]), FadeIn(l2[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
