# KájovoMail — forenzní explicitní zadání pro AI generování programu

## 1. Účel dokumentu

Tento dokument je závazné technické zadání pro vygenerování kompletního produktu **KájovoMail**. Je určen pro AI generátor kódu i pro lidské vývojáře. Cílem je vygenerovat funkční, testovatelný a nasaditelný software, nikoli pouze návrh, pseudokód, wireframe nebo dílčí ukázku.

KájovoMail je multiplatformní e-mailový klient s centrálním serverovým jádrem, webovou aplikací, desktopovou aplikací pro Windows a macOS a nativní Android aplikací. Součástí produktu je serverová integrace s OpenAI pro generování e-mailových odpovědí.

## 2. Priorita zdrojů a rozhodovací pravidla

### 2.1 Priorita dokumentů

Při generování repozitáře a aplikací platí tato priorita:

1. **`/ManifestDesignKájovo.md`**  
   Jediný závazný zdroj pravdy pro značku, signaci, logo, barvy, layout brand prvků, tokeny, motion, UI brand integraci a release gate pro brand.

2. **Tento dokument `KájovoMailZadání.md`**  
   Závazný zdroj pravdy pro architekturu, funkční požadavky, repozitář, build, testy, API, bezpečnost, chování aplikace a akceptační kritéria.

3. **Původní obchodní zadání `KajovoMail.txt`**  
   Zdroj původního uživatelského záměru a produktové logiky.

### 2.2 Řešení konfliktů

- Pokud vznikne konflikt v oblasti značky, UI brandingu nebo loga, má absolutní přednost `ManifestDesignKájovo.md`.
- Pokud vznikne konflikt v technické implementaci, má přednost tento dokument.
- Pokud některá věc není výslovně popsána, AI generátor musí zvolit konzervativní, bezpečné a testovatelné řešení, které neporuší manifest ani tento dokument.
- AI generátor nesmí doplňovat vlastní alternativní brand pravidla, vlastní logo, vlastní barevný systém mimo manifest ani „dočasné“ placeholder řešení.

## 3. Nevyjednatelné zásady produktu

### 3.1 Centrální serverové jádro

Celé řešení musí být postaveno tak, že:

- veškerá komunikace s OpenAI probíhá **výhradně na serveru**,
- veškeré sdílené nastavení uživatele se ukládá **na serveru**,
- práce s e-mailovými účty, složkami a odesíláním probíhá přes serverové API,
- desktop, web a Android jsou klienti jednoho centrálního systému.

### 3.2 Žádná perzistentní lokální databáze e-mailů na klientech

Na desktopu ani na Androidu nesmí vznikat perzistentní lokální databáze e-mailového obsahu. Je povoleno pouze:

- krátkodobé uložení v paměti RAM,
- dočasné cache soubory pro technické potřeby,
- bezpečné uložení autentizačního tokenu nebo session klíče v systémovém secure storage.

Zakázáno je:

- lokálně držet vlastní trvalou kopii mailboxu,
- vytvářet lokální index celé pošty jako autoritativní zdroj dat,
- provádět lokální „odpojenou“ správu složek jako primární režim.

### 3.3 Autoritativní zdroj pošty

Autoritativním zdrojem e-mailových zpráv a složek je vzdálený poštovní server.

- **IMAP + SMTP** je plnohodnotný režim.
- **POP3 + SMTP** je pouze omezený kompatibilní režim.

### 3.4 Omezení protokolu POP3

Protože POP3 nepodporuje plnohodnotnou obousměrnou synchronizaci a serverový model složek, musí být v implementaci výslovně rozlišeno:

- **IMAP účet** = plná podpora složek, serverových přesunů, stavů zpráv, vyhledávání a synchronizace.
- **POP3 účet** = omezený režim bez plné parity funkcí.

V režimu POP3 je povinné zobrazit uživateli upozornění, že následující funkce nemusí být dostupné nebo nebudou mít stejnou spolehlivost jako u IMAP:

- serverová správa složek,
- přesuny mezi serverovými složkami,
- synchronizace stavů přečteno / nepřečteno,
- serverové vyhledávání napříč složkami,
- Outlook-like workflow parity.

## 4. Povinný výsledný produkt

Musí vzniknout kompletní řešení obsahující:

1. **backend / serverové jádro**
2. **webovou aplikaci pro `mail.hcas.cz`**
3. **desktop aplikaci pro Windows a macOS**
4. **nativní Android aplikaci**
5. **automatizované testy**
6. **CI/CD pipeline**
7. **repozitář s připravenou strukturou pro brand assety dle manifestu**
8. **dokumentaci**
9. **forenzní audit Outlook workflow před implementací**
10. **forenzní audit MIME kompatibility a renderingu e-mailu**
11. **forenzní audit OpenAI orchestrace a bezpečnostní integrace**
12. **nasaditelný build**

AI generátor nesmí dodat pouze jednu část systému. Požadováno je celé řešení.

## 5. Povinná struktura repozitáře

Repozitář musí být vytvořen jako monorepo minimálně v této struktuře:

```text
/
├─ ManifestDesignKájovo.md
├─ KájovoMailZadání.md
├─ signace/
│  ├─ signace.svg
│  ├─ signace.pdf
│  └─ signace.png
├─ apps/
│  └─ kajovo-mail/
│     ├─ brand/
│     │  └─ brand.json
│     ├─ logo/
│     │  ├─ sources/
│     │  │  └─ logo_master.svg
│     │  └─ exports/
│     │     ├─ full/
│     │     ├─ mark/
│     │     ├─ wordmark/
│     │     └─ signace/
│     ├─ palette/
│     │  └─ palette.json
│     ├─ ui-tokens/
│     │  └─ tokens.json
│     ├─ ui-motion/
│     │  └─ motion.json
│     └─ ux/
│        └─ ia.json
├─ backend/
├─ web/
├─ desktop/
├─ android/
├─ docs/
│  ├─ forensic-audit/
│  │  ├─ outlook-mail-workflows.md
│  │  ├─ mime-email-compatibility.md
│  │  └─ openai-orchestration-and-security.md
│  ├─ architecture.md
│  ├─ api/
│  │  └─ openapi.yaml
│  ├─ security.md
│  ├─ deployment.md
│  └─ test-matrix.md
├─ infra/
├─ scripts/
└─ .github/workflows/
```

### 5.1 Brand assety a logo

