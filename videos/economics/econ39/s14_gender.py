from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Gender(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The gender gap", r"Why do women still earn less, \ and when does the gap open?",
             "Chapter twelve. The gender gap.",
             lit={2014: r"Goldin", 2019: r"Kleven, \ Landais and S\o{}gaard"}, scale=("person", "household"),
             horizon=("a decade",))
        self.convergence()
        self.hours()
        self.penalty()
        self.fact()

    def convergence(self):
        G = load("gender")
        ys, r = np.array(G["years"]), np.array(G["ratio"])
        ax = plane([1978, 2026], [0.55, 0.9], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.8,
                   xticks=[1980, 1990, 2000, 2010, 2020], yticks=[0.6, 0.7, 0.8, 0.9],
                   ylabel=r"women's median weekly earnings over men's", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        k00 = list(ys).index(2000)
        ln1 = path(ax, ys[:k00 + 1], r[:k00 + 1], WOMEN, 3.4, smooth=False)
        ln2 = path(ax, ys[k00:], r[k00:], WOMEN, 3.4, smooth=False)
        side = VGroup(
            label(rf"1979: \ {100 * G['r1979']:.0f}\%", font_size=20, color=WOMEN),
            label(rf"2000: \ {100 * r[k00]:.0f}\%", font_size=20, color=WOMEN),
            label(rf"2025: \ {100 * G['r2025']:.0f}\%", font_size=20, color=WOMEN),
            label(r"full-time workers; \\ not adjusted for \\ hours or occupation", font_size=15, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"BLS, \ Current Population Survey, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "In 1979 the median woman working full time in America earned "
            f"{100 * G['r1979']:.0f} percent of the median man's weekly pay. <bookmark mark='a'/> Over the next two "
            "decades the gap closed fast, as women's schooling caught up and then overtook men's, and women entered "
            f"professions they had been kept out of: by 2000 the ratio was {100 * r[k00]:.0f} percent. "
            "<bookmark mark='b'/> Since then it has crept up, to "
            f"{100 * G['r2025']:.0f} percent in 2025. The question is what is left."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(side[3]))
            vo.wait_until("a")
            self.play(Create(ln1), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(ln2), FadeIn(side[2]), run_time=2.0)
        self.clear_scene()

    def hours(self):
        hc = history_card(2014, r"Claudia Goldin", r"`A Grand Gender Convergence: \ Its Last Chapter': \ the gap "
                          r"would shrink, \ and might vanish, \ if firms did not reward long hours and particular "
                          r"hours disproportionately", color=E.ACCENT, width=11.0, font_size=24).move_to(UP * 1.6)
        ax = plane([30, 70], [0, 1.6], center=DOWN * 1.2, x_length=7.0, y_length=2.4, xticks=[40, 50, 60, 70],
                   yticks=[0, 0.5, 1.0, 1.5], xlabel=r"hours a week", ylabel=r"pay", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=13)
        h = np.linspace(30, 70, 60)
        lin = path(ax, h, h / 45, HSCHOOL, 3.0)
        cvx = path(ax, h, (h / 45) ** 2.2, LOSS, 3.0, yr=(0, 1.6))
        keys = VGroup(label(r"blue: \ pay in proportion to hours \ (pharmacy, \ tech)", font_size=16,
                            color=HSCHOOL),
                      label(r"red: \ long, \ fixed hours paid more than in proportion \ (law, \ finance)",
                            font_size=16, color=LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(ax, DOWN,
                                                                                                        buff=0.2)
        tag = published_tag(tables.GENDER.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Claudia Goldin, who received the Nobel prize for this work in 2023, argued that the last chapter is "
            "about time. <bookmark mark='a'/> In many jobs, pay rises in proportion to hours. <bookmark mark='b'/> "
            "In others, long hours, and hours at particular times, the evening meeting, the client call at night, "
            "are rewarded more than in proportion, because one person who is always available is worth more than "
            "two who share the work. Whoever in a couple takes the flexible job, usually the mother, earns less per "
            "hour. Pharmacy, she showed, became a flexible profession, with a small gender gap; law and finance did "
            "not."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.15), FadeIn(tag), FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(lin), FadeIn(keys[0]))
            vo.wait_until("b")
            self.play(Create(cvx), FadeIn(keys[1]))
        self.clear_scene()

    def penalty(self):
        G = load("gender")
        C, K = G["child"], G["kls"]
        ev = np.array(C["event"])
        ax = plane([-5.5, 10.5], [-0.4, 0.1], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.6, y_length=4.8,
                   xticks=[-5, 0, 5, 10], yticks=[-0.4, -0.3, -0.2, -0.1, 0, 0.1],
                   xlabel=r"years since the first child", ylabel=r"earnings relative to the year before",
                   xfmt=lambda v: f"{v:+.0f}", yfmt=lambda v: f"{100 * v:+.0f}\\%", font_size=14)
        zero = seg(ax, -5.5, 0, 10.5, 0, GREY_B, 1.5, dashed=True)
        birth = vline(ax, -0.5, -0.4, 0.1, GREY_B)
        lm = path(ax, ev, C["men"], MEN, 3.2, smooth=False)
        lw = path(ax, ev, C["women"], WOMEN, 3.2, smooth=False)
        dm = VGroup(*[dot(ax, x, y, MEN, 0.06) for x, y in zip(ev, C["men"])])
        dw = VGroup(*[dot(ax, x, y, WOMEN, 0.06) for x, y in zip(ev, C["women"])])
        lp = path(ax, ev, C["planted"], GREY_A, 2.0, smooth=False)
        side = VGroup(
            label(r"blue: \ fathers", font_size=18, color=MEN),
            label(r"pink: \ mothers", font_size=18, color=WOMEN),
            label(rf"the child penalty, \\ years 6 to 10: \ {100 * C['long_run']:.0f}\%", font_size=18,
                  color=E.ACCENT),
            label(r"grey: \ the planted truth", font_size=16, color=GREY_A),
            label(rf"Denmark: \ about {K['penalty']}\% \\ in the long run", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        kc = history_card(2019, r"Kleven, \ Landais and S\o{}gaard", r"follow Danish parents year by year around "
                          r"the birth of their first child, \ in the government's records, \ against people of the "
                          r"same age who had a child at another time", color=WOMEN, width=10.4, font_size=24)
        with self.voiceover(
            "When does the gap open? In 2019 Henrik Kleven, Camille Landais and Jakob Egholt Søgaard followed "
            "Danish parents through the government's records, year by year around the birth of their first child, "
            "comparing them with their own earlier selves and with people of the same age who had a child at a "
            "different time. <bookmark mark='a'/> On the Island, the same design: fathers' earnings barely move "
            "when the child arrives. <bookmark mark='b'/> Mothers' fall by "
            f"{say_pct(-np.expm1(C['women'][list(ev).index(1)]), 0)} in the first year, and never recover: "
            f"<bookmark mark='c'/> ten years later they are about {say_pct(-np.expm1(C['long_run']), 0)} below where "
            "they would have been. "
            "<bookmark mark='d'/> The Island's truth is planted, and the design recovers it. "
            f"<bookmark mark='e'/> In Denmark the long-run penalty is about {K['penalty']} percent, through fewer "
            "hours, "
            "less work and lower pay per hour, and the share of the remaining gender gap caused by children rose from "
            f"about {K['share1980']} percent in 1980 to about {K['share2013']} percent by 2013."
        ) as vo:
            self.play(FadeIn(kc, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeOut(kc), run_time=0.5)
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(birth), FadeIn(tag), Create(lm), FadeIn(dm), FadeIn(side[0]),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lw), FadeIn(dw), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(lp), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def fact(self):
        G = load("gender")
        C = G["child"]
        f = facts.BY_KEY["child_penalty"]
        data_m = label(rf"Denmark: \\ mothers' earnings \\ about {G['kls']['penalty']}\% lower \\ in the long run",
                       font_size=18, color=WHITE)
        theory_m = label(r"hours and flexibility: \\ who in a couple \\ takes the flexible job", font_size=18,
                         color=WOMEN)
        agora_m = label(rf"the event study \\ recovers a planted \\ penalty: \ {100 * C['long_run']:.0f}\%",
                        font_size=18, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, WOMEN, None)).move_to(UP * 0.3)
        tag = published_tag(tables.GENDER.tag, corner=DR, font_size=11)
        with self.voiceover(
            "That makes it one of the series' facts. <bookmark mark='a'/> In the data, the gender gap in earnings "
            "opens at the birth of the first child. <bookmark mark='b'/> The theory is about hours, flexibility, and "
            "who in a couple takes the flexible job. <bookmark mark='c'/> And Agora's event study recovers a planted "
            "penalty of about the size the Danish records show."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(fc.cols[k][2:]))
        self.clear_scene()
