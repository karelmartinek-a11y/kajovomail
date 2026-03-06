# KájovoMail — finální zadání

## 1. Účel dokumentu

Tento dokument je závazné technické a produktové zadání pro realizaci systému **KájovoMail**. Definuje cílový produkt, architekturu, funkční rozsah, integrační pravidla, bezpečnost, provozní požadavky, testy a podmínky předání.

Cílem je dodat plně funkční, testovatelný a nasaditelný software, nikoli prototyp, wireframe, dílčí ukázku nebo kostru bez implementace.

## 2. Závazné dokumenty a rozhodovací pravidla

### 2.1 Hierarchie závaznosti

1. **Manifest designu v adresáři `docs/`** je jediný zdroj pravdy pro značku, signaci, logo, palety, tokeny, motion, přítomnost brand prvků v UI a release gate související se značkou.
2. **Tento dokument** je jediný zdroj pravdy pro architekturu, funkční chování, integrační pravidla, bezpečnost, API, provoz, testy a definici hotového produktu.

### 2.2 Řešení konfliktů

- V otázkách značky, loga, signace, tokenů, palet, motion a vizuální přítomnosti brand prvků má absolutní přednost manifest.
- V otázkách architektury, datových toků, bezpečnosti, funkcí, API a provozu má přednost tento dokument.
- Pokud některá situace není popsána explicitně, musí být zvoleno konzervativní, bezpečné, testovatelné a provozně udržitelné řešení, které neporuší manifest ani tento dokument.
- Nesmí vzniknout paralelní řídicí dokument pro brand ani alternativní sada pravidel, která by obcházela manifest.

## 3. Vstupní závazné podklady v repozitáři

V repozitáři jsou již přítomné závazné podklady, které musí být převzaty beze změny významu a bez nahrazování novou variantou:

- `docs/ManifestDesignKájovo.md` — závazný manifest značky.
- `brand/brand/brand.json` — metadata značky aplikace.
- `brand/palette/palette.json` — závazná paleta pro UI.
- `brand/ui-tokens/tokens.json` — závazné UI tokeny.
- `brand/ui-motion/motion.json` — závazná motion pravidla.
- `brand/signace/signace.svg`, `brand/signace/signace.pdf`, `brand/signace/signace.png` — povinná signace.
- `brand/logo/sources/logo_master.svg` — master logo aplikace.
- `brand/logo/exports/` — rychlé exporty full, mark, wordmark a signace.

Tyto assety jsou referenční zdroj. Implementace je smí převzít, zrcadlit do cílové struktury produktu nebo používat build procesem, ale nesmí vzniknout alternativní logo, náhradní signace, upravená paleta ani vlastní brand pravidla mimo manifest.

## 4. Cíl produktu

KájovoMail je multiplatformní e-mailový klient s centrálním serverovým jádrem a třemi klienty:

- webová aplikace pro `mail.hcas.cz`,
- desktopová aplikace pro Windows a macOS,
- nativní Android aplikace.

Součástí produktu je serverová integrace s OpenAI pro generování návrhů e-mailových odpovědí. Produkt musí poskytovat jednotné chování napříč platformami, sdílená uživatelská nastavení, centrální bezpečnostní politiku a jednotné API.

## 5. Cílový výstup implementace

Výsledkem musí být kompletní monorepo obsahující minimálně:

- backend,
- web,
- desktop,
- android,
- infrastrukturní a build soubory,
- automatizované testy,
- CI/CD pipeline,
- OpenAPI dokumentaci,
- dokumentaci provozu, bezpečnosti a nasazení,
- integraci závazných brand assetů a kontrol vyplývajících z manifestu.

Řešení musí být připravené k reálnému nasazení. Nesmí být odevzdána pouze část systému.

## 6. Rozsah MVP a výslovně nepovinné oblasti

### 6.1 Povinný rozsah MVP

MVP musí pokrýt:

- přihlášení do aplikace a správu session,
- správu více e-mailových účtů,
- plnohodnotný IMAP/SMTP režim,
- omezený POP3/SMTP režim,
- práci se složkami a zprávami,
- serverové vyhledávání a virtuální pohledy,
- compose, reply, reply all, forward a odeslání,
- AI generování návrhů odpovědí,
- funkci „Nabídky",
- sdílená nastavení mezi klienty,
- bezpečnostní, auditní a provozní minimum,
- testy a release gate.

### 6.2 Mimo rozsah MVP

Do MVP nejsou povinné tyto oblasti:

- plnohodnotný rules engine,
- PST/OST kompatibilita,
- Exchange-specifické enterprise funkce mimo obecný IMAP/SMTP model,
- pokročilý custom builder pro search folders,
- garantovaná synchronizace rozšířených follow-up metadat do cizích klientů.

Tyto oblasti mohou být řešeny až v další fázi, ale nesmí být rozpracovány způsobem, který komplikuje architekturu MVP nebo vytváří falešný dojem dokončené funkce.