- Repozitář musí obsahovat strukturu požadovanou manifestem.
- Pokud finální logo ještě není fyzicky dodáno, AI **nesmí vymyslet náhradní logo**.
- AI musí připravit repozitář a validační skripty tak, aby šlo finální logo vložit později do správné struktury.
- Produkční release musí být blokován, pokud chybí povinné assety definované manifestem.

## 6. Povinný technologický stack

Tento stack je závazný, pokud není objektivní technický důvod ho změnit. Změna musí být zdůvodněna v ADR dokumentu.

### 6.1 Backend

- Jazyk: **Python 3.12+**
- API framework: **FastAPI**
- Databáze: **PostgreSQL**
- Cache / queue: **Redis**
- Asynchronní úlohy: worker procesy pro synchronizaci pošty, odesílání a OpenAI operace
- Reverzní proxy: **Nginx** nebo ekvivalent
- Kontejnerizace: **Docker / Docker Compose**

### 6.2 Web

- Frontend: **React + TypeScript**
- Build: moderní SPA nebo SSR podle zvoleného návrhu, ale se zachováním plné parity funkcí
- Komunikace pouze se serverovým API
- Žádná přímá komunikace s IMAP/SMTP ani OpenAI z prohlížeče

### 6.3 Desktop

- Jazyk: **Python**
- UI framework: **PySide6 / Qt 6**
- Desktop aplikace musí být skutečná desktopová aplikace, ne zabalený webview shell
- Build výstupy:
  - Windows: instalační balíček
  - macOS: spustitelná aplikace / balíček

### 6.4 Android

- Jazyk: **Kotlin**
- UI: **Jetpack Compose**
- Aplikace musí být **nativní**
- Nesmí být postavená jako WebView wrapper
- Musí používat stejné serverové API jako web a desktop

## 7. Povinná architektura systému

## 7.1 Doménový model

Systém musí minimálně obsahovat tyto doménové entity:

- User
- AuthSession
- EmailAccount
- EmailFolder
- EmailMessage
- EmailThread
- EmailDraft
- AttachmentMeta
- AIPromptProfile
- AIContextBlock
- OfferTag
- OfferState
- UserPreferences
- AuditLog
- OpenAIRequestLog

### 7.2 Serverové služby

Server musí být rozdělen minimálně na tyto logické služby / moduly:

1. **Auth service**
2. **Email account service**
3. **IMAP/POP/SMTP connector service**
4. **Mail synchronization service**
5. **Folder service**
6. **Message service**
7. **Search service**
8. **Draft service**
9. **AI orchestration service**
10. **Email send service**
11. **Offer / tag service**
12. **Settings synchronization service**
13. **Audit and logging service**

### 7.3 Komunikační model

Klienti komunikují výhradně přes serverové API:

- REST API pro CRUD operace a načítání dat
- WebSocket / server push pro změny stavu:
  - nové zprávy,
  - změna složek,
  - dokončení AI generování,
  - změna tagů nabídek,
  - stav synchronizace.

## 8. Povinný forenzní audit Outlook workflow před implementací

Před samotnou implementací musí AI generátor vytvořit dokument:

`docs/forensic-audit/outlook-mail-workflows.md`

Tento dokument musí vzniknout z autoritativních veřejných zdrojů a musí popsat funkční workflow, nikoli vizuální kopii produktu Microsoft Outlook.

### 8.1 Účel auditu

Audit musí určit, které pracovní postupy Outlooku jsou pro KájovoMail závazné jako funkční inspirace.

### 8.2 Povinný rozsah auditu

Audit musí minimálně pokrýt:

- práci se složkami,
- přesun e-mailů mezi složkami,
- přesun složek,
- vytváření složek,
- mazání složek,
- přejmenování složek,
- drag and drop workflow,
- reply,
- reply all,
- forward,
- citaci předchozí historie,
- prefix `Re:` v předmětu,
- označení přečteno / nepřečteno,
- flag / follow-up styl označení,
- vyhledávání,
- filtry podle:
  - odesílatele,
  - příjemce,
  - předmětu,
  - data,
  - stavu přečtení,
  - příloh,
- search folders / virtuální pohledy typu:
  - Unread,
  - Flagged,
  - With attachments,
- archivaci,
- mazání,
- bulk akce nad více zprávami.

### 8.3 Povinný výstup auditu

Audit musí obsahovat tabulku:

- workflow v Outlooku,
- očekávané chování v KájovoMail,
- stav implementace,
- poznámku k omezením IMAP / POP3,
- test, který prokáže shodu workflow.

### 8.4 Zakázané chování

- Zakázáno je slepě kopírovat vizuální vzhled Outlooku.
- Zakázáno je použít Microsoft assety, ikony, screenshoty nebo proprietární design.
- Povinné je převzít funkční logiku a ergonomii, nikoli cizí vizuální identitu.

### 8.5 Výsledek provedeného auditu Outlook workflow (stav šetření: 2026-03-06)

Níže uvedená tabulka je závazný normativní výstup provedeného šetření. Popisuje pouze workflow, které bylo možné doložit z autoritativních veřejných zdrojů společnosti Microsoft. Tyto body jsou od této chvíle součástí tohoto zadání a mají stejnou závaznost jako ostatní kapitoly dokumentu.

