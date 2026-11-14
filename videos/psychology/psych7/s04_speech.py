from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403

BROCA_AT, WERNICKE_AT = (-0.36, -0.02), (0.22, 0.06)


class Speech(VoiceoverScene):
    def construct(self):
        self.card()
        self.tan()
        self.second()
        self.diagram()
        self.refined()

    def card(self):
        card = chapter_card(3, r"Two aphasias and a diagram", r"What can one patient and one brain show?",
                            lit={1861: r"Broca's patient", 1874: r"Wernicke's diagram"}, part=PART,
                            scale=("brain", "mind"), marr=("how", "tissue"))
        with self.voiceover(
            "Chapter three. Two aphasias and a diagram."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def tan(self):
        head = heading(r"Paris, 1861: \ a man who could say one syllable")
        brain = brain_side(5.6, fill=0.25).move_to([-3.7, 0.0, 0])
        mark = lesion_mark(at(brain, *BROCA_AT), 0.42)
        mark_l = label(r"the damage Broca found", font_size=24, color=LESION).next_to(mark, DOWN, buff=0.9)
        arrow = Arrow(mark_l.get_top(), mark.get_bottom(), color=LESION, stroke_width=3, buff=0.05)
        bubble = VGroup(RoundedRectangle(width=2.4, height=0.9, corner_radius=0.3, color=VOLT, stroke_width=3),
                        label(r"``tan, tan''", font_size=32, color=VOLT))
        bubble[1].move_to(bubble[0])
        bubble.next_to(brain, UP, buff=0.15).shift(LEFT * 1.4)
        rows = VGroup(
            wrapped_label(r"Leborgne: \ in hospital for twenty years, \ called Tan after the one thing he said",
                          5.6, 28, WHITE),
            wrapped_label(r"he understood what was said to him, \ and answered with gestures", 5.6, 28, SPARED),
            wrapped_label(r"after his death: \ a lesion low in the left frontal lobe", 5.6, 28, LESION),
            wrapped_label(r"more patients followed, \ and in every one the damage was on the left", 5.6, 28,
                          P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.5, -0.2, 0])
        src = historical_tag(archive.BROCA_1861.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "In April 1861 a patient called Leborgne was moved to the surgical ward of the Bicêtre hospital, "
            "near Paris. He'd been in the hospital for twenty years. <bookmark mark='a'/> Everyone called "
            "him Tan, because that was the one syllable he could say. <bookmark mark='b'/> And yet he "
            "understood what was said to him. He answered questions with gestures, and got angry when he "
            "wasn't understood. A few days later he died, and the surgeon, Paul Broca, examined his brain. "
            "<bookmark mark='c'/> There was a lesion low in the left frontal lobe. Broca showed the brain to "
            "the Anthropological Society the next day. Here was a faculty, speech, lost by itself, and a "
            "place. <bookmark mark='d'/> Over the next few years he collected more patients who had lost "
            "their speech, and in every one the damage was on the left side. We speak, he said, with the "
            "left hemisphere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(brain))
            vo.wait_until("a")
            self.play(FadeIn(bubble, scale=0.8), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(mark, scale=0.4), FadeIn(mark_l), GrowArrow(arrow), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def second(self):
        head = heading(r"1874: \ the opposite patient")
        brain = brain_side(5.6, fill=0.25).move_to([-3.7, 0.3, 0])
        m1 = lesion_mark(at(brain, *BROCA_AT), 0.42)
        m2 = lesion_mark(at(brain, *WERNICKE_AT), 0.42).set_color(DATA)
        l1 = label(r"Broca", font_size=24, color=LESION).next_to(m1, UP, buff=0.75)
        l2 = label(r"Wernicke", font_size=24, color=DATA).next_to(m2, UP, buff=0.95)
        table = VGroup()
        heads = [r"", r"speaks", r"understands"]
        data = [(r"damage at the front", LESION, (False, True)), (r"damage further back", DATA, (True, False))]
        colx = [2.0, 4.3, 5.9]
        for j, h in enumerate(heads):
            table.add(label(h, font_size=26, color=GREY_A).move_to([colx[j], 1.3, 0]))
        for i, (name, col, cells) in enumerate(data):
            y = 0.5 - 0.9 * i
            table.add(label(name, font_size=27, color=col).move_to([colx[0], y, 0]))
            for j, ok in enumerate(cells):
                table.add(label(r"yes" if ok else r"no", font_size=34, color=SPARED if ok else LESION).move_to(
                    [colx[j + 1], y, 0]))
        keep_in_frame(table)
        end = wrapped_label(r"Each patient can do what the other cannot. \ Hold that pattern: \ the next chapter "
                            r"is about what it proves.", 12.6, 29, P.ACCENT).to_edge(DOWN, buff=0.55)
        src = historical_tag(archive.WERNICKE_1874.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Thirteen years later a German doctor of twenty-six, Carl Wernicke, described the opposite "
            "patient. <bookmark mark='a'/> These patients spoke fluently, in long sentences with a normal "
            "rhythm. But the words were wrong or invented, and they couldn't understand what was said to "
            "them. Their damage was further back, at the top of the temporal lobe, next to the part of the "
            "cortex that receives sound. <bookmark mark='b'/> Set the two side by side. With damage at the "
            "front, the patient understands and can't speak. With damage further back, the patient speaks "
            "and can't understand. <bookmark mark='c'/> Each can do what the other can't. That crossed "
            "pattern has a name, a double dissociation, and it's the strongest evidence a lesion can give. "
            "The next chapter is about why, and about how it can still fool you. But first, look at what "
            "Wernicke did with it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(brain), FadeIn(m1), FadeIn(l1))
            vo.wait_until("a")
            self.play(FadeIn(m2, scale=0.4), FadeIn(l2))
            vo.wait_until("b")
            self.play(FadeIn(table, lag_ratio=0.1), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def _diagram(self, origin, cut=None):
        """Wernicke and Lichtheim's diagram.  ``cut`` names a module to draw as destroyed."""
        o = np.asarray(origin, float)
        pos = {"hearing": (-2.6, -1.7), "word sounds": (-2.6, 0.0), "concepts": (0.0, 1.6),
               "word movements": (2.6, 0.0), "articulation": (2.6, -1.7)}
        text = {"hearing": r"hearing", "word sounds": r"sounds of words", "concepts": r"concepts",
                "word movements": r"movements of words", "articulation": r"mouth and tongue"}
        boxes = {}
        for name, (x, y) in pos.items():
            col = LESION if name == cut else (TEMPORAL if name in ("hearing", "word sounds") else
                                              FRONTAL if name in ("word movements", "articulation") else VOLT)
            boxes[name] = module_box(text[name], col, width=2.5, height=0.75, font_size=24).move_to(
                o + np.array([x, y, 0]))
        arrows = {
            "in": link(boxes["hearing"].get_top(), boxes["word sounds"].get_bottom()),
            "up": link(boxes["word sounds"].get_top(), boxes["concepts"].get_left() + DOWN * 0.1),
            "down": link(boxes["concepts"].get_right() + DOWN * 0.1, boxes["word movements"].get_top()),
            "out": link(boxes["word movements"].get_bottom(), boxes["articulation"].get_top()),
            "pathway": link(boxes["word sounds"].get_right(), boxes["word movements"].get_left(),
                            color=LESION if cut == "pathway" else THRESH, width=5),
        }
        g = VGroup(*boxes.values(), *arrows.values())
        g.boxes, g.arrows = boxes, arrows
        if cut == "pathway":
            mid = arrows["pathway"].get_center()
            g.add(VGroup(Line(mid + UL * 0.22, mid + DR * 0.22, color=LESION, stroke_width=6),
                         Line(mid + UR * 0.22, mid + DL * 0.22, color=LESION, stroke_width=6)))
        return g

    def diagram(self):
        a = load("aphasia")
        head = heading(r"The first diagram of a function: \ boxes, arrows, and a prediction")
        d = self._diagram([-3.4, -0.4, 0])
        tasks = a["tasks"]
        short = {"understand speech": r"understand", "speak": r"speak", "repeat": r"repeat"}
        colx = [1.3, 4.1, 5.3, 6.5]
        table = VGroup()
        for j, t in enumerate(tasks):
            table.add(label(short[t], font_size=23, color=GREY_A).move_to([colx[j + 1], 1.55, 0]))
        names = [r"cut the front box", r"cut the back box", r"cut the pathway"]
        cols = [FRONTAL, TEMPORAL, THRESH]
        rows = VGroup()
        for i in range(3):
            y = 0.8 - 0.85 * i
            row = VGroup(label(names[i], font_size=25, color=cols[i]).move_to([colx[0] + 0.9, y, 0]))
            for j in range(len(tasks)):
                ok = a["full"][i][j] > 0.5
                row.add(label(r"yes" if ok else r"no", font_size=30, color=SPARED if ok else LESION).move_to(
                    [colx[j + 1], y, 0]))
            rows.add(row)
        VGroup(table, rows).shift(RIGHT * 0.1)
        keep_in_frame(VGroup(table, rows))
        end = wrapped_label(r"The third row had never been seen. \ It was then found: \ conduction aphasia.", 6.2,
                            28, P.ACCENT).move_to([4.0, -2.3, 0])
        keep_in_frame(end)
        src = historical_tag(archive.WERNICKE_1874.cite)
        tag = psyche_tag(r"computed: Psyche, the diagram as a model")
        with self.voiceover(
            "Wernicke didn't stop at two places. He drew a diagram. <bookmark mark='a'/> Sound comes in, and "
            "reaches a store of the sounds of words, in the temporal lobe. From there it reaches the "
            "concepts, and you understand. To speak, a concept calls up the movements of a word, in the "
            "frontal lobe, and they drive the mouth and tongue. <bookmark mark='b'/> And there's one more "
            "arrow. A child learns to speak by imitating what it hears, so the sounds of words must be "
            "connected directly to their movements. <bookmark mark='c'/> Now treat the diagram as a model, "
            "and damage it. Destroy the front box: understanding survives, speech and repetition go. That's "
            "Broca's patient. Destroy the back box: speech survives, in a fashion, and understanding and "
            "repetition go. That's Wernicke's. <bookmark mark='d'/> Now cut only the pathway between them. "
            "The model says the patient will understand, and speak, and be unable to do one thing: repeat "
            "what they've just heard. <bookmark mark='e'/> No such patient had been described. Wernicke "
            "predicted one from the diagram. They were then found, and the syndrome is called conduction "
            "aphasia. A drawing of boxes and arrows had predicted a human being. This is the method "
            "cognitive psychology still uses, and it started here."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d.boxes[n]) for n in d.boxes], lag_ratio=0.3),
                      LaggedStart(*[GrowArrow(d.arrows[n]) for n in ("in", "up", "down", "out")], lag_ratio=0.5),
                      run_time=6.0)
            vo.wait_until("b")
            self.play(GrowArrow(d.arrows["pathway"]))
            vo.wait_until("c")
            self.play(FadeIn(table), FadeIn(rows[0]), Indicate(d.boxes["word movements"], color=LESION))
            self.play(FadeIn(rows[1]), Indicate(d.boxes["word sounds"], color=LESION))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), Indicate(d.arrows["pathway"], color=LESION, scale_factor=1.1))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def refined(self):
        head = heading(r"2007: \ Broca's own specimens, scanned")
        brain = brain_side(5.6, fill=0.25).move_to([-3.7, 0.0, 0])
        small = Circle(radius=0.36, color=THRESH, stroke_width=3).move_to(at(brain, *BROCA_AT))
        small_l = label(r"``Broca's area'' on the textbook's map", font_size=22, color=THRESH).next_to(
            brain, UP, buff=0.1).shift(LEFT * 0.6)
        big = lesion_mark(at(brain, -0.22, 0.05), 1.0)
        big.set_fill(opacity=0.45)
        rows = VGroup(
            wrapped_label(r"Broca kept the brains. \ They are still in a museum in Paris.", 5.6, 28, WHITE),
            wrapped_label(r"The scans: \ damage far beyond the surface, into deep tissue and a long fibre "
                          r"tract", 5.6, 28, LESION),
            wrapped_label(r"neither brain's damage covers the whole of the region now called Broca's area",
                          5.6, 28, WHITE),
            wrapped_label(r"The left frontal lobe matters for speech. \ The lasting syndrome needs more than "
                          r"the one area.", 5.6, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.5, -0.2, 0])
        src = published_tag(archive.DRONKERS_2007.cite)
        tag = note(r"schematic: the extent is not to scale").to_corner(DR, buff=0.2)
        with self.voiceover(
            "One postscript, because this is a series that checks. Broca didn't cut Leborgne's brain open. "
            "He kept it whole, and it has sat in a museum in Paris ever since. <bookmark mark='a'/> In 2007 "
            "Nina Dronkers and her colleagues put it, and the brain of Broca's second patient, into a "
            "scanner. <bookmark mark='b'/> In both, the damage ran far beyond what Broca could see on the "
            "surface. It went deep, into the tissue underneath, and through one of the long bundles of "
            "fibres that connect the front of the brain to the back. <bookmark mark='c'/> And in neither "
            "brain did the damage cover the whole of the region that textbooks now label Broca's area. "
            "<bookmark mark='d'/> So the finding stands, and it's been refined. The left frontal lobe matters "
            "for speech. But the lasting loss of speech takes more damage than the one patch on the diagram, "
            "and the tidy picture of one area for one faculty was always tidier than the brains it came "
            "from. Even Wernicke said his boxes were an aid to reasoning, not a piece of anatomy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(brain), Create(small), FadeIn(small_l))
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(big, scale=0.4), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(small, color=WHITE, scale_factor=1.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()
