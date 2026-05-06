/* ===== i18n System ===== */
const I18N_TRANSLATIONS = {
  "de": {
    "nav": { "about": "Über", "research": "Forschung", "publications": "Publikationen", "contact": "Kontakt" },
    "hero": {
      "name": "Simon Filler",
      "role": "M.Ed. · Promovend Empirische Politikdidaktik",
      "bio": "Unterrichtsforschung, KI in Forschung und Lehre, Politikdidaktik.",
      "affiliation": "Technische Universität Dortmund",
      "affiliation2": "Didaktik der Sozialwissenschaften",
      "cta_primary": "Schreib mir",
      "cta_secondary": "Forschung ansehen"
    },
    "meta": {
      "period": "Zeitraum",
      "role": "Rolle",
      "year_now": "heute"
    },
    "roles": {
      "comenedes": "Mitarbeiter",
      "diss": "Promotionsstudent",
      "talktrace": "Entwickler",
      "lars": "Koordination"
    },
    "research": {
      "label": "Forschung",
      "title": "Projekte",
      "subtitle": "Dissertation, Projektbeteiligung und aktuelle Arbeiten.",
      "comenedes_tag": "Projekt",
      "comenedes_status": "Aktiv",
      "comenedes_title": "ComeNEDeS",
      "comenedes_body": "Das Projekt ComeNEDeS_NRW entwickelt phasenübergreifende Kooperationsstrukturen zwischen Hochschulen und dem staatlichen Lehrerfortbildungssystem in NRW. Im Teilprojekt „Demokratie“ an der TU Dortmund werden Fortbildungskonzepte für Lehrkräfte der Sozialwissenschaften, Wirtschaft-Politik und Gesellschaftslehre systematisiert und erprobt.",
      "comenedes_link1": "Mehr erfahren",
      "comenedes_link2": "Teilprojekt Demokratie",
      "diss_tag": "Dissertationsprojekt",
      "diss_status": "Aktiv",
      "diss_title": "Wahlen im Fokus",
      "diss_body": "Entwicklung und Erprobung von Kooperationsskripten im Politikunterricht. Fokus auf kognitive Aktivierung und politische Urteilsbildung bei Schüler*innen der 8. Jahrgangsstufe. Mixed-Methods-Design mit Wissenstests, Kleingruppen-Videographie und Arbeitsheften.",
      "diss_link": "Mehr erfahren",
      "talktrace_tag": "Software",
      "talktrace_status": "Aktiv",
      "talktrace_title": "TalkTrace AI base",
      "talktrace_body": "Software zur Analyse verbaler Interaktionen. Sie basiert auf Shiny für Python und nutzt Large Language Models, um quantitative Metriken und qualitative Kodierungen von transkribierten Dialogen zu erstellen und als strukturierte Berichte zu exportieren.",
      "talktrace_dev": "(in Entwicklung)",
      "lars_tag": "OER-Projekt",
      "lars_status": "Beendet",
      "lars_title": "LArS.nrw",
      "lars_body": "Lernen mit Animationsfilmen realer Unterrichtsszenen. Im Projekt entstanden 24 Animationsfilme (3–6 Min.), Comics und umfangreiche Materialien für die universitäre Lehramtsbildung. Reale Videos zeigen typische Interaktionen und fördern professionelle Wahrnehmungsfähigkeiten.",
      "lars_link1": "Mehr erfahren",
      "lars_link2": "Projektwebsite"
    },
    "publications": {
      "label": "Publikationen",
      "title": "Ausgewählte Beiträge",
      "subtitle": "Zeitschriftenartikel und Tagungsbeiträge.",
      "pub1_title": "Vorstellung LArS-Modul A: Einstiegsphase",
      "pub1_venue": "In: Gronostay, D., Manzel, S., Hahn-Laudenberg, K., Teuwsen, J. (Hrsg.) Professionelle Unterrichtswahrnehmung im sozialwissenschaftlichen Fachunterricht. Politische Bildung. Springer VS, Wiesbaden.",
      "pub2_venue": "Preprint, Zenodo.",
      "pub3_venue": "Preprint, Zenodo.",
      "doi": "DOI"
    },
    "contact": {
      "label": "Kontakt",
      "title": "Schreib mir",
      "lead": "Für Forschungsfragen, Kooperationen oder einfach Hallo sagen.",
      "social_orcid": "ORCID",
      "social_researchgate": "ResearchGate",
      "social_linkedin": "LinkedIn",
      "social_instagram": "Instagram"
    },
    "footer": {
      "rabbit_text": "Coaching · Mentoring · Beratung",
      "impress": "Impressum"
    },
    "matrix": {
      "quote": "\"Wie schon der große Philosoph Mick Jagger sagte: 'You can't always get what you want.'\" — Dr. House",
      "about_label": "Über mich",
      "about_body": "Ich tüftle gern an Dingen rum, an Problemen, Systemen, Plänen. Hängen bleibe ich an Technik, Japan, Anime, Theologie und Vibecoding. Also Sachen bauen, die funktionieren und sich gut anfühlen. Manchmal klappt das auf Anhieb, manchmal endet's in drei Stunden Stack Overflow.",
      "mentoring_label": "Mentoring",
      "mentoring_body1": "Begleitung bei Hausarbeiten, Bachelor- oder Masterthesis, von der ersten Panik vor der Themenwahl bis zum Abgabe-Knopf.",
      "mentoring_body2": "Schwerpunkt: dass der Prozess sich nicht wie Strafarbeit anfühlt und du am Ende sagen kannst „das hab ich geschrieben\". KI darf mitspielen, aber so, dass dein:e Prof beim Lesen nicht nervös wird.",
      "coaching_label": "Coaching",
      "coaching_body1": "Seit Jahren regelmäßig im Gym, Schwerpunkt schweres Krafttraining im Powerlifting-Stil. Ich helf dir, einen Plan zu finden, der zu dir passt, dabei sauber zu heben (Knie nicht nach innen, Rücken keine Banane) und nicht alle zwei Wochen das System zu wechseln, weil auf Instagram was Neues kursiert.",
      "coaching_body2": "Plus: Essen, das deinen Trainingseinsatz nicht sabotiert. Ziel ist nicht, sich täglich selbst zu besiegen, das verliert man meistens. Ziel ist, dranzubleiben.",
      "advice_label": "Beratung",
      "advice_body1": "Hilfe bei den Sachen, bei denen man als Erwachsene:r angeblich eigenständig durchblickt: ETF oder lieber nicht? Welches Handy? Lohnt sich der Stromanbieter-Wechsel?",
      "advice_body2": "Statt fertiger Antworten zeig ich dir, wo ich nachgeguckt hätte und worauf zu achten ist, damit du beim nächsten Mal nicht wieder fragen musst.",
      "status_label": "Status:",
      "status_note": "aktuell keine Slots verfügbar"
    },
    "lang": { "toggle": "EN" }
  },
  "en": {
    "nav": { "about": "About", "research": "Research", "publications": "Publications", "contact": "Contact" },
    "hero": {
      "name": "Simon Filler",
      "role": "M.Ed. · PhD Candidate Empirical Civic Education",
      "bio": "Educational research, AI in research and teaching, civic education.",
      "affiliation": "TU Dortmund University",
      "affiliation2": "Social Science Education",
      "cta_primary": "Get in touch",
      "cta_secondary": "View research"
    },
    "meta": {
      "period": "Period",
      "role": "Role",
      "year_now": "present"
    },
    "roles": {
      "comenedes": "Staff Member",
      "diss": "PhD Student",
      "talktrace": "Developer",
      "lars": "Coordination"
    },
    "research": {
      "label": "Research",
      "title": "Projects",
      "subtitle": "Dissertation, project participation and current work.",
      "comenedes_tag": "Project",
      "comenedes_status": "Active",
      "comenedes_title": "ComeNEDeS",
      "comenedes_body": "The ComeNEDeS_NRW project develops cross-phase cooperation structures between universities and the state teacher education system in North Rhine-Westphalia. In the 'Democracy' sub-project at TU Dortmund, training concepts for teachers of social sciences, economics-politics and social studies are systematised and tested.",
      "comenedes_link1": "Learn more",
      "comenedes_link2": "Sub-project Democracy",
      "diss_tag": "Dissertation Project",
      "diss_status": "Active",
      "diss_title": "Focus on Elections",
      "diss_body": "Development and testing of cooperation scripts in civic education. Focus on cognitive activation and political reasoning in 8th-grade students. Mixed-methods design with knowledge tests, small-group videography and workbooks.",
      "diss_link": "Learn more",
      "talktrace_tag": "Software",
      "talktrace_status": "Active",
      "talktrace_title": "TalkTrace AI base",
      "talktrace_body": "Software for analysing verbal interactions. Based on Shiny for Python, it uses Large Language Models to generate quantitative metrics and qualitative codings from transcribed dialogues and export them as structured reports.",
      "talktrace_dev": "(under development)",
      "lars_tag": "OER Project",
      "lars_status": "Completed",
      "lars_title": "LArS.nrw",
      "lars_body": "Learning with animation films of real classroom scenes. The project produced 24 animation films (3–6 min), comics and extensive materials for university teacher education. Real videos show typical interactions and promote professional perception skills.",
      "lars_link1": "Learn more",
      "lars_link2": "Project website"
    },
    "publications": {
      "label": "Publications",
      "title": "Selected Contributions",
      "subtitle": "Journal articles and conference papers.",
      "pub1_title": "Vorstellung LArS-Modul A: Einstiegsphase",
      "pub1_venue": "Gronostay, D., Manzel, S., Hahn-Laudenberg, K., Teuwsen, J. (Hrsg.)",
      "pub2_venue": "Preprint, Zenodo.",
      "pub3_venue": "Preprint, Zenodo.",
      "doi": "DOI"
    },
    "contact": {
      "label": "Contact",
      "title": "Get in touch",
      "lead": "For research questions, collaborations or just saying hello.",
      "social_orcid": "ORCID",
      "social_researchgate": "ResearchGate",
      "social_linkedin": "LinkedIn",
      "social_instagram": "Instagram"
    },
    "footer": {
      "rabbit_text": "Coaching · Mentoring · Consulting",
      "impress": "Legal Notice"
    },
    "matrix": {
      "quote": "\"As the great philosopher Mick Jagger said: 'You can't always get what you want.'\" — Dr. House",
      "about_label": "About me",
      "about_body": "I like tinkering with things, problems, systems, plans. I get stuck on tech, Japan, anime, theology and vibecoding. Building stuff that works and feels right. Sometimes it clicks on the first try, sometimes it ends in three hours of Stack Overflow.",
      "mentoring_label": "Mentoring",
      "mentoring_body1": "Support for term papers, bachelor's or master's theses, from the first panic about picking a topic all the way to clicking submit.",
      "mentoring_body2": "The focus: making sure the process doesn't feel like detention and you can honestly say at the end 'I wrote this'. AI can play along, but in a way that doesn't make your professor nervous while reading.",
      "coaching_label": "Coaching",
      "coaching_body1": "I've been in the gym regularly for years, focused on heavy strength training in a powerlifting style. I'll help you find a plan that fits you, lift cleanly (knees out, back not bent like a banana) and not switch your whole system every two weeks because something new is trending on Instagram.",
      "coaching_body2": "Plus: food that doesn't sabotage all the work you put in. The goal isn't to beat yourself daily, you mostly lose that fight. The goal is to keep showing up.",
      "advice_label": "Advice",
      "advice_body1": "Help with the stuff you're supposedly meant to figure out on your own as an adult: ETF or maybe not? Which phone? Is switching power supplier actually worth it?",
      "advice_body2": "Instead of finished answers I'll show you where I would have looked and what to watch out for, so next time you won't have to ask again.",
      "status_label": "Status:",
      "status_note": "currently no slots available"
    },
    "lang": { "toggle": "DE" }
  }
};

