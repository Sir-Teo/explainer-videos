from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403


class Reading(VoiceoverScene):
    def construct(self):
        card_section(self, 10, r"Learning to read", r"Why did the reading wars end?", scale=("person", "society"))
        self.simple()
        self.wars()

    def simple(self):
        d = load("reading")
        head = heading(r"The simple view of reading")
        eq = MathTex(r"\text{reading comprehension} = \text{decoding} \times \text{language comprehension}",
                     font_size=30).move_to([0, 2.2, 0])
        A = axes([0, 1], [0, 1], x_length=3.8, y_length=3.4, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"decoding", ylabel=r"language comprehension",
                 center=[-3.9, -0.6, 0], font_size=12)
        rc = np.clip(np.asarray(d["rc"]), 0, 1)
        cols = [interpolate_color(ManimColor(AUTH), ManimColor(GOOD), float(v)) for v in rc]
        pts = VGroup(*[Dot(A.ax.c2p(float(x), float(y)), radius=0.035, color=c) for x, y, c in
                       zip(d["dec"], d["lc"], cols)])
        rows = rows_of([
            (r"Gough and Tunmer, \ 1986: \ reading comprehension is the product of decoding words and understanding "
             r"language; \ if either is zero, \ so is reading", WHITE),
            (rf"400 simulated children, \ coloured by comprehension: \ good listeners who cannot decode read about as "
             rf"poorly ({d['rc_low_dec']:.2f}) as good decoders who do not understand ({d['rc_low_lc']:.2f})", MODEL),
            (r"two different problems, \ needing two different kinds of teaching: \ phonics for one, \ vocabulary and "
             r"knowledge for the other", PERSON),
        ], 6.4, 19, 0.38).move_to([3.2, -0.7, 0])
        tag = psyche_tag(r"\texttt{work.simple\_view}, \ 400 simulated children")
        with self.voiceover(
            "Why did the reading wars end? Start with a model. <bookmark mark='a'/> In 1986 Philip Gough and William "
            "Tunmer proposed that reading comprehension is the product of decoding words and understanding language. "
            "If either is zero, so is reading. <bookmark mark='b'/> Here are four hundred simulated children, coloured "
            "by comprehension. Good listeners who can't decode read about as poorly as good decoders who don't "
            "understand. <bookmark mark='c'/> Those are two different problems, needing two different kinds of "
            "teaching: phonics for one, and vocabulary and knowledge for the other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eq), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(pts))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def wars(self):
        rows_section(self, r"The reading wars", [
            (r"for decades, \ ``whole language'' teaching held that children learn to read as they learn to talk, \ "
             r"from meaning and context", WHITE),
            (r"the evidence: \ English spelling maps to sounds systematically enough that explicit, \ systematic "
             r"phonics helps beginners, \ most of all those at risk (the US National Reading Panel, \ 2000)", GOOD),
            (r"guessing words from pictures and context, \ taught as a strategy, \ trains what skilled readers do "
             r"not do: \ Part 18's eye movements land on nearly every word", AUTH),
            (r"Castles, \ Rastle and Nation, \ 2018: \ phonics first, \ then fluency, \ vocabulary and knowledge; \ "
             r"decoding is necessary, \ not sufficient", MODEL),
        ], "For decades, the reading wars were fought between two views. <bookmark mark='a'/> Whole-language teaching "
           "held that children learn to read as they learn to talk, from meaning and context. <bookmark mark='b'/> "
           "The evidence says English spelling maps to sounds systematically enough that explicit, systematic phonics "
           "helps beginners, most of all those at risk. The US National Reading Panel concluded so in 2000. "
           "<bookmark mark='c'/> Guessing words from pictures and context, taught as a strategy, trains what skilled "
           "readers don't do. Part 18's eye movements land on nearly every word. <bookmark mark='d'/> Anne Castles, "
           "Kathleen Rastle and Kate Nation summed it up in 2018: phonics first, then fluency, vocabulary and "
           "knowledge. Decoding is necessary, and not sufficient.", tag=published_tag(r"Castles, \ Rastle \& Nation "
                                                                                       r"(2018)"))
