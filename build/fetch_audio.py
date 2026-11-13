# Downloads the blog narration MP3s and the audio/explainer patches from the public repo
# getontv989-code/caseauthority-audio at the commit pinned in audio/manifest.json, checking every SHA1.
# Any failure exits 1, so the build fails and nothing goes live.
import hashlib, json, os, sys, time, urllib.request
man = json.load(open('audio/manifest.json'))
PATCHES = {'audio_patch.py': '5d554d6f70574bb34021f19927023b5348d9ce54', 'explainer_patch.py': '5b8026edae71c0e5655a19ff76ad8d8f4b5f10e6'}
any_a = next(iter(man.values()))
def get(name, sha1):
    url = 'https://raw.githubusercontent.com/%s/%s/%s' % (any_a['repo'], any_a['commit'], name)
    for i in range(4):
        try:
            data = urllib.request.urlopen(url, timeout=90).read()
            if hashlib.sha1(data).hexdigest() == sha1:
                return data
            err = 'checksum mismatch'
        except Exception as e:
            err = str(e)
        time.sleep(2 ** (i + 1))
    sys.exit('fetch_audio: %s: %s' % (url, err))
for n, s in PATCHES.items():
    open(n, 'wb').write(get(n, s))
os.makedirs('public/blog/audio', exist_ok=True)
for slug, a in man.items():
    open('public/blog/audio/%s.mp3' % slug, 'wb').write(get(slug + '.mp3', a['sha1']))
print('fetch_audio: %d patches, %d mp3' % (len(PATCHES), len(man)))
