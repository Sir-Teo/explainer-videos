from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.roads()
        self.island()
        self.question()
        self.title()
        self.objectives()

    def roads(self):
        T = tables.OLKEN_2007.data
        chain = flow_chain([(r"a village \\ road, \ built", POOR), (r"engineers dig \\ core samples", AUDIT),
                            (r"price what is \\ really in it", AUDIT), (r"compare with \\ the books", CORRUPT)],
                           notes=[rf"over {T['projects']} \\ projects, \ Indonesia",
                                  r"how much sand, \\ rock, \ gravel",
                                  r"and the labour \\ it took", r"the gap is \\ missing money"],
                           box_w=2.8, font_size=20, note_size=17)
        chain.move_to(UP * 1.2)
        cures = VGroup(
            VGroup(label(r"from above", font_size=22, color=AUDIT),
                   label(rf"an audit: \ the chance raised \\ from {T['audit_from']}\% to {T['audit_to']}\%",
                         font_size=19, color=GREY_A)).arrange(DOWN, buff=0.12),
            VGroup(label(r"from below", font_size=22, color=VOTER),
                   label(r"village meetings \\ to account for \\ the money", font_size=19, color=GREY_A)
                   ).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=2.4).move_to(DOWN * 1.9)
        tag = published_tag(tables.OLKEN_2007.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In the early 2000s the economist Benjamin Olken wanted to know how much of the money for new roads in "
            f"Indonesian villages was stolen. <bookmark mark='a'/> Over {T['projects']} villages were building a road. "
            "<bookmark mark='b'/> When each road was finished, he sent engineers to dig core samples out of it, "
            "<bookmark mark='c'/> to estimate how much sand, rock and gravel was really in it, and what the "
            "materials and the labour would have cost. <bookmark mark='d'/> The gap between that and what the "
            "village reported spending is money that went missing. More than a fifth of it, on average. "
            "<bookmark mark='e'/> Then he tested two cures, drawn at random: an audit from above, by government "
            "auditors, <bookmark mark='f'/> and village meetings from below, where the money had to be accounted for "
            "in front of the people it was meant for."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(cures[0], shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(cures[1], shift=UP * 0.1))
        self.clear_scene()

    def island(self):
        R = load("roads")
        rows = [(r"no audit, \\ no meeting", R["control"], CONTROL),
                (r"effect of \\ an audit", R["audit"], AUDIT),
                (r"effect of \\ meetings", R["meetings"], VOTER)]
        ax = plane([0, 3], [-0.15, 0.35], center=LEFT * 1.8 + DOWN * 0.3, x_length=6.6, y_length=4.6, xticks=[],
                   yticks=[-0.1, 0, 0.1, 0.2, 0.3], ylabel=r"share of spending missing, \ and changes in it",
                   yfmt=lambda v: f"{100 * v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        zero = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(3, 0), color=GREY_B, stroke_width=1.4)
        bars = VGroup()
        for i, (nm, v, col) in enumerate(rows):
            p0, p1 = ax.ax.c2p(0.5 + i - 0.3, 0), ax.ax.c2p(0.5 + i + 0.3, v)
            r = Rectangle(width=p1[0] - p0[0], height=max(abs(p1[1] - p0[1]), 0.02), stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(nm, font_size=15, color=WHITE).next_to(ax.ax.c2p(0.5 + i, -0.15), DOWN,
                                                                             buff=0.12),
                            label(rf"{100 * v:+.1f}".replace("-", "{-}") if i else rf"{100 * v:.1f}\%",
                                  font_size=17, color=WHITE).next_to(r, UP if v >= 0 else DOWN, buff=0.06)))
        side = VGroup(
            label(rf"the Island: \ {TRUTH['roads']['n']} road projects, \\ audits and meetings \\ drawn at random",
                  font_size=18, color=WHITE),
            label(rf"audits: \ {100 * R['audit']:+.1f} points \\ (s.e. {100 * R['audit_se']:.1f})".replace("-", "{-}"),
                  font_size=18, color=AUDIT),
            label(rf"meetings: \ {100 * R['meetings']:+.1f} \\ (s.e. {100 * R['meetings_se']:.1f})".replace("-", "{-}"),
                  font_size=18, color=VOTER),
            label(r"planted: \ $-$8 and $-$1", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"The Island runs the same experiment on {TRUTH['roads']['n']} of its own road projects. <bookmark "
            f"mark='a'/> Where there is neither an audit nor a meeting, {100 * R['control']:.0f} percent of the "
            "money is missing. <bookmark mark='b'/> An audit, announced in advance, cuts that by "
            f"{100 * abs(R['audit']):.1f} points. <bookmark mark='c'/> Meetings move it by "
            f"{100 * abs(R['meetings']):.1f}, with a standard error of {100 * R['meetings_se']:.1f}: hardly at all. "
            "<bookmark mark='d'/> The planted truths were eight points and one, and the trial recovers them. "
            "Chapter seven comes back to what Olken found in Indonesia, and why the cure from below did so little."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), FadeIn(side[0]), *[FadeIn(b[1]) for b in bars],
                      run_time=1.0)
            for mk, b, sd in zip("abc", bars, (None, side[1], side[2])):
                vo.wait_until(mk)
                anims = [GrowFromEdge(b[0], DOWN if mk == "a" else UP), FadeIn(b[2])]
                if sd is not None:
                    anims.append(FadeIn(sd))
                self.play(*anims)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why do small groups win policies that cost everyone else more?", font_size=26, color=FEW),
            label(r"what do voters control, \ and what do lobbies buy?", font_size=26, color=VOTER),
            label(r"how do you measure what is hidden, \ and what cuts it?", font_size=26, color=AUDIT),
            label(r"why do bad institutions last, \ and what makes a state able to act?", font_size=26, color=ELITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "So this part asks why governments so often choose policies that economists can show are wasteful. "
            "<bookmark mark='a'/> Why do small groups win policies that cost everyone else more than they gain? "
            "<bookmark mark='b'/> What do voters control, and what do lobbies buy? <bookmark mark='c'/> How can "
            "anyone measure what is hidden, like corruption, and what cuts it? <bookmark mark='d'/> And why do bad "
            "institutions last, and what makes a state able to act at all?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1900, 2025], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, DEM, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 47 \ $\cdot$ \ Political Economy", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part forty-seven: political economy."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IX \ $\cdot$ \ The Fields", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"collective action; \ a game of building or lobbying; \ rent seeking",
            r"voters and close elections, \ with real data; \ lobbies and capture; \ politicians as agents",
            r"audits; \ corruption measured four ways; \ why bad institutions last",
            r"state capacity and democracy; \ conflict; \ media; \ cycles timed to elections",
            r"two dials; \ the people who use this; \ the frontier",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> Why small groups organize and large ones do not, a game for you "
            "to play, and the waste of chasing rents. <bookmark mark='b'/> Voters, with the real record of close "
            "Senate elections; lobbies and the regulators they capture; and politicians as agents of voters. "
            "<bookmark mark='c'/> Audits, four ways of measuring corruption, and why bad institutions last. "
            "<bookmark mark='d'/> The capacity of states, democracy and growth, conflict, the media, and economic "
            "cycles timed to elections. <bookmark mark='e'/> Two dials, the people who use these ideas, and the "
            "frontier."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