## 7. Nevyjednatelné architektonické zásady

### 7.1 Centrální serverové jádro

Celý systém musí být navržen jako **server-centric**. Platí následující zásady:

- veškerá komunikace klientů probíhá přes serverové API,
- veškerá komunikace s OpenAI probíhá výhradně na serveru,
- veškeré sdílené uživatelské a administrátorské nastavení se ukládá na serveru,
- veškerá práce s e-mailovými účty, složkami, zprávami, drafty a odesíláním probíhá přes serverové API,
- web, desktop i Android jsou klienti jednoho systému a nesmí si vytvářet vlastní nezávislou interpretační logiku pro poštovní workflow.

### 7.2 Žádná perzistentní lokální databáze pošty na klientech

Na desktopu ani Androidu nesmí vzniknout perzistentní lokální databáze e-mailového obsahu. Povoleno je pouze:

- držení dat v RAM,
- krátkodobá technická cache s automatickým úklidem,
- bezpečné uložení session tokenu nebo obdobného autentizačního artefaktu v systémovém secure storage.

Zakázáno je:

- trvale ukládat lokální kopii mailboxu jako primární pracovní zdroj,
- budovat lokální fulltextový index celé pošty na klientovi,
- realizovat off-line mailbox jako výchozí provozní model.

### 7.3 Autoritativní zdroj dat

- Autoritativním zdrojem e-mailových zpráv, složek a mailbox-native stavů je vzdálený poštovní server.
- Autoritativním zdrojem uživatelů, session, nastavení, AI profilů, overlay metadat, nabídek, auditních záznamů a interních provozních dat je backend KájovoMail.
- Pokud backend používá pomocný index nebo cache, nesmí tím změnit fakt, že poštovní server zůstává autoritativním zdrojem pošty.

### 7.4 Styl backendové architektury

Pro MVP je závazný **modulární monolit** s jasně oddělenými bounded contexts a s oddělenými worker procesy pro asynchronní úlohy. Distribuce do samostatných služeb v budoucnu musí být možná bez změny veřejných kontraktů, ale pro MVP se nepožaduje mikroservisní rozpad.

### 7.5 Idempotence a odolnost

Všechny operace, které mohou být spuštěny opakovaně nebo asynchronně, musí být navrženy jako idempotentní. To platí zejména pro:

- synchronizaci mailboxu,
- move/copy operace,
- generování AI odpovědi,
- ukládání draftu,
- odeslání e-mailu,
- změny stavů nabídky.

## 8. Cílová architektura systému

### 8.1 Kontext systému

Architektura musí obsahovat tyto vrstvy:

1. **Klienti** — web, desktop, Android.
2. **API vrstva** — autentizace, autorizace, validace, REST API, WebSocket/event stream.
3. **Aplikační doména** — účty, složky, zprávy, drafty, search, nabídky, AI orchestrace, nastavení.
4. **Integrační vrstva** — IMAP/POP3/SMTP konektory a OpenAI konektor.
5. **Datová vrstva** — PostgreSQL, Redis, případně pomocný serverový index.
6. **Asynchronní worker vrstva** — synchronizace pošty, odesílání, AI operace, reindexace a notifikace.

### 8.2 Nasazovací topologie

Produkční nasazení musí minimálně obsahovat:

- reverzní proxy,
- API aplikaci,
- worker procesy,
- PostgreSQL,
- Redis,
- perzistentní logy a metriky,
- konfigurační a tajné údaje mimo repozitář.

### 8.3 Interní moduly backendu

Backend musí být rozdělen minimálně na tyto moduly:

- **Auth** — přihlášení, session, změna a reset hesla, odhlášení všech session.
- **Users & Preferences** — uživatel, role, uživatelské preference, čtecí režim, podpis, výchozí účet.
- **Accounts & Credentials** — e-mailové účty, capability discovery, test připojení, šifrované uložení přístupů.
- **Mailbox Sync** — synchronizace složek, zpráv, stavů, capability map a kurzorů.
- **Folders** — strom složek, default/system folders, uživatelské složky, přesuny, rename, delete, oblíbené složky.
- **Messages** — list, detail, thready, mark read/unread, flag/unflag, bulk akce, move/copy/archive/delete.
- **Drafts & Compose** — drafty, autosave, preview, rendering plain/HTML varianty.
- **Send** — validace, MIME sestavení, odeslání, idempotence odeslání.
- **Search** — serverové vyhledávání, query parser, virtuální pohledy, paginace.
- **AI Orchestration** — request builder, structured output, validace, rendering návrhu odpovědi, request policy.
- **Offers** — vazba nabídky na thread/message, stavy, přechody stavů, dlaždice a filtry.
- **Audit & Security** — audit log, bezpečnostní události, redakce citlivých údajů, rate limiting.
- **Notifications & Events** — WebSocket/event stream, změnové notifikace klientům.

