#
#
#
.DEFAULT_GOAL := help

ifneq ($(token),)
	# To get a personal token, visit https://github.com/settings/tokens and log in.
	export GITHUB_REPO_TOKEN=$(token)
endif


.venv:
	# creating virtual environment $@
	@python3 -m venv $@
	@$@/bin/pip install --upgrade pip setuptools wheel


.PHONY: devenv
devenv: scripts/requirements.txt .venv ## creates virtual env and install dev tools
	# installing $<
	@.venv/bin/pip install -r $<


draft-agenda.md: ## markdown with review agenda provided a personal access token (set GITHUB_REPO_TOKEN or 'make token=1234 review-draft.md').
	@.venv/bin/python3 scripts/new-review.py --token=${GITHUB_REPO_TOKEN} agenda --output=$@


.PHONY: shell
shell: .venv ## starts a python shell
	# Starting python ...
	@.venv/bin/python3


.PHONY: clean
clean: ## cleans unversioned and ignored files
	@git clean -ndfx
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	# remove unversioned
	-@git clean -dfx


.PHONY: help
help: ## this colorful help
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]._-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

