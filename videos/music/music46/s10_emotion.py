from __future__ import annotations

import numpy as np

from videos.music.music46.common import *  # noqa: F403


class Emotion(SoundScene):
    def construct(self):
        chapter(self, 9, r"Expressed emotion", r"How does music sound happy or sad?")
        self.quiz()
        self.cues()
        self.chills()
        self.mechanisms()
        self.sad()
        self.memory()
        self.replicate()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("emotion")
        c = clip("emotion.four")
        card = listen_card(r"The Tune's first two phrases, \ four ways. \ For each, \ which emotion does it express: \ "
                           r"happy, \ sad, \ angry or tender?", width=10.4)
        with self.voiceover(
            "A question for your ears. The Tune's first two phrases, four ways. For each, which emotion does it express: "
            "happy, sad, angry, or tender?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        keys = list(d["settings"])
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.2, corner_radius=0.15, stroke_color=GREY_B), label(k, font_size=30, color=WHITE)).arrange(ORIGIN)
                         for k in keys]).arrange(RIGHT, buff=0.6).move_to(UP * 0.9)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"four settings", kind="synthesized", detail=r"piano, \ strings, \ brass, \ flute", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        ans = VGroup(*[label(d["answer"][k], font_size=22, color=TUNE).next_to(boxes[i], DOWN, buff=0.3) for i, k in enumerate(keys)])
        how = label(r"fast, \ high, \ major, \ detached; \ \ slow, \ low, \ minor, \ legato; \ \ fast, \ low, \ minor, \ loud; \ \ slow, \ high, \ major, \ soft", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Happy, sad, angry, tender. Most listeners agree, and they agree across cultures more than you might expect. "
            "The notes were the same each time. What changed were cues: tempo, register, mode, loudness, articulation and "
            "timbre."
        ):
            self.play(FadeIn(ans), FadeIn(how))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cues(self):
        hdr = [r"", r"tempo", r"loudness", r"articulation", r"mode", r"timbre"]
        table = [(r"happy", r"fast", r"fairly loud", r"detached", r"major", r"bright"),
                 (r"sad", r"slow", r"soft", r"legato", r"minor", r"dull"),
                 (r"angry", r"fast", r"loud", r"sharp attacks", r"minor or dissonant", r"harsh"),
                 (r"tender", r"slow", r"soft", r"legato", r"major", r"soft, \ dull")]
        cells = VGroup(*[label(t, font_size=17, color=GREY_A) for t in hdr], *[label(t, font_size=17, color=TUNE if j == 0 else WHITE) for row in table for j, t in enumerate(row)])
        cells.arrange_in_grid(rows=5, cols=6, buff=(0.45, 0.4)).move_to(DOWN * 0.1)
        head = label(r"cues to expressed emotion \ (after Juslin and Laukka, \ 2003)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"the same cues signal emotion in speech: \ a sad voice is slow, \ low and soft", font_size=17, color=TUNE).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Patrik Juslin and Petri Laukka reviewed over a hundred studies in 2003 and found a consistent code. "
            "<bookmark mark='a'/> Happy: fast, fairly loud, detached, major, bright. Sad: slow, soft, legato, minor, dull. "
            "Angry: fast, loud, sharp attacks, harsh. Tender: slow, soft, legato, gentle. <bookmark mark='b'/> And the same "
            "cues signal emotion in speech: a sad voice is slow, low and soft. Music may borrow the code the voice already "
            "uses."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(cells).copy().set_opacity(0.15)))
            vo.wait_until("a")
            self.play(FadeIn(cells))
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sad(self):
        items = [
            (r"perceived emotion is not felt emotion: \ a sad song need not make you sad", WHITE),
            (r"many people enjoy sad music: \ nostalgia, \ being moved, \ peacefulness are common reports", WHITE),
            (r"Vuoskoski, \ Eerola and others: \ enjoyment of sad music goes with empathy and openness", WHITE),
            (r"Huron's suggestion: \ the consolation hormone prolactin, \ released by sadness without real loss", TUNE),
            (r"a hypothesis, \ not yet confirmed", GREY_A),
        ]
        rows_scene(self, r"the pleasure of sad music", items,
                   "Why would anyone enjoy sad music? <bookmark mark='b'/> First, perceived emotion is not felt emotion: a sad "
                   "song need not make you sad. <bookmark mark='c'/> Many people do enjoy sad music, and report nostalgia, being "
                   "moved, and peace. <bookmark mark='d'/> Jonna Vuoskoski, Tuomas Eerola and others found that enjoyment of sad "
                   "music goes with empathy and openness. <bookmark mark='e'/> Huron suggested a hormone of consolation, "
                   "prolactin, released by sadness without any real loss, <bookmark mark='f'/> a hypothesis not yet confirmed.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def replicate(self):
        items = [
            (r"the `Mozart effect' \ (1993): \ ten minutes of Mozart briefly raised spatial reasoning; \ later meta-analyses found little or nothing", WHITE),
            (r"what remained was arousal and mood: \ any enjoyable stimulus helped a little", WHITE),
            (r"claims of music's power to cure, \ calm or teach often rest on small studies", WHITE),
            (r"the replication standard: \ preregistration, \ larger samples, \ shared data", TUNE),
            (r"chapter 10: \ predictive processing, \ and machines as listeners", GREY_A),
        ]
        rows_scene(self, r"what does not replicate", items,
                   "Some claims do not survive. <bookmark mark='b'/> The Mozart effect of 1993 said that ten minutes of Mozart "
                   "briefly raised spatial reasoning; later meta-analyses found little or nothing, <bookmark mark='c'/> and what "
                   "remained was arousal and mood: any enjoyable stimulus helped a little. <bookmark mark='d'/> Claims of music's "
                   "power to cure, calm or teach often rest on small studies. <bookmark mark='e'/> The remedy is the replication "
                   "standard: preregistration, larger samples, shared data. <bookmark mark='f'/> Chapter ten turns to predictive "
                   "processing, and machines as listeners.", marks="bcdef")

    # ------------------------------------------------------------------
    def chills(self):
        items = [
            (r"chills, \ or frisson: \ a shiver and goose bumps; \ about half to two thirds of people report them from music", WHITE),
            (r"Sloboda \ (1991): \ listeners' chill passages often held new harmonies, \ sudden loudness, \ or a voice entering", WHITE),
            (r"Grewe and colleagues \ (2007): \ chills are personal and unreliable: \ the same passage rarely gives everyone a chill", WHITE),
            (r"they follow expectation: \ violations, \ entrances, \ and arrivals after a build", TUNE),
            (r"the hook's dopamine, \ on the skin", GREY_A),
        ]
        rows_scene(self, r"chills", items,
                   "The hook's chills have been studied directly. <bookmark mark='b'/> Chills, or frisson, a shiver and goose "
                   "bumps, are reported from music by roughly half to two thirds of people. <bookmark mark='c'/> John Sloboda "
                   "found in 1991 that listeners' chill passages often held a new harmony, a sudden change in loudness, or a "
                   "voice entering; <bookmark mark='d'/> Oliver Grewe and colleagues found in 2007 that chills are personal and "
                   "unreliable: the same passage rarely gives everyone a chill. <bookmark mark='e'/> They follow expectation: "
                   "violations, entrances, and arrivals after a build. <bookmark mark='f'/> The hook's dopamine, on the skin.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def mechanisms(self):
        items = [
            (r"Juslin's BRECVEMA \ (2013): \ eight ways music arouses emotion", WHITE),
            (r"brainstem reflex \ (a sudden loud sound), \ rhythmic entrainment, \ evaluative conditioning", WHITE),
            (r"emotional contagion \ (the voice-like cues of this chapter), \ visual imagery, \ episodic memory", WHITE),
            (r"musical expectancy \ (this part's subject) \ and aesthetic judgement", TUNE),
            (r"different mechanisms, \ different time courses, \ different brain systems", GREY_A),
        ]
        rows_scene(self, r"eight mechanisms", items,
                   "Patrik Juslin listed the routes by which music arouses emotion, under the acronym BRECVEMA. "
                   "<bookmark mark='b'/> A brainstem reflex to a sudden loud sound; rhythmic entrainment of the body; evaluative "
                   "conditioning, music paired with past events. <bookmark mark='c'/> Emotional contagion, catching the "
                   "voice-like cues of this chapter; visual imagery; episodic memory. <bookmark mark='d'/> Musical expectancy, "
                   "this part's subject, and aesthetic judgement. <bookmark mark='e'/> Different mechanisms, with different time "
                   "courses and different brain systems.", marks="bcde")

    # ------------------------------------------------------------------
    def memory(self):
        items = [
            (r"the reminiscence bump: \ people remember and value most the music of their late teens and early twenties", WHITE),
            (r"Krumhansl and Zupnick \ (2013): \ young adults also knew, \ and liked, \ their parents' bump-era music", WHITE),
            (r"music cues autobiographical memories vividly, \ often with emotion attached", WHITE),
            (r"in dementia, \ musical memory is often among the last to go", TUNE),
            (r"liking a song is partly liking a time of one's life", GREY_A),
        ]
        rows_scene(self, r"music and memory", items,
                   "Memory is one of the strongest routes. <bookmark mark='b'/> In the reminiscence bump, people remember and "
                   "value most the music of their late teens and early twenties; <bookmark mark='c'/> Carol Krumhansl and Justin "
                   "Zupnick found in 2013 that young adults also knew, and liked, the music of their parents' bump years. "
                   "<bookmark mark='d'/> Music cues autobiographical memories vividly, often with emotion attached, "
                   "<bookmark mark='e'/> and in dementia musical memory is often among the last to go. <bookmark mark='f'/> "
                   "Liking a song is partly liking a time of one's life.", marks="bcdef")
