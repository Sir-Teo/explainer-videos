from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403

FIRST = "#9FB8F2"
LATEST = E.ACCENT


class Revisions(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Revisions: \ the recession nobody saw at first", r"How much do the first numbers change?",
             "Chapter eleven. Revisions: the recession nobody saw at first.", scale=("nation",),
             horizon=("a quarter", "a decade"))
        self.vintages()
        self.scatter()
        self.why()

    # ------------------------------------------------------------------
    def vintages(self):
        r = load("revisions")
        show = r["show"]
        g = r["growth"]
        ax = axes([0, len(show)], [-10, 4], x_length=8.4, y_length=4.8, yticks=[-8, -6, -4, -2, 0, 2, 4],
                  yfmt=lambda v: f"{v:+.0f}\\%".replace("+0", "0").replace("-", "{-}"),
                  ylabel=r"real GDP growth, \ annualized", font_size=20, center=LEFT * 1.8 + DOWN * 0.2)
        a = ax.ax
        zero = Line(a.c2p(0, 0), a.c2p(len(show), 0), color=GREY_B, stroke_width=1.5)
        qlab = VGroup(*[label(q.replace(":", " "), font_size=20, color=GREY_B).next_to(a.c2p(i + 0.5, -10), DOWN,
                                                                                      buff=0.15)
                        for i, q in enumerate(show)])

        def bars_for(v):
            out = VGroup()
            for i, q in enumerate(show):
                val = g[v].get(q)
                if val is None:
                    out.add(Rectangle(width=0.7, height=0.01, stroke_width=0, fill_opacity=0).move_to(a.c2p(i + 0.5, 0)))
                    continue
                lo, hi = a.c2p(i + 0.5, 0), a.c2p(i + 0.5, val)
                col = E.MISS if val < 0 else E.GAIN
                out.add(Rectangle(width=0.7, height=max(abs(hi[1] - lo[1]), 0.01), stroke_width=0, fill_color=col,
                                  fill_opacity=0.85).move_to((lo + hi) / 2))
            return out

        def values_for(v):
            out = VGroup()
            for i, q in enumerate(show):
                val = g[v].get(q)
                if val is None:
                    out.add(VectorizedPoint(a.c2p(i + 0.5, 0)))
                    continue
                t = label(f"{val:+.1f}".replace("-", "{-}"), font_size=20)
                t.next_to(a.c2p(i + 0.5, val), UP if val >= 0 else DOWN, buff=0.08)
                out.add(t)
            return out

        stops = ["2008Q3", "2008Q4", "2008Q4", "2009Q1", "2009Q3", "2011Q3", r["vintages"][-1]]
        names = {"2008Q3": r"August 2008", "2008Q4": r"November 2008", "2009Q1": r"February 2009",
                 "2009Q3": r"August 2009, after a comprehensive revision", "2011Q3": r"August 2011",
                 r["vintages"][-1]: r"today (November 2026)"}
        cur = bars_for(stops[0])
        vals = values_for(stops[0])
        vt = label(rf"vintage: \\ {names[stops[0]]}", font_size=25, color=E.ACCENT).move_to([3.0, 2.6, 0],
                                                                                            aligned_edge=UL)
        nber = label(r"1 December 2008: \\ the NBER dates the start \\ of the recession \\ to December 2007",
                     font_size=22, color=E.MISS).move_to([3.0, 1.1, 0], aligned_edge=UL)
        q4 = label(r"2008 Q4: \\ first $-3.8\%$ \\ today $-8.5\%$", font_size=26, color=E.MISS)
        q4.move_to([3.0, -1.0, 0], aligned_edge=UL)
        tag = data_tag(r"Philadelphia Fed, Real-Time Data Set for Macroeconomists (ROUTPUT), vintages 2008Q3--2026Q4",
                       corner=DL, font_size=15)
        with self.voiceover(
            "Every number in this part is an estimate, and estimates are revised. The Federal Reserve Bank of "
            "Philadelphia keeps every version of America's GDP as it was first published and as it was revised, "
            "quarter by quarter, since 1965. <bookmark mark='a'/> Here is real GDP growth in 2008, as it stood in "
            "August of that year: a slowdown, nothing worse. <bookmark mark='b'/> By November, the third quarter "
            "showed a small fall. <bookmark mark='c'/> On the first of December 2008, the committee that dates "
            "American recessions announced that one had begun a year before, in December 2007. The numbers then "
            "published barely showed it. <bookmark mark='d'/> In February 2009 the first estimate for the fourth "
            "quarter arrived: a fall of 3.8 percent at an annual rate. Then the revisions came. "
            "<bookmark mark='e'/> The first quarter of 2008 turned from growth to decline. <bookmark mark='f'/> "
            "The fourth quarter was revised down, and down again, <bookmark mark='g'/> and it now stands at an "
            "annualized fall of 8.5 percent: more than twice as deep as first reported. The recession everyone "
            "lived through was worse than the numbers said at the time, and policy was made on those numbers."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(qlab), FadeIn(tag), FadeIn(vt))
            vo.wait_until("a")
            self.play(FadeIn(cur), FadeIn(vals))
            for mk, v in zip("bcdefg", stops[1:]):
                vo.wait_until(mk)
                if mk == "c":
                    self.play(FadeIn(nber))
                    continue
                nb, nv = bars_for(v), values_for(v)
                nvt = label(rf"vintage: \\ {names[v]}", font_size=25, color=E.ACCENT).move_to([3.0, 2.6, 0],
                                                                                         aligned_edge=UL)
                self.play(Transform(cur, nb), Transform(vals, nv), Transform(vt, nvt), run_time=1.3)
                if mk == "g":
                    self.play(FadeIn(q4))
        self.clear_scene()

    def scatter(self):
        r = load("revisions")
        fl = r["first_latest"]
        f, l = np.array(fl["first"]), np.array(fl["latest"])
        ax = axes([-12, 18], [-12, 18], x_length=5.6, y_length=5.6, xticks=[-10, -5, 0, 5, 10, 15],
                  yticks=[-10, -5, 0, 5, 10, 15], xlabel=r"first estimate, \ annualized growth",
                  ylabel=r"today's estimate", font_size=20, center=LEFT * 2.8 + DOWN * 0.3)
        a = ax.ax
        diag = DashedLine(a.c2p(-12, -12), a.c2p(18, 18), color=GREY_B, stroke_width=1.5)
        dots = VGroup(*[Dot(a.c2p(x, y), radius=0.04, color=FIRST, fill_opacity=0.7) for x, y in zip(f, l)
                        if -12 < x < 18 and -12 < y < 18])
        flips = VGroup(*[Dot(a.c2p(x, y), radius=0.06, color=E.MISS) for x, y in zip(f, l)
                         if np.sign(x) != np.sign(y) and -12 < x < 18 and -12 < y < 18])
        rows = VGroup(
            label(rf"{r['n']} quarters, \ 1965--2023", font_size=26),
            label(rf"typical revision: \ {r['mean_abs_rev']:.1f} points", font_size=26, color=E.ACCENT),
            label(rf"on average, revised up {r['mean_rev']:.2f} points", font_size=24, color=GREY_A),
            label(rf"sign flipped: \ {r['sign_flips']} quarters", font_size=26, color=E.MISS),
            label(rf"correlation, first and today: \ {r['corr']:.2f}", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6)
        tag = data_tag(r"Philadelphia Fed, Real-Time Data Set: first vintage reporting each quarter, and 2026Q4",
                       corner=DR, font_size=15)
        with self.voiceover(
            "Was 2008 unusual? <bookmark mark='a'/> Here is every quarter from 1965 to 2023: the growth first "
            "published, across, against the growth we believe today, up. If first estimates were final, every "
            "dot would sit on the dashed line. <bookmark mark='b'/> They scatter around it. The typical revision "
            f"is {r['mean_abs_rev']:.1f} percentage points of annualized growth, when growth itself averages "
            "about three, and revisions have more often been upward. <bookmark mark='c'/> In "
            f"{r['sign_flips']} quarters, the first estimate didn't even get the sign right: growth became decline, "
            "or decline growth. <bookmark mark='d'/> Still, the first numbers carry most of the signal: they "
            f"correlate {r['corr']:.2f} with today's."
        ) as vo:
            self.play(FadeIn(ax), Create(diag), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.005), FadeIn(rows[0]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(flips, scale=0.5), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def why(self):
        steps = flow_chain([(r"advance estimate", FIRST), (r"second and third", E.HOUSEHOLDS),
                            (r"annual revisions", E.FIRMS), (r"comprehensive revisions", LATEST)],
                           box_w=2.9, box_h=1.0, buff=0.45, font_size=24,
                           notes=[r"about a month after the quarter: partial data, the rest projected",
                                  r"the next two months: fuller surveys",
                                  r"tax records, annual surveys of businesses",
                                  r"every five years or so: new definitions, the economic census"],
                           note_size=20)
        steps.move_to(UP * 0.9)
        rd = label(r"2013: \ research and development counted as investment, \ back to 1929", font_size=24,
                   color=LATEST).to_edge(DOWN, buff=1.3)
        real = label(r"policy is made on the first numbers: \ real-time data (Part 31)", font_size=26,
                     color=E.ACCENT).to_edge(DOWN, buff=0.55)
        title = label(r"Why the numbers change", font_size=34).to_edge(UP, buff=0.5)
        tag = published_tag(r"BEA, NIPA Handbook, chapter 1", corner=DR, font_size=15)
        with self.voiceover(
            "Why revise? Because the first estimate is a race. <bookmark mark='a'/> The advance estimate comes "
            "about a month after a quarter ends, when much of the data hasn't arrived and the rest is projected "
            "from trends. <bookmark mark='b'/> It's revised in each of the next two months, <bookmark mark='c'/> "
            "then once a year, as tax records and annual surveys of businesses arrive, <bookmark mark='d'/> and "
            "every five years or so in a comprehensive revision, which can change the definitions themselves. "
            "<bookmark mark='e'/> In 2013 the Bureau of Economic Analysis began counting research and development "
            "as investment, and rewrote GDP all the way back to 1929. <bookmark mark='f'/> Central banks and "
            "governments can't wait for the final numbers, so they act on the first ones. Part 31 shows what "
            "that did to policy in the 1970s."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(title))
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                if i:
                    self.play(GrowArrow(steps.arrows[i - 1]), run_time=0.4)
                self.play(FadeIn(steps.boxes[i], shift=RIGHT * 0.2), FadeIn(steps.notes[i]))
            vo.wait_until("e")
            self.play(FadeIn(rd))
            vo.wait_until("f")
            self.play(FadeIn(real))
        self.clear_scene()
