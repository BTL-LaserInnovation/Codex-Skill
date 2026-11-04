# Visual guide for elementary and middle school readers

## Choose a visual that answers the question

| Paper content | Visual | Avoid |
| --- | --- | --- |
| A procedure or system | A few ordered scenes with concrete objects | A network of unexplained arrows |
| A controlled comparison | Side-by-side groups with the same scale | Comparing differently sized icons |
| Counts or proportions | One icon per item for small samples, or a labeled bar chart | Decorative quantities that contradict the data |
| A proposed mechanism | A simple diagram marked “proposed explanation” | Showing speculation as an observed event |
| Several papers | Separate source labels and compatible comparisons | Silently pooling different populations or units |

Prefer a few large, clearly labeled elements, one reading direction, and an uncluttered background. Do not shrink text to fit; shorten it or split the image. Use a font with Korean glyphs for Korean content. Color is supplementary: label groups and distinguish shapes when useful.

For quantitative plots, show units, denominators, and relevant conditions. Use a common scale; start ordinary count bars at zero. Show numerical uncertainty only if provided by the source. Explicitly label values estimated by digitizing a figure; do not present them as exact source data.

## Prepare a visual brief

Settle the audience, question, takeaway, panel sequence, verified facts, visible uncertainty, source location, and viewing size before drawing. A short internal note suffices; it does not replace the image.

Each panel needs a concrete scene, short label, and supported message. Distinguish source-backed content from explanatory decoration. For image generation, specify these constraints and reserve room for exact labels added separately if needed. Inspect the actual image; a correct prompt does not guarantee a correct result.

Choose an analogy whose familiar behavior matches the part being explained. A sieve can illustrate separation by size but must not imply that a real membrane rejects substances only by size. Explain mismatches that matter. Avoid fairies or purposeful actions implying that molecules think or choose.

## Worked example: a fictional seed experiment

This is invented teaching material, not an actual paper or scientific finding.

Given excerpt: p.2 describes 20 mung beans per group, equal moisture, ambient temperature 22°C, and a lamp for group A for two hours/day. Table 1 on p.4 gives 14 germinated seeds in A and 10 in B after five days. Page 5 calls it a small pilot; randomization is unspecified, no statistical test is reported, and seed-surface temperature was not measured.

| Claim | Source | Image treatment |
| --- | --- | --- |
| Two groups of 20 seeds; only A received a lamp | p.2 | Equal trays, labels “하루 2시간 빛” / “램프 없음” |
| 14 vs 10 germinated after five days | p.4, Table 1 | 20 icons per group, exactly 14 / 10 sprouts; “5일 뒤 관찰” |
| Pilot limitations | p.5 | “아직 더 실험해야 해요.”; full detail in analysis |
| A fairy waking seeds | Analogy, not source evidence | Optional small illustration labeled “이해를 돕는 비유” |

A readable four-panel image could say:

1. **Question:** “빛을 받으면 싹이 더 많이 날까?” — show a seed and lamp.
2. **Experiment:** “씨앗을 20개씩 나눴어요.” — two equal trays; add lamp conditions and “물과 주변 온도는 같아요.”
3. **Observation:** “5일 뒤 싹을 세었어요.” — counts “빛 받은 쪽: 14개” / “램프 없는 쪽: 10개.”
4. **Takeaway:** “이번엔 4개 더 싹이 났어요.” and “아직 더 실험해야 해요.”

Keep the uncertainty readable in panel 4. Put exact units, ambient temperature, and source details in the caption if the image is crowded. Explain to middle school readers that an unmeasured temperature difference or chance could contribute. Do not say “twice as many,” “light definitely caused this,” or “works for all seeds.” The counts are 70% and 50%, a 20-percentage-point difference or a ratio of 1.4; counts are simpler for younger readers.

## Final inspection

Verify icon counts and labels against the source. Check arrow meanings and reading order. A child should be able to identify the question, comparison, result, and uncertainty without a dense paragraph. Open the exported file, not only its source. Inspect raster exports separately if they could change text or layout. If only an SVG was produced and inspected, say so rather than claiming a PNG exists.
