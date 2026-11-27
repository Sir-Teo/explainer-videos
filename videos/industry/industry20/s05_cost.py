from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Cost(VoiceoverScene):
    def construct(self):
        card(self, 4, "The cost of one medicine", "What does one approved drug cost, once the failures are counted?",
             "Chapter four. The cost of one medicine. What does one approved drug really cost, once you pay for all the "
             "ones that failed?", lit=("dollar",))
        self.arithmetic()
        self.waiting()
        self.rnd()
        self.total()

    def total(self):
        T = R["rd_total"]
        c = stat_cards([(f"${T['total']:.0f}bn", f"research and development of {T['n']} drug companies in this film, 2025", BRAND),
                        (f"{100 * T['total'] / T['rev']:.0f}%", "of their combined revenue", PRICE)], y=0.6, size=46, span=10)
        fl = VGroup(*[draw.flask(0.8, LAB if i % 2 else BIO) for i in range(6)]).arrange(RIGHT, buff=0.4).move_to([0, -1.8, 0])
        src = source("Forms 10-K and 20-F via SEC company facts: research and development, 2025", size=12)
        beat(self,
             f"Add it up. <bookmark mark='a'/> The {T['n']} drug companies measured in this film spent about "
             f"{T['total']:.0f} billion dollars on research and development in 2025, <bookmark mark='b'/> "
             f"{100 * T['total'] / T['rev']:.0f} per cent of their combined revenue, a fifth of every dollar a patient or "
             "insurer pays. <bookmark mark='c'/> That spending, not the factory, is the real cost of a medicine, and it "
             "is spent on the failures as much as on the successes.",
             base=[src], steps=[c[0], c[1], fl])

    def waiting(self):
        Dsp = R["drug_split"]
        C = R["cost"]
        pa = viz.plot_axes([0, 10.5], [0, 3], x_length=9.0, y_length=4.0, xticks=[0, 2.3, 5.9, 9.2, 10.5],
                           yticks=[0, 1, 2, 3], xfmt=lambda v: f"year {v:.1f}", yfmt=lambda v: f"${v:.0f}",
                           ylabel="what a dollar spent at the start must earn by approval, at 10.5% a year", size=13).move_to([-0.6, -0.45, 0])
        ax = pa.ax
        pts = [(t, 1.105 ** t) for t in np.linspace(0, 10.5, 60)]
        curve = poly(ax, pts, PRICE, 4)
        end = marker(ax, 10.5, Dsp["cap_factor"], f"${Dsp['cap_factor']:.2f}", PRICE, side=LEFT)
        coin = draw.coin_stack(5, 0.25).move_to([-2.6, 0.6, 0])
        tag = estimate_tag("a 10.5% a year cost of capital, as in the Works", size=12)
        beat(self,
             "Why does waiting cost so much? <bookmark mark='a'/> Money spent on Phase one is spent more than ten years "
             "before the drug can earn anything. Investors could have put it elsewhere, so it has to earn a return all "
             f"that time. <bookmark mark='b'/> At ten and a half per cent a year, a dollar spent at the start must bring "
             f"back {Dsp['cap_factor']:.2f} dollars by the day of approval just to break even. That is why the cost of a "
             f"drug with the waiting counted, {C['capitalized'] / 1e3:.1f} billion in our model, is about twice the cost "
             "without it.",
             base=[pa, coin, tag], steps=[curve, end])

    def arithmetic(self):
        C = R["cost"]
        costs = C["costs"]
        reach = C["reach"]
        rows = VGroup()
        for i, ((name, cst), p) in enumerate(zip(costs, reach)):
            rows.add(VGroup(tx(name, 17, WHITE, bold=True).move_to([-5.0, 1.8 - 0.55 * i, 0], aligned_edge=LEFT),
                            tx(f"${cst:.0f}m", 17, PRICE).move_to([-2.2, 1.8 - 0.55 * i, 0]),
                            tx(f"x {100 * p:.1f}% who get there", 16, GREY_A).move_to([0.4, 1.8 - 0.55 * i, 0]),
                            tx(f"= ${cst * p:.1f}m", 17, WHITE).move_to([3.4, 1.8 - 0.55 * i, 0])))
        hd = VGroup(tx("stage", 14, GREY_B).move_to([-5.0, 2.4, 0], aligned_edge=LEFT), tx("cost", 14, GREY_B).move_to([-2.2, 2.4, 0]),
                    tx("share of candidates", 14, GREY_B).move_to([0.4, 2.4, 0]), tx("expected", 14, GREY_B).move_to([3.4, 2.4, 0]))
        tot = tx(f"per candidate: ${C['spend']:.0f}m", 19, WHITE, bold=True).move_to([0.6, -0.6, 0])
        per = tx(f"per approved drug: ${C['spend']:.0f}m / {100 * C['p_approval']:.1f}% = ${C['per_approval'] / 1e3:.1f}bn", 21, BAD, bold=True).move_to([0.6, -1.3, 0])
        cap = tx(f"counting {C['years']:.1f} years of waiting at 10.5% a year: ${C['capitalized'] / 1e3:.1f}bn", 19, PRICE, bold=True).move_to([0.6, -2.0, 0])
        tag = estimate_tag("the Works: BIO's success rates and durations, illustrative costs per stage", size=12)
        beat(self,
             "Do the arithmetic for one candidate. <bookmark mark='a'/> In our model each stage costs this much, but only "
             "the candidates that get there pay it: Phase one costs twenty-five million, and every candidate pays it; "
             f"Phase three costs two hundred and fifty, but only {100 * reach[2]:.0f} per cent of candidates get that far. "
             f"<bookmark mark='b'/> On average a candidate costs about {C['spend']:.0f} million dollars. "
             f"<bookmark mark='c'/> But only {100 * C['p_approval']:.1f} per cent become medicines, so each approved drug "
             f"has to carry the cost of about twelve: {C['per_approval'] / 1e3:.1f} billion dollars. "
             f"<bookmark mark='d'/> And the money is spent years before any sales; counting the cost of waiting, about "
             f"{C['capitalized'] / 1e3:.1f} billion. Economists' estimates of the cost of a new drug differ mostly over "
             "exactly these inputs: what each stage costs, the odds, and the cost of waiting.",
             base=[hd, tag], steps=[rows, tot, per, cap])

    def rnd(self):
        Rn = R["rnd"]
        s = Rn["share"]
        order = sorted(s, key=lambda k: -s[k])
        items = [(k, 100 * s[k], BIO if k in ("Regeneron", "Vertex", "Amgen", "Gilead", "Biogen") else
                  (GENERIC if k in ("Teva", "Viatris") else BRAND), f"{100 * s[k]:.0f}%") for k in order]
        rows = hbars(items, max_value=45, x0=-1.0, top=2.3, row=0.4, length=6.0, size=14, bar_h=0.28)
        src = source("Forms 10-K and 20-F via SEC company facts: research and development over revenue, latest year", size=12)
        beat(self,
             "So drug companies spend a lot on research. <bookmark mark='a'/> Regeneron and Vertex, two biotech "
             f"companies, spent {100 * s['Regeneron']:.0f} and {100 * s['Vertex']:.0f} per cent of their revenue on it in "
             f"their latest year; the big companies, Merck, AstraZeneca and Lilly, about a fifth to a quarter. "
             f"<bookmark mark='b'/> The generic makers, Teva and Viatris, which copy medicines whose patents have expired, "
             "spend only five to seven per cent. A company that invents medicines lives on research; one that copies "
             "them lives on making them cheaply.",
             base=[rows.axis, head("Research and development as a share of revenue"), src],
             steps=[VGroup(*rows[:-2]), VGroup(*rows[-2:])])
