from __future__ import annotations

from videos.industry.industry34.common import *  # noqa: F403


class Labour(VoiceoverScene):
    def construct(self):
        card(self, 6, "A third of every dollar", "What happens to a restaurant when wages rise?",
             "Chapter six. A third of every dollar. Labour is the cost a restaurant controls most directly, and the one that "
             "has risen fastest.", lit=("dollar", "change"))
        self.wages()
        self.shares()
        self.rota()
        self.works()

    def wages(self):
        T = R["traffic"]
        A, Mn = T["ahe"], T["minwage"]
        ch = line_chart({"average hourly pay, leisure and hospitality": (A, LABC), "federal minimum wage": (Mn, BAD)},
                        x=(2006, 2027), y=(0, 26), xticks=[2006, 2010, 2014, 2018, 2022, 2026], yticks=[0, 5, 10, 15, 20, 25],
                        xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}", ylabel="dollars an hour",
                        width=8.2, height=4.3, center=(-1.6, -0.45), nudge={"federal minimum wage": -0.2})
        a0, a1 = A[min(A)], A[max(A)]
        k19 = near(A, 2019.96)
        src = source("BLS, average hourly earnings of all employees in leisure and hospitality; Department of Labor, federal minimum wage; via FRED", size=12)
        beat(self,
             "<bookmark mark='a'/> The federal minimum wage has been 7.25 dollars an hour since 2009. <bookmark mark='b'/> But "
             f"the average hourly pay of workers in hotels, restaurants and leisure rose from {a0:.2f} dollars in 2006 to "
             f"{A[k19]:.2f} at the end of 2019 and {a1:.2f} in 2026: up {100 * (a1 / A[k19] - 1):.0f} per cent in under seven "
             "years. In this series' reading, restaurants compete for the same workers as warehouses and shops, and the "
             "federal floor stopped mattering long ago.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["federal minimum wage"], ch.labels["federal minimum wage"]),
                                         VGroup(ch.lines["average hourly pay, leisure and hospitality"], ch.labels["average hourly pay, leisure and hospitality"])])

    def shares(self):
        Un = R["unit"]
        MC = "McDonald's company stores"
        items = [(n, 100 * Un[n]["labour"], c, f"{100 * Un[n]['labour']:.0f}c") for n, c in
                 (("McDonald's company stores", FR), ("Chipotle", OP), ("Darden", FULL))]
        rows = hbars(items, max_value=40, x0=-0.2, top=1.2, row=1.1, length=6.4, size=18, bar_h=0.55)
        hd = tx("Labour, cents per dollar of restaurant sales", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        crew = draw.crowd(12, h=0.45, color=LABC, cols=12).move_to([0, -2.1, 0])
        src = source("McDonald's and Chipotle, Forms 10-K for 2025; Darden, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "<bookmark mark='a'/> At McDonald's own restaurants, crew and managers cost "
             f"{100 * Un[MC]['labour']:.0f} cents of each dollar of sales. "
             f"<bookmark mark='b'/> At Chipotle, {100 * Un['Chipotle']['labour']:.0f}. <bookmark mark='c'/> At Darden's sit-down "
             f"restaurants, with waiters and cooks, {100 * Un['Darden']['labour']:.0f}: the largest single cost. A restaurant "
             "can buy cheaper ingredients only so far; the hours on the rota are where the margin is won or lost.",
             base=[rows.axis, hd, crew, src], steps=[rows[0], rows[1], rows[2]])

    def works(self):
        U = R["run"]
        from explainer.industry.works import franchise as fw
        base = fw.Store(sales=U["auv"], food=U["store"]["food"], labour=U["store"]["labour"], labour_fixed=U["store"]["fixed"], fees=U["take"],
                        ad=U["store"]["ad"], other=U["store"]["other"], delivery=U["store"]["delivery"], commission=U["store"]["commission"],
                        invest=U["store"]["invest"])
        ws = [round(1.0 + 0.025 * i, 3) for i in range(0, 13)]
        prof = {100 * (w - 1): base.with_(wage=w).year()["profit"] / 1e3 for w in ws}
        var = base.fees + base.ad + base.other + base.delivery * base.commission
        pr = {100 * (w - 1): (base.with_(wage=w).year()["profit"] + base.sales * (w - 1) * base.labour * (1 - var)) / 1e3 for w in ws}
        ch = line_chart({"prices unchanged": (prof, BAD), "prices raised to cover the wage rise": (pr, GOOD)}, x=(0, 30), y=(0, 420),
                        xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[0, 100, 200, 300, 400], xfmt=lambda v: f"+{v:.0f}%", yfmt=lambda v: f"${v:.0f}k",
                        ylabel="the Works' franchisee: a year's profit, by wages against today's", width=8.2, height=4.3, center=(-1.6, -0.45),
                        nudge={"prices unchanged": -0.2})
        tag = estimate_tag("the Works: prices raised by the wage rise times labour's share of sales; customers assumed not to leave", size=12)
        w20 = prof[near(prof, 20)]
        beat(self,
             "Back to the Works' franchisee. <bookmark mark='a'/> If wages rise twenty per cent and prices stay the same, "
             f"profit falls from {prof[0]:.0f} thousand dollars to {w20:.0f} thousand. <bookmark mark='b'/> If the owner can "
             f"raise prices enough to cover the extra wages, about {base.labour * 20:.0f} per cent, and customers keep coming, profit "
             f"falls only to {pr[near(pr, 20)]:.0f} thousand, because the franchisor's fees and the apps take their share of the "
             "higher prices too. In this "
             "series' reading, the restaurant prices of the intermission suggest that much of the wage rise was passed on to "
             "diners, and the question for every chain is how much more customers will bear.",
             base=[ch.frame, tag], steps=[VGroup(ch.lines["prices unchanged"], ch.labels["prices unchanged"]),
                                         VGroup(ch.lines["prices raised to cover the wage rise"], ch.labels["prices raised to cover the wage rise"])])

    def rota(self):
        U = R["run"]
        b = U["base"]
        lab = b["labour"]
        fx = U["store"]["fixed"]
        bar = viz.bar_split([("fixed", fx, LABC), ("moves with sales", 1 - fx, GOOD)], 1.0, width=10.0, height=0.9).move_to([0, 0.8, 0])
        l1 = tx(f"${lab * fx / 1e3:.0f}k: managers and the minimum crew", 18, LABC, bold=True).next_to(bar[0], DOWN, buff=0.2)
        l2 = tx(f"${lab * (1 - fx) / 1e3:.0f}k: extra hours at busy times", 18, GOOD, bold=True).next_to(bar[1], DOWN, buff=0.2)
        hd = tx(f"the Works' franchisee: ${lab / 1e6:.2f}m of wages a year", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        crew = draw.crowd(10, h=0.4, color=LABC, cols=10).move_to([0, -2.1, 0])
        tag = estimate_tag("the Works: this series' assumption that 60% of labour is fixed", size=12)
        beat(self,
             f"In the Works, the restaurant pays about {lab / 1e6:.1f} million dollars of wages a year. <bookmark mark='a'/> "
             f"Most of it, about {lab * fx / 1e3:.0f} thousand, is fixed: a manager on every shift and enough crew to open "
             "the doors, even at three in the afternoon. <bookmark mark='b'/> The rest follows the lunch and dinner rush. "
             "Scheduling those extra hours to the minute is the craft of running a restaurant, and it is why a wage rise "
             "hurts most in the quiet hours, when the minimum crew is serving few customers.",
             base=[hd, crew, tag], steps=[VGroup(bar[0], l1), VGroup(bar[1], l2)])
