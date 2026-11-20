from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403


class DD(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Diamond and Dybvig", r"Why does a bank make everyone better off, \ and how?",
             "Chapter three. Diamond and Dybvig.", lit={1983: r"Diamond and Dybvig", 2022: r"the Nobel prize"},
             scale=("firm",), horizon=("a year",))
        self.setup_()
        self.contract()

    def setup_(self):
        d = load("dd")
        rows = VGroup(
            label(r"three dates; \ each depositor has one unit at date 0", font_size=23, color=GREY_A),
            label(rf"a share $t = {d['t']:g}$ turn out impatient: \ they must consume at date 1; \ the rest can wait",
                  font_size=23, color=RUN),
            label(r"nobody knows their own type at date 0, \ and types are private", font_size=22, color=GREY_A),
            label(rf"an investment pays $R = {d['R']:g}$ at date 2, \ or 1 if cut short at date 1", font_size=23,
                  color=LOAN),
            label(r"alone, \ each gets 1 if impatient, \ $R$ if patient: \ a gamble on one's own type",
                  font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Diamond and Dybvig, JPE 91(3) (1983): \ 401--419", corner=DR, font_size=12)
        with self.voiceover(
            "Douglas Diamond and Philip Dybvig wrote the model in 1983; it won them a share of the Nobel prize in "
            "2022. <bookmark mark='a'/> There are three dates, and each person starts with one unit. "
            f"<bookmark mark='b'/> A share of them, here a quarter, will turn out to need their money early, at date "
            "one. The rest can wait. <bookmark mark='c'/> Nobody knows in advance which they will be, and nobody can "
            f"prove their type to anyone else. <bookmark mark='d'/> The only investment pays {d['R']:g} if it is held "
            "to date two, but only one if it is cut short. <bookmark mark='e'/> On their own, people get one if they "
            "turn out impatient, and one and a half if patient. That is a gamble on their own type, and people "
            "who dislike risk would pay to insure it."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def contract(self):
        d = load("dd")
        rows = VGroup(
            MathTex(r"\max_{c_1, c_2}\; t\,u(c_1) + (1-t)\,u(c_2) \quad \text{s.t.} \quad "
                    r"t\,c_1 + (1-t)\,\frac{c_2}{R} "
                    r"= 1", font_size=40, color=WHITE),
            MathTex(r"u'(c_1) = R\,u'(c_2) \;\Rightarrow\; c_2 = R^{1/\gamma} c_1, \qquad c_1 = \frac{1}{t + (1-t)"
                    r"R^{1/\gamma - 1}}", font_size=38, color=DEPOSIT),
            label(rf"with $\gamma = {d['gamma']:g}$: \ $c_1 = {d['c1']:.3f}$, \ $c_2 = {d['c2']:.3f}$ \ against "
                  rf"autarky's 1 and {d['R']:g}", font_size=25, color=E.ACCENT),
            label(r"a demand deposit: \ withdraw $c_1$ whenever you like, \ or wait for $c_2$", font_size=23,
                  color=STAY),
            label(r"the bank insures depositors against their own impatience, \ and it works if only the impatient "
                  r"withdraw", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "A bank can provide that insurance. <bookmark mark='a'/> Choose what to pay at each date to maximize "
            "expected utility, given that whatever is paid early must come from investments cut short. "
            "<bookmark mark='b'/> The first-order condition says the marginal utility of early consumption equals "
            "R times that of late. With constant relative risk aversion, the solution is in closed form. "
            f"<bookmark mark='c'/> With a risk aversion of two, the bank pays {d['c1']:.2f} to anyone who withdraws "
            f"early and {d['c2']:.2f} to anyone who waits: more than one for the impatient, less than one and a half "
            "for the patient. <bookmark mark='d'/> That is a demand deposit. <bookmark mark='e'/> It makes everyone "
            "better off, provided only the impatient withdraw early. And that proviso is the whole problem."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
