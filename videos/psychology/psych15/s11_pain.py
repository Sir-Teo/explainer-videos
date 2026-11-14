from __future__ import annotations

import numpy as np

from videos.psychology.psych15.common import *  # noqa: F403


class Pain(VoiceoverScene):
    def construct(self):
        self.card()
        self.bellrope()
        self.gatecircuit()
        self.gatecurve()
        self.phantom()

    def card(self):
        card = chapter_card(10, r"Pain", r"Why does pain not follow the injury?",
                            lit={1664: r"Descartes", 1965: r"Melzack \& Wall"}, part=PART, scale=("circuit", "mind"),
                            marr=("what", "how"))
        with self.voiceover("Chapter ten. Pain."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def bellrope(self):
        head = heading(r"A bell rope, \ or a decision?")
        rows = rows_of([
            (r"Descartes, \ 1664: \ fire tugs a thread in the foot, \ which rings a bell in the brain", WHITE),
            (r"pain as a line from injury to sensation: \ more damage, \ more pain", PAIN),
            (r"but soldiers with grave wounds have often asked for less relief than civilians after surgery", BAD),
            (r"and amputees feel pain in hands that are gone", BAD),
            (r"2020 definition: \ an unpleasant sensory and emotional experience associated with, \ or resembling, \ tissue damage", PRIOR),
        ], 12.6, 28, 0.4).move_to([0, -0.1, 0])
        with self.voiceover(
            "The oldest theory of pain is a bell rope. <bookmark mark='a'/> In a book published in 1664, René "
            "Descartes drew a foot near a fire: the heat tugs a thread running up to the brain, which rings like a "
            "bell. <bookmark mark='b'/> Pain, on this view, is a line from injury to sensation: more damage, more "
            "pain. <bookmark mark='c'/> It doesn't fit. Henry Beecher, an anaesthetist in the Second World War, noticed "
            "that soldiers with grave wounds often asked for less pain relief than civilians with lesser surgical "
            "wounds. <bookmark mark='d'/> And most amputees feel pain, sometimes for years, in a hand or foot that "
            "isn't there. <bookmark mark='e'/> So the International Association for the Study of Pain now defines it "
            "as an experience, sensory and emotional, associated with, or resembling, tissue damage: not a reading of "
            "the damage itself."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def gatecircuit(self):
        head = heading(r"Melzack and Wall's gate, \ 1965")
        L = Arrow([-6.0, 1.4, 0], [-1.2, 1.4, 0], buff=0, color=TOUCH, stroke_width=5)
        S = Arrow([-6.0, -1.0, 0], [-1.2, -1.0, 0], buff=0, color=PAIN, stroke_width=5)
        ll = label(r"large fibres: \ touch, \ rubbing", font_size=22, color=TOUCH).next_to(L, UP, buff=0.1)
        sl = label(r"small fibres: \ injury", font_size=22, color=PAIN).next_to(S, DOWN, buff=0.1)
        sg = Circle(radius=0.4, color=PRIOR, fill_opacity=0.25).move_to([-2.6, 0.2, 0])
        sgl = label(r"SG", font_size=24, color=PRIOR).move_to(sg)
        T = Circle(radius=0.5, color=WHITE, fill_opacity=0.15).move_to([0.2, 0.2, 0])
        Tl = label(r"T", font_size=30).move_to(T)
        out = Arrow(T.get_right(), [2.2, 0.2, 0], buff=0, color=PAIN, stroke_width=5)
        ol = label(r"to the brain", font_size=22, color=PAIN).next_to(out, UP, buff=0.1)
        e1 = Arrow([-1.2, 1.4, 0], T.get_top() + LEFT * 0.2, buff=0.05, color=TOUCH, stroke_width=3)
        e2 = Arrow([-1.2, -1.0, 0], T.get_bottom() + LEFT * 0.2, buff=0.05, color=PAIN, stroke_width=3)
        e3 = Arrow([-3.4, 1.4, 0], sg.get_top(), buff=0.05, color=TOUCH, stroke_width=3)
        e4 = DashedLine([-3.4, -1.0, 0], sg.get_bottom(), color=PAIN, stroke_width=3)
        e5 = DashedLine(sg.get_right(), T.get_left(), color=PRIOR, stroke_width=4)
        fig = VGroup(L, S, ll, sl, sg, sgl, T, Tl, out, ol, e1, e2, e3, e4, e5).shift(LEFT * 0.4 + UP * 0.3)
        eq = MathTex(r"T = \frac{w_L L + w_S S}{1 + g\,\mathrm{SG}}, \qquad \mathrm{SG} = \max(L - kS,\ 0)",
                     font_size=34).move_to([3.4, 2.0, 0])
        keep_in_frame(eq)
        rows = rows_of([
            (r"T cells in the spinal cord's dorsal horn pass the signal up", WHITE),
            (r"large fibres also drive an inhibitory interneuron \ (SG) \ that closes the gate", TOUCH),
            (r"small fibres inhibit that interneuron, \ opening the gate", PAIN),
            (r"and the brain sends signals down that open and close it too", PRIOR),
        ], 12.4, 26, 0.24).to_edge(DOWN, buff=0.75)
        tag = historical_tag(rf"{archive.MELZACK_WALL_1965.cite}; \ drawn as Psyche's circuit")
        with self.voiceover(
            "In 1965 Ronald Melzack and Patrick Wall proposed a circuit in the spinal cord. "
            "<bookmark mark='a'/> Cells in the dorsal horn, which they called T cells, pass the signal up to the "
            "brain, driven by both kinds of fibre. <bookmark mark='b'/> But the large touch fibres also drive an "
            "inhibitory interneuron, here labelled SG for the substantia gelatinosa, which damps T's inputs: it closes "
            "the gate. <bookmark mark='c'/> The small fibres that signal injury inhibit that interneuron, holding the "
            "gate open. <bookmark mark='d'/> And fibres coming down from the brain can open and close it too, which is "
            "where attention, fear and expectation get their grip on pain. Psyche's version is this equation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(fig[:4]), FadeIn(T), FadeIn(Tl), GrowArrow(out), FadeIn(ol))
            vo.wait_until("a")
            self.play(GrowArrow(e1), GrowArrow(e2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(sg), FadeIn(sgl), GrowArrow(e3), Create(e5), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(e4), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Write(eq))
        self.clear_scene()

    def gatecurve(self):
        d = load("gate")
        head = heading(r"Why rubbing helps")
        A = axes([0, 2], [0, 2], x_length=6.8, y_length=4.2, xticks=[0, 0.5, 1, 1.5, 2], yticks=[0, 0.5, 1, 1.5, 2],
                 xlabel=r"injury signal in the small fibres", ylabel=r"output of T", center=[-2.6, -0.3, 0])
        ax = A.ax
        c0 = curve(ax, d["small"], d["T_none"], PAIN, stroke_width=4)
        c2 = curve(ax, d["small"], d["T_rub"], TOUCH, stroke_width=4)
        leg = legend([(PAIN, r"no touch"), (TOUCH, r"rubbing")], font_size=22)
        leg.move_to(ax.c2p(0.45, 1.6))
        rows = rows_of([
            (rf"the same injury, \ 1 unit: \ T at {d['at1_none']:.2f} alone, \ {d['at1_rub']:.2f} while rubbing", TOUCH),
            (r"you rub a knocked elbow because it works", WHITE),
            (r"the basis of TENS: \ electrical stimulation of the large fibres through the skin", GREY_A),
            (r"the details of the 1965 circuit were wrong; \ the idea of a gate, \ and of control from above, \ survived", PRIOR),
        ], 4.8, 26, 0.32).move_to([4.4, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ \texttt{hearing.gate}")
        with self.voiceover(
            "Run the circuit. <bookmark mark='a'/> The horizontal axis is the injury signal in the small fibres, and "
            "the curves are the output of T, with no touch and with vigorous rubbing. For the same injury, rubbing "
            "cuts T's output by more than half, and the more the injury signal grows, the more it takes to close the "
            "gate. <bookmark mark='b'/> You rub a knocked elbow because it "
            "works. <bookmark mark='c'/> It's also the basis of TENS machines, which stimulate the large fibres "
            "electrically through the skin. <bookmark mark='d'/> Much of the 1965 wiring diagram turned out to be "
            "wrong in detail. What survived is the idea itself: that pain signals are gated in the spinal cord, and "
            "that the brain controls the gate from above. That changed pain from a bell rope into a decision."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c0), Create(c2), FadeIn(leg), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def phantom(self):
        head = heading(r"Pain without a body part, \ and relief without a drug")
        rows = rows_of([
            (r"phantom limbs: \ most amputees feel the missing limb, \ and many feel pain in it", PAIN),
            (r"the body map in the cortex is still there, \ and still active: \ Part 7's homunculus", PRIOR),
            (r"1996: \ Ramachandran's mirror box: \ seeing the intact hand in the mirror can ease the phantom", VISION),
            (r"1978: \ Levine, \ Gordon and Fields: \ naloxone, \ which blocks opioids, \ undoes placebo relief", TIMING),
            (r"the brain makes its own painkillers on expectation: \ placebo returns in Part 57", GREY_A),
        ], 12.6, 27, 0.4).move_to([0, -0.1, 0])
        tag = published_tag(archive.LEVINE_1978.cite)
        with self.voiceover(
            "Two more facts that a bell rope can't explain. <bookmark mark='a'/> Most people who lose a limb continue "
            "to feel it, and many feel pain in it. <bookmark mark='b'/> The limb's map in the cortex, Part 7's "
            "homunculus, is still there and still active, and with nothing coming in it can be driven by its "
            "neighbours. <bookmark mark='c'/> In 1996 Vilayanur Ramachandran had amputees put their intact hand in a "
            "box with a mirror, so that it seemed to occupy the missing hand's place. Seeing the phantom move eased "
            "the pain for some of them, though the evidence from controlled trials is still modest. "
            "<bookmark mark='d'/> And in 1978, Jon Levine, Newton Gordon and Howard Fields gave patients, after wisdom "
            "teeth were removed, either naloxone, a drug that blocks opioids, or an inert placebo. Naloxone made the "
            "pain worse, but only in the people whose pain a placebo had relieved. <bookmark mark='e'/> Expecting "
            "relief had made their brains release their own opioids. Placebo returns in Part 57, on health and care."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
