"""Part 16's computed results as Markdown, for the README's Results section:

    python -m videos.ai.ai16.results
"""

from __future__ import annotations

import numpy as np

from videos.ai.ai16.compute import load


def ms(v):
    a = np.asarray(v, float)
    return f"{a.mean():.3f} ({a.min():.3f}–{a.max():.3f})"


def main():
    out = []
    m = load("moe")
    out.append("* Mixture against dense (held-out bits per character, mean (range) of 3 seeds, 2,000 steps): dense with the "
               f"mixture's arithmetic {ms(m['dense_active_valid'])}, the mixture {ms(m['moe_valid'])}, dense with its "
               f"parameters {ms(m['dense_total_valid'])}; on the scoreboard's passage {np.mean(m['dense_active_passage']):.3f}, "
               f"{np.mean(m['moe_passage']):.3f}, {np.mean(m['dense_total_passage']):.3f}. Parameters (total/used per "
               f"character): {m['dense_active_counts']['total']:,}/{m['dense_active_counts']['active']:,}, "
               f"{m['moe_counts']['total']:,}/{m['moe_counts']['active']:,}, {m['dense_total_counts']['total']:,}.")
    sp = load("speed")
    out.append(f"* Milliseconds per training step on one core: dense {1e3 * sp['dense_active']:.0f}, mixture "
               f"{1e3 * sp['moe']:.0f}, wide dense {1e3 * sp['dense_total']:.0f}.")
    b = load("balance")
    for k, nm in (("none", "no balancing"), ("aux", "Switch's loss"), ("moe", "loss-free bias")):
        out.append(f"* {nm}: busiest expert {np.mean(b[f'{k}_busiest']):.2f}× a fair share (end, mean over seeds and "
                   f"blocks), starved experts {int(np.sum(b[f'{k}_starved']))} of 48, MaxVio {np.mean(b[f'{k}_maxvio']):.2f}, "
                   f"bits {ms(b[f'{k}_valid'])}.")
    f = load("fine")
    out.append(f"* Coarse / fine / fine + shared (2 seeds): {ms(f['moe_valid'])}, {ms(f['fine_valid'])}, "
               f"{ms(f['shared_valid'])}.")
    c = load("capacity")
    i1 = list(c["cfs"]).index(1.0)
    out.append("* Token-slots dropped at capacity factor 1 (imposed after training): " + ", ".join(
        f"{k} {100 * np.mean(np.asarray(c[f'{k}_drops'])[:, i1]):.1f}%" for k in ("none", "aux", "moe"))
        + f"; trained with c = 1: {ms(c['cf_train_valid'])} against {ms(c['nocf_train_valid'])}.")
    p = load("parallel")
    out.append("* Four simulated GPUs, busiest GPU's share × 4: " + ", ".join(
        f"{k} {p[f'{k}_slowdown']:.2f}" for k in ("none", "aux", "moe"))
               + f". DeepSeek-V3: {p['v3_bytes']:,.0f} bytes and {p['v3_flops'] / 1e6:.0f} MFLOP per token per MoE layer "
               f"({p['v3_intensity']:,.0f} FLOP/byte) against {p['ridge_ib']:,.0f} for FP8 over InfiniBand.")
    a = load("accounting")
    out.append(f"* DeepSeek-V3 counted from its config: {a['v3']['total'] / 1e9:.1f}B total, "
               f"{a['v3']['active_with_embed'] / 1e9:.1f}B active ({a['v3']['active'] / 1e9:.1f}B without the input "
               f"embedding); Mixtral {a['mixtral']['total'] / 1e9:.2f}B / {a['mixtral']['active'] / 1e9:.2f}B.")
    u = load("upcycle")
    out.append(f"* Upcycling (2 seeds): kept dense {ms(u['dense_half_valid'])}, upcycled {ms(u['upcycled_valid'])}, "
               f"mixture from scratch {ms(u['moe_valid'])}; upcycled training compute "
               f"{100 * u['compute_up'] / u['compute_moe']:.0f}% of from scratch.")
    s = load("special")
    for li in range(2):
        out.append(f"* Mutual information, block {li + 1} (bits, 3 seeds): previous "
                   f"{np.mean([s[f'moe_s{k}_l{li}']['prv'] for k in range(3)]):.2f}, current "
                   f"{np.mean([s[f'moe_s{k}_l{li}']['cur'] for k in range(3)]):.2f}, next "
                   f"{np.mean([s[f'moe_s{k}_l{li}']['nxt'] for k in range(3)]):.2f}, shuffled "
                   f"{np.mean([s[f'moe_s{k}_l{li}']['shuf'] for k in range(3)]):.3f}.")
    d = load("mod")
    out.append("* Mixture-of-depths (MFLOP per character, bits, 2 seeds): " + "; ".join(
        f"{k} {d[f'{k}_flops'] / 1e6:.2f}, {ms(d[f'{k}_valid'])}" for k in d["names"])
        + f". Deciding causally, the 12.5% model routes {100 * np.mean(d['mod12_causal_frac']):.0f}% and scores "
          f"{ms(d['mod12_causal'])}.")
    g = load("gradcheck")
    out.append(f"* Router gradient: formula and autograd agree with finite differences to "
               f"{g['softmax-k']['err_analytic']:.1e} (relative); our MoE layer's router to {g['layer_err']:.1e}.")
    mx = load("mix1991")
    out.append(f"* 1991 mixture: the gate's trust in its favourite expert {ms(mx['compete_sharp_final'])} competing, "
               f"{ms(mx['cooperate_sharp_final'])} cooperating.")
    r = load("recall")
    out.append("* Recall (8 keys per query, 2 seeds): " + ", ".join(
        f"{k} {100 * np.mean(r[f'{k}_acc']):.0f}%" for k in r["modes"]) + "; imposed on the full model: " + ", ".join(
        f"{k} {100 * np.mean(r[f'imposed_{k}_acc']):.0f}%" for k in ("window", "blocks", "topk")) + ".")
    t = load("topk")
    out.append(f"* Part 13's transformer: all keys {t['full']:.3f} bits; 8 keys by score {t['bits_topk'][1]:.3f}, "
               f"a window of 8 {t['bits_window'][1]:.3f}.")
    lt = load("lottery")
    for sd in lt["seeds"]:
        out.append(f"* Lottery seed {sd}: dense {lt[f'dense_s{sd}']:.3f}; at {100 * lt[f'remain_s{sd}'][-1]:.0f}% of the "
                   f"weights: ticket {lt[f'ticket_s{sd}'][-1]:.3f}, re-initialized {lt[f'reinit_s{sd}'][-1]:.3f}, random "
                   f"mask {lt[f'random_s{sd}'][-1]:.3f}.")
    pr = load("prune24")
    out.append("* 2:4 on the dense model (3 seeds): dense " + ms([pr[f"dense_s{s}"] for s in pr["seeds"]]) + "; " + "; ".join(
        f"{k} " + ms([pr[f"{k}_s{s}"] for s in pr["seeds"]]) for k in pr["methods"]) + "; retrained magnitude 2:4 "
        + ms([pr[f"magnitude_24_ft_s{s}"] for s in pr["seeds"]]) + ", Wanda 2:4 " + ms([pr[f"wanda_24_ft_s{s}"] for s in pr["seeds"]]) + ".")
    ac = load("actsparse")
    B = np.asarray([ac[f"bits_s{s}"] for s in ac["seeds"]], float)
    out.append("* Activations zeroed (share, bits): " + ", ".join(f"{100 * fr:.0f}% {b:.3f}" for fr, b in zip(ac["fracs"], B.mean(0))) + ".")
    S = load("scoreboard")
    out.append("* Scoreboard rows: " + ", ".join(f"{r_['label']} {r_['bits']:.3f}" for r_ in S["rows"] if r_["part"] == 16) + ".")
    print("\n".join(out))


if __name__ == "__main__":
    main()
