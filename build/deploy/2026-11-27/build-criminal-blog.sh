set -e
R=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/177bcf9dedce746e733125daafcfefd89d301dc2
get(){ for i in 1 2 3 4; do if curl -fsSL "$R/$1" -o "$2" && [ "$(sha1sum < "$2" | cut -c1-40)" = "$3" ]; then return 0; fi; sleep $((2**i)); done; echo "build input fetch failed: $1"; exit 1; }
get build/engine-2026-11-08.txz engine.txz fc7528cffa2cf2b8002ae1ed184ea67deeff3e61
python3 -c "import glob,tarfile;[tarfile.open(f).extractall() for f in sorted(glob.glob('*.txz'))]"
mkdir -p brands/criminal/posts media
get build/sister/criminal/what-access-to-give-your-seo-agency.json brands/criminal/posts/what-access-to-give-your-seo-agency.json 81f200c15616f36cf90d492cfeed30cccfe80816
get build/sister/criminal/what-does-an-seo-agency-do-for-criminal-defense-lawyers.json brands/criminal/posts/what-does-an-seo-agency-do-for-criminal-defense-lawyers.json a7fe873448d61b0190dd9b942f1ecbef0038e500
get build/sister/criminal/bing-seo-for-criminal-defense-lawyers.json brands/criminal/posts/bing-seo-for-criminal-defense-lawyers.json d451cccbd059987428bdd7b2352754acd1902628
get build/sister/criminal/how-to-read-a-monthly-seo-report.json brands/criminal/posts/how-to-read-a-monthly-seo-report.json 5002aa713ea773f0f1a9de83afe49e0b7d5f7a09
get build/sister/criminal/get-found-online-first-seo-for-criminal-defense-attorneys.json brands/criminal/posts/get-found-online-first-seo-for-criminal-defense-attorneys.json c2c17a8c4ce35953d5addbbcb867007486da4b4b
get build/sister/criminal/how-to-rank-in-ai-overviews.json brands/criminal/posts/how-to-rank-in-ai-overviews.json 19a2a54c7b63333f1a36059ed99e0ba31e60b931
get build/sister/criminal/questions-to-ask-when-hiring-an-seo-company.json brands/criminal/posts/questions-to-ask-when-hiring-an-seo-company.json b27dea30d19d1d2123499a9b7c401456f6c47f5f
get build/sister/criminal/google-screened.json brands/criminal/posts/google-screened.json 37a50319fb92b282061eed2acfbfe0c69e492815
get build/sister/criminal/how-to-improve-avvo-rating.json brands/criminal/posts/how-to-improve-avvo-rating.json a223b0e9c5d9f5c6db794de486cf9589b71b12e8
get build/sister/criminal/how-to-get-criminal-defense-clients.json brands/criminal/posts/how-to-get-criminal-defense-clients.json f428e1a5d6d8365b2faaf44352194f2b6af91924
get build/sister/criminal/criminal-defense-attorney-website-design.json brands/criminal/posts/criminal-defense-attorney-website-design.json 571bc9245dc59ce07169a292ceba873e3ee9ec7f
get build/sister/criminal/google-business-profile-for-criminal-defense-lawyers.json brands/criminal/posts/google-business-profile-for-criminal-defense-lawyers.json 9a5145bcee693fc5a3532c2a9b518036e3936b33
get build/sister/criminal/dui-lawyer-seo.json brands/criminal/posts/dui-lawyer-seo.json bd4297604ad0c41fface364a645a4a12885aad87
get build/sister/criminal/criminal-lawyer-advertising.json brands/criminal/posts/criminal-lawyer-advertising.json 867419615fae8562411c0602ed12fe5f143070d2
get build/sister/criminal/google-ads-for-criminal-defense-lawyers.json brands/criminal/posts/google-ads-for-criminal-defense-lawyers.json c8568d423b98f61cf45d5a75b11f875fe08ee1ee
mkdir -p engine/.cache
get build/sister/site-pinned.js engine/.cache/site.js 953b43503bed7ed465276d16778f4a526845f3d0
python3 engine/build.py brands/criminal public
python3 engine/verify.py brands/criminal public
get audio_patch.py audio_patch.py 5d554d6f70574bb34021f19927023b5348d9ce54
get explainer_patch.py explainer_patch.py dff467bf5cdd91bc095080fb536141fa25592c10
get build/sister/sister_media.py sister_media.py 96a7dab8176e4126313556515aeabefcc9407681
get build/sister/criminal-manifest.json media/criminal-manifest.json b2956ba894ae34f9b31cb46c89610efc6744a9f2
python3 sister_media.py criminal public
get build/author_patch.py author_patch.py e23931704783e4d6cb30632349939080df7c93f3
python3 author_patch.py public
get build/sources_patch.py sources_patch.py f32120f9bf958c4a78a902967c8ceb279efe7e5d
get build/sources/criminal.json sources.json ca7faf07f85c98cc5c32bbf80acd5e6cc447f084
python3 sources_patch.py public sources.json
N=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/dc5b17a6be5822e0c6c98f1b2c72d15e610830f7/build
for i in 1 2 3 4; do if curl -fsSL "$N/sitename_patch.py" -o sitename_patch.py && [ "$(sha1sum < sitename_patch.py | cut -c1-40)" = "417b5e08f0c149b4e1ec05b48cb6d1ca9e630966" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: sitename_patch.py"; exit 1; }; sleep $((2**i)); done
python3 sitename_patch.py public blog
get build/sister/sister_split.py sister_split.py 47758394f930613a90a9de512a070908299ff431
A=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/e25e6ba7197edf7e3ada2c10b638e65aa18c198a/build
for i in 1 2 3 4; do if curl -fsSL "$A/a11y_patch.py" -o a11y_patch.py && [ "$(sha1sum < a11y_patch.py | cut -c1-40)" = "8e28d9077a486ba8426f24f0905072fb40181f7c" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: a11y_patch.py"; exit 1; }; sleep $((2**i)); done
python3 a11y_patch.py public
python3 sister_split.py criminal blog
CT=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/de9bcd7aa3814aef9b768fcd6eea78ac39cef887/build
for i in 1 2 3 4; do if curl -fsSL "$CT/cta_patch.py" -o cta_patch.py && [ "$(sha1sum < cta_patch.py | cut -c1-40)" = "345aa2005ae86999b774de7dfc875c97acce663a" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: cta_patch.py"; exit 1; }; sleep $((2**i)); done
python3 cta_patch.py public criminal
SC=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/0a4c3e96f84063ea9611df261c8fdade047ebabf
sget(){ for i in 1 2 3 4; do if curl -fsSL "$SC/$1" -o "$2" && [ "$(sha1sum < "$2" | cut -c1-40)" = "$3" ]; then return 0; fi; sleep $((2**i)); done; echo "build input fetch failed: $1"; exit 1; }
sget build/schema_patch.py schema_patch.py 4d4e747c18dd9bc351de8b7d65ffaedb58292514
python3 schema_patch.py public criminal blog

N2=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/debb42f996ea7c34e4bb3b23a7391d55d21056bc/build
for i in 1 2 3 4; do if curl -fsSL "$N2/sitename2_patch.py" -o sitename2_patch.py && [ "$(sha1sum < sitename2_patch.py | cut -c1-40)" = "c85442c52955efbf4629cd74efeceace75adf642" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: sitename2_patch.py"; exit 1; }; sleep $((2**i)); done
python3 sitename2_patch.py public criminal blog
