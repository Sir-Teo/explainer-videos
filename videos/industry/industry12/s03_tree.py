from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Tree(VoiceoverScene):
    def construct(self):
        card(self, 2, "Three raw materials, a thousand products", "What does the chemical industry actually make?",
             "Chapter two. Three raw materials, a thousand products.", lit=("unit", "make"))
        self.tree()
        self.sales()

    def node(self, text, color, x, y, size=17, w=2.5):
        t = tx(text, size, "#0E1117", bold=True)
        box = RoundedRectangle(corner_radius=0.1, width=max(w, t.width + 0.3), height=t.height + 0.25, stroke_width=0,
                               fill_color=color, fill_opacity=0.92).move_to([x, y, 0])
        t.move_to(box)
        return VGroup(box, t)

    def tree(self):
        roots = [("natural gas", GAS, 1.8), ("crude oil", OIL, -0.2), ("salt", SALT, -2.2)]
        blocks = [("ammonia", NITRO, 2.9, 0), ("methanol", GAS, 2.0, 0), ("ethylene", ETHYL, 1.1, 0), ("propylene", ETHYL, 0.2, 1),
                  ("butadiene", OIL, -0.7, 1), ("benzene, xylenes", OIL, -1.6, 1), ("chlorine, caustic soda", SALT, -2.6, 2)]
        mats = [("fertilizers", FERT, 2.9), ("solvents, glues", GAS, 2.0), ("polyethylene", PLASTIC, 1.1), ("PVC", PLASTIC, 0.25),
                ("polypropylene", PLASTIC, -0.6), ("synthetic rubber", OIL, -1.45), ("polyester, nylon", SPEC, -2.3)]
        R_ = VGroup(*[self.node(n, c, -5.4, y, 19, 2.2) for n, c, y in roots])
        B_ = VGroup(*[self.node(n, c, -1.9, y, 15, 2.7) for n, c, y, _ in blocks])
        M_ = VGroup(*[self.node(n, c, 1.8, y, 15, 2.6) for n, c, y in mats])
        icons = VGroup(draw.sack(0.45, label_="N"), draw.paint_can(0.45), draw.pellet_bag(0.5), draw.rebar(0.6, 2, "#C9D3E0"),
                       draw.can(0.5, "#7EC8F5", "#F2C14E"), Circle(0.22, stroke_color="#3E4553", stroke_width=6),
                       draw.person(0.5, SPEC))
        for ic, m in zip(icons, M_):
            ic.scale_to_fit_height(min(ic.height, 0.5))
            ic.next_to(m, RIGHT, buff=0.35)
        prod = VGroup(tx("fields", 13, GREY_A), tx("paint, adhesives", 13, GREY_A), tx("bags, bottles, films", 13, GREY_A),
                      tx("pipes, window frames", 13, GREY_A), tx("car parts, packaging", 13, GREY_A), tx("tyres", 13, GREY_A),
                      tx("clothes, carpets", 13, GREY_A))
        for p_, ic in zip(prod, icons):
            p_.next_to(ic, RIGHT, buff=0.15)
        links = VGroup()
        src_of = {0: [0, 1, 2], 1: [2, 3, 4, 5], 2: [6]}
        for r_i, bs in src_of.items():
            for b_i in bs:
                links.add(Line(R_[r_i].get_right(), B_[b_i].get_left(), stroke_color=GREY_D, stroke_width=1.5))
        mlinks = VGroup(*[Line(B_[i].get_right(), M_[j].get_left(), stroke_color=GREY_D, stroke_width=1.5)
                          for i, j in ((0, 0), (1, 1), (2, 2), (2, 3), (6, 3), (3, 4), (4, 5), (5, 6))])
        heads = VGroup(tx("raw materials", 15, GREY_B), tx("building blocks", 15, GREY_B), tx("materials", 15, GREY_B),
                       tx("what we buy", 15, GREY_B))
        for h, x in zip(heads, (-5.4, -1.9, 1.8, 5.2)):
            h.move_to([x, 3.55, 0])
        with self.voiceover(
            "The chemical industry starts from very few raw materials. <bookmark mark='a'/> Natural gas, crude oil and "
            "salt. <bookmark mark='b'/> From them it makes a handful of building blocks, in enormous quantities: "
            "ammonia and methanol from the methane in gas; ethylene, propylene and butadiene from ethane or from "
            "naphtha; benzene and xylenes from oil; and chlorine and caustic soda by passing electricity through salt "
            "water. <bookmark mark='c'/> The building blocks are joined into materials: fertilizers; solvents and glues; "
            "polyethylene from ethylene; PVC from ethylene and chlorine; polypropylene; synthetic rubber; polyester and "
            "nylon. <bookmark mark='d'/> And the materials become things: crops, paint, bags and bottles, pipes, car "
            "parts, tyres and clothes. Every step down the tree adds value, and, as we will see, the money is not spread "
            "evenly along it."
        ) as vo:
            self.play(FadeIn(heads), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in R_], lag_ratio=0.25), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(r_, scale_factor=1.08) for r_ in R_], lag_ratio=0.25), run_time=1.2)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in links], lag_ratio=0.05), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in B_], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(l_) for l_ in mlinks], lag_ratio=0.05), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in M_], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(i_, shift=RIGHT * 0.2), FadeIn(p_)) for i_, p_ in zip(icons, prod)],
                                  lag_ratio=0.2), run_time=3.0)
        self.clear_scene()

    def sales(self):
        T_ = R["tree"]
        cols = {"basic chemicals": ETHYL, "plastics, rubber and fibres": PLASTIC, "fertilizers and farm chemicals": FERT,
                "medicines": SPEC, "paints and adhesives": PRICE, "soaps, cleaners and cosmetics": GASES, "other": "#5D6B82"}
        items = [(k, v, cols[k], f"${v:,.0f}bn") for k, v in sorted(T_["sales"].items(), key=lambda kv: -kv[1])]
        tm = viz.treemap(items, width=10.0, height=5.0, size=17).move_to([0, -0.5, 0])
        head = tx(f"What US chemical makers sold, 2022: about ${T_['total'] / 1000:.1f} trillion", 22, WHITE, bold=True).to_edge(
            UP, buff=0.35)
        src = source("US Census Bureau, 2022 Economic Census (sales by six-digit industry, NAICS 325, summed into groups)",
                     size=13)
        with self.voiceover(
            f"How big is it? American chemical makers sold about {T_['total']:,.0f} billion dollars' worth of products in "
            "2022, by the Census Bureau's count. <bookmark mark='a'/> The largest group is the basic chemicals at the "
            f"root of the tree, about {T_['sales']['basic chemicals']:.0f} billion dollars, petrochemicals among them. "
            f"<bookmark mark='b'/> Then medicines, about {T_['sales']['medicines']:.0f} billion, which this series leaves "
            "for its own part. <bookmark mark='c'/> Then plastics and rubber, soaps and cosmetics, paints, and "
            "fertilizers. This part follows the industrial chemistry: the basic chemicals, the plastics and fertilizers "
            "made from them, the gases, and the speciality products at the end of the chain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tm[0], scale=0.95))
            vo.wait_until("a")
            self.play(Indicate(tm[0], color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(tm[1], scale=0.95))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b, scale=0.95) for b in tm[2:]], lag_ratio=0.2), run_time=2.0)
        self.clear_scene()
