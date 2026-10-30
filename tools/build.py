# -*- coding: utf-8 -*-
"""Sanhita Atlas — annotated reference to the Bharatiya Nyaya Sanhita, 2023."""
import html
import json
import os
import re
import shutil

E = lambda s: html.escape(str(s), quote=True)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "dist")
SEC = json.load(open("/scratch/work/bns/sections.json", encoding="utf-8"))
BYN = {s["n"]: s for s in SEC}

CHAPTERS = [
    (1, "I", "Preliminary", 1, 3, "#6b7280", "Short title, application, definitions and general explanations."),
    (2, "II", "Punishments", 4, 13, "#b45309", "The seven punishments, commutation, fines and solitary confinement."),
    (3, "III", "General Exceptions", 14, 44, "#0f766e", "Mistake, accident, infancy, unsoundness of mind, consent, necessity — and the right of private defence."),
    (4, "IV", "Abetment, Criminal Conspiracy and Attempt", 45, 62, "#7c2d12", "Liability for instigating, conspiring and attempting, including abetment that never ripens into the offence."),
    (5, "V", "Offences against Woman and Child", 63, 99, "#9d174d", "Sexual offences, criminal force, marriage offences, miscarriage, trafficking and offences against children."),
    (6, "VI", "Offences affecting the Human Body", 100, 146, "#1e40af", "Culpable homicide and murder, hurt, restraint and confinement, kidnapping and forced labour."),
    (7, "VII", "Offences against the State", 147, 158, "#4c1d95", "Waging war, conspiracy against the State, and acts endangering sovereignty."),
    (8, "VIII", "Offences relating to the Army, Navy and Air Force", 159, 168, "#166534", "Abetting mutiny and seducing service personnel from their allegiance."),
    (9, "IX", "Offences relating to Elections", 169, 177, "#a16207", "Bribery, undue influence, personation and interference with elections."),
    (10, "X", "Offences relating to Coin, Currency and Government Stamps", 178, 188, "#0e7490", "Counterfeiting coins and notes, and offences against government stamps."),
    (11, "XI", "Offences against Public Tranquillity", 189, 197, "#b91c1c", "Unlawful assembly, rioting, affray and promoting enmity."),
    (12, "XII", "Offences by or relating to Public Servants", 198, 205, "#3f6212", "Disobedience of law, false records and unlawful trade by officials."),
    (13, "XIII", "Contempt of the Lawful Authority of Public Servants", 206, 226, "#7e22ce", "Obstruction, false information, resistance to apprehension and attempt to suicide."),
    (14, "XIV", "False Evidence and Offences against Public Justice", 227, 269, "#155e75", "Perjury, fabricated evidence, harbouring, escape and bail-jumping."),
    (15, "XV", "Offences affecting Public Health, Safety, Decency and Morals", 270, 297, "#9a3412", "Nuisance, adulteration, obscenity and negligence with dangerous substances."),
    (16, "XVI", "Offences relating to Religion", 298, 302, "#4338ca", "Defiling places of worship, outraging religious feelings and disturbing assemblies."),
    (17, "XVII", "Offences against Property", 303, 334, "#065f46", "Theft, snatching, extortion, robbery, dacoity, criminal breach of trust, cheating, mischief and trespass."),
    (18, "XVIII", "Offences relating to Documents and Property Marks", 335, 350, "#86198f", "Forgery, false documents and electronic records, counterfeit seals and property marks."),
    (19, "XIX", "Criminal Intimidation, Insult, Annoyance and Defamation", 351, 357, "#a21caf", "Threats, intentional insult, statements conducing to public mischief and defamation."),
    (20, "XX", "Repeal and Savings", 358, 358, "#44403c", "Repeals the Indian Penal Code, 1860, with a savings clause for pending proceedings."),
]
CHOF = {}
for n, r, t, f, l, c, b in CHAPTERS:
    for i in range(f, l + 1):
        CHOF[i] = (n, r, t, c)

IPC = {"4": "53", "34": "96", "61": "120B", "63": "375", "64": "376", "70": "376D", "74": "354",
       "75": "354A", "78": "354D", "79": "509", "85": "498A", "100": "299", "101": "300",
       "103": "302", "105": "304", "106": "304A", "109": "307", "111": "—", "113": "—",
       "115": "323", "117": "325", "118": "324", "119": "326", "124": "326A", "137": "363",
       "140": "364A", "143": "370", "152": "124A", "189": "141", "191": "147", "196": "153A",
       "226": "309", "238": "201", "303": "379", "304": "—", "308": "384", "309": "392",
       "310": "395", "316": "406", "317": "411", "318": "420", "336": "465", "338": "467",
       "351": "506", "356": "499/500"}