const I18N = {
  currentLang: 'de',
  data: I18N_TRANSLATIONS,

  init() {
    const saved = localStorage.getItem('lang');
    const browserLang = navigator.language.slice(0,2);
    const preferred = saved || (this.data[browserLang] ? browserLang : 'de');
    this.setLang(preferred, false);

    document.querySelectorAll('[data-lang-toggle]').forEach(btn => {
      btn.addEventListener('click', () => {
        const target = this.currentLang === 'de' ? 'en' : 'de';
        this.setLang(target, true);
      });
    });
  },

  setLang(lang, save=true) {
    if (!this.data[lang]) return;
    this.currentLang = lang;
    if (save) localStorage.setItem('lang', lang);

    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.dataset.i18n;
      const text = this.get(key);
      if (text !== undefined) {
        if (el.hasAttribute('data-i18n-attr')) {
          const attr = el.dataset.i18nAttr;
          el.setAttribute(attr, text);
        } else {
          el.textContent = text;
        }
      }
    });

    document.querySelectorAll('[data-lang-toggle]').forEach(btn => {
      btn.textContent = this.get('lang.toggle');
    });

    document.documentElement.setAttribute('lang', lang === 'de' ? 'de' : 'en');
  },

  get(key) {
    const parts = key.split('.');
    let obj = this.data[this.currentLang];
    for (const p of parts) {
      if (!obj) return undefined;
      obj = obj[p];
    }
    return obj;
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => I18N.init());
} else {
  I18N.init();
}
