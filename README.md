## Google-repo-action

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Javier-varez/google-repo-action/Checkout%20tests)

This is a Github action to checkout multiple repositories managed with a single Manifest file. It does this by using the [Google-repo](https://gerrit.googlesource.com/git-repo/). This tool is commonly used with Gerrit. Although support for a normal git server like Github is not optimal, It still seems like a good option to manage multiple interdependent repositories.

## Using this action

The following example shows how to use this action.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: checkout
      uses: Javier-varez/google-repo-action@v0.2
      with:
        manifest-url: 'Organization/repo'
        manifest-branch: 'main'
        manifest-file: 'default.xml'
        manifest-group: 'default'
        checkout-deps: false
```

  * `manifest-url` declares the Github organization and the repository inside it that contains the manifest.
  * `manifest-branch` is used to define the branch for the manifest file.
  * `manifest-file` select the specific file within the specified branch and provided manifest repo url.
  * `manifest-group` can be used to checkout a specific group or set of groups.
  * `checkout-deps` can be used to dowload interdependent changes in the context of presubmit testing.
  * `generated-manifest` can be set if you want to generate a manifest with the checked-out frozen revisions of the repo.

## Downloading dependent changes during presubmit

Gerrit provides a `Depends-On` tag that can be used to mark interdependent changes during presubmit testing in the CI environment. This creates cross-links between repositories by using the `Change-Id` of a given change. However, we cannot use this concept with `Github`, since it does not keep track of commits or changes by `Change-Id`.

Instead, we follow a different approach. We will use a `Depends-On` tag in the commit message, but instead of referncing the `Change-Id`, we can reference dependent Github projects following the `organization/repo` naming.

Let's say that we have 2 different repositories in our manifest, like so:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
  <remote fetch="https://github.com" name="github" review="https://github.com"/>
  <default revision="main" remote="github" sync-j="4" sync-s="true" />

  <project name="MyOrganization/RepoA" path="repo_a" />
  <project name="MyOrganization/RepoB" path="repo_b" />
</manifest>

```

Now, when a change in `RepoA` depends on a change in `RepoB`, we can simply mark it in the commit message like this:

```
Commit title

Commit message text

Depends-On: MyOrganization/RepoB
```

Then we push this in a branch (let's use the name `feature_branch` for this example) to Github. This triggers the Github Workflow in `RepoA`. If `checkout-deps` is `true`, this Github Action will perform the following actions:

  * Download the repository for the given manifest xml.
  * Checkout the `GITHUB_REF` (`feature_branch` in our example) of the repository that originated the checkout.
  * Inspect the commit message looking for any `Depends-On` tags.
  * Checkout the same `GITHUB_REF` in those repositories too.

Now, when doing presubmit testing for the change in `RepoA` it will be tested with the respective branch in `RepoB`, which doesn't need to be submitted to the main branch.

