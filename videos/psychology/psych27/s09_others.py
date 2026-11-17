from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


def box(text, col, pos, w=2.0, h=0.8, fs=20):
    b = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=col, stroke_width=2,
                         fill_color=BLACK, fill_opacity=0.6).move_to(pos)
    return VGroup(b, label(text, font_size=fs, color=col).move_to(b))


class Others(VoiceoverScene):
    def construct(self):
        self.card()
        self.recurrent()
        self.higher()
        self.map_()

    def card(self):
        card = chapter_card(8, r"Recurrence and higher order", r"Two more theories, \ one prediction each",
                            lit={2006: r"Lamme; \ Lau \& Passingham", 2011: r"Lau \& Rosenthal",
                                 2019: r"Brown, \ Lau \& LeDoux"},
                            part=PART, scale=("mind", "brain"), marr=("how",))
        with self.voiceover("Chapter eight. Recurrence and higher order."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def recurrent(self):
        head = heading(r"Recurrent processing")
        areas = VGroup(*[box(n, RPT, [-5.0 + 2.4 * k, 1.2, 0], w=1.7) for k, n in
                         enumerate((r"V1", r"V2", r"V4", r"IT", r"PFC"))])
        ff = VGroup(*[Arrow(areas[k].get_right(), areas[k + 1].get_left(), buff=0.05, color=UNSEEN, stroke_width=3,
                            max_tip_length_to_length_ratio=0.25) for k in range(4)])
        fb = VGroup(*[CurvedArrow(areas[k + 1].get_bottom() + LEFT * 0.2, areas[k].get_bottom() + RIGHT * 0.2,
                                  angle=-PI / 2.5, color=RPT, stroke_width=3, tip_length=0.12) for k in range(3)])
        lab_ff = label(r"feed-forward sweep: \ about 100 ms, \ unconscious", font_size=20, color=UNSEEN).next_to(
            areas, UP, buff=0.35)
        lab_fb = label(r"local recurrence: \ experience", font_size=20, color=RPT).next_to(areas, DOWN, buff=0.75)
        rows = rows_of([
            (r"Lamme, \ 2006: \ a first sweep through the visual areas extracts features, \ unconsciously; \ "
             r"experience arises when later areas feed back to earlier ones", WHITE),
            (r"prediction: \ interrupt the feedback, \ as backward masking does, \ and awareness goes while the first "
             r"sweep survives", RPT),
            (r"local recurrence for seeing; \ global, \ workspace-like recurrence only for reporting", MODEL),
        ], 12.0, 23, 0.3).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Lamme (2006)")
        with self.voiceover(
            "Two more theories, each with one diagram and one prediction. <bookmark mark='a'/> Victor Lamme's "
            "recurrent processing theory starts from timing. A first sweep of activity passes through the visual "
            "areas in about a hundred milliseconds, extracting features, and on its own it is unconscious. "
            "<bookmark mark='b'/> Experience arises when later areas feed back to earlier ones, and the areas "
            "reverberate. <bookmark mark='c'/> So interrupt the feedback, as a mask arriving at the right moment "
            "does, and awareness should vanish while the first sweep survives, which is roughly what masking "
            "studies find. <bookmark mark='d'/> For Lamme, local recurrence within the visual areas is enough for "
            "seeing; the wide, workspace-like recurrence is needed only for reporting, which puts him on the side of "
            "the back of the brain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(areas))
            vo.wait_until("a")
            self.play(Create(ff), FadeIn(lab_ff), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(fb), FadeIn(lab_fb))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def higher(self):
        head = heading(r"Higher-order theories")
        first = box(r"a visual state: \ red, \ there", SEEN, [-3.4, 0.2, 0], w=3.6, h=1.0, fs=22)
        second = box(r"a state about it: \ I am seeing red", HOT, [-3.4, 2.0, 0], w=3.6, h=1.0, fs=22)
        arr = Arrow(second.get_bottom(), first.get_top(), buff=0.08, color=HOT, stroke_width=4)
        rows = rows_of([
            (r"Rosenthal; \ Lau and Rosenthal, \ 2011: \ a state is conscious when the mind represents itself as being "
             r"in it", WHITE),
            (r"the higher-order state lives in prefrontal cortex; \ metacognition, \ Part 12's meta-$d'$, \ is close "
             r"kin", HOT),
            (r"Lau and Passingham, \ 2006: \ two masking conditions with the same accuracy, \ different reported "
             r"visibility; \ the difference was in prefrontal cortex", GNW),
            (r"prediction: \ awareness can change while performance does not", MODEL),
        ], 5.8, 22, 0.32).move_to([3.4, 0.2, 0])
        tag = published_tag(r"Lau \& Passingham (2006); \ Lau \& Rosenthal (2011); \ Brown, \ Lau \& LeDoux (2019)")
        with self.voiceover(
            "The other family is the higher-order theories. <bookmark mark='a'/> On David Rosenthal's account, "
            "developed with Hakwan Lau, a mental state is conscious when the mind represents itself as being in "
            "it. Seeing red is unconscious until there is also a state to the effect that I am seeing red. "
            "<bookmark mark='b'/> The higher-order state is thought to live in prefrontal cortex, and it's close kin "
            "to the metacognition of Part 12. <bookmark mark='c'/> In 2006 Lau and Richard Passingham found two "
            "masking conditions in which people were equally accurate but reported different visibility, and the "
            "difference showed up in dorsolateral prefrontal cortex. <bookmark mark='d'/> The prediction that sets "
            "these theories apart: awareness can change while performance stays the same, and when it does, look "
            "to the front of the brain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(first))
            vo.wait_until("a")
            self.play(FadeIn(second), GrowArrow(arr), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def map_(self):
        head = heading(r"Four theories, \ one question: \ front or back?")
        cols = [(r"global workspace", r"front and back: \ ignition in prefrontal--parietal network", GNW, r"front"),
                (r"integrated information", r"the posterior hot zone", IIT, r"back"),
                (r"recurrent processing", r"local recurrence in sensory cortex", RPT, r"back"),
                (r"higher order", r"prefrontal re-representation", HOT, r"front")]
        boxes = VGroup()
        for name, txt, col, side in cols:
            b = RoundedRectangle(corner_radius=0.12, width=2.9, height=2.6, stroke_color=col, stroke_width=2,
                                 fill_color=BLACK, fill_opacity=0.5)
            body = VGroup(label(name, font_size=21, color=col), wrapped_label(txt, 2.5, 19, WHITE),
                          label(side, font_size=26, color=col)).arrange(DOWN, buff=0.3).move_to(b)
            boxes.add(VGroup(b, body))
        boxes.arrange(RIGHT, buff=0.25).move_to([0, 0.6, 0])
        foot = wrapped_label(r"no-report designs, \ lesions and stimulation are the tests: \ does experience survive "
                             r"when the front is silent, \ or removed?", 12.0, 24, MODEL).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Seth \& Bayne (2022)")
        with self.voiceover(
            "Put the four side by side, as Anil Seth and Tim Bayne did in a 2022 review, and one question divides "
            "them. <bookmark mark='a'/> The workspace needs the prefrontal and parietal network; higher-order "
            "theories need prefrontal re-representation. Integrated information and recurrent processing put "
            "experience in the back of the brain. <bookmark mark='b'/> No-report designs, lesions and stimulation "
            "are the tests: does experience survive when the front of the brain is silent, or damaged? That's the "
            "question an adversarial collaboration set out to settle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in boxes], lag_ratio=0.5), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()
