from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403


class Ancient(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"The sea battle and the master argument", r"Is the future already settled?",
                            lit=(-350, -300), part=PART)
        with self.voiceover("Chapter one. The sea battle and the master argument."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.sea_battle()
        self.master()
        self.exits()
        self.leibniz()

    def sea_battle(self):
        hc = history_card(r"c.\ 350 BCE", r"Aristotle, \textit{On Interpretation} 9", r"`There will be a sea battle "
                          r"tomorrow'", width=6.0, color=HIST).to_corner(UL, buff=0.35)
        t0 = Dot([-3.4, -0.8, 0], radius=0.1, color=WORLD)
        t1 = Dot([0.4, 0.5, 0], radius=0.1, color=OK)
        t2 = Dot([0.4, -2.1, 0], radius=0.1, color=BAD)
        b1, b2 = Line(t0.get_center(), t1.get_center(), color=ACC), Line(t0.get_center(), t2.get_center(), color=ACC)
        lab = VGroup(label(r"today", font_size=22, color=GREY_A).next_to(t0, DOWN, buff=0.15),
                     label(r"tomorrow: \ a battle", font_size=22, color=OK).next_to(t1, RIGHT, buff=0.2),
                     label(r"tomorrow: \ no battle", font_size=22, color=BAD).next_to(t2, RIGHT, buff=0.2))
        arg = VGroup(label(r"if `there will be a battle' is true today, \ the battle cannot fail to happen", font_size=24),
                     label(r"if it is false today, \ the battle cannot happen", font_size=24),
                     label(r"so whatever happens, happens necessarily: \ fatalism", font_size=26, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Modal logic begins with a battle that has not happened yet. <bookmark mark='a'/>In On Interpretation, "
            "chapter nine, Aristotle considers the sentence 'there will be a sea battle tomorrow'. "
            "<bookmark mark='b'/>Today the future branches: tomorrow there may be a battle, or there may not. "
            "<bookmark mark='c'/>Now argue: if the sentence is already true today, the battle cannot fail to "
            "happen; if it is already false, the battle cannot happen. Either way, everything that happens happens "
            "of necessity. That is fatalism. Aristotle seems to conclude that such sentences about the future are not "
            "yet true or false, though scholars still dispute what he meant. Chapter eleven will give two precise "
            "answers."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(t0), Create(b1), Create(b2), FadeIn(t1), FadeIn(t2), FadeIn(lab))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(a, shift=UP * 0.15) for a in arg], lag_ratio=0.5), run_time=3)
        self.clear_scene()

    def master(self):
        hc = history_card(r"c.\ 300 BCE", r"Diodorus Cronus", r"the Master Argument, reported by Epictetus, "
                          r"\textit{Discourses} II.19", width=6.6, color=HIST).to_corner(UL, buff=0.35)
        d = load("master")
        rows = VGroup(*[label(rf"{i + 1}.\ \ {c['text']}", font_size=28) for i, c in enumerate(d["claims"])]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -0.3, 0])
        clash = label(r"Diodorus: \ these three cannot all be true", font_size=28, color=BAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A generation later, Diodorus Cronus made an argument so famous that it was simply called the Master. "
            "Only its premises survive, in a report by Epictetus. <bookmark mark='a'/>Every true proposition about "
            "the past is necessary: what has happened cannot now not have happened. <bookmark mark='b'/>Nothing "
            "impossible follows from something possible. <bookmark mark='c'/>And something is possible that neither "
            "is true nor ever will be: a battle that could have been fought but never is. <bookmark mark='d'/>"
            "Diodorus claimed that these three are inconsistent, and the ancient schools agreed. They disagreed "
            "about which one to give up."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(clash))
        self.clear_scene()

    def exits(self):
        d = load("master")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=[tuple(x) for x in d["mus"]], radius=2.5, width=4.2, font_size=22,
                       center=[0, -0.5, 0], title=r"The Price List: \ the Master Argument")
        positions = [(("C",), r"Diodorus", r"the possible is what is or will be true: \ a strong determinism"),
                     (("P",), r"Cleanthes", r"some past truths are not necessary"),
                     (("I",), r"Chrysippus", r"the impossible can follow from the possible")]
        assert sorted(tuple(x) for x in d["mcs"]) == sorted(p[0] for p in positions)
        with self.voiceover(
            "As a Price List: three claims, one conflict, and three exits. The Stoics took all three. "
            "<bookmark mark='a'/>Diodorus gave up the third: the possible is just what is or will at some time be "
            "true. Nothing that never happens was ever possible. <bookmark mark='b'/>Cleanthes, Zeno's successor, "
            "gave up the first: some truths about the past are not necessary. <bookmark mark='c'/>And Chrysippus, the "
            "great Stoic logician, gave up the second: something impossible can follow from something possible. "
            "<bookmark mark='d'/>Notice that each exit is a theory of what 'possible' means. To decide between them, "
            "we need a definition, and that took two thousand years."
        ) as vo:
            self.play(FadeIn(pl.title), LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.25), Create(pl.conflict))
            for i, (mk, (mcs, name, who)) in enumerate(zip("abc", positions)):
                vo.wait_until(mk)
                if i:
                    self.play(*pl.reset(), run_time=0.6)
                anims, centre = pl.position(mcs, name, who, width=3.2)
                self.play(*anims)
            vo.wait_until("d")
            self.play(*pl.reset(), run_time=0.6)
        self.clear_scene()

    def leibniz(self):
        hc = history_card(1710, r"Leibniz, \textit{Theodicy}", r"this is the best of all possible worlds",
                          width=5.4, color=HIST).to_corner(UL, buff=0.35)
        med = VGroup(history_card(r"c.\ 1020", r"Avicenna", r"necessary in itself, \ or necessary through another",
                                  width=5.6, color=HIST),
                     history_card(r"c.\ 1300", r"John Duns Scotus", r"synchronic contingency: \ at the moment I choose, "
                                  r"I could choose otherwise", width=5.6, color=HIST)).arrange(RIGHT, buff=0.4).move_to(
            [0, 0.4, 0])
        defs = VGroup(
            VGroup(label(r"necessary", font_size=30, color=GOAL), label(r"true in every possible world", font_size=26)),
            VGroup(label(r"possible", font_size=30, color=GOAL), label(r"true in some possible world", font_size=26)),
            VGroup(label(r"contingent", font_size=30, color=GOAL),
                   label(r"true in some, false in others", font_size=26))).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        for r in defs:
            r[1].next_to(r[0], RIGHT, buff=0.5)
        x = max(r[0].get_right()[0] for r in defs) + 0.5
        for r in defs:
            r[1].set_x(x + r[1].width / 2)
        defs.move_to([0, -0.2, 0])
        miss = label(r"missing: \ which worlds are possible \textit{from} which \ (Kripke, Chapter 3)", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Medieval logicians kept refining the logic of necessity. Avicenna distinguished what is necessary in "
            "itself from what is necessary through another, <bookmark mark='m'/>and around 1300 John Duns Scotus argued "
            "that at the very "
            "moment I choose, I could have chosen otherwise: alternatives existing side by side, not one after "
            "another. That idea of simultaneous alternatives is the ancestor of possible worlds. Leibniz gave it its "
            "most famous picture. <bookmark mark='a'/>God surveyed infinitely many possible worlds, and created "
            "the best of them. <bookmark mark='b'/>A truth is necessary when it holds in every possible world; "
            "possible, when it holds in some; contingent, when it holds in some and fails in others. "
            "<bookmark mark='c'/>One thing was still missing, and it turned out to be the key: worlds that are "
            "possible from one world need not be possible from another. That idea arrived in 1959."
        ) as vo:
            self.play(FadeIn(med[0], shift=UP * 0.2))
            vo.wait_until("m")
            self.play(FadeIn(med[1], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(med), FadeIn(hc))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in defs], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(miss))
        self.clear_scene()
