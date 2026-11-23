"""Lab 1: split a phone's price into the chain's slices, value added and per-phone profit, and test the 2026 memory shock."""

import numpy as np

from videos.coursekit import labs
from explainer.industry.register import get, span
from explainer.industry.works import chain

TITLE = "Where the money goes: the Dollar of one phone"
GOAL = ("Rebuild the film's Dollar of a $1,099 phone from the Register's figures, sample its uncertain inputs over "
        "their ranges to see how far Apple's profit per phone can move, and redo it for the 2026 phone, when memory "
        "became the scarce link.")
TASKS = [
    "Set the channel margin to 0 (every phone sold in Apple's own stores) and then to 15%. How many dollars of "
    "Apple's profit per phone does the channel decide?",
    "Using the per-phone function, compute Samsung's mobile revenue per phone for 2025 from its results (MX revenue "
    "KRW 114.4 trillion, 241.2 million phones shipped, KRW 1,421 to the dollar). Why does this overstate the phone's "
    "price?",
    "Raise the 2026 memory cost from $244 to $300 per phone. What price rise would keep Apple's profit per phone at "
    "its 2025 level?",
]


def dollar(price, bom, memory=None, channel=None, assembly=None, other=None):
    return chain.dollar(
        price, bom, memory=memory,
        indirect_share=get("apple.indirect_share.fy2026"),
        channel_margin=get("assume.channel_margin") if channel is None else channel,
        assembly=get("assume.assembly") if assembly is None else assembly,
        other_cogs=get("assume.other_cogs") if other is None else other,
        opex_ratio=get("apple.opex.fy2025") / get("apple.revenue.fy2025"),
        tax_rate=get("apple.taxrate.fy2025"))


