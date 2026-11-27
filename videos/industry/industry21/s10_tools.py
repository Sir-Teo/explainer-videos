from __future__ import annotations

from videos.industry.industry21.common import *  # noqa: F403


class Tools(VoiceoverScene):
    def construct(self):
        card(self, 8, "Picks and shovels", "Who sells to the laboratories and the drug companies?",
             "Chapter eight. Picks and shovels. Behind the hospitals and the drug companies of Part 20 stand the companies "
             "that sell them instruments, chemicals and services.", lit=("unit", "change"))
        self.sizes()
        self.thermo()
        self.iqvia()
        self.illumina()

    def sizes(self):
        T = R["tools"]
        role = {"Thermo Fisher": "instruments, reagents, drug manufacturing", "Danaher": "diagnostics and life-science tools",
                "IQVIA": "runs clinical trials for drug makers", "Agilent": "laboratory instruments",
                "Illumina": "gene sequencers"}
        items = [(k, v, TOOLS if k != "IQVIA" else LABS, f"${v:.1f}bn") for k, v in sorted(T["rev"].items(), key=lambda kv: -kv[1])]
        rows = hbars(items, max_value=46, x0=-2.8, top=1.8, row=0.85, length=5.6, size=18, bar_h=0.45)
        roles = VGroup(*[tx(role[n], 14, GREY_A).next_to(rows[i][2], RIGHT, buff=0.25) for i, (n, *_) in enumerate(items)])
        fl = draw.flask(0.9, TOOLS).move_to([-6.0, 2.6, 0])
        src = source("Forms 10-K via SEC company facts: revenue, latest fiscal year", size=12)
        beat(self,
             "Here are five of them, by revenue in their latest year. <bookmark mark='a'/> Thermo Fisher, the largest, "
             f"{items[0][1]:.1f} billion dollars: instruments, laboratory chemicals and the manufacturing of medicines for "
             f"others. <bookmark mark='b'/> Danaher, {T['rev']['Danaher']:.1f} billion of diagnostics and tools. "
             f"<bookmark mark='c'/> IQVIA, {T['rev']['IQVIA']:.1f} billion, which runs clinical trials for drug makers, "
             "the trials of Part 20. <bookmark mark='d'/> And Agilent and Illumina, which make laboratory instruments and "
             "gene sequencers. When drug companies spend on research, these companies sell to them.",
             base=[rows.axis, fl, head("The suppliers to medicine"), src],
             steps=[[rows[0], roles[0]], [rows[1], roles[1]], [rows[2], roles[2]], [VGroup(*rows[3:]), VGroup(*roles[3:])]])

    def thermo(self):
        T = R["tools"]
        tm = T["tmo"]
        ch = line_chart({"Thermo Fisher": (tm, TOOLS)}, x=(2017, 2025), y=(0, 50), xticks=list(range(2017, 2026, 2)),
                        yticks=[0, 10, 20, 30, 40, 50], yfmt=lambda v: f"${v:.0f}bn", ylabel="Thermo Fisher's revenue",
                        width=9.0, height=4.2, center=(-0.4, -0.5), label_end=False)
        m1 = marker(ch.ax, 2019, tm[2019], f"2019: ${tm[2019]:.1f}bn", GREY_A, side=UP)
        m2 = marker(ch.ax, 2022, tm[2022], f"2022: ${tm[2022]:.1f}bn", TOOLS, side=UP)
        m3 = marker(ch.ax, 2025, tm[2025], f"2025: ${tm[2025]:.1f}bn", TOOLS, side=DOWN)
        src = source("Thermo Fisher Scientific Inc., Forms 10-K via SEC company facts: revenue", size=12)
        beat(self,
             "Picks and shovels ride the same waves as the miners. <bookmark mark='a'/> Thermo Fisher sold "
             f"{tm[2019]:.1f} billion dollars in 2019. <bookmark mark='b'/> In the pandemic years its sales jumped, to "
             f"{tm[2020]:.1f} billion in 2020 and {tm[2022]:.1f} billion in 2022. "
             f"<bookmark mark='c'/> Then demand settled: {tm[2025]:.1f} billion in 2025, still well above where it began.",
             base=[ch.frame, src], steps=[m1, [ch.lines["Thermo Fisher"], m2], m3])

    def iqvia(self):
        T = R["tools"]
        iq = T["iqv"]
        ch = line_chart({"IQVIA": (iq, LABS)}, x=(2011, 2025), y=(0, 18), xticks=[2011, 2015, 2019, 2023, 2025],
                        yticks=[0, 6, 12, 18], yfmt=lambda v: f"${v:.0f}bn", ylabel="IQVIA's revenue", width=8.6,
                        height=4.0, center=(-0.6, -0.5), label_end=False)
        m0 = marker(ch.ax, 2011, iq[2011], f"2011: ${iq[2011]:.1f}bn", LABS, side=UP)
        m1 = marker(ch.ax, 2025, iq[2025], f"2025: ${iq[2025]:.1f}bn", LABS, side=LEFT)
        fl = draw.flask(1.0, LABS).move_to([5.4, 1.6, 0])
        src = source("IQVIA Holdings Inc. (and its predecessor), Forms 10-K via SEC company facts: revenue", size=12)
        beat(self,
             "The trials of Part 20 are a business of their own. <bookmark mark='a'/> IQVIA, which runs clinical trials "
             f"for drug companies, among other services, had {iq[2011]:.1f} billion dollars of revenue in 2011, as its "
             f"predecessor Quintiles. <bookmark mark='b'/> In 2025 it had {iq[2025]:.1f} billion. A drug company that spends a fifth "
             "of its revenue on research buys much of that research from others.",
             base=[ch.frame, fl, src], steps=[m0, [ch.lines["IQVIA"], m1]])

    def illumina(self):
        T = R["tools"]
        il = T["ilmn"]
        pr = T["ilmn_profit"]
        ch = line_chart({"Illumina": (il, TOOLS)}, x=(2012, 2025), y=(0, 5), xticks=[2012, 2015, 2018, 2021, 2025],
                        yticks=[0, 1, 2, 3, 4, 5], yfmt=lambda v: f"${v:.0f}bn", ylabel="Illumina's revenue", width=7.6,
                        height=4.0, center=(-1.6, -0.5), label_end=False)
        loss = VGroup(tx("net income, $bn", 15, GREY_A),
                      *[tx(f"{y}: {v:+.1f}", 16, GOOD if v >= 0 else BAD, bold=True) for y, v in sorted(pr.items()) if y >= 2021]
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, 0.0, 0])
        src = source("Illumina, Inc., Forms 10-K via SEC company facts: revenue and net income", size=12)
        beat(self,
             "And tools can stall. <bookmark mark='a'/> Illumina, whose machines read DNA, grew from "
             f"{il[2012]:.1f} billion dollars of revenue in 2012 to {il[2022]:.1f} billion in 2022, <bookmark mark='b'/> "
             f"then shrank a little, to {il[2025]:.1f} billion in 2025, and reported losses from 2022 to 2024 before "
             "returning to profit. A maker of tools grows only as fast as its customers' research and testing.",
             base=[ch.frame, src], steps=[ch.lines["Illumina"], loss])
