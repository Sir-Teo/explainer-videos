"""Live instruments: pictures driven by a recorded run, so the screen moves the way the machine did.

* :class:`Meter`: a labelled number (and an optional bar) that follows a ``ValueTracker`` or an array indexed by
  one, for running counts, CPI, accuracy, hit rates;
* :class:`EventStrip`: a conveyor of events entering on the right (branch outcomes and a predictor's guesses,
  cache hits and misses, packets lost and delivered), one row per stream, scrolling smoothly as a tracker
  advances;
* :class:`PipelineFlow`: Pebble's five stages as a datapath with instructions travelling through it as packets,
  cycle by cycle from a chart recorded by :mod:`explainer.cs.pebble.pipe` (``record=``). It shows stalls as
  bubbles, forwarding as arcs that flash backwards, and flushes as packets dropping out. Its clock, retired
  count and CPI update as it runs;
* :class:`Race`: lanes that fill in proportion to measured times, with running clocks: the same loop on shuffled
  and sorted data, two programs, two machines.

Each instrument is built from data the part computed; none of them invents a step.
"""

from __future__ import annotations

import numpy as np
from manim import *  # noqa: F403

from explainer.style import C

MONO = "DejaVu Sans Mono"
STAGES = ("IF", "ID", "EX", "MEM", "WB")
STAGE_COLOR = {"IF": C.CS_DATA, "ID": C.CS_CONTROL, "EX": C.CS_FUNC, "MEM": C.CS_INF, "WB": C.CS_TRUE}
STAGE_NAME = {"IF": "fetch", "ID": "decode", "EX": "execute", "MEM": "memory", "WB": "write back"}
PACKET_COLORS = [C.CS_DATA, C.CS_HEAD, C.CS_FUNC, C.CS_CONTROL, C.CS_INF, C.CS_CODE, C.CS_COST]


def _label(text, **kw):
    from explainer.analysis import label

    return label(text, **kw)


def _mono(s, size, color=WHITE):
    from explainer.zh_text import verbatim

    with verbatim():
        return Text(s, font=MONO, font_size=size, color=color)


# ---------------------------------------------------------------------------
# a number that follows the run
# ---------------------------------------------------------------------------
class Meter(VGroup):
    """``Meter(r"CPI", tracker, values=cpi_by_cycle, fmt="{:.2f}")``: the label, then the value read from
    ``values[int(tracker)]`` (or the tracker itself), redrawn every frame.  ``bar=(lo, hi)`` adds a bar."""

    def __init__(self, name: str, tracker: ValueTracker, values=None, fmt="{:.2f}", color=C.CS_HEAD, font_size=26,
                 bar=None, bar_width=2.4, unit=""):
        super().__init__()
        self.tracker, self.values, self.fmt, self.unit = tracker, values, fmt, unit
        self.name = _label(name, font_size=font_size - 4, color=GREY_B)
        self.num = _mono(self._text(), font_size, color)
        row = VGroup(self.name, self.num).arrange(RIGHT, buff=0.22)
        self.add(row)
        self._size, self._color = font_size, color
        self.num.add_updater(self._redraw)
        if bar:
            lo, hi = bar
            track = RoundedRectangle(width=bar_width, height=0.14, corner_radius=0.07, stroke_width=0,
                                     fill_color=GREY_D, fill_opacity=0.6).next_to(row, DOWN, buff=0.12,
                                                                                 aligned_edge=LEFT)
            fill = always_redraw(lambda: RoundedRectangle(
                width=max(0.02, bar_width * float(np.clip((self.value() - lo) / (hi - lo), 0, 1))), height=0.14,
                corner_radius=0.07, stroke_width=0, fill_color=color, fill_opacity=0.9).align_to(track, LEFT).move_to(
                track.get_center(), coor_mask=[0, 1, 0]))
            self.add(track, fill)

    def value(self) -> float:
        t = self.tracker.get_value()
        if self.values is None:
            return t
        k = int(np.clip(np.floor(t + 1e-9), 0, len(self.values) - 1))
        return float(self.values[k])

    def _text(self) -> str:
        v = self.value()
        return (self.fmt.format(v) if not np.isnan(v) else "-") + self.unit

    def _redraw(self, m):
        new = _mono(self._text(), self._size, self._color)
        new.move_to(m, aligned_edge=LEFT)
        m.become(new)


