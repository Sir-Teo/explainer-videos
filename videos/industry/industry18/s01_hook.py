from __future__ import annotations

from videos.industry.industry18.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.two()
        self.boeing()
        self.engine()
        self.title()

    def two(self):
        H = R["hook"]
        a = VGroup(draw.plane(3.4, AIRBUS), tx("Airbus", 24, AIRBUS, bold=True),
                   tx(f"{H['ab']:.0f}", 64, AIRBUS, bold=True), tx("airliners delivered in 2025", 16, GREY_A)).arrange(DOWN, buff=0.18).move_to([-3.4, 0.2, 0])
        b = VGroup(draw.plane(3.4, BOEING), tx("Boeing", 24, BOEING, bold=True),
                   tx(f"{H['ba']:.0f}", 64, BOEING, bold=True), tx("commercial airplanes delivered in 2025", 16, GREY_A)).arrange(DOWN, buff=0.18).move_to([3.4, 0.2, 0])
        back = tx(f"Airbus's order backlog at the end of 2025: {H['ab_backlog']:,.0f} aircraft", 18, PRICE, bold=True).to_edge(DOWN, buff=0.9)
        src = source("Airbus SE, Annual Report 2025 (ESEF); The Boeing Company, Form 10-K 2025", size=12)
        beat(self,
             "Almost every large passenger jet in the world is built by one of two companies. <bookmark mark='a'/> In "
             f"2025 Airbus, the European maker, delivered {H['ab']:.0f} airliners. <bookmark mark='b'/> Boeing, the American "
             f"maker, delivered {H['ba']:.0f}. <bookmark mark='c'/> And Airbus had orders for "
             f"another {H['ab_backlog']:,.0f} still to build: more than ten years of work at the pace it builds today. Two "
             "makers, and airlines queuing for a decade.",
             base=[src], steps=[a, b, back])

    def boeing(self):
        H = R["hook"]
        ni = {y: v for y, v in R["accounting"]["ni"].items() if 2014 <= y <= 2025}
        items = [(str(y), v, GOOD if v >= 0 else BAD, ("-" if v < 0 else "") + f"${abs(v):.1f}bn") for y, v in sorted(ni.items())]
        top = max(abs(v) for v in ni.values())
        bars_ = VGroup()
        for i, (lab, v, col, vt) in enumerate(items):
            x = -5.4 + 0.98 * i
            h = 2.3 * abs(v) / top
            rect = Rectangle(width=0.66, height=max(h, 0.03), stroke_width=0, fill_color=col, fill_opacity=0.9)
            rect.move_to([x, -0.4 + (h / 2 if v >= 0 else -h / 2), 0])
            rect.grow = DOWN if v >= 0 else UP
            bars_.add(VGroup(rect, tx(vt, 12, col, bold=True).next_to(rect, UP if v >= 0 else DOWN, buff=0.06),
                             tx(lab, 13, GREY_A).move_to([x, -0.4 + (-0.25 if v >= 0 else 0.25), 0])))
        axis = Line([-5.9, -0.4, 0], [6.2, -0.4, 0], stroke_color=GREY_B, stroke_width=2)
        losses = sum(v for y, v in ni.items() if 2019 <= y <= 2024)
        src = source("The Boeing Company, Forms 10-K (net income attributable to shareholders), via SEC company facts", size=12)
        beat(self,
             "Being one of two sounds like a licence to print money. <bookmark mark='a'/> Here is Boeing's profit, year by "
             f"year. Up to 2018 it earned between five and ten billion dollars a year. <bookmark mark='b'/> Then two crashes "
             "of its 737 MAX, a worldwide grounding, a pandemic that emptied the skies, a door panel blown out in flight "
             f"and a strike: from 2019 to 2024 Boeing lost {-losses:.0f} billion dollars in all. <bookmark mark='c'/> In 2025 "
             f"it was back in profit, {ni[2025]:.1f} billion, while its airliner business itself still lost "
             f"{-H['bca_op'] / 1e3:.1f} billion.",
             base=[axis, head("Boeing's net income, 2014-2025"), src],
             steps=[VGroup(*bars_[:5]), VGroup(*bars_[5:11]), bars_[11]])

    def engine(self):
        H = R["hook"]
        E = R["engines"]
        eng = draw.turbofan(3.0, ENGINE).move_to([-4.4, 0.4, 0])
        pie = VGroup(
            Rectangle(width=6.0 * E["equipment"] / (E["equipment"] + E["services"]), height=0.7, stroke_width=0, fill_color=GREY_B, fill_opacity=0.9),
            Rectangle(width=6.0 * E["services"] / (E["equipment"] + E["services"]), height=0.7, stroke_width=0, fill_color=ENGINE, fill_opacity=0.9)).arrange(RIGHT, buff=0).move_to([2.2, 0.8, 0])
        labs = VGroup(tx(f"new engines ${E['equipment'] / 1e3:.1f}bn", 15, GREY_A).next_to(pie[0], DOWN, buff=0.15),
                      tx(f"spare parts and servicing ${E['services'] / 1e3:.1f}bn", 15, ENGINE, bold=True).next_to(pie[1], DOWN, buff=0.15))
        note = tx(f"GE Aerospace: aftermarket services about {H['ge_services']:.0f}% of revenue", 18, ENGINE, bold=True).move_to([2.2, -1.4, 0])
        src = source("General Electric Company (GE Aerospace), Form 10-K 2025 (Commercial Engines & Services)", size=12)
        beat(self,
             "And there is a second puzzle, inside the airliner. <bookmark mark='a'/> The engines on it are made by a "
             "handful of companies, the largest of them GE Aerospace. <bookmark mark='b'/> In 2025 GE's commercial engine "
             f"business sold {E['equipment'] / 1e3:.1f} billion dollars of new engines, <bookmark mark='c'/> and "
             f"{E['services'] / 1e3:.1f} billion of spare parts and servicing for the engines already flying. "
             "<bookmark mark='d'/> The money is in the years after the sale. GE's own report counts delivering more new "
             "engines as a drag on its profit; why a business would sell its product for so little is one of the threads "
             "of this film.",
             base=[src], steps=[eng, [pie[0], labs[0]], [pie[1], labs[1]], note])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part eighteen: aerospace and defence. Why are there only two makers of large "
                            "airliners, and why does the engine maker sell at a loss?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
