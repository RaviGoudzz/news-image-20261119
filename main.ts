// news-image-20261119 entry: copies the day's front page to the grader's output.
import { copyFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const target = join(process.env.MAKEFUN_OUTPUT_DIR ?? "/output", "entry.png");

copyFileSync(source, target);
console.log("entry.png written to", target);
