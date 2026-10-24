from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (CHUNKC, CONTC, DECODEC, DISC, F, PART, PREFILLC, STATICC, hbars, load, node_box,
                                   take_away, x_)

KIND_COL = {0: PREFILLC, 1: DECODEC, 2: GREY_D}


def gantt(rows, t_end, slots=8, width=11.4, row_h=0.26, origin=(-5.7, 0.0)):
    """Requests in a server's slots over time: prefill (orange), decode (blue), a finished slot left idle (grey)."""
    x0, y0 = origin
    g = VGroup()
    frame = VGroup(*[Rectangle(width=width, height=row_h * 0.9, stroke_color=GREY_D, stroke_width=0.8,
                               fill_opacity=0).move_to([x0 + width / 2, y0 - k * row_h, 0]) for k in range(slots)])
    bars = VGroup()
    for slot, a, b, kind, rid in rows:
        if a >= t_end:
            continue
        b = min(b, t_end)
        w = max((b - a) / t_end * width, 0.012)
        op = 0.9 if int(rid) % 2 == 0 else 0.6
        bars.add(Rectangle(width=w, height=row_h * 0.72, stroke_width=0, fill_color=KIND_COL[int(kind)],
                           fill_opacity=op if kind != 2 else 0.5)
                 .move_to([x0 + (a / t_end) * width + w / 2, y0 - int(slot) * row_h, 0]))
    g.add(frame, bars)
    g.frame, g.bars = frame, bars
    return g


