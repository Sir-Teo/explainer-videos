from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


class Herds(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Herds and cascades", r"Why do rational people ignore what they know?",
             "Chapter ten. Herds and cascades.", lit={1992: r"Banerjee; Bikhchandani, Hirshleifer, Welch"},
             scale=("person", "market"), horizon=("a day",))
        self.restaurants()
        self.chain()
        self.quality()

    def restaurants(self):
        Cs = load("cascade")
        q = Cs["q"]
        ex = Cs["examples"][:4]
        rows = VGroup()
        for run in ex:
            dots_ = VGroup(*[Dot(radius=0.09, color=(GAIN if a == 1 else LOSS)) for a in run[:24]]).arrange(
                RIGHT, buff=0.12)
            rows.add(dots_)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.8)
        rules = VGroup(
            label(rf"two restaurants; \ one is better; \ each diner gets a private hint, \ right {100 * q:.0f}\% of "
                  r"the time", font_size=21, color=WHITE),
            label(r"diners arrive one by one and see where the earlier ones went", font_size=21, color=RECEIVER),
            label(r"once one restaurant leads by two choices, \ a diner's own hint cannot outweigh the lead",
                  font_size=21, color=ERR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.6)
        key = label(r"each row: \ one queue of diners \ (green: \ the better restaurant)", font_size=18,
                    color=GREY_A).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"Banerjee, \ QJE (1992); \ Bikhchandani, \ Hirshleifer and Welch, \ JPE (1992)",
                            corner=DR, font_size=12)
        hc = history_card(1992, r"Abhijit Banerjee; \ Bikhchandani, \ Hirshleifer and Welch", r"herds and "
                          r"informational cascades: \ rational people who stop using what they know",
                          color=ERR, width=10.0, font_size=24).move_to(DOWN * 0.4)
        with self.voiceover(
            "Now let people learn from each other's actions instead of from a designer. In 1992 Abhijit Banerjee, "
            "and separately Sushil Bikhchandani, David Hirshleifer and Ivo Welch, showed how a crowd can go wrong "
            f"with nobody making a mistake. <bookmark mark='a'/> Two restaurants, one better. Each diner gets a "
            f"private hint that is right {100 * q:.0f} percent of the time. <bookmark mark='b'/> Diners arrive one "
            "by one and see where the earlier ones went. <bookmark mark='c'/> The first follows her hint. So may "
            "the second. But once one restaurant leads by two choices, a diner's single hint cannot outweigh the "
            "lead, so she follows the crowd whatever her hint says, and so does everyone after her. Her choice "
            "reveals nothing, and learning stops. <bookmark mark='d'/> Four queues: most settle on the better "
            "restaurant; some lock onto the worse one within the first few diners, and never leave."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            for mk, r_ in zip("abc", rules):
                vo.wait_until(mk)
                if mk == "a":
                    self.play(FadeOut(hc))
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(LaggedStart(*[LaggedStart(*[FadeIn(d, scale=0.5) for d in r_], lag_ratio=0.08) for r_ in rows],
                                  lag_ratio=0.25), FadeIn(key), run_time=4.0)
        self.clear_scene()

    def chain(self):
        Cs = load("cascade")
        n = Cs["n"]
        x = np.arange(1, n + 1)
        ax = plane([0, n], [0, 1], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"diners so far",
                   ylabel=r"probability", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        r = path(ax, x, Cs["right"], GAIN, 3.0, smooth=False)
        w = path(ax, x, Cs["wrong"], LOSS, 3.0, smooth=False)
        nn = path(ax, x, Cs["none"], GREY_B, 2.4, smooth=False)
        side = VGroup(
            label(r"green: \ a cascade on the better", font_size=19, color=GAIN),
            label(r"red: \ a cascade on the worse", font_size=19, color=LOSS),
            label(r"grey: \ still learning", font_size=19, color=GREY_B),
            label(rf"in the end: \ {100 * Cs['limit_right']:.1f}\% right, \\ {100 * Cs['limit_wrong']:.1f}\% wrong "
                  rf"for ever", font_size=20, color=E.ACCENT),
            label(rf"simulated, \ 20{{,}}000 queues: \\ {100 * Cs['share_right']:.1f}\% right", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "The arithmetic is exact. Count the hints that earlier choices have revealed, for the better restaurant "
            "minus against it; a cascade starts when the count reaches two either way. <bookmark mark='a'/> The "
            "chance of a cascade on the better restaurant rises quickly; <bookmark mark='b'/> the chance of one "
            "on the worse rises too; <bookmark mark='c'/> and the chance of still learning falls to almost "
            f"nothing within a dozen diners. <bookmark mark='d'/> In the end {100 * Cs['limit_right']:.1f} percent "
            f"of queues are right, and {100 * Cs['limit_wrong']:.1f} percent are wrong for ever, although the "
            "hints of the whole queue together would leave no doubt. <bookmark mark='e'/> Twenty thousand simulated "
            "queues agree with the formula."
        ) as vo:
            self.play(FadeIn(ax))
            for mk, c_, s_ in zip("abc", (r, w, nn), side[:3]):
                vo.wait_until(mk)
                self.play(Create(c_), FadeIn(s_), run_time=1.4)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def quality(self):
        Cs = load("cascade")
        qs = np.array(Cs["qs"])
        ax = plane([0.5, 1.0], [0.5, 1.0], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0], yticks=[0.5, 0.75, 1.0],
                   xlabel=r"how often each hint is right", ylabel=r"how often the queue ends right",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        cascade = path(ax, qs, Cs["right_by_q"], SENDER, 3.0)
        diag = seg(ax, 0.5, 0.5, 1.0, 1.0, GREY_B, 1.4, dashed=True)
        side = VGroup(
            label(r"gold: \ the queue, \ in the end", font_size=19, color=SENDER),
            label(r"dashed: \ one diner alone", font_size=19, color=GREY_B),
            label(r"pooling every hint would \\ be right almost surely", font_size=19, color=GAIN),
            label(r"the herd does a little better \\ than one person, \ and far \\ worse than the crowd's "
                  r"knowledge", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "How bad is it? <bookmark mark='a'/> The gold line is how often a long queue ends up right, against how "
            "good each hint is. <bookmark mark='b'/> The dashed line is a single diner on her own hint. <bookmark "
            "mark='c'/> Pooling everyone's hints would make the queue right almost surely. <bookmark mark='d'/> The "
            "herd does a little better than a lone diner and much worse than what the crowd collectively knows. "
            "The information is lost because actions are coarser than beliefs: once the herd forms, nobody's choice "
            "says what they saw. Reviews, ratings and fashions are attempts to keep that information flowing."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(cascade), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(diag), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
