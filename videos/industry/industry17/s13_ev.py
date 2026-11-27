from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403

REGIONS = [("Norway", "Norway"), ("China", "China"), ("Europe", "Europe"), ("World", "World"), ("United States", "United States")]


class Electric(VoiceoverScene):
    def construct(self):
        card(self, 11, "The electric car", "What does the battery change, and why have so many lost money on it?",
             "Chapter eleven. The electric car. What does the battery change, and why have so many lost money on it?",
             lit=("make", "change"))
        self.battery()
        self.shares()
        self.losses()

    def battery(self):
        E = R["ev"]
        pk = E["pack"]
        pa = viz.plot_axes([2008, 2024], [0, 1500], x_length=6.6, y_length=4.2, xticks=[2008, 2012, 2016, 2020, 2023],
                           yticks=[0, 500, 1000, 1500], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:,.0f}",
                           ylabel="battery pack cost per kWh (2023 dollars)", size=13).move_to([-3.2, -0.5, 0])
        bars_ = viz.year_bars(pa, sorted(pk), [pk[y] for y in sorted(pk)], EV, width=0.32)
        l0 = tx(f"${pk[2008]:,.0f}", 15, EV, bold=True).next_to(bars_[0], UP, buff=0.08)
        l1 = tx(f"${pk[2023]:,.0f}", 15, EV, bold=True).next_to(bars_[-1], UP, buff=0.08)
        B = E["battery"]
        packs = VGroup(VGroup(draw.battery_pack(2.4), tx(f"a {B['kwh']} kWh pack, 2008 costs: {usd(B['cost2008'])}", 15, GREY_A)).arrange(DOWN, buff=0.1),
                       VGroup(draw.battery_pack(2.4, color=GOOD), tx(f"2023 costs: {usd(B['cost'])}", 17, GOOD, bold=True)).arrange(DOWN, buff=0.1),
                       VGroup(draw.engine(1.0), tx(f"the engine, gearbox and exhaust it replaces: say {usd(B['ice'])}", 14, GREY_A),
                              tx(f"parity at about ${B['parity']:.0f} per kWh", 15, PRICE, bold=True)).arrange(DOWN, buff=0.08)).arrange(DOWN, buff=0.35).move_to([3.7, -0.2, 0])
        tag = estimate_tag("the engine's cost: an assumption, for scale", size=13)
        src = source("US Department of Energy, Vehicle Technologies Office, Fact of the Week #1354 (estimates at 100,000 packs a "
                     "year, usable energy)", size=12)
        with self.voiceover(
            "An electric car swaps the engine, gearbox, fuel tank and exhaust for a battery and a motor. The battery is "
            "the expensive part. <bookmark mark='a'/> America's Department of Energy estimates what a battery pack costs to "
            f"make, per kilowatt-hour of energy it can store. In 2008, about {pk[2008]:,.0f} dollars in today's money. "
            f"<bookmark mark='b'/> By 2023, {pk[2023]:,.0f}: {100 * E['pack_fall']:.0f} per cent less. "
            f"<bookmark mark='c'/> For a {B['kwh']} kilowatt-hour pack, enough for a family car, that is the difference "
            f"between {B['cost2008']:,.0f} dollars and {B['cost']:,.0f}. <bookmark mark='d'/> If the engine, gearbox and "
            f"exhaust it replaces cost something like {B['ice']:,.0f} dollars to make, the battery reaches parity near "
            f"{B['parity']:.0f} dollars a kilowatt-hour. Close, but not yet, by these estimates."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(tag), FadeIn(ghost(bars_, opacity=0.3)))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars_[0], DOWN), FadeIn(l0))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_[1:]], lag_ratio=0.1), run_time=2.5)
            self.play(FadeIn(l1))
            vo.wait_until("c")
            self.play(FadeIn(packs[0]), FadeIn(packs[1]))
            vo.wait_until("d")
            self.play(FadeIn(packs[2]))
        self.clear_scene()

    def shares(self):
        E = R["ev"]
        S = E["shares"]
        pa = viz.plot_axes([2012, 2026], [0, 100], x_length=9.0, y_length=4.4, xticks=[2012, 2015, 2018, 2021, 2025],
                           yticks=[0, 25, 50, 75, 100], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}%",
                           ylabel="electric share of new cars sold (battery and plug-in hybrid)", size=13).move_to([-0.8, -0.5, 0])
        lines, labs = VGroup(), VGroup()
        for key, name in REGIONS:
            s = {y: v for y, v in S[key].items() if 2012 <= y <= 2025}
            col = COUNTRY_COL[key]
            lines.add(poly(pa, sorted(s.items()), col, 4 if key in ("China", "World") else 3))
            labs.add(tx(f"{name} {s[2025]:.0f}%", 15, col, bold=True).next_to(pa.ax.c2p(2025, s[2025]), RIGHT, buff=0.12))
        src = source("IEA, Global EV Outlook 2026, via Our World in Data", size=12)
        w, c, e, u = S["World"][2025], S["China"][2025], S["Europe"][2025], S["United States"][2025]
        with self.voiceover(
            "And so the share of electric cars has climbed, very unevenly. <bookmark mark='a'/> In Norway, "
            f"{S['Norway'][2025]:.0f} per cent of new cars sold in 2025 were electric. "
            f"<bookmark mark='b'/> In China, {c:.0f} per cent: more than half. <bookmark mark='c'/> In Europe, {e:.0f}; "
            f"in the world as a whole, {w:.0f}. <bookmark mark='d'/> In the United States, {u:.0f}, and the federal tax "
            "credits for electric cars were repealed in 2025, as Tesla's own annual report notes. Much the same cars, "
            "and shares from one in ten to almost all: what differs from place to place is policy and price."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(ghost(lines, opacity=0.25)))
            for mk, k in zip("abcd", ([0], [1], [2, 3], [4])):
                vo.wait_until(mk)
                self.play(*[Create(lines[i]) for i in k], run_time=1.8)
                self.play(*[FadeIn(labs[i]) for i in k])
        self.clear_scene()

    def losses(self):
        E = R["ev"]
        me = E["model_e"]
        wd = E["writedowns"]
        rows = VGroup()
        for i, (name, v) in enumerate(sorted(wd.items(), key=lambda kv: -kv[1])):
            y = 1.2 - 0.85 * i
            b = bar(-1.0, y, v * 0.3, 0.5, BAD)
            rows.add(VGroup(tx(name, 18, WHITE, bold=True).next_to([-1.2, y, 0], LEFT, buff=0.0), b,
                            tx(f"${v:.1f}bn", 17, BAD, bold=True).next_to(b, RIGHT, buff=0.12)))
        head = tx("Charges for cancelled or scaled-back electric plans, 2025", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        per = VGroup(tx("Ford Model e, loss per vehicle:", 16, GREY_A),
                     tx(f"2024 {usd(me['per'][0])}", 20, BAD, bold=True), tx(f"2025 {usd(me['per'][1])}", 20, BAD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([-4.6, -2.0, 0])
        tsla = VGroup(tx("Tesla, 2025:", 16, GREY_A), tx(f"automotive gross margin {E['tsla_gm']:.1f}%", 18, EV, bold=True),
                      tx(f"incl. ${E['credits'] / 1000:.1f}bn of regulatory credits sold", 15, GREY_A), tx("to other carmakers", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([3.4, -2.0, 0])
        src = source("Ford and GM, Forms 10-K 2025; Stellantis, Form 20-F 2025 (EUR 18.8bn at the 2025 average rate); Tesla, Form 10-K 2025", size=12)
        with self.voiceover(
            "For the established makers, the electric car has so far been a way to lose money. <bookmark mark='a'/> Ford's "
            f"electric business lost about {-me['per'][0]:,.0f} dollars per vehicle in 2024 and {-me['per'][1]:,.0f} in "
            "2025, on sales too small to cover its costs. <bookmark mark='b'/> In 2025 the old "
            f"makers wrote off a large part of their electric plans. Stellantis took charges of about {wd['Stellantis']:.0f} "
            f"billion dollars, Ford {wd['Ford']:.1f} billion, General Motors {wd['GM']:.1f} billion: platforms "
            "abandoned, programmes cancelled, battery plants resized. <bookmark mark='c'/> Tesla, which makes nothing but "
            f"electric cars, does make money on them: its automotive gross margin was "
            f"{E['tsla_gm']:.1f} per cent, and part of its revenue came from selling regulatory credits to other carmakers "
            "that needed them to meet emissions rules."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(ghost(*[r_[0] for r_ in rows], opacity=0.3)))
            vo.wait_until("a")
            self.play(FadeIn(per))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in rows], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(tsla))
        self.clear_scene()
