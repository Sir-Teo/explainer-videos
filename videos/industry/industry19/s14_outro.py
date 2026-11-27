from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        H, B, Bk, Rb = R["hook"], R["base"], R["backlog"], R["robots"]
        lines = [
            (f"Otis: new elevators {100 * H['ne_op'] / H['ne_sales']:.1f}% margin; service {100 * H['sv_op'] / H['sv_sales']:.0f}%",
             SERVICE),
            (f"the Works' maker: service {100 * B['svc_rev_share']:.0f}% of revenue, {100 * B['svc_profit_share']:.0f}% of profit; "
             f"worst year {100 * B['svc_sw']['worst_fall']:.0f}% against {100 * B['new_sw']['worst_fall']:.0f}%", SERVICE),
            ("the tender: when servicing is worth enough, machines are sold near cost", PRICE),
            (f"Caterpillar's backlog: ${Bk['cat'][0]:.0f}bn to ${Bk['cat'][2]:.0f}bn in under two years", MACHINE),
            (f"robots: {Rb['stock']:.0f} million at work; China installs most and now makes most of its own", ROBOT),
        ]
        g = VGroup(*[tx(t, 20, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.6:
                r_.scale_to_fit_width(12.6)
        beat(self,
             "So how do the machine makers earn more after the sale than at it? <bookmark mark='a'/> Because every "
             "machine sold joins an installed base that needs parts, service and repairs for years, at margins the "
             "factory never sees. <bookmark mark='b'/> That base is steadier than new sales, which swing with the "
             "capital-goods cycle. <bookmark mark='c'/> Makers know it, so they fight hard at the sale, and machines go "
             "cheap. <bookmark mark='d'/> The cycle is still the business's weather, and for Caterpillar, right now, it "
             "is a boom. "
             "<bookmark mark='e'/> And the newest machines, the robots, are being bought, and increasingly made, in China. "
             "The industry's old rule still holds: the company that sold the machine has the first claim on the decades "
             "of work it will need, and the best businesses here are the ones that never let that claim go.",
             base=[head("After the sale")], steps=list(g))

    def close(self):
        ex = draw.excavator(3.6, MACHINE).move_to([-3.6, 0.6, 0])
        lift = draw.elevator(3.4, floors=6, color=BLUE).move_to([3.2, 0.6, 0])
        nxt = tx("Next: Part 20, Pharmaceuticals", 26, PRICE, bold=True).move_to([0, -2.6, 0])
        with self.voiceover("Machines that work for decades, and the companies that keep them working: the excavator "
                            "that needs new tracks, the elevator that needs its inspection, the robot that needs its "
                            "software. The sale is the beginning of the business, not the end. Next time: "
                            "pharmaceuticals, where most of the cost is in the discovery.") as vo:
            self.play(FadeIn(ex), FadeIn(lift))
            self.play(Rotate(ex.boom, 0.35, about_point=ex.pivot.get_center()), lift.car.animate.set_y(lift.floor_y(5)),
                      rate_func=there_and_back, run_time=3)
            self.play(FadeIn(nxt))
        self.clear_scene()