def run(seed=0):
    lab = labs.Lab()
    rng = np.random.default_rng(seed)

    # 1. The Dollar of the 2025 phone, and its slices summing to the price
    p17, bom17 = get("price.17pro.256"), get("bom.17pro")
    d = dollar(p17, bom17)
    assert abs(d.total() - p17) < 1e-6
    lab.row("2025 phone: Apple's profit per phone (central)", f"${d.get('profit').amount:.0f}")

    # 2. Monte Carlo over the uncertain inputs, uniform on each range
    lo_b, hi_b = span("bom.17pro")
    lo_c, hi_c = span("assume.channel_margin")
    lo_a, hi_a = span("assume.assembly")
    lo_o, hi_o = span("assume.other_cogs")
    draws = np.array([dollar(p17, rng.uniform(lo_b, hi_b), channel=rng.uniform(lo_c, hi_c),
                             assembly=rng.uniform(lo_a, hi_a), other=rng.uniform(lo_o, hi_o)).get("profit").amount
                      for _ in range(4000)])
    q05, q50, q95 = np.quantile(draws, [0.05, 0.5, 0.95])
    lab.row("profit per phone, 5th to 95th percentile", f"${q05:.0f} to ${q95:.0f} (median ${q50:.0f})")
    worst = dollar(p17, hi_b, channel=hi_c, assembly=hi_a, other=hi_o).get("profit").amount
    best = dollar(p17, lo_b, channel=lo_c, assembly=lo_a, other=lo_o).get("profit").amount
    assert worst - 1e-9 <= draws.min() and draws.max() <= best + 1e-9  # the corners bound every draw

    # 3. Value added along a chain sums to the price; sales do not
    chip = d.get("chip").amount
    links = [("wafer", 0.12 * chip), ("TSMC", chip), ("Apple", p17 - d.get("channel").amount), ("shop", p17)]
    va = chain.value_added(links)
    assert abs(sum(a for _, _, a in va) - p17) < 1e-9 and sum(s for _, s, _ in va) > 2 * p17 - 100
    lab.row("value added along the chain / sales along the chain", f"${sum(a for _, _, a in va):,.0f} / "
            f"${sum(s for _, s, _ in va):,.0f}")

    # 4. Per phone: Apple against Xiaomi
    units = get("share.apple.units.2025") - get("share.apple.units.q4_2025") + get("share.apple.units.q4_2024")
    a_rev, a_gp = chain.per_unit(get("apple.iphone_sales.fy2025") * 1e3, units, get("apple.gm_products.fy2025"))
    x_rev, x_gp = chain.per_unit(get("xiaomi.phone_rev.2025") * 1e3 / get("fx.cny.2025"),
                                 get("xiaomi.phone_units.2025"), get("xiaomi.phone_gm.2025"))
    lab.row("gross profit per phone: Apple / Xiaomi", f"${a_gp:.0f} / ${x_gp:.0f} (x{a_gp / x_gp:.0f})")
    assert a_gp / x_gp > 10

    # 5. The 2026 phone: memory at TrendForce's 34% of a bill 38% larger
    p18 = get("price.18pro.256")
    bom18 = bom17 * (1 + get("bom.rise.18pro"))
    mem18 = get("bom.memory_share.2026") * bom18
    e = dollar(p18, bom18, memory=mem18)
    lab.row("2026 phone: memory per phone, Apple's profit", f"${mem18:.0f}, ${e.get('profit').amount:.0f}")
    assert e.get("profit").amount < d.get("profit").amount  # a $100 rise does not cover the memory

    # 6. Storage tiers: the 2TB price rise against its memory-cost rise
    tiers = chain.tier_passthrough((256, 512, 1024, 2048), (1199, 1399, 1599, 1999), (1299, 1499, 1899, 2499),
                                   get("memory.dram.2025"), get("memory.dram.2026"),
                                   get("memory.nand256.2025") / 256, get("memory.nand256.2026") / 256)
    lab.row("2TB: price rise / memory-cost rise", f"+${tiers[-1][1]} / +${tiers[-1][2]:.0f}")
    assert 380 < tiers[-1][2] < 520

    fig, (ax1, ax2) = labs.figure(2)
    keys = ["channel", "parts", "assembly", "other_cogs", "opex", "tax", "profit"]
    names = ["shop", "parts", "assembly", "other costs", "Apple's costs", "tax", "Apple's profit"]
    cols = [labs.ORANGE, labs.GREY, labs.BLUE, labs.GREY, labs.BLUE, labs.GREY, labs.GREEN]
    for x, dd in ((0, d), (1, e)):
        vals = [dd.get("channel").amount, dd.group("parts"), dd.get("assembly").amount, dd.get("other_cogs").amount,
                dd.get("opex").amount, dd.get("tax").amount, dd.get("profit").amount]
        bottom = 0
        for k, (v, c) in enumerate(zip(vals, cols)):
            ax1.bar(x, v, bottom=bottom, color=c, alpha=0.55 + 0.45 * (k % 2), width=0.55,
                    label=names[k] if x == 0 else None)
            bottom += v
    ax1.set_xticks([0, 1], ["2025: $1,099", "2026: $1,199"])
    ax1.set_ylabel("dollars per phone")
    ax1.set_title("The Dollar of one iPhone Pro (256GB)")
    ax1.legend(fontsize=7, loc="upper left")
    gb = [t[0] for t in tiers]
    x = np.arange(len(gb))
    ax2.bar(x - 0.18, [t[1] for t in tiers], 0.36, color=labs.GOLD, label="price rise")
    ax2.bar(x + 0.18, [t[2] for t in tiers], 0.36, color=labs.RED, label="memory-cost rise (WSJ)")
    ax2.set_xticks(x, ["256GB", "512GB", "1TB", "2TB"])
    ax2.set_ylabel("dollars per phone, 2025 to 2026")
    ax2.set_title("iPhone Pro Max: who pays for the memory")
    ax2.legend(fontsize=8)
    lab.fig = fig
    lab.note = ("The slices always sum to the price. Between the 5th and 95th percentiles the uncertain inputs move "
                "Apple's profit per phone by about $60 either way; the 2026 memory shock took about $100.")
    return lab