### 8.4 Datové vlastnictví a perzistence

V PostgreSQL se ukládají zejména:

- uživatelé, role a session,
- e-mailové účty a jejich šifrované přihlašovací údaje,
- zjištěné capability providerů,
- synchronizační kurzory a technický stav synchronizace,
- metadata zpráv a složek potřebná pro rychlé listování a hledání,
- serverový pomocný index nebo jeho referenční metadata,
- drafty, preview a odesílací stavy,
- follow-up overlay metadata,
- nabídky a jejich stavové přechody,
- AI profily, content bloky, pravidla formulace a request logy,
- auditní záznamy, provozní záznamy a idempotency key evidence.

V Redis se ukládá zejména:

- queue pro asynchronní úlohy,
- krátkodobá cache,
- fan-out notifikací,
- distribuované zámky a debounce mechanizmy.

Mailserver zůstává autoritativním zdrojem poštovních dat. Backend smí držet metadata, index a provozní cache, ale nesmí zavést interní datový model, který by se stal novým zdrojem pravdy pro mailbox.

### 8.5 Synchronizační model

Synchronizace musí podporovat:

- počáteční napojení účtu,
- inkrementální synchronizaci,
- ruční obnovení uživatelem,
- periodickou synchronizaci na pozadí,
- bezpečné zpracování chyb a retry politiku,
- detekci capability změn provideru,
- konzistentní promítnutí změn do všech klientů přes event stream.

Synchronizace musí být navržena tak, aby:

- neprováděla duplicitní zápisy,
- uměla obnovit běh po přerušení,
- uměla znovu bezpečně přehrát úlohu,
- rozlišovala mezi mailbox-native stavem a KájovoMail overlay metadaty.

### 8.6 Threading a identita zprávy

Primární threading musí vycházet z RFC hlaviček `Message-ID`, `In-Reply-To` a `References`. Heuristiky nad předmětem smí sloužit pouze jako doplněk pro UI a nesmí měnit transportní realitu zpráv.

### 8.7 Event model

Systém musí poskytovat server push alespoň pro tyto události:

- změna stavu synchronizace,
- nová nebo změněná zpráva,
- změna složek,
- dokončení AI generování,
- změna stavu nabídky,
- změna draftu uloženého na serveru,
- odhlášení session nebo změna bezpečnostního stavu.

## 9. Povinný technologický stack

### 9.1 Backend

- Python 3.12+
- FastAPI
- PostgreSQL
- Redis
- worker procesy pro asynchronní úlohy
- Docker a Docker Compose pro vývojové prostředí
- reverzní proxy typu Nginx nebo ekvivalent

Backend musí obsahovat migrační mechanismus databáze, strukturované logování a OpenAPI generaci.

### 9.2 Web

- React
- TypeScript
- komunikace pouze se serverovým API
- žádná přímá komunikace s IMAP, POP3, SMTP ani OpenAI

Web může být realizován jako SPA nebo SSR aplikace, ale musí zachovat úplnou funkční paritu tam, kde to dává smysl, a musí splnit brand, a11y a responsive pravidla z manifestu.

### 9.3 Desktop

- Python
- PySide6 / Qt 6
- skutečná desktopová aplikace
- zákaz WebView shellu jako náhrady desktopového klienta

### 9.4 Android

- Kotlin
- Jetpack Compose
- nativní aplikace
- zákaz WebView wrapperu

## 10. Doménový model

Systém musí minimálně obsahovat následující doménové entity:

- `User`
- `Role`
- `AuthSession`
- `EmailAccount`
- `AccountCapability`
- `SyncCursor`
- `EmailFolder`
- `EmailMessage`
- `EmailThread`
- `EmailDraft`
- `AttachmentMeta`
- `FollowUpOverlay`
- `SearchView`
- `Offer`
- `OfferState`
- `UserPreferences`
- `AIProfile`
- `AIContentBlock`
- `AIRequestLog`
- `AuditLog`
- `IdempotencyKey`

### 10.1 Datové hranice entity zprávy

Pro každou zprávu musí být odlišeno:

- mailbox-native identifikace a stav,
- indexovaná metadata pro listy a search,
- KájovoMail overlay metadata,
- dočasné prezentační reprezentace pro klienty.

### 10.2 Follow-up metadata

Systém musí výslovně odlišovat:

- interoperabilní mailbox flag,
- rozšířená follow-up metadata KájovoMail.

Uživatel v UI musí vždy poznat, co je přenositelný mailbox-native stav a co je pouze rozšíření KájovoMail.

## 11. Funkční požadavky

### 11.1 Autentizace a uživatelé

Systém musí poskytovat:

- přihlášení jménem a heslem,
- odhlášení,
- změnu hesla,
- reset hesla,
- správu session,
- možnost logického odhlášení všech session,
- role-based access pro administrativní části.

