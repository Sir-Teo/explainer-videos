from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ one island, \ five rules, \ five winners", r"38 islanders rank five plans for the "
             r"harvest feast. \ Which plan should win?", "Chapter one. Play it: one island, five rules, five winners.",
             lit={1770: r"Borda", 1785: r"Condorcet", 1871: r"Ware's instant runoff"}, scale=("community",),
             horizon=("a day",))
        self.ballots()
        self.rules()

    def ballot_row(self, p):
        bs = VGroup(*[ballot(r, n, w=1.3, font_size=24) for n, r in p["profile"]]).arrange(RIGHT, buff=0.7)
        return bs

    def ballots(self):
        p = load("playit")
        stage = game_stage(12.4, 6.0, center=DOWN * 0.15)
        bs = self.ballot_row(p).move_to(stage.box.get_center() + LEFT * 2.6 + DOWN * 0.15)
        key = VGroup(*[label(rf"{c}: \ {PLAN[c]}", font_size=22, color=VOTE[c]) for c in "ABCDE"]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.14).move_to(stage.box.get_center() + RIGHT * 3.7 + UP * 0.6)
        ask = label(r"which plan should win?", font_size=28, color=E.ACCENT).next_to(key, DOWN, buff=0.45)
        head = label(r"38 islanders, \ four kinds of ballot: \ best at the top, \ the number who cast it above",
                     font_size=22, color=GREY_A).move_to(stage.box.get_top() + DOWN * 0.55)
        ring = countdown().next_to(ask, DOWN, buff=0.3)
        with self.voiceover(
            "Thirty-eight islanders must choose one of five plans for the harvest feast: a feast of fish, a feast of "
            "fruit, a dance, a boat race, or a market fair. <bookmark mark='a'/> Their rankings come in four kinds. "
            "Twelve islanders put the fish first. Eleven put the fruit first. Eight put the dance first, and seven "
            "the boat race. Nobody puts the market fair first, but look where it sits on every ballot. "
            "<bookmark mark='b'/> Which plan should the island choose? Pause, and decide."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(key), FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bs], lag_ratio=0.5), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(ask), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def rules(self):
        p = load("playit")
        bs = self.ballot_row(p).scale(0.72).to_edge(UP, buff=0.3).shift(LEFT * 3.2)
        key = VGroup(*[label(rf"{c}: \ {PLAN[c]}", font_size=17, color=VOTE[c]) for c in "ABCDE"]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).to_corner(UR, buff=0.35)
        w = p["winners"]
        pl, ru, irv, bo = p["plurality"], p["runoff"], p["irv"], p["borda"]
        lines = [
            ("plurality", rf"most first places: \ A {pl['A']}, \ B {pl['B']}, \ C {pl['C']}, \ D {pl['D']}, \ "
                          rf"E {pl['E']}", w["plurality"]),
            ("two-round runoff", rf"the top two meet: \ B beats A, \ {ru['votes'][1]} to {ru['votes'][0]}",
             w["runoff"]),
            ("instant runoff", r"drop the last, \ pass on its ballots: \ E, \ then D, \ then B go; \ C beats A, \ "
                               r"26 to 12", w["instant runoff"]),
            ("Borda count", rf"4 points for a first place, \ 3 for a second, \ ...: \ D {bo['D']}, \ E {bo['E']}, "
                            rf"\ B {bo['B']}", w["Borda"]),
            ("Condorcet", r"beats every other plan head to head", w["Condorcet"]),
        ]
        rows = VGroup()
        for name, how, win in lines:
            rows.add(VGroup(label(name, font_size=23, color=RULE), label(how, font_size=19, color=GREY_A),
                            label(win, font_size=32, color=VOTE[win])))
        y0 = 0.9
        for i, r in enumerate(rows):
            y = y0 - 0.78 * i
            r[0].move_to([-6.6 + r[0].width / 2, y, 0])
            r[1].move_to([-3.2 + r[1].width / 2, y, 0])
            r[2].move_to([6.0, y, 0])
        foot = label(r"five reasonable rules, \ five different winners, \ from the same ballots", font_size=25,
                     color=E.ACCENT).to_edge(DOWN, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Now count the votes five ways. <bookmark mark='a'/> By plurality, the plan with the most first places "
            "wins: the fish, with twelve. <bookmark mark='b'/> In a two-round runoff, the top two meet: the fish "
            "against the fruit, and the fruit wins, twenty-six to twelve, because everyone who did not put "
            "fish first ranks it last. <bookmark mark='c'/> By instant runoff, the plan with the fewest first places "
            "drops out and its ballots pass to their next choice, round after round: the market fair goes, then the "
            "boat race, whose seven ballots lift the dance above the fruit, and the fruit goes; the dance then beats "
            "the fish. <bookmark mark='d'/> By Borda's count, four points for a first place, three for a second, and "
            "so on, the boat race wins with a hundred and one. <bookmark mark='e'/> And the market fair, which nobody "
            "put first, beats every other plan in a head-to-head vote: it is the Condorcet winner. "
            "<bookmark mark='f'/> Five reasonable rules, five different winners, from the very same ballots."
        ) as vo:
            self.play(FadeIn(bs), FadeIn(key), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), FadeIn(r[1]), run_time=0.8)
                self.play(FadeIn(r[2], scale=1.3), run_time=0.6)
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()
