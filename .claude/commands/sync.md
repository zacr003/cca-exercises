Read the four session-persistence files in docs/:
- docs/memory.md
- docs/lessons.md
- docs/task-list.md
- docs/registry.md

Then check whether the user passed the argument `start` (i.e., the command was `/sync start`).

---

## If `start` argument: Beginning-of-Session Sync

**1. Check git status**

Run:
```bash
cd ~/Desktop/cca-exercises && git status && git log --oneline -5
```

- If the working tree is dirty or there are unpushed commits, commit and push now:
  ```bash
  git add docs/ .claude/ domain-1/ domain-2/ domain-3/ domain-4/ domain-5/ production/ *.json *.md *.sh
  git commit -m "sync: catch-up commit $(date +%Y-%m-%d)"
  git push origin main 2>/dev/null || echo "NOTE: No remote configured."
  ```
- If clean and pushed, confirm that.

**2. Show today's task list**

Read docs/task-list.md and print the full Active Sprint section. Highlight any items that are past-due based on today's date. Note the next sprint milestone and how many days away it is.

**3. Report back**

- Git status (clean/pushed or what was committed)
- Active task list
- Next milestone + days remaining

No docs/ file updates at session start.

---

## If no argument (default): End-of-Session Sync

**1. Review the session**
Summarize what changed: exercises created or modified, concepts practiced, questions drilled, any new gotchas discovered.

**2. Update docs/memory.md**
- Update "Current State" domain progress table and exercise counts
- Update "Last Session Summary" with a 3–5 bullet recap of today's work
- Update the date in the header

**3. Update docs/task-list.md**
- Check off any tasks completed this session (`[ ]` → `[x]`)
- Add any new tasks discovered
- Update the "Last updated" date

**4. Update docs/registry.md**
- Add any new exercise files to the appropriate domain table with description and status
- Update the "Last updated" date

**5. Update docs/lessons.md**
- Add any new conventions, gotchas, or exam traps surfaced this session
- Update any existing rules that were clarified or changed

**6. Commit and push to GitHub**
```bash
cd ~/Desktop/cca-exercises

git add docs/ .claude/commands/sync.md domain-1/ domain-2/ domain-3/ domain-4/ domain-5/ production/ *.json *.md *.sh

git commit -m "sync: session update $(date +%Y-%m-%d)"

git push origin main 2>/dev/null || echo "NOTE: No remote configured. Run: git remote add origin <your-github-repo-url> && git push -u origin main"
```

**7. Report back**
Summarize what was updated in each docs/ file and confirm git status.