Administrátor musí spravovat globální OpenAI konfiguraci, sdílené AI profily a bezpečnostní nastavení. Běžný uživatel smí měnit pouze své účty, preference, osobní podpis a povolené osobní AI volby.

### 11.2 E-mailové účty

Při přidání účtu musí být k dispozici formulář nebo wizard se vstupy minimálně:

- typ účtu: IMAP nebo POP3,
- incoming server,
- SMTP server,
- porty,
- způsob šifrování,
- uživatelské jméno,
- heslo,
- volitelný zobrazovaný název účtu,
- volitelný display name odesílatele,
- volitelný reply-to.

Před uložením účtu musí být možné otestovat:

- přihlášení k incoming serveru,
- přihlášení k SMTP,
- čtení seznamu složek nebo dostupného mailbox rozsahu,
- odeslání testovací zprávy, pokud to uživatel povolí.

Systém musí podporovat více účtů. Musí být možné účet přidat, upravit, deaktivovat, smazat a zvolit jako výchozí.

### 11.3 Režim IMAP a režim POP3

#### IMAP

IMAP je plnohodnotný režim. Musí podporovat:

- strom složek,
- přesuny a kopie zpráv,
- správu složek,
- mailbox-native stavy,
- serverové vyhledávání,
- virtuální pohledy nad serverově dostupnými daty,
- interoperabilní flag.

#### POP3

POP3 je omezený kompatibilní režim. V UI musí být jasně uvedeno, že plná funkční parita s IMAP neexistuje. V POP3 režimu není povinné a nesmí být vydáváno za plně podporované zejména:

- serverová správa složek,
- přesuny mezi serverovými složkami,
- spolehlivá synchronizace přečteno/nepřečteno,
- serverové vyhledávání napříč složkami,
- plná interoperabilita flag/follow-up workflow,
- Outlook-like ergonomie složek a search folders.

### 11.4 Správa složek

V IMAP režimu musí být možné:

- zobrazit strom složek,
- vytvořit složku a podsložku,
- přejmenovat uživatelskou složku,
- smazat uživatelskou složku,
- přesunout uživatelskou složku pod jiného rodiče,
- rozlišit system/default folders a user folders,
- zakázat rename, move a delete na system/default folders, pokud provider akci nepovolí,
- připnout oblíbené složky,
- dočasně rozbalit sbalenou cílovou složku při hoveru během drag and drop.

Při smazání složky musí být vyžádáno potvrzení s informací, že dojde i k odstranění položek ve složce.

### 11.5 Správa zpráv

Povinné operace se zprávami:

- nový e-mail,
- reply,
- reply all,
- forward,
- delete,
- archive,
- move,
- copy,
- mark read,
- mark unread,
- flag,
- unflag,
- follow-up overlay,
- multi-select,
- bulk operace.

Na desktopu musí být multi-select ergonomický pro sousedící i nesousedící položky pomocí běžných desktopových zkratek. Web a Android musí mít platformně přirozený ekvivalent.

Drag and drop zprávy mezi složkami znamená **MOVE by default**. Akce **COPY** musí být samostatná explicitní operace.

### 11.6 Historie odpovědi a citační režimy

Při reply a reply all musí systém:

- zachovat historii e-mailu,
- vložit historii do citované podoby pod nově psaný text,
- použít prefix `Re:` pouze tehdy, pokud předmět tento prefix ještě neobsahuje,
- nepřikládat původní přílohy ve výchozím stavu,
- podporovat plain-text i HTML citaci.

Při forward musí systém:

- použít prefix `FW:` pouze tehdy, pokud již předmět odpovídající prefix neobsahuje,
- ve výchozím stavu přenést původní přílohy, pokud tomu nebrání bezpečnostní politika nebo limit provideru.

Výchozí citační režim je **Include original message text**. Nastavení musí umožnit minimálně ještě jednu alternativní citační variantu.

### 11.7 Search folders / virtuální pohledy

Systém musí podporovat alespoň tyto virtuální pohledy:

- Nepřečtené,
- Označené vlajkou,
- S přílohami.

Tyto pohledy jsou čistě virtuální. Nesmí způsobovat fyzický přesun ani duplikaci zpráv.

### 11.8 Vyhledávání a filtrování

Vyhledávání musí být dostupné na webu, desktopu i Androidu.

Musí podporovat minimálně:

- fulltext v předmětu,
- fulltext v těle,
- odesílatele,
- příjemce,
- přesnou frázi v uvozovkách,
- stav přečtení,
- přílohy,
- datum od/do,
- označení vlajkou,
- scope current folder,
- scope current account,
- scope all folders v rámci účtu.

Minimální syntaxe dotazu musí podporovat `AND`, `OR`, `NOT`, přesnou frázi v uvozovkách a filtry typu přílohy nebo read/unread.

