# Publishing prytaniapartners.com — step-by-step guide

This guide takes the `site/` folder in this package live at
**https://www.prytaniapartners.com** using GitHub Pages (free, no subscription).
It also covers moving your DNS away from the old Wix placeholder.

Total time: roughly 30–45 minutes, plus DNS propagation (minutes to a few hours).

---

## Step 1 — Create a GitHub account and repository

1. Go to https://github.com and sign up (free) if you don't have an account.
2. Click **New repository**. Name it `prytania-website` (any name works).
   Set it to **Public** — required for free GitHub Pages. Note: the *code* is
   public, which is fine for a website, but see the note on preview privacy below.
3. On your new repository page, click **uploading an existing file** (or
   **Add file → Upload files**) and drag in the **contents of the `site/`
   folder** — `index.html`, `styles.css`, `404.html`, `robots.txt`,
   `sitemap.xml`, and the `p/` folder. The files must sit at the top level of
   the repository, not inside a `site/` subfolder.
4. Click **Commit changes**.

## Step 2 — Turn on GitHub Pages

1. In the repository, go to **Settings → Pages**.
2. Under *Build and deployment*, set **Source** to `Deploy from a branch`,
   branch `main`, folder `/ (root)`. Save.
3. After a minute, the page shows a URL like
   `https://<your-username>.github.io/prytania-website/`. Open it — your site
   is live on that temporary address.

## Step 3 — Connect your domain

1. Still in **Settings → Pages**, under *Custom domain*, enter
   `www.prytaniapartners.com` and save. GitHub creates a `CNAME` file in the
   repository — leave it there.
2. Now update DNS where your domain is registered. If your domain is
   currently *managed by Wix* (nameservers point to Wix), log in to Wix →
   Domains → prytaniapartners.com → **Manage DNS records**. If it's at another
   registrar (GoDaddy, Namecheap, TransIP, etc.), edit DNS there instead.
3. Remove/replace the existing Wix records and add:

   | Type  | Host/Name | Value                     |
   |-------|-----------|---------------------------|
   | CNAME | www       | `<your-username>.github.io` |
   | A     | @         | 185.199.108.153           |
   | A     | @         | 185.199.109.153           |
   | A     | @         | 185.199.110.153           |
   | A     | @         | 185.199.111.153           |

   The four A records make the bare domain `prytaniapartners.com` work too.
4. Back in GitHub **Settings → Pages**, once DNS has propagated, tick
   **Enforce HTTPS**. GitHub issues a free SSL certificate automatically.
5. If you were paying Wix for a site plan (not just the domain), you can
   cancel it — the domain registration itself is the only thing to keep.

## Step 4 — Verify

- https://www.prytaniapartners.com loads the new homepage over HTTPS.
- https://prytaniapartners.com redirects to the www version.
- A wrong address like /nothing-here shows the custom 404 page.
- The sample preview works: `/p/q6aN2EjKG4xT/`.

---

## Working with private project previews

Each project preview lives at an unguessable address like
`https://www.prytaniapartners.com/p/q6aN2EjKG4xT/`. These URLs are never
linked from the public site, carry a `noindex` tag so search engines that
stumble on them won't list them, and use ~72 bits of randomness — effectively
impossible to guess.

To create a new preview, run (from this folder, Python 3 required):

    python3 tools/new_preview.py "Project title" "Client name"

It creates the folder, prints the private URL, and you put the
work-in-progress files in its `draft/` subfolder. Then upload the new folder
to GitHub the same way as in Step 1 (or `git push` if you use git). To
withdraw access, delete the folder — the link then shows the 404 page.

**Privacy note:** with a free *public* GitHub repository, someone who finds
your GitHub account could technically browse the repository and see the
preview folders. If that matters, either (a) make the repository **private**
and host on **Cloudflare Pages** or **Netlify** instead (both deploy private
repos free — same files, same result), or (b) upgrade to GitHub Pro. Unique
links are a courtesy lock, not a vault: don't put truly confidential material
in previews regardless of host.

---

## Alternative: Cloudflare Pages (also free, private repo allowed)

1. Sign up at https://pages.cloudflare.com, connect your GitHub repository
   (can be private) or drag-and-drop the `site/` folder directly.
2. Add the custom domain `www.prytaniapartners.com` in the Pages project.
3. Cloudflare walks you through pointing DNS (usually moving nameservers to
   Cloudflare, which also speeds the site up worldwide).

Everything else in this guide works the same.
