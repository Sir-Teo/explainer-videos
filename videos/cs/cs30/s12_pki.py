from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, flow_box, load, mono)


class Pki(VoiceoverScene):
    def construct(self):
        self.card()
        self.chain()
        self.transparency()

    def card(self):
        card = chapter_card(11, r"Certificates and trust", r"Whose public key is this?", lit=(1988, 2011, 2013),
                            extra=((1988, r"X.509"), (2011, r"DigiNotar"), (2013, r"Certificate Transparency"),
                                   (2015, r"Let's Encrypt")), part=PART)
        with self.voiceover("Chapter eleven. Certificates, and trust."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def chain(self):
        k = load("pki")
        head = label(r"A chain of signatures", font_size=34).to_edge(UP, buff=0.3)
        names = k["chain"]
        boxes = VGroup(*[flow_box(rf"\texttt{{{n}}}", c, w=4.6, h=0.8, font=20) for n, c in
                         zip(names, (YES, HEAD, DATA))]).arrange(UP, buff=0.8).next_to(head, DOWN, buff=0.5).to_edge(
            LEFT, buff=1.2)
        tags = VGroup(label(r"leaf: \ the website's key", font_size=18, color=YES),
                      label(r"intermediate CA", font_size=18, color=HEAD),
                      label(r"root CA: \ built into the browser", font_size=18, color=DATA))
        for t, b in zip(tags, boxes):
            t.next_to(b, RIGHT, buff=0.3)
        arrows = VGroup(*[Arrow(boxes[i + 1].get_bottom(), boxes[i].get_top(), buff=0.06, stroke_width=2.5,
                                color=GREY_B) for i in range(2)])
        sl = VGroup(*[label(r"signs", font_size=16, color=GREY_A).next_to(a, LEFT, buff=0.1) for a in arrows])
        checks = VGroup(
            label(rf"the chain verifies: \ {'yes' if k['ok'] else 'no'}", font_size=22, color=YES),
            label(rf"change the leaf's name: \ {'yes' if k['tampered'] else 'rejected'}", font_size=22, color=NO),
            label(rf"a self-made certificate for the same name: \ {'yes' if k['self_signed'] else 'rejected'}",
                  font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=1.1)
        note = label(r"a certificate: \ ``this public key belongs to this name'', \ signed by someone you already "
                     r"trust", font_size=21, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A signature tells you which key signed. It does not tell you whose key that is. <bookmark mark='a'/> A "
            "certificate binds a name to a public key, and is signed by a certificate authority. Here the website "
            "pebble dot example has a key, certified by an intermediate authority, which is certified in turn by a "
            "root authority. <bookmark mark='b'/> The root's key is not certified by anyone: it ships inside your "
            "browser or operating system, in a list of about a hundred and fifty root certificates. <bookmark mark='c'/> Our "
            "chain, signed with our ECDSA, verifies. Change one character of the website's name and the signature "
            "fails. A certificate the attacker signs with their own key fails too, because no trusted root vouches "
            "for it. <bookmark mark='d'/> So trust is delegated: you trust the roots, the roots trust the "
            "intermediates, and they vouch for websites."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]), FadeIn(tags[0]))
            self.play(FadeIn(boxes[1]), FadeIn(tags[1]), GrowArrow(arrows[0]), FadeIn(sl[0]))
            vo.wait_until("b")
            self.play(FadeIn(boxes[2]), FadeIn(tags[2]), GrowArrow(arrows[1]), FadeIn(sl[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in checks], lag_ratio=0.5))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def transparency(self):
        head = label(r"When authorities fail", font_size=34).to_edge(UP, buff=0.3)
        lines = VGroup(
            label(r"any of $\sim$150 roots can certify \textbf{any} name: \ the weakest one sets the security of all",
                  font_size=22, color=NO),
            label(r"2011: \ DigiNotar, \ a Dutch CA, \ was hacked; \ fake certificates for \texttt{google.com} were "
                  r"used against users in Iran", font_size=22, color=NO),
            label(r"\textbf{Certificate Transparency} \ (Laurie and Langley, 2013): \ every certificate goes into "
                  r"public, \ append-only logs", font_size=22, color=YES),
            label(r"the logs are Merkle trees \ (Part 29): \ a short proof shows a certificate is in, \ and that the "
                  r"log only grew", font_size=22, color=HEAD),
            label(r"browsers reject certificates without log receipts \ (Chrome, 2018): \ misissuance is now "
                  r"\textit{visible}", font_size=22, color=DATA),
            label(r"Let's Encrypt \ (2015): \ free, \ automated certificates; \ most of the web is HTTPS since",
                  font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "The weakness of this system is its breadth. <bookmark mark='a'/> Any trusted root can certify any name, so "
            "the least careful authority sets the security of every website. <bookmark mark='b'/> In 2011 the Dutch "
            "authority DigiNotar was broken into, and certificates for google dot com, signed by a trusted root, were "
            "used to intercept users in Iran. DigiNotar was removed from every browser and went bankrupt. <bookmark "
            "mark='c'/> The response, from Ben Laurie and Adam Langley at Google, was Certificate Transparency: every "
            "certificate must be recorded in public, append-only logs. <bookmark mark='d'/> The logs are Part 29's "
            "Merkle trees. A short proof shows that a certificate is in the log, and another that the log has only ever "
            "grown, never been rewritten. <bookmark mark='e'/> Since 2018 Chrome rejects certificates that cannot prove "
            "they were logged, so a misissued certificate can no longer be used in secret. <bookmark mark='f'/> And "
            "since Let's Encrypt began issuing free, automated certificates in 2015, most of the web has moved to "
            "HTTPS."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
