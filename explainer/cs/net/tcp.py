"""TCP congestion control on a bottleneck (Part 37): an event-driven packet simulator of flows sharing one link.

    res = dumbbell(flows=[Flow("reno", rtt=0.1), Flow("cubic", rtt=0.1)], mbps=10, buffer=None (BDP), qdisc="droptail",
                   loss=0.0, duration=30)
    res["flows"][i]: throughput (Mb/s), bytes, retransmits, cwnd trace [(t, cwnd)], rtt samples
    res["queue"]: [(t, packets)], drops, utilization

Each flow sends MSS-sized packets (1460 bytes of data, 1500 on the wire) whenever its window allows (BBR paces).
The bottleneck serves packets at ``mbps``; its queue is drop-tail, RED (Floyd and Jacobson) or CoDel (Nichols and
Jacobson); ``loss`` adds random drops; a flow's ``jitter`` delays its ACKs by a random amount that has nothing to do with
congestion, keeping them in order (Wi-Fi and cellular links aggregate ACKs this way).  The receiver acknowledges every packet individually (as with SACK), so the
sender knows which packets arrived:
* a transmission is declared lost when three transmissions sent after it have been acknowledged (fast retransmit;
  counting transmissions rather than sequence numbers, as RACK does, so that a lost retransmission is noticed too);
* the window is cut at most once per round trip of losses (fast recovery); if no acknowledgement comes for an RTO
  (Jacobson/Karels: SRTT + 4 RTTVAR, at least 200 ms; Karn's rule: no samples from retransmissions) everything
  outstanding is resent and the window restarts at one packet.
Congestion control:
* ``fixed``: a constant window and go-back-n retransmission on timeout, with no backoff: the TCPs of 1986;
* ``vegas``: delay-based: keep between 2 and 4 of the flow's own packets queued (Brakmo and Peterson, 1994);
* ``reno``: slow start (+1 per ACK) to ssthresh, then +1/cwnd per ACK; on loss cwnd = ssthresh = cwnd / 2;
* ``cubic``: W(t) = C (t - K)^3 + W_max, K = cbrt(W_max (1 - beta) / C), C = 0.4, beta = 0.7 (RFC 9438), never below
  the Reno-friendly window;
* ``bbr``: estimate the bottleneck bandwidth (max delivery rate over 10 round trips) and the propagation delay (min
  RTT over 10 s); start up at gain 2.885 until the bandwidth stops growing, drain the queue that built, then pace at
  gain x bandwidth with gains 1.25, 0.75, 1, 1, 1, 1, 1, 1; cap inflight at 2 x BDP; every 10 s, PROBE_RTT drains to four packets to re-measure the delay; ignores loss
  (BBRv1).
"""
from __future__ import annotations

import heapq
import math
import random
from dataclasses import dataclass, field

MSS = 1460
WIRE = 1500


@dataclass
class Flow:
    cc: str = "reno"
    rtt: float = 0.1                # two-way propagation delay, seconds
    start: float = 0.0
    size: int | None = None         # bytes to send (None: unlimited)
    name: str = ""
    window: float = 32.0            # for "fixed": the window, never changed
    jitter: float = 0.0             # extra delay on this flow's ACK path, uniform in [0, jitter]: not congestion
    ack_sched: float = 0.0
    # state
    cwnd: float = 2.0
    ssthresh: float = 1e9
    next_seq: int = 0
    inflight: dict = field(default_factory=dict)      # seq -> send time
    tx_of: dict = field(default_factory=dict)         # seq -> id of its latest transmission
    tx_count: int = 0
    highest_tx_acked: int = -1
    retx_set: set = field(default_factory=set)
    acked: set = field(default_factory=set)
    highest_acked: int = -1
    recover: int = -1
    srtt: float | None = None
    rttvar: float = 0.0
    rto: float = 1.0
    last_ack_time: float = 0.0
    delivered: int = 0
    delivered_warm: int = 0
    retransmits: int = 0
    trace: list = field(default_factory=list)
    rtts: list = field(default_factory=list)
    done_time: float | None = None
    # cubic
    w_max: float = 0.0
    epoch: float | None = None
    # bbr
    bw_samples: list = field(default_factory=list)
    min_rtt: float = 1e9
    min_rtt_time: float = 0.0
    pacing_next: float = 0.0
    cycle: int = 0
    cycle_start: float = 0.0
    delivered_at: dict = field(default_factory=dict)
    bbr_state: str = "startup"
    full_bw: float = 0.0
    full_bw_count: int = 0
    probe_rtt_end: float = 0.0


