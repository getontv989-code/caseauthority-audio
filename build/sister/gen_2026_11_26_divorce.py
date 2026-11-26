#!/usr/bin/env python3
"""2026-11-26 divorce post: On-Page vs Off-Page SEO for Divorce Lawyers (basic SEO, agency angle: what each kind of SEO means and who does what). Zutrix 2026-11-26 (Google Ads volume, Zutrix KD): on page vs off page seo 110 KD22 (same volume on-page vs off-page seo, off page vs on page seo), what is on page vs off page seo 40 KD0, on page vs off page vs technical seo 10 (cluster ~160). Semrush connector returned ERROR 122 that day. Mash approved 2026-11-26 ("tie it to their niches, 2000 plus words, our assets").
Nearest live pages: family-law-seo (service page), seo-audit-for-family-law-firms (service page), blog/seo-contract (contracts). This post explains the three kinds of SEO for a family law site, not the service offer.
Facts used (sources_patch, keys checked in earlier rounds): Google title links doc (generated automatically), Core Web Vitals doc, Google spam policies (link spam, keyword stuffing), Google local ranking (relevance, distance, popularity). No pricing figures."""
import json, os
P = {
 'slug': 'on-page-vs-off-page-seo-for-divorce-lawyers',
 'keyword': 'on page vs off page seo',
 'title': 'On-Page vs Off-Page SEO for Divorce Lawyers, Explained',
 'meta': 'On-page vs off-page SEO for divorce and family law firms: what each one covers, how technical SEO fits in, and which parts your firm and your agency should own.',
 'h1': 'On-Page vs Off-Page SEO: What Each One Means for a Divorce and Family Law Firm',
 'nav_label': 'On-Page vs Off-Page SEO',
 'tag': 'SEO Basics',
 'date': '2026-11-26',
 'lead': "Sit through enough marketing calls and you will hear the phrases on-page SEO and off-page SEO thrown around as if everyone knows what they mean. Most family lawyers nod along, because they are busy and the agency seems confident. Then the invoice arrives with line items like on-page optimization and off-page authority building, and it is hard to tell what was actually done or whether it was worth doing. It does not need to be that murky. On-page SEO is the work done on your own website. Off-page SEO is the work done elsewhere that makes people and search engines trust your firm. Technical SEO is the plumbing that lets both of them work. This guide explains each one in the context of a divorce and family law practice, shows where they overlap and helps you see which parts matter most for the clients you want.",
 'quick_answer': "On-page SEO is everything on your own website that helps it rank: the words on each page, titles and headings, how pages are organized and linked together and how clearly they answer what people search. Off-page SEO is everything outside your website that builds trust in your firm: your Google Business Profile, reviews, mentions and links from respected sites, directory listings and your reputation in the community. Technical SEO, often grouped with on-page work, makes sure your site is fast, secure and easy for search engines to crawl. A family law firm needs all three. On-page work tells Google what you do and where. Off-page work convinces Google, and the people searching, that you are the firm to trust with something as personal as a divorce or custody case.",
 'takeaways': [
  ['On-Page Is Your Site.', 'Words, titles, headings and links on your own pages.'],
  ['Off-Page Is Your Reputation.', 'Reviews, mentions and links from other sites.'],
  ['Technical Is the Plumbing.', 'Speed, security and pages Google can reach.'],
  ['You Need All Three.', 'Great pages without trust, or trust without pages, both stall.'],
  ['The Map Is Off-Page Too.', 'Your Google Business Profile lives outside your site.'],
  ['Know Who Does What.', 'Agree which parts the firm owns and which the agency handles.'],
 ],
 'sections': [
  {'h2': 'What Is the Difference Between On-Page and Off-Page SEO?',
   'answer': 'On-page SEO is work on your own website. Off-page SEO is work outside it that builds trust and reputation.',
   'paras': [
    "Think of your firm's online presence as a courtroom. On-page SEO is your own case: the evidence you present, how clearly it is organized and how well it answers the questions in front of the judge. Off-page SEO is what others say about you: the witnesses, the character references, your standing in the local legal community. A strong case with no credibility struggles, and a good reputation with a sloppy case does too.",
    "On-page work happens on pages you control. You can rewrite a paragraph about child custody, change a page title or add a link from your divorce page to your mediation page today. Off-page work depends partly on other people. A local news site decides whether to quote you, clients decide whether to leave reviews and other organizations decide whether to list or link to your firm.",
    "Search engines use both. Your own pages tell them what you do, where you do it and how well you explain it. Signals from elsewhere tell them whether you are a real, established, trusted firm. For a sensitive practice area like family law, where people are choosing someone to guide them through one of the hardest periods of their lives, both sides carry real weight.",
   ]},
  {'h2': 'What Does On-Page SEO Include for a Family Law Firm?',
   'answer': 'Clear practice pages, helpful answers to common questions, good titles and headings, sensible internal links and content that matches what people in your area search.',
   'paras': [
    "The heart of on-page SEO is your content. Most family law firms need a clear page for each main service they want clients for: divorce, contested divorce, uncontested divorce, child custody, child support, spousal support, property division, prenuptial agreements, adoption, protective orders and so on. Each page should explain the service in plain terms, describe how it works in your state and county and make it easy to get in touch.",
    "On-page SEO also covers the parts search engines read closely. The page title, the main heading and the first few lines should make it obvious what the page is about and where you practice. Headings should break the page into the questions people actually ask, such as how custody is decided or how long a divorce takes in your state. Short, direct answers near the top help both readers and AI tools.",
    "Finally, it covers how your pages connect. Internal links, meaning links from one page on your site to another, guide visitors from a general divorce page to the more specific pages on custody, support or mediation. They also help search engines understand which pages matter most. Our page on [[a:divorce-attorney-content-marketing|divorce attorney content marketing]] covers how to plan that content.",
   ]},
  {'h2': 'How Much Do Page Titles and Headings Matter?',
   'answer': 'A lot. They are among the clearest signals of what a page is about, and they shape how your result looks in search.',
   'paras': [
    "Your page title is the clickable line people see in search results, and it is one of the first things a search engine reads. Google says its title links are generated automatically, drawing mainly on the title you set but also on headings and other text on the page. That means a clear, accurate title gives you the best chance of controlling how your result appears.",
    "A good title for a family law page names the service and the place and reads like something a person would click. Child Custody Lawyer in a named county, with your firm name at the end, is clearer than a vague title like Our Practice Areas. Each page should have its own title. Ten pages all called Family Law Attorney confuse search engines and searchers alike.",
    "Headings matter for a similar reason. They help people scanning on a phone find the part they need, and they show search engines how the page is organized. A page that answers the five questions people most often ask about custody, each under its own heading, usually serves both readers and rankings better than a single long block of text.",
   ]},
  {'h2': 'What Is Technical SEO, and Is It On-Page or Off-Page?',
   'answer': 'It is the behind the scenes work that lets search engines find, load and understand your site, and it is usually grouped with on-page SEO.',
   'paras': [
    "Technical SEO covers how your website is built rather than what it says. Can search engines reach every important page? Does the site load quickly on a phone? Is it secure? Are old pages redirected when they move? Is there structured data that tells search engines your firm's name, address, phone and practice areas?",
    "Because it all happens on your own site, most people group technical SEO with on-page work, and some list it as a third category. The label matters less than the work. A family law site with brilliant content will still struggle if Google cannot crawl half of it, or if pages take so long to load that people give up.",
    "Speed deserves special mention. Many people searching for a divorce lawyer are doing so on a phone, often privately and in short bursts. Google's Core Web Vitals measure real-world user experience for loading performance, interactivity and visual stability, and a site that is slow or jumps around while loading frustrates exactly the people you want to reach. Our page on [[a:family-law-website-design|family law website design]] covers how design and speed work together.",
   ]},
  {'h2': 'What Does Off-Page SEO Include for a Divorce Lawyer?',
   'answer': 'Your Google Business Profile, reviews, directory listings, mentions and links from trusted sites and your wider reputation.',
   'paras': [
    "Off-page SEO is everything outside your website that shapes how search engines and people see your firm. For most family law firms the biggest single piece is the Google Business Profile, the listing that appears on Google Maps and in the map results for searches like divorce lawyer near me. It lives on Google, not on your site, which is why it counts as off-page work.",
    "Reviews come next. They influence where you appear on the map and whether people trust you enough to call. Directory listings, such as bar association listings and established legal directories, help confirm that your name, address and phone number are real and consistent. Mentions and links from respected sites, such as local news, family law organizations, community groups and legal publications, show that others vouch for your firm.",
    "Off-page work also includes the less measurable parts of reputation: speaking at local events, contributing to legal publications and building referral relationships with therapists, financial advisers and other professionals. These rarely show up as a line in an SEO report, but they create the mentions and searches that help your firm stand out.",
   ]},
  {'h2': 'Why Is the Google Business Profile So Important in Family Law?',
   'answer': 'Because many people searching for a divorce or custody lawyer see the map first and call straight from it.',
   'paras': [
    "When someone searches for a divorce lawyer, a custody attorney or a family law firm near them, Google often shows a map with three firms before the regular results. Many people never scroll further. They read the reviews, check the distance and tap call. For a local practice, that map spot can be worth more than any single page on your website.",
    "Google says local results are mainly based on relevance, distance and popularity. You cannot change where a searcher is standing, but you can make your profile as relevant as possible with the right categories, services and description, and you can build popularity through genuine reviews and a strong reputation. Keeping the profile accurate and active is one of the highest value off-page tasks for most family law firms.",
    "It also needs protecting. Profiles can be suspended for problems such as keywords stuffed into the business name or an address that does not meet Google's guidelines. Our guide on what to do when a [[a:blog/google-business-profile-suspended|Google Business Profile is suspended]] explains how to avoid that and how to recover if it happens.",
   ]},
  {'h2': 'How Do Reviews Fit Into Off-Page SEO for a Divorce Practice?',
   'answer': 'They are a trust signal for both Google and future clients, and they need careful, private handling in family law.',
   'paras': [
    "Reviews help in two ways. They are part of how Google judges a firm's popularity on the map, and they are often the deciding factor for someone choosing between three family law firms they have never heard of. A steady flow of recent, genuine reviews tends to help on both fronts.",
    "Family law adds a layer of care. Many clients do not want their name next to a review about their divorce. Some will want to share their experience, and others never will, and both choices should be respected. Ask simply and without pressure, never offer anything in return and never review yourself or ask staff to do it.",
    "Replies need even more care. A reply must never confirm that the reviewer was a client, mention their case or reveal anything private, even if the review is negative or unfair. A short, professional reply that thanks people for feedback and invites them to call the office is usually the safest approach. Get this wrong and you risk both your reputation and a bar complaint.",
   ]},
  {'h2': 'What Makes a Good Link for a Family Law Firm?',
   'answer': 'A link from a real, relevant, respected site that chose to mention your firm, not a link that was bought or traded.',
   'paras': [
    "A link from another website works a bit like a referral. A link from your local family court's resource page, a respected parenting organization, a regional newspaper or a state bar section tells search engines your firm is trusted by people who know the field. One such link can matter more than hundreds of links from directories nobody uses.",
    "The way links are earned matters as much as where they come from. Google's spam policies say links bought or traded to manipulate rankings break its spam policies, and sites caught doing it can lose visibility. Good off-page work earns links through real activity: commenting on family law changes for local media, writing for legal publications, sponsoring community programs and creating resources others want to cite.",
    "When an agency reports on links, ask where they came from. A short list of real, relevant sites is a good sign. A long list of unfamiliar sites, especially ones that publish anything for a fee, is worth questioning.",
   ]},
  {'h2': 'Which Matters More for Divorce Lawyers, On-Page or Off-Page SEO?',
   'answer': 'Neither on its own. On-page work is usually the place to start, and off-page work is what helps you win competitive searches.',
   'paras': [
    "If your website is thin, out of date or missing pages for the services you want, start there. No amount of reviews or links will rank a custody page that does not exist. On-page work is also fully in your control, so it is often the fastest place to make progress.",
    "Once your pages are solid, off-page work becomes the deciding factor in competitive markets. In a large city, dozens of family law firms will have decent websites. The ones that rise to the top of the map and the results tend to have stronger reviews, more trusted mentions and a clearer reputation.",
    "The best results come from doing both steadily, rather than swinging from one to the other. A family law firm that publishes clear, helpful pages and builds its reputation month after month will usually outpace one that does a burst of either and then stops.",
   ]},
  {'h2': 'Which Parts Should Your Firm Own, and Which Can an Agency Handle?',
   'answer': 'The firm should own its accounts, client relationships and legal accuracy. An agency can handle most of the technical, content and outreach work.',
   'paras': [
    "Some things should always stay with the firm. Your domain, website, Google Business Profile, Search Console and analytics accounts should be in the firm's name. Client relationships, including how and when you ask for reviews, belong with the firm. So does the final say on anything that describes the law or your services, because the bar holds the lawyers responsible.",
    "An agency can take on most of the rest. Technical fixes, keyword research, drafting and improving practice pages, structuring headings and internal links, managing the Business Profile, monitoring reviews and earning genuine mentions are all work a good agency handles. What matters is that you can see what they did and why.",
    "When you review a proposal or a contract, look for this split in plain words. Our guide to the [[a:blog/seo-contract|SEO contract]] explains what to look for in the paperwork, and our page on [[a:family-law-seo|family law SEO]] explains how we approach the work.",
   ]},
  {'h2': 'Common On-Page and Off-Page Mistakes Family Law Firms Make',
   'answer': 'One page for every service, stuffed keywords, slow mobile pages, ignored reviews and shortcuts like bought links.',
   'paras': [
    "On the website side, the most common mistake is a single practice areas page that tries to cover divorce, custody, support, adoption and more in a few paragraphs. It ranks for none of them well. The second is writing for search engines instead of people, repeating city names and keywords until the page reads badly. Google's spam policies on keyword stuffing exist for exactly this reason.",
    "Technical mistakes are often invisible until they hurt. A site redesign that changes every page address without redirects, a mobile page that loads slowly or a form that quietly stops working can undo months of progress. Regular checks catch these before they cost you clients.",
    "Off the website, the common mistakes are a neglected or inaccurate Business Profile, no plan for asking for reviews, careless replies that reveal too much and shortcuts like bought links or fake listings. Each can damage both your rankings and your standing with the bar.",
   ]},
  {'h2': 'How Do You Know if On-Page and Off-Page SEO Are Working?',
   'answer': 'Watch calls and enquiries from search, map visibility, clicks on your key pages and the quality of the clients who reach you.',
   'paras': [
    "On-page progress often shows up first in Google Search Console, the free tool that shows which searches your pages appear for and how often people click. If your custody page starts appearing for more custody searches in your county and getting more clicks, the on-page work is likely helping.",
    "Off-page progress tends to show up on the map and in the phone. More appearances in the map pack across your area, more calls from your Business Profile and more people saying they found you on Google are good signs. Reviews growing steadily is another.",
    "The final measure is whether the right clients are calling. A family law firm that wants complex custody and high asset divorces should judge SEO by those enquiries, not just by overall traffic. Agree with your agency which numbers matter most and review them regularly.",
   ]},
  {'h2': 'A Note on Trademarks, Figures and Bar Rules',
   'answer': 'This guide explains how on-page and off-page SEO generally work and does not promise any ranking or result.',
   'paras': [
    "Google, Google Business Profile, Google Maps and Google Search Console are trademarks of Google LLC. CaseAuthority is not affiliated with, endorsed by or sponsored by Google. Descriptions of Google's tools and policies are based on what Google publishes on its own public pages at the time of writing, which can change.",
    "Search results vary by market, competition, location and device, and nothing in this guide promises a ranking, a number of calls or any outcome. Lawyer advertising rules vary by state, especially on reviews, testimonials and specialist claims, so check your state bar's current rules before publishing.",
   ]},
 ],
 'faq': [
  {'q': 'What Is On-Page SEO in Simple Terms?', 'a': 'It is the work done on your own website to help it rank, such as clear practice pages, good titles and headings, helpful answers and sensible links between pages.'},
  {'q': 'What Is Off-Page SEO in Simple Terms?', 'a': 'It is the work done outside your website that builds trust, such as your Google Business Profile, reviews, directory listings and mentions or links from respected sites.'},
  {'q': 'Is Technical SEO Part of On-Page SEO?', 'a': 'It is usually grouped with on-page work because it happens on your site. It covers speed, security, crawling and structured data.'},
  {'q': 'Is Google Business Profile On-Page or Off-Page SEO?', 'a': 'Off-page. The profile lives on Google, not on your website, but it is one of the most important parts of SEO for a local family law firm.'},
  {'q': 'Which Should a Divorce Firm Do First?', 'a': 'Usually on-page, by making sure you have clear pages for the services you want. Then build reviews, mentions and links to compete for the busiest searches.'},
  {'q': 'Can I Do Off-Page SEO Myself?', 'a': 'Some of it, such as asking for reviews and keeping your profile accurate. Earning media mentions and links usually takes more time and outreach.'},
 ],
 'related': ['family-law-seo', 'local-seo-for-divorce-lawyers', 'family-law-website-design', 'seo-audit-for-family-law-firms'],
}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(P, open(os.path.join(here, 'divorce', P['slug'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', P['slug'])
