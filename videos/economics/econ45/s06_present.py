from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Present(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Present bias", r"Why do plans made for tomorrow fail tomorrow?",
             "Chapter five. Present bias.",
             lit={1968: r"Phelps and Pollak", 1997: r"Laibson", 1999: r"O'Donoghue and Rabin"},
             scale=("person",), horizon=("a day", "a year"))
        self.curves()
        self.reversal()
        self.naifs()
        self.contract()

    def curves(self):
        t = np.arange(0, 31)
        beta, delta = 0.7, 0.99
        exp_ = delta ** t
        qh = np.where(t == 0, 1.0, beta * delta ** t)
        ax = plane([0, 30], [0, 1.05], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"days from now",
                   ylabel=r"weight on a reward", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        e_ln = path(ax, t, exp_, TC, 3.0, smooth=False)
        q_dots = VGroup(*[dot(ax, a, b, NAIF, 0.06) for a, b in zip(t, qh)])
        q_ln = path(ax, t[1:], qh[1:], NAIF, 3.0, smooth=False)
        drop = Arrow(ax.ax.c2p(0.3, 0.98), ax.ax.c2p(0.9, beta * delta + 0.02), buff=0.02, color=LOSS,
                     stroke_width=3, max_tip_length_to_length_ratio=0.25)
        eq = MathTex(r"U_0 = u_0 + \beta \sum_{t \ge 1} \delta^{t} u_t", font_size=38, color=THEORY)
        side = VGroup(
            eq,
            label(r"grey: \ exponential, \\ $\delta^t$ (Part 7)", font_size=18, color=TC),
            label(rf"pink: \ $\beta\,\delta^t$, \ with \\ $\beta$ = {beta}: \ everything \\ after today is cut",
                  font_size=18, color=NAIF),
            label(r"the drop is between \\ now and later, \ not \\ between later and later", font_size=18,
                  color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.PRESENT_BIAS.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Part seven discounted the future at a steady rate: each day further away is worth the same fraction "
            "less. <bookmark mark='a'/> That is the grey curve. <bookmark mark='b'/> Present bias adds one number. "
            "Everything that is not today is multiplied by beta, less than one, and after that the steady rate "
            "applies. The formula is due to Edmund Phelps and Robert Pollak, and David Laibson brought it into "
            "economics in 1997. <bookmark mark='c'/> The whole difference is a drop between now and everything else. "
            "Between next Tuesday and next Wednesday, nothing special happens. Between today and tomorrow, a great "
            "deal does."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(eq), run_time=1.2)
            vo.wait_until("a")
            self.play(Create(e_ln), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(q_ln), FadeIn(q_dots), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(GrowArrow(drop), FadeIn(side[3]))
        self.clear_scene()

    def reversal(self):
        beta, delta = 0.7, 0.999
        now = (100.0, beta * delta * 110.0)
        later = (beta * delta ** 365 * 100.0, beta * delta ** 366 * 110.0)
        rows = VGroup()
        for i, (when, a, b, pick) in enumerate(((r"today, \ or tomorrow?", *now, 0),
                                                 (r"in a year, \ or a year and a day?", *later, 1))):
            y = 1.0 - 1.9 * i
            q = label(when, font_size=24, color=WHITE).move_to(np.array([-4.2, y, 0]))
            opts = VGroup()
            for j, (amt, val) in enumerate(((100, a), (110, b))):
                col = GAIN if j == pick else GREY_B
                box = RoundedRectangle(width=2.6, height=1.15, corner_radius=0.12, stroke_color=col,
                                       stroke_width=2.6 if j == pick else 1.6, fill_color="#141821", fill_opacity=1)
                t1 = label(rf"\${amt}", font_size=28, color=col).move_to(box.get_center() + UP * 0.2)
                t2 = label(rf"feels like {val:.0f}", font_size=17, color=GREY_A).next_to(t1, DOWN, buff=0.1)
                opts.add(VGroup(box, t1, t2).move_to(np.array([0.2 + 3.0 * j, y, 0])))
            rows.add(VGroup(q, opts))
        head = label(rf"the same choice, \ seen from today \ ($\beta$ = {beta}, \ $\delta$ = {delta} a day)",
                     font_size=24, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(r"plan for patience, \ then switch when the day comes: \ a preference reversal", font_size=22,
                     color=LOSS).to_edge(DOWN, buff=0.7)
        tag = published_tag(tables.PRESENT_BIAS.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The drop makes plans unstable. <bookmark mark='a'/> Offer a hundred dollars today or a hundred and "
            f"ten tomorrow. Tomorrow's money is cut by beta, so the hundred and ten feels like {now[1]:.0f}: take "
            "the hundred today. <bookmark mark='b'/> Now offer the same pair a year from now: a hundred in a year, "
            "or a hundred and ten in a year and a day. Both are in the future, both are cut by beta, and the extra "
            "ten dollars wins. <bookmark mark='c'/> So today you plan to wait for the hundred and ten. A year from "
            "now, the day arrives, the first option becomes today, and you take the hundred. Your plan and your "
            "choice disagree, and they will disagree every time. The gym member signs up as the planner and shows "
            "up, or not, as the chooser."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0][0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def naifs(self):
        O = load("odr")
        cols = {"tc": TC, "naif": NAIF, "soph": SOPH}
        names = {"tc": r"Part 5's agent", "naif": r"the naif", "soph": r"the sophisticate"}
        blocks = VGroup()
        for b_i, (key, title, unit) in enumerate((("cost", r"a report: \ the cost is paid the week it is written",
                                                   r"cost"),
                                                  ("reward", r"a film: \ the pleasure comes the week it is seen",
                                                   r"pleasure"))):
            R = O[key]
            y0 = 1.6 - 3.0 * b_i
            hd = label(title, font_size=21, color=E.ACCENT).move_to(np.array([-0.5, y0 + 0.55, 0]))
            weeks = VGroup()
            for w, v in enumerate(R["values"]):
                box = RoundedRectangle(width=1.7, height=0.75, corner_radius=0.1, stroke_color=GREY_B, stroke_width=1.6,
                                       fill_color="#141821", fill_opacity=1)
                t = label(rf"week {w + 1}: \ {unit} {v:.0f}", font_size=15, color=WHITE).move_to(box)
                weeks.add(VGroup(box, t))
            weeks.arrange(RIGHT, buff=0.2).move_to(np.array([-1.6, y0 - 0.15, 0]))
            who = VGroup()
            for j, k in enumerate(("tc", "naif", "soph")):
                wk = R[k] - 1
                d = Dot(weeks[wk].get_bottom() + DOWN * (0.18 + 0.22 * j), radius=0.08, color=cols[k])
                who.add(d)
            legend = VGroup(*[label(rf"{names[k]}: \ week {R[k]}", font_size=17, color=cols[k])
                              for k in ("tc", "naif", "soph")]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            legend.next_to(weeks, RIGHT, buff=0.5)
            blocks.add(VGroup(hd, weeks, who, legend))
        tag = published_tag(tables.PRESENT_BIAS.tag + r"; \ $\beta = 1/2$", corner=DR, font_size=11)
        rc, rr = O["cost"], O["reward"]
        with self.voiceover(
            "Ted O'Donoghue and Matthew Rabin asked what happens when people do, or do not, know they are present "
            "biased. Take a report due within four weeks, with beta one half. <bookmark mark='a'/> Writing it costs "
            "3 this week, then 5, 8 and 13 as other work piles up. <bookmark mark='b'/> Part five's agent writes it "
            f"in week {rc['tc']}. The naif, sure that a later self will do it, keeps postponing to a week that "
            f"looks cheap from today, and writes it in week {rc['naif']}, at the worst cost. The sophisticate "
            "knows the week-three self would also postpone, so week two is the last chance before the worst week, "
            f"and writes it in week {rc['soph']}. Knowing your bias helps. <bookmark mark='c'/> Now a pleasure "
            "instead: a film, better each week, 3, 5, 8, 13. <bookmark mark='d'/> Part five's agent waits for the "
            f"best, week {rr['tc']}. The naif gives in early, in week {rr['naif']}. The sophisticate, expecting to "
            f"give in anyway, gives in in week {rr['soph']}. Knowing your bias, with pleasures, can make it worse."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(blocks[0][0]), FadeIn(blocks[0][1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(w, scale_factor=1.06) for w in blocks[0][1]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in blocks[0][2]], lag_ratio=0.4),
                      FadeIn(blocks[0][3]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(blocks[1][0]), FadeIn(blocks[1][1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in blocks[1][2]], lag_ratio=0.4),
                      FadeIn(blocks[1][3]), run_time=2.0)
        self.clear_scene()

    def contract(self):
        K = load("contract")
        rows = [(r"naif, \ monopoly", K["naif_monopoly"], NAIF), (r"sophisticate, \ monopoly", K["soph_monopoly"],
                                                                     SOPH),
                (r"naif, \ competition", K["naif_competition"], NAIF),
                (r"sophisticate, \ competition", K["soph_competition"], SOPH)]
        tbl = VGroup()
        hdr = VGroup(*[label(t, font_size=18, color=GREY_A) for t in (r"member, \ market", r"price of a visit",
                                                                       r"monthly fee", r"member's real gain")])
        tbl.add(hdr)
        for nm, r, col in rows:
            tbl.add(VGroup(label(nm, font_size=19, color=col), label(dollars(r["p"]), font_size=19, color=WHITE),
                           label(dollars(r["F"]), font_size=19, color=WHITE),
                           label(dollars(r["realized_surplus"]), font_size=19,
                                 color=LOSS if r["realized_surplus"] < 0 else GAIN)))
        for row in tbl:
            for j, c in enumerate(row):
                c.move_to(np.array([-4.3 + 3.0 * j, 0, 0]))
        tbl.arrange(DOWN, buff=0.38).move_to(DOWN * 0.2)
        for row in tbl:
            for j, c in enumerate(row):
                c.set_x(-4.3 + 3.0 * j)
        head = label(rf"the contract a gym designs \ (a visit costs it \${K['m']:.0f}; \ $\beta$ = {K['beta']})",
                     font_size=24, color=E.ACCENT).to_edge(UP, buff=0.5)
        eq = MathTex(r"p^{*} = m - (1 - \beta)\, b", font_size=34, color=THEORY).next_to(head, DOWN, buff=0.3)
        foot = label(r"a gym cannot pay people to come, \ so the price of a visit stops at zero, \ and the fee carries "
                     r"everything", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(tables.PRESENT_BIAS.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Now be the gym. What contract should you offer a present-biased member? <bookmark mark='a'/> Stefano "
            "DellaVigna and Ulrike Malmendier worked it out in 2004. For a good whose costs come now and benefits "
            "later, the profit-maximizing price of a visit is below what a visit costs the gym, by the share of the "
            "benefit the member's present bias throws away. <bookmark mark='b'/> On the Island, a visit costs the "
            f"gym {K['m']:.0f} dollars, and the best price is {say_num(K['naif_monopoly']['p'], 2)}. Below zero. "
            "The fee carries the profit. <bookmark mark='c'/> A monopoly gym charges the naif a higher fee than the "
            "sophisticate, because the naif expects to go more often, and leaves the naif worse off than staying "
            f"home, by {money_words(-K['naif_monopoly']['realized_surplus'])}. <bookmark mark='d'/> Competition "
            "returns the fee to cost for both. The per-visit price stays below cost: for a present-biased member, "
            "that helps, a little commitment sold with the membership. <bookmark mark='e'/> Real gyms cannot pay "
            "people to come, so the price of a visit stops at zero: a flat fee with free visits, the contract of the "
            "hook."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tbl[0]))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(tbl[1]))
            vo.wait_until("c")
            self.play(FadeIn(tbl[2]), Indicate(tbl[1][3], color=WHITE))
            vo.wait_until("d")
            self.play(FadeIn(tbl[3]), FadeIn(tbl[4]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
