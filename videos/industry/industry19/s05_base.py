from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403


class Base(VoiceoverScene):
    def construct(self):
        card(self, 4, "The installed base", "What does a maker earn from every machine still working?",
             "Chapter four. The installed base: every machine a company has sold that is still working, and still "
             "needs parts, service and repairs.", lit=("dollar", "moat"))
        self.otis()
        self.model()
        self.split()
        self.rivals()
        self.lifetime()

    def rivals(self):
        rng = np.random.default_rng(19)
        few = VGroup(*[Dot([x, y, 0], radius=0.05, color=MACHINE) for x, y in zip(rng.uniform(-6.2, -1.4, 60), rng.uniform(-1.8, 1.6, 60))])
        many = VGroup(*[Dot([x, y, 0], radius=0.035, color=SERVICE) for x, y in zip(rng.uniform(0.6, 6.2, 600), rng.uniform(-1.8, 1.6, 600))])
        lf = tx("hundreds offer new elevators", 18, MACHINE, bold=True).move_to([-3.8, 2.3, 0])
        lm = tx("several thousand offer maintenance", 18, SERVICE, bold=True).move_to([3.4, 2.3, 0])
        big = tx("the big four in both: Otis, KONE, Schindler, TK Elevator", 16, GREY_A).to_edge(DOWN, buff=0.75)
        src = source("Otis Worldwide Corporation, Form 10-K 2025 (competition), citing industry estimates", size=12)
        beat(self,
             "The base is not the maker's by right. <bookmark mark='a'/> Otis's report counts hundreds of companies that "
             "install new elevators <bookmark mark='b'/> and several thousand that maintain them, from the other big makers "
             "to small independent firms that service anyone's lifts. <bookmark mark='c'/> Every maintenance contract can "
             "be lost when it ends. Otis's report lists what decides it: price, reputation, delivery, quality, "
             "reliability, and long-term service and product support. The attach rate of Run it is a number each of them "
             "works on every day.",
             base=[src], steps=[[few, lf], [many, lm], big])

    def lifetime(self):
        B = R["base"]
        price = 1.0
        svc = B["lifetime"]
        a = Rectangle(width=1.6, height=1.6, stroke_width=0, fill_color=MACHINE, fill_opacity=0.9).move_to([-2.4, -1.6, 0])
        a.grow = DOWN
        b = Rectangle(width=1.6, height=1.6 * svc, stroke_width=0, fill_color=SERVICE, fill_opacity=0.9)
        b.move_to([0.6, -2.4 + 0.8 * svc, 0])
        b.grow = DOWN
        la = VGroup(tx("the machine", 17, MACHINE, bold=True), tx("1.0", 22, MACHINE, bold=True)).arrange(DOWN, buff=0.05).next_to(a, UP, buff=0.12)
        lb = VGroup(tx(f"{B['life']} years of parts and service", 17, SERVICE, bold=True), tx(f"{svc:.1f}", 22, SERVICE, bold=True)).arrange(DOWN, buff=0.05).next_to(b, UP, buff=0.12)
        base_line = Line([-4.0, -2.4, 0], [2.2, -2.4, 0], stroke_color=GREY_B, stroke_width=2)
        otis = VGroup(tx("Otis, 2025:", 18, GREY_A),
                      tx(f"${B['per_unit']:,.0f}", 34, SERVICE, bold=True),
                      tx("of service sales per lift or", 15, GREY_A), tx("escalator it maintains", 15, GREY_A)).arrange(DOWN, buff=0.08).move_to([4.6, 0.2, 0])
        tag = estimate_tag(f"the Works: service at {100 * B['service_rate']:.0f}% of the price a year for {B['life']} years, undiscounted", size=12)
        beat(self,
             "Look at it from the owner's side. <bookmark mark='a'/> In our model a machine costs one unit to buy. "
             f"<bookmark mark='b'/> Over its {B['life']} years its owner spends {svc:.1f} units more on parts and service: "
             "almost twice the price of the machine. The price on the day of the sale is the smaller part of what the "
             "owner will pay. <bookmark mark='c'/> Otis's service business brought in about "
             f"{B['per_unit']:,.0f} dollars in 2025 for each of the {B['units']:.1f} million lifts and escalators it looks "
             "after.",
             base=[base_line, tag], steps=[[a, la], [b, lb], otis])

    def otis(self):
        B = R["base"]
        o = B["otis"]
        rows = []
        for i, (name, col) in enumerate((("New Equipment", MACHINE), ("Service", SERVICE))):
            sales, op = o[name]
            y = 1.0 - 1.9 * i
            sb = Rectangle(width=6.0 * sales / 9442, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.35).move_to([-2.6 + 3.0 * sales / 9442, y + 0.3, 0])
            pb = Rectangle(width=6.0 * op / 9442 * 3, height=0.5, stroke_width=0, fill_color=col, fill_opacity=1).move_to([-2.6 + 3.0 * op / 9442 * 3, y - 0.35, 0])
            sb.grow = pb.grow = LEFT
            lab = VGroup(tx(name, 20, col, bold=True)).move_to([-4.4, y, 0])
            vs = tx(f"sales ${sales / 1e3:.1f}bn", 16, GREY_A).next_to(sb, RIGHT, buff=0.15)
            vp = tx(f"profit ${op / 1e3:.2f}bn: {100 * op / sales:.1f}%", 16, col, bold=True).next_to(pb, RIGHT, buff=0.15)
            rows.append(VGroup(lab, sb, vs, pb, vp))
        key = tx("profit bars drawn three times larger than sales bars", 13, GREY_B).to_edge(DOWN, buff=0.75)
        q = tx(f"China: over half of Otis's new units, about a fifth of its new-equipment sales", 15, GREY_A).next_to(key, UP, buff=0.15)
        src = source("Otis Worldwide Corporation, Form 10-K 2025: segment results", size=12)
        beat(self,
             "Back to Otis, because it shows the installed base more clearly than anyone. <bookmark mark='a'/> Its new "
             f"equipment business sold {o['New Equipment'][0] / 1e3:.1f} billion dollars of elevators in 2025 and kept "
             f"{100 * o['New Equipment'][1] / o['New Equipment'][0]:.1f} per cent as profit. Over half of its new units "
             "went to China, the industry's largest market, yet they brought only about a fifth of its new-equipment "
             "sales. <bookmark mark='b'/> Its service business "
             f"sold {o['Service'][0] / 1e3:.1f} billion dollars and kept {100 * o['Service'][1] / o['Service'][0]:.0f} per "
             f"cent. Service was {B['sv_share']} per cent of Otis's sales and 91 per cent of its segment profit. Otis "
             "tries to turn every elevator it installs into a maintenance contract, and to win the maintenance of other "
             "makers' elevators too.",
             base=[key, q, src], steps=[rows[0], rows[1]])

    def model(self):
        B = R["base"]
        rows = B["rows"]
        nr = {r["year"]: r["new_rev"] for r in rows}
        sr = {r["year"]: r["svc_rev"] for r in rows}
        ch = line_chart({"new machines": (nr, MACHINE), "parts and service": (sr, SERVICE)}, x=(0, 39), y=(0, 450),
                        xticks=[0, 10, 20, 30, 39], yticks=[0, 100, 200, 300, 400], xfmt=lambda v: f"year {int(v)}",
                        yfmt=lambda v: f"{v:.0f}", ylabel="the Works' maker: revenue a year ($m)", width=9.0, height=4.4,
                        center=(-1.0, -0.45))
        ax = ch.ax
        crash = callout(ax, 18, nr[18], f"a crash year: new sales {100 * (nr[18] / nr[17] - 1):.0f}%", BAD, at=(24, 30))
        tag = estimate_tag(f"the Works: machines work {B['life']} years and bring {100 * B['service_rate']:.0f}% of their price "
                           "a year in parts and service", size=12)
        beat(self,
             "Here is why that matters, in a model maker. <bookmark mark='a'/> Its sales of new machines rise and fall "
             "with the capital-goods cycle, and in one bad year they halve. <bookmark mark='b'/> But every machine it has "
             f"sold works for {B['life']} years and brings in parts and service every year. As the installed base builds "
             "up, that line rises above the new sales, <bookmark mark='c'/> and in the crash year it hardly moves: the "
             "machines already working still wear out.",
             base=[ch.frame, tag], steps=[[ch.lines["new machines"], ch.labels["new machines"]],
                                         [ch.lines["parts and service"], ch.labels["parts and service"]], crash])

    def split(self):
        B = R["base"]
        c = stat_cards([(f"{100 * B['svc_rev_share']:.0f}%", "of the model's revenue from parts and service", SERVICE),
                        (f"{100 * B['svc_profit_share']:.0f}%", "of its profit", SERVICE),
                        (f"{100 * B['new_sw']['worst_fall']:.0f}% / {100 * B['svc_sw']['worst_fall']:.0f}%",
                         "worst year: new sales / service", BAD)], y=0.6, size=42, span=12)
        vs = tx(f"Otis, 2025: service {B['sv_share']}% of sales and 91% of segment profit", 19, GREY_A).move_to([0, -1.4, 0])
        tag = estimate_tag(f"the Works: new machines at a {100 * B['new_margin']:.0f}% margin, service at "
                           f"{100 * B['service_margin']:.0f}%", size=12)
        beat(self,
             "Add it up over the model's mature years. <bookmark mark='a'/> Parts and service bring in "
             f"{100 * B['svc_rev_share']:.0f} per cent of the revenue and {100 * B['svc_profit_share']:.0f} per cent of the "
             f"profit, and in the worst year service fell {-100 * B['svc_sw']['worst_fall']:.0f} per cent while new "
             f"sales fell {-100 * B['new_sw']['worst_fall']:.0f}. <bookmark mark='b'/> Those are close to Otis's real "
             "proportions. The machine is how the customer is won; the installed base is how the company lives.",
             base=[tag], steps=[c, vs])