class Scheduling(VoiceoverScene):
    def construct(self):
        self.card()
        self.static()
        self.results()
        self.stalls()
        self.disagg()

    def card(self):
        card = chapter_card(4, r"Continuous batching", r"When may a new conversation join the batch?", part=PART)
        with self.voiceover("Chapter four. Continuous batching."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def static(self):
        s = load("serving")
        gs, gc = np.asarray(s["gantt_static"]), np.asarray(s["gantt_cont"])
        arr = np.asarray(s["gantt_arrive"])
        t_end = float(max(gs[:, 2].max(), gc[:, 2].max()))
        t_c = float(gc[:, 2].max())
        top = gantt(gs, t_end, origin=(-5.7, 2.0))
        bot = gantt(gc, t_end, origin=(-5.7, -1.15))
        tl = label(r"static batches: \ wait for the whole batch", font_size=22, color=STATICC)
        tl.next_to(top.frame[0], UP, buff=0.35).align_to(top.frame, LEFT)
        bl = label(r"continuous batching: \ a finished slot is refilled at the next step", font_size=22, color=CONTC)
        bl.next_to(bot.frame[0], UP, buff=0.35).align_to(bot.frame, LEFT)

        def marks(y):
            return VGroup(*[Triangle(fill_color=GREY_A, fill_opacity=1, stroke_width=0).scale(0.05).rotate(PI)
                            .move_to([-5.7 + a / t_end * 11.4, y, 0]) for a in arr if a < t_end])

        am_top, am_bot = marks(2.2), marks(-0.95)
        key = VGroup(*[VGroup(Square(0.18, stroke_width=0, fill_color=c_, fill_opacity=0.9),
                              label(t_, font_size=18, color=c_)).arrange(RIGHT, buff=0.1)
                       for c_, t_ in ((PREFILLC, r"prefill"), (DECODEC, r"decode"), (GREY_D, r"idle, \ finished"),
                                      (GREY_A, r"$\blacktriangledown$ \ a request arrives"))]).arrange(RIGHT, buff=0.5)
        key.to_edge(DOWN, buff=0.3)
        tag = note(rf"simulated: \ $8$ slots, \ ${len(arr)}$ requests, \ costs measured on this computer",
                   font_size=18).to_corner(UR, buff=0.2)
        fin_s = float(gs[:, 2].max())
        hc = history_card(2022, r"Gyeong-In Yu et al., \ Orca", rf"iteration-level scheduling: \ "
                          rf"${F.ORCA['gain']}\times$ the throughput of FasterTransformer at the same latency, \ "
                          rf"{F.ORCA['model']}", width=5.6, font_size=18, color=CONTC)
        with self.voiceover(
            "A server has many conversations to write at once, and they don't arrive together or end together. "
            "<bookmark mark='a'/> Until 2022 the usual way was static batching: gather a batch, prefill all the "
            "prompts, and decode until every answer in the batch is finished. A short answer leaves its slot idle "
            "while the longest one goes on, and new requests wait outside. <bookmark mark='b'/> In 2022 a team at "
            "Seoul National University proposed the fix, in a system called Orca: schedule at every step instead "
            "of every batch. <bookmark mark='c'/> When a conversation finishes, its slot goes to the next one "
            "waiting, at the very next step. Here are the same requests both ways, on this computer's measured "
            f"costs: continuous batching finishes all of them in {t_c:.1f} seconds; static batches take "
            f"{fin_s:.1f}."
        ) as vo:
            self.play(FadeIn(tl), FadeIn(top.frame), FadeIn(am_top), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in top.bars], lag_ratio=0.01), run_time=3.0)
            vo.wait_until("b")
            hc.move_to([3.6, -2.0, 0])
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeOut(hc), FadeIn(bl), FadeIn(bot.frame), FadeIn(am_bot))
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bot.bars], lag_ratio=0.01), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        s = load("serving")
        one = s["one"]
        names = [("static", r"static batches", STATICC), ("continuous", r"continuous", CONTC)]
        tp = [one[k]["throughput"] for k, _, _ in names]
        tt = [one[k]["ttft"][0] for k, _, _ in names]
        head = label(rf"{400} requests, \ ${s['rate']:g}$ a second; \ prompts of ${s['prompt_mean']:.0f}$ tokens, "
                     rf"\ answers of ${s['out_mean']:.0f}$, \ on average", font_size=22, color=GREY_A)
        head.to_edge(UP, buff=0.35)
        b1 = hbars(tp, [n[1] for n in names], [n[2] for n in names], width=3.6, row_h=0.62, font_size=22, lo=0,
                   hi=max(tp) * 1.05, fmt_v=lambda v: rf"{v:.0f}")
        b1.move_to([-2.2, 0.4, 0])
        t1 = label(r"tokens written a second", font_size=22, color=GREY_A).next_to(b1, UP, buff=0.35)
        b2 = hbars(tt, [n[1] for n in names], [n[2] for n in names], width=3.2, row_h=0.62, font_size=22, lo=0,
                   hi=max(tt) * 1.05, fmt_v=lambda v: rf"{v:.2f}\,\text{{s}}" if v < 10 else rf"{v:.0f}\,\text{{s}}")
        b2.move_to([3.9, 0.4, 0])
        t2 = label(r"median wait for the first token", font_size=22, color=GREY_A).next_to(b2, UP, buff=0.35)
        cost = s["cost"]
        model = note(rf"each step's time fitted to this computer's measurements: \ $a + b\,B + c \sum \text{{context}} "
                     rf"+ p \cdot \text{{prompt tokens}}$ \ (worst error ${100 * s['fit_err']:.0f}\%$)",
                     font_size=18).to_edge(DOWN, buff=0.35)
        gain = tp[1] / tp[0]
        window = one["static"]["n"] / s["rate"]  # how long the requests take to arrive
        # a server keeps up when it finishes soon after the last request arrives
        st_keeps, co_keeps = (one[k]["span"] < 1.35 * window for k in ("static", "continuous"))
        st_say = (f"write {tp[0]:.0f} tokens a second, and keep up." if st_keeps else
                  f"can't keep up: they write {tp[0]:.0f} tokens a second, fewer than are asked for, so the queue "
                  "grows.")
        co_say = "and keeps up with the traffic." if co_keeps else "and still falls behind."
        if tt[0] >= 2:
            wait_say = (f"a median of {tt[0]:.0f} seconds with static batches, {1e3 * tt[1]:.0f} milliseconds with "
                        "continuous batching.")
        else:
            wait_say = (f"a median of {1e3 * tt[0]:.0f} milliseconds with static batches, {1e3 * tt[1]:.0f} with "
                        "continuous batching.")
        with self.voiceover(
            "With more traffic the difference is stark. <bookmark mark='a'/> We simulated a server on this "
            f"computer's measured costs: 400 requests arriving at random, {s['rate']:g} a second, with long-tailed "
            "lengths, like real chat. <bookmark mark='b'/> Static batches " + st_say + " Continuous batching "
            f"writes {tp[1]:.0f}, {x_(gain)} times as many, " + co_say + " <bookmark mark='c'/> And the wait for a "
            "first token: " + wait_say + " Serving systems have worked this way ever since."
        ) as vo:
            self.play(FadeIn(head), FadeIn(model))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(t1), LaggedStart(*[AnimationGroup(FadeIn(r_.name), GrowFromEdge(r_.bar, LEFT),
                                                               FadeIn(r_.val)) for r_ in b1], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(t2), LaggedStart(*[AnimationGroup(FadeIn(r_.name), GrowFromEdge(r_.bar, LEFT),
                                                               FadeIn(r_.val)) for r_ in b2], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stalls(self):
        s = load("serving")
        one = s["one"]
        c, ch = one["continuous"], one["chunked"]
        rows = [(r"median", 0), (r"99th percentile", 2), (r"longest", 3)]
        g = VGroup()
        for j, (nm, q) in enumerate(rows):
            vals = [c["gap"][q] * 1e3, ch["gap"][q] * 1e3]
            g.add(VGroup(label(nm, font_size=22, color=GREY_A),
                         hbars(vals, [r"whole prompts", r"chunks of $256$"], [CONTC, CHUNKC], width=3.6, row_h=0.42,
                               font_size=20, lo=0, hi=max(c["gap"][3], ch["gap"][3]) * 1e3 * 1.05,
                               fmt_v=lambda v: rf"{v:.0f}\,\text{{ms}}")).arrange(DOWN, aligned_edge=LEFT, buff=0.15))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([2.0, -0.4, 0])
        head = label(r"time between two tokens of one answer", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        # the picture: one step that carries a whole prompt, against steps that carry chunks of it
        st = VGroup(*[Rectangle(width=0.25, height=0.5, stroke_width=0, fill_color=DECODEC, fill_opacity=0.85)
                      for _ in range(5)])
        big = Rectangle(width=1.5, height=0.5, stroke_width=0, fill_color=PREFILLC, fill_opacity=0.9)
        row1 = VGroup(st[0], st[1], big, st[2], st[3], st[4]).arrange(RIGHT, buff=0.05).move_to([-4.3, 1.2, 0])
        st2 = VGroup(*[VGroup(Rectangle(width=0.25, height=0.5, stroke_width=0, fill_color=DECODEC, fill_opacity=0.85),
                              Rectangle(width=0.3 if k in (2, 3, 4, 5) else 0.0001, height=0.5, stroke_width=0,
                                        fill_color=PREFILLC, fill_opacity=0.9)).arrange(RIGHT, buff=0.0)
                       for k in range(8)]).arrange(RIGHT, buff=0.05).move_to([-4.3, -0.4, 0])
        l1 = label(r"a prompt in one step: \ every answer stalls", font_size=20, color=CONTC).next_to(row1, UP, buff=0.2)
        l2 = label(r"in chunks: \ every step a little longer", font_size=20, color=CHUNKC).next_to(st2, UP, buff=0.2)
        tag = schematic_tag(corner=DL)
        hc = history_card(2024, r"Amey Agrawal et al., \ Sarathi-Serve", rf"chunked prefill: \ up to "
                          rf"${F.SARATHI['gain'][1]}\times$ the serving capacity of vLLM", width=4.4, font_size=18,
                          color=CHUNKC).move_to([-4.3, -2.3, 0])
        cut = c["gap"][3] / ch["gap"][3]
        with self.voiceover(
            "Continuous batching has a cost of its own. <bookmark mark='a'/> When a new prompt joins, its whole "
            "prefill runs inside one step, and every conversation in the batch waits for it. "
            f"<bookmark mark='b'/> In our simulation the median gap between two tokens of an answer is "
            f"{1e3 * c['gap'][0]:.0f} milliseconds, but the longest is {1e3 * c['gap'][3]:.0f}. "
            "<bookmark mark='c'/> In 2024 Sarathi-Serve cut prompts into chunks, and gave each step a budget: the "
            "decodes, plus as much prompt as fits. <bookmark mark='d'/> With chunks of 256 tokens, the longest gap "
            f"falls to {1e3 * ch['gap'][3]:.0f} milliseconds, {x_(cut)} times shorter, for almost no change in the "
            "median."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(row1), FadeIn(l1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m_[0]) for m_ in g], lag_ratio=0.2),
                      *[AnimationGroup(FadeIn(m_[1][0].name), GrowFromEdge(m_[1][0].bar, LEFT), FadeIn(m_[1][0].val))
                        for m_ in g])
            vo.wait_until("c")
            self.play(FadeIn(st2), FadeIn(l2), FadeIn(hc))
            vo.wait_until("d")
            self.play(*[AnimationGroup(FadeIn(m_[1][1].name), GrowFromEdge(m_[1][1].bar, LEFT), FadeIn(m_[1][1].val))
                        for m_ in g])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def disagg(self):
        s = load("serving")
        f4 = s["four"]
        co, di = f4["colocated"], f4["disaggregated"]
        # four workers, two ways (schematic)
        wk = VGroup(*[node_box(r"prefill $+$ decode", CONTC, font_size=18, pad=0.15) for _ in range(4)])
        wk.arrange(DOWN, buff=0.15).move_to([-5.0, 0.6, 0])
        pre = node_box(r"prefill", PREFILLC, font_size=18, pad=0.3)
        decs = VGroup(*[node_box(r"decode", DECODEC, font_size=18, pad=0.3) for _ in range(3)]).arrange(DOWN, buff=0.15)
        right = VGroup(pre, decs).arrange(RIGHT, buff=0.9).move_to([-1.8, 0.6, 0])
        arrows = VGroup(*[Arrow(pre.get_right(), d_.get_left(), buff=0.08, stroke_width=2, color=GREY_B,
                                max_tip_length_to_length_ratio=0.15) for d_ in decs])
        cache_l = label(r"caches sent across", font_size=16, color=GREY_B).next_to(arrows, UP, buff=0.05)
        lw = label(r"four alike", font_size=20, color=CONTC).next_to(wk, UP, buff=0.2)
        lr = label(r"one prefills, \ three decode", font_size=20, color=DISC).next_to(right, UP, buff=0.2)
        cols = [CONTC, DISC]
        g = VGroup()
        for nm, q, scale in ((r"median gap", ("gap", 0), 1e3), (r"99th-percentile gap", ("gap", 2), 1e3),
                             (r"median first token", ("ttft", 0), 1e3)):
            vals = [co[q[0]][q[1]] * scale, di[q[0]][q[1]] * scale]
            g.add(VGroup(label(nm, font_size=20, color=GREY_A),
                         hbars(vals, [r"four alike", r"split"], cols, width=2.6, row_h=0.36, font_size=18, lo=0,
                               hi=max(vals) * 1.1, fmt_v=lambda v: rf"{v:.0f}\,\text{{ms}}"))
                  .arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.4, 0.3, 0])
        tag = note(rf"simulated: \ ${s['rate4']:g}$ requests a second on four workers", font_size=18).to_corner(UR,
                                                                                                         buff=0.2)
        hist = VGroup(
            history_card(2024, r"Splitwise; \ DistServe", rf"prefill and decode on separate GPUs: \ "
                         rf"${F.DISTSERVE['requests']}\times$ the requests within latency targets", width=4.2,
                         font_size=17, color=DISC),
            history_card(2024, r"DeepSeek-V3; \ Mooncake (Kimi)", rf"prefill on ${F.DSV3['prefill_unit'][1]}$ GPUs, \ "
                         rf"decode on ${F.DSV3['decode_unit'][1]}$; \ Kimi: \ ${F.MOONCAKE['requests']}\%$ more "
                         r"requests", width=4.2, font_size=17, color=DISC),
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.3)
        tail = co["gap"][2] / di["gap"][2]
        dt = di["ttft"][0] / co["ttft"][0]
        if tail > 1.2 and dt > 1.2:
            verdict = (f"Splitting cut the 99th-percentile gap {x_(tail)} times, but the median wait for a first token "
                       f"grew {x_(dt)} times, because one worker now does every prefill: the split has to be sized to "
                       "the traffic.")
        elif tail > 1.2:
            verdict = f"Splitting cut the 99th-percentile gap {x_(tail)} times, with no cost to the first token."
        else:
            verdict = "Here splitting didn't help the gaps: our prompts are short, so they interfere little."
        with self.voiceover(
            "There is another way to keep prompts from stalling answers: put them on different machines. "
            "<bookmark mark='a'/> Prefill is arithmetic and decode is memory, so in 2024 Splitwise and DistServe "
            "gave each its own GPUs, sending each prompt's cache across when it's done. DeepSeek serves V3 this way: "
            f"prefill on units of {F.DSV3['prefill_unit'][1]} GPUs, decode on units of "
            f"{F.DSV3['decode_unit'][1]}. <bookmark mark='b'/> We tried it in the simulation: four workers that "
            "each do both, against one that prefills and three that decode. <bookmark mark='c'/> " + verdict
        ) as vo:
            self.play(FadeIn(wk), FadeIn(lw), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(right), FadeIn(lr), LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.2),
                      FadeIn(cache_l), FadeIn(hist))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m_) for m_ in g], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(g[1], color=DISC, scale_factor=1.04))
        self.wait(0.3)
        self.clear_scene()
