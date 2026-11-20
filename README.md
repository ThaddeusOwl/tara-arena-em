# TARA: ARENA [4.1] Emergent Misalignment (pinned + Colab-fixed)

A frozen copy of ARENA's **[4.1] Emergent Misalignment** exercises for TARA students. The Week 11 errata fixes are
built in, so the notebook runs on Colab without any file edits.

| | Open in Colab |
|---|---|
| Exercises | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ThaddeusOwl/tara-arena-em/blob/main/chapter4_alignment_science/exercises/part1_emergent_misalignment/4.1_Emergent_Misalignment_exercises.ipynb) |
| Solutions | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ThaddeusOwl/tara-arena-em/blob/main/chapter4_alignment_science/exercises/part1_emergent_misalignment/4.1_Emergent_Misalignment_solutions.ipynb) |

## Why this exists

ARENA moved from `callummcdougall/ARENA_3.0` to
[`ARENA-education/ARENA_materials`](https://github.com/ARENA-education/ARENA_materials) and rewrote this notebook. The
old notebook's setup cell downloads `ARENA_3.0/archive/refs/heads/main.zip`, which now redirects to the new repo, so it
no longer unzips correctly. Even if it did, it would pull in files that don't match the old notebook. This repo pins
everything the notebook depends on:

| Dependency | Pinned to |
|---|---|
| ARENA exercise files (`solutions.py`, `tests.py`, `utils.py`) | `callummcdougall/ARENA_3.0@fbcca86` (14 Sept 2026), unmodified |
| [Model Organisms for EM](https://github.com/clarifying-EM/model-organisms-for-EM) repo | `8460e4e` (cloned by the setup cell) |

## Student instructions

1. Open the exercises link above, then **File → Save a copy in Drive**.
2. **Runtime → Change runtime type → GPU.**
3. In the **🔑 Secrets** panel (left sidebar), add the following and switch on **Notebook access** for each:
   - `OPENROUTER_API_KEY`: required (the autorater, from section 2 onwards)
   - `HF_TOKEN`: required from "Steering with Learned Vectors" (section 3) onwards
4. Run the cells in order.

Loading the models takes about 10–15 minutes on Colab. The "Comparing Steering Vectors via KL Divergence" cell can take
30+ minutes, and students can skip it to get to section 4.

## Changes from the ARENA original

All of these are in the notebooks only. Run `git diff a6d2c46 -- '*.ipynb'` to see them, or read
[`scripts/patch_notebooks.py`](scripts/patch_notebooks.py), which applies them to the pristine snapshot.

- **Setup cell**:
  - Downloads this repo instead of ARENA's.
  - Installs `bitsandbytes>=0.46.1` (Week 11 errata #2), quoted so the shell doesn't read `>` as a redirect.
  - Drops the `transformer_lens` install, which this notebook never imports.
  - Clones the EM repo at a pinned commit (errata #1).
- **API keys** (errata #1, #4 and #5): on Colab, the setup cell copies the `OPENROUTER_API_KEY` and `HF_TOKEN` secrets
  into environment variables. `solutions.py` and the EM repo's `pt_utils.py` already read them with `os.getenv`, and
  `load_dotenv()` doesn't overwrite variables that are already set. That makes the manual edits to `solutions.py` and
  `pt_utils.py` unnecessary, which also fixes `tests.test_steering_hook_matches_reference`. Locally, a `.env` file
  still works as before.
- **Notes**:
  - A TARA instructions box at the top.
  - A timing warning before the slow KL-divergence cell.
  - Header Colab links point here.
  - Colab metadata defaults to a GPU runtime.

## Updating

To change the notebooks, edit `scripts/patch_notebooks.py`, then re-run it on the pristine files:

```bash
git checkout a6d2c46 -- chapter4_alignment_science && python3 scripts/patch_notebooks.py
```

Credit for all exercise content goes to [ARENA](https://www.arena.education/) and the authors of
[Model Organisms for Emergent Misalignment](https://github.com/clarifying-EM/model-organisms-for-EM).
