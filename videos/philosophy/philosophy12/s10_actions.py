from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Actions(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Announcements, secrets and lies", r"How does information change a model?",
                            lit=(), part=PART)
        with self.voiceover("Chapter nine. Announcements, secrets and lies."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.public()
        self.private()
        self.lies()

    def public(self):
        head = label(r"Public announcement logic", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        f = MathTex(r"M, w \models [\psi]\varphi \iff \big(M, w \models \psi \ \Rightarrow\ M|_{\psi}, w \models "
                    r"\varphi\big)", font_size=34, color=GOAL).next_to(head, DOWN, buff=0.45)
        rows = VGroup(
            label(r"$M|_\psi$: \ the model with every $\lnot\psi$ world deleted", font_size=24),
            label(r"the reduction axioms rewrite every $[\psi]$ away: \ e.g. \ $[\psi]K_a\varphi \leftrightarrow "
                  r"(\psi \rightarrow K_a[\psi]\varphi)$", font_size=23, color=GREY_A),
            label(r"so the logic is no stronger than epistemic logic itself, \ yet it describes change", font_size=23,
                  color=GREY_A),
            label(r"but common knowledge needs more: \ `relativized' common knowledge (van Benthem, van Eijck, Kooi "
                  r"2006)", font_size=21, color=GREY_B)).arrange(DOWN, buff=0.3).move_to([0, -0.9, 0])
        with self.voiceover(
            "Every announcement so far has deleted worlds. <bookmark mark='a'/>Public announcement logic makes this "
            "a modality: after the announcement of psi, phi holds, if phi is true in the model with every "
            "not-psi world deleted. <bookmark mark='b'/>Plaza showed that the new operator can always be rewritten "
            "away. After psi, a knows phi, just when, if psi is true, a knows that after psi, phi. "
            "<bookmark mark='c'/>So the logic is no stronger than epistemic logic itself, yet it describes how "
            "knowledge changes. <bookmark mark='d'/>Common knowledge is the exception: to rewrite it away one needs "
            "a richer operator, relativized common knowledge, found by van Benthem, van Eijck and Kooi in 2006."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            for mk, r in zip("abcd", rows):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def private(self):
        d = load("private")
        head = label(r"A private message: \ the product update", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        who = label(r"Baltag, \ Moss \ and Solecki (1998)", font_size=21, color=GREY_B).next_to(head, DOWN, buff=0.15)
        # the static model: p, ~p; nobody knows
        mpos = {"p": [-1.0, 0, 0], "~p": [1.0, 0, 0]}
        M = AgentGraph(["p", "~p"], {"a": [("p", "~p")], "b": [("p", "~p")]}, mpos, {"p": r"p", "~p": r"\lnot p"},
                       radius=0.38, font_size=24, center=[-4.6, 0.6, 0], offsets={"a": 0.08, "b": -0.08})
        Ml = label(r"before: \ neither knows $p$", font_size=19, color=GREY_A).next_to(M, DOWN, buff=0.2)
        times = MathTex(r"\otimes", font_size=50, color=GREY_B).move_to([-2.6, 0.6, 0])
        epos = {"read": [0, 0.6, 0], "skip": [0, -0.6, 0]}
        E = VGroup(
            VGroup(RoundedRectangle(width=1.8, height=0.6, corner_radius=0.15, color=COMMON),
                   label(r"read: \ pre $p$", font_size=19)).move_to([-1.0, 1.2, 0]),
            VGroup(RoundedRectangle(width=1.8, height=0.6, corner_radius=0.15, color=GREY_B),
                   label(r"skip: \ pre $\top$", font_size=19)).move_to([-1.0, 0.0, 0]))
        for e in E:
            e[1].move_to(e[0])
        eb = Arrow(E[0].get_bottom(), E[1].get_top(), buff=0.05, color=AG["b"], stroke_width=3)
        el = label(r"Bob thinks: \ nothing happened", font_size=18, color=AG["b"]).next_to(eb, RIGHT, buff=0.1)
        eq = MathTex(r"=", font_size=50, color=GREY_B).move_to([2.35, 0.6, 0])
        ppos = {"p/read": [0, 0.9, 0], "p/skip": [-0.9, -0.6, 0], "~p/skip": [0.9, -0.6, 0]}
        N = AgentGraph(["p/read", "p/skip", "~p/skip"], {"b": [("p/skip", "~p/skip")], "a": [("p/skip", "~p/skip")]},
                       ppos, {"p/read": r"p\,/\,\text{read}", "p/skip": r"p\,/\,\text{skip}",
                              "~p/skip": r"\lnot p\,/\,\text{skip}"}, radius=0.55, font_size=17, center=[4.4, 0.6, 0],
                       offsets={"a": 0.07, "b": -0.07})
        arrow_b = VGroup(*[Arrow(N.pos["p/read"], N.pos[w], buff=0.6, color=AG["b"], stroke_width=3)
                           for w in ("p/skip", "~p/skip")])
        rows = VGroup(
            VGroup(label(r"Ann knows $p$", font_size=22), mark(d["a_knows_p"], 26)).arrange(RIGHT, buff=0.3),
            VGroup(label(r"Bob does not", font_size=22), mark(not d["b_knows_p"], 26)).arrange(RIGHT, buff=0.3),
            VGroup(label(r"Bob believes Ann still doesn't know", font_size=22),
                   mark(d["b_thinks_a_ignorant"], 26)).arrange(RIGHT, buff=0.3),
            VGroup(label(r"$p$ is not common knowledge", font_size=22), mark(not d["common_p"], 26)).arrange(
                RIGHT, buff=0.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Private information needs more than deletion. <bookmark mark='a'/>Alexandru Baltag, Lawrence Moss and "
            "Sławomir Solecki modelled it as a product. Start with what Ann and Bob know: p, or not p, and neither "
            "can tell. <bookmark mark='b'/>Then an action model: the events that might happen, and who can tell them "
            "apart. Ann reads a letter saying p; that event can only happen where p is true. Or nothing happens. Bob "
            "sees nothing, so as far as he can tell, nothing happened. <bookmark mark='c'/>The product pairs every "
            "world with every event that can happen there, and an agent confuses two pairs when she confuses both the "
            "worlds and the events. <bookmark mark='d'/>The Reasoner computes it. In the actual pair, p and read, Ann "
            "knows p. Bob does not. Bob, wrongly but rationally, believes Ann still does not know. And p is not common "
            "knowledge. Strictly, Bob's new state is belief rather than knowledge, since the world he thinks actual "
            "is not: product updates naturally produce belief, and this is where the logics of belief take over."
        ) as vo:
            self.play(FadeIn(head), FadeIn(who))
            vo.wait_until("a")
            self.play(FadeIn(M), FadeIn(Ml))
            vo.wait_until("b")
            self.play(FadeIn(times), FadeIn(E), GrowArrow(eb), FadeIn(el))
            vo.wait_until("c")
            self.play(FadeIn(eq), FadeIn(N), *[GrowArrow(a) for a in arrow_b])
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.5), run_time=4)
        self.clear_scene()

    def lies(self):
        head = label(r"Lies, \ and why they still inform", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"a lie: \ announcing $\psi$ where $\psi$ is false", font_size=24),
            label(r"deletion cannot model it: \ the actual world would vanish", font_size=24, color=BAD),
            label(r"so dynamic logics of belief revise instead: \ the listener comes to \textit{believe} $\psi$",
                  font_size=23, color=GREY_A),
            label(r"van Ditmarsch (2014), \ `Dynamics of lying': \ lies, bluffs, and the liar who is believed",
                  font_size=21, color=GREY_B),
            label(r"knowledge only ever shrinks the space; \ belief can move to the wrong part of it \ (Part 14)",
                  font_size=24, color=GOAL)).arrange(DOWN, buff=0.32).move_to([0, -0.4, 0])
        with self.voiceover(
            "And what about lies? <bookmark mark='a'/>A lie announces psi where psi is false. "
            "<bookmark mark='b'/>Deletion cannot model it: the actual world itself would be deleted. "
            "<bookmark mark='c'/>So the dynamic logics of belief revise instead of deleting: the listener comes to "
            "believe psi, and the actual world survives, now ranked as implausible. <bookmark mark='d'/>Hans van "
            "Ditmarsch has worked out the logic of lies, bluffs, and liars who are believed. <bookmark mark='e'/>"
            "Knowledge can only shrink the space of possibilities. Belief can move to the wrong part of it. Part 14 "
            "is about how rational belief changes."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
