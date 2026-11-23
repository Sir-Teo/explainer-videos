from __future__ import annotations

from videos.industry.industry1.common import *  # noqa: F403

LAYERS = (
    ("cover", "Cover glass", I.CASE),
    ("display", "Display", I.DISPLAY),
    ("frame", "Body and frame", I.CASE),
    ("board", "Logic board", I.CHIP),
    ("battery", "Battery", I.POWER),
    ("camera", "Cameras", I.CAMERA),
)

# Who makes each layer: (company, region) - companies on Apple's published supplier list and in teardown reports.
MAKERS = {
    "cover": [("Corning", "US")],
    "display": [("Samsung Display", "Korea"), ("LG Display", "Korea")],
    "frame": [("enclosure makers", "China")],
    "board": [("Apple designs the chip", "US"), ("TSMC makes it", "Taiwan"), ("Samsung", "Korea"),
              ("SK hynix", "Korea"), ("Micron", "US"), ("Kioxia", "Japan"), ("Qualcomm", "US"), ("Broadcom", "US"),
              ("Murata", "Japan")],
    "battery": [("cell and pack makers", "China")],
    "camera": [("Sony sensors", "Japan"), ("Largan lenses", "Taiwan"), ("LG Innotek", "Korea")],
}


class Inside(VoiceoverScene):
    def construct(self):
        card(self, 2, "Inside the phone", "What is in it, and who makes each part?",
             "Chapter two. Inside the phone.", lit=("unit", "make"))
        self.explode()
        self.regions()

    def explode(self):
        ph = viz.phone(4.4, back=True, body=BODY_17).shift(LEFT * 4.9)
        ex = viz.exploded(LAYERS, w=3.0, d=1.7, gap=0.86).scale(0.88).move_to(LEFT * 4.9 + DOWN * 0.1)
        names = VGroup(*[T(n, 21, c).move_to(np.array([-2.75, l.get_center()[1], 0]), aligned_edge=LEFT)
                         for (k, n, c), l in zip(LAYERS, ex)])
        rows = {}
        for (k, n, c), l in zip(LAYERS, ex):
            ps = VGroup(*[pill(m, region=r, size=19) for m, r in MAKERS[k]])
            if k == "board":
                ps = VGroup(VGroup(*ps[:4]).arrange(RIGHT, buff=0.12), VGroup(*ps[4:]).arrange(RIGHT, buff=0.12)
                            ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            else:
                ps.arrange(RIGHT, buff=0.12)
            if ps.width > 7.5:
                ps.scale_to_fit_width(7.5)
            ps.move_to(np.array([-0.55, l.get_center()[1], 0]), aligned_edge=LEFT)
            rows[k] = ps
        assembly = VGroup(T("Put together by", 20, I.DIM), pill("Foxconn", region="Taiwan", size=18),
                          pill("Luxshare", region="China", size=18), pill("Tata Electronics", region="India", size=18),
                          T("in China and India", 20, I.DIM)).arrange(RIGHT, buff=0.16).to_edge(DOWN, buff=0.38)
        src = source("Apple Supplier List; teardown reports (TechInsights); Apple Form 10-K FY2026", corner=UR)
        with self.voiceover(
            "From the outside a phone is one object. <bookmark mark='a'/> Take it apart and it is six layers, each "
            "made by different companies. <bookmark mark='b'/> On top, the cover glass, from Corning, an American "
            "glass maker. <bookmark mark='c'/> Under it, the display: an organic light-emitting panel, made for "
            "Apple by Samsung Display and LG Display, both of South Korea. <bookmark mark='d'/> The body and frame, "
            "machined from aluminium by enclosure makers in China. <bookmark mark='e'/> Then the logic board, the "
            "phone's brain. Its main processor is designed by Apple in California and manufactured by TSMC in "
            "Taiwan. Its working memory and storage come from Samsung and SK hynix of Korea, Micron of the United "
            "States and Kioxia of Japan. The modem that talks to the cell towers comes from Qualcomm, and the radio "
            "parts from Broadcom, Murata and others. <bookmark mark='f'/> The battery cells and packs come from "
            "makers in China. <bookmark mark='g'/> And the cameras pair image sensors from Sony in Japan with lenses "
            "from Largan in Taiwan and camera modules from LG Innotek in Korea. <bookmark mark='h'/> Finally, the "
            "whole thing is put together by contract manufacturers: Foxconn, a Taiwanese company, and Luxshare, a "
            "Chinese one, in factories in China, and increasingly by Foxconn and Tata Electronics in India."
        ) as vo:
            self.play(FadeIn(ph, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(ReplacementTransform(ph, ex), run_time=1.8)
            for k, m in zip(("cover", "display", "frame", "board", "battery", "camera"), "bcdefg"):
                vo.wait_until(m)
                i = [x[0] for x in LAYERS].index(k)
                self.play(FadeIn(names[i]), FadeIn(rows[k], shift=RIGHT * 0.15), run_time=0.9)
            vo.wait_until("h")
            self.play(FadeIn(assembly, shift=UP * 0.15))
        self.ex, self.rows, self.names, self.assembly, self.src = ex, rows, names, assembly, src

    def regions(self):
        counts = {}
        for k, ms in MAKERS.items():
            for _, r in ms:
                counts[r] = counts.get(r, 0) + 1
        for r in ("Taiwan", "China", "India"):
            counts[r] = counts.get(r, 0) + 1
        tiles = viz.region_map(regions=("US", "Europe", "India", "China", "Korea", "Japan", "Taiwan", "SE Asia"),
                               w=1.9, h=0.9, size=21)
        world = VGroup(*tiles.values()).move_to(DOWN * 0.3)
        lit = [r for r in ("US", "Korea", "Japan", "Taiwan", "China", "India")]
        quote = VGroup(T("“A significant majority of the Company’s manufacturing is performed ... by outsourcing", 19,
                         I.TEXT), T("partners located primarily in China mainland, India, Japan, South Korea, Taiwan and "
                         "Vietnam.”", 19, I.TEXT), T("Apple, Form 10-K, fiscal 2026", 17, I.DIM)
                       ).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.45)
        head = TB("Six layers, at least six economies", 32, I.TEXT).to_edge(UP, buff=0.55)
        with self.voiceover(
            "Six layers, and at least six economies. <bookmark mark='a'/> The United States, South Korea, Japan, "
            "Taiwan, China and India each make a part that this phone cannot do without, and Apple's own annual "
            "report adds Vietnam to the list of places where its products are made. <bookmark mark='b'/> No country "
            "makes a modern phone alone. The question for the rest of this part is how the 1,099 dollars is shared "
            "among all these companies, and why it is shared the way it is."
        ) as vo:
            self.play(FadeOut(VGroup(self.ex, self.names, *self.rows.values(), self.assembly, self.src)), FadeIn(head))
            self.play(FadeIn(world), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[tiles[r][0].animate.set_fill(opacity=0.55) for r in lit], lag_ratio=0.25),
                      run_time=2.2)
            self.play(tiles["SE Asia"][0].animate.set_fill(opacity=0.35))
            vo.wait_until("b")
            self.play(FadeIn(quote, shift=UP * 0.1))
        self.clear_scene()
