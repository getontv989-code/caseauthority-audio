#!/usr/bin/env python3
"""Sister-site blog media: 'Listen to this article' narration + the 1-minute animated explainer.
Runs in a sister-site build after engine/build.py and verify.py:
  python3 sister_media.py <brand> <public_dir>
Needs audio_patch.py and explainer_patch.py (the same patches the PI blog uses) in the working dir, and
media/<brand>-manifest.json. Downloads each MP3 from the public caseauthority-audio repo at the pinned commit,
checks its SHA1, then patches every post. Any failure exits non-zero so nothing goes live half done.
"""
import hashlib, json, os, sys, time, urllib.request
# Explainer specs for the sister sites, keyed by brand then post slug. Same rules as the PI specs: Title Case, no em dashes.
G, K, S = '#CEAA32', '#0E0E0F', '#d9d2c3'
CTA = lambda h, p: {'h': h, 'p': p, 'btn': 'Get my free audit', 'href': '/sales'}
SISTER_SPECS = {
'criminal': {
'google-ads-for-criminal-defense-lawyers': {
  'title': 'Google Ads for Criminal Defense in 60 Seconds',
  'sub': 'How to set up search ads that bring retained clients, not wasted clicks.',
  'bubble': 'Here is how defense ads should be built.',
  'scenes': [
    {'kind': 'answer', 'h': 'Show Up for the Exact Charge',
     'p': 'People search right after an arrest. Your ad should name their charge and their county.',
     'v': {'kind': 'search', 'q': 'dui lawyer near me', 'results': [('Your Firm', True), ('County Defense Group', False), ('Main Street Law', False)]}},
    {'h': 'Split Campaigns by Charge', 'p': 'Separate campaigns for DUI, drug charges, assault and theft keep spending under control.',
     'v': {'kind': 'pages', 'pages': [('DUI Defense', 'Own budget'), ('Drug Charges', 'Own budget'), ('Assault', 'Own budget'), ('Theft', 'Own budget')]}},
    {'h': 'Block the Wrong Searches', 'p': 'Negative keywords stop ads showing for jobs, free help, inmate lookups and law school.',
     'v': {'kind': 'checklist', 'title': 'Common negative keywords', 'items': ['jobs and salary', 'free or pro bono', 'inmate search', 'law school']}},
    {'h': 'Match Ads to Your Phone Hours', 'p': 'Late-night ads only pay off if a real person answers late-night calls.',
     'v': {'kind': 'race', 'fast': ('Answered live at 2am', 'Client retained'), 'slow': ('Voicemail until morning', 'Hired another firm')}},
    {'h': 'Follow the Ad Rules', 'p': 'No promised outcomes, careful with past results, no specialist claims your state does not allow.',
     'v': {'kind': 'shield', 'chips': ['State bar rules', 'No guarantees', 'Google ad policies']}},
    {'h': 'Track Retained Clients', 'p': 'Count calls that become paying clients, by charge and by county, not clicks.',
     'v': {'kind': 'sources', 'title': 'Retained clients by campaign', 'items': [('DUI', 85), ('Drug charges', 65), ('Assault', 50), ('General', 30)], 'tag': 'Illustrative example'}},
  ],
  'cta': CTA('Want Your Google Ads to Bring Retained Clients?', 'Get a free audit of your Google visibility and ads.'),
},
'criminal-lawyer-advertising': {
  'title': 'Criminal Lawyer Advertising in 60 Seconds',
  'sub': 'Where defense firms spend, and what turns an ad into a client.',
  'bubble': 'Here is where defense ads pay off.',
  'scenes': [
    {'kind': 'answer', 'h': 'Be There Right After the Arrest',
     'p': 'People search soon after an arrest, often at night. Ads that show up then, and a phone that gets answered, win the case.',
     'v': {'kind': 'search', 'q': 'criminal lawyer near me', 'results': [('Your Firm', True), ('County Defense Group', False), ('Main Street Law', False)]}},
    {'h': 'Pick Channels by Job', 'p': 'Search ads and Local Services Ads catch people looking now. Radio and billboards help them remember your name.',
     'v': {'kind': 'compare', 'cols': ['Search ads', 'Billboards'], 'rows': [('Reach people searching now', (True, False)), ('Build name recognition', (False, True)), ('Easy to track', (True, False))]}},
    {'h': 'Name the Charge', 'p': 'Ads for a specific charge, sent to a matching page, beat a general criminal lawyer message.',
     'v': {'kind': 'pages', 'pages': [('DUI Defense', 'Your county'), ('Drug Charges', 'Your county'), ('Assault', 'Your county'), ('Expungement', 'Your county')]}},
    {'h': 'Plan for Busy Seasons', 'p': 'Arrests and searches often rise around holidays and summer. Raise budgets and cover the phones before they start.',
     'v': {'kind': 'timeline', 'title': 'Common busy periods', 'points': [('Summer', 'July 4', 20), ('Labor Day', 'September', 45), ('Holidays', 'Nov to Dec', 72), ('New Year', 'January', 92)], 'tag': 'Varies by market'}},
    {'h': 'Answer Every Call', 'p': 'People call several firms. The first kind, clear answer usually gets hired.',
     'v': {'kind': 'race', 'fast': ('Answered live at 11pm', 'Client hired'), 'slow': ('Voicemail until morning', 'Hired another firm')}},
    {'h': 'Follow the Ad Rules', 'p': 'No guarantees, careful with past results, and never identify a client without consent.',
     'v': {'kind': 'shield', 'chips': ['State bar rules', 'No guarantees', 'Client privacy']}},
  ],
  'cta': CTA('Want More Calls From People Who Need a Defense Lawyer?', 'Get a free audit of your Google visibility and ads.'),
},
'dui-lawyer-seo': {
  'title': 'DUI Lawyer SEO in 60 Seconds',
  'sub': 'How DUI and DWI attorneys get found when people search after an arrest.',
  'bubble': 'Here is how DUI clients find you.',
  'scenes': [
    {'kind': 'answer', 'h': 'Be Found Fast, Answer Fast',
     'p': 'People search soon after an arrest, often at night. Firms that show up first and answer the phone get most DUI calls.',
     'v': {'kind': 'search', 'q': 'DUI lawyer near me', 'results': [('Your Firm', True), ('County Defense Group', False), ('Main Street Law', False)]}},
    {'h': 'The Map Comes First', 'p': 'Many DUI searches show map results at the top. A complete Google Business Profile is a big part of DUI SEO.',
     'v': {'kind': 'map', 'names': ['Your Firm', 'County Defense Group', 'Main Street Law']}},
    {'h': 'One Page per DUI Case Type', 'p': 'First offense, license suspension, refusal and felony DUI each deserve their own clear page.',
     'v': {'kind': 'pages', 'pages': [('First DUI', 'Your county'), ('License Hearing', 'Your county'), ('Breath Test Refusal', 'Your county'), ('Felony DUI', 'Your county')]}},
    {'h': 'Use Your State\'s Words', 'p': 'If your state says DWI or OWI, your pages should lead with that word.',
     'v': {'kind': 'checklist', 'title': 'Match local wording', 'items': ['DUI, DWI, OWI or OUI', 'Local license hearing name', 'Real court names', 'Counties you cover']}},
    {'h': 'Reviews Build Trust', 'p': 'Ask kindly, never pressure, and keep replies general to protect client privacy.',
     'v': {'kind': 'stars', 'tag': 'Genuine reviews', 'reviews': ['Calm, clear and quick to answer.', 'Explained every step.']}},
    {'h': 'Track Signed Clients', 'p': 'Rankings help, but the real measure is DUI calls and the clients who hire you.',
     'v': {'kind': 'compare', 'cols': ['Rankings', 'Clients'], 'rows': [('Brings in calls', (False, True)), ('Ties to fees', (False, True)), ('Shows what to fix', (False, True))]}},
  ],
  'cta': CTA('Want to See Where Your Firm Shows Up for DUI Searches?', 'Get a free audit of your Google Maps and search visibility.'),
},
'seo-keywords-for-criminal-defense-lawyers': {
  'title': 'Criminal Defense Keywords in 60 Seconds',
  'sub': 'Which searches bring criminal defense clients, and what to do with them.',
  'bubble': 'Some searches bring clients. Some do not.',
  'scenes': [
    {'kind': 'answer', 'h': 'Charge Plus Place Brings Clients',
     'p': 'Searches that name a charge and a city, like DUI lawyer in Houston, usually come from people who need a lawyer now.',
     'v': {'kind': 'search', 'q': 'drug possession lawyer houston', 'results': [('Your Firm', True), ('Harris Defense Law', False), ('Bayou Criminal Attorneys', False)]}},
    {'h': 'Near Me Means Maps', 'p': 'Near me searches are won mostly through your Google Business Profile and reviews.',
     'v': {'kind': 'map', 'names': ['Your Firm', 'Harris Defense Law', 'Bayou Criminal Attorneys']}},
    {'h': 'One Page per Charge', 'p': 'Give each charge you defend its own clear page so Google knows what you handle.',
     'v': {'kind': 'pages', 'pages': [('DUI Defense', 'Your city'), ('Drug Charges', 'Your city'), ('Assault', 'Your city'), ('Theft', 'Your city')]}},
    {'h': 'Use Their Words', 'p': 'Write the way people search, not in legal jargon.',
     'v': {'kind': 'checklist', 'title': 'Words people use', 'items': ['Criminal lawyer near me', 'DWI attorney', 'Got arrested what now', 'Bail hearing lawyer']}},
    {'h': 'Skip Searches That Never Hire', 'p': 'Students and the curious search too. Focus on searches from people who need help.',
     'v': {'kind': 'compare', 'cols': ['Curious', 'Hiring'], 'rows': [('Needs help now', (False, True)), ('Names a charge', (False, True)), ('Names a place', (False, True))]}},
  ],
  'cta': CTA('Want to Know Which Searches Bring Your Firm Clients?', 'Get a free audit of your rankings and Google Business Profile.'),
},
},
'divorce': {
'email-marketing-for-divorce-lawyers': {
  'title': 'Email Marketing for Divorce Lawyers in 60 Seconds',
  'sub': 'Stay helpful while people decide, without putting anyone at risk.',
  'bubble': 'Divorce decisions take time. Email helps.',
  'scenes': [
    {'kind': 'answer', 'h': 'Divorce Decisions Take Time',
     'p': 'Many people research for months. Helpful emails keep your firm remembered until they are ready.',
     'v': {'kind': 'timeline', 'title': 'A typical path to hiring', 'points': [('Search', 'Week 1', 15), ('Guide download', 'Week 3', 40), ('Consultation', 'Month 2', 68), ('Retainer', 'Month 4', 92)], 'tag': 'Varies by person'}},
    {'h': 'Only Email People Who Asked', 'p': 'Consultation requests, guide downloads, past clients and referral partners. Never bought lists.',
     'v': {'kind': 'checklist', 'title': 'Who belongs on your list', 'items': ['Consultation requests', 'Guide downloads', 'Past clients who opted in', 'Referral partners']}},
    {'h': 'Keep Every Email Safe', 'p': 'Ask for a safe address, use discreet subject lines and keep case details out of marketing emails.',
     'v': {'kind': 'shield', 'chips': ['Safe address', 'Discreet subject', 'No case details']}},
    {'h': 'Follow Up After Consultations', 'p': 'A short, kind sequence brings back people who went quiet while they decided.',
     'v': {'kind': 'phone', 'title': 'Your checklist from our office', 'rows': ['Documents to gather', 'How custody usually works', 'Book a time when ready']}},
    {'h': 'Stay Close to Referrers', 'p': 'Therapists, financial planners and other lawyers refer to firms they remember.',
     'v': {'kind': 'compare', 'cols': ['Newsletter', 'No contact'], 'rows': [('Remembered by referrers', (True, False)), ('Past clients come back', (True, False)), ('Builds trust over time', (True, False))]}},
    {'h': 'Measure Consultations', 'p': 'Track booked consultations and retainers from email, not open rates.',
     'v': {'kind': 'sources', 'title': 'Consultations by list', 'items': [('Consultation follow-up', 85), ('Guide downloads', 60), ('Past clients', 45), ('Referral partners', 40)], 'tag': 'Illustrative example'}},
  ],
  'cta': CTA('Want More Consultations From People Already Researching You?', 'Get a free audit of your Google visibility and website.'),
},
'divorce-attorney-advertising': {
  'title': 'Divorce Attorney Advertising in 60 Seconds',
  'sub': 'Channels, timing and the tone that builds trust.',
  'bubble': 'Divorce clients research first. Here is how to reach them.',
  'scenes': [
    {'kind': 'answer', 'h': 'People Research Before They Call',
     'p': 'Divorce is a considered decision. The best ads catch people ready to hire and build trust with those still deciding.',
     'v': {'kind': 'search', 'q': 'divorce lawyer near me', 'results': [('Your Firm', True), ('Family Law Partners', False), ('Smith and Lee Law', False)]}},
    {'h': 'Match the Channel to the Job', 'p': 'Search ads and Local Services Ads reach people ready to hire. Social media and video build familiarity over time.',
     'v': {'kind': 'compare', 'cols': ['Search ads', 'Social ads'], 'rows': [('Ready to hire now', (True, False)), ('Builds trust over time', (False, True)), ('Easy to track', (True, False))]}},
    {'h': 'Plan for January', 'p': 'Many people wait until after the holidays. Prepare budgets, ads and staff before the new year.',
     'v': {'kind': 'timeline', 'title': 'When interest often rises', 'points': [('November', 'Helpful content', 15), ('December', 'Stay visible', 40), ('January', 'Busiest month', 68), ('August', 'Before school', 92)], 'tag': 'Varies by market'}},
    {'h': 'Calm Ads Connect Best', 'p': 'Name the help you offer, where you offer it and a private first step. Skip promises and fear.',
     'v': {'kind': 'checklist', 'title': 'A good divorce ad', 'items': ['Names the case type', 'Names your area', 'Private first step', 'Real attorney, not stock']}},
    {'h': 'Respect Privacy in Follow Up', 'p': 'Ask when and how it is safe to contact someone, and stick to it.',
     'v': {'kind': 'phone', 'title': 'New divorce inquiry', 'rows': ['Best time to call?', 'Okay to text?', 'Consultation booked']}},
    {'h': 'Follow the Ad Rules', 'p': 'Each state has its own rules on lawyer ads, testimonials and client privacy.',
     'v': {'kind': 'shield', 'chips': ['State bar rules', 'No guarantees', 'Protect children\'s privacy']}},
  ],
  'cta': CTA('Want More Retained Clients From Your Ads?', 'Get a free audit of your Google visibility and ads.'),
},
'divorce-leads': {
  'title': 'Divorce Leads in 60 Seconds',
  'sub': 'Where family law leads come from, and what turns them into clients.',
  'bubble': 'Leads are not clients. Here is why.',
  'scenes': [
    {'kind': 'answer', 'h': 'Judge Leads by Retained Clients',
     'p': 'You can buy leads, pay for ads, or earn leads in Google and through referrals. What matters is who retains you.',
     'v': {'kind': 'phone', 'title': 'New divorce inquiry', 'rows': ['Both spouses\' names', 'Conflict check first', 'Consultation booked']}},
    {'h': 'Bought Leads Are Often Shared', 'p': 'A lead sold to several firms rewards speed over care. Exclusive leads give you room to help.',
     'v': {'kind': 'compare', 'cols': ['Bought', 'Earned'], 'rows': [('Starts quickly', (True, False)), ('Only your firm', (False, True)), ('Keeps working', (False, True))]}},
    {'h': 'Earned Leads Arrive With Trust', 'p': 'People who find you in Google or through a referral often arrive ready to listen.',
     'v': {'kind': 'search', 'q': 'divorce lawyer near me', 'results': [('Your Firm', True), ('Family Law Partners', False), ('Westside Divorce Law', False)]}},
    {'h': 'Check Conflicts First', 'p': 'The other spouse may call too. Collect key names and run a conflict check before hearing the details.',
     'v': {'kind': 'checklist', 'title': 'First minutes of the call', 'items': ['Both spouses\' names', 'Run a conflict check', 'Safety concerns?', 'Explain next steps']}},
    {'h': 'A Calm First Call Wins', 'p': 'People going through a divorce are stressed. A prompt, kind response signs more clients.',
     'v': {'kind': 'race', 'fast': ('Kind reply within minutes', 'Consultation booked'), 'slow': ('Reply two days later', 'Hired another firm')}},
    {'h': 'Know Your Bar Rules', 'p': 'Paying for leads is regulated, and rules vary by state.',
     'v': {'kind': 'shield', 'chips': ['State bar rules', 'No paid recommendations', 'Honest lead services']}},
  ],
  'cta': CTA('Want More Divorce Leads That Come Only to You?', 'Get a free audit of where your firm stands in Google and Maps.'),
},
'family-law-marketing-ideas': {
  'title': 'Family Law Marketing Ideas in 60 Seconds',
  'sub': 'Simple ideas a family law firm can start this week.',
  'bubble': 'Here is where to start.',
  'scenes': [
    {'kind': 'answer', 'h': 'Start With the Basics',
     'p': 'A complete Google Business Profile, steady reviews and clear pages for each type of case usually come first.',
     'v': {'kind': 'map', 'names': ['Your Firm', 'Family Law Partners', 'Westside Divorce Law']}},
    {'h': 'Ask for Reviews Kindly', 'p': 'People choosing a family lawyer read reviews closely. A simple, polite request works best.',
     'v': {'kind': 'stars', 'tag': 'Genuine reviews', 'reviews': ['Kind and honest from day one.', 'Always answered my questions.']}},
    {'h': 'One Page per Type of Case', 'p': 'Divorce, custody, support and protective orders each deserve their own clear page.',
     'v': {'kind': 'pages', 'pages': [('Divorce', 'Your county'), ('Child Custody', 'Your county'), ('Child Support', 'Your county'), ('Protective Orders', 'Your county')]}},
    {'h': 'Build Referral Partners', 'p': 'Therapists, financial advisers and other attorneys can send warm, trusting clients.',
     'v': {'kind': 'split', 'title': 'Example lead mix', 'parts': [('Search and Maps', 5, G), ('Referrals', 3, S), ('Ads', 2, K)], 'tag': 'Illustrative example'}},
    {'h': 'Answer Fast and Kindly', 'p': 'A prompt, calm reply turns more inquiries into consultations.',
     'v': {'kind': 'race', 'fast': ('Reply within minutes', 'Consultation booked'), 'slow': ('Reply next week', 'Hired another firm')}},
  ],
  'cta': CTA('Want to Know Which Ideas Will Help Your Firm Most?', 'Get a free audit of your Google visibility and reviews.'),
},
},
}

