# CindyScript skill definition (ATCM 2026)

Companion material for

> *Lowering the Authoring Barrier: GUI-Based Natural-Language Dynamic Geometry for Mathematics Materials*, ATCM 2026.

This repository publishes the **CindyScript skill definition** (the Gemini *system instruction*) and the **gateway HTML** that displays the generated figure. It does **not** publish the authors’ conversion proxy or any API key.

## Try it (same flow as `cindySendPrompt`)

The confirmation page ports the client logic from the paper: on click it opens a tab, sends the instruction with this skill as the system instruction, extracts the CindyScript, and loads it in the gateway. Points stay draggable with no further API calls.

**Your** Gemini API key is required. The authors’ proxy is never called.

### On GitHub Pages (after the repo is public)

Open `try.html` on the Pages site, paste a key from [Google AI Studio](https://aistudio.google.com/), choose a sample prompt, press **cindySendPrompt(prompt)**. Allow pop-ups.

### Locally

```bash
python serve.py
```

This serves the folder at `http://127.0.0.1:8765/try.html` and opens it in a browser. Do not double-click `try.html` as a `file://` page: the Gemini request is then blocked by the browser.

## What is included

| File | Role |
|------|------|
| [`try.html`](try.html) | Browser confirmation test (`cindySendPrompt` client flow) |
| [`skill-definition.md`](skill-definition.md) | Exact system instruction (`gemini-3.5-flash`, temperature `0`, `maxOutputTokens` `16384`) |
| [`skill-definition.js`](skill-definition.js) | Same skill, loaded by `try.html` |
| [`cindy_csinit_query_plus.html`](cindy_csinit_query_plus.html) | Gateway: `csinit` query → Cindy.js figure |
| [`serve.py`](serve.py) | Local server that opens `try.html` |
| [`reproduce.py`](reproduce.py) | Optional CLI: print the model reply only |

The live PHP proxy used in the paper is intentionally omitted. It holds a personal API key on the authors’ server (Goal 4: keys never enter a material or the browser). Readers reproduce the conversion with their own key.

The skill text mentions the authors’ hosted copy of the gateway,

`https://kita-u.github.io/cindy-skill-definition/try.html`

That page only displays a figure. It does not call Gemini. `try.html` uses the gateway file in this repository instead.

## Relation to the paper

The paper’s table of `create` commands, the `nearpoint` helper, the five worked constructions, and the two-block output contract are excerpts of `skill-definition.md`. This repository is the full definition requested at review time.

## Licence

The skill text and gateway HTML are released under [CC BY 4.0](LICENSE).
