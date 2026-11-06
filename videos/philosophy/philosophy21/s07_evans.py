from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Evans(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Can identity be vague?", r"Is there a vague fact about whether $a$ is $b$?",
                            lit=(1978, 1988), part=PART)
        with self.voiceover("Chapter six. Can identity be vague?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.proof()
        self.models()
        self.replies()

    def proof(self):
        d = load("evans")
        hc = history_card(1978, r"Gareth Evans", r"`Can There Be Vague Objects?', \ \textit{Analysis}", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        key = label(r"$\nabla \varphi$: \ it is indeterminate whether $\varphi$; \ \ $\Delta\varphi$: \ determinately "
                    r"$\varphi$", font_size=19, color=GREY_A).next_to(hc, DOWN, buff=0.25).to_edge(LEFT, buff=0.5)
        steps = VGroup()
        for i, (f, why) in enumerate(d["steps"]):
            m = MathTex(r"(" + str(i + 1) + r")\quad " + f, font_size=32, color=OK if i == 4 else WHITE)
            w = label(why, font_size=20, color=GREY_A)
            row = VGroup(m, w)
            m.move_to([-5.6 + m.width / 2, 0.8 - 0.75 * i, 0])
            w.move_to([0.8 + w.width / 2, 0.8 - 0.75 * i, 0])
            if w.width > 6.0:
                w.width = 6.0
                w.move_to([0.8 + w.width / 2, 0.8 - 0.75 * i, 0])
            steps.add(row)
        concl = label(r"assume indeterminate identity, \ derive determinate distinctness: \ no vague identity",
                      font_size=20, color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Could it be vague whether two things are one? A cloud's edges are vague; perhaps so is whether this "
            "cloud is that one. In a single page, Gareth Evans argued no. <bookmark mark='a'/>Suppose it is "
            "indeterminate whether a is b. <bookmark mark='b'/>Then b has a property: being such that it is "
            "indeterminate whether it is a. <bookmark mark='c'/>But a is determinately a; it is not indeterminate "
            "whether a is a. <bookmark mark='d'/>So a lacks that property. <bookmark mark='e'/>By Leibniz's law, a and "
            "b differ in a property, so a is not b. The assumption of indeterminate identity yields distinctness. "
            "Identity, Evans concluded, cannot be vague."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(key))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            self.play(FadeIn(concl))
        self.clear_scene()

    def models(self):
        d = load("evans")
        head = label(r"Model-checked over precisifications", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        n = d["precisifications"]
        ex = d["example"]
        cols = [PARTC, WHOLE, NOM]
        grid = VGroup()
        for j in range(n):
            x = -4.4 + 1.55 * j
            tl = label(r"sharpening " + f"{j + 1}", font_size=19, color=GREY_A).move_to([x, 1.7, 0])
            da = Dot([x, 1.0, 0], radius=0.2, color=cols[ex["a"][j]])
            db = Dot([x, 0.2, 0], radius=0.2, color=cols[ex["b"][j]])
            eq = label(r"$a = b$" if ex["a"][j] == ex["b"][j] else r"$a \ne b$", font_size=21,
                       color=OK if ex["a"][j] == ex["b"][j] else BAD).move_to([x, -0.45, 0])
            grid.add(VGroup(tl, da, db, eq))
        nl = VGroup(label(r"$a$ denotes", font_size=19, color=GREY_A).move_to([-6.1, 1.0, 0]),
                    label(r"$b$ denotes", font_size=19, color=GREY_A).move_to([-6.1, 0.2, 0]))
        rows = stack([(r"names denote objects \ (colours) \ on each way of making the language precise", WHITE),
                      (r"with rigid names: \ " + f"{d['rigid_vague']}" + r" of " + f"{d['rigid_pairs']}" +
                       r" pairs make $a = b$ indeterminate", OK),
                      (r"with non-rigid names: \ " + f"{d['nonrigid_vague']}" + r" of " + f"{d['all_pairs']}" +
                       r" do, \ like this one", GOAL),
                      (r"but then step (2) fails: \ `$b$ is such that \dots' \ has no single object to be about", BAD),
                      (r"Lewis \ (1988): \ the vagueness is in our words, \ not in the objects", UNIV)],
                     font_size=20, aligned_edge=LEFT, width=6.2).move_to([3.7, -0.4, 0])
        with self.voiceover(
            "The Reasoner tests the argument on models. <bookmark mark='a'/>Treat vagueness as many admissible ways "
            "of making our language precise; on each, the names a and b denote objects, shown as colours. Determinately "
            "means on every sharpening. <bookmark mark='b'/>If both names are rigid, denoting the same object on "
            "every sharpening, the Reasoner finds that no pair makes a equals b indeterminate: none of nine. "
            "<bookmark mark='c'/>If names may shift, many pairs do: here a is the same on every sharpening, and b "
            "coincides with it on two of three. <bookmark mark='d'/>But then step two of Evans's proof has nothing to "
            "be about: b does not pick out a single object of which we can predict anything. "
            "<bookmark mark='e'/>David Lewis drew the moral: Evans is right that objects cannot be vaguely identical; "
            "the vagueness lies in which objects our words pick out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g_) for g_ in grid], lag_ratio=0.3), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def replies(self):
        head = label(r"Vague objects anyway?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"semantic vagueness", r"Lewis, \ Fine: \ all vagueness is in language: \ many precise candidates, \ "
                                    r"none chosen \ (Part 5)", UNIV),
            (r"epistemicism", r"Williamson \ (1994): \ every identity is sharp, \ but we cannot know where the line is",
             ABS),
            (r"ontic vagueness", r"Tye; \ Barnes and Williams \ (2011): \ the world itself is indeterminate; \ "
                                 r"Evans's step (2) is denied", NOM),
            (r"van Inwagen \ (1988)", r"vague identity is allowed, \ but contraposition fails in a three-valued "
                                      r"logic", BAD),
            (r"the stakes", r"Parfit's spectrum and fission ask whether `is it me?' \ can lack a determinate answer",
             GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Not everyone accepts Evans's conclusion. <bookmark mark='a'/>Most take the semantic view, with Lewis "
            "and Kit Fine: all vagueness lies in language, where many precise candidate meanings are left unchosen, "
            "as in Part 5. <bookmark mark='b'/>Timothy Williamson's epistemicism says every identity is sharp, but we "
            "cannot know where the line falls. <bookmark mark='c'/>Others defend vagueness in the world itself: "
            "Michael Tye, and Elizabeth Barnes and Robert Williams, who deny Evans's abstraction step. "
            "<bookmark mark='d'/>Peter van Inwagen allows vague identity, and gives up contraposition in a "
            "three-valued logic. <bookmark mark='e'/>The stakes are personal: Parfit's spectrum and fission ask "
            "whether is it me can lack a determinate answer."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
