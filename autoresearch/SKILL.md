---
name: autoresearch
description: Runs an autonomous experiment loop to optimize a single metric by iteratively modifying a designated file. Use when user says "autoresearch", "run experiments", "optimize this metric", "experiment loop", "autonomous optimization", or "run the research loop". Do NOT use for one-off code changes, code review, refactoring, test writing, or manual debugging.
---

## Important

Follow these rules strictly.

* Do not modify any file other than the designated target file.
* Do not modify the evaluation command, metric extraction, or results ledger format.
* Do not install new packages or add dependencies beyond what already exists.
* Do not stop to ask the user if you should continue. The user may be away. Run until interrupted.
* Do not skip the baseline run. The first experiment is always the unmodified code.
* Do not keep changes that make the metric worse, even if the code looks "better."
* Always commit before running an experiment. Always revert on failure.
* Always log every experiment to the results ledger, including crashes and discards.

## Purpose

Run an autonomous experiment loop that optimizes a single measurable metric by iteratively modifying a single designated file. Each experiment is a git commit. Improvements are kept; regressions are discarded. The loop runs indefinitely until the user interrupts.

Inspired by Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) pattern.

## Configuration

The skill reads its configuration from `autoresearch.yaml` in the project root.

Required fields:

```yaml
target_file: train.py                    # The ONLY file you are allowed to edit
eval_command: uv run train.py            # Command that produces the metric
metric_name: val_bpb                     # Human-readable name of the metric
metric_direction: lower                  # "lower" or "higher" is better
metric_pattern: "^val_bpb:\\s+(\\S+)"    # Regex to extract metric value from command output
```

Optional fields:

```yaml
time_budget: 300                         # Max seconds per experiment (default: 300)
results_file: results.tsv               # Path for results ledger (default: results.tsv)
```

If `autoresearch.yaml` does not exist, ask the user to create one. Do not guess configuration values.

## Setup Procedure

Before entering the experiment loop, complete these steps exactly:

1. **Read configuration**: Read `autoresearch.yaml` from the project root. Validate all required fields are present. If any are missing, stop and tell the user.

2. **Agree on a run tag**: Propose a tag based on today's date (e.g., `mar16`). The branch `autoresearch/<tag>` must not already exist.

3. **Create the experiment branch**: `git checkout -b autoresearch/<tag>` from the current branch. This isolates all experiments from main development.

4. **Read the target file**: Read the designated `target_file` to understand the current state. Also read any other files referenced in the config or necessary for context, but remember: you can only EDIT the target file.

5. **Add results file to .gitignore**: Ensure the results file path is in `.gitignore` so it survives git resets. If `.gitignore` does not exist, create it with just this entry.

6. **Initialize the results ledger**: Create the results file with the header row:
   ```
   commit	metric_value	status	description
   ```

7. **Establish baseline**: Run the eval command on unmodified code. Record the result as the baseline in the ledger. This is experiment zero.

8. **Confirm and go**: Print a summary of the configuration, baseline result, and begin the loop.

## The Experiment Loop

Once setup is complete, execute this loop. Do not stop.

```
LOOP FOREVER:

  1. THINK
     - Review the results ledger: what has been tried, what worked, what failed
     - Review the current state of the target file
     - Hypothesize a specific improvement and explain your reasoning in 1-2 sentences

  2. IMPLEMENT
     - Edit ONLY the target file
     - Make the change that implements your hypothesis

  3. COMMIT
     - git add <target_file>
     - git commit -m "experiment: <short description of what you changed>"

  4. RUN
     - Execute: <eval_command> > run.log 2>&1
     - Use the configured time_budget as a timeout
     - Do NOT let output flood your context — always redirect to run.log

  5. MEASURE
     - Extract the metric: grep the metric_pattern from run.log
     - If grep returns empty, the run crashed. Go to CRASH HANDLING.

  6. DECIDE
     - If metric improved (better than best so far):
       → KEEP. Log as "keep" in the ledger. This is the new best.
     - If metric is equal or worse:
       → DISCARD. Run: git reset --hard HEAD~1
       → Log as "discard" in the ledger.

  7. LOG
     - Append a row to the results ledger:
       commit_hash (7 chars) | metric_value | status | description
     - Use tabs as separator, not commas.

  8. CONTINUE
     - Return to step 1. Do not pause. Do not ask the user.
```

## Simplicity Criterion

Before keeping an improvement, assess whether the complexity added is justified by the metric gain.

- A marginal improvement that adds significant code complexity → **discard**
- A marginal improvement from *deleting* code or simplifying → **always keep**
- A large improvement that adds complexity → **keep**, note the complexity cost in the description
- Equal metric but simpler code → **keep** (simplification win)

When in doubt, prefer simpler code.

## Crash Handling

When the eval command crashes (empty metric output, non-zero exit code, or timeout):

1. Read the last 50 lines of run.log: `tail -n 50 run.log`
2. Diagnose the failure:
   - **Fixable bug** (typo, missing import, shape mismatch): Fix it, re-commit, re-run. Up to 2 fix attempts per experiment.
   - **Fundamental failure** (OOM, algorithm won't converge, incompatible change): Discard immediately. `git reset --hard HEAD~1`. Log as "crash".
3. If the eval command exceeds twice the configured `time_budget`, kill it and treat as a crash.

## Git Workflow

- All experiments happen on the `autoresearch/<tag>` branch. Never modify main/master.
- Each experiment is one commit to one file.
- Discarded experiments are reverted with `git reset --hard HEAD~1`.
- The results ledger is untracked (in `.gitignore`) so it survives resets.
- When the user interrupts, the branch contains only the chain of successful improvements.

## Results Ledger Format

Tab-separated values. Do NOT use commas.

```
commit	metric_value	status	description
a1b2c3d	0.997900	keep	baseline (unmodified)
b2c3d4e	0.993200	keep	increased learning rate to 0.04
c3d4e5f	1.005000	discard	switched to GeLU activation
d4e5f6g	0.000000	crash	doubled model width (OOM)
```

Columns:
- `commit`: Short git hash (7 chars). Use `0000000` for crashes that were reverted.
- `metric_value`: The measured value. Use `0.000000` for crashes.
- `status`: One of `keep`, `discard`, `crash`.
- `description`: Brief text describing what was tried.

## Session Limits

Claude Code sessions can end due to context limits or user interruption.

- The results ledger persists on disk.
- The experiment branch persists in git.
- To resume: re-invoke the skill. Read the existing ledger and branch state, then enter the loop directly. Do NOT re-run setup.

## When Ideas Run Dry

If stuck after several discarded experiments:

1. Re-read the target file from scratch
2. Review the full results ledger for patterns in what worked vs didn't
3. Try combining two previously successful ideas
4. Try the opposite of recent failed attempts
5. Try a more radical change
6. Try removing code rather than adding it

The loop runs until the human interrupts. Think harder, not shorter.
