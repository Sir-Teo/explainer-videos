from __future__ import annotations

import numpy as np

from videos.music.music42.common import *  # noqa: F403

OPN = {(): r"the idea", ("first three notes",): r"its first three notes", ("diminish",): r"twice as fast"}


class Develop(SoundScene):
    def construct(self):
        chapter(self, 2, r"Developing variation", r"How does a phrase grow from four notes?")
        self.sentence_form()
        self.hear()
        self.derived()
        self.brahms()
        self.unity()

    # ------------------------------------------------------------------
    def sentence_form(self):
        blocks = VGroup()
        spec = [(r"basic idea", 2, TUNE), (r"repetition", 2, TUNE), (r"continuation: \ fragments", 2, BLUE), (r"faster", 1, BLUE), (r"cadence", 1, EAR)]
        x = -5.5
        for txt, w, col in spec:
            r = Rectangle(width=1.375 * w, height=0.9, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.18)
            r.move_to([x + 1.375 * w / 2, 0.6, 0])
            blocks.add(VGroup(r, label(txt, font_size=17, color=WHITE).move_to(r)))
            x += 1.375 * w
        nums = VGroup(*[label(rf"{b + 1}", font_size=15, color=GREY_A).move_to([-5.5 + 1.375 * (b + 0.5), -0.1, 0]) for b in range(8)])
        side = VGroup(label(r"Schoenberg's `sentence': \ an idea, \ its repetition, \ then a continuation that breaks it into pieces and speeds up", font_size=19, color=WHITE),
                      label(r"the continuation `liquidates' the idea: \ fewer of its features remain, \ until only the cadence is left", font_size=19, color=WHITE),
                      label(r"Beethoven's piano sonatas open this way again and again", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.8)
        head = label(r"a plan for eight bars: \ the sentence", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "How does a phrase grow from a motive? Schoenberg described a plan for eight bars that he called the sentence. "
            "<bookmark mark='a'/> A basic idea of two bars, then its repetition, often on another degree. "
            "<bookmark mark='b'/> Then a continuation that breaks the idea into fragments and speeds up, liquidating it, "
            "until only the cadence is left. Beethoven's piano sonatas open this way again and again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(blocks[:2]), FadeIn(nums), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(blocks[2:]), FadeIn(side[1:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("develop")
        c = clip("develop.sentence")
        g = scored(d["melody"], d["chords"], width=12.0, height=2.2, lo=55, hi=72, size=14).move_to(UP * 0.5)
        tags = VGroup()
        for f in d["figures"]:
            name = OPN.get(tuple(f["ops"]), "+".join(f["ops"]))
            k = f["k"]
            sh = "" if k == 0 else (rf" \ {k:+d}")
            x = g.frame.get_left()[0] + 12.0 * f["t"] / g.total
            tags.add(label(name + sh, font_size=13, color=BLUE if f["ops"] else TUNE).move_to([x + 0.05, g.frame.get_bottom()[1] - 0.3 - 0.3 * (len(tags) % 2), 0], aligned_edge=LEFT))
        cap = label(r"numbers: \ steps on the scale the figure is moved by", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"a sentence of ours, \ grown from the motive", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is a sentence of ours built from the motive. Bars one and two: the idea, then the idea a step higher. Bars "
            "three and four: its first three notes, falling in sequence. Bars five and six: the whole motive at twice the "
            "speed, falling again. Then a cadence. Listen for the motive in every bar."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(tags), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a sentence", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            flash(snd, g.roll.notes, [n[1] * 0.42 for n in d["melody"]], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derived(self):
        d = load("develop")
        rows_ = text_rows([
            (rf"{d['notes']} notes, \ every one of them before the cadence taken from the motive", WHITE),
            (r"two operations do almost all the work: \ fragmentation and transposition, \ then diminution", WHITE),
            (rf"the widest leap is {d['widest_leap']} semitones, \ the motive's own fifth", WHITE),
            (r"the harmony moves twice a bar, \ chosen so that every strong beat is a chord tone", TUNE),
            (r"made by hand; \ the searcher of chapter 9 has to find such plans for itself", GREY_A),
        ])
        head = label(r"what the sentence is made of", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            f"Take stock. <bookmark mark='a'/> The sentence has {say(d['notes'])} notes, and every one before the cadence comes "
            "from the motive. <bookmark mark='b'/> Two operations do almost all the work, fragmentation and transposition, "
            f"and then diminution. <bookmark mark='c'/> The widest leap is {say(d['widest_leap'])} semitones, the motive's "
            "own fifth. <bookmark mark='d'/> The harmony moves twice a bar, chosen so that every strong beat is a chord tone. "
            "<bookmark mark='e'/> We made it by hand. The searcher of chapter nine has to find such plans for itself."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def brahms(self):
        items = [
            (r"Schoenberg, \ `Brahms the Progressive' \ (1947): \ `developing variation'", WHITE),
            (r"each new idea is a variation of an earlier one, \ so a piece unfolds without literal repetition", WHITE),
            (r"Brahms, \ and Beethoven before him, \ build long movements from a few motives this way", WHITE),
            (r"unity from the source, \ variety from the operations: \ the balance a composer manages", TUNE),
            (r"Schoenberg's twelve-tone rows \ (Part 29) \ push the idea to its limit: \ everything from one ordering", GREY_A),
        ]
        rows_scene(self, r"developing variation", items,
                   "Schoenberg gave the technique a name in an essay of 1947, Brahms the Progressive: developing variation. "
                   "<bookmark mark='b'/> Each new idea is a variation of an earlier one, so a piece unfolds without literal "
                   "repetition. <bookmark mark='c'/> Brahms, and Beethoven before him, built long movements from a few motives "
                   "this way. <bookmark mark='d'/> Unity comes from the source, and variety from the operations; the balance "
                   "between them is what a composer manages. <bookmark mark='e'/> Schoenberg's own twelve-tone rows, Part 29, "
                   "push the idea to its limit: everything from one ordering.", marks="bcde")

    # ------------------------------------------------------------------
    def unity(self):
        d = load("search")
        v = d["best"]["verdict"]
        items = [
            (r"unity: \ the share of bars whose figure the motive yields in at most two operations", WHITE),
            (r"variety: \ the share of bars whose figure is not repeated note for note", WHITE),
            (r"both are computable, \ because the operations are functions: \ search them all, \ two deep", WHITE),
            (rf"the searcher's kept draft: \ unity {v['unity']:.2f}, \ variety {v['variety']:.2f}", TUNE),
            (r"critics that measure a balance are the heart of chapter 9", GREY_A),
        ]
        rows_scene(self, r"unity and variety, \ measured", items,
                   "Can that balance be measured? <bookmark mark='b'/> Call unity the share of bars whose figure the motive "
                   "yields in at most two operations, <bookmark mark='c'/> and variety the share of bars whose figure is not "
                   "repeated note for note. <bookmark mark='d'/> Both are computable, because the operations are functions: a "
                   "program can try them all, two deep. <bookmark mark='e'/> The draft the searcher kept in the opening "
                   f"question scores {say(v['unity'], 2)} for unity and {say(v['variety'], 2)} for variety. "
                   "<bookmark mark='f'/> Critics that measure a balance are the heart of chapter nine.", marks="cdef")
