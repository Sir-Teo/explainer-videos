from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403


def grid_table(header, rows, col_w=(2.6, 2.4, 2.4), row_h=0.62, font_size=28, colors=None):
    """A small table: ``header`` cells, then ``rows`` of cells (TeX strings).  ``colors``: per row."""
    g = VGroup()
    cells = []
    y = 0.0
    for r, row in enumerate([header] + rows):
        x = 0.0
        line = []
        for c, (text, w) in enumerate(zip(row, col_w)):
            col = GREY_B if r == 0 else ((colors[r - 1] if colors else WHITE) if c == 0 else WHITE)
            t = label(text, font_size=font_size - (4 if r == 0 else 0), color=col)
            t.move_to([x + w / 2, y, 0])
            g.add(t)
            line.append(t)
            x += w
        cells.append(line)
        y -= row_h
    total_w = sum(col_w)
    g.add(Line([0, -row_h / 2, 0], [total_w, -row_h / 2, 0], color=GREY_D, stroke_width=1.5))
    g.cells = cells
    return g


class Friday(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Two people: comparative advantage", r"Why would someone who is better at everything trade "
             r"with someone who is worse at everything?", "Chapter three. Two people: comparative advantage.",
             lit={1817: r"Ricardo's \emph{Principles}"}, scale=("person",), horizon=("a day",))
        self.arrival()
        self.costs()
        self.trade()
        self.joint()
        self.ricardo()

    # ------------------------------------------------------------------
    def arrival(self):
        r = load("ricardo")
        c, f = r["people"]
        a = islander("crusoe", 0.9, name=True)
        b = islander("friday", 0.9, name=True)
        VGroup(a, b).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.4)
        tab = grid_table([r"", r"hours per fish", r"hours per coconut"],
                         [[r"Crusoe", rf"{c['hours_per_fish']:g}", rf"{c['hours_per_coconut']:g}"],
                          [r"Friday", rf"{f['hours_per_fish']:g}", rf"{f['hours_per_coconut']:g}"]],
                         colors=[CRUSOE, FRIDAY], font_size=32).move_to(DOWN * 0.2)
        tab.move_to(DOWN * 0.4)
        ab = label(r"Crusoe is faster at both: \ an absolute advantage in each", font_size=28, color=GREY_A)
        ab.next_to(tab, DOWN, buff=0.6)
        note_ = label(r"12 hours a day each; \ straight-line technologies, so the arithmetic is exact", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        tag = illustrative_tag(r"illustrative numbers", corner=DR, font_size=17)
        with self.voiceover(
            "Now a second person comes ashore. Call him Friday. <bookmark mark='a'/> To keep the arithmetic exact, "
            "give each of them a fixed number of hours per fish and per coconut, and twelve hours in the day. "
            f"Crusoe needs {c['hours_per_fish']:g} hour per fish and {c['hours_per_coconut']:g} per coconut. "
            f"Friday is slower at both: {f['hours_per_fish']:g} hours per fish, {f['hours_per_coconut']:g} per "
            "coconut. <bookmark mark='b'/> So Crusoe is better at everything. If anyone should do without the "
            "other, surely it's Crusoe. What could he possibly gain from Friday?"
        ) as vo:
            self.play(FadeIn(a, shift=RIGHT * 0.2), FadeIn(b, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(note_), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(ab, shift=UP * 0.1))
        self.clear_scene()

    def costs(self):
        r = load("ricardo")
        c, f = r["people"]
        tab = grid_table([r"", r"a fish costs", r"a coconut costs"],
                         [[r"Crusoe", rf"{c['oc_fish']:.2g} coconut", rf"{c['oc_coconut']:.3g} fish"],
                          [r"Friday", rf"{f['oc_fish']:.2g} coconut", rf"{f['oc_coconut']:.3g} fish"]],
                         col_w=(2.4, 3.2, 3.2), colors=[CRUSOE, FRIDAY], font_size=32).move_to(UP * 0.6)
        tab.move_to(UP * 0.8)
        ring_f = SurroundingRectangle(tab.cells[1][1], color=CRUSOE, buff=0.12, corner_radius=0.08)
        ring_c = SurroundingRectangle(tab.cells[2][2], color=FRIDAY, buff=0.12, corner_radius=0.08)
        why_ = MathTex(r"\text{a fish costs}", r"=", r"\frac{\text{hours per fish}}{\text{hours per coconut}}",
                       r"\ \text{coconuts}", font_size=34).to_edge(UP, buff=0.5)
        verdict = VGroup(label(r"Crusoe gives up less to catch a fish", font_size=28, color=CRUSOE),
                         label(r"Friday gives up less to gather a coconut", font_size=28, color=FRIDAY),
                         label(r"a comparative advantage each: \ in what costs them least", font_size=28,
                               color=E.ACCENT)).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.6)
        with self.voiceover(
            "The answer is in what things cost each of them, and cost means what Crusoe learned alone: what you "
            "give up. <bookmark mark='a'/> An hour spent catching a fish is an hour not spent gathering coconuts. "
            "So a fish costs the hours per fish divided by the hours per coconut, in coconuts. "
            f"<bookmark mark='b'/> For Crusoe, a fish costs {c['oc_fish']:.1f} of a coconut. For Friday it costs "
            f"{f['oc_fish']:.1f}. And turn it around: a coconut costs Crusoe {c['oc_coconut']:g} fish, but Friday "
            f"only {f['oc_coconut']:g}. <bookmark mark='c'/> Crusoe is faster at both, but he isn't cheaper at "
            "both. He is cheaper at fish; Friday is cheaper at coconuts. That's called comparative advantage, and "
            "it's the one thing that matters for trade. Nobody can have a comparative advantage in everything."
        ) as vo:
            self.play(*[FadeIn(x) for x in tab.cells[0]], FadeIn(tab[-1]),
                      *[FadeIn(x) for x in tab.cells[1][:1] + tab.cells[2][:1]])
            vo.wait_until("a")
            self.play(Write(why_))
            vo.wait_until("b")
            self.play(FadeIn(tab.cells[1][1]), FadeIn(tab.cells[2][1]))
            self.play(FadeIn(tab.cells[1][2]), FadeIn(tab.cells[2][2]))
            vo.wait_until("c")
            self.play(Create(ring_f), Create(ring_c))
            self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.1) for v in verdict], lag_ratio=0.5), run_time=2.5)
        self.clear_scene()

    def trade(self):
        r = load("ricardo")
        c, f = r["people"]
        axs, people = [], [c, f]
        for k, (p, col) in enumerate(zip(people, (CRUSOE, FRIDAY))):
            a = axes([0, 13], [0, 6.5], x_length=5.0, y_length=3.6, xticks=[0, 4, 8, 12], yticks=[0, 2, 4, 6],
                     xlabel=r"fish", font_size=18, center=[-3.4 + 6.8 * k, -0.6, 0])
            line = Line(a.ax.c2p(0, p["max_coconuts"]), a.ax.c2p(p["max_fish"], 0), color=col, stroke_width=4)
            name = label(p["name"], font_size=28, color=col).next_to(a.ax, UP, buff=0.3)
            yl = label(r"coconuts", font_size=18, color=GREY_A).next_to(a.ax, UP, buff=0.05).align_to(a.ax, LEFT)
            alone = Dot(a.ax.c2p(p["alone"]["fish"], p["alone"]["coconuts"]), radius=0.08, color=GREY_A)
            after = Dot(a.ax.c2p(p["trade"]["fish"], p["trade"]["coconuts"]), radius=0.1, color=E.ACCENT)
            make = Dot(a.ax.c2p(p["makes"]["fish"], p["makes"]["coconuts"]), radius=0.08, color=col)
            arrow = Arrow(make.get_center(), after.get_center(), buff=0.1, color=E.ACCENT, stroke_width=3,
                          max_tip_length_to_length_ratio=0.12)
            g = VGroup(a, line, name, yl)
            g.alone, g.after, g.make, g.arrow, g.ax = alone, after, make, arrow, a
            axs.append(g)
        at = [label(rf"alone: \ {p['alone']['fish']:.1f} fish, \ {p['alone']['coconuts']:.2f} coconuts",
                    font_size=20, color=GREY_A).next_to(g.ax, DOWN, buff=0.5) for p, g in zip(people, axs)]
        tt = [label(rf"after trade: \ {p['trade']['fish']:.1f} fish, \ {p['trade']['coconuts']:.2f} coconuts",
                    font_size=20, color=E.ACCENT).next_to(a_, DOWN, buff=0.1) for p, a_ in zip(people, at)]
        price = r["price"]
        lo, hi = r["band"]
        band = VGroup(label(rf"the price of a fish: \ {price:.1f} coconut", font_size=30, color=E.ACCENT),
                      label(rf"between Crusoe's cost, {lo:.1f}, \ and Friday's, {hi:.1f}", font_size=22,
                            color=GREY_A)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.3).shift(LEFT * 1.5)
        sold = c["makes"]["fish"] - c["trade"]["fish"]
        tag = agora_tag(r"computed: Agora, the competitive equilibrium of the two", corner=UR, font_size=16)
        gc = c["trade"]["coconuts"] - c["alone"]["coconuts"]
        gf = f["trade"]["fish"] - f["alone"]["fish"]
        with self.voiceover(
            "Here are their two frontiers, straight lines now. <bookmark mark='a'/> Alone, suppose each of them "
            "spends sixty percent of the day fishing. Crusoe gets "
            f"{c['alone']['fish']:.1f} fish and {c['alone']['coconuts']:.1f} coconuts; Friday gets "
            f"{f['alone']['fish']:.1f} fish and {f['alone']['coconuts']:.2f} coconuts. <bookmark mark='b'/> Now "
            f"let each do only what he's cheapest at. Crusoe fishes all day: {c['makes']['fish']:.0f} fish. "
            f"Friday gathers all day: {f['makes']['coconuts']:.1f} coconuts. <bookmark mark='c'/> And let them "
            "trade, at whatever price makes the fish Crusoe wants to sell equal to the fish Friday wants to buy. "
            f"Agora solves for it: {price:.1f} of a coconut per fish. It has to lie between their two costs, "
            f"{lo:.1f} and {hi:.1f}, or one of them would rather make his own. <bookmark mark='d'/> Crusoe sells "
            f"{sold:.1f} fish for {sold * price:.2f} coconuts. <bookmark mark='e'/> He ends up with as many fish "
            f"as before, and {gc:.2f} of a coconut more. Friday ends up with as many coconuts as before, and "
            f"{gf:.1f} fish more. Each of them is now living outside his own frontier, at a point he could never "
            "reach alone."
        ) as vo:
            self.play(*[FadeIn(g) for g in axs], FadeIn(tag))
            vo.wait_until("a")
            self.play(*[FadeIn(g.alone, scale=0.5) for g in axs], *[FadeIn(x) for x in at])
            vo.wait_until("b")
            self.play(*[FadeIn(g.make, scale=0.5) for g in axs])
            vo.wait_until("c")
            self.play(FadeIn(band, shift=DOWN * 0.1))
            vo.wait_until("d")
            self.play(*[GrowArrow(g.arrow) for g in axs], *[FadeIn(g.after, scale=0.5) for g in axs])
            vo.wait_until("e")
            self.play(*[FadeIn(x) for x in tt], *[Flash(g.after, color=E.ACCENT) for g in axs])
        self.clear_scene()

    def joint(self):
        r = load("ricardo")
        corners = r["joint"]
        ax = axes([0, 19], [0, 11.5], x_length=6.8, y_length=4.8, xticks=[0, 6, 12, 18], yticks=[0, 4, 8],
                  xlabel=r"fish, both together", font_size=20, center=[-2.6, -0.4, 0])
        yl = label(r"coconuts, both together", font_size=20, color=GREY_A).next_to(ax.ax, UP, buff=0.15).align_to(
            ax.ax, LEFT)
        poly = VMobject(stroke_color=E.ACCENT, stroke_width=4)
        poly.set_points_as_corners([ax.ax.c2p(*corners[0]), ax.ax.c2p(*corners[1]), ax.ax.c2p(*corners[2])])
        ta, tt = r["total_alone"], r["total_trade"]
        p_alone = Dot(ax.ax.c2p(ta["fish"], ta["coconuts"]), radius=0.09, color=GREY_A)
        p_trade = Dot(ax.ax.c2p(tt["fish"], tt["coconuts"]), radius=0.11, color=E.ACCENT)
        la = label(rf"alone: \ {ta['fish']:.1f} fish, \ {ta['coconuts']:.2f} coconuts", font_size=22,
                   color=GREY_A).next_to(p_alone, LEFT, buff=0.15).shift(DOWN * 0.2)
        lt = label(rf"specialized: \ {tt['fish']:.0f} fish, \ {tt['coconuts']:.1f} coconuts", font_size=22,
                   color=E.ACCENT).next_to(p_trade, UR, buff=0.1)
        kink = label(r"the kink: \ each makes only his cheapest good", font_size=22, color=GREY_B)
        kink.next_to(p_trade, RIGHT, buff=0.3).shift(DOWN * 0.6)
        side = VGroup(
            label(r"more of both, \ from the same hours", font_size=28, color=E.ACCENT),
            label(r"nobody worked harder", font_size=24, color=GREY_A),
            label(r"nobody knew more", font_size=24, color=GREY_A),
            label(r"the gain is the trade itself", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.4, 1.0, 0])
        with self.voiceover(
            "Put the two of them together. <bookmark mark='a'/> Their joint frontier has a kink in it: start with "
            "both gathering coconuts, and move the person with the cheaper fish to fishing first. That's Crusoe, "
            "until he's fishing all day, and only then Friday. <bookmark mark='b'/> Alone, their totals were "
            f"{ta['fish']:.1f} fish and {ta['coconuts']:.2f} coconuts, a point inside the frontier. "
            "<bookmark mark='c'/> Specialized, it's "
            f"{tt['fish']:.0f} fish and {tt['coconuts']:.1f} coconuts, right on the kink: more of both, from the "
            "same twenty-four hours. <bookmark mark='d'/> Nobody worked harder, and nobody learned anything. The "
            "extra food comes from the trade itself, from each doing what costs him least."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(poly), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(p_alone, scale=0.5), FadeIn(la))
            vo.wait_until("c")
            self.play(FadeIn(p_trade, scale=0.5), FadeIn(lt), FadeIn(kink))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.1) for s in side], lag_ratio=0.4), run_time=2.5)
        self.clear_scene()

    def ricardo(self):
        r = load("ricardo")["ricardo"]
        eng, por = r["england"], r["portugal"]
        hc = history_card(1817, r"David Ricardo, \emph{On the Principles of Political Economy and Taxation}",
                          r"chapter 7, \ ``On Foreign Trade''", color=E.ACCENT, width=7.4, font_size=26)
        hc.to_edge(UP, buff=0.4)
        tab = grid_table([r"", r"cloth", r"wine"],
                         [[r"England", rf"{eng['cloth']}", rf"{eng['wine']}"],
                          [r"Portugal", rf"{por['cloth']}", rf"{por['wine']}"]],
                         col_w=(2.8, 2.0, 2.0), colors=[CLOTH, WINE], font_size=32)
        tab.next_to(hc, DOWN, buff=0.5)
        unit = label(r"men working for a year to make one unit", font_size=22, color=GREY_B).next_to(tab, DOWN,
                                                                                                    buff=0.2)
        concl = VGroup(
            label(r"Portugal is better at both, \ and still buys English cloth", font_size=28, color=WHITE),
            label(r"each country gains; \ inside each country, some lose (Part 35)", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(unit, DOWN, buff=0.5)
        src = published_tag(tables.RICARDO_1817.tag, corner=DL, font_size=18)
        with self.voiceover(
            "This is the argument David Ricardo published in 1817, with countries instead of castaways. "
            f"<bookmark mark='a'/> In his example, England needs the labour of {eng['cloth']} men for a year to "
            f"make a quantity of cloth, and {eng['wine']} to make a quantity of wine. Portugal needs "
            f"{por['cloth']} and {por['wine']}. Portugal is better at both. <bookmark mark='b'/> But wine costs "
            "Portugal less cloth than it costs England, so Portugal makes wine, England makes cloth, and they "
            "trade. Both have more. <bookmark mark='c'/> It's one of the few ideas in the social sciences that is "
            "both true and surprising, and it's the foundation of the theory of trade in Part thirty-five. That "
            "part also covers what this simple version leaves out: inside each country, the people who used to "
            "make the imported good can lose, even when the country gains."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(unit))
            vo.wait_until("b")
            self.play(FadeIn(concl[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(concl[1], shift=UP * 0.1))
        self.clear_scene()
