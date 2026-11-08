from __future__ import annotations

from videos.philosophy.philosophy40.common import *  # noqa: F403


class Hume(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"The standard of taste", r"If beauty is felt, \ can anyone be wrong about it?", lit=(1757,), part=PART)
        with self.voiceover("Chapter seven. The standard of taste."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.standard()
        self.critics()
        self.price()
        self.objections()
        self.wine()
        self.wall_brick()

    def standard(self):
        head = history_card(1757, r"David Hume", r"``Of the Standard of Taste''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"the problem", r"beauty is in the mind, \ yet some judgments are better: \ is there a standard?", TASTE),
                (r"Sancho's kinsmen", r"two wine-tasters detect leather and iron; \ mocked, \ until a key on a leathern thong is found in the barrel", ART),
                (r"the true judge", r"strong sense, \ delicate sentiment, \ practice, \ comparison, \ and freedom from prejudice", SYM),
                (r"the standard", r"the joint verdict of such judges, \ and what pleases across ages and nations: \ Homer, \ still admired", GOAL)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "David Hume's essay Of the Standard of Taste, of 1757, is the classic attempt. <bookmark "
            "mark='a'/>Beauty, he says, is no quality in things themselves; it exists in the mind that contemplates "
            "them. Yet some judgments are plainly better than others. Is there a standard? <bookmark mark='b'/>He "
            "tells a story from Don Quixote: two of Sancho's kinsmen taste a hogshead of wine. One detects a taste of "
            "leather, the other of iron, and they are mocked, until the barrel is emptied and an old key on a "
            "leathern thong is found at the bottom. <bookmark mark='c'/>The true judge has strong sense, delicate "
            "sentiment, practice, the habit of comparison, and freedom from prejudice. <bookmark mark='d'/>The "
            "standard of taste is the joint verdict of such judges, and what has pleased across ages and nations: the "
            "same Homer who pleased at Athens and Rome two thousand years ago is still admired at Paris and London."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def critics(self):
        c = load("critics")
        P = c["panels"]
        k = c["correlation"]
        assert P == [1, 2, 4, 8, 16, 32, 64] and k["true judges"][-1] == 0.998 and k["prejudiced judges"][-1] == 0.622
        head = label(r"Hume's true judges, \ as an analogy", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 6, 1], y_range=[0.4, 1.0, 0.1], x_length=6.6, y_length=4.2,
                  axis_config={"color": GREY_B, "include_tip": False, "font_size": 16},
                  y_axis_config={"numbers_to_include": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                                 "decimal_number_config": {"num_decimal_places": 1}}).move_to([-2.8, -0.5, 0])
        xt = VGroup(*[label(str(n), font_size=16, color=GREY_A).next_to(ax.c2p(i, 0.4), DOWN, buff=0.15)
                      for i, n in enumerate(P)])
        xl = label(r"critics on the panel", font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.25)
        yl = label(r"how well the panel's verdict tracks quality \ (correlation)", font_size=18,
                   color=GREY_A).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        cols = {"novices": GREY_A, "true judges": TASTE, "prejudiced judges": ART}
        curves = {name: VMobject(color=cc, stroke_width=4).set_points_as_corners(
            [ax.c2p(i, v) for i, v in enumerate(k[name])]) for name, cc in cols.items()}
        side = stack([(r"30 works, \ each with a hidden quality", GREY_A),
                      (r"verdict = quality + idiosyncrasy + noise", GREY_A),
                      (rf"novices: \ 1 critic {k['novices'][0]:.2f}, \ 64 critics {k['novices'][-1]:.2f}", GREY_A),
                      (rf"true judges: \ {k['true judges'][0]:.2f} alone, \ {k['true judges'][-1]:.3f} as a panel",
                       TASTE),
                      (rf"prejudiced: \ a shared bias for fashion: \ stuck near {k['prejudiced judges'][-1]:.2f}", ART)],
                     font_size=19, buff=0.26, aligned_edge=LEFT)
        for s0 in side:
            if s0.width > 5.0:
                s0.width = 5.0
        side.move_to([4.2, -0.2, 0])
        with self.voiceover(
            "Hume's claim can be modelled, as an analogy. <bookmark mark='a'/>Thirty works have a hidden quality. "
            "Each critic's verdict is the quality, plus her own idiosyncratic taste, plus noise. <bookmark "
            "mark='b'/>Novices are noisy and idiosyncratic: one novice's verdicts correlate with quality only point "
            "four eight, though a panel of sixty four reaches point nine seven. <bookmark mark='c'/>Hume's true "
            "judges are practised and delicate: even alone they reach point eight nine, and a small panel almost "
            "perfect agreement with quality. <bookmark mark='d'/>But give skilled judges a shared prejudice, a taste "
            "for what is fashionable that has nothing to do with quality, and no panel, however large, gets much "
            "past point six. Averaging removes individual noise, not shared bias. That is why Hume required his judges "
            "to be free from prejudice, and why he trusted the test of time: the verdicts of many ages and nations, "
            "whose prejudices differ."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(curves["novices"]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(curves["true judges"]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(Create(curves["prejudiced judges"]), FadeIn(side[4]))
        self.clear_scene()

    def price(self):
        d = load("taste")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mus"] == [["BETTER", "DG", "FEEL"]] and sorted(d["mcs"]) == [["BETTER"], ["DG"], ["FEEL"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.4, width=4.0, font_size=20,
                       center=[0, -0.6, 0], title=r"The Price List: \ the paradox of taste")
        positions = [(("DG",), r"some tastes are better", r"Hume: \ true judges; \ Kant: \ a claim to everyone's "
                                                          r"agreement"),
                     (("BETTER",), r"no work is better", r"subjectivism: \ `it's all a matter of taste'"),
                     (("FEEL",), r"beauty is a property", r"aesthetic realists: \ Sibley \ (1959); \ Zangwill \ (2001)")]
        with self.voiceover(
            "Hume's essay begins from a paradox. <bookmark mark='a'/>There is no disputing about taste. Some works "
            "are better than others: whoever ranks a minor poet with Milton, Hume says, is as absurd as one who calls "
            "a molehill as high as a mountain. And judgments of beauty rest on feeling, not proof. <bookmark "
            "mark='b'/>If feeling settles beauty and no feeling is better than another, no work is better. <bookmark "
            "mark='c'/>Hume and Kant deny that all tastes are equal, keeping feeling as the ground of judgment. "
            "<bookmark mark='d'/>The subjectivist denies that any work is better. <bookmark mark='e'/>And aesthetic "
            "realists, such as Frank Sibley and Nick Zangwill, hold that beauty and grace are properties of the work, "
            "which feeling detects rather than constitutes."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cde", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=40, current=40).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(40, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the fortieth brick in the Wall. <bookmark mark='a'/>The dream was a rule for beauty: a formula, "
            "like Birkhoff's, or a ratio, like the golden one, that would settle which works are beautiful. Hume's "
            "paradox shows why none can: beauty is felt, and no rule replaces the feeling. Yet some judgments are "
            "better than others. <bookmark mark='b'/>What it forces is trust in trained judges rather than rules: "
            "Hume's joint verdict of the true judges, and the test of time."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[40], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()

    def objections(self):
        head = label(r"The problems with true judges", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the circle", r"true judges are those who judge correctly, \ and correct judgments are theirs \ (Levinson, \ 2002)", BAD),
                (r"mere exposure", r"Zajonc \ (1968): \ we come to like what we see often", TASTE),
                (r"the canon", r"Cutting \ (2003): \ the Impressionist canon tracks how often the paintings were reproduced", ART),
                (r"Hume's reply", r"the test of time: \ fashions pass, \ what survives across ages and nations is the evidence", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Hume's standard has its problems. <bookmark mark='a'/>It threatens a circle: true judges are those who "
            "judge correctly, and correct judgments are whatever true judges say, as Jerrold Levinson put it in 2002. "
            "<bookmark mark='b'/>Robert Zajonc showed in 1968 that we come to like what we merely see often. "
            "<bookmark mark='c'/>James Cutting found in 2003 that the canon of French Impressionism tracks how often "
            "the paintings were reproduced in books, and that exposure alone could shift students' preferences among "
            "them. <bookmark mark='d'/>Hume's reply is the test of time: fashions pass, and what survives across ages "
            "and nations, whose prejudices differ, is the best evidence we have."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def wine(self):
        head = label(r"Sancho's kinsmen, \ tested", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Brochet \ (2001)", r"a white wine dyed red was described by students of oenology in the words used for red wines", BAD),
                (r"Hodgson \ (2008)", r"judges at a state fair, \ given the same wine three times, \ often scored it very differently", TASTE),
                (r"but", r"trained tasters do detect faults and flavours novices miss: \ delicacy is real, \ if rarer than claimed", SYM),
                (r"the lesson", r"Hume's judges need blind tests: \ freedom from prejudice must be engineered", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Hume's wine story can be tested. <bookmark mark='a'/>Frédéric Brochet found in 2001 that when a white "
            "wine was dyed red, students of oenology described it in the vocabulary of red wines. <bookmark "
            "mark='b'/>Robert Hodgson found in 2008 that judges at a California state fair, given the same wine three "
            "times without knowing it, often scored it very differently. <bookmark mark='c'/>Yet trained tasters do "
            "detect faults and flavours that novices miss: delicacy of taste is real, if rarer than its owners claim. "
            "<bookmark mark='d'/>The lesson for Hume's true judges is that freedom from prejudice must be engineered, "
            "by tasting blind, as the jury theorem of Part 39 needed independence."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
