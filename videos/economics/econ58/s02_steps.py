from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403


class Steps(VoiceoverScene):
    def construct(self):
        card(self, 1, r"The steps of an appraisal", r"Whose gains count, \ and compared with what?",
             "Chapter one. The steps of an appraisal.", lit={1936: r"the Flood Control Act", 1981: r"Executive Order "
                                                              r"12291"},
             scale=("person", "nation"), horizon=("a century",))
        self.steps()
        self.ledger()

    def steps(self):
        chain = flow_chain([(r"the options, \ and the counterfactual", GREY_B),
                            (r"standing: \ whose gains and losses count", TRAV),
                            (r"the impacts, \ year by year", BEN),
                            (r"a value for each, \ in money", SAFE),
                            (r"discount, \ and add up", RATE),
                            (r"test the assumptions; \ recommend", COST)], direction=DOWN, box_w=4.4, box_h=0.72,
                           buff=0.22, font_size=20,
                           notes=[r"the ferry keeps running: \ that is the comparison, \ not `nothing'",
                                  r"the Island's people, \ Bo included; \ visitors? \ the mainland?",
                                  r"crossings, \ minutes, \ fares, \ deaths, \ decibels, \ the build",
                                  r"surplus; \ the value of time; \ of a statistical life",
                                  r"a dollar in 2060 is not a dollar today",
                                  r"what moves the answer, \ and by how much"], note_size=19)
        chain.move_to(DOWN * 0.2)
        head = label(r"a cost-benefit analysis, \ in six steps", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.4)
        guides = VGroup(
            history_card(2003, r"HM Treasury, \ \emph{The Green Book}", r"how British government appraises "
                         r"projects, \ programmes and policies", color=RATE, width=5.4, font_size=20),
            history_card(2003, r"OMB, \ \emph{Circular A-4}", r"how American agencies analyse their "
                         r"regulations", color=CBO, width=5.4, font_size=20),
        ).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.2)
        with self.voiceover(
            "Every cost-benefit analysis, from a flood wall to a rule on lorry brakes, goes through the same steps, "
            "and the textbooks and the guidance manuals, the Treasury's Green Book in Britain and the Office of "
            "Management and Budget's circular in America, agree on them. <bookmark mark='a'/> First, the options, and "
            "the counterfactual: what happens if nothing is built. For the bridge, that is not nothing; it is the "
            "ferry, still running, with traffic still growing. Every benefit is measured against that. <bookmark "
            "mark='b'/> Second, standing: whose gains and losses count. The Island's travellers count, and so does "
            "Bo, who loses his trade; whether a visitor from the mainland counts is a choice, and it should be "
            "written down. <bookmark mark='c'/> Third, the impacts, year by year: crossings, minutes, fares, deaths, "
            "decibels, and the cost of building. <bookmark mark='d'/> Fourth, a value for each in money. <bookmark "
            "mark='e'/> Fifth, discount them to today and add them up. <bookmark mark='f'/> And sixth, move every "
            "assumption to see which ones decide the answer, before recommending anything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(guides, shift=UP * 0.1))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                if not k:
                    self.play(FadeOut(guides), run_time=0.5)
                anims = [FadeIn(chain.boxes[k], shift=DOWN * 0.1), FadeIn(chain.notes[k], shift=RIGHT * 0.1)]
                if k:
                    anims.append(GrowArrow(chain.arrows[k - 1]))
                self.play(*anims)
        self.clear_scene()

    def ledger(self):
        B = load("bridge")
        y = B["year"]
        p = B["params"]
        bo = y["Bo's profit"]
        st = strait(width=7.6, height=1.9, label_size=16).to_edge(UP, buff=0.35)
        st.bridge.set_stroke(opacity=1.0)
        rows = [
            (r"travellers: \ time saved on today's crossings", f"{y['time']:+.1f}", TRAV),
            (r"travellers: \ the fare no longer paid", f"{y['fares']:+.1f}", TRAV),
            (r"new crossings the bridge makes worth taking", f"{y['new trips']:+.1f}", TRAV),
            (r"Bo: \ the ferry's lost profit", f"{bo:+.1f}", BO),
            (rf"lives: \ {y['lives']:.2f} fewer deaths a year, \ at the VSL", f"{y['safety']:+.1f}", SAFE),
        ]
        tab = VGroup()
        for txt, val, col in rows:
            tab.add(VGroup(label(txt, font_size=24, color=col), label(f"${val.replace('-', '{-}')}$",
                                                                       font_size=26, color=col)))
        for r_ in tab:
            r_[1].next_to(r_[0], RIGHT, buff=0.3)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        for r_ in tab:
            r_[1].set_x(4.6, direction=RIGHT)
        once = VGroup(label(rf"once: \ build {sum(B['build']):.0f} over three years; \ noise for "
                            rf"{p['homes']} homes", font_size=24, color=COST),
                      label(rf"every year: \ upkeep {p['maintenance']:.1f}", font_size=24, color=COST)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15)
        head = label(r"a year of the bridge, \ millions of Island dollars", font_size=25, color=GREY_A)
        blk = VGroup(head, tab, once).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(st, DOWN, buff=0.35)
        blk.set_x(0)
        tag = island_tag(r"the Island: \ agora.appraisal.BRIDGE", corner=DR, font_size=12)
        with self.voiceover(
            "Here is the bridge's ledger, the Island's first year of it, in millions of Island dollars. "
            f"<bookmark mark='a'/> Travellers save time on the {y['q0']:.2f} million crossings they make now: "
            f"{y['time']:.1f} million a year at the value of time. <bookmark mark='b'/> They stop paying Bo's fare: "
            f"{y['fares']:.1f} million. <bookmark mark='c'/> A free, fast bridge makes crossings worth taking that "
            f"were not worth the ferry: {y['new trips']:.1f} million of gains on those. <bookmark mark='d'/> Bo "
            f"loses his ferry's profit, {abs(bo):.1f} million a year. <bookmark "
            f"mark='e'/> And the ferry is more dangerous than a bridge: about {y['lives']:.2f} fewer deaths a year, "
            "valued at the Island's value of a statistical life. <bookmark mark='f'/> Against that: three years and "
            f"{sum(B['build']):.0f} million of building, upkeep every year, and noise for the homes by the approach "
            "road. The next three chapters explain where each of these numbers comes from."
        ) as vo:
            self.play(FadeIn(st), FadeIn(tag), FadeIn(head))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(FadeIn(tab[k], shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(once, shift=RIGHT * 0.15))
        self.clear_scene()
