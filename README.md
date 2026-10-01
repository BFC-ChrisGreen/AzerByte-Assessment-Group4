# Azerbyte Group Project

This is your group's shared repository for the Azerbyte distributed-system prototype.

Each member will work in their own local clone, but everyone contributes to the same version on GitHub. Do not fork this repository.

## The Project

Azerbyte is a fictional online role-playing game that needs a distributed system for managing shared player and character data. Over the next few topics, your group will build a Python client, a separately running Flask API and persistent SQLite storage. The components will communicate using HTTP and JSON.

The final prototype should allow users to:

- View all characters.
- Find an individual character.
- Create a new character.
- Update existing character information.
- Receive an appropriate response when a request cannot be completed.
- Restart the system without losing stored data.

## Repository Structure

```text
azerbyte-group-XX/
├── README.md
├── requirements.txt
├── guides/
├── team-practice/
├── client/
├── server/
├── database/
├── tests/
├── evidence/
└── docs/
```

| Folder | Purpose |
|---|---|
| `guides` | Step-by-step instructions for each stage of the build. |
| `team-practice` | Topic 3 collaborative Git activity. |
| `client` | Python command-line client and, later, the Tkinter interface. |
| `server` | Flask API and server-side code. |
| `database` | SQLite database and database setup files. |
| `tests` | Test scripts and documented test cases. |
| `evidence` | Group evidence that supports the working prototype. |
| `docs` | Shared technical documentation and design decisions. |

Your individual technical evaluation must not be stored in this shared repository. Submit it separately through Canvas.

## Where to Start

Complete the guides in order:

1. `guides/01-working-as-a-group.md`
2. `guides/02-your-first-api.md`

The first guide is completed during Topic 3. It makes sure that everyone can clone, pull, commit and push safely before the group starts building assessed work.

The second guide is completed during Topic 4. You will create the first Flask API and Python client yourselves after the ideas have been introduced in class. The `client` and `server` folders are intentionally empty apart from their README files.

Do not skip ahead. Later guides will be added as the relevant topics are introduced.

## Everyday Git Workflow

Before starting a new task:

```bash
git status
git pull
```

After completing and testing a small change:

```bash
git status
git add .
git commit -m "Describe the completed change"
git push
```

## Working Rules

- Communicate before editing shared files.
- Pull before beginning a new task.
- Make small, focused commits.
- Test changes before pushing.
- Use your own GitHub account.
- Do not use force push.
- Do not delete or discard changes you do not recognise.
- Use fictional and synthetic data only.
- Never commit passwords, access tokens, API keys or other credentials.
- Keep individual assessment writing outside the shared repository.

## Completion Evidence

The final repository should contain:

- The complete working prototype.
- Clear setup and running instructions.
- Meaningful commits from every group member.
- Evidence of functional and unsuccessful request testing.
- Agreed data rules and technical decisions.
- No real personal data or credentials.
