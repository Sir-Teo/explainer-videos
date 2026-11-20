from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Game(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Time inconsistency: \ inflation as a game", r"Why would a central bank that dislikes "
             r"inflation end up with too much?", "Chapter nine. Time inconsistency: inflation as a game.",
             lit={1977: r"Kydland and Prescott", 1983: r"Barro and Gordon"}, scale=("nation",), horizon=("a year",))
        self.setup_()
        self.bias()
        self.rules()

    def setup_(self):
        B = load("bg")
        rows = VGroup(
            label(r"Kydland and Prescott, \ 1977; \ Barro and Gordon, \ 1983", font_size=26, color=E.ACCENT),
            label(r"the central bank dislikes inflation, \ and wants output a little above its natural level",
                  font_size=23, color=CB),
            MathTex(r"L = \tfrac12\,\pi^2 + \tfrac{\lambda}{2}\,(y - y^* - k)^2, \qquad y - y^* = b\,(\pi - \pi^e)",
                    font_size=38, color=WHITE),
            label(rf"on the Island: \ $\lambda = {B['lam']:.0f}$, \ $k = {B['k']:.0f}$, \ $b = {B['b']:.0f}$",
                  font_size=22, color=GREY_A),
            label(r"the public sets $\pi^e$ first; \ then the bank chooses $\pi$", font_size=23, color=EXPECT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Kydland and Prescott, \ JPE 85(3) (1977): \ 473--491; \ Barro and Gordon, \ JPE 91(4) "
                            r"(1983): \ 589--610", corner=DR, font_size=12)
        with self.voiceover(
            "Why did central banks let it happen? Finn Kydland and Edward Prescott in 1977, and Robert Barro and "
            "David Gordon in 1983, turned the question into a game. <bookmark mark='a'/> The central bank dislikes "
            "inflation, but it would also like output a little above its natural level, perhaps because taxes and "
            "monopolies keep the natural level too low. <bookmark mark='b'/> Its loss is half the square of "
            "inflation plus lambda times half the square of the gap between output and that target. Output rises "
            "above its natural level only when inflation surprises. <bookmark mark='c'/> On the Island, the bank "
            "wants output two above natural, and cares about output as much as inflation. "
            "<bookmark mark='d'/> The timing matters. The public forms its expectations, in wage contracts, first. "
            "Then the bank chooses inflation."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def bias(self):
        B = load("bg")
        g = B["game"]
        cards = point_cards([
            (r"promise zero", rf"if believed, \ $\pi^e = 0$: \\ loss {g['loss_rule']:.1f}", OUTPUT),
            (r"then cheat", rf"inflate {g['pi_cheat']:.0f}\%, \ output up: \\ loss {g['loss_cheat']:.1f}", INFL),
            (r"but the public knows", r"it will not believe \\ the promise", EXPECT),
            (r"the equilibrium", rf"$\pi = \lambda b k = {g['pi_discretion']:.0f}\%$, \ output at $y^*$: \\ loss "
                                  rf"{g['loss_discretion']:.1f}", HOLD),
        ], width=12.6, cols=2, font_size=22).move_to(DOWN * 0.1)
        head = label(r"discretion: \ the inflation bias", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Play it forward. <bookmark mark='a'/> Suppose the bank promises zero inflation, and is believed. Then "
            f"output sits at its natural level, and the loss is {g['loss_rule']:.0f}. <bookmark mark='b'/> But once "
            f"wages are set, the bank is tempted: inflate by {g['pi_cheat']:.0f} percent, surprise everyone, push "
            f"output up, and the loss falls to {g['loss_cheat']:.0f}. <bookmark mark='c'/> The public can work this "
            "out too, so it never believes the promise. <bookmark mark='d'/> In equilibrium, expected inflation is "
            "exactly high enough that the bank has no reason to surprise anyone: lambda times b times k, "
            f"{g['pi_discretion']:.0f} percent. Output is at its natural level anyway, and the loss is "
            f"{g['loss_discretion']:.0f}, double the rule's. All of the inflation, none of the gain. Nobody did "
            "anything irrational; the problem is that the bank cannot commit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def rules(self):
        rows = VGroup(
            label(r"rules versus discretion", font_size=28, color=E.ACCENT),
            label(r"a rule the bank cannot break \ (like zero inflation) \ beats freedom to choose each year",
                  font_size=23, color=OUTPUT),
            label(r"time inconsistency: \ the best plan today is not the best choice tomorrow", font_size=23,
                  color=EXPECT),
            label(r"also: \ patents, \ tax amnesties, \ bailouts, \ hostage negotiations", font_size=22,
                  color=GREY_A),
            label(r"the cure must make the promise credible: \ chapter 11", font_size=23, color=CB),
            label(r"Kydland and Prescott: \ the Nobel prize, \ 2004", font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "The lesson is about rules versus discretion. <bookmark mark='a'/> A rule the bank cannot break beats "
            "freedom to choose afresh each year, even for a bank with good intentions. <bookmark mark='b'/> Kydland "
            "and Prescott called the problem time inconsistency: the best plan made today is not the best choice "
            "when tomorrow comes. <bookmark mark='c'/> It is everywhere: a government that promises never to bail "
            "out banks, never to grant another tax amnesty, never to pay a ransom. <bookmark mark='d'/> The cure "
            "has to make the promise believable, and chapter eleven shows how central banks tried. "
            "<bookmark mark='e'/> Kydland and Prescott shared the Nobel prize in 2004."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
