from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403

GROUPS = (r"the poor", r"the middle", r"the rich")


class Capture(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Lobbying and capture", r"What does money in politics buy?",
             "Chapter five. Lobbying and capture.",
             lit={1971: r"Stigler", 1994: r"Grossman and Helpman", 2001: r"Fisman"}, scale=("industry", "nation"),
             horizon=("a year",))
        self.stigler()
        self.organized()
        self.weights()
        self.connections()

    def stigler(self):
        chain = flow_chain([(r"an industry \\ is regulated", LOBBY), (r"it knows the most, \\ cares the most", FEW),
                            (r"the regulator \\ needs its experts", LOBBY),
                            (r"rules that \\ protect the industry", LOSS)],
                           notes=[r"to protect \\ the public", r"Olson's \\ small group", r"and its \\ future jobs",
                                  r"entry barred, \\ prices kept up"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.7)
        foot = label(r"George Stigler, \ 1971: \ ``as a rule, \ regulation is acquired by the industry and is designed "
                     r"and operated primarily for its benefit''", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.CAPTURE_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Olson's logic has a sharp consequence for regulation. <bookmark mark='a'/> A regulator is set up to "
            "protect the public from an industry. <bookmark mark='b'/> But the industry knows far more about its "
            "business than anyone else, and cares far more about the rules. <bookmark mark='c'/> The regulator "
            "needs its expertise, and its staff may one day want its jobs. <bookmark mark='d'/> So rules drift "
            "toward the industry's interest: licences that keep out entrants, prices held up. In 1971 George "
            "Stigler put it bluntly: as a rule, regulation is acquired by the industry, and designed and operated "
            "primarily for its benefit. He called it capture."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(foot), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
        self.clear_scene()

    def organized(self):
        V = load("voting")
        ax = plane([0, 3], [-1.0, 0.7], center=LEFT * 2.0 + DOWN * 0.35, x_length=6.6, y_length=4.6, xticks=[],
                   yticks=[-0.8, -0.4, 0, 0.4], ylabel=r"net transfer, \ share of average income",
                   yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}") if v else "0", font_size=14)
        zero = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(3, 0), color=GREY_B, stroke_width=1.4)
        old, new = VGroup(), VGroup()
        for i, nm in enumerate(GROUPS):
            for grp, t, col, dx in ((old, V["plain"]["transfer"][i], GREY_B, -0.17),
                                    (new, V["lobby"]["transfer"][i], LOBBY if i == 2 else VOTER, 0.17)):
                p0, p1 = ax.ax.c2p(0.5 + i + dx - 0.15, 0), ax.ax.c2p(0.5 + i + dx + 0.15, t)
                r = Rectangle(width=p1[0] - p0[0], height=max(abs(p1[1] - p0[1]), 0.02), stroke_width=0,
                              fill_color=col, fill_opacity=0.85).move_to((p0 + p1) / 2)
                grp.add(VGroup(r, label(rf"{t:+.2f}".replace("-", "{-}"), font_size=14, color=WHITE).next_to(
                    r, UP if t >= 0 else DOWN, buff=0.05)))
        names = VGroup(*[label(nm, font_size=15, color=WHITE).next_to(ax.ax.c2p(0.5 + i, -1.0), DOWN, buff=0.1)
                         for i, nm in enumerate(GROUPS)])
        side = VGroup(
            label(r"grey: \ chapter four's \\ voters alone", font_size=18, color=GREY_B),
            label(r"the rich organize: \\ their contributions \\ buy campaign ads, \\ and ads buy votes", font_size=18,
                  color=LOBBY),
            label(r"the rich pay far less; \\ the others get less", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Add money to chapter four's model. <bookmark mark='a'/> In grey, the transfers when only voters count. "
            "<bookmark mark='b'/> Now let the rich organize, as a lobby: they give money to whichever party "
            "promises them more, and the money buys advertising that wins votes elsewhere. In the parties' "
            "arithmetic, the organized group now counts as if it had many more swing voters. <bookmark mark='c'/> "
            f"The rich, who paid {100 * -V['plain']['transfer'][2]:.0f} percent of average income, now pay "
            f"{100 * -V['lobby']['transfer'][2]:.0f} percent, and the middle's gain shrinks from "
            f"{100 * V['plain']['transfer'][1]:.0f} to {100 * V['lobby']['transfer'][1]:.0f} percent. Nothing "
            "about the groups' needs changed, only who was organized."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), FadeIn(names), run_time=1.0)
            vo.wait_until("a")
            self.play(*[GrowFromEdge(b[0], DOWN if V["plain"]["transfer"][i] >= 0 else UP) for i, b in enumerate(old)],
                      *[FadeIn(b[1]) for b in old], FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            self.play(*[GrowFromEdge(b[0], DOWN if V["lobby"]["transfer"][i] >= 0 else UP) for i, b in enumerate(new)],
                      *[FadeIn(b[1]) for b in new], run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(new[2], color=WHITE))
        self.clear_scene()

    def weights(self):
        T = tables.CAPTURE_47.data
        eq = MathTex(r"G = \text{contributions} + a \times \text{welfare}", font_size=40, color=THEORY).move_to(
            UP * 2.9)
        rows = VGroup(
            label(r"Grossman and Helpman, \ 1994: \ a government sells protection \\ to organized industries, \ "
                  r"weighing their money against everyone's welfare", font_size=22, color=WHITE),
            label(r"protection is higher where the industry is organized, \ produces much \\ and imports little, \ "
                  r"and where imports respond little to the price", font_size=22, color=LOBBY),
            label(rf"Goldberg and Maggi, \ 1999: \ the weight on welfare, \ $a$, \ {T['gm_lo']} to {T['gm_hi']} "
                  r"times \\ the weight on money: \ the government is mostly benevolent, \\ and still sells "
                  r"protection at the margin", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(eq, DOWN, buff=0.55)
        gh = MathTex(r"\frac{t_i}{1+t_i} = \frac{I_i - \alpha_L}{a + \alpha_L}\cdot\frac{z_i}{e_i}",
                     font_size=34, color=THEORY).next_to(rows, DOWN, buff=0.4)
        gh_note = label(r"$I_i$: \ organized or not; \ $z_i$: \ output over imports; \ $e_i$: \ how much imports "
                        r"respond; \ $\alpha_L$: \ the share of people organized", font_size=16,
                        color=GREY_A).next_to(gh, DOWN, buff=0.2)
        tag = published_tag(tables.CAPTURE_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Part thirty-five met this in trade policy. <bookmark mark='a'/> In Gene Grossman and Elhanan "
            "Helpman's model, a government weighs the contributions of organized industries against the welfare of "
            "everyone. <bookmark mark='b'/> It predicts more protection for industries that are organized, produce "
            "much and import little, and whose imports barely respond to price, where protection costs the "
            "least welfare. <bookmark mark='c'/> When Pinelopi Goldberg and Giovanni Maggi fitted it to American "
            f"tariffs and quotas, the weight on welfare came out {T['gm_lo']} to {T['gm_hi']} times the weight on "
            "money. The government was mostly benevolent. It sold protection anyway, because at the margin a "
            "little protection costs everyone a little and pays a few a lot: Olson's arithmetic again."
        ) as vo:
            self.play(FadeIn(tag), Write(eq), run_time=1.5)
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
                if mk == "b":
                    self.play(Write(gh), FadeIn(gh_note), run_time=2.0)
            self.play(Circumscribe(gh, color=E.ACCENT, buff=0.1))
        self.clear_scene()

    def connections(self):
        chain = flow_chain([(r"Indonesia, \\ 1995--97", ELITE), (r"rumours: \\ Suharto is ill", LOSS),
                            (r"connected firms' \\ shares fall more", LOBBY), (r"a large part of their \\ value was "
                                                                               r"the connection", E.ACCENT)],
                           notes=[r"firms ranked by \\ ties to the \\ president's family", r"a natural \\ experiment",
                                  r"than unconnected \\ firms' shares", r"Fisman, \\ 2001"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.5)
        tag = published_tag(tables.CAPTURE_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "How much is a political connection worth? Raymond Fisman found a way to price it. <bookmark "
            "mark='a'/> In the last years of President Suharto's rule in Indonesia, consultants ranked firms by "
            "how closely they were tied to the president and his family. <bookmark mark='b'/> Several times, "
            "rumours spread that Suharto was gravely ill. <bookmark mark='c'/> Each time, the shares of the most "
            "connected firms fell further than the shares of the rest. <bookmark mark='d'/> Investors were telling "
            "him how much of each firm's value depended on the president staying alive: for the best-connected, "
            "a large share. The stock market, it turns out, is a corruption meter."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
        self.clear_scene()
