---
name: Pre-release to staging
about: Creates an issue to pre-release from master to staging deploy
title: 'Pre-release master -> staging_SPRINTNAME_VERSION (DATE)'
labels: ''
assignees: 'pcrespov'

---

In preparation for [pre-release](https://github.com/ITISFoundation/osparc-simcore/releases). Here an initial (incomplete) list of tasks to prepare before pre-releasing:


- [ ] Draft changelog from commits list (see [docs/releasing-workflow-instructions.md](https://github.com/ITISFoundation/osparc-simcore/blob/6cae77e5444f825f67fca65876922c8d26901fd2/docs/releasing-workflow-instructions.md))
- [ ] Check important changes 🚨
- [ ] Devops check (⚠️ devops)
- [ ] e2e testing check
- [ ] Pre-release summary
- [ ] After-release notes

---


# Check important changes 🚨

<!-- Staging is an intermediate environment between development (master) and production that allows us to test in isolation
changes in the framework. In addition, the pre-release workflow shall be used as a simulation to production that can help us to
anticipate changes and mitigate failures. 

Explain what motivates this pre-release? Which important changes we might pay attention to? How should we
test them? Is there anything in particular we should monitor?

In this section start first with a *motivation*; then mark 🚨 important changes in changelog and add an explanation 
on how to test them (append as [TODO: ... ] after selected changelog entries).
-->



#  Devops check (⚠️ devops)
<!-- The goal here is to analyze the PRs marked with (⚠️ devops).  We should determine and prepare necessary changes required in the environments configs. 

This procedure should be taken also as an exercise in preparation for the release to production as well.
 -->


# e2e testing check
<!-- Check that e2e in master: are there any major known issues? -->




# Draft Changelog
<!-- Changelog follow structure defined in https://keepachangelog.com/en/1.0.0/ -->


## Added
<!-- Added for new features.  -->
## Changed
<!-- Changed for changes in existing functionality.  -->
## Deprecated
<!-- for soon-to-be removed features. -->
## Removed
<!-- for now removed features. -->
## Fixed
<!-- for any bug fixes. -->
## Security / Maintenance
<!--  Security in case of vulnerabilities.
	or some maintanence work on CI/CD/tests/scripts
 -->


**Legend**

- ✨ New feature
- 🐛 Fixes bugs
- ♻️ Refactors code
- ⬆️ Upgrades dependencies
- 🔒️ Fixes security issues
- 🔨 Adds or updates development scripts or CI.
- 🚨 Important change. REQUIRES target testing before releasing to production. Steps to test appended as ``[TODO:  ... ]``
- 📌 can be cherry-picked to production




# Pre-release summary

- what:  <!-- ```make release-staging name=switzer version=2 git_sha=dbcc9a645f25468ed57d227c42e8daad6ccb62d8``` in [``master``](https://github.com/ITISFoundation/osparc-simcore/commits/master) -->
- who: <!-- @Surfict @GitHK  -->
- when: <!-- THURSDAY Oct.20, afternoon -->



# After-release notes


<!-- 
This section is to keep notes/logs about the pre-release process. We should report any problem or incident
that occurred during this process. Notes on special warnings or configurations we should pay attention ...
or in general any relevant information that helps us mitigate the risk of failure when releasing to production
 -->