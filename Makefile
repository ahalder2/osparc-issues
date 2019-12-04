#
#
#
.DEFAULT_GOAL := help

token ?= unknown

.venv:
	# creating virtual environment $@
	@python3 -m venv $@
	@$@/bin/pip install -U pip setuptools wheel


.PHONY: devenv
devenv: scripts/requirements.txt .venv ## creates virtual env and install dev tools
	# installing $<
	@.venv/bin/pip install -r $<


draft-agenda.md: ## produces a review draft. Usage make token=1234 review-draft.md
	@.venv/bin/python3 scripts/new-review.py --token=$(token) agenda --output=$@


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
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

