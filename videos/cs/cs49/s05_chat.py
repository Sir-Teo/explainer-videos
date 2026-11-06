from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, mono


def block(name, sub, color, w=2.1, h=0.95):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2,
                         fill_color=BG, fill_opacity=1)
    t = label(name, font_size=19 if sub else 17, color=WHITE)
    s = label(sub, font_size=15, color=color) if sub else VectorizedPoint()
    for m in (t, s):
        if m.width > w - 0.15:
            m.width = w - 0.15
    VGroup(t, s).arrange(DOWN, buff=0.08).move_to(r) if sub else t.move_to(r)
    return VGroup(r, t, s)


def link(a, b, color=GREY_C):
    return Arrow(a, b, buff=0.08, stroke_width=2, color=color, max_tip_length_to_length_ratio=0.12)


def cell(text, color, w=0.62, h=0.5, size=16):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.6, fill_color=BG, fill_opacity=1)
    return VGroup(r, mono(text, size=size, color=color).move_to(r))


def num(x, digits=0):
    return f"{x:,.{digits}f}".replace(",", "{,}")


class Chat(VoiceoverScene):
    def construct(self):
        self.card()
        self.napkin()
        self.design()
        self.ordering()
        self.sync()
        self.secrets()

    def card(self):
        card = chapter_card(4, r"A chat service", r"How do messages arrive once, \ in order, \ on phones that come "
                            r"and go?", lit=(2011, 2016), extra=((2011, r"WebSocket, \ RFC 6455"),
                                                                (2016, r"the double ratchet published")), part=PART)
        with self.voiceover("Chapter four. A chat service."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def napkin(self):
        head = label(r"Requirements and the napkin", font_size=36).to_edge(UP, buff=0.3)
        req = wrapped_label(r"one-to-one and group messages; \ each delivered once, \ in order, \ to every device, \ "
                            r"including phones that were off; \ receipts; \ end-to-end encryption", 12.4,
                            font_size=21, color=WHITE).next_to(head, DOWN, buff=0.4)
        users, per, online, per_server = 100e6, 40, 50e6, 2e6
        day = users * per
        rate = round(day / 86_400, -3)
        rows = [[r"daily users", r"100 million", r""],
                [r"messages", r"40 per user a day", rf"about {num(rate)} a second; \ {num(3 * rate)} at a "
                                                    r"3$\times$ peak"],
                [r"message bodies", r"100 bytes each", rf"{day * 100 / 1e9:.0f} GB a day"],
                [r"open connections", r"50 million at the peak", rf"{online / per_server:.0f} servers at 2 million "
                                                                 r"each"]]
        tab = grid_table([r"quantity", r"assumption", r"result"], rows, widths=[3.0, 3.8, 5.6], row_h=0.55,
                         font_size=19, mono_cols=())
        tab.next_to(req, DOWN, buff=0.5)
        for k in range(1, len(rows) + 1):
            tab.cells[k][2].set_color(HEAD)
        foot = note(r"assumptions illustrative; \ 2 million connections on one server: \ WhatsApp's engineering "
                    r"blog, \ 2012", font_size=16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A chat service carries one-to-one and group messages. <bookmark mark='a'/> Each must arrive exactly "
            "once, in order, on every device, including phones that were off, with receipts and end-to-end "
            "encryption. <bookmark mark='b'/> Suppose a hundred million daily users sending forty messages each: "
            f"about {rate:,.0f} a second, three times that at the peak. <bookmark mark='c'/> The bodies are small, "
            f"about {day * 100 / 1e9:.0f} gigabytes a day. <bookmark mark='d'/> The unusual number is connections: "
            "a waiting phone keeps one open, so fifty million are open at the peak. WhatsApp reported two million "
            "on one server in 2012, so twenty-five machines could in principle hold them; a real fleet is larger."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(req))
            vo.wait_until("b")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), FadeIn(VGroup(*tab.cells[1])),
                      FadeIn(foot))
            self.play(FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[3])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[4])))
        self.wait(0.4)
        self.clear_scene()

    def design(self):
        head = label(r"Connection servers and a session registry", font_size=36).to_edge(UP, buff=0.3)
        y = 0.9
        ana = block(r"Ana", r"phone", DATA, w=1.5).move_to([-6.0, y, 0])
        gwa = block(r"gateway 1", r"WebSockets", GREY_B, w=2.0).move_to([-3.85, y, 0])
        chat = block(r"chat service", r"by conversation", HEAD, w=2.2).move_to([-1.0, y, 0])
        gwb = block(r"gateway 3", r"WebSockets", GREY_B, w=2.0).move_to([1.85, y, 0])
        ben = block(r"Ben", r"phone", LAM, w=1.5).move_to([5.9, y, 0])
        reg = block(r"session registry", r"Ben $\to$ gateway 3", YES, w=2.7).move_to([-1.0, y + 1.45, 0])
        store = block(r"message store", r"a log per conversation", KERN, w=2.7).move_to([-1.0, y - 1.5, 0])
        push = block(r"push service", r"wakes a sleeping phone", NO, w=2.5).move_to([4.3, y - 1.5, 0])
        boxes = VGroup(ana, gwa, chat, gwb, ben, reg, store, push)
        arrows = VGroup(link(ana.get_right(), gwa.get_left()), link(gwa.get_right(), chat.get_left()),
                        link(chat.get_right(), gwb.get_left()), link(gwb.get_right(), ben.get_left()),
                        link(chat.get_top(), reg.get_bottom()), link(chat.get_bottom(), store.get_top()),
                        link(chat.get_corner(DR), push.get_left()), link(push.get_top(), ben.get_bottom()))
        notes = VGroup(
            wrapped_label(r"a \textbf{WebSocket} \ (RFC 6455, \ 2011) \ is one long-lived TCP connection carrying "
                          r"messages both ways: \ the server can send without being asked", 12.4, font_size=19,
                          color=WHITE),
            wrapped_label(r"gateways hold connections and nothing else; \ the registry, \ with short leases \ "
                          r"(Part 39), \ says which gateway holds which device", 12.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is the design. <bookmark mark='a'/> Each phone keeps a WebSocket open to a gateway: one long-lived "
            "connection on which the server can send without being asked. Gateways hold connections and nothing "
            "else, so they can be many and simple. <bookmark mark='b'/> Ana sends. Her gateway passes the message "
            "to the chat service, partitioned by conversation, which appends it to that conversation's log. "
            "<bookmark mark='c'/> A session registry, with short leases, says Ben's phone is on gateway three, and "
            "the message goes down that connection. <bookmark mark='d'/> If Ben's phone is asleep, the push "
            "service wakes it through the phone maker's notification system, and the phone connects and fetches "
            "what it missed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes), Create(arrows))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            m = Dot(ana.get_center(), radius=0.11, color=DATA)
            self.play(FadeIn(m))
            self.play(m.animate.move_to(gwa.get_center()), run_time=0.6)
            self.play(m.animate.move_to(chat.get_center()), run_time=0.6)
            c = m.copy().set_color(KERN)
            self.play(c.animate.move_to(store.get_center()), run_time=0.6)
            vo.wait_until("c")
            q = m.copy().set_color(YES)
            self.play(q.animate.move_to(reg.get_center()), FadeIn(notes[1]), run_time=0.6)
            self.play(q.animate.move_to(chat.get_center()), run_time=0.6)
            self.play(FadeOut(q), m.animate.move_to(gwb.get_center()), run_time=0.7)
            self.play(m.animate.move_to(ben.get_center()), run_time=0.7)
            vo.wait_until("d")
            p = Dot(chat.get_center(), radius=0.11, color=NO)
            self.play(FadeIn(p))
            self.play(p.animate.move_to(push.get_center()), run_time=0.7)
            self.play(p.animate.move_to(ben.get_center()), run_time=0.7)
            self.play(FadeOut(p), FadeOut(m), FadeOut(c))
        self.wait(0.4)
        self.clear_scene()

    def ordering(self):
        head = label(r"The hard part: \ order", font_size=36).to_edge(UP, buff=0.3)
        xs = {"ben": -4.6, "srv": -2.7, "ana": -0.8}
        top, bot = 2.2, -2.0
        lanes = VGroup()
        for k, n in ((r"ben", r"Ben"), (r"srv", r"conversation\\owner"), (r"ana", r"Ana")):
            lanes.add(Line([xs[k], top, 0], [xs[k], bot, 0], color=GREY_D, stroke_width=2))
            lanes.add(label(n, font_size=17, color=GREY_A).next_to([xs[k], top, 0], UP, buff=0.1))

        def msg(a, b, y0, y1, color):
            return Arrow([xs[a], y0, 0], [xs[b], y1, 0], buff=0, stroke_width=2.5, color=color,
                         max_tip_length_to_length_ratio=0.1)
        m1 = VGroup(msg("ben", "srv", 1.5, 0.9, DATA), msg("srv", "ana", 0.9, 0.3, DATA))
        m2 = VGroup(msg("ana", "srv", -0.3, -0.9, LAM), msg("srv", "ben", -0.9, -1.5, LAM))
        s1 = label(r"\textbf{41}", font_size=18, color=HEAD).move_to([xs["srv"] - 0.3, 0.9 - 0.3, 0])
        s2 = label(r"\textbf{42}", font_size=18, color=HEAD).move_to([xs["srv"] + 0.3, -0.9 - 0.3, 0])
        t1 = label(r"``Dinner at 8?''\\stamped 10:00:00", font_size=16, color=DATA).next_to(
            [xs["ben"], 1.5, 0], LEFT, buff=0.1)
        t2 = label(r"``Yes!''\\stamped 09:59:58", font_size=16, color=LAM).next_to([xs["ana"], -0.3, 0], RIGHT,
                                                                                 buff=0.1)
        skew = label(r"Ana's clock runs 3 s slow", font_size=16, color=NO).next_to(t2, DOWN, buff=0.1).align_to(
            t2, LEFT)

        def lst(title, items, color):
            t = label(title, font_size=19, color=color)
            rows = VGroup(*[label(s, font_size=18, color=WHITE) for s in items]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.12)
            return VGroup(t, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        bad = lst(r"sorted by phone clocks", [r"Ana: \ Yes!", r"Ben: \ Dinner at 8?"], NO)
        good = lst(r"sorted by sequence number", [r"41 \ Ben: \ Dinner at 8?", r"42 \ Ana: \ Yes!"], YES)
        VGroup(bad, good).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([4.3, 1.0, 0])
        ill = note(r"illustrative", font_size=16).next_to(good, DOWN, buff=0.3).align_to(good, LEFT)
        foot = wrapped_label(r"one writer per conversation numbers its messages: \ an order within each "
                             r"conversation, \ which is all a reader sees; \ a retried send carries the same client "
                             r"ID and gets the same number \ (Part 43)", 12.4, font_size=19,
                             color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The hard part is order. <bookmark mark='a'/> Ben asks, dinner at eight? Ana reads it and answers yes. "
            "<bookmark mark='b'/> But her phone's clock runs three seconds slow, so her answer is stamped earlier "
            "than his question. <bookmark mark='c'/> Sorted by the phones' clocks, the answer comes first. Server "
            "clocks differ too, as Part 38 showed: unsynchronised clocks cannot order events reliably. "
            "<bookmark mark='d'/> The fix is a sequence number. Each conversation has one owner, its partition's "
            "leader, which numbers messages as they arrive. Ana answered after seeing forty-one, so her answer "
            "gets a larger number. The order holds within a conversation only, which is all a reader sees, and a "
            "retried send carries the same client identifier, Part 43's idempotency key, and keeps its number."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lanes))
            vo.wait_until("a")
            self.play(GrowArrow(m1[0]), FadeIn(t1))
            self.play(GrowArrow(m1[1]))
            self.play(GrowArrow(m2[0]))
            self.play(GrowArrow(m2[1]))
            vo.wait_until("b")
            self.play(FadeIn(t2), FadeIn(skew))
            vo.wait_until("c")
            self.play(FadeIn(bad))
            vo.wait_until("d")
            self.play(FadeIn(s1), FadeIn(s2))
            self.play(FadeIn(good), FadeIn(ill))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def sync(self):
        head = label(r"Receipts and offline sync", font_size=36).to_edge(UP, buff=0.3)
        seqs = list(range(38, 48))
        tape = VGroup(*[cell(str(s), KERN if s <= 44 else GREY_B) for s in seqs]).arrange(RIGHT, buff=0)
        tape.move_to([0, 1.4, 0])
        tt = label(r"the conversation's log, \ by sequence number", font_size=18, color=GREY_A).next_to(tape, UP,
                                                                                                       buff=0.2)

        def marker(s, text, color, below=True):
            c = tape[seqs.index(s)]
            tri = Triangle(color=color, fill_opacity=1).scale(0.1)
            if below:
                tri.rotate(0).next_to(c, DOWN, buff=0.06)
            else:
                tri.rotate(PI).next_to(c, UP, buff=0.06)
            t = label(text, font_size=16, color=color).next_to(tri, DOWN if below else UP, buff=0.08)
            return VGroup(tri, t)
        delivered = marker(44, r"delivered to Ben's phone", YES)
        read = marker(42, r"read by Ben", DATA)
        read[1].shift(DOWN * 0.45)
        for c in tape[7:]:
            c.set_opacity(0)
        offline = label(r"Ben's phone is off", font_size=18, color=NO).move_to([0, -0.6, 0])
        ask = mono("sync(conversation, after=44)", size=17, color=YES).move_to([-2.6, -1.2, 0])
        notes = VGroup(
            wrapped_label(r"receipts are watermarks: \ one number per member and device, \ \textit{delivered up to} "
                          r"and \textit{read up to}, \ not one record per message", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"a phone that holds 44 and receives 46 knows 45 is missing, \ and asks for it", 12.4,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        ill = note(r"illustrative", font_size=16).to_corner(UR, buff=0.4).shift(DOWN * 0.5)
        with self.voiceover(
            "Sequence numbers also give receipts and offline sync almost for free. <bookmark mark='a'/> Each "
            "conversation's log is numbered. Ben's phone acknowledges what it has received, up to forty-four: that "
            "is the second tick, delivered. <bookmark mark='b'/> When Ben has looked, his phone reports read up to "
            "forty-two. Each receipt is a watermark, one number per member and device, not a record per message. "
            "<bookmark mark='c'/> Now Ben's phone is switched off, and three more messages arrive. "
            "<bookmark mark='d'/> When it reconnects it asks for everything after forty-four, and gets exactly the "
            "three it missed. And a phone that holds forty-four and suddenly receives forty-six knows that "
            "forty-five is missing, and asks for it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tt), FadeIn(tape[:7]), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(delivered, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(read, shift=UP * 0.1), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(offline))
            self.play(LaggedStart(*[c.animate.set_opacity(1) for c in tape[7:]], lag_ratio=0.4), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeOut(offline), FadeIn(ask))
            copies = VGroup(*[c.copy() for c in tape[7:]])
            self.play(copies.animate.arrange(RIGHT, buff=0.1).next_to(ask, RIGHT, buff=0.5), run_time=1.5)
            self.play(delivered.animate.shift(RIGHT * 3 * tape[0].width), *[c[0].animate.set_stroke(color=KERN)
                                                                            for c in tape[7:]],
                      *[c[1].animate.set_color(KERN) for c in tape[7:]])
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def secrets(self):
        head = label(r"Groups, \ and keys the server never sees", font_size=36).to_edge(UP, buff=0.3)
        snd = block(r"sender", r"encrypts once", DATA, w=1.8).move_to([-5.7, 1.3, 0])
        srv = block(r"server", r"sees ciphertext", GREY_B, w=1.9).move_to([-3.4, 1.3, 0])
        mem = VGroup(*[block(rf"member {k}", r"", LAM, w=1.5, h=0.5) for k in range(1, 5)]).arrange(
            DOWN, buff=0.15).move_to([-1.0, 1.3, 0])
        fan = VGroup(link(snd.get_right(), srv.get_left()),
                     *[link(srv.get_right(), m.get_left()) for m in mem])
        gnote = wrapped_label(r"WhatsApp's groups use \textbf{sender keys}: \ each member sends its own chain key to every "
                              r"other member once, \ pairwise; \ then one encryption per message, \ and the server "
                              r"fans out the ciphertext \ (chapter 2)", 6.2, font_size=18, color=WHITE)
        gnote.next_to(VGroup(snd, mem), DOWN, buff=0.35).align_to(snd, LEFT)
        x0 = 0.9
        cks = VGroup(*[block(rf"chain key {k}", r"", HEAD if k < 3 else KERN, w=1.25, h=0.5) for k in range(1, 5)])
        cks.arrange(RIGHT, buff=0.35).move_to([x0 + 2.75, 1.5, 0])
        kdf = VGroup(*[link(cks[k].get_right(), cks[k + 1].get_left()) for k in range(3)])
        mks = VGroup(*[label(rf"msg key {k}", font_size=15, color=GREY_A).next_to(cks[k - 1], DOWN, buff=0.4)
                       for k in range(1, 5)])
        down = VGroup(*[link(cks[k].get_bottom(), mks[k].get_top()) for k in range(4)])
        dh = label(r"a new Diffie--Hellman \ (Part 30) \ on each reply", font_size=16, color=KERN).next_to(
            kdf[1], UP, buff=0.45)
        dha = link(dh.get_bottom(), kdf[1].get_center())
        rt = label(r"the double ratchet \ (Perrin \& Marlinspike, \ 2016)", font_size=19, color=HEAD).next_to(
            cks, UP, buff=1.05)
        rnote = wrapped_label(r"each key is a hash of the last \ (Part 29), \ used once and deleted: \ a stolen "
                              r"phone cannot read old messages; \ the next Diffie--Hellman locks the thief out of "
                              r"new ones", 5.9, font_size=18, color=WHITE).next_to(mks, DOWN, buff=0.35)
        rnote.align_to(cks, LEFT)
        foot = wrapped_label(r"the trade-off: \ the server cannot search, \ filter by content \ or restore history "
                             r"without the user's keys, \ and every extra device is another recipient", 12.4,
                             font_size=19, color=NO).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Two last pieces. <bookmark mark='a'/> A group message is stored once and fanned out to every member, "
            "the push of chapter two, with pulls for very large groups. <bookmark mark='b'/> With end-to-end "
            "encryption the server only ever relays ciphertext. Between two devices, Signal's double ratchet, "
            "published by Trevor Perrin and Moxie Marlinspike in 2016, derives each message's key by hashing the "
            "previous chain key, Part 29, and deletes it after use, so a stolen phone cannot read old messages. "
            "<bookmark mark='c'/> Each reply also mixes in a fresh Diffie-Hellman exchange, Part 30, which locks a "
            "thief out of new ones. <bookmark mark='d'/> WhatsApp's groups use sender keys, distributed pairwise once, so a "
            "message is encrypted once. <bookmark mark='e'/> The price: the server cannot search or filter "
            "content, and every extra device is another recipient."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(snd), FadeIn(srv), FadeIn(mem), Create(fan))
            pk = Dot(snd.get_center(), radius=0.1, color=DATA)
            self.play(FadeIn(pk))
            self.play(pk.animate.move_to(srv.get_center()), run_time=0.6)
            cp = VGroup(*[pk.copy() for _ in mem])
            self.remove(pk)
            self.play(*[d.animate.move_to(m.get_center()) for d, m in zip(cp, mem)], run_time=0.8)
            self.play(FadeOut(cp))
            vo.wait_until("b")
            self.play(FadeIn(rt), FadeIn(cks[:2]), GrowArrow(kdf[0]), FadeIn(mks[:2]), Create(down[:2]))
            self.play(FadeIn(rnote))
            self.play(cks[0].animate.set_opacity(0.3), mks[0].animate.set_opacity(0.3))
            vo.wait_until("c")
            self.play(FadeIn(dh), GrowArrow(dha), GrowArrow(kdf[1]), FadeIn(cks[2:]), GrowArrow(kdf[2]),
                      FadeIn(mks[2:]), Create(down[2:]))
            vo.wait_until("d")
            self.play(FadeIn(gnote))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN,)
