from __future__ import annotations

import numpy as np

from videos.music.music43.common import *  # noqa: F403

META = [("games", 26), ("music", 21), ("sports", 18), ("education", 4), ("professions", 1)]


class Practice(SoundScene):
    def construct(self):
        chapter(self, 9, r"Practice and the performer's body", r"What does practice explain, \ and what does it cost?")
        self.ericsson()
        self.meta()
        self.how()
        self.anxiety()
        self.body()

    # ------------------------------------------------------------------
    def ericsson(self):
        items = [
            (r"Ericsson, \ Krampe and Tesch-R\"omer \ (1993): \ violin students at a Berlin academy, \ ranked by their teachers", WHITE),
            (r"the best had practised alone about 10,000 hours by age 20; \ the least good about 5,000", WHITE),
            (r"`deliberate practice': \ effortful, \ focused on weaknesses, \ with feedback; \ not just playing", WHITE),
            (r"popularised as a `10,000-hour rule', \ which the authors did not claim", TUNE),
            (r"how much of skill does practice explain?", GREY_A),
        ]
        rows_scene(self, r"deliberate practice", items,
                   "How are performers made? In 1993 Anders Ericsson, Ralf Krampe and Clemens Tesch-Römer studied violin "
                   "students at a Berlin academy, ranked by their teachers. <bookmark mark='b'/> The best had practised alone "
                   "about ten thousand hours by the age of twenty; the least good, about five thousand. <bookmark mark='c'/> They "
                   "called the key ingredient deliberate practice: effortful, focused on weaknesses, with feedback, and not just "
                   "playing. <bookmark mark='d'/> It was popularised as a ten-thousand-hour rule, which the authors did not "
                   "claim. <bookmark mark='e'/> How much of skill does practice actually explain?", marks="bcde")

    # ------------------------------------------------------------------
    def meta(self):
        x0, W = -2.6, 7.0
        bars = VGroup()
        for i, (k, v) in enumerate(META):
            w = W * v / 30
            y = 1.4 - 0.75 * i
            bars.add(VGroup(label(k, font_size=21, color=WHITE).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT),
                            Rectangle(width=max(w, 0.04), height=0.45, stroke_width=0, fill_color=TUNE if k == "music" else BLUE, fill_opacity=0.85).move_to([x0 + w / 2, y, 0]),
                            label(rf"{v}\%" if v > 1 else r"under 1\%", font_size=19, color=WHITE).move_to([x0 + w + 0.55, y, 0])))
        cap = label(r"share of the differences in performance accounted for by deliberate practice \ (Macnamara, \ Hambrick and Oswald, \ 2014; \ 88 studies)", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.7)
        head = label(r"what practice explains", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "In 2014 Brooke Macnamara, David Hambrick and Frederick Oswald pooled eighty-eight studies. <bookmark mark='a'/> Deliberate practice accounted for about twenty-one per cent of the differences in performance in music, twenty-six in games, eighteen in sports, four in education, and under one per cent in the professions. Practice matters a great deal in music, and leaves substantial unexplained variation. These observational associations neither allocate the remainder among causes nor measure an individual's potential."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.25))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def how(self):
        items = [
            (r"spacing beats massing: \ practice spread over days is retained better than the same hours in one block", WHITE),
            (r"interleaving: \ mixing passages and tempos in a session helps later performance, \ though it feels worse", WHITE),
            (r"slow practice and chunking: \ build a passage from units the hand can run without attention", WHITE),
            (r"mental practice works, \ less than physical: \ the motor plan is rehearsed without the muscles", TUNE),
            (r"the same findings as motor learning in sport", GREY_A),
        ]
        rows_scene(self, r"how to practise, \ by the evidence", items,
                   "What makes practice work? Studies of motor learning give some answers. <bookmark mark='b'/> Spacing beats "
                   "massing: practice spread over days is retained better than the same hours in one block. "
                   "<bookmark mark='c'/> Interleaving, mixing passages and tempos within a session, helps later performance, "
                   "though it feels worse at the time. <bookmark mark='d'/> Slow practice and chunking build a passage from units "
                   "the hands can run without attention. <bookmark mark='e'/> Mental practice works too, less than physical "
                   "practice: the motor plan is rehearsed without the muscles. <bookmark mark='f'/> These are the same findings as "
                   "in sport.", marks="bcdef")

    # ------------------------------------------------------------------
    def anxiety(self):
        items = [
            (r"performance anxiety is common: \ in surveys of orchestral musicians, \ a large minority report it as a problem", WHITE),
            (r"some arousal helps; \ too much narrows attention and stiffens the hands", WHITE),
            (r"what helps in trials: \ cognitive and behavioural therapy, \ graded exposure, \ preparation", WHITE),
            (r"beta-blockers damp the trembling, \ not the worry, \ and are used widely", TUNE),
            (r"memory: \ performers memorise by sound, \ by hand, \ by sight and by structure, \ so one can rescue another", GREY_A),
        ]
        rows_scene(self, r"memory and anxiety", items,
                   "Then there is the stage. <bookmark mark='b'/> Performance anxiety is common: in surveys of orchestral musicians a large minority report it as a problem. <bookmark mark='c'/> Some arousal helps; too much narrows attention and stiffens the hands. <bookmark mark='d'/> In trials, cognitive and behavioural therapy, graded exposure and preparation help. <bookmark mark='e'/> Some musicians use prescribed beta-blockers for physical symptoms; effects, contraindications and treatment choices require individual clinical assessment. <bookmark mark='f'/> And memory: performers memorise by sound, by hand, by sight and by structure, so that when one fails another can rescue it.", marks="bcdef")

    # ------------------------------------------------------------------
    def body(self):
        items = [
            (r"overuse injuries are the commonest complaint: \ hands, \ arms, \ neck and back", WHITE),
            (r"focal dystonia: \ a complex neurological movement disorder; \ about 1 in 100 professional musicians", WHITE),
            (r"hearing: \ orchestral players can exceed safe daily noise doses; \ woodwinds seated in front of the brass are the classic case", WHITE),
            (r"the EU's 2003 noise directive applies to orchestras: \ screens, \ seating and earplugs", TUNE),
            (r"chapter 10: \ machines that learn to perform", GREY_A),
        ]
        rows_scene(self, r"the performer's body", items,
                   "Performing is also physical work. <bookmark mark='b'/> Overuse injuries of the hands, arms, neck and back are the commonest complaint. <bookmark mark='c'/> Task-specific focal dystonia, a complex neurological movement disorder affecting voluntary control, affects roughly one professional musician in a hundred. <bookmark mark='d'/> Hearing is at risk too: orchestral players can exceed safe daily noise doses, the woodwinds seated in front of the brass being the classic case. <bookmark mark='e'/> The European Union's 2003 noise directive applies to orchestras, which now use screens, seating plans and earplugs. <bookmark mark='f'/> Chapter ten turns to machines that learn to perform.", marks="bcdef")
