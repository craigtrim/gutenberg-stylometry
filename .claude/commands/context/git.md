# Git Context

Handle git operations for craigtrim.com repository based on the user's instructions.

**User Instructions:** $ARGUMENTS

## Repository Structure

```
/Users/craigtrim/git/mville/cosc-agentic-systems/
├── demos/           # JSX demos
├── site/
│   ├── articles/    # HTML articles
│   ├── gallery/     # Image gallery
│   ├── images/      # Static images
│   ├── gists/       # Code gists
│   └── index.html   # Homepage
└── .claude/         # Claude commands
```

## Git Configuration

```bash
git config --global user.name "Craig Trim"
git config --global user.email "craigtrim@gmail.com"
```

## Commit Message Format

Use conventional commit prefixes:
- `feat:` - New feature or demo
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code restructuring
- `style:` - Formatting, styling changes
- `chore:` - Maintenance tasks

**Examples:**
- `feat: Add tokenizer-evolution demo`
- `fix: Correct slider behavior in multilingual-tax`
- `docs: Update article on context windows`
- `refactor: Simplify state management in polysemy-graph`

## Commit Rules

- **No Co-Authored-By lines** - Do not include co-author attributions
- **Atomic commits** - One logical change per commit
- **Descriptive messages** - Reflect the actual work done

## Chunking Large Commits

When changes span multiple areas, break them into logical commits. Use your judgment based on these guidelines:

**Split by content type:**
- Demos get their own commits (one per demo, or group related demos)
- Articles get their own commits (one per article)
- Config/command changes get their own commit
- Homepage/landing page changes get their own commit

**Split by nature of change:**
- New features separate from bug fixes
- Refactoring separate from new functionality
- Style/formatting changes separate from logic changes

**Logical groupings (commit together):**
- A demo and its README update
- An article and its images
- Related command files that work together
- Multiple files changed for the same bug fix

**Example: Large changeset with 15 modified files**

Instead of one massive commit, create:
1. `feat: Add llm-landscape demo`
2. `feat: Add tfidf-book-explorer demo`
3. `fix: Update slider range in multilingual-tax`
4. `docs: Update bpe-history article with new section`
5. `chore: Consolidate Claude commands into context folder`

**When in doubt:**
- If changes touch different demos → separate commits
- If changes touch different articles → separate commits
- If changes are unrelated in purpose → separate commits
- If you can describe the commit in one clear sentence → it's probably atomic enough

## Checking for Changes

**Single folder:**
```bash
git status -- demos/DEMO_NAME/
git diff HEAD -- demos/DEMO_NAME/
```

**All changes:**
```bash
git status
git diff HEAD
```

**Porcelain format (for scripting):**
```bash
git status --porcelain -- demos/DEMO_NAME/
```

## Staging Changes

**Single demo:**
```bash
git add demos/DEMO_NAME/
```

**Single article:**
```bash
git add site/articles/ARTICLE_NAME/
```

**All demos:**
```bash
git add demos/
```

**All articles:**
```bash
git add site/articles/
```

## Creating Commits

```bash
git commit -m "prefix: Commit message here"
```

## Verifying Commits

```bash
git log -1 --oneline
```

## Batch Processing Demos

When committing all demos:

1. List all directories in `demos/`
2. For each demo, check if it has changes
3. If changes exist, stage and commit with appropriate message
4. Skip demos with no changes
5. Report summary (commits created, demos skipped)

## Batch Processing Articles

When committing all articles:

1. List all directories in `site/articles/`
2. For each article, check if it has changes
3. If changes exist, stage and commit with appropriate message
4. Skip articles with no changes
5. Report summary

## Instructions

Follow the user's instructions in `$ARGUMENTS`. This may include:
- Committing a specific demo or article
- Committing all demos or all articles
- Checking what has changed
- Creating commits with specific messages
- Reviewing recent commit history

Always check for changes before attempting to commit. If no changes exist, inform the user and stop.
