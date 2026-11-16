from __future__ import annotations

import numpy as np

from videos.music.music59.common import *  # noqa: F403


class Wireless(SoundScene):
    def construct(self):
        chapter(self, 8, r"Wireless and networks", r"How do forty radio microphones share a stage without hearing each other?")
        self.imd()
        self.plan()
        self.inears()
        self.network()

    # ------------------------------------------------------------------
    def imd(self):
        items = [
            (r"each wireless microphone transmits on its own carrier, \ a few hundred kHz wide, \ in the UHF band", WHITE),
            (r"any nonlinearity \ (a receiver's amplifier, \ two transmitters side by side) \ mixes carriers into new frequencies", WHITE),
            (r"the worst: \ third-order products \ $2f_1 - f_2$ \ and \ $f_1 + f_2 - f_3$, \ which land inside the band", WHITE),
            (r"one lands on another microphone's carrier, \ and that microphone hisses or drops out", WHITE),
            (r"so the frequencies are chosen so that no product falls near any carrier", TUNE),
        ]
        rows_scene(self, r"intermodulation", items,
                   "Large shows use dozens of radio microphones and in-ear transmitters. <bookmark mark='b'/> Many conventional systems use separate UHF carriers of a few hundred kilohertz bandwidth; other bands and digital architectures also exist. <bookmark mark='c'/> But any nonlinearity, a receiver's amplifier, two transmitters worn side by side, mixes carriers into new frequencies. <bookmark mark='d'/> The worst are the third-order products, two f one minus f two, and f one plus f two minus f three, which land inside the band. <bookmark mark='e'/> If one lands on another microphone's carrier, that microphone hisses or drops out. <bookmark mark='f'/> So the frequencies are chosen so that no product falls near any carrier: Part 50's intermodulation, now in radio.", marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        d = load("wireless")
        lo, hi = d["band"]
        ax = frame_axes(width=11.0, height=1.4, xlo=lo, xhi=hi, ylo=0, yhi=1, center=UP * 0.6)
        tv = VGroup(*[Rectangle(width=11.0 * (b - a) / (hi - lo), height=1.4, stroke_width=0, fill_color=GREY_D, fill_opacity=0.8).move_to(ax.to((a + b) / 2, 0.5)) for a, b in d["tv"]])
        tvl = label(r"occupied TV channels", font_size=14, color=GREY_A).next_to(tv[0], UP, buff=0.05)
        plan = VGroup(*[Line(ax.to(f_, 0), ax.to(f_, 1), color=TUNE, stroke_width=3) for f_ in d["plan"]])
        a2 = frame_axes(width=11.0, height=1.0, xlo=lo, xhi=hi, ylo=0, yhi=1, center=DOWN * 1.4)
        even = VGroup(*[Line(a2.to(f_, 0), a2.to(f_, 1), color=EAR, stroke_width=3) for f_ in d["even"]])
        xt = VGroup(*[label(f"{v:.0f} MHz", font_size=13, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.08) for v in (470, 490, 510, 530)])
        l1 = label(rf"Monochord's planner: \ {len(d['plan'])} carriers, \ no third-order product within 100 kHz of any \ ({d['n_products_plan']:,} products checked)", font_size=15, color=TUNE).next_to(ax, UP, buff=0.35)
        l2 = label(rf"24 carriers evenly every 500 kHz: \ {d['hits_even']} of them hit by a product", font_size=15, color=EAR).next_to(a2, UP, buff=0.1)
        head = label(r"a frequency plan", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is a plan for a band from four hundred and seventy to five hundred and forty-two megahertz, around three "
            "occupied television channels. <bookmark mark='a'/> Spacing carriers evenly is the worst thing to do: on an even "
            f"grid every product lands on another carrier, and all {say(d['hits_even'])} are hit. <bookmark mark='b'/> "
            f"Monochord's planner walks up the band and accepts a frequency only if, with those already chosen, no third-order "
            f"product falls within a hundred kilohertz of any carrier: {say(len(d['plan']))} carriers fit, irregularly "
            "spaced, with every product falling in the gaps. Real planning software adds fifth-order products, receiver limits "
            "and a scan of the local spectrum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(tv), FadeIn(tvl), FadeIn(a2))
            vo.wait_until("a")
            self.play(FadeIn(even), FadeIn(l2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in plan], lag_ratio=0.08), FadeIn(l1), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inears(self):
        items = [
            (r"wedges on the floor point loudspeakers at microphones: \ Chapter 1's loop, \ on every stage", WHITE),
            (r"in-ear monitors: \ a custom mix in sealed earpieces, \ by radio, \ and no loop at all", WHITE),
            (r"a quieter stage, \ cleaner microphones, \ and the same mix wherever the singer walks", WHITE),
            (r"the cost: \ isolation from the room and the crowd, \ so ambient microphones are mixed back in", WHITE),
            (r"and a limiter on every pack: \ a sealed earpiece can deliver a dangerous level, \ Chapter 10's subject", TUNE),
        ]
        rows_scene(self, r"in-ear monitors", items,
                   "Radio also changed what musicians hear. <bookmark mark='b'/> Wedges on the floor point loudspeakers at "
                   "microphones: Chapter 1's loop, on every stage. <bookmark mark='c'/> In-ear monitors send each musician a "
                   "custom mix by radio to sealed earpieces, and direct monitor-speaker coupling is greatly reduced. <bookmark mark='d'/> The stage is quieter, "
                   "the microphones cleaner, and the mix the same wherever the singer walks. <bookmark mark='e'/> The cost is "
                   "isolation from the room and the crowd, so engineers mix ambient microphones back in. <bookmark mark='f'/> And "
                   "suitable monitor systems should use configured limiting and controlled levels; features vary, because a sealed earpiece can deliver a dangerous level, the subject of Chapter 10.", marks="bcdef")

    # ------------------------------------------------------------------
    def network(self):
        items = [
            (r"audio now travels on networks: \ Dante \ (2006), \ AES67 \ (2013): \ hundreds of channels on one Ethernet cable", WHITE),
            (r"every device must sample at the same instant: \ a shared clock, \ by the Precision Time Protocol \ (IEEE 1588)", WHITE),
            (r"latency budget: \ about 1 ms of network, \ a few ms of converters and processing: \ under 10 ms from microphone to loudspeaker", WHITE),
            (r"a musician hears a delay of 10 ms as standing 3.4 m further away: \ tolerable on stage, \ not in in-ear monitors", WHITE),
            (r"redundancy: \ two networks, \ every packet sent twice", TUNE),
        ]
        rows_scene(self, r"networks and clocks", items,
                   "And the cables have become a network. <bookmark mark='b'/> Dante from 2006, and the open standard AES67 from 2013, carry hundreds of channels on one Ethernet cable. <bookmark mark='c'/> Every device must sample at the same instant, so they share a clock by the Precision Time Protocol, IEEE 1588, good to well under a microsecond. <bookmark mark='d'/> The latency budget: about a millisecond of network, a few of converters and processing, under ten from microphone to loudspeaker. <bookmark mark='e'/> A musician hears ten milliseconds as standing three and a half metres further away: tolerable on a stage, not in in-ear monitors, where it combs against the sound of their own skull. <bookmark mark='f'/> Some professional systems support dual-network redundancy; it is a configured capability, not inherent in every network.", marks="bcdef")
