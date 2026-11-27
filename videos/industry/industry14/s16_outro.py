from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.tunnel()
        self.answers()

    def tunnel(self):
        H = R["hook"]
        water = Rectangle(width=14.4, height=1.0, stroke_width=0, fill_color="#3E6E8E", fill_opacity=0.8).move_to([0, -0.6, 0])
        ground = Rectangle(width=14.4, height=2.6, stroke_width=0, fill_color="#2A2219", fill_opacity=1).move_to([0, -2.4, 0])
        old = Line([-7.2, -1.35, 0], [7.2, -1.35, 0], stroke_color=SEWAGE, stroke_width=10)
        old_l = tx("the sewers of the 1858 plan", 15, SEWAGE, bold=True).move_to([-3.8, -1.05, 0])
        new = Line([-7.2, -2.55, 0], [7.2, -2.55, 0], stroke_color=WATER, stroke_width=18)
        new_l = tx(f"the Thames Tideway Tunnel, licensed in {H['tideway']:.0f}", 15, WATER, bold=True).move_to([2.6, -3.05, 0])
        skyline = draw.skyline(10.0, seed=14).move_to([0, -0.1, 0], aligned_edge=DOWN)
        quote = VGroup(tx("Ofwat's licence went to", 18, GREY_A), tx("Bazalgette Tunnel Limited", 30, WHITE, bold=True)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.5)
        src = source("GOV.UK, Thames Tideway Tunnel: government support package contract documents (updated July 2026)", size=13)
        with self.voiceover(
            "Back to London. <bookmark mark='a'/> The plan for the drains Parliament paid for in 1858 was the work of the "
            "Metropolitan Board of Works' engineers, among them Joseph Bazalgette. <bookmark mark='b'/> A century and a "
            "half later London needed a new sewer tunnel under the river. In "
            f"{H['tideway']:.0f}, Ofwat licensed a private company to design, build, finance, operate and maintain it, "
            "with the government standing behind it against risks no private investor would take. "
            "<bookmark mark='c'/> The company's name: Bazalgette Tunnel Limited."
        ) as vo:
            self.play(FadeIn(ground), FadeIn(water), FadeIn(skyline), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(old), FadeIn(old_l), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(new), FadeIn(new_l), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(quote, shift=DOWN * 0.1))
        self.clear_scene()

    def answers(self):
        qs = [("What is sold?", "a service on a fixed network: water in, sewage out; a stop on a route; a ton into a hole"),
              ("How is it made?", "almost all fixed cost, in pipes, works, trucks and landfills that last for decades"),
              ("Where does the dollar go?", "to the return on a regulated asset base, and to whoever owns the hole"),
              ("Why does it stay there?", "density, permits and regulators: nobody can lay a second set of pipes"),
              ("What moves it?", "new rules, the cost of borrowing, the price of a bale; rarely the customer")]
        rows = VGroup()
        for i, (q, a) in enumerate(qs):
            rows.add(VGroup(tx(q, 20, PRICE, bold=True), tx(a, 16, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([-5.6, 2.3 - 1.05 * i, 0], aligned_edge=LEFT))
        with self.voiceover(
            "So, the businesses nobody thinks about. <bookmark mark='a'/> They sell a service delivered through a network "
            "nobody can duplicate. <bookmark mark='b'/> Almost all of their cost is fixed, in things that last for "
            "decades. <bookmark mark='c'/> The money goes to the return on those things, set by a regulator or by the "
            "scarcity of a permit. <bookmark mark='d'/> Density, permits and regulators keep it there. "
            "<bookmark mark='e'/> And what moves it is rarely the customer, who cannot do without it, but new rules, the "
            "cost of borrowing and, for the recyclers, the price of a bale. That is why they are so steady, and why "
            "the bill only ever goes one way. Next time: the factories of Act Three, starting with the most complicated "
            "thing humanity makes, the semiconductor."
        ) as vo:
            head = tx("Water and waste, in five answers", 24, WHITE, bold=True).to_edge(UP, buff=0.3)
            self.play(FadeIn(head), *[FadeIn(r_[0].copy().set_opacity(0.25)) for r_ in rows])
            for m_, r_ in zip("abcde", rows):
                vo.wait_until(m_)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
