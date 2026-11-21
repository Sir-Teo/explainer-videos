from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


class Reputation(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Reputation", r"Why fight a battle you would rather avoid?",
             "Chapter eleven. Reputation.", lit={1978: r"Selten", 1982: r"Kreps and Wilson; Milgrom and Roberts"},
             scale=("firm", "market"), horizon=("a decade",))
        self.paradox()
        self.resolution()

    def paradox(self):
        C = load("chain")
        rows = VGroup(
            label(rf"a chain store in {len(C['rows'])} towns; \ in each, \ one by one, \ an entrant decides whether "
                  r"to enter", font_size=22, color=WHITE),
            label(r"fighting an entrant costs the store; \ accommodating is better, \ once the entrant is in",
                  font_size=22, color=WEAK),
            label(r"in the last town, \ the store accommodates; \ so in the one before, \ and so on back",
                  font_size=22, color=GREY_A),
            label(r"backward induction: \ every entrant enters, \ and is accommodated", font_size=22, color=ERR),
            label(r"Selten: \ no real chain store would play this way", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(UP * 0.2)
        tag = published_tag(r"Selten, \ Theory and Decision 9 (1978)", corner=DR, font_size=12)
        hc = history_card(1978, r"Reinhard Selten", r"``The chain store paradox'': \ what backward induction "
                          r"says, \ and what nobody believes", color=SENDER, width=10.0,
                          font_size=24).move_to(UP * 0.4)
        with self.voiceover(
            "Reputation is information about what someone will do. Reinhard Selten found a paradox in 1978. "
            f"<bookmark mark='a'/> A chain store has branches in {len(C['rows'])} towns. One by one, a local "
            "rival decides whether to enter. <bookmark mark='b'/> If one does, the store can fight a price war, "
            "which costs it, or accommodate, which costs less. <bookmark mark='c'/> In the last town there is no "
            "future to protect, so the store accommodates. Then, in the town before, fighting cannot deter the "
            "last entrant, so the store accommodates there too, and so on, all the way back. <bookmark mark='d'/> "
            "Every rival enters, and none is fought. <bookmark mark='e'/> Selten thought no real chain store would "
            "behave this way: surely it would fight the early entrants to deter the later ones."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                if mk == "a":
                    self.play(FadeOut(hc))
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def resolution(self):
        C = load("chain")
        rows = C["rows"]
        n = len(rows)
        ks = [n - r["k"] + 1 for r in rows]
        ax = plane([0.5, n + 0.5], [0, 1.05], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.6, y_length=4.4,
                   xticks=[1, 5, 10, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"town, \ in the order the entrants come", ylabel=r"probability",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        rep = path(ax, ks, [r["reputation"] for r in rows], BELIEF, 3.0, smooth=False)
        thr = path(ax, ks, [r["threshold"] for r in rows], GREY_B, 2.0, smooth=False)
        enter = VGroup(*[dot(ax, x, r["enter"], ERR, 0.07) for x, r in zip(ks, rows)])
        side = VGroup(
            label(rf"a {100 * C['delta']:.0f}\% chance the store is \\ the kind that always fights", font_size=19,
                  color=WHITE),
            label(r"purple: \ the store's reputation", font_size=19, color=BELIEF),
            label(r"grey: \ the reputation that \\ deters entry", font_size=19, color=GREY_B),
            label(r"red: \ the chance of entry", font_size=19, color=ERR),
            label(rf"entry only in the last {C['k_star']} towns; \\ before that, \ an ordinary store \\ fights to look "
                  r"tough", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Kreps and Wilson; \ Milgrom and Roberts, \ JET 27(2) (1982)", corner=DR, font_size=12)
        with self.voiceover(
            "David Kreps and Robert Wilson, and Paul Milgrom and John Roberts, resolved it with a little doubt. "
            f"<bookmark mark='a'/> Suppose there is a {100 * C['delta']:.0f} percent chance that the store is a "
            "kind that always fights, perhaps because its managers enjoy it. <bookmark mark='b'/> Then fighting "
            "is how an ordinary store keeps entrants guessing: its reputation is the entrants' belief that it is "
            "the tough kind. <bookmark mark='c'/> Early on, with many towns to come, even a small reputation is "
            "enough to deter entry: the grey line, the reputation needed, is tiny. <bookmark mark='d'/> Only near "
            f"the end, in the last {C['k_star']} towns, do entrants come in; and an ordinary store still fights "
            "with some probability to keep its reputation alive. <bookmark mark='e'/> A small doubt about one's "
            "type, and a long horizon, are enough to make a threat credible. The same logic explains why "
            "central banks guard their reputations for fighting inflation."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(rep), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(thr), FadeIn(side[2]), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(enter), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
