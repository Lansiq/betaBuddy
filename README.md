# betaBuddy
McMaster 2021 Capstone Project

# How to use
Can download [Github App](https://desktop.github.com/) to run all commands and see changes

or

Can use command prompt as well, see commands below:

# Helpful Commands
Below is a set of commands to use for pushing and pulling from the git repository. Please read and ask me if you need clarification on what each does.

### git add ***filename.extention***
Will stage files, i.e., get them ready to commit
 > Bash commands can be used, i.e., to stage all changed files
```
git add *
```

### git commit -m "***commitMessage***"
Will update the local repository with the files you listed in your "git add"
 > Git requires a message to commit describing changes you made.

### git push
Any commited changes will be updated on the git server for everyone to pull from

### git fetch
Checks if there are any changes/inconsistencies between your local repository and github

### git pull
Updates all files to be up to date on your local repository

### git merge
If multiple people are working on the projects at the same time, you may need to do a merge if another user pushes before you.

This means your project repository is currently out of date (regardless if the file you are working on is different), therefore merging allows all changes across all users to be synched up.

Just ensure multiple people ***ARE NOT*** working on the *same* file.

### git checkout -b ***branchName***
To alleviate issues with merging on the same project, new branches can be developed which essentially makes a "copy" of the original branch. Therefore changes can be made on the same files without needing to merge.

Merging will only occur when commiting to the main branch, i.e.,
 ```
 git checkout master
 git merge ***branchName***
 ```