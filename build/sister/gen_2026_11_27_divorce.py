#!/usr/bin/env python3
"""2026-11-27 divorce post: Outsource SEO for Family Law Firms (agency vs freelancer vs in-house). Semrush web UI (US, bulk) 2026-11-27: outsource seo 1,900 KD20 $24.81; seo outsourcing 1,600 KD26 $18.30; outsourcing seo 1,000 KD24 $16.16; outsourced seo 1,000 KD25 $24.81; outsourcing seo services 720 KD26; in house seo 390 KD28; hire seo freelancer 320 KD27; seo agency vs freelancer 70 KD14; seo agency vs in house 50 KD20 (cluster ~7,050). Semrush API connector returned ERROR 122. Mash approved 2026-11-27.
Nearest live pages: blog/seo-contract (contract terms), family-law-marketing-agency (service page), criminal blog/what-does-an-seo-agency-do-for-criminal-defense-lawyers (the work itself). This post is the decision: outsource or not, and to whom. Leans to agency, no smug tone toward freelancers.
Facts used (sources_patch, checked 2026-11-27): Google Do you need an SEO (sometimes hiring a professional can be helpful; a small local business can do much of the work itself), SEO starter guide (no secrets), link spam policy, ABA Model Rule 7.1. No pricing figures."""
import json, os
P = {
 'slug': 'outsource-seo-for-family-law-firms',
 'keyword': 'outsource seo',
 'title': 'Outsource SEO for Family Law Firms: Agency, Freelancer or In-House?',
 'meta': 'Should a family law firm outsource SEO? Compare an agency, a freelancer and an in-house hire, what each handles well and how to decide for your divorce practice.',
 'h1': 'Should a Family Law Firm Outsource SEO? Agency, Freelancer or In-House Compared',
 'nav_label': 'Outsourcing SEO',
 'tag': 'Working With an Agency',
 'date': '2026-11-27',
 'lead': "Most family law firms reach the same point sooner or later. The website is a few years old, the phone is quieter than it should be and a competitor across town seems to show up for every divorce search. Someone has to own SEO, and the question is who. You could hire someone onto the team, bring in a freelancer or hand the work to an agency. Each option can work, and each one can go badly wrong. The right choice depends on the size of your firm, how competitive your market is and how much time the partners can spend managing it. This guide walks through what outsourcing SEO really means for a divorce and family law practice, how the three options compare and how to decide.",
 'quick_answer': "Outsourcing SEO means paying an outside specialist, either a freelancer or an agency, to handle the work of getting your family law firm found on Google rather than hiring someone onto your staff. For most small and mid-sized family law firms, outsourcing to a specialist agency is the most practical choice, because SEO needs several skills at once: technical site work, content about divorce, custody and support, Google Business Profile management, local links and call tracking. A freelancer can suit a firm with modest needs and a clear scope. An in-house hire makes sense mainly for larger firms with several offices and enough work to keep a specialist busy. Whichever route you take, the firm should own its accounts, agree clear goals and judge the work by consultations and signed clients.",
 'takeaways': [
  ['SEO Is Several Jobs.', 'Technical work, content, the map, links and tracking all need skill.'],
  ['Agencies Bring a Team.', 'One partner covers every skill, with cover when someone is away.'],
  ['Freelancers Suit Narrow Jobs.', 'Good for a defined project or a firm with modest needs.'],
  ['In-House Needs Scale.', 'Usually worth it for larger, multi-office firms.'],
  ['Keep Ownership In-House.', 'Whoever does the work, the firm owns the accounts.'],
  ['Judge by Signed Clients.', 'Consultations and retainers, not traffic, decide if it works.'],
 ],
 'sections': [
  {'h2': 'What Does It Mean to Outsource SEO?',
   'answer': 'It means paying an outside freelancer or agency to do the work of getting your firm found in search, instead of hiring a staff member to do it.',
   'paras': [
    "SEO, or search engine optimization, is the work of helping your firm show up when people search for help with divorce, custody, support or other family law matters, and turning those searches into calls. Someone has to do that work. When it is done by a person on your payroll, it is in-house. When it is done by someone outside the firm under an agreement, it is outsourced.",
    "Outsourcing is common in law. Firms already outsource bookkeeping, IT support, process serving and often web design. SEO fits the same pattern, because it is specialist work that most lawyers neither have time for nor want to learn in depth. Google itself acknowledges this, noting that sometimes hiring a professional can be helpful, while also warning that the wrong hire can damage a site.",
    "Outsourcing does not mean handing over the whole relationship with your clients or giving up control. The best outsourced setups keep the firm firmly in charge: the firm owns the accounts, sets the goals and approves anything that describes the law or the firm's services. The outside team does the specialist work within those lines.",
   ]},
  {'h2': 'Why Do Family Law Firms Outsource SEO?',
   'answer': 'Because SEO needs several specialist skills, steady attention and up to date knowledge that few small firms can keep in-house.',
   'paras': [
    "Family law SEO is not one task. It includes fixing technical problems on the website, writing clear pages for divorce, custody, support, mediation and protective orders, managing the Google Business Profile and reviews with care, earning mentions from local and legal sources, tracking calls and forms and reporting on all of it. Few people are excellent at every one of those.",
    "It also needs steady attention. Family law searches are local and competitive, and the firms ranking above you are not standing still. A burst of effort followed by months of silence rarely works. Outsourcing gives you someone whose job is to keep the work moving every month, even when the partners are in trial or mediation.",
    "Finally, search changes constantly. Google updates how it ranks pages, how the map works and how AI answers appear at the top of results. A specialist who works on many sites sees these changes early. A busy firm that only thinks about SEO occasionally usually sees them late, after the calls have already dropped.",
   ]},
  {'h2': 'Can a Family Law Firm Do SEO Itself?',
   'answer': 'Some of it, yes. The basics are worth doing in any case, but the specialist parts are where most firms get stuck.',
   'paras': [
    "Google says that if you run a small local business, you can probably do much of the work yourself, starting with its SEO starter guide. That is fair. A firm can keep its Google Business Profile accurate, ask happy clients for reviews, make sure its name, address and phone number match everywhere and answer common questions on its website.",
    "The harder parts are technical site work, research into what people actually search, structured data, earning genuine media mentions and reliable call tracking. These take time to learn and time to do well. They are also where mistakes cost the most. A technical error can hide your pages from Google for months without anyone noticing.",
    "Many family law firms find a middle path. The firm keeps the parts that need the lawyers' voice and judgment, such as reviewing content and replying to reviews, and outsources the rest. Even if you outsource everything, knowing the basics helps you judge whether the work is good. Our guide on [[a:blog/on-page-vs-off-page-seo-for-divorce-lawyers|on-page vs off-page SEO for divorce lawyers]] is a good starting point.",
   ]},
  {'h2': 'What Are the Three Main Options?',
   'answer': 'An in-house hire, an independent freelancer or a specialist agency, each with a different balance of control, skill and cost.',
   'paras': [
    "The first option is to hire someone onto your staff. They work only for your firm, know your practice closely and can respond quickly. The second is a freelancer, an independent specialist who works for several clients and takes on a defined scope for your firm. The third is an agency, a team that handles SEO for multiple firms and assigns several people to your account.",
    "There is no single right answer for every firm. A solo practitioner, a five lawyer divorce boutique and a regional family law firm with four offices will each weigh the options differently. The useful question is not which option is best in general, but which one fits your firm's size, market and appetite for managing the work.",
    "The sections below look at each option in turn, then at how to decide. Throughout, keep one point in mind. Whoever does the work, the firm should own its domain, website, Google Business Profile, Search Console and analytics. That protects you whichever route you choose and makes it easier to change course later.",
   ]},
  {'h2': 'When Does an In-House SEO Hire Make Sense?',
   'answer': 'Mainly for larger family law firms with several offices and enough ongoing work to keep a specialist fully busy.',
   'paras': [
    "An in-house hire has real strengths. They are part of the team, attend meetings, learn the firm's voice and can coordinate closely with intake and the lawyers. For a large firm with several offices, many practice pages and a steady stream of content, that closeness can be valuable.",
    "The challenges are just as real. One person rarely has every skill SEO needs, so an in-house hire often still relies on outside help for technical work or links. They need tools, training and someone at the firm who can manage and judge their work. And if they leave, the knowledge often leaves with them, along with any accounts that were set up in their name.",
    "For most small and mid-sized family law firms, a full-time SEO role is more capacity than the work needs. Some firms combine the two approaches, with a marketing coordinator in-house who works alongside an outside agency. That can give the firm a single point of contact while still drawing on a wider team.",
   ]},
  {'h2': 'When Does a Freelancer Make Sense?',
   'answer': 'For a defined project or a firm with modest, clear needs, where one skilled person can cover the work.',
   'paras': [
    "A good freelancer can be an excellent fit. Many are highly skilled specialists who left agencies to work independently. They are often flexible, direct to work with and well suited to a clearly defined job, such as a technical audit, a set of new practice pages or cleaning up your Google Business Profile.",
    "The limits come from being one person. A freelancer may be strong in technical SEO but less experienced with content, or skilled at content but new to local links. Holidays, illness and busy periods with other clients can slow things down. And if the freelancer moves on, the firm needs to find someone new and bring them up to speed.",
    "If you choose a freelancer, agree the scope in writing, check examples of their work with other professional services firms and make sure everything they set up is in the firm's name. For an ongoing, all round SEO program in a competitive family law market, many firms find they need more than one person can give.",
   ]},
  {'h2': 'When Does an Agency Make Sense?',
   'answer': 'For most small and mid-sized family law firms that want one partner to cover every part of SEO consistently.',
   'paras': [
    "An agency brings a team. Technical specialists, writers, local search specialists and analysts can each handle the part they know best, coordinated by one main contact. If someone is away, the work continues. If Google changes something, the team usually sees it across many sites and adjusts quickly.",
    "A specialist legal agency adds something more: familiarity with how family law clients search and what they need to see. People looking for a divorce lawyer often search privately, sometimes worried about a spouse seeing their history, and they want calm, clear information before they call. An agency that understands that writes and builds differently from one that mostly works with shops and restaurants.",
    "The risks with agencies are real too. Some are slow, some put junior staff on accounts and some use shortcuts that break Google's rules. That is why choosing the right agency matters more than the decision to use one. Our page on [[a:family-law-marketing-agency|working with a family law marketing agency]] explains how we approach it.",
   ]},
  {'h2': 'How Do the Options Compare Side by Side?',
   'answer': 'In-house gives the most closeness, freelancers the most flexibility and agencies the widest range of skills and the most continuity.',
   'paras': [
    "On skills, agencies usually cover the most ground, freelancers cover a focused set and an in-house hire covers whatever one person knows. On continuity, agencies tend to be strongest because the work does not stop when one person is away, while freelancers and in-house hires depend on a single individual.",
    "On closeness to the firm, in-house wins. An employee knows the partners, the intake team and the cases better than any outside party. Freelancers and agencies can come close with good communication and regular check-ins, but they will always be one step removed.",
    "On management time, agencies and good freelancers usually need less from the firm, because they bring their own processes. An in-house hire needs someone at the firm to set goals, review work and support their development. Total cost depends on the market and the scope of work, so compare like for like: what exactly each option will do each month, and what it would cost the firm if that work did not happen.",
   ]},
  {'h2': 'What Should Stay In-House Whatever You Choose?',
   'answer': 'Ownership of every account, final review of legal content, client communication and the decision about which cases you want.',
   'paras': [
    "Some things should never be outsourced. The firm should own its domain, website, hosting, Google Business Profile, Search Console, analytics and call tracking, with outside specialists added as users. That way the firm keeps its history and can change providers without losing anything.",
    "Legal content needs a lawyer's eye. Anything that explains divorce, custody, support or property division in your state should be reviewed by someone at the firm before it goes live. ABA Model Rule 7.1 says a lawyer shall not make a false or misleading communication about the lawyer's services, and the responsibility for what appears on your website stays with the firm.",
    "Client communication stays with the firm too. Replies to reviews, follow-up with leads and intake decisions belong with people who understand family law clients and the firm's duties to them. Finally, the firm decides which cases it wants more of. An outside team can only aim the work well if you tell it clearly where to aim.",
   ]},
  {'h2': 'What Are the Warning Signs of Bad Outsourced SEO?',
   'answer': 'Guaranteed rankings, secret methods, accounts in the provider\'s name, vague reports and bought links.',
   'paras': [
    "Be cautious of anyone who guarantees first place on Google or a set number of cases. Google's starter guide is clear that there are no secrets that will automatically rank your site first. Promises like that usually mean either a misunderstanding of how search works or tactics that put the firm at risk.",
    "Watch how links are earned. Google's policies say links bought or traded to manipulate rankings break its spam policies, and a family law site caught that way can lose visibility it took years to build. Ask any provider to describe where links come from. Local news, bar groups, community organizations and legal publications are good answers.",
    "Other warning signs are quieter. Accounts set up in the provider's name, reports full of charts but no list of work done, a reluctance to explain changes and long silences between updates all suggest a relationship that will be hard to judge and hard to leave. Our guide on [[a:blog/seo-contract|what to check in an SEO contract]] covers the terms that protect the firm.",
   ]},
  {'h2': 'How Should You Measure Outsourced SEO?',
   'answer': 'By consultations and signed clients from search, supported by calls, forms and map visibility, reviewed together each month.',
   'paras': [
    "Whoever does the work, agree up front how you will judge it. For a family law firm, the numbers that matter most are calls and forms from search, consultations booked and clients retained. Behind those sit leading indicators, such as map visibility in your area and rankings for the searches that bring in the cases you want.",
    "Make sure the tracking is in place before judging results. Calls from your website and your map listing should be counted, and intake should record where each new client found the firm. Without that, it is impossible to tell whether SEO is working or simply busy.",
    "Review the numbers together each month, and ask what work was done and what comes next. A good outsourced partner welcomes these conversations, because clear results are the best case for continuing the relationship.",
   ]},
  {'h2': 'How Do You Decide What Is Right for Your Firm?',
   'answer': 'Match the option to your firm\'s size, market, budget and how much time the partners can give to managing it.',
   'paras': [
    "Start with three questions. How competitive is family law search in your area? How many practice areas and offices do you need to promote? How much time can someone at the firm realistically spend managing SEO each month? A solo practitioner in a smaller market has different needs from a multi-office firm in a major city.",
    "For many firms, the answer is a specialist agency for the ongoing work, with the firm keeping ownership and final review. Firms with a narrow, defined need may do well with a skilled freelancer. Larger firms with steady work across several offices may justify an in-house role, often supported by outside specialists.",
    "Whatever you choose, revisit the decision once a year. Firms grow, markets change and what fit three years ago may not fit today. If the firm owns its accounts and the work is well documented, changing course is straightforward.",
   ]},
  {'h2': 'A Note on Trademarks, Figures and Bar Rules',
   'answer': 'This guide compares common ways firms handle SEO and does not promise any ranking or result.',
   'paras': [
    "Google and Google Business Profile are trademarks of Google LLC. CaseAuthority is not affiliated with, endorsed by or sponsored by Google. Descriptions of Google's guidance are based on what Google publishes on its own public pages at the time of writing, which can change.",
    "Nothing in this guide promises a ranking, a number of calls or any outcome, and results vary by market, competition and the work done. Lawyer advertising rules and rules on sharing client information with vendors vary by state, so check your state bar's current rules before engaging an outside provider.",
   ]},
 ],
 'faq': [
  {'q': 'Is It Better to Outsource SEO or Do It In-House?', 'a': 'For most small and mid-sized family law firms, outsourcing to a specialist is more practical. In-house usually makes sense for larger firms with several offices and steady work.'},
  {'q': 'Should I Hire an SEO Freelancer or an Agency?', 'a': 'A freelancer suits a defined project or modest needs. An agency suits ongoing, all round SEO in a competitive market, because it brings several skills and continuity.'},
  {'q': 'What SEO Work Can a Family Law Firm Do Itself?', 'a': 'Keeping the Google Business Profile accurate, asking clients for reviews, keeping contact details consistent and answering common questions on the website.'},
  {'q': 'Who Should Own My Accounts if I Outsource SEO?', 'a': 'The firm. Your domain, website, Google Business Profile, Search Console and analytics should be in the firm name, with outside specialists added as users.'},
  {'q': 'How Do I Know if Outsourced SEO Is Working?', 'a': 'Track calls, forms, consultations and signed clients from search, alongside map visibility and rankings for the searches that matter to your firm.'},
  {'q': 'Can Outsourced SEO Hurt My Firm?', 'a': 'Yes, if the provider uses tactics such as bought links or misleading content. Choose carefully and ask how they earn links and what they change.'},
 ],
 'related': ['family-law-marketing-agency', 'family-law-seo', 'local-seo-for-divorce-lawyers', 'seo-audit-for-family-law-firms'],
}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(P, open(os.path.join(here, 'divorce', P['slug'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', P['slug'])
