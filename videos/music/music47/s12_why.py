from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403


class Why(SoundScene):
    def construct(self):
        chapter(self, 11, r"Why music?", r"Did music evolve for something, \ or come along with something else?")
        self.classics()
        self.cheesecake()
        self.bonding()
        self.table()
        self.ours()

    # ------------------------------------------------------------------
    def classics(self):
        items = [
            (r"Charles Darwin \ (1871): \ song began as courtship display, \ like birdsong, \ before language", WHITE),
            (r"Herbert Spencer \ (1857): \ music grew out of the cadences of emotional speech", WHITE),
            (r"Darwin's view puts music first and speech after; \ Spencer's the reverse", WHITE),
            (r"Steven Mithen \ (2005): \ a shared ancestor of both, \ musical and wordless", TUNE),
            (r"each tells a story; \ the work is to find what each predicts", GREY_A),
        ]
        rows_scene(self, r"the first theories", items,
                   "Why do humans make music at all? The theories are old. <bookmark mark='b'/> Charles Darwin, in 1871, thought "
                   "song began as courtship display, as in birds, before there was language. <bookmark mark='c'/> Herbert "
                   "Spencer, in 1857, thought music grew out of the cadences of emotional speech. Darwin puts music first and "
                   "speech after; Spencer the reverse. <bookmark mark='e'/> Steven Mithen, in 2005, proposed a shared ancestor "
                   "of both, musical and wordless. <bookmark mark='f'/> Each tells a story; the work is to find what each "
                   "predicts.", marks="bcef")

    # ------------------------------------------------------------------
    def cheesecake(self):
        items = [
            (r"Steven Pinker \ (1997): \ music is `auditory cheesecake', \ a confection for faculties evolved for other jobs", WHITE),
            (r"language, \ hearing the scene \ (Part 45), \ emotional calls, \ motor control: \ music tickles them all", WHITE),
            (r"on this view nothing in us was selected for music itself", WHITE),
            (r"it predicts no music-specific abilities: \ every musical skill should be a borrowed one", TUNE),
            (r"amusia, \ infants' early tuning and beat-keeping are the evidence each side argues over", GREY_A),
        ]
        rows_scene(self, r"a by-product?", items,
                   "The sharpest sceptic is Steven Pinker. <bookmark mark='b'/> In 1997 he called music auditory cheesecake: a "
                   "confection made for faculties that evolved for other jobs. <bookmark mark='c'/> Language, hearing the "
                   "scene, emotional calls, motor control: music tickles them all. <bookmark mark='d'/> On this view nothing in "
                   "us was selected for music itself, <bookmark mark='e'/> so every musical skill should be a borrowed one. "
                   "<bookmark mark='f'/> Amusia, infants' early tuning, and beat-keeping are the evidence each side argues "
                   "over.", marks="bcdef")

    # ------------------------------------------------------------------
    def bonding(self):
        items = [
            (r"Savage and colleagues \ (2021): \ music and the capacities behind it coevolved to bond groups together", WHITE),
            (r"singing and moving in time build trust and cooperation, \ in groups far larger than grooming can hold", WHITE),
            (r"Mehr, \ Max Krasnow, \ Gregory Bryant and Edward Hagen \ (2021): \ music began as credible signals", WHITE),
            (r"a coordinated group display signals a coalition's strength; \ a lullaby signals a carer's attention", TUNE),
            (r"both in the same journal, \ answered by dozens of commentaries: \ the debate is open", GREY_A),
        ]
        rows_scene(self, r"two current answers", items,
                   "Two current answers appeared side by side in 2021. <bookmark mark='b'/> Savage and colleagues argued that "
                   "music and the capacities behind it coevolved to bond groups together: <bookmark mark='c'/> singing and "
                   "moving in time build trust and cooperation, in groups far larger than grooming can hold. "
                   "<bookmark mark='d'/> Mehr, Max Krasnow, Gregory Bryant and Edward Hagen argued that music began as credible "
                   "signals. <bookmark mark='e'/> A coordinated display shows a coalition's strength to outsiders; a lullaby "
                   "shows an infant its carer's attention. <bookmark mark='f'/> Both appeared in the same journal, answered by "
                   "dozens of commentaries. The debate is open.", marks="bcdef")

    # ------------------------------------------------------------------
    def table(self):
        rows_ = [
            (r"theory", r"predicts", r"evidence so far"),
            (r"courtship", r"sex differences in who makes music, \ and display", r"weak: \ lullabies and group song are everywhere"),
            (r"by-product", r"no abilities special to music", r"contested: \ amusia spares speech; \ beat-keeping is rare in animals"),
            (r"bonding", r"synchrony builds cooperation", r"lab studies: \ moving in time increases helping"),
            (r"signalling", r"forms fit their audiences", r"lullabies and dance songs recognized across cultures"),
        ]
        g = VGroup()
        for i, (a, b, c) in enumerate(rows_):
            y = 1.9 - 0.95 * i
            col = GREY_A if i == 0 else WHITE
            g.add(VGroup(label(a, font_size=19, color=TUNE if i else GREY_A).move_to([-5.0, y, 0], aligned_edge=LEFT),
                         label(b, font_size=18, color=col).move_to([-2.9, y, 0], aligned_edge=LEFT),
                         label(c, font_size=18, color=col).move_to([1.2, y, 0], aligned_edge=LEFT)))
        for r in g:
            for t in r:
                if t.width > 4.6:
                    t.set_width(4.6)
            r[1].move_to([-2.9, r[1].get_y(), 0], aligned_edge=LEFT)
            r[2].move_to([1.2, r[2].get_y(), 0], aligned_edge=LEFT)
        rule = Line([-5.1, 1.45, 0], [6.4, 1.45, 0], color=GREY_B, stroke_width=1.5)
        head = label(r"what each theory predicts", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Set them side by side by what they predict. <bookmark mark='a'/> Courtship predicts that music is mostly made "
            "by one sex, for display; but lullabies and group song are everywhere. <bookmark mark='b'/> The by-product view "
            "predicts no abilities special to music; that is contested, since amusia can spare speech and beat-keeping is "
            "rare among animals. <bookmark mark='c'/> Bonding predicts that moving in time builds cooperation, and in the "
            "lab, people who have moved in synchrony help each other more. <bookmark mark='d'/> Signalling predicts that "
            "musical forms fit their audiences, which is what the lullaby and the dance song do. The theories are not "
            "exclusive: music may serve several of these at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g[0]), FadeIn(rule), FadeIn(VGroup(*[r[0] for r in g[1:]])))
            for mark, r in zip("abcd", g[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r[1:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        items = [
            (r"our simulated singers had no musical genes, \ only noise, \ memory and a few weak biases", WHITE),
            (r"yet transmission gave their melodies discrete levels, \ small steps, \ simple lengths and repetition", WHITE),
            (r"so shared features need not mean a shared evolved design", WHITE),
            (r"but the biases themselves must come from somewhere: \ hearing, \ memory, \ the body", TUNE),
            (r"origins are a question about both: \ what we bring, \ and what passing it on does", GREY_A),
        ]
        rows_scene(self, r"what our chains add", items,
                   "This part's computations add one caution. <bookmark mark='b'/> Our simulated singers had no musical genes, noise, memory and explicit pitch-category, duration and leap biases. <bookmark mark='c'/> Those assumptions shape the discrete levels, small steps, simple lengths and repetition that emerge in simulation. <bookmark mark='d'/> So shared features need not mean a shared evolved design. <bookmark mark='e'/> But the biases themselves must come from somewhere: hearing, memory, the body. <bookmark mark='f'/> Origins are a question about both: what we bring, and what passing it on does.", marks="bcdef")
