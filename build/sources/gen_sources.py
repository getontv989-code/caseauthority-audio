#!/usr/bin/env python3
"""Builds pi.json, criminal.json, divorce.json for sources_patch.py.
Every URL here was opened and checked against the claim it backs on 2026-11-10.
New post: add an entry with about 3 links to sources a reader can verify."""
import json, os

S = {
 'GLR': ('https://support.google.com/business/answer/7091?hl=en', 'Google Business Profile Help: Tips to improve your local ranking on Google'),
 'GBPG': ('https://support.google.com/business/answer/3038177?hl=en', 'Google Business Profile Help: Guidelines for representing your business on Google'),
 'GCAT': ('https://support.google.com/business/answer/7249669?hl=en', 'Google Business Profile Help: Manage your business category'),
 'GREV': ('https://support.google.com/business/answer/3474122?hl=en', 'Google Business Profile Help: Tips to get more reviews'),
 'GUGC': ('https://support.google.com/contributionpolicy/answer/7400114?hl=en', 'Google Maps User Generated Content Policy: Prohibited and restricted content'),
 'GSUSP': ('https://support.google.com/business/answer/4569145?hl=en', 'Google Business Profile Help: Fix suspended or disabled profiles'),
 'LSA': ('https://support.google.com/localservices/answer/6224841?hl=en', 'Google Local Services Help: Getting started with Local Services Ads'),
 'LSARANK': ('https://support.google.com/localservices/answer/7527305?hl=en', 'Google Local Services Help: About ad rankings'),
 'LSASCREEN': ('https://support.google.com/localservices/answer/12174778?hl=en', 'Google Local Services Help: Business screening and verification requirements'),
 'ADSST': ('https://support.google.com/google-ads/answer/2472708?hl=en', 'Google Ads Help: About the search terms report'),
 'GSC': ('https://support.google.com/webmasters/answer/7576553?hl=en', 'Google Search Console Help: Performance report'),
 'KWSTUFF': ('https://developers.google.com/search/docs/essentials/spam-policies#keyword-stuffing', 'Google Search Central: Spam policies (keyword stuffing)'),
 'LINKSPAM': ('https://developers.google.com/search/docs/essentials/spam-policies#link-spam', 'Google Search Central: Spam policies (link spam)'),
 'TITLE': ('https://developers.google.com/search/docs/appearance/title-link', 'Google Search Central: Influencing title links in Google Search'),
 'AIFEAT': ('https://developers.google.com/search/docs/appearance/ai-features', 'Google Search Central: AI features and your website'),
 'CWV': ('https://developers.google.com/search/docs/appearance/core-web-vitals', 'Google Search Central: Understanding Core Web Vitals and Google search results'),
 'PAGEX': ('https://developers.google.com/search/docs/appearance/page-experience', 'Google Search Central: Understanding page experience'),
 'MOVE': ('https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes', 'Google Search Central: Site moves and migrations'),
 'DOINEED': ('https://developers.google.com/search/docs/fundamentals/do-i-need-seo', 'Google Search Central: Do you need an SEO?'),
 'WEBDEV': ('https://web.dev/learn/performance/why-speed-matters', 'web.dev (Google): Why does speed matter?'),
 'WCAG': ('https://www.w3.org/WAI/standards-guidelines/wcag/', 'W3C Web Accessibility Initiative: WCAG 2 overview'),
 'ABA71': ('https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_1_communication_concerning_a_lawyer_s_services/', 'American Bar Association: Model Rule 7.1, Communications Concerning a Lawyer\'s Services'),
 'ABA72': ('https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_2_advertising/', 'American Bar Association: Model Rule 7.2, Communications Concerning a Lawyer\'s Services: Specific Rules'),
 'ABA73': ('https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_3_direct_contact_with_prospective_clients/', 'American Bar Association: Model Rule 7.3, Solicitation of Clients'),
 'ABA15': ('https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_5_fees/', 'American Bar Association: Model Rule 1.5, Fees'),
 'MDL': ('https://www.law.cornell.edu/uscode/text/28/1407', 'Cornell Law School LII: 28 U.S. Code 1407, Multidistrict litigation'),
 'SOL': ('https://www.law.cornell.edu/wex/statute_of_limitations', 'Cornell Law School LII: Statute of limitations'),
 'COMP': ('https://www.law.cornell.edu/wex/comparative_negligence', 'Cornell Law School LII: Comparative negligence'),
 'NHTSA': ('https://www.nhtsa.gov/campaign/drive-sober-or-get-pulled-over', 'NHTSA: Drive Sober or Get Pulled Over'),
 'UW': ('https://www.washington.edu/news/2016/08/21/is-divorce-seasonal-uw-research-shows-biannual-spike-in-divorce-filings/', 'University of Washington: Is divorce seasonal? UW research shows biannual spike in divorce filings'),
 'HOTLINE': ('https://www.thehotline.org/', 'National Domestic Violence Hotline'),
 'PEW': ('https://www.pewresearch.org/short-reads/2025/06/25/34-of-us-adults-have-used-chatgpt-about-double-the-share-in-2023/', 'Pew Research Center: 34% of U.S. adults have used ChatGPT, about double the share in 2023'),
 'WHITESPARK': ('https://whitespark.ca/local-search-ranking-factors/', 'Whitespark: Local Search Ranking Factors report'),
 'BRIGHTLOCAL': ('https://www.brightlocal.com/research/local-consumer-review-survey/', 'BrightLocal: Local Consumer Review Survey'),
 'BATES': ('https://www.law.cornell.edu/supremecourt/text/433/350', 'Cornell Law School LII: Bates v. State Bar of Arizona, 433 U.S. 350 (1977)'),
 'WENTFORIT': ('https://www.law.cornell.edu/supremecourt/text/515/618', 'Cornell Law School LII: Florida Bar v. Went For It, Inc., 515 U.S. 618 (1995)'),
 'GADPOL': ('https://support.google.com/adspolicy/answer/6008942?hl=en', 'Google Advertising Policies Help: Google Ads policies'),
 'GNEG': ('https://support.google.com/google-ads/answer/2453972?hl=en', 'Google Ads Help: About negative keywords'),
 'GLOC': ('https://support.google.com/google-ads/answer/2453995?hl=en', 'Google Ads Help: About targeting geographic locations'),
 'GSCHED': ('https://support.google.com/google-ads/answer/2404244?hl=en', 'Google Ads Help: About ad scheduling'),
 'GCALL': ('https://support.google.com/google-ads/answer/2453991?hl=en', 'Google Ads Help: About call assets'),
 'GCONV': ('https://support.google.com/google-ads/answer/1722022?hl=en', 'Google Ads Help: About conversion measurement'),
 'CANSPAM': ('https://www.law.cornell.edu/uscode/text/15/7704', 'Cornell Law School LII: 15 U.S. Code 7704, Other protections for users of commercial electronic mail (CAN-SPAM Act)'),
 'GMAILSEND': ('https://support.google.com/a/answer/81126?hl=en', 'Gmail Help: Email sender guidelines'),
 'FTCBUY': ('https://www.law.cornell.edu/cfr/text/16/465.4', 'Cornell Law School LII: 16 CFR 465.4, Buying positive or negative consumer reviews (FTC rule)'),
 'FTCSUPP': ('https://www.law.cornell.edu/cfr/text/16/465.7', 'Cornell Law School LII: 16 CFR 465.7, Review suppression (FTC rule)'),
 'GREPLY': ('https://support.google.com/business/answer/3474050?hl=en', 'Google Business Profile Help: Manage customer reviews'),
 'GVERIFY': ('https://support.google.com/business/answer/7107242?hl=en', 'Google Business Profile Help: Verify your business on Google'),
 'CONFLICT': ('https://www.law.cornell.edu/wex/conflict_of_interest', 'Cornell Law School LII Wex: Conflict of interest'),
 'GPERS': ('https://support.google.com/adspolicy/answer/143465?hl=en', 'Google Advertising Policies Help: Restricted targeting in personalized advertising'),
 'PRIV': ('https://www.law.cornell.edu/wex/attorney-client_privilege', 'Cornell Law School LII Wex: Attorney-client privilege'),
}

