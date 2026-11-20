from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


class Chains(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Value chains", r"Where is an iPhone made?", "Chapter eleven. Value chains.",
             lit={2010: r"Xing and Detert"}, scale=("firm", "world"), horizon=("a year",))
        self.iphone()

    def iphone(self):
        C = load("chains")
        flow = flow_chain([(r"design and software", USA), (r"parts", ARCH), (r"assembly", CHINA), (r"sale", GAIN)],
                          notes=[r"California", r"Japan, \ Korea, \ Germany, \ Taiwan, \ America",
                                 rf"China: \ \${C['china_va']:.2f} a phone", r"America and the world"],
                          box_w=2.6, font_size=21, note_size=17).move_to(UP * 2.1)
        W = 8.6
        x0 = -4.6
        bar1 = Rectangle(width=W, height=0.5, fill_color=CHINA, fill_opacity=0.85, stroke_width=0)
        bar1.move_to(np.array([x0 + W / 2, 0.1, 0]))
        shell = Rectangle(width=W, height=0.5, fill_color=ARCH, fill_opacity=0.25, stroke_color=ARCH,
                          stroke_width=1.5).move_to(np.array([x0 + W / 2, -0.95, 0]))
        w_cn = W * C["china_va"] / C["total"]
        sliver = Rectangle(width=w_cn, height=0.5, fill_color=CHINA, fill_opacity=0.95, stroke_width=0)
        sliver.move_to(np.array([x0 + W - w_cn / 2, -0.95, 0]))
        lab1 = VGroup(label(r"counted as a Chinese export", font_size=18, color=GREY_A).next_to(bar1, UP, buff=0.1,
                                                                                                aligned_edge=LEFT),
                      label(rf"\${C['total']:.2f}", font_size=22, color=CHINA).next_to(bar1, RIGHT, buff=0.2))
        lab2 = VGroup(label(rf"parts from Japan, \ Korea, \ Germany, \ Taiwan, \ America: \ \${C['parts']:.2f}",
                            font_size=18, color=ARCH).next_to(shell, UP, buff=0.1, aligned_edge=LEFT),
                      label(rf"\${C['china_va']:.2f} \ made in China", font_size=22, color=CHINA).next_to(
                          shell, RIGHT, buff=0.2))
        foot = VGroup(
            label(rf"gross trade: \ the iPhone added \${C['deficit'] / 1e9:.1f}bn to America's {C['year']} "
                  r"deficit with China", font_size=20, color=TARIFF),
            label(rf"value added: \ the same trade shows an American surplus of \${C['va_surplus'] / 1e6:.0f}m",
                  font_size=20, color=GAIN),
            label(r"trade in tasks: \ a disruption anywhere stops the chain \ (Parts 63 and 66)", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.55)
        tag = published_tag(tables.XING_DETERT_2010.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Much of modern trade is not in finished goods but in tasks. <bookmark mark='a'/> The iPhone of 2009 was "
            "designed in California, built from parts made in Japan, Korea, Germany, Taiwan and America, and "
            "assembled in China, which added about six dollars and fifty cents to each phone. "
            "<bookmark mark='b'/> Yet every phone shipped from China counted as a Chinese export at its full "
            f"factory cost, about {C['total']:.0f} dollars: in gross terms, Yuqing Xing and Neal Detert "
            "calculated, the iPhone added "
            f"{C['deficit'] / 1e9:.1f} billion dollars to America's trade deficit with China that year. "
            "<bookmark mark='c'/> Counted by value added, China's share of each phone was its six dollars and "
            "fifty cents of assembly, and the same trade showed a small American surplus. "
            "<bookmark mark='d'/> Chains like this make countries more productive and more fragile: a factory "
            "closed by a flood or a pandemic stops production everywhere downstream, the subject of Parts "
            "sixty-three and sixty-six."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(flow.boxes[0]), FadeIn(flow.notes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in flow.boxes[1:]], *[GrowArrow(a) for a in flow.arrows],
                                  *[FadeIn(n) for n in flow.notes[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(GrowFromEdge(bar1, LEFT), FadeIn(lab1), FadeIn(foot[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(shell), FadeIn(lab2[0]), run_time=0.8)
            self.play(GrowFromEdge(sliver, RIGHT), FadeIn(lab2[1]), FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()
