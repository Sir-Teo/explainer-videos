from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (block_image, CTRL, DATA, HEAD, LAM, NO, PART, YES, load, pixel_image)


class Hook(VoiceoverScene):
    def construct(self):
        self.penguin()
        self.story()
        self.plan()

    def penguin(self):
        p = load("penguin")
        head = label(r"One cipher, \ used two ways", font_size=36).to_edge(UP, buff=0.3)
        imgs = Group(*[pixel_image(p[k], p["w"], p["h"], height=2.7) for k in ("plain", "ecb", "cbc")])
        imgs.arrange(RIGHT, buff=0.55).next_to(head, DOWN, buff=0.45)
        blk = Group(*[block_image(p[k], p["w"], p["h"], height=2.7).move_to(im) for k, im in
                      (("ecb", imgs[1]), ("cbc", imgs[2]))])
        caps = VGroup(
            label(r"our logo: \ 128 $\times$ 96 grey bytes", font_size=20, color=GREY_A),
            label(r"AES, \ each block alone \ (ECB)", font_size=20, color=NO),
            label(r"AES, \ blocks chained \ (CBC)", font_size=20, color=YES),
        )
        for c, im in zip(caps, imgs):
            c.next_to(im, DOWN, buff=0.18)
        lines = VGroup(
            label(rf"{p['blocks']} blocks of 16 bytes; \ only {p['distinct_plain']} different ones: \ equal blocks give "
                  r"equal ciphertext", font_size=22, color=WHITE),
            label(rf"chained, \ the same key gives {p['distinct_cbc']} different blocks: \ noise", font_size=22,
                  color=YES),
            label(r"paint each ciphertext block with its own first three bytes: \ equal blocks, \ equal colours",
                  font_size=22, color=WHITE),
            label(r"the cipher was not broken: \ it was \textbf{used} wrongly", font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "This is our logo: a hundred and twenty-eight by ninety-six grey pixels, one byte each. <bookmark "
            "mark='a'/> Now encrypt it with AES, the cipher that protects most of the world's traffic, with a "
            "128-bit key. Here is the ciphertext, drawn as pixels. You can still see the logo. <bookmark mark='b'/> "
            "Nothing is wrong with AES. The image was cut into seven hundred and sixty-eight blocks of sixteen bytes, "
            "and each block was encrypted on its own, the obvious way. Equal blocks of background give equal blocks "
            "of ciphertext: only eighty-five different blocks appear, exactly as many as in the picture. <bookmark "
            "mark='c'/> The same cipher with the same key, used in a mode that chains each block to the one before, "
            "gives this: every block different. <bookmark mark='d'/> To see the difference plainly, paint each "
            "sixteen-byte block of ciphertext with a colour made from its own first three bytes. Under ECB the logo "
            "is unmistakable; chained, it is confetti. <bookmark mark='e'/> A cipher is a component. "
            "Secrecy comes from how it is used, and from proving that using it that way is safe. That is this part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(imgs[0]), FadeIn(caps[0]))
            vo.wait_until("a")
            self.play(FadeIn(imgs[1]), FadeIn(caps[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(imgs[2]), FadeIn(caps[2]), FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeOut(imgs[1]), FadeIn(blk[0]), FadeOut(imgs[2]), FadeIn(blk[1]), FadeIn(lines[2]))
            vo.wait_until("e")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def story(self):
        head = label(r"Two thousand years of secrets", font_size=36).to_edge(UP, buff=0.35)
        events = [
            (r"c.\ 50 BC", r"Caesar: \\ shift by 3", GREY_B),
            (r"c.\ 850", r"al-Kindi: \\ count letters", DATA),
            (r"1553", r"Bellaso, \ Vigen\`ere: \\ many shifts", DATA),
            (r"1932--45", r"Enigma \\ broken", CTRL),
            (r"1949", r"Shannon: \\ perfect secrecy", YES),
            (r"1977", r"DES; \\ public keys", LAM),
            (r"2001", r"AES", HEAD),
        ]
        n = len(events)
        xs = [-5.8 + 11.6 * i / (n - 1) for i in range(n)]
        axis = Line([-6.2, 0.2, 0], [6.2, 0.2, 0], color=GREY_D, stroke_width=2)
        dots = VGroup(*[Dot([x, 0.2, 0], radius=0.08, color=c) for x, (_, _, c) in zip(xs, events)])
        years = VGroup(*[label(y, font_size=20, color=c).next_to(d, UP if i % 2 == 0 else DOWN, buff=0.2)
                         for i, (d, (y, _, c)) in enumerate(zip(dots, events))])
        what = VGroup(*[label(t, font_size=19, color=WHITE).next_to(yl, UP if i % 2 == 0 else DOWN, buff=0.12)
                        for i, (yl, (_, t, _)) in enumerate(zip(years, events))])
        lines = VGroup(
            label(r"for most of history, \ ciphers were broken by \textbf{counting}", font_size=23, color=DATA),
            label(r"Shannon \ (1949): \ perfect secrecy needs a key as long as the message", font_size=23, color=YES),
            label(r"modern cryptography: \ assume the attacker's computing is \textbf{limited}, \ then prove "
                  r"and attack", font_size=23, color=HEAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "For two thousand years secret writing was a contest between the people who made ciphers and the people "
            "who broke them, and the breakers usually won. <bookmark mark='a'/> Julius Caesar shifted letters. In "
            "the ninth century al-Kindi showed how to break any such cipher by counting letters. Ciphers with many "
            "shifts held out for three hundred years, and the Enigma machine for a decade, until Polish and British "
            "mathematicians broke it, again by counting. <bookmark mark='b'/> Then in 1949 Claude Shannon proved "
            "what perfect secrecy costs: a key as long as the message itself. <bookmark mark='c'/> Modern "
            "cryptography gets around his theorem with one assumption: the attacker's computing power is limited. "
            "It builds everything on that, from the Data Encryption Standard to AES, and then attacks its own "
            "constructions as hard as it can."
        ) as vo:
            self.play(FadeIn(head), Create(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(d, y, w)) for d, y, w in zip(dots[:4], years[:4], what[:4])],
                                  lag_ratio=0.5), FadeIn(lines[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(dots[4], years[4], what[4])), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(dots[5:], years[5:], what[5:])), FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Secrets", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"frequency analysis, \ Vigen\`ere, \ Enigma and Rejewski's theorem",
            r"perfect secrecy, \ and what ``secure'' means against a bounded attacker",
            r"pseudorandom generators, \ functions and permutations",
            r"AES from scratch, \ the avalanche, \ and the modes that make it safe",
            r"MACs, \ hash functions, \ Merkle trees and password hashing",
            r"attacks: \ differential, \ timing, \ bad randomness; \ the frontier",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 29 of Computer Science, Built: Secrets. <bookmark mark='a'/> In this part: the classical ciphers "
            "and how they fell, ending with Enigma; Shannon's perfect secrecy, and what security can mean when keys "
            "are short; pseudorandom generators, functions and permutations, the objects the rest is built from; AES, "
            "from scratch, on Part 28's field of bytes; the modes, message authentication codes and hash functions "
            "that make it safe to use; and the attacks: differential cryptanalysis, timing, and bad randomness."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