SCREENED = ('Google Screened badge', 'Google Verified badge')
VERIFIED_FIX = {'old': 'Google Screened badge', 'new': 'Google Verified badge'}


def L(text, key):
    return {'text': text, 'url': S[key][0], 'title': S[key][1]}


PI = {
 'law-firm-marketing-trends': {
  'links': [L('A Pew Research Center survey found that about a third of U.S. adults had used ChatGPT', 'PEW'),
            L('Google says the best practices for SEO remain relevant for AI features in Google Search', 'AIFEAT'),
            L('leads come in as phone calls and messages sent through the ad', 'LSA'),
            L('Statements must not be false or misleading', 'ABA71')]},
 'reputation-management-for-attorneys': {
  'links': [L('reviews must reflect a genuine experience', 'GREV'),
            L('rule on consumer reviews makes it an unfair or deceptive practice to buy reviews', 'FTCBUY'),
            L('groundless legal threats or intimidation to get a review removed', 'FTCSUPP'),
            L('You can reply to reviews once your profile is verified', 'GREPLY'),
            L('Most states do not let lawyers give anything of value for a recommendation', 'ABA72')]},
 'personal-injury-lawyer-advertising': {
  'links': [L('Bates v. State Bar of Arizona', 'BATES'),
            L('Rule 7.1 says a lawyer must not make false or misleading statements about their services', 'ABA71'),
            L('Florida Bar v. Went For It', 'WENTFORIT'),
            L('Google also has its own advertising policies', 'GADPOL')]},
 'why-seo-for-personal-injury-lawyers-matters': {
  'edits': [{'old': 'Local Services Ads sit above everything else with a Google Screened badge',
             'new': 'Local Services Ads sit at the top of the page with a Google Verified badge'}],
  'links': [L('summaries Google and tools like ChatGPT now show before any link', 'AIFEAT'),
            L('Google Verified badge', 'LSA'),
            L('ranking in them depends on reviews, responsiveness and proximity', 'LSARANK'),
            L('Most PI firms work on contingency', 'ABA15')]},
 'how-personal-injury-lawyers-rank-in-the-google-map-pack': {
  'edits': [{'old': 'Google describes local ranking in three words: relevance, prominence and distance.',
             'new': 'Google says local results are mainly based on relevance, distance and popularity, which it used to call prominence.'}],
  'links': [L('Google says local results are mainly based on relevance, distance and popularity', 'GLR'),
            L('The primary category is the single most important field', 'WHITESPARK'),
            L("it breaks Google's rules", 'GUGC'),
            L("your state bar's advertising rules", 'ABA72')]},
 'how-to-get-personal-injury-clients': {
  'edits': [VERIFIED_FIX,
            {'old': 'and prominence (reviews, links and how well known your firm is)',
             'new': 'and prominence, which Google now calls popularity (reviews, links and how well known your firm is)'}],
  'links': [L('fast-growing new source', 'PEW'),
            L('Ranking there depends on three things', 'GLR'),
            L('ABA Model Rule 7.2', 'ABA72'),
            L('placement depends heavily on your reviews and how quickly you answer', 'LSARANK')]},
 'how-much-should-a-law-firm-spend-on-marketing': {
  'edits': [{'old': '</a> appear above the regular ads with a Google Screened badge',
             'new': '</a> usually appear at the top of the page with a Google Verified badge'},
            {'old': '<p>General small business guidance often suggests a figure in the high single digits as a share of revenue, and many legal marketing surveys report numbers in a similar range. ',
             'new': '<p>'}],
  'links': [L('Google Verified badge', 'LSA'),
            L('your placement depends on reviews and how quickly you respond', 'LSARANK'),
            L('being careful with past results and testimonials', 'ABA71'),
            L('following rules about paying for referrals', 'ABA72')]},
 'how-to-compare-seo-proposals-for-personal-injury-law-firms': {
  'links': [L("No agency controls Google's results.", 'DOINEED'),
            L('reviews and local listings', 'GLR'),
            L("state's rules on fee arrangements and referrals", 'ABA72')]},
 'law-firm-marketing-plan': {
  'links': [L('A fast, clear website', 'CWV'),
            L('Reviews, categories, photos and regular updates all play a part', 'GLR'),
            L('client solicitation', 'ABA73')]},
 'mass-tort-marketing': {
  'links': [L('multidistrict litigation (MDL)', 'MDL'),
            L('Filing deadlines also apply, and they vary by state and by injury', 'SOL'),
            L('fee sharing that has to follow your state rules', 'ABA15'),
            L('Bar rules on who may communicate with potential clients', 'ABA73')]},
 'personal-injury-intake-form': {
  'links': [L('Every state has deadlines for filing claims', 'SOL'),
            L('what staff can say to potential clients', 'ABA73'),
            L('That is both a bar rule concern', 'ABA71')]},
 'personal-injury-lead-generation': {
  'links': [L('charge per lead rather than per click', 'LSA'),
            L('generally do not allow a lawyer to give anything of value to someone for recommending the lawyer', 'ABA72'),
            L('A firm with many recent, genuine reviews tends to earn more calls', 'BRIGHTLOCAL')]},
 'personal-injury-marketing-ideas': {
  'links': [L('set the primary category to Personal Injury Attorney', 'GCAT'),
            L("Both break Google's rules", 'GUGC'),
            L("Google's appeals process", 'GSUSP'),
            L("Handle any referral fees only as your state's rules allow", 'ABA15')]},
 'seo-for-accident-claims': {
  'edits': [{'old': 'and injured people searching on a phone will leave a slow page within seconds',
             'new': 'and people on a phone are quick to leave a slow page: the BBC found it lost an additional 10% of users for every extra second its site took to load'}],
  'links': [L('how fault works in your state', 'COMP'),
            L('Google uses many of these signals in rankings', 'PAGEX'),
            L('the BBC found', 'WEBDEV'),
            L('bought link packages can lead to penalties', 'LINKSPAM')]},
 'seo-roi-case-studies-personal-injury-attorneys': {
  'links': [L('charge per lead instead of per click', 'LSA'),
            L('placement depends on reviews and responsiveness', 'LSARANK'),
            L('Google Business Profile work', 'GLR')]},
 'website-design-for-personal-injury-lawyers': {
  'links': [L('Google looks at how quickly and smoothly pages load as part of how it judges a website', 'CWV'),
            L('If page addresses change without proper redirects', 'MOVE'),
            L('strong color contrast', 'WCAG'),
            L('Words like expert or specialist can be restricted unless the lawyer holds a recognized certification', 'ABA72')]},
 'is-local-seo-worth-it-for-personal-injury-attorneys': {
  'edits': [VERIFIED_FIX],
  'links': [L('Google ties Map Pack rankings closely to where a business is actually located', 'GLR'),
            L("trying to fake a location can break Google's guidelines", 'GBPG'),
            L("These break Google's rules", 'GUGC'),
            L('Google Verified badge', 'LSA')]},
}

