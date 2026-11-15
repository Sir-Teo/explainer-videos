from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403

SIX = [(r"happiness", 0.9, 0.35), (r"sadness", -0.8, -0.4), (r"anger", -0.85, 0.55), (r"fear", -0.6, 0.85),
       (r"surprise", 0.05, 0.95), (r"disgust", -0.7, 0.1)]


class Faces(VoiceoverScene):
    def construct(self):
        self.card()
        self.darwin()
        self.fore()
        self.method()
        self.review()

    def card(self):
        card = chapter_card(3, r"Faces", r"Are there six universal emotions with six universal faces?",
                            lit={1872: r"Darwin", 1971: r"Ekman \& Friesen", 1994: r"Russell", 2014: r"Gendron et al.",
                                 2019: r"Barrett et al."},
                            part=PART, scale=("person", "culture"), marr=("what",))
        with self.voiceover("Chapter three. Faces."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def darwin(self):
        head = heading(r"Darwin's expressions")
        faces = VGroup()
        for name, v, a in SIX:
            f = face(v, a, color=FACE, radius=0.55)
            faces.add(VGroup(f, label(name, font_size=18, color=FACE).next_to(f, DOWN, buff=0.15)))
        faces.arrange_in_grid(rows=2, cols=3, buff=(0.7, 0.45)).move_to([-3.4, 0.0, 0])
        rows = rows_of([
            (r"1872: \ Charles Darwin, \ \emph{The Expression of the Emotions in Man and Animals}: \ expressions "
             r"are inherited, \ shared with other animals, \ and once served a purpose", WHITE),
            (r"he showed photographs to guests at dinner and asked what they saw: \ an early recognition test", FACE),
            (r"Paul Ekman, \ a century later: \ six basic emotions, \ each with its own face, \ recognized "
             r"everywhere", COG),
            (r"schematic faces here, \ drawn from two numbers each; \ Ekman used photographs of posed faces",
             MODEL),
        ], 5.8, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Darwin (1872); \ Ekman (1992)")
        with self.voiceover(
            "If emotions are built into the body, perhaps they are built into the face. <bookmark mark='a'/> In 1872 "
            "Charles Darwin published The Expression of the Emotions in Man and Animals. He argued that expressions "
            "are inherited, shared in part with other animals, and once served a purpose: widened eyes take in more, "
            "a wrinkled nose shuts out a smell. <bookmark mark='b'/> He even showed photographs of faces to guests "
            "at dinner and asked what they saw, one of the first recognition tests. <bookmark mark='c'/> A century "
            "later Paul Ekman made the claim precise: six basic emotions, happiness, sadness, anger, fear, surprise "
            "and disgust, each with its own facial configuration, recognized everywhere. <bookmark mark='d'/> The "
            "faces drawn here are schematic, built from two numbers each; Ekman used photographs of posed faces."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(f) for f in faces], lag_ratio=0.2))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def fore(self):
        head = heading(r"New Guinea, \ the late 1960s")
        story = RoundedRectangle(corner_radius=0.12, width=5.6, height=1.3, color=COG, fill_opacity=0.08).move_to(
            [-3.4, 1.4, 0])
        st = wrapped_label(r"``His friend has come, \ and he is happy.''", 5.0, 22, COG).move_to(story)
        three = VGroup(*[face(v, a, color=FACE, radius=0.5) for v, a in ((0.9, 0.35), (-0.8, -0.4), (-0.6, 0.85))])
        three.arrange(RIGHT, buff=0.7).move_to([-3.4, -0.6, 0])
        pick = SurroundingRectangle(three[0], color=PLEAS, buff=0.12)
        rows = rows_of([
            (r"Ekman and Wallace Friesen, \ 1971: \ the Fore of New Guinea, \ with little contact with outsiders "
             r"or their media", WHITE),
            (r"a story is told; \ the listener picks the face that fits, \ from two or three photographs", COG),
            (r"matching was far above chance for most emotions; \ fear and surprise were often confused", PLEAS),
            (r"the Fore's own posed expressions were recognized by Americans, \ above chance", FACE),
        ], 5.8, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Ekman \& Friesen (1971)")
        with self.voiceover(
            "The strongest evidence came from people who had never seen Western faces on screen. "
            "<bookmark mark='a'/> Ekman and Wallace Friesen worked with the Fore people of New Guinea, who had "
            "little contact with outsiders or their media. <bookmark mark='b'/> A short story was told through an "
            "interpreter: his friend has come, and he is happy. The listener chose the face that fitted from two or "
            "three photographs. <bookmark mark='c'/> Matching was far above chance for most emotions, though fear "
            "and surprise were often confused. <bookmark mark='d'/> And when Fore people posed expressions, "
            "Americans recognized them above chance too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(story), FadeIn(st), FadeIn(three))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(pick))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def method(self):
        head = heading(r"What the method adds")
        forced = VGroup(label(r"forced choice", font_size=24, color=COG),
                        wrapped_label(r"one face, \ six words: \ which is it?", 4.6, 21, WHITE)).arrange(DOWN, buff=0.2)
        free = VGroup(label(r"free response", font_size=24, color=FACE),
                      wrapped_label(r"one face: \ what is this person feeling? \ or sort the faces into piles, \ "
                                    r"no words given", 4.6, 21, WHITE)).arrange(DOWN, buff=0.2)
        VGroup(forced, free).arrange(RIGHT, buff=1.2).move_to([0, 1.5, 0])
        rows = rows_of([
            (r"James Russell, \ 1994: \ forced choice among a few labels inflates agreement; \ by elimination, "
             r"\ a face that is not happy is narrowed to five", COG),
            (r"Maria Gendron and colleagues, \ 2014: \ Himba villagers in Namibia, \ sorting 36 faces freely, \ "
             r"did not make the six piles; \ given emotion words, \ they came closer", FACE),
            (r"agreement is real, \ and above chance; \ how much of it is in the face, \ and how much in the task, "
             r"\ is the question", WHITE),
        ], 12.2, 24, 0.38).move_to([0, -1.5, 0])
        tag = published_tag(r"Russell (1994); \ Gendron et al.\ (2014)")
        with self.voiceover(
            "Then critics looked at the method. <bookmark mark='a'/> Most studies used forced choice: one face, six "
            "words, which is it? The alternative is free response: what is this person feeling? Or sort the faces "
            "into piles, with no words given. <bookmark mark='b'/> James Russell argued in 1994 that forced choice "
            "inflates agreement, partly by elimination: a face that is obviously not happy has only five words "
            "left. <bookmark mark='c'/> In 2014 Maria Gendron and colleagues asked Himba villagers in Namibia to "
            "sort thirty-six faces freely. They did not make the six piles; given emotion words, they came closer. "
            "<bookmark mark='d'/> The agreement is real, and above chance. How much of it is in the face, and how "
            "much in the task, is the question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(forced), FadeIn(free))
            for m, r in zip("bcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def review(self):
        head = heading(r"Faces in the wild")
        A = axes([0, 1], [0, 1], x_length=5.0, y_length=3.0, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", ylabel=r"share of angry episodes", center=[-3.6, -0.4, 0], font_size=16)
        b1 = bars(A.ax, [0.3], [0.25], FACE, width=0.3)
        b2 = bars(A.ax, [0.7], [0.75], GREY_B, width=0.3)
        l1 = wrapped_label(r"with a scowl", 1.6, 17, FACE).next_to(A.ax.c2p(0.3, 0), DOWN, buff=0.15)
        l2 = wrapped_label(r"with other faces", 1.6, 17, GREY_B).next_to(A.ax.c2p(0.7, 0), DOWN, buff=0.15)
        rows = rows_of([
            (r"Barrett, \ Adolphs, \ Marsella, \ Martinez and Pollak, \ 2019: \ four tests for a face that "
             r"signals an emotion: \ reliability, \ specificity, \ generalizability, \ validity", WHITE),
            (r"reliability: \ people scowl when angry about a quarter of the time", FACE),
            (r"specificity: \ people also scowl when concentrating, \ confused, \ or in bright sun", COG),
            (r"their conclusion: \ facial movements are not reliable or specific readouts of emotion, \ "
             r"whatever their role in communication", UNPL),
        ], 5.8, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Barrett et al.\ (2019)")
        with self.voiceover(
            "In 2019 a review settled what can be settled. <bookmark mark='a'/> Lisa Feldman Barrett, Ralph "
            "Adolphs, Stacy Marsella, Aleix Martinez and Seth Pollak set four tests for a face that signals an "
            "emotion: reliability, specificity, generalizability, and validity. <bookmark mark='b'/> On "
            "reliability: in studies of people actually feeling anger, they scowl about a quarter of the time. "
            "<bookmark mark='c'/> On specificity: people also scowl when concentrating, confused, or squinting in "
            "bright sun. <bookmark mark='d'/> Their conclusion: facial movements are not reliable or specific "
            "readouts of emotion, whatever role they play in communication. That conclusion matters for software "
            "that claims to read emotions from faces, in chapter fourteen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(b1), FadeIn(b2), FadeIn(l1), FadeIn(l2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
