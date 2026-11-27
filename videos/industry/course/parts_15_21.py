"""Act III, Making (Parts 15-21)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=15, level="U", widget="fab", prereq=(4, 5, 6),
        question="Why do the most advanced chips come from so few factories?",
        story="The part opens with Gordon Moore's article of April 1965 (the components on the most economical chip "
              "doubling every year, 65,000 by 1975) and with Hsinchu in 1987, where TSMC set out to make other "
              "companies' chips and design none of its own; in 2025 it made 12,682 products for 534 customers. The "
              "viewer chooses between building a $20bn fab and booking a foundry at $17,000 a wafer: at 5,000 wafers a "
              "month a good die costs $29 from the foundry and $183 from a half-empty fab still learning its process, "
              "and owning first pays at about 32,000. A chip is a loop of film, resist, light and etch repeated layer on "
              "layer; a 300 mm wafer holds about 640 dies of 100 mm2, and random defects make an 800 mm2 die yield half "
              "as often. TSMC spends a third to a half of its revenue on fabs every year, used about 88% of its capacity "
              "in 2025 and earned about $8,100 a wafer. The industry split into fabless designers (Nvidia, from $6.9bn "
              "to $215.9bn of revenue without a fab) and foundries, while Intel's foundry lost $10.3bn in 2025; ASML is "
              "the only maker of EUV machines. America's chip output rose about 5,089 times since 1972 as the real price "
              "fell 98%. Memory swings from loss to boom (Micron, from a $2.3bn quarterly operating loss to $43.8bn of "
              "operating profit in a quarter); the analog makers ride cars and factories. High-performance computing rose "
              "from 43% to 68% of TSMC's revenue; its three 2-3 nm fabs are all in Taiwan; America subsidizes fabs at "
              "home and restricts who may buy. WSTS forecast $975bn for 2026 and sales passed $1.22 trillion by "
              "September; the series calls more than $1.8 trillion for the year (65%).",
        handoff="Part 16, electronics, follows the chips into the devices, and asks why the company that builds the device "
                "keeps the least of it.",
        outside="Percentages, logarithms and exponentials; Part 4's fixed and variable costs; Part 5's moats; Part 6's cycle.",
        objectives={
            "U": ["Explain how a chip is made, and why a fab costs the same whether it is full or empty.",
                  "Explain the split between fabless designers, foundries and integrated makers, and why it happened.",
                  "Explain why the most advanced chips come from a few fabs, one foundry and one maker of machines."],
            "M": ["Compute gross dies on a wafer, the yield at a defect density and the cost of a good die.",
                  "Compute a fab's cost per wafer at a given loading and the volume at which owning beats booking.",
                  "Compute a doubling time from two counts, and what operating leverage does to a memory maker's profit."],
            "D": ["Score two forecasts (Moore's of 1965 and WSTS's of December 2025) and say which assumption failed.",
                  "Judge how much of the 2026 boom is price and how much volume, and what would end it."],
            "I": ["Read a foundry's revenue by node and platform, its utilization and its capital spending in a 20-F.",
                  "Place a chip company on the map: foundry, fabless, integrated, memory, equipment, design software."],
        },
        results=[
            ("Gross dies", r"N = \frac{\pi r^2}{A} - \frac{\pi d}{\sqrt{2A}}"),
            ("Yield", r"Y = e^{-A D}"),
            ("Cost of a good die", r"c = \frac{F/(12v) + c_w}{N\,Y}"),
            ("Doubling time", r"T = \frac{t_1 - t_0}{\log_2(n_1/n_0)}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, "s09_intermission", 8, 9, 10, 11), I=(12,), D=(13,),
        also=(("The Register's rows for Part 15", "explainer/industry/data/rows_p15.py"),
              ("Dies, yield, the learning curve, the fab and Run it", "explainer/industry/works/fab.py"),
              ("TSMC's fabs", "explainer/industry/data/tables.py"),
              ("FRED, Our World in Data, the SEC's foreign filers and the companies' accounts",
               "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=16, level="U", widget="assembler", prereq=(1, 4, 5, 15),
        question="Why does the company that builds the device keep the least of it?",
        story="The part opens with Stan Shih, the founder of Acer, who in 1992 drew the value added along the computer "
              "industry and found 'a smile-shaped curve', with manufacturing at the bottom. In 2025 Hon Hai (Foxconn) took "
              "in NT$8.1 trillion, about $260bn, and kept 2.3 cents in the dollar; Apple kept 28 cents of $479bn. The viewer "
              "runs an assembler offered 20 million devices a year at $30 each if it builds an $800m plant: worth -$194m "
              "if the brand moves the work after three years and +$420m if it renews, so the plant pays only above a 32% "
              "chance of renewal. A device is assembled on a surface-mount line and by hand; Apple's hardware is made by "
              "partners in China, India, Japan, South Korea, Taiwan and Vietnam. The Works' $900 device splits into parts, "
              "a $30 fee and the brand's $260 of profit: the smile from arithmetic. Six contract manufacturers kept 0-5 "
              "cents a year for fifteen years; turnkey revenue makes the margin look thin (3% against 50% on the fee), and "
              "Hon Hai turns its assets 1.6 times a year for a 9.6% return on equity. Its servers overtook its phones in "
              "2025, its largest customer fell from 54% to 44% of revenue, and its servers arm earned 4.7 cents against "
              "1.4. Apple's services earn a 76% gross margin. Connector makers keep 10-20 cents; LG Display lost money in "
              "six of ten years. Televisions' price index fell 99.4% since 1951. Intel's PC chips earned 29-35% while HP's "
              "and Dell's PCs earned 5-8%, and HP's printing 18.7%. US server imports rose from $23bn (2017) to $165bn "
              "(2025). Hon Hai's assets in China shrank while Vietnam's, America's, Mexico's and India's grew. Tariffs "
              "from 2018 hardly moved phones or laptops until 2023-25; then China's share of US phone imports fell from 81% "
              "to 45% and of laptops from 66% to 18%, and the Supreme Court struck down the emergency tariffs in February "
              "2026. The Commerce Secretary's 2025 forecast that iPhone assembly would come to America has not come true; "
              "the series calls India above half of US smartphone imports in 2026 (55%).",
        handoff="Part 17, cars, turns to a product whose makers also struggle to keep much of what they sell.",
        outside="Percentages and discounting; Part 1's phone and its dollar; Part 4's fixed costs; Part 5's moats; Part 15's chips.",
        objectives={
            "U": ["Explain Shih's smile: why value added is high at the parts and brand ends and low in assembly.",
                  "Explain how a device is assembled, and who does the work for which brands.",
                  "Explain why tariffs moved assembly slowly, and where it went."],
            "M": ["Value a plant built for one customer's order, with and without renewal, and find the break-even chance.",
                  "Show how turnkey revenue changes an assembler's margin without changing its profit.",
                  "Decompose a return on equity into margin, asset turnover and leverage."],
            "D": ["Score a forecast (the Commerce Secretary's, April 2025) against trade and employment data.",
                  "Judge how far a quality-adjusted price index measures what buyers gained."],
            "I": ["Read an assembler's segment, customer and geographic notes (Hon Hai's) and a brand's gross margins.",
                  "Read customs data by partner to see where a product is assembled, and when it moved."],
        },
        results=[
            ("Plant value", r"V(p) = V_{\text{order}} + p\,V_{\text{renewal}}"),
            ("Break-even renewal", r"p^* = -V_{\text{order}} / V_{\text{renewal}}"),
            ("Turnkey margin", r"m = \frac{\pi}{q\,(\text{parts} + \text{fee})}"),
            ("DuPont", r"\frac{NI}{E} = \frac{NI}{S}\cdot\frac{S}{A}\cdot\frac{A}{E}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, "s09_intermission", 8, 9, 10, 11), I=(12,), D=(13,),
        also=(("The Register's rows for Part 16", "explainer/industry/data/rows_p16.py"),
              ("The device, the assembler and Run it", "explainer/industry/works/device.py"),
              ("UN Comtrade, BLS, FRED, the SEC extracts and Hon Hai's statements", "explainer/industry/data/SOURCES.md")),
    ),
]
