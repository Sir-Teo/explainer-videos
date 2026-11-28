"""Register rows for Part 32, *E-commerce*.  Checked 2026-11-28.

The Forms 10-K for 2025 of Amazon, eBay, Etsy, Shopify, MercadoLibre, Coupang and Wayfair and Chewy's for fiscal 2025;
Amazon's 10-Qs for the third quarters of 2025 and 2026; the 20-Fs for 2025 of PDD, JD and Sea and Alibaba's for fiscal
2026; Amazon's letters to shareholders for 1997 (as reprinted with the 2008 letter) and 2000; ContextLogic's (Wish's)
prospectus of November 2020 and its 10-Ks for 2022 and 2024; the FTC's release of 26 September 2023; Amazon's seller
pricing page.  Series are the Filing Room's SEC and FRED extracts and Amazon's revenue table in ``tables.py``.
"""

from explainer.industry.register import Row, add

C = "2026-11-28"
P = (32,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
AMZN = SEC + "1018724/000101872426000004/amzn-20251231.htm"
AMZNQ25 = SEC + "1018724/000101872425000123/amzn-20250930.htm"
AMZNQ26 = SEC + "1018724/000101872426000040/amzn-20260930.htm"
AMZN23 = SEC + "1018724/000101872424000008/amzn-20231231.htm"
L97 = SEC + "1018724/000119312509081096/dex991.htm"
L00 = SEC + "1018724/000103221001500339/dex991.txt"
EBAY = SEC + "1065088/000106508826000027/ebay-20251231.htm"
ETSY = SEC + "1370637/000137063726000019/etsy-20251231.htm"
SHOP = SEC + "1594805/000159480526000007/shop-20251231.htm"
MELI = SEC + "1099590/000109959026000006/meli-20251231.htm"
CPNG = SEC + "1834584/000183458426000024/cpng-20251231.htm"
W = SEC + "1616707/000161670726000027/w-20251231.htm"
CHWY = SEC + "1766502/000176650226000034/chwy-20260201.htm"
PDD = SEC + "1737806/000110465926050727/pdd-20251231x20f.htm"
JD = SEC + "1549802/000119312526157870/d53690d20f.htm"
BABA = SEC + "1577552/000119312526231755/baba-20260331.htm"
SE = SEC + "1703399/000114036126015366/ef20067274_20f.htm"
WISHS1 = SEC + "1822250/000119312520298630/d82777ds1.htm"
WISH22 = SEC + "1822250/000095017023004711/wish-20221231.htm"
WISH24 = SEC + "1822250/000095017025037990/logc-20241231.htm"
FTC = "https://www.ftc.gov/news-events/news/press-releases/2023/09/ftc-sues-amazon-illegally-maintaining-monopoly-power"
AMZP = "https://sell.amazon.com/pricing"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def am(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Amazon.com, Form 10-K for 2025", AMZN, fact)


def wk(key, value, unit, definition, lo, hi):
    return r(key, value, unit, definition, "this series' assumption", "", "", kind="assumption", lo=lo, hi=hi)


add(
    # Amazon
    am("am32.sales", 716.924, "US$ billion", "net sales, 2025 ($638.0bn in 2024)"),
    am("am32.online", 269.287, "US$ billion", "online stores: product sales and digital media where Amazon records revenue gross, 2025"),
    am("am32.3p", 172.162, "US$ billion", "third-party seller services: 'commissions and any related fulfillment and shipping fees, and other "
       "third-party seller services', 2025"),
    am("am32.ads", 68.635, "US$ billion", "advertising services: 'sponsored ads, display, and video advertising', 2025 ($56.2bn in 2024)"),
    am("am32.subs", 49.619, "US$ billion", "subscription services, including Amazon Prime fees, 2025"),
    am("am32.aws", 128.725, "US$ billion", "AWS net sales, 2025"),
    am("am32.op.na", 29.619, "US$ billion", "North America segment operating income, 2025 ($24.967bn in 2024)"),
    am("am32.op.intl", 4.750, "US$ billion", "International segment operating income, 2025 ($3.792bn in 2024)"),
    am("am32.op.aws", 45.606, "US$ billion", "AWS segment operating income, 2025 ($39.834bn in 2024)"),
    am("am32.ship", 102.7, "US$ billion", "shipping costs, 2025 ($95.8bn in 2024), in cost of sales"),
    am("am32.fulfil", 109.074, "US$ billion", "fulfillment expense, 2025: operating and staffing fulfillment centers, physical stores and customer "
       "service, and payment processing"),
    am("am32.tech", 108.521, "US$ billion", "technology and infrastructure expense, 2025"),
    am("am32.mkt", 47.129, "US$ billion", "sales and marketing expense, 2025"),
    am("am32.emp", 1576000, "people", "approximately 1,576,000 full-time and part-time employees at 31 December 2025"),
    am("am32.3pdef", 1, "flag", "third-party seller services: 'We are not the seller of record in these transactions'"),
    am("am32.china", 1, "flag", "'China-based sellers account for significant portions of our third-party seller services and "
       "advertising revenues'"),
    am("am32.fixed", 1, "flag", "'Our variable costs include ... picking, packaging, and preparing orders for shipment, transportation ... Our "
       "fixed costs include the costs necessary to build and run our technology infrastructure ... and to build and optimize "
       "our fulfillment network'"),
    r("am32.ftc.settle", 2.5, "US$ billion", "'During Q3 2025, we recorded $2.5 billion of expense related to the settlement of a lawsuit "
      "with the Federal Trade Commission (FTC)'", "Amazon.com, Form 10-Q for the third quarter of 2025", AMZNQ25, "2025-09-30"),
    r("am32.ftc.suit", 1, "flag", "the FTC's suit 'in September 2023 in the W.D. Wash.' alleges that 'Amazon has a monopoly in markets for "
      "online superstores and marketplace services' maintained through practices 'relating to our pricing policies, advertising "
      "practices, the structure of Prime, and promotion of our own products on our website'", "Amazon.com, Form 10-K for 2023",
      AMZN23, "2023-09"),
    r("am32.ftc.ads", 22, "states", "'In August 2026, the Federal Trade Commission and 22 state Attorneys General filed a complaint' alleging "
      "'that Amazon harmed advertisers through, among other things, misrepresentations, omissions, and unfair business practices "
      "involving the use of reserve prices in Amazon's sponsored ad auctions'; Amazon disputes the allegations",
      "Amazon.com, Form 10-Q for the third quarter of 2026", AMZNQ26, "2026-08"),
    r("am32.q3.3p", 134.850, "US$ billion", "third-party seller services, nine months to 30 September 2026 ($119.3bn a year before)",
      "Amazon.com, Form 10-Q for the third quarter of 2026", AMZNQ26, "2026-09-30"),
    r("am32.q3.ads", 56.689, "US$ billion", "advertising services, nine months to 30 September 2026 ($47.3bn a year before)",
      "Amazon.com, Form 10-Q for the third quarter of 2026", AMZNQ26, "2026-09-30"),
    r("am32.q3.aws", 125.803, "US$ billion", "AWS net sales, nine months to 30 September 2026 ($93.1bn a year before)",
      "Amazon.com, Form 10-Q for the third quarter of 2026", AMZNQ26, "2026-09-30"),
    r("am32.l97", 147.8, "US$ million", "1997 revenue: 'by year-end, we had served more than 1.5 million customers, yielding 838% revenue "
      "growth to $147.8 million'; 'this is Day 1 for the Internet'; 'When forced to choose between optimizing the appearance of our "
      "GAAP accounting and maximizing the present value of future cash flows, we'll take the cash flows'",
      "Amazon.com, 1997 letter to shareholders (reprinted with the 2008 letter, Form 8-K of April 2009)", L97, "1998"),
    r("am32.l97.cust", 1.5, "million", "customers served by the end of 1997", "Amazon.com, 1997 letter to shareholders", L97, "1997"),
    r("am32.l00", 80, "percent", "'Ouch. It's been a brutal year for many in the capital markets and certainly for Amazon.com "
      "shareholders. As of this writing, our shares are down more than 80% from when I wrote you last year'; sales of $2.76bn in "
      "2000 from $1.64bn in 1999; 20 million customers", "Amazon.com, 2000 letter to shareholders (Form 8-K of April 2001)", L00, "2001-04"),
    r("am32.ftc.half", 50, "percent", "the FTC's allegation: 'Combined, all of these fees force many sellers to pay close to 50% of their "
      "total revenues to Amazon'", "Federal Trade Commission, press release of 26 September 2023", FTC, "2023-09-26", kind="official"),
    r("am32.referral", 15, "percent", "referral fee for many categories (for example backpacks, handbags and luggage; footwear; beauty, "
      "health and personal care above $10); 8% for computers and consumer electronics; minimum $0.30; the Professional plan is "
      "$39.99 a month", "Amazon, 'Pricing' (selling on Amazon), US store", AMZP, "2026-11-28", kind="press",
      note="Amazon's own published fee schedule, read on the date checked"),

    # eBay, Etsy, Shopify
    r("eb32.gmv", 79.609, "US$ billion", "GMV, 2025 ($74.7bn in 2024); 51% outside the United States", "eBay, Form 10-K for 2025", EBAY, "2025"),
    r("eb32.take", 13.94, "percent", "take rate (net revenues over GMV), 2025 (13.77% in 2024)", "eBay, Form 10-K for 2025", EBAY, "2025"),
    r("eb32.ads", 1.993, "US$ billion", "advertising revenues, 2025, mostly Promoted Listings ($1.69bn in 2024 on the same basis)",
      "eBay, Form 10-K for 2025", EBAY, "2025"),
    r("eb32.buyers", 135, "million", "active buyers at the end of 2025, with 2.5 billion live listings", "eBay, Form 10-K for 2025", EBAY, "2025"),
    r("et32.gms", 11.917, "US$ billion", "gross merchandise sales, 2025 ($12.587bn in 2024), of which the Etsy marketplace $10.46bn",
      "Etsy, Form 10-K for 2025", ETSY, "2025"),
    r("et32.take", 24.2, "percent", "revenue take rate, 2025 (22.3% in 2024)", "Etsy, Form 10-K for 2025", ETSY, "2025"),
    r("et32.services", 0.876, "US$ billion", "services revenue (on-site advertising and shipping labels), 2025, up 11.3%",
      "Etsy, Form 10-K for 2025", ETSY, "2025"),
    r("et32.buyers", 86.5, "million", "Etsy marketplace active buyers at 31 December 2025, with 5.6 million active sellers",
      "Etsy, Form 10-K for 2025", ETSY, "2025-12-31"),
    r("et32.fees", 0.20, "US$", "listing fee per item; 'Etsy Payments processing fees, which typically vary between 3.0% and 6.5%'",
      "Etsy, Form 10-K for 2025", ETSY, "2025"),
    r("sh32.gmv", 378.441, "US$ billion", "GMV facilitated, 2025 ($292.3bn in 2024, $235.9bn in 2023)", "Shopify, Form 10-K for 2025", SHOP, "2025"),
    r("sh32.mrr", 205, "US$ million", "monthly recurring revenue at the end of 2025", "Shopify, Form 10-K for 2025", SHOP, "2025-12-31"),
    r("sh32.pay", 65.6, "percent", "Shopify Payments penetration, 2025: GMV of $248.1bn processed through it (61.9% in 2024)",
      "Shopify, Form 10-K for 2025", SHOP, "2025"),
    r("sh32.merch", 76, "percent", "merchant solutions' share of total revenues, 2025 (subscription solutions 24%)",
      "Shopify, Form 10-K for 2025", SHOP, "2025"),

    # MercadoLibre, Coupang, Sea, China
    r("ml32.gmv", 65.037, "US$ billion", "gross merchandise volume, 2025 ($51.5bn in 2024); 2,429 million items sold; 121 million unique "
      "active buyers", "MercadoLibre, Form 10-K for 2025", MELI, "2025"),
    r("ml32.tpv", 277.823, "US$ billion", "Mercado Pago total payment volume, 2025; 78 million fintech monthly active users",
      "MercadoLibre, Form 10-K for 2025", MELI, "2025"),
    r("cp32.cust", 24.6, "million", "Product Commerce active customers in the fourth quarter of 2025 (22.8 million a year before)",
      "Coupang, Form 10-K for 2025", CPNG, "2025-12-31"),
    r("cp32.sqft", 78, "million square feet", "'over 78 million square feet of fulfillment, logistics, and other operating spaces'",
      "Coupang, Form 10-K for 2025", CPNG, "2025"),
    r("cp32.rev", 29.592, "US$ billion", "Product Commerce net revenues, 2025", "Coupang, Form 10-K for 2025", CPNG, "2025"),
    r("se32.gmv", 127.4, "US$ billion", "Shopee GMV, 2025 ($100.5bn in 2024), with 13.9 billion gross orders; e-commerce service revenue "
      "11.4% of GMV (10.8% in 2024)", "Sea Limited, Form 20-F for 2025", SE, "2025"),
    r("pdd32.oms", 217.783, "RMB billion", "online marketing services and others, 2025 (50.4% of revenues; 62.0% in 2023)",
      "PDD Holdings, Form 20-F for 2025", PDD, "2025"),
    r("pdd32.ts", 214.063, "RMB billion", "transaction services, 2025 (49.6% of revenues; RMB94.1bn, 38.0%, in 2023)",
      "PDD Holdings, Form 20-F for 2025", PDD, "2025"),
    r("pdd32.ts23", 94.099, "RMB billion", "transaction services, 2023", "PDD Holdings, Form 20-F for 2025", PDD, "2023"),
    r("pdd32.oms23", 153.541, "RMB billion", "online marketing services and others, 2023", "PDD Holdings, Form 20-F for 2025", PDD, "2023"),
    r("pdd32.temu", 1, "flag", "'following its initial launch in North America in September 2022, Temu expanded to Oceania in March 2023 "
      "and Europe in April 2023'", "PDD Holdings, Form 20-F for 2025", PDD, "2022-09"),
    r("pdd32.minimis", 1, "flag", "US de minimis (Section 321): 'Effective May 2, 2025, this exemption ceased to apply for low-value imports "
      "from China. Effective August 29, 2025, this exemption was eliminated for imports from all countries'",
      "PDD Holdings, Form 20-F for 2025", PDD, "2025-08-29"),
    r("pdd32.usd", 6.9931, "RMB per US$", "the convenience translation rate at 31 December 2025 (H.10)", "PDD Holdings, Form 20-F for 2025",
      PDD, "2025-12-31"),
    r("jd32.product", 1023.802, "RMB billion", "net product revenues, 2025 (78.2% of total net revenues of RMB1,309.1bn)",
      "JD.com, Form 20-F for 2025", JD, "2025"),
    r("jd32.market", 107.131, "RMB billion", "marketplace and marketing revenues, 2025", "JD.com, Form 20-F for 2025", JD, "2025"),
    r("jd32.logi", 178.152, "RMB billion", "logistics and other service revenues, 2025", "JD.com, Form 20-F for 2025", JD, "2025"),
    r("jd32.fulfil", 88.176, "RMB billion", "fulfillment expense, 2025", "JD.com, Form 20-F for 2025", JD, "2025"),
    r("ba32.cmr", 343.867, "RMB billion", "customer management revenue of Taobao and Tmall, fiscal year to 31 March 2026",
      "Alibaba Group, Form 20-F for fiscal 2026", BABA, "FY2026"),
    r("ba32.quick", 78.520, "RMB billion", "quick commerce revenue, fiscal 2026, up 47%", "Alibaba Group, Form 20-F for fiscal 2026", BABA, "FY2026"),
    r("ba32.usd", 6.8980, "RMB per US$", "the convenience translation rate at 31 March 2026", "Alibaba Group, Form 20-F for fiscal 2026",
      BABA, "2026-03-31"),

    # Direct retailers
    r("w32.aov", 312, "US$", "average order value, 2025 ($300 in 2024); 21 million active customers; 40 million orders delivered; 80.3% of "
      "orders from repeat customers", "Wayfair, Form 10-K for 2025", W, "2025"),
    r("ch32.autoship", 83.3, "percent", "Autoship customer sales as a percentage of net sales, fiscal 2025 (79.2% in 2024, 76.2% in 2023); "
      "21.3 million active customers", "Chewy, Form 10-K for fiscal 2025", CHWY, "FY2025"),

    # Wish
    r("wish32.mau", 100, "million", "'connecting more than 100 million monthly active users ... in over 100 countries to over 500,000 "
      "merchants offering approximately 150 million items'; 'one of the largest and fastest growing global ecommerce platforms'; "
      "'Today, most of our merchants are based in China'",
      "ContextLogic (Wish), Form S-1, 20 November 2020", WISHS1, "2020-11-20"),
    r("wish32.sm", 78, "percent", "sales and marketing expense as a percentage of revenue, 2019 (91% in 2018; 64% in the nine months to "
      "September 2020)", "ContextLogic (Wish), Form S-1, 20 November 2020", WISHS1, "2019"),
    r("wish32.drop", 68, "percent", "'MAUs decreased approximately 68% from the year ended December 31, 2022 compared to the year ended "
      "December 31, 2021. We believe this decline was primarily driven by our decision to significantly reduce our digital "
      "advertising expenditures'", "ContextLogic (Wish), Form 10-K for 2022", WISH22, "2022"),
    r("wish32.sale", 162, "US$ million", "sale of substantially all its operating assets to Qoo10 for 'a purchase price equal to $162 "
      "million in cash, after giving effect to the purchase price adjustments' (approved 18 April 2024)",
      "ContextLogic, Form 10-K for 2024", WISH24, "2024-04"),

    # The Works
    wk("wk32.basket", 40.0, "US$", "a marketplace order's value", 25.0, 60.0),
    wk("wk32.margin", 0.55, "share of price", "a seller's price less the cost of its goods, before platform fees", 0.40, 0.70),
    wk("wk32.take", 0.30, "share of GMV", "commission and fulfilment fees the platform charges", 0.15, 0.40),
    wk("wk32.ad", 0.06, "share of GMV", "sellers' spending on ads on the platform", 0.02, 0.12),
    wk("wk32.fixed", 60000.0, "US$ a year", "a median seller's own fixed costs", 20000.0, 150000.0),
    wk("wk32.cac", 60.0, "US$", "a direct brand's cost of acquiring a customer", 30.0, 150.0),
    wk("wk32.retention", 0.40, "share a year", "the share of a direct brand's customers still buying a year later", 0.2, 0.6),
)
