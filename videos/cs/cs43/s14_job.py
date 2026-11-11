from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def service(name, color, w=2.6, h=1.0):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color, stroke_width=2, fill_color=BG,
                         fill_opacity=1)
    return VGroup(r, label(name, font_size=24, color=color).move_to(r))


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.flow()
        self.drift()
        self.keys()
        self.end_to_end()

    def card(self):
        card = chapter_card(13, r"The Job as three services", r"Can counts stay exact on a network that lies?",
                            lit=(1981, 1984), extra=((1981, r"TCP's sequence numbers"),
                                                     (1984, r"the end-to-end argument")), part=PART)
        with self.voiceover("Chapter thirteen. The Job as three services."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def flow(self):
        w = load("job")["with_keys"]
        head = label(r"Messages on a bad network", font_size=36).to_edge(UP, buff=0.3)
        tok = service(r"tokenize", DATA).move_to([-4.6, 1.0, 0])
        cnt = service(r"count", HEAD).move_to([0.6, 1.0, 0])
        rnk = service(r"rank", YES).move_to([5.0, 1.0, 0])
        link2 = Arrow(cnt.get_right(), rnk.get_left(), buff=0.1, color=GREY_B, stroke_width=2)
        rng = random.Random(7)
        dots, fates = VGroup(), []
        for k in range(14):
            fate = "lost" if k in (3, 9) else ("dup" if k == 6 else "ok")
            fates.append(fate)
            dots.add(Dot(radius=0.09, color=DATA).move_to(tok.get_right() + RIGHT * 0.15 + UP * rng.uniform(-0.3,
                                                                                                         0.3)))
        stats = VGroup(*[label(t, font_size=21, color=c) for t, c in (
            (rf"{w['words']:,} words in {w['chunks']} chunks of counts", WHITE),
            (rf"{w['messages']} messages sent, \ counting retries and acknowledgements", GREY_A),
            (rf"{w['lost']} lost, \ {w['duplicated']} duplicated, \ {w['rounds']} rounds of retries", NO))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -1.6, 0])
        x_marks = VGroup()
        with self.voiceover(
            "Here is the Job split across a network. <bookmark mark='a'/> The tokenizer reads the first "
            f"{w['words']:,} words of our thirty novels and sends the counter one message per chunk of two hundred "
            "words, each message carrying that chunk's word counts. The counter adds them up, and the ranker asks "
            "it for the top words. <bookmark mark='b'/> Our simulated network loses five percent of messages, "
            "acknowledgements included, and duplicates two percent. <bookmark mark='c'/> So the tokenizer retries "
            "every chunk until it is acknowledged. That took three rounds and, counting retries and "
            f"acknowledgements, {w['messages']} messages. {w['lost']} were lost and {w['duplicated']} were "
            "duplicated."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tok), FadeIn(cnt), FadeIn(rnk), GrowArrow(link2))
            vo.wait_until("a")
            self.play(FadeIn(stats[0]))
            vo.wait_until("b")
            anims = []
            for d, fate in zip(dots, fates):
                if fate == "lost":
                    mid = (tok.get_right() + cnt.get_left()) / 2 + DOWN * rng.uniform(-0.2, 0.2)
                    anims.append(Succession(FadeIn(d), d.animate.move_to(mid).set_color(NO), FadeOut(d)))
                    x_marks.add(Cross(scale_factor=0.12, stroke_color=NO).move_to(mid))
                else:
                    anims.append(Succession(FadeIn(d), d.animate.move_to(cnt.get_left() + LEFT * 0.12)))
            self.play(LaggedStart(*anims, lag_ratio=0.18), run_time=4)
            self.play(FadeIn(x_marks))
            dup = dots[6].copy().set_color(HEAD)
            self.play(dup.animate.shift(UP * 0.35), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(stats[1]), FadeIn(stats[2]))
        self.wait(0.4)
        self.clear_scene()

    def drift(self):
        sw = load("job")["sweep"]
        head = label(r"Without keys, \ counts drift", font_size=36).to_edge(UP, buff=0.3)
        x0, y0, xw, yh = -5.2, -2.4, 7.0, 4.4
        ymax = 3000
        ax = VGroup(Line([x0, y0, 0], [x0 + xw, y0, 0], color=GREY_C), Line([x0, y0, 0], [x0, y0 + yh, 0],
                                                                              color=GREY_C))

        def pt(i, v):
            return [x0 + i / (len(sw) - 1) * xw, y0 + v / ymax * yh, 0]
        ticks = VGroup()
        for i, r in enumerate(sw):
            ticks.add(label(rf"{100 * r['loss']:.0f}\% / {100 * r['dup']:.0f}\%", font_size=16,
                            color=GREY_B).move_to([pt(i, 0)[0], y0 - 0.3, 0]))
        for v in (0, 1000, 2000, 3000):
            ticks.add(label(f"{v:,}", font_size=16, color=GREY_B).move_to([x0 - 0.45, pt(0, v)[1], 0]))
        xl = label(r"messages lost / duplicated", font_size=17, color=GREY_B).next_to(ax[0], DOWN, buff=0.55)
        yl = label(r"words with a wrong count \ (of 5,882)", font_size=17, color=GREY_B).next_to(ax[1], UP,
                                                                                               buff=0.12)
        bad = VMobject(color=NO, stroke_width=3).set_points_as_corners([pt(i, r["without_wrong"])
                                                                        for i, r in enumerate(sw)])
        good = VMobject(color=YES, stroke_width=3).set_points_as_corners([pt(i, r["with_keys_wrong"])
                                                                          for i, r in enumerate(sw)])
        bl = label(r"retries, \ no keys", font_size=19, color=NO).next_to(bad.get_end(), UP, buff=0.15)
        gl = label(r"retries + idempotency keys: \ 0", font_size=19, color=YES).next_to(good.get_end(), UP,
                                                                                       buff=0.15).shift(LEFT * 1.0)
        side = VGroup(
            wrapped_label(rf"at 20\% loss: \ {sw[-1]['without_wrong']:,} words wrong, \ "
                          rf"{sw[-1]['without_over']:,} counts too many", 3.6, font_size=19, color=NO),
            wrapped_label(r"every error is an over-count: \ retries never lose data, \ they repeat it", 3.6,
                          font_size=19, color=HEAD),
            wrapped_label(rf"with keys, \ exact at every rate; \ only the message count grows \ "
                          rf"({sw[0]['messages']} to {sw[-1]['messages']})", 3.6, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Now vary the network. <bookmark mark='a'/> On a perfect network, retries never happen and both "
            "versions are exact. As the network gets worse, the counter without protection counts more and more "
            f"words wrongly: at twenty percent loss and ten percent duplication, {sw[-1]['without_wrong']:,} of the "
            f"five thousand eight hundred and eighty-two words are wrong, {sw[-1]['without_over']:,} counts too "
            "many in all. <bookmark mark='b'/> Every error is an over-count. Retrying never loses data; it repeats "
            "it. <bookmark mark='c'/> With idempotency keys the counts are exact at every rate. The only price is "
            f"traffic: the messages grow from {sw[0]['messages']} to {sw[-1]['messages']} as the network worsens."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(bad), run_time=2)
            self.play(FadeIn(bl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(good), FadeIn(gl), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def keys(self):
        w = load("job")["with_keys"]
        head = label(r"What the counter remembers", font_size=36).to_edge(UP, buff=0.3)
        msg = VGroup(RoundedRectangle(width=4.4, height=1.1, corner_radius=0.1, stroke_color=DATA, fill_color=BG,
                                      fill_opacity=1))
        mt = VGroup(label(r"key: \ \texttt{tokenizer-1/chunk-117}", font_size=19, color=HEAD),
                    label(r"counts: \ \texttt{the 12, whale 3, sea 2, ...}", font_size=19, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to(msg[0])
        msg.add(mt)
        msg.move_to([-4.0, 1.3, 0])
        table = VGroup(*[label(rf"\texttt{{chunk-{k}}}", font_size=17, color=GREY_A) for k in (114, 115, 116, 117)])
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        tframe = SurroundingRectangle(table, color=HEAD, buff=0.2)
        tl = label(r"keys already applied", font_size=18, color=HEAD).next_to(tframe, UP, buff=0.1)
        store = VGroup(tframe, table, tl).move_to([1.8, 1.2, 0])
        check = label(r"seen? \ skip, \ but acknowledge again", font_size=20, color=YES).next_to(store, RIGHT,
                                                                                               buff=0.3)
        if check.get_right()[0] > 6.9:
            check.next_to(store, DOWN, buff=0.25)
        lines = VGroup(
            wrapped_label(rf"one key per chunk: \ {w['chunks']} keys for the whole run; \ applied atomically with "
                          r"the counts, \ or a crash between them breaks the guarantee", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"forgetting: \ keep keys as long as a retry can arrive \ (a time to live), \ or give each "
                          r"sender a sequence number and keep only the highest applied, \ as TCP does \ (Part 37)",
                          12.4, font_size=20, color=LAM),
            wrapped_label(r"in industry: \ payment APIs take an \texttt{Idempotency-Key} header; \ Kafka's "
                          r"idempotent producers number their messages \ (2017)", 12.4, font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "What did the fix cost? <bookmark mark='a'/> Each message carries a key that names it: which "
            "tokenizer, which chunk. <bookmark mark='b'/> The counter keeps the set of keys it has applied. A "
            "message whose key it has seen is skipped, but acknowledged again, because the first acknowledgement "
            "may be the one that was lost. <bookmark mark='c'/> Here that is one key per chunk, "
            f"{w['chunks']} in all, and the key must be recorded in the same transaction as the counts, or a crash "
            "between the two breaks the guarantee. <bookmark mark='d'/> Keys cannot be kept for ever. Either keep "
            "each for as long as a retry might still arrive, or give each sender a sequence number and keep only "
            "the highest one applied, as TCP does with bytes. <bookmark mark='e'/> This is what industry does: "
            "payment APIs accept an idempotency key with every request, and since 2017 Kafka's producers number "
            "their messages so that brokers can drop duplicates."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(msg))
            vo.wait_until("b")
            self.play(FadeIn(store))
            self.play(Indicate(table[-1], color=HEAD), FadeIn(check))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def end_to_end(self):
        head = label(r"The end-to-end argument", font_size=36).to_edge(UP, buff=0.3)
        layers = [(r"application: \ apply each key once", YES), (r"transport: \ TCP, \ exactly-once bytes", DATA),
                  (r"network: \ loses, \ duplicates, \ reorders", NO)]
        stack = VGroup()
        for t, c in layers:
            r = Rectangle(width=6.2, height=0.8, stroke_color=c, stroke_width=2, fill_color=BG, fill_opacity=1)
            stack.add(VGroup(r, label(t, font_size=21, color=c).move_to(r)))
        stack.arrange(DOWN, buff=0).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
        crash = VGroup(label(r"the counter crashes after adding, \ before acknowledging", font_size=19, color=NO),
                       label(r"$\Rightarrow$ \ TCP's guarantee ends at the socket", font_size=19, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(stack, RIGHT, buff=0.5)
        lines = VGroup(
            wrapped_label(r"Saltzer, \ Reed and Clark \ (1984): \ a function that needs the application's knowledge "
                          r"can only be completed at the endpoints; \ lower layers can make it faster, \ never "
                          r"correct", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"so exactly-once is a property of the whole system, \ not of a protocol: \ at-least-once "
                          r"delivery plus an idempotent effect, \ recorded with the effect", 12.4, font_size=21,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Why not let the network layer handle it? TCP already delivers bytes exactly once and in order. "
            "<bookmark mark='a'/> But TCP's guarantee ends at the socket. If the counter adds a chunk and then "
            "crashes before acknowledging it, a new connection carries the retry, and TCP has no way to know it is "
            "a repeat. <bookmark mark='b'/> This is the end-to-end argument of Jerome Saltzer, David Reed and David "
            "Clark, from 1984: a function that needs the application's knowledge can only be completed at the "
            "endpoints. Lower layers can make it faster, but never make it correct. <bookmark mark='c'/> So "
            "exactly-once is a property of a whole system, not of any one protocol: at-least-once delivery, plus "
            "an effect that is idempotent, and recorded together with the effect itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(stack))
            vo.wait_until("a")
            self.play(FadeIn(crash))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM)
