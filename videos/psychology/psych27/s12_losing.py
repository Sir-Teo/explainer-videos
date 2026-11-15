from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


def matrix_img(M, col, center, width=3.2, height=1.8):
    """A binary channels-by-time matrix drawn as an image (ones coloured), in a frame."""
    M = np.asarray(M, dtype=float)
    rgb = np.array(color_to_rgb(col)) * 255
    img = np.zeros(M.shape + (3,), dtype=np.uint8)
    img[M > 0] = rgb.astype(np.uint8)
    im = ImageMobject(img)
    im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    im.stretch_to_fit_width(width)
    im.stretch_to_fit_height(height)
    frame = Rectangle(width=width, height=height, stroke_color=GREY_C, stroke_width=1.5)
    return Group(im, frame).move_to(center)


class Losing(VoiceoverScene):
    def construct(self):
        self.card()
        self.states()
        self.owen()
        self.pci_()

    def card(self):
        card = chapter_card(11, r"Losing consciousness", r"How do you tell whether someone is there?",
                            lit={2006: r"Owen et al.", 2010: r"Monti et al.", 2013: r"Casali et al.",
                                 2024: r"Bodien et al."},
                            part=PART, scale=("brain", "society"), marr=("what",))
        with self.voiceover("Chapter eleven. Losing consciousness."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def states(self):
        head = heading(r"Wakefulness and awareness")
        A = axes([0, 1], [0, 1], x_length=5.0, y_length=4.0, xticks=None, yticks=None,
                 xlabel=r"wakefulness \ (arousal)", ylabel=r"awareness \ (content)", center=[-3.4, -0.2, 0],
                 font_size=17)
        pts = [(0.92, 0.92, r"awake", SEEN), (0.75, 0.7, r"drowsy", SEEN), (0.25, 0.55, r"REM sleep: \ dreams", GNW),
               (0.2, 0.15, r"deep sleep", UNSEEN), (0.08, 0.06, r"anaesthesia, \ coma", LOST),
               (0.85, 0.12, r"vegetative state", LOST), (0.8, 0.4, r"minimally conscious", HOT)]
        dots = VGroup()
        for x, y, t, c in pts:
            dt_ = Dot(A.ax.c2p(x, y), color=c, radius=0.09)
            dots.add(VGroup(dt_, label(t, font_size=16, color=c).next_to(dt_, LEFT if x > 0.6 else RIGHT, buff=0.1)))
        rows = rows_of([
            (r"two dimensions: \ how awake the brain is, \ and whether there is experience", WHITE),
            (r"in dreaming sleep, \ awareness without wakefulness; \ in the vegetative state, \ eyes open and "
             r"sleep--wake cycles, \ with no sign of awareness", GNW),
            (r"no sign is not no awareness: \ the signs are behavioural, \ and some patients cannot move", LOST),
        ], 5.6, 22, 0.32).move_to([3.5, 0.0, 0])
        tag = published_tag(r"Laureys (2005)")
        with self.voiceover(
            "Consciousness can also be lost. <bookmark mark='a'/> It helps to separate two dimensions: how awake the "
            "brain is, and whether there is any experience. Awake, both are high; in deep sleep and anaesthesia, both "
            "fall. <bookmark mark='b'/> But they come apart. In dreaming sleep, from Part 10, there is experience with "
            "little wakefulness. In the vegetative state, now often called unresponsive wakefulness, patients open "
            "their eyes and cycle between sleep and waking, yet show no sign of awareness. <bookmark mark='c'/> No "
            "sign is not the same as no awareness. The signs are behavioural, and some patients can't move."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(dots[0]), FadeIn(dots[1]), FadeIn(dots[3]), FadeIn(dots[4]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots[2]), FadeIn(dots[5]), FadeIn(dots[6]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def owen(self):
        head = heading(r"Imagine playing tennis")
        t1 = VGroup(label(r"``imagine playing tennis''", font_size=24, color=SEEN),
                    label(r"supplementary motor area", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.15)
        t2 = VGroup(label(r"``imagine walking through your house''", font_size=24, color=GNW),
                    label(r"parahippocampal place area", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.15)
        VGroup(t1, t2).arrange(RIGHT, buff=1.0).move_to([0, 1.8, 0])
        rows = rows_of([
            (r"Owen and colleagues, \ 2006: \ a woman in a vegetative state after a road accident, \ asked in the "
             r"scanner to imagine each, \ activated the same areas as healthy volunteers", WHITE),
            (r"Monti and colleagues, \ 2010: \ 5 of 54 patients could do it; \ one answered yes-or-no questions by "
             r"choosing which to imagine", SEEN),
            (r"Bodien and colleagues, \ 2024: \ in 353 patients with brain injury across several countries, \ about a "
             r"quarter of those who could not follow commands at the bedside did so in the scanner or EEG", GNW),
            (r"cognitive--motor dissociation: \ awareness hidden behind an inability to move", MODEL),
        ], 12.0, 23, 0.34).move_to([0, -1.0, 0])
        tag = published_tag(r"Owen et al.\ (2006); \ Monti et al.\ (2010); \ Bodien et al.\ (2024)")
        with self.voiceover(
            "In 2006 Adrian Owen and colleagues found a way past the body. <bookmark mark='a'/> In the scanner, they "
            "asked a young woman diagnosed as vegetative after a road accident to imagine playing tennis, and then "
            "to imagine walking through her house. Her brain activated the same areas as healthy volunteers': the "
            "supplementary motor area for tennis, a place area for the house. <bookmark mark='b'/> In 2010 Martin "
            "Monti, Owen and colleagues tested fifty-four patients. Five could do it, and one answered yes-or-no "
            "questions by choosing which to imagine. <bookmark mark='c'/> In 2024 Yelena Bodien and colleagues "
            "tested three hundred and fifty-three patients with brain injury in several countries. About a quarter "
            "of those who couldn't follow commands at the bedside did so, by this kind of test, in the scanner or the "
            "EEG. <bookmark mark='d'/> It's called cognitive-motor dissociation: awareness hidden behind an "
            "inability to move."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(t1), FadeIn(t2))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def pci_(self):
        d = load("pci")
        head = heading(r"Zap and zip: \ the complexity index")
        kinds = [("wake", r"awake: \ spreads, \ varied", SEEN), ("sleep", r"deep sleep: \ one big wave", UNSEEN),
                 ("local", r"anaesthesia: \ stays local", LOST), ("noise", r"noise: \ not a response", GREY_B)]
        cells = Group()
        for k, t, c in kinds:
            img = matrix_img(d[f"{k}_M"], c, ORIGIN, width=2.8, height=1.6)
            cells.add(Group(img, label(t, font_size=18, color=c).next_to(img, UP, buff=0.1),
                             label(rf"PCI {d[k + '_pci']:.2f}", font_size=22, color=WHITE).next_to(img, DOWN,
                                                                                                    buff=0.12)))
        cells.arrange_in_grid(rows=2, cols=2, buff=(0.5, 0.45)).move_to([-3.3, -0.1, 0])
        rows = rows_of([
            (r"Massimini, \ Casali and colleagues: \ a magnetic pulse to the cortex, \ the EEG response recorded, \ "
             r"significant activity marked channel by channel", WHITE),
            (r"PCI: \ how compressible the response is \ (Lempel--Ziv), \ normalized: \ high when it spreads and stays "
             r"varied", MODEL),
            (rf"Casarotto and colleagues, \ 2016: \ above {d['threshold']:.2f}, \ conscious in every benchmark case; \ "
             r"some unresponsive patients score above it", GNW),
            (r"why the noise cell does not count: \ only significant responses to the pulse are kept", GREY_A),
        ], 5.6, 21, 0.3).move_to([3.5, -0.1, 0])
        tag = psyche_tag(r"\texttt{workspace.lz76}, \ \texttt{pci}, \ \texttt{responses}: \ illustrative patterns")
        with self.voiceover(
            "Can awareness be measured without any task at all? <bookmark mark='a'/> Marcello Massimini, Adenauer "
            "Casali and colleagues zap the cortex with a magnetic pulse and record the echo in the EEG, marking, "
            "channel by channel, where the response is significant. <bookmark mark='b'/> Then they zip it: the "
            "perturbational complexity index is how hard the response is to compress. It is high when the echo "
            "spreads widely and stays varied, both integrated and differentiated. Psyche's illustrative patterns show "
            "the idea: an awake-like response that spreads and varies scores high; deep sleep's single "
            "stereotyped wave and anaesthesia's local blip score low. <bookmark mark='c'/> In 2016 Silvia Casarotto "
            f"and colleagues found a threshold, {d['threshold']:.2f}, above which every benchmark case was "
            "conscious, and some unresponsive patients scored above it. <bookmark mark='d'/> And the noise cell scores "
            "highest of all, which is why only significant responses to the pulse are kept. Complexity alone is not "
            "consciousness."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells[:3]], lag_ratio=0.5), FadeIn(rows[1]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(cells[3]), FadeIn(rows[3]))
        self.clear_scene()
