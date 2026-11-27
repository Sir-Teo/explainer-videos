"""The Works' chemical plants (Part 12): a steam cracker that can run on ethane or naphtha, its cost of a tonne of
ethylene at a site with local gas and world oil prices, the world price set by the dearest cracker still needed, and
an industrial gas plant at a customer's fence under a long contract.

Yields are EIA's (AEO2026 Industrial Demand Module assumptions, Table 6, from the American Chemistry Council's
Ethylene Product Stewardship Manual).  Heating values are textbook figures.  Prices of ethane and naphtha relative to
gas and crude, the energy a cracker burns and its other cash costs are this series' assumptions, stated here and
labelled as a model on screen.  No manim here.
"""

from __future__ import annotations

from dataclasses import dataclass

# tonnes of product per tonne of feed (EIA, AEO2026 IDM assumptions, Table 6)
YIELDS = {
    "ethane": {"hydrogen": 0.0591, "methane": 0.0704, "ethylene": 0.8091, "propylene": 0.0194, "butadiene": 0.0178,
               "butylenes": 0.0081, "benzene": 0.0081, "toluene": 0.0008, "xylene": 0.0, "aromatics": 0.0073,
               "fuel oil": 0.0},
    "naphtha": {"hydrogen": 0.0097, "methane": 0.1694, "ethylene": 0.3867, "propylene": 0.1547, "butadiene": 0.0476,
                "butylenes": 0.0507, "benzene": 0.0437, "toluene": 0.0166, "xylene": 0.0224, "aromatics": 0.0735,
                "fuel oil": 0.0251},
}
FUEL_GASES = ("hydrogen", "methane")            # burned in the plant's own furnaces, worth what gas costs
# higher heating values, million Btu per tonne (MJ/kg / 1.05506)
MMBTU_PER_T = {"hydrogen": 141.8 / 1.05506, "methane": 55.5 / 1.05506, "ethane": 51.9 / 1.05506}

# --- this series' assumptions -----------------------------------------------------------------------------------
ETHANE_FEE = 60.0          # $ a tonne over ethane's value as gas: fractionation and pipeline
NAPHTHA_BBL_PER_T = 9.0    # barrels in a tonne of naphtha
NAPHTHA_TO_CRUDE = 0.9     # naphtha's price relative to Brent, per barrel
COPRODUCT_PREMIUM = 1.1    # propylene, butadiene, aromatics and the rest sold at this multiple of naphtha's price
ENERGY = {"ethane": 17.0, "naphtha": 25.0}   # million Btu of fuel per tonne of ethylene, before the fuel gases made
OTHER_CASH = 150.0         # $ a tonne of ethylene: labour, maintenance, catalysts, utilities other than fuel


def feed_price(feed: str, gas: float, brent: float) -> float:
    """$ a tonne of feed: ethane at its value as gas plus a fee; naphtha at a fixed share of Brent."""
    if feed == "ethane":
        return gas * MMBTU_PER_T["ethane"] + ETHANE_FEE
    return brent * NAPHTHA_BBL_PER_T * NAPHTHA_TO_CRUDE


