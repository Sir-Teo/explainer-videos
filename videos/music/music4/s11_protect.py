from __future__ import annotations

import numpy as np

from videos.music.music4.common import *  # noqa: F403


def hours_text(h: float) -> str:
    if h >= 1:
        return rf"{h:g} h"
    if h * 60 >= 1:
        return rf"{h * 60:.0f} min"
    return rf"{h * 3600:.0f} s"


class Protect(SoundScene):
    def construct(self):
        chapter(self, 10, r"The only pair you get", r"How much sound is too much?", lit=(1863,), extra=((1998, r"NIOSH's recommended noise limit"),))
        self.cells()
        self.dose()
        self.advice()

    # ------------------------------------------------------------------
    def cells(self):
        w = load("wave")
        co = Cochlea(width=10.4, names=True, ticks=()).move_to(UP * 2.1)
        co.remove(co.axis, co.unit)
        xs = np.linspace(0.3, 34.7, 120)
        inner = VGroup(*[Dot(co.p(mm) + DOWN * 0.5, radius=0.036, color=EAR) for mm in xs])
        hit = [k for k, mm in enumerate(xs) if 7.5 < mm < 12.5]
        g = faxes(125, 8000, [-70, 5], x_length=6.0, y_length=2.6, ylabel=r"threshold shift (dB HL)", yticks=[-60, -40, -20, 0],
                  fticks=(250, 500, 1000, 2000, 4000, 8000), font_size=18, yfmt=lambda v: f"{-v:g}")
        g.move_to(RIGHT * 3.3 + DOWN * 1.6)
        fs = np.array([125, 250, 500, 1000, 2000, 3000, 4000, 6000, 8000])
        loss = -np.array([5, 5, 5, 8, 12, 30, 45, 30, 18.0])
        ag = fcurve(g, fs, loss, BAD)
        ad = VGroup(*[Dot(g.at(f, v), radius=0.06, color=BAD) for f, v in zip(fs, loss)])
        tag = label(r"schematic: \ the notch that noise leaves", font_size=18, color=GREY_C).next_to(g, DOWN, buff=0.7)
        facts = VGroup(label(rf"{w['inner']:,} inner hair cells in each ear".replace(",", "{,}"), font_size=30, color=EAR),
                       label(r"in birds and fish, \ lost hair cells grow back", font_size=26, color=GREY_A),
                       label(r"in mammals, \ they do not", font_size=30, color=BAD),
                       label(r"noise injury often leaves \\ a 3--6 kHz notch", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(LEFT * 3.8 + DOWN * 1.5)
        with self.voiceover(
            "This chapter has no sound in it, and that is the point. <bookmark mark='a'/> Everything you have "
            f"heard in this series reached you through about {say(w['inner'])} inner hair cells in each ear. A "
            "phone camera has millions of sensors. You have a few thousand, and they have to last a lifetime. "
            "<bookmark mark='b'/> In birds and in fish, a hair cell that dies is replaced. <bookmark mark='c'/> In "
            "mammals it is not. You were born with all the hair cells you will ever have. <bookmark mark='d'/> And "
            "noise can injure hair cells and their nerve connections; outer hair cells are particularly vulnerable. "
            "A common audiogram pattern is a notch between three and six kilohertz, often deepest near four. "
            "Ear-canal resonance and cochlear mechanics contribute, but not every exposed ear has this pattern, "
            "and a notch alone is not a diagnosis. <bookmark mark='e'/> Here is a schematic example: thresholds "
            "are raised near four kilohertz, with partial recovery at higher frequencies."
        ) as vo:
            quiet = VGroup(speaker_icon(0.7, GREY_B), label(r"this chapter is silent", font_size=40, color=GREY_A)).arrange(RIGHT, buff=0.4)
            cross = Line(quiet[0].get_corner(DL) + DL * 0.1, quiet[0].get_corner(UR) + UR * 0.1, color=BAD, stroke_width=6)
            self.play(FadeIn(quiet), Create(cross), run_time=0.8)
            vo.wait_until("a")
            self.play(FadeOut(quiet), FadeOut(cross), run_time=0.4)
            self.play(FadeIn(co), LaggedStart(*[FadeIn(p) for p in inner], lag_ratio=0.01), FadeIn(facts[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[inner[k].animate.set_color(GREY_E) for k in hit], lag_ratio=0.1), FadeIn(facts[3]), run_time=3.0)
            vo.wait_until("e")
            self.play(FadeIn(g), Create(ag), FadeIn(ad), FadeIn(tag), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dose(self):
        d = load("dose")
        rows = d["rows"]
        head = label(r"NIOSH recommended daily exposure criterion (1998)", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        base_y, x0 = -1.2, -5.6
        bars, tags = VGroup(), VGroup()
        for k, r in enumerate(rows):
            h = 4.0 * r["hours"] / 8.0  # linear duration scale: each 3 dB halves the height
            b = Rectangle(width=0.8, height=h, stroke_width=0, fill_color=interpolate_color(ManimColor(GOOD), ManimColor(BAD), k / (len(rows) - 1)), fill_opacity=0.85)
            b.move_to(RIGHT * (x0 + 1.25 * k) + UP * (base_y + h / 2))
            bars.add(b)
            tags.add(VGroup(label(rf"{r['dba']} dBA", font_size=22, color=GREY_A).next_to(b, DOWN, buff=0.12),
                            label(hours_text(r["hours"]), font_size=26).next_to(b, UP, buff=0.1)))
        rule = VGroup(label(r"85 dBA for 8 hours a day", font_size=28, color=GOOD),
                      label(r"every 3 dB more: \ half the time", font_size=28, color=BAD),
                      label(r"(3 dB is twice the power)", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(RIGHT * 4.6 + UP * 1.3)
        ask = pause_card(r"A club, \ or the front of a rock concert: \ 100 dBA. \\ What duration reaches the NIOSH daily criterion?", width=7.6).move_to(DOWN * 2.75)
        ans = VGroup(MathTex(r"100 - 85 = 15\ \text{dB} = 5 \text{ halvings}", font_size=32),
                     MathTex(r"\tfrac{8\ \text{h}}{2^5} = 15\ \text{minutes}", font_size=36, color=BAD)).arrange(RIGHT, buff=0.9).move_to(DOWN * 2.75)
        with self.voiceover(
            "How much is too much? NIOSH's 1998 occupational recommendation uses a simple energy-based criterion. It reduces risk; it is not a guarantee against damage or the same as the US legal OSHA limit. <bookmark mark='a'/> Eighty-five decibels, A-weighted, is the criterion for eight hours a day. That is about the level of heavy traffic. <bookmark mark='b'/> For every three "
            "decibels above that, the time is halved. Three decibels is twice the power, so the rule says that "
            "what matters is the total energy delivered to the ear. <bookmark mark='c'/> Eighty-eight decibels "
            "for four hours. Ninety-one for two. Ninety-four for one. <bookmark mark='d'/> Now you do one. A "
            "club, or the front of a rock concert, runs at about a hundred decibels. What duration reaches the NIOSH daily criterion?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(tags[0]), FadeIn(rule[0]))
            vo.wait_until("b")
            self.play(FadeIn(rule[1]), FadeIn(rule[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(t)) for b, t in zip(bars[1:4], tags[1:4])], lag_ratio=0.6), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "A hundred is fifteen decibels above eighty-five. Fifteen is five lots of three, so the time is "
            "halved five times: eight hours divided by thirty-two. <bookmark mark='a'/> Fifteen minutes. Not a "
            "whole evening: fifteen minutes. <bookmark mark='b'/> And it keeps going. At a hundred and six "
            f"decibels, under four minutes. At a hundred and twelve, less than one. <bookmark mark='c'/> Now run "
            "it backwards. A pair of earplugs that takes twenty decibels off turns a hundred into eighty. Every "
            f"three decibels doubles the time, so twenty decibels multiplies it by about {say(round(d['plug_factor'], -1))}. "
            "That calculation assumes the plugs actually provide twenty decibels of attenuation in your ears. Fit and frequency matter; a package rating does not establish a safe duration."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(ans[0]))
            vo.wait_until("a")
            self.play(FadeIn(ans[1]), GrowFromEdge(bars[4], DOWN), FadeIn(tags[4]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(t)) for b, t in zip(bars[5:], tags[5:])], lag_ratio=0.6), run_time=2.5)
            vo.wait_until("c")
            plug = label(rf"actual fitted reduction $20$ dB: \\ equal-dose time $\times\,{round(d['plug_factor'], -1):.0f}$", font_size=30, color=GOOD).move_to(RIGHT * 4.6 + DOWN * 0.5)
            self.play(FadeIn(plug))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def advice(self):
        rows = VGroup(
            VGroup(label(r"distance", font_size=32, color=TUNE), wrapped_label(r"ideal point source in the open: \ distance doubled, 6 dB less: \ four times the equal-dose duration \quad (Part 2)", 9.8, 25, GREY_A)),
            VGroup(label(r"plugs", font_size=32, color=TUNE), wrapped_label(r"musicians' earplugs lower every frequency about equally, \ so music still sounds like music", 9.8, 25, GREY_A)),
            VGroup(label(r"time", font_size=32, color=TUNE), wrapped_label(r"the dose adds up over the day: \ take breaks, \ and count the journey home on headphones", 9.8, 25, GREY_A)),
            VGroup(label(r"the warning", font_size=32, color=BAD), wrapped_label(r"ringing, \ or dull hearing, \ after a concert means the dose was too large", 9.8, 25, GREY_A)),
        )
        for k, r in enumerate(rows):
            r[0].move_to(LEFT * 6.3, aligned_edge=LEFT)
            r[1].move_to(LEFT * 3.9, aligned_edge=LEFT)
            r.shift(UP * (1.0 - 1.0 * k))
        opening = VGroup(label(r"in the middle of an orchestra: \\ often above 85 dBA, \ for hours", font_size=28, color=GREY_A),
                         label(r"a violinist's left ear: \\ a hand's width from the instrument", font_size=28, color=GREY_A)).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.5)
        who = label(r"World Health Organization: \ more than a billion young people are at risk from unsafe listening", font_size=26, color=EAR).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Musicians are not exempt; they are the most exposed. Players in the middle of an orchestra are "
            "often above eighty-five decibels for hours, and a violinist's left ear sits a hand's width from "
            "the instrument. So, four habits. <bookmark mark='a'/> Distance: for an isolated point source in the open, twice as far is about six decibels less. Rooms and loudspeaker arrays can differ; in that approximation, the equal-dose duration increases fourfold. <bookmark mark='b'/> Plugs: "
            "the ones made for musicians lower every frequency by about the same amount, so the music still "
            "sounds like music, only quieter. <bookmark mark='c'/> Time: the dose adds up over the whole day, and "
            "the headphones on the journey home count too. <bookmark mark='d'/> And one warning sign. If your ears "
            "ring after a concert, or the world sounds dull, the dose was too large. The ringing usually fades. "
            "In the last chapter you will see why that is not the same as no harm done. <bookmark mark='e'/> The "
            "World Health Organization estimates that more than a billion young people are at risk of hearing "
            "loss from the way they listen. Everything else in this series depends on your not being one of them."
        ) as vo:
            self.play(FadeIn(opening[0]))
            self.wait(3.5)
            self.play(FadeIn(opening[1]))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
            vo.wait_until("e")
            self.play(FadeIn(who))
        self.wait(0.4)
        self.clear_scene()
