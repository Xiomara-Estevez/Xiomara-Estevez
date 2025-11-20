import express from "express";
import multer from "multer";
import fetch from "node-fetch";
import dotenv from "dotenv";
import fs from "fs";
import path from "path";

dotenv.config();

const app = express();
const upload = multer({ dest: "uploads/" });

app.use(express.static("public"));
app.use(express.json());

// Basic health check
app.get("/health", (req, res) => res.send({ ok: true }));

/**
 * POST /upload
 * - file: multipart form field "file"
 * - optional form field "targetPath": path inside repo (e.g., "submissions/user123/")
 *
 * Server reads uploaded file and commits to GitHub repo using a Personal Access Token.
 */
app.post("/upload", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }
    const { originalname, path: filepath } = req.file;
    const targetPath = (req.body.targetPath || "").replace(/^\/+/, "");

    // Read file
    const buffer = fs.readFileSync(filepath);
    const contentBase64 = buffer.toString("base64");

    // Compose repo path (timestamp prefix to avoid overwrite)
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    const repoPath = `${targetPath}${timestamp}-${originalname}`;

    // GitHub API: create or update file
    const ownerRepo = process.env.GITHUB_REPO; // format: "owner/repo"
    if (!ownerRepo) throw new Error("GITHUB_REPO not configured in env");

    const url = `https://api.github.com/repos/${ownerRepo}/contents/${encodeURIComponent(
      repoPath
    )}`;

    const body = {
      message: req.body.commitMessage || `Upload from Brightspace Companion: ${originalname}`,
      content: contentBase64
    };

    const token = process.env.GITHUB_TOKEN;
    if (!token) throw new Error("GITHUB_TOKEN not configured in env");

    const ghRes = await fetch(url, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "User-Agent": "brightspace-bridge",
        Accept: "application/vnd.github+json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });

    const ghJson = await ghRes.json();

    // cleanup uploaded file
    fs.unlinkSync(filepath);

    if (!ghRes.ok) {
      console.error("GitHub API error:", ghJson);
      return res.status(500).json({ error: "GitHub API error", details: ghJson });
    }

    // Optionally trigger a repository_dispatch event (uncomment if you want)
    // await triggerRepoDispatch(ownerRepo, token, "brightspace_upload", { path: repoPath });

    return res.json({
      ok: true,
      path: ghJson.content?.path,
      sha: ghJson.content?.sha,
      url: ghJson.content?.html_url
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: err.message });
  }
});

// Optional: endpoint for testing commit with JSON content (no file)
app.post("/commit-json", async (req, res) => {
  try {
    const { filename = `data-${Date.now()}.json`, json } = req.body;
    if (!json) return res.status(400).json({ error: "no json provided" });

    const ownerRepo = process.env.GITHUB_REPO;
    const token = process.env.GITHUB_TOKEN;
    const contentBase64 = Buffer.from(JSON.stringify(json, null, 2)).toString("base64");

    const url = `https://api.github.com/repos/${ownerRepo}/contents/${encodeURIComponent(filename)}`;

    const ghRes = await fetch(url, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "User-Agent": "brightspace-bridge",
        Accept: "application/vnd.github+json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: `JSON commit ${filename}`,
        content: contentBase64
      })
    });

    const ghJson = await ghRes.json();
    if (!ghRes.ok) {
      console.error(ghJson);
      return res.status(500).json({ error: "GitHub API error", details: ghJson });
    }

    return res.json({ ok: true, html_url: ghJson.content?.html_url });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server listening on ${port}`));
