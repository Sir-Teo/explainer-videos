from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403


class Shift(VoiceoverScene):
    def construct(self):
        card(self, 13, "From factories to services", "If America makes more than ever, why do fewer people make it?",
             "Chapter thirteen. From factories to services.", lit=("change",))
        self.jobs()
        self.prices()
        self.why()

    def jobs(self):
        M = R["mfg_jobs"]
        yrs, share, health, jobs = M["years"], M["share"], M["health"], M["jobs"]
        pa = viz.plot_axes((1939, 2025), (0, 40), x_length=6.0, y_length=4.3, xticks=[1939, 1960, 1980, 2000, 2025],
                           yticks=[0, 10, 20, 30, 40], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}%",
                           size=15, ylabel="manufacturing's share of payroll jobs").shift(LEFT * 3.4 + DOWN * 0.4)
        line = VMobject(stroke_color="#F2A65A", stroke_width=3.5).set_points_as_corners(
            [pa.ax.c2p(y, s) for y, s in zip(yrs, share)])
        k43 = yrs.index(1943)
        peak = VGroup(Dot(pa.ax.c2p(1943, share[k43]), color="#F2A65A", radius=0.06),
                      T(f"1943: {share[k43]:.0f}%", 15, "#F2A65A")).arrange(RIGHT, buff=0.1)
        peak.move_to(pa.ax.c2p(1943, share[k43]) + RIGHT * 0.75)
        end = T(f"2025: {share[-1]:.0f}%", 15, "#F2A65A").next_to(pa.ax.c2p(2025, share[-1]), UP, buff=0.1)
        out = M["output"]
        k79 = yrs.index(1979)
        right = VGroup(
            VGroup(TB(f"{jobs[k79]:.1f}m → {jobs[-1]:.1f}m", 30, "#F2A65A"),
                   T("manufacturing jobs, 1979 to 2025", 18, I.TEXT)).arrange(DOWN, buff=0.05),
            VGroup(TB(f"+{100 * (out[2025] / out[1987] - 1):.0f}%", 30, I.PROFIT),
                   T("manufacturing's real output, 1987 to 2025", 18, I.TEXT)).arrange(DOWN, buff=0.05),
            VGroup(TB(f"{health[0]:.1f}m → {health[-1]:.1f}m", 30, "#7BD88F"),
                   T("jobs in education and health care, 1939 to 2025", 18, I.TEXT)).arrange(DOWN, buff=0.05),
        ).arrange(DOWN, buff=0.5).move_to(RIGHT * 3.6 + DOWN * 0.2)
        src = source("BLS Current Employment Statistics and the Federal Reserve's manufacturing output index, via FRED")
        with self.voiceover(
            "Here is the change in people. <bookmark mark='a'/> In 1943, in the middle of the war, almost two "
            "American payroll jobs in five were in manufacturing. In 2025, one in twelve. <bookmark mark='b'/> The "
            "number of factory jobs peaked in 1979, at 19.4 million; in 2025 it was 12.6 million. <bookmark "
            "mark='c'/> Yet the factories did not make less. Their real output, adjusted for prices, was 57 percent "
            "higher in 2025 than in 1987. <bookmark mark='d'/> Meanwhile education and health care grew from 1.4 "
            "million jobs in 1939 to 27 million."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(line), run_time=2.5)
            self.play(FadeIn(peak), FadeIn(end))
            vo.wait_until("b")
            self.play(FadeIn(right[0], shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(right[1], shift=LEFT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(right[2], shift=LEFT * 0.1))
        self.clear_scene()

    def prices(self):
        P = R["prices"]
        ch = P["change"]
        PAY = "Average hourly earnings of production and nonsupervisory employees"
        rows = [("Tuition, school fees and childcare", "Tuition, school fees, childcare"),
                ("Medical care services", "Doctors' and hospitals' services"), ("Rent of primary residence", "Rent"),
                ("Food away from home", "Restaurant meals"), ("Services", "All services"), ("All items", "All prices"),
                ("New vehicles", "New cars"), ("Apparel", "Clothes"), ("Durable goods", "All durable goods"),
                ("Toys", "Toys"), ("Computers, peripherals and smart home assistants", "Computers")]
        sc = 2.1  # screen units per 100%
        x0 = -0.6
        bars = VGroup()
        for k, (key, name) in enumerate(rows):
            v = ch[key]
            y = 2.15 - k * 0.43
            col = "#7BD88F" if v > 1.0 else ("#8B95A7" if v > 0.3 else "#7EC8F5")
            r = Rectangle(width=max(abs(v) * sc, 0.02), height=0.3, fill_color=col, fill_opacity=0.9, stroke_width=0)
            r.move_to(np.array([x0, y, 0]), aligned_edge=LEFT if v >= 0 else RIGHT)
            val = T(f"{100 * v:+.0f}%", 16, col).next_to(r, RIGHT if v >= 0 else LEFT, buff=0.1)
            nm = T(name, 17, I.TEXT)
            if v >= 0:
                nm.move_to(np.array([x0 - 0.15, y, 0]), aligned_edge=RIGHT)
            else:
                nm.next_to(val, LEFT, buff=0.15)
            bars.add(VGroup(nm, r, val))
        axis = Line(np.array([x0, 2.45, 0]), np.array([x0, 2.15 - 10 * 0.43 - 0.25, 0]), color=I.EDGE, stroke_width=1.5)
        pay = ch[PAY]
        px = x0 + pay * sc
        mark = DashedLine(np.array([px, 2.5, 0]), np.array([px, 2.15 - 10 * 0.43 - 0.25, 0]), color=I.ACCENT,
                          stroke_width=2)
        mlab = VGroup(TB(f"hourly pay {100 * pay:+.0f}%", 17, I.ACCENT), T("production workers", 14, I.ACCENT)
                      ).arrange(DOWN, buff=0.03).next_to(mark, UP, buff=0.05)
        head = T(f"Change in prices, {P['y0']} to {P['y1']}", 24, I.TEXT).to_corner(UL, buff=0.4)
        src = source("BLS consumer price indexes (US city average) and average hourly earnings, annual averages, via "
                     "FRED", size=14)
        with self.voiceover(
            f"The prices tell the same story from the other side. <bookmark mark='a'/> Between {P['y0']} and "
            f"{P['y1']}, the pay of an hour of an ordinary worker's time rose {say_pct(pay)}. <bookmark mark='b'/> "
            "The prices of the things that are mostly people's time rose about as fast or faster: school fees and "
            f"childcare {say_pct(ch['Tuition, school fees and childcare'])}, the services of doctors and hospitals "
            f"{say_pct(ch['Medical care services'])}, a meal in a restaurant {say_pct(ch['Food away from home'])}. "
            f"<bookmark mark='c'/> The prices of things made in factories barely moved, or fell: a new car "
            f"{say_pct(ch['New vehicles'])}, clothes about one percent, toys down "
            f"{say_pct(-ch['Toys'])}, computers down {say_pct(-ch['Computers, peripherals and smart home assistants'])}, "
            "because the statisticians count each year's faster, bigger machine as more computer for the money. "
            "<bookmark mark='d'/> So an hour of work buys far more goods than it did, and about the same amount of "
            "care, teaching and cooking. That is why spending, and jobs, flowed towards services, even as factories "
            "made more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(axis))
            vo.wait_until("a")
            self.play(Create(mark), FadeIn(mlab))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars[:6]], lag_ratio=0.15), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.1) for b in bars[6:]], lag_ratio=0.2), run_time=2)
            vo.wait_until("d")
            self.play(Indicate(bars[0], color="#7BD88F", scale_factor=1.03), Indicate(bars[-1], color="#7EC8F5",
                                                                                      scale_factor=1.03))
        self.clear_scene()

    def why(self):
        reasons = [
            ("Machines", ("Factories and farms raised output per worker faster than almost any",
                          "other industry: the same goods need fewer people.")),
            ("Wants", ("As people get richer they spend more of each extra dollar on health,",
                       "education, travel and advice than on more things.")),
            ("Prices", ("An hour of a nurse or a teacher cannot be sped up like a production line,",
                        "so services grow dearer relative to goods: Baumol's cost disease.")),
            ("Trade", ("From 2000, competition from imports, much of it from China,",
                       "closed factories that would otherwise have stayed open.")),
        ]
        rows = VGroup()
        for name, (l1, l2) in reasons:
            body = VGroup(T(l1, 22, I.TEXT), T(l2, 22, I.TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            name_t = TB(name, 26, I.ACCENT)
            name_t.set_width(name_t.width)
            r = VGroup(name_t, body).arrange(RIGHT, buff=0.4, aligned_edge=UP)
            body.shift(RIGHT * (1.9 - name_t.width))
            if r.width > 12.6:
                r.scale_to_fit_width(12.6)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(DOWN * 0.1).align_to(LEFT * 6.2, LEFT)
        head = TB("Why the economy moved from goods to services", 28, I.TEXT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Four forces did this. <bookmark mark='a'/> Machines: factories and farms raised output per worker "
            "faster than almost any other industry, so the same goods need fewer people. <bookmark mark='b'/> Wants: "
            "as people get richer, they spend more of each extra dollar on health, education, travel and advice, and "
            "less on more things. <bookmark mark='c'/> Prices: an hour of a nurse, a teacher or a lawyer cannot be "
            "sped up like a production line, so services keep getting dearer relative to goods, as the prices "
            "just showed. The economist William Baumol called it the cost disease. <bookmark mark='d'/> And trade: from 2000, competition from "
            "imports, much of it from China, closed factories that would otherwise have stayed open. Economists "
            "still argue about how much each force counts; they agree all four are real."
        ) as vo:
            self.play(FadeIn(head))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[i], shift=RIGHT * 0.15), run_time=0.9)
        self.clear_scene()
