"""Every number in Part 32 of *Industry, Built* ("E-commerce"), from the Register, the Filing Room, the tables and the Works.

    python -m videos.industry.industry32.compute        # prints the film's numbers; writes .cache/industry32/computed.json

Items:
    hook        Amazon from its 1997 letter to 2025: revenue, its mix, and where the operating income came from
    run         the Run it marketplace: take rate, ad load and delivery promise, with both sides answering (the Works)
    models      shop against marketplace: what is counted as revenue; take rates from Shopify to Etsy
    dollar      a seller's dollar on a marketplace; Amazon's seller fees against its own costs of delivering
    fulfil      the cost of an order against volume and speed; Amazon's shipping costs; warehouse and courier jobs
    ads         advertising inside the shop: Amazon's, eBay's and PDD's; the Works' ad load
    traffic     the intermission's series: e-commerce's share of retail, its sales, and the jobs behind it
    cloud       Prime, Autoship and the cloud: subscriptions, and AWS's profit against the shops'
    world       China, Temu and the end of the de minimis rule; Latin America, Korea, Southeast Asia
    direct      direct brands: buying customers (the Works' brand), Wish, Allbirds and the others
    landscape   the companies by revenue and margin
    called      Wish's prospectus against what followed; this series' call on e-commerce's share
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.data.tables import table
from explainer.industry.register import get
from explainer.industry.works import marketplace as mk

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry32"

# ticker: (name, group, the registered rate that turns its currency into US dollars)
NAMES = {"AMZN": ("Amazon", "mixed", None), "EBAY": ("eBay", "market", None), "ETSY": ("Etsy", "market", None),
         "SHOP": ("Shopify", "tools", None), "W": ("Wayfair", "shop", None), "CHWY": ("Chewy", "shop", None),
         "MELI": ("MercadoLibre", "mixed", None), "CPNG": ("Coupang", "shop", None), "PDD": ("PDD (Temu)", "market", "pdd32.usd"),
         "JD": ("JD.com", "shop", "pdd32.usd"), "BABA": ("Alibaba", "market", "ba32.usd"), "SE": ("Sea (Shopee)", "mixed", None),
         "VIPS": ("Vipshop", "shop", "pdd32.usd"), "JMIA": ("Jumia", "market", None), "GLBE": ("Global-e", "tools", None),
         "RVLV": ("Revolve", "shop", None), "WRBY": ("Warby Parker", "brand", None), "BIRD": ("Allbirds", "brand", None),
         "CVNA": ("Carvana", "shop", None), "CART": ("Instacart", "delivery", None), "DASH": ("DoorDash", "delivery", None),
         "FIGS": ("FIGS", "brand", None), "BYON": ("Beyond (Overstock)", "shop", None)}


def _q(rows: list) -> dict:
    by: dict = collections.defaultdict(dict)
    for r in rows:
        by[r["series"]][str(r["month"])] = r["value"]
    return by


def _ym(p: str) -> float:
    return int(p[:4]) + (int(p[5:7]) - 0.5) / 12


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_ecom"):
        if r.get("revenue"):
            y, m = int(str(r["year_end"])[:4]), int(str(r["year_end"])[5:7])
            sec[r["ticker"]][y - 1 if m <= 3 else y] = r
    f = _q(read("fred_ecom"))
    last = {t: max(d) for t, d in sec.items()}

    def g(t, item, y=None):
        y = last[t] if y is None else y
        return sec[t][y].get(item) if y in sec[t] else None

    # the hook: Amazon
    groups = ("online", "physical", "3p", "subs", "ads", "aws", "other")
    mix = {k: table(f"amzn.{k}") for k in groups}
    years = list(range(2015, 2026))
    op = {k: table(f"amzn.op.{k}") for k in ("na", "intl", "aws")}
    R["hook"] = dict(l97=get("am32.l97"), cust97=get("am32.l97.cust"), down00=get("am32.l00"), rev=get("am32.sales"),
                     hist={y: sec["AMZN"][y]["revenue"] for y in range(2009, last["AMZN"] + 1)},
                     mix={k: {y: mix[k].get(y, 0) / 1e3 for y in years} for k in groups},
                     op={k: {y: op[k][y] / 1e3 for y in years} for k in op},
                     aws_share=get("am32.op.aws") / (get("am32.op.na") + get("am32.op.intl") + get("am32.op.aws")),
                     ads=get("am32.ads"), emp=get("am32.emp"))

    # Run it: the marketplace
    M = mk.Marketplace(basket=get("wk32.basket"), margin=get("wk32.margin"), take=get("wk32.take"), ad=get("wk32.ad"),
                       fixed_median=get("wk32.fixed"))
    takes = [float(round(x, 3)) for x in np.linspace(0.10, 0.45, 15)]
    ads = [float(round(x, 3)) for x in np.linspace(0.0, 0.14, 15)]
    days = [1.0, 1.5, 2.0, 3.0, 4.0]
    big = M.with_(buyers_max=4 * M.buyers_max, sellers_max=4 * M.sellers_max)
    R["run"] = dict(base=M.solve(), take=M.take, ad=M.ad, days=M.days, margin=M.margin, basket=M.basket,
                    by_take=M.sweep("take", takes), by_ad=M.sweep("ad", ads), by_days=M.sweep("days", days),
                    big_days={d: big.with_(days=d).solve() for d in days},
                    cpo={n: {d: mk.cost_per_order(n * 1e9, d) for d in (1.0, 2.0, 3.0)} for n in (0.25, 0.5, 1, 2, 3, 4, 6, 8)})

    # models: shop against marketplace
    tr = {"Shopify": 100 * g("SHOP", "revenue") / get("sh32.gmv"), "Shopee": 11.4,
          "eBay": get("eb32.take"), "Etsy": get("et32.take")}
    R["models"] = dict(take=tr, amzn_online=get("am32.online"), amzn_3p=get("am32.3p"), jd_product=get("jd32.product"),
                       jd_total=g("JD", "revenue"), jd_market=get("jd32.market"), jd_logi=get("jd32.logi"),
                       shop_gmv=get("sh32.gmv"), shop_rev=g("SHOP", "revenue"), shop_pay=get("sh32.pay"),
                       basket=get("wk32.basket"), take_works=get("wk32.take"))

    # a seller's dollar
    b = get("wk32.basket")
    ref = get("am32.referral") / 100
    goods = (1 - get("wk32.margin")) * b
    R["dollar"] = dict(basket=b, referral=ref * b, fulfil=(get("wk32.take") - ref) * b, ads=get("wk32.ad") * b, goods=goods,
                       keep=b - goods - get("wk32.take") * b - get("wk32.ad") * b, ftc=get("am32.ftc.half"),
                       amzn_3p=get("am32.3p"), amzn_ads=get("am32.ads"), amzn_ship=get("am32.ship"), amzn_fulfil=get("am32.fulfil"))

    # fulfilment
    R["fulfil"] = dict(ship=table("amzn.ship"), threep={y: table("amzn.3p")[y] / 1e3 for y in years},
                       ware={_ym(m): v for m, v in f["CES4349300001"].items() if m >= "2000-01"},
                       courier={_ym(m): v for m, v in f["CES4349200001"].items() if m >= "2000-01"},
                       coupang_sqft=get("cp32.sqft"), jd_fulfil=get("jd32.fulfil"), emp=get("am32.emp"))

    # advertising
    store_op = {y: (table("amzn.op.na")[y] + table("amzn.op.intl")[y]) / 1e3 for y in years}
    R["ads"] = dict(amzn={y: v / 1e3 for y, v in table("amzn.ads").items()}, store_op=store_op,
                    ebay=get("eb32.ads"), etsy=get("et32.services"), pdd_oms=get("pdd32.oms"),
                    pdd_share=100 * get("pdd32.oms") / (get("pdd32.oms") + get("pdd32.ts")),
                    q3=get("am32.q3.ads"), q3_prev=47.318)

    # traffic
    e = f["ECOMNSA"]
    R["traffic"] = dict(share={int(m[:4]) + (int(m[5:7]) - 1) / 12: v for m, v in f["ECOMPCTSA"].items()},
                        sales={y: sum(v for mm, v in e.items() if mm.startswith(str(y))) / 1e3
                               for y in range(2000, 2026)},
                        last=max(f["ECOMPCTSA"]), last_share=f["ECOMPCTSA"][max(f["ECOMPCTSA"])],
                        ware=R["fulfil"]["ware"], courier=R["fulfil"]["courier"])

    # the subscription and the cloud
    R["cloud"] = dict(subs={y: table("amzn.subs")[y] / 1e3 for y in years}, aws_op=R["hook"]["op"]["aws"], store_op=store_op,
                      autoship=get("ch32.autoship"), aws=get("am32.aws"), q3_aws=get("am32.q3.aws"))

    # the world
    rate = get("pdd32.usd")
    R["world"] = dict(pdd={2023: (get("pdd32.oms23"), get("pdd32.ts23")), 2025: (get("pdd32.oms"), get("pdd32.ts"))},
                      pdd_rev={y: sec["PDD"][y]["revenue"] / rate for y in sorted(sec["PDD"]) if y >= 2018},
                      jd=(get("jd32.product"), get("jd32.market"), get("jd32.logi")), baba_cmr=get("ba32.cmr"),
                      baba_quick=get("ba32.quick"), shopee=get("se32.gmv"), meli_gmv=get("ml32.gmv"), meli_tpv=get("ml32.tpv"),
                      cpng=get("cp32.cust"), cpng_rev=get("cp32.rev"), rate=rate)

    # direct brands
    B = mk.Brand(cac=get("wk32.cac"), retention=get("wk32.retention"))
    R["direct"] = dict(cac={c: B.with_(cac=c).cumulative(5) for c in (30.0, 60.0, 90.0)},
                       life={c: B.with_(cac=c).lifetime() for c in (30.0, 60.0, 90.0)},
                       payback={c: B.with_(cac=c).payback_year() for c in (30.0, 60.0, 90.0)},
                       first=B.first, repeat=B.repeat, margin=B.margin, retention=B.retention,
                       wish={y: (sec["WISH"][y]["revenue"], sec["WISH"][y]["marketing"]) for y in range(2018, 2024)},
                       brands={t: {y: sec[t][y]["revenue"] for y in sorted(sec[t])} for t in ("BIRD", "WRBY", "FIGS")},
                       mkt_share={NAMES[t][0]: 100 * g(t, "marketing") / g(t, "revenue")
                                  for t in ("BIRD", "WRBY", "FIGS", "RVLV", "W", "CHWY", "ETSY", "EBAY") if g(t, "marketing")},
                       wayfair_repeat=80.3, aov=get("w32.aov"))

    # landscape
    comp = []
    for tk, (nm, grp, rk) in NAMES.items():
        if tk not in sec:
            continue
        ys = sorted(sec[tk])
        y = ys[-1]
        div = get(rk) if rk else 1.0
        mm = [sec[tk][k]["profit"] / sec[tk][k]["revenue"] for k in ys if y - 4 <= k <= y and sec[tk][k].get("profit") is not None]
        comp.append(dict(name=nm, group=grp, rev=sec[tk][y]["revenue"] / div, margin=float(np.median(mm)), fy=y, tk=tk))
    R["landscape"] = dict(companies=comp)

    R["called"] = dict(wish=R["direct"]["wish"], mau=get("wish32.mau"), drop=get("wish32.drop"), sale=get("wish32.sale"),
                       sm=get("wish32.sm"), line=19.0, prob=0.45, share=R["traffic"]["share"], last_share=R["traffic"]["last_share"])
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    H = R["hook"]
    print("hook", H["rev"], round(H["aws_share"], 3), {y: round(v, 1) for y, v in H["hist"].items()})
    print("store op", {y: round(H["op"]["na"][y] + H["op"]["intl"][y], 1) for y in H["op"]["na"]})
    U = R["run"]
    pick = lambda s: {k: (round(v / 1e9, 2) if abs(v) > 1e5 else round(v, 3)) for k, v in s.items()}  # noqa: E731
    print("run base", pick(U["base"]))
    print("by take", {t: (round(s["sellers"] / 1e3), round(s["buyers"] / 1e6, 1), round(s["revenue"] / 1e9, 2), round(s["profit"] / 1e9, 2)) for t, s in U["by_take"].items()})
    print("by ad", {t: (round(s["buyers"] / 1e6, 1), round(s["ads"] / 1e9, 2), round(s["profit"] / 1e9, 2)) for t, s in U["by_ad"].items()})
    print("by days", {t: (round(s["buyers"] / 1e6, 1), round(s["cost_per_order"], 2), round(s["profit"] / 1e9, 2)) for t, s in U["by_days"].items()})
    print("big days", {t: (round(s["buyers"] / 1e6, 1), round(s["cost_per_order"], 2), round(s["profit"] / 1e9, 2)) for t, s in U["big_days"].items()})
    print("models", R["models"]["take"])
    print("dollar", {k: round(v, 2) for k, v in R["dollar"].items()})
    print("ads", R["ads"]["amzn"], {y: round(v, 1) for y, v in R["ads"]["store_op"].items()}, round(R["ads"]["pdd_share"], 1))
    T = R["traffic"]
    print("share", T["last"], T["last_share"], {y: round(v) for y, v in T["sales"].items() if y in (2000, 2010, 2019, 2020, 2025)})
    print("world", {k: v for k, v in R["world"].items() if k != "pdd_rev"}, {y: round(v, 1) for y, v in R["world"]["pdd_rev"].items()})
    D = R["direct"]
    print("direct", {c: [round(x) for x in v] for c, v in D["cac"].items()}, D["payback"], {c: round(v) for c, v in D["life"].items()})
    print("wish", D["wish"], {k: round(v, 1) for k, v in D["mkt_share"].items()})
    print("landscape", sorted([(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"]) for c in R["landscape"]["companies"]], key=lambda t: -t[1]))


if __name__ == "__main__":
    main()
