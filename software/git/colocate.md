Co-located
==========

Storing multiple git repositories in a single directory (not using submodules). For _this_ purpose there is a repository (1) which should be read/write and others that are read-only (that's important later).

```
mv .git .git-repo1
# now clone the second
git clone <repo2>
mv .git .git-repo2
mv .git-repo1 .git
```

At this point repo1 (the read/write repo) is now going to respond to 'git' commands. To run against another repo
```
git --git-dir=.git-repo2 <command>
```

There will be some difficulties with multiple .gitignore but if only one repo (1) has one, it can have exclusions defined for the others ones (since the others are read-only in this case)

```
git --git-dir=.git-repo2 config core.excludefiles ".git-repo2-exclude"
```

Of course the .git-repo2-exclude file would need to be included in repo1's repository.

## References

[1] http://stackoverflow.com/questions/436125/two-git-repositories-in-one-directory

