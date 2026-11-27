from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403

COLS = {"China": CHINA, "Japan": BLUE, "United States": PRICE, "South Korea": ROBOT, "Germany": GREY_A}


class Robots(VoiceoverScene):
    def construct(self):
        card(self, 7, "Automation: the robots", "Who is buying the machines that replace work in factories?",
             "Chapter seven. Automation. The fastest-growing kind of machine is the industrial robot. Who buys them?",
             lit=("change",))
        self.installs()
        self.makers()
        self.density()

    def makers(self):
        Rb = R["robots"]
        hist = Rb["dom_hist"]
        items = [(k, v, CHINA if k != "about 2013-2022" else GREY_B, f"{v}%") for k, v in hist.items()]
        bars_ = vbars(items, base_y=-2.3, height=3.2, width=1.2, gap=0.6, x0=-5.4)
        ex = R["china"]["robots"]
        rows = hbars([("Japan", ex["Japan"][2025], BLUE, f"${ex['Japan'][2025]:.2f}bn"),
                      ("China", ex["China"][2025], CHINA, f"${ex['China'][2025]:.2f}bn (2015: ${ex['China'][2015]:.2f}bn)"),
                      ("Germany", ex["Germany"][2025], GREY_A, f"${ex['Germany'][2025]:.2f}bn"),
                      ("United States", ex["United States"][2025], PRICE, f"${ex['United States'][2025]:.2f}bn")],
                     max_value=2.0, x0=3.0, top=1.2, row=0.6, length=2.8, size=14, bar_h=0.36)
        h1 = tx("Chinese makers' share of China's robot market", 16, WHITE, bold=True).move_to([-3.4, 2.4, 0])
        h2 = tx("robot exports, 2025", 16, WHITE, bold=True).move_to([4.0, 2.4, 0])
        src = source("International Federation of Robotics, press releases of 24 September 2024 and 24 September 2026; UN "
                     "Comtrade, HS 847950", size=12)
        beat(self,
             "Who makes the robots China buys? <bookmark mark='a'/> For about a decade, Chinese makers sold around "
             f"{hist['about 2013-2022']} per cent of them; the rest came from foreign suppliers. "
             f"<bookmark mark='b'/> Then their share jumped: {hist['2023']} per cent in 2023, {hist['2024']} in 2024, "
             f"{hist['2025']} in 2025. <bookmark mark='c'/> And China has started exporting robots: "
             f"{ex['China'][2025]:.2f} billion dollars of them in 2025, against {ex['China'][2015]:.2f} billion in 2015, "
             f"though Japan, at {ex['Japan'][2025]:.2f} billion, still exports the most.",
             base=[h1, h2, rows.axis, src], steps=[bars_[0], VGroup(*bars_[1:]), rows])

    def installs(self):
        Rb = R["robots"]
        inst = Rb["inst"]
        ser = {k: ({y: v / 1e3 for y, v in inst[k].items() if y >= 2011}, COLS[k]) for k in COLS}
        ch = line_chart(ser, x=(2011, 2025), y=(0, 380), xticks=[2011, 2015, 2020, 2025], yticks=[0, 100, 200, 300],
                        yfmt=lambda v: f"{v:.0f}k", ylabel="industrial robots installed a year, thousands", width=8.6, height=4.4,
                        center=(-1.6, -0.45), nudge={"United States": 0.18, "Japan": 0.0, "South Korea": -0.15, "Germany": -0.3})
        arm = draw.robot_arm().scale(1.3).move_to([5.3, 1.6, 0])
        facts = VGroup(tx(f"world, 2025: more than {inst['World'][2025] / 1e3:.0f}k installed", 15, WHITE, bold=True),
                       tx(f"{Rb['stock']:.0f} million at work", 15, WHITE, bold=True),
                       tx(f"China: {100 * inst['China'][2025] / inst['World'][2025]:.0f}% of the world's", 15, CHINA, bold=True),
                       tx(f"Chinese makers: {Rb['china_dom']}% of China's market", 15, CHINA, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.9, -1.2, 0])
        src = source("International Federation of Robotics, World Robotics, via the AI Index Report 2026 and Our World in "
                     "Data (to 2024); IFR, 24 September 2026 (2025)", size=12)

        def wave(vo):
            if hasattr(arm, "upper") and hasattr(arm, "elbow"):
                self.play(Rotate(arm.upper, 0.5, about_point=arm.lower[0].get_end()), rate_func=there_and_back, run_time=1.5)

        beat(self,
             "Here are the industrial robots installed each year since 2011 in the five biggest markets. "
             f"<bookmark mark='a'/> China's line leaves the others behind: {inst['China'][2025] / 1e3:.0f} thousand robots "
             f"in 2025, {100 * inst['China'][2025] / inst['World'][2025]:.0f} per cent of the world's. <bookmark mark='b'/> "
             f"America installed about {inst['United States'][2025] / 1e3:.1f} thousand, passing Japan, which the IFR has "
             "called the world's predominant robot-making country. <bookmark mark='c'/> And the robots China installs are now mostly made in China: "
             f"Chinese makers sold {Rb['china_dom']} per cent of them. There are {Rb['stock']:.0f} million robots at work "
             f"in the world's factories, and the IFR expects installations to reach {Rb['fc2029'] / 1e3:.0f} thousand a "
             "year by 2029.",
             base=[ch.frame, arm, src], steps=[[ch.lines["China"], ch.labels["China"]],
                                               [ch.lines[k] for k in ("Japan", "United States", "South Korea", "Germany")] +
                                               [ch.labels[k] for k in ("Japan", "United States", "South Korea", "Germany")],
                                               facts], after=wave)

    def density(self):
        Rb = R["robots"]
        d = Rb["density"]
        order = sorted(d, key=lambda k: -d[k])
        items = [(k, d[k], {"China": CHINA, "United States": PRICE, "EU-27": BLUE}.get(k, ROBOT), f"{d[k]:,}") for k in order]
        rows = hbars(items, max_value=1100, x0=-1.6, top=2.0, row=0.6, length=7.0, size=17, bar_h=0.4)
        src = source("International Federation of Robotics, press release of 12 November 2026: robots per 10,000 "
                     "manufacturing employees, 2025", size=12)
        beat(self,
             "But China buys the most robots because it has the most factories. Divide by the number of factory workers. "
             f"<bookmark mark='a'/> South Korea has {d['South Korea']:,} robots for every ten thousand manufacturing "
             f"employees, Singapore {d['Singapore']}, Germany {d['Germany']}, Japan {d['Japan']}. "
             f"<bookmark mark='b'/> America has {d['United States']}, the European Union {d['EU-27']}, and China "
             f"{d['China']}, though China's has more than doubled in five years. Density measures how far automation has gone; the totals show where the "
             "buying is.",
             base=[rows.axis, head("Robot density, 2025: robots per 10,000 factory workers"), src],
             steps=[VGroup(*rows[:4]), VGroup(*rows[4:])])