| Oblast | Doložené chování Outlooku | Závazný požadavek pro KájovoMail | Omezení / interpretační poznámka | Povinný akceptační test |
|---|---|---|---|---|
| Výběr více zpráv | Outlook podporuje výběr sousedících zpráv pomocí **Shift** a nesousedících pomocí **Ctrl**. [A1] | Desktop musí podporovat multi-select se stejnou ergonomií. Web a Android musí mít ekvivalentní multi-select režim (checkboxy / long-press). | Tato ergonomie je závazná pro desktop; na mobilu se připouští platformně přirozená varianta. | Uživatel vybere 10 sousedících zpráv pomocí Shift a 3 nesousedící pomocí Ctrl a provede bulk akci. |
| Přesun zprávy drag and drop | V Outlooku drag and drop standardně **přesouvá** zprávu do cílové složky; Outlook umí také explicitní akci **Move** nebo **Copy to folder**. U sbalené složky se při hoveru zobrazí podsložky. [A1] | Desktop musí mít drag and drop jako **MOVE** by default. Akce **COPY** musí být explicitní a oddělená. Hover nad sbalenou složkou musí dočasně rozbalit podstrom. | POP3 režim tuto paritu nesplňuje; v POP3 se drag and drop mezi serverovými složkami nepožaduje. | Přetažení vybrané zprávy přesune zprávu; explicitní příkaz Copy vytvoří kopii bez smazání zdroje. |
| Vytváření složek a podsložek | Outlook umožňuje vytvořit top-level folder i subfolder v levém stromu složek. [A4][A25] | V IMAP režimu musí být možné vytvořit složku i podsložku přímo ze stromu složek. | Název musí být validován podle omezení serveru. | Uživatel vytvoří složku i podsložku a po reloadu UI i po re-sync zůstávají na serveru. |
| Přesun a přejmenování složek | Outlook umožňuje přesun a přejmenování uživatelských složek. Defaultní složky nelze libovolně přesouvat nebo přejmenovat. [A5][A26] | KájovoMail musí rozlišovat **system/default folders** a **user folders**. U systémových složek musí UI zakázat rename/move/delete, pokud to provider neumožní. | Neplatí absolutně pro všechny providery; rozhoduje skutečná capability serveru, ale výchozí politika je konzervativní zákaz. | Pokus o rename Inbox je v UI blokován; rename uživatelské složky uspěje a projeví se na serveru. |
| Mazání složek | Outlook dovoluje smazat složku, kterou uživatel vytvořil; smazáním se mažou i její položky. [A6] | KájovoMail musí před smazáním složky zobrazit potvrzení obsahující informaci, že jsou odstraňovány i položky složky. | U providerů s košem může být interně provedeno přesunutí do koše; uživatelská sémantika je stále „delete folder“. | Smazání user folderu vyžaduje potvrzení a po potvrzení složka zmizí ze serveru. |
| Search Folders / virtuální pohledy | Search Folders jsou v Outlooku **virtuální složky** bez přesunu nebo duplikace zpráv. New Outlook používá především předdefinovaná kritéria; classic Outlook umí pokročilejší custom varianty. [A2] | KájovoMail musí mít nejméně tyto virtuální pohledy: **Unread**, **Flagged / For Follow Up**, **With Attachments**. Nesmí fyzicky přesouvat zprávy. | Pokročilý builder custom Search Folders je volitelný Phase 2. MVP musí mít alespoň předdefinované pohledy. | Zpráva zůstane ve zdrojové složce a současně je viditelná ve virtuálním pohledu, pokud splňuje kritérium. |
| Vyhledávání a filtry | Outlook podporuje search box, exact phrase v uvozovkách a operátory **AND / OR / NOT**. Podporuje built-in filters a filter button. [A7][A8] | KájovoMail musí serverově podporovat: exact phrase, AND/OR/NOT, sender, recipient, subject, body, attachments, date range, read/unread, flag. UI musí mít scope selector: current folder / current account / all folders. | Outlook vrací v některých režimech jen prvních 1 000 výsledků; KájovoMail tuto limitaci **nesmí bezdůvodně kopírovat**. Místo toho má vracet paginované výsledky. [A7] | Uživatel zadá dotaz `"expense reports"` a pak `expense AND report`; výsledky se liší podle syntaxe a lze přepnout scope. |
| Reply / Reply All / Forward | Outlook rozlišuje Reply, Reply All a Forward. Reply přidává prefix **RE:**, Forward prefix **FW:**. Reply a Reply All nepřenášejí původní přílohy; Forward je přenáší. [A9] | KájovoMail musí vygenerovat stejné výchozí chování: **Reply = RE:, bez původních příloh**, **Reply All = RE:, bez původních příloh**, **Forward = FW:, s původními přílohami**, pokud není bezpečnostní politikou zakázáno jinak. | Uživatel smí přílohy v reply ručně znovu připojit; výchozí chování ale musí odpovídat Outlook workflow. | Reply nemá původní attachmenty; Forward je obsahuje. |
| Citace původního e-mailu | Outlook při reply/forward standardně zahrnuje původní zprávu pod novým textem a nabízí několik stylů zobrazení originálu. [A10] | Default v KájovoMail musí být **Include original message text**. V advanced settings má být volitelně: indent, prefix each line, attach original, do not include original. | Pro MVP je povinný default režim a minimálně ještě jedna alternativní citační varianta. | U reply je původní zpráva pod odpovědí; změna citačního stylu se projeví v preview. |
| Přečteno / nepřečteno | Outlook umožňuje označit zprávy jako read/unread na jedné i více zprávách. [A3] | KájovoMail musí podporovat mark read / mark unread pro single i multi-select. Nastavení Reading Pane má obsahovat chování „mark as read on open / on delay / manually“. | Konkrétní default delay lze zvolit implementačně; musí však existovat centrální nastavení. | Uživatel označí více zpráv jako unread a stav se promítne do seznamu i detailu. |
| Follow-up / flag | Outlook umí flagovat zprávy pro sebe i pro příjemce; flagged messages se zobrazují ve For Follow Up Search Folder. Microsoft zároveň uvádí, že u IMAP účtů nelze měnit flag text a Start/Due date. [A11][A12] | KájovoMail musí implementovat dvě vrstvy: **(1)** přenositelný mailbox flag (`\Flagged`) a **(2)** rozšířená follow-up metadata (due date, reminder, custom label) uložená v serverovém overlay KájovoMail, pokud je provider nativně nepodporuje. | Tím se zabrání falešnému dojmu, že všechna follow-up metadata synchronizují do cizích klientů. Přenositelnost je garantována pouze pro prostý flag/unflag. | IMAP zprávu lze označit a je vidět jako flagged i v jiném klientu; due date zůstává korektně viditelný alespoň v KájovoMail. |
| Pravidla (Rules) | Outlook umí pravidla pro přesun, flag a reakci na zprávy. [A24] | **Není součástí MVP.** AI generátor je nesmí rozšiřovat do plného rule engine, pokud to uživatel výslovně nepožádá. | Tím se drží scope v mezích původního zadání. | V repozitáři nebude plný rules engine; maximálně ADR s návrhem pro Phase 2. |

### 8.6 Doplňkový forenzní audit MIME kompatibility a renderingu e-mailu

Tento audit byl proveden proto, že původní zadání výslovně požaduje maximální kompatibilitu napříč klienty a současně zakazuje spoléhat se na obrázky nebo komplikované HTML jako na nosný prvek sdělení.

