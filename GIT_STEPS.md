# Git Steps for satyaRaspi/1ssa

Run these commands from the extracted project folder.

```bash
cd /Users/satyassrinivasan/Desktop/1ss
```

```bash
git init
git branch -M main
git add .
git commit -m "Initial Shakti Scheme application deployment"
git remote add origin https://github.com/satyaRaspi/1ssa.git
git push -u origin main
```

If the remote already exists:

```bash
git remote set-url origin https://github.com/satyaRaspi/1ssa.git
git push -u origin main
```

If Git says there is nothing to commit, check status:

```bash
git status
```

If Git asks for credentials, use username:

```text
satyaRaspi
```

For password, use a GitHub Personal Access Token, not the normal GitHub password.
