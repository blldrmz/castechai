"""Build the translated home pages (cs/, de/, ru/) from index.html.

index.html (English) is the source. Edit the English page, then run:
    python3 tools/build_i18n.py
Each entry in T maps an exact English fragment to its translations.
The script also refreshes the language switcher, hreflang links and sitemap.xml.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://castechai.com"
LANGS = ["en", "cs", "de", "ru"]
OG_LOCALE = {"en": "en_US", "cs": "cs_CZ", "de": "de_DE", "ru": "ru_RU"}
LABEL = {"en": "EN", "cs": "CS", "de": "DE", "ru": "RU"}

T = [
    # head
    ("<title>CasTech AI — Intelligent Casino Table Systems by Virexa</title>", {
        "cs": "<title>CasTech AI — inteligentní systémy pro kasinové stoly od Virexa</title>",
        "de": "<title>CasTech AI — Intelligente Systeme für Casino-Spieltische von Virexa</title>",
        "ru": "<title>CasTech AI — интеллектуальные системы для игровых столов казино от Virexa</title>"}),
    ('content="CasTech AI — Intelligent Casino Table Systems by Virexa"', {
        "cs": 'content="CasTech AI — inteligentní systémy pro kasinové stoly od Virexa"',
        "de": 'content="CasTech AI — Intelligente Systeme für Casino-Spieltische von Virexa"',
        "ru": 'content="CasTech AI — интеллектуальные системы для игровых столов казино от Virexa"'}, 2),
    ('content="CasTech AI develops computer-vision technology for casino table operations, starting with AI-assisted Blackjack monitoring. A Virexa AI Technologies division."', {
        "cs": 'content="CasTech AI vyvíjí technologii počítačového vidění pro provoz kasinových stolů, počínaje monitoringem blackjacku s podporou AI. Divize Virexa AI Technologies."',
        "de": 'content="CasTech AI entwickelt Computer-Vision-Technologie für den Betrieb von Casino-Spieltischen, beginnend mit KI-gestütztem Blackjack-Monitoring. Ein Geschäftsbereich der Virexa AI Technologies."',
        "ru": 'content="CasTech AI разрабатывает технологию компьютерного зрения для работы игровых столов казино, начиная с мониторинга блэкджека с помощью ИИ. Подразделение Virexa AI Technologies."'}, 3),
    # header / nav
    ('aria-label="CasTech AI home"', {"cs": 'aria-label="CasTech AI – úvod"', "de": 'aria-label="CasTech AI – Startseite"', "ru": 'aria-label="CasTech AI – главная"'}),
    ("<small>ARTIFICIAL INTELLIGENCE SYSTEMS</small>", {"cs": "<small>SYSTÉMY UMĚLÉ INTELIGENCE</small>", "de": "<small>KI-SYSTEME</small>", "ru": "<small>СИСТЕМЫ ИСКУССТВЕННОГО ИНТЕЛЛЕКТА</small>"}),
    ('aria-label="Open navigation"', {"cs": 'aria-label="Otevřít menu"', "de": 'aria-label="Menü öffnen"', "ru": 'aria-label="Открыть меню"'}),
    ('aria-label="Main navigation"', {"cs": 'aria-label="Hlavní menu"', "de": 'aria-label="Hauptmenü"', "ru": 'aria-label="Главное меню"'}),
    ('<a href="#about">About</a>', {"cs": '<a href="#about">O nás</a>', "de": '<a href="#about">Über uns</a>', "ru": '<a href="#about">О нас</a>'}),
    ('<a href="#capabilities">Technology</a>', {"cs": '<a href="#capabilities">Technologie</a>', "de": '<a href="#capabilities">Technologie</a>', "ru": '<a href="#capabilities">Технология</a>'}),
    ('<a href="#architecture">System</a>', {"cs": '<a href="#architecture">Systém</a>', "de": '<a href="#architecture">System</a>', "ru": '<a href="#architecture">Система</a>'}),
    ('<a href="#roadmap">Roadmap</a>', {"cs": '<a href="#roadmap">Plán vývoje</a>', "de": '<a href="#roadmap">Roadmap</a>', "ru": '<a href="#roadmap">Дорожная карта</a>'}),
    ('<a href="#company">Principles</a>', {"cs": '<a href="#company">Principy</a>', "de": '<a href="#company">Prinzipien</a>', "ru": '<a href="#company">Принципы</a>'}),
    ('class="nav-cta">Contact ↗</a>', {"cs": 'class="nav-cta">Kontakt ↗</a>', "de": 'class="nav-cta">Kontakt ↗</a>', "ru": 'class="nav-cta">Контакты ↗</a>'}),
    # hero
    ("<span class=\"dot\"></span> COMPUTER VISION FOR LIVE TABLE GAMES</div>", {
        "cs": "<span class=\"dot\"></span> POČÍTAČOVÉ VIDĚNÍ PRO ŽIVÉ STOLNÍ HRY</div>",
        "de": "<span class=\"dot\"></span> COMPUTER VISION FÜR LIVE-TISCHSPIELE</div>",
        "ru": "<span class=\"dot\"></span> КОМПЬЮТЕРНОЕ ЗРЕНИЕ ДЛЯ ЖИВЫХ НАСТОЛЬНЫХ ИГР</div>"}),
    ('<h1 id="heroTitle">Intelligence for <em>every move</em> at the table.</h1>', {
        "cs": '<h1 id="heroTitle">Inteligence pro <em>každý tah</em> u stolu.</h1>',
        "de": '<h1 id="heroTitle">Intelligenz für <em>jeden Zug</em> am Tisch.</h1>',
        "ru": '<h1 id="heroTitle">Интеллект для <em>каждого хода</em> за столом.</h1>'}),
    ("CasTech AI is developing an intelligent computer-vision layer for casino table operations — designed to support real-time event detection, game validation and clearer operational decisions.", {
        "cs": "CasTech AI vyvíjí inteligentní vrstvu počítačového vidění pro provoz kasinových stolů – navrženou pro detekci událostí v reálném čase, kontrolu průběhu hry a jasnější provozní rozhodování.",
        "de": "CasTech AI entwickelt eine intelligente Computer-Vision-Ebene für den Betrieb von Casino-Spieltischen – konzipiert für Ereigniserkennung in Echtzeit, Spielvalidierung und klarere betriebliche Entscheidungen.",
        "ru": "CasTech AI разрабатывает интеллектуальный слой компьютерного зрения для работы игровых столов казино — для распознавания событий в реальном времени, проверки хода игры и более ясных операционных решений."}),
    ('class="btn btn-primary">Explore the technology <span>↗</span>', {
        "cs": 'class="btn btn-primary">Prozkoumat technologii <span>↗</span>',
        "de": 'class="btn btn-primary">Technologie entdecken <span>↗</span>',
        "ru": 'class="btn btn-primary">Узнать о технологии <span>↗</span>'}),
    ('class="btn btn-ghost">Discuss a pilot <span>↗</span>', {
        "cs": 'class="btn btn-ghost">Domluvit pilotní projekt <span>↗</span>',
        "de": 'class="btn btn-ghost">Pilotprojekt besprechen <span>↗</span>',
        "ru": 'class="btn btn-ghost">Обсудить пилотный проект <span>↗</span>'}),
    ("<span>Camera-assisted analytics</span><span>Event-based logic</span><span>Human-led decisions</span>", {
        "cs": "<span>Analytika s kamerami</span><span>Logika založená na událostech</span><span>Rozhoduje člověk</span>",
        "de": "<span>Kameragestützte Analyse</span><span>Ereignisbasierte Logik</span><span>Der Mensch entscheidet</span>",
        "ru": "<span>Аналитика по камерам</span><span>Логика на основе событий</span><span>Решения принимает человек</span>"}),
    ('aria-label="Illustrative casino table monitoring visualization with detected seat activity"', {
        "cs": 'aria-label="Ilustrační vizualizace monitoringu kasinového stolu s detekovanou aktivitou na místech"',
        "de": 'aria-label="Illustrative Darstellung der Tischüberwachung mit erkannter Platzaktivität"',
        "ru": 'aria-label="Иллюстрация мониторинга игрового стола с обнаруженной активностью на местах"'}),
    ("Conceptual interface illustration — not a live detection feed.", {
        "cs": "Koncepční ilustrace rozhraní – nejde o živý přenos detekce.",
        "de": "Konzeptionelle Darstellung der Oberfläche – kein Live-Erkennungsbild.",
        "ru": "Концептуальная иллюстрация интерфейса — не прямая трансляция распознавания."}),
    # about
    ("The approach / 01", {"cs": "Přístup / 01", "de": "Ansatz / 01", "ru": "Подход / 01"}),
    ("See the table.<br>Understand the event.", {"cs": "Vidět stůl.<br>Pochopit událost.", "de": "Den Tisch sehen.<br>Das Ereignis verstehen.", "ru": "Видеть стол.<br>Понимать событие."}),
    ("Casino table operations depend on accuracy, speed and consistent interpretation of fast-moving events.<br><br><strong>CasTech AI aims to turn camera observations into structured, actionable operational signals</strong> — supporting staff while keeping final decisions in human hands.", {
        "cs": "Provoz kasinových stolů stojí na přesnosti, rychlosti a jednotném vyhodnocování rychlých událostí.<br><br><strong>CasTech AI chce proměnit záznam kamer ve strukturované, využitelné provozní signály</strong> – na podporu personálu, přičemž konečné rozhodnutí zůstává v rukou lidí.",
        "de": "Der Betrieb von Casino-Spieltischen hängt von Genauigkeit, Tempo und einer einheitlichen Bewertung schneller Ereignisse ab.<br><br><strong>CasTech AI will Kamerabeobachtungen in strukturierte, nutzbare betriebliche Signale verwandeln</strong> – zur Unterstützung des Personals, während die endgültige Entscheidung beim Menschen bleibt.",
        "ru": "Работа игровых столов казино зависит от точности, скорости и единообразной оценки быстро меняющихся событий.<br><br><strong>CasTech AI стремится превращать наблюдения камер в структурированные операционные сигналы, с которыми можно работать</strong>, — помогая персоналу и оставляя окончательные решения за людьми."}),
    # capabilities
    ("Designed capabilities / 02", {"cs": "Plánované funkce / 02", "de": "Geplante Funktionen / 02", "ru": "Проектируемые функции / 02"}),
    ("Purpose-built table intelligence.", {"cs": "Inteligence navržená pro herní stůl.", "de": "Intelligenz, gebaut für den Spieltisch.", "ru": "Интеллект, созданный для игрового стола."}),
    ("Our development focus is practical table-level analysis, with features introduced and validated by game module. The capabilities below describe the engineering scope, not a claim of completed commercial deployment.", {
        "cs": "Vývoj se soustředí na praktickou analýzu na úrovni stolu; funkce zavádíme a ověřujeme po jednotlivých herních modulech. Níže uvedené funkce popisují technický rozsah, nikoli dokončené komerční nasazení.",
        "de": "Unser Entwicklungsschwerpunkt ist die praktische Analyse auf Tischebene; Funktionen werden je Spielmodul eingeführt und validiert. Die folgenden Funktionen beschreiben den technischen Umfang und sind keine Aussage über einen abgeschlossenen kommerziellen Einsatz.",
        "ru": "Мы сосредоточены на практическом анализе на уровне стола; функции внедряются и проверяются для каждого игрового модуля отдельно. Перечисленные ниже функции описывают технический объём работ, а не завершённое коммерческое внедрение."}),
    ("CAPABILITY / ", {"cs": "FUNKCE / ", "de": "FUNKTION / ", "ru": "ФУНКЦИЯ / "}, 6),
    ("<h3>Seat &amp; Bet Detection</h3><p>Identify active player positions and betting-area activity through camera-based observation.</p>", {
        "cs": "<h3>Detekce míst a sázek</h3><p>Rozpoznání obsazených hráčských míst a aktivity v sázkových polích pomocí kamer.</p>",
        "de": "<h3>Platz- und Einsatzerkennung</h3><p>Erkennung aktiver Spielerplätze und der Aktivität in den Setzfeldern per Kamera.</p>",
        "ru": "<h3>Распознавание мест и ставок</h3><p>Определение занятых мест игроков и активности в зонах ставок с помощью камер.</p>"}),
    ("<h3>Card &amp; Game State Analysis</h3><p>Map detected cards and events to a table-game rules engine for operational checks.</p>", {
        "cs": "<h3>Analýza karet a stavu hry</h3><p>Propojení rozpoznaných karet a událostí s pravidly dané stolní hry pro provozní kontroly.</p>",
        "de": "<h3>Karten- und Spielstandanalyse</h3><p>Abgleich erkannter Karten und Ereignisse mit einer Regel-Engine des Tischspiels für betriebliche Prüfungen.</p>",
        "ru": "<h3>Анализ карт и хода игры</h3><p>Сопоставление распознанных карт и событий с правилами настольной игры для операционных проверок.</p>"}),
    ("<h3>Chip &amp; Payout Verification</h3><p>Developing chip recognition and payout cross-checks to support transaction accuracy.</p>", {
        "cs": "<h3>Kontrola žetonů a výplat</h3><p>Vyvíjíme rozpoznávání žetonů a křížovou kontrolu výplat pro přesnější transakce.</p>",
        "de": "<h3>Chip- und Auszahlungsprüfung</h3><p>Wir entwickeln Chiperkennung und Auszahlungsabgleiche für genauere Transaktionen.</p>",
        "ru": "<h3>Проверка фишек и выплат</h3><p>Разрабатываем распознавание фишек и перекрёстную проверку выплат для точности операций.</p>"}),
    ("<h3>Dealer Error Alerts</h3><p>Flag possible rule deviations or action mismatches for review and timely correction.</p>", {
        "cs": "<h3>Upozornění na chyby krupiéra</h3><p>Označení možných odchylek od pravidel nebo nesouladu akcí ke kontrole a včasné opravě.</p>",
        "de": "<h3>Hinweise auf Dealerfehler</h3><p>Markierung möglicher Regelabweichungen oder unstimmiger Aktionen zur Prüfung und rechtzeitigen Korrektur.</p>",
        "ru": "<h3>Оповещения об ошибках дилера</h3><p>Отметка возможных отклонений от правил или несоответствий действий для проверки и своевременного исправления.</p>"}),
    ("<h3>Visual Table Feedback</h3><p>Coordinate table status, seat indications and operator-facing alert visualizations.</p>", {
        "cs": "<h3>Vizuální zpětná vazba u stolu</h3><p>Sjednocené zobrazení stavu stolu, indikace míst a upozornění pro obsluhu.</p>",
        "de": "<h3>Visuelles Tisch-Feedback</h3><p>Abgestimmte Anzeige von Tischstatus, Platzmarkierungen und Hinweisen für das Personal.</p>",
        "ru": "<h3>Визуальная обратная связь за столом</h3><p>Согласованное отображение статуса стола, индикации мест и оповещений для персонала.</p>"}),
    ("<h3>Modular Game Architecture</h3><p>Extend the computer-vision and rules approach from Blackjack to other table games.</p>", {
        "cs": "<h3>Modulární architektura her</h3><p>Rozšíření přístupu počítačového vidění a pravidel z blackjacku na další stolní hry.</p>",
        "de": "<h3>Modulare Spielarchitektur</h3><p>Übertragung des Computer-Vision- und Regelansatzes von Blackjack auf weitere Tischspiele.</p>",
        "ru": "<h3>Модульная архитектура игр</h3><p>Перенос подхода компьютерного зрения и правил с блэкджека на другие настольные игры.</p>"}),
    # architecture
    ("Architecture / 03", {"cs": "Architektura / 03", "de": "Architektur / 03", "ru": "Архитектура / 03"}),
    ("From pixels to operational context.", {"cs": "Od pixelů k provoznímu kontextu.", "de": "Von Pixeln zum betrieblichen Kontext.", "ru": "От пикселей к операционному контексту."}),
    ("Camera-based observation is only the beginning. CasTech AI is being designed around a clear separation between recognition, game-state interpretation and actionable alerts.", {
        "cs": "Sledování kamerami je jen začátek. CasTech AI je navrženo s jasným oddělením rozpoznávání, vyhodnocení stavu hry a využitelných upozornění.",
        "de": "Die Kamerabeobachtung ist nur der Anfang. CasTech AI wird mit einer klaren Trennung zwischen Erkennung, Interpretation des Spielstands und verwertbaren Hinweisen entwickelt.",
        "ru": "Наблюдение камерами — только начало. CasTech AI проектируется с чётким разделением распознавания, интерпретации хода игры и оповещений, на которые можно реагировать."}),
    ("<h4>Camera input</h4><p>Table and game-area observation through configured camera angles.</p>", {
        "cs": "<h4>Vstup z kamer</h4><p>Sledování stolu a herní plochy z nastavených úhlů kamer.</p>",
        "de": "<h4>Kamera-Input</h4><p>Beobachtung von Tisch und Spielfläche aus konfigurierten Kamerawinkeln.</p>",
        "ru": "<h4>Данные с камер</h4><p>Наблюдение за столом и игровой зоной с настроенных ракурсов камер.</p>"}),
    ("<h4>Vision analysis</h4><p>Detection and classification of relevant cards, chips, zones and movements.</p>", {
        "cs": "<h4>Obrazová analýza</h4><p>Detekce a klasifikace relevantních karet, žetonů, zón a pohybů.</p>",
        "de": "<h4>Bildanalyse</h4><p>Erkennung und Klassifizierung relevanter Karten, Chips, Zonen und Bewegungen.</p>",
        "ru": "<h4>Анализ изображения</h4><p>Обнаружение и классификация карт, фишек, зон и движений.</p>"}),
    ("<h4>Rules &amp; verification</h4><p>Event mapping and cross-checks aligned to the specific game module.</p>", {
        "cs": "<h4>Pravidla a ověření</h4><p>Mapování událostí a křížové kontroly podle konkrétního herního modulu.</p>",
        "de": "<h4>Regeln und Prüfung</h4><p>Ereigniszuordnung und Abgleiche passend zum jeweiligen Spielmodul.</p>",
        "ru": "<h4>Правила и проверка</h4><p>Сопоставление событий и перекрёстные проверки по конкретному игровому модулю.</p>"}),
    ("<h4>Operator feedback</h4><p>Useful visual indicators and reviewable operational alerts.</p>", {
        "cs": "<h4>Zpětná vazba pro obsluhu</h4><p>Užitečné vizuální indikátory a upozornění, která lze zkontrolovat.</p>",
        "de": "<h4>Feedback für das Personal</h4><p>Hilfreiche visuelle Anzeigen und überprüfbare betriebliche Hinweise.</p>",
        "ru": "<h4>Обратная связь для персонала</h4><p>Понятные визуальные индикаторы и оповещения, которые можно проверить.</p>"}),
    # roadmap
    ("Modular development / 04", {"cs": "Modulární vývoj / 04", "de": "Modulare Entwicklung / 04", "ru": "Модульная разработка / 04"}),
    ("One framework.<br>Multiple table games.", {"cs": "Jeden základ.<br>Více stolních her.", "de": "Ein Framework.<br>Viele Tischspiele.", "ru": "Одна платформа.<br>Много настольных игр."}),
    ("Roadmap order reflects planned development priorities. Listed modules are not representations of launched products.", {
        "cs": "Pořadí odpovídá plánovaným prioritám vývoje. Uvedené moduly nejsou uvedené produkty na trhu.",
        "de": "Die Reihenfolge entspricht den geplanten Entwicklungsprioritäten. Die aufgeführten Module sind keine bereits eingeführten Produkte.",
        "ru": "Порядок отражает запланированные приоритеты разработки. Перечисленные модули не являются выпущенными продуктами."}),
    ('<span class="tag focus">Initial development focus</span>', {
        "cs": '<span class="tag focus">Aktuální priorita vývoje</span>',
        "de": '<span class="tag focus">Aktueller Entwicklungsfokus</span>',
        "ru": '<span class="tag focus">Текущий приоритет разработки</span>'}),
    ('<span class="tag">Planned module</span>', {"cs": '<span class="tag">Plánovaný modul</span>', "de": '<span class="tag">Geplantes Modul</span>', "ru": '<span class="tag">Планируемый модуль</span>'}, 7),
    ("<strong>Russian Poker</strong>", {"cs": "<strong>Ruský poker</strong>", "de": "<strong>Russisches Poker</strong>", "ru": "<strong>Русский покер</strong>"}),
    ("<strong>Roulette</strong>", {"cs": "<strong>Ruleta</strong>", "de": "<strong>Roulette</strong>", "ru": "<strong>Рулетка</strong>"}),
    ("<strong>Blackjack</strong>", {"cs": "<strong>Blackjack</strong>", "de": "<strong>Blackjack</strong>", "ru": "<strong>Блэкджек</strong>"}, None),
    # principles
    ("Design principles / 05", {"cs": "Principy návrhu / 05", "de": "Gestaltungsprinzipien / 05", "ru": "Принципы проектирования / 05"}),
    ("Built around operational reality.", {"cs": "Postaveno na skutečném provozu.", "de": "Gebaut für die betriebliche Realität.", "ru": "Создано для реальной работы казино."}),
    ("Our work starts with how casino tables actually operate: rules, staff workflow, accuracy requirements and integration constraints.", {
        "cs": "Vycházíme z toho, jak kasinové stoly skutečně fungují: pravidla, práce personálu, požadavky na přesnost a omezení integrace.",
        "de": "Unsere Arbeit beginnt damit, wie Casino-Spieltische tatsächlich funktionieren: Regeln, Arbeitsabläufe des Personals, Genauigkeitsanforderungen und Integrationsvorgaben.",
        "ru": "Мы исходим из того, как на самом деле работают игровые столы: правила, работа персонала, требования к точности и ограничения интеграции."}),
    ("<h3>Assist, don't obscure</h3><p>Make alerts explainable and give operators the context to verify the observation.</p>", {
        "cs": "<h3>Pomáhat, ne zatemňovat</h3><p>Upozornění musí být srozumitelná a obsluha musí mít kontext, aby mohla zjištění ověřit.</p>",
        "de": "<h3>Unterstützen statt verschleiern</h3><p>Hinweise nachvollziehbar machen und dem Personal den Kontext zur Überprüfung geben.</p>",
        "ru": "<h3>Помогать, а не запутывать</h3><p>Оповещения должны быть понятными, а персонал — иметь контекст для проверки наблюдения.</p>"}),
    ("<h3>Accuracy before scale</h3><p>Validate detection and rules logic systematically before expanding across game types.</p>", {
        "cs": "<h3>Přesnost před rozsahem</h3><p>Detekci a logiku pravidel systematicky ověřujeme dříve, než je rozšíříme na další hry.</p>",
        "de": "<h3>Genauigkeit vor Größe</h3><p>Erkennung und Regellogik systematisch validieren, bevor sie auf weitere Spiele ausgeweitet werden.</p>",
        "ru": "<h3>Точность важнее масштаба</h3><p>Систематически проверяем распознавание и логику правил, прежде чем расширять их на другие игры.</p>"}),
    ("<h3>Purpose-limited camera intelligence</h3><p>Prioritize table events and operational consistency rather than unnecessary personal identification.</p>", {
        "cs": "<h3>Kamerová inteligence s omezeným účelem</h3><p>Přednost mají události u stolu a jednotný provoz, ne zbytečná identifikace osob.</p>",
        "de": "<h3>Zweckgebundene Kameraintelligenz</h3><p>Im Vordergrund stehen Tischereignisse und ein einheitlicher Betrieb, nicht die unnötige Identifizierung von Personen.</p>",
        "ru": "<h3>Камеры только для своей задачи</h3><p>В приоритете события за столом и единообразие работы, а не лишняя идентификация людей.</p>"}),
    ("<h3>Engineered by Virexa</h3><p>CasTech AI is a specialized technology initiative under Virexa AI Technologies.</p>", {
        "cs": "<h3>Vyvinuto společností Virexa</h3><p>CasTech AI je specializovaný technologický projekt společnosti Virexa AI Technologies.</p>",
        "de": "<h3>Entwickelt von Virexa</h3><p>CasTech AI ist eine spezialisierte Technologieinitiative der Virexa AI Technologies.</p>",
        "ru": "<h3>Разработано Virexa</h3><p>CasTech AI — специализированный технологический проект компании Virexa AI Technologies.</p>"}),
    # contact
    ("Contact / 06", {"cs": "Kontakt / 06", "de": "Kontakt / 06", "ru": "Контакты / 06"}),
    ("Talk technology.<br>Build clarity.", {"cs": "Mluvme o technologii.<br>Vneseme jasno.", "de": "Über Technologie sprechen.<br>Klarheit schaffen.", "ru": "Поговорим о технологии.<br>Внесём ясность."}),
    ("For development partnerships, pilot discussions and technical inquiries, reach our team directly.", {
        "cs": "Ohledně vývojových partnerství, pilotních projektů a technických dotazů nás kontaktujte přímo.",
        "de": "Für Entwicklungspartnerschaften, Pilotprojekte und technische Anfragen erreichen Sie unser Team direkt.",
        "ru": "По вопросам партнёрства в разработке, пилотных проектов и техническим вопросам обращайтесь к нам напрямую."}),
    ("CASTECH AI · BUSINESS INQUIRIES", {"cs": "CASTECH AI · OBCHODNÍ DOTAZY", "de": "CASTECH AI · GESCHÄFTSANFRAGEN", "ru": "CASTECH AI · ДЕЛОВЫЕ ЗАПРОСЫ"}),
    ('Pilot%20Discussion">Discuss a pilot <span>↗</span>', {
        "cs": 'Pilot%20Discussion">Domluvit pilotní projekt <span>↗</span>',
        "de": 'Pilot%20Discussion">Pilotprojekt besprechen <span>↗</span>',
        "ru": 'Pilot%20Discussion">Обсудить пилотный проект <span>↗</span>'}),
    ("CasTech AI is a development initiative of Virexa AI Technologies s.r.o. (IČO 29716055), Cihlářská 782/10a, Prosek, 190 00 Praha 9, Czech Republic. General group information is available at", {
        "cs": "CasTech AI je vývojový projekt společnosti Virexa AI Technologies s.r.o. (IČO 29716055), Cihlářská 782/10a, Prosek, 190 00 Praha 9, Česká republika. Informace o skupině najdete na",
        "de": "CasTech AI ist eine Entwicklungsinitiative der Virexa AI Technologies s.r.o. (IČO 29716055), Cihlářská 782/10a, Prosek, 190 00 Praha 9, Tschechische Republik. Informationen zur Gruppe finden Sie unter",
        "ru": "CasTech AI — проект в разработке компании Virexa AI Technologies s.r.o. (IČO 29716055), Cihlářská 782/10a, Prosek, 190 00 Praha 9, Чешская Республика. Информация о группе — на сайте"}),
    # footer
    ("Virexa AI Technologies</a> division</span>", {"cs": "Virexa AI Technologies</a> – divize</span>", "de": "Virexa AI Technologies</a> – Geschäftsbereich</span>", "ru": "Virexa AI Technologies</a> – подразделение</span>"}),
    (" · A <a href=\"https://virexa-tech.com\"", {"cs": " · <a href=\"https://virexa-tech.com\"", "de": " · <a href=\"https://virexa-tech.com\"", "ru": " · <a href=\"https://virexa-tech.com\""}),
    ("Cihlářská 782/10a, Prosek, 190 00 Praha 9, Czech Republic</div>", {
        "cs": "Cihlářská 782/10a, Prosek, 190 00 Praha 9, Česká republika</div>",
        "de": "Cihlářská 782/10a, Prosek, 190 00 Praha 9, Tschechische Republik</div>",
        "ru": "Cihlářská 782/10a, Prosek, 190 00 Praha 9, Чешская Республика</div>"}),
    ('<a href="#top">Back to top ↑</a><a href="/privacy.html">Privacy Policy</a><a href="/terms.html">Terms &amp; Conditions</a>', {
        "cs": '<a href="#top">Nahoru ↑</a><a href="/privacy.html">Ochrana osobních údajů (EN)</a><a href="/terms.html">Obchodní podmínky (EN)</a>',
        "de": '<a href="#top">Nach oben ↑</a><a href="/privacy.html">Datenschutz (EN)</a><a href="/terms.html">AGB (EN)</a>',
        "ru": '<a href="#top">Наверх ↑</a><a href="/privacy.html">Политика конфиденциальности (EN)</a><a href="/terms.html">Условия (EN)</a>'}),
    ('<a href="mailto:info@castechai.com">Contact</a></div>', {"cs": '<a href="mailto:info@castechai.com">Kontakt</a></div>', "de": '<a href="mailto:info@castechai.com">Kontakt</a></div>', "ru": '<a href="mailto:info@castechai.com">Контакты</a></div>'}),
]


def path(lang):
    return "/" if lang == "en" else f"/{lang}/"


def alternates():
    tags = [f'<link rel="alternate" hreflang="{l}" href="{SITE}{path(l)}">' for l in LANGS]
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/">')
    return "<!--alt-->" + "\n  ".join(tags) + "<!--/alt-->"


def switcher(cur):
    links = "".join(
        f'<a href="{path(l)}" hreflang="{l}" lang="{l}"' + (' aria-current="true"' if l == cur else "") + f">{LABEL[l]}</a>"
        for l in LANGS)
    names = {"en": "Language", "cs": "Jazyk", "de": "Sprache", "ru": "Язык"}
    return f'<!--lang--><div class="lang" role="group" aria-label="{names[cur]}">{links}</div><!--/lang-->'


def common(html, lang):
    html = re.sub(r"<!--alt-->.*?<!--/alt-->", alternates(), html, flags=re.S)
    html = re.sub(r"<!--lang-->.*?<!--/lang-->", switcher(lang), html, flags=re.S)
    return html


def translate(src, lang):
    out = src
    for entry in T:
        en, tr = entry[0], entry[1]
        n = entry[2] if len(entry) > 2 else 1
        found = out.count(en)
        if n is not None and found != n:
            raise SystemExit(f"[{lang}] expected {n}x, found {found}x: {en[:70]}")
        out = out.replace(en, tr[lang])
    out = out.replace('<html lang="en">', f'<html lang="{lang}">', 1)
    out = out.replace(f'<link rel="canonical" href="{SITE}/">', f'<link rel="canonical" href="{SITE}{path(lang)}">', 1)
    out = out.replace(f'<meta property="og:url" content="{SITE}/">', f'<meta property="og:url" content="{SITE}{path(lang)}">', 1)
    out = out.replace('<meta property="og:locale" content="en_US">', f'<meta property="og:locale" content="{OG_LOCALE[lang]}">', 1)
    return common(out, lang)


def main():
    src_path = ROOT / "index.html"
    src = common(src_path.read_text(encoding="utf-8"), "en")
    if '<meta property="og:locale"' not in src:
        src = src.replace('<meta property="og:type" content="website">',
                          '<meta property="og:type" content="website">\n  <meta property="og:locale" content="en_US">', 1)
    src_path.write_text(src, encoding="utf-8")
    for lang in LANGS[1:]:
        d = ROOT / lang
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(translate(src, lang), encoding="utf-8")
    urls = [path(l) for l in LANGS] + ["/privacy.html", "/terms.html"]
    body = "\n".join(f"<url><loc>{SITE}{u}</loc></url>" for u in urls)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n', encoding="utf-8")
    print("built:", ", ".join(LANGS))


if __name__ == "__main__":
    main()
