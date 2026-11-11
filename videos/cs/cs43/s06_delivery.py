from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import seq_diagram
from videos.cs.cs43.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, grid_table, load, mono


def at(sd, t, right=True):
    """The point on a (shifted) sequence diagram's right or left line at time t."""
    return np.array([sd[1 if right else 0].get_x(), sd[0].get_y() + sd.y(t), 0])


def seq(events, font=17, **kw):
    """Part 37's sequence diagram, with each arrow's label turned to run along the arrow, just above it, so that
    steep arrows never cross their own labels."""
    sd = seq_diagram([(a, b, "", r, c) for a, b, _, r, c in events], font=font, **kw)
    for grp, (_, _, text, _, c) in zip(sd.arrows, events):
        if not text:
            continue
        ln = grp[0]
        a, b = ln.get_start(), ln.get_end()
        ang = np.arctan2(b[1] - a[1], b[0] - a[0])
        if ang > PI / 2:
            ang -= PI
        elif ang < -PI / 2:
            ang += PI
        t = label(text, font_size=font, color=c).rotate(ang)
        t.move_to((a + b) / 2 + np.array([-np.sin(ang), np.cos(ang), 0]) * 0.2)
        grp.add(t)
    return sd


class Delivery(VoiceoverScene):
    def construct(self):
        self.card()
        self.promises()
        self.counts()
        self.explore()
        self.counterexample()
        self.theorem()
        self.keys()

    def card(self):
        card = chapter_card(5, r"At most, \ at least, \ exactly once", r"How many times did that message happen?",
                            lit=(1978, 2017), extra=((1978, r"Gray: \ the two generals"),
                                                     (2017, r"Kafka: \ exactly-once semantics")), part=PART)
        with self.voiceover("Chapter five. At most, at least, exactly once."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def promises(self):
        head = label(r"Three promises", font_size=36).to_edge(UP, buff=0.3)
        retry = [(0.2, 1.0, r"inc 1", True, DATA), (1.3, None, r"ack", False, YES),
                 (2.4, 3.2, r"inc 1 again", True, HEAD), (3.4, 4.2, r"ack", False, YES)]
        specs = [(r"at most once", [(0.3, None, r"inc 1", True, DATA)], -4.6),
                 (r"at least once", retry, -0.15), (r"exactly once", retry, 4.3)]
        diagrams, titles, marks, results = VGroup(), VGroup(), [], VGroup()
        for (name, ev, x) in specs:
            sd = seq(ev, t_max=4.4, height=3.2, gap=2.4, names=(r"sender", r"counter"), font=17,
                             center=[x, -0.2, 0])
            diagrams.add(sd)
            titles.add(label(name, font_size=24, color=WHITE).next_to(sd[2:4], UP, buff=0.2).set_x(x))
            mk = VGroup()
            if name != "at most once":
                mk.add(label(r"1", font_size=18, color=YES).move_to(at(sd, 1.0) + RIGHT * 0.25))
                if name == "at least once":
                    mk.add(label(r"2", font_size=18, color=NO).move_to(at(sd, 3.2) + RIGHT * 0.25))
                else:
                    mk.add(label(r"seen: \ skip", font_size=16, color=YES).next_to(at(sd, 3.2), RIGHT,
                                                                                buff=0.12))
            marks.append(mk)
        res = [(r"counter 0: \ lost for good", NO), (r"counter 2: \ applied twice", NO),
               (r"counter 1: \ correct", YES)]
        for (t, c), sd in zip(res, diagrams):
            results.add(label(t, font_size=21, color=c).next_to(sd, DOWN, buff=0.25).set_x(sd[0].get_x() / 2 +
                                                                                           sd[1].get_x() / 2))
        sch = label(r"schematic: \ one increment each", font_size=16, color=GREY_B).to_corner(DR, buff=0.35)
        rules = VGroup(*[label(t, font_size=19, color=GREY_A).next_to(r, DOWN, buff=0.15) for t, r in zip(
            (r"send once, \ never retry", r"retry until acknowledged", r"retry, \ and remember ids"), results)])
        with self.voiceover(
            "A sender can promise one of three things about how often a message takes effect. <bookmark mark='a'/> "
            "At most once: send it once, never retry. Nothing repeats, but a lost message is gone. "
            "<bookmark mark='b'/> At least once: retry until acknowledged. Nothing is lost, but if the "
            "acknowledgement went missing, the retry applies the increment twice. <bookmark mark='c'/> Exactly "
            "once: retry until acknowledged, and have the receiver remember the identifier of every message it "
            "applied, skipping a repeat but acknowledging it again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sch))
            for mk, sd, t, m, r, ru in zip("abc", diagrams, titles, marks, results, rules):
                vo.wait_until(mk)
                self.play(FadeIn(t), FadeIn(sd[:4]))
                for k, a in enumerate(sd.arrows):
                    self.play(Create(a), run_time=0.5)
                    if k == 0 and len(m):
                        self.play(FadeIn(m[0]), run_time=0.3)
                    if k == 2 and len(m) > 1:
                        self.play(FadeIn(m[1]), run_time=0.3)
                self.play(FadeIn(r), FadeIn(ru))
        self.wait(0.4)
        self.clear_scene()

    def counts(self):
        s = load("semantics")
        P = s["policies"]
        head = label(rf"{s['n']:,} increments", font_size=36).to_edge(UP, buff=0.3)
        desc = label(rf"the network loses {100 * s['loss']:.0f}\% of messages, \ acknowledgements included, \ and "
                     rf"duplicates {100 * s['dup']:.0f}\%", font_size=20, color=GREY_A).next_to(head, DOWN, buff=0.3)
        zx = 0.6
        scale = 4.4 / max(abs(p["error"]) for p in P.values())
        ys = (1.0, -0.3, -1.6)
        zero = DashedLine([zx, 1.65, 0], [zx, -2.05, 0], color=GREY_B, dash_length=0.08)
        zl = label(rf"{s['n']:,}: \ the true count", font_size=18, color=GREY_B).next_to(zero, DOWN, buff=0.1)
        rows = []
        for (name, col), y in zip(((r"at most once", NO), (r"at least once", KERN), (r"exactly once", YES)), ys):
            p = P[name]
            nm = label(name, font_size=22, color=WHITE).move_to([0, y, 0]).to_edge(LEFT, buff=0.5)
            e = p["error"]
            if e:
                bar = Rectangle(width=abs(e) * scale, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85)
                bar.move_to([zx + e * scale / 2, y, 0])
                what = rf"{abs(e):,} lost" if e < 0 else rf"{e:,} extra"
            else:
                bar = Dot([zx, y, 0], radius=0.12, color=YES)
                what = r"exact"
            v = label(rf"{p['count']:,}: \ {what}", font_size=20, color=col).next_to(bar, UP, buff=0.1)
            rows.append((nm, bar, v))
        foot = wrapped_label(rf"messages sent, \ counting retries and acknowledgements: \ "
                             rf"{P['at most once']['messages']:,} at most once; \ "
                             rf"{P['at least once']['messages']:,} at least once and "
                             rf"{P['exactly once']['messages']:,} exactly once, \ in "
                             rf"{P['exactly once']['retry_rounds']} rounds of retries: \ deduplication costs no "
                             r"traffic", 12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "We ran all three on one simulated network: ten thousand increments, with five percent of messages lost, "
            "acknowledgements included, and two percent duplicated. <bookmark mark='a'/> At most once counted nine "
            "thousand six hundred and ninety-four: three hundred and six lost. <bookmark mark='b'/> At least once "
            "counted ten thousand seven hundred and fifty-four: seven hundred and fifty-four too many. "
            "<bookmark mark='c'/> Exactly once counted ten thousand, exactly. <bookmark mark='d'/> And it cost "
            "nothing extra on the wire: the same messages, in the same four rounds of retries, as at least once. "
            "The whole difference is a set of identifiers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(desc), Create(zero), FadeIn(zl), *[FadeIn(r[0]) for r in rows])
            for mk, (nm, bar, v) in zip("abc", rows):
                vo.wait_until(mk)
                if isinstance(bar, Dot):
                    self.play(FadeIn(bar, scale=0.3), FadeIn(v))
                else:
                    self.play(GrowFromEdge(bar, RIGHT if bar.get_center()[0] < zx else LEFT), FadeIn(v))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def explore(self):
        m = load("modelcheck")
        d, p = m["dedup"], m["plain"]
        head = label(r"Every execution, \ explored", font_size=36).to_edge(UP, buff=0.3)
        desc = wrapped_label(r"the model: \ a sender with 2 increments, \ each sent up to 3 times until acknowledged; "
                             r"\ a network that may drop any message or acknowledgement, \ duplicate one, \ and "
                             r"deliver in any order; \ breadth-first search \ (Part 18) \ visits every reachable state",
                             12.4, font_size=19, color=GREY_A).next_to(head, DOWN, buff=0.3)

        def panel(title, color, n, lines):
            box = RoundedRectangle(width=6.8, height=2.0, corner_radius=0.12, stroke_color=color, stroke_width=2,
                                   fill_color=BG, fill_opacity=1)
            t = label(title, font_size=24, color=color)
            num = DecimalNumber(n, num_decimal_places=0, group_with_commas=True, font_size=38, color=color)
            st = label(r"states", font_size=24, color=color)
            body = wrapped_label(lines, 6.3, font_size=21, color=WHITE)
            top = VGroup(t, num, st).arrange(RIGHT, buff=0.25)
            st.align_to(num, DOWN)
            g = VGroup(top, body).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(box)
            g.align_to(box, LEFT).shift(RIGHT * 0.2)
            out = VGroup(box, g)
            out.num, out.n = num, n
            return out
        pd = panel(r"with deduplication:", YES, d["states"],
                   r"the counter never exceeds 2; \ every final state with both acknowledged has counter exactly 2")
        pp = panel(r"without:", NO, p["states"], rf"a violation {len(p['trace'])} steps from the start: \ counter "
                                                 rf"{p['counter_at_violation']}")
        panels = VGroup(pd, pp).arrange(DOWN, buff=0.5).next_to(desc, DOWN, buff=0.55).to_edge(LEFT, buff=0.4)
        g = m["growth"]
        chart = bar_chart([r["states"] for r in g], [f"{r['messages']}" for r in g], [LAM] * len(g), height=3.2,
                          bar_w=0.65, gap=0.5, fmt_=lambda v: f"{v:,}", font_size=19, log=True)
        chart.next_to(panels, RIGHT, buff=0.8).align_to(panels, DOWN).shift(UP * 0.35)
        ct = label(r"states, \ one resend each \ (log scale)", font_size=19, color=GREY_A).next_to(chart, UP,
                                                                                                buff=0.2)
        cx = label(r"increments", font_size=18, color=GREY_A).next_to(chart.names, DOWN, buff=0.12)
        ratios = [g[i]["states"] / g[i - 1]["states"] for i in range(1, len(g))]
        rx = label(r"each extra increment: \ " + r", \ ".join(rf"$\times {x:.0f}$" for x in ratios), font_size=19,
                   color=HEAD).next_to(cx, DOWN, buff=0.2)
        with self.voiceover(
            "A simulation samples executions; a model checker visits all of them. <bookmark mark='a'/> Our model: two "
            "increments, each sent up to three times until acknowledged, over a network that may drop any message "
            "or acknowledgement, duplicate one, and deliver in any order. A breadth-first search visits every "
            "reachable state. <bookmark mark='b'/> With deduplication there are four thousand three hundred and "
            "nineteen, and in none does the counter exceed two; whenever both increments were acknowledged, it is "
            "exactly two. <bookmark mark='c'/> Without deduplication there are nine thousand five hundred and "
            "seventy-nine, and a violation six steps from the start. <bookmark mark='d'/> The catch is size: each "
            "extra increment multiplies the states about twenty-fold."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(desc))
            for mk, pan in zip("bc", (pd, pp)):
                vo.wait_until(mk)
                pan.num.set_value(0)
                self.play(FadeIn(pan))
                self.play(ChangeDecimalToValue(pan.num, pan.n), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(ct), FadeIn(chart[0]), FadeIn(chart.names), FadeIn(cx))
            for b, v in zip(chart.bars, chart.vals):
                self.play(GrowFromEdge(b, DOWN), FadeIn(v), run_time=0.5)
            self.play(FadeIn(rx))
        self.wait(0.4)
        self.clear_scene()

    def counterexample(self):
        p = load("modelcheck")["plain"]
        tr = p["trace"]
        head = label(r"The counterexample", font_size=36).to_edge(UP, buff=0.3)
        sends = [k for k, s in enumerate(tr) if s.startswith("send")]
        dels = [k for k, s in enumerate(tr) if s.startswith("deliver")]
        ev = []
        for j, (a, b) in enumerate(zip(sends, dels)):
            ev.append((0.7 * a, 0.7 * b + 0.3, r"increment 0" if j == 0 else r"again", True, DATA if j == 0 else HEAD))
        t_max = 0.7 * dels[-1] + 0.6
        sd = seq(ev, t_max=t_max, height=4.6, gap=4.2, names=(r"sender", r"counter"), font=17,
                         center=[-2.7, -0.35, 0])
        cnt = VGroup(*[label(rf"counter {j + 1}", font_size=18, color=NO if j + 1 > 2 else YES).next_to(
            at(sd, 0.7 * b + 0.3), RIGHT, buff=0.15) for j, b in enumerate(dels)])
        timers = VGroup(*[label(r"timer fires", font_size=16, color=GREY_B).next_to(at(sd, 0.7 * a, False), LEFT,
                                                                                    buff=0.15) for a in sends[1:]])
        steps = VGroup()
        for k, s in enumerate(tr):
            row = VGroup(label(f"{k + 1}", font_size=18, color=GREY_B), mono(s, size=18,
                                                                             color=DATA if s.startswith("send")
                                                                             else KERN)).arrange(RIGHT, buff=0.3)
            steps.add(row)
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        bad = label(rf"$\Rightarrow$ counter {p['counter_at_violation']} \ $>$ 2", font_size=20, color=NO)
        sl = label(r"the trace found", font_size=18, color=GREY_A)
        col = VGroup(sl, steps, bad).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.0, 1.0, 0])
        notes = VGroup(
            wrapped_label(r"breadth-first, \ so a shortest violation", 4.6, font_size=19, color=WHITE),
            wrapped_label(r"the network lost nothing and invented nothing: \ a slow network and a hasty timer "
                          r"suffice", 4.6, font_size=19, color=HEAD),
            wrapped_label(r"with deduplication, \ steps 5 and 6 change nothing", 4.6, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(col, DOWN, buff=0.35).align_to(col, LEFT)
        with self.voiceover(
            "Because the search is breadth-first, the violation it found is a shortest one. <bookmark mark='a'/> The "
            "sender sends increment zero; its timer fires before any acknowledgement could arrive, so it sends it "
            "again, and a third time. <bookmark mark='b'/> The network delivers all three copies, and the counter, "
            "keeping no identifiers, adds three. <bookmark mark='c'/> Nothing was lost or invented: a slow network "
            "and a hasty timer are enough. With deduplication, the last two deliveries would change nothing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd[:4]), FadeIn(sl))
            vo.wait_until("a")
            for j, a in enumerate(sends):
                arrow = sd.arrows[j]
                part = [FadeIn(steps[a])]
                if j:
                    part.append(FadeIn(timers[j - 1]))
                self.play(Create(arrow), *part, run_time=0.8)
            vo.wait_until("b")
            for j, b in enumerate(dels):
                self.play(Indicate(sd.arrows[j], color=KERN), FadeIn(cnt[j]), FadeIn(steps[b]), run_time=0.7)
            self.play(FadeIn(bad), Flash(cnt[-1], color=NO))
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def theorem(self):
        d = load("modelcheck")["dedup"]
        head = label(r"Exactly once, \ proved", font_size=36).to_edge(UP, buff=0.3)
        thm = wrapped_label(r"\textbf{Theorem.} \ If the sender resends each message until it is acknowledged, \ the "
                            r"receiver acknowledges every copy but applies each id at most once, \ and the network is "
                            r"\textbf{fair} \ (a message sent infinitely often is eventually delivered), \ then every "
                            r"message is applied exactly once.", 12.4, font_size=27, color=HEAD)
        steps = []
        for tag, col, text in (
                (r"never twice", YES, (r"an id is applied only if it is not yet in the receiver's set, \ and joins "
                                       r"the set in the same step: \ the counter always equals the size of the set")),
                (r"never zero", DATA, (r"an acknowledgement for $i$ is sent only after a copy of $i$ arrived, \ "
                                       r"so an acknowledged $i$ was applied; \ an unacknowledged one is resent for "
                                       r"ever, \ and fairness delivers a copy")),
                (r"it ends", LAM, (r"acknowledgements are fair too, \ so the sender eventually hears one for "
                                   r"each message and stops"))):
            t = label(tag, font_size=24, color=col)
            box = SurroundingRectangle(t, color=col, buff=0.12, corner_radius=0.06)
            body = wrapped_label(text, 10.0, font_size=24, color=WHITE)
            steps.append(VGroup(VGroup(box, t), body))
        for s in steps:
            s[1].next_to(s[0], RIGHT, buff=0.35).align_to(s[0], UP)
        tags_w = max(s[0].width for s in steps)
        for s in steps:
            s[1].shift(RIGHT * (tags_w - s[0].width))
        proof = VGroup(*steps).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        VGroup(thm, proof).arrange(DOWN, aligned_edge=LEFT, buff=0.7).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(rf"the model checker's resends are bounded, \ so it cannot assume fairness: \ it checked "
                             rf"the conditional form, \ ``if both were acknowledged, \ the counter is 2'', \ in all "
                             rf"{d['states']:,} states", 12.4, font_size=20, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A model checker covers one small case; a proof covers them all. <bookmark mark='a'/> Suppose the sender "
            "resends each message until it is acknowledged, the receiver acknowledges every copy but applies each "
            "identifier at most once, and the network is fair: a message sent infinitely often is eventually "
            "delivered. Then every message is applied exactly once. <bookmark mark='b'/> Never twice: an "
            "identifier is applied only if it is not yet in the receiver's set, and joins the set in the same "
            "step. <bookmark mark='c'/> Never zero: an acknowledgement is sent only after a copy arrived, so an "
            "acknowledged message was applied, and an unacknowledged one is resent until fairness delivers it. "
            "<bookmark mark='d'/> And with fair acknowledgements, the sender stops. <bookmark mark='e'/> Our "
            "bounded model checked the conditional form instead."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            for mk, s in zip("bcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s[0]), FadeIn(s[1], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def keys(self):
        head = label(r"Idempotency keys, \ and the generals again", font_size=36).to_edge(UP, buff=0.3)
        ev = [(0.0, 0.8, r"POST /payments, \ key K", True, DATA), (1.0, None, r"201: \ payment 88", False, YES),
              (2.0, 2.8, r"retry: \ same body, \ key K", True, HEAD), (3.0, 3.8, r"201: \ payment 88", False, YES)]
        sd = seq(ev, t_max=4.0, height=3.6, gap=5.0, names=(r"client", r"server"), font=17,
                         center=[-3.3, 0.15, 0])
        a1 = label(r"charge the card; \ store K $\to$ result", font_size=17, color=WHITE).next_to(
            at(sd, 0.8), RIGHT, buff=0.15)
        a2 = label(r"K found: \ no charge, \ replay", font_size=17, color=YES).next_to(at(sd, 2.8), RIGHT,
                                                                                    buff=0.15)
        key = mono("Idempotency-Key: 5f2c9a1e-7b", size=16, color=HEAD)
        kl = label(r"K: \ chosen by the client, \ random, \ one per intended operation", font_size=17,
                   color=GREY_A)
        kg = VGroup(key, kl).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(sd[2], UP, buff=0.2).align_to(
            sd[2], LEFT).shift(LEFT * 0.3)
        store = grid_table([r"key", r"stored result"], [[r"K", r"201: \ payment 88"]], widths=[0.9, 2.6], row_h=0.42,
                           font_size=18, mono_cols=())
        sbox = SurroundingRectangle(store, color=KERN, buff=0.15, corner_radius=0.06)
        stl = wrapped_label(r"the server's table, \ written in the same transaction as the charge", 3.6,
                            font_size=18, color=KERN)
        sg = VGroup(VGroup(store, sbox), stl).arrange(DOWN, buff=0.12).to_edge(RIGHT, buff=0.4).set_y(0.3)
        ill = label(r"illustrative", font_size=16, color=GREY_B).next_to(sd, DOWN, buff=0.1).align_to(sd, LEFT)
        gen = VGroup(
            wrapped_label(r"exactly-once \textbf{delivery} is impossible: \ the client can never be sure its message "
                          r"arrived \ (the two generals, \ Part 38)", 12.4, font_size=20, color=NO),
            wrapped_label(r"exactly-once \textbf{processing} is not: \ at-least-once delivery plus a receiver that "
                          r"remembers, \ as proved above", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Payment APIs make this part of their interface. <bookmark mark='a'/> The client chooses a fresh random "
            "key for each operation it intends, and sends it with the request. The server charges the card and stores "
            "the key with the result, in one transaction. <bookmark mark='b'/> The response is lost, so the client "
            "retries with the same key, <bookmark mark='c'/> and the server returns the stored result instead of "
            "charging again. <bookmark mark='d'/> Part 38's two generals showed that a client can never be certain "
            "its message arrived: exactly-once delivery is impossible. <bookmark mark='e'/> But exactly-once "
            "processing needs only at-least-once delivery and a receiver that remembers, and that we have just "
            "proved."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd[:4]), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(kg))
            self.play(Create(sd.arrows[0]))
            self.play(FadeIn(a1), FadeIn(sg))
            vo.wait_until("b")
            self.play(Create(sd.arrows[1]))
            self.play(Create(sd.arrows[2]))
            vo.wait_until("c")
            self.play(Indicate(store.cells[1][0], color=HEAD), FadeIn(a2))
            self.play(Create(sd.arrows[3]))
            vo.wait_until("d")
            self.play(FadeIn(gen[0]))
            vo.wait_until("e")
            self.play(FadeIn(gen[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM, YES, BG)
