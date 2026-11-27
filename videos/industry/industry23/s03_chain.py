from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403

EXP_COL = {"China": BAD, "Vietnam": GOOD, "Italy": LUX, "Turkey": PRICE, "India": OFF, "Cambodia": FAST}


def _stage(icon, name: str, col) -> VGroup:
    box = RoundedRectangle(corner_radius=0.12, width=1.85, height=1.7, stroke_color=col, stroke_width=2.5)
    icon.scale_to_fit_height(0.75)
    if icon.width > 1.5:
        icon.scale_to_fit_width(1.5)
    icon.move_to(box.get_center() + UP * 0.22)
    return VGroup(box, icon, tx(name, 14, col, bold=True).move_to(box.get_center() + DOWN * 0.55))


def _yarn(col) -> VGroup:
    ball = Circle(radius=0.4, stroke_width=0, fill_color=col, fill_opacity=1)
    lines = VGroup(*[Arc(radius=0.4 * f, start_angle=a, angle=2.2, stroke_color="#0E1117", stroke_width=2)
                     for f, a in ((0.9, 0.3), (0.6, 1.8), (0.35, 3.6))])
    tail = Line([0.35, -0.2, 0], [0.75, -0.45, 0], stroke_color=col, stroke_width=3)
    return VGroup(ball, lines, tail)


def _fabric(col) -> VGroup:
    roll = VGroup(Rectangle(width=1.2, height=0.5, stroke_width=0, fill_color=col, fill_opacity=1),
                  Ellipse(width=0.25, height=0.5, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).shift(LEFT * 0.6))
    return roll


def _fibre(col) -> VGroup:
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=col, fill_opacity=0.9).shift(v)
                    for r, v in ((0.25, LEFT * 0.2), (0.22, RIGHT * 0.2 + UP * 0.1), (0.2, UP * 0.3), (0.18, DOWN * 0.15 + RIGHT * 0.05))])


