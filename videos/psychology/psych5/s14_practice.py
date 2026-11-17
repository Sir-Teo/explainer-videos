from __future__ import annotations

import numpy as np

from videos.psychology.psych5.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.devices()
        self.limits()

    def card(self):
        card = chapter_card(13, r"In practice: \ talking to nerves", r"What can be built once the signal is "
                            r"understood?", lit=(), part=PART, scale=("neuron", "person"), marr=("tissue",))
        with self.voiceover(
            "Chapter thirteen. In practice: talking to nerves."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def devices(self):
        head = heading(r"Four technologies, one chapter each")
        items = [
            (r"cochlear implant", r"A row of electrodes in the inner ear fires the hearing nerve directly, with "
             r"brief current pulses.", r"chapter 6: \ pulses above threshold, spaced by the dead time", THRESH),
            (r"local anaesthetic", r"Lidocaine blocks the sodium channel. \ No sodium loop, no signal, no pain "
             r"reaching the brain.", r"chapter 5: \ set $\bar g_{Na}$ to zero", NA),
            (r"deep-brain stimulator", r"A pacemaker for a brain circuit: \ steady trains of pulses that change "
             r"how the cells nearby fire.", r"chapters 6 and 8: \ rates and rhythms", MODEL),
            (r"neuromorphic chip", r"Silicon circuits that integrate and fire, so that a chip computes with "
             r"spikes and stays idle between them.", r"chapter 9: \ the least a neuron can be", GATE["n"]),
        ]
        cards = VGroup()
        for name, what, link, color in items:
            box = panel(6.4, 2.7, color=color)
            body = VGroup(label(name, font_size=34, color=color), wrapped_label(what, 5.8, 27, WHITE),
                          label(link, font_size=23, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            body.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.3)
            cards.add(VGroup(box, body))
        cards.arrange_in_grid(2, 2, buff=0.3).move_to([0, -0.35, 0])
        with self.voiceover(
            "Understanding the nerve signal was not an academic matter. Each idea in this part became a "
            "technology. <bookmark mark='a'/> If the hair cells of the inner ear are lost, the hearing nerve "
            "is still there, waiting for input. A cochlear implant gives it input directly: a row of "
            "electrodes delivering brief pulses of current, strong enough to cross threshold, timed so that "
            "the fibres can follow. Hundreds of thousands of people hear through them. "
            "<bookmark mark='b'/> A local anaesthetic, like the lidocaine a dentist uses, is a molecule that "
            "plugs the sodium channel. In the model, that's setting the sodium conductance to zero. The "
            "signal can't start, so nothing reaches the brain from that tooth. <bookmark mark='c'/> A "
            "deep-brain stimulator is a pacemaker for a circuit inside the brain, used above all in "
            "Parkinson's disease. It delivers steady trains of pulses that change the firing of the cells "
            "around the electrode. <bookmark mark='d'/> And engineers build chips out of integrate-and-fire "
            "units, which compute with spikes and draw almost no power between them. None of these would "
            "have been designed by trial and error. They were designed from the equations."
        ) as vo:
            self.play(FadeIn(head))
            for mark, c_ in zip("abcd", cards):
                vo.wait_until(mark)
                self.play(FadeIn(c_, shift=UP * 0.15))
        self.clear_scene()

    def limits(self):
        hh = load("spike")
        head = heading(r"What the model tells an engineer, and what it does not")
        left = VGroup(
            label(r"it tells you", font_size=34, color=MODEL),
            wrapped_label(rf"how strong a pulse must be: \ a threshold, here {hh['threshold']:.0f} $\mu$A/cm$^2$ "
                          r"for half a millisecond", 5.8, 27, WHITE),
            wrapped_label(rf"how fast you may pulse: \ nothing gets through for {hh['absolute']:.0f} ms after a "
                          r"signal", 5.8, 27, WHITE),
            wrapped_label(r"which fibres respond first: \ the thick ones", 5.8, 27, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        right = VGroup(
            label(r"it does not tell you", font_size=34, color=BAD),
            wrapped_label(r"what the pattern of signals means to the brain that receives it", 5.8, 27, WHITE),
            wrapped_label(r"how a person learns to hear through sixteen electrodes", 5.8, 27, WHITE),
            wrapped_label(r"why stimulating one small nucleus eases a tremor", 5.8, 27, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        cols = VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.35, 0])
        end = wrapped_label(r"The neuron is the right level for the first list. \ The second needs circuits, "
                            r"learning and a person, which is the rest of the series.", 12.2, 28, P.ACCENT)
        end.to_edge(DOWN, buff=0.6)
        tag = note(r"numbers: Psyche's squid membrane at $6.3^\circ$C, for illustration").to_corner(DR, buff=0.2)
        with self.voiceover(
            "It's worth being precise about what the model gives the engineer. <bookmark mark='a'/> It says "
            "how strong a pulse must be, and how the threshold trades against the pulse's length. It says "
            "how fast you can pulse before the dead time swallows every second one. And the cable equation "
            "says which fibres respond first to a current from outside: the thick ones, which is why "
            "stimulation tends to recruit the wrong fibres before the right ones. <bookmark mark='b'/> What "
            "it doesn't say is what any of it means. A cochlear implant delivers a crude pattern through a "
            "dozen or two electrodes, to a nerve built for thousands of channels, and people still come to "
            "understand speech with it, usually over months. That learning isn't in the membrane. Why "
            "stimulating one small region relieves a tremor is still argued about. <bookmark mark='c'/> So "
            "the neuron is the right level of description for some questions and the wrong one for others. "
            "Knowing which level a question lives at is half of this subject, and it's why every chapter "
            "card in this series carries that row of levels."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in left], lag_ratio=0.6), run_time=8.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in right], lag_ratio=0.6), run_time=8.0)
            vo.wait_until("c")
            self.play(FadeIn(end, shift=UP * 0.15))
        self.clear_scene()
