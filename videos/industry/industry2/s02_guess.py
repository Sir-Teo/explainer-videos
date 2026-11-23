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
            self.play(FadeIn(ask), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(a[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in a[1]], lag_ratio=0.25),
                      run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(b[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in b[1]], lag_ratio=0.25),
                      run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(c[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in c[1]], lag_ratio=0.2),
                      run_time=2)
            vo.wait_until("d")
            self.play(Indicate(VGroup(a[0], b[0], c[0]), color=I.ACCENT, scale_factor=1.06))
        self.clear_scene()
