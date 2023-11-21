# Contribution

## How to Contribute

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run `pre-commit run --all-files` to run all hooks on all files. (See [Pre-Commit Hooks](instructions_for_pre-commit.md) for more information)
5. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the Branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

- Pull requests must be reviewed by at least one other person before being merged.
- Pull requests must pass all checks before being merged.
- If you have access to the slack channel, please post a link to your PR in the slack channel, that is the fastest way to get it reviewed.

## Workflow

Typically, you will make a feature branch off of `main` and make your changes there. When you are done, you will open a pull request to merge your feature branch into `main`.

You can name your feature branch whatever you want, but it is recommended to use the following naming convention:

either 
* `feat/<feature-name>`
* `bugfix/<bug-name>`
* `hotfix/<hotfix-name>` 
* `<ticket-number>/<feature-name>`

For example, if you are working on a feature to add a new endpoint to the transcription service, you could name your branch `feat/add-new-endpoint-to-transcription-service`.

## Specifications

* [Style Guide](style_guide.md)
* [Instructions for Pre-Commit](instructions_for_pre-commit.md)

## Editing Documentation
* Please see [Editing Documentation](editing_docs.md) for more information on how to edit this documentation! 

## Raise an Issue

If you have a suggestion that would make this better, please fork the repo and create an issue. You can also simply open an issue with the tag "enhancement". We have templates for issues, so please use them!

## Reminders

* Be sure to write tests for your code. These are within the `tests` directory.
  * Your PR will not be merged if it does not pass all tests.
* Be sure to write docstrings for your code. 
* You have to re-run `git add` after the pre-commit hook runs.
* Pull requests must be reviewed by at least one other person before being merged.
* Keep your PRs small and focused. If you have multiple changes, please make multiple PRs! This makes it easier to review and merge.