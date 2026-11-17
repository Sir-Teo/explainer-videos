from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.ebbinghaus()
        self.your_list()
        self.question()
        self.objectives()

    def ebbinghaus(self):
        e = archive.EBBINGHAUS_1885.data
        syll = VGroup(*[label(s, font_size=40, color=WORD) for s in ("DAX", "BUP", "ZOL", "KEF", "MIB", "TOV", "WUG")])
        syll.arrange(RIGHT, buff=0.55).move_to([0, 2.5, 0])
        strip = trial_strip([
            (r"a list of 13 syllables", label(r"DAX \ BUP \ ZOL \ ...", font_size=28, color=WORD), r"read aloud"),
            (r"repeat until recited without error", label(r"1, 2, 3, ...", font_size=30, color=GREY_B),
             r"time it"),
            (r"wait: \ 20 minutes to 31 days", label(r"...", font_size=40, color=GREY_B), ""),
            (r"learn it again", label(r"faster", font_size=30, color=MODEL), r"time it"),
        ], frame_w=2.7, frame_h=1.2, font_size=19).move_to([0, 0.55, 0])
        eq = MathTex(r"\text{savings}", r"=", r"\frac{T_{\text{first}} - T_{\text{again}}}{T_{\text{first}}}",
                     font_size=40).move_to([0, -1.35, 0])
        eq[0].set_color(MODEL)
        rows = rows_of([
            (rf"Berlin, \ 1879 to 1884: \ one subject, \ himself; \ about {num(e['syllables_created'])} invented "
             r"syllables, \ chosen to mean nothing", WHITE),
            (r"savings measure memory that recall cannot see: \ a list you cannot recite is still learnt faster",
             MODEL),
        ], 12.4, 25, 0.25).to_edge(DOWN, buff=0.75)
        tag = historical_tag(archive.EBBINGHAUS_1885.cite)
        with self.voiceover(
            "In the early 1880s, in Berlin, a young philosopher named Hermann Ebbinghaus set out to do what most of "
            "his colleagues thought impossible: to measure memory. <bookmark mark='a'/> He needed material that "
            "carried no meaning, so that what he already knew could not help him. So he made it up: about two "
            "thousand three hundred syllables, a consonant, a vowel and a consonant, that are not words. "
            "<bookmark mark='b'/> He read a list of thirteen of them aloud, at a steady pace, again and "
            "again, until he could recite it without a mistake, and timed how long that took. Then he waited, "
            "from twenty minutes to a month, and learned the same list again. <bookmark mark='c'/> The second "
            "learning was faster, and the time he saved, as a share of the first, was his measure of what "
            "remained. <bookmark mark='d'/> Savings is a remarkable idea. A day later he could recite almost none of "
            "a list, and yet it was still in him: he learned it again in two thirds of the time. Memory is more than "
            "what you can call up."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.15) for s in syll], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(syll), FadeIn(strip))
            vo.wait_until("c")
            self.play(Write(eq))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def your_list(self):
        stage = demo_stage(8.8, 4.2, center=[0, 0.6, 0])
        note = label(r"sixteen words, \ one every second and a half; \ then write down all you remember",
                     font_size=24, color=GREY_A).next_to(stage, DOWN, buff=0.3)
        with self.voiceover(
            "Ebbinghaus was his own subject. Today, you are mine. <bookmark mark='a'/> Find a pen and a piece of "
            "paper. Sixteen words will appear, one every second and a half. Just watch them. When they stop, write "
            "down every word you can remember, in any order, in the order they come to you. Here they come."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(note))
        spot = stage.box.get_center() + UP * 0.2
        for w in WORDS:
            t_ = label(w, font_size=72, color=WHITE).move_to(spot)
            self.add(t_)
            self.wait(1.2)
            self.remove(t_)
            self.wait(0.3)
        pen = label(r"now write down every word you remember, \ in any order", font_size=32, color=YOU).move_to(spot)
        pause = VGroup(Rectangle(width=0.22, height=0.8, fill_color=YOU, fill_opacity=1, stroke_width=0),
                       Rectangle(width=0.22, height=0.8, fill_color=YOU, fill_opacity=1, stroke_width=0)
                       ).arrange(RIGHT, buff=0.22).next_to(pen, DOWN, buff=0.45)
        with self.voiceover(
            "Now write down every word you remember, in the order they come to mind. Pause the video, and take as "
            "long as you need. <bookmark mark='a'/> When you're done, number your words: one for the first you "
            "wrote, two for the second, and so on. Keep the paper. We'll score it together, and by the end of the "
            "hour your sheet will show three of the most reliable regularities in all of psychology."
        ) as vo:
            self.play(FadeIn(pen))
            self.play(FadeIn(pause))
            vo.wait_until("a")
            self.play(pen.animate.set_color(GREY_B), FadeOut(pause))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ when you remember, \ what is being searched, \ and with what?")
        rows = rows_of([
            (r"how fast is a memory lost, \ and what law does the loss follow?", LOST),
            (r"why the first and the last words, \ and why in that order?", WORD),
            (r"what you do while learning, \ and where you are, \ when you try to remember", CUE),
            (r"two models of the search, \ one of them fitted to 3,528 lists of real recall", MODEL),
            (r"memory as a valley a network rolls into, \ and the brain systems that keep it", CTX),
        ], 11.8, 30, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "This part is about long-term memory, and above all about how you find something in it. "
            "<bookmark mark='a'/> How quickly is a memory lost, and what law does the loss follow? "
            "<bookmark mark='b'/> Why do people remember the first and the last words of a list best, and why do "
            "they recall them in the order they do? <bookmark mark='c'/> What does it matter what you were doing "
            "while you learned, and where you were? <bookmark mark='d'/> We'll build two models of the search, and "
            "fit one of them to three and a half thousand lists recalled by real people. <bookmark mark='e'/> And "
            "we'll see memory as a valley that a network of neurons rolls into, and the brain systems that make it."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 20", font_size=34, color=GREY_B), label(r"Memory I: \ Storing and Finding",
                                                                           font_size=60))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"savings and the forgetting curve: \ three laws fitted, \ and ACT-R's activation",
            r"the serial-position curve and the order of recall, \ measured on open data",
            r"encoding and cues: \ levels of processing; \ divers on land and under water",
            r"SAM, \ and a context that drifts: \ derived, \ simulated, \ fitted by maximum likelihood",
            r"a Hopfield network: \ storage by Hebb's rule, \ recall by settling, \ capacity near $0.14N$",
            r"memory systems, \ recognition's two processes, \ and the hippocampus as an index",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 20 of Psychology, Built, the third part of Act Five, on thinking: memory, storing and "
            "finding. <bookmark mark='a'/> We'll start with Ebbinghaus's curve and fit three laws to it, and meet "
            "an equation that turns forgetting into a statement about the world. Then the shape and the order of "
            "free recall, measured on an open dataset from more than a hundred people. Then what happens at learning "
            "and at retrieval, including a famous experiment with divers and its replication. Then the two great "
            "models of the search, ending with one in which a slowly drifting context does almost all the work, "
            "derived and fitted. Then memories as the valleys of a network, the systems of memory in the brain, the "
            "two ways of recognising a face, and the hippocampus as an index to the rest."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=26.0)
        self.clear_scene()
