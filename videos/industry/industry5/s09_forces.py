from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403

# Porter's five forces, and how each bears on two industries (this film's reading; Damodaran's returns, 2025)
FORCES = [("Rivals inside", "how hard the firms already there compete", UP * 0.0),
          ("New entrants", "how easily others can come in", RIGHT),
          ("Substitutes", "other ways to meet the same need", DOWN),
          ("Buyers", "how much power customers have to push prices down", LEFT),
          ("Suppliers", "how much power suppliers have to push costs up", UP)]
AIR = ["fares cut to fill seats (Part 4)", "planes can be leased; new airlines keep starting",
       "a train, a car, a video call", "travellers compare every fare in seconds",
       "two plane makers, a few engine makers, unionized crews"]
TOB = ["a few firms that rarely fight on price", "advertising limits and brands lock in the leaders",
       "few, so far", "smokers are loyal to a brand", "tobacco leaf from many farmers"]


class Forces(VoiceoverScene):
    def construct(self):
        card(self, 11, "Five forces", "Who else takes a share of an industry's profit?",
             "Chapter eleven. Five forces.", lit=("moat", "who"))
        keep = draw.castle(1.7, moat=0.3).move_to([0, -0.35, 0])
        pos = {"New entrants": np.array([4.3, -0.2, 0]), "Substitutes": np.array([0, -2.75, 0]),
               "Buyers": np.array([-4.3, -0.2, 0]), "Suppliers": np.array([0, 2.55, 0])}
        boxes, arrows = VGroup(), VGroup()
        for name, what, _ in FORCES[1:]:
            p = pos[name]
            b = VGroup(tx(name, 22, ENTRANT, bold=True), tx(what, 14, GREY_B)).arrange(DOWN, buff=0.06).move_to(p)
            boxes.add(b)
            start = p + (keep.get_center() - p) * 0.28
            end = keep.get_center() + (p - keep.get_center()) * 0.42
            arrows.add(Arrow(start, end, buff=0.1, color=ENTRANT, stroke_width=5, max_tip_length_to_length_ratio=0.2))
        rivals = VGroup(tx("Rivals inside", 20, GOLD, bold=True), tx(FORCES[0][1], 14, GREY_B)).arrange(DOWN, buff=0.05)
        rivals.next_to(keep, DOWN, buff=0.15)
        head = tx("Michael Porter, Harvard Business Review, 1979", 18, GREY_B).to_corner(UL, buff=0.35)
        with self.voiceover(
            "A moat keeps out one kind of attacker: newcomers. But a castle's treasure can leak away in other "
            "directions too. <bookmark mark='a'/> In 1979 Michael Porter, a young professor at Harvard Business "
            "School, drew the picture that business schools still teach. An industry's profit, he argued, is "
            "squeezed by five forces. <bookmark mark='b'/> The rivalry among the firms already inside. "
            "<bookmark mark='c'/> The threat of new entrants. <bookmark mark='d'/> The threat of substitutes, other "
            "ways of meeting the same need. <bookmark mark='e'/> The power of buyers to push prices down. "
            "<bookmark mark='f'/> And the power of suppliers to push costs up. Every one of them can drain the "
            "treasure, and the industries with lasting returns are those where all five are weak."
        ) as vo:
            self.play(FadeIn(keep, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(FadeIn(rivals))
            for k, m in enumerate("cdef"):
                vo.wait_until(m)
                self.play(FadeIn(boxes[k], shift=-arrows[k].get_vector() * 0.1), GrowArrow(arrows[k]), run_time=0.9)
        self.play(FadeOut(head))
        self.compare(keep, boxes, arrows, rivals)

    def compare(self, keep, boxes, arrows, rivals):
        D = {d["name"]: d for d in R["roc"]["industries"]}
        air, tob = D["Air Transport"], D["Tobacco"]
        grp = VGroup(keep, boxes, arrows, rivals)
        self.play(grp.animate.scale(0.62).move_to([-3.4, -0.1, 0]))
        right = VGroup()
        rows = []
        for k, (name, _, _) in enumerate(FORCES):
            a = tx(AIR[k], 15, COST_)
            t = tx(TOB[k], 15, RET)
            n_ = tx(name, 16, GOLD, bold=True)
            rows.append(VGroup(n_, a, t))
        head = VGroup(tx("Airlines", 22, COST_, bold=True), tx("Tobacco", 22, RET, bold=True))
        y0 = 2.4
        head[0].move_to([2.2, y0 + 0.6, 0])
        head[1].move_to([5.3, y0 + 0.6, 0])
        for k, r_ in enumerate(rows):
            y = y0 - 0.85 * k
            r_[0].move_to([3.75, y + 0.22, 0])
            r_[1].move_to([2.2, y - 0.08, 0])
            r_[2].move_to([5.3, y - 0.08, 0])
            for t_ in r_[1:]:
                if t_.width > 2.9:
                    t_.scale_to_fit_width(2.9)
            right.add(r_)
        res = VGroup(tx(f"return on capital: {100 * air['roc']:.0f}%", 20, COST_, bold=True).move_to([2.2, -2.15, 0]),
                     tx(f"return on capital: {100 * tob['roc']:.0f}%", 20, RET, bold=True).move_to([5.3, -2.15, 0]))
        note = tx("the forces are this film's reading; the returns are Damodaran's, for 2025", 15, GREY_C).to_edge(
            DOWN, buff=0.3)
        with self.voiceover(
            "Hold two industries up to it. <bookmark mark='a'/> Airlines face all five at full strength. Their rivals "
            "cut fares to fill empty seats, as Part 4 showed. New airlines keep starting, because planes can be "
            "leased. Trains, cars and video calls are substitutes. Travellers compare every fare in seconds. And "
            "the suppliers are strong: two companies make almost every large airliner, and crews are unionized. "
            "<bookmark mark='b'/> Tobacco faces almost none of them. A few firms that rarely fight on price; brands "
            "and advertising limits that lock the leaders in; few substitutes; loyal customers; and a leaf bought "
            f"from many farmers. <bookmark mark='c'/> Airlines earned {100 * air['roc']:.0f} percent on their "
            f"capital in 2025, by Damodaran's count; tobacco {100 * tob['roc']:.0f}. Buffett's Kitty Hawk joke and "
            "Porter's diagram are saying the same thing."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), FadeIn(r_[1])) for r_ in rows], lag_ratio=0.4),
                      run_time=4.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[2]) for r_ in rows], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(res), FadeIn(note))
        self.clear_scene()