Vyhledávání musí běžet serverově. Smí kombinovat nativní možnosti provideru s pomocným indexem, ale výsledky musí být stránkované, stabilně řazené a bez mechanického převzetí libovolných cizích limitů typu „prvních 1000 výsledků“.

### 11.9 Compose, drafty a odesílání

Systém musí podporovat:

- nový e-mail,
- reply/reply all/forward,
- serverově uložené drafty,
- autosave draftu,
- přílohy,
- preview před odesláním,
- validaci příjemců,
- idempotentní odeslání.

Drafty musí být serverově uložené tak, aby byly dostupné napříč klienty. Pokud provider podporuje koncepty vhodným způsobem, smí být implementována synchronizace do provider Drafts, ale autoritativní aplikační draft pro KájovoMail musí být řízen backendem.

#### Povinný MIME formát

Každý odeslaný e-mail musí být vytvořen jako `multipart/alternative` s pořadím:

1. `text/plain; charset=UTF-8`
2. `text/html; charset=UTF-8`

Plain-text i HTML varianta musí vzniknout ze stejného významového zdroje a musí nést stejnou informaci.

#### Povolený rozsah HTML editoru

Editor musí umožnit pouze konzervativní a kompatibilní formátování:

- odstavce,
- tučné,
- podtržení,
- seznamy,
- základní velikosti textu,
- základní zarovnání,
- citace.

Zakázáno je automaticky generovat nebo vkládat:

- externí obrázky,
- inline logo nebo grafický podpis ve výchozím stavu,
- externí fonty,
- JavaScript,
- iframe,
- video,
- formulářové prvky,
- složitý CSS layout,
- animace.

Odchozí e-mail musí být plně srozumitelný i v klientovi, který nezobrazí obrázky.

### 11.10 Přílohy

Přílohy musí být zpracovány jako standardní MIME attachmenty. Přenos a stažení příloh musí být realizovány přes backend a musí být streamované tak, aby se velké soubory nenačítaly celé do paměti klienta ani API procesu, pokud to není nutné.

UI musí před odesláním validovat limity velikosti podle konfigurace účtu nebo provideru.

### 11.11 AI generování odpovědí

#### Umístění v UI

Na desktopu musí být k dispozici pravý úzký panel se sekcemi:

- **Zadání** — pole pro neformální instrukci uživatele,
- **Nabídky** — přehled aktivních nabídek.

Na webu a Androidu může být stejné chování řešeno adaptivně, ale funkční rozsah musí zůstat zachován.

#### Povinné vstupy do AI generování

Backend musí sestavit prompt z těchto vrstev:

1. neměnná systémová pravidla aplikace,
2. administrátorské AI nastavení,
3. uživatelské AI preference v povoleném rozsahu,
4. content bloky,
5. historie aktuálního vlákna,
6. aktuální zpráva a kontext,
7. ad hoc instrukce uživatele.

#### Chování AI

AI musí být instruována tak, aby:

- používala pouze fakta dodaná vstupem,
- nic si nevymýšlela,
- nepracovala s neoznačenými domněnkami,
- vracela zdvořilý, věcný a strukturovaný návrh,
- explicitně označila chybějící fakta,
- nevracela přímo finální svévolné HTML určené k odeslání bez serverové validace.

#### Technologie OpenAI integrace

OpenAI integrace musí splnit tyto podmínky:

- volání pouze ze serveru,
- použití **Responses API**,
- použití **Structured Outputs** nebo ekvivalentně přísného schématu,
- výchozí request policy `store: false`,
- zákaz ukládání API klíče do klientských aplikací,
- zákaz aktivace externích built-in tools v běžném generování odpovědi.

#### Meziformát AI výstupu

AI musí vracet strukturovaný meziformát, ze kterého backend deterministicky vytvoří:

- plain-text variantu,
- HTML variantu,
- preview pro uživatele.

Meziformát musí obsahovat minimálně pole pro jazyk, režim práce s předmětem, předmět, oslovení, bloky těla, závěr, podpis, chybějící fakta a příznak nutnosti lidské revize.

#### Revize před odesláním

Každý AI návrh musí být před odesláním uživatelsky revidovatelný. Uživatel musí mít možnost:

- text upravit,
- změnit předmět,
- doplnit nebo odebrat příjemce,
- upravit vazbu na nabídku,
- generování zahodit,
- odeslání zrušit.

#### Ochrana soukromí při AI

Do OpenAI se standardně odesílá pouze předmět, tělo, historie, nutná metadata, content bloky a uživatelské instrukce. Přílohy se do OpenAI nesmí odesílat automaticky.

### 11.12 Funkce „Nabídky“

Při práci se zprávou nebo při odesílání odpovědi musí být možné označit e-mail jako nabídku.

Systém musí:

- vytvořit nabídku navázanou na thread nebo message,
- uložit stav nabídky,
- zobrazit nabídku v UI jako dlaždici nebo položku panelu,
- umožnit filtraci a rychlý přechod na související komunikaci.