# ── annotations: explanation, worked example, case law ───────────────────
ANN = {
 4: dict(
  why=["Section 4 fixes the menu of sentences a court may impose. Six are carried over from the IPC; the seventh — "
       "community service — is new, and it is the only punishment in the code that is defined nowhere else.",
       "The order matters in practice: a court must select from this list, and a sentence that is not one of the "
       "seven is not a sentence the Sanhita authorises."],
  ex="An offender convicted for the first time of theft of property worth less than ₹5,000 may be ordered to "
     "perform community service instead of a short custodial sentence, under the proviso to s. 303(2).",
  cases=[("Bachan Singh v State of Punjab", "(1980) 2 SCC 684",
          "Death is a permissible but exceptional sentence. A court must weigh aggravating against mitigating "
          "circumstances and record reasons; it cannot be imposed as a matter of course."),
         ("Mithu v State of Punjab", "(1983) 2 SCC 277",
          "A provision making the death sentence mandatory for a class of murders was struck down — the sentencing "
          "discretion cannot be taken away by statute.")]),
 34: dict(
  why=["The right of private defence is the one place where the code permits a person to use force that would "
       "otherwise be an offence. It is protective, not punitive: it exists to repel an attack, and it ends the "
       "moment the threat does.",
       "Sections 35 to 44 supply the detail — when the right extends to causing death, when it begins and when it "
       "continues, and the limits where the aggressor is not the real danger."],
  ex="A shopkeeper struck on the head with an iron rod grabs a stool and strikes back while the attacker is still "
     "advancing. He acts in private defence of the body; had he pursued the attacker after he fled, the right "
     "would have ended.",
  cases=[("Darshan Singh v State of Punjab", "(2010) 2 SCC 333",
          "The right arises from a reasonable apprehension of danger, not from actual harm. The force used must be "
          "proportionate to the threat, and the right is not available to a person who starts the fight.")]),
 63: dict(
  why=["Section 63 is definitional: it describes the act, and s. 64 supplies the punishment. The seven "
       "descriptions in sub-clauses (a) to (d) are exhaustive — conduct outside them is not rape under this "
       "section, however serious.",
       "The section retains a marital exception: intercourse with a wife who is not under eighteen is excluded. "
       "The explanations fix the meaning of consent, and make absence of physical resistance irrelevant."],
  ex="Consent given because the woman believes she is about to be killed is not consent — Explanation 2 to s. 63. "
     "The act falls within clause (a) and is punished under s. 64.",
  cases=[("Independent Thought v Union of India", "(2017) 10 SCC 800",
          "The marital exception cannot be read to permit intercourse with a wife between fifteen and eighteen; "
          "the court read down the exception to harmonise it with the age of consent.")]),
 69: dict(
  why=["Section 69 closes a gap the IPC left open. Where intercourse is obtained by deceit — a false promise of "
       "marriage, or a promise made without any intention of keeping it — but the ingredients of s. 63 are not "
       "made out, this section applies.",
       "It is a new offence, so there is no IPC equivalent and no case law under it yet."],
  ex="A man promises marriage to induce a woman to have intercourse, never intending to marry her. The conduct is "
     "not rape, because consent was not obtained by fear or fraud as s. 63 defines it — but it is an offence "
     "under this section."),
 75: dict(
  why=["Section 75 codifies what the Supreme Court had already required of every employer in Vishaka. It lists "
       "four kinds of unwelcome conduct, and the explanation makes clear that the standard is the recipient's "
       "experience, not the actor's intention.",
       "The provision sits alongside the POSH Act, 2013, which supplies the complaint machinery the criminal "
       "section does not."],
  ex="A supervisor who repeatedly sends sexually coloured messages to a junior after being asked to stop commits "
     "the offence under clause (iv), even if no physical contact occurs.",
  cases=[("Vishaka v State of Rajasthan", "(1997) 6 SCC 241",
          "The Court laid down binding guidelines on sexual harassment at the workplace — the direct precursor to "
          "both this section and the 2013 Act.")]),
 79: dict(
  why=["Section 79 punishes the word or gesture itself, not any resulting harm. The insult to modesty is the "
       "gravamen; the provision is complete on utterance.",
       "It is a cognizable, bailable offence, and it is often charged together with s. 74 where force is also used."],
  ex="A man makes an obscene gesture at a woman in a public place intending to insult her modesty. The offence is "
     "complete without any assault.",
  cases=[("Rupan Deol Bajaj v K.P.S. Gill", "(1995) 6 SCC 194",
          "The Court set aside the quashing of proceedings, holding that whether conduct outrages modesty is a "
          "question of fact to be tried, not decided at the threshold.")]),
 85: dict(
  why=["Section 85 carries forward IPC 498-A. The offence is cruelty by a husband or his relatives, and the "
       "explanation defines cruelty in two ways: conduct likely to drive a woman to suicide or grave injury, and "
       "harassment made with a view to coercing her or her family for property.",
       "It is cognizable, non-bailable and non-compoundable — which is why the arrest guidelines matter so much "
       "in practice."],
  ex="A husband and his mother repeatedly demand that the wife bring a car from her parents, and threaten her with "
     "consequences if she does not. That is cruelty under clause (b) of the explanation.",
  cases=[("Arnesh Kumar v State of Bihar", "(2014) 8 SCC 273",
          "For offences punishable with up to seven years, arrest is not automatic. Police must satisfy themselves "
          "that arrest is necessary, and magistrates must not authorise detention mechanically."),
         ("Rajesh Sharma v State of U.P.", "(2017) 8 SCC 821",
          "Introduced family welfare committees before arrest in 498-A complaints. The committee directions were "
          "later modified in Social Action Forum for Manav Adhikar (2018), which retained the Arnesh Kumar "
          "safeguards instead.")]),
 100: dict(
  why=["Section 100 defines culpable homicide: causing death by an act done with the intention of causing death, "
       "or of causing such bodily injury as is likely to cause death, or with knowledge that the act is likely to "
       "cause death.",
       "Everything in Chapter VI that ends in a death begins here. Murder in s. 101 is a subset of culpable "
       "homicide, not a separate act."],
  ex="A man pushes a stranger during a quarrel; the stranger falls, strikes his head and dies. There is no "
     "intention to kill and no knowledge that death was likely — but the act is culpable homicide if the "
     "requisite intention or knowledge as to injury is present.",
  cases=[("State of A.P. v Rayavarapu Punnayya", "(1976) 4 SCC 382",
          "Laid down the method for distinguishing culpable homicide from murder: first ask whether the act falls "
          "within s. 299 at all, then whether it falls within one of the four clauses of s. 300.")]),
 101: dict(
  why=["Section 101 defines murder. It applies where the act falls within s. 100 and is done with the intention of "
       "causing death, or of causing injury the offender knows to be likely to cause death, or is in itself "
       "sufficient in the ordinary course of nature to cause death.",
       "Sub-section (2) is new: a group of five or more acting in concert on grounds of race, caste, community, "
       "sex, place of birth, language or personal belief commits murder. This is the provision aimed at mob "
       "lynching."],
  ex="Five men drag a man from his shop and beat him to death because of his community. Each member of the group "
     "is liable under s. 101(2), and the punishment is in s. 103(2).",
  cases=[("Virsa Singh v State of Punjab", "AIR 1958 SC 465",
          "For clause three, the prosecution must prove only that the injury was intentional and was sufficient "
          "in the ordinary course of nature to cause death — not that death was intended.")]),
 103: dict(
  why=["Section 103 fixes the punishment for murder: death or imprisonment for life, and a fine. Neither is "
       "mandatory. Sub-section (2) covers group murder under s. 101(2), and adds a minimum fine of ₹5 lakh.",
       "The choice between the two sentences is where most of the argument in a murder trial actually happens."],
  ex="A single assailant convicted under s. 101(1) faces life or death; the court must give reasons for whichever "
     "it chooses, and the prosecution must place aggravating circumstances on record.",
  cases=[("Bachan Singh v State of Punjab", "(1980) 2 SCC 684",
          "Death is reserved for the rarest of rare cases, where the alternative of life is unquestionably "
          "foreclosed."),
         ("Machhi Singh v State of Punjab", "(1983) 3 SCC 470",
          "Set out the aggravating factors — manner of the murder, motive, the victim's vulnerability — that a "
          "court weighs before imposing death.")]),
 106: dict(
  why=["Section 106 punishes causing death by a rash or negligent act. The base punishment was raised from two "
       "years to five, and sub-section (2) is new: a driver who causes death by rash or negligent driving and "
       "then escapes without reporting to the police faces up to ten years.",
       "The distinction between rashness and negligence is the whole argument in these cases — rashness is "
       "advertence to risk without desire for the consequence; negligence is the failure to advert at all."],
  ex="A truck driver overtakes on a blind curve at speed, kills a pedestrian and drives on without stopping. That "
     "is s. 106(2), not s. 106(1) — the escape is the aggravating element.",
  cases=[("Alister Anthony Pareira v State of Maharashtra", "(2012) 2 SCC 648",
          "In cases of drunken or rash driving, a heavy sentence may be justified; the court must consider the "
          "gravity of the consequences alongside the offender's conduct."),
         ("State of Punjab v Saurabh Bakshi", "(2015) 5 SCC 182",
          "Courts should not be lenient in fatal road-accident cases; the sentence must reflect the public interest "
          "in deterrence.")]),
 152: dict(
  why=["Section 152 replaces sedition. The label is gone, but the offence is broader in one respect: it expressly "
       "covers exciting or attempting to excite secession or armed rebellion, and it adds electronic communication "
       "and financial means to the modes of commission.",
       "The constitutional question that surrounded s. 124-A — whether criticising the government can be an offence "
       "— has not been settled under the new provision."],
  ex="A person publishes a video calling for an armed uprising against the State. That falls within s. 152. "
     "Publishing an article criticising a government policy, without more, does not.",
  cases=[("Kedar Nath Singh v State of Bihar", "AIR 1962 SC 955",
          "Sedition is constitutional only if it is read to require incitement to violence or a tendency to create "
          "public disorder — mere criticism of the government is protected speech."),
         ("S.G. Vombatkere v Union of India", "(2022) 7 SCC 209",
          "The Supreme Court kept s. 124-A IPC in abeyance pending reconsideration — a decision that now bears on "
          "how s. 152 is used.")]),
 196: dict(
  why=["Section 196 punishes promoting disharmony or feelings of enmity between groups on grounds of religion, "
       "race, place of birth, residence or language. The Sanhita adds electronic communication to the modes, and "
       "language to the grounds.",
       "The offence requires a deliberate act, not merely words that offend."],
  ex="A speaker at a public meeting urges the crowd to attack members of another religion. That is promoting "
     "enmity under s. 196(1)(a).",
  cases=[("Rangarajan v P. Jagjivan Ram", "(1989) 2 SCC 574",
          "The mens rea of promoting disharmony is essential. An article that is critical but not intended to "
          "create hostility between groups does not fall within the section.")]),
 226: dict(
  why=["Section 226 retains attempt to suicide as an offence, but changes what happens to the person who attempts "
       "it. Sub-section (2) creates a presumption that the person was suffering from severe stress, and "
       "sub-section (3) directs the State to provide rehabilitation rather than prosecution.",
       "The offence exists mainly to give the police a lawful basis to intervene and to take the person to a "
       "hospital or shelter."],
  ex="A person who attempts suicide after a family dispute is presumed to be under severe stress; the magistrate "
     "may direct release on a bond and refer the person for counselling.",
  cases=[("Gian Kaur v State of Punjab", "(1996) 2 SCC 648",
          "The right to life does not include the right to die; attempt to suicide and abetment of suicide are "
          "distinct offences."),
         ("Common Cause v Union of India", "(2018) 5 SCC 1",
          "Recognised passive euthanasia and advance medical directives, which changes the ground on which "
          "withdrawal of treatment is analysed.")]),
 303: dict(
  why=["Theft is the dishonest taking of movable property out of another's possession without consent. The "
       "definition is in sub-section (1); the punishment is in sub-section (2), which also provides for community "
       "service on a first conviction of small-value theft.",
       "Three elements have to be proved: a dishonest intention, movable property, and moving it out of the "
       "complainant's possession without consent."],
  ex="A cashier who moves ₹200 from the till into his pocket intending never to return it commits theft, even if "
     "he is caught before leaving the shop.",
  cases=[("K.N. Mehra v State of Rajasthan", "AIR 1957 SC 369",
          "There must be a fresh and independent movement of the property in order to take it; merely handling or "
          "touching it is not enough.")]),
 316: dict(
  why=["Criminal breach of trust is the dishonest misappropriation of property that was entrusted to the accused. "
       "The essence is the entrustment — the property must have been handed over for a purpose, and then used "
       "against that purpose.",
       "The section grades punishment by the offender's role: a carrier or warehouse-keeper, a clerk or servant, "
       "and a public servant all attract higher sentences."],
  ex="A lawyer receives ₹10 lakh from a client to be held in escrow and spends it on his own expenses. That is "
     "criminal breach of trust under s. 316(2).",
  cases=[("Jaikrishnadas Manohardas Desai v State of Bombay", "AIR 1960 SC 889",
          "The prosecution must establish entrustment and dishonest misappropriation; mere inability to account "
          "for the property is not by itself enough.")]),
 318: dict(
  why=["Cheating requires deception followed by dishonest inducement. The deception must precede the delivery of "
       "property, and the inducement must be dishonest — a broken promise made in good faith is a civil wrong, "
       "not this offence.",
       "Punishment is graded by the value of the property and by whether the offender attempted to cause death or "
       "grievous hurt."],
  ex="A man sells a plot he has already sold to someone else, knowing he has no title, and takes the buyer's "
     "money. That is cheating under s. 318(4).",
  cases=[("Hridaya Ranjan Prasad Verma v State of Bihar", "(2000) 4 SCC 168",
          "The distinction between breach of contract and cheating turns on intention at the time of the "
          "transaction. A mere failure to keep a promise is not cheating.")]),
 356: dict(
  why=["Defamation punishes the publication of an imputation intended to harm reputation. Sub-section (1) covers "
       "the making or publishing, and the exceptions carve out truth for the public good, fair comment and "
       "privileged statements.",
       "The Sanhita adds community service as an alternative to imprisonment, which matters because most "
       "defamation prosecutions end in a fine."],
  ex="A newspaper publishes an allegation that a businessman has committed fraud, knowing it to be false. That is "
     "defamation under s. 356(1), unless truth for the public good is established.",
  cases=[("Subramanian Swamy v Union of India", "(2016) 7 SCC 221",
          "Criminal defamation was upheld as a reasonable restriction on speech under Article 19(2), the Court "
          "holding that reputation is a facet of the right to life.")]),
 111: dict(
  why=["Organised crime is new. It targets continuing unlawful activity by a crime syndicate — kidnapping, "
       "extortion, land grabbing, contract killing, economic offences, cyber-crime, trafficking, and more — "
       "carried on singly or jointly.",
       "The section also reaches whoever facilitates it: a person who organises, assists or is a member of the "
       "syndicate. There is no IPC equivalent, and no case law under it yet."],
  ex="A group that runs a protection racket across three districts, extorting shopkeepers over two years, falls "
     "within s. 111 even if each individual act is also charged separately."),
 113: dict(
  why=["Terrorist act is new. It covers acts done with the intention of threatening the unity, integrity, "
       "sovereignty or security of India, or of striking terror in the people, by using bombs, firearms, "
       "hazardous substances or any other means.",
       "It overlaps with the UAPA but is a standalone offence under the general penal code, which means it can be "
       "investigated by ordinary police without the UAPA's procedural framework."],
  ex="A person plants an explosive device in a market with intent to strike terror. That is a terrorist act under "
     "s. 113, punishable with death or life where it results in death."),
 304: dict(
  why=["Snatching is new. It covers the sudden or forcible seizure of property from a person or their possession "
       "— the chain-snatching case that the IPC had to fit awkwardly into theft or robbery.",
       "The distinction from theft is the suddenness and the element of force or seizure; the distinction from "
       "robbery is that no force is used on the person in order to commit the taking."],
  ex="A motorcyclist grabs a woman's bag as he rides past, without her being able to resist. That is snatching "
     "under s. 304, not robbery."),
}

