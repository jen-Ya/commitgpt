**Summary**

Sends git log and git diff summaries to chatgpt, along with an optional hint for the commit message and proposes 3 commit messages.
You can chose one of the proposed messages or continue the chat to get other proposals.

Small and hackable vanilla Python script, without any package dependencies.

The only requirement is a OpenAI API key.

**Install**

Save anywhere in PATH, make it executable, add your api key as `OPENAI_API_KEY` env variable.

```bash
curl -Lo /usr/local/bin/commitgpt https://raw.githubusercontent.com/jen-Ya/commitgpt/dev/commitgpt.py
chmod +x /usr/local/bin/commitgpt
echo "export OPENAI_API_KEY=<YOUR_KEY>" >> .bash_profile
```

**Usage**

After `git add`, instead of `git commit`, execute `commitgpt`.
You can optionally provide a hint for the commit message as first argument, e. g. `commitgpt "I did X"`

```
my-cool-project $ git add -u
my-cool-project $ commitgpt

1. Improve unit tests for user authentication
2. Improve unit tests for user authentication module
3. Write initial unit tests

Choose an option (1-3), type nothing to abort, anything else to continue chat:

> also refactor

1. Refactor code and add initial unit tests
2. Refactor code and write initial unit tests
3. Refactor code and add initial unit tests

Choose an option (1-3), type nothing to abort, anything else to continue chat:

> sorry actually just test   

1. Write initial unit tests
2. Improve unit tests for user authentication module
3. Write initial unit tests

Choose an option (1-3), type nothing to abort, anything else to continue chat:

> 1

You selected: Write initial unit tests

[dev (root-commit) 083bc38] Write initial unit tests
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 test.py

Commit successful.
```

Of course, the commit messages in this repo are made using commitgpt.py:

```
commitgpt $ git add .
commitgpt $ commitgpt 

1. Add README.md and commitgpt.py for automated commit message generation
2. Add README.md and initial version of commitgpt.py script
3. Initialize repository with README and commitgpt.py script

Choose an option (1-3), type nothing to abort, anything else to continue chat:

> 2

You selected: Add README.md and initial version of commitgpt.py script

[dev (root-commit) 1b9b287] Add README.md and initial version of commitgpt.py script
 2 files changed, 256 insertions(+)
 create mode 100644 README.md
 create mode 100755 commitgpt.py

Commit successful.
```

**Tweaking**

You can change the globals at the start of the script:

`INITIAL_PROMPT` Specifies commit message guidlines and requirements
`NUM_CHOICES` Number of choices chatgpt will provide

`API_KEY` Is read from environment `OPENAI_API_KEY`, but you can also hard code it

Limits of `git diff` and `git log` context, that are sent to ChatGPT:

`GIT_LOG_LIMIT`
`GIT_DIFF_LINES_PER_FILE_LIMIT`
`GIT_DIFF_TOTAL_LINES_LIMIT`