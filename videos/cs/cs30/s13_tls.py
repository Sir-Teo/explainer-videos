from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, flow_box, load, mono)


class Tls(VoiceoverScene):
    def construct(self):
        self.card()
        self.handshake()
        self.schedule()

    def card(self):
        card = chapter_card(12, r"TLS 1.3", r"What happens when you open a website?", lit=(1995, 2018),
                            extra=((1995, r"SSL 2.0"), (2018, r"TLS 1.3 \ (RFC 8446)")), part=PART)
        with self.voiceover("Chapter twelve. TLS 1.3."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def handshake(self):
        t = load("tls")
        head = label(r"A handshake between two of our machines", font_size=34).to_edge(UP, buff=0.3)
        lx, rx = -4.6, 4.6
        L = label(r"client", font_size=24, color=DATA).move_to([lx, 2.5, 0])
        R = label(r"server \ (\texttt{pebble.example})", font_size=24, color=HEAD).move_to([rx, 2.5, 0])
        vl = DashedLine([lx, 2.2, 0], [lx, -2.0, 0], color=GREY_D)
        vr = DashedLine([rx, 2.2, 0], [rx, -2.0, 0], color=GREY_D)
        arrows = VGroup()
        y = 1.8
        for who, name, what, nbytes in t["messages"]:
            a, b = ([lx, y, 0], [rx, y, 0]) if who == "client" else ([rx, y, 0], [lx, y, 0])
            col = DATA if who == "client" else HEAD
            enc = name.startswith("{") or name.startswith("application")
            ar = Arrow(a, b, buff=0, stroke_width=3 if enc else 2.2, color=col, max_tip_length_to_length_ratio=0.03)
            txt = VGroup(label(rf"\texttt{{{name.replace('{', chr(92) + '{').replace('}', chr(92) + '}')}}}",
                               font_size=18, color=YES if enc else WHITE),
                         label(rf"{what} \ ({nbytes} bytes)", font_size=15, color=GREY_A)).arrange(DOWN, buff=0.04)
            txt.next_to(ar, UP, buff=0.05)
            arrows.add(VGroup(ar, txt))
            y -= 0.85
        lines = VGroup(
            label(r"one round trip, \ then encrypted data; \ braces: \ encrypted under keys from the exchange",
                  font_size=20, color=WHITE),
            label(rf"checked: \ shared secret equal \ ({'yes' if t['shared_equal'] else 'no'}), \ certificate chain \ "
                  rf"({'yes' if t['cert_ok'] else 'no'}), \ signature over the transcript \ "
                  rf"({'yes' if t['cv_ok'] else 'no'}), \ Finished MAC \ ({'yes' if t['finished_ok'] else 'no'})",
                  font_size=20, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Everything so far comes together in TLS 1.3, the protocol under HTTPS, standardised in 2018. We ran a "
            "version of it between two of our machines. <bookmark mark='a'/> The client sends a hello containing a "
            "fresh X25519 public key. <bookmark mark='b'/> The server answers with its own. Both can now compute the "
            "same shared secret, and every later message is encrypted. <bookmark mark='c'/> The server's next flight, "
            "encrypted, carries its certificate chain, a signature over everything said so far, and a MAC called "
            "Finished. The signature is what defeats chapter four's man in the middle: only the holder of the "
            "certified key could have signed this transcript. <bookmark mark='d'/> The client checks it all and sends "
            "its own Finished MAC. <bookmark mark='e'/> Then application data flows, under authenticated encryption. "
            "One round trip, and every check passed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(L), FadeIn(R), Create(vl), Create(vr))
            for mk, a in zip("abcde", arrows):
                vo.wait_until(mk)
                self.play(GrowArrow(a[0]), FadeIn(a[1]))
            self.play(FadeIn(lines))
        self.wait(0.3)
        self.clear_scene()

    def schedule(self):
        head = label(r"The key schedule, \ and forward secrecy", font_size=34).to_edge(UP, buff=0.3)
        boxes = VGroup(
            flow_box(r"X25519 shared secret", DATA, w=3.4, h=0.7, font=19),
            flow_box(r"HKDF-Extract", GREY_B, w=2.4, h=0.7, font=19),
            flow_box(r"handshake secret", HEAD, w=2.8, h=0.7, font=19),
        ).arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.7)
        outs = VGroup(*[flow_box(t, c, w=3.0, h=0.6, font=17) for t, c in
                        ((r"handshake traffic keys", HEAD), (r"Finished MAC keys", LAM),
                         (r"master secret $\to$ data keys", YES))]).arrange(DOWN, buff=0.25).next_to(boxes, DOWN,
                                                                                                    buff=0.6)
        outs.align_to(boxes[2], RIGHT)
        arr = VGroup(Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.06, stroke_width=2.5, color=GREY_B),
                     Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.06, stroke_width=2.5, color=GREY_B),
                     *[Arrow(boxes[2].get_bottom(), o.get_top(), buff=0.06, stroke_width=2, color=GREY_B)
                       for o in outs[:1]])
        lab = label(r"HKDF-Expand with labels \\ and the transcript hash", font_size=17, color=GREY_A).next_to(
            outs, LEFT, buff=0.4)
        lines = VGroup(
            label(r"HKDF \ (Krawczyk, 2010): \ HMAC turned into a key-derivation function; \ ours matches RFC 5869",
                  font_size=21, color=WHITE),
            label(r"every key is bound to the \textbf{transcript}: \ change one byte of a hello and nothing verifies",
                  font_size=21, color=HEAD),
            label(r"\textbf{forward secrecy}: \ the X25519 keys are thrown away; \ the server's long-term key only "
                  r"\textit{signs}", font_size=21, color=YES),
            label(r"steal the server's key next year: \ today's recorded traffic stays secret \ (not so with RSA key "
                  r"transport)", font_size=21, color=YES),
            label(r"TLS 1.3 also removed: \ RSA key transport, \ CBC, \ custom groups, \ compression, \ renegotiation",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Where do all those keys come from? <bookmark mark='a'/> The shared secret from the exchange goes through "
            "HKDF, a key-derivation function built from HMAC by Hugo Krawczyk; ours matches its standard's test "
            "vectors. <bookmark mark='b'/> From one secret it derives separate keys for the handshake, for the Finished "
            "MACs and for application data, each labelled, and each mixed with a hash of the transcript. So if an "
            "attacker changes a single byte of either hello, nothing verifies. <bookmark mark='c'/> The exchange keys "
            "are ephemeral, used once and discarded. The server's long-term key only signs. <bookmark mark='d'/> That "
            "is forward secrecy: an attacker who records today's traffic and steals the server's key next year still "
            "cannot read it. With the old RSA key transport, they could. <bookmark mark='e'/> TLS 1.3 also deleted "
            "most of what earlier versions got wrong: RSA key transport, CBC modes, custom groups, compression and "
            "renegotiation, all the subjects of famous attacks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes[0]))
            vo.wait_until("a")
            self.play(GrowArrow(arr[0]), FadeIn(boxes[1]), GrowArrow(arr[1]), FadeIn(boxes[2]), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arr[2]), FadeIn(outs), FadeIn(lab), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()
