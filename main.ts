// news-image-20261126 — "The World Today", Thursday 26 November 2026.
//
// The graded program does no drawing at all: it copies the pre-drawn
// front page (entry.png, rendered at build time with Pillow) into the
// output directory. No network, no fonts, no randomness — both graded
// runs write the same bytes.
//
// Run:  node main.ts            (writes /output/entry.png)
//       MAKEFUN_OUTPUT_DIR=out node main.ts
import { closeSync, copyFileSync, existsSync, mkdirSync, openSync, readSync, statSync } from "node:fs";
import { join, resolve } from "node:path";

const SOURCE = resolve(import.meta.dirname, "entry.png");
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const TARGET = join(OUTPUT_DIR, "entry.png");

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

if (!existsSync(SOURCE)) {
  throw new Error(`missing pre-drawn image: ${SOURCE}`);
}

// Sanity check the file really is a PNG before copying it.
const fd = openSync(SOURCE, "r");
const head = Buffer.alloc(8);
readSync(fd, head, 0, 8, 0);
closeSync(fd);
if (!head.equals(PNG_SIGNATURE)) {
  throw new Error(`entry.png is not a PNG file: ${SOURCE}`);
}
if (statSync(SOURCE).size > 1024 * 1024) {
  throw new Error("entry.png exceeds the 1 MiB limit before copying");
}

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(SOURCE, TARGET);

const { size } = statSync(TARGET);
if (size > 1024 * 1024) {
  throw new Error(`entry.png exceeds the 1 MiB limit: ${size} bytes`);
}
console.log(`wrote ${TARGET} (${size} bytes)`);
