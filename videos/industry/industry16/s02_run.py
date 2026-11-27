from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403

HOME, ABROAD, DECLINE = "#F2A65A", "#B58CFF", "#9AA3B2"


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: the order that needs a plant", "A brand offers you a huge order at a thin margin. Do you build?",
             "Chapter one. Run it: the order that needs a plant.", lit=("make", "dollar"))
        self.setup_()
        self.flows()
        self.curve()
        self.tooling()

    def setup_(self):
        G = R["run"]
        brand = VGroup(draw.phone(1.3, screen=BRAND), tx("the brand", 16, BRAND, bold=True)).arrange(DOWN, buff=0.15).move_to([-4.6, 1.0, 0])
        plant = VGroup(draw.factory(2.2), tx("you: the assembler", 16, ASSEMBLER, bold=True)).arrange(DOWN, buff=0.15).move_to([4.4, 1.0, 0])
        order = VGroup(tx("The order", 20, WHITE, bold=True),
                       tx(f"{G['units'] / 1e6:.0f} million devices a year, for {G['years']} years", 15, GREY_A),
                       tx(f"you are paid ${G['fee']:.0f} a device to assemble and test", 15, GREY_A),
                       tx("a new plant, ready in a year", 15, GREY_A),
                       tx(f"then: renewed for {G['renewal']} more years, or moved elsewhere", 15, PRICE)).arrange(DOWN, buff=0.07)
        frame = SurroundingRectangle(order, buff=0.2, corner_radius=0.1, stroke_color=GREY_B, stroke_width=2, fill_color="#151A23", fill_opacity=1)
        doc = VGroup(frame, order).move_to([0, 1.0, 0])
        costs = VGroup(tx(f"the plant: ${G['plant']:.0f} million", 16, WHITE, bold=True),
                       tx(f"each device: ${G['labour']:.0f} of labour, ${G['other']:.0f} of power, logistics and scrap", 15, GREY_A),
                       tx(f"the plant's overhead: ${G['fixed']:.0f} million a year", 15, GREY_A)).arrange(DOWN, buff=0.07).move_to([0, -2.1, 0])
        arrow = Arrow(brand.get_right(), doc.get_left(), buff=0.15, color=BRAND, stroke_width=3)
        arrow2 = Arrow(doc.get_right(), plant.get_left(), buff=0.15, color=ASSEMBLER, stroke_width=3)
        tag = estimate_tag("the Works' assembler: an illustration in round numbers", corner=DR, size=12)
        with self.voiceover(
            "You run an assembler, a company that builds devices for other people's brands. <bookmark mark='a'/> A brand "
            f"offers you an order: {G['units'] / 1e6:.0f} million devices a year for {G['years']} years, at "
            f"${G['fee']:.0f} a device for assembling and testing them. The catch: it wants a new plant, ready in a year. "
            f"<bookmark mark='b'/> The plant costs ${G['plant']:.0f} million. Each device costs you about "
            f"${G['labour'] + G['other']:.0f} in labour, power and logistics, and the plant costs ${G['fixed']:.0f} million "
            "a year to keep open. <bookmark mark='c'/> After three years the brand will either renew for three more, or move "
            "the work to someone else. It will not tell you which."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(brand), FadeIn(plant), FadeIn(ghost(doc, costs, opacity=0.25)))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(doc, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(GrowArrow(arrow2), FadeIn(costs, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(Indicate(order[-1], color=PRICE, scale_factor=1.08))
        self.clear_scene()

    def flows(self):
        G = R["run"]
        g = G["games"]["build"]
        fl = g["flows"]
        sc = 0.0032
        base = 0.4
        bars, labs = VGroup(), VGroup()
        for t, v in enumerate(fl):
            x = -5.0 + 1.35 * t
            renew = t > G["years"]
            col = BAD if v < 0 else (HOME if not renew else HOME)
            b = Rectangle(width=0.8, height=max(abs(v) * sc, 0.02), stroke_color=col, stroke_width=2 if renew else 0,
                          fill_color=col, fill_opacity=0.25 if renew else 0.9)
            b.move_to([x, base, 0], aligned_edge=DOWN if v >= 0 else UP)
            bars.add(b)
            labs.add(VGroup(tx(f"{'+' if v >= 0 else '-'}${abs(v):.0f}m", 14, col, bold=True).next_to(b, UP if v >= 0 else DOWN, buff=0.06),
                            tx(f"year {t}", 13, GREY_B).move_to([x, base - 0.25 if v >= 0 else base + 0.25, 0])))
        zero = Line([-5.6, base, 0], [3.6, base, 0], stroke_color=GREY_B, stroke_width=1.5)
        brace1 = Brace(VGroup(*bars[1:1 + G["years"]]), UP, color=GREY_B).shift(UP * 1.1)
        b1 = tx("the order", 14, GREY_A).next_to(brace1, UP, buff=0.05)
        brace2 = Brace(VGroup(*bars[1 + G["years"]:]), UP, color=PRICE).shift(UP * 1.1)
        b2 = tx("if renewed", 14, PRICE).next_to(brace2, UP, buff=0.05)
        res = VGroup(tx("value today, at 8% a year", 15, GREY_A),
                     tx(f"if not renewed: -${abs(g['no']):.0f}m", 20, BAD, bold=True),
                     tx(f"if renewed: +${g['yes']:.0f}m", 20, GOOD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.3, 1.2, 0])
        tag = estimate_tag("the Works' assembler: an illustration in round numbers", corner=DR, size=12)
        with self.voiceover(
            "Here is the plant's cash, year by year. <bookmark mark='a'/> Year zero: you spend "
            f"${G['plant']:.0f} million building it. <bookmark mark='b'/> Year one, the line is still learning, and runs at "
            f"half speed: about ${fl[1]:.0f} million. Years two and three, at full speed: about ${fl[2]:.0f} million each. "
            f"<bookmark mark='c'/> Add it up in today's money and the order alone leaves you about ${abs(g['no']):.0f} "
            "million short. <bookmark mark='d'/> Only if the brand renews do the later years arrive, and then the plant is "
            f"worth about ${g['yes']:.0f} million. Thirty dollars a device sounds like plenty; on a plant that may stand idle in "
            "three years, it is not."
        ) as vo:
            self.play(FadeIn(zero), FadeIn(tag), FadeIn(ghost(*bars, opacity=0.2)), *[FadeIn(l_[1]) for l_ in labs])
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], UP), FadeIn(labs[0][0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[t], DOWN), FadeIn(labs[t][0])) for t in range(1, 1 + G["years"])], lag_ratio=0.3),
                      GrowFromCenter(brace1), FadeIn(b1), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(res[:2], shift=LEFT * 0.1))
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[t], DOWN), FadeIn(labs[t][0])) for t in range(1 + G["years"], len(fl))], lag_ratio=0.3),
                      GrowFromCenter(brace2), FadeIn(b2), run_time=2.0)
            self.play(FadeIn(res[2], shift=LEFT * 0.1))
        self.clear_scene()

    def curve(self):
        G = R["run"]
        cv = G["curve"]
        ps = sorted(cv)
        pa = viz.plot_axes([0, 1], [-400, 600], x_length=8.4, y_length=4.6, xticks=[0, 0.25, 0.5, 0.75, 1.0],
                           yticks=[-400, -200, 0, 200, 400, 600], xfmt=lambda v: f"{100 * v:.0f}%", yfmt=lambda v: f"${v:.0f}m",
                           ylabel="the plant's expected value today", size=13).move_to([-1.4, -0.4, 0])
        xl = tx("chance the brand renews", 14, GREY_B).next_to(pa, DOWN, buff=0.1)
        zero = DashedLine(pa.ax.c2p(0, 0), pa.ax.c2p(1, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        lines = {k: poly(pa, [(p, cv[p][k]) for p in ps], col, 4) for k, col in (("decline", DECLINE), ("build", HOME), ("abroad", ABROAD))}
        names = {"decline": "decline", "build": "build the plant", "abroad": "build in a new country"}
        labs = VGroup(*[tx(names[k], 15, col, bold=True).next_to(pa.ax.c2p(1, cv[ps[-1]][k]), RIGHT, buff=0.1)
                        for k, col in (("decline", DECLINE), ("build", HOME), ("abroad", ABROAD))])
        even = G["games"]["build"]["even"]
        em = Dot(pa.ax.c2p(even, 0), radius=0.08, color=PRICE)
        el = tx(f"worth it above about {100 * even:.0f}%", 15, PRICE, bold=True).next_to(em, DOWN + RIGHT, buff=0.1)
        side = VGroup(tx("A new country: half the labour,", 14, GREY_A), tx("a plant 10% dearer, a slower start.", 14, GREY_A),
                      tx(f"It wins only if renewal is likelier", 14, ABROAD, bold=True), tx(f"than about {100 * G['cross']:.0f}%.", 14, ABROAD, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.9, -2.2, 0])
        tag = estimate_tag("the Works' assembler: an illustration in round numbers", corner=DR, size=12)
        with self.voiceover(
            "So the decision is a bet on the brand. <bookmark mark='a'/> Across: the chance it renews. Up: what the plant is "
            "worth today. Declining is worth nothing either way. <bookmark mark='b'/> Building is worth it only if you put "
            f"the chance of renewal above about {100 * even:.0f} per cent. <bookmark mark='c'/> And a plant in a new country, "
            "with cheaper labour but a slower start, pays only if renewal is likelier still. <bookmark mark='d'/> That is the "
            "assembler's life: the brand holds the customer and the design, and can take the work elsewhere; the assembler "
            "holds the plant. Whoever can walk away keeps the margin."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(zero), FadeIn(tag), Create(lines["decline"]), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(Create(lines["build"]), FadeIn(labs[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(GrowFromCenter(em), FadeIn(el))
            vo.wait_until("c")
            self.play(Create(lines["abroad"]), FadeIn(labs[2]), FadeIn(side), run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(lines["build"], color=HOME, scale_factor=1.0))
        self.clear_scene()

    def tooling(self):
        G = R["run"]
        g, t = G["games"]["build"], G["tooling"]
        def col(x, v, name, sub, c_):
            sc = 0.0035
            b = Rectangle(width=1.5, height=abs(v) * sc, stroke_width=0, fill_color=c_, fill_opacity=0.9).move_to([x, 0.0, 0], aligned_edge=DOWN if v >= 0 else UP)
            lab = tx(f"{'+' if v >= 0 else '-'}${abs(v):.0f}m", 18, c_, bold=True).next_to(b, UP if v >= 0 else DOWN, buff=0.08)
            nm = VGroup(tx(name, 15, WHITE, bold=True), tx(sub, 12, GREY_A)).arrange(DOWN, buff=0.03).move_to([x, 2.6, 0])
            return VGroup(b, lab, nm)
        a = col(-3.2, g["no"], "you pay for the plant", f"${G['plant']:.0f}m", BAD)
        b = col(1.2, t["no"], "the brand pays half", f"you pay ${t['plant']:.0f}m", GOOD)
        zero = Line([-5.0, 0, 0], [3.0, 0, 0], stroke_color=GREY_B, stroke_width=1.5)
        head = tx("Value today if the brand does not renew", 18, GREY_A).move_to([-1.0, 3.3, 0])
        side = VGroup(tx("Whoever pays for the plant", 16, WHITE, bold=True), tx("carries the risk that", 16, WHITE, bold=True),
                      tx("the work moves away.", 16, WHITE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([5.0, 0.4, 0])
        tag = estimate_tag("the Works' assembler: an illustration in round numbers", corner=DR, size=12)
        with self.voiceover(
            "There is a way out, and it shows who holds the power. <bookmark mark='a'/> If you pay for the plant and the "
            f"brand walks away after three years, you are about ${abs(g['no']):.0f} million down. <bookmark mark='b'/> If "
            f"the brand pays for half of it, the tools and the special equipment, the same three years leave you about "
            f"${t['no']:.0f} million up. <bookmark mark='c'/> A brand that wants a plant built quickly can pay for the "
            "tooling, and then the assembler no longer needs to trust it. Whoever pays for the machines carries the risk "
            "that the work moves away."
        ) as vo:
            self.play(FadeIn(zero), FadeIn(head), FadeIn(tag), FadeIn(a[2]), FadeIn(b[2]), FadeIn(ghost(a[0], b[0], opacity=0.25)))
            vo.wait_until("a")
            self.play(GrowFromEdge(a[0], UP), FadeIn(a[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(b[1]))
            vo.wait_until("c")
            self.play(FadeIn(side, shift=LEFT * 0.1))
        self.clear_scene()