| Oblast | Doložené zjištění | Závazný požadavek pro KájovoMail | Povinný akceptační test |
|---|---|---|---|
| `multipart/alternative` | RFC 2046 stanoví, že části `multipart/alternative` jsou alternativní reprezentace stejné informace, mají být v pořadí **od nejprostší po nejbohatší**, a klient má zobrazit poslední formát, který umí. Plain text má být první, bohatší formát až za ním. [A14] | Každý odchozí e-mail musí být generován jako `multipart/alternative`, s částí `text/plain` **první** a `text/html` **druhou / bohatší**. | Test MIME stromu potvrdí pořadí `text/plain` -> `text/html`. |
| Plain text jako plnohodnotná reprezentace | RFC 2046 definuje `text/plain` jako lineární text bez markup instrukcí; Outlook umí HTML zprávy automaticky zobrazit jako plain text. [A14][A17] | Plain-text část nesmí být „odpadní derivát“. Musí být plně čitelná, samostatná a bez HTML značek. | Text/plain je čitelný samostatně, neobsahuje značky a zachovává smysl zprávy. |
| Externí obrázky v Outlooku | Classic Outlook umožňuje blokovat automatické stahování internetových obrázků; Outlook for Mac má internetové obrázky defaultně blokované kvůli ochraně soukromí. [A15][A16] | KájovoMail nesmí stavět čitelnost e-mailu na externích obrázcích, logu nebo grafickém podpisu. Výchozí nastavení nesmí do odchozích zpráv vkládat externí obrázky ani inline logo. | Odchozí zpráva je plně srozumitelná i při zcela vypnutém načítání externích obrázků. |
| Externí obrázky v Gmailu | Gmail na desktopu a Androidu obrázky typicky zobrazuje automaticky, ale u podezřelých zpráv může vyžadovat ruční potvrzení. [A18][A19] | Specifikace nesmí předpokládat jednotné chování klientů. E-mail musí fungovat stejně dobře, i když jeden klient obrázky ukáže a jiný ne. | Testovací sada obsahuje scénář „images blocked“ a zpráva zůstává použitelná. |
| HTML rozsah | Z kombinace RFC a klientského chování plyne, že bohatá HTML vrstva je pouze zlepšení prezentace, nikoli jediný nosič významu. [A14][A15][A16] | Povolené HTML zůstává úmyslně konzervativní: odstavce, tučné, podtržení, seznamy, citace, základní velikosti textu, základní zarovnání. | HTML preview i plain preview nesou stejnou informaci. |

### 8.7 Doplňkový forenzní audit OpenAI orchestrace a bezpečnostní integrace

Tento audit byl proveden proto, že zadání požaduje centralizovanou AI orchestrace vrstvu a sdílené nastavení napříč desktopem, webem a Androidem.

| Oblast | Doložené zjištění | Závazný požadavek pro KájovoMail | Povinný akceptační test |
|---|---|---|---|
| Umístění API klíče | OpenAI výslovně uvádí, že API key je tajný a nesmí být vystaven v klientském kódu; má být načítán serverově z env nebo key managementu. [A20] | Veškeré OpenAI volání musí jít **výhradně z backendu**. API klíč nesmí být uložen v desktopu, webovém frontendu ani Androidu. | Build artefakty klientů neobsahují OpenAI klíč; bezpečnostní scan to potvrzuje. |
| Zvolený API endpoint | Responses API vytváří model response a umí vracet text i JSON výstupy. [A21] | Backend musí používat **Responses API** jako jediný schválený endpoint pro generování odpovědí. | Integrační test zavolá `/responses` přes backend a validuje návrat strukturovaného výstupu. |
| Strukturovaný výstup | OpenAI doporučuje používat Structured Outputs místo JSON mode, pokud je to možné, protože Structured Outputs vynucují shodu se schématem. [A22] | AI odpověď musí být generována přes strict schema (`text.format` / JSON schema) a teprve poté renderována do plain/HTML varianty. | Nevalidní AI výstup je zachycen validátorem a zpráva se neodešle. |
| Ukládání odpovědí u provideru | OpenAI uvádí, že Responses jsou stored by default, a pro vypnutí ukládání se má použít `store: false`. [A23] | Pro KájovoMail je **výchozí politika `store: false`**. Jakákoli odchylka musí být explicitně konfigurovatelná a zdokumentovaná. | Request builder backendu v produkční konfiguraci posílá `store: false`. |
| Tool usage a determinismus | Responses API umí používat tools a custom code. [A21] | V MVP nesmí být při generování odpovědí zapínány externí built-in tools (web search, file search apod.), pokud to není výslovně navržená feature. Vstupy mají být omezeny na content, historii vlákna a uživatelské zadání. | Audit request payloadu potvrdí, že při běžném generování nejsou aktivní externí tools. |

### 8.8 Závazné doplnění specifikace po provedeném šetření

Na základě výše uvedených auditů se tato specifikace závazně doplňuje takto:

1. **Drag and drop zprávy = MOVE by default.** COPY je samostatná explicitní akce.
2. **Reply / Reply All nepřenáší původní přílohy.** Forward je přenáší, pokud to neblokuje bezpečnostní politika.
3. **Defaultní citační režim** je „Include original message text“.
4. **Search Folders jsou virtuální.** Zprávy se kvůli nim nesmí fyzicky přesouvat.
5. **Portable mailbox flag** je oddělen od rozšířeného follow-up overlay KájovoMail.
6. **Default/system folders** mají být chráněny před rename/move/delete, pokud provider nedeklaruje opak.
7. **MIME pořadí je normativní:** `text/plain` první, `text/html` druhý.
8. **Externí obrázky a logo nejsou výchozí součástí odesílaných zpráv.**
9. **OpenAI requesty běží jen na serveru** a v produkčním defaultu používají `store: false`.
10. **Structured Outputs jsou povinné** a model nesmí vracet finální HTML určené k přímému odeslání bez serverové validace.

### 8.9 Co audit výslovně neukládá do MVP

Na základě šetření bylo záměrně rozhodnuto, že do MVP nejsou povinné tyto oblasti:

- plnohodnotný Outlook rules engine,
- PST/OST kompatibilita,
- Exchange-specifické enterprise funkce mimo obecný IMAP/SMTP model,
- pokročilé custom Search Folders na úrovni classic Outlook,
- synchronizace rozšířených follow-up dat do cizích klientů jako garantovaná funkce.

Tyto body mohou být řešeny až jako Phase 2 nebo samostatné rozšíření.

## 9. Funkční požadavky — e-mailové účty

## 9.1 Přidání účtu

V nastavení musí být wizard nebo formulář pro přidání účtu se vstupy:

- typ účtu: IMAP nebo POP3
- SMTP server
- incoming server
- porty
- šifrování
- uživatelské jméno
- heslo
- volitelný název účtu v UI

