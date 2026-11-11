from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.capacity()
        self.local()
        self.good()
        self.open_()

    def card(self):
        card = chapter_card(14, r"Frontier: \ capacity and locality", r"What is still unknown about codes?",
                            lit=(2008, 2023), extra=((2008, r"Guruswami--Rudra"), (2021, r"c$^3$-LTCs; \ good qLDPC"),
                                                     (2023, r"Reed--Muller")), part=PART)
        with self.voiceover("Chapter fourteen. The frontier: capacity and locality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def capacity(self):
        head = label(r"Old codes, \ new theorems", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"\textbf{Reed--Muller codes} \ (1954): \ evaluations of low-degree polynomials in many variables",
                  font_size=22, color=WHITE),
            label(r"do they reach capacity? \ On erasure channels: \ yes \ (Kudekar et al., 2016, \ by symmetry and "
                  r"sharp thresholds)", font_size=22, color=DATA),
            label(r"on every binary symmetric channel: \ yes \ (Abbe and Sandon, 2023) \ --- seventy years after the "
                  r"codes", font_size=22, color=YES),
            label(r"\textbf{list decoding}: \ return a short list of candidates instead of one \ (Elias, \ Wozencraft, "
                  r"1957)", font_size=22, color=HEAD),
            label(r"Sudan \ (1997), \ Guruswami--Sudan: \ Reed--Solomon codes list-decode far beyond half their "
                  r"distance", font_size=22, color=HEAD),
            label(r"Guruswami and Rudra \ (2008): \ \textbf{folded} RS codes correct a $1 - R - \varepsilon$ "
                  r"fraction of errors: \ optimal", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Some of the newest results are about the oldest codes. <bookmark mark='a'/> Reed-Muller codes, from "
            "1954, evaluate low-degree polynomials in many variables. <bookmark mark='b'/> Do they reach Shannon's "
            "capacity? On erasure channels, Shrinivas Kudekar and coauthors proved yes in 2016, using only the "
            "codes' symmetry. <bookmark mark='c'/> For every binary symmetric channel, Emmanuel Abbe and Colin "
            "Sandon proved it in 2023, nearly seventy years after the codes were invented. <bookmark mark='d'/> "
            "Another idea: when there are too many errors to decode uniquely, return a short list of candidates. "
            "<bookmark mark='e'/> Madhu Sudan showed in 1997 that Reed-Solomon codes can be list-decoded well past "
            "half their distance. <bookmark mark='f'/> And Venkatesan Guruswami and Atri Rudra found folded "
            "Reed-Solomon codes that correct a fraction of errors approaching one minus the rate: the best "
            "possible."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def local(self):
        d = load("local")
        head = label(r"Reading one bit from a damaged codeword", font_size=34).to_edge(UP, buff=0.35)
        rows = [[f"{r['delta'] * 100:g}\\%", f"{r['one'] * 100:.1f}\\%", f"{r['bound'] * 100:.0f}\\%",
                 f"{r['maj15'] * 100:.1f}\\%"] for r in d["rows"]]
        tab = grid_table([r"corrupted", r"2 queries", r"bound $1 - 2\delta$", r"30 queries, \ majority"], rows,
                         widths=[2.4, 2.6, 3.0, 3.6], row_h=0.42, font_size=21, mono_cols=(),
                         colors=[[NO, YES, GREY_A, DATA]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        tl = label(rf"the Hadamard code of a {d['k']}-bit message: \ all {d['n']:,} parities; \ 3,000 trials per row"
                   .replace(",", "{,}"), font_size=18, color=GREY_A).next_to(tab, DOWN, buff=0.12)
        lines = VGroup(
            label(r"to learn bit $i$: \ read positions $a$ and $a \oplus e_i$ for a random $a$; \ their XOR is $x_i$, "
                  r"unless one is corrupted", font_size=21, color=WHITE),
            label(r"each query is uniformly random, \ so each lands on damage with probability $\delta$: \ success "
                  r"$\ge 1 - 2\delta$", font_size=21, color=YES),
            label(r"a \textbf{locally decodable code}: \ any bit from a constant number of reads, \ the cousin of "
                  r"Part 27's linearity test", font_size=21, color=HEAD),
            label(r"the price: \ length $2^k$ for $k$ bits. \ binary 2-query codes need exponential length; \\ 3-query bounds have "
                  r"large gaps", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.22).next_to(tl, DOWN, buff=0.35)
        with self.voiceover(
            "Sometimes you need one bit of a huge encoded file, not all of it. <bookmark mark='a'/> The Hadamard code "
            "stores every parity of the message. To learn bit i, read the codeword at a random position a and at a "
            "with bit i flipped; their exclusive or is the bit. <bookmark mark='b'/> Each of the two reads lands on a "
            "uniformly random position, so if a fraction delta is corrupted, the answer is right with probability "
            "at least one minus two delta. Our measurements sit just above that line, and a majority over fifteen "
            "pairs is nearly always right. <bookmark mark='c'/> This is a locally decodable code, the cousin of "
            "Part 27's linearity test. <bookmark mark='d'/> The price is length: two to the k positions for k bits. "
            "Binary two-query codes require exponential length for constant noise and success guarantees. For three queries, the optimal length is still open, with large gaps "
            "between the bounds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(tl))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def good(self):
        head = label(r"2021--22: \ good codes that are also local", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"a \textbf{locally testable} code: \ a few random reads tell a codeword from a word far from all "
                  r"codewords", font_size=22, color=WHITE),
            label(r"wanted for decades: \ constant rate, \ constant relative distance, \ \textbf{and} constant "
                  r"queries \ (``c$^3$'')", font_size=22, color=GREY_A),
            label(r"Dinur, \ Evra, \ Livne, \ Lubotzky, \ Mozes \ (2021), \ and Panteleev and Kalachev: \ built, \ "
                  r"from high-dimensional expanders", font_size=22, color=YES),
            label(r"the same ideas gave \textbf{good quantum LDPC codes} \ (Panteleev and Kalachev, 2021): \ a "
                  r"20-year question", font_size=22, color=DATA),
            label(r"quantum computers need codes to survive at all \ (Part 53): \ the surface code, \ and now "
                  r"these", font_size=22, color=LAM),
            label(r"and back to Part 27: \ PCPs are built from locally testable codes", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Two linked breakthroughs came in 2021. <bookmark mark='a'/> A locally testable code lets you check, by "
            "reading a few random symbols, whether a word is a codeword or far from every codeword. <bookmark "
            "mark='b'/> For decades nobody knew whether such codes could also have constant rate and constant "
            "relative distance, the c-cubed codes. <bookmark mark='c'/> Irit Dinur, Shai Evra, Ron Livne, "
            "Alexander Lubotzky and Shahar Mozes built them, and so, independently, did Pavel Panteleev and Gleb "
            "Kalachev, using high-dimensional expanders. <bookmark mark='d'/> Panteleev and Kalachev's construction "
            "also gave the first good quantum LDPC codes, answering a twenty-year-old question. <bookmark mark='e'/> "
            "Quantum computers cannot work at all without error correction, as Part 53 shows. <bookmark mark='f'/> "
            "And locally testable codes are what the PCP theorems of Part 27 are made of."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open problems", font_size=34).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"1. \ Do long binary codes exist above the Gilbert--Varshamov bound?", font_size=22, color=WHITE),
            label(r"2. \ Close the gap between GV and the linear-programming bound", font_size=22, color=WHITE),
            label(r"3. \ Explicit binary codes that reach the GV bound at all", font_size=22, color=WHITE),
            label(r"4. \ How short can a 3-query locally decodable code be?", font_size=22, color=WHITE),
            label(r"5. \ Fast decoders that reach capacity at \textbf{short} lengths \ (hundreds of bits)",
                  font_size=22, color=WHITE),
            label(r"6. \ Do Reed--Muller codes reach capacity under \textbf{efficient} decoding?", font_size=22,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5)
        star = label(r"$\bigstar$ \ the part's research problem takes a small case of the fifth", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Six open problems. <bookmark mark='a'/> Whether any long binary codes beat the random ones of Gilbert "
            "and Varshamov. <bookmark mark='b'/> Where, between that bound and the linear-programming bound, the "
            "truth lies. <bookmark mark='c'/> Whether any explicit construction even matches random codes. "
            "<bookmark mark='d'/> How short a locally decodable code that reads three symbols can be. <bookmark "
            "mark='e'/> How close to capacity fast decoders can get at short lengths, which matter for control "
            "messages and the internet of things. <bookmark mark='f'/> And whether Reed-Muller codes reach capacity "
            "with an efficient decoder, not just in principle. <bookmark mark='g'/> This part's research problem "
            "takes a small, computable case of the fifth."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcdef", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