MAPPING = [
    ("302", "Murder", "103", "Punishment for murder", "Death or life; the death penalty is no longer mandatory."),
    ("300", "Murder — definition", "101", "Murder", "Sub-section (2) adds group murder on identity grounds."),
    ("299", "Culpable homicide", "100", "Culpable homicide", "Carried forward."),
    ("304", "Culpable homicide not amounting to murder", "105", "Punishment", "Two-part structure retained."),
    ("304A", "Death by negligence", "106", "Causing death by negligence", "Raised to five years; new sub-section (2) for fleeing the scene."),
    ("307", "Attempt to murder", "109", "Attempt to murder", "Carried forward."),
    ("309", "Attempt to suicide", "226", "Attempt to commit suicide", "Presumption of severe stress; rehabilitation instead of jail."),
    ("323", "Voluntarily causing hurt", "115", "Voluntarily causing hurt", "Community service available."),
    ("325", "Grievous hurt", "117", "Voluntarily causing grievous hurt", "Eight categories retained."),
    ("326A", "Acid attack", "124", "Hurt by acid attack", "Ten-year minimum retained."),
    ("354", "Assault on a woman", "74", "Assault on a woman", "Carried forward."),
    ("354A", "Sexual harassment", "75", "Sexual harassment", "Four clauses retained."),
    ("354D", "Stalking", "78", "Stalking", "Includes monitoring internet use."),
    ("363", "Kidnapping", "137", "Kidnapping", "Definition and punishment consolidated."),
    ("364A", "Kidnapping for ransom", "140", "Kidnapping for ransom", "Death or life retained."),
    ("370", "Trafficking", "143", "Trafficking of a person", "Graded by age and number of victims."),
    ("375", "Rape — definition", "63", "Rape", "Marital exception retained, keyed to the wife's age."),
    ("376", "Punishment for rape", "64", "Punishment for rape", "Ten years to life retained."),
    ("376D", "Gang rape", "70", "Gang rape", "Twenty years to life."),
    ("379", "Theft", "303", "Theft", "Community service for a first small-value conviction."),
    ("392", "Robbery", "309", "Robbery", "Carried forward."),
    ("395", "Dacoity", "310", "Dacoity", "Carried forward."),
    ("406", "Criminal breach of trust", "316", "Criminal breach of trust", "Carried forward."),
    ("411", "Receiving stolen property", "317", "Receiving stolen property", "Carried forward."),
    ("420", "Cheating", "318", "Cheating", "Punishment graded by value and consequence."),
    ("465", "Forgery", "336", "Forgery", "Carried forward."),
    ("498A", "Cruelty by husband or relatives", "85", "Cruelty", "Carried forward with the same explanation."),
    ("499/500", "Defamation", "356", "Defamation", "Community service added."),
    ("506", "Criminal intimidation", "351", "Criminal intimidation", "Graded punishment."),
    ("509", "Insult to modesty", "79", "Insult to the modesty of a woman", "Carried forward."),
    ("120B", "Criminal conspiracy", "61", "Criminal conspiracy", "Punishment graded by the object offence."),
    ("124A", "Sedition", "152", "Acts endangering sovereignty", "Recast; secession and armed rebellion added."),
    ("141", "Unlawful assembly", "189", "Unlawful assembly", "Five-person threshold retained."),
    ("147", "Rioting", "191", "Rioting", "Punishment moved to sub-section (2)."),
    ("153A", "Promoting enmity", "196", "Promoting enmity", "Language added to the protected grounds."),
    ("201", "Causing disappearance of evidence", "238", "Causing disappearance of evidence", "Carried forward."),
    ("96", "Private defence", "34", "Private defence", "Carried forward with ss. 35–44."),
]