CRIMINAL = {
 'criminal-defense-attorney-website-design': {
  'links': [L('measure real-world user experience for loading performance, interactivity and visual stability', 'CWV'),
            L('Web Content Accessibility Guidelines, known as WCAG 2', 'WCAG'),
            L('a lawyer must not make false or misleading statements about their services', 'ABA71'),
            L('Words like specialist, expert or certified are restricted in many states', 'ABA72')]},
 'google-business-profile-for-criminal-defense-lawyers': {
  'links': [L('Google offers several ways to verify a business', 'GVERIFY'),
            L('including unnecessary information in your business name is not permitted', 'GBPG'),
            L('local results are mainly based on relevance, distance and popularity', 'GLR'),
            L('you can submit an appeal through', 'GSUSP'),
            L('offering incentives in exchange for reviews is strictly prohibited', 'GREV')]},
 'google-ads-for-criminal-defense-lawyers': {
  'links': [L('Negative keywords tell Google which searches should never show your ad', 'GNEG'),
            L('Google lets you choose between showing ads to people who are in or regularly in your target areas', 'GLOC'),
            L('Ad scheduling lets you choose the days and hours your ads appear', 'GSCHED'),
            L('Call assets add a phone number or call button to your search ads', 'GCALL'),
            L('Set up conversion tracking for the actions that matter', 'GCONV'),
            L('Google has its own advertising policies as well', 'GADPOL')]},
 'criminal-lawyer-advertising': {
  'links': [L('Reviewing the search terms report', 'ADSST'),
            L('For lawyers, Google screens the firm before the ads go live', 'LSASCREEN'),
            L('Many areas see more DUI enforcement around holidays', 'NHTSA'),
            L('Some states also limit contacting people directly', 'ABA73')]},
 'dui-lawyer-seo': {
  'links': [L('Google tends to show firms close to the person searching', 'GLR'),
            L('Never offer anything in return for a review, and never write reviews yourself', 'GUGC'),
            L('Nobody controls Google', 'DOINEED')]},
 'seo-keywords-for-criminal-defense-lawyers': {
  'links': [L('Tools like Google Search Console', 'GSC'),
            L('Use the keyword in the page title', 'TITLE'),
            L('Do not stuff the keyword in over and over', 'KWSTUFF')]},
}

