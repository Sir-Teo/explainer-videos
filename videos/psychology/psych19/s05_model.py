from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403


def box(text, color, w=2.6, h=1.1, font_size=24):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=color, stroke_width=3,
                         fill_color="#05070B", fill_opacity=1)
    return VGroup(r, wrapped_label(text, w - 0.25, font_size, color).move_to(r))


class Model(VoiceoverScene):
    def construct(self):
        self.card()
        self.modal()
        self.components()
        self.word_length()
        self.rate()

    def card(self):
        card = chapter_card(4, r"A system, \ not a store", r"What is short-term memory for?",
                            lit={1968: r"Atkinson \& Shiffrin", 1970: r"Shallice \& Warrington",
                                 1974: r"Baddeley \& Hitch"}, part=PART, scale=("mind", "brain"), marr=("what", "how"))
        with self.voiceover("Chapter four. A system, not a store."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def modal(self):
        p = archive.SHALLICE_WARRINGTON_1970.data
        head = heading(r"The modal model, \ and a patient it could not explain")
        b1 = box(r"sensory registers", GREY_B)
        b2 = box(r"short-term store", MEM)
        b3 = box(r"long-term store", LOOP)
        chain = VGroup(b1, b2, b3).arrange(RIGHT, buff=1.2).move_to([0, 1.7, 0])
        arr = VGroup(Arrow(b1.get_right(), b2.get_left(), buff=0.1, color=GREY_C),
                     Arrow(b2.get_right(), b3.get_left(), buff=0.1, color=GREY_C))
        reh = CurvedArrow(b2.get_top() + LEFT * 0.4, b2.get_top() + RIGHT * 0.4, angle=-2.5, color=MEM)
        rl = label(r"rehearsal", font_size=19, color=MEM).next_to(reh, UP, buff=0.08)
        rows = rows_of([
            (r"1968: \ Atkinson and Shiffrin: \ information passes through the short-term store on its way to the "
             r"long-term one", WHITE),
            (r"the longer an item is rehearsed there, \ the better it is learned", MEM),
            (rf"patient K.F.: \ a left-hemisphere injury; \ a digit span of about {p['kf_digit_span']}", LOST),
            (r"yet he learned word lists and pairs normally: \ a damaged gateway, \ an intact destination", LOOP),
            (r"and H.M., \ Part 7, \ showed the reverse: \ a double dissociation", GREY_A),
        ], 12.4, 25, 0.24).to_edge(DOWN, buff=0.8)
        tag = historical_tag(archive.SHALLICE_WARRINGTON_1970.cite)
        with self.voiceover(
            "By the late 1960s the pieces had been assembled into one diagram. <bookmark mark='a'/> Richard "
            "Atkinson and Richard Shiffrin's model, the modal model, has information flow from brief sensory registers "
            "into a short-term store of a few items, and from there into a long-term store. <bookmark mark='b'/> "
            "Rehearsal keeps items alive in the short-term store, and the longer they stay there, the better they're "
            "learned. The short-term store is the gateway to everything lasting. <bookmark mark='c'/> Then came a "
            "patient. K.F. had injured the left side of his brain in a motorcycle accident, and his span for "
            f"spoken digits was about {p['kf_digit_span']}. <bookmark mark='d'/> If the short-term store is the "
            "gateway, he should have learned nothing new. But Elizabeth Warrington and Tim Shallice found that he "
            "learned word lists and paired associates normally. <bookmark mark='e'/> H.M., in Part 7, had the "
            "opposite pattern: a normal span, and no new long-term memories. Two patients, two dissociations, and a "
            "gateway that isn't one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(chain), FadeIn(arr))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(reh), FadeIn(rl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), b2[0].animate.set_stroke(LOST, 5))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def components(self):
        head = heading(r"Working memory: \ Baddeley and Hitch, \ 1974")
        ex = box(r"central executive: \ attention and control", EXEC, w=4.6, h=1.0)
        lp = box(r"phonological loop: \ sounds, \ rehearsed by inner speech", LOOP, w=3.8, h=1.2, font_size=22)
        sk = box(r"visuospatial sketchpad: \ shapes and places", SKETCH, w=3.8, h=1.2, font_size=22)
        eb = box(r"episodic buffer \ (2000): \ bound episodes", MEM, w=3.8, h=1.2, font_size=22)
        lower = VGroup(lp, eb, sk).arrange(RIGHT, buff=0.45)
        g = VGroup(ex, lower).arrange(DOWN, buff=0.7).move_to([0, 1.35, 0])
        links = VGroup(*[Line(ex.get_bottom(), b.get_top(), color=GREY_C, stroke_width=2) for b in lower])
        ltm = label(r"long-term memory", font_size=22, color=GREY_B).next_to(lower, DOWN, buff=0.3)
        rows = rows_of([
            (r"dual-task logic: \ hold six digits while reasoning; \ reasoning slows a little, \ and does not collapse",
             WHITE),
            (r"so short-term memory is not one store, \ and it is not idle: \ it is a workspace for thinking", EXEC),
            (r"verbal and visual loads interfere within a kind, \ much less across kinds", LOOP),
        ], 12.4, 25, 0.24).to_edge(DOWN, buff=0.8)
        tag = historical_tag(archive.BADDELEY_HITCH_1974.cite)
        with self.voiceover(
            "Alan Baddeley and Graham Hitch asked a different question in 1974. <bookmark mark='a'/> Not how much "
            "the store holds, but what it's for. If the short-term store is the mind's workspace, filling it with six "
            "digits should wreck reasoning. It didn't: people verifying sentences about the order of two letters "
            "while repeating six digits slowed down, but kept their accuracy. <bookmark mark='b'/> So they replaced "
            "the store with a system. A central executive that directs attention, served by slave systems: "
            "<bookmark mark='c'/> a phonological loop that holds sounds and refreshes them by inner speech, and a "
            "visuospatial sketchpad for shapes and places. A verbal load interferes with a verbal task much more than "
            "with a visual one, and the other way round. In 2000 Baddeley added an episodic buffer that binds the "
            "pieces into episodes and talks to long-term memory. The phonological loop is the best understood part, "
            "and it makes a prediction you can test on yourself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(ex), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(lp), FadeIn(sk), Create(links[0]), Create(links[2]), FadeIn(rows[2]))
            self.play(FadeIn(eb), Create(links[1]), FadeIn(ltm))
        self.clear_scene()

    def word_length(self):
        d = load("loop")
        head = heading(r"The word-length effect, \ and how to abolish it")
        lists = VGroup(label(r"wit, \ sum, \ harm, \ bay, \ top", font_size=28, color=LOOP),
                       label(r"university, \ aluminium, \ opportunity, \ hippopotamus, \ refrigerator", font_size=26,
                             color=SLOT)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, 2.45, 0])
        A = axes([1, 9], [0, 1], x_length=6.4, y_length=2.8, xticks=[1, 3, 5, 7, 9], yticks=[0, 0.5, 1],
                 xlabel=r"words in the list", ylabel=r"whole list correct", center=[-2.6, -0.2, 0], font_size=18,
                 yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        L = d["lengths"]
        cs = VGroup(curve_in(ax, L, d["short_loop"], LOOP, 4), curve_in(ax, L, d["long_loop"], SLOT, 4))
        sup = VGroup(DashedVMobject(curve_in(ax, L, d["short_suppressed"], LOOP, 3), num_dashes=30),
                     DashedVMobject(curve_in(ax, L, d["long_suppressed"], SLOT, 3), num_dashes=30))
        key = legend([(LOOP, r"short words"), (SLOT, r"long words"), (GREY_B, r"dashed: \ saying ``the the the''")],
                     font_size=18)
        key.arrange(RIGHT, buff=0.45).next_to(A, DOWN, buff=0.25)
        keep_in_frame(key)
        rows = rows_of([
            (r"spans are longer for short words, \ even with the same number of syllables", WHITE),
            (r"Psyche: \ each item fades in about 2 s unless inner speech refreshes it; \ one cycle takes the list's "
             r"spoken length", MODEL),
            (r"say ``the the the'' aloud, \ and inner speech is busy: \ the effect vanishes, \ span falls to a small "
             r"non-verbal store", GREY_A),
            (rf"spans: \ short {d['short_loop_span']:.1f}, \ long {d['long_loop_span']:.1f}; \ suppressed "
             rf"{d['short_suppressed_span']:.1f} for both", MEM),
        ], 5.2, 22, 0.3).move_to([3.85, -0.3, 0])
        ptag = psyche_tag(r"\texttt{wm.loop\_span}: \ lifetimes lognormal, \ median 2 s; \ a store of 2")
        tag = published_tag(archive.BADDELEY_1975.cite)
        with self.voiceover(
            "Try these two lists. <bookmark mark='a'/> Five short words, and five long ones. People recall fewer long "
            "words than short ones, and Baddeley, Neil Thomson and Mary Buchanan showed in 1975 that it's spoken "
            "duration that matters, even when the words have the same number of syllables. <bookmark mark='b'/> "
            "Psyche's loop has one assumption: each item's trace fades in about two seconds unless inner speech "
            "says it again, and one pass of inner speech takes as long as the list takes to say. The curves show the "
            "chance of recalling a whole list against its length. <bookmark mark='c'/> Now the test you can run on "
            "yourself: say the the the, aloud, over and over, while you try to hold the list. Inner speech is busy, "
            "the loop can't refresh anything, and the word-length effect disappears. What is left is a small store "
            "that doesn't care how long the words are. <bookmark mark='d'/> In the model, the span for short words "
            f"is {d['short_loop_span']:.1f}, for long words {d['long_loop_span']:.1f}, and under suppression "
            f"{d['short_suppressed_span']:.1f} for both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(lists))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(A))
            vo.wait_until("b")
            self.play(Create(cs[0]), Create(cs[1]), FadeIn(rows[1]), FadeIn(ptag), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(sup[0]), Create(sup[1]), FadeIn(key), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def rate(self):
        d = load("loop")
        p = archive.BADDELEY_1975.data
        head = heading(r"Span is what you can say in about two seconds")
        A = axes([1, 4], [0, 10], x_length=6.6, y_length=3.6, xticks=[1, 2, 3, 4], yticks=[0, 2, 4, 6, 8, 10],
                 xlabel=r"reading rate, \ words per second", ylabel=r"span, \ words", center=[-2.4, 0.4, 0],
                 font_size=18)
        ax = A.ax
        c = VGroup(curve_in(ax, d["rate"], d["rate_span"], MODEL, 4), scatter(ax, d["rate"], d["rate_span"], MODEL, 0.05))
        sec = p["seconds_of_speech"]
        two = DashedLine(ax.c2p(1, sec * 1), ax.c2p(4, sec * 4), color=DATA, stroke_width=2)
        tl = label(r"two seconds' worth", font_size=19, color=DATA).next_to(ax.c2p(3.9, 7.6), LEFT, buff=0.1)
        rows = rows_of([
            (r"across people and word sets, \ span rises in a straight line with reading rate", WHITE),
            (r"Baddeley's summary: \ the loop holds what can be said in about two seconds", DATA),
            (r"fast talkers have longer spans; \ so do languages with short number words", MEM),
            (r"digit spans are longer in Chinese, \ whose digits are single quick syllables, \ than in Welsh", LOOP),
        ], 5.4, 23, 0.3).move_to([3.85, 0.3, 0])
        ptag = psyche_tag(r"\texttt{wm.loop\_span}: \ span against $1 / $word duration")
        tag = published_tag(archive.BADDELEY_1975.cite)
        with self.voiceover(
            "The loop predicts more than a difference between two lists. <bookmark mark='a'/> Plot span against how "
            "fast the words can be read aloud, and it rises in a straight line. <bookmark mark='b'/> Baddeley's "
            "summary is that the loop holds about as much as you can say in two seconds. <bookmark mark='c'/> It "
            "follows that fast talkers have longer spans, and so do languages whose number words are short. "
            "<bookmark mark='d'/> Digit span is longer in Chinese, where each digit is one quick syllable, than in "
            "English, and longer in English than in Welsh, where the digits take longer to say. Part of what a span "
            "measures is the speed of your inner voice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(ptag))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(two), FadeIn(tl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