NEW_OFFENCES = [
    ("111", "Organised crime", "Continuing unlawful activity by a crime syndicate — kidnapping, extortion, land grabbing, contract killing, financial fraud, trafficking, cyber-crime."),
    ("112", "Petty organised crime", "The smaller-scale counterpart: theft, snatching, cheating or unauthorised betting committed by a syndicate."),
    ("113", "Terrorist act", "A standalone offence of doing an act intended to threaten the unity, integrity, sovereignty or security of India."),
    ("101", "Group murder on identity grounds", "Section 101(2) covers murder by five or more on grounds of race, caste, community, sex, place of birth or language."),
    ("304", "Snatching", "Sudden seizure of movable property from a person or their possession."),
    ("69", "Sexual intercourse by deceitful means", "Obtaining intercourse by deceit or a false promise of marriage, where the act is not rape."),
]


def paras(text):
    t = re.sub(r"\s+", " ", text).strip()
    t = re.sub(r"(?<=[;:.,—])\s+(?:or\s+)?(?=\([a-z0-9]{1,3}\)\s)", "\n", t)
    t = re.sub(r"\s+(?=\([ivx]{1,4}\)\s)", "\n", t)
    t = re.sub(r"\s+(?=(Explanation|Illustration|Exception)\s?[0-9]?\.?—)", "\n", t)
    return [p.strip() for p in t.split("\n") if p.strip()]


def punishment(n):
    m = re.search(r"shall (?:also )?be punished with ([^.]{12,170})", BYN[n]["text"])
    if not m:
        return None
    s = re.sub(r"\s+", " ", m.group(1)).strip(" ,;")
    return s[0].upper() + s[1:]


def xrefs(n):
    txt = BYN[n]["text"]
    found = []
    for m in re.finditer(r"sections?\s+(\d{1,3})(?:\s*\(\d\))?", txt):
        k = int(m.group(1))
        if 1 <= k <= 358 and k != n and k not in found:
            found.append(k)
    return found[:8]


