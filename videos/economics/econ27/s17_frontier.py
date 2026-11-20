from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ supply shocks that cut demand", r"Can a shutdown cause a demand shortage "
             r"bigger than itself?", "Chapter fifteen. Frontier: supply shocks that cut demand.",
             lit={2022: r"Guerrieri, Lorenzoni, Straub and Werning"}, scale=("market", "nation"),
             horizon=("a quarter",))
        self.question()
        self.mechanism()
        self.open_()

    def question(self):
        rows = VGroup(
            label(r"spring 2020: \ restaurants, \ cinemas and airlines shut by law", font_size=24, color=PRICE),
            label(r"a supply shock: \ those goods simply cannot be bought", font_size=24, color=OUTPUT),
            label(r"in AS--AD, \ a supply shock raises prices; \ but prices and inflation fell that spring",
                  font_size=23, color=GREY_A),
            label(r"Guerrieri, \ Lorenzoni, \ Straub and Werning, \ 2022: \ Keynesian supply shocks", font_size=24,
                  color=E.ACCENT),
            label(r"a supply shock that cuts demand by more than itself", font_size=24, color=SPEND),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Guerrieri, \ Lorenzoni, \ Straub and Werning, \ AER 112(5) (2022): \ 1437--1474",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The frontier starts in the spring of 2020. <bookmark mark='a'/> Restaurants, cinemas and airlines were "
            "shut, by law. <bookmark mark='b'/> That is a supply shock: those things simply could not be bought. "
            "<bookmark mark='c'/> In the picture of chapter ten, a supply shock raises prices. But that spring, "
            "prices across the economy fell, and so did spending on things that were still open. "
            "<bookmark mark='d'/> Veronica Guerrieri, Guido Lorenzoni, Ludwig Straub and Ivan Werning explained it "
            "in 2022. <bookmark mark='e'/> A supply shock can be Keynesian: it can cut demand by more than it cuts "
            "supply."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def mechanism(self):
        rows = VGroup(
            label(r"with one sector, \ never: \ a supply shock always leaves too much demand, \ not too little",
                  font_size=22, color=GREY_A),
            label(r"with two sectors: \ the waiter loses income, \ and stops spending in the open sector too",
                  font_size=22, color=PRICE),
            label(r"and if households cannot borrow against better times, \ the loss of income spills over",
                  font_size=22, color=SAVE),
            label(r"if goods are poor substitutes, \ money not spent on dinners is saved, \ not spent on books",
                  font_size=22, color=SPEND),
            label(r"so: \ fiscal stimulus is weaker, \ because the multiplier runs through closed shops",
                  font_size=22, color=GOV),
            label(r"monetary policy, \ if not stuck at zero, \ can matter more: \ by keeping firms alive",
                  font_size=22, color=COUPON),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        with self.voiceover(
            "How? <bookmark mark='a'/> In an economy with one good, it cannot happen: if supply falls, there is "
            "always too much demand, not too little. <bookmark mark='b'/> With two sectors it can. A waiter in a "
            "closed restaurant loses income, and stops spending in the sectors that are still open. "
            "<bookmark mark='c'/> If households cannot borrow against the better times to come, the lost income "
            "spills over in full. <bookmark mark='d'/> And if the goods are poor substitutes, money not spent on "
            "dinners is saved, not spent on books. Then demand falls by more than supply. "
            "<bookmark mark='e'/> Their conclusions cut against the textbook. Ordinary fiscal stimulus is weaker "
            "than usual, because the multiplier has to run through shops that are shut. "
            "<bookmark mark='f'/> And monetary policy, as long as it is not stuck at zero, can do more, by keeping "
            "firms alive until they can reopen."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def open_(self):
        rows = VGroup(
            label(r"open questions", font_size=30, color=E.ACCENT),
            label(r"how much of a slump is demand, \ and how much supply? \ the answer changes the policy",
                  font_size=23, color=SPEND),
            label(r"how long is the short run? \ do slumps leave scars on capacity (hysteresis)?", font_size=23,
                  color=PRICE),
            label(r"how big are multipliers when rates are at zero, \ or when the slump is local? \ (Part 32)",
                  font_size=23, color=GOV),
            label(r"can a central bank escape the trap by promises alone? \ (Part 31)", font_size=23, color=COUPON),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.1)
        with self.voiceover(
            "The questions still open. <bookmark mark='a'/> How much of any slump is a shortage of demand, and how "
            "much a loss of supply? The answer decides the policy. <bookmark mark='b'/> How long is the short run, "
            "and does a long slump leave scars on what the economy can produce, so that demand shapes supply? "
            "<bookmark mark='c'/> How big are multipliers when interest rates are at zero, or when the slump hits "
            "one region and not the rest? <bookmark mark='d'/> And can a central bank stuck at zero escape by "
            "promises alone?"
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
