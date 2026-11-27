from __future__ import annotations

from videos.industry.industry26.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        U = R["run"]
        B = R["bond"]
        lines = [
            ("value is income over a rate: a one-point rise at 5% takes a sixth off the price", RATE),
            (f"income moves more than rent: the Works' office lost a third of its rent and {100 * (1 - U['office']['now']['noi'] / U['office']['then']['noi']):.0f}% of its income", INCOME),
            (f"the rate moves on its own: Realty Income bought at {B['o_yield'][2021]:.1f}% in 2021 and {B['o_yield'][2024]:.1f}% in 2024", VALUE),
            ("the lease is the asset: long promises from strong tenants are worth most", SHOP),
            (f"the loan decides who loses; offices emptied (BXP {get('bxp.occ.2019'):.1f}% let to {get('bxp.occ'):.1f}%) as warehouses re-let at +{get('pld.rentchange'):.0f}%", LOAN),
        ]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So what is a building worth? <bookmark mark='a'/> Its income divided by a rate, and at low rates small changes "
             "in the rate move the price a great deal. <bookmark mark='b'/> Its income moves more than its rent, because its "
             "costs do not leave with its tenants. <bookmark mark='c'/> The rate moves with the whole market for money, which "
             "is why a building's price can fall a third while nothing about it changes. <bookmark mark='d'/> What a landlord "
             "really owns is its leases: who has promised to pay, how much and for how long. <bookmark mark='e'/> And when the "
             "income and the rate both move against a building, its loan decides who takes the loss: the owner first, then the "
             "lender. Warehouses filled while offices emptied, and the same arithmetic made one richer and left the other worth less than its loan.",
             base=[head("Income over a rate")], steps=list(g))

    def close(self):
        tower = draw.office_tower(1.0).move_to([-4.6, -0.6, 0])
        draw.light(tower.windows, 0.87)
        shed = draw.warehouse(2.2).move_to([-1.4, -0.4, 0])
        mall = draw.mall(2.0).move_to([1.8, -0.4, 0])
        mast = draw.cell_tower(1.8).move_to([4.8, -0.2, 0])
        nxt = tx("Next: Part 27, Shipping and Ports", 26, VALUE, bold=True).move_to([0, -2.8, 0])
        with self.voiceover("An office, a shed, a mall and a mast: four bonds with roofs, priced by the same formula and "
                            "ruined or enriched by its two numbers. Next time, Act Five, moving: shipping and ports, and how "
                            "moving a tonne across an ocean became nearly free."):
            self.play(LaggedStart(FadeIn(tower), FadeIn(shed), FadeIn(mall), FadeIn(mast), lag_ratio=0.4), run_time=2.4)
            self.play(FadeIn(nxt))
        self.clear_scene()
