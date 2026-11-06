from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, module_box, tag_box


def msg_square(color=DATA, side=0.38):
    return Square(side_length=side, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=0.6)


class Queues(VoiceoverScene):
    def construct(self):
        self.card()
        self.decouple()
        self.visibility()
        self.dead_letters()
        self.pubsub()
        self.partitions()

    def card(self):
        card = chapter_card(7, r"Queues and pub/sub", r"How do services talk without waiting for each other?",
                            lit=(2003, 2011), extra=((2003, r"Hohpe and Woolf: \ integration patterns"),
                                                     (2011, r"Kafka \ (LinkedIn)")), part=PART)
        with self.voiceover("Chapter seven. Queues, and publish and subscribe."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def decouple(self):
        head = label(r"A buffer between two services", font_size=36).to_edge(UP, buff=0.3)
        prod = module_box(r"producer", DATA, w=2.2, h=0.8, font=21).move_to([-5.2, 1.2, 0])
        cons = module_box(r"consumer", YES, w=2.2, h=0.8, font=21).move_to([5.2, 1.2, 0])
        slots = VGroup(*[Square(side_length=0.5, stroke_color=GREY_C, stroke_width=1.5) for _ in range(8)])
        slots.arrange(LEFT, buff=0.06).move_to([0, 1.2, 0])          # slot 0 is the head, on the right
        qlabel = label(r"queue", font_size=19, color=GREY_B).next_to(slots, UP, buff=0.15)
        a1 = Arrow(prod.get_right(), slots.get_left(), buff=0.15, color=GREY_B, stroke_width=2)
        a2 = Arrow(slots.get_right(), cons.get_left(), buff=0.15, color=GREY_B, stroke_width=2)
        down = label(r"deploying", font_size=18, color=NO).next_to(cons, DOWN, buff=0.15)
        lines = VGroup(
            wrapped_label(r"\textbf{decoupled in time}: \ the producer hands over its message and moves on; \ the "
                          r"consumer need not even be running", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"\textbf{decoupled in rate}: \ a burst waits in the queue, \ and the consumer works "
                          r"through it at its own pace \ (until the queue fills: \ chapter 8)", 12.4, font_size=21,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -0.5, 0])
        products = VGroup(*[tag_box(t, color=KERN, size=20) for t in ("Amazon SQS", "RabbitMQ", "Apache Kafka",
                                                                      "Google Cloud Pub/Sub")])
        products.arrange(RIGHT, buff=0.4).move_to([0, -2.4, 0])
        msgs = [msg_square().move_to(prod) for _ in range(5)]
        with self.voiceover(
            "Every call so far has been a conversation: the caller waits while the callee works, and if the callee "
            "is down, the call fails. <bookmark mark='a'/> A message queue puts a buffer between them. The producer "
            "hands its message to the queue and moves on, even while the consumer is in the middle of a deploy. "
            "<bookmark mark='b'/> When the consumer comes back, the messages are waiting, and it works through them "
            "at its own pace. Producer and consumer are decoupled in time, and in rate. <bookmark mark='c'/> This "
            "is the idea behind Amazon's Simple Queue Service, RabbitMQ, Apache Kafka and Google's Cloud Pub/Sub, "
            "and Gregor Hohpe and Bobby Woolf catalogued its patterns in 2003."
        ) as vo:
            self.play(FadeIn(head), FadeIn(prod), FadeIn(cons), FadeIn(slots), FadeIn(qlabel), GrowArrow(a1),
                      GrowArrow(a2))
            vo.wait_until("a")
            cons.save_state()
            self.play(cons.animate.set_opacity(0.3), FadeIn(down), FadeIn(lines[0]))
            for i, m in enumerate(msgs):
                self.add(m)
                self.play(m.animate.move_to(slots[i]), run_time=0.45)
            vo.wait_until("b")
            self.play(cons.animate.restore(), FadeOut(down), FadeIn(lines[1]))
            for m in msgs:
                self.play(m.animate.move_to(cons), run_time=0.4)
                self.remove(m)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in products], lag_ratio=0.25))
        self.wait(0.4)
        self.clear_scene()

    def visibility(self):
        v = load("visibility")
        T = v["timeout"]
        head = label(r"Receive, \ hide, \ delete", font_size=36).to_edge(UP, buff=0.3)
        q = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.1, stroke_color=GREY_C, stroke_width=1.5)
        q.move_to([-4.6, 1.7, 0])
        ql = label(r"queue", font_size=18, color=GREY_B).next_to(q, UP, buff=0.1)
        m = tag_box(r"order 17", color=DATA, size=17).move_to(q)
        wa = module_box(r"worker A", LAM, w=2.0, h=0.7, font=19).move_to([0.4, 2.3, 0])
        wb = module_box(r"worker B", KERN, w=2.0, h=0.7, font=19).move_to([0.4, 1.1, 0])
        side = VGroup(
            wrapped_label(r"receiving does not remove a message: \ it is hidden for the \textbf{visibility "
                          r"timeout}", 3.9, font_size=19, color=WHITE),
            wrapped_label(r"deleting it is the acknowledgement", 3.9, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.9, 1.7, 0])
        # a timeline of one message's life, seconds 0-60
        x0, w, tmax = -4.3, 10.4, 60.0

        def X(t):
            return x0 + w * t / tmax
        ax = Line([X(0), -2.6, 0], [X(tmax), -2.6, 0], color=GREY_C, stroke_width=1.5)
        ticks = VGroup(*[VGroup(Line([X(t), -2.66, 0], [X(t), -2.54, 0], color=GREY_C),
                                label(f"{t:g}", font_size=16, color=GREY_B).move_to([X(t), -2.85, 0]))
                         for t in (0, 10, 20, 30, 40, 50, 60)])
        unit = label(r"seconds", font_size=16, color=GREY_B).next_to(ticks, RIGHT, buff=0.2).shift(UP * 0.02)
        rows_y = {"hidden": -0.2, "A": -1.0, "B": -1.8}
        names = VGroup(label(r"message hidden", font_size=17, color=GREY_A),
                       label(r"worker A", font_size=17, color=LAM),
                       label(r"worker B", font_size=17, color=KERN))
        for n, y in zip(names, rows_y.values()):
            n.move_to([X(0) - 0.25 - n.width / 2, y, 0])

        def bar(t0, t1, y, color):
            return Rectangle(width=X(t1) - X(t0), height=0.36, stroke_width=0, fill_color=color,
                             fill_opacity=0.8).move_to([(X(t0) + X(t1)) / 2, y, 0])
        hid1, hid2 = bar(0, T, rows_y["hidden"], GREY_B), bar(T, 42, rows_y["hidden"], GREY_B)
        a1, a2, a3 = bar(0, T, rows_y["A"], LAM), bar(T, 42, rows_y["A"], LAM), bar(42, 55, rows_y["A"], LAM)
        b_work = bar(T, 42, rows_y["B"], KERN)
        expire = DashedLine([X(T), 0.15, 0], [X(T), -2.6, 0], color=HEAD, stroke_width=2, dash_length=0.08)
        exl = label(rf"timeout, \ {T:g}\,s", font_size=17, color=HEAD).next_to(expire, UP, buff=0.05)
        del_b = label(r"B deletes", font_size=17, color=YES).next_to(b_work, RIGHT, buff=0.12)
        side.add(wrapped_label(r"A finishes too: \ the work is done twice", 3.9, font_size=19, color=NO))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.9, 1.6, 0])
        ill = label(r"illustrative times", font_size=16, color=GREY_B).to_corner(DR, buff=0.3)
        copy_a = m.copy()
        with self.voiceover(
            "A queue must not lose a message when a consumer crashes halfway through it. <bookmark mark='a'/> So "
            "receiving a message does not remove it. Worker A receives this order, and the queue hides it for a "
            "visibility timeout, here thirty seconds, which is also the default of Amazon's queue. Only when the "
            "worker has finished does it delete the message: that is its acknowledgement. <bookmark mark='b'/> But "
            "worker A is slow. The timeout expires, the message reappears, and worker B takes it. "
            "<bookmark mark='c'/> B finishes and deletes it. Then A, which never crashed, finishes as well. The work "
            "has been done twice, and nothing malfunctioned: this is at-least-once delivery, working as designed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(q), FadeIn(ql), FadeIn(m), FadeIn(wa), FadeIn(wb), Create(ax),
                      FadeIn(ticks), FadeIn(unit), FadeIn(names), FadeIn(ill))
            vo.wait_until("a")
            self.play(copy_a.animate.move_to(wa), m.animate.set_opacity(0.2), FadeIn(side[0]))
            self.play(GrowFromEdge(hid1, LEFT), GrowFromEdge(a1, LEFT), run_time=2.5, rate_func=linear)
            self.play(FadeIn(side[1]), run_time=0.5)
            vo.wait_until("b")
            self.play(Create(expire), FadeIn(exl), m.animate.set_opacity(1))
            copy_b = m.copy()
            self.play(copy_b.animate.move_to(wb), m.animate.set_opacity(0.2))
            self.play(GrowFromEdge(hid2, LEFT), GrowFromEdge(a2, LEFT), GrowFromEdge(b_work, LEFT), run_time=1.5,
                      rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(del_b), FadeOut(m), copy_b[0].animate.set_stroke(YES), copy_b[1].animate.set_color(YES))
            self.play(GrowFromEdge(a3, LEFT), run_time=1.0, rate_func=linear)
            self.play(FadeIn(side[2]), copy_a[0].animate.set_stroke(NO), copy_a[1].animate.set_color(NO),
                      Indicate(VGroup(a1, a2, a3), color=NO, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def dead_letters(self):
        v = load("visibility")
        extra = v["receives"] - v["processed"] - 5 * v["dead_lettered"]      # receives beyond the first
        head = label(r"Poison messages and the dead-letter queue", font_size=36).to_edge(UP, buff=0.3)
        q = RoundedRectangle(width=2.4, height=0.9, corner_radius=0.1, stroke_color=GREY_C, stroke_width=1.5)
        q.move_to([-5.0, 1.4, 0])
        ql = label(r"queue", font_size=18, color=GREY_B).next_to(q, UP, buff=0.1)
        wk = module_box(r"worker", LAM, w=1.8, h=0.7, font=19).move_to([-1.6, 1.4, 0])
        dlq = RoundedRectangle(width=2.4, height=0.9, corner_radius=0.1, stroke_color=NO, stroke_width=2)
        dlq.move_to([-3.3, -0.6, 0])
        dl = label(r"dead-letter queue", font_size=18, color=NO).next_to(dlq, DOWN, buff=0.1)
        bad = tag_box(r"bad order", color=NO, size=16).move_to(q)
        count = label(r"receives: \ 0", font_size=19, color=HEAD).next_to(q, DOWN, buff=0.25)
        rows = [[r"messages", f"{v['messages']:,}"], [r"receives in all", f"{v['receives']:,}"],
                [r"processed more than once", f"{v['processed_more_than_once']}"],
                [r"extra receives", f"{extra}"], [r"dead-lettered after 5 receives", f"{v['dead_lettered']}"]]
        tab = grid_table([rf"our queue, \ timeout {v['timeout']:g}\,s", r""], rows, widths=[4.2, 1.4], row_h=0.42,
                         font_size=19, mono_cols=())
        tab.move_to([3.6, 1.0, 0])
        for r in (3, 4):
            tab.cells[r][1].set_color(HEAD)
        tab.cells[5][1].set_color(NO)
        setup = wrapped_label(r"work takes 5--20\,s; \ 5\% of messages are slow, \ 40--90\,s; \ 0.2\% are poison "
                              r"and always fail", 5.6, font_size=18, color=GREY_A).next_to(tab, DOWN, buff=0.25)
        lesson = wrapped_label(r"at-least-once delivery: \ every consumer must be \textbf{idempotent}, \ so that "
                               r"doing a message twice does it once \ (chapter 5's keys)", 12.4, font_size=21,
                               color=YES).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Some messages can never succeed: a malformed order, say, that crashes every worker that touches it. "
            "<bookmark mark='a'/> Each failure returns it to the queue, and without a limit it would circle "
            "forever, wasting a worker each time. So queues count receives, and after a maximum, here five, move "
            "the message to a dead-letter queue for a person to inspect. <bookmark mark='b'/> We ran two thousand "
            "messages through a simulated queue, with work of five to twenty seconds, one message in twenty slow, "
            "at forty to ninety seconds, and one in five hundred poisoned. <bookmark mark='c'/> Ninety-eight "
            "messages were processed more than once, some of them three times, and two were dead-lettered. The "
            "lesson is chapter five's: a consumer must be idempotent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(q), FadeIn(ql), FadeIn(wk), FadeIn(bad), FadeIn(count))
            vo.wait_until("a")
            self.play(FadeIn(dlq), FadeIn(dl))
            for k in range(1, 6):
                new = label(rf"receives: \ {k}", font_size=19, color=HEAD).move_to(count)
                self.play(bad.animate.move_to(wk.get_center() + DOWN * 0.75), Transform(count, new), run_time=0.35)
                self.play(Indicate(wk, color=NO, scale_factor=1.1), run_time=0.3)
                if k < 5:
                    self.play(bad.animate.move_to(q), run_time=0.35)
            self.play(bad.animate.move_to(dlq))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(VGroup(*tab.cells[1])),
                      FadeIn(setup))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r])) for r in range(2, 6)], lag_ratio=0.4),
                      run_time=2)
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()

    def pubsub(self):
        head = label(r"Publish and subscribe", font_size=36).to_edge(UP, buff=0.3)
        pub = module_box(r"orders", DATA, w=1.9, h=0.7, font=20).move_to([-5.6, 0.6, 0])
        topic = module_box(r"topic: \ order placed", HEAD, w=2.9, h=0.8, font=19).move_to([-2.4, 0.6, 0])
        subs = VGroup()
        consumers = VGroup()
        for i, (name, col) in enumerate(((r"email", YES), (r"billing", LAM), (r"analytics", KERN))):
            y = 1.9 - i * 1.3
            slots = VGroup(*[Square(side_length=0.38, stroke_color=GREY_C, stroke_width=1.2) for _ in range(4)])
            slots.arrange(LEFT, buff=0.04).move_to([1.3, y, 0])
            subs.add(slots)
            consumers.add(module_box(name, col, w=1.9, h=0.62, font=19).move_to([4.6, y, 0]))
        sub_l = label(r"one subscription each", font_size=17, color=GREY_B).next_to(subs, UP, buff=0.12)
        a0 = Arrow(pub.get_right(), topic.get_left(), buff=0.1, color=GREY_B, stroke_width=2)
        fan = VGroup(*[Arrow(topic.get_right(), s.get_left(), buff=0.1, color=GREY_B, stroke_width=2) for s in subs])
        out = VGroup(*[Arrow(s.get_right(), c.get_left(), buff=0.1, color=GREY_B, stroke_width=2)
                       for s, c in zip(subs, consumers)])
        lines = VGroup(
            wrapped_label(r"a \textbf{queue} gives each message to \textit{one} consumer: \ workers compete, \ and the "
                          r"work is shared", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"a \textbf{topic} gives each message to \textit{every} subscription, \ each with its own "
                          r"queue and pace; \ the publisher does not know who listens", 12.4, font_size=20,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -2.3, 0])
        with self.voiceover(
            "A queue gives each message to one consumer. Workers compete for messages, and the work is shared "
            "among them. <bookmark mark='a'/> Publish and subscribe gives each message to everyone who is "
            "interested. The orders service publishes an event, order placed, to a topic. <bookmark mark='b'/> Each "
            "subscription receives its own copy, in its own queue: email, billing and analytics each read at their "
            "own pace, and a slow one does not hold back the others. <bookmark mark='c'/> The publisher does not "
            "know who is listening, so a new subscriber can be added without changing it. That is decoupling "
            "again, in who as well as when."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pub), FadeIn(topic), GrowArrow(a0), FadeIn(subs), FadeIn(sub_l),
                      FadeIn(consumers), *[GrowArrow(a) for a in fan], *[GrowArrow(a) for a in out],
                      FadeIn(lines[0]))
            vo.wait_until("a")
            ev = msg_square(HEAD).move_to(pub)
            self.add(ev)
            self.play(ev.animate.move_to(topic), run_time=0.7)
            vo.wait_until("b")
            copies = [msg_square(HEAD, 0.32).move_to(topic) for _ in subs]
            self.remove(ev)
            self.add(*copies)
            self.play(*[c.animate.move_to(s[0]) for c, s in zip(copies, subs)], FadeIn(lines[1]), run_time=0.9)
            self.play(copies[0].animate.move_to(consumers[0]), copies[1].animate.move_to(consumers[1]), run_time=0.7)
            self.play(FadeOut(copies[0]), FadeOut(copies[1]), Indicate(consumers[2], color=GREY_B), run_time=0.6)
            vo.wait_until("c")
            self.play(copies[2].animate.move_to(consumers[2]), run_time=0.7)
            self.play(FadeOut(copies[2]))
        self.wait(0.4)
        self.clear_scene()

    def partitions(self):
        head = label(r"Order per key: \ a partitioned log", font_size=36).to_edge(UP, buff=0.3)
        keys = {"alice": (0, DATA), "bob": (1, LAM), "carol": (2, YES), "dave": (1, KERN)}
        stream = [("alice", 1), ("bob", 1), ("alice", 2), ("carol", 1), ("dave", 1), ("bob", 2), ("alice", 3),
                  ("carol", 2), ("dave", 2)]
        cw, n = 0.78, 6
        x_first = -1.6
        rows_y = [1.6, 0.6, -0.4]
        cells = []
        plabels = VGroup()
        for p, y in enumerate(rows_y):
            row = VGroup(*[Rectangle(width=cw, height=0.55, stroke_color=GREY_C, stroke_width=1.2)
                           for _ in range(n)]).arrange(RIGHT, buff=0).move_to([x_first + n * cw / 2, y, 0])
            cells.append(row)
            plabels.add(label(rf"partition {p}", font_size=17, color=GREY_A).next_to(row, LEFT, buff=0.15))
        offs = VGroup(*[VGroup(*[label(f"{i}", font_size=16, color=GREY_B).next_to(c, UP, buff=0.03)
                                 for i, c in enumerate(cells[0])])])
        hashbox = module_box(r"hash(key) mod 3", HEAD, w=2.4, h=0.6, font=17).move_to([-5.4, 0.6, 0])
        src = label(r"messages, \ each with a key", font_size=17, color=GREY_B).next_to(hashbox, UP, buff=0.5)
        groups = VGroup(*[module_box(rf"consumer {p + 1}", GREY_B, w=1.75, h=0.5, font=16).move_to(
            [cells[p].get_right()[0] + 1.15, y, 0]) for p, y in enumerate(rows_y)])
        glabel = label(r"one consumer group", font_size=16, color=GREY_B).next_to(groups, UP, buff=0.12)
        ill = label(r"illustrative keys and hashes", font_size=16, color=GREY_B).to_corner(DR, buff=0.3)
        lines = VGroup(
            wrapped_label(r"the same key always lands in the same partition: \ order holds \textit{within} a "
                          r"partition, \ not across them", 12.4, font_size=20, color=YES),
            wrapped_label(r"a consumer group divides the partitions; \ each consumer commits an \textbf{offset}, \ "
                          r"how far it has read, \ and resumes from it after a crash: \ a log you can replay \ "
                          r"(Part 46)", 12.4, font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -2.1, 0])
        fill = [0, 0, 0]
        placed = []
        for k, i in stream:
            p, col = keys[k]
            t = tag_box(f"{k[0]}{i}", color=col, size=15, w=cw - 0.12, h=0.42).move_to(cells[p][fill[p]])
            fill[p] += 1
            placed.append(t)
        pointers = VGroup(*[Triangle(color=HEAD, fill_opacity=1).scale(0.09).rotate(PI).next_to(cells[p][0], DOWN,
                                                                                               buff=0.04)
                            for p in range(3)])
        with self.voiceover(
            "What about order? One queue with many workers cannot promise it: two workers race, and a slow one "
            "finishes last. <bookmark mark='a'/> Kafka's answer, from LinkedIn in 2011, is a partitioned log. "
            "Each message carries a key, a customer, say, and a hash of the key picks one of the partitions, so "
            "every message for the same key lands in the same partition, in order. <bookmark mark='b'/> Order holds "
            "within a partition and not across them, and order per customer is usually the order that matters. "
            "<bookmark mark='c'/> A consumer group divides the partitions among its members, and each "
            "consumer commits an offset: how far it has read. After a crash it resumes from its offset. The log "
            "can be replayed, which is where Part 46 begins."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hashbox), FadeIn(src), *[FadeIn(r) for r in cells], FadeIn(plabels),
                      FadeIn(offs), FadeIn(ill))
            vo.wait_until("a")
            for t in placed:
                c = t.copy().move_to(hashbox)
                self.play(FadeIn(c, scale=0.8), run_time=0.2)
                self.play(ReplacementTransform(c, t), run_time=0.35)
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(groups), FadeIn(glabel), FadeIn(pointers), FadeIn(lines[1]))
            for step in range(3):
                anims = [pointers[p].animate.shift(RIGHT * cw) for p in range(3) if step < fill[p] - 1]
                if anims:
                    self.play(*anims, run_time=0.5)
        self.wait(0.4)
        self.clear_scene()


_ = (BG, NO)
