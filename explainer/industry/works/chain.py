"""A chain: where a customer's payment goes, link by link (Part 1; reused wherever a Dollar is drawn).

Three calculations, each small enough to check by hand:

* :func:`dollar` splits a retail price into the shop's margin, the parts, assembly, other costs of sales, the brand's
  operating costs, its tax and its profit.  The slices always sum to the price (tested).
* :func:`value_added` takes the sales of each firm along a chain and returns what each one *adds*: its sales minus
  what it bought from the link before.  Adding sales counts the same dollar again at every link; adding value added
  gives back the final price exactly.
* :func:`per_unit` turns a firm's segment revenue, units and gross margin into revenue and gross profit per unit.
* :func:`tier_passthrough` compares, storage tier by storage tier, a price increase with the increase in memory
  cost, given DRAM per phone and flash per gigabyte in two years.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Slice:
    key: str
    label: str
    amount: float
    group: str               # "channel", "parts", "assembly", "other", "opex", "tax", "profit"
    who: str = ""            # the firms the money goes to, for the label
    lo: float | None = None  # a range, where the slice is uncertain
    hi: float | None = None


@dataclass
class Dollar:
    price: float
    slices: list = field(default_factory=list)

    def total(self) -> float:
        return sum(s.amount for s in self.slices)

    def get(self, key: str) -> Slice:
        for s in self.slices:
            if s.key == key:
                return s
        raise KeyError(key)

    def group(self, group: str) -> float:
        return sum(s.amount for s in self.slices if s.group == group)


# The parts of a premium phone, as shares of its bill of materials (this series' estimate from teardown houses'
# published splits: the display and the processor were the two largest lines before 2026; memory was about a tenth).
PREMIUM_PARTS_2025 = (
    ("display", "Display", 0.17, "Samsung Display, LG Display"),
    ("chip", "Processor", 0.16, "designed by Apple, made by TSMC"),
    ("camera", "Cameras", 0.15, "Sony sensors; Largan, LG Innotek"),
    ("rf", "Modem and radios", 0.14, "Qualcomm, Broadcom, Murata, Skyworks"),
    ("memory", "Memory and storage", 0.10, "Samsung, SK hynix, Micron, Kioxia"),
    ("case", "Frame and glass", 0.09, "Corning; enclosure makers"),
    ("power", "Battery and power", 0.05, "cell makers in China; TI"),
    ("other", "Everything else", 0.14, "audio, haptics, sensors, board"),
)


def parts(bom: float, shares=PREMIUM_PARTS_2025, memory: float | None = None) -> list[Slice]:
    """The bill of materials as slices.  With ``memory`` given, memory takes that amount and the other parts share
    the rest of ``bom`` in their original proportions."""
    out = []
    mem_share = dict((k, s) for k, _, s, _ in shares)["memory"]
    rest = bom - (memory if memory is not None else mem_share * bom)
    for k, label, s, who in shares:
        amt = (memory if k == "memory" else rest * s / (1 - mem_share)) if memory is not None else s * bom
        out.append(Slice(k, label, amt, "parts", who))
    return out


def dollar(price: float, bom: float, *, indirect_share: float, channel_margin: float, assembly: float,
           other_cogs: float, opex_ratio: float, tax_rate: float, memory: float | None = None,
           shares=PREMIUM_PARTS_2025) -> Dollar:
    """Split a retail ``price`` (before sales tax) into the slices of the chain.

    The shop or carrier keeps ``channel_margin`` on the ``indirect_share`` of units it sells; the brand's own stores
    keep it all.  The brand's operating costs are ``opex_ratio`` of its revenue (its R&D and selling costs spread
    evenly over everything it sells), and tax is ``tax_rate`` of its operating profit."""
    channel = price * indirect_share * channel_margin
    revenue = price - channel
    gross = revenue - bom - assembly - other_cogs
    opex = opex_ratio * revenue
    pretax = gross - opex
    tax = tax_rate * pretax
    d = Dollar(price)
    d.slices.append(Slice("channel", "Shop or carrier", channel, "channel", "AT&T, Verizon, Best Buy ..."))
    d.slices += parts(bom, shares, memory)
    d.slices.append(Slice("assembly", "Assembly and test", assembly, "assembly", "Foxconn, Luxshare, Tata"))
    d.slices.append(Slice("other_cogs", "Shipping, warranty, licences", other_cogs, "other"))
    d.slices.append(Slice("opex", "Apple: research and selling", opex, "opex", "Apple"))
    d.slices.append(Slice("tax", "Income tax", tax, "tax", "governments"))
    d.slices.append(Slice("profit", "Apple's profit", pretax - tax, "profit", "Apple's shareholders"))
    return d


def value_added(chain: list[tuple[str, float]]) -> list[tuple[str, float, float]]:
    """[(firm, its sales)] in order along the chain -> [(firm, sales, value added)].  Each firm is taken to buy only
    from the firm before it, so value added is its sales minus the previous firm's."""
    out, prev = [], 0.0
    for firm, sales in chain:
        out.append((firm, sales, sales - prev))
        prev = sales
    return out


def per_unit(revenue: float, units: float, gross_margin: float) -> tuple[float, float]:
    """Revenue and gross profit per unit (same money unit as ``revenue``; ``units`` in the same scale)."""
    r = revenue / units
    return r, r * gross_margin


def tier_passthrough(sizes_gb, price_old, price_new, dram_old, dram_new, nand_gb_old, nand_gb_new):
    """For each storage size: (size, price change, memory-cost change, the part the brand absorbs)."""
    out = []
    for gb, p0, p1 in zip(sizes_gb, price_old, price_new):
        dmem = (dram_new - dram_old) + gb * (nand_gb_new - nand_gb_old)
        out.append((gb, p1 - p0, dmem, dmem - (p1 - p0)))
    return out