Povinná pole nabídky:

- interní ID,
- vazba na účet,
- vazba na thread nebo message,
- název nabídky,
- výchozí label odvozený ze subjectu nebo odesílatele,
- ručně editovatelný label,
- stav nabídky,
- čas vytvoření a poslední změny,
- identita autora poslední změny.

Povinné stavy nabídky:

- aktivní,
- vyřízená pozitivně,
- vyřízená negativně,
- archivovaná.

Počáteční stav je aktivní. Přechody do uzavřených stavů musí být auditované.

### 11.13 Nastavení aplikace

Aplikace musí obsahovat minimálně tyto sekce nastavení:

- e-mailové účty,
- uživatelské preference,
- AI nastavení v povoleném rozsahu,
- administrátorské OpenAI nastavení,
- bezpečnost a session,
- chování reading pane a citačního režimu.

Sekce OpenAI musí zahrnovat minimálně:

- API klíč spravovaný pouze na serveru,
- test spojení,
- model nebo modelový profil,
- systémová pravidla,
- podpis,
- pravidla formulace odpovědí,
- content bloky.

Klient po uložení nesmí znát plné znění API klíče. V UI se zobrazuje pouze maskovaná hodnota a možnost klíč změnit.

## 12. Uživatelské rozhraní a platformní požadavky

### 12.1 Společná pravidla pro všechny klienty

Všechny klienty musí splnit:

- respekt k manifestu včetně povinné přítomnosti signace,
- použití závazných tokenů a motion pravidel,
- hotové stavy loading, empty, error, offline a všechny další view vyžadované manifestem,
- jednotnou sémantiku akcí a stavů,
- dostupnost minimálně na úrovni WCAG 2.2 AA tam, kde to platforma umožňuje,
- srozumitelnou validaci formulářů,
- čitelné focus stavy,
- zákaz generických placeholder textů v hotovém produktu.

### 12.2 Desktop

Desktop aplikace musí po spuštění nabíhat v maximalizovaném okně a obsahovat minimálně:

- levý panel se seznamem účtů, stromem složek, oblíbenými složkami a virtuálními pohledy,
- střední panel se seznamem zpráv,
- pravý hlavní panel s reading pane a compose zónou,
- pravý úzký panel pro AI zadání a nabídky,
- toolbar pro nové zprávy, reply, reply all, forward, delete, archive, move, mark read/unread, flag, search, filter, settings a refresh.

### 12.3 Web

Webová aplikace musí:

- být dostupná na `mail.hcas.cz`,
- poskytovat funkční paritu s desktopem tam, kde to dává smysl,
- splnit povinné breakpointy z manifestu,
- fungovat výhradně přes HTTPS,
- používat bezpečné cookies nebo jiný ekvivalentní bezpečný session model,
- mít CSRF ochranu tam, kde je relevantní,
- mít rate limiting pro login a další citlivé endpointy,
- vést audit log přihlášení a bezpečnostně významných událostí.

### 12.4 Android

Android aplikace musí být nativní a obsahovat minimálně obrazovky:

- login,
- seznam účtů a složek,
- seznam zpráv,
- detail zprávy,
- compose/reply,
- nastavení,
- AI panel jako bottom sheet, side sheet nebo samostatný screen,
- nabídky.

Android musí respektovat:

- systémové přístupnostní nastavení,
- font scaling,
- dark mode bez porušení pravidel signace,
- reduced-motion ekvivalent,
- bezpečné uložení session tokenu.

## 13. API kontrakty a integrační rozhraní

### 13.1 Obecná pravidla API

Backend musí publikovat OpenAPI specifikaci. Veřejné REST API musí být verzované, doporučeně pod prefixem `/api/v1`.

API musí používat:

- konzistentní validační pravidla,
- standardizovaný error envelope,
- stránkování a stabilní řazení,
- auditovatelné změnové operace,
- idempotency key pro odeslání a další citlivé mutace,
- serverové časové údaje v jednoznačném formátu,
- jasné rozlišení synchronních a asynchronních operací.

### 13.2 Minimální endpointy

OpenAPI musí pokrýt minimálně tyto oblasti:

- autentizace,
- účty,
- složky,
- zprávy,
- vyhledávání,
- drafty,
- AI generování,
- odesílání,
- nabídky,
- uživatelská nastavení,
- event stream / WebSocket.

