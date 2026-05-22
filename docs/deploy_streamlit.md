# Deploy to Streamlit Community Cloud

Streamlit Community Cloud deploys from GitHub. This local project must be pushed to a
remote GitHub repository before deployment.

## Repository Settings

- Repository: create a GitHub repository, for example `dynamic-balance`.
- Branch: `main`.
- Main file path in Streamlit: `app/ui/Home.py`.
- Dependencies file: `requirements.txt`.

## Local Git Commands

After creating an empty GitHub repository, run:

```powershell
git remote add origin https://github.com/<your-user>/dynamic-balance.git
git branch -M main
git push -u origin main
```

Then open Streamlit Community Cloud and deploy:

```text
Repository: <your-user>/dynamic-balance
Branch: main
Main file path: app/ui/Home.py
```

## Important

Do not commit real bank data. Keep real files under:

- `data/raw/`
- `data/private/`
- `reports/private/`

These folders are ignored by Git.
