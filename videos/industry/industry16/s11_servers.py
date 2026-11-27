from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403

ORDER = ["Mexico", "Taiwan", "Thailand", "China", "other"]


class Servers(VoiceoverScene):
    def construct(self):
        card(self, 9, "The new box: servers", "What is the fastest-growing thing the assemblers build?",
             "Chapter nine. The new box: servers.", lit=("sold", "change"))
        self.imports()
        self.makers()
        self.builders()
        self.dell()

    def imports(self):
        S = R["servers"]["imports"]
        ys = list(range(2015, 2026))
        sc = 4.6 / 170
        base = -2.5
        cols = VGroup()
        for i, y in enumerate(ys):
            x = -5.6 + 0.95 * i
            stack, h0 = VGroup(), base
            parts = {p: S.get(p, {}).get(y, 0.0) for p in ORDER[:-1]}
            parts["other"] = S["World"][y] - sum(parts.values())
            for p in ORDER:
                v = max(parts[p], 0)
                if v * sc < 0.004:
                    continue
                r_ = Rectangle(width=0.62, height=v * sc, stroke_width=0, fill_color=COUNTRY_COL[p], fill_opacity=0.9).move_to([x, h0, 0], aligned_edge=DOWN)
                stack.add(r_)
                h0 += v * sc
            lab = tx(str(y), 12, GREY_B).move_to([x, base - 0.22, 0])
            tot = tx(f"${S['World'][y]:.0f}bn", 13, WHITE, bold=True).move_to([x, h0 + 0.18, 0])
            cols.add(VGroup(stack, lab, tot))
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=COUNTRY_COL[p], fill_opacity=0.9), tx(p, 14, GREY_A)).arrange(RIGHT, buff=0.08)
                       for p in ORDER]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.3, 0.6, 0])
        head = tx("US imports of computer processing units (servers and the like)", 20, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("UN Comtrade: US imports, HS 847150 (processing units), by partner, 2015-2025, as reported by the United States", size=13)
        m, t = S["Mexico"], S["Taiwan"]
        with self.voiceover(
            "Now the box that changed the business. <bookmark mark='a'/> Here is what America imported of computer "
            "processing units, the customs category that holds servers, each year since 2015. "
            f"<bookmark mark='b'/> For years it ran at twenty to forty billion dollars, mostly from Mexico. "
            f"<bookmark mark='c'/> Then the data-centre boom: ${S['World'][2024]:.0f} billion in 2024 and "
            f"${S['World'][2025]:.0f} billion in 2025. From Mexico, ${m[2025]:.0f} billion; from Taiwan, ${t[2025]:.0f} "
            f"billion, up from ${t[2023]:.0f} billion two years before. <bookmark mark='d'/> And from China, which supplied "
            f"${S['China'][2018]:.1f} billion in 2018: ${S['China'][2025]:.1f} billion. The servers are built close to the "
            "buyer, or where the chips are made."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(key), *[FadeIn(c[1]) for c in cols], FadeIn(ghost(*[c[0] for c in cols], opacity=0.2)))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(*[GrowFromEdge(r_, DOWN) for r_ in c[0]], FadeIn(c[2])) for c in cols[:3]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(*[GrowFromEdge(r_, DOWN) for r_ in c[0]], FadeIn(c[2])) for c in cols[3:9]], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(*[GrowFromEdge(r_, DOWN) for r_ in c[0]], FadeIn(c[2])) for c in cols[9:]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(key[3], color=COUNTRY_COL["China"], scale_factor=1.1))
        self.clear_scene()

    def makers(self):
        S = R["servers"]
        sm, cl = S["smci"], S["cls"]
        (c24, c25), (s24, s25) = S["cloud"], S["sce"]
        rows = [(draw.server_rack(0.9, 0.8), "Supermicro: server maker, fiscal years to June", f"revenue ${sm[2019]:.1f}bn (2019) to ${sm[max(sm)]:.1f}bn ({max(sm)})",
                 sm[max(sm)] / sm[2019], "#7EC8F5"),
                (draw.server_rack(0.9, 0.6), "Celestica: contract manufacturer", f"revenue ${cl[2022]:.1f}bn (2022) to ${cl[2025]:.1f}bn (2025)", cl[2025] / cl[2022], "#F2A65A"),
                (draw.factory(1.0), "Hon Hai: cloud and networking", f"NT${c24 / 1000:.2f}tn (2024) to NT${c25 / 1000:.2f}tn (2025)", c25 / c24, "#B58CFF")]
        g = VGroup()
        for i, (ic, name, what, x_, col) in enumerate(rows):
            y = 1.8 - 1.7 * i
            ic.scale_to_fit_height(0.9).move_to([-5.6, y, 0])
            t = VGroup(tx(name, 17, WHITE, bold=True), tx(what, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([-4.8, y, 0], aligned_edge=LEFT)
            m = tx(f"x{x_:.1f}", 34, col, bold=True).move_to([4.8, y, 0])
            g.add(VGroup(ic, t, m))
        src = source("SEC EDGAR: Super Micro Computer and Celestica, Forms 10-K; Hon Hai, audited statements 2025 (revenue by product type)", size=13)
        with self.voiceover(
            "The companies that build them grew with them. <bookmark mark='a'/> Supermicro, an American server maker, sold "
            f"about ${sm[2019]:.1f} billion in its fiscal 2019 and ${sm[max(sm)]:.0f} billion in the year to June "
            f"{max(sm)}. <bookmark mark='b'/> Celestica, a Canadian contract manufacturer, grew from ${cl[2022]:.1f} billion "
            f"to ${cl[2025]:.1f} billion in three years. <bookmark mark='c'/> And Hon Hai's cloud and networking line rose "
            f"by {100 * (c25 / c24 - 1):.0f} per cent in a single year. And, as Hon Hai's own segments showed, building "
            "servers pays better, for now, than building phones."
        ) as vo:
            self.play(FadeIn(src), *[FadeIn(r_[0]) for r_ in g], FadeIn(ghost(*[r_[1] for r_ in g], opacity=0.25)))
            for mk, r_ in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r_[1], shift=RIGHT * 0.2), FadeIn(r_[2], scale=1.2))
        self.clear_scene()

    def dell(self):
        S = R["servers"]
        ai = S["dell_ai"]
        (ir, io_), (cr, co) = S["dell_isg"], S["dell_csg"]
        sc = 0.13
        bars = VGroup()
        for i, y in enumerate((2024, 2025, 2026)):
            b = Rectangle(width=0.9, height=ai[y] * sc, stroke_width=0, fill_color="#7EC8F5", fill_opacity=0.6 + 0.15 * i).move_to([-5.0 + 1.3 * i, -2.4, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, tx(f"${ai[y]:.1f}bn", 15, "#7EC8F5", bold=True).next_to(b, UP, buff=0.06), tx(f"FY{y}", 13, GREY_B).next_to(b, DOWN, buff=0.08)))
        bl = tx("Dell: AI-optimized servers, net revenue", 16, WHITE, bold=True).move_to([-3.7, 2.4, 0])
        cmp_ = VGroup(tx("Dell, fiscal 2026: operating income per dollar", 16, WHITE, bold=True),
                      VGroup(tx("servers, networking, storage:", 15, GREY_A), tx(f"{100 * io_ / ir:.1f} cents", 22, "#7EC8F5", bold=True)).arrange(RIGHT, buff=0.15),
                      VGroup(tx("personal computers:", 15, GREY_A), tx(f"{100 * co / cr:.1f} cents", 22, "#B58CFF", bold=True)).arrange(RIGHT, buff=0.15),
                      tx(f"revenue: ${ir:.0f}bn and ${cr:.0f}bn", 14, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, 0.2, 0])
        src = source("Dell Technologies, Form 10-K for the year to 30 January 2026 (segment results; ISG revenue by product)", size=13)
        with self.voiceover(
            "The same shift shows inside one brand. <bookmark mark='a'/> Dell began reporting the servers it builds for "
            f"artificial intelligence separately. They brought in about ${ai[2024]:.1f} billion in its fiscal 2024, "
            f"${ai[2025]:.1f} billion the next year <bookmark mark='b'/> and ${ai[2026]:.1f} billion in the year to January "
            f"2026. <bookmark mark='c'/> Its server, networking and storage group earned {100 * io_ / ir:.1f} cents of "
            f"operating income per dollar; its personal computers, {100 * co / cr:.1f}. For now, the new box pays for the "
            "brand as well as for the builder."
        ) as vo:
            self.play(FadeIn(src), FadeIn(bl), *[FadeIn(b_[2]) for b_ in bars], FadeIn(ghost(*[b_[0] for b_ in bars], opacity=0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1])) for b_ in bars[:2]], lag_ratio=0.4), run_time=1.5)
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1]))
            vo.wait_until("c")
            self.play(FadeIn(cmp_, shift=LEFT * 0.1))
        self.clear_scene()

    def builders(self):
        S = R["servers"]
        M = S["margins"]
        pa = viz.plot_axes([2016, 2026], [0, 0.1], x_length=8.4, y_length=4.2, xticks=[2016, 2018, 2020, 2022, 2024, 2026],
                           yticks=[0, 0.02, 0.04, 0.06, 0.08, 0.1], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue, fiscal years", size=13).move_to([-1.4, -0.4, 0])
        ls = poly(pa, sorted((y, v) for y, v in M["SMCI"].items() if y >= 2016), "#7EC8F5", 4)
        lc = poly(pa, sorted((y, v) for y, v in M["CLS"].items() if y >= 2016), "#F2A65A", 4)
        ll = VGroup(tx("Supermicro", 15, "#7EC8F5", bold=True).next_to(pa.ax.c2p(max(M["SMCI"]), M["SMCI"][max(M["SMCI"])]), RIGHT, buff=0.1),
                    tx("Celestica", 15, "#F2A65A", bold=True).next_to(pa.ax.c2p(max(M["CLS"]), M["CLS"][max(M["CLS"])]), RIGHT, buff=0.1))
        fii = Dot(pa.ax.c2p(2025, S["fii_margin"]), radius=0.1, color="#B58CFF")
        fl = tx("Hon Hai's servers arm, 2025 (operating)", 13, "#B58CFF", bold=True).next_to(fii, LEFT, buff=0.15).shift(DOWN * 0.3)
        src = source("SEC EDGAR: Super Micro Computer and Celestica, Forms 10-K; Hon Hai, audited statements 2025 (segments)", size=13)
        cm = M["CLS"]
        with self.voiceover(
            "Did the boom fatten the builders' margins? A little. <bookmark mark='a'/> Celestica kept "
            f"{100 * cm[2022]:.1f} cents in the dollar in 2022 and {100 * cm[2025]:.1f} in 2025. <bookmark mark='b'/> "
            "Supermicro has swung between about two and nine cents. <bookmark mark='c'/> And Hon Hai's server arm earned "
            f"{100 * S['fii_margin']:.1f} cents of operating income. Better than building phones, but still the bottom of "
            f"the smile. The money in a server goes to the chips inside it: Nvidia, as the last film showed, kept "
            f"{get('nvda.gm'):.0f} cents of gross margin on each dollar it sold."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(ghost(ls, lc, opacity=0.3)))
            vo.wait_until("a")
            self.play(Create(lc), FadeIn(ll[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ls), FadeIn(ll[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(GrowFromCenter(fii), FadeIn(fl))
        self.clear_scene()
