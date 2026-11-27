set -e
R=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/177bcf9dedce746e733125daafcfefd89d301dc2
get(){ for i in 1 2 3 4; do if curl -fsSL "$R/$1" -o "$2" && [ "$(sha1sum < "$2" | cut -c1-40)" = "$3" ]; then return 0; fi; sleep $((2**i)); done; echo "build input fetch failed: $1"; exit 1; }
get build/engine-2026-11-08.txz engine.txz fc7528cffa2cf2b8002ae1ed184ea67deeff3e61
get build/sister/brand-estate.txz brand-estate.txz 54f0721ae80e6deee8ee6925d44987ed84e1ccfd
python3 -c "import glob,tarfile;[tarfile.open(f).extractall() for f in sorted(glob.glob('*.txz'))]"
mkdir -p brands/estate/posts engine/.cache media
get build/sister/estate/website-redesign-seo-for-estate-planning-firms.json brands/estate/posts/website-redesign-seo-for-estate-planning-firms.json 399bea56057327e498b150803c6b646247ba4f05
get build/sister/estate/seo-vs-ppc-for-estate-planning-attorneys.json brands/estate/posts/seo-vs-ppc-for-estate-planning-attorneys.json 6700eb0db7707d82941aaee914c3b22da89eb7d3
get build/sister/estate/zero-click-searches-for-estate-planning-firms.json brands/estate/posts/zero-click-searches-for-estate-planning-firms.json b255635dd799e9744777a4b5548454ff6f66ebf2
get build/sister/estate/link-building-for-law-firms.json brands/estate/posts/link-building-for-law-firms.json 1ee921664bb1d76423dc31574b61d8795433cb54
get build/sister/estate/get-found-online-first-seo-for-estate-planning-attorneys.json brands/estate/posts/get-found-online-first-seo-for-estate-planning-attorneys.json 49100b943b7870bf3ba73634f887966fddea326f
get build/sister/estate/how-to-rank-in-google-ai-mode.json brands/estate/posts/how-to-rank-in-google-ai-mode.json 5c8854d7db8cc4be7a87c9bf7540d16f2e529985
get build/sister/estate/seo-retainer.json brands/estate/posts/seo-retainer.json abe2d9c92f9232c9cfc9c3436145d15c405693ee
get build/sister/estate/estate-planning-seminars.json brands/estate/posts/estate-planning-seminars.json 4b842f12d7f61af1d22cb550d289060e523db200
get build/sister/estate/martindale-av-rating.json brands/estate/posts/martindale-av-rating.json b1ded15d035f99665835e7dd41b04142677cd153
get build/sister/estate/how-to-get-estate-planning-clients.json brands/estate/posts/how-to-get-estate-planning-clients.json bb3f488cf26f64b1a74512976f887cbb4c769e5f
get build/sister/estate/estate-planning-marketing-ideas.json brands/estate/posts/estate-planning-marketing-ideas.json ddb7fd837fe1b14d21de8ff46a8568745e934764
get build/sister/site-pinned.js engine/.cache/site.js 953b43503bed7ed465276d16778f4a526845f3d0
python3 engine/build.py brands/estate public
python3 engine/verify.py brands/estate public
get audio_patch.py audio_patch.py 5d554d6f70574bb34021f19927023b5348d9ce54
get explainer_patch.py explainer_patch.py dff467bf5cdd91bc095080fb536141fa25592c10
get build/sister/sister_media.py sister_media.py 96a7dab8176e4126313556515aeabefcc9407681
get build/sister/estate-manifest.json media/estate-manifest.json b5fd6529f51cb592d909fd559431cad175dc1bdb
python3 sister_media.py estate public
get build/author_patch.py author_patch.py e23931704783e4d6cb30632349939080df7c93f3
python3 author_patch.py public
get build/sources_patch.py sources_patch.py f32120f9bf958c4a78a902967c8ceb279efe7e5d
get build/sources/estate.json sources.json 7b8e155e2b8654caeb218713f44afa03a78307be
python3 sources_patch.py public sources.json
get build/sitename_patch.py sitename_patch.py 417b5e08f0c149b4e1ec05b48cb6d1ca9e630966
python3 sitename_patch.py public blog
get build/a11y_patch.py a11y_patch.py 8e28d9077a486ba8426f24f0905072fb40181f7c
python3 a11y_patch.py public
get build/sister/sister_split.py sister_split.py 47758394f930613a90a9de512a070908299ff431
python3 sister_split.py estate blog
CT=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/de9bcd7aa3814aef9b768fcd6eea78ac39cef887/build
for i in 1 2 3 4; do if curl -fsSL "$CT/cta_patch.py" -o cta_patch.py && [ "$(sha1sum < cta_patch.py | cut -c1-40)" = "345aa2005ae86999b774de7dfc875c97acce663a" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: cta_patch.py"; exit 1; }; sleep $((2**i)); done
python3 cta_patch.py public estate
SC=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/0a4c3e96f84063ea9611df261c8fdade047ebabf
sget(){ for i in 1 2 3 4; do if curl -fsSL "$SC/$1" -o "$2" && [ "$(sha1sum < "$2" | cut -c1-40)" = "$3" ]; then return 0; fi; sleep $((2**i)); done; echo "build input fetch failed: $1"; exit 1; }
sget build/schema_patch.py schema_patch.py 4d4e747c18dd9bc351de8b7d65ffaedb58292514
python3 schema_patch.py public estate blog

N2=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/debb42f996ea7c34e4bb3b23a7391d55d21056bc/build
for i in 1 2 3 4; do if curl -fsSL "$N2/sitename2_patch.py" -o sitename2_patch.py && [ "$(sha1sum < sitename2_patch.py | cut -c1-40)" = "c85442c52955efbf4629cd74efeceace75adf642" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: sitename2_patch.py"; exit 1; }; sleep $((2**i)); done
python3 sitename2_patch.py public estate blog