### 9.2 Test připojení

Před uložením účtu musí být možné otestovat:

- přihlášení k incoming serveru,
- přihlášení k SMTP,
- schopnost číst seznam složek,
- schopnost odeslat testovací zprávu, pokud to uživatel povolí.

### 9.3 Více účtů

Systém musí podporovat více účtů. Musí být možné:

- přidat více účtů,
- upravit účet,
- deaktivovat účet,
- smazat účet,
- vybrat výchozí účet pro novou zprávu.

## 10. Funkční požadavky — správa e-mailů a složek

## 10.1 Základní operace se zprávami

Povinné operace:

- nový e-mail,
- odpověď,
- odpověď všem,
- přeposlání,
- smazání,
- archivace,
- přesun do složky,
- kopie do složky,
- označení přečteno,
- označení nepřečteno,
- flag / follow-up,
- multi-select a bulk operace.

### 10.1.1 Přenositelné flagy vs. rozšířený follow-up overlay

Na základě provedeného auditu Outlook a omezení IMAP platí:

- přenositelný, interoperabilní základ je stav **flag / unflag**,
- rozšířené atributy jako due date, reminder a custom text nesmí být vydávány za univerzálně synchronizovanou vlastnost všech mailbox providerů,
- pokud provider tyto atributy nativně neumí, ukládají se jako **serverový overlay KájovoMail**,
- UI musí uživateli jasně odlišit:
  - co je mailbox-native,
  - co je KájovoMail-enhanced metadata.

Tím se zachová kompatibilita s jinými klienty bez falešného příslibu plné parity follow-up funkcí.

## 10.2 Historie odpovědi

Při odpovědi musí systém:

- zachovat historii e-mailu,
- zobrazit ji v běžně očekávatelné citované podobě,
- doplnit standardní předmět s prefixem `Re:` pouze tehdy, pokud již neexistuje,
- podporovat HTML i plain-text variantu historie,
- u reply a reply all výchozím stavem **nepřikládat původní přílohy**,
- u forward výchozím stavem **přenést původní přílohy**, pokud to bezpečnostní politika účtu dovolí,
- defaultně použít režim citace odpovídající Outlook „Include original message text“.

## 10.3 Složky

V režimu IMAP musí být možné:

- založit složku,
- přejmenovat složku,
- smazat složku,
- přesunout složku pod jiného rodiče,
- přesouvat zprávy drag and drop mezi složkami,
- přesouvat složky drag and drop tam, kde to dává smysl,
- připnout oblíbené složky,
- zobrazit strom složek,
- rozlišovat system/default folders a user folders,
- zakázat rename/move/delete na system/default folders, pokud to provider nepovolí,
- při drag and drop hoverem dočasně rozbalit sbalenou cílovou složku.

### 10.4 Search folders / chytré pohledy

Systém musí podporovat alespoň tyto virtuální pohledy:

- Nepřečtené
- Označené vlajkou
- S přílohami

Tyto pohledy nesmí fyzicky přesouvat zprávy. Musí fungovat jako virtuální filtr.

## 11. Funkční požadavky — vyhledávání a filtrování

Vyhledávání musí být dostupné na webu, desktopu i Androidu.

### 11.1 Povinná kritéria

Musí být možné vyhledávat a filtrovat podle:

- fulltextu v předmětu,
- fulltextu v těle,
- odesílatele,
- příjemce,
- přesné fráze,
- složky,
- stavu přečtení,
- příloh,
- data od / do,
- označení vlajkou.

### 11.2 Rozsah vyhledávání

Musí být možné hledat:

- v aktuální složce,
- ve všech složkách účtu,
- ve virtuálních pohledech.

UI musí mít explicitní přepínač scope alespoň pro:

- current folder,
- current account / current mailbox,
- all folders dostupné v daném účtu.

### 11.2.1 Syntaxe dotazů

Minimální podporovaná syntaxe musí zahrnovat:

- přesnou frázi v uvozovkách,
- operátory `AND`, `OR`, `NOT`,
- hledání podle jména osoby / části jména v poli odesílatele nebo příjemce,
- filtr `has attachments`,
- filtr `read/unread`.

KájovoMail nesmí mechanicky převzít Outlook limit prvních 1 000 výsledků; místo toho musí používat serverovou paginaci a stabilní řazení výsledků.

### 11.3 Technická implementace vyhledávání

Protože klienti nemají mít lokální perzistentní databázi pošty, vyhledávání musí běžet serverově. Server smí použít:

- nativní možnosti IMAP SEARCH,
- vlastní serverový pomocný index pro výkon,
- kombinaci obojího.

Pomocný index nesmí změnit to, že autoritativním zdrojem zůstává poštovní server.

## 12. Funkční požadavky — editor a odesílání

## 12.1 Povinný formát odeslání

Každý odeslaný e-mail musí být automaticky vytvořen jako:

- `multipart/alternative`
  - `text/plain; charset=UTF-8`
  - `text/html; charset=UTF-8`

Pořadí MIME částí je závazné:

1. `text/plain` musí být první,
2. `text/html` musí být až bohatší následná alternativa.

Plain-text i HTML verze musí vzniknout z jednoho společného obsahu a musí nést stejný význam.

## 12.2 Povolený rozsah formátování

Editor musí umožnit pouze konzervativní a kompatibilní formátování:

- odstavce,
- tučné písmo,
- podtržení,
- seznamy,
- základní velikosti textu,
- základní zarovnání,
- citace.

### 12.3 Zakázaný obsah v HTML e-mailech

Zakázáno je automaticky generovat nebo vkládat:

- externí obrázky,
- inline obrázky jako součást podpisu ve výchozím stavu,
- externí fonty,
- JavaScript,
- iframe,
- video,
- formulářové prvky,
- složitý CSS layout,
- animace.

### 12.4 Logo v odesílaných e-mailech

Ve výchozím nastavení se do odchozích e-mailů **nevkládá žádné inline logo ani grafický podpis**. Důvodem je maximalizace kompatibility a eliminace situací, kdy klient vyžaduje ruční potvrzení pro zobrazení obrázků.

### 12.5 Přílohy

Přílohy jsou standardní funkcí e-mailového klienta a mohou být odesílány jako klasické MIME attachmenty. Nesmí se však stát závislým prvkem pro správné zobrazení hlavního textu e-mailu.

## 13. Funkční požadavky — AI generování odpovědí

## 13.1 Umístění v UI

