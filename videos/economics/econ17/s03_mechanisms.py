from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403


def box(text, color, w=2.6, h=1.0, font_size=22):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=color, stroke_width=3,
                         fill_color=BACKGROUND, fill_opacity=1)
    return VGroup(r, label(text, font_size=font_size, color=color).move_to(r))


class Mechanisms(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Mechanisms, \ and the revelation principle", r"If people will game any rule, \ which rules "
             r"are worth considering?", "Chapter two. Mechanisms, and the revelation principle.",
             lit={1960: r"Hurwicz", 1979: r"Myerson; \ Dasgupta, Hammond and Maskin", 2007: r"the Nobel prize"},
             scale=("person", "market"), horizon=("a day",))
        self.rules()
        self.picture()
        self.checklist()

    def rules(self):
        rows = VGroup(
            label(r"a mechanism: \ a rule that turns what people say into what happens", font_size=26, color=MECH),
            label(r"an auction, \ a vote, \ a school assignment, \ a tax: \ all mechanisms", font_size=24),
            label(r"people know things the designer doesn't: \ their values, \ their preferences, \ their costs",
                  font_size=24, color=GREY_A),
            label(r"and they'll say whatever gets them the most, \ given how others play", font_size=24,
                  color=REJECT),
            label(r"Leonid Hurwicz, \ from 1960: \ design the rule knowing it will be played", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Hurwicz (1960, 1972); \ the Nobel prize to Hurwicz, Maskin and Myerson (2007)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "The Boston rule is a mechanism. <bookmark mark='a'/> A mechanism is any rule that turns what people "
            "say into what happens. <bookmark mark='b'/> An auction is one, and so is a vote, a school assignment, "
            "or a tax. <bookmark mark='c'/> The trouble is that people know things the designer does not: what "
            "things are worth to them, what they prefer, what they cost. <bookmark mark='d'/> And they will say "
            "whatever gets them the most, given how everyone else plays, as you were tempted to in Play it. "
            "<bookmark mark='e'/> From 1960 Leonid Hurwicz built a theory of rules designed in the knowledge that "
            "they will be played as games. He shared the 2007 Nobel prize for it, with Eric Maskin and Roger "
            "Myerson."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def picture(self):
        head = label(r"the revelation principle, \ in one picture", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.4)
        types = box(r"what you know", WHITE, w=2.4).move_to(LEFT * 5.2 + UP * 0.8)
        strat = box(r"your best play", HELD, w=2.5).move_to(LEFT * 1.8 + UP * 0.8)
        mech = box(r"any rule", MECH, w=2.2).move_to(RIGHT * 1.4 + UP * 0.8)
        out = box(r"what happens", STABLE, w=2.4).move_to(RIGHT * 4.9 + UP * 0.8)
        arrows = VGroup(Arrow(types.get_right(), strat.get_left(), buff=0.1, color=GREY_B),
                        Arrow(strat.get_right(), mech.get_left(), buff=0.1, color=GREY_B),
                        Arrow(mech.get_right(), out.get_left(), buff=0.1, color=GREY_B))
        wrap = DashedVMobject(RoundedRectangle(width=VGroup(strat, mech).width + 0.6, height=1.7, corner_radius=0.2,
                                               stroke_color=STABLE, stroke_width=3), num_dashes=40).move_to(
            VGroup(strat, mech))
        wl = label(r"a new rule: \ ``tell me what you know, \ and I'll play your best play for you''",
                   font_size=22, color=STABLE).next_to(wrap, DOWN, buff=0.3)
        rows = VGroup(
            label(r"under the new rule, \ telling the truth is a best reply", font_size=24, color=STABLE),
            label(r"so whatever any rule can achieve, \ a rule where truth is safe can achieve too", font_size=24),
            label(r"the designer may look only at truthful rules: \ the search gets much smaller", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).next_to(wl, DOWN, buff=0.45)
        tag = published_tag(r"Myerson, Econometrica 47(1) (1979); \ Gibbard (1973)", corner=DR, font_size=13)
        with self.voiceover(
            "Which rules are worth considering, when every rule will be gamed? A simple picture cuts the search "
            "down. <bookmark mark='a'/> Under any rule, each person goes from what they know to their best play, "
            "and the rule turns the plays into what happens. <bookmark mark='b'/> Now build a new rule: tell me what "
            "you know, and I will make your best play for you. <bookmark mark='c'/> Under the new rule, telling the "
            "truth is a best reply, since lying would only make the rule play for someone you are not. "
            "<bookmark mark='d'/> So whatever any rule can achieve in equilibrium, a rule where the truth is safe "
            "can achieve too. <bookmark mark='e'/> That is the revelation principle, and it lets a designer look "
            "only at rules where people tell the truth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(types), GrowArrow(arrows[0]), FadeIn(strat), GrowArrow(arrows[1]), FadeIn(mech),
                      GrowArrow(arrows[2]), FadeIn(out), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(wrap), FadeIn(wl))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def checklist(self):
        head = label(r"what a designer wants, \ and what each rule delivers", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.35)
        cols = [r"efficient", r"truth is safe", r"voluntary", r"pays for itself", r"stable"]
        rules = [
            (r"Vickrey--Clarke--Groves", ["y", "y", "y", "n", "-"], MONEY),
            (r"double auction", ["n", "n", "y", "y", "-"], HELD),
            (r"the Boston rule", ["n", "n", "y", "y", "n"], REJECT),
            (r"deferred acceptance", ["~", "~", "y", "y", "y"], STABLE),
            (r"top trading cycles", ["y", "y", "y", "y", "n"], KIDNEY),
        ]
        xs = [-3.0, -0.6, 1.4, 3.3, 5.3]
        hdr = VGroup(*[label(c, font_size=20, color=GREY_B).move_to([x, 2.3, 0]) for c, x in zip(cols, xs)])
        sym = {"y": (r"\checkmark", STABLE), "n": (r"\times", REJECT), "~": (r"\sim", HELD), "-": (r"\cdot", GREY_C)}
        rows = VGroup()
        for i, (name, marks, c) in enumerate(rules):
            y = 1.55 - 0.72 * i
            g = VGroup(label(name, font_size=22, color=c).move_to([-5.8, y, 0], aligned_edge=LEFT))
            for m, x in zip(marks, xs):
                s, col = sym[m]
                g.add(MathTex(s, font_size=38, color=col).move_to([x, y, 0]))
            rows.add(g)
        foot = VGroup(
            label(r"$\sim$: \ for the proposing side only; \ efficient among stable matchings for them", font_size=19,
                  color=GREY_A),
            label(r"no rule ticks every box: \ Gibbard and Satterthwaite (1973, 1975) for votes, \ Myerson and "
                  r"Satterthwaite (1983) for trade", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is what a designer usually wants. The outcome should be efficient. Telling the truth should be "
            "safe. Taking part should be voluntary, with nobody worse off than if they had stayed away. The rule "
            "should pay for itself, without outside money. And, when people are being matched, it should be stable: "
            "no pair should want to break away together. <bookmark mark='a'/> Vickrey, Clarke and Groves's rule "
            "is efficient, truthful and voluntary, but does not pay for itself, as chapter three shows. "
            "<bookmark mark='b'/> The double auction pays for itself but is not efficient: chapter four. "
            "<bookmark mark='c'/> The Boston rule fails on truth and on stability. <bookmark mark='d'/> Deferred "
            "acceptance is stable, and truthful for the side that proposes. <bookmark mark='e'/> And top trading "
            "cycles, in chapter nine, is efficient and truthful but not stable. <bookmark mark='f'/> No rule ticks "
            "every box, and there are theorems saying none can."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()