# ---------------------------------------------------------------------------
# a conveyor of events
# ---------------------------------------------------------------------------
class EventStrip(VGroup):
    """Rows of cells entering on the right as ``self.t`` grows: cell k of every row appears once ``t > k`` and
    slides left one step per unit of ``t``; at most ``window`` cells are visible.

    ``rows`` are lists of ``(fill_color, mark)`` pairs (``mark`` a short string drawn on the cell, or None);
    ``names`` label the rows on the left.  :meth:`advance` plays it forward."""

    def __init__(self, rows, names=(), window=28, cell=0.3, gap=0.06, row_gap=0.16, font_size=18, name_width=1.6):
        super().__init__()
        self.t = ValueTracker(0.0)
        self.window, self.step = window, cell + gap
        n = max(len(r) for r in rows)
        self.n, self.cell, self.row_step = n, cell, cell + row_gap
        self.w0 = window * self.step + 0.1
        self.frame = Rectangle(width=self.w0, height=len(rows) * self.row_step + 0.1, stroke_width=0)
        self.add(self.frame)
        self.cells = []
        self.labels = VGroup()
        for j, row in enumerate(rows):
            y = self.frame.get_top()[1] - 0.05 - cell / 2 - j * self.row_step
            cells = []
            for k, (color, mark) in enumerate(row):
                sq = RoundedRectangle(width=cell, height=cell, corner_radius=0.05, stroke_width=0, fill_color=color,
                                      fill_opacity=0.85)
                g = VGroup(sq)
                if mark:
                    g.add(_mono(mark, int(font_size * 0.9), WHITE).move_to(sq))
                g.move_to([0, y, 0]).set_opacity(0)
                g._j, g._k = j, k
                cells.append(g)
                self.add(g)
            self.cells.append(cells)
            if j < len(names) and names[j]:
                lab = _label(names[j], font_size=font_size, color=GREY_B)
                lab.move_to([self.frame.get_left()[0] - 0.2 - lab.width / 2, y, 0])
                self.labels.add(lab)
        self.add(self.labels)
        for row in self.cells:
            for g in row:
                g.add_updater(self._place)

    def _place(self, g):
        """Lay cell ``g`` out from the strip's frame as it is now (so the strip can be moved and scaled)."""
        s = self.frame.width / self.w0
        age = self.t.get_value() - g._k  # how long ago it arrived, in steps
        right = self.frame.get_right()[0] - (0.05 + self.cell / 2) * s
        x = right - (age - 1) * self.step * s if age > 0 else right + self.step * s
        y = self.frame.get_top()[1] - (0.05 + self.cell / 2 + g._j * self.row_step) * s
        op = float(np.clip(age, 0, 1)) * float(np.clip(self.window - age + 1, 0, 1))
        g.move_to([x, y, 0])
        for sub in g:
            if isinstance(sub, RoundedRectangle):
                sub.set_fill(opacity=0.85 * op)
            else:
                sub.set_opacity(op)

    def advance(self, scene, steps, run_time=None, rate_func=linear, per_step=0.18, **kw):
        end = min(self.n, self.t.get_value() + steps)
        rt = run_time if run_time is not None else max(0.3, per_step * (end - self.t.get_value()))
        scene.play(self.t.animate.set_value(end), run_time=rt, rate_func=rate_func, **kw)


