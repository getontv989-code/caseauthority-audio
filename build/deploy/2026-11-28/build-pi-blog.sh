set -e
B=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/177bcf9dedce746e733125daafcfefd89d301dc2/build
get(){ for i in 1 2 3 4; do if curl -fsSL "$B/$1" -o "$2" && [ "$(sha1sum < "$2" | cut -c1-40)" = "$3" ]; then return 0; fi; sleep $((2**i)); done; echo "build input fetch failed: $1"; exit 1; }
mkdir -p src audio
get posts__z21-multi-location-seo-for-personal-injury-law-firms.py src/posts__z21-multi-location-seo-for-personal-injury-law-firms.py.part00 13f077c6eeca23fd039c4c85cab562f43ce1d060
get posts__z20-seo-kpis-for-personal-injury-law-firms.py src/posts__z20-seo-kpis-for-personal-injury-law-firms.py.part00 9528c39de36b3c091bc30f1e0bf90bc316608ed7
get posts__z19-how-to-get-a-knowledge-panel-on-google.py src/posts__z19-how-to-get-a-knowledge-panel-on-google.py.part00 c77da398c346e6dc694dba75c6846477c4f981c2
get posts__z18-why-is-my-law-firm-website-not-ranking-on-google.py src/posts__z18-why-is-my-law-firm-website-not-ranking-on-google.py.part00 7014cfc5c5b27b67f68aeaf2b77c999e0e7c4587
get posts__z17-get-found-online-first-seo-for-personal-injury-lawyers.py src/posts__z17-get-found-online-first-seo-for-personal-injury-lawyers.py.part00 c5abc76c1d03947ef9b0fa55e69bab3ae72dc9af
get posts__z16-how-to-rank-in-chatgpt.py src/posts__z16-how-to-rank-in-chatgpt.py.part00 1f6f1d01b3eee10c03ac5fb3072addea2210754a
get posts__z15-seo-guarantee.py src/posts__z15-seo-guarantee.py.part00 17329b43b9834af6826563201ea835ebfda0a3bb
get posts__z14-million-dollar-advocates-forum.py src/posts__z14-million-dollar-advocates-forum.py.part00 04132c8989e87241022c2b7e3382938ab4ec6fe1
get posts__z13-is-super-lawyers-legit.py src/posts__z13-is-super-lawyers-legit.py.part00 3236d6a9029abbf22426d252ef6fcbb0ddf31dd6
get posts__z06-website-design-for-personal-injury-lawyers.py src/posts__z06-website-design-for-personal-injury-lawyers.py.part00 07343f11210295f506115c9b53b62fb931f8a67d
get posts__z07-personal-injury-lead-generation.py src/posts__z07-personal-injury-lead-generation.py.part00 598aca2b349418b363544ba90ad3ef23103075fc
get posts__z08-mass-tort-marketing.py src/posts__z08-mass-tort-marketing.py.part00 31f798eb26876f0fa21dd32db116b244eb71d123
get posts__z09-personal-injury-lawyer-advertising.py src/posts__z09-personal-injury-lawyer-advertising.py.part00 529d727db211b3f075c263bfe3a74e4e7ccdc324
get posts__z10-reputation-management-for-attorneys.py src/posts__z10-reputation-management-for-attorneys.py.part00 56f8191667e21ac2c5638e3ee57cdc9662cda815
get posts__z11-law-firm-marketing-trends.py src/posts__z11-law-firm-marketing-trends.py.part00 6c0d0a60223ffa52f46688157749d92e7a9a653e
get posts__z12-how-long-does-seo-take-for-law-firms.py src/posts__z12-how-long-does-seo-take-for-law-firms.py.part00 c045ed9d6fe24efb67ef8e55656a543cc8ee6218
get manifest.json audio/manifest.json 39da8e4723d27e719ead659e977e9210aa79c1ce
get fetch_audio.py fetch_audio.py 4c454ffa2e07572a120190be448e4994814a15e9
get linkedin_patch.py linkedin_patch.py 8536422960a92063341d267fc1077985f9a8e64a
get author_patch.py author_patch.py e23931704783e4d6cb30632349939080df7c93f3
for p in src/*.part00; do b=${p%.part00}; t=$(basename "$b" | sed "s#__#/#g"); mkdir -p "$(dirname "$t")"; cat "$b".part* > "$t"; done
python3 seo_patch.py
python3 speed_patch.py
python3 agent_patch.py
python3 hdr_patch.py
printf '\n' >> blog_pages.py
cat roi_post.py >> blog_pages.py
for f in posts/*.py; do if [ -f "$f" ]; then printf '\n' >> blog_pages.py; cat "$f" >> blog_pages.py; fi; done
python3 site_patch.py
python3 fetch_assets.py
python3 build.py
grep -rIlE "5859402698|940-2698" public | xargs -r sed -i -e "s/(585) 940-2698/(838) 205-8892/g" -e "s/+1-585-940-2698/+1-838-205-8892/g" -e "s/+15859402698/+18382058892/g"
if grep -rIqE "585.{0,3}940.{0,3}2698" public; then echo "old phone number still present"; grep -rIoE ".{20}585.{0,3}940.{0,3}2698" public | head; exit 1; fi
python3 tags_patch.py
python3 og_patch.py
python3 cache_patch.py
python3 fetch_audio.py
python3 audio_patch.py public audio/manifest.json
python3 explainer_patch.py public
python3 linkedin_patch.py public
python3 author_patch.py public
get sources_patch.py sources_patch.py f32120f9bf958c4a78a902967c8ceb279efe7e5d
get sources/pi.json sources.json cdf3feee56add5f296b7abc48f0388cdb24dd736
python3 sources_patch.py public sources.json
A=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/e25e6ba7197edf7e3ada2c10b638e65aa18c198a/build
for i in 1 2 3 4; do if curl -fsSL "$A/a11y_patch.py" -o a11y_patch.py && [ "$(sha1sum < a11y_patch.py | cut -c1-40)" = "8e28d9077a486ba8426f24f0905072fb40181f7c" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: a11y_patch.py"; exit 1; }; sleep $((2**i)); done
python3 a11y_patch.py public
N=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/dc5b17a6be5822e0c6c98f1b2c72d15e610830f7/build
for i in 1 2 3 4; do if curl -fsSL "$N/sitename_patch.py" -o sitename_patch.py && [ "$(sha1sum < sitename_patch.py | cut -c1-40)" = "417b5e08f0c149b4e1ec05b48cb6d1ca9e630966" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: sitename_patch.py"; exit 1; }; sleep $((2**i)); done
python3 sitename_patch.py public blog
python3 split.py blog
python3 verify.py blog
GP=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/ff4ed5dc42ec4e3d0b945f86e88e2d6600681732/build
for i in 1 2 3 4; do if curl -fsSL "$GP/guide_patch.py" -o guide_patch.py && [ "$(sha1sum < guide_patch.py | cut -c1-40)" = "7f70b5ff5a4128532c6c9d2f8f4fe555332e1cbc" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: guide_patch.py"; exit 1; }; sleep $((2**i)); done
python3 guide_patch.py public blog
CT=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/de9bcd7aa3814aef9b768fcd6eea78ac39cef887/build
for i in 1 2 3 4; do if curl -fsSL "$CT/cta_patch.py" -o cta_patch.py && [ "$(sha1sum < cta_patch.py | cut -c1-40)" = "345aa2005ae86999b774de7dfc875c97acce663a" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: cta_patch.py"; exit 1; }; sleep $((2**i)); done
python3 cta_patch.py public pi
python3 positioning_patch.py public
HS=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/91085d0e1c03bb5b5107f260d19880ed0e2faa74/build
for i in 1 2 3 4; do if curl -fsSL "$HS/homeseo_patch.py" -o homeseo_patch.py && [ "$(sha1sum < homeseo_patch.py | cut -c1-40)" = "b5c5c85aa97c24ee68d732a90c4287c16d4a7989" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: homeseo_patch.py"; exit 1; }; sleep $((2**i)); done
python3 homeseo_patch.py public blog
SC=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/0a4c3e96f84063ea9611df261c8fdade047ebabf
sget(){ for i in 1 2 3 4; do if curl -fsSL "$SC/$1" -o "$2" && [ "$(sha1sum < "$2" | cut -c1-40)" = "$3" ]; then return 0; fi; sleep $((2**i)); done; echo "build input fetch failed: $1"; exit 1; }
sget build/schema_patch.py schema_patch.py 4d4e747c18dd9bc351de8b7d65ffaedb58292514
python3 schema_patch.py public pi blog

N2=https://raw.githubusercontent.com/getontv989-code/caseauthority-audio/debb42f996ea7c34e4bb3b23a7391d55d21056bc/build
for i in 1 2 3 4; do if curl -fsSL "$N2/sitename2_patch.py" -o sitename2_patch.py && [ "$(sha1sum < sitename2_patch.py | cut -c1-40)" = "c85442c52955efbf4629cd74efeceace75adf642" ]; then break; fi; [ $i = 4 ] && { echo "build input fetch failed: sitename2_patch.py"; exit 1; }; sleep $((2**i)); done
python3 sitename2_patch.py public pi blog
