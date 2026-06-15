---
description: {{DESCRIPTION}}
argument-hint: "[query]"
---

# /{{PLUGIN_NAME}}

{{DESCRIPTION}}

When invoked, this command should:

1. Parse the user's request (use `$ARGUMENTS` if present).
2. Delegate the actual work to the `{{SKILL_SLUG}}` skill bundled in this plugin.
3. Present the result to the user concisely.

If `$ARGUMENTS` is empty, ask the user what they want to do in one short follow-up question, then proceed.

---

TODO (delete after first edit):
- Replace this body with the prompt that defines what `/{{PLUGIN_NAME}}` does.
- Keep it imperative and concrete. Bad: "be helpful with X". Good: "given a textbook problem photo, extract the variables, choose the right formula, solve symbolically with SymPy, present the worked solution".
- Cross-reference the bundled skill if the heavy lifting belongs there.