Minimální sadu endpointů tvoří alespoň:

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `POST /api/v1/auth/change-password`
- `POST /api/v1/auth/request-password-reset`
- `GET /api/v1/accounts`
- `POST /api/v1/accounts`
- `PATCH /api/v1/accounts/{id}`
- `DELETE /api/v1/accounts/{id}`
- `POST /api/v1/accounts/test`
- `GET /api/v1/folders`
- `POST /api/v1/folders`
- `PATCH /api/v1/folders/{id}`
- `DELETE /api/v1/folders/{id}`
- `GET /api/v1/messages`
- `GET /api/v1/messages/{id}`
- `POST /api/v1/messages/search`
- `POST /api/v1/messages/move`
- `POST /api/v1/messages/copy`
- `POST /api/v1/messages/mark-read`
- `POST /api/v1/messages/mark-unread`
- `POST /api/v1/messages/flag`
- `POST /api/v1/messages/unflag`
- `GET /api/v1/search-views`
- `POST /api/v1/drafts`
- `PATCH /api/v1/drafts/{id}`
- `POST /api/v1/ai/generate-reply`
- `POST /api/v1/send`
- `GET /api/v1/offers`
- `PATCH /api/v1/offers/{id}`
- `GET /api/v1/events/ws`

### 13.3 Asynchronní operace

Pro operace jako synchronizace, AI generování a některé odesílací workflow musí systém podporovat stavový model typu:

- queued,
- running,
- succeeded,
- failed,
- canceled.

Klient musí být schopen stav načíst přes REST a dostat notifikaci přes event stream.

## 14. Bezpečnost a ochrana dat

### 14.1 Povinné bezpečnostní principy

Musí být splněno minimálně:

- šifrovaný přenos všech klientů k serveru,
- bezpečné hashování hesel,
- šifrované uložení mail credentials a OpenAI klíče,
- oddělení dat podle identity uživatele,
- role-based access pro administrativní části,
- audit log důležitých akcí,
- možnost odhlášení všech session,
- žádný OpenAI klíč v klientských artefaktech,
- žádné logování tajných údajů a plných message bodies do běžných aplikačních logů.

### 14.2 Logování a audit

Je nutné výslovně odlišit:

- **audit log** — bezpečnostně a provozně významné změny,
- **aplikační log** — technické logy pro provoz,
- **AI request log** — metadata o AI operaci bez úniku citlivého obsahu mimo nutný rozsah.

Každý záznam musí obsahovat korelační identifikátor.

### 14.3 Ochrana webové vrstvy

Web musí mít minimálně:

- HTTPS only,
- bezpečné cookies nebo jiný ekvivalentní session model,
- CSRF ochranu tam, kde je relevantní,
- rate limiting,
- ochranu proti běžným XSS a injection vektorům,
- bezpečnostní hlavičky a konzervativní CSP tam, kde je to kompatibilní s aplikací.

### 14.4 Ochrana AI integrace

- OpenAI klíč je uložen pouze na serveru.
- Produkční default je `store: false`.
- Přílohy se neodesílají automaticky.
- Do AI se nepředávají data mimo nutný rozsah.
- AI výstup je vždy validován proti schématu a aplikačním pravidlům.

## 15. Nefunkční požadavky a provozní kvalita

### 15.1 Výkon a odezva

Řešení musí být navrženo tak, aby běžné operace nepůsobily jako blokující a aby uživatel vždy viděl srozumitelný stav rozpracované operace. Platí zejména:

- listy zpráv a složek musí být stránkované,
- detail zprávy musí být načítán lazy a bezpečně,
- vyhledávání musí vracet první stránku výsledků bez klientského zamrznutí,
- AI generování musí mít viditelný průběh a chybový stav,
- žádná platforma nesmí být závislá na blokujících dlouhých operacích v UI threadu.

### 15.2 Observabilita

Produkční provoz musí poskytovat:

- strukturované logy,
- základní technické metriky,
- měření latencí klíčových endpointů,
- měření úspěšnosti synchronizace, odesílání a AI generování,
- healthcheck a readiness endpointy,
- korelační ID napříč API, workery a integračními voláními.

### 15.3 Migrace a kompatibilita změn

Databázové změny musí být řízeny migracemi. Veřejné API změny musí být zpětně kompatibilní v rámci jedné major verze, nebo musí být explicitně verzované.

### 15.4 Zálohy a obnova

Musí být zdokumentována obnova minimálně pro:

- PostgreSQL,
- konfigurační data,
- AI profily a content bloky,
- auditní záznamy podle retenční politiky.

KájovoMail nezálohuje vzdálený mailbox jako autoritativní zdroj pošty.

### 15.5 Mazání dat

Při smazání účtu nebo uživatele musí systém odstranit nebo anonymizovat vlastní interní data v rozsahu definovaném retenční politikou. Zároveň musí být vyčištěny serverové cache, overlay metadata a pomocné indexy vztahující se k odstraněné entitě.

## 16. Repozitář a cílová struktura

Cílové monorepo musí obsahovat minimálně:

```text
/
├─ brand/
├─ docs/
├─ backend/
├─ web/
├─ desktop/
├─ android/
├─ infra/
├─ scripts/
└─ .github/workflows/
```

Adresář `brand/` musí obsahovat převzaté nebo build procesem zrcadlené assety a metadata dodaná ve vstupním repozitáři. Pokud manifest vyžaduje další cílovou exportní strukturu pro aplikaci, musí být doplněna bez porušení významu a bez změny assetů.