# ---------------------------------------------------------------------------
# the pipeline, live
# ---------------------------------------------------------------------------
class PipelineFlow(VGroup):
    """Pebble's five-stage pipeline with instructions moving through it, from a recorded chart (the dict that
    ``videos/cs/cs7/compute.py``'s ``_chart`` returns: ``chart`` rows of stage -> sequence number plus ``events``,
    and ``seq`` -> {text, flushed}).

    ``self.cycle(scene, c)`` animates cycle ``c``; ``self.run(scene, c0, c1)`` plays a range.  ``self.clock``,
    ``self.retired`` and ``self.cpi`` are the readouts."""

    def __init__(self, data, width=12.4, stage_w=1.95, h=1.35, font_size=16, show_names=True, readouts=True):
        super().__init__()
        self.data, self.chart, self.info = data, data["chart"], data["seq"]
        n = len(STAGES)
        gap = (width - n * stage_w) / (n - 1)
        self.stage, self.reg = {}, []
        x = -width / 2 + stage_w / 2
        self.boxes = VGroup()
        for k, s in enumerate(STAGES):
            col = STAGE_COLOR[s]
            b = RoundedRectangle(width=stage_w, height=h, corner_radius=0.14, stroke_color=col, stroke_width=2.2,
                                 fill_color=col, fill_opacity=0.07).move_to([x, 0, 0])
            t = Text(s, font="DejaVu Sans", font_size=22, weight=BOLD, color=col).move_to(b.get_top() + DOWN * 0.26)
            grp = VGroup(b, t)
            if show_names:
                grp.add(_label(STAGE_NAME[s], font_size=16, color=GREY_B).next_to(b, DOWN, buff=0.12))
            self.stage[s] = grp
            self.boxes.add(grp)
            if k < n - 1:
                r = Rectangle(width=0.1, height=h + 0.3, stroke_width=0, fill_color=C.CS_CLOCK,
                              fill_opacity=0.55).move_to([x + stage_w / 2 + gap / 2, 0, 0])
                self.reg.append(r)
            x += stage_w + gap
        self.regs = VGroup(*self.reg)
        self.add(self.boxes, self.regs)
        self.stage_w, self.h, self.font_size = stage_w, h, font_size
        self.packets: dict[int, VGroup] = {}
        self.bubbles: dict[str, VGroup] = {}
        self._live_bubbles: dict[str, VGroup] = {}
        self._colors: dict[int, str] = {}
        self.retired_n, self.c = 0, -1
        # readouts: the clock, instructions retired, CPI so far
        self.tracker = ValueTracker(0)
        if readouts:
            ret = np.cumsum([1 if r["WB"] is not None and not self.info[str(r["WB"])]["flushed"]
                             and self.info[str(r["WB"])]["text"] != "?" else 0 for r in self.chart])
            cyc = np.arange(1, len(self.chart) + 1)
            cpi = np.where(ret > 0, cyc / np.maximum(ret, 1), np.nan)
            self.clock = Meter(r"cycle", self.tracker, values=cyc, fmt="{:.0f}", color=C.CS_CLOCK)
            self.retired = Meter(r"retired", self.tracker, values=ret, fmt="{:.0f}", color=C.CS_TRUE)
            self.cpi = Meter(r"CPI", self.tracker, values=cpi, fmt="{:.2f}", color=C.CS_COST)
            self.readouts = VGroup(self.clock, self.retired, self.cpi).arrange(RIGHT, buff=0.8)
            self.readouts.next_to(self.boxes, UP, buff=0.45)
            self.add(self.readouts)
        self.tick = VGroup(*[r.copy().set_fill(C.CS_CLOCK, opacity=1).set_stroke(width=0) for r in self.reg])
        self.tick.set_opacity(0)
        self.add(self.tick)

    # where a packet sits in a stage (scaled with the instrument)
    def slot(self, s):
        b = self.stage[s][0]
        return b.get_center() + DOWN * 0.12 * (b.height / self.h)

    def _packet(self, seq) -> VGroup:
        if seq not in self.packets:
            it = self.info[str(seq)]
            color = self._colors.setdefault(seq, PACKET_COLORS[len(self._colors) % len(PACKET_COLORS)])
            sc = self.stage["IF"][0].width / self.stage_w
            txt = _mono(it["text"], self.font_size, WHITE)
            wmax = (self.stage_w - 0.22) * sc
            box = RoundedRectangle(width=wmax, height=0.5 * sc, corner_radius=0.1 * sc, stroke_color=color,
                                   stroke_width=2, fill_color=color, fill_opacity=0.32)
            txt.scale(sc)
            if txt.width > wmax - 0.12 * sc:
                txt.width = wmax - 0.12 * sc
            p = VGroup(box, txt.move_to(box))
            p.box = box
            p.move_to(self.slot("IF") + LEFT * (self.stage_w * 0.9 * sc))
            p.set_opacity(0)
            self.packets[seq] = p
        return self.packets[seq]

    def _new_bubble(self, s) -> VGroup:
        """An empty slot: a dashed bubble labelled ``nop``."""
        sc = self.stage["IF"][0].width / self.stage_w
        c = Circle(radius=0.24 * sc, stroke_color=GREY_B, stroke_width=2)
        t = Text("nop", font=MONO, font_size=13, color=GREY_B).scale(sc).move_to(c)
        b = VGroup(DashedVMobject(c, num_dashes=14), t).move_to(self.slot(s)).set_opacity(0)
        self.bubbles.setdefault("all", VGroup()).add(b)
        return b

    def state(self, c):
        """Stage -> sequence number in cycle ``c`` (slots fetched past ``halt``, recorded as "?", are empty)."""
        if not 0 <= c < len(self.chart):
            return {s: None for s in STAGES}
        row = self.chart[c]
        return {s: (row[s] if row[s] is not None and self.info[str(row[s])]["text"] != "?" else None)
                for s in STAGES}

    def cycle(self, scene, c, run_time=0.75, flash=True):
        """Animate the step from cycle ``c - 1`` to cycle ``c``."""
        prev, now = self.state(c - 1), self.state(c)
        row = self.chart[c]
        sc = self.stage["IF"][0].width / self.stage_w
        where_prev = {s: st for st, s in prev.items() if s is not None}
        where_now = {s: st for st, s in now.items() if s is not None}
        flushed = set()
        for ev in row["events"]:
            if ev[0] == "flush":
                flushed.update(ev[1])
        moves, extras = [], []
        for seq, st in where_now.items():
            p = self._packet(seq)
            if seq not in scene.mobjects and p not in scene.mobjects:
                scene.add(p)
            target = self.slot(st)
            if seq not in where_prev:
                moves.append(p.animate.move_to(target).set_opacity(1))
            elif where_prev[seq] != st:
                moves.append(p.animate.move_to(target))
            else:  # held in place: stalled
                moves.append(Wiggle(p, scale_value=1.06, rotation_angle=0.02 * TAU))
            if self.info[str(seq)]["flushed"] and seq in flushed:
                moves.append(p.box.animate.set_stroke(GREY_D).set_fill(GREY_D, 0.25))
        for seq, st in where_prev.items():
            if seq in where_now:
                continue
            p = self._packet(seq)
            if self.info[str(seq)]["flushed"]:
                moves.append(p.animate.shift(DOWN * 1.2 * sc).set_opacity(0))
            else:  # retired: out of write back, to the right
                moves.append(p.animate.shift(RIGHT * self.stage_w * 0.8 * sc).set_opacity(0))
        # bubbles: a stall (or a busy unit) sends an empty slot down the pipe, one stage a cycle
        nxt = {}
        for st, b in self._live_bubbles.items():
            i = STAGES.index(st)
            if i + 1 < len(STAGES) and now[STAGES[i + 1]] is None:
                nxt[STAGES[i + 1]] = b
                moves.append(b.animate.move_to(self.slot(STAGES[i + 1])))
            else:
                moves.append(FadeOut(b, scale=0.6))
        for ev in row["events"]:
            if ev[0] in ("stall", "busy"):
                st = "EX" if ev[0] == "stall" else "MEM"
                if now[st] is None and st not in nxt:
                    b = self._new_bubble(st)
                    prev_st = STAGES[STAGES.index(st) - 1]
                    b.move_to(self.slot(prev_st))
                    scene.add(b)
                    moves.append(b.animate.move_to(self.slot(st)).set_opacity(0.9))
                    nxt[st] = b
        self._live_bubbles = nxt
        moves.append(self.tracker.animate.set_value(c))
        moves.append(Succession(self.tick.animate(run_time=0.12).set_opacity(0.9),
                                self.tick.animate(run_time=0.3).set_opacity(0)))
        scene.play(*moves, run_time=run_time)
        if flash:
            seen = set()
            for ev in row["events"]:
                if ev[0] == "fwd" and ev[1] in self.packets and ev[2] in self.packets and (ev[1], ev[2]) not in seen:
                    seen.add((ev[1], ev[2]))
                    a = self.packets[ev[1]].get_top()
                    b = self.packets[ev[2]].get_top()
                    arc = ArcBetweenPoints(a + UP * 0.05, b + UP * 0.05, angle=-PI / 2.2, color=C.CS_HEAD,
                                           stroke_width=5)
                    extras.append(ShowPassingFlash(arc.copy(), time_width=0.6))
                    extras.append(Indicate(self.packets[ev[2]], color=C.CS_HEAD, scale_factor=1.08))
            if extras:
                scene.play(*extras, run_time=0.6)
        self.c = c

    def run(self, scene, c0, c1, per_cycle=0.75, flash=True, on_cycle=None):
        for c in range(c0, c1):
            self.cycle(scene, c, run_time=per_cycle, flash=flash)
            if on_cycle:
                on_cycle(c)

    def everything(self):
        """Every mobject the run may have added (to clear them together)."""
        return VGroup(self, *self.packets.values(), *self.bubbles.values())


