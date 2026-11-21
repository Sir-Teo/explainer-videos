from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403

PLAN_SHORT = {"free trade throughout": r"A: \ free trade throughout",
              "a tariff, kept": r"B: \ a 25\% tariff, \ kept",
              "a tariff for two rounds, then free trade": r"C: \ a tariff for two rounds, \ then free trade"}


def cell(txt, color, w=2.9, h=0.75, font=20, fill=0.18):
    box = Rectangle(width=w, height=h, stroke_color=GREY_B, stroke_width=1.4, fill_color=color, fill_opacity=fill)
    if not txt:                                   # an empty TeX string cannot be typeset
        return VGroup(box.set_stroke(opacity=0))
    return VGroup(box, label(txt, font_size=font, color=WHITE).move_to(box))


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ a tariff arrives", r"You set America's trade policy for ten rounds, \ against a "
             r"partner you do not know: \ which plan?", "Chapter two. Play it: a tariff arrives.",
             scale=("nation", "world"), horizon=("a decade",))
        self.stage()
        self.reveal()

    def matrix(self):
        R = load("repeated")
        pay = R["stage"]["pay"]
        g = VGroup()
        head = VGroup(cell(r"", BACKGROUND, fill=0), cell(r"partner: \ free trade", ROW, font=17),
                      cell(r"partner: \ 25\% tariff", ROW, font=17)).arrange(RIGHT, buff=0)
        g.add(head)
        for me in ("free", "tariff"):
            r = VGroup(cell(r"you: \ free trade" if me == "free" else r"you: \ 25\% tariff", US, font=17))
            for them in ("free", "tariff"):
                u = pay[f"{me}|{them}"][0]
                col = FREE if u > 0.01 else (TARIFF if u < -0.01 else GREY_C)
                r.add(cell(rf"{u:+.2f}\%".replace("-", "{-}"), col, font=22))
            g.add(r.arrange(RIGHT, buff=0))
        g.arrange(DOWN, buff=0)
        return g, pay

    def stage(self):
        g, pay = self.matrix()
        g.scale(0.9).to_edge(UP, buff=0.6)
        note = label(r"your real income, \ each round, \ from the model of chapter four \ (the United States against "
                     r"the rest)", font_size=17, color=GREY_A).next_to(g, DOWN, buff=0.2)
        plans = VGroup(*[label(PLAN_SHORT[p], font_size=22, color=E.ACCENT) for p in PLAN_SHORT]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22)
        partners = VGroup(
            label(r"your partner is one of three kinds, \ equally likely:", font_size=20, color=GREY_A),
            label(r"copies your last move \ (tit for tat)", font_size=19, color=ROW),
            label(r"never retaliates", font_size=19, color=ROW),
            label(r"retaliates for ever once you tax it", font_size=19, color=ROW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        VGroup(plans, partners).arrange(RIGHT, buff=1.0, aligned_edge=UP).next_to(note, DOWN, buff=0.45)
        tag = island_tag(r"a model: \ agora.tradewar.stage\_payoffs, \ repeated", corner=DL, font_size=12)
        with self.voiceover(
            "Your turn. You set America's trade policy for ten rounds, a round a year, against the rest of the "
            "world as one partner. <bookmark mark='a'/> Each round, the model of chapter four gives your real "
            "income. Both at free trade: zero. A twenty-five percent tariff while the partner keeps free trade: "
            f"you gain {pay['tariff|free'][0]:.2f} percent, because you pay less for what you import. The partner "
            f"taxes you and you do not: you lose {-pay['free|tariff'][0]:.2f}. Both tax: you lose "
            f"{-pay['tariff|tariff'][0]:.2f}. <bookmark mark='b'/> You have three plans: free trade throughout; a "
            "tariff, kept; or a tariff for two rounds, then back to free trade. <bookmark mark='c'/> And you do not "
            "know your partner. It may copy your last move, it may never retaliate, or it may retaliate for ever "
            "once taxed. Each is equally likely, and next year counts nine tenths as much as this one. Which plan?"
        ) as vo:
            self.play(FadeIn(tag), FadeIn(g), FadeIn(note))
            vo.wait_until("a")
            self.play(Indicate(g, scale_factor=1.02))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in plans], lag_ratio=0.4), run_time=1.6)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in partners], lag_ratio=0.3), run_time=1.6)
        ring = countdown().scale(0.5).to_corner(DR, buff=0.3)
        self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.wait(0.3)
        self.clear_scene()

    def reveal(self):
        R = load("repeated")
        res = R["results"]
        partners = ("tit for tat", "never retaliates", "retaliates for ever")
        plans = list(PLAN_SHORT)
        head = VGroup(cell(r"", BACKGROUND, w=3.9, fill=0),
                      *[cell(p, ROW, w=2.6, font=16) for p in (r"tit for tat", r"never retaliates",
                                                                  r"retaliates for ever")],
                      cell(r"average", E.ACCENT, w=2.0, font=16)).arrange(RIGHT, buff=0)
        table = VGroup(head)
        avgs = {}
        for p in plans:
            vals = [res[f"{q}|{p}"]["total"] for q in partners]
            avgs[p] = float(np.mean(vals))
            r = VGroup(cell(PLAN_SHORT[p], US, w=3.9, font=15))
            for v in vals:
                col = FREE if v > 0.01 else (TARIFF if v < -0.01 else GREY_C)
                r.add(cell(rf"{v:+.2f}".replace("-", "{-}"), col, w=2.6, font=20))
            col = FREE if avgs[p] > 0.01 else (TARIFF if avgs[p] < -0.01 else GREY_C)
            r.add(cell(rf"{avgs[p]:+.2f}".replace("-", "{-}"), col, w=2.0, font=20, fill=0.35))
            table.add(r.arrange(RIGHT, buff=0))
        table.arrange(DOWN, buff=0).move_to(UP * 0.6)
        if table.width > 13.2:
            table.scale_to_fit_width(13.2)
        unit = label(r"the discounted sum of your real income over ten rounds, \ percent of a year's income",
                     font_size=17, color=GREY_A).next_to(table, DOWN, buff=0.25)
        lesson = label(r"tariffs pay only against a partner who will not answer", font_size=22,
                       color=E.ACCENT).next_to(unit, DOWN, buff=0.5)
        tag = island_tag(r"computed: \ agora.tradewar.repeated \ (discount 0.9)", corner=DL, font_size=12)
        kept = res["never retaliates|a tariff, kept"]["total"]
        tft = res["tit for tat|a tariff, kept"]["total"]
        with self.voiceover(
            "Here is what each plan earns against each partner. <bookmark mark='a'/> Free trade throughout earns "
            "zero against everyone: nothing gained, nothing lost. <bookmark mark='b'/> A tariff kept earns "
            f"{kept:.1f} percent of a year's income against a partner who never retaliates, but against the other "
            f"two, who answer and keep answering, it loses {-tft:.1f}. <bookmark mark='c'/> A tariff for two "
            "rounds is worst against the partner who never forgives: you pay the war, then free trade on your side "
            "while they keep their tariff. <bookmark mark='d'/> Averaged over the three partners, free trade wins. "
            "A tariff pays only if you are sure your partner will not answer, and partners learn. That is the "
            "logic of the trade agreements in the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(unit), FadeIn(tag))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(table[k + 1][:4], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(*[FadeIn(table[k + 1][4]) for k in range(3)], FadeIn(lesson))
        self.clear_scene()
