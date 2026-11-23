from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403

JOB_GROUP = {"Manufacturing": "goods", "Construction": "goods", "Mining": "goods", "Utilities": "goods",
             "Retail trade": "trade", "Wholesale trade": "trade", "Transportation": "trade", "Information": "info",
             "Finance, insurance, real estate": "finance", "Professional and business services": "services",
             "Health care and social assistance": "people", "Education (private)": "people",
             "Leisure and hospitality": "people", "Other services": "people", "Government": "government"}


class Jobs(VoiceoverScene):
    def construct(self):
        card(self, 6, "The economy by jobs", "Where do Americans work, and what does each job add?",
             "Chapter six. The economy by jobs.", lit=("unit", "make"))
        self.map()
        self.per_job()
        self.pay()

    def map(self):
        J = R["jobs"]
        tm = viz.treemap([(d["sector"].replace(" and social assistance", "").replace(" and business services",
                                                                                   " services"),
                           d["jobs"], GROUP[JOB_GROUP[d["sector"]]], f"{d['jobs']:.1f}m") for d in J], 11.6, 5.6, 19)
        tm.move_to(DOWN * 0.35)
        order = sorted(range(len(J)), key=lambda i: -J[i]["jobs"])
        head = VGroup(TB(f"{R['jobs_total']:.1f} million", 30, I.ACCENT), T("payroll jobs in the United States, 2025",
                      22, I.TEXT)).arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.35)
        src = source("BLS Current Employment Statistics via FRED, 2025 averages (excludes farms and the self-employed)",
                     corner=DR, size=14)
        with self.voiceover(
            "Now draw the same economy by jobs. <bookmark mark='a'/> In 2025 American employers had 158 million "
            "people on their payrolls. <bookmark mark='b'/> The biggest blocks are government, health care and "
            "professional and business services, each with more than 22 million jobs, then restaurants, hotels and "
            "entertainment with 17 million, and shops with 15. <bookmark mark='c'/> Manufacturing employs 12.6 "
            "million people, about one job in twelve. <bookmark mark='d'/> Compare the two maps. Real estate and "
            "finance are a fifth of the value added and six percent of the jobs; restaurants and hotels are four "
            "percent of the value added and more than ten percent of the jobs."
        ) as vo:
            # one person for each million jobs, coloured by industry, then gathered into the map's blocks
            counts, acc, done = [], 0.0, 0
            for i in order:
                acc += J[i]["jobs"]
                counts.append(int(round(acc)) - done)
                done += counts[-1]
            people, groups = VGroup(), []
            for i, n in zip(order, counts):
                g_ = VGroup(*[draw.person(0.3, color=GROUP[JOB_GROUP[J[i]["sector"]]]) for _ in range(n)])
                groups.append(g_)
                people.add(*g_)
            people.arrange_in_grid(cols=22, buff=(0.14, 0.14)).move_to(DOWN * 0.35)
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(head), LaggedStart(*[FadeIn(p_, scale=0.5) for p_ in people], lag_ratio=0.01),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(*[ReplacementTransform(groups[k], tm[i]) for k, i in enumerate(order[:5])], run_time=2.2)
            vo.wait_until("c")
            self.play(*[ReplacementTransform(groups[k + 5], tm[i]) for k, i in enumerate(order[5:])], run_time=2.2)
            vo.wait_until("d")
            fi = [d["sector"] for d in J].index("Finance, insurance, real estate")
            le = [d["sector"] for d in J].index("Leisure and hospitality")
            self.play(Indicate(tm[fi], color=WHITE, scale_factor=1.05), Indicate(tm[le], color=WHITE, scale_factor=1.05))
        self.clear_scene()

    def per_job(self):
        J = sorted(R["jobs"], key=lambda d: -d["per_job"])
        items = [(d["sector"].replace(" and social assistance", "").replace("Finance, insurance, real estate",
                                                                            "Finance and real estate*"),
                  d["per_job"] / 1e3, GROUP[JOB_GROUP[d["sector"]]], "") for d in J]
        rows = viz.margin_ladder(items, max_value=900, bar_len=6.0, row_h=0.4, size=18, name_w=4.6,
                                 fmt=lambda v: f"${v:,.0f}k")
        rows.move_to(RIGHT * 0.9 + DOWN * 0.25)
        head = T("Value added per payroll job, 2025", 24, I.TEXT).to_edge(UP, buff=0.35)
        note = T("*includes the rent homeowners are counted as paying themselves", 15, I.FAINT).to_corner(DR, buff=0.3)
        src = source("BEA value added / BLS payroll jobs: this film's division", size=14)
        with self.voiceover(
            "Divide one map by the other and you get the value added per job. <bookmark mark='a'/> At the top are "
            "industries where a few people run a great deal of equipment or property: utilities, about 845 thousand "
            "dollars per job, mining, and information, which includes software and telecoms. Real estate and "
            "finance look highest of all, but the homeowners' rent inflates them. <bookmark mark='b'/> At the bottom "
            "are industries where the work is done by people, face to face: health care, about 100 thousand dollars "
            "per job, private education, and restaurants and hotels, 76 thousand. <bookmark mark='c'/> This is not a "
            "measure of how hard anyone works. It is a measure of how much machinery, property and software stands "
            "behind each worker, and of the prices the industry can charge. A nurse's hour cannot be made by a "
            "machine; an hour of electricity can."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(note))
            self.play(LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.04), *[FadeIn(r[1]) for r in rows])
            vo.wait_until("a")
            self.play(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows[:5]], run_time=1.4)
            vo.wait_until("b")
            self.play(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows[5:]], run_time=1.6)
        self.clear_scene()

    def pay(self):
        P = R["pay"]
        LABEL = {"Health care and social assistance": "Education and health care",
                 "Finance, insurance, real estate": "Finance and real estate",
                 "Professional and business services": "Professional and business svcs"}
        items = [(LABEL.get(k, k), v, GROUP[JOB_GROUP[k]], f"value added per job ${va / 1e3:,.0f}k")
                 for k, v, va in P["rows"]]
        rows = viz.margin_ladder(items, max_value=60, bar_len=4.6, row_h=0.4, size=16, name_w=4.1,
                                 fmt=lambda v: f"${v:.2f}")
        rows.move_to(LEFT * 0.3 + DOWN * 0.35)
        head = T("Average hourly pay by industry, 2025", 24, I.TEXT).to_edge(UP, buff=0.35)
        top, bot = P["rows"][0], P["rows"][-1]
        vas = [va for _, _, va in P["rows"]]
        note = VGroup(T(f"pay: {top[1] / bot[1]:.1f} times from bottom to top", 19, I.ACCENT),
                      T(f"value added per job: {max(vas) / min(vas):.0f} times", 19, I.ACCENT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_edge(DOWN, buff=0.4)
        src = source("BLS Current Employment Statistics, average hourly earnings of all employees, via FRED; "
                     "government not published", corner=UR, size=13).shift(DOWN * 0.45)
        with self.voiceover(
            "Does the value a job adds show up in its pay? <bookmark mark='a'/> Partly. In 2025 the average hour "
            f"of work in a private business paid {say_money(P['total'])}. In information and in the utilities, "
            f"about {say_money(top[1])}. In shops, about {say_money(P['rows'][-2][1])}, and in restaurants and "
            f"hotels, {say_money(bot[1])}. <bookmark mark='b'/> But look at the spread. From the lowest-paid "
            f"industry to the highest, pay rises about {top[1] / bot[1]:.1f} times. Value added per job, in the "
            f"previous chart, rose about {max(vas) / min(vas):.0f} times. <bookmark mark='c'/> Pay is set in a "
            "labour market that all industries share: a cashier could become a clerk at the power company, if "
            "hired. So pay varies far less than what a job adds, and the rest of the difference goes somewhere "
            "else. The next chapter follows it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.08), run_time=2.6)
            vo.wait_until("b")
            self.play(FadeIn(note[0]))
            self.play(FadeIn(note[1]))
            vo.wait_until("c")
            self.play(Indicate(note, color=I.ACCENT, scale_factor=1.03))
        self.clear_scene()
