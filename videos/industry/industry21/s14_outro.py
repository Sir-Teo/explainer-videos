from __future__ import annotations

from videos.industry.industry21.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        H, B, F, U = R["hook"], R["base"], R["fda"], R["run"]
        lines = [
            ("the surgeon chooses: skill and training tie the surgeon to a system", SURGEON),
            (f"the hospital buys: a robot for ${H['price'][0]:.1f}m to ${H['price'][1]:.1f}m, or placed and paid for by use", WHITE),
            (f"then the installed base pays: {B['recurring']}% of Intuitive's revenue recurs; GE HealthCare keeps "
             f"{100 * B['gehc_gm_services']:.0f}c of a service dollar", GOOD),
            (f"the regulator: about {F['k510_5']:,.0f} clearances by comparison a year, {F['pma_5']:.0f} new approvals", DEVICE),
            ("the payer sets the price, and where it buys for a nation, as in China, it sets it low", PAYER),
        ]
        g = VGroup(*[tx(t, 20, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.6:
                r_.scale_to_fit_width(12.6)
        beat(self,
             "So who is the customer? <bookmark mark='a'/> The surgeon, who chooses, and whose skill, once learned on one "
             "system, is costly to move. <bookmark mark='b'/> The hospital, which buys the machine, or lets the maker put it "
             "there and pays by the operation. <bookmark mark='c'/> And then the installed base, which pays its maker for "
             "years: instruments, service and tests, bought again and again. <bookmark mark='d'/> Behind them the "
             "regulator, which lets most devices in by comparison with the last, so that devices improve in small steps "
             "and rivals follow fast. <bookmark mark='e'/> And the payer, who in America pays through insurers and "
             "governments, and in China increasingly buys for the nation and names the price. A device company sells to "
             "all of them, and earns most where the machine is already in place.",
             base=[head("The three customers")], steps=list(g))

    def close(self):
        bot = draw.surgical_robot(2.4).move_to([0, 0.6, 0])
        nxt = tx("Next: Part 22, Consumer Goods", 26, PRICE, bold=True).move_to([0, -2.4, 0])
        with self.voiceover("A machine sold once, and an operation billed a thousand times: medical technology earns where "
                            "the surgeon's hands and the hospital's budget meet, and it sells to people who rarely pay the "
                            "bill themselves. Next time: consumer goods, and why a company "
                            "can charge double for soap for a hundred years.") as vo:
            self.play(FadeIn(bot, shift=UP * 0.2), run_time=1.5)
            for k in range(3):
                self.play(*[a.animate.shift(DOWN * 0.08 * (1 if (i + k) % 2 else -1)) for i, a in enumerate(bot.arms)], run_time=0.6)
            self.play(FadeIn(nxt))
        self.clear_scene()
