from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Compatibilism(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Compatibilism", r"Could freedom be something determinism leaves intact?",
                            lit=(1971, 1998), part=PART)
        with self.voiceover("Chapter six. Compatibilism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.classical()
        self.hierarchy()
        self.reasons()
        self.responsive()
        self.miracles()
        self.price()

    def classical(self):
        head = label(r"Freedom as acting as you will", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Hobbes \ (1651)", r"liberty is the absence of external impediments to doing what one wills", LAW),
                (r"Hume \ (1748)", r"`a power of acting or not acting, \ according to the determinations of the will'",
                 LAW),
                (r"the conditional analysis", r"`could have done otherwise' means `would have, \ had he chosen to'",
                 WILL),
                (r"the trouble", r"what if he could not have chosen to? \ a phobia, \ a compulsion: \ the analysis "
                                 r"says free", BAD)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "Compatibilists say that freedom, properly understood, is something determinism leaves intact. "
            "<bookmark mark='a'/>For Thomas Hobbes, liberty is just the absence of external impediments to doing "
            "what one wills. <bookmark mark='b'/>For David Hume, it is a power of acting or not acting, according to "
            "the determinations of the will. <bookmark mark='c'/>On this view, he could have done otherwise means: "
            "he would have, had he chosen to; and that can be true in a deterministic world. "
            "<bookmark mark='d'/>The trouble is a person who could not have chosen otherwise, someone in the grip of "
            "a phobia or a compulsion. The conditional is true of them too, and they are not free."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def hierarchy(self):
        hc = history_card(1971, r"Harry Frankfurt", r"`Freedom of the Will and the Concept of a Person'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        def box(t, c, at):
            return VGroup(RoundedRectangle(width=4.0, height=0.9, corner_radius=0.2, color=c, fill_opacity=0.1),
                          label(t, font_size=19, color=c)).move_to(at)
        a1 = box(r"a desire for the drug", BLAME, [-3.6, -1.2, 0])
        a2 = box(r"a desire to be rid of it", SELF, [-3.6, 0.6, 0])
        b1 = box(r"a desire for the drug", BLAME, [2.4, -1.2, 0])
        b2 = box(r"a desire to have it", SELF, [2.4, 0.6, 0])
        aa = Arrow(a2.get_bottom(), a1.get_top(), buff=0.1, color=BAD)
        ba = Arrow(b2.get_bottom(), b1.get_top(), buff=0.1, color=OK)
        al = label(r"the unwilling addict", font_size=21, color=BAD).next_to(a1, DOWN, buff=0.3)
        bl = label(r"the willing addict", font_size=21, color=OK).next_to(b1, DOWN, buff=0.3)
        foot = label(r"free will: \ the will you act on is the will you want to have", font_size=21,
                     color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Frankfurt's second great paper, of 1971, located freedom in the structure of the will. "
            "<bookmark mark='a'/>We have desires, and we also have desires about our desires. Consider two addicts. "
            "<bookmark mark='b'/>The unwilling addict craves the drug, and wants not to want it. When he takes it, "
            "he acts on a desire he repudiates. <bookmark mark='c'/>The willing addict craves it too, but endorses "
            "the craving. Both are equally unable to stop; only the second acts freely. "
            "<bookmark mark='d'/>Free will, for Frankfurt, is having the will you want to have. Nothing in that "
            "requires the will to be undetermined."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(a1), FadeIn(b1))
            vo.wait_until("b")
            self.play(FadeIn(a2), GrowArrow(aa), FadeIn(al))
            vo.wait_until("c")
            self.play(FadeIn(b2), GrowArrow(ba), FadeIn(bl))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def reasons(self):
        head = label(r"Reasons-responsiveness, \ and local miracles", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Fischer and Ravizza \ (1998)", r"guidance control: \ the act issues from the agent's own mechanism, "
                                                  r"\ which would respond to reasons", SELF),
                (r"moderately", r"would recognize a sufficient reason to do otherwise in some range of cases, \ and "
                                r"act on it in at least one", WILL),
                (r"Lewis \ (1981)", r"`Are We Free to Break the Laws?': \ I could have done something such that, \ "
                                    r"had I done it, \ a law would have been broken", LAW),
                (r"against the argument", r"so the laws are not fixed in the sense premise 1 needs", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "The most developed compatibilism today is John Martin Fischer and Mark Ravizza's. "
            "<bookmark mark='a'/>An agent has guidance control of an act when it issues from a mechanism that is "
            "the agent's own and that responds to reasons. <bookmark mark='b'/>Responds moderately: it would "
            "recognize sufficient reasons to do otherwise across a range of cases, and act on them in at least one. "
            "That is a fact about the mechanism, and it holds in a deterministic world. "
            "<bookmark mark='c'/>David Lewis attacked the consequence argument directly. I could have raised my "
            "hand, he said, though only in the weak sense that I could have done something such that, had I done "
            "it, a law would have been broken, a small local miracle. <bookmark mark='d'/>In that sense the laws "
            "are not fixed, and the repaired argument's first premise is false."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def responsive(self):
        d = load("responsive")
        head = label(r"Reasons-responsiveness, \ checked", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        A = d["agents"]
        assert d["desire"] == 5 and A["a responsive agent"]["moderate"] and not A["an erratic agent"]["moderate"]
        assert not A["a compulsive agent"]["weak"]
        x0, step = -2.4, 0.62
        nums = VGroup(*[label(str(r), font_size=17, color=GREY_A).move_to([x0 + step * k, 1.6, 0])
                        for k, r in enumerate(d["reasons"])])
        nl = label(r"strength of the reason to refrain \ (desire: \ 5)", font_size=17, color=GREY_A).next_to(
            nums, UP, buff=0.2)
        line = DashedLine([x0 + step * 5.5, 1.9, 0], [x0 + step * 5.5, -1.3, 0], color=GREY_C)
        rows = VGroup()
        for j, (name, a) in enumerate(A.items()):
            y = 0.9 - 0.8 * j
            marks = VGroup(*[Dot([x0 + step * k, y, 0], radius=0.11, color=OK if v else BAD)
                             for k, v in enumerate(a["refrains"])])
            verdict = label(r"moderately responsive" if a["moderate"] else (r"not regular" if a["weak"] else
                                                                            r"not reactive"),
                            font_size=17, color=OK if a["moderate"] else BAD).move_to([5.6, y, 0])
            rows.add(VGroup(label(name, font_size=18, color=WHITE).move_to([-5.0, y, 0]), marks, verdict))
        key = label(r"green: \ refrains \quad red: \ takes it", font_size=16, color=GREY_A).move_to([0, -1.55, 0])
        foot = stack([(r"weak reactivity: \ refrains on at least one sufficient reason", WILL),
                      (r"regular receptivity: \ the refusals form an intelligible pattern", SELF)], font_size=19,
                     buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The conditions can be checked on mechanisms. <bookmark mark='a'/>Each faces eleven scenarios in which "
            "a desire of strength five to take a drug meets a reason to refrain of strength zero to ten. "
            "<bookmark mark='b'/>The responsive agent refrains exactly when the reason outweighs the desire. "
            "<bookmark mark='c'/>The erratic agent refrains at seven and at ten, but takes it at eight and nine. It "
            "responds to some sufficient reason, so it is weakly reactive, but its refusals form no intelligible "
            "pattern: it is not regularly receptive. <bookmark mark='d'/>The compulsive agent takes it whatever the "
            "reason: not reactive at all. <bookmark mark='e'/>Only the first is moderately reasons-responsive, and so, "
            "on Fischer and Ravizza's view, responsible, whether or not its mechanism is deterministic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nums), FadeIn(nl), Create(line), FadeIn(key))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), LaggedStart(*[GrowFromCenter(m) for m in r[1]], lag_ratio=0.05),
                          FadeIn(r[2]))
                if mk == "b":
                    self.play(FadeIn(foot[0]))
                if mk == "c":
                    self.play(FadeIn(foot[1]))
            vo.wait_until("e")
            self.play(Indicate(rows[0], color=OK, scale_factor=1.03))
        self.clear_scene()

    def miracles(self):
        d = load("miracles")
        head = label(r"A small miracle, \ or a different past \ (Lewis, \ 1979)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        assert d["miracle_changes_act"] and d["lawful_diff_at_0"] == 17 and d["width"] == 61 and d["steps"] == 30
        diff = np.array(d["diff"])
        act = np.array(d["actual"])
        T, W = diff.shape
        rgb = np.zeros((T, W, 3), dtype=np.uint8)
        rgb[act == 1] = [60, 70, 90]
        rgb[act == 0] = [22, 26, 34]
        rgb[diff == 1] = [242, 166, 90]
        rgb = rgb[::-1]                                          # time runs up the screen
        rgb = np.kron(rgb, np.ones((8, 8, 1), dtype=np.uint8))
        img = ImageMobject(rgb)
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        img.height = 4.6
        img.move_to([-3.0, -0.4, 0])
        cell = img.height / T
        agent = Square(side_length=cell * 1.4, color=WILL, stroke_width=3).move_to(
            img.get_corner(UL) + np.array([(d["agent"] + 0.5) * cell, -0.5 * cell, 0]))
        tl = VGroup(label(r"now: \ the act", font_size=16, color=WILL).next_to(img, UP, buff=0.1),
                    label(r"the remote past", font_size=16, color=GREY_A).next_to(img, DOWN, buff=0.1),
                    label(r"time", font_size=16, color=GREY_A).rotate(PI / 2).next_to(img, LEFT, buff=0.15))
        side = stack([(r"a deterministic, \ reversible world: \ 61 cells, \ 30 steps", GREY_A),
                      (r"a small miracle: \ change 1 cell just before, \ and the act differs; \ the past is ours",
                       OK),
                      (r"no miracle: \ the laws, \ run backward, \ make the past differ too: \ 17 cells at time "
                       r"0 \ (orange)", BAD),
                      (r"Lewis: \ `could have done otherwise' needs only the first", GOAL)], font_size=19,
                     aligned_edge=LEFT, width=5.2, buff=0.3).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Lewis's point can be seen on a toy world. <bookmark mark='a'/>Here is a deterministic world, sixty one "
            "cells wide, run for thirty steps by a reversible law: each state fixes the next, and the previous. One "
            "cell at the top is an agent's act. <bookmark mark='b'/>What would a world be like in which the act "
            "differed? One answer: a small miracle. Change one cell just before the act, and let the laws resume. "
            "The act differs, and the whole past is exactly ours. <bookmark mark='c'/>The other answer: no miracle at "
            "all. Then the laws hold everywhere, and running them backward from the different act, the difference "
            "spreads into the past, one cell per step. By time zero, seventeen cells of the world differ, scattered "
            "across its whole width. <bookmark mark='d'/>Lewis argued that when we say we could have done "
            "otherwise, we mean the first kind of world: one that departs from ours by a small miracle just before "
            "we act. We are able to do something such that, had we done it, a law would have been broken; we are "
            "not able to break a law."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(img), FadeIn(tl), Create(agent), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(agent, color=WILL))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def price(self):
        d = load("tetrad")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert sorted(d["mcs"]) == [["A"], ["C"], ["D"], ["F"]]
        sv = d["survey"]
        assert (sv["compatibilism"], sv["libertarianism"], sv["no free will"]) == (0.592, 0.188, 0.112)
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.4, width=3.8, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ free will")
        positions = [(("F",), r"no free will", r"hard determinism; \ Pereboom", sv["no free will"],
                      r"PhilPapers 2020"),
                     (("A",), r"source compatibilism", r"Frankfurt; \ Fischer", None, r"counted with compatibilism"),
                     (("C",), r"leeway compatibilism", r"Hume; \ Lewis; \ Vihvelin", sv["compatibilism"],
                      r"compatibilism, \ both kinds"),
                     (("D",), r"libertarianism", r"Kane; \ O'Connor; \ van Inwagen", sv["libertarianism"],
                      r"PhilPapers 2020")]
        with self.voiceover(
            "Four claims cannot all be true. <bookmark mark='a'/>Some of our acts are free. An act is free only if "
            "the agent could have done otherwise. If determinism is true, no one could ever have done otherwise. "
            "And determinism is true. <bookmark mark='b'/>One has to go. <bookmark mark='c'/>Deny the first: there "
            "is no free will, the view of hard determinists and of Derk Pereboom, held by eleven percent of "
            "philosophers in the PhilPapers survey of 2020. <bookmark mark='d'/>Deny the second, with Frankfurt and "
            "Fischer: freedom does not need alternatives. <bookmark mark='e'/>Deny the third, with Hume and Lewis: "
            "we could have done otherwise, in the sense that matters, even if determinism is true. Compatibilists "
            "of both kinds together are fifty nine percent. <bookmark mark='f'/>Or deny the fourth: libertarians, "
            "nineteen percent, hold that freedom requires indeterminism, and that we have it. The next chapter "
            "asks how."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who, share, note) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, share=share, share_note=note, width=3.0)
                self.play(*anims)
        self.clear_scene()
