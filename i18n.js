/* ===== i18n System ===== */
const I18N_TRANSLATIONS = {
  "de": {
    "skip": { "to_content": "Zum Inhalt springen" },
    "hero": {
      "role": "M.Ed. · Wissenschaftlicher Mitarbeiter · Empirische Politikdidaktik",
      "bio": "Ich erforsche, wie kooperative und kompetitive Diskussionsformate die politische Urteilsbildung im Politikunterricht beeinflussen – videobasiert und quasi-experimentell.",
      "affiliation": "Technische Universität Dortmund",
      "affiliation2": "Institut für Didaktik integrativer Fächer · Didaktik der Sozialwissenschaften"
    },
    "links": {
      "tu_href": "https://idif.sowi.tu-dortmund.de/professuren/didaktik-der-sozialwissenschaften/lukas-brandt/",
      "tu_title": "Profil an der TU Dortmund",
      "tu_sub": "Vita, Forschung, Publikationen und Vorträge",
      "orcid_sub": "Werke und Forschungsnachweis",
      "rg_sub": "Publikationen und fachlicher Austausch",
      "li_sub": "Beruflicher Werdegang",
      "mail_title": "E-Mail",
      "mail_href": "mailto:lukas.brandt@tu-dortmund.de"
    },
    "footer": {
      "impress": "Impressum",
      "privacy": "Datenschutz"
    },
    "lang": { "toggle": "EN" }
  },
  "en": {
    "skip": { "to_content": "Skip to content" },
    "hero": {
      "role": "M.Ed. · Research Associate · Empirical Civic Education",
      "bio": "I study how cooperative and competitive discussion formats shape political judgement in civic education – video-based and quasi-experimental.",
      "affiliation": "TU Dortmund University",
      "affiliation2": "Institute for Interdisciplinary Didactics · Didactics of Social Sciences"
    },
    "links": {
      "tu_href": "https://idif.sowi.tu-dortmund.de/en/professorships/didactics-of-social-sciences/lukas-brandt/",
      "tu_title": "Profile at TU Dortmund University",
      "tu_sub": "CV, research, publications and talks",
      "orcid_sub": "Works and research record",
      "rg_sub": "Publications and academic exchange",
      "li_sub": "Professional background",
      "mail_title": "Email",
      "mail_href": "mailto:lukas.brandt@tu-dortmund.de"
    },
    "footer": {
      "impress": "Legal Notice",
      "privacy": "Privacy"
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
