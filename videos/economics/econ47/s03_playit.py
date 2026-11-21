from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ build or lobby?", r"What do you do with your hundred tokens?",
             "Chapter two. Play it: build or lobby?", lit={1967: r"Tullock"}, scale=("group",), horizon=("a day",))
        self.rules()
        self.ask()
        self.reveal()

    def rules(self):
        T = load("tokens")
        rows = VGroup(
            label(rf"{T['N']} players, \ {T['endowment']:.0f} tokens each", font_size=26, color=WHITE),
            label(r"keep a token: \ it is worth 1 to you", font_size=24, color=GREY_A),
            label(rf"build with it: \ it returns {T['mpcr']:.1f} to every player, \ you included", font_size=24,
                  color=GAIN),
            label(rf"lobby with it: \ a prize of {T['prize']:.0f} tokens is shared in proportion to lobbying",
                  font_size=24, color=LOBBY),
            label(r"if nobody lobbies, \ the prize is shared equally", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to(UP * 0.75)
        head = label(r"Your turn: \ a hundred tokens", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        people = VGroup(*[Circle(radius=0.27, stroke_color=WHITE if i == 0 else GREY_B, stroke_width=2.2,
                                 fill_color=E.ACCENT if i == 0 else GREY_D, fill_opacity=0.35)
                          for i in range(T["N"])]).arrange(RIGHT, buff=0.38).move_to(DOWN * 2.35)
        you = label(r"you", font_size=16, color=WHITE).next_to(people[0], DOWN, buff=0.12)
        token = Dot(people[0].get_center(), radius=0.1, color=GAIN)
        gains = VGroup(*[label(rf"+{T['mpcr']:.1f}", font_size=15, color=GAIN).next_to(c, UP, buff=0.1)
                         for c in people])
        prize = VGroup(RoundedRectangle(width=1.5, height=0.7, corner_radius=0.1, stroke_color=LOBBY,
                                        fill_color=LOBBY, fill_opacity=0.25),
                       label(rf"prize {T['prize']:.0f}", font_size=17, color=LOBBY))
        prize[1].move_to(prize[0])
        prize.next_to(people, RIGHT, buff=0.45)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Your turn. You are one of {T['N']} players, each with {T['endowment']:.0f} tokens. <bookmark mark='a'/> "
            "A token you keep is worth one to you. <bookmark mark='b'/> A token you put into building, a road, a "
            f"school, returns {T['mpcr']:.1f} to every one of the {T['N']} players, so it is worth three to the "
            "group, but only 0.3 to you. <bookmark mark='c'/> A token you spend on lobbying buys you a share of a "
            f"prize of {T['prize']:.0f} tokens: the government's favours, divided in proportion to how much each "
            "player lobbied. <bookmark mark='d'/> If nobody lobbies, the prize is shared equally."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0], shift=RIGHT * 0.1),
                      LaggedStart(*[FadeIn(c) for c in people], lag_ratio=0.1), FadeIn(you), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.1), FadeIn(token))
            self.play(token.animate.move_to(people.get_center() + UP * 0.9), run_time=1.0)
            self.play(FadeOut(token), LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in gains], lag_ratio=0.08),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.1), FadeOut(gains), FadeIn(prize))
            self.play(*[Indicate(c, color=LOBBY) for c in people], run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(rows[4], shift=RIGHT * 0.1))
        self.clear_scene()

    def ask(self):
        head = label(r"How many tokens do you keep, \ build with, \ and lobby with?", font_size=30,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=1.4, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=2.4, fill_color=c, fill_opacity=0.12),
                                label(t, font_size=26, color=c))
                         for t, c in ((r"keep \ \_\_\_", GREY_A), (r"build \ \_\_\_", GAIN),
                                      (r"lobby \ \_\_\_", LOBBY))])
        for b in boxes:
            b[1].move_to(b[0])
        boxes.arrange(RIGHT, buff=0.6).move_to(UP * 0.3)
        ring = countdown().scale(0.6).next_to(boxes, DOWN, buff=0.7)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Pause, and split your hundred tokens: how many do you keep, how many do you build with, and how many "
            "do you spend on lobbying?"
        ):
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3),
                      FadeIn(ring), run_time=2.0)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.clear_scene()

    def reveal(self):
        T = load("tokens")
        rows = [(r"everyone builds", T["best_payoff"], GAIN), (r"half build, \ half lobby: \ the builders",
                                                              T["mixed_builders"], GREY_B),
                (r"half build, \ half lobby: \ the lobbyists", T["mixed_lobbyists"], LOBBY),
                (r"everyone lobbies, \ nobody builds", T["nash_payoff"], LOSS)]
        bars = VGroup()
        for i, (nm, v, col) in enumerate(rows):
            y = 1.9 - 0.95 * i
            w = v / 360 * 7.2
            r = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-2.4 + w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=19, color=col).next_to(np.array([-2.6, y, 0]), LEFT, buff=0.1), r,
                            label(rf"{v:.0f}", font_size=21, color=WHITE).next_to(r, RIGHT, buff=0.15)))
        head = label(r"tokens each player ends with", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(rf"in equilibrium each lobbies {T['nash_lobby']:.0f}: \ {T['nash_total_lobbying']:.0f} of the "
                     rf"{T['prize']:.0f}-token prize is spent chasing it", font_size=21, color=GREY_A).to_edge(
            DOWN, buff=0.6)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Here is what happens. <bookmark mark='a'/> If everyone builds, everyone ends with {T['best_payoff']:.0f} "
            "tokens: the building triples, and the prize is shared equally. <bookmark mark='b'/> But look at a "
            f"society where half build and half lobby. The builders end with {T['mixed_builders']:.0f}; <bookmark "
            f"mark='c'/> the lobbyists, who keep their tokens and take the whole prize, with "
            f"{T['mixed_lobbyists']:.0f}. Each player does better by lobbying than by building, whatever the others "
            "do, so building collapses. <bookmark mark='d'/> In equilibrium nobody builds, everyone lobbies "
            f"{T['nash_lobby']:.0f} tokens, and each ends with {T['nash_payoff']:.0f}: barely more than they started "
            f"with. <bookmark mark='e'/> {T['nash_total_lobbying']:.0f} tokens are spent to win a prize of "
            f"{T['prize']:.0f}. That is rent seeking, and the next chapter takes it apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(b[0]) for b in bars])
            for mk, b in zip("abcd", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
