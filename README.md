# Prepare and Review Interviews

An Agent Skill for evidence-based interview preparation and post-interview review. It researches the company and role, connects them to a candidate's verified experience, and turns interview notes into specific practice actions.

## What it does

- Prepares for interviews using company information, a job description, and the candidate's evidence.
- Reviews interview recordings, transcripts, question lists, or notes.
- Stores a local candidate profile and session summaries for reuse.
- Separates verified facts from predictions, public reports, and uncertain transcription.

## Install

### Codex

Install for all projects:

```bash
gh skill install zhechun539/prepare-review-interviews prepare-review-interviews --agent codex --scope user
```

For the current project only, use `--scope project`. If you do not use `gh skill`, download this repository and copy `skills/prepare-review-interviews/` into the skill directory supported by your agent. Keep the entire folder structure; the skill uses its `references/` and `scripts/` directories.

Start a new agent session after installation, then ask it to use `$prepare-review-interviews`.

### Other agents

This follows the Agent Skills folder format: keep `SKILL.md` together with its references and scripts, and install the folder in the skill directory supported by your agent. If the agent uses a sandbox, make the full folder available inside that sandbox and register the parent directory as a skill/capability directory when required by that runtime.

## Local profile and privacy

The profile store runs locally and does not upload resumes or portfolios. By default it writes to `~/.codex/interview-prep-review/`; set `INTERVIEW_PREP_STATE_DIR` to use another local folder. Keep personal profiles, resumes, transcripts, and interview notes out of this repository. The repository's `.gitignore` excludes common local profile and cache files as a precaution.

Python 3.10 or later is required for the bundled profile-store script. The script uses only the Python standard library.

## Use

For interview preparation, provide the company or official homepage, job description, and interview stage. For review, provide the transcript, notes, or recording and identify the role and stage when known. The skill will distinguish confirmed information from assumptions and predictions.

## Contents

- `skills/prepare-review-interviews/SKILL.md` — workflow and safety rules
- `skills/prepare-review-interviews/references/` — preparation, review, research, and profile guidance
- `skills/prepare-review-interviews/scripts/profile_store.py` — local profile and session storage
- `skills/prepare-review-interviews/agents/openai.yaml` — Codex display metadata

## License

MIT. See [LICENSE](LICENSE).