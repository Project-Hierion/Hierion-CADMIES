
## **Basic Workflow**
# Check repo status

git status

**Add files to staging**

git add <file>              # Add specific file
git add .                   # Add all files
git add *.js               # Add all JS files

# Commit changes
git commit -m "Commit message"
git commit -am "Add and commit tracked files"

# Push to remote
git push origin main
git push -u origin main    # Set upstream and push


**Merging and Pulling**

# Fetch and merge
git pull origin main
git pull --rebase origin main

# Merge branches
git merge <branch-name>

# Fetch without merging
git fetch origin


**Undoing Changes**
Discard working directory changes

git checkout -- <file>
git restore <file>

#Unstage files
git reset HEAD <file>
git restore --staged <file>

# Amend last commit
git commit --amend -m "New message"

# Revert a commit
git revert <commit-hash>

**Viewing History**
View commit history

git log
git log --oneline
git log --graph --oneline --all

# View changes
git diff                   # Unstaged changes
git diff --staged          # Staged changes
git show <commit-hash>     # Specific commit details


**Stashing**  (quick save to continue working, then commit everything at once)

# Save changes temporarily
git stash
git stash save "message"

# List stashes
git stash list

# Apply stashed changes
git stash apply
git stash pop              # Apply and remove from stash

# Drop stash
git stash drop