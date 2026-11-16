from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card_section(self, 14, r"In practice: \ codecs and representations", r"Where does efficient coding earn "
                     r"money?", scale=("society",))
        self.where()
        self.levels()

    def where(self):
        chips_section(self, r"Where this is a job", [
            (r"perceptual codecs", r"JPEG quantizes fine detail coarsely, \ where the eye is least sensitive; \ "
                                   r"MP3 drops sounds that Part 15's masking hides", MODEL),
            (r"neuromorphic sensors", r"event cameras report only changes at each pixel: \ predictive coding in "
                                      r"silicon", PERSON),
            (r"representation learning", r"sparse dictionaries and autoencoders, \ now used to find "
                                         r"interpretable features inside AI models", GOOD),
            (r"display and imaging", r"tone mapping and gamma curves spend levels where people see differences", SYMP),
        ], "Where does efficient coding earn money? <bookmark mark='a'/> In perceptual codecs. JPEG quantizes fine "
           "detail coarsely, where the eye is least sensitive, and MP3 drops sounds that Part 15's masking hides. "
           "<bookmark mark='b'/> In neuromorphic sensors: event cameras report only the changes at each pixel, which "
           "is predictive coding in silicon. <bookmark mark='c'/> In representation learning: sparse dictionaries and "
           "autoencoders, now used to find interpretable features inside AI models. <bookmark mark='d'/> And in "
           "display and imaging, where tone mapping and gamma curves spend levels where people can see differences.")

    def levels(self):
        d = load("codes")
        head = heading(r"A worked example: \ twenty levels")
        A = axes([0.3, 20.7], [0, 0.28], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 0.05, 0.1, 0.2],
                 yfmt=lambda v: f"{v:g}", ylabel=r"share of responses", center=[-3.3, 0.3, 0], font_size=12)
        x = np.arange(1, 21)
        bl = bars(A.ax, x - 0.2, d["linear_use"], AUTH, width=0.38)
        bm = bars(A.ax, x + 0.2, d["matched_use"], GOOD, width=0.38)
        flat = DashedLine(A.ax.c2p(0.3, 0.05), A.ax.c2p(20.7, 0.05), color=GREY_B, stroke_width=1.5)
        xl = label(r"response level, \ low to high", font_size=13, color=GREY_A).next_to(A, DOWN, buff=0.1)
        key = VGroup(label(r"evenly spaced", font_size=13, color=AUTH),
                     label(r"matched to the world", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.2)
        gain = d["matched_bits"] / d["linear_bits"] - 1
        rows = rows_of([
            (r"a sensor with 20 output levels for local contrast in Psyche's images", WHITE),
            (r"evenly spaced levels: \ the middle few are used constantly, \ the rest rarely", AUTH),
            (rf"levels at the quantiles: \ each used about equally (one is empty, \ because many patches are "
             rf"perfectly flat); \ {d['matched_bits']:.2f} bits per reading against {d['linear_bits']:.2f}", GOOD),
            (rf"{100 * gain:.0f}\% more information from the same hardware, \ by Laughlin's rule", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"Psyche: \ the \texttt{codes} item")
        with self.voiceover(
            "Here's a worked example. <bookmark mark='a'/> A sensor has twenty output levels for local contrast in "
            "Psyche's images. <bookmark mark='b'/> With evenly spaced levels, the middle few are used constantly and "
            "the rest rarely. <bookmark mark='c'/> With levels at the quantiles of the contrast distribution, each "
            "is used about equally often. One is empty, because many patches are perfectly flat. That gives four "
            "point two bits per reading, against three point seven. <bookmark mark='d'/> That's about fourteen "
            "percent more information from the same hardware, by Laughlin's rule."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(xl), FadeIn(key), Create(flat))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bl], lag_ratio=0.05))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bm], lag_ratio=0.05))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
