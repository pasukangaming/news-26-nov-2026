# The World Today — 26 November 2026

Entry for the make.fun bounty
[Sum up 26 November's world news in one image](https://make.fun/bounty/news-image-20261126)
($100 shared by the 50 highest-ranked entries, free entry).

## The image

A newspaper front page for Thursday 26 November 2026. The lead story is
the one that dominated the day's news in every briefing: **Washington
proposes new tariffs on 14 trading partners** — Vietnam 35%, India 25%,
China 20%, and the EU, Japan and South Korea 15% each — accusing them of
flooding world markets with excess factory output. A bar chart of the
proposed rates makes the story readable at a glance.

Three more stories from the day fill the page:

- **Cairo** — a fuel tanker fire on the ring road kills at least 31 people.
- **Red Sea / Saudi Arabia** — Houthi strikes hit Saudi ports and the Ras
  Tanura refinery, pushing oil prices up.
- **Kyiv** — Russian ballistic missiles strike the capital, wounding seven,
  as diplomacy to end the war faces new uncertainty.

The footer ticker adds North Korea's vow to expand its nuclear arsenal,
the first Pakistani astronaut boarding China's Tiangong station, and
SpaceX's approval for one million satellites.

## How it works

- `draw_image.py` (build time only) renders the front page with Pillow
  into `entry.png` — 1024×1024, about 122 KB.
- `main.ts` (Node 22, standard library only) copies `entry.png` to
  `/output/entry.png`. It draws nothing at grade time, uses no network and
  no fonts, so both graded runs write identical bytes.

## Run it

```sh
node main.ts                          # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).

Built by [pasukangaming](https://github.com/pasukangaming) for the make.fun
account @arif-teguh-ristyan.
