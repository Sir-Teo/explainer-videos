from __future__ import annotations

from videos.industry.industry21.common import *  # noqa: F403


class Boom(VoiceoverScene):
    def construct(self):
        card(self, 7, "A new procedure: pulsed field ablation", "What happens when a better way to do an operation arrives?",
             "Chapter seven. A new procedure. Devices usually improve by small steps. Sometimes a new way of doing an "
             "operation arrives, and the market moves within two years.", lit=("change",))
        self.heart()
        self.sales()
        self.cannibal()
        self.watchman()

    def heart(self):
        hrt = VGroup(Circle(radius=1.2, stroke_color=BAD, stroke_width=4, fill_color=BAD, fill_opacity=0.25),
                     Circle(radius=0.45, stroke_color=BAD, stroke_width=3).shift(UP * 0.35 + LEFT * 0.35)).move_to([-4.0, 0.2, 0])
        cath = CubicBezier([-6.6, -2.4, 0], [-5.8, -1.0, 0], [-4.8, -0.4, 0], [-4.35, 0.55, 0], stroke_color=DEVICE, stroke_width=5)
        zap = VGroup(*[Line([-4.35, 0.55, 0], [-4.35 + 0.45 * np.cos(a), 0.55 + 0.45 * np.sin(a), 0], stroke_color=PRICE,
                            stroke_width=3) for a in np.linspace(0, TAU, 9)[:-1]])
        t = VGroup(tx("atrial fibrillation: an irregular heartbeat", 18, WHITE, bold=True),
                   tx("ablation: a catheter, threaded into the heart, scars the tissue", 16, GREY_A),
                   tx("that sets off the irregular rhythm", 16, GREY_A),
                   tx("old ways: heat (radiofrequency) or cold (cryoablation)", 16, GREY_A),
                   tx("new way: short pulses of electric field", 16, PRICE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([2.4, 0.4, 0])
        src = source("Boston Scientific Corporation, Form 10-K 2025: Electrophysiology", size=12)
        beat(self,
             "Atrial fibrillation is an irregular heartbeat. <bookmark mark='a'/> One treatment is "
             "ablation: a doctor threads a catheter through a vein into the heart and destroys the small areas of tissue "
             "that set off the irregular rhythm. <bookmark mark='b'/> For years that meant heat or cold. "
             "<bookmark mark='c'/> Pulsed field ablation uses very short pulses of electric field instead. Boston "
             "Scientific's version is called Farapulse; its report dates the launch to 2024.",
             base=[src], steps=[[hrt, t[0]], [cath, t[1], t[2], t[3]], [zap, t[4]]])

    def sales(self):
        B = R["boom"]
        ep = B["ep"]
        items = [(str(y), v / 1e3, PRICE, f"${v / 1e3:.1f}bn") for y, v in sorted(ep.items())]
        bars_ = vbars(items, base_y=-2.3, height=3.8, width=1.4, gap=1.0, x0=-4.8)
        rev = VGroup(tx("Boston Scientific's total revenue", 16, GREY_A),
                     tx(f"${B['bsx_rev'][2023]:.1f}bn (2023) to ${B['bsx_rev'][2025]:.1f}bn (2025)", 20, WHITE, bold=True)
                     ).arrange(DOWN, buff=0.08).move_to([3.9, 1.4, 0])
        q = VGroup(tx("'rapid conversion from legacy", 16, PRICE), tx("treatment modalities to PFA'", 16, PRICE)
                   ).arrange(DOWN, buff=0.06).move_to([3.9, -0.4, 0])
        src = source("Boston Scientific Corporation, Form 10-K 2025: Electrophysiology net sales", size=12)
        beat(self,
             f"Look at Boston Scientific's electrophysiology sales. <bookmark mark='a'/> {ep[2023] / 1e3:.1f} billion "
             f"dollars in 2023. <bookmark mark='b'/> {ep[2024] / 1e3:.1f} billion in 2024. <bookmark mark='c'/> "
             f"{ep[2025] / 1e3:.1f} billion in 2025, four times as much in two years. <bookmark mark='d'/> The company's "
             f"whole revenue went from {B['bsx_rev'][2023]:.1f} to {B['bsx_rev'][2025]:.1f} billion, and its report "
             "describes a rapid conversion from the old ways to the new.",
             base=[head("Boston Scientific: electrophysiology sales"), src], steps=[bars_[0], bars_[1], bars_[2], [rev, q]])

    def cannibal(self):
        B = R["boom"]
        c = stat_cards([(f"${B['impair']}m", "Boston Scientific's 2024 write-downs, mostly of its cryoablation businesses", BAD),
                        (f"+{B['crhf']}%", "Medtronic's heart-rhythm sales, fiscal 2026, with strong growth in pulsed field ablation", DEVICE)],
                       y=0.6, size=44, span=12)
        note = tx("A new procedure replaces old products, including the maker's own.", 19, WHITE, bold=True).move_to([0, -1.6, 0])
        src = source("Boston Scientific Corporation, Form 10-K 2025; Medtronic plc, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "A new procedure replaces old products, including the maker's own. <bookmark mark='a'/> In 2024 Boston "
             f"Scientific wrote down {B['impair']} million dollars of intangible assets, mostly from cryoablation "
             "companies it had bought, because Farapulse was taking their place. <bookmark mark='b'/> Rivals followed: "
             f"Medtronic's heart-rhythm sales grew {B['crhf']} per cent in its fiscal 2026, with strong growth in its own "
             "pulsed field products. <bookmark mark='c'/> In devices, an advantage lasts until the next procedure, not until a patent "
             "date.",
             base=[src], steps=[c[0], c[1], note])

    def watchman(self):
        B = R["boom"]
        w = B["watchman"]
        items = [(str(y), v / 1e3, DEVICE, f"${v / 1e3:.2f}bn") for y, v in sorted(w.items())]
        bars_ = vbars(items, base_y=-2.3, height=3.0, width=1.2, gap=0.8, x0=-3.6)
        t = VGroup(tx("Watchman: closes off a pouch of the heart", 18, DEVICE, bold=True),
                   tx("for patients with atrial fibrillation at risk of stroke,", 16, GREY_A),
                   tx("an alternative to blood-thinning drugs", 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.0, 1.0, 0])
        src = source("Boston Scientific Corporation, Form 10-K 2025: Watchman net sales", size=12)
        beat(self,
             "The same patients bring more business. <bookmark mark='a'/> Boston Scientific's Watchman closes off the left "
             "atrial appendage, a pouch of the heart, in patients with atrial fibrillation at risk of stroke, as an "
             "alternative to blood thinners. <bookmark mark='b'/> Its sales rose from "
             f"{w[2023] / 1e3:.2f} billion dollars in 2023 to {w[2025] / 1e3:.2f} billion in 2025. A device company grows by "
             "finding procedures, and then the patients for them.",
             base=[head("Boston Scientific: Watchman sales"), src], steps=[t, bars_])
