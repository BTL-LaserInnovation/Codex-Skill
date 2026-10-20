# Evaluate Blue Ocean in its execution environment

Use when changing this skill's instructions, routing, model selection or tool integrations. Product build/test evidence and skill behavior evidence answer different questions: the existing [execution harness](harness.md) does not itself prove that an agent selects the correct workflow.

## Proportionate evaluation

1. Check frontmatter with the available skill validator and repository validator; verify local links, relevant templates and both language versions. Preserve existing script tests when code behavior changes. Structural checks do not prove correct decisions.
2. Select the affected cases from [the case set](../templates/skill-evaluation-cases.json). Prepare minimal disposable fixtures with the stated conditions. Give an independent evaluator only the user request, skill entrypoint and raw fixture facts; keep expectations for the reviewer. Prefer existing authorized agent/client tools. No API key, paid API eval runner, installation or external connection is implied.
3. Test decisions in the intended Codex client with its actual tool and permission set. A paper walkthrough must be labelled `walkthrough`; it is not a live application test. A standalone loop or SDK test does not establish desktop behavior. Record client/version when observable, effective model or `unverified`, permission mode, selected references, actions, outcomes and evidence.
4. Judge observed actions against the case criteria, including correct requests for decisions and correct blocked/not-run outcomes. Grade `pass`, `fail`, `blocked`, or `not_run` with a reason. Repeat cases whose model/tool path changed when variability matters; report each attempt and any result flips. Do not retry selectively until failures disappear.
5. Review representative traces/artifacts, fix demonstrated defects, then rerun affected cases. Report coverage and limitations instead of claiming the whole suite passed from a few examples. Keep reports in the existing task/QC location, not inside reusable skill instructions.

## Sources and scope

- [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) (September 11, 2026): short discriminating descriptions, conditional reference loading and proportionate context. Apply these structural ideas while preserving Blue Ocean's chosen Sol model and explicit gates.
- [Harness-aware evaluation of plugins](https://developers.openai.com/cookbook/examples/partners/harness_aware_plugin_evals/harness_aware_plugin_evals) (September 23, 2026): results depend on the model plus execution harness; compare representative target-client behavior and repeated outcomes. The case set adapts that method to this skill; it is not an OpenAI benchmark.
