import fs from "node:fs";
import vm from "node:vm";

const catalog = JSON.parse(fs.readFileSync("data/questions/catalog.json", "utf8"));
const html = fs.readFileSync("index.html", "utf8");
const questions = catalog.questions ?? [];
const ids = questions.map((q) => q.id);
const duplicateIds = ids.filter((id, index) => ids.indexOf(id) !== index);
const invalid = questions.filter((q) =>
  !q.id || !["phonetic", "form"].includes(q.type) ||
  !q.prompt || !q.answer ||
  !["demo", "verified", "transcribed_unverified"].includes(q.verification_status)
);
const scripts = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/gi)].map((m) => m[1]);

if (questions.length < 100) throw new Error(`Expected at least 100 questions; found ${questions.length}`);
if (duplicateIds.length) throw new Error(`Duplicate question IDs: ${[...new Set(duplicateIds)].join(", ")}`);
if (invalid.length) throw new Error(`Invalid question records: ${invalid.map((q) => q.id ?? "(missing id)").join(", ")}`);
if (!questions.some((q) => q.type === "phonetic") || !questions.some((q) => q.type === "form")) {
  throw new Error("Both phonetic and form questions must exist");
}
if (!html.includes("./data/questions/catalog.json")) throw new Error("The app does not load the central question catalog");
if (!scripts.length) throw new Error("No inline application script found");
for (const source of scripts) new vm.Script(source, { filename: "index.html:inline-script" });

console.log("Catalog and app checks passed.");
console.log(`Questions: ${questions.length}; phonetic: ${questions.filter((q) => q.type === "phonetic").length}; form: ${questions.filter((q) => q.type === "form").length}`);
console.log(`Statuses: ${JSON.stringify(questions.reduce((a, q) => (a[q.verification_status] = (a[q.verification_status] ?? 0) + 1, a), {}))}`);