@dataclass
class Cracker:
    feed: str              # "ethane" or "naphtha"
    capacity: float = 1.5  # million tonnes of ethylene a year
    fixed: float = 150.0   # $ million a year that do not vary with output
    capex: float = 6000.0  # $ million to build

    @property
    def y(self) -> dict:
        return YIELDS[self.feed]

    def credits(self, gas: float, brent: float) -> float:
        """$ of co-products per tonne of feed: fuel gases at the local gas price, the rest at a premium to naphtha."""
        naphtha = brent * NAPHTHA_BBL_PER_T * NAPHTHA_TO_CRUDE
        c = 0.0
        for k, v in self.y.items():
            if k == "ethylene":
                continue
            c += v * (gas * MMBTU_PER_T[k] if k in FUEL_GASES else naphtha * COPRODUCT_PREMIUM)
        return c

    def cost(self, gas: float, brent: float, gas_feed: float | None = None) -> float:
        """Cash cost of a tonne of ethylene: feed less co-product credits, per tonne of ethylene, plus fuel at the local
        gas price and other cash costs.  ``gas_feed`` prices ethane when its market differs from the fuel gas."""
        g_feed = gas if gas_feed is None else gas_feed
        net_feed = feed_price(self.feed, g_feed, brent) - self.credits(gas, brent)
        return net_feed / self.y["ethylene"] + ENERGY[self.feed] * gas + OTHER_CASH

    def breakdown(self, gas: float, brent: float) -> dict:
        f = feed_price(self.feed, gas, brent) / self.y["ethylene"]
        cr = self.credits(gas, brent) / self.y["ethylene"]
        return {"feed": f, "credits": cr, "fuel": ENERGY[self.feed] * gas, "other": OTHER_CASH,
                "cost": f - cr + ENERGY[self.feed] * gas + OTHER_CASH, "feed_per_t": 1 / self.y["ethylene"]}

    def margin(self, price: float, gas: float, brent: float) -> float:
        """$ million a year at full output."""
        return (price - self.cost(gas, brent)) * self.capacity - self.fixed


def world_price(costs: list[float], markup: float = 50.0) -> float:
    """The world price of ethylene in a well-supplied market: the cash cost of the dearest cracker still needed, plus a
    little.  Here, the highest of the sites' costs (the marginal plant), as on Part 4's cost curve."""
    return max(costs) + markup


def play(years: list[int], gas: dict, brent: dict, site_gas: dict, markup: float = 50.0) -> dict:
    """Run a Texas ethane cracker and a European naphtha cracker through history.  ``site_gas`` maps a site name to its
    gas price series; the price each year is set by the dearest of the sites (with ``markup``).  Returns each site's
    cost and margin a tonne, and the price, by year."""
    sites = {"Texas, ethane": Cracker("ethane"), "Europe, naphtha": Cracker("naphtha"), "Asia, naphtha": Cracker("naphtha")}
    gas_of = {"Texas, ethane": "US", "Europe, naphtha": "EU", "Asia, naphtha": "Asia"}
    out = {s: {"cost": {}, "margin": {}} for s in sites}
    out["price"] = {}
    for y in years:
        costs = {s: c.cost(site_gas[gas_of[s]][y], brent[y]) for s, c in sites.items()}
        p = world_price(list(costs.values()), markup)
        out["price"][y] = p
        for s in sites:
            out[s]["cost"][y] = costs[s]
            out[s]["margin"][y] = p - costs[s]
    return out


# ------------------------------------------------------------------------------------------- industrial gases
@dataclass
class GasPlant:
    """An air separation unit at a customer's fence, under a long contract with a minimum purchase (take-or-pay)."""
    capex: float = 400.0        # $ million
    years: int = 15             # contract length
    capacity: float = 1.0       # million tonnes of oxygen a year
    fee: float = 75.0           # $ million a year, fixed facility fee the customer pays whatever it takes
    price: float = 40.0         # $ a tonne for what it actually takes
    cash_cost: float = 25.0     # $ a tonne (mostly power)
    minimum: float = 0.8        # share of capacity paid for even if not taken

    def cash(self, taken: float) -> float:
        """$ million in a year when the customer takes ``taken`` (share of capacity)."""
        billed = max(taken, self.minimum)
        return self.fee + billed * self.capacity * self.price - taken * self.capacity * self.cash_cost

    def npv(self, taken: list[float], rate: float = 0.08) -> float:
        return -self.capex + sum(self.cash(t) / (1 + rate) ** (k + 1) for k, t in enumerate(taken))


def haber(n2: float = 1.0) -> dict:
    """N2 + 3 H2 -> 2 NH3: tonnes of hydrogen and of ammonia for ``n2`` tonnes of nitrogen."""
    n, h = 14.007, 1.008
    return {"hydrogen": n2 * 3 * 2 * h / (2 * n), "ammonia": n2 * 2 * (n + 3 * h) / (2 * n)}
