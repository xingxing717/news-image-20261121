[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/xingxing717/news-image-20261121/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/xingxing717/news-image-20261121/reward.svg)](https://make.fun/c/news-image-20261121)
# The World Today — Saturday 21 November 2026

A one-page newspaper front page that sums up the world's news of
Saturday 21 November 2026 in a single 1024×1024 image, built for the
[make.fun competition](https://make.fun/c/news-image-20261121).

## The image

* **Masthead + date:** "THE WORLD TODAY — SATURDAY 21 NOVEMBER 2026"
* **Lead story:** Iran strikes US bases in Bahrain — the Revolutionary
  Guards say missiles and drones hit US positions at al-Riffa and Awali;
  Bahrain reports a civilian industrial site ablaze, no injuries, and
  air defences intercepting more attacks — with a flat vector
  illustration of the night attack over the Gulf.
* **39 stories across 7 regions**, each with a headline, a one-line
  summary and its source outlet:
  * Middle East & the Gulf — Saudi Arabia intercepts 3 Houthi missiles
    aimed at Riyadh; an Israeli strike kills 3 in a Gaza food truck;
    a Basra power fire kills four; Brent oil at $91; Gulf economies sink.
  * Europe & the War — a Russian missile hits Zelenskyy's hometown
    Kryvyi Rih, killing two including a 7-year-old boy; Denmark expels
    a Russian diplomat; cost-of-living protests; Paris police jailed
    over a racist beating; Villepin runs for president.
  * The Americas — Mexico captures FBI most-wanted cartel boss Chapo
    Isidro; Trump threatens a data-centre tax; the FBI crime database
    is reportedly hacked; a US child dies of measles; Bolsonaro in
    intensive care.
  * Asia-Pacific — Trump defends his Putin friendship after the
    Shenzhen summit; Japan "left out"; Seoul moves to impeach its top
    judge; Nepal's PM to visit India; a magnitude 6.8 quake off
    Timor-Leste.
  * Climate & Disasters — COP31 in overtime with still no deal; a
    magnitude 6.7 quake shakes Peru; 700,000 displaced in Ethiopia;
    US deep-sea mining leases sold; Kenya starts drilling for oil.
  * Markets, Tech & Science — the AI sell-off pushes US stocks into
    correction; Nvidia's chief ousted; YouTube nears a schools payout;
    CERN spots an ultra-rare decay; mosquitoes cut dengue in Brazil.
  * Also Today — Alcaraz reaches the ATP final; Harden passes Kobe
    with 51; England beat the All Blacks; Colturi wins for Albania;
    GTA VI makes $3.8 billion; Peter Fluck dies; UN Women ex-chief
    Mlambo-Ngcuka dies; a swimmer crosses the Strait of Hormuz.

Every story was verified against reporting dated 21 November 2026
(events that happened, or were first reported, on that day). Sources
include Reuters, AP, BBC, Xinhua, USGS, UPI, The Guardian, Yonhap and
France 24, and are credited story by story in the image.

## How it is built

`render.py` (Python 3, Pillow) draws the whole page from scratch:
masthead, ticker, lead illustration, six section panels with small
drawn glyphs, and an "Also Today" band. `main.py` copies the rendered
`entry.png` to the output directory, so both graded runs write
identical bytes. Fonts are the embedded DejaVu fonts in `fonts/`.

## Reproduce

```sh
python3 render.py          # writes entry.png (deterministic)
python3 render.py          # second run: byte-identical
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```
