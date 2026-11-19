from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403


class Piece(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Piece rates: \ Safelite", r"When a firm starts paying for each windscreen, \ how much more do "
             r"its workers fit, \ and why?", "Chapter six. Piece rates: Safelite.",
             lit={1994: r"Safelite's switch", 2000: r"Lazear", 2004: r"Shearer", 2005: r"Bandiera et al."},
             scale=("person", "firm"), horizon=("a year",))
        self.switch()
        self.sorting()
        self.split()
        self.others()

    def switch(self):
        lz = tables.LAZEAR_2000.data
        hc = history_card(1994, r"Safelite Glass, \ Columbus, Ohio", r"the largest installer of car windscreens in the "
                          r"United States", color=PAY, width=11.0, font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"before: \ installers paid by the hour, \ with a minimum standard to meet", font_size=24),
            label(r"a new computer system records who installed each windscreen", font_size=24, color=SIGNAL),
            label(r"1994--95: \ a piece rate for each one, \ with the hourly wage kept as a floor", font_size=24,
                  color=PAY),
            label(rf"output per worker rises by {100 * lz['gain_published']:.0f}\%", font_size=30, color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).next_to(hc, DOWN, buff=0.55)
        tag = published_tag(r"Lazear, AER 90(5) (2000)", corner=DR, font_size=13)
        with self.voiceover(
            "Now a firm that changed its contract. <bookmark mark='a'/> Safelite Glass, in Columbus, Ohio, was the "
            "largest installer of car windscreens in the United States. Its installers were paid by the hour, with a "
            "minimum standard to meet. <bookmark mark='b'/> In the early nineties a new computer system began to "
            "record who had installed each windscreen, so output could be measured worker by worker. "
            "<bookmark mark='c'/> In 1994 and 1995 Safelite switched to paying a piece rate for each windscreen, "
            "keeping the hourly wage as a floor for anyone who fell short. <bookmark mark='d'/> Edward Lazear "
            "studied the switch. Output per worker rose by forty-four percent."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def sorting(self):
        floor, rate = 2.0, 0.5
        ax = plane([0, 10], [0, 5.2], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.2, y_length=4.6, xticks=[],
                   yticks=[], xlabel=r"windscreens a day", ylabel=r"a day's pay", font_size=16)
        a = ax.ax
        hourly = seg(ax, 0, floor, 10, floor, color=GREY_B, width=3)
        hl = label(r"hourly pay", font_size=15, color=GREY_B).next_to(a.c2p(9.6, floor), DOWN, buff=0.12,
                                                                     aligned_edge=RIGHT)
        kink = floor / rate
        ppp = VGroup(seg(ax, 0, floor, kink, floor, color=PAY, width=4), seg(ax, kink, floor, 10, rate * 10,
                                                                             color=PAY, width=4))
        pl = label(r"piece rate, \ with the floor", font_size=15, color=PAY).next_to(a.c2p(9.0, rate * 9.0), LEFT,
                                                                                   buff=0.15)
        std = seg(ax, 2.5, 0, 2.5, 5.0, color=GREY_C, width=1.5, dashed=True)
        stdl = label(r"the minimum \\ standard", font_size=13, color=GREY_C).next_to(a.c2p(2.5, 5.0), RIGHT, buff=0.08)
        rng = np.random.default_rng(3)
        able = np.sort(rng.uniform(0, 1, 14))
        before = VGroup(*[Dot(a.c2p(2.3 + 0.2 * (k % 3), 0.3 + 0.22 * (k // 3)), radius=0.055, color=GREY_A)
                          for k in range(len(able))])
        after_x = [max(2.5, 1.5 + 8.0 * x) for x in able]
        after = VGroup(*[Dot(a.c2p(x, 0.35), radius=0.055, color=EFFORT) for x in after_x])
        side = VGroup(
            label(r"paid by the hour, \ everyone does the standard: \\ more earns nothing", font_size=21,
                  color=GREY_B),
            label(r"paid by the piece, \ each fits as many \\ as their skill makes worth it", font_size=21,
                  color=EFFORT),
            label(r"and who works there changes: \\ quick installers stay and apply; \\ slow ones are likelier to leave",
                  font_size=21, color=PAY),
            label(r"two effects: \ the same people work harder, \\ and different people take the job", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = illustrative_tag(r"illustrative: \ Lazear's model, \ not his data", corner=DR, font_size=13)
        with self.voiceover(
            "Lazear's explanation has two parts. <bookmark mark='a'/> Paid by the hour, an installer who meets the "
            "standard earns the same whether they fit one windscreen more or ten, so each does about the standard. "
            "<bookmark mark='b'/> Paid by the piece, each installer fits as many as their own skill makes worth the "
            "effort, so the quick ones spread out to the right. <bookmark mark='c'/> And the job attracts different "
            "people. A quick installer earns more at Safelite than before, so quick installers stay, and apply; a "
            "slow one gains nothing and is likelier to leave. <bookmark mark='d'/> So there are two effects: the same "
            "people working harder, which is incentives, and different people taking the job, which is sorting."
        ) as vo:
            self.play(FadeIn(ax), Create(hourly), FadeIn(hl), Create(std), FadeIn(stdl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), LaggedStart(*[FadeIn(d) for d in before], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(Create(ppp), FadeIn(pl), FadeIn(side[1]))
            self.play(*[Transform(b, a_) for b, a_ in zip(before, after)], run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), *[d.animate.set_opacity(0.25) for d in before[:4]])
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def split(self):
        lz = tables.LAZEAR_2000.data
        total = 100 * lz["gain_published"]
        ax = plane([0, 50], [0, 1], center=UP * 1.0, x_length=10.5, y_length=1.2, xticks=[0, 10, 20, 30, 40, 50],
                   yticks=[], xlabel=r"rise in output per worker, \ percent", ylabel="", font_size=16,
                   xfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        u = a.x_axis.get_unit_size()
        inc = Rectangle(width=total / 2 * u, height=0.7, stroke_width=0, fill_color=EFFORT, fill_opacity=0.85
                        ).move_to(a.c2p(0, 0.5), aligned_edge=LEFT)
        srt = Rectangle(width=total / 2 * u, height=0.7, stroke_width=0, fill_color=PAY, fill_opacity=0.85
                        ).next_to(inc, RIGHT, buff=0)
        il = label(r"incentives: \ the same workers", font_size=17, color=BACKGROUND).move_to(inc)
        sl = label(r"sorting: \ who works there", font_size=17, color=BACKGROUND).move_to(srt)
        tl = label(rf"{total:.0f}\%", font_size=24, color=E.ACCENT).next_to(srt, RIGHT, buff=0.15)
        rows = VGroup(
            label(r"about half of the rise from each \ (the published estimate)", font_size=22),
            label(rf"pay rose too: \ workers kept part of the gain, \ about {100 * lz['wage_rise']:.0f}\% more on "
                  r"average", font_size=22, color=PAY),
            label(rf"the 1996 working paper: \ {100 * lz['gain_wp'][0]:.0f} to {100 * lz['gain_wp'][1]:.0f}\%, \ "
                  r"depending on what is held fixed", font_size=20, color=GREY_B),
            label(r"why not everywhere? \ here output is easy to count, \ and a bad fitting comes back to its "
                  r"installer", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(ax, DOWN, buff=0.6)
        tag = published_tag(r"Lazear, AER 90(5) (2000); \ NBER WP 5672 (1996)", corner=DR, font_size=13)
        with self.voiceover(
            "Lazear could tell the two effects apart, because he had each installer's output before and after the "
            "switch, and could also compare the people who left with the people who joined. <bookmark mark='a'/> "
            "About half of the forty-four percent came from incentives, the same workers fitting more, and about "
            "half from sorting. <bookmark mark='b'/> The workers shared in it: average pay rose by about ten percent. "
            "<bookmark mark='c'/> An earlier working paper put the rise at twenty to thirty-six percent, depending on "
            "what is held fixed; the forty-four is the figure usually quoted. <bookmark mark='d'/> Why doesn't every "
            "firm pay by the piece? Because at Safelite output is easy to count, and a badly fitted windscreen comes "
            "back to the installer who fitted it, to be redone without pay. Chapter seven is about the jobs where "
            "neither is true."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(inc, LEFT), FadeIn(il))
            self.play(GrowFromEdge(srt, LEFT), FadeIn(sl), FadeIn(tl), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def others(self):
        pr = tables.PIECE_RATES.data
        c1 = study_card(r"Tree planters in British Columbia", r"Bruce Shearer, \ 2004", [
            (r"varied", r"planters randomly assigned to piece rates or a daily wage"),
            (r"found", rf"piece rates raised output by about {100 * pr['shearer']:.0f}\%"),
        ], design="RCT", width=6.2, font_size=21)
        c2 = study_card(r"Fruit pickers on a British farm", r"Bandiera, Barankay and Rasul, \ 2005", [
            (r"varied", r"from pay relative to the others' to a piece rate"),
            (r"found", rf"output at least {100 * pr['bbr']:.0f}\% higher under piece rates"),
            (r"why", r"relative pay: picking fast hurts your friends, so pickers held back"),
        ], design="DiD", width=6.2, font_size=21)
        VGroup(c1, c2).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 0.5)
        foot = label(r"chapter thirteen puts these on a dial", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Shearer, REStud 71(2) (2004); \ Bandiera, Barankay and Rasul, QJE 120(3) (2005)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Safelite is one firm. Two other studies come close to experiments. <bookmark mark='a'/> In British "
            "Columbia, Bruce Shearer had tree planters randomly assigned to piece rates or a daily wage. Piece rates "
            "raised output by about twenty percent. <bookmark mark='b'/> On a farm in Britain, Oriana Bandiera, Iwan "
            "Barankay and Imran Rasul watched fruit pickers move from pay relative to the others' to a piece rate. "
            "Output rose by at least half. Under relative pay, picking faster lowers your friends' pay, and the "
            "pickers held back, most of all when their friends were in the same field. <bookmark mark='c'/> "
            "Chapter thirteen puts these numbers on a dial."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(c1, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
