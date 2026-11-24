// News-image entry for 24 November 2026 (Node 22, standard library only).
// The entry is the image entry.png beside this file; the program copies it
// to the output directory the grader provides, byte for byte, so the judge
// sees exactly the rendered image.
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const target = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');

copyFileSync(source, target);

// Guard against a truncated or corrupted copy: the output must hash
// exactly the same as the entry, not merely match its size.
const digest = (path) => createHash('sha256').update(readFileSync(path)).digest('hex');
if (digest(source) !== digest(target)) {
  throw new Error('entry.png copy is incomplete: output hash differs from source');
}
