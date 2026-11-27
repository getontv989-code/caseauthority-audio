set -e
R=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/75b26058dc11ec9a41f342b6b176444ab6f376e2
get(){ for i in 1 2 3 4; do if curl -fsSL "$R/$1" -o "$2" && [ "$(sha1sum < "$2" | cut -c1-40)" = "$3" ]; then return 0; fi; sleep $((2**i)); done; echo "build input fetch failed: $1"; exit 1; }
get build/engine-2026-11-08.txz engine.txz fc7528cffa2cf2b8002ae1ed184ea67deeff3e61
python3 -c "import glob,tarfile;[tarfile.open(f).extractall() for f in sorted(glob.glob('*.txz'))]"
mkdir -p brands/divorce/posts media
get build/sister/divorce/outsource-seo-for-family-law-firms.json brands/divorce/posts/outsource-seo-for-family-law-firms.json 92a149b50456aa5be6f87ca18bbf78abfe6ba545
get build/sister/divorce/on-page-vs-off-page-seo-for-divorce-lawyers.json brands/divorce/posts/on-page-vs-off-page-seo-for-divorce-lawyers.json a580539e2bae986b6c389f547e2ab7e989d5011d
get build/sister/divorce/apple-maps-business-listing-for-divorce-lawyers.json brands/divorce/posts/apple-maps-business-listing-for-divorce-lawyers.json 75f0eab763f472e8a6205ed220bcfb9aabad74a6
get build/sister/divorce/google-business-profile-suspended.json brands/divorce/posts/google-business-profile-suspended.json b778e88791b9d92269afc587227b743ed3224bfd
get build/sister/divorce/get-found-online-first-seo-for-divorce-attorneys.json brands/divorce/posts/get-found-online-first-seo-for-divorce-attorneys.json ee021b7d36524a3cbc91aa1bcc18cfd6db82381a
get build/sister/divorce/is-seo-still-relevant.json brands/divorce/posts/is-seo-still-relevant.json 90b198611861d0e33550a89a003ece6de652223a
get build/sister/divorce/seo-contract.json brands/divorce/posts/seo-contract.json 536733133c665554e1aab4b0d37d167fc517ca3e
get build/sister/divorce/collaborative-law-training.json brands/divorce/posts/collaborative-law-training.json cd46387d4a222e15d2509c196d36ec330bcff693
get build/sister/divorce/divorce-month.json brands/divorce/posts/divorce-month.json 5fc3346a6723b3ac8579aa29bb078a3064139c7e
get build/sister/divorce/how-to-get-family-law-clients.json brands/divorce/posts/how-to-get-family-law-clients.json 96bb0142d557e20b59bdf6ebe427cbda1b3c7e3f
get build/sister/divorce/family-law-ppc.json brands/divorce/posts/family-law-ppc.json ea8bbadb4327184835fbed6318f15238d90a0b69
get build/sister/divorce/family-law-intake-form.json brands/divorce/posts/family-law-intake-form.json c820ee78b63f86803cc54bc796e277e3797c80d8
get build/sister/divorce/divorce-leads.json brands/divorce/posts/divorce-leads.json 6f4dcad5b066ed2b7ed0f2bd426e82c17b041658
get build/sister/divorce/divorce-attorney-advertising.json brands/divorce/posts/divorce-attorney-advertising.json 7c02660e416fa1ee178758bb19bf9ed3e7ff64f8
get build/sister/divorce/email-marketing-for-divorce-lawyers.json brands/divorce/posts/email-marketing-for-divorce-lawyers.json 08e40f9b5144e6fb7ec6625de69e2f87943b561d
mkdir -p engine/.cache
get build/sister/site-pinned.js engine/.cache/site.js 953b43503bed7ed465276d16778f4a526845f3d0
python3 engine/build.py brands/divorce public
python3 engine/verify.py brands/divorce public
get audio_patch.py audio_patch.py 5d554d6f70574bb34021f19927023b5348d9ce54
get explainer_patch.py explainer_patch.py dff467bf5cdd91bc095080fb536141fa25592c10
get build/sister/sister_media.py sister_media.py 96a7dab8176e4126313556515aeabefcc9407681
get build/sister/divorce-manifest.json media/divorce-manifest.json c7cdfcb67000e629b57cf390f6ab4390b94a32ae
python3 sister_media.py divorce public
get build/author_patch.py author_patch.py e23931704783e4d6cb30632349939080df7c93f3
python3 author_patch.py public
get build/sources_patch.py sources_patch.py f32120f9bf958c4a78a902967c8ceb279efe7e5d
get build/sources/divorce.json sources.json 191cbc3802c7de2c4abb1ddd571d70cfb4a97a68
python3 sources_patch.py public sources.json
N=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/dc5b17a6be5822e0c6c98f1b2c72d15e610830f7/build
for i in 1 2 3 4; do if curl -fsSL "$N/sitename_patch.py" -o sitename_patch.py && [ "$(sha1sum < sitename_patch.py | cut -c1-40)" = "417b5e08f0c149b4e1ec05b48cb6d1ca9e630966" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: sitename_patch.py"; exit 1; }; sleep $((2**i)); done
python3 sitename_patch.py public blog
get build/sister/sister_split.py sister_split.py 47758394f930613a90a9de512a070908299ff431
A=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/e25e6ba7197edf7e3ada2c10b638e65aa18c198a/build
for i in 1 2 3 4; do if curl -fsSL "$A/a11y_patch.py" -o a11y_patch.py && [ "$(sha1sum < a11y_patch.py | cut -c1-40)" = "8e28d9077a486ba8426f24f0905072fb40181f7c" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: a11y_patch.py"; exit 1; }; sleep $((2**i)); done
python3 a11y_patch.py public
python3 sister_split.py divorce blog
CT=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/de9bcd7aa3814aef9b768fcd6eea78ac39cef887/build
for i in 1 2 3 4; do if curl -fsSL "$CT/cta_patch.py" -o cta_patch.py && [ "$(sha1sum < cta_patch.py | cut -c1-40)" = "345aa2005ae86999b774de7dfc875c97acce663a" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: cta_patch.py"; exit 1; }; sleep $((2**i)); done
python3 cta_patch.py public divorce
SC=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/0a4c3e96f84063ea9611df261c8fdade047ebabf
sget(){ for i in 1 2 3 4; do if curl -fsSL "$SC/$1" -o "$2" && [ "$(sha1sum < "$2" | cut -c1-40)" = "$3" ]; then return 0; fi; sleep $((2**i)); done; echo "build input fetch failed: $1"; exit 1; }
sget build/schema_patch.py schema_patch.py 4d4e747c18dd9bc351de8b7d65ffaedb58292514
python3 schema_patch.py public divorce blog

N2=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/debb42f996ea7c34e4bb3b23a7391d55d21056bc/build
for i in 1 2 3 4; do if curl -fsSL "$N2/sitename2_patch.py" -o sitename2_patch.py && [ "$(sha1sum < sitename2_patch.py | cut -c1-40)" = "c85442c52955efbf4629cd74efeceace75adf642" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: sitename2_patch.py"; exit 1; }; sleep $((2**i)); done
python3 sitename2_patch.py public divorce blog
