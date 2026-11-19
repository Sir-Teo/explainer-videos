from __future__ import annotations

from scipy.stats import norm

from videos.economics.econ10.common import *  # noqa: F403

LATE = TOWN
EARLY = STUD


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ fare classes and revenue management", r"How does a seller with fixed "
             r"capacity decide which buyers to turn away?", "Chapter fifteen. In practice: fare classes and revenue "
             "management.", lit={1972: r"Littlewood's rule"}, scale=("firm", "market"), horizon=("a day", "a year"))
        self.fences()
        self.rule()

    def fences(self):
        head = label(r"an airline fare menu is second-degree discrimination", font_size=32, color=E.ACCENT).to_edge(
            UP, buff=0.5)
        rows = VGroup(
            label(r"the same seat, \ sold at many prices, \ each with its own conditions", font_size=25),
            label(r"book three weeks ahead, \ stay over a Saturday night, \ no refunds: \ cheap", font_size=25,
                  color=EARLY),
            label(r"book the day before, \ fly home the same day, \ change it if you like: \ dear", font_size=25,
                  color=LATE),
            label(r"the conditions are fences: \ cheap for those who would pay little, \\ irksome for those who "
                  r"would pay a lot", font_size=24),
            label(r"Dupuit's roofless carriage, \ a century and a half on", font_size=26, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "The menus of chapter six are everywhere in travel. <bookmark mark='a'/> An airline sells the same seat "
            "at many prices, each with its own conditions. <bookmark mark='b'/> Book three weeks ahead, stay over "
            "a Saturday night, accept no refund, and the fare is low. <bookmark mark='c'/> Book the day before, fly "
            "home the same evening, keep the right to change, and it is high. <bookmark mark='d'/> The conditions "
            "are fences. They cost a tourist little, and a business traveller a great deal, so each picks the fare "
            "meant for them. <bookmark mark='e'/> It is Dupuit's roofless carriage, a century and a half on."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def rule(self):
        lw = load("littlewood")
        rev = np.array(lw["revenue"])
        seats, lo, hi, m, s = lw["seats"], lw["p_lo"], lw["p_hi"], lw["mean_hi"], lw["sd_hi"]
        y_star = norm.ppf(1 - lo / hi, loc=m, scale=s)
        ax = plane([0, 40], [100, 220], center=LEFT * 2.9 + DOWN * 0.4, x_length=6.2, y_length=4.8,
                   xticks=[0, 10, 20, 30, 40], yticks=[100, 140, 180, 220], xlabel=r"seats kept back for late "
                   r"bookers", ylabel=r"expected fares, \ \$", font_size=16)
        a = ax.ax
        ys = np.arange(seats + 1)
        curve = path(ax, ys, rev, color=E.ACCENT, width=3.5, smooth=False, yr=(100, 220))
        best = lw["protect_best"]
        B = Dot(a.c2p(best, rev[best]), radius=0.09, color=E.ACCENT)
        bl = label(rf"keep {best}: \ \${rev[best]:.0f}", font_size=18, color=E.ACCENT).next_to(B, UP, buff=0.12)
        Z = Dot(a.c2p(0, rev[0]), radius=0.08, color=EARLY)
        zl = label(rf"keep none: \ \${rev[0]:.0f}", font_size=18, color=EARLY).next_to(Z, DR, buff=0.1)
        side = VGroup(
            label(rf"Bo's last ferry: \ {seats} seats", font_size=23),
            label(rf"students book early at \${lo:.0f}, \ and there are always enough of them", font_size=21,
                  color=EARLY),
            label(rf"townsfolk come late at \${hi:.0f}: \ about {m}, \ give or take {s}", font_size=21, color=LATE),
            label(r"keep back one more seat only if \\ the chance a late booker takes it, \ times \$10, \\ is at "
                  r"least the \$4 a student pays now", font_size=21),
            MathTex(rf"p_{{\text{{hi}}}}\,P(D_{{\text{{hi}}}} > y) = p_{{\text{{lo}}}} \;\Rightarrow\; y = "
                    rf"{y_star:.1f}", font_size=30, color=E.ACCENT),
            label(r"Littlewood (1972), \ for BOAC: \ the start of revenue management; \\ Part 60 tells how it won "
                  r"an airline war", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Fences decide who pays which fare. A seller with a fixed number of seats must also decide how many "
            "cheap ones to sell. <bookmark mark='a'/> Bo's last ferry of the day has forty seats. "
            "<bookmark mark='b'/> Students book early, at four dollars, and there are always enough of them to "
            "fill the boat. <bookmark mark='c'/> Townsfolk come at the last minute and pay ten, but how many will "
            "come is uncertain: about twelve, give or take five. Sell every seat to students and Bo takes a sure "
            "hundred and sixty dollars. <bookmark mark='d'/> Keep seats back, and some may sail empty. Ken "
            "Littlewood's rule, from British Overseas Airways in 1972: keep back one more seat only if the chance "
            "that a late passenger will want it, times the ten dollar fare, is at least the four dollars a student "
            "would pay for it now. <bookmark mark='e'/> The chance must be at least forty percent, which gives "
            "thirteen seats. Agora simulates two hundred thousand evenings: keeping thirteen back raises the "
            "expected takings from a hundred and sixty dollars to about two hundred and thirteen, and no other "
            "number does better. <bookmark mark='f'/> That rule was the beginning of revenue management, now run "
            "for every airline seat, hotel room and rental car. Part sixty tells how it won an airline war."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(Z), FadeIn(zl))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Create(curve), run_time=2)
            vo.wait_until("e")
            self.play(Write(side[4]), FadeIn(B), FadeIn(bl))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()