Na desktopu musí být vpravo úzký boční panel s minimálně dvěma sekcemi:

1. **Zadání** — pole pro neformální instrukce uživatele
2. **Nabídky** — dlaždice s aktivními nabídkami

Na webu a Androidu může být tentýž obsah řešen adaptivně, ale funkčně musí být zachován.

## 13.2 Povinné vstupy do AI generování

Server musí pro každé generování odpovědi sestavit prompt z těchto částí:

1. **neměnná systémová pravidla aplikace**
2. **uživatelské / administrátorské AI nastavení**
3. **content / kontextové bloky**
4. **historie aktuálního e-mailového vlákna**
5. **ad hoc uživatelské zadání ze sekce „Zadání“**

### 13.3 Povinné systémové chování AI

AI musí být instruována tak, aby:

- používala pouze fakta, která jsou v poskytnutém contentu a v historii e-mailu,
- nic si nevymýšlela,
- nepoužívala domněnky,
- nebyla vulgární,
- vytvořila strukturovanou a zdvořilou odpověď,
- při chybějících faktech raději upozornila na nedostatek podkladů, než aby doplňovala neověřený obsah.

## 13.4 Povinná technologie OpenAI integrace

OpenAI integrace musí být implementována na serveru a musí používat:

- **Responses API**
- **Structured Outputs** nebo ekvivalentně striktní strukturované schéma
- výchozí request policy **`store: false`**
- serverově uložený API key mimo klientské aplikace

AI nesmí generovat přímo finální svévolný HTML e-mail bez serverové validace.

V MVP se při běžném generování odpovědí nesmí aktivovat externí built-in tools, pokud pro ně neexistuje samostatné zadání a audit datových toků.

## 13.5 Povinný meziformát AI výstupu

AI musí vracet strukturovaný meziformát, například JSON objekt, z něhož server deterministicky vytvoří:

- plain-text variantu,
- HTML variantu.

Doporučené pole struktury:

- language
- subject_mode
- subject
- greeting
- body_blocks
- closing
- signature
- missing_facts
- needs_user_review

### 13.6 Náhled před odesláním

Každá AI vygenerovaná odpověď musí být před odesláním zobrazena uživateli k revizi. Uživatel musí mít možnost:

- text upravit,
- odeslání zrušit,
- změnit tag nabídky,
- změnit předmět,
- doplnit příjemce.

## 14. Funkce „Nabídky“

Při odesílání odpovědi musí být k dispozici volba:

**„Tento e-mail je nabídka“**

Pokud je volba aktivní, systém musí:

- vytvořit entitu nabídky navázanou na e-mailové vlákno nebo konkrétní zprávu,
- přiřadit jí stav,
- zobrazit ji v pravém panelu jako dlaždici.

### 14.1 Povinná pole nabídky

- interní ID
- vazba na účet
- vazba na thread / message
- název nabídky
- výchozí label odvozený ze subjectu nebo odesílatele
- ručně editovatelný label
- stav nabídky

### 14.2 Povinné stavy nabídky

- aktivní
- vyřízená pozitivně
- vyřízená negativně
- archivovaná

## 15. Uživatelské rozhraní — desktop

Desktop aplikace musí po spuštění nabíhat v maximalizovaném okně a obsahovat minimálně:

### 15.1 Levý panel

- seznam účtů
- strom složek
- oblíbené složky
- virtuální pohledy
- možnost rozbalit / skrýt panel

### 15.2 Střední panel

- seznam zpráv ve vybrané složce
- informace minimálně:
  - odesílatel,
  - předmět,
  - ukázka textu,
  - datum / čas,
  - stav přečtení,
  - příznak přílohy,
  - příznak nabídky

### 15.3 Pravý hlavní panel

- horní část: čtení vybraného e-mailu
- dolní část: editor odpovědi nebo nové zprávy

### 15.4 Pravý úzký panel

- sekce Zadání pro AI
- tlačítko Vygeneruj odpověď
- sekce Nabídky s dlaždicemi

### 15.5 Toolbar

Povinné akce:

- Nový e-mail
- Odpovědět
- Odpovědět všem
- Přeposlat
- Smazat
- Archivovat
- Přesunout
- Označit přečteno / nepřečteno
- Flag
- Vyhledat
- Filtr
- Nastavení
- Synchronizovat / obnovit

## 16. Uživatelské rozhraní — web

Webová aplikace musí být dostupná na `mail.hcas.cz` a musí mít funkční paritu s desktopem tam, kde to dává smysl.

### 16.1 Autentizace

Web musí obsahovat:

- login jménem a heslem,
- změnu hesla,
- reset hesla,
- odhlášení,
- správu session.

### 16.2 Bezpečnost webu

- výhradně HTTPS
- bezpečné cookies / tokeny
- CSRF ochrana tam, kde je relevantní
- rate limiting pro login endpointy
- audit log přihlášení

## 17. Uživatelské rozhraní — Android

Android aplikace musí být nativní a funkčně musí pokrýt stejné scénáře jako desktop, s adaptací na mobilní použití.

### 17.1 Povinné obrazovky

- login
- seznam účtů / složek
- seznam zpráv
- detail zprávy
- compose / reply
- nastavení
- AI panel jako bottom sheet / side sheet / samostatný screen
- nabídky

### 17.2 Povinné chování

- žádná přímá komunikace s OpenAI
- žádná perzistentní lokální mail databáze
- pouze bezpečné uložení session tokenu
- respektování systémových přístupnostních nastavení

## 18. Nastavení aplikace

## 18.1 Sekce E-mailové účty

- přidání / editace / smazání účtu
- test připojení
- výběr výchozího účtu

## 18.2 Sekce OpenAI

Musí obsahovat:

- API klíč
- test spojení
- model nebo modelový profil
- systémovou roli
- podpis
- pravidla formulace odpovědí
- content bloky

### 18.3 Uložení API klíče

API klíč se ukládá pouze na serveru, šifrovaně. Klient jej po uložení nesmí znát v plném znění. V UI se zobrazuje pouze maskovaná hodnota a možnost klíč změnit.

## 19. Bezpečnost a ochrana dat

Povinné bezpečnostní principy:

- šifrovaný přenos všech klientů k serveru,
- šifrované uložení hesel a API klíčů,
- oddělení uživatelských dat podle identity,
- audit log důležitých akcí,
- role-based access pro administrativní části,
- žádné ukládání OpenAI klíče do desktopu ani Androidu,
- možnost logického odhlášení všech session.