def dumbbell(flows: list[Flow], mbps: float = 10.0, buffer: int | None = None, qdisc: str = "droptail",
             loss: float = 0.0, duration: float = 30.0, seed: int = 0, trace_every: float = 0.05,
             red=(0.25, 0.75, 0.1), codel=(0.005, 0.1), warmup: float = 0.0) -> dict:
    rng = random.Random(seed)
    rate = mbps * 1e6 / (WIRE * 8)                   # packets a second
    base = min(f.rtt for f in flows)
    bdp = rate * base
    B = int(round(bdp)) if buffer is None else buffer
    B = max(B, 2)
    events: list = []
    k = 0

    def push(t, kind, data):
        nonlocal k
        k += 1
        heapq.heappush(events, (t, k, kind, data))

    queue: list = []                                   # (flow index, seq, enqueue time, retransmission?)
    busy_until = 0.0
    drops = 0
    served = 0
    qtrace = []
    avg_q = 0.0
    codel_first_above = None
    codel_dropping = False
    codel_count = 0
    codel_next = 0.0
    next_trace = 0.0
    for i, f in enumerate(flows):
        f.name = f.name or f"{f.cc}{i}"
        if f.cc == "fixed":
            f.cwnd = f.window
            f.rto = 2 * f.rtt
        f.last_ack_time = f.start
        push(f.start, "send", i)

    def can_send(f, t):
        if f.size is not None and f.next_seq * MSS >= f.size and not f.retx_set:
            return False
        return len(f.inflight) < f.cwnd

    def transmit(i, seq, t, retx=False):
        nonlocal busy_until, drops, avg_q
        f = flows[i]
        f.inflight[seq] = t
        f.tx_count += 1
        f.tx_of[seq] = f.tx_count
        if retx:
            f.retransmits += 1
            f.retx_set.discard(seq)
        f.delivered_at[seq] = (t, f.delivered)
        # one-way to the bottleneck: half the propagation delay, then the queue
        push(t + f.rtt / 4, "arrive", (i, seq, retx))

    def enqueue(i, seq, retx, t):
        nonlocal drops, avg_q, busy_until
        if loss and rng.random() < loss:
            drops += 1
            return
        if qdisc == "red":
            lo, hi, pmax = red
            avg_q = 0.998 * avg_q + 0.002 * len(queue)
            x = (avg_q - lo * B) / max(1e-9, (hi - lo) * B)
            if x >= 1 or (x > 0 and rng.random() < pmax * x):
                drops += 1
                return
        if len(queue) >= B:
            drops += 1
            return
        queue.append((i, seq, t, retx))
        if len(queue) == 1 and busy_until <= t:
            busy_until = t + 1 / rate
            push(busy_until, "depart", None)

    def on_ack(i, seq, t, sent_t, delivered_before, retx):
        f = flows[i]
        if seq in f.acked:
            return
        f.acked.add(seq)
        f.inflight.pop(seq, None)
        f.delivered += 1
        if t >= warmup:
            f.delivered_warm += 1
        f.last_ack_time = t
        f.highest_acked = max(f.highest_acked, seq)
        f.highest_tx_acked = max(f.highest_tx_acked, f.tx_of.get(seq, -1))
        rtt = t - sent_t
        if not retx:                                  # Karn's rule
            f.rtts.append((t, rtt))
            if f.srtt is None:
                f.srtt, f.rttvar = rtt, rtt / 2
            else:
                f.rttvar = 0.75 * f.rttvar + 0.25 * abs(f.srtt - rtt)
                f.srtt = 0.875 * f.srtt + 0.125 * rtt
            if f.cc != "fixed":                       # 1986: a fixed timer that ignores queueing delay
                f.rto = max(0.2, f.srtt + 4 * f.rttvar)
            if rtt <= f.min_rtt:
                f.min_rtt, f.min_rtt_time = rtt, t
        # delivery rate sample (for BBR)
        if delivered_before is not None:
            st, d0 = delivered_before
            if t > st:
                f.bw_samples.append((t, (f.delivered - d0) / (t - st)))
        # loss detection: three later packets acknowledged
        lost = [s for s in f.inflight if f.tx_of.get(s, 0) + 3 <= f.highest_tx_acked]
        if lost:
            for s in lost:
                f.retx_set.add(s)
                f.inflight.pop(s, None)
            if f.cc not in ("bbr", "fixed") and min(lost) > f.recover:
                f.recover = f.next_seq
                if f.cc == "cubic":
                    f.w_max = f.cwnd
                    f.cwnd = max(2.0, f.cwnd * 0.7)
                    f.ssthresh = f.cwnd
                    f.epoch = t
                else:
                    f.cwnd = f.ssthresh = max(2.0, f.cwnd / 2)
            if f.cc != "bbr":                         # BBR's model ignores loss: it keeps updating
                return
        grow(f, t)

    def grow(f, t):
        if f.cc == "fixed":
            return
        if f.cc == "vegas":
            if f.cwnd < f.ssthresh and f.cwnd < 8:
                f.cwnd += 1
                return
            base_rtt = f.min_rtt if f.min_rtt < 1e9 else f.rtt
            cur = f.srtt or f.rtt
            diff = (f.cwnd / base_rtt - f.cwnd / cur) * base_rtt        # packets queued by this flow
            if diff < 2:
                f.cwnd += 1 / f.cwnd
            elif diff > 4:
                f.cwnd = max(2.0, f.cwnd - 1 / f.cwnd)
            return
        if f.cc == "bbr":
            recent = [b for (tt, b) in f.bw_samples if tt > t - 10 * (f.srtt or f.rtt)]
            f.bw_samples = f.bw_samples[-2000:]
            bw = max(recent) if recent else 2 / f.rtt
            rt = f.min_rtt if f.min_rtt < 1e9 else f.rtt
            if f.bbr_state == "startup":
                if bw > f.full_bw * 1.25:
                    f.full_bw, f.full_bw_count = bw, 0
                elif t - f.cycle_start > rt:
                    f.full_bw_count += 1
                    f.cycle_start = t
                    if f.full_bw_count >= 3:
                        f.bbr_state = "drain"
                gain = 2.885
            elif f.bbr_state == "probe_rtt":
                f.pacing = bw
                f.cwnd = 4.0
                if t >= f.probe_rtt_end:
                    f.bbr_state = "probe"
                    f.cycle_start = t
                return
            elif f.bbr_state == "drain":
                gain = 1 / 2.885
                if len(f.inflight) <= bw * rt:
                    f.bbr_state = "probe"
                    f.cycle_start = t
            else:
                if t - f.min_rtt_time > 10:                   # PROBE_RTT: drain to 4 packets, re-measure
                    f.bbr_state = "probe_rtt"
                    f.min_rtt = 1e9
                    f.probe_rtt_end = t + 0.2 + rt
                    f.cwnd = 4.0
                    return
                if t - f.cycle_start > rt:
                    f.cycle = (f.cycle + 1) % 8
                    f.cycle_start = t
                gain = [1.25, 0.75, 1, 1, 1, 1, 1, 1][f.cycle]
            f.pacing = gain * bw
            f.cwnd = max(4.0, bw * rt * (2.885 if f.bbr_state == "startup" else 2))
            return
        if f.cwnd < f.ssthresh:
            f.cwnd += 1
        elif f.cc == "cubic" and f.epoch is not None:
            C, beta = 0.4, 0.7
            K = (f.w_max * (1 - beta) / C) ** (1 / 3)
            target = C * (t - f.epoch - K) ** 3 + f.w_max
            reno = f.w_max * beta + 3 * (1 - beta) / (1 + beta) * (t - f.epoch) / (f.srtt or f.rtt)
            f.cwnd = max(f.cwnd + 0.01, min(target, f.cwnd * 1.5), reno)
        else:
            f.cwnd += 1 / f.cwnd

    t = 0.0
    while events:
        t, _, kind, data = heapq.heappop(events)
        if t > duration:
            break
        if t >= next_trace:
            qtrace.append((t, len(queue)))
            for f in flows:
                f.trace.append((t, f.cwnd))
            next_trace = t + trace_every
        if kind == "send":
            i = data
            f = flows[i]
            if t < f.start:
                continue
            # RTO
            oldest = min(f.inflight.values()) if (f.inflight and f.cc == "fixed") else None
            if f.inflight and (t - f.last_ack_time > f.rto or (oldest is not None and t - oldest > f.rto)):
                for s in list(f.inflight):
                    f.retx_set.add(s)
                f.inflight.clear()
                if f.cc not in ("bbr", "fixed"):
                    f.ssthresh = max(2.0, f.cwnd / 2)
                    f.cwnd = 1.0
                if f.cc == "fixed":                        # the pre-1988 behaviour: resend everything, same window
                    f.rto = max(0.2, 2 * f.rtt)
                f.recover = f.next_seq
                f.last_ack_time = t
                if f.cc != "fixed":
                    f.rto = min(60.0, f.rto * 2)
            sent_any = False
            while can_send(f, t):
                if f.cc == "bbr" and getattr(f, "pacing", None):
                    if t < f.pacing_next - 1e-12:
                        break
                    base_t = f.pacing_next if f.pacing_next > t - 2 / f.pacing else t
                    f.pacing_next = base_t + 1 / f.pacing
                if f.retx_set:
                    s = min(f.retx_set)
                    transmit(i, s, t, retx=True)
                else:
                    if f.size is not None and f.next_seq * MSS >= f.size:
                        break
                    transmit(i, f.next_seq, t)
                    f.next_seq += 1
                sent_any = True
            if f.size is not None and f.next_seq * MSS >= f.size and not f.inflight and not f.retx_set:
                if f.done_time is None:
                    f.done_time = t
                continue
            if f.cc == "bbr" and getattr(f, "pacing", None):
                push(max(f.pacing_next, t + 1e-6), "send", i)
            else:
                push(t + 1 / rate / 4 if sent_any else t + 1 / rate, "send", i)
        elif kind == "arrive":
            i, seq, retx = data
            enqueue(i, seq, retx, t)
        elif kind == "depart":
            if queue:
                i, seq, t0, retx = queue.pop(0)
                sojourn = t - t0
                drop = False
                if qdisc == "codel":
                    target, interval = codel
                    if sojourn < target or len(queue) < 2:
                        codel_first_above = None
                        codel_dropping = False
                    else:
                        if codel_first_above is None:
                            codel_first_above = t + interval
                        elif t >= codel_first_above and not codel_dropping:
                            codel_dropping, codel_count, codel_next = True, 1, t
                        if codel_dropping and t >= codel_next:
                            drop = True
                            codel_count += 1
                            codel_next = t + interval / math.sqrt(codel_count)
                if drop:
                    drops += 1
                else:
                    served += 1
                    f = flows[i]
                    d0 = f.delivered_at.get(seq)
                    sent_t = f.inflight.get(seq, t0)
                    at = t + f.rtt * 3 / 4
                    if f.jitter:                          # delayed, but in order (a FIFO path)
                        at = max(at + f.jitter * rng.random(), f.ack_sched)
                        f.ack_sched = at
                    push(at, "ack", (i, seq, sent_t, d0, retx))
                if queue:
                    busy_until = t + 1 / rate
                    push(busy_until, "depart", None)
        elif kind == "ack":
            i, seq, sent_t, d0, retx = data
            on_ack(i, seq, t, sent_t, d0, retx)
    T = min(t, duration)
    out = []
    for f in flows:
        dur = max(1e-9, (f.done_time or T) - max(f.start, warmup))
        out.append({"name": f.name, "cc": f.cc, "rtt": f.rtt, "delivered": f.delivered,
                    "mbps": (f.delivered_warm if warmup else f.delivered) * MSS * 8 / dur / 1e6, "retransmits": f.retransmits,
                    "trace": f.trace, "rtts": f.rtts[::max(1, len(f.rtts) // 400)], "done": f.done_time,
                    "srtt": f.srtt})
    return {"flows": out, "queue": qtrace, "drops": drops, "buffer": B, "bdp": bdp, "rate_pps": rate,
            "utilization": served / max(1e-9, T * rate), "time": T}


def mathis(rtt: float, p: float) -> float:
    """Throughput in Mb/s of a long Reno flow with random loss p: (MSS / RTT) sqrt(3/2) / sqrt(p)."""
    return MSS * 8 / rtt * math.sqrt(1.5 / p) / 1e6


def jain(xs) -> float:
    xs = list(xs)
    return sum(xs) ** 2 / (len(xs) * sum(x * x for x in xs))