# ---------------------------------------------------------------------------
# a race: two (or more) runs side by side, in proportion to how long each took
# ---------------------------------------------------------------------------
class Race(VGroup):
    """Lanes that fill in proportion to measured times: ``Race([("sorted", 3.2e-3, YES), ("shuffled", 38e-3, NO)],
    unit="ms", scale=1e3)``.  ``self.t`` runs from 0 to the slowest time; each lane's bar, clock and finish flag
    follow it.  :meth:`go` plays it in ``seconds`` of film (the fastest lane finishing at the same rate as the
    others, so the gap is the real ratio)."""

    def __init__(self, lanes, unit="s", scale=1.0, fmt="{:.1f}", width=9.0, lane_h=0.5, gap=0.42, font_size=26,
                 name_width=2.6):
        super().__init__()
        self.t = ValueTracker(0.0)
        self.total = max(sec for _, sec, _ in lanes)
        self.lanes = VGroup()
        self.bars, self.clocks, self.flags = [], [], []
        for k, (name, sec, color) in enumerate(lanes):
            y = -k * (lane_h + gap)
            lab = _label(name, font_size=font_size, color=color)
            if lab.width > name_width:
                lab.width = name_width
            lab.move_to([-width / 2 - 0.25 - lab.width / 2, y, 0])
            track = RoundedRectangle(width=width, height=lane_h, corner_radius=lane_h / 2, stroke_color=GREY_D,
                                     stroke_width=1.5, fill_color=GREY_E, fill_opacity=0.35).move_to([0, y, 0])

            def bar(track=track, sec=sec, color=color):
                f = float(np.clip(self.t.get_value() / sec, 0, 1))
                w = max(1e-3, track.width * f)
                r = RoundedRectangle(width=max(w, track.height), height=track.height, corner_radius=track.height / 2,
                                     stroke_width=0, fill_color=color, fill_opacity=0.75 if f < 1 else 0.95)
                r.stretch_to_fit_width(max(w, 1e-3))
                return r.align_to(track, LEFT).move_to(track.get_center(), coor_mask=[0, 1, 0]).set_opacity(
                    0 if f <= 0 else 1)

            b = always_redraw(bar)
            clock = _mono(fmt.format(0.0) + " " + unit, font_size - 2, color)

            def tick(m, track=track, sec=sec, color=color):
                v = min(self.t.get_value(), sec) * scale
                new = _mono(fmt.format(v) + " " + unit, font_size - 2, color)
                m.become(new.next_to(track, RIGHT, buff=0.25))

            clock.add_updater(tick)
            self.lanes.add(VGroup(lab, track))
            self.bars.append(b)
            self.clocks.append(clock)
            self.add(lab, track, b, clock)

    def go(self, scene, seconds=6.0, **kw):
        scene.play(self.t.animate.set_value(self.total), run_time=seconds, rate_func=linear, **kw)

    def freeze(self):
        for m in self.bars + self.clocks:
            m.clear_updaters()
        return self
