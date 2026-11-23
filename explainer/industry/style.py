"""The look of *Industry, Built*: one sans-serif face, one palette, used the same way in every part.

Colours carry meaning across the series: money is gold, profit green, cost red, the shop orange, and each link of a
chain keeps its colour from part to part (memory is always coral, chips violet).  Regions have fixed colours too,
so a map in Part 1 and a map in Part 57 read the same.
"""

from __future__ import annotations

from types import SimpleNamespace

FONT = "Inter"
FONT_DISPLAY = "Inter Display"
BACKGROUND = "#0E1117"

I = SimpleNamespace(  # noqa: E741  (the series palette, as E is Economics, Built's)
    TEXT="#E8EAED",
    DIM="#9AA3B2",
    FAINT="#5B6372",
    PANEL="#161B24",
    EDGE="#2A3140",
    ACCENT="#F2C14E",      # the series' accent: the price, the question
    MONEY="#F2C14E",
    PROFIT="#7BD88F",
    COST="#F25F5C",
    TAX="#6B7280",
    CHANNEL="#F2A65A",     # shops, carriers, distributors
    BRAND="#7EC8F5",       # the brand that designs and sells the product
    CHIP="#B58CFF",        # processors and the foundry that makes them
    MEMORY="#FF7A6B",      # DRAM and flash storage
    DISPLAY="#4FD1C5",
    CAMERA="#8FB4FF",
    RF="#F29AC1",          # modems, radios, antennas
    CASE="#C8B79A",        # glass, frame, enclosure
    POWER="#A3D977",       # battery, power management
    OTHER="#8B95A7",
    ASSEMBLY="#B0B8C8",    # assembly and test
    LABOUR="#D9A8F0",
    UNKNOWN="#4A5263",     # what the sources cannot split: drawn grey
)

# Regions keep their colours across the series.
REGION = {
    "US": "#5DA9E9",
    "China": "#E9655D",
    "Taiwan": "#A68CF2",
    "Korea": "#4FC3A1",
    "Japan": "#F2B84B",
    "Europe": "#8FA8C8",
    "India": "#F28C38",
    "SE Asia": "#C7D96A",
    "Other": "#6B7280",
}
REGION_NAME = {"US": "United States", "China": "China mainland", "Taiwan": "Taiwan", "Korea": "South Korea",
               "Japan": "Japan", "Europe": "Europe", "India": "India", "SE Asia": "Southeast Asia",
               "Other": "Elsewhere"}
