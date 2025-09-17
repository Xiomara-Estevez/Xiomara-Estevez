# Deploying the Patient Portal to AWS Amplify

This repo contains a simple static site in the `Patient_portal/` folder. The following steps will publish it to AWS Amplify and ensure the Cognito Hosted UI redirects back to the deployed site.

1. Connect repository to Amplify
   - In the AWS Console, open **AWS Amplify** → **Get started** → **Host web app**.
   - Connect your Git provider and select the repository `Xiomara-Estevez` and branch `main`.
   - For **Build settings**, Amplify will detect `amplify.yml` at the repo root; it will publish the `Patient_portal` folder.

2. App URL and callback
   - After Amplify finishes deploying you'll get a URL like `https://<appId>.amplifyapp.com` (optionally with branch subpath).
   - Decide which page you want Cognito to redirect to after sign-in:
     - Option A: `index.html` — redirect to `https://<app>.amplifyapp.com/index.html` so the app receives `?code=` and then client-side JS can forward to `welcome_portal.html`.
     - Option B: `welcome_portal.html` — redirect directly to the portal landing page.

3. Configure Cognito App client
   - Open Amazon Cognito → User Pools → select your pool → App client settings.
   - Under **Callback URL(s)** add the exact Amplify URL(s) you will use. Examples:
     - `https://<app>.amplifyapp.com/index.html`
     - `https://<app>.amplifyapp.com/welcome_portal.html`
   - Also add the same to **Sign out URL(s)**.
   - Save changes.

4. Verify flow
   - Click your Amplify app URL, open the Register/Login link, complete hosted UI sign-in.
   - Confirm the hosted UI returns to the chosen callback with `?code=` or with tokens in the fragment.
   - If you used `index.html`, the `portal.js` script (already adjusted) will detect params and redirect to `welcome_portal.html`.

Notes
   - The repo includes an `amplify.yml` that instructs Amplify to publish the `Patient_portal` directory.
   - If your Cognito app uses a custom domain or multiple environments, add each domain exactly in the callback list.
