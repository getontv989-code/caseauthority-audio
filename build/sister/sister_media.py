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
'criminal-defense-attorney-website-design': {
  'title': 'Criminal Defense Website Design in 60 Seconds',
  'sub': 'What a defense firm website needs in the hours after an arrest.',
  'bubble': 'Here is what the site must do.',
  'scenes': [
    {'kind': 'answer', 'h': 'Built for the Hours After an Arrest',
     'p': 'Worried families search on a phone, often at night, and call the clearest firm they find.',
     'v': {'kind': 'search', 'q': 'dui lawyer near me', 'results': [('Your Firm', True), ('County Defense Group', False), ('Main Street Law', False)]}},
    {'h': 'Make Calling Effortless', 'p': 'A visible number, click to call and a short, discreet form on every page.',
     'v': {'kind': 'phone', 'title': 'Call us now', 'rows': ['We answer 24/7', 'Free consultation', 'Do not share case details here']}},
    {'h': 'One Page per Charge', 'p': 'Separate pages for each key charge, tied to the courts you cover.',
     'v': {'kind': 'pages', 'pages': [('DUI Defense', 'Your county'), ('Drug Charges', 'Your county'), ('Assault', 'Your county'), ('DUI Defense', 'Nearby county')]}},
    {'h': 'Privacy Builds Trust', 'p': 'Ask only for a name and a safe way to reach them. No case details before you talk.',
     'v': {'kind': 'shield', 'chips': ['Short forms', 'Secure site', 'Discreet wording']}},
    {'h': 'Fast Pages Keep Visitors', 'p': 'Every extra second gives a stressed visitor a reason to leave.',
     'v': {'kind': 'race', 'fast': ('Page loads quickly', 'Consultation booked'), 'slow': ('Page loads slowly', 'Back to search results')}},
    {'h': 'Track Retained Clients', 'p': 'Count calls and forms from each page that become paying clients.',
     'v': {'kind': 'sources', 'title': 'Retained clients by page', 'items': [('DUI page', 80), ('Drug charges', 60), ('Assault', 45), ('Home page', 30)], 'tag': 'Illustrative example'}},
  ],
  'cta': CTA('Is Your Website Costing You Clients?', 'Get a free audit of your website, Google visibility and calls.'),
},
'google-business-profile-for-criminal-defense-lawyers': {
  'title': 'Google Business Profile for Defense Lawyers in 60 Seconds',
  'sub': 'How to show up in the map when someone has just been arrested.',
  'bubble': 'Here is how the map brings defense calls.',
  'scenes': [
    {'kind': 'answer', 'h': 'The Map Gets the First Calls',
     'p': 'Families search on their phone right after an arrest and call one of the first firms they see.',
     'v': {'kind': 'map', 'names': ['Your Firm', 'County Defense Group', 'Main Street Law']}},
    {'h': 'Real Name, Real Office', 'p': 'No keywords in your name and no virtual offices. Both can get a profile suspended.',
     'v': {'kind': 'shield', 'chips': ['Real firm name', 'Staffed office', 'One profile per office']}},
    {'h': 'Pick the Right Categories', 'p': 'Criminal justice attorney as the main category, plus only what you truly handle.',
     'v': {'kind': 'checklist', 'title': 'Profile basics', 'items': ['Main category', 'Honest hours', 'Services by charge', 'Real photos']}},
    {'h': 'Ask for Reviews Privately', 'p': 'Clients value discretion. They never need to mention their charge.',
     'v': {'kind': 'phone', 'title': 'A note from our office', 'rows': ['Your case is resolved', 'No need to mention your case', 'Share how we treated you']}},
    {'h': 'Never Confirm a Client', 'p': 'Reply to every review without names, charges, courts or outcomes.',
     'v': {'kind': 'compare', 'cols': ['General reply', 'Detailed reply'], 'rows': [('Protects the client', (True, False)), ('Follows confidentiality rules', (True, False)), ('Looks professional', (True, False))]}},
    {'h': 'Track Retained Clients', 'p': 'Count calls from your profile that become paying clients, by charge.',
     'v': {'kind': 'sources', 'title': 'Retained clients from the map', 'items': [('DUI', 80), ('Drug charges', 60), ('Assault', 45), ('Theft', 35)], 'tag': 'Illustrative example'}},
  ],
  'cta': CTA('Want More Calls From the Google Map?', 'Get a free audit of your Google Business Profile and local visibility.'),
},
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
'family-law-ppc': {
  'title': 'Family Law PPC in 60 Seconds',
  'sub': 'How to run Google Ads that bring retained clients, not wasted clicks.',
  'bubble': 'Here is how to set up family law ads.',
  'scenes': [
    {'kind': 'answer', 'h': 'Split Campaigns by Matter',
     'p': 'Separate campaigns for divorce, custody and support keep the budget under control.',
     'v': {'kind': 'split', 'title': 'Example budget split', 'parts': [('Divorce', 5, G), ('Custody', 3, K), ('Support', 2, S)], 'tag': 'Illustrative example'}},
    {'h': 'Block the Wrong Searches', 'p': 'Negative keywords stop ads showing for free forms and do it yourself divorce.',
     'v': {'kind': 'checklist', 'title': 'Negative keywords', 'items': ['free', 'forms and papers', 'do it yourself', 'jobs and paralegal']}},
    {'h': 'Stay in Your Counties', 'p': 'Show ads only where you take cases, to people who are actually there.',
     'v': {'kind': 'map', 'names': ['Your Firm', 'County Family Law', 'Main Street Law']}},
    {'h': 'Match the Page to the Search', 'p': 'A custody ad leads to a custody page, not the home page.',
     'v': {'kind': 'search', 'q': 'child custody lawyer near me', 'results': [('Your Firm', True), ('County Family Law', False), ('Divorce Forms Online', False)]}},
    {'h': 'Protect Privacy', 'p': 'Discreet ads, safe contact details and care with remarketing on shared devices.',
     'v': {'kind': 'shield', 'chips': ['Safe phone', 'Discreet ads', 'No remarketing']}},
    {'h': 'Measure Retainers', 'p': 'Track calls, consultations and signed retainers by campaign.',
     'v': {'kind': 'sources', 'title': 'From click to client', 'items': [('Clicks', 95), ('Calls and forms', 65), ('Consultations', 45), ('Retainers signed', 30)], 'tag': 'Illustrative example'}},
  ],
  'cta': CTA('Want Your Ads to Bring Retained Clients?', 'Get a free audit of your ads, website and Google visibility.'),
},
'family-law-intake-form': {
  'title': 'Family Law Intake Forms in 60 Seconds',
  'sub': 'Ask the right questions, keep people safe and win more consultations.',
  'bubble': 'Intake is where clients are won.',
  'scenes': [
    {'kind': 'answer', 'h': 'Intake Is Where Clients Are Won',
     'p': 'People often contact several firms. The first clear, kind reply usually books the consultation.',
     'v': {'kind': 'race', 'fast': ('Reply within the hour', 'Consultation booked'), 'slow': ('Reply next afternoon', 'Booked with another firm')}},
    {'h': 'Keep the First Form Short', 'p': 'Ask what you need for the consultation. Save detailed finances for later.',
     'v': {'kind': 'checklist', 'title': 'First intake form', 'items': ['Safe contact details', 'Other party for conflict check', 'Type of matter and children', 'Urgent issues and court dates']}},
    {'h': 'Check Conflicts First', 'p': 'Get the other party’s name before the person tells their story.',
     'v': {'kind': 'timeline', 'title': 'Order of intake', 'points': [('Names', 'Step 1', 20), ('Conflict check', 'Step 2', 45), ('Short story', 'Step 3', 70), ('Consultation', 'Step 4', 92)], 'tag': 'Typical order'}},
    {'h': 'Ask How to Reach Them Safely', 'p': 'A safe phone and email, and whether messages are okay to leave.',
     'v': {'kind': 'shield', 'chips': ['Safe phone', 'Safe email', 'Discreet messages']}},
    {'h': 'Follow Up With Care', 'p': 'Confirm the consultation, explain fees simply and check in with people still deciding.',
     'v': {'kind': 'phone', 'title': 'Your consultation is booked', 'rows': ['Date and time', 'What to bring', 'How our fees work']}},
    {'h': 'Measure Every Step', 'p': 'Form starts, completions, consultations and retainers, by source.',
     'v': {'kind': 'sources', 'title': 'Intake by step', 'items': [('Forms started', 90), ('Forms completed', 70), ('Consultations held', 50), ('Retainers signed', 35)], 'tag': 'Illustrative example'}},
  ],
  'cta': CTA('Want More Consultations to Become Clients?', 'Get a free audit of your website, forms and Google visibility.'),
},
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
'estate': {
'estate-planning-marketing-ideas': {
  'title': 'Estate Planning Marketing Ideas in 60 Seconds',
  'sub': 'How estate planning firms get found and chosen.',
  'bubble': 'Here is what works.',
  'scenes': [
    {'kind': 'answer', 'h': 'Be There When They Decide',
     'p': 'People put off planning for years, then search fast after a life event.',
     'v': {'kind': 'search', 'q': 'estate planning attorney near me', 'results': [('Your Firm', True), ('Legacy Law Group', False), ('Main Street Wills', False)]}},
    {'h': 'Win the Map', 'p': 'A complete Google profile and steady reviews put you in the top three.',
     'v': {'kind': 'map', 'names': ['Your Firm', 'Legacy Law Group', 'Main Street Wills']}},
    {'h': 'One Page per Service', 'p': 'Wills, trusts, probate and powers of attorney each get a clear page.',
     'v': {'kind': 'pages', 'pages': [('Wills', 'Your county'), ('Living Trusts', 'Your county'), ('Probate', 'Your county'), ('Powers of Attorney', 'Your county')]}},
    {'h': 'Ask for Honest Reviews', 'p': 'Ask right after signing, with a short link. Never pay for reviews.',
     'v': {'kind': 'stars', 'tag': 'Reviews from real clients', 'reviews': ['Made a hard topic simple.', 'Our trust was done in two weeks.']}},
    {'h': 'Build Adviser Referrals', 'p': 'Financial advisers and CPAs send clients who already trust you.',
     'v': {'kind': 'split', 'title': 'Example client mix', 'parts': [('Search and Maps', 5, G), ('Referrals', 3, S), ('Seminars', 2, K)], 'tag': 'Illustrative example'}},
    {'h': 'Answer Fast', 'p': 'The first firm to call back often books the consultation.',
     'v': {'kind': 'race', 'fast': ('Call back in minutes', 'Consultation booked'), 'slow': ('Call back next week', 'Hired another firm')}},
  ],
  'cta': CTA('Want to Know Which Ideas Fit Your Firm?', 'Get a free audit of your Google visibility and reviews.'),
},
},
}

SITES = {'criminal': 'https://seocriminaldefenselawyer.com', 'divorce': 'https://seodivorcelawyer.com', 'estate': 'https://seoestatelawyer.com'}


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
