// news-image-20261122 entry program (Node 22, standard library only).
//
// The entry image is drawn by draw.py and stored beside this file as
// entry.png. This program checks it against the competition gate — a whole
// PNG, at most 1 MiB and at most 1024 by 1024 pixels — and copies it to the
// output directory. It writes the same bytes on every run: the copy is a
// byte-for-byte copy of the file in the repository.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const LIMIT_BYTES = 1048576;
const LIMIT_PIXELS = 1024;
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

function fail(message: string): never {
  throw new Error(message);
}

function main(): void {
  const root = dirname(resolve(process.argv[1]));
  const sourcePath = join(root, "entry.png");
  const outputDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
  const targetPath = join(outputDir, "entry.png");

  const info = statSync(sourcePath);
  if (info.size > LIMIT_BYTES) {
    fail(`entry.png is ${info.size} bytes, over the ${LIMIT_BYTES} byte limit`);
  }

  const bytes = readFileSync(sourcePath);
  for (let i = 0; i < PNG_SIGNATURE.length; i++) {
    if (bytes[i] !== PNG_SIGNATURE[i]) {
      fail("entry.png does not start with the PNG signature");
    }
  }
  if (bytes.length < 24 || bytes.toString("ascii", 12, 16) !== "IHDR") {
    fail("entry.png has no IHDR chunk where one is expected");
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width > LIMIT_PIXELS || height > LIMIT_PIXELS) {
    fail(`entry.png is ${width}x${height}, over ${LIMIT_PIXELS}x${LIMIT_PIXELS}`);
  }

  mkdirSync(outputDir, { recursive: true });
  copyFileSync(sourcePath, targetPath);
  console.log(
    `entry.png OK (${width}x${height}, ${info.size} bytes) -> ${targetPath}`,
  );
}

main();
