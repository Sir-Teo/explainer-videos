from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403


class Panels(VoiceoverScene):
    def construct(self):
        card(self, 6, "Surveys and panels", "Where do the commercial numbers come from, and what can they not see?",
             "Chapter six. Surveys and panels.", lit=("unit",))
        till = VGroup(RoundedRectangle(corner_radius=0.08, width=1.4, height=0.9, stroke_width=0, fill_color="#2E3645",
                                       fill_opacity=1),
                      Rectangle(width=1.0, height=0.3, stroke_width=0, fill_color="#7BD88F", fill_opacity=0.8).shift(UP * 0.15),
                      Line(LEFT * 0.5 + DOWN * 0.25, RIGHT * 0.5 + DOWN * 0.25, stroke_color=GREY_B, stroke_width=3))
        kinds = [(VGroup(till, tx("scan", 14, GREY_A)).arrange(DOWN, buff=0.08), "Scanner panels",
                  "every barcode at the tills of the shops that share their data",
                  "misses shops that do not share, vending machines, home and office delivery"),
                 (VGroup(draw.house(0.7, color=STONE), draw.person(0.5, color=STONE)).arrange(RIGHT, buff=0.1),
                  "Household panels", "families who record what they buy",
                  "people forget; the families who agree to it are not quite like everyone else"),
                 (VGroup(RoundedRectangle(corner_radius=0.08, width=1.1, height=0.7, stroke_width=0, fill_color="#2B4C9B",
                                          fill_opacity=1), Rectangle(width=1.1, height=0.12, stroke_width=0,
                                                                     fill_color="#0E1117", fill_opacity=1).shift(UP * 0.12)),
                  "Card and app data", "what cardholders of one bank or one app spend",
                  "cash, other banks and other apps are invisible"),
                 (VGroup(RoundedRectangle(corner_radius=0.04, width=0.6, height=0.8, stroke_width=0, fill_color="#E8E4DA",
                                          fill_opacity=1), draw.factory(0.6, color=FACTORY)).arrange(RIGHT, buff=0.1),
                  "Surveys of companies", "what firms report to the statistical office or a trade body",
                  "late, and filed by what the plant mainly makes")]
        rows = VGroup()
        for pic, head, sees, misses in kinds:
            pic.scale_to_fit_height(min(pic.height, 0.75))
            t_ = VGroup(tx(head, 23, WHITE, bold=True), tx("sees: " + sees, 16, RETAIL), tx("misses: " + misses, 16, "#E8554E")
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            rows.add(VGroup(pic, t_).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.35, 0])
        for r_ in rows:
            r_[0].move_to([rows.get_left()[0] + 0.7, r_.get_y(), 0])
            r_[1].next_to(r_[0], RIGHT, buff=0.4).align_to(rows[0][1], LEFT)
        if rows.width > 13.4:
            rows.scale_to_fit_width(13.4)
        head = tx("Every source is a window, not the whole house", 26, GOLD, bold=True).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Most market numbers you read come from firms that sell data, and each of them looks through one "
            "window. <bookmark mark='a'/> Scanner panels collect every barcode beeped at the tills of the shops "
            "that agree to share their data. They see supermarket bottled water in fine detail, and they miss "
            "vending machines, and the five-gallon jugs delivered to offices. <bookmark mark='b'/> Household panels "
            "ask families to record what they buy. People forget, and the families willing to do it are not quite "
            "like everyone else. <bookmark mark='c'/> Card and app data see what one bank's or one app's customers "
            "spend: never the cash, never the other banks. <bookmark mark='d'/> And surveys of companies, by "
            "statistical offices or trade bodies, are thorough and late, and file each plant by what it mainly "
            "makes. When two firms' estimates of the same market differ by a factor of two, the first question is "
            "not who is wrong. It is which window each of them was looking through."
        ) as vo:
            self.play(FadeIn(head))
            for r_, m in zip(rows, "abcd"):
                vo.wait_until(m)
                self.play(FadeIn(r_[0], scale=0.8), FadeIn(r_[1], shift=RIGHT * 0.15))
        self.clear_scene()
