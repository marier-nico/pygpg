# Contributing To pygpg

Thanks for considering contributing to this project! Generally, if
you're ever unsure about anything, just ask. Don't be afraid of doing
something wrong, if something needs tweaking, you'll get helpful feedback.

# How Can I Contribute

## Reporting Bugs

To report a bug, open an issue and describe the problem you've
encountered. You should give some steps to reproduce as well.

## Suggesting Features

To suggest a feature, open an issue and explain what the feature would
do, how it would be used and why it would be useful.

## Contributing Code

Feel free to just open a pull request if you're confident that what
you're doing would be a good fit for this project. Make sure to read
the pull request template for more specific instructions.

# Style Guide

## Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 50 characters or less
- Do not include a period (`.`) at the end of the first line
- Include a line skip between the first line and the rest of your commit
- Explain what the commit does and why it does it after the first line
- Reference issues and pull requests liberally after the first line
- Wrap text at 72 characters after the first line

**Example**
```
Subject line (imperative, <= 50 chars, no ".")

Multi-line description of a commit,
explain what and why, not how.
Wrap at 72 characters.

[Ticket: X]
```

**Note**: For pull requests, the title corresponds to the commit's
subject line. The description of the pull request, up to its first
[thematic break](https://github.github.com/gfm/#thematic-breaks),
corresponds to the commit's body (multi-line description in the example
above).

## Python Style Guide

Formatting is enforced with [black](https://github.com/psf/black), and
type hints are enforced with [mypy](https://github.com/python/mypy).
Code style is enforced by both [pylint](https://github.com/PyCQA/pylint)
and [flake8](https://github.com/PyCQA/flake8).
