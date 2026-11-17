from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


def box(text, color, w=2.5, h=1.25, font_size=26):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=color, stroke_width=3,
                         fill_color="#05070B", fill_opacity=1)
    return VGroup(r, wrapped_label(text, w - 0.25, font_size, color).move_to(r))


class Filters(VoiceoverScene):
    def construct(self):
        self.card()
        self.cherry()
        self.split_span()
        self.broadbent()

    def card(self):
        card = chapter_card(1, r"The cocktail party and the filter", r"How does one voice win in a noisy room?",
                            lit={1953: r"Cherry", 1958: r"Broadbent"}, part=PART, scale=("mind",),
                            marr=("what", "how"))
        with self.voiceover("Chapter one. The cocktail party and the filter."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def cherry(self):
        head = heading(r"Two messages, \ one in each ear")
        headph = VGroup(Arc(radius=1.1, start_angle=0, angle=PI, color=GREY_B, stroke_width=4),
                        RoundedRectangle(width=0.35, height=0.7, corner_radius=0.12, color=CUE, fill_opacity=0.4)
                        .move_to([-1.1, -0.2, 0]),
                        RoundedRectangle(width=0.35, height=0.7, corner_radius=0.12, color=ATT, fill_opacity=0.4)
                        .move_to([1.1, -0.2, 0]))
        headph.move_to([0, 1.5, 0])
        left = label(r"left ear: \ ignore", font_size=24, color=CUE).next_to(headph, LEFT, buff=0.4)
        right = label(r"right ear: \ repeat aloud, \ word by word", font_size=24, color=ATT).next_to(headph, RIGHT,
                                                                                                      buff=0.4)
        keep_in_frame(right)
        rows = rows_of([
            (r"1953: \ Colin Cherry names the cocktail party problem, \ and tests it with headphones", WHITE),
            (r"shadowing: \ repeat one ear's message aloud as it arrives", ATT),
            (r"from the other ear people report almost nothing: \ not the words, \ not even the language", CUE),
            (r"but they notice a change from a man's voice to a woman's, \ or a pure tone", GREY_A),
            (r"physical features get through; \ meaning seems not to", ATT),
        ], 12.4, 27, 0.32).move_to([0, -1.45, 0])
        tag = historical_tag(archive.CHERRY_1953.cite)
        with self.voiceover(
            "At a party, a dozen conversations reach your ears at once, and you follow one. <bookmark mark='a'/> In "
            "1953 Colin Cherry, an engineer interested in communication, called this the cocktail party problem, and "
            "turned it into an experiment with headphones. <bookmark mark='b'/> A different message plays in each "
            "ear, and the listener must shadow one of them: repeat it aloud, word by word, as it arrives. That keeps "
            "attention firmly on one ear. <bookmark mark='c'/> Afterwards, asked about the other ear, people could "
            "say almost nothing: not the words, not the topic, and in some tests not even whether the language had "
            "changed. <bookmark mark='d'/> But they did notice when the voice changed from a man's to a woman's, or "
            "when the speech was replaced by a tone. <bookmark mark='e'/> Physical features of the ignored message got "
            "through. Its meaning, apparently, did not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(headph))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(left), FadeIn(rows[1]))
            for m, r in zip("cde", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def split_span(self):
        head = heading(r"The split span")
        lefts = VGroup(*[label(d, font_size=44, color=CUE) for d in "734"]).arrange(DOWN, buff=0.35)
        rights = VGroup(*[label(d, font_size=44, color=ATT) for d in "291"]).arrange(DOWN, buff=0.35)
        lefts.move_to([-3.2, 1.0, 0])
        rights.move_to([-1.2, 1.0, 0])
        ll = label(r"left ear", font_size=22, color=CUE).next_to(lefts, UP, buff=0.25)
        rl = label(r"right ear", font_size=22, color=ATT).next_to(rights, UP, buff=0.25)
        pairs = VGroup(*[DashedLine(lefts[k].get_right(), rights[k].get_left(), color=GREY_D, stroke_width=2)
                         for k in range(3)])
        rep = VGroup(label(r"reported: \ 7 3 4, \ then 2 9 1", font_size=28, color=WHITE),
                     label(r"ear by ear, \ easily", font_size=24, color=GOOD),
                     label(r"asked for 7 2, \ 3 9, \ 4 1: \ pair by pair, \ much worse", font_size=24, color=BAD))
        rep.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.0, 1.0, 0])
        rows = rows_of([
            (r"three pairs of digits, \ one of each pair in each ear, \ at the same moment", WHITE),
            (r"people recall one ear's digits, \ then the other's: \ the ear is the unit of selection", ATT),
            (r"Broadbent: \ the mind switches between channels defined by physical features", GREY_A),
        ], 12.4, 27, 0.32).to_edge(DOWN, buff=0.8)
        tag = historical_tag(archive.BROADBENT_1958.cite)
        with self.voiceover(
            "Donald Broadbent, who had trained as an RAF pilot and studied how air-traffic controllers coped with many "
            "voices at once, added a simpler test. "
            "<bookmark mark='a'/> Three pairs of digits arrive at once, one of each pair in each ear: seven and two "
            "together, then three and nine, then four and one. <bookmark mark='b'/> Asked to report them in any order, "
            "people give one ear's digits and then the other's: seven three four, then two nine one. Asked to give "
            "them pair by pair, in the order they arrived, they do much worse. <bookmark mark='c'/> So the ear, a "
            "physical channel, is the unit the mind selects, and switching between channels takes time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ll), FadeIn(rl))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(lefts[k]), FadeIn(rights[k]), Create(pairs[k]))
                                    for k in range(3)], lag_ratio=0.6), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rep[0]), FadeIn(rep[1]), FadeIn(rows[1]))
            self.play(FadeIn(rep[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def broadbent(self):
        head = heading(r"1958: \ the first box-and-arrow diagram of a mind")
        senses = box(r"the senses, \ in parallel", GREY_B, 2.3)
        store = box(r"a short-term store: \ everything, \ briefly", CUE, 2.5)
        filt = box(r"a selective filter: \ by physical feature", ATT, 2.5)
        chan = box(r"a limited channel: \ meaning, \ one at a time", CONTROL, 2.6)
        mem = box(r"long-term memory, \ response", GREY_B, 2.3)
        chain = VGroup(senses, store, filt, chan, mem).arrange(RIGHT, buff=0.38).move_to([0, 1.3, 0])
        if chain.width > 13.4:
            chain.scale_to_fit_width(13.4)
        arrows = VGroup(*[Arrow(chain[k].get_right(), chain[k + 1].get_left(), buff=0.06, color=GREY_B,
                                stroke_width=3, max_tip_length_to_length_ratio=0.3) for k in range(4)])
        rows = rows_of([
            (r"Perception and Communication: \ information flows through stages, \ like a telephone line", WHITE),
            (r"the filter selects early, \ by ear, \ voice or location, \ before meaning is extracted", ATT),
            (r"what the filter rejects is never understood: \ it decays from the store in seconds", CUE),
            (r"a mind drawn as information processing: \ the template for half a century of cognitive psychology",
             CONTROL),
        ], 12.4, 26, 0.32).to_edge(DOWN, buff=0.8)
        tag = historical_tag(archive.BROADBENT_1958.cite)
        with self.voiceover(
            "In 1958, in Perception and Communication, Broadbent drew what he thought was happening, and the drawing "
            "changed psychology. <bookmark mark='a'/> Information flows through stages, like signals through a "
            "telephone exchange. The senses take everything in, in parallel, into a short-term store that holds it "
            "briefly. <bookmark mark='b'/> Then a selective filter passes one channel, chosen by a physical feature: "
            "an ear, a voice, a location. Only what passes reaches a channel of limited capacity, where meaning is "
            "extracted, one message at a time. <bookmark mark='c'/> What the filter rejects is never understood, and "
            "fades from the store in a few seconds. That explains Cherry's listeners and the split span. "
            "<bookmark mark='d'/> It was among the first diagrams of a mind as information processing, boxes and "
            "arrows that could be tested, and it set the style of cognitive psychology for the next fifty years. "
            "Its specific claim, that selection comes early, before meaning, lasted about a year."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(senses), GrowArrow(arrows[0]), FadeIn(store), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[1]), FadeIn(filt), FadeIn(rows[1]))
            self.play(GrowArrow(arrows[2]), FadeIn(chan), GrowArrow(arrows[3]), FadeIn(mem))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
