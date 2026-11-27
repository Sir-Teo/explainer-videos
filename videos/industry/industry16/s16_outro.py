from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.measured()
        self.server()
        self.answers()

    def measured(self):
        comp = R["components"]["margins"]
        C, B = R["contract"], R["brand"]
        pts = [("Amphenol", comp["APH"][2025], PARTS, 0.3), ("TE", comp["TEL"][2025], PARTS, 0.75), ("Corning", comp["GLW"][2025], PARTS, 1.2),
               ("Flex", C["margins"]["FLEX"][2025], ASSEMBLER, 2.2), ("Hon Hai", C["margins"]["HONHAI"][2025], ASSEMBLER, 2.65),
               ("Jabil", C["margins"]["JBL"][2025], ASSEMBLER, 3.1), ("HP", B["margins"]["HPQ"][2025], BRAND, 4.1),
               ("Logitech", B["margins"]["LOGI"][max(B["margins"]["LOGI"])], BRAND, 4.55), ("Apple", B["ni"] / B["rev"], BRAND, 5.0)]
        pa = viz.plot_axes([0, 5.3], [0, 0.3], x_length=9.6, y_length=4.4, xticks=[], yticks=[0, 0.1, 0.2, 0.3],
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="net income per dollar of revenue, latest year", size=13).move_to([-0.4, -0.3, 0])
        dots = VGroup()
        for name, m, col, x in pts:
            d = Dot(pa.ax.c2p(x, m), radius=0.1, color=col)
            dots.add(VGroup(d, tx(name, 12, col, bold=True).next_to(d, UP, buff=0.08)))
        sm = [pa.ax.c2p(0.3, comp["APH"][2025]), pa.ax.c2p(2.65, C["margins"]["HONHAI"][2025]), pa.ax.c2p(5.0, B["ni"] / B["rev"])]
        curve = VMobject(stroke_color=PRICE, stroke_width=5, fill_opacity=0).set_points_smoothly(sm)
        stages = VGroup(tx("components", 16, PARTS, bold=True).move_to([pa.ax.c2p(0.75, 0)[0], pa.ax.c2p(0, 0)[1] - 0.35, 0]),
                        tx("assembly", 16, ASSEMBLER, bold=True).move_to([pa.ax.c2p(2.65, 0)[0], pa.ax.c2p(0, 0)[1] - 0.35, 0]),
                        tx("brands", 16, BRAND, bold=True).move_to([pa.ax.c2p(4.55, 0)[0], pa.ax.c2p(0, 0)[1] - 0.35, 0]))
        head = tx(f"Shih's smile, {R['hook']['shih']:.0f}, measured in 2025", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("SEC EDGAR: Forms 10-K of Amphenol, TE Connectivity, Corning, Flex, Jabil, HP, Logitech and Apple; Hon Hai, audited "
                     "statements 2025", size=12)
        with self.voiceover(
            "Back to the question: why does the company that builds the device keep the least of it? "
            "<bookmark mark='a'/> Put the year's accounts in a row, from the makers of the parts to the assemblers to the "
            "brands. <bookmark mark='b'/> Shih's smile is still there, thirty-four years on. The assembler keeps little "
            "because almost anyone with a plant and a workforce could do its job, because one brand can bring it half its "
            "business, and because the plant stays when the order leaves. The ends keep more when they own something that "
            "cannot be swapped: a part nobody else makes, or a name and a set of services that customers come back to. "
            "Where they do not, as with the PC makers, the brand end sags too."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src), FadeIn(stages), FadeIn(ghost(*dots, opacity=0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.12), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(curve), run_time=2.0)
        self.clear_scene()

    def server(self):
        S = R["servers"]
        (ir, io_) = S["dell_isg"]
        pts = [("chips: Nvidia, gross margin", get("nvda.gm") / 100, PARTS, 0.6),
               ("assembly: Hon Hai's servers arm, operating", S["fii_margin"], ASSEMBLER, 2.5),
               ("brand: Dell's server group, operating", io_ / ir, BRAND, 4.4)]
        pa = viz.plot_axes([0, 5], [0, 0.8], x_length=9.0, y_length=4.4, xticks=[], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="margin per dollar of revenue (measures differ, see labels)", size=12).move_to([-0.4, -0.3, 0])
        dots = VGroup()
        for name, m, col, x in pts:
            d = Dot(pa.ax.c2p(x, m), radius=0.12, color=col)
            dots.add(VGroup(d, tx(name, 13, col, bold=True).next_to(d, UP, buff=0.1), tx(f"{100 * m:.0f}%", 18, col, bold=True).next_to(d, DOWN, buff=0.1)))
        curve = VMobject(stroke_color=PRICE, stroke_width=4, fill_opacity=0).set_points_smoothly([pa.ax.c2p(x, m) for _, m, _, x in pts])
        head = tx("The same smile, in a server", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("NVIDIA, Form 10-K FY2026; Hon Hai, audited statements 2025 (segments); Dell, Form 10-K FY2026 (ISG)", size=12)
        with self.voiceover(
            "And the newest box draws the same curve. <bookmark mark='a'/> The maker of its chips, Nvidia, kept "
            f"{get('nvda.gm'):.0f} cents of gross margin on the dollar. <bookmark mark='b'/> The assembler, Hon Hai's server "
            f"arm, about {100 * S['fii_margin']:.0f} cents of operating income. <bookmark mark='c'/> The brand that sells the "
            f"finished server, Dell's server group, about {100 * io_ / ir:.0f}. The measures differ, but the shape does not: "
            "deep in the middle, high where something cannot be swapped."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src), FadeIn(ghost(*dots, opacity=0.3)))
            for mk, d in zip("abc", dots):
                vo.wait_until(mk)
                self.play(GrowFromCenter(d[0]), FadeIn(d[1]), FadeIn(d[2]))
            self.play(Create(curve), run_time=1.5)
        self.clear_scene()

    def answers(self):
        qs = [("What is sold?", "a device built from other companies' parts, under a brand, and the services sold to its owners"),
              ("How is it made?", "on lines that place, solder, assemble and test, mostly by contract manufacturers in Asia"),
              ("Where does the dollar go?", "to the brand and to the makers of parts nobody else can make; little to the assembler"),
              ("Why does it stay there?", "the brand holds the customer and can move the work; the assembler holds the plant"),
              ("What moves it?", "new boxes like servers, tariffs and the slow move from China to India, Vietnam and Mexico")]
        rows = VGroup()
        for i, (q, a) in enumerate(qs):
            rows.add(VGroup(tx(q, 20, PRICE, bold=True), tx(a, 16, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([-5.6, 2.3 - 1.05 * i, 0], aligned_edge=LEFT))
        with self.voiceover(
            "Electronics, in five answers. <bookmark mark='a'/> What is sold is a device built from other companies' "
            "parts, under a brand, and then the services sold to everyone who owns one. <bookmark mark='b'/> It is made on "
            "lines that place, solder, assemble and test, mostly by contract manufacturers in Asia. <bookmark mark='c'/> The "
            "dollar goes to the brand and to the makers of parts nobody else can make, and very little to the assembler. "
            "<bookmark mark='d'/> It stays there because the brand holds the customer and can move the work, while the "
            "assembler holds the plant. <bookmark mark='e'/> And what moves it are new boxes, like the servers of the "
            "data-centre boom, and tariffs, and the slow move of assembly from China to India, Vietnam and Mexico. Next "
            "time: cars, and why it is so hard to make money making them."
        ) as vo:
            head = tx("Electronics, in five answers", 24, WHITE, bold=True).to_edge(UP, buff=0.3)
            self.play(FadeIn(head), *[FadeIn(r_[0].copy().set_opacity(0.25)) for r_ in rows])
            for m_, r_ in zip("abcde", rows):
                vo.wait_until(m_)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
