# Programmatic Content Hub

## 1. How to run the local test server
To view the generated site locally, run the following command in your terminal from the `auto-revenue-hub` directory:
```bash
cd public
python -m http.server 8000
```
Then open your web browser and go to `http://localhost:8000`.

## 2. How to push this to GitHub for 100% free hosting
Initialize a git repository, commit the files, and push to a new GitHub repository:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```
Once pushed:
1. Go to your repository settings on GitHub.
2. Navigate to **Pages** (under the "Code and automation" section).
3. Under "Build and deployment", set the source to **GitHub Actions**.
4. The included `.github/workflows/main.yml` will automatically build your site and deploy it to GitHub Pages for free twice a day.

## 3. Where to paste the affiliate links
Open the `build_site.py` file in your editor.
Look for the following string templates near the top of the file (lines 115-128):

```python
AD_TOP = """
        <!-- TODO: Paste your Google AdSense code OR Amazon Affiliate Banner here -->
        <div class="ad-container">
            <p><em>Advertisement Placeholder (Top)</em></p>
            <!-- INS ID: YOUR_TRACKING_ID_HERE -->
        </div>
"""

AD_BOTTOM = """
        <!-- TODO: Paste your Google AdSense code OR Amazon Affiliate Banner here -->
        <div class="ad-container">
            <p><em>Advertisement Placeholder (Bottom)</em></p>
            <!-- INS ID: YOUR_TRACKING_ID_HERE -->
        </div>
"""
```
Replace the content inside these HTML string blocks with your actual Google AdSense script tags or Amazon Affiliate banner HTML. The python script will automatically inject them into every generated page.
