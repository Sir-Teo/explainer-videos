from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403

COLS = {"Amazon": "#F2A65A", "Walmart": "#7EC8F5", "UnitedHealth": "#7BD88F", "Apple": "#E8EAED",
        "McKesson": "#4FD1C5", "NVIDIA": "#A3D977", "Alphabet": "#F2C14E", "Microsoft": "#8FB4FF", "Meta": "#B58CFF"}


def ranking(title, items, fmt, width=3.4, size=19):
    top = max(v for _, v in items)
    rows = VGroup()
    for name, v in items:
        bar = Rectangle(width=max(width * v / top, 0.05), height=0.3, fill_color=COLS[name], fill_opacity=0.85,
                        stroke_width=0)
        lab = VGroup(T(name, size, I.TEXT), TB(fmt(v), size, COLS[name])).arrange(RIGHT, buff=0.15)
        rows.add(VGroup(lab, bar).arrange(DOWN, aligned_edge=LEFT, buff=0.06))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    return VGroup(TB(title, 24, I.ACCENT), rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3)


class Guess(VoiceoverScene):
    def construct(self):
        card(self, 1, "Which is the biggest business?", "Biggest by what?",
             "Chapter one. Which is the biggest business?", lit=("unit",))
        C = R["companies"]
        a = ranking("By sales", C["by_sales"], lambda v: f"${v:.0f}bn")
        b = ranking("By operating profit", C["by_profit"], lambda v: f"${v:.0f}bn")
        c = ranking("By employees", C["by_jobs"], lambda v: f"{v / 1e6:.2f}m" if v >= 1e6 else f"{v / 1e3:.0f}k")
        g = VGroup(a, b, c).arrange(RIGHT, buff=0.7, aligned_edge=UP).move_to(DOWN * 0.15)
        if g.width > 13.2:
            g.scale_to_fit_width(13.2)
        ask = T("Before each column appears: who is first?", 22, I.DIM).to_edge(UP, buff=0.4)
        src = source("Companies' 10-Ks, fiscal years ending June 2025 to March 2026 (employees: latest 10-K); SEC structured data", size=14)
        with self.voiceover(
            "Start with a question that sounds simple. Which is the biggest business in America? Make a guess before "
            "each answer appears. <bookmark mark='a'/> By sales, the largest companies listed in the United States "
            "are Amazon, at 717 billion dollars in 2025, then Walmart, UnitedHealth, the health insurer, Apple, and a "
            "company many people have never heard of: McKesson, which distributes medicines. <bookmark mark='b'/> By "
            "profit, the list is completely different: Apple, NVIDIA, Alphabet and Microsoft, each with around 130 "
            "billion dollars of operating profit, then Meta and Amazon. <bookmark mark='c'/> And by the number of "
            "people they employ, different again: Walmart, with about 2.1 million, then Amazon, with 1.6 million. "
            "NVIDIA, the second most profitable, employs about 42 thousand. <bookmark mark='d'/> Three measures, "
            "three answers. The same is true of whole industries, and the rest of this part is about which measure "
            "tells you what."
        ) as vo:
            icons = VGroup(draw.coin_stack(5, 0.14), draw.coin_stack(3, 0.14, color=I.PROFIT),
                           draw.crowd(3, 0.3, cols=3))
            for ic, col_ in zip(icons, (a, b, c)):
                ic.next_to(col_[0], RIGHT, buff=0.2)

            def show(col_, ic):
                return AnimationGroup(FadeIn(col_[0]), FadeIn(ic, shift=DOWN * 0.1), LaggedStart(*[
                    AnimationGroup(FadeIn(r[0], shift=RIGHT * 0.1), GrowFromEdge(r[1], LEFT)) for r in col_[1]],
                    lag_ratio=0.25))
            self.play(FadeIn(ask), FadeIn(src))
            vo.wait_until("a")
            self.play(show(a, icons[0]), run_time=2)
            vo.wait_until("b")
            self.play(show(b, icons[1]), run_time=2)
            vo.wait_until("c")
            self.play(show(c, icons[2]), run_time=2)
            vo.wait_until("d")
            # the same company, three places
            names = [[n for n, _ in C[k]] for k in ("by_sales", "by_profit", "by_jobs")]
            links = VGroup()
            for nm in ("Amazon", "Apple", "Walmart"):
                rows_ = [col_[1][lst.index(nm)] if nm in lst else None for col_, lst in zip((a, b, c), names)]
                for r0, r1 in zip(rows_, rows_[1:]):
                    if r0 is None or r1 is None:  # only between neighbouring columns
                        continue
                    p0, p1 = r0.get_right() + RIGHT * 0.08, r1.get_left() + LEFT * 0.08
                    links.add(CubicBezier(p0, p0 + RIGHT * 0.4, p1 + LEFT * 0.4, p1, stroke_color=COLS[nm],
                                          stroke_width=3, stroke_opacity=0.85))
            self.play(Indicate(VGroup(a[0], b[0], c[0]), color=I.ACCENT, scale_factor=1.06),
                      LaggedStart(*[Create(l_) for l_ in links], lag_ratio=0.3), run_time=2.0)
        self.clear_scene()
