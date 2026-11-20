"""
Apply TARA's Colab fixes to the ARENA 4.1 Emergent Misalignment notebooks.

Run from the repo root on the pristine ARENA snapshot (commit a6d2c46 in this repo):

    python scripts/patch_notebooks.py

The .py files (solutions.py, tests.py, utils.py) are left untouched: instead of editing solutions.py and the EM repo's
pt_utils.py by hand (as in the Week 11 errata), the setup cell copies the Colab secrets into environment variables,
which is where those files already look for them.
"""

import json
from pathlib import Path

OWNER = "ThaddeusOwl"
REPO = "tara-arena-em"
BRANCH = "main"
EM_REPO = "https://github.com/clarifying-EM/model-organisms-for-EM.git"
EM_COMMIT = "8460e4e426d3a89e8ed51aac0eadcdf7ac10469d"
ARENA_COMMIT = "fbcca86bf3ad3f09de5ab3edcb4df327396ee724"

SECTION_DIR = Path("chapter4_alignment_science/exercises/part1_emergent_misalignment")
NOTEBOOKS = ["4.1_Emergent_Misalignment_exercises.ipynb", "4.1_Emergent_Misalignment_solutions.ipynb"]
COLAB_BASE = f"https://colab.research.google.com/github/{OWNER}/{REPO}/blob/{BRANCH}/{SECTION_DIR}"

TARA_NOTE = f"""> **TARA hosted version.** This is ARENA's [4.1] Emergent Misalignment notebook as it was on 14 Sept 2026 \
(`callummcdougall/ARENA_3.0` commit `{ARENA_COMMIT[:7]}`), with the Colab fixes from the Week 11 errata built in. \
ARENA has since moved to `ARENA-education/ARENA_materials` and rewritten this notebook, so the original Colab link no longer works.
>
> **Before you start:**
>
> 1. **File → Save a copy in Drive**, so your work is saved.
> 2. **Runtime → Change runtime type → GPU.**
> 3. Add these in the **🔑 Secrets** panel (left sidebar), and switch on **Notebook access** for each:
>     - `OPENROUTER_API_KEY`: required (used by the autorater from section 2 onwards)
>     - `HF_TOKEN`: required from "Steering with Learned Vectors" (section 3) onwards
> 4. Run the setup cells below in order. You **don't** need to edit `solutions.py` or `pt_utils.py` (unlike the Week 11 \
errata): the setup cell handles the API keys for you.
>
> **Timings:** loading the models takes about 10–15 minutes on Colab. The "Comparing Steering Vectors via KL Divergence" \
cell can take 30+ minutes. You can skip it if you want to get to section 4."""

SETUP_CELL = f'''import os
import shutil
import sys
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules

chapter = "chapter4_alignment_science"
repo = "{REPO}"
branch = "{BRANCH}"

# Pinned snapshot of the Model Organisms for EM repo, so upstream changes can't break this notebook
EM_REPO = "{EM_REPO}"
EM_COMMIT = "{EM_COMMIT}"

# Install dependencies (Colab already has torch, transformers, peft & accelerate)
if IN_COLAB:
    %pip install -q einops jaxtyping openai python-dotenv tabulate "bitsandbytes>=0.46.1"
else:
    try:
        import bitsandbytes, dotenv, einops, jaxtyping, openai, peft, tabulate
    except ImportError:
        %pip install -q einops jaxtyping openai python-dotenv tabulate peft accelerate "bitsandbytes>=0.46.1"

# Get root directory, handling 3 different cases: (1) Colab, (2) notebook not in this repo, (3) notebook in this repo
root = (
    "/content"
    if IN_COLAB
    else "/root"
    if repo not in os.getcwd()
    else str(next(p for p in Path.cwd().parents if p.name == repo))
)

# Download the exercise files (checks for the section folder, so a failed download is retried on re-running)
exercises_path = Path(f"{{root}}/{{chapter}}/exercises/part1_emergent_misalignment")
if Path(root).exists() and not exercises_path.exists():
    if not IN_COLAB:
        !sudo apt-get install unzip
        %pip install jupyter ipython --upgrade

    !wget -q -O {{root}}/{{branch}}.zip https://github.com/{OWNER}/{{repo}}/archive/refs/heads/{{branch}}.zip
    !unzip -q -o {{root}}/{{branch}}.zip '{{repo}}-{{branch}}/{{chapter}}/exercises/*' -d {{root}}
    shutil.copytree(f"{{root}}/{{repo}}-{{branch}}/{{chapter}}", f"{{root}}/{{chapter}}", dirs_exist_ok=True)
    shutil.rmtree(f"{{root}}/{{repo}}-{{branch}}")
    os.remove(f"{{root}}/{{branch}}.zip")
assert exercises_path.exists(), "Downloading the exercise files failed - check the output above"

# Clone the EM repo into the exercises directory, at the pinned commit
em_dir = f"{{root}}/{{chapter}}/exercises/model-organisms-for-EM"
if not Path(f"{{em_dir}}/em_organism_dir").exists():
    !rm -rf "{{em_dir}}"
    !git init -q "{{em_dir}}" && git -C "{{em_dir}}" fetch -q --depth 1 {{EM_REPO}} {{EM_COMMIT}} && git -C "{{em_dir}}" checkout -q FETCH_HEAD
assert Path(f"{{em_dir}}/em_organism_dir").exists(), "Cloning the EM repo failed - check the output above"

# On Colab, read API keys from Colab secrets into environment variables. `solutions.py` and the EM repo read them with
# `os.getenv`, and `load_dotenv()` never overwrites variables that are already set, so no file edits are needed.
if IN_COLAB:
    from google.colab import userdata

    for secret, used_for in [
        ("OPENROUTER_API_KEY", "the autorater (sections 2 onwards)"),
        ("HF_TOKEN", "loading LoRA checkpoints (section 3 onwards)"),
    ]:
        try:
            os.environ[secret] = userdata.get(secret)
        except Exception as e:
            print(
                f"⚠️ Couldn't read the Colab secret {{secret}} ({{type(e).__name__}}), which is needed for {{used_for}}. "
                "Add it in the 🔑 Secrets panel, switch on notebook access, then re-run this cell."
            )

if f"{{root}}/{{chapter}}/exercises" not in sys.path:
    sys.path.append(f"{{root}}/{{chapter}}/exercises")

os.chdir(f"{{root}}/{{chapter}}/exercises")'''