DIVORCE = {
 'family-law-ppc': {
  'links': [L('Negative keywords let you exclude search terms from your campaigns', 'GNEG'),
            L('Google lets you choose between showing ads to people who are in or regularly in your target areas', 'GLOC'),
            L('A University of Washington study of divorce filings', 'UW'),
            L('Google lists relationship hardships among its sensitive interest categories', 'GPERS'),
            L('Google can track calls directly from your ads', 'GCONV')]},
 'family-law-intake-form': {
  'links': [L('check for potential conflicts before accepting someone as a client', 'CONFLICT'),
            L('if a third party is present during a privileged communication', 'PRIV'),
            L('National Domestic Violence Hotline', 'HOTLINE'),
            L('explain the scope of the work and the basis of the fee, preferably in writing', 'ABA15')]},
 'email-marketing-for-divorce-lawyers': {
  'links': [L('the CAN-SPAM Act sets basic rules for commercial email', 'CANSPAM'),
            L('sender guidelines, for example, ask senders to set up email authentication', 'GMAILSEND'),
            L('National Domestic Violence Hotline', 'HOTLINE'),
            L('Most states do not let lawyers pay or give anything of value for a recommendation', 'ABA72')]},
 'divorce-attorney-advertising': {
  'edits': [{'old': 'Some markets also see more interest in late summer, before children go back to school.',
             'new': 'Some markets also see more interest in late summer, before children go back to school. A University of Washington study of divorce filings found they peaked in March and August, the periods after the winter and summer holidays.'}],
  'links': [L('Watch the search terms report', 'ADSST'),
            L('Lawyers go through screening before the ads run', 'LSASCREEN'),
            L('A University of Washington study of divorce filings', 'UW'),
            L('care with words like expert or specialist', 'ABA72')]},
 'divorce-leads': {
  'links': [L('Google Ads and Local Services Ads', 'LSA'),
            L('when to share emergency resources', 'HOTLINE'),
            L('generally do not allow a lawyer to pay someone for recommending them', 'ABA72')]},
 'family-law-marketing-ideas': {
  'links': [L('as your main category', 'GCAT'),
            L('a direct link to your Google review page', 'GREV'),
            L('Never offer anything in return for a review', 'GUGC')]},
}

here = os.path.dirname(os.path.abspath(__file__))
for name, m in (('pi', PI), ('criminal', CRIMINAL), ('divorce', DIVORCE)):
    with open(os.path.join(here, name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
print('wrote', len(PI), len(CRIMINAL), len(DIVORCE))
