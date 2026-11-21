from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403


def kp_positions():
    """Hub 0 with leaves 1-7 on the left; the clique 8-12 as a pentagon on the right."""
    pos = {0: np.array([-1.6, 0, 0])}
    for k in range(1, 8):
        a = PI / 2 + (k - 1) * (2 * PI - 0.9) / 6 + 0.45
        pos[k] = pos[0] + 1.35 * np.array([np.cos(a), np.sin(a), 0])
    c = np.array([1.9, 0, 0])
    for m, k in enumerate(range(8, 13)):
        a = PI + 2 * PI * m / 5
        pos[k] = c + 1.0 * np.array([np.cos(a), np.sin(a), 0])
    return pos


class KeyPlayer(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Games on networks: \ the key player", r"If effort is contagious, \ whose removal cuts "
             r"the most?", "Chapter eleven. Games on networks: the key player.",
             lit={1993: r"Manski", 2006: r"Ballester et al."}, scale=("person", "city"),
             horizon=("a year",))
        self.game()
        self.remove()
        self.peers()

    def game(self):
        K = load("keyplayer")
        G = np.array(K["G"])
        x = np.array(K["effort"])
        pos = kp_positions()
        shift = LEFT * 2.6 + DOWN * 0.3
        edges = VGroup(*[Line(pos[i] + shift, pos[j] + shift, stroke_width=1.8, color=GREY_C)
                         for i in range(len(G)) for j in range(i + 1, len(G)) if G[i, j]])
        nodes = VGroup(*[Circle(radius=0.12 + 0.045 * x[k], stroke_color=SEED if k in (0, 8) else PEOPLE,
                                stroke_width=2.2, fill_color=SEED if k in (0, 8) else PEOPLE,
                                fill_opacity=0.35).move_to(pos[k] + shift) for k in range(len(G))])
        eq = label(r"$x_i = a + \delta \sum_j g_{ij} x_j \;\Rightarrow\; x = (I - \delta G)^{-1} a$", font_size=26)
        side = VGroup(
            eq,
            label(r"each player's effort rises \\ with the efforts of their links", font_size=19, color=WHITE),
            label(rf"hub: \ {int(K['degree'][0])} links, \ effort {x[0]:.1f}", font_size=19, color=SEED),
            label(rf"clique members: \ 4 or 5 links, \ effort {x[9]:.1f} to {x[8]:.1f}", font_size=19,
                  color=PEOPLE),
            label(r"effort = Bonacich centrality: \\ links, \ and links of links", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Ballester, \ Calvó-Armengol and Zenou, \ Econometrica 74(5) (2006); \ the Island: \ "
                            r"agora.network.key\_player", corner=DL, font_size=12)
        with self.voiceover(
            "Some behaviour is contagious: studying, smoking, crime. Coralio Ballester, Antoni Calvó-Armengol and "
            "Yves Zenou wrote it as a game on a network. <bookmark mark='a'/> Each player chooses an effort, and "
            "the more effort their contacts put in, the more each wants to put in, by a factor delta for each "
            "link. <bookmark mark='b'/> Here are thirteen of the Island's teenagers: on the left, a popular one "
            "with seven friends who do not know each other; on the right, a tight group of five who all know each "
            "other, one of whom also knows the popular one. <bookmark mark='c'/> In equilibrium the hub, with "
            f"eight links, puts in {x[0]:.1f}. <bookmark mark='d'/> The clique members, with four or five links "
            f"each, put in more, {x[9]:.1f} to {x[8]:.1f}, because their friends' friends are also their "
            "friends. <bookmark mark='e'/> Effort equals each player's Bonacich centrality: it counts links, and "
            "links of links, and so on, each further step discounted."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(edges), FadeIn(nodes), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(nodes[0], color=SEED))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), *[Indicate(nodes[k], color=PEOPLE) for k in range(8, 13)])
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def remove(self):
        K = load("keyplayer")
        drop = np.array(K["drop"])
        who = ((0, r"the hub", SEED), (1, r"a follower", GREY_B), (8, r"the bridge \\ in the clique", SHOCK),
               (9, r"another \\ clique member", PEOPLE))
        vals = [100 * drop[k] / K["total"] for k, _, _ in who]
        ax = plane([-0.6, 3.6], [0, 55], center=LEFT * 2.6 + DOWN * 0.3, x_length=6.4, y_length=4.6, xticks=[],
                   yticks=[0, 10, 20, 30, 40, 50], ylabel=r"total effort lost if removed, \ \%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        b = bars(ax, range(4), vals, [c for _, _, c in who], width=0.55)
        labs = VGroup(*[label(n, font_size=14, color=c).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.12)
                        for k, (_, n, c) in enumerate(who)])
        vl = VGroup(*[label(f"{v:.0f}", font_size=15, color=c).next_to(x, UP, buff=0.06)
                      for v, (_, _, c), x in zip(vals, who, b)])
        side = VGroup(
            label(r"the key player: \ not the one with most links", font_size=20, color=SHOCK),
            label(r"remove the bridge: \ the clique loses its \\ most connected member, \ and the hub its link",
                  font_size=19, color=WHITE),
            label(r"policing, \ public health, \ marketing: \\ target the key player, \ not the most popular",
                  font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"the Island: \ $\delta$ = 0.2; \ agora.network.key\_player", corner=DL, font_size=12)
        with self.voiceover(
            "Now a policy question. You can remove one player, by persuading them, treating them, or arresting "
            "them. Whose removal cuts the group's total effort the most? <bookmark mark='a'/> Removing the hub, "
            f"the one with most friends, cuts it by {vals[0]:.0f} percent. <bookmark mark='b'/> A follower, by "
            f"{vals[1]:.0f}. <bookmark mark='c'/> But the clique member who also knows the hub cuts it by "
            f"{vals[2]:.0f} percent: <bookmark mark='d'/> more than another clique member, {vals[3]:.0f}, and far "
            "more than the hub. <bookmark mark='e'/> The key player is the one whose removal changes the network "
            "most, and that is not simply the one with most links. Ballester, Calvó-Armengol and Zenou derived a "
            "centrality that finds them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[k], DOWN), FadeIn(vl[k]))
                if k == 2:
                    self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def peers(self):
        head = label(r"but are peers really contagious?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.4)
        cards = point_cards([
            (r"the reflection problem", r"friends behave alike because they influence each other, \ because they "
             r"chose each other, \ or because they share a school: \ the averages alone cannot tell (Manski, \ 1993)",
             SHOCK),
            (r"a network helps", r"a friend's friend who is not your friend moves your friend but not you directly: \ "
             r"an instrument built from the network itself (Bramoullé, \ Djebbari and Fortin, \ 2009)", LINK),
            (r"or randomize", r"assign roommates or classmates at random, \ and the sorting goes away", GAIN),
            (r"the lesson", r"the key-player policy is only as good as the evidence that effort is contagious", GDP),
        ], cols=2, width=12.8, font_size=19).next_to(head, DOWN, buff=0.45)
        tag = published_tag(r"Manski, \ Review of Economic Studies 60(3) (1993); \ Bramoullé, \ Djebbari and Fortin, "
                            r"\ Journal of Econometrics 150(1) (2009)", corner=DL, font_size=12)
        with self.voiceover(
            "All of this assumes that effort really is contagious. <bookmark mark='a'/> Charles Manski called the "
            "difficulty the reflection problem: friends may behave alike because they influence each other, "
            "because they chose each other for being alike, or because they share a school and a teacher. From "
            "group averages alone, the three cannot be told apart. <bookmark mark='b'/> A network helps. A friend "
            "of your friend who is not your friend moves your friend but not you, except through your friend: "
            "Yann Bramoullé, Habiba Djebbari and Bernard Fortin turned that into an instrument. <bookmark "
            "mark='c'/> Or assign roommates or classmates at random, and the sorting goes away. <bookmark "
            "mark='d'/> The key-player policy is only as good as the evidence that the effort is contagious."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
