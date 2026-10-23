"""Write the computed results into README.md, between <!-- results --> and <!-- /results -->.

    python -m videos.ai.ai18.results
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np

from videos.ai.ai18.compute import CACHE, load


def lines() -> list[str]:
    out = []
    have = lambda n: CACHE.path(n).exists()  # noqa: E731
    if have("published"):
        P = load("published")
        out.append(f"* From published figures: Llama 3.1's 6ND = {P['llama_6nd']:.3g} FLOP (reported 3.8e25); its MFU "
                   f"from Table 4's TFLOP/s over 989: {', '.join(f'{100 * m:.1f}%' for m in P['llama_mfu'])} (reported "
                   f"43/41/38%); one unplanned interruption every {P['llama_mtbf_h']:.2f} h, about once in "
                   f"{P['llama_gpu_mtbf_years']:.1f} years per GPU; a full checkpoint ≈ {P['llama_ckpt_s']:.0f} s, Young's "
                   f"interval {P['llama_young_s'] / 60:.1f} min; PaLM's MFU without attention {100 * P['palm_mfu']:.1f}%; "
                   f"DeepSeek-V3 ${P['dsv3_usd'] / 1e6:.3f}M, {P['dsv3_days_per_T']:.2f} days per trillion tokens on 2,048 "
                   f"GPUs; 16 bytes/parameter: Llama 3.1 {P['mem16']['llama3'] / 1e12:.2f} TB (≥ {P['h100_needed']} "
                   f"H100s); ZeRO's example {', '.join(f'{m:.2f}' for m in P['zero_mem'])} GB.")
    if have("web"):
        W = load("web")
        out.append(f"* Common Crawl sample ({W['crawl']}, WET files {W['files']}): {W['n_pages']:,} pages, "
                   f"{W['n_langs']} languages; {W['blocked']} blocked by URL; English {dict(W['langs'])['en']:,}, of which "
                   f"{W['english']:,} kept (p ≥ 0.65, ≥ 50 words). WARC slices: {W['warc_pages']} HTML pages, "
                   f"{W['html_bytes'] / 1e6:.1f} MB of HTML → {W['extracted_bytes'] / 1e6:.2f} MB of text "
                   f"({100 * W['extracted_share']:.1f}%; median page {100 * W['median_ratio']:.1f}%).")
    if have("dedup"):
        D = load("dedup")
        worst = max(abs(b["measured"] - b["predicted"]) for b in D["bins"])
        out.append(f"* MinHash-LSH (112 hashes, 14 × 8): on {len(D['pair_s']):,} page pairs, per-hash agreement vs Jaccard "
                   f"mean gap {D['agree_err']:.3f}; measured collision rate within {worst:.3f} of 1 − (1 − s⁸)¹⁴ in every "
                   f"bin; s at P = ½: {D['s_half']:.3f}. Sample: {D['exact']} exact and {D['removed']} near duplicates of "
                   f"{D['n']:,}. Gutenberg licences: {D['foot_caught']}/{D['foot_pairs']} pairs caught (J ≥ "
                   f"{D['foot_jaccard'][0]:.3f}); novels {D['body_caught']}/{D['body_pairs']}.")
    if have("quality"):
        Q = load("quality")
        out.append(f"* Quality classifier (fastText, {Q['n_train']:,} of FineWeb-Edu's Llama 3 annotations; cut "
                   f"{Q['cut']:.2f} on P(score ≥ 3)): F1 {100 * Q['f1']:.1f}% (precision {100 * Q['precision']:.1f}%, "
                   f"recall {100 * Q['recall']:.1f}%) on {Q['n_test']:,} held-out pages, against FineWeb-Edu's 82%; "
                   f"kept {Q['cc_kept_n']} of {Q['cc_n']:,} crawl pages ({100 * Q['cc_kept']:.1f}%).")
    if have("contamination"):
        K = load("contamination")
        out.append(f"* Contamination: the scoreboard's passage shares {K['passage_hits']} of {K['passage_grams']:,} "
                   f"13-grams ({K['passage_hits8']} of {K['passage_grams8']:,} 8-grams) with the training text; "
                   f"{K['valid_flagged']} of {K['valid_paras']:,} held-out paragraphs share a 13-gram.")
    if have("mixture"):
        M = load("mixture")
        t = M["tests"]
        row = "; ".join(f"{n} {np.mean([t[f'test_{n}_{s}']['test'] for s in (0, 1)]):.3f}"
                        for n in ("natural", "uniform", "regmix"))
        out.append(f"* RegMix on the novels: {len(M['proxy'])} proxy runs, leave-one-out correlation "
                   f"{M['loo_corr']:.2f}; pick {', '.join(f'{100 * w:.0f}%' for w in M['best'])} (natural "
                   f"{', '.join(f'{100 * w:.0f}%' for w in M['natural'])}); loss on the scoreboard's chapter, nats per "
                   f"token, mean of two seeds: {row}.")
    if have("collapse"):
        Cl = load("collapse")
        r, a = np.asarray(Cl["replace"]).mean(0), np.asarray(Cl["accumulate"]).mean(0)
        out.append(f"* Model collapse (unigram, {Cl['n']:,} samples, {Cl['gens']} generations, {Cl['seeds']} seeds): "
                   f"support {r[0, 0]:.0f} → {r[-1, 0]:.0f} tokens (replace) vs {a[-1, 0]:.0f} (accumulate); "
                   f"cross-entropy on real text {r[0, 1]:.2f} → {r[-1, 1]:.2f} vs {a[-1, 1]:.2f} bits.")
    if have("accounting"):
        A = load("accounting")
        out.append(f"* FLOP counter (our 128 × 4 model, {A['T']} tokens): backward/forward {A['ratio']:.3f}; total / 6NT "
                   f"{A['both'] / A['six']:.4f}; attention adds {100 * A['attn_share'] / (1 - A['attn_share']):.1f}%; "
                   f"recomputation {100 * (A['ckpt_ratio'] - 1):.1f}% more. Activations: {A['per_fused']:.2f} d per token "
                   f"per layer (FP32, fused attention), {A['per_recompute']:.2f} d recomputed, unfused attention + "
                   f"{A['quad_per_head']:.2f} T² per head per layer.")
    if have("collectives"):
        Cc = load("collectives")
        out.append(f"* Collectives (gloo, {Cc['p']} processes): α = {Cc['alpha'] * 1e6:.0f} µs, B = {Cc['B'] / 1e9:.2f} "
                   f"GB/s from point-to-point; large messages took "
                   f"{', '.join(f'{k} {v:.1f}×' for k, v in Cc['ratio'].items())} the α–β prediction (load average "
                   f"{Cc['loadavg_before'][0]:.0f} on 4 cores); sums checked: {Cc['ok']}.")
    if have("parallel"):
        Pr = load("parallel")
        out.append(f"* Parallelism checked on 4 processes ({Pr['n_params']:,}-parameter model, {Pr['steps']} AdamW steps): "
                   f"largest parameter difference from one process, DP {Pr['err']['dp']:.1e}, ZeRO-3 "
                   f"{Pr['err']['zero3']:.1e}; ZeRO-3 keeps {Pr['persistent_dp'] / Pr['persistent_z3']:.2f}× less and "
                   f"sends {Pr['sent_z3'] / Pr['sent_dp']:.2f}× more. Tensor parallel (2 / 4 ranks): output error "
                   f"{Pr['tp']['2']['err_y']:.1e} / {Pr['tp']['4']['err_y']:.1e}. Ring attention: {Pr['ring']['err']:.1e}.")
    if have("pipeline"):
        Pp = load("pipeline")
        out.append(f"* Pipeline (p = {Pp['p']}, m = {Pp['m']}, simulated): bubble GPipe {100 * Pp['gpipe']['bubble']:.1f}%, "
                   f"1F1B {100 * Pp['1f1b']['bubble']:.1f}%, interleaved {100 * Pp['interleaved']['bubble']:.1f}%, ZB-H1 "
                   f"{100 * Pp['zb']['bubble']:.1f}% (all equal to their formulas); peak micro-batches on GPU 0: GPipe "
                   f"{Pp['gpipe']['peak'][0]:.0f}, 1F1B {Pp['1f1b']['peak'][0]:.0f}.")
    if have("precision"):
        Pc = load("precision")
        f = Pc["final"]
        out.append("* Precision (250 steps, two seeds, final held-out loss): " +
                   "; ".join(f"{k} {min(v):.3f}–{max(v):.3f}" for k, v in f.items()) +
                   f". Activation gradients: {100 * Pc['hist']['below_normal']:.0f}% below FP16's smallest normal, "
                   f"{100 * Pc['hist']['below_sub']:.0f}% flushed to zero. E4M3 error on the series' model: per tensor "
                   f"{100 * Pc['qerr']['act_tensor']:.2f}%, per 1 × 128 tile {100 * Pc['qerr']['act_tile']:.2f}%.")
    if have("precision_acc"):
        A = load("precision_acc")
        out.append(f"* FP16 with {A['accum']}-way accumulation: " +
                   "; ".join(f"{k} {min(v):.3f}–{max(v):.3f}" for k, v in A["final"].items()) + ".")
    if have("stability"):
        S = load("stability")
        rows = []
        for c in S["configs"]:
            rows.append(f"{c}: " + ", ".join(f"{np.mean(v):.2f}" for v in S["final"][c]) + " (max logit " +
                        ", ".join(f"{max(v):.0f}" for v in S["maxlogit"][c]) + ")")
        out.append(f"* Stability (learning rates {S['lrs']}, final loss, mean of 2 seeds): " + "; ".join(rows) + ".")
    if have("mtp"):
        Mt, MC = load("mtp"), load("mtp_cost")
        out.append(f"* MTP ({Mt['steps']} steps, two seeds): next-token loss without {np.mean(Mt['final']['0']):.3f}, with "
                   f"{np.mean(Mt['final']['0.3']):.3f}; acceptance {', '.join(f'{100 * a:.1f}%' for a in Mt['accept'])}; "
                   f"extra arithmetic {100 * MC['extra_share']:.0f}%.")
    if have("recipe"):
        R = load("recipe")
        sb = lambda k: " / ".join(f"{v:.3f}" for v in R[k].get("seeds_bits", [R[k]["bits"]]))  # noqa: E731
        sv = lambda k: " / ".join(f"{v:.3f}" for v in R[k].get("seeds_val", [R[k]["val"]]))  # noqa: E731
        out.append(f"* Recipes (3.0M tokens, 732 steps, seed 0 / seed 1): 2020 held-out {sv('base')}, {sb('base')} bpc; "
                   f"2026 {sv('full')}, {sb('full')} bpc; largest attention logit "
                   f"{R['base']['max_logit']:.0f} vs {R['full']['max_logit']:.0f} (seed 0); WSD cooldown branch at "
                   f"{R['branch']['steps']} steps {R['branch']['val']:.3f} vs {R['branch']['stable_val']:.3f} still stable.")
    if have("mfu"):
        Mf = load("mfu")
        out.append(f"* MFU on this CPU (peak {Mf['peak'] / 1e9:.1f} GFLOP/s, one core): 2020 recipe "
                   f"{100 * Mf['base']['mfu']:.0f}%, 2026 recipe {100 * Mf['full']['mfu']:.0f}%.")
    return out


def main():
    path = Path(__file__).parent / "README.md"
    s = path.read_text()
    body = "\n".join(lines())
    s = re.sub(r"<!-- results -->.*?<!-- /results -->", "<!-- results -->\n" + body + "\n<!-- /results -->", s,
               flags=re.S)
    path.write_text(s)
    print(body)


if __name__ == "__main__":
    main()
