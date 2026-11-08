from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Animals(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Other animals", r"Which creatures could there be something it is like to be?",
                            lit=(2012, 2024), part=PART)
        with self.voiceover("Chapter fourteen. Other animals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.declarations()
        self.markers()
        self.precaution()

    def declarations(self):
        head = label(r"Two declarations", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        groups = [(r"mammals", 2), (r"birds", 2), (r"reptiles", 1), (r"amphibians", 1), (r"fishes", 1),
                  (r"octopuses and squid", 1), (r"crabs and lobsters", 1), (r"insects", 1)]
        # a simple tree: a trunk, with branches to each group
        trunk = Line([-6.0, -2.2, 0], [5.6, -2.2, 0], color=GREY_C)
        leaves = VGroup()
        for k, (g, _) in enumerate(groups):
            x = -5.4 + 1.5 * k
            leaves.add(VGroup(Line([x, -2.2, 0], [x, -0.6, 0], color=GREY_C),
                              Dot([x, -0.6, 0], radius=0.1, color=GREY_B),
                              wrapped_label(g, 1.3, 16, GREY_A).move_to([x, -0.15, 0])))
        y12 = label(r"Cambridge, \ 2012: \ the neurological substrates of consciousness are not unique to humans: \ "
                    r"all mammals and birds, \ and many others, \ including octopuses", font_size=18,
                    color=FUNC).move_to([0, 2.3, 0])
        y24a = label(r"New York, \ 2024: \ strong support for mammals and birds", font_size=18,
                     color=OK).move_to([0, 1.6, 0])
        y24b = label(r"at least a realistic possibility in all vertebrates, \ and many invertebrates, \ at minimum "
                     r"cephalopods, \ decapods and insects", font_size=18, color=SIG).move_to([0, 1.1, 0])
        strong = VGroup(*[leaves[k][1].copy().set_color(OK).scale(1.6) for k in (0, 1)])
        possible = VGroup(*[leaves[k][1].copy().set_color(SIG).scale(1.6) for k in range(2, 8)])
        with self.voiceover(
            "Who else is conscious? Two declarations mark how scientific opinion has moved. "
            "<bookmark mark='a'/>In 2012 a group of neuroscientists meeting in Cambridge declared that humans are "
            "not unique in possessing the neurological substrates of consciousness: all mammals and birds, and many "
            "other creatures, including octopuses, have them too. <bookmark mark='b'/>In 2024 the New York "
            "Declaration on Animal Consciousness went further. It found strong scientific support for conscious "
            "experience in mammals and birds, <bookmark mark='c'/>and at least a realistic possibility of it in all "
            "vertebrates, reptiles, amphibians and fishes, and in many invertebrates, including at minimum "
            "octopuses and squid, crabs and lobsters, and insects. <bookmark mark='d'/>And it added a third "
            "sentence, about ethics: when there is a realistic possibility of conscious experience in an animal, "
            "it is irresponsible to ignore it in decisions that affect that animal."
        ) as vo:
            self.play(FadeIn(head), Create(trunk), LaggedStart(*[FadeIn(l) for l in leaves], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(y12))
            vo.wait_until("b")
            self.play(FadeIn(y24a), FadeIn(strong))
            vo.wait_until("c")
            self.play(FadeIn(y24b), LaggedStart(*[FadeIn(p) for p in possible], lag_ratio=0.15))
            vo.wait_until("d")
            self.play(Indicate(VGroup(y24a, y24b), color=GOAL, scale_factor=1.02))
        self.clear_scene()

    def markers(self):
        hc = history_card(2021, r"Jonathan Birch et al.", r"\textit{Review of the Evidence of Sentience in "
                                                          r"Cephalopod Molluscs and Decapod Crustaceans}", width=7.4,
                          color=HIST).to_corner(UL, buff=0.3)
        crit = [r"nociceptors", r"brain regions that integrate them", r"connections between the two",
                r"responses changed by anaesthetics or painkillers", r"trade-offs between threat and reward",
                r"flexible protection of an injury", r"learning to avoid harm",
                r"seeking out painkillers when injured"]
        col = VGroup(*[VGroup(label(f"{k + 1}.", font_size=19, color=SIG), label(c, font_size=19, color=WHITE)
                              ).arrange(RIGHT, buff=0.2) for k, c in enumerate(crit)]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).move_to([-2.0, -0.6, 0])
        side = stack([(r"no single test: \ a balance of markers", GREY_A),
                      (r"very strong evidence for octopuses; \ strong for true crabs", OK),
                      (r"UK Animal Welfare \ (Sentience) \ Act, \ 2022: \ covers decapods and cephalopods", GOAL)],
                     font_size=19, aligned_edge=LEFT, width=4.6, buff=0.3).move_to([4.4, -0.4, 0])
        with self.voiceover(
            "How is such evidence weighed? <bookmark mark='a'/>In 2021 Jonathan Birch and colleagues reviewed the "
            "evidence for sentience in octopuses, squid, crabs and lobsters for the British government, with eight "
            "criteria. Does the animal have receptors for damage? Brain regions that integrate their signals, and "
            "connections between the two? Are its responses changed by anaesthetics or painkillers? Does it trade "
            "off threat against reward? Does it protect an injury flexibly? Does it learn to avoid harm? Does it "
            "seek out painkillers when injured? <bookmark mark='b'/>No one criterion settles it; the markers are "
            "weighed together. <bookmark mark='c'/>They found very strong evidence for octopuses, and strong "
            "evidence for true crabs. <bookmark mark='d'/>Following the review, the Animal Welfare Sentience Act "
            "that the United Kingdom passed in 2022 covers decapod crustaceans and cephalopod molluscs as well as "
            "vertebrates."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in col], lag_ratio=0.3), run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def precaution(self):
        head = label(r"Reasoning under uncertainty about minds", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the theories disagree", r"a workspace? \ higher-order states? \ $\Phi$? \ each draws the line "
                                           r"in a different place", GREY_A),
                (r"markers, \ not theories", r"Birch: \ use behaviour and anatomy that most theories would count as "
                                             r"evidence", FUNC),
                (r"proportionate precaution", r"Birch, \ \textit{The Edge of Sentience} \ (2024): \ take the "
                                              r"realistic possibility seriously, \ at a reasonable cost", OK),
                (r"the same question", r"for machines, \ markers drawn from behaviour are easier to fake: \ the next "
                                       r"chapter", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "This is reasoning under deep uncertainty. <bookmark mark='a'/>The theories of this part draw the line "
            "in different places: a workspace, a higher-order state, or phi would each give a different answer for "
            "a bee. <bookmark mark='b'/>So Birch recommends markers rather than theories: features of behaviour and "
            "anatomy that most theories would count as evidence. <bookmark mark='c'/>And in his book of 2024 he "
            "argues for proportionate precaution: when sentience is a realistic possibility, take it seriously, at "
            "a cost that is reasonable for what is at stake. <bookmark mark='d'/>The same question can be asked of "
            "machines, with one difference that makes it harder: a system trained on human behaviour can produce "
            "the behavioural markers without what they mark."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
