**Summary**

Sends git log and git diff summaries to chatgpt, along with an optional hint for the commit message and proposes 3 commit messages.
You can chose one of the proposed messages or continue the chat to get other proposals.

**Install**

Save anywhere in PATH, make it executable, add your api key as `OPENAI_API_KEY` env variable.

**Example usage**

```
my-cool-project $ git add -u
my-cool-project $ commitgpt

1. Improve unit tests for user authentication
5. Improve unit tests for user authentication module
6. Write initial unit tests

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