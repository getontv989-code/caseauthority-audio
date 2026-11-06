Build inputs the blog deploy's build.sh downloads (SHA1-checked) before building:
new post files (posts__zNN-<slug>.py), audio manifest.json and fetch_audio.py.
This keeps big text files out of the deploy request. See redesign/blog-split/README.md in the project files.