MARK = ('<svg class="brand__mark" viewBox="0 0 26 26" fill="none" aria-hidden="true">'
        '<rect x="1" y="1" width="24" height="24" rx="6" stroke="#1d5c4c" stroke-width="1.5"/>'
        '<path d="M7.5 8.5h11M7.5 13h11M7.5 17.5h7" stroke="#17150f" stroke-width="1.7" stroke-linecap="round"/></svg>')
I_SEARCH = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round"><circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/></svg>')
I_MENU = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
          'stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>')
I_X = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
       'stroke-width="1.9" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>')
I_ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
           'stroke-linecap="round"><path d="M5 12h13M12.5 6l6 6-6 6"/></svg>')


def sidebar(rel, active_ch=None, cur=None):
    if cur and active_ch:
        num, r, t, f, l, c, b = CHAPTERS[active_ch - 1]
        out = ['<p class="side__k" style="color:%s">Chapter %s &middot; %s</p>' % (c, r, E(t))]
        for s in SEC:
            if f <= s["n"] <= l:
                cls = ' aria-current="true"' if s["n"] == cur else ""
                out.append('<a class="side__a" href="%ssection/%d.html"%s><span class="mono" '
                           'style="color:%s">%d</span><span>%s</span></a>'
                           % (rel, s["n"], cls, c, s["n"], E(s["title"] or "Provision")))
        out.append('<a class="side__a" href="%schapters.html" style="margin-top:.8rem;color:var(--muted)">'
                   'All chapters</a>' % rel)
        return '<aside class="side">%s</aside>' % "".join(out)
    out = ['<p class="side__k">Chapters</p><div class="side__grp">']
    for n, r, t, f, l, c, b in CHAPTERS:
        cls = ' aria-current="true"' if n == active_ch else ""
        out.append('<a class="side__a" href="%schapter/%d.html"%s><span class="dot" style="background:%s">'
                   '</span><span>%s</span><small>%d</small></a>' % (rel, n, cls, c, E(t), l - f + 1))
    out.append('</div><p class="side__k">Reference</p><div class="side__grp">')
    for href, label in [("browse.html", "All sections"), ("mapping.html", "IPC to BNS"),
                        ("changes.html", "What changed"), ("about.html", "About")]:
        out.append('<a class="side__a" href="%s%s">%s</a>' % (rel, href, E(label)))
    out.append("</div>")
    return '<aside class="side">%s</aside>' % "".join(out)


def drawer(rel, active_ch=None):
    out = ['<p class="drawer__k">Chapters</p>']
    for n, r, t, f, l, c, b in CHAPTERS:
        cls = ' aria-current="true"' if n == active_ch else ""
        out.append('<a class="drawer__a" href="%schapter/%d.html"%s><span class="dot" style="background:%s">'
                   '</span><span>%s</span><span>%d–%d</span></a>' % (rel, n, cls, c, E(t), f, l))
    out.append('<p class="drawer__k">Reference</p>')
    for href, label in [("browse.html", "All sections"), ("mapping.html", "IPC to BNS"),
                        ("changes.html", "What changed"), ("about.html", "About")]:
        out.append('<a class="drawer__a" href="%s%s"><span>%s</span></a>' % (rel, href, E(label)))
    return "".join(out)


def page(path, title, desc, body, active="", side=True, ch=None, cur=None):
    rel = "../" * path.count("/")
    nav = "".join('<a href="%s%s"%s>%s</a>' % (rel, h, ' aria-current="true"' if h == active else "", l)
                  for h, l in [("index.html", "Home"), ("browse.html", "Sections"),
                               ("chapters.html", "Chapters"), ("mapping.html", "IPC to BNS"),
                               ("changes.html", "What changed")])
    shell = ('<div class="shell">%s<main class="content">' % sidebar(rel, ch, cur) if side
             else '<div class="shell" style="grid-template-columns:1fr"><main class="content">')
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="theme-color" content="#faf9f6">
<meta name="sa-base" content="%(rel)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<link rel="icon" href="%(rel)sassets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%(rel)sassets/css/app.css">
<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.0.0/dist/fuse.min.js" defer></script>
<script src="%(rel)sassets/js/app.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.1/dist/cdn.min.js" defer></script>
</head>
<body>
<header class="hdr">
  <div class="hdr__in">
    <button class="mbtn" id="menuBtn" aria-label="Open menu" x-data @click="$dispatch('toggle-drawer')">%(menu)s</button>
    <a class="brand" href="%(rel)sindex.html">%(mark)s<span class="brand__name">Sanhita Atlas</span>
      <span class="brand__sub">BNS 2023</span></a>
    <nav class="nav" aria-label="Primary">%(nav)s</nav>
    <div class="hdr__act">
      <button class="sbtn" x-data @click="$dispatch('open-search')" aria-label="Search">%(search)s
        <span>Search</span><kbd>/</kbd></button>
    </div>
  </div>
</header>

<div class="scrim" x-data @click="$dispatch('close-drawer')"></div>
<aside class="drawer" aria-label="Menu">
  <div class="drawer__top">
    <a class="brand" href="%(rel)sindex.html">%(mark)s<span class="brand__name">Sanhita Atlas</span></a>
    <button class="drawer__x" x-data @click="$dispatch('close-drawer')" aria-label="Close">%(x)s</button>
  </div>
  <div class="drawer__body">%(drawer)s</div>
</aside>

<div class="smodal" x-data="searchModal()" x-show="$store.ui.search" x-cloak
     @open-search.window="open()" @keydown.escape.window="close()">
  <div class="smodal__box" @click.outside="close()">
    <div class="smodal__in">%(search)s
      <input id="sq" type="search" placeholder="Search sections, offences, phrases" autocomplete="off"
             x-model="q" @input.debounce.100ms="q = $event.target.value; run()"
             @keydown.arrow-down.prevent="move(1)" @keydown.arrow-up.prevent="move(-1)"
             @keydown.enter.prevent="go()"><kbd>esc</kbd></div>
    <div class="smodal__res">
      <template x-if="!q"><p class="smodal__none">Search all 358 sections by number, title or a phrase from the text.</p></template>
      <template x-if="q && !results.length"><p class="smodal__none">No match. Try a section number or a shorter phrase.</p></template>
      <template x-for="(r,i) in results" :key="r.n">
        <a :href="base+r.url" :class="i===sel ? 'sel' : ''" @mouseenter="sel=i" @click="close()">
          <strong x-text="r.title"></strong><span x-text="r.context"></span></a>
      </template>
    </div>
    <div class="smodal__foot"><span>&uarr;&darr; move &middot; &crarr; open</span><span x-text="results.length + ' results'"></span></div>
  </div>
</div>

%(shell)s
%(body)s
</main></div>

