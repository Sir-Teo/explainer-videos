from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.three()
        self.answers()

    def three(self):
        P, U, D = R["plant"], R["run"], R["dealers"]
        items = [
            (VGroup(draw.factory(1.3, MAKER)), "Plants cost the same full or empty",
             f"break-even near {100 * P['be_share']:.0f}% of capacity; demand can fall a third in two years"),
            (VGroup(draw.suv(0.9, YOU), draw.suv(0.9, RIVAL)).arrange(RIGHT, buff=0.1), "Every maker is tempted to fill its own plant",
             f"so all discount: {('-' if U['table']['discount|discount'][0] < 0 else '')}${abs(U['table']['discount|discount'][0]):.0f}m each, against "
             f"-${abs(U['table']['hold|hold'][0]):.0f}m if all held"),
            (VGroup(draw.wrench(0.6), draw.battery_pack(1.1, color=FINANCE)).arrange(RIGHT, buff=0.15), "The money is around the car, not in it",
             f"service and finance: {100 * (D['gp_share']['ps'] + D['gp_share']['fi']):.0f}% of a dealer's gross profit; lenders; luxury"),
        ]
        rows = VGroup()
        for i, (icon, head, sub) in enumerate(items):
            y = 1.9 - 1.75 * i
            icon.move_to([-5.4, y, 0])
            t_ = VGroup(tx(head, 21, PRICE, bold=True), tx(sub, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-4.3, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(icon, t_))
        head = tx("Why it is so hard to make money making cars", 24, WHITE, bold=True).to_edge(UP, buff=0.3)
        with self.voiceover(
            "So, why is it so hard to make money making the most desired product of the century? Three reasons, all "
            "measured in this film. <bookmark mark='a'/> First, a car plant costs nearly the same whether it is full or "
            "half empty, while the demand for cars can collapse in two years. Profit lives on the steep part of the line, "
            "and the line keeps moving. <bookmark mark='b'/> Second, because every maker's plant costs the same full or "
            "empty, every maker is tempted to fill its own: in the showroom duel discounting always pays for one, and "
            "costs everyone; in China the duel is playing out across a whole country. <bookmark mark='c'/> Third, the carmaker "
            "is above all a buyer and an assembler of other people's work, and much of the money is made around the car "
            "rather than in it: in fixing it, in lending against it, and in the few brands that can charge for "
            "exclusivity."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(r_[0]) for r_ in rows], FadeIn(ghost(*[r_[1][0] for r_ in rows], opacity=0.35)))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[1], shift=RIGHT * 0.15))
        self.clear_scene()

    def answers(self):
        qs = [("What is sold?", "a machine of some 30,000 parts, many made by others, and the loan, the service and the parts after it"),
              ("How is it made?", "stamped, welded, painted and assembled on a moving line, in plants that must stay busy"),
              ("Where does the dollar go?", "mostly to suppliers; a few cents to the maker; the dealer earns on service and finance"),
              ("Why does it stay there?", "plants cost the same full or empty, so makers fight for volume; brands like Ferrari choose not to"),
              ("What moves it?", "the battery, China's makers and their exports, tariffs, and the cycle of the economy")]
        rows = VGroup()
        for i, (q, a) in enumerate(qs):
            rows.add(VGroup(tx(q, 20, PRICE, bold=True), tx(a, 16, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
                     .move_to([-6.0, 2.3 - 1.05 * i, 0], aligned_edge=LEFT))
        with self.voiceover(
            "Automobiles, in five answers. <bookmark mark='a'/> What is sold is a machine of some thirty thousand parts, "
            "many of them made by other companies, and then the loan, the servicing and the spare parts that follow it. "
            "<bookmark mark='b'/> It is made by stamping, welding, painting and assembly on a moving line, in plants that "
            "must stay busy to pay. <bookmark mark='c'/> The dollar goes mostly to the suppliers, a few cents to the "
            "maker, and the dealer earns its living on service and finance. <bookmark mark='d'/> It stays that way because "
            "plants cost the same full or empty, so makers fight for volume; only a few brands, like Ferrari, choose not "
            "to. <bookmark mark='e'/> And what moves it now are the battery, China's makers and their exports, the tariffs "
            "raised against them, and, as always, the economy. Next time: aircraft, and why there are only two makers of "
            "large airliners."
        ) as vo:
            head = tx("Automobiles, in five answers", 24, WHITE, bold=True).to_edge(UP, buff=0.3)
            self.play(FadeIn(head), *[FadeIn(r_[0].copy().set_opacity(0.25)) for r_ in rows])
            for m_, r_ in zip("abcde", rows):
                vo.wait_until(m_)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
