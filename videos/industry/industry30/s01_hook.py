from __future__ import annotations

from videos.industry.industry30.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.revenue()
        self.margins()
        self.prices()
        self.title()

    def revenue(self):
        H = R["hook"]
        three = {y: v for y, v in H["carriers3"].items()}
        ch = line_chart({"Verizon, AT&T and T-Mobile": (three, WIRELESS), "Alphabet, Meta and Netflix": (H["over"], OVER)},
                        x=(2015, 2025), y=(0, 700), xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[0, 200, 400, 600],
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="revenue, $bn a year", width=8.8, height=4.4, center=(-1.3, -0.45))
        phones = VGroup(*[draw.phone(0.7, screen=c) for c in (WIRELESS, OVER, CABLE)]).arrange(RIGHT, buff=0.25).to_corner(UR, buff=0.5)
        src = source("Forms 10-K via SEC company facts", size=12)
        a, b = three, H["over"]
        beat(self,
             "Almost everything you do on a phone travels over a network built by a telephone company. "
             f"<bookmark mark='a'/> America's three wireless carriers took in {a[2015]:.0f} billion dollars in 2015, and "
             f"{a[2025]:.0f} billion in 2025: {100 * (a[2025] / a[2015] - 1):.0f} per cent more in ten years, a merger "
             f"included. <bookmark mark='b'/> Three companies whose services travel over those networks, Alphabet, Meta "
             f"and Netflix, took in {b[2015]:.0f} billion in 2015 and {b[2025]:.0f} billion in 2025: "
             f"{b[2025] / b[2015]:.1f} times as much. The pipe is essential, and it is the services flowing through it that "
             "have grown.",
             base=[ch.frame, phones, src], steps=[VGroup(ch.lines["Verizon, AT&T and T-Mobile"], ch.labels["Verizon, AT&T and T-Mobile"]),
                                                  VGroup(ch.lines["Alphabet, Meta and Netflix"], ch.labels["Alphabet, Meta and Netflix"])])

    def margins(self):
        M = R["hook"]["margins"]
        items = [(k, M[k], OVER if k in ("Alphabet", "Meta", "Netflix") else WIRELESS, f"{M[k]:.0f}%")
                 for k in ("Meta", "Alphabet", "Netflix", "Verizon", "T-Mobile", "AT&T")]
        rows = hbars(items, max_value=45, x0=0.2, top=1.9, row=0.72, length=5.6, size=17, bar_h=0.4)
        lab = tx("operating profit per dollar of revenue, 2025", 17, GREY_A).to_edge(UP, buff=0.7)
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "And they keep more of each dollar. <bookmark mark='a'/> Meta kept "
             f"{M['Meta']:.0f} cents of operating profit per dollar in 2025, Alphabet {M['Alphabet']:.0f}, Netflix "
             f"{M['Netflix']:.0f}. <bookmark mark='b'/> Verizon kept {M['Verizon']:.0f}, T-Mobile {M['T-Mobile']:.0f}, AT&T "
             f"{M['AT&T']:.0f}, and then spent much of it on the next network.",
             base=[rows.axis, lab, src], steps=[VGroup(*rows[:3]), VGroup(*rows[3:])])

    def prices(self):
        H = R["hook"]
        ch = line_chart({"telephone services after inflation": (H["real"], WIRELESS)}, x=(1998, 2025), y=(0.3, 1.1),
                        xticks=[1998, 2004, 2010, 2016, 2022], yticks=[0.4, 0.6, 0.8, 1.0], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"x{v:.1f}", ylabel="CPI for telephone services divided by the CPI for all items, 1998 = 1",
                        width=9.2, height=4.4, center=(-0.6, -0.45), label_end=False)
        m = marker(ch.ax, 2025, H["real"][2025], f"2025: x{H['real'][2025]:.2f}", WIRELESS, side=LEFT)
        src = source("BLS, CPI-U for telephone services and all items, annual averages, via FRED", size=12)
        beat(self,
             "And the price of the service? <bookmark mark='a'/> Measured by the consumer price index, telephone service "
             f"cost about {100 * (1 - H['nominal'][2025]):.0f} per cent less in 2025 than in 1998, while prices in general "
             f"roughly doubled. <bookmark mark='b'/> After inflation, {100 * (1 - H['real'][2025]):.0f} per cent cheaper, "
             "for a service that now carries video, maps and money instead of voice.",
             base=[ch.frame, src], steps=[ch.lines["telephone services after inflation"], m])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part thirty: telecoms. Why do the companies that carry everything capture so "
                            "little of what it is worth?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