class Chain(VoiceoverScene):
    def construct(self):
        card(self, 2, "Where clothes are made", "Who makes the clothes, and where?",
             "Chapter two. Where clothes are made. Before the buyer's guess, the long chain that turns a field of cotton or "
             "a barrel of oil into a shirt on a rail.", lit=("make",))
        self.flow()
        self.nike()
        self.shares()
        self.exports()
        self.china()
        self.jobs()

    def flow(self):
        M = R["made"]
        cols = [GOOD, PRICE, FAST, BRANDC, DEPT, LUX]
        stages = VGroup(_stage(_fibre(cols[0]), "fibre", cols[0]), _stage(_yarn(cols[1]), "yarn", cols[1]),
                        _stage(_fabric(cols[2]), "fabric", cols[2]), _stage(draw.sewing_machine(1.4), "cut and sew", cols[3]),
                        _stage(draw.ship(1.4) if hasattr(draw, "ship") else Square(), "ship", cols[4]),
                        _stage(draw.rail(2.4, n=3), "shop", cols[5])).arrange(RIGHT, buff=0.32).move_to([0, 1.0, 0])
        arrows = VGroup(*[Arrow(stages[i].get_right(), stages[i + 1].get_left(), buff=0.04, stroke_width=3, stroke_color=GREY_B,
                                max_tip_length_to_length_ratio=0.4) for i in range(5)])
        lulu = VGroup(tx(f"Lululemon's fabric, 2025: about {get('lulu.fabric.suppliers')} suppliers", 17, FAST, bold=True),
                      tx(f"{get('lulu.taiwan')}% from Taiwan, {get('lulu.fabric.cn')}% from mainland China, "
                         f"{get('lulu.fabric.kr')}% South Korea, {get('lulu.fabric.vn')}% Vietnam", 16, WHITE)
                      ).arrange(DOWN, buff=0.12).move_to([0, -1.7, 0])
        src = source("lululemon athletica inc., Form 10-K for fiscal 2025", size=12)
        beat(self,
             "A shirt passes through many hands before it reaches a shop. <bookmark mark='a'/> First a fibre: cotton from a "
             "farm, or polyester and nylon, which start as oil. <bookmark mark='b'/> The fibre is spun into yarn, "
             "<bookmark mark='c'/> and the yarn knitted or woven into fabric, then dyed. <bookmark mark='d'/> The fabric is "
             "cut into pieces and sewn, still mostly by people at sewing machines, <bookmark mark='e'/> packed, shipped, "
             "<bookmark mark='f'/> and hung on a rail. Each step can happen in a different country. <bookmark mark='g'/> "
             f"Lululemon's 2025 report says its fabric came from about {get('lulu.fabric.suppliers')} suppliers, "
             f"{get('lulu.taiwan')} per cent of it from Taiwan and {get('lulu.fabric.cn')} per cent from mainland China, and "
             "then went to other factories, in other countries, to be sewn.",
             base=[src], steps=[stages[0], [arrows[0], stages[1]], [arrows[1], stages[2]], [arrows[2], stages[3]],
                                [arrows[3], stages[4]], [arrows[4], stages[5]], lulu])

    def nike(self):
        M = R["made"]
        shoe = draw.sneaker(2.0).move_to([-3.4, 2.0, 0])
        shirt = draw.tshirt(1.4, color=SPORT).move_to([3.4, 2.0, 0])
        left = VGroup(tx(f"{M['fw_factories']:.0f}", 46, PRICE, bold=True), tx("footwear factories", 16, GREY_A),
                      tx(f"in {M['fw_countries']:.0f} countries, run by {M['fw_makers']:.0f} contractors", 16, WHITE)
                      ).arrange(DOWN, buff=0.1).move_to([-3.4, 0.0, 0])
        right = VGroup(tx(f"{M['ap_factories']:.0f}", 46, PRICE, bold=True), tx("apparel factories", 16, GREY_A),
                       tx(f"in {M['ap_countries']:.0f} countries, run by {M['ap_makers']:.0f} contractors", 16, WHITE)
                       ).arrange(DOWN, buff=0.1).move_to([3.4, 0.0, 0])
        own = tx("NIKE owns none of them", 26, BAD, bold=True).move_to([0, -2.0, 0])
        src = source("NIKE, Inc., Form 10-K for fiscal 2026: manufacturing (31 May 2026)", size=12)
        beat(self,
             "NIKE calls itself the largest seller of athletic footwear and apparel in the world, and it makes almost none "
             "of it. <bookmark mark='a'/> In May 2026 "
             f"NIKE's shoes came from {M['fw_factories']:.0f} factories in {M['fw_countries']:.0f} countries, run by "
             f"{M['fw_makers']:.0f} independent manufacturers. <bookmark mark='b'/> Its clothes came from "
             f"{M['ap_factories']:.0f} factories in {M['ap_countries']:.0f} countries, run by {M['ap_makers']:.0f}. "
             f"Behind them stood {M['tier2']:.0f} main suppliers of materials. <bookmark mark='c'/> NIKE owns none of "
             "them: its report says nearly all its products are made by independent contractors, outside the United "
             "States. What NIKE owns is the design, the name and the customers.",
             base=[shoe, shirt, src], steps=[left, right, own])

    def shares(self):
        M = R["made"]
        fw = hbars([(k, v, EXP_COL.get(k, FAST if k == "Indonesia" else GREY_B), f"{v:.0f}%") for k, v in M["fw"].items()],
                   max_value=60, x0=-4.4, top=1.5, row=0.75, length=3.4, size=17, bar_h=0.42)
        ap = hbars([(k, v, EXP_COL.get(k, GREY_B), f"{v:.0f}%") for k, v in M["ap"].items()],
                   max_value=60, x0=2.6, top=1.5, row=0.75, length=3.4, size=17, bar_h=0.42)
        h1 = tx("NIKE Brand shoes, fiscal 2026", 18, PRICE, bold=True).move_to([-4.0, 2.5, 0])
        h2 = tx("NIKE Brand clothes", 18, SPORT, bold=True).move_to([3.0, 2.5, 0])
        top = tx(f"four contractors made {M['fw_top4']:.0f}% of the shoes", 18, WHITE, bold=True).move_to([-3.4, -1.6, 0])
        src = source("NIKE, Inc., Form 10-K for fiscal 2026", size=12)
        beat(self,
             "And where? <bookmark mark='a'/> Of NIKE's shoes, "
             f"{M['fw']['Vietnam']:.0f} per cent were made in Vietnam, {M['fw']['Indonesia']:.0f} per cent in Indonesia, "
             f"and only {M['fw']['China']:.0f} per cent in China. <bookmark mark='b'/> Of its clothes, "
             f"{M['ap']['Vietnam']:.0f} per cent in Vietnam, {M['ap']['Cambodia']:.0f} in Cambodia, {M['ap']['China']:.0f} in "
             f"China. <bookmark mark='c'/> And the shoes are concentrated: four contractors made about {M['fw_top4']:.0f} per "
             f"cent of them, while the six largest clothing contractors made about {get('nke.ap.top6')} per cent of the "
             "clothes, spread over many more factories.",
             base=[h1, h2, src], steps=[[fw.axis, fw], [ap.axis, ap], top])

    def exports(self):
        E = R["made"]["exp2023"]
        items = [(k, v, EXP_COL[k], f"${v:.0f}bn") for k, v in sorted(E.items(), key=lambda kv: -kv[1])]
        rows = hbars(items, max_value=160, x0=-1.6, top=1.8, row=0.62, length=7.0, size=17, bar_h=0.38)
        lab = tx("exports of clothing to the whole world, 2023 (HS chapters 61 and 62)", 16, GREY_A).to_edge(UP, buff=0.8)
        q = tx(f"Quotas on clothing ended on 1 January {get('wto.quota')}", 18, PRICE, bold=True).move_to([0, -2.4, 0])
        src = source("UN Comtrade, exports as reported by each country; WTO, Agreement on Textiles and Clothing. Bangladesh's "
                     "last report in the extract is for 2018", size=12)
        beat(self,
             "Now the countries as a whole. <bookmark mark='a'/> In 2023 China exported "
             f"{E['China']:.0f} billion dollars of clothes, more than the next five on this list together. <bookmark mark='b'/> "
             f"Vietnam {E['Vietnam']:.0f} billion; Italy, the luxury maker, {E['Italy']:.0f}; Turkey {E['Turkey']:.0f}; India "
             f"{E['India']:.0f}; Cambodia {E['Cambodia']:.0f}. Bangladesh, a large exporter, is missing because its last report "
             "to the UN database in this extract is for 2018. <bookmark mark='c'/> This map was drawn partly by a rule change. "
             "Before 1995 much of the clothing that poorer countries sold to richer ones was held to quotas, negotiated "
             "country by country, so orders were spread by quota as well as by cost. Under the WTO's Agreement on Textiles "
             f"and Clothing its members agreed to remove the quotas by 1 January {get('wto.quota')}, and since then orders "
             "have been free to go where the cost and the speed suit the buyer.",
             base=[rows.axis, lab, src], steps=[rows[:1], rows[1:], q])

    def china(self):
        X = R["made"]["exports"]
        series = {k: ({y: v for y, v in X[k].items()}, EXP_COL[k]) for k in ("China", "Vietnam", "Italy", "Turkey", "India")}
        ch = line_chart(series, x=(2010, 2025), y=(0, 180), xticks=[2010, 2013, 2016, 2019, 2022, 2025],
                        yticks=[0, 30, 60, 90, 120, 150, 180], yfmt=lambda v: f"${v:.0f}bn", ylabel="clothing exports to the world",
                        width=9.4, height=4.4, center=(-0.6, -0.45),
                        nudge={"Vietnam": 0.35, "Italy": 0.08, "Turkey": 0.1, "India": -0.18})
        pk = max(X["China"], key=X["China"].get)
        m = marker(ch.ax, pk, X["China"][pk], f"{pk}: ${X['China'][pk]:.0f}bn", BAD, side=UP)
        src = source("UN Comtrade, HS 61 and 62, exports to the world as reported; Vietnam has reported to 2023", size=12)
        beat(self,
             "Over time. <bookmark mark='a'/> China's clothing exports rose to "
             f"{X['China'][pk]:.0f} billion dollars in {pk}, and have not grown since: {X['China'][2025]:.0f} billion in 2025. "
             f"<bookmark mark='b'/> Vietnam's tripled between 2010 and 2023, its latest report, to {X['Vietnam'][2023]:.0f} "
             "billion. Italy's, Turkey's and India's grew more slowly. NIKE's report shows the result for one company rather "
             f"than the reasons: China now makes only {R['made']['fw']['China']:.0f} per cent of its shoes.",
             base=[ch.frame, src], steps=[[ch.lines["China"], ch.labels["China"], m],
                                          [ch.lines[k] for k in ("Vietnam", "Italy", "Turkey", "India")] +
                                          [ch.labels[k] for k in ("Vietnam", "Italy", "Turkey", "India")]])

    def jobs(self):
        M = R["made"]
        ch = line_chart({"jobs": (M["jobs"], DEPT)}, x=(1990, 2025), y=(0, 1000), xticks=[1990, 2000, 2010, 2020, 2025],
                        yticks=[0, 200, 400, 600, 800, 1000], yfmt=lambda v: f"{v:.0f}k",
                        ylabel="people employed making clothes in the United States", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        a = marker(ch.ax, 1990, M["jobs90"], f"1990: {M['jobs90']:.0f},000", WHITE, side=RIGHT)
        b = marker(ch.ax, 2025, M["jobs25"], f"2025: {M['jobs25']:.0f},000", BAD, side=UP)
        src = source("BLS, Current Employment Statistics: all employees, apparel manufacturing (SA), annual averages, via FRED", size=12)
        beat(self,
             "And the other side of that move. <bookmark mark='a'/> In 1990, "
             f"{M['jobs90']:.0f} thousand Americans worked making clothes. <bookmark mark='b'/> By 2025, "
             f"{M['jobs25']:.0f} thousand: fewer than one in ten of those jobs is left. The sewing went abroad; the design, "
             "the brands and the shops stayed, and NIKE, with its four hundred contract factories and none of its own, is "
             "what that looks like from the inside.",
             base=[ch.frame, src], steps=[[ch.lines["jobs"], a], b])