Adresář `docs/` musí obsahovat minimálně:

- tuto finální specifikaci,
- manifest,
- architektonickou dokumentaci,
- OpenAPI specifikaci,
- dokument bezpečnosti,
- dokument nasazení,
- testovací matici.

## 17. Testy, kvalita a release gate

### 17.1 Povinné typy testů

Musí vzniknout minimálně:

- unit testy backendu,
- integrační testy IMAP/POP3/SMTP konektorů,
- testy synchronizace a retry chování,
- testy MIME generování,
- testy AI orchestrace se schema validací,
- API kontraktní testy,
- UI testy webu,
- UI testy desktopu,
- UI testy Androidu,
- brand compliance testy podle manifestu,
- bezpečnostní smoke testy,
- testy kritických error, empty a offline stavů.

### 17.2 Povinné akceptační scénáře

Minimálně musí projít tyto scénáře:

1. Uživatel přidá IMAP účet, test připojení uspěje a načtou se složky.
2. Uživatel přidá POP3 účet a UI zobrazí omezení režimu.
3. Uživatel otevře e-mail, doplní instrukci do AI panelu, vygeneruje odpověď a před odesláním ji upraví.
4. Odeslaná odpověď je vytvořena jako `multipart/alternative` ve správném pořadí částí.
5. Plain-text část je čitelná a neobsahuje HTML značky.
6. HTML část neobsahuje zakázané prvky.
7. Drag and drop přesune zprávu mezi složkami a změna se projeví na serveru.
8. Explicitní copy do složky vytvoří kopii bez smazání zdroje.
9. Reply a reply all nepřenášejí původní přílohy, forward je přenese.
10. System/default složku nelze přejmenovat nebo smazat, pokud provider akci nepovolí.
11. IMAP flag je interoperabilní a rozšířený due date zůstává konzistentně viditelný v KájovoMail.
12. Vyhledávání podporuje exact phrase a logické operátory.
13. Search view je virtuální a neprovádí fyzický přesun zprávy.
14. Nabídka vzniklá z e-mailu je viditelná v panelu Nabídky a její stav lze změnit.
15. Build klientů neobsahuje OpenAI klíč.
16. Produkční request policy posílá do OpenAI `store: false`.
17. Web, desktop i Android sdílejí stejné serverové nastavení a promítají změny přes API.
18. Release selže, pokud chybí povinné brand assety nebo je porušen manifest.

### 17.3 Blokující důvody pro release

Release musí být zablokován, pokud nastane alespoň jedna z následujících situací:

- porušení manifestu,
- chybějící povinné brand assety,
- neprošlé kritické testy,
- chybějící OpenAPI dokumentace,
- přítomnost `TODO`, `TBD`, neimplementovaných stubů nebo placeholder textů v produkčním kódu,
- přímé volání OpenAI z klienta,
- lokální perzistentní databáze pošty na desktopu nebo Androidu,
- výchozí vkládání inline loga nebo externích obrázků do odchozího e-mailu.

## 18. Build a nasazení

### 18.1 Backend

Musí být dodáno:

- Dockerfile,
- Docker Compose pro vývoj,
- migrační skripty,
- `.env.example`,
- produkční konfigurační šablony,
- dokumentace nasazení.

### 18.2 Web

Musí být dodáno:

- build pipeline,
- produkční build,
- konfigurace pro `mail.hcas.cz`,
- dokumentace prostředí a deploye.

### 18.3 Desktop

Musí být dodáno:

- build skripty pro Windows,
- build skripty pro macOS,
- instalační artefakty nebo plně reprodukovatelná build pipeline,
- podepisování artefaktů, pokud je v cílovém prostředí vyžadováno.

### 18.4 Android

Musí být dodáno:

- Android Studio projekt,
- debug build,
- release build pipeline,
- workflow pro APK nebo AAB,
- podpisová a release dokumentace.

## 19. Definice hotového produktu

Produkt je považován za hotový pouze tehdy, pokud současně platí:

1. existuje backend, web, desktop i Android,
2. funguje autentizace, session a správa uživatelů v požadovaném rozsahu,
3. funguje napojení na IMAP/SMTP,
4. funguje omezený POP3 režim s korektně komunikovanými omezeními,
5. funguje práce se složkami a zprávami v IMAP režimu,
6. funguje serverové vyhledávání a virtuální pohledy,
7. fungují drafty a odeslání jako `multipart/alternative`,
8. funguje serverová AI orchestrace a uživatelská revize před odesláním,
9. funguje funkce Nabídky,
10. klienti neukládají perzistentní lokální databázi pošty,
11. brand integrace odpovídá manifestu,
12. existují automatizované testy a release gate,
13. řešení je nasaditelné a zdokumentované,
14. v produkčním kódu ani v UI nejsou placeholdery, neimplementované stuby a provizorní texty.
