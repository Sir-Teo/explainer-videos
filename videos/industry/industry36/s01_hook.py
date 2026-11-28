from __future__ import annotations

from videos.industry.industry36.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.copies()
        self.microsoft()
        self.costs()
        self.history()
        self.title()

    def copies(self):
        disks = VGroup(*[draw.laptop(1.2) for _ in range(5)]).arrange(RIGHT, buff=0.35).move_to([0, 1.3, 0])
        c = stat_cards([("$ millions", "to write the first copy: years of engineers' time", ENG),
                        ("about $0", "to make the next copy, and the one after", PROFIT)], y=-1.4, size=36, span=11)
        tag = estimate_tag("this series' illustration", size=12)
        beat(self,
             "A program is written once. <bookmark mark='a'/> The first copy can take years of work by hundreds of engineers. "
             "<bookmark mark='b'/> Every copy after it costs almost nothing to make: it is the same pattern of bits, sent down "
             "a wire. No other product in this series behaves like that. So what is a business worth when the second copy "
             "costs nothing?",
             base=[disks, tag], steps=[c[0], c[1]])

    def microsoft(self):
        H = R["hook"]
        c = stat_cards([(bn(H["rev"], 0), "Microsoft's revenue, year to June 2026", STOCK),
                        (bn(H["op"], 0), f"operating income: {100 * H['op'] / H['rev']:.0f} cents a dollar", PROFIT),
                        (f"{H['staff'] / 1e3:.0f}k", "full-time employees", GA)], y=0.6, size=40, span=12)
        src = source("Microsoft, Form 10-K for fiscal 2026; operating income via SEC company facts", size=12)
        beat(self,
             f"<bookmark mark='a'/> Microsoft took in {H['rev']:.0f} billion dollars in the year to June 2026. "
             f"<bookmark mark='b'/> Its operating income was {H['op']:.0f} billion: {100 * H['op'] / H['rev']:.0f} cents of every "
             "dollar, after paying for everything, from the engineers to the data centres to the sales teams. "
             f"<bookmark mark='c'/> It did that with about {H['staff'] / 1e3:.0f} thousand employees: roughly "
             f"{H['op'] * 1e9 / H['staff'] / 1e3:,.0f} thousand dollars of operating income for each of them.",
             base=[src], steps=list(c))

    def costs(self):
        H = R["hook"]
        items = [("cost of revenue: data centres, devices, support", H["cost"], HOST, bn(H["cost"])),
                 ("research and development", H["rnd"], ENG, bn(H["rnd"])),
                 ("sales and marketing", H["sm"], SALES, bn(H["sm"])),
                 ("operating income", H["op"], PROFIT, bn(H["op"]))]
        rows = hbars(items, max_value=170, x0=0.6, top=1.6, row=0.95, length=5.4, size=17, bar_h=0.55)
        hd = tx("where Microsoft's revenue went, fiscal 2026", 21, WHITE, bold=True).to_edge(UP, buff=0.7)
        src = source("Microsoft, Form 10-K for fiscal 2026", size=12)
        beat(self,
             f"Where did its {H['rev']:.0f} billion go? <bookmark mark='a'/> {H['cost']:.0f} billion on the cost of revenue: "
             "mostly data centres, plus the Xbox consoles and laptops it builds and the people who support customers. "
             f"<bookmark mark='b'/> {H['rnd']:.0f} billion on research and development, <bookmark mark='c'/> {H['sm']:.0f} "
             f"billion on selling. <bookmark mark='d'/> And {H['op']:.0f} billion left over. What the engineers build can be "
             "sold again and again; the data centres, though, grow with every customer, and that is where the industry is "
             "changing.",
             base=[rows.axis, hd, src], steps=list(rows))

    def history(self):
        H = R["hook"]
        Hh = H["hist"]
        rev = {y: v[0] for y, v in Hh.items()}
        op = {y: v[1] for y, v in Hh.items()}
        ch = line_chart({"revenue": (rev, STOCK), "operating income": (op, PROFIT)}, x=(2009, 2026), y=(0, 350),
                        xticks=[2009, 2014, 2019, 2024, 2026], yticks=[0, 100, 200, 300], yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="Microsoft, fiscal years to June, $bn", width=8.6, height=4.3, center=(-1.0, -0.45))
        src = source("Microsoft, Forms 10-K via SEC company facts", size=12)
        beat(self,
             f"<bookmark mark='a'/> Microsoft's revenue was {rev[2009]:.0f} billion dollars in 2009 and {rev[2026]:.0f} billion "
             f"in 2026. <bookmark mark='b'/> Its operating income grew from {op[2009]:.0f} billion to {op[2026]:.0f} billion. "
             f"Most of the growth is in what it now rents rather than sells: {H['service']:.0f} billion of the "
             f"{H['rev']:.0f} came from services and subscriptions, and {H['product']:.0f} billion from licences and devices.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["revenue"], ch.labels["revenue"]), VGroup(ch.lines["operating income"], ch.labels["operating income"])])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part thirty-six: software. What is a business worth when the second copy costs "
                            "nothing?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
