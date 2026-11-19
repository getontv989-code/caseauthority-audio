#!/usr/bin/env python3
"""2026-11-19 criminal post: questions to ask when hiring an SEO company (Semrush 880/mo KD 14, + 'questions to ask seo company' 480 KD 16, 'questions to ask an seo company' 260 KD 3, 'questions to ask seo marketing company' 210 KD 12, 'questions to ask local seo company' 170 KD 7, 'questions to ask seo agency' 170 KD 14, 'what questions to ask a seo company' 170 KD 14, 'questions to ask seo agency before hiring' 70, cluster about 2,400). Mash approved: tailored to criminal defense firms.
Cluster: questions about experience with criminal defense, charge and court pages, local SEO and the map, reporting, ownership, links, timelines, AI search, intake, contracts; answers that should worry you.
Facts used (checked 2026-11-19): Google Search Central 'Do you need an SEO?' (sample interview questions: examples of previous work, Google Search Essentials, results and timeframe, how success is measured, experience in your industry and city, sharing all changes; only grant read access to Search Console at audit stage; SEO should ask what makes your business unique; no one can guarantee a #1 ranking); Search Console Help users and permissions (restricted user has simple view rights on most data); SEO starter guide (changes can take a few hours to several months). Links to the PI blog are not used; links go to criminal posts how-to-get-criminal-defense-clients and seo-keywords-for-criminal-defense-lawyers."""
import json, os
P = {
 'slug': 'questions-to-ask-when-hiring-an-seo-company',
 'keyword': 'questions to ask when hiring an seo company',
 'title': 'Questions to Ask When Hiring an SEO Company for Criminal Defense',
 'meta': 'The questions criminal defense lawyers should ask before hiring an SEO company, what good answers sound like and the replies that should make you walk away.',
 'h1': 'Questions to Ask When Hiring an SEO Company for Your Criminal Defense Firm',
 'nav_label': 'Questions to Ask an SEO Company',
 'tag': 'Hiring an SEO Agency',
 'date': '2026-11-19',
 'lead': "Hiring an SEO company is a big decision for a criminal defense firm. The right partner can help people who have just been arrested, charged or called in for questioning find your firm first, often at the most stressful moment of their lives. The wrong one can waste a year of fees, fill your site with pages that do not convert or put your rankings at risk. The best way to tell them apart is to ask good questions before you sign. This guide covers the questions criminal defense lawyers should ask any SEO company or agency, what good answers tend to sound like, the replies that should make you walk away and how to judge the answers by the thing that matters most: calls that turn into retained clients.",
 'quick_answer': 'Before hiring an SEO company, ask about its experience with criminal defense firms, how it would rank you for the charges and courts you handle, what work it will do each month, how it measures calls and retained clients, who owns your website and accounts, how it earns links and how long results usually take. Google suggests asking for examples of past work, whether the company follows Google Search Essentials, what results it expects and in what timeframe and whether it will share every change it makes to your site. Good answers are specific, honest about time and focused on your market. Be wary of guaranteed rankings, secret methods, vague reporting and contracts that keep your site or profile if you leave.',
 'takeaways': [
  ['Ask About Your Practice.', 'Charges, courts and cities matter more than general SEO talk.'],
  ['Ask How They Measure.', 'Calls and retained clients beat rankings and traffic charts.'],
  ['Ask Who Owns What.', 'Your site, content and Google profile should stay yours.'],
  ['Ask About Links.', 'Shortcuts can put your rankings and reputation at risk.'],
  ['Ask About Time.', 'Honest agencies give realistic timelines, not promises.'],
  ['Watch Their Questions.', 'A good agency asks about your firm before it pitches.'],
 ],
 'sections': [
  {'h2': 'Why Do Criminal Defense Firms Need to Ask Different Questions?',
   'answer': 'Because criminal defense clients search fast, local and charge by charge, so an SEO company has to understand urgency, courts and bar rules, not just general marketing.',
   'paras': [
    'Most people who need a criminal defense lawyer did not plan to. They search after an arrest, a DUI stop, a call from a detective or a court date that is days away. They type things like DUI lawyer near me, assault lawyer in a county or how to get a charge dropped, and they often call the first firm that looks capable and answers the phone.',
    'That makes criminal defense SEO different from many other practice areas. It depends on strong local visibility, pages for each charge and court you handle, a Google Business Profile that shows up in the map and a site that makes calling easy on a phone. It also has to follow your state bar\'s advertising rules and protect client confidentiality.',
    'An SEO company that works mainly with shops, dentists or software firms may do good work in general but miss these details. The questions below are designed to show quickly whether an agency understands how people choose a criminal defense lawyer. Our guide to [[a:blog/how-to-get-criminal-defense-clients|how to get criminal defense clients]] covers the wider picture.',
   ]},
  {'h2': 'What Experience Do You Have With Criminal Defense Law Firms?',
   'answer': 'Ask for examples of work for criminal defense or other law firms, how results were measured and whether you can speak with past clients.',
   'paras': [
    'Google suggests a simple starting question when interviewing an SEO: can you show me examples of your previous work and share some success stories? It also suggests asking about the company\'s experience in your industry and in your country or city. For a criminal defense firm, that means asking about law firms in general and criminal defense in particular.',
    'Listen for specifics. A good answer names the kinds of firms the company has worked with, the markets they were in and what changed, such as more calls from search, better map visibility or more consultations for certain charges. A weak answer talks only about traffic growth or awards without explaining what that meant for the firm.',
    'Ask for references and actually call them. Google recommends checking an SEO\'s business references and asking past clients whether the service was useful, the company was easy to work with and the results were positive. Respect that some firms will not want to be named, but an agency with no references at all is a risk.',
   ]},
  {'h2': 'How Would You Help Us Rank for the Charges and Courts We Handle?',
   'answer': 'A good agency will talk about pages for each main charge, the courts and counties you serve and the questions people ask, not just a single practice page.',
   'paras': [
    'Ask the agency how it would structure your site. Criminal defense searches are very specific. Someone charged with a DUI is not searching for criminal defense in general, and someone facing drug charges in one county may never see a page written for another. A strong plan usually includes pages for your main charges, such as DUI, drug charges, assault, theft and domestic violence, and for the courts and areas you serve.',
    'Ask how it would make those pages genuinely useful. Good pages explain the charge, the possible penalties in plain terms, what happens at the local court and what to do next, without promising outcomes. Thin pages that swap one city name for another rarely help people and can fall foul of Google\'s guidance on low value content.',
    'Ask about keywords too. A good agency will explain which searches it would target first and why, based on search volume, competition and the cases you want more of. Our guide to [[a:blog/seo-keywords-for-criminal-defense-lawyers|SEO keywords for criminal defense lawyers]] shows the kinds of searches that matter.',
   ]},
  {'h2': 'What Will You Do for Our Google Business Profile and Map Rankings?',
   'answer': 'Ask how the agency will improve your profile, categories, reviews and local signals, because many criminal defense calls come straight from the map.',
   'paras': [
    'When someone searches for a DUI lawyer or criminal defense attorney near them, Google often shows a map with three firms before any normal results. Many people call straight from there. So ask the agency what it will do to help you appear in that map for the areas you serve.',
    'A good answer covers your Google Business Profile categories, services and description, photos, your address and phone details, how you will earn honest reviews and how your website supports your profile with clear local pages. It should also mention following Google\'s guidelines for representing your business, since breaking them can lead to a suspended profile.',
    'Ask who will own and control the profile. Your firm should be the owner, with the agency added as a manager if needed. If an agency creates a new profile for you, make sure it is in your name and that you have full access from day one.',
   ]},
  {'h2': 'What Work Will You Do Each Month?',
   'answer': 'Ask for a clear list of deliverables, such as pages, fixes, profile work and outreach, so you can see what you are paying for and check it was done.',
   'paras': [
    'SEO can feel like a black box, and that is where many firms get frustrated. Ask the agency to describe what a typical month looks like. How many pages will it write or improve? What technical work will it do? How much time goes to your Google Business Profile, links and reporting?',
    'You do not need every detail fixed in stone, because a good plan changes as results come in. But you should know the main activities and how you will see them. Google suggests asking whether the SEO will share all the changes it makes to your site and provide detailed information about its recommendations and the reasoning behind them.',
    'Be careful with answers that are all strategy and no work. Phrases like ongoing optimization or authority building are fine, but ask what they mean in practice. If the agency cannot explain its work in plain language, it will be hard for you to judge it later.',
   ]},
  {'h2': 'How Will You Measure Success and Report to Us?',
   'answer': 'Ask how the agency tracks calls, forms and retained clients from search, not just rankings, and how often you will see a report you can understand.',
   'paras': [
    'Google suggests asking any SEO how it measures success. For a criminal defense firm, the honest answer should lead to calls and retained clients. Rankings and traffic are useful signs of progress, but they do not pay the bills.',
    'Ask how calls from your website and Google profile will be tracked, how form fills and chat leads will be counted and how you can connect those leads to consultations and retained clients in your intake system. Ask what data you will see from your own Google Search Console and analytics accounts, not just the agency\'s own tools.',
    'Ask how often reports come and what they include. A useful report explains what was done, what changed and what comes next, in plain words. If a report is all charts with no explanation, ask for a short monthly call or summary as well.',
   ]},
  {'h2': 'Who Owns Our Website, Content and Accounts?',
   'answer': 'Your firm should own its domain, website, content, Google Business Profile, Search Console and analytics, and keep them all if you ever leave.',
   'paras': [
    'This may be the most important question of all. Some marketing companies build sites on their own platforms, register domains in their own name or keep control of Google profiles. That can make it very hard to leave, because you lose the very things you paid to build.',
    'Ask directly. Who owns the domain? Who owns the website and its content? If you host it, can we move it? Who is the owner of our Google Business Profile, Google Search Console and analytics? What happens to all of this if we cancel?',
    'Be careful with access, too. Google suggests that if an SEO offers an audit, you should only grant read access to Search Console at that stage, not write access. Search Console lets you add a restricted user, who has simple view rights on most data, which is usually enough for an audit. Grant fuller access later, once you have decided to work together.',
   ]},
  {'h2': 'How Do You Earn Links and Mentions?',
   'answer': 'Ask how the agency earns links, because bought or traded links can hurt your rankings, while genuine local and legal mentions help.',
   'paras': [
    'Links from other websites still matter for SEO, and criminal defense is a competitive area. That tempts some agencies to buy links, trade them or place them on low quality sites. Google\'s spam policies treat links bought or traded to manipulate rankings as a violation, and the damage can take a long time to repair.',
    'A good answer focuses on earning genuine mentions. That might include local bar association listings, community involvement, speaking at events, helpful guides other sites want to reference, legal directories that matter in your market and press coverage handled within your state bar\'s rules.',
    'Ask to see examples of links the agency has earned for other firms, and ask how many it typically builds. Large numbers of links with no detail on where they come from are a warning sign. Google also notes that you should never have to link to an SEO.',
   ]},
  {'h2': 'How Long Will It Take to See Results?',
   'answer': 'An honest agency will say it depends on your site, market and competitors, and will explain early signs of progress before calls and clients grow.',
   'paras': [
    'Google suggests asking what kind of results the SEO expects to see, and in what timeframe. Google\'s own SEO starter guide says some changes might take effect in a few hours, others could take several months. In a competitive criminal defense market, building strong visibility often takes longer than that.',
    'A good answer is honest and specific. It might explain that technical fixes and profile improvements can show early movement, while new charge pages and links build over months. It should also explain what you will see first, such as more impressions in Search Console, then more clicks and then more calls.',
    'Be wary of any promise of the first page or a number one spot by a certain date. Google says no one can guarantee a #1 ranking on Google, and warns people to be careful with SEOs that claim to guarantee rankings.',
   ]},
  {'h2': 'How Do You Handle Bar Rules and Client Confidentiality?',
   'answer': 'Ask how the agency checks content against your state bar\'s advertising rules and keeps client details out of reviews, case results and reports.',
   'paras': [
    'Your website, Google profile and every page an agency writes for you are lawyer advertising. Ask how the agency handles that. Does it understand that some states restrict words like expert or specialist? Does it know that claims about results may need disclaimers? Will you approve every page before it goes live?',
    'Confidentiality matters even more in criminal defense. Ask how the agency handles reviews, case results and testimonials, and how it makes sure replies to reviews never confirm that someone was a client or mention details of a case. Ask what client data, if any, the agency will see and how it is protected.',
    'A good agency will treat you as the final decision maker on anything that touches your bar rules. It should be comfortable saying that it follows common practices but that you, or your ethics counsel, have the final word.',
   ]},
  {'h2': 'Are You Ready for AI Search and Answer Engines?',
   'answer': 'Ask how the agency approaches AI features in Google and AI assistants, and listen for answers based on strong pages and good SEO rather than secret tricks.',
   'paras': [
    'More people now see AI answers in Google and ask AI assistants questions like what happens after a first DUI. Some agencies sell special services for this, sometimes called AEO or GEO. It is fair to ask what they do and how it differs from good SEO.',
    'Google says the best practices for SEO remain relevant for AI features in Google Search. Its guide to hiring an SEO also suggests checking whether any advice on optimizing for AI experiences is aligned with Google\'s official guidance. A good answer talks about clear, accurate pages that answer real questions, strong local signals and a trustworthy site.',
    'Be careful with promises that your firm will be the answer in any AI tool. No one controls those systems. Clear, helpful content written for the people you serve is still the best way to show up.',
   ]},
  {'h2': 'What Do You Need From Us, and What Is in the Contract?',
   'answer': 'Ask what the agency needs from your team, how long the contract runs, how you can leave and what notice is needed, before you sign anything.',
   'paras': [
    'SEO works best as a partnership. Ask what the agency needs from you, such as time for interviews about your practice, reviews of new pages, photos, details about the courts you appear in and feedback from your intake team. A firm that cannot give any time may struggle to get the best results.',
    'Then ask about the contract. How long is the term? Is there a minimum period? How much notice is needed to cancel? Are there setup fees? What happens to your site and accounts if you leave? Read the contract as carefully as you would any agreement you review for a client.',
    'Finally, notice what the agency asks you. Google says a good SEO should be interested in you and your business and should ask what makes it unique, who your competitors are and how your customers find you. If an agency talks only about itself, that tells you a lot.',
   ]},
  {'h2': 'Which Answers Should Make You Walk Away?',
   'answer': 'Guaranteed rankings, a special relationship with Google, secret methods, no references, vague reporting and contracts that keep your site or profile are reasons to say no.',
   'paras': [
    'Some answers should end the conversation. Google says to beware of SEOs that claim to guarantee rankings, allege a special relationship with Google or advertise a priority submit to Google. It also says to be careful if a company is secretive or will not clearly explain what it intends to do.',
    'Other warning signs include an agency that cannot name any law firm clients, refuses to share which keywords it will target, will not let you own your website or Google profile, promises large numbers of links with no detail or pushes you to sign on the first call.',
    'Trust your instincts. You judge witnesses and opposing counsel for a living. If an agency\'s answers sound rehearsed, vague or too good to be true, keep looking. The right SEO partner will be happy to answer every question on this list in plain words.',
   ]},
  {'h2': 'A Note on Figures, Independence and Bar Rules',
   'answer': 'This guide is general information, CaseAuthority is not affiliated with Google and nothing here promises any ranking or result.',
   'paras': [
    'Google, Google Search Console and Google Business Profile are trademarks of Google LLC. CaseAuthority is not affiliated with, endorsed by or sponsored by Google. Descriptions of what Google says are based on its own public pages at the time of writing, which may change. Results from SEO vary by market, competition, the condition of a website and many other factors, and no part of this guide promises any ranking, number of clients or outcome.',
    'Lawyer advertising is regulated and the rules vary by state, including rules on website content, reviews, case results and words like expert or specialist. The ideas in this guide describe common practices in legal marketing. They are not legal advice. Check your state bar\'s current rules or speak to an ethics counsel if you are unsure.',
   ]},
 ],
 'faq': [
  {'q': 'What Is the Most Important Question to Ask an SEO Company?', 'a': 'Ask how it will measure success. For a criminal defense firm, the answer should lead to calls, consultations and retained clients from search, not just rankings or traffic.'},
  {'q': 'Should I Hire an SEO Company That Guarantees Results?', 'a': 'Be careful. Google says no one can guarantee a #1 ranking on Google. A good agency can promise its work and reporting, but not where Google will rank you.'},
  {'q': 'What Access Should I Give an SEO Company?', 'a': 'For an audit, Google suggests read access to Search Console only. Once you hire them, add the agency as a user or manager, but keep your firm as the owner of every account.'},
  {'q': 'How Do I Check an SEO Company\'s References?', 'a': 'Ask for past law firm clients you can speak with, and ask them whether the service was useful, easy to work with and brought results they could measure.'},
  {'q': 'Do Criminal Defense Firms Need a Specialist SEO Agency?', 'a': 'Not always, but the agency should understand urgent local searches, charge and court pages, the Google map and state bar advertising rules. Ask for examples that show it.'},
  {'q': 'How Many SEO Companies Should I Interview?', 'a': 'Speaking with at least two or three helps you compare answers, plans and reporting. Ask each one the same questions so you can compare them fairly.'},
 ],
 'related': ['criminal-defense-seo-expert', 'criminal-defense-marketing-agency', 'criminal-defense-law-firm-seo', 'local-seo-for-criminal-defense-lawyers'],
}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(P, open(os.path.join(here, 'criminal', P['slug'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', P['slug'])
