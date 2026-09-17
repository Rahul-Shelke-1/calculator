# Cloudflare Pages Deployment

This guide documents the setup required to deploy the Calculator documentation site to Cloudflare Pages using GitHub Actions.

The deployment flow is:

```text
GitHub Repository
       │
       │ GitHub Actions
       ▼
Wrangler
       │
       │ API Token
       ▼
Cloudflare
       │
       ▼
Cloudflare Pages
       │
       ▼
Calculator Documentation
```

## Prerequisites

Before starting, make sure you have:

* A Cloudflare account
* A GitHub repository
* A Cloudflare Pages project
* The Cloudflare account ID
* A Cloudflare API token with the required Pages permissions
* GitHub Actions enabled for the repository

---

## 1. Create the Cloudflare Pages Project

Sign in to the Cloudflare dashboard and navigate to **Workers & Pages**.

Create a Pages project for the documentation site.

For this project, the Pages project is:

```text
calculator-docs-preview
```

The project name is important because it is referenced by Wrangler during deployment:

```bash
npx wrangler pages deploy site \
  --project-name calculator-docs-preview
```

Keep the project name consistent between Cloudflare and the GitHub Actions workflow.

---

## 2. Find the Cloudflare Account ID

The Cloudflare account ID identifies the Cloudflare account that owns the Pages project.

It can be found in the Cloudflare dashboard under the account information.

Store it as:

```text
CLOUDFLARE_ACCOUNT_ID
```

Example:

```text
CLOUDFLARE_ACCOUNT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Important

The account ID is **not a secret** in the same way an API token is. However, it is still useful to keep it in the GitHub Actions configuration rather than hard-coding infrastructure-specific values throughout the workflow.

---

## 3. Create a Cloudflare API Token

Navigate to the Cloudflare [API Tokens](https://dash.cloudflare.com) section.

Create a **Custom Token** rather than using the global API key.

Use a descriptive name, for example:

```text
calculator-github-pages-deploy
```

The token should have only the permissions required for the Pages deployment.

For the Pages deployment, the token needs the appropriate **Cloudflare Pages write/edit permission** and **Workers Scripts Write** for the target account.

Avoid giving the token unnecessary account-wide permissions.

---

## 4. Configure Token Expiration

When creating the token, Cloudflare allows an expiration/TTL to be configured.

For a GitHub Actions deployment token, understand the consequence before choosing a short TTL.

For example:

```text
Token created
     │
     ▼
Active
     │
     │  TTL = 7 days
     ▼
Expired
```

If a one-week expiration is configured, the GitHub Actions deployment will stop working once the token expires.

For a long-running project, either:

* use an appropriate longer lifetime, or
* deliberately use a short lifetime and rotate the token as part of the security process.

Do not assume that a token failure means the GitHub Actions workflow is broken.

---

## 5. Save the API Token

Cloudflare displays the API token when it is created.

Store it securely.

The token should **never** be committed to the repository.

Do not put it in:

```text
.env committed to Git
GitHub workflow YAML
README.md
MkDocs documentation
source code
```

The token should instead be stored as a GitHub Actions secret.

---

## 6. Verify the Token Locally

Before configuring GitHub Actions, verify that the token itself works.

Set the environment variables locally:

```bash
export CLOUDFLARE_API_TOKEN="your-token"
export CLOUDFLARE_ACCOUNT_ID="your-account-id"
```

Do not print the token.

The token can be verified through Cloudflare's token verification API.

For this project, a helper script is available at:

```text
scripts/check_cloudflare_token.py
```

Run it with:

```bash
uv run --with requests python scripts/check_cloudflare_token.py
```

A successful result should look similar to:

```text
Checking Cloudflare API token...
✅ Token is valid: active
Checking Cloudflare account access...
✅ Cloudflare account access confirmed.
   Account: My Account
   Account ID: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

🎉 Cloudflare authentication is working.
```

This verifies two things:

1. The API token is valid.
2. The token can access the specified Cloudflare account.

---

## 7. Configure GitHub Actions Secrets

Go to:

```text
GitHub Repository
    → Settings
    → Secrets and variables
    → Actions
```

Create the following repository secrets:

```text
CLOUDFLARE_API_TOKEN
CLOUDFLARE_ACCOUNT_ID
```

### `CLOUDFLARE_API_TOKEN`

Value:

```text
<the Cloudflare API token>
```

### `CLOUDFLARE_ACCOUNT_ID`

Value:

```text
<the Cloudflare account ID>
```

GitHub Actions exposes these values to the workflow without storing them directly in the repository.

---

## 8. Configure the GitHub Actions Workflow

The workflow uses the official Cloudflare Wrangler GitHub Action.

The relevant deployment step is:

```yaml
- name: Publish Preview to Cloudflare Pages
  id: cloudflare_deploy
  uses: cloudflare/wrangler-action@v4
  with:
    apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
    command: pages deploy site --project-name calculator-docs-preview --branch=${{ github.head_ref }}
    gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