<footer class="foot">
  <div class="foot__in">
    <span>Sanhita Atlas &middot; Bharatiya Nyaya Sanhita, 2023 (Act 45 of 2023)</span>
    <div class="foot__links">
      <a href="%(rel)sbrowse.html">All sections</a><a href="%(rel)schapters.html">Chapters</a>
      <a href="%(rel)smapping.html">IPC to BNS</a><a href="%(rel)sabout.html">About</a>
      <a href="https://www.indiacode.nic.in/" target="_blank" rel="noopener">India Code</a>
    </div>
    <span>Not legal advice &middot; verify against the Gazette</span>
  </div>
</footer>
<style>[x-cloak]{display:none!important}</style>
</body>
</html>""" % {"title": E(title), "desc": E(desc), "rel": rel, "nav": nav, "body": body,
              "mark": MARK, "menu": I_MENU, "search": I_SEARCH, "x": I_X,
              "drawer": drawer(rel, ch), "shell": shell}


def pager(prev, nxt):
    def cell(item, kind):
        if not item:
            return '<span class="pg pg--%s is-empty"></span>' % kind
        href, label, sub = item
        return ('<a class="pg pg--%s" href="%s"><span>%s</span><strong>%s</strong><small>%s</small></a>'
                % (kind, href, "Previous" if kind == "prev" else "Next", E(label), E(sub)))
    return '<nav class="pager">%s%s</nav>' % (cell(prev, "prev"), cell(nxt, "next"))


# ── pages ────────────────────────────────────────────────────────────────
def home():
    cards = "".join(
        '<a class="card" href="chapter/%d.html"><span class="card__k">'
        '<span class="dot" style="background:%s"></span>Chapter %s &middot; ss. %d–%d</span>'
        '<h3>%s</h3><p>%s</p></a>' % (n, c, r, f, l, E(t), E(b))
        for n, r, t, f, l, c, b in CHAPTERS[:6])
    featured = "".join(
        '<a class="card" href="section/%d.html"><span class="card__k">Section %d</span>'
        '<h3>%s</h3><p>%s</p></a>'
        % (n, n, E(BYN[n]["title"]), E(ANN[n]["why"][0][:120] + "…"))
        for n in (103, 85, 152))
    return """
<section class="hero">
  <div class="hero__in">
    <div>
      <p class="eyebrow">Bharatiya Nyaya Sanhita &middot; Act 45 of 2023</p>
      <h1>The penal code, <em>annotated</em>.</h1>
      <p class="hero__lede">All 358 sections of the BNS with the statutory text, an explanation of what each one
      does, a worked example, and the case law that still governs it.</p>
      <div class="hero__act">
        <a class="btn btn--primary" href="browse.html">Browse all 358 sections %s</a>
        <a class="btn btn--ghost" href="section/103.html">Start with s. 103</a>
      </div>
    </div>
    <aside class="hero__panel">
      <h4>The code at a glance</h4>
      <dl class="facts">
        <div><dt>358</dt><dd>sections</dd></div>
        <div><dt>20</dt><dd>chapters</dd></div>
        <div><dt>21</dt><dd>annotated in full</dd></div>
        <div><dt>37</dt><dd>IPC mappings</dd></div>
      </dl>
    </aside>
  </div>
</section>

<div class="wrap">
  <section class="sect">
    <div class="sect__head"><h2>Annotated sections</h2>
      <a class="sect__link" href="browse.html">See all sections</a></div>
    <div class="grid grid--3">%s</div>
  </section>

  <section class="sect">
    <div class="sect__head"><h2>Browse by chapter</h2>
      <a class="sect__link" href="chapters.html">All 20 chapters</a></div>
    <div class="grid grid--3">%s</div>
  </section>

  <section class="sect">
    <div class="callout">
      <h4>How to read this</h4>
      <p>Every section page carries the text of the provision. Twenty-one of them — the ones that carry the most
      weight in practice — also carry an explanation, a worked example and the leading cases. Those cases were
      decided under the Indian Penal Code, which the Sanhita replaced; they remain persuasive on the same
      language.</p>
    </div>
  </section>
