from __future__ import annotations

from videos.industry.industry21.common import *  # noqa: F403


class China(VoiceoverScene):
    def construct(self):
        card(self, 9, "China's procurement", "What happens when the payer buys for a whole country?",
             "Chapter nine. China's procurement. In America the three customers bargain separately. In China, increasingly, "
             "the state buys for everyone.", lit=("dollar", "change"))
        self.where()
        self.vbp()
        self.effects()
        self.robots()

    def where(self):
        W = R["where"]
        wm = draw.world_map(width=11.0).move_to([0, 0.2, 0])
        pos = {"United States": (-98, 39), "Europe": (10, 50), "Asia": (110, 30), "elsewhere": (-55, -15)}
        cols = {"United States": DEVICE, "Europe": IMAGING, "Asia": PRICE, "elsewhere": GOOD}
        steps = []
        for k, v in W.items():
            c = Circle(radius=0.012 * v ** 0.5, stroke_color=cols[k], stroke_width=2, fill_color=cols[k], fill_opacity=0.45).move_to(wm.p(*pos[k]))
            lab = tx(f"{k}: {v:,}", 16, cols[k], bold=True).next_to(c, DOWN, buff=0.1)
            steps.append([c, lab])
        src = source("Intuitive Surgical, Inc., Form 10-K 2025: da Vinci installed base by region", size=12)
        beat(self,
             "First, where the robots are. Of Intuitive's robots at the end of 2025, <bookmark mark='a'/> "
             f"{W['United States']:,} were in the United States, more than half, <bookmark mark='b'/> {W['Europe']:,} in "
             f"Europe, <bookmark mark='c'/> {W['Asia']:,} in Asia <bookmark mark='d'/> and {W['elsewhere']:,} elsewhere. "
             "Intuitive's own explanation for America's lead is that American patients can choose their provider and "
             "their treatment, that the way operations are paid for there supports new techniques, and that it invested "
             "there first. Elsewhere the buyer is more often a government, and governments buy differently.",
             base=[wm, head("da Vinci robots installed, end of 2025"), src], steps=steps)

    def vbp(self):
        wm = draw.world_map(width=7.0).move_to([-3.2, 0.6, 0])
        dot = Dot(wm.p(104, 35), radius=0.14, color=BAD)
        q = quote(["'China has implemented a volume-based procurement process designed to",
                   "decrease prices for medical devices and other products.'"], "Stryker Corporation, Form 10-K 2025",
                  size=16, width=6.2).move_to([3.6, 1.4, 0])
        how = bullets(["the state buys for many hospitals at once", "in volume, for a lower price"], size=17,
                      head="volume-based procurement").move_to([3.6, -1.2, 0])
        src = source("Stryker Corporation, Form 10-K 2025", size=12)
        beat(self,
             "China's government has been buying medicines and devices in bulk. <bookmark mark='a'/> Stryker's report puts "
             "it plainly: China has implemented a volume-based procurement process designed to decrease prices for medical "
             "devices. <bookmark mark='b'/> Instead of each hospital bargaining alone, the state buys for many hospitals at "
             "once, in volume, for a lower price. The surgeon and the hospital still "
             "use the device; the price is set further up.",
             base=[wm, dot, src], steps=[q, how])

    def effects(self):
        q1 = quote(["'Lower sales in China were due to the impact of challenging market conditions,",
                    "including the impact of volume-based procurement programs.'"], "Abbott Laboratories, Form 10-K 2025, on "
                   "its Core Laboratory diagnostics", size=15, width=11.0).move_to([0, 1.6, 0])
        q2 = quote(["'... increased competition from local companies and the prevalence of Volume Based Procurement",
                    "policies, both of which have impacted our orders and revenues and may continue to do so.'"],
                   "GE HealthCare Technologies, Form 10-K 2025", size=15, width=11.0).move_to([0, -0.6, 0])
        src = source("Abbott Laboratories and GE HealthCare Technologies Inc., Forms 10-K 2025", size=12)
        beat(self,
             "The foreign makers feel it in their accounts. <bookmark mark='a'/> Abbott says its diagnostics sales in China "
             "fell, among other things because of volume-based procurement. <bookmark mark='b'/> GE HealthCare names two "
             "forces in China: procurement by volume, and competition from local companies, which it says have both cut "
             "into its orders and revenue. A buyer that pools a nation's demand can name its price, and a home-grown "
             "maker that can meet it wins the volume.",
             base=[src], steps=[q1, q2])

    def robots(self):
        C = R["china"]
        bots = VGroup(*[draw.surgical_robot(0.55) for _ in range(12)]).arrange_in_grid(2, 6, buff=0.25).move_to([-3.2, 0.6, 0])
        q = tx(f"China's 2023 quota: {C['quota']} new surgical robots, from any maker", 19, PRICE, bold=True).move_to([0, -1.4, 0])
        q2 = tx("since 2022, several provinces cap what hospitals may charge for robotic surgery", 17, BAD, bold=True).move_to([0, -2.1, 0])
        side = VGroup(tx("Even the robot is rationed.", 20, WHITE, bold=True)).move_to([3.4, 1.0, 0])
        src = source("Intuitive Surgical, Inc., Form 10-K 2025", size=12)
        beat(self,
             "Even the robot is rationed. <bookmark mark='a'/> China's health commission sets a quota for large medical "
             f"equipment: its 2023 quota allowed the sale of {C['quota']} new surgical robots, from Intuitive or anyone "
             "else. <bookmark mark='b'/> And since 2022 several provinces have limited what hospitals may charge patients "
             "for robotic surgery, which Intuitive says has cut both the number of operations there and its instrument "
             "prices.",
             base=[bots, side, src], steps=[q, q2])