CLONE_MD = f"""The setup code above has already cloned the [Model Organisms for EM](https://github.com/clarifying-EM/model-organisms-for-EM) \
repo into `chapter4_alignment_science/exercises/model-organisms-for-EM` (pinned to commit `{EM_COMMIT[:7]}`). On Colab, it \
also loaded your `OPENROUTER_API_KEY` and `HF_TOKEN` from Colab secrets.

If you're running this outside Colab, create an `.env` file inside `chapter4_alignment_science/exercises` with your keys \
instead:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
HF_TOKEN=your_huggingface_token_here
```"""

KL_NOTE = """> **TARA note:** the next code cell can take **30+ minutes** on Colab. If you're short on time, skip running it, \
read the observations below the plot, and move on."""

OLD_ASSERT = 'assert OPENROUTER_API_KEY, "Please set OPENROUTER_API_KEY in your .env file"'
NEW_ASSERT = (
    'assert OPENROUTER_API_KEY, "Please set OPENROUTER_API_KEY as a Colab secret (🔑 in the left sidebar), '
    'or in your .env file if running locally"'
)


def to_source(text: str) -> list[str]:
    lines = text.split("\n")
    return [line + "\n" for line in lines[:-1]] + [lines[-1]]


def md_cell(text: str) -> dict:
    return {"cell_type": "markdown", "execution_count": None, "metadata": {}, "outputs": [], "source": to_source(text)}


def find_cell(cells: list[dict], cell_type: str, predicate) -> int:
    matches = [i for i, c in enumerate(cells) if c["cell_type"] == cell_type and predicate("".join(c["source"]))]
    assert len(matches) == 1, f"Expected exactly one matching {cell_type} cell, found {len(matches)}"
    return matches[0]


def patch(nb: dict) -> None:
    cells = nb["cells"]

    # Header: point the Colab links at this repo
    i = find_cell(cells, "markdown", lambda s: s.startswith("# [4.1] Emergent Misalignment"))
    src = "".join(cells[i]["source"])
    for name in NOTEBOOKS:
        old_prefix = "https://colab.research.google.com/github/callummcdougall/ARENA_3.0/blob/main/"
        old = f"{old_prefix}{SECTION_DIR}/{name}?t=20260520"
        assert old in src, f"Header link for {name} not found"
        src = src.replace(old, f"{COLAB_BASE}/{name}")
    cells[i]["source"] = to_source(src)

    # TARA instructions, straight after the header image
    i = find_cell(cells, "markdown", lambda s: s.startswith('<img src="https://raw.githubusercontent.com/info-arena'))
    cells.insert(i + 1, md_cell(TARA_NOTE))

    # Setup cell: download this repo, install bitsandbytes, clone the pinned EM repo, load Colab secrets
    i = find_cell(cells, "code", lambda s: s.startswith("import os\nimport sys\nfrom pathlib import Path\n\nIN_COLAB"))
    cells[i]["source"] = to_source(SETUP_CELL)
    cells[i]["outputs"] = []
    cells[i]["execution_count"] = None

    # Instructions for cloning the EM repo by hand are no longer needed
    i = find_cell(cells, "markdown", lambda s: s.startswith("Before running the setup code, you should clone"))
    cells[i]["source"] = to_source(CLONE_MD)

    # Friendlier error if the key is missing
    i = find_cell(cells, "code", lambda s: OLD_ASSERT in s)
    cells[i]["source"] = to_source("".join(cells[i]["source"]).replace(OLD_ASSERT, NEW_ASSERT))

    # Warn about the slow KL-divergence cell
    i = find_cell(cells, "markdown", lambda s: s.startswith("### Comparing Steering Vectors via KL Divergence"))
    assert cells[i + 1]["cell_type"] == "code" and "def compare_steering_vectors_kl" in "".join(cells[i + 1]["source"])
    cells.insert(i + 1, md_cell(KL_NOTE))

    # Colab should open these with a GPU runtime by default
    nb["metadata"].setdefault("accelerator", "GPU")
    nb["metadata"].setdefault("colab", {"provenance": [], "gpuType": "T4"})
    nb["metadata"].setdefault("kernelspec", {"name": "python3", "display_name": "Python 3"})


if __name__ == "__main__":
    for name in NOTEBOOKS:
        path = SECTION_DIR / name
        nb = json.loads(path.read_text())
        assert not any("TARA hosted version" in "".join(c["source"]) for c in nb["cells"]), f"{path} already patched"
        patch(nb)
        path.write_text(json.dumps(nb))  # same serialisation as the ARENA originals
        print(f"Patched {path}")