### 19.1 OpenAI a soukromí

Do OpenAI se standardně odesílá pouze:

- předmět,
- tělo konverzace,
- potřebná metadata pro generování odpovědi,
- administrátorem definovaný content,
- uživatelské zadání.

Přílohy se do OpenAI nesmí odesílat automaticky, pokud k tomu neexistuje explicitní funkce a informovaný souhlas uživatele.

## 20. Povinné API kontrakty

Backend musí publikovat a udržovat OpenAPI dokumentaci minimálně pro:

- autentizaci,
- účty,
- složky,
- zprávy,
- vyhledávání,
- koncepty,
- AI generování,
- odesílání,
- nabídky,
- uživatelská nastavení.

Minimální endpointy:

- `POST /auth/login`
- `POST /auth/logout`
- `POST /auth/change-password`
- `POST /auth/request-password-reset`
- `GET /accounts`
- `POST /accounts`
- `POST /accounts/test`
- `GET /folders`
- `POST /folders`
- `PATCH /folders/{id}`
- `DELETE /folders/{id}`
- `GET /messages`
- `GET /messages/{id}`
- `POST /messages/search`
- `POST /messages/move`
- `POST /messages/copy`
- `POST /messages/mark-read`
- `POST /messages/mark-unread`
- `POST /messages/flag`
- `POST /messages/unflag`
- `GET /search-folders`
- `POST /drafts`
- `PATCH /drafts/{id}`
- `POST /ai/generate-reply`
- `POST /send`
- `GET /offers`
- `PATCH /offers/{id}`

## 21. Design a značka — závazná integrace manifestu

### 21.1 Povinnost převzít manifest beze změny

Soubor `ManifestDesignKájovo.md` musí být do repozitáře převzat beze změny a respektován jako SSOT.

### 21.2 Povinnost UI tokenů a motion tokenů

Repozitář musí obsahovat minimálně:

- `apps/kajovo-mail/palette/palette.json`
- `apps/kajovo-mail/ui-tokens/tokens.json`
- `apps/kajovo-mail/ui-motion/motion.json`
- `apps/kajovo-mail/brand/brand.json`

### 21.3 Signace a brand přítomnost

Web, desktop i Android musí respektovat povinnou přítomnost brand prvků a signace dle manifestu. Pokud by signace kolidovala s UI, upraví se UI, nikoli signace.

### 21.4 Zákaz alternativního brandingu

Zakázáno je:

- vytvořit jinou signaci,
- vytvořit jiné logo bez dodaného assetu,
- vytvořit paralelní brand pravidla,
- použít jiné fonty nebo barvy tam, kde manifest předepisuje konkrétní hodnoty.

## 22. Testy a release gate

## 22.1 Povinné typy testů

Musí vzniknout minimálně:

- unit testy backendu
- integrační testy IMAP/SMTP
- testy MIME generování
- testy AI orchestrace se schema validací
- UI testy webu
- UI testy desktopu
- UI testy Androidu
- brand compliance testy dle manifestu
- bezpečnostní smoke testy

## 22.2 Povinné akceptační scénáře

Minimálně musí projít tyto scénáře:

1. Uživatel přidá IMAP účet, test připojení uspěje, načtou se složky.
2. Uživatel otevře e-mail, doplní text do „Zadání“, vygeneruje odpověď a před odesláním ji upraví.
3. Odeslaná odpověď odejde jako `multipart/alternative`.
4. Plain-text část je čitelná a neobsahuje HTML značky.
5. HTML část neobsahuje zakázané prvky.
6. E-mail označený jako nabídka se zobrazí jako dlaždice v panelu Nabídky.
7. Přesun e-mailu mezi složkami drag and drop se projeví na serveru.
8. Vyhledání nepřečtených e-mailů funguje.
9. Reply nepřenese původní přílohy, zatímco Forward je přenese.
10. System/default složku nelze přejmenovat nebo smazat, pokud provider akci zakazuje.
11. IMAP flag je interoperabilní a rozšířený follow-up due date zůstane konzistentně viditelný v KájovoMail.
12. Backend posílá OpenAI request se `store: false`.
13. Web, desktop i Android sdílejí stejné serverové nastavení OpenAI.
14. Release selže, pokud chybí povinné brand assety nebo jsou porušeny testy manifestu.

## 23. Build a deployment výstupy

AI generátor musí dodat:

### 23.1 Backend

- Dockerfile
- docker-compose pro vývoj
- produkční konfigurační šablony
- `.env.example`

### 23.2 Web

- build skripty
- produkční build
- konfigurační dokumentaci pro `mail.hcas.cz`

### 23.3 Desktop

- build skripty pro Windows
- build skripty pro macOS
- instalační artefakty nebo jejich reprodukovatelný build pipeline

### 23.4 Android

- Android Studio projekt
- debug build
- release build pipeline
- APK nebo AAB workflow

## 24. Výslovné zákazy pro AI generátor kódu

AI generátor nesmí:

- odevzdat jen kostru bez reálné funkčnosti,
- ponechat v produkčním kódu `TODO`, `TBD`, neimplementované stuby nebo placeholder texty,
- použít lokální mail databázi jako hlavní zdroj pošty na desktopu nebo Androidu,
- posílat OpenAI requesty přímo z klientských aplikací,
- generovat náhradní logo nebo náhradní brand pravidla,
- ignorovat manifest,
- vynechat audit Outlook workflow,
- vynechat plain-text verzi e-mailu,
- vkládat do e-mailů defaultně obrázky nebo externí assety,
- nasadit řešení bez testů.

## 25. Minimální definice „hotovo“

Produkt je považován za hotový pouze tehdy, pokud současně platí:

1. existuje backend, web, desktop i Android,
2. funguje přihlášení a správa účtu,
3. funguje napojení na IMAP/SMTP,
4. funguje AI generování odpovědi ze serveru,
5. funguje odeslání `multipart/alternative`,
6. funguje správa složek v IMAP režimu,
7. funguje vyhledávání a filtry,
8. funguje funkce Nabídky,
9. brand integrace odpovídá manifestu,
10. existují automatické testy a build pipeline,
11. repozitář je připraven pro doplnění finálního loga dle manifestu,
12. nevyskytují se neimplementované placeholdery.

## 26. Doporučená implementační strategie

AI generátor má postupovat v těchto krocích:

1. založit monorepo a převzít manifest,
2. vytvořit forenzní audit Outlook workflow,
3. definovat API a datový model,
4. implementovat backend a autentizaci,
5. implementovat e-mailové konektory,
6. implementovat AI orchestrace vrstvu,
7. implementovat web,
8. implementovat desktop,
9. implementovat Android,
10. doplnit testy, brand compliance a release gate,
11. připravit build a deployment.

## 27. Jednověté shrnutí pro AI generátor

Vygeneruj kompletní monorepo KájovoMail s Python backendem, React webem, PySide6 desktopem a nativním Kotlin Android klientem, s centrální serverovou komunikací s OpenAI, s plnou IMAP/SMTP podporou, s omezeným POP3 režimem, s odesíláním e-mailů jako `multipart/alternative`, s forenzně převzatými workflow z Outlooku, s funkcí Nabídky, bez lokální perzistentní mail databáze na klientech, a s bezvýhradným dodržením `ManifestDesignKájovo.md`.


## 28. Autoritativní zdroje použité při forenzním šetření

Níže uvedené zdroje byly použity při doplnění tohoto zadání. Všechny další implementační interpretace se musí držet těchto zdrojů nebo přísněji konzervativního chování.

- **[A1]** Microsoft Support — Move or copy an item to another folder in Outlook  
  https://support.microsoft.com/en-us/office/move-or-copy-an-item-to-another-folder-in-outlook-19768dfe-86c4-40bf-b82c-1c084b624492
- **[A2]** Microsoft Support — Use Search Folders to find messages or other Outlook items  
  https://support.microsoft.com/en-us/office/use-search-folders-to-find-messages-or-other-outlook-items-c1807038-01e4-475e-8869-0ccab0a56dc5
- **[A3]** Microsoft Support — Mark a message as read or unread in Outlook  
  https://support.microsoft.com/en-us/office/mark-a-message-as-read-or-unread-in-outlook-59b44298-08c2-4eb7-8128-ea0fb7f52720
- **[A4]** Microsoft Support — Create a folder or subfolder in Outlook  
  https://support.microsoft.com/en-us/office/create-a-folder-or-subfolder-in-outlook-3d3120d4-3c0e-4fef-b396-89b68324eba6
- **[A5]** Microsoft Support — Move or rename a folder in Outlook for Mac  
  https://support.microsoft.com/en-us/office/move-or-rename-a-folder-in-outlook-for-mac-e20fedab-6214-4648-a0bf-937d8e05f170
- **[A6]** Microsoft Support — Delete a folder  
  https://support.microsoft.com/en-us/office/delete-a-folder-af63d84b-65a4-447b-8f42-7b6f4898c6ad
- **[A7]** Microsoft Support — How to search in Outlook  
  https://support.microsoft.com/en-us/office/how-to-search-in-outlook-d824d1e9-a255-4c8a-8553-276fb895a8da
- **[A8]** Microsoft Support — Find a message or item with Instant Search  
  https://support.microsoft.com/en-us/office/find-a-message-or-item-with-instant-search-69748862-5976-47b9-98e8-ed179f1b9e4d
- **[A9]** Microsoft Support — Reply to or forward an email message  
  https://support.microsoft.com/en-us/office/reply-to-or-forward-an-email-message-a843f8d3-01b0-48da-96f5-a71f70d0d7c8
- **[A10]** Microsoft Support — Change how the original message appears in replies and forwards  
  https://support.microsoft.com/en-us/office/change-how-the-original-message-appears-in-replies-and-forwards-1207f4ea-f7cf-4cdf-9298-5982fa2e5e2f
- **[A11]** Microsoft Support — Flag email messages for follow up  
  https://support.microsoft.com/en-us/office/flag-email-messages-for-follow-up-9d0f175f-f3e9-406d-bbf7-9c57e1f781cc
- **[A12]** Microsoft Support — Review flagged email messages  
  https://support.microsoft.com/en-gb/office/review-flagged-email-messages-9ed8bff1-9c61-4c32-af3d-fc7b94b88356
- **[A13]** Microsoft Support — What is the difference between POP and IMAP?  
  https://support.microsoft.com/en-us/office/what-is-the-difference-between-pop-and-imap-85c0e47f-931d-4035-b409-af3318b194a8
- **[A14]** IETF — RFC 2046: Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types  
  https://datatracker.ietf.org/doc/html/rfc2046
- **[A15]** Microsoft Support — Block or unblock automatic picture downloads in classic Outlook email messages  
  https://support.microsoft.com/en-us/office/block-or-unblock-automatic-picture-downloads-in-classic-outlook-email-messages-15e08854-6808-49b1-9a0a-50b81f2d617a
- **[A16]** Microsoft Support — Automatically download pictures from the Internet in Outlook for Mac  
  https://support.microsoft.com/en-us/office/automatically-download-pictures-from-the-internet-in-outlook-for-mac-3e61c1fe-02f7-4280-9aef-9bc0233b564c
- **[A17]** Microsoft Support — Read email messages in plain text  
  https://support.microsoft.com/en-us/office/read-email-messages-in-plain-text-16dfe54a-fadc-4261-b2ce-19ad072ed7e3
- **[A18]** Google Help — Turn images on or off in Gmail (desktop)  
  https://support.google.com/mail/answer/145919?hl=en
- **[A19]** Google Help — Turn images on or off in Gmail (Android)  
  https://support.google.com/mail/answer/145919?co=GENIE.Platform%3DAndroid&hl=en
- **[A25]** Microsoft Support — Organize email by using folders in Outlook  
  https://support.microsoft.com/en-us/office/organize-email-by-using-folders-in-outlook-0616c259-4bc1-4f35-807d-61eb59ac79c1
- **[A26]** Microsoft Support — Move an email folder  
  https://support.microsoft.com/en-us/office/move-an-email-folder-1cf90622-dcc6-4f8d-8edf-e15ab5c425b2

- **[A20]** OpenAI API Reference — Authentication  
  https://developers.openai.com/api/reference/overview
- **[A21]** OpenAI API Reference — Create a model response (`POST /responses`)  
  https://developers.openai.com/api/reference/resources/responses/methods/create
- **[A22]** OpenAI API — Structured model outputs  
  https://developers.openai.com/api/docs/guides/structured-outputs/
- **[A23]** OpenAI API — Migrate to the Responses API  
  https://developers.openai.com/api/docs/guides/migrate-to-responses
- **[A24]** Microsoft Support — Set up rules in Outlook  
  https://support.microsoft.com/en-us/office/set-up-rules-in-outlook-75ab719a-2ce8-49a7-a214-6d62b67cbd41