The important pieces are:

```yaml
apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

and:

```yaml
accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

The deployment command is:

```bash
pages deploy site --project-name calculator-docs-preview
```

Here:

```text
site/
  │
  └── Generated MkDocs site
```

is the directory being uploaded to Cloudflare Pages.

---

## 9. Build the Documentation

Before deployment, MkDocs generates the static documentation site.

For example:

```bash
uv run mkdocs build
```

This produces:

```text
site/
├── index.html
├── ...
└── ...
```

The generated `site/` directory is then passed to Wrangler.

---

## 10. Deployment Flow

The complete workflow is:

```text
Developer
    │
    │ Push / Pull Request
    ▼
GitHub
    │
    ▼
GitHub Actions
    │
    ├── Build documentation
    │
    ├── Test
    │
    └── Generate site/
    │
    ▼
Wrangler
    │
    │ CLOUDFLARE_API_TOKEN
    │ CLOUDFLARE_ACCOUNT_ID
    ▼
Cloudflare API
    │
    ▼
Cloudflare Pages
    │
    ▼
calculator-docs-preview
```

---

## 11. Trigger the Workflow

Push the workflow changes to GitHub:

```bash
git push
```

Then open:

```text
GitHub Repository
    → Actions
    → Cloudflare Pages workflow
```

The workflow should:

1. Checkout the repository.
2. Install dependencies.
3. Build the documentation.
4. Generate the `site/` directory.
5. Authenticate Wrangler using the GitHub secret.
6. Deploy `site/` to Cloudflare Pages.

---

## 12. Verify the Deployment

After the GitHub Actions workflow succeeds, verify that the documentation site is available through the configured Cloudflare Pages URL.

For the Calculator project, the documentation deployment is separate from the Flask application deployment.

```text
Calculator Application
        │
        └── Flask
             └── Future AWS deployment

Calculator Documentation
        │
        └── MkDocs
             └── Cloudflare Pages
```

This separation keeps application infrastructure independent from documentation hosting.

---

# Troubleshooting

## `Invalid API Token`

Example:

```text
Authentication error [code: 10000]
Invalid access token [code: 9109]
```

or:

```text
HTTP 401
code: 1000
message: Invalid API Token
```

First verify the token locally:

```bash
uv run --with requests python scripts/check_cloudflare_token.py
```

If the script reports:

```text
❌ Token verification failed
```

the problem is with the token itself rather than GitHub Actions.

Possible causes include:

* The token expired.
* The token was revoked.
* The token was deleted.
* The token was copied incorrectly.
* The token does not have the required permissions.

Create a new token if necessary and update:

```text
CLOUDFLARE_API_TOKEN
```

in GitHub repository secrets.

---

## Token Is Valid but Deployment Fails

If token verification succeeds but the Pages deployment fails, check:

1. `CLOUDFLARE_ACCOUNT_ID` is correct.
2. The token belongs to the same Cloudflare account.
3. The token has the required Pages permissions.
4. The Pages project exists.
5. The project name is correct.

The project name must match:

```text
calculator-docs-preview
```

and the workflow:

```bash
--project-name calculator-docs-preview
```

---

## Never Debug by Printing the Token

Do **not** add:

```bash
echo "$CLOUDFLARE_API_TOKEN"
```

to the workflow.

Do not print the token from Python either.

A credential should be treated as compromised if it is accidentally exposed in logs.

If a token is exposed, revoke it and create a new one.

---

# Credential Management Summary

| Credential              | Purpose                       |                Secret? | Storage                        |
| ----------------------- | ----------------------------- | ---------------------: | ------------------------------ |
| `CLOUDFLARE_API_TOKEN`  | Authenticate Wrangler         |                    Yes | GitHub Actions Secret          |
| `CLOUDFLARE_ACCOUNT_ID` | Identify Cloudflare account   |                     No | GitHub Actions Secret/Variable |
| `GITHUB_TOKEN`          | GitHub Actions authentication | Automatically provided | GitHub Actions                 |

The important security boundary is:

```text
Cloudflare API Token
        │
        ▼
GitHub Secret
        │
        ▼
GitHub Actions
        │
        ▼
Wrangler
        │
        ▼
Cloudflare Pages
```

The API token never needs to exist in the Git repository itself.