</div>
""" % (I_ARROW, featured, cards)


def browse():
    rows = "".join(
        '<tr data-ch="%d" data-s="%s"><td class="sref">%d</td>'
        '<td><a href="section/%d.html">%s</a></td>'
        '<td class="mono" style="color:var(--muted)">%s</td>'
        '<td>%s</td></tr>'
        % (CHOF[s["n"]][0], E(("%d %s %s" % (s["n"], s["title"], s["text"][:300])).lower()),
           s["n"], s["n"], E(s["title"] or "—"),
           '<span class="dot" style="background:%s;display:inline-block;margin-right:.4rem"></span>%s'
           % (CHOF[s["n"]][3], CHOF[s["n"]][1]),
           '<span class="chip chip--accent" style="font-size:.62rem">Annotated</span>'
           if s["n"] in ANN else "")
        for s in SEC)
    opts = "".join('<option value="%d">Chapter %s — %s</option>' % (n, r, E(t))
                   for n, r, t, f, l, c, b in CHAPTERS)
    return ('<div class="crumbs"><a href="index.html">Home</a><i>/</i><em>Sections</em></div>'
            '<div class="phead"><h1>All 358 sections</h1>'
            '<p class="phead__lede">The complete Sanhita in order. Filter by chapter, or search by number, title '
            'or a phrase from the text.</p></div>'
            '<div x-data="tableFilter()" x-init="init()"><div class="toolbar">'
            '<div class="field">' + I_SEARCH +
            '<input type="search" placeholder="Search sections" x-model="q" '
            '@input="q = $event.target.value; filter()"></div>'
            '<div class="field" style="flex:0 1 280px"><select x-model="ch" '
            '@change="ch = $event.target.value; filter()"><option value="">All chapters</option>' + opts +
            '</select></div><span class="count" x-text="shown + \' of 358\'"></span></div>'
            '<div class="tw"><div class="tw__s"><table><thead><tr>'
            '<th style="width:70px">No.</th><th>Section</th><th style="width:60px">Ch.</th>'
            '<th style="width:110px"></th></tr></thead><tbody x-ref="body">' + rows + '</tbody></table>'
            '</div></div></div>')


def chapters():
    cards = "".join(
        '<a class="card" href="chapter/%d.html"><span class="card__k">'
        '<span class="dot" style="background:%s"></span>Chapter %s &middot; ss. %d–%d</span>'
        '<h3>%s</h3><p>%s</p></a>' % (n, c, r, f, l, E(t), E(b))
        for n, r, t, f, l, c, b in CHAPTERS)
    return ('<div class="crumbs"><a href="index.html">Home</a><i>/</i><em>Chapters</em></div>'
            '<div class="phead"><h1>The twenty chapters</h1>'
            '<p class="phead__lede">The Sanhita runs in one continuous sequence of 358 sections. These are the '
            'chapters those sections fall into.</p></div><div class="grid grid--2">%s</div>' % cards)


def chapter(n):
    num, r, t, f, l, c, b = CHAPTERS[n - 1]
    secs = [s for s in SEC if f <= s["n"] <= l]
    rows = "".join(
        '<tr><td class="sref">%d</td><td><a href="../section/%d.html">%s</a></td><td>%s</td></tr>'
        % (s["n"], s["n"], E(s["title"] or "—"),
           '<span class="chip chip--accent" style="font-size:.62rem">Annotated</span>'
           if s["n"] in ANN else "")
        for s in secs)
    prev = (("../chapter/%d.html" % (n - 1), "Chapter %s" % CHAPTERS[n - 2][1],
             CHAPTERS[n - 2][2]) if n > 1 else None)
    nxt = (("../chapter/%d.html" % (n + 1), "Chapter %s" % CHAPTERS[n][1],
            CHAPTERS[n][2]) if n < 20 else None)
    return ('<div class="crumbs"><a href="../index.html">Home</a><i>/</i>'
            '<a href="../chapters.html">Chapters</a><i>/</i><em>Chapter %s</em></div>' % r +
            '<div class="sec-head"><span class="sec-num" style="color:%s">%s</span>'
            '<span class="sec-chap">Chapter &middot; ss. %d–%d</span></div>' % (c, r, f, l) +
            '<h1 class="sec-title">%s</h1>' % E(t) +
            '<p class="phead__lede" style="margin-bottom:1.6rem">%s</p>' % E(b) +
            '<div class="pmeta"><span class="chip chip--mono">%d sections</span>'
            '<span class="chip">%d annotated</span></div>' % (len(secs), sum(1 for s in secs if s["n"] in ANN)) +
            '<div class="tw" style="margin-top:2rem"><div class="tw__s"><table><thead><tr>'
            '<th style="width:70px">No.</th><th>Section</th><th style="width:110px"></th></tr></thead>'
            '<tbody>%s</tbody></table></div></div>' % rows + pager(prev, nxt))


def section(n):
    s = BYN[n]
    chn, chr_, cht, col = CHOF[n]
    raw = re.sub(r"^%d\.\s*" % n, "", s["text"])
    body = "".join('<p>%s</p>' % E(p) for p in paras(raw))
    ann = ANN.get(n)
    pun = punishment(n)
    ipc = IPC.get(str(n))

    main = '<div class="statute">%s</div>' % body
    if ann:
        main += '<div class="block"><p class="block__k">What it means</p>%s</div>' % "".join(
            "<p>%s</p>" % E(p) for p in ann["why"])
        if ann.get("ex"):
            main += ('<div class="block"><p class="block__k">Worked example</p>'
                     '<div class="example"><span class="lbl">Illustration</span><p>%s</p></div></div>'
                     % E(ann["ex"]))
        if ann.get("cases"):
            main += ('<div class="block"><p class="block__k">Case law</p><div class="cases">%s</div></div>'
                     % "".join('<article class="case"><h4>%s</h4><span>%s</span><p>%s</p></article>'
                               % (E(a), E(b), E(c)) for a, b, c in ann["cases"]))

    rail = ['<div class="rail__box"><p class="rail__k">Provision</p><dl>']
    rail.append('<div><dt>Chapter</dt><dd><a href="../chapter/%d.html">%s — %s</a></dd></div>'
                % (chn, chr_, E(cht)))
    if ipc and ipc != "—":
        rail.append('<div><dt>IPC equivalent</dt><dd>Section %s</dd></div>' % ipc)
    elif ipc == "—":
        rail.append('<div><dt>IPC equivalent</dt><dd>None — new offence</dd></div>')
    if pun:
        rail.append('<div><dt>Punishment</dt><dd>%s</dd></div>' % E(pun))
    rail.append('<div><dt>Status</dt><dd>In force from 1 July 2024</dd></div></dl></div>')
    xs = xrefs(n)
    if xs:
        rail.append('<div class="rail__box"><p class="rail__k">Cross-references</p><ul class="xrefs">%s</ul></div>'
                    % "".join('<li><a href="../section/%d.html"><small>%d</small>%s</a></li>'
                              % (k, k, E(BYN[k]["title"] or "Provision")) for k in xs))
    rail.append('<div class="rail__box"><p class="rail__k">In this chapter</p><ul class="xrefs">%s</ul></div>'
                % "".join('<li><a href="../section/%d.html"><small>%d</small>%s</a></li>'
                          % (k, k, E(BYN[k]["title"] or "Provision"))
                          for k in range(max(1, n - 2), min(359, n + 3)) if k != n))

    prev = (("../section/%d.html" % (n - 1), "Section %d" % (n - 1), BYN[n - 1]["title"]) if n > 1 else None)
    nxt = (("../section/%d.html" % (n + 1), "Section %d" % (n + 1), BYN[n + 1]["title"]) if n < 358 else None)

    return ('<div class="crumbs"><a href="../index.html">Home</a><i>/</i>'
            '<a href="../chapter/%d.html">Chapter %s</a><i>/</i><em>Section %d</em></div>' % (chn, chr_, n) +
            '<div class="sec-head"><span class="sec-num" style="color:%s">%d</span>'
            '<span class="sec-chap" style="color:%s">Chapter %s</span></div>' % (col, n, col, chr_) +
            '<h1 class="sec-title">%s</h1>' % E(s["title"] or "Provision") +
            '<div class="pmeta"><span class="chip chip--mono">Section %d</span>' % n +
            ('<span class="chip chip--accent">Annotated</span>' if ann else '') +
            ('<span class="chip">IPC %s</span>' % ipc if ipc and ipc != "—" else '') +
            '<span class="chip">In force 1 Jul 2024</span></div>' +
            '<div class="split" style="margin-top:2.2rem"><div>%s</div><aside>%s</aside></div>' % (
                main, "".join(rail)) +
            '<div class="note"><p>Text extracted from the Gazette notification of 25 December 2023 and '
            'reformatted for reading. Check the official copy before relying on it.</p></div>' +
            pager(prev, nxt))


def mapping():
    rows = "".join(
        '<tr data-s="%s"><td class="mono">%s</td><td>%s</td><td class="sref">%s</td>'
        '<td><a href="section/%s.html">%s</a></td><td style="color:var(--muted)">%s</td></tr>'
        % (E(("%s %s %s %s" % (a, at, b, bt)).lower()), E(a), E(at), E(b), b, E(bt), E(note))
        for a, at, b, bt, note in MAPPING)
    return ('<div class="crumbs"><a href="index.html">Home</a><i>/</i><em>IPC to BNS</em></div>'
            '<div class="phead"><h1>IPC to BNS</h1><p class="phead__lede">The provisions most often looked up, and '
            'where each one landed. Where a provision was substantively rewritten, the note says so rather than '
            'implying equivalence.</p></div>'
            '<div x-data="tableFilter()" x-init="init()"><div class="toolbar">'
            '<div class="field">' + I_SEARCH +
            '<input type="search" placeholder="Search an IPC or BNS section" x-model="q" '
            '@input="q = $event.target.value; filter()"></div>'
            '<span class="count" x-text="shown + \' of %d\'"></span></div>' % len(MAPPING) +
            '<div class="tw"><div class="tw__s"><table><thead><tr>'
            '<th style="width:80px">IPC</th><th style="width:220px">Offence</th><th style="width:70px">BNS</th>'
            '<th style="width:220px">Provision</th><th>Note</th></tr></thead><tbody x-ref="body">' + rows +
            '</tbody></table></div></div></div>'
            '<div class="note"><p>Selected correspondences, not a complete concordance.</p></div>')


def changes():
    cards = "".join(
        '<a class="card" href="section/%s.html"><span class="card__k">Section %s</span><h3>%s</h3>'
        '<p>%s</p></a>' % (s.split("(")[0], E(s), E(t), E(d)) for s, t, d in NEW_OFFENCES)
    return ('<div class="crumbs"><a href="index.html">Home</a><i>/</i><em>What changed</em></div>'
            '<div class="phead"><h1>What changed on 1 July 2024</h1>'
            '<p class="phead__lede">The Sanhita is not a rewrite of the IPC so much as a renumbering with '
            'deliberate changes layered on top. These are the ones that alter outcomes.</p></div>'
            '<div class="grid grid--2">' + cards + '</div>'
            '<div class="note"><p>Twenty offences were added, nineteen provisions dropped, punishments raised for '
            'thirty-three offences and fines for eighty-three.</p></div>')


def about():
    return ('<div class="crumbs"><a href="index.html">Home</a><i>/</i><em>About</em></div>'
            '<div class="phead"><h1>About Sanhita Atlas</h1></div>'
            '<div class="block"><p>A reference to the Bharatiya Nyaya Sanhita, 2023 — the code that replaced the '
            'Indian Penal Code on 1 July 2024. Every section number moved, and the Act is easier to read one '
            'provision at a time than as a hundred-page PDF.</p>'
            '<p>The text of all 358 sections was extracted from the Gazette notification of 25 December 2023. '
            'Chapter boundaries, section titles and the IPC correspondence were checked against the published '
            'comparative tables. Twenty-one sections carry a written explanation, a worked example and the leading '
            'cases.</p>'
            '<p>It is independent, unaffiliated with the Government of India or any court, and not legal advice.</p>'
            '</div>'
            '<div class="grid grid--3">'
            '<div class="card"><span class="card__k">Text</span><h3>From the Gazette</h3>'
            '<p>Parsed from the 102-page notification, section by section, not copied from commentary.</p></div>'
            '<div class="card"><span class="card__k">Case law</span><h3>IPC-era authority</h3>'
            '<p>The cases were decided under the IPC. They remain persuasive where the Sanhita kept the same '
            'language — and are marked as such.</p></div>'
            '<div class="card"><span class="card__k">Stack</span><h3>Static, searchable</h3>'
            '<p>Alpine.js for the drawer, search and filters; Fuse.js for full-text search. No tracking.</p></div>'
            '</div>')


def notfound():
    return ('<div style="padding:5rem 0;text-align:center">'
            '<p class="eyebrow" style="justify-content:center">Error 404</p>'
            '<h1 style="margin-bottom:.6rem">That page is not in the code</h1>'
            '<p style="color:var(--muted);margin-bottom:1.6rem">Sections run from 1 to 358, and chapters from '
            'I to XX.</p><a class="btn btn--primary" href="index.html">Back to the overview</a></div>')


def search_index():
    return [{"n": s["n"], "url": "section/%d.html" % s["n"],
             "title": "Section %d — %s" % (s["n"], s["title"] or "Provision"),
             "context": "Chapter %s · %s" % (CHOF[s["n"]][1], CHOF[s["n"]][2]),
             "text": s["text"][:900]} for s in SEC]


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    for d in ("assets/css", "assets/js", "assets/img", "assets/data", "section", "chapter"):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)

    for path, title, desc, body, active, side in [
        ("index.html", "Sanhita Atlas — the annotated Bharatiya Nyaya Sanhita, 2023",
         "All 358 sections of the BNS with the statutory text, explanations, worked examples and case law.",
         home(), "", False),
        ("browse.html", "All 358 sections — Sanhita Atlas", "Browse every section of the BNS.",
         browse(), "browse.html", True),
        ("chapters.html", "The twenty chapters — Sanhita Atlas", "The twenty chapters and their ranges.",
         chapters(), "chapters.html", True),
        ("mapping.html", "IPC to BNS — Sanhita Atlas", "Section correspondence between the IPC and the BNS.",
         mapping(), "mapping.html", True),
        ("changes.html", "What changed — Sanhita Atlas", "The offences and penalties that changed.",
         changes(), "changes.html", True),
        ("about.html", "About — Sanhita Atlas", "About the reference.", about(), "about.html", True)]:
        with open(os.path.join(OUT, path), "w", encoding="utf-8") as f:
            f.write(page(path, title, desc, body, active, side=side))

    for n in range(1, 21):
        p = "chapter/%d.html" % n
        with open(os.path.join(OUT, p), "w", encoding="utf-8") as f:
            f.write(page(p, "Chapter %s — %s" % (CHAPTERS[n - 1][1], CHAPTERS[n - 1][2]),
                         CHAPTERS[n - 1][6], chapter(n), "", True, n))
    for s in SEC:
        n = s["n"]
        p = "section/%d.html" % n
        with open(os.path.join(OUT, p), "w", encoding="utf-8") as f:
            f.write(page(p, "Section %d — %s" % (n, s["title"] or "BNS"),
                         s["text"][:150] + "…", section(n), "", True, CHOF[n][0], n))

    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(page("404.html", "Page not found — Sanhita Atlas", "Not found.", notfound(), "", False))
    with open(os.path.join(OUT, "assets/data/search.json"), "w", encoding="utf-8") as f:
        json.dump(search_index(), f, ensure_ascii=False, separators=(",", ":"))
    for src, dst in [("src/app.js", "assets/js/app.js"), ("src/app.css", "assets/css/app.css"),
                     ("src/favicon.svg", "assets/img/favicon.svg"), ("README.md", "README.md")]:
        if os.path.exists(os.path.join(HERE, src)):
            shutil.copy(os.path.join(HERE, src), os.path.join(OUT, dst))
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print("pages:", 6 + 20 + 358 + 1, "| annotated:", len(ANN))


if __name__ == "__main__":
    main()
