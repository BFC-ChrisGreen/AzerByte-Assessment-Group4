# Guide 1: Working as a Group

Before building Azerbyte, the group needs to prove that everyone can work in the same repository without losing somebody else's changes.

By the end of this guide, every member should have:

- Cloned the shared repository.
- Created and pushed their own member file.
- Pulled work created by somebody else.
- Taken part in the controlled conflict activity.
- Agreed how the group will work during the project.

## 1. Clone the Repository

Complete this individually.

1. Open your assigned Azerbyte repository on GitHub.
2. Check that you are signed in using your own GitHub account.
3. Select **Code** and copy the HTTPS address.
4. Open Visual Studio Code.
5. Press **Ctrl+Shift+P** and select **Git: Clone**.
6. Paste the repository address.
7. Choose a suitable local folder.
8. Open the repository when prompted.

Do not fork the repository. The full group works in this one shared repository.

Open a terminal and run:

```bash
git status
```

The working tree should be clean.

### Checkpoint

Every member can open the same GitHub repository and has their own local clone in Visual Studio Code.

## 2. Add Your Member File

Open:

```text
team-practice/members
```

Create a Markdown file using your name, for example:

```text
chris-green.md
```

Add:

```markdown
# Chris Green

## Proposed Project Role

Development and testing

## One Git Working Rule

Pull the latest version before beginning a new task.
```

Replace the example details with your own.

Save the file, then run:

```bash
git status
git add .
git commit -m "Add Chris team profile"
```

Use your own name in the commit message.

## 3. Share the Member Files

For this first activity, push one person at a time.

The first member runs:

```bash
git push
```

The next member runs:

```bash
git pull
git push
```

Repeat until everyone has pushed. All members then run:

```bash
git pull
```

Open `team-practice/members` and check that every member file is present.

### Checkpoint

GitHub shows at least one commit from every member's own account.

## 4. Complete the Conflict Practice

Choose two members as Member A and Member B. Both run:

```bash
git status
git pull
```

Both open:

```text
team-practice/conflict-practice.txt
```

Before either person pushes:

- Member A replaces the line with `Pull before beginning new work.`
- Member B replaces the same line with `Tell the group which file you are editing.`

Both save and commit their own change locally.

Member A pushes first. Member B then tries to push and should see a rejected push.

Member B runs:

```bash
git pull --no-rebase
```

Open the conflicted file and edit it so the final version contains both rules:

```text
Pull before beginning new work.
Tell the group which file you are editing.
```

Remove all conflict markers, save the file, then run:

```bash
git add .
git commit -m "Resolve team practice conflict"
git push
```

Everyone else runs `git pull`.

Do not use force push or discard either member's work.

### Checkpoint

Every local copy contains both rules and `git status` reports a clean working tree.

## 5. Complete the Working Agreement

Open:

```text
team-practice/working-agreement.md
```

Complete it as a group. One member should commit and push the completed agreement, then everyone else should pull it.

## Final Check

- Every member has made a commit.
- Every member has pulled somebody else's work.
- The conflict file contains both agreed rules.
- The working agreement is complete.
- Every local copy is up to date.