SITES = {'criminal': 'https://seocriminaldefenselawyer.com', 'divorce': 'https://seodivorcelawyer.com'}


def fetch(url, sha1):
    err = ''
    for i in range(4):
        try:
            data = urllib.request.urlopen(url, timeout=90).read()
            if hashlib.sha1(data).hexdigest() == sha1:
                return data
            err = 'checksum mismatch'
        except Exception as e:
            err = str(e)
        time.sleep(2 ** (i + 1))
    sys.exit('sister_media: %s: %s' % (url, err))


def main(brand, pub='public'):
    man = json.load(open('media/%s-manifest.json' % brand))
    specs = SISTER_SPECS[brand]
    # audio files
    os.makedirs(os.path.join(pub, 'blog', 'audio'), exist_ok=True)
    for slug, a in man.items():
        url = 'https://raw.githubusercontent.com/%s/%s/%s' % (a['repo'], a['commit'], a['path'])
        open(os.path.join(pub, 'blog', 'audio', slug + '.mp3'), 'wb').write(fetch(url, a['sha1']))
    # player + AudioObject (same code as the PI blog, with this site's domain)
    ap = {'__name__': 'audio_patch'}
    exec(open('audio_patch.py').read(), ap)
    ap['SITE'] = SITES[brand]
    ap['main'](pub, 'media/%s-manifest.json' % brand)
    # explainers (same renderer as the PI blog, with this site's specs)
    xp = {'__name__': 'explainer_patch'}
    exec(open('explainer_patch.py').read(), xp)
    xp['SPECS'].clear()
    xp['SPECS'].update(specs)
    sys.argv = ['explainer_patch.py', pub]
    xp['main']()
    # checks
    for slug in sorted(set(man) | set(specs)):
        h = open(os.path.join(pub, 'blog', slug + '.html'), encoding='utf-8').read()
        if slug in man and (h.count('class="listen"') != 1 or '"AudioObject"' not in h or SITES[brand] + '/blog/audio/' not in h):
            sys.exit('sister_media: audio check failed for ' + slug)
        if slug in specs and h.count('class="xp"') != 1:
            sys.exit('sister_media: explainer check failed for ' + slug)
    posts = [f[:-5] for f in os.listdir(os.path.join(pub, 'blog')) if f.endswith('.html') and f != 'index.html']
    missing = [p for p in posts if p not in man or p not in specs]
    if missing:
        sys.exit('sister_media: posts without audio or explainer: ' + ', '.join(missing))
    print('sister_media: %s, %d audio, %d explainers' % (brand, len(man), len(specs)))


if __name__ == '__main__':
    main(*sys.argv[1:])
