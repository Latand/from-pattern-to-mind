# -*- coding: utf-8 -*-
# Single source of truth for the trilingual (EN/UK/RU) build.
# Regenerates index.html (prose + diagram with 3 language layers) and i18n.js.
import json

BLUE="#8AB4F8"; MINT="#5EEAD4"; PURP="#B79CF0"; GOLD="#F4C77B"
SUB="#9AA6CC"; INK="#FFFFFF"; FILL="#141C32"
W,H=2080,1300
LANGS=["en","uk","ru"]

def esc(s): return s.replace("&","&amp;")

# ================= DIAGRAM DATA (geometry language-independent) =================
NH=58
N = {
 'pattern':   dict(x=340,  y=655, w=210, c=MINT, origin=True),
 'attractor': dict(x=720,  y=655, w=226, c=BLUE),
 'form':      dict(x=1085, y=655, w=210, c=BLUE),
 'agency':    dict(x=1445, y=655, w=200, c=BLUE),
 'mind':      dict(x=1790, y=655, w=200, c=BLUE),
 'compression':dict(x=340, y=415, w=210, c=BLUE),
 'dynstab':   dict(x=720,  y=415, w=238, c=BLUE),
 'time':      dict(x=1085, y=415, w=178, c=BLUE),
 'compute':   dict(x=1445, y=415, w=224, c=BLUE),
 'beauty':    dict(x=340,  y=195, w=196, c=MINT),
 'possible':  dict(x=900,  y=180, w=228, c=PURP),
 'logic':     dict(x=1360, y=180, w=216, c=BLUE),
 'isreal':    dict(x=340,  y=895, w=200, c=BLUE),
 'reality':   dict(x=340,  y=1095,w=234, c=BLUE),
 'existence': dict(x=720,  y=895, w=198, c=BLUE),
 'attrtypes': dict(x=1085, y=895, w=252, c=MINT),
 'ideaattr':  dict(x=1455, y=895, w=216, c=MINT),
 'scale':     dict(x=1085, y=1095,w=244, c=PURP),
 'selection': dict(x=1795, y=895, w=210, c=PURP),
 'ourrole':   dict(x=1820, y=1095,w=226, c=PURP),
}
NODE_ORDER=list(N.keys())

E = [
 ('pattern','attractor',BLUE,False,True,0.5),
 ('attractor','form',BLUE,False,True,0.5),
 ('form','agency',BLUE,False,True,0.5),
 ('agency','mind',BLUE,False,True,0.5),
 ('pattern','compression',BLUE,False,False,0.5),
 ('attractor','dynstab',BLUE,False,False,0.5),
 ('form','time',BLUE,False,False,0.5),
 ('agency','compute',BLUE,False,False,0.5),
 ('compression','beauty',MINT,False,False,0.5),
 ('logic','possible',PURP,True,False,0.5),
 ('possible','pattern',PURP,True,False,0.74),
 ('possible','form',PURP,True,False,0.66),
 ('pattern','isreal',BLUE,False,False,0.5),
 ('reality','isreal',BLUE,False,False,0.5),
 ('attractor','existence',BLUE,False,False,0.5),
 ('form','attrtypes',MINT,False,False,0.5),
 ('mind','ideaattr',MINT,False,False,0.5),
 ('ideaattr','attractor',MINT,False,False,0.6),
 ('mind','selection',PURP,True,False,0.5),
 ('selection','ourrole',PURP,True,False,0.5),
 ('scale','selection',PURP,True,False,0.46),
]
PILL_POS=[(575,108),(1360,96),(520,778),(1632,778)]

# ---- diagram label translations ----
NODE_T={
 'en':{'pattern':'PATTERN','attractor':'ATTRACTOR','form':'FORM','agency':'AGENCY','mind':'MIND',
  'compression':'COMPRESSION','dynstab':'DYNAMICAL STABILITY','time':'TIME','compute':'COMPUTE',
  'beauty':'BEAUTY','possible':'POSSIBLE PATTERNS','logic':'LOGIC','isreal':'IS IT REAL?',
  'reality':'REALITY CONSTRAINT','existence':'EXISTENCE','attrtypes':'ATTRACTOR TYPES',
  'ideaattr':'IDEA ATTRACTORS','scale':'SCALE CONFLICT','selection':'SELECTION','ourrole':'OUR ROLE'},
 'uk':{'pattern':'ПАТЕРН','attractor':'АТРАКТОР','form':'ФОРМА','agency':'АГЕНТНІСТЬ','mind':'РОЗУМ',
  'compression':'СТИСНЕННЯ','dynstab':'ДИНАМІЧНА СТІЙКІСТЬ','time':'ЧАС','compute':'ОБЧИСЛЕННЯ',
  'beauty':'КРАСА','possible':'МОЖЛИВІ ПАТЕРНИ','logic':'ЛОГІКА','isreal':'ЦЕ РЕАЛЬНЕ?',
  'reality':'ОБМЕЖЕННЯ ДІЙСНІСТЮ','existence':'ІСНУВАННЯ','attrtypes':'ТИПИ АТРАКТОРІВ',
  'ideaattr':'АТРАКТОРИ ІДЕЙ','scale':'КОНФЛІКТ МАСШТАБІВ','selection':'ВИБІР','ourrole':'НАША РОЛЬ'},
 'ru':{'pattern':'ПАТТЕРН','attractor':'АТТРАКТОР','form':'ФОРМА','agency':'АГЕНТНОСТЬ','mind':'РАЗУМ',
  'compression':'СЖАТИЕ','dynstab':'ДИНАМИЧЕСКАЯ УСТОЙЧИВОСТЬ','time':'ВРЕМЯ','compute':'ВЫЧИСЛЕНИЕ',
  'beauty':'КРАСОТА','possible':'ВОЗМОЖНЫЕ ПАТТЕРНЫ','logic':'ЛОГИКА','isreal':'ЭТО РЕАЛЬНО?',
  'reality':'ОГРАНИЧЕНИЕ РЕАЛЬНОСТЬЮ','existence':'СУЩЕСТВОВАНИЕ','attrtypes':'ТИПЫ АТТРАКТОРОВ',
  'ideaattr':'АТТРАКТОРЫ ИДЕЙ','scale':'КОНФЛИКТ МАСШТАБОВ','selection':'ВЫБОР','ourrole':'НАША РОЛЬ'},
}
NODE_S={
 'en':{'pattern':'compressible by a model','attractor':'stable region in state-space','form':'attractor realized in matter',
  'agency':'a defended pattern','mind':'models possible patterns','compression':'pattern as description',
  'dynstab':'pattern as return','time':'pattern unfolding','compute':'substrate-general; cells compute',
  'beauty':'compression progress','possible':'what could be · Platonic?','logic':'first filter: non-contradiction',
  'isreal':'recoverable + predictive','reality':'reality pushes back','existence':'pattern that persists',
  'attrtypes':'cell fate · phenotypes · neurotypes?','ideaattr':'patterns in idea-space',
  'scale':'local attractor, global harm','selection':'which to realize?','ourrole':'search · test · choose · realize'},
 'uk':{'pattern':'стискуваний моделлю','attractor':'стійка зона у просторі станів','form':'атрактор, втілений у матерії',
  'agency':'захищений патерн','mind':'моделює можливі патерни','compression':'патерн як опис',
  'dynstab':'патерн як повернення до рівноваги','time':'патерн, що розгортається','compute':'поза субстратом; клітини теж обчислюють',
  'beauty':'поступ стиснення','possible':'те, що могло б бути · платонізм?','logic':'перший фільтр: несуперечність',
  'isreal':'відтворюваність + передбачуваність','reality':'дійсність чинить спротив','existence':'патерн, що триває',
  'attrtypes':'доля клітини · фенотипи · нейротипи?','ideaattr':'патерни у просторі ідей',
  'scale':'локальна стійкість, шкода для цілого','selection':'що втілювати?','ourrole':'шукати·перевіряти·обирати·втілювати'},
 'ru':{'pattern':'сжимается моделью','attractor':'устойчивая зона в пространстве состояний','form':'аттрактор, воплощённый в материи',
  'agency':'защищённый паттерн','mind':'моделирует возможные паттерны','compression':'паттерн как описание',
  'dynstab':'паттерн как возврат','time':'разворачивание паттерна','compute':'клетки тоже вычисляют',
  'beauty':'прогресс сжатия','possible':'то, что могло бы быть · платонизм?','logic':'первый фильтр: непротиворечивость',
  'isreal':'воспроизводимо + предсказывает','reality':'реальность сопротивляется','existence':'паттерн, который длится',
  'attrtypes':'судьба клетки · фенотипы · нейротипы?','ideaattr':'паттерны в пространстве идей',
  'scale':'локальный аттрактор, вред для целого','selection':'что воплощать?','ourrole':'искать·проверять·выбирать·воплощать'},
}
EDGE_L={
 'en':['becomes stable','realized in matter','defended under load','modeled by','seen as','seen as','unfolds in','runs on',
  'felt as','bounds the possible','options','could-be','is it real?','corrects','persists as','comes in kinds',
  'lives in minds','a kind of attractor','must choose','falls to us','forces the choice'],
 'uk':['стає стійким','втілюється в матерії','захищається під тиском','моделюється','постає як','постає як','розгортається у','працює на',
  'відчувається як','окреслює можливе','варіанти','могло б бути','чи це реальне?','виправляє','триває як','буває різних видів',
  'живе в розумах','різновид атрактора','мусить обирати','лягає на нас','продиктовує вибір'],
 'ru':['становится устойчивым','воплощается в материи','защищается под нагрузкой','моделируется','предстаёт как','предстаёт как','разворачивается во','работает на',
  'ощущается как','очерчивает возможное','варианты','могло бы быть','реально ли это?','исправляет','длится как','бывает разных видов',
  'живёт в умах','разновидность аттрактора','должен выбирать','ложится на нас','вынуждает выбирать'],
}
PILL_L={
 'en':['Beauty = felt ingression?','Logic: frame or ground?','Mind, or world?','Threshold or gradient?'],
 'uk':['Краса = відчуте входження форми?','Логіка: рамка чи основа?','Розум чи світ?','Поріг чи градієнт?'],
 'ru':['Красота = ощущаемое вхождение формы?','Логика: рамка или основа?','Разум или мир?','Порог или градиент?'],
}
LEG_L={
 'en':['defensible','plausible analogy','speculative / normative','open question'],
 'uk':['обґрунтоване','правдоподібна аналогія','спекулятивне / нормативне','відкрите питання'],
 'ru':['обоснованное','правдоподобная аналогия','спекулятивное / нормативное','открытый вопрос'],
}
LEG_TITLE={'en':'LAYERS','uk':'ШАРИ','ru':'СЛОИ'}
HDR_TITLE={'en':'From Pattern to Mind','uk':'Від патерну до розуму','ru':'От паттерна к разуму'}
HDR_SUB={'en':'logic ▸ pattern ▸ attractor ▸ form ▸ agency ▸ mind',
 'uk':'логіка ▸ патерн ▸ атрактор ▸ форма ▸ агентність ▸ розум',
 'ru':'логика ▸ паттерн ▸ аттрактор ▸ форма ▸ агентность ▸ разум'}
CAP_L={
 'en':'↻ this map is itself an idea-attractor — a compression to test against reality, then drop where it fails.',
 'uk':'↻ ця мапа й сама є ідеєю-атрактором — стисненням, яке варто перевірити дійсністю і відкинути там, де воно не справджується.',
 'ru':'↻ эта карта и сама — идея-аттрактор: сжатие, которое стоит проверить действительностью и отбросить там, где оно не работает.',
}

def border(n, tx, ty):
    cx,cy=n['x'],n['y']; hw=n['w']/2+9; hh=NH/2+9
    dx,dy=tx-cx,ty-cy
    if dx==0 and dy==0: return cx,cy
    sx=hw/abs(dx) if dx else 9e9; sy=hh/abs(dy) if dy else 9e9
    s=min(sx,sy)
    return cx+dx*s, cy+dy*s

def build_svg():
    out=[]; A=out.append
    A('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Calibri, Segoe UI, sans-serif" role="img" aria-labelledby="diagram-title diagram-desc">'%(W,H,W,H))
    A('<title id="diagram-title">From Pattern to Mind &mdash; concept map</title>')
    A('<desc id="diagram-desc">A left-to-right spine reads pattern, attractor, form, agency, mind, with lenses and tests linked by arrows. Colour marks how much weight each claim bears.</desc>')
    A('<rect width="%d" height="%d" fill="#0B1020"/>'%(W,H))
    # static stars (fixed, copied from prior seed render)
    stars=[(683,328,1.3,'#93A0C4'),(118,168,1.6,BLUE),(768,1213,1.0,'#93A0C4'),(459,96,1.0,MINT),(876,163,1.0,BLUE),
     (1148,889,1.0,'#93A0C4'),(273,477,1.6,'#93A0C4'),(1213,146,1.6,'#93A0C4'),(832,121,1.0,BLUE),(1160,292,1.3,MINT),
     (315,1127,1.0,'#93A0C4'),(651,1167,1.6,BLUE),(231,1211,1.6,'#93A0C4'),(404,782,1.0,'#93A0C4'),(1478,148,1.6,BLUE),
     (1287,441,1.3,'#93A0C4'),(1108,895,1.3,MINT),(1219,948,1.3,MINT),(528,388,1.6,BLUE),(187,1196,1.3,'#93A0C4'),
     (1033,723,1.6,MINT),(609,1267,1.0,BLUE),(1068,876,1.0,MINT),(331,1021,1.3,BLUE),(1990,178,1.6,'#93A0C4'),
     (1636,662,1.3,'#93A0C4'),(737,1237,1.3,'#93A0C4'),(1652,954,1.0,BLUE),(1954,572,1.3,'#93A0C4'),(1380,153,1.0,'#93A0C4'),
     (1456,654,1.6,'#93A0C4'),(2053,932,1.3,'#93A0C4'),(810,730,1.0,MINT),(747,364,1.6,BLUE)]
    for x,y,r,c in stars:
        A('<circle cx="%d" cy="%d" r="%.1f" fill="%s" opacity="0.10"/>'%(x,y,r,c))
    A('<defs>')
    for name,col in [('b',BLUE),('m',MINT),('p',PURP),('g',GOLD)]:
        A('<marker id="ar-%s" markerWidth="13" markerHeight="13" refX="9" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L9,4 L0,8 z" fill="%s"/></marker>'%(name,col))
    A('</defs>')
    A('<rect x="150" y="624" width="1810" height="62" rx="31" fill="#0E1733" opacity="0.45"/>')
    mk={BLUE:'b',MINT:'m',PURP:'p',GOLD:'g'}
    # ---- shared geometry: edge lines + label anchor positions, node rects, legend lines ----
    edge_pos=[]
    for src,dst,col,dashed,thick,t in E:
        a=N[src]; b=N[dst]
        x1,y1=border(a,b['x'],b['y']); x2,y2=border(b,a['x'],a['y'])
        w = 3.0 if thick else 1.7
        op = 0.85 if thick else (0.5 if dashed else 0.6)
        dash=' stroke-dasharray="6,6"' if dashed else ''
        A('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" opacity="%.2f"%s marker-end="url(#ar-%s)"/>'%(x1,y1,x2,y2,col,w,op,dash,mk[col]))
        lx=x1+(x2-x1)*t; ly=y1+(y2-y1)*t
        edge_pos.append((lx,ly,col))
    for k in NODE_ORDER:
        n=N[k]; x=n['x']-n['w']/2; y=n['y']-NH/2
        sw = 2.6 if n.get('origin') else 1.7
        A('<rect x="%.0f" y="%.0f" width="%d" height="%d" rx="11" fill="%s" stroke="%s" stroke-width="%.1f"/>'%(x,y,n['w'],NH,FILL,n['c'],sw))
    lx0=44; ly0=1150
    yy=ly0+18
    leg_dash=[False,False,True,True]; leg_col=[BLUE,MINT,PURP,GOLD]
    leg_y=[]
    for i in range(4):
        dash=' stroke-dasharray="4,4"' if leg_dash[i] else ''
        A('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.6"%s/>'%(lx0,yy,lx0+28,yy,leg_col[i],dash))
        leg_y.append(yy); yy+=18
    # ---- per-language text layers ----
    for lang in LANGS:
        disp='' if lang=='en' else ' style="display:none"'
        A('<g class="dgroup" data-lang="%s"%s>'%(lang,disp))
        A('<text x="40" y="50" fill="#FFFFFF" font-size="25" font-weight="700" font-family="Georgia, serif">%s</text>'%esc(HDR_TITLE[lang]))
        A('<text x="40" y="74" fill="#93A0C4" font-size="13">%s</text>'%esc(HDR_SUB[lang]))
        # nodes
        for k in NODE_ORDER:
            n=N[k]; t=NODE_T[lang][k]; s=NODE_S[lang][k]
            tl=len(t); fs=15 if tl<=12 else (13 if tl<=17 else 12)
            A('<text x="%d" y="%d" fill="%s" font-size="%d" font-weight="700" text-anchor="middle">%s</text>'%(n['x'],n['y']-3,INK,fs,esc(t)))
            A('<text x="%d" y="%d" fill="%s" font-size="11" text-anchor="middle" font-style="italic">%s</text>'%(n['x'],n['y']+15,SUB,esc(s)))
        # edge labels
        for i,(lx,ly,col) in enumerate(edge_pos):
            lab=EDGE_L[lang][i]; tw=len(lab)*5.9+16
            A('<rect x="%.1f" y="%.1f" width="%.1f" height="18" rx="5" fill="#0B1020" opacity="0.92"/>'%(lx-tw/2,ly-9,tw))
            A('<text x="%.1f" y="%.1f" fill="%s" font-size="10.5" text-anchor="middle">%s</text>'%(lx,ly+3.5,col,esc(lab)))
        # pills
        for i,(px,py) in enumerate(PILL_POS):
            txt=PILL_L[lang][i]; pw=len(txt)*6.0+24
            A('<rect x="%.1f" y="%.1f" width="%.1f" height="28" rx="14" fill="#1A1530" stroke="%s" stroke-width="1.3"/>'%(px-pw/2,py-14,pw,GOLD))
            A('<text x="%.1f" y="%.1f" fill="%s" font-size="11.5" text-anchor="middle">%s</text>'%(px,py+4,GOLD,esc(txt)))
        # legend
        A('<text x="%d" y="%d" fill="#93A0C4" font-size="12" font-weight="700">%s</text>'%(lx0,ly0,esc(LEG_TITLE[lang])))
        for i in range(4):
            A('<text x="%d" y="%d" fill="#CDD6F0" font-size="11.5">%s</text>'%(lx0+36,leg_y[i]+3,esc(LEG_L[lang][i])))
        A('<text x="%d" y="1262" fill="#93A0C4" font-size="12" text-anchor="end" font-style="italic">%s</text>'%(W-40,esc(CAP_L[lang])))
        A('</g>')
    A('</svg>')
    return "\n".join(out)

# ================= PROSE / UI STRINGS =================
# D[key] = {en, uk, ru}. Values are HTML (innerHTML). Natural translations, no calque.
D = {}
def add(k,en,uk,ru): D[k]={'en':en,'uk':uk,'ru':ru}

add('doc.title','From Pattern to Mind','Від патерну до розуму','От паттерна к разуму')
add('eyebrow','A thinking map &middot; philosophy of mind',
 'Мапа для мислення &middot; філософія свідомості',
 'Карта для мышления &middot; философия сознания')
add('h1','From Pattern <em>to</em> Mind','Від патерну <em>до</em> розуму','От паттерна <em>к</em> разуму')
add('dek','A working model of how structure becomes stable, then alive, then felt, and how the same machinery can turn an idea into a trap.',
 'Робоча модель того, як структура стає стійкою, потім живою, потім відчутою &mdash; і як той самий механізм здатен обернути ідею на пастку.',
 'Рабочая модель того, как структура становится устойчивой, потом живой, потом переживаемой &mdash; и как тот же механизм способен превратить идею в ловушку.')
add('mode.short','Concise','Стисло','Кратко')
add('mode.full','Full','Розгорнуто','Подробно')

add('lede.short',
 'I built this map to think with. The wager: take pattern as the primitive and see how far one ladder climbs &mdash; from bare structure, to agents that defend it, to minds that model what they could become. A pattern is anything you can describe more briefly than its instances. Where the climb stops says as much as where it holds.',
 'Цю мапу я зробив, щоб нею думати. Ставка проста: узяти патерн за вихідне поняття й подивитися, як високо здіймаються одні сходи &mdash; від голої структури до агентів, що її обороняють, і до розумів, які уявляють, чим іще можуть стати. Патерн &mdash; це будь-що, що можна описати коротше, ніж його прояви. Там, де сходи уриваються, видно не менше, ніж там, де вони тримають.',
 'Эту карту я сделал, чтобы ею думать. Ставка проста: взять паттерн за исходное понятие и посмотреть, как высоко ведёт одна лестница &mdash; от голой структуры к агентам, что её отстаивают, и к разумам, которые представляют, чем ещё могут стать. Паттерн &mdash; это всё, что можно описать короче, чем его проявления. Там, где подъём обрывается, видно не меньше, чем там, где он держит.')
add('lede.full',
 'I have been building this map to think with. The wager is plain: I take pattern as the primitive and see how far one ladder climbs, from bare structure to agents that defend it. Where the climb stops is as informative as where it holds. Many things we keep in separate drawers &mdash; physical form, biological agency, beauty, mind, ideology &mdash; turn out to live on that ladder. A pattern, here, is a regularity you can describe more briefly than the list of its instances, relative to some model or code. A sine wave, a crystal lattice, an octave, a morphogenetic field: each is a short description standing in for something that would otherwise take forever to write down.',
 'Цю мапу я роблю, щоб нею думати. Ставка пряма: беру патерн за вихідне поняття й дивлюся, як високо здіймаються одні сходи &mdash; від голої структури до агентів, що її обороняють. Там, де підйом уривається, видно не менше, ніж там, де він тримає. Чимало речей, які ми тримаємо по різних шухлядах &mdash; фізична форма, біологічна агентність, краса, розум, ідеологія, &mdash; зрештою живуть на цих самих сходах. Патерн тут &mdash; це закономірність, яку можна описати коротше за перелік її проявів, відносно якоїсь моделі чи коду. Синусоїда, кристалічна ґратка, октава, морфогенетичне поле: кожне &mdash; короткий опис, що заступає те, на що інакше пішла б ціла вічність.',
 'Эту карту я строю, чтобы ею думать. Ставка прямая: беру паттерн за исходное понятие и смотрю, как высоко ведёт одна лестница &mdash; от голой структуры к агентам, что её отстаивают. Там, где подъём обрывается, видно не меньше, чем там, где он держит. Многое, что мы держим по разным полкам &mdash; физическая форма, биологическая агентность, красота, разум, идеология, &mdash; в итоге живёт на этой же лестнице. Паттерн здесь &mdash; это закономерность, которую можно описать короче, чем перечень её проявлений, относительно некоторой модели или кода. Синусоида, кристаллическая решётка, октава, морфогенетическое поле: каждое &mdash; короткое описание, заменяющее то, на что иначе ушла бы вечность.')

# figure UI
add('maphint','drag to pan &middot; scroll or pinch to zoom &middot; double-click to reset',
 'тягни, щоб рухати &middot; колесо чи щипок &mdash; масштаб &middot; подвійний клік скидає',
 'тяни, чтобы двигать &middot; колесо или щипок &mdash; масштаб &middot; двойной клик сбрасывает')
add('map.reset','reset','скинути','сброс')
add('legend.hard','defensible','обґрунтоване','обоснованное')
add('legend.bridge','plausible analogy','правдоподібна аналогія','правдоподобная аналогия')
add('legend.spec','speculative / normative','спекулятивне / нормативне','спекулятивное / нормативное')
add('legend.open','open question','відкрите питання','открытый вопрос')
add('fig.caption',
 'From Pattern to Mind. The spine reads left to right: a pattern becomes an attractor, an attractor becomes a form, a defended form becomes agency, and a modeling agent becomes a mind. Color marks how much weight each claim can bear.',
 'Від патерну до розуму. Хребет читається зліва направо: патерн стає атрактором, атрактор &mdash; формою, захищена форма &mdash; агентністю, а агент, що моделює, &mdash; розумом. Колір показує, яку вагу витримує кожне твердження.',
 'От паттерна к разуму. Хребет читается слева направо: паттерн становится аттрактором, аттрактор &mdash; формой, защищённая форма &mdash; агентностью, а моделирующий агент &mdash; разумом. Цвет показывает, какой вес выдерживает каждое утверждение.')

# kickers
add('k.ladder','<span class="dot"></span>The ladder','<span class="dot"></span>Сходи','<span class="dot"></span>Лестница')
add('k.logic','<span class="dot"></span>Logic','<span class="dot"></span>Логіка','<span class="dot"></span>Логика')
add('k.agency','<span class="dot"></span>Agency','<span class="dot"></span>Агентність','<span class="dot"></span>Агентность')
add('k.compute','<span class="dot"></span>Compute','<span class="dot"></span>Обчислення','<span class="dot"></span>Вычисление')
add('k.beauty','<span class="dot"></span>Beauty','<span class="dot"></span>Краса','<span class="dot"></span>Красота')
add('k.reality','<span class="dot"></span>Reality','<span class="dot"></span>Реальність','<span class="dot"></span>Реальность')
add('k.existence','<span class="dot"></span>Existence','<span class="dot"></span>Існування','<span class="dot"></span>Существование')
add('k.ideas','<span class="dot"></span>Ideas','<span class="dot"></span>Ідеї','<span class="dot"></span>Идеи')
add('k.selection','<span class="dot"></span>Selection','<span class="dot"></span>Вибір','<span class="dot"></span>Выбор')
add('k.open','<span class="dot"></span>Open','<span class="dot"></span>Відкрите','<span class="dot"></span>Открытое')
add('k.neighbors','<span class="dot"></span>Neighbors','<span class="dot"></span>Сусіди','<span class="dot"></span>Соседи')
add('k.sources','<span class="dot"></span>Sources','<span class="dot"></span>Джерела','<span class="dot"></span>Источники')

# ---- LADDER ----
add('ladder.short',
 '<h2>Five rungs</h2><ul class="ladder">'
 '<li><b>Pattern</b> &mdash; <span>a regularity compressible by some model.</span></li>'
 '<li><b>Attractor</b> &mdash; <span>a pattern a system returns to under a dynamics.</span></li>'
 '<li><b>Form</b> &mdash; <span>an attractor embodied in a substrate.</span></li>'
 '<li><b>Agency</b> &mdash; <span>a form that defends itself under perturbation.</span></li>'
 '<li><b>Mind</b> &mdash; <span>agency that models patterns it does not yet have.</span></li>'
 '</ul><p>Each rung adds one thing the rung below lacks.</p>',
 '<h2>П&rsquo;ять щаблів</h2><ul class="ladder">'
 '<li><b>Патерн</b> &mdash; <span>закономірність, яку якась модель здатна стиснути.</span></li>'
 '<li><b>Атрактор</b> &mdash; <span>патерн, до якого система повертається за певної динаміки.</span></li>'
 '<li><b>Форма</b> &mdash; <span>атрактор, утілений у середовищі.</span></li>'
 '<li><b>Дієвість</b> &mdash; <span>форма, що сама себе обороняє під збуренням.</span></li>'
 '<li><b>Розум</b> &mdash; <span>дієвість, яка моделює патерни, котрих ще не має.</span></li>'
 '</ul><p>Кожен щабель додає те, чого бракує щаблю під ним.</p>',
 '<h2>Пять ступеней</h2><ul class="ladder">'
 '<li><b>Паттерн</b> &mdash; <span>закономерность, которую способна сжать некоторая модель.</span></li>'
 '<li><b>Аттрактор</b> &mdash; <span>паттерн, к которому система возвращается при некоторой динамике.</span></li>'
 '<li><b>Форма</b> &mdash; <span>аттрактор, воплощённый в среде.</span></li>'
 '<li><b>Агентность</b> &mdash; <span>форма, что сама себя отстаивает под возмущением.</span></li>'
 '<li><b>Разум</b> &mdash; <span>агентность, моделирующая паттерны, которых у неё ещё нет.</span></li>'
 '</ul><p>Каждая ступень добавляет то, чего нет у предыдущей.</p>')
add('ladder.full',
 '<h2>Five rungs carry most of the weight</h2><ul class="ladder">'
 '<li><b>Pattern</b> &mdash; <span>a regularity compressible by some model or code.</span></li>'
 '<li><b>Attractor</b> &mdash; <span>a region a system tends to return to under a dynamics.</span></li>'
 '<li><b>Form</b> &mdash; <span>the embodied expression of an attractor in a substrate.</span></li>'
 '<li><b>Agency</b> &mdash; <span>active preservation of a form or goal-state under perturbation.</span></li>'
 '<li><b>Mind</b> &mdash; <span>agency with counterfactual modeling of possible patterns.</span></li>'
 '</ul><p>Each rung adds one thing the rung below lacks. That is the reason to prefer a ladder over the slogan &ldquo;everything is pattern,&rdquo; which explains nothing. One note on a word that recurs below. In its strict sense &mdash; the one nonlinear dynamics makes precise &mdash; an <em>attractor</em> needs a state space and a dynamics, a set that trajectories fall toward. I use it literally only when those can be specified, and as a disciplined analogy for minds and cultures otherwise.</p>',
 '<h2>П&rsquo;ять щаблів несуть основну вагу</h2><ul class="ladder">'
 '<li><b>Патерн</b> &mdash; <span>закономірність, яку здатна стиснути якась модель чи код.</span></li>'
 '<li><b>Атрактор</b> &mdash; <span>зона, до якої система схильна повертатися за певної динаміки.</span></li>'
 '<li><b>Форма</b> &mdash; <span>утілений вияв атрактора в середовищі.</span></li>'
 '<li><b>Дієвість</b> &mdash; <span>дієве збереження форми чи цільового стану під збуренням.</span></li>'
 '<li><b>Розум</b> &mdash; <span>дієвість, що в умовному способі прораховує можливі патерни.</span></li>'
 '</ul><p>Кожен щабель додає те, чого бракує щаблю під ним. Саме тому сходи кращі за гасло &laquo;усе є патерн&raquo;, яке не пояснює нічого. Одне слово, що повертатиметься далі, варто застерегти. У строгому сенсі &mdash; тому, який уточнює нелінійна динаміка, &mdash; <em>атрактор</em> потребує простору станів і динаміки: множини, до якої сходяться траєкторії. Буквально я вживаю його лише там, де їх можна задати; для розумів і культур &mdash; як виважену аналогію.</p>',
 '<h2>Пять ступеней несут основной вес</h2><ul class="ladder">'
 '<li><b>Паттерн</b> &mdash; <span>закономерность, которую способна сжать некоторая модель или код.</span></li>'
 '<li><b>Аттрактор</b> &mdash; <span>область, к которой система склонна возвращаться при некоторой динамике.</span></li>'
 '<li><b>Форма</b> &mdash; <span>воплощённое выражение аттрактора в среде.</span></li>'
 '<li><b>Агентность</b> &mdash; <span>деятельное сохранение формы или целевого состояния под возмущением.</span></li>'
 '<li><b>Разум</b> &mdash; <span>агентность, что в сослагательном ключе просчитывает возможные паттерны.</span></li>'
 '</ul><p>Каждая ступень добавляет то, чего нет у предыдущей. Потому лестница лучше лозунга &ldquo;всё есть паттерн&rdquo;, который не объясняет ничего. Об одном слове, что вернётся дальше, стоит предупредить. В строгом смысле &mdash; том, который уточняет нелинейная динамика, &mdash; <em>аттрактор</em> требует пространства состояний и динамики: множества, к которому сходятся траектории. Буквально я беру его лишь там, где их можно задать; для разумов и культур &mdash; как выверенную аналогию.</p>')

# ---- LOGIC ----
add('logic.short',
 '<h2>The first filter</h2><p>Logic draws the outer boundary before physics does: a square circle is never built. The filters nest &mdash; <strong>logically possible &sup; dynamically stable &sup; realized in matter &sup; self-defending</strong> &mdash; and every rung sits inside the one before it.</p>',
 '<h2>Перший фільтр</h2><p>Межу окреслює логіка ще до фізики: квадратне коло не збудують ніколи. Фільтри вкладені один в одного &mdash; <strong>логічно можливе &sup; динамічно стійке &sup; утілене в матерії &sup; самозахисне</strong> &mdash; і кожен щабель лежить усередині попереднього.</p>',
 '<h2>Первый фильтр</h2><p>Границу очерчивает логика ещё до физики: квадратный круг не построят никогда. Фильтры вложены один в другой &mdash; <strong>логически возможное &sup; динамически устойчивое &sup; воплощённое в материи &sup; самозащитное</strong> &mdash; и каждая ступень лежит внутри предыдущей.</p>')
add('logic.full',
 '<h2>The first filter</h2><p>Before physics narrows anything, logic has already drawn the outer boundary: a square circle is not waiting somewhere to be built. Non-contradiction is the first filter on the space of patterns. Physics then keeps the stable ones, matter realizes some of those, and agency defends a few.</p>'
 '<p>The filters nest: <strong>logically possible &sup; dynamically stable &sup; realized in matter &sup; self-defending</strong>. Every rung of the ladder sits inside the one before it.</p>'
 '<p>One caution keeps this honest. When wave and particle, or a cell that cooperates and competes, look contradictory, the description is usually too coarse for the level it covers; sharpen the model and the clash dissolves. A real contradiction forbids; an apparent one only asks for a better model.</p>',
 '<h2>Перший фільтр</h2><p>Перш ніж фізика почне звужувати межі, логіка вже окреслила зовнішній контур: квадратне коло ніде не чекає свого втілення. Несуперечність &mdash; це перший фільтр для простору патернів. Потім фізика відбирає стійкі закономірності, матерія втілює деякі з них, а агентність захищає лічені одиниці.</p>'
 '<p>Фільтри вкладені: <strong>логічно можливе &sup; динамічно стійке &sup; утілене в матерії &sup; самозахисне</strong>. Кожен щабель сходів лежить усередині попереднього.</p>'
 '<p>Одне застереження тримає цю думку чесною. Коли хвиля і частинка чи клітина, що водночас співпрацює і суперничає, видаються суперечливими, опис зазвичай надто грубий для того рівня, який охоплює; вигостри модель &mdash; і сутичка розчиняється. Справжня суперечність забороняє; уявна лише просить кращої моделі.</p>',
 '<h2>Первый фильтр</h2><p>Прежде чем физика что-то сузит, логика уже очертила внешнюю границу: квадратный круг нигде не ждёт, чтобы его построили. Непротиворечивость &mdash; первый фильтр на пространстве паттернов. Дальше физика оставляет устойчивые, материя воплощает иные из них, а агентность отстаивает немногие.</p>'
 '<p>Фильтры вложены: <strong>логически возможное &sup; динамически устойчивое &sup; воплощённое в материи &sup; самозащитное</strong>. Каждая ступень лестницы лежит внутри предыдущей.</p>'
 '<p>Одна оговорка держит мысль честной. Когда волна и частица или клетка, что разом сотрудничает и соперничает, кажутся противоречивыми, описание обычно слишком грубо для того уровня, который охватывает; заостри модель &mdash; и столкновение растворяется. Настоящее противоречие запрещает; мнимое лишь просит модели получше.</p>')

# ---- AGENCY ----
add('agency.short',
 '<h2>A defended pattern</h2><p>A snowflake holds its shape until it melts; a cell spends its whole life holding its own, repairing and pumping and regulating. The difference is active correction: an agent detects deviation from a preferred state and acts to undo it. A bacterium swims back up the gradient; your body holds 37&deg;C without believing in thermostats. Agency comes by degree, measured by how many kinds of disturbance a system can absorb and still reach the same end.</p>',
 '<h2>Захищений патерн</h2><p>Сніжинка тримає свою форму, доки не розтане. Клітина ж присвячує все своє життя втриманню власної: лагодить мембрану, перекачує йони, регулює хімічні процеси. Різниця полягає в активній протидії відхиленням: агент виявляє відхилення від цільового стану й діє, щоб його ліквідувати. Бактерія повертається назад проти градієнта поживних речовин; твоє тіло підтримує температуру близько 37&deg;C, гадки не маючи про термостати. Агентність має різні ступені; її мірою є те, скільки різновидів збурень система здатна поглинути без втрати кінцевої мети.</p>',
 '<h2>Защищённый паттерн</h2><p>Снежинка держит свою форму, пока не растает; клетка же всю жизнь удерживает своё &mdash; чинит, перекачивает, настраивает. Разница в активном исправлении: агент замечает отклонение от желаемого состояния и действует, чтобы его отменить. Бактерия плывёт назад вверх по градиенту; твоё тело держит 37&deg;C, не веря ни в какие термостаты. Агентность бывает разной степени: её меряют тем, сколько видов возмущения система способна поглотить и всё равно прийти к той же цели.</p>')
add('agency.full',
 '<h2>A defended pattern</h2><p>A snowflake has structure and loses it the moment the temperature rises. A cell has structure and spends its whole existence keeping it: repairing the membrane, pumping ions, regulating its chemistry, importing food, expelling waste. Both have a pattern. The difference is that the cell detects deviations from viability and acts to reduce them. Agency begins where stability becomes active correction.</p>'
 '<p>An agent, then, is a system that detects deviation from a preferred state and acts to restore or protect it.</p>'
 '<p>An asteroid on an orbit follows a pattern, and if something knocks it off course it simply continues on the new course. A bacterium knocked away from food swims back up the gradient. The bacterium has a state it returns to. That returned-to state is the goal, and the goal shows up in behavior long before anything writes it down. Your body holds its temperature near 37&deg;C without believing anything about thermostats. It shivers, it sweats, it gets hungry.</p>'
 '<p>Agency comes by degree, but not every resistance is agency. A crystal merely resists deformation; a flame conditionally self-maintains; a bacterium regulates, repairs, and returns itself to viable states; a human defends across enormous scales: body, identity, family, a scientific theory, a country. A useful measure is how many kinds of disturbance a system can absorb and still arrive at the same end.</p>',
 '<h2>Захищений патерн</h2><p>Сніжинка має структуру й втрачає її, щойно теплішає. Клітина має структуру й утримує її протягом усього існування: лагодить мембрану, перекачує йони, регулює власну хімію, вбирає поживу, виводить відходи. Патерн є в обох випадках. Різниця в тому, що клітина фіксує відхилення від життєздатного стану й протидіє їм. Агентність народжується там, де стійкість перетворюється на активне самовідновлення.</p>'
 '<p>Отже, агент &mdash; це система, яка помічає відхилення від бажаного стану й діє, щоб відновлювати чи вберігати його.</p>'
 '<p>Астероїд на орбіті просто слідує патерну. Якщо щось зіб&rsquo;є його з курсу, він продовжить рух новою траєкторією. Бактерія, відкинута від їжі, пливе назад проти градієнта. Бактерія має стан, до якого прагне повернутися. Цей цільовий стан і є її метою &mdash; і ця мета виявляє себе в поведінці задовго до того, як хтось сторонній її запише. Твоє тіло підтримує температуру близько 37&deg;C, гадки не маючи про існування термостатів. Воно тремтить, пітніє, відчуває голод.</p>'
 '<p>Агентність має різні ступені, однак не будь-який опір є агентністю. Кристал лише опирається деформації; полум&rsquo;я підтримує себе за певних умов; бактерія регулює процеси, лагодить пошкодження й повертає себе до норми; а людина захищає себе на багатьох рівнях: від власного тіла та ідентичності до родини, наукової теорії чи цілої країни. Універсальним мірилом тут є те, скільки різновидів зовнішніх завад система здатна нейтралізувати й усе одно прийти до своєї мети.</p>',
 '<h2>Защищённый паттерн</h2><p>Снежинка имеет структуру и теряет её в тот же миг, как поднимается температура. Клетка имеет структуру и всё своё существование её удерживает: чинит мембрану, перекачивает ионы, настраивает собственную химию, поглощает пищу, выводит отходы. Паттерн есть у обеих. Разница в том, что клетка замечает отклонения от жизнеспособности и действует, чтобы их уменьшить. Агентность начинается там, где устойчивость становится активным исправлением.</p>'
 '<p>Итак, агент &mdash; это система, что замечает отклонение от желаемого состояния и действует, чтобы восстановить или уберечь его.</p>'
 '<p>Астероид на орбите идёт за паттерном, и если что-то собьёт его с курса, он просто двинется новым. Бактерия, отброшенная от еды, плывёт назад вверх по градиенту. У бактерии есть состояние, к которому она возвращается. Это состояние и есть цель, а цель проступает в поведении задолго до того, как её хоть кто-то запишет. Твоё тело держит температуру около 37&deg;C, ничего не думая о термостатах. Оно дрожит, потеет, хочет есть.</p>'
 '<p>Агентность бывает разной степени, но не всякое сопротивление &mdash; агентность. Кристалл лишь противится деформации; пламя поддерживает себя при определённых условиях; бактерия настраивает, чинит и возвращает себя к жизнеспособным состояниям; человек отстаивает себя на огромных масштабах: тело, личность, семью, научную теорию, страну. Удобная мера &mdash; сколько видов возмущения система способна поглотить и всё равно прийти к той же цели.</p>')

# ---- COMPUTE ----
add('compute.short',
 '<h2>Substrate-general logic</h2><p>The same logic runs on ion channels, transistors, or interfering waves; the universe still charges rent in energy, speed, and error. Even non-neural cells compute &mdash; Levin&rsquo;s bioelectric signals help decide what body to build &mdash; though that means goal-directed regulation, not thought. More compute searches more of the pattern-space, finds deeper compressions, and buys more agency.</p>',
 '<h2>Логіка поза субстратом</h2><p>Та сама логіка працює на йонних каналах, транзисторах чи інтерференційних хвилях; але Всесвіт усе одно стягує за це плату: часом, енергією та похибками. Обчислення відбуваються навіть у безмозких клітинах: біоелектричні сигнали допомагають організму визначити, яке тіло будувати. Звісно, тут ідеться про цілеспрямовану самоорганізацію, а не про свідоме мислення. Більше обчислювального ресурсу означає глибше сканування простору патернів, ефективніше стиснення і, як наслідок, вищий ступінь агентності.</p>',
 '<h2>Логика вне субстрата</h2><p>Та же логика работает на ионных каналах, транзисторах или интерферирующих волнах; вселенная всё равно берёт свою плату &mdash; энергией, скоростью, ошибкой. Вычисляют даже не-нейронные клетки: биоэлектрические сигналы в работах Левина помогают решить, какое тело строить, &mdash; хотя речь о целенаправленном упорядочивании, а не о мысли. Больше вычислений &mdash; шире обзор пространства паттернов, глубже сжатия и больше агентности.</p>')
add('compute.full',
 '<h2>Substrate-general logic</h2><p>Computation is substrate-general: the same operations run on ion channels, on transistors, or on interfering waves, where resonance adds and cancellation subtracts. The logic is portable; the universe charges rent. Every real machine pays its substrate&rsquo;s bill in energy, speed, and error.</p>'
 '<p>So computation reaches well past the brain. Following Levin&rsquo;s work on bioelectricity, even non-neural cells compute with electrical signals, and that signalling helps decide what body to build &mdash; the thread that runs down from thought to morphology. None of this means a cell reasons or feels; it means goal-directed regulation over a space of problems, cognition in the basal sense and nothing grander. And the search has structure: patterns prune the space, so a system explores the allowed region rather than the whole of it, which is what keeps it cheap enough to run.</p>'
 '<p>More of it changes what is reachable. More compute means more of the pattern-space searched, which means deeper compressions found and more value pulled out &mdash; and more agency too, since a richer model answers more kinds of disturbance. The scaling looks the same whether the substrate is a chip or an organism. Compute does not invent possibilities; it searches, realizes, and constrains the ones the substrate already allows.</p>',
 '<h2>Логіка поза субстратом</h2><p>Обчислення не прив&rsquo;язане до субстрату: ті самі дії йдуть на йонних каналах, на транзисторах чи на хвилях, де резонанс додає, а гасіння віднімає. Логіка переносна; Всесвіт бере за неї плату. Кожна справжня машина оплачує рахунок свого субстрату &mdash; енергією, швидкістю, похибкою.</p>'
 '<p>Тож обчислення сягає далеко за межі мозку. Услід за працями Левіна про біоелектрику, навіть не-нейронні клітини обчислюють електричними сигналами, і ця сигналізація допомагає вирішити, яке тіло будувати, &mdash; нитка, що тягнеться згори, від думки до морфології. Ніщо з цього не означає, що клітина мислить чи відчуває; ідеться про цілеспрямоване впорядкування на просторі задач, пізнання в найпростішому сенсі й нічого величнішого. І пошук не хаотичний: патерни підрізають простір, тож система обстежує лише дозволену ділянку, а не весь &mdash; саме це й тримає його достатньо дешевим, щоб узагалі працювати.</p>'
 '<p>Що його більше, то ширше коло досяжного. Більше обчислень &mdash; ширший огляд простору патернів, а отже, глибші знайдені стиснення й більше видобутої цінності; і більше дієвості теж, адже багатша модель відповідає на більше різновидів збурення. Закон зростання той самий, чи то субстрат &mdash; мікросхема, чи організм. Обчислення не вигадує можливостей; воно обстежує, втілює й обмежує ті, що субстрат уже дозволяє.</p>',
 '<h2>Логика вне субстрата</h2><p>Вычисление не привязано к субстрату: те же действия идут на ионных каналах, на транзисторах или на интерферирующих волнах, где резонанс прибавляет, а гашение вычитает. Логика переносима; вселенная взимает за неё плату. Каждая настоящая машина оплачивает счёт своего субстрата &mdash; энергией, скоростью, ошибкой.</p>'
 '<p>Так что вычисление достаёт далеко за пределы мозга. Вслед за работами Левина о биоэлектрике, даже не-нейронные клетки вычисляют электрическими сигналами, и эта сигнализация помогает решить, какое тело строить, &mdash; нить, что тянется от мысли к морфологии. Ничто из этого не значит, что клетка рассуждает или чувствует; речь о целенаправленном упорядочивании на пространстве задач, познании в простейшем смысле &mdash; и ни о чём более высоком. И поиск не хаотичен: паттерны подрезают пространство, и система обследует лишь дозволенную область, а не всю &mdash; именно это и держит его достаточно дешёвым, чтобы вообще работать.</p>'
 '<p>Чем его больше, тем шире круг достижимого. Больше вычислений &mdash; шире обзор пространства паттернов, а значит, глубже найденные сжатия и больше извлечённой ценности; и больше агентности тоже, ведь более богатая модель отвечает на больше видов возмущения. Закон роста тот же, будь субстрат микросхемой или организмом. Вычисление не выдумывает возможностей; оно обследует, воплощает и ограничивает те, что субстрат уже дозволяет.</p>')

# ---- BEAUTY ----
add('beauty.short',
 '<h2>Beauty as compression progress</h2><p>Repetition bores and noise says nothing; beauty lives between, where a new pattern still fits the larger one. A theme states itself, varies, resolves, and the fit is the reward. Following Schmidhuber, the feeling may track compression progress: a model expanding without breaking. The signal can lie &mdash; a myth, a slogan, a conspiracy can all feel beautiful &mdash; because a compression can fit the mind while missing the world.</p>',
 '<h2>Краса як поступ стиснення</h2><p>Повтор набридає, а шум не каже нічого; краса живе поміж ними &mdash; там, де новий патерн усе ще лягає в більший. Тема заявляє себе, варіюється, розв&rsquo;язується, і ця злагода й є нагородою. Услід за Шмідгубером, відчуття, можливо, стежить за поступом стиснення: за миттю, коли модель ширшає, не ламаючись. Сигнал уміє брехати &mdash; міф, гасло, змова теж бувають на смак прекрасні, &mdash; бо стиснення може лягти в розум, проминувши світ.</p>',
 '<h2>Красота как прогресс сжатия</h2><p>Повтор приедается, а шум не говорит ничего; красота живёт между ними &mdash; там, где новый паттерн всё ещё ложится в больший. Тема заявляет себя, варьируется, разрешается, и это совпадение и есть награда. Вслед за Шмидхубером, чувство, возможно, следит за прогрессом сжатия: за мигом, когда модель ширится, не ломаясь. Сигнал умеет лгать &mdash; миф, лозунг, заговор тоже могут казаться прекрасными, &mdash; ведь сжатие может лечь в разум, минуя мир.</p>')
add('beauty.full',
 '<h2>Beauty as compression progress</h2><p>Repetition alone is dull. <em>AAAAAA</em> is maximally compressible and says nothing. Noise sits at the other end, with no compression available at all. The interesting zone lies between them, and music lives there. What lives there is meaningful surprise, and the word <em>meaningful</em> is doing the work: a new pattern that still fits the larger pattern. Mere novelty will not do, since noise is novel too and fits nothing. A theme repeats, so the mind builds a model. The theme varies, which creates tension. The variation resolves, and the mind registers that the new material belonged to the larger shape all along. That moment of fit is the reward.</p>'
 '<p>One possibility, and here I am following Schmidhuber, is that the feeling tracks how fast a model improves, more than how much order is already there. Beauty may mark compression progress: the moment a model expands without breaking. The compressions that stay beautiful tend to be the ones simple enough to grasp, rich enough to keep exploring, and useful enough to predict the next moment. This is suggestive, and far from settled &mdash; the older inverted-U results on novelty and complexity, from Berlyne onward, hold in some domains and fray in others &mdash; so the word <em>may</em> is load-bearing.</p>'
 '<p>That signal can lie. A myth can be beautiful. A propaganda symbol can be elegant. A conspiracy theory can feel like a key turning in a lock. Beauty is evidence that a compression fits the mind, and a compression can fit the mind while missing the world.</p>',
 '<h2>Краса як поступ стиснення</h2><p>Сам по собі повтор нудний. <em>AAAAAA</em> стискається до краю й не каже нічого. Шум сидить на іншому кінці &mdash; стиснути його не вийде взагалі. Цікава смуга пролягає поміж ними, і музика живе саме там. Те, що там живе, &mdash; це значуща несподіванка, і слово <em>значуща</em> робить тут усю роботу: новий патерн, що все ще лягає в більший. Самої новизни замало, адже шум теж новий і не лягає ні в що. Тема повторюється &mdash; розум вибудовує модель. Тема варіюється &mdash; виникає напруга. Варіація розв&rsquo;язується &mdash; і розум усвідомлює, що новий матеріал увесь час належав до більшої форми. Ця мить злагоди й є нагородою.</p>'
 '<p>Одна з можливостей, і тут я йду за Шмідгубером, полягає в тому, що відчуття стежить радше за тим, як швидко модель кращає, ніж за тим, скільки ладу вже є. Краса, можливо, позначає поступ стиснення: мить, коли модель ширшає, не ламаючись. Стиснення, що лишаються прекрасними, зазвичай досить прості, щоб їх ухопити, досить багаті, щоб їх розвідувати далі, і досить корисні, щоб передбачити наступну мить. Це наводить на думку, але далеко не вирішене &mdash; давніші результати про перевернуту U-подібну криву щодо новизни й складності, від Берлайна й далі, тримаються в одних царинах і розповзаються в інших, &mdash; тож слово <em>можливо</em> тут несуче.</p>'
 '<p>Цей сигнал уміє брехати. Міф буває прекрасним. Пропагандистський символ буває витонченим. Теорія змови відчувається, наче ключ, що провертається в замку. Краса &mdash; це свідчення, що стиснення лягло в розум, а стиснення може лягти в розум, проминувши світ.</p>',
 '<h2>Красота как прогресс сжатия</h2><p>Сам по себе повтор скучен. <em>AAAAAA</em> сжимается до предела и не говорит ничего. Шум сидит на другом конце &mdash; сжать его не выйдет вовсе. Любопытная полоса пролегает между ними, и музыка живёт именно там. То, что там живёт, &mdash; это значимая неожиданность, и слово <em>значимая</em> делает тут всю работу: новый паттерн, что всё ещё ложится в больший. Одной новизны мало, ведь шум тоже нов и не ложится ни во что. Тема повторяется &mdash; разум выстраивает модель. Тема варьируется &mdash; возникает напряжение. Вариация разрешается &mdash; и разум осознаёт, что новый материал всё это время принадлежал к большей форме. Этот миг совпадения и есть награда.</p>'
 '<p>Одна из возможностей, и тут я иду за Шмидхубером, в том, что чувство следит скорее за тем, как быстро модель улучшается, чем за тем, сколько строя уже есть. Красота, возможно, отмечает прогресс сжатия: миг, когда модель ширится, не ломаясь. Сжатия, что остаются прекрасными, обычно достаточно просты, чтобы их ухватить, достаточно богаты, чтобы их разведывать дальше, и достаточно полезны, чтобы предсказать следующий миг. Это наводит на мысль, но далеко не решено &mdash; прежние результаты о перевёрнутой U-образной кривой по новизне и сложности, от Берлайна и далее, держатся в одних областях и расползаются в других, &mdash; так что слово <em>возможно</em> тут несущее.</p>'
 '<p>Этот сигнал умеет лгать. Миф бывает прекрасным. Пропагандистский символ бывает изящным. Теория заговора отзывается, как ключ, щёлкающий в замке. Красота &mdash; это свидетельство, что сжатие легло в разум, а сжатие может лечь в разум, минуя мир.</p>')

# ---- REALITY ----
add('reality.short',
 '<h2>When is a pattern real?</h2><p>A pattern earns warrant when independent minds can recover it and use it to predict, act, and be corrected. Whether that recoverability makes a pattern real or only reveals it, I leave open. Science and propaganda both compress the world; good compression lets reality correct it, and bad compression explains the correction away.</p>',
 '<h2>Коли патерн реальний?</h2><p>Патерн здобуває право на довіру, коли незалежні розуми здатні його відтворити й користуватися ним, щоб передбачати, діяти й допускати поправку. Чи робить така відтворюваність патерн реальним, а чи лише його виявляє &mdash; я лишаю відкритим. І наука, і пропаганда стискають світ; добре стиснення дозволяє дійсності себе виправити, а погане &mdash; тлумачить поправку так, щоб її знешкодити.</p>',
 '<h2>Когда паттерн реален?</h2><p>Паттерн обретает право на доверие, когда независимые разумы способны его воспроизвести и пользоваться им, чтобы предсказывать, действовать и допускать поправку. Делает ли такая воспроизводимость паттерн реальным или лишь его обнаруживает &mdash; я оставляю открытым. И наука, и пропаганда сжимают мир; хорошее сжатие позволяет действительности себя исправить, а плохое &mdash; растолковывает поправку так, чтобы её обезвредить.</p>')
add('reality.full',
 '<h2>When is a pattern real?</h2><p>A pattern earns warrant when independent minds can recover it and use it to predict, to act, and to be corrected. Newtonian mechanics was superseded and is still not fake. Diagnostic categories are messy and still not imaginary. Musical intervals are read through culture, and the frequency ratios underneath them are no hallucination.</p>'
 '<p>Whether that recoverability <em>constitutes</em> a pattern&rsquo;s reality or merely <em>reveals</em> it, I leave open. It may be a separate realm, it may be part of the pattern itself, it may be both. A hidden planet was real before anyone detected it; a private pain is real before anyone else can recover it &mdash; and in each case how we would ever know stays tangled with what is there. I would rather hold the question than fake an answer.</p>'
 '<p>The test does its work even with the metaphysics open. Science and propaganda both compress the world; the difference lives in what each does next. Good compression lets reality correct it; bad compression explains the correction away.</p>',
 '<h2>Коли патерн реальний?</h2><p>Патерн здобуває право на довіру, коли незалежні розуми здатні його відтворити й користуватися ним, щоб передбачати, діяти й допускати поправку. Ньютонову механіку перевершили, та підробкою вона не стала. Діагностичні категорії плутані, та уявними вони не є. Музичні інтервали прочитуються крізь культуру, а співвідношення частот під ними &mdash; жодна не омана.</p>'
 '<p>Чи <em>становить</em> така відтворюваність реальність патерну, а чи лише її <em>виявляє</em> &mdash; я лишаю відкритим. Це може бути окрема царина, може бути частиною самого патерну, може бути й те, й те. Прихована планета була реальною ще до того, як її помітили; чужий біль реальний ще до того, як хтось інший зможе його відтворити, &mdash; і щоразу те, як ми взагалі могли б про це знати, заплутане з тим, що там є насправді. Радше потримаю питання, ніж підроблю відповідь.</p>'
 '<p>Перевірка робить своє навіть із відкритою метафізикою. І наука, і пропаганда стискають світ; різниця в тому, що кожна робить далі. Добре стиснення дозволяє дійсності себе виправити; погане &mdash; тлумачить поправку так, щоб її знешкодити.</p>',
 '<h2>Когда паттерн реален?</h2><p>Паттерн обретает право на доверие, когда независимые разумы способны его воспроизвести и пользоваться им, чтобы предсказывать, действовать и допускать поправку. Ньютонову механику превзошли, но подделкой она не стала. Диагностические категории путаны, но мнимыми они не являются. Музыкальные интервалы прочитываются сквозь культуру, а соотношения частот под ними &mdash; отнюдь не галлюцинация.</p>'
 '<p>Составляет ли такая воспроизводимость реальность паттерна или лишь её обнаруживает &mdash; я оставляю открытым. Это может быть отдельная область, может быть частью самого паттерна, может быть и то, и другое. Скрытая планета была реальной ещё до того, как её обнаружили; чужая боль реальна ещё до того, как кто-то другой сможет её воспроизвести, &mdash; и всякий раз то, как мы вообще могли бы об этом знать, запутано с тем, что там есть на самом деле. Скорее подержу вопрос, чем подделаю ответ.</p>'
 '<p>Проверка делает своё даже с открытой метафизикой. И наука, и пропаганда сжимают мир; разница в том, что каждая делает дальше. Хорошее сжатие позволяет действительности себя исправить; плохое &mdash; растолковывает поправку так, чтобы её обезвредить.</p>')

# ---- EXISTENCE ----
add('existence.short',
 '<h2>A stronger reading</h2><p>A bolder version, held loosely: to exist is to be a pattern, and only noise resists all compression. On this view a form is a timeless possibility, and time is how it enters matter.</p>',
 '<h2>Сильніше прочитання</h2><p>Сміливіша версія, яку подаю обережно, не наполягаючи: існувати означає бути патерном, і лише шум опирається будь-якому стисненню. За цим поглядом форма &mdash; це позачасова можливість, а час &mdash; те, чим вона входить у матерію.</p>',
 '<h2>Более сильное прочтение</h2><p>Более смелая версия, за которую держусь не слишком крепко: существовать значит быть паттерном, и лишь шум противится всякому сжатию. При таком взгляде форма &mdash; это вневременная возможность, а время &mdash; то, чем она входит в материю.</p>')
add('existence.full',
 '<h2>A stronger reading</h2><p>There is a bolder version of all this, and I want to flag it as a reading and hold it loosely. On the strong version, to exist is to be a pattern. What resists all compression is noise &mdash; pure randomness, with no description shorter than itself. Chaos is a different animal: a short rule whose long run still outruns prediction. Anything you can point to at all is already compressible enough to point at.</p>'
 '<p>Time fits the same picture, and here the debt is to Whitehead. On this reading a form is a timeless possibility, and time is the dimension in which it becomes actual and embodied &mdash; what Whitehead called the form&rsquo;s <em>ingression</em> into matter. An agent is what lets a timeless shape unfold through action. Whether this is ontology or only a useful lens is the open question from the last section, carried one level deeper.</p>',
 '<h2>Сильніше прочитання</h2><p>Є сміливіша версія всього цього, і я хочу позначити її саме як прочитання й триматися обережно, не наполягаючи. За сильною версією, існувати означає бути патерном. Те, що опирається будь-якому стисненню, &mdash; це шум: чиста випадковість, чий опис не коротший за неї саму. Хаос &mdash; геть інша річ: коротке правило, чий довгий перебіг усе одно випереджає передбачення. Будь-що, на що взагалі можна вказати, уже досить стисне, щоб на нього вказати.</p>'
 '<p>Час лягає в ту саму картину, і тут борг &mdash; перед Вайтгедом. За цим прочитанням форма &mdash; позачасова можливість, а час &mdash; той вимір, у якому вона стає дійсною й утіленою; Вайтгед називав це <em>інгресією</em> форми в матерію. Агент &mdash; це те, що дає позачасовій формі розгорнутися через дію. Чи це онтологія, чи лише зручна призма &mdash; те саме відкрите питання з попереднього розділу, узяте на щабель глибше.</p>',
 '<h2>Более сильное прочтение</h2><p>Есть более смелая версия всего этого, и я хочу обозначить её именно как прочтение и держаться не слишком крепко. По сильной версии, существовать значит быть паттерном. То, что противится всякому сжатию, &mdash; это шум: чистая случайность, чьё описание не короче её самой. Хаос &mdash; совсем иная материя: короткое правило, чей долгий ход всё равно обгоняет предсказание. Всё, на что вообще можно указать, уже достаточно сжато, чтобы на него указать.</p>'
 '<p>Время ложится в ту же картину, и тут долг &mdash; перед Уайтхедом. По этому прочтению форма &mdash; вневременная возможность, а время &mdash; то измерение, в котором она становится действительной и воплощённой; Уайтхед называл это <em>ингрессией</em> формы в материю. Агент &mdash; это то, что даёт вневременной форме развернуться через действие. Онтология это или лишь удобная призма &mdash; тот же открытый вопрос из прошлого раздела, взятый на ступень глубже.</p>')

# ---- IDEAS ----
add('ideas.short',
 '<h2>Ideologies behave like attractors</h2><p>Ideas move between minds, and some behave like attractors: cheap, sticky, self-sealing. Fascism, Nazism, and <em>ruscism</em> hand a believer an identity, an enemy, an explanation, and a mission in one move, then treat every correction as persecution and every doubt as betrayal.</p>',
 '<h2>Ідеології поводяться, як атрактори</h2><p>Ідеї переходять між розумами, і деякі поводяться, як атрактори: дешеві, чіпкі, наглухо замкнені на собі. Фашизм, нацизм і <em>рашизм</em> одним рухом вручають адептові ідентичність, ворога, пояснення й місію, а тоді кожну поправку видають за переслідування, кожен сумнів &mdash; за зраду.</p>',
 '<h2>Идеологии ведут себя как аттракторы</h2><p>Идеи переходят между разумами, и некоторые ведут себя как аттракторы: дешёвые, цепкие, наглухо замкнутые на себе. Фашизм, нацизм и <em>рашизм</em> одним движением вручают адепту идентичность, врага, объяснение и миссию, а затем всякую поправку выдают за преследование, всякое сомнение &mdash; за измену.</p>')
add('ideas.full',
 '<h2>Ideologies behave like attractors too</h2><p>Ideas live in minds and travel between them, and some of them behave like attractors. An ideology compresses a mess of experience into one simple shape, spreads, rewards belonging, punishes doubt, and explains its own failures by demanding more of itself. <em>We are pure and they are corrupt. Everything wrong comes from them. Doubt is betrayal.</em> That is a very cheap compression. It accounts for a great deal with one brutal rule, which is exactly what makes it attractive, and it stays false and self-sealing the whole time.</p>'
 '<p>Authoritarian ultranationalist ideologies &mdash; fascism, Nazism, and contemporary Russian fascism (<em>ruscism</em>, the self-justifying militarism behind Russia&rsquo;s war on Ukraine, which is how Timothy Snyder reads the present Russian state) &mdash; behave like pathological attractors in idea-space, and reading them that way explains their stickiness. They hand a believer identity, an enemy, an explanation, and a mission in a single move. Their core pathology is that they are self-sealing: correction is reinterpreted as persecution, doubt as betrayal, and failure as proof that the doctrine has not yet been applied completely enough.</p>',
 '<h2>Ідеології теж поводяться, як атрактори</h2><p>Ідеї живуть у розумах і кочують між ними, і деякі з них поводяться, як атрактори. Ідеологія стискає безлад досвіду в одну просту форму, шириться, винагороджує за приналежність, карає за сумнів, а власні провали пояснює вимогою більшої відданості собі. <em>Ми чисті, а вони зіпсуті. Усе лихе йде від них. Сумнів &mdash; це зрада.</em> Це дуже дешеве стиснення. Воно пояснює величезне коло речей одним брутальним правилом &mdash; саме це й вабить, &mdash; і весь цей час лишається хибним і наглухо замкненим на собі.</p>'
 '<p>Авторитарні ультранаціоналістичні ідеології &mdash; фашизм, нацизм і сучасний російський фашизм (<em>рашизм</em>, самовиправдальна войовничість, що стоїть за російською війною проти України, &mdash; так прочитує теперішню російську державу Тімоті Снайдер) &mdash; поводяться, як патологічні атрактори в просторі ідей, і таке прочитання пояснює їхню чіпкість. Вони одним рухом вручають адептові ідентичність, ворога, пояснення й місію. Головна їхня патологія в тому, що вони наглухо замкнені на собі: поправку перетлумачують як переслідування, сумнів &mdash; як зраду, а поразку &mdash; як доказ, що доктрину ще не втілили достатньо повно.</p>',
 '<h2>Идеологии тоже ведут себя как аттракторы</h2><p>Идеи живут в разумах и кочуют между ними, и некоторые из них ведут себя как аттракторы. Идеология сжимает беспорядок опыта в одну простую форму, ширится, вознаграждает за принадлежность, карает за сомнение, а собственные провалы объясняет требованием большей преданности себе. <em>Мы чисты, а они порочны. Всё дурное идёт от них. Сомнение &mdash; это измена.</em> Это очень дешёвое сжатие. Оно объясняет огромный круг вещей одним брутальным правилом &mdash; именно это и манит, &mdash; и всё это время остаётся ложным и наглухо замкнутым на себе.</p>'
 '<p>Авторитарные ультранационалистические идеологии &mdash; фашизм, нацизм и современный российский фашизм (<em>рашизм</em>, самооправдательная воинственность, стоящая за российской войной против Украины, &mdash; так прочитывает нынешнее российское государство Тимоти Снайдер) &mdash; ведут себя как патологические аттракторы в пространстве идей, и такое прочтение объясняет их цепкость. Они одним движением вручают адепту идентичность, врага, объяснение и миссию. Их корневая патология в том, что они наглухо замкнуты на себе: поправку перетолковывают как преследование, сомнение &mdash; как измену, а поражение &mdash; как доказательство, что доктрину ещё не воплотили достаточно полно.</p>')

# ---- SELECTION ----
add('selection.short',
 '<h2>Which patterns should we realize?</h2><p>Plenty of stable patterns are worth refusing &mdash; cancer, addiction, fascism &mdash; locally stable and globally destructive, holding themselves together by eating the systems that hold them. That a pattern can exist says nothing about whether to build it. The choice is value-laden, and it falls to us.</p>',
 '<h2>Які патерни нам варто втілювати?</h2><p>Чимало стійких патернів варто відкинути &mdash; рак, залежність, фашизм, &mdash; локально стійких і згубних для цілого, що тримаються купи, поїдаючи ті системи, які їх тримають. Те, що патерн може існувати, не каже нічого про те, чи варто його будувати. Цей вибір просякнутий цінностями, і робити його доведеться нам.</p>',
 '<h2>Какие паттерны нам стоит воплощать?</h2><p>Немало устойчивых паттернов стоит отвергнуть &mdash; рак, зависимость, фашизм, &mdash; локально устойчивых и губительных для целого, что держатся вместе, поедая те системы, которые их держат. То, что паттерн может существовать, не говорит ничего о том, стоит ли его строить. Этот выбор пропитан ценностями, и делать его нам.</p>')
add('selection.full',
 '<h2>Which patterns should we realize?</h2><p>The map would be dangerous if it stopped at description, because plenty of stable patterns are worth refusing: cancer, addiction loops, torture systems, a maximizer that grinds the world into paperclips. That a pattern can exist tells you nothing about whether it should be built. That last step is a choice, and it carries values the earlier steps do not contain.</p>'
 '<p>What those examples share is a particular shape: they are <strong>locally stable and globally destructive</strong>. Cancer is a cellular attractor that violates the coherence of the organism. Addiction is a reward-loop attractor that consumes the agency of the person. Fascism is a social attractor that devours plural human agency. A pattern can be perfectly stable and still be pathological if it preserves itself by destroying the larger systems that make it possible.</p>'
 '<p>That a pattern can exist says nothing about whether it should be built. Which patterns are worth realizing is a separate, value-laden question, and the map does not settle it. Prediction is the floor; the choice is not in the physics.</p>'
 '<p>Still, the choice falls to someone. As conscious agents we are the ones who can recognize that these patterns exist at all, and that recognition is where the duty starts: to seek them out, test them, and choose. Who, if not us?</p>',
 '<h2>Які патерни нам варто втілювати?</h2><p>Мапа була б небезпечною, якби спинилася на описі, бо чимало стійких патернів варто відкинути: рак, петлі залежності, системи тортур, максимізатор, що перемелює світ на скріпки. Те, що патерн може існувати, не каже нічого про те, чи треба його будувати. Цей останній крок &mdash; вибір, і він несе цінності, яких у попередніх кроках немає.</p>'
 '<p>Спільне в цих прикладах &mdash; певна форма: вони <strong>локально стійкі й згубні для цілого</strong>. Рак &mdash; клітинний атрактор, що ламає злагодженість організму. Залежність &mdash; атрактор винагородної петлі, що поглинає агентність людини. Фашизм &mdash; суспільний атрактор, що пожирає множинну людську агентність. Патерн може бути цілком стійким і все одно патологічним, якщо береже себе, руйнуючи ті більші системи, які роблять його можливим.</p>'
 '<p>Те, що патерн може існувати, не каже нічого про те, чи треба його будувати. Які патерни варто втілювати &mdash; це окреме питання, просякнуте цінностями, і мапа його не вирішує. Передбачення &mdash; це підлога; вибору у фізиці немає.</p>'
 '<p>І все ж вибір комусь випадає. Як свідомі агенти, саме ми здатні взагалі розпізнати, що ці патерни існують, і з цього розпізнання починається обов&rsquo;язок: вишукувати їх, перевіряти й обирати. Хто, як не ми?</p>',
 '<h2>Какие паттерны нам стоит воплощать?</h2><p>Карта была бы опасной, если бы остановилась на описании, ведь немало устойчивых паттернов стоит отвергнуть: рак, петли зависимости, системы пыток, максимизатор, перемалывающий мир в скрепки. То, что паттерн может существовать, не говорит ничего о том, нужно ли его строить. Этот последний шаг &mdash; выбор, и он несёт ценности, которых в предыдущих шагах нет.</p>'
 '<p>Общее в этих примерах &mdash; определённая форма: они <strong>локально устойчивы и губительны для целого</strong>. Рак &mdash; клеточный аттрактор, ломающий слаженность организма. Зависимость &mdash; аттрактор петли вознаграждения, поглощающий агентность человека. Фашизм &mdash; общественный аттрактор, пожирающий множественную человеческую агентность. Паттерн может быть вполне устойчивым и всё же патологичным, если бережёт себя, разрушая те большие системы, которые делают его возможным.</p>'
 '<p>То, что паттерн может существовать, не говорит ничего о том, нужно ли его строить. Какие паттерны стоит воплощать &mdash; это отдельный вопрос, пропитанный ценностями, и карта его не решает. Предсказание &mdash; это нижняя граница; выбора в физике нет.</p>'
 '<p>И всё же выбор кому-то выпадает. Как сознательные агенты, именно мы способны вообще распознать, что эти паттерны существуют, и с этого распознавания начинается долг: выискивать их, проверять и выбирать. Кто, если не мы?</p>')

# ---- OPEN ----
add('open.body',
 '<h2>Four questions I keep open</h2>'
 '<p class="q">Is pattern something the mind imposes, or something the world is made of?</p>'
 '<p class="q">Is there a real threshold where &ldquo;agent&rdquo; begins, or only a smooth axis with no line on it?</p>'
 '<p class="q">Is beauty the felt signature of a form arriving in a mind, the same event described from the inside?</p>'
 '<p class="q">Is logic an outer frame on the space of patterns, or the deepest pattern of all, the one the whole ladder grows from?</p>',
 '<h2>Чотири питання, які лишаю відкритими</h2>'
 '<p class="q">Патерн &mdash; це те, що розум накидає світові, чи те, з чого світ зроблений?</p>'
 '<p class="q">Чи є справжній поріг, де починається &laquo;агент&raquo;, чи лише плавна вісь без жодної межі на ній?</p>'
 '<p class="q">Чи краса &mdash; це відчутний підпис форми, що прибуває в розум, та сама подія, описана зсередини?</p>'
 '<p class="q">Логіка &mdash; це зовнішня рамка на просторі патернів, чи найглибший патерн з усіх, той, з якого ростуть усі сходи?</p>',
 '<h2>Четыре вопроса, что оставляю открытыми</h2>'
 '<p class="q">Паттерн &mdash; это то, что разум набрасывает на мир, или то, из чего мир сделан?</p>'
 '<p class="q">Есть ли настоящий порог, где начинается &laquo;агент&raquo;, или лишь плавная ось без всякой черты на ней?</p>'
 '<p class="q">Красота &mdash; это ощутимая подпись формы, прибывающей в разум, то же событие, описанное изнутри?</p>'
 '<p class="q">Логика &mdash; это внешняя рамка на пространстве паттернов или глубочайший паттерн из всех, тот, из которого растёт вся лестница?</p>')

# ---- NEIGHBORS ----
add('neighbors.short',
 '<h2>Where this sits</h2><p>Built on dynamical systems, information theory, cybernetics, theories of prediction, basal cognition in living cells, compression accounts of beauty, and the study of how ideologies spread. Full citations in the expanded view.</p>',
 '<h2>Де це стоїть</h2><p>Спирається на динамічні системи, теорію інформації, кібернетику, теорії передбачення, найпростіше пізнання в живих клітинах, стискальні пояснення краси й дослідження того, як шириться ідеологія. Повні посилання &mdash; у розгорнутому вигляді.</p>',
 '<h2>Где это стоит</h2><p>Опирается на динамические системы, теорию информации, кибернетику, теории предсказания, простейшее познание в живых клетках, сжимающие объяснения красоты и исследования того, как ширится идеология. Полные ссылки &mdash; в развёрнутом виде.</p>')
add('neighbors.full',
 '<h2>Where this sits</h2><p>This map does not review the work it leans on, but it should at least point. The language of attractors and state spaces is nonlinear dynamics. The idea of a pattern as a short description runs from Shannon&rsquo;s entropy through Kolmogorov, Solomonoff, and minimum description length. The picture of development as movement through constrained valleys is Waddington&rsquo;s, now redrawn with dynamical-systems tools. Agency as prediction and regulation owes to cybernetics and to Friston&rsquo;s free-energy principle; cognition below the brain, to Levin&rsquo;s bioelectric cells. Beauty as learnable surprise is Berlyne and Schmidhuber. The darker chapter &mdash; how ideas spread, harden, and turn self-sealing &mdash; draws on Dawkins, Arendt, Adorno, Hoffer, and Snyder. The Platonic temptation is Plato by way of Whitehead and Penrose. Full citations are below.</p>',
 '<h2>Де це стоїть</h2><p>Ця мапа не оглядає праці, на які спирається, та бодай вказати на них вона мусить. Мова атракторів і просторів станів &mdash; це нелінійна динаміка. Думка про патерн як короткий опис тягнеться від Шеннонової ентропії через Колмогорова, Соломонова й мінімальну довжину опису. Картина розвитку як руху вузькими долинами &mdash; Воддінгтонова, нині перемальована засобами динамічних систем. Агентність як передбачення й упорядкування завдячує кібернетиці та Фрістоновому принципу вільної енергії; пізнання нижче за мозок &mdash; біоелектричним клітинам Левіна. Краса як навчувана несподіванка &mdash; це Берлайн і Шмідгубер. Темніший розділ &mdash; як ідеї ширяться, тверднуть і замикаються на собі &mdash; черпає з Докінза, Арендт, Адорно, Гоффера й Снайдера. Платонівська спокуса &mdash; це Платон через Вайтгеда й Пенроуза. Повні посилання &mdash; нижче.</p>',
 '<h2>Где это стоит</h2><p>Эта карта не делает обзор работ, на которые опирается, но хотя бы указать на них она обязана. Язык аттракторов и пространств состояний &mdash; это нелинейная динамика. Мысль о паттерне как коротком описании тянется от шенноновской энтропии через Колмогорова, Соломонова и минимальную длину описания. Картина развития как движения узкими долинами &mdash; уоддингтоновская, ныне перерисованная средствами динамических систем. Агентность как предсказание и упорядочивание обязана кибернетике и фристоновскому принципу свободной энергии; познание ниже мозга &mdash; биоэлектрическим клеткам Левина. Красота как обучаемая неожиданность &mdash; это Берлайн и Шмидхубер. Более тёмная глава &mdash; как идеи ширятся, твердеют и замыкаются на себе &mdash; черпает из Докинза, Арендт, Адорно, Хоффера и Снайдера. Платоновский соблазн &mdash; это Платон через Уайтхеда и Пенроуза. Полные ссылки &mdash; ниже.</p>')

# ---- SOURCES ----
add('sources.h2','The shoulders this stands on','Плечі, на яких це стоїть','Плечи, на которых это стоит')
# Sources body: keep author + cited title in original; translate the trailing descriptions.
_SRC_HEADS = {
 'dyn':('Dynamical systems &amp; form','Динамічні системи й форма','Динамические системы и форма'),
 'info':('Information &amp; compression','Інформація та стиснення','Информация и сжатие'),
 'agency':('Agency, prediction &amp; regulation','Агентність, передбачення, упорядкування','Агентность, предсказание, упорядочивание'),
 'basal':('Basal cognition &amp; bioelectricity','Найпростіше пізнання й біоелектрика','Простейшее познание и биоэлектрика'),
 'beauty':('Beauty &amp; aesthetics','Краса й естетика','Красота и эстетика'),
 'ideo':('Ideas, ideology &amp; authoritarianism','Ідеї, ідеологія, авторитаризм','Идеи, идеология, авторитаризм'),
 'meta':('Forms &amp; metaphysics','Форми й метафізика','Формы и метафизика'),
}
def src_full(lang):
    n = {'en':'A working essay that leans on real work. Where a claim belongs to someone, the credit is here.',
         'uk':'Робоче есе, що спирається на справжні праці. Де твердження комусь належить, тут і подяка.',
         'ru':'Рабочее эссе, опирающееся на настоящие труды. Где утверждение кому-то принадлежит, здесь и благодарность.'}[lang]
    def L(en,uk,ru): return {'en':en,'uk':uk,'ru':ru}[lang]
    H=lambda key: _SRC_HEADS[key][LANGS.index(lang)]
    parts=['<p class="note">%s</p>'%n]
    # dynamical
    parts.append('<h3>%s</h3><ul>'%H('dyn'))
    parts.append('<li>Strogatz, S. H. <cite>Nonlinear Dynamics and Chaos</cite> (1994). '+L('Attractors, state space, bifurcations, the difference between chaos and noise.','Атрактори, простір станів, біфуркації, різниця між хаосом і шумом.','Аттракторы, пространство состояний, бифуркации, разница между хаосом и шумом.')+'</li>')
    parts.append('<li>Waddington, C. H. <cite>The Strategy of the Genes</cite> (1957). '+L('The epigenetic landscape; development as constrained valleys.','Епігенетичний ландшафт; розвиток як рух вузькими долинами.','Эпигенетический ландшафт; развитие как движение узкими долинами.')+'</li>')
    parts.append('<li>Bhattacharya, S. et al. &ldquo;A deterministic map of Waddington&rsquo;s epigenetic landscape for cell fate specification.&rdquo; <cite>BMC Systems Biology</cite> (2011).</li>')
    parts.append('<li>Ferrell, J. E. &ldquo;Bistability, bifurcations, and Waddington&rsquo;s epigenetic landscape.&rdquo; <cite>Current Biology</cite> (2012).</li>')
    parts.append('<li>Thom, R. <cite>Structural Stability and Morphogenesis</cite> (1972). '+L('Catastrophe theory; sudden change of form under smooth parameters.','Теорія катастроф; раптова зміна форми за плавних параметрів.','Теория катастроф; внезапная смена формы при плавных параметрах.')+'</li>')
    parts.append('</ul>')
    # info
    parts.append('<h3>%s</h3><ul>'%H('info'))
    parts.append('<li>Shannon, C. E. &ldquo;A Mathematical Theory of Communication.&rdquo; <cite>Bell System Technical Journal</cite> (1948). '+L('Entropy, redundancy, noise.','Ентропія, надлишковість, шум.','Энтропия, избыточность, шум.')+'</li>')
    parts.append('<li>Kolmogorov, A. N. &ldquo;Three approaches to the quantitative definition of information&rdquo; (1965). '+L('Algorithmic complexity, the shortest program.','Алгоритмічна складність, найкоротша програма.','Алгоритмическая сложность, кратчайшая программа.')+'</li>')
    parts.append('<li>Solomonoff, R. J. &ldquo;A Formal Theory of Inductive Inference&rdquo; (1964). '+L('Universal induction.','Універсальна індукція.','Универсальная индукция.')+'</li>')
    parts.append('<li>Rissanen, J. &ldquo;Modeling by shortest data description.&rdquo; <cite>Automatica</cite> (1978). '+L('Minimum description length.','Мінімальна довжина опису.','Минимальная длина описания.')+'</li>')
    parts.append('<li>Schmidhuber, J. &ldquo;Driven by Compression Progress&rdquo; (2008). '+L('Curiosity, beauty, and surprise as the felt reward of better compression.','Цікавість, краса й несподіванка як відчутна нагорода за краще стиснення.','Любопытство, красота и неожиданность как ощутимая награда за лучшее сжатие.')+'</li>')
    parts.append('</ul>')
    # agency
    parts.append('<h3>%s</h3><ul>'%H('agency'))
    parts.append('<li>Conant, R. C., &amp; Ashby, W. R. &ldquo;Every good regulator of a system must be a model of that system&rdquo; (1970).</li>')
    parts.append('<li>Friston, K. &ldquo;The free-energy principle: a unified brain theory?&rdquo; <cite>Nature Reviews Neuroscience</cite> (2010).</li>')
    parts.append('<li>Parr, T., Pezzulo, G., &amp; Friston, K. <cite>Active Inference</cite> (2022).</li>')
    parts.append('<li>Kirchhoff, M. et al. &ldquo;The Markov blankets of life.&rdquo; <cite>J. Royal Society Interface</cite> (2018).</li>')
    parts.append('</ul>')
    # basal
    parts.append('<h3>%s</h3><ul>'%H('basal'))
    parts.append('<li>Levin, M. &ldquo;Bioelectric signaling: reprogrammable circuits underlying embryogenesis, regeneration, and cancer.&rdquo; <cite>Cell</cite> (2021).</li>')
    parts.append('<li>Levin, M. &ldquo;Bioelectric networks: the cognitive glue enabling evolutionary scaling.&rdquo; <cite>Animal Cognition</cite> (2023).</li>')
    parts.append('<li>Levin, M., &amp; Dennett, D. &ldquo;Cognition all the way down.&rdquo; <cite>Aeon</cite> (2020).</li>')
    parts.append('</ul>')
    # beauty
    parts.append('<h3>%s</h3><ul>'%H('beauty'))
    parts.append('<li>Berlyne, D. E. <cite>Aesthetics and Psychobiology</cite> (1971). '+L('Arousal, novelty, complexity, the inverted-U.','Збудження, новизна, складність, перевернута U.','Возбуждение, новизна, сложность, перевёрнутая U.')+'</li>')
    parts.append('<li>Marin, M. M. et al. &ldquo;Berlyne Revisited.&rdquo; <cite>Frontiers in Human Neuroscience</cite> (2016). '+L('Why the evidence is mixed.','Чому свідчення суперечливі.','Почему свидетельства противоречивы.')+'</li>')
    parts.append('<li>Chmiel, A., &amp; Schubert, E. &ldquo;Back to the inverted-U for music preference.&rdquo; <cite>Psychology of Music</cite> (2017).</li>')
    parts.append('</ul>')
    # ideology
    parts.append('<h3>%s</h3><ul>'%H('ideo'))
    parts.append('<li>Dawkins, R. <cite>The Selfish Gene</cite> (1976). '+L('The origin of &ldquo;meme&rdquo;; treat as heuristic, not settled science of culture.','Походження поняття &laquo;мем&raquo;; брати як евристику, а не усталену науку про культуру.','Происхождение понятия &laquo;мем&raquo;; брать как эвристику, а не устоявшуюся науку о культуре.')+'</li>')
    parts.append('<li>Homer-Dixon, T. et al. &ldquo;A Complex Systems Approach to the Study of Ideology.&rdquo; <cite>J. Social and Political Psychology</cite> (2013).</li>')
    parts.append('<li>Arendt, H. <cite>The Origins of Totalitarianism</cite> (1951).</li>')
    parts.append('<li>Adorno, T. W. et al. <cite>The Authoritarian Personality</cite> (1950).</li>')
    parts.append('<li>Hoffer, E. <cite>The True Believer</cite> (1951).</li>')
    parts.append('<li>Snyder, T. &ldquo;We Should Say It. Russia Is Fascist&rdquo; (2022). '+L('On <em>ruscism</em>; offered as a political-historical diagnosis, and contested as a taxonomic label.','Про <em>рашизм</em>; запропоновано як політико-історичний діагноз і заперечувано як таксономічний ярлик.','О <em>рашизме</em>; предложено как политико-исторический диагноз и оспаривается как таксономический ярлык.')+'</li>')
    parts.append('</ul>')
    # metaphysics
    parts.append('<h3>%s</h3><ul>'%H('meta'))
    parts.append('<li>Plato. <cite>Phaedo</cite>, <cite>Republic</cite>, <cite>Parmenides</cite>, <cite>Timaeus</cite>. '+L('The theory of Forms.','Теорія форм (ейдосів).','Теория форм (эйдосов).')+'</li>')
    parts.append('<li>Whitehead, A. N. <cite>Process and Reality</cite> (1929). '+L('Eternal objects and &ldquo;ingression.&rdquo;','Вічні об&rsquo;єкти та &laquo;інгресія&raquo;.','Вечные объекты и &laquo;ингрессия&raquo;.')+'</li>')
    parts.append('<li>Penrose, R. <cite>The Road to Reality</cite> (2004). '+L('A modern mathematical Platonism.','Сучасний математичний платонізм.','Современный математический платонизм.')+'</li>')
    parts.append('</ul>')
    return "".join(parts)
D['sources.full']={'en':src_full('en'),'uk':src_full('uk'),'ru':src_full('ru')}

add('footer','From Pattern to Mind &middot; a thinking artifact, revised against criticism more than once.',
 'Від патерну до розуму &middot; артефакт для мислення, не раз перероблений у відповідь на критику.',
 'От паттерна к разуму &middot; артефакт для мышления, не раз переработанный в споре с критикой.')

# ================= ASSEMBLE index.html =================
def el(tag, cls, key, extra=''):
    return '<%s class="%s" data-i18n="%s"%s>%s</%s>'%(tag,cls,key,(' '+extra if extra else ''),D[key]['en'],tag)

CARDS=[
 ('interlude-0','k-blue','ladder'),
 ('interlude-logic','k-blue','logic'),
 ('interlude-1','k-blue','agency'),
 ('interlude-compute','k-blue','compute'),
 ('interlude-2','k-mint','beauty'),
 ('interlude-3','k-blue','reality'),
 ('interlude-exist','k-purp','existence'),
 ('interlude-4','k-mint','ideas'),
 ('interlude-5','k-purp','selection'),
]

def build_cards():
    o=[]
    for img,kc,key in CARDS:
        o.append('<section class="scene card is-short" style="background-image:url(\'fptm-assets/%s.webp\')">'%img)
        o.append('<button type="button" class="cardtoggle" aria-label="Toggle detail"></button>')
        o.append('<p class="kicker %s" data-i18n="k.%s">%s</p>'%(kc,key,D['k.'+key]['en']))
        o.append('<div class="card-short" data-i18n="%s.short">%s</div>'%(key,D[key+'.short']['en']))
        o.append('<div class="card-full" data-i18n="%s.full">%s</div>'%(key,D[key+'.full']['en']))
        o.append('</section>')
    # open (no toggle)
    o.append('<section class="scene" style="background-image:url(\'fptm-assets/interlude-6.webp\')">')
    o.append('<p class="kicker k-gold" data-i18n="k.open">%s</p>'%D['k.open']['en'])
    o.append('<div data-i18n="open.body">%s</div>'%D['open.body']['en'])
    o.append('</section>')
    # neighbors
    o.append('<section class="scene card is-short" style="background-image:url(\'fptm-assets/interlude-7.webp\')">')
    o.append('<button type="button" class="cardtoggle" aria-label="Toggle detail"></button>')
    o.append('<p class="kicker k-mint" data-i18n="k.neighbors">%s</p>'%D['k.neighbors']['en'])
    o.append('<div class="card-short" data-i18n="neighbors.short">%s</div>'%D['neighbors.short']['en'])
    o.append('<div class="card-full" data-i18n="neighbors.full">%s</div>'%D['neighbors.full']['en'])
    o.append('</section>')
    # sources
    o.append('<section class="sources card is-short">')
    o.append('<button type="button" class="cardtoggle" aria-label="Toggle detail"></button>')
    o.append('<p class="kicker k-mint" data-i18n="k.sources">%s</p>'%D['k.sources']['en'])
    o.append('<h2 data-i18n="sources.h2">%s</h2>'%D['sources.h2']['en'])
    o.append('<div class="card-full" data-i18n="sources.full">%s</div>'%D['sources.full']['en'])
    o.append('</section>')
    return "\n  ".join(o)

CSS = open('_css_block.txt',encoding='utf-8').read() if False else None  # placeholder; replaced below

# read existing file to lift the CSS + the two trailing scripts verbatim
src = open('index.html',encoding='utf-8').read()
style_start = src.index('<style>'); style_end = src.index('</style>')+len('</style>')
STYLE = src[style_start:style_end]
# the two scripts at the end (pan/zoom + toggle)
sidx = src.index('<script>')
if '<script src="i18n.js">' in src:
    SCRIPTS = src[sidx:src.index('<script src="i18n.js">')]
else:
    SCRIPTS = src[sidx:src.rindex('</script>')+len('</script>')]

EXTRA_CSS = """
<style>
/* language switch: pinned, unobtrusive, top-right */
.langswitch{position:fixed; top:14px; right:14px; z-index:60; display:flex; gap:1px;
  padding:3px; border:1px solid var(--line); border-radius:999px;
  background:rgba(8,12,26,.55); -webkit-backdrop-filter:blur(9px); backdrop-filter:blur(9px);
  box-shadow:0 8px 26px -16px rgba(0,0,0,.9)}
.langswitch button{font-family:"Fraunces",serif; font-size:11.5px; letter-spacing:.16em; text-transform:uppercase;
  color:var(--mute); background:transparent; border:0; padding:5px 11px; border-radius:999px; cursor:pointer;
  line-height:1; transition:color .18s, background .18s}
.langswitch button:hover{color:var(--soft)}
.langswitch button.active{color:var(--bg); background:var(--mint)}
@media(max-width:680px){ .langswitch{top:10px; right:10px} .langswitch button{padding:5px 9px; font-size:11px; letter-spacing:.1em} }
/* mode switch: lighter, text-style to match the editorial tone */
.modeswitch{gap:0}
.modeswitch button{border:0; border-bottom:1px solid transparent; border-radius:0; padding:6px 14px; background:transparent; letter-spacing:.06em}
.modeswitch button.active{border-color:var(--mint); background:transparent; color:var(--ink)}
</style>
"""

LANG_SCRIPT = """
<script src="i18n.js"></script>
<script>
(function(){
  var btns = document.querySelectorAll('.langswitch button');
  var svgGroups = document.querySelectorAll('svg .dgroup');
  function setLang(l){
    if(!I18N[l]) l='en';
    document.documentElement.lang = l;
    document.querySelectorAll('[data-i18n]').forEach(function(el){
      var v = I18N[l][el.getAttribute('data-i18n')];
      if(v != null) el.innerHTML = v;
    });
    svgGroups.forEach(function(g){ g.style.display = g.getAttribute('data-lang') === l ? '' : 'none'; });
    btns.forEach(function(b){ b.classList.toggle('active', b.getAttribute('data-lang') === l); });
    if(I18N[l]['doc.title']) document.title = I18N[l]['doc.title'];
    try{ localStorage.setItem('fptm-lang', l); }catch(e){}
  }
  var saved = localStorage.getItem('fptm-lang');
  var def = saved || (navigator.language||'en').slice(0,2).toLowerCase();
  if(['en','uk','ru'].indexOf(def) < 0) def='en';
  btns.forEach(function(b){ b.addEventListener('click', function(){ setLang(b.getAttribute('data-lang')); }); });
  setLang(def);
})();
</script>
"""

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>From Pattern to Mind</title>
<meta name="description" content="A working model of how structure becomes stable, alive, and felt, and how the same machinery can turn an idea into a trap.">
<meta property="og:type" content="article">
<meta property="og:title" content="From Pattern to Mind">
<meta property="og:description" content="One ladder — pattern, attractor, form, agency, mind — and the same lens turned on beauty, computation, and how an idea becomes a trap. Interactive map + essay.">
<meta property="og:url" content="https://latand.github.io/from-pattern-to-mind/">
<meta property="og:image" content="https://latand.github.io/from-pattern-to-mind/from-pattern-to-mind-diagram.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="From Pattern to Mind">
<meta name="twitter:description" content="One ladder — pattern, attractor, form, agency, mind — turned on beauty, computation, and how an idea becomes a trap.">
<meta name="twitter:image" content="https://latand.github.io/from-pattern-to-mind/from-pattern-to-mind-diagram.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&display=swap" rel="stylesheet">
"""

svg = build_svg()

BODY = """</head>
<body class="mode-short">
<div class="langswitch" role="group" aria-label="Language">
  <button type="button" data-lang="en">EN</button>
  <button type="button" data-lang="uk">UK</button>
  <button type="button" data-lang="ru">RU</button>
</div>
<main class="wrap">

<header class="hero reveal d1">
  <p class="eyebrow" data-i18n="eyebrow">__EYEBROW__</p>
  <h1 data-i18n="h1">__H1__</h1>
  <p class="dek" data-i18n="dek">__DEK__</p>
</header>

<div class="modeswitch reveal d2" role="group" aria-label="Reading length">
  <button type="button" data-mode="short" data-i18n="mode.short">__MSHORT__</button>
  <button type="button" data-mode="full" data-i18n="mode.full">__MFULL__</button>
</div>

<div class="rule reveal d2"></div>

<div class="col">
  <p class="lede reveal d2 v-short" data-i18n="lede.short">__LEDESHORT__</p>
  <p class="lede reveal d2 v-full" data-i18n="lede.full">__LEDEFULL__</p>
</div>

<figure class="diagram reveal d2">
  <div class="frame" id="mapFrame"><div class="panzoom" id="panzoom">__SVG__</div>
  <div class="maphint" data-i18n="maphint">__MAPHINT__</div>
  <div class="mapctl">
    <button type="button" data-z="out" aria-label="Zoom out">&minus;</button>
    <button type="button" data-z="in" aria-label="Zoom in">+</button>
    <button type="button" class="reset" data-z="reset" data-i18n="map.reset" aria-label="Reset view">__RESET__</button>
  </div></div>
  <div class="legend">
    <span><i class="hard"></i><span data-i18n="legend.hard">__LGH__</span></span>
    <span><i class="bridge"></i><span data-i18n="legend.bridge">__LGB__</span></span>
    <span><i class="spec"></i><span data-i18n="legend.spec">__LGS__</span></span>
    <span><i class="open"></i><span data-i18n="legend.open">__LGO__</span></span>
  </div>
  <figcaption data-i18n="fig.caption">__FIGCAP__</figcaption>
</figure>

<div class="col">
  __CARDS__
</div>

<footer data-i18n="footer">__FOOTER__</footer>

</main>
"""

BODY = (BODY
 .replace('__EYEBROW__',D['eyebrow']['en']).replace('__H1__',D['h1']['en']).replace('__DEK__',D['dek']['en'])
 .replace('__MSHORT__',D['mode.short']['en']).replace('__MFULL__',D['mode.full']['en'])
 .replace('__LEDESHORT__',D['lede.short']['en']).replace('__LEDEFULL__',D['lede.full']['en'])
 .replace('__MAPHINT__',D['maphint']['en']).replace('__RESET__',D['map.reset']['en'])
 .replace('__LGH__',D['legend.hard']['en']).replace('__LGB__',D['legend.bridge']['en'])
 .replace('__LGS__',D['legend.spec']['en']).replace('__LGO__',D['legend.open']['en'])
 .replace('__FIGCAP__',D['fig.caption']['en']).replace('__FOOTER__',D['footer']['en'])
 .replace('__CARDS__',build_cards())
 .replace('__SVG__',svg))

html = HEAD + STYLE + EXTRA_CSS + BODY + SCRIPTS + LANG_SCRIPT + "\n</body>\n</html>\n"
open('index.html','w',encoding='utf-8').write(html)

# override prose with idiomatic translations authored separately (uk.json / ru.json)
import os
for _lang in ('uk','ru'):
    _p = _lang + '.json'
    if os.path.exists(_p):
        _ov = json.load(open(_p, encoding='utf-8'))
        for _k, _v in _ov.items():
            if _k in D:
                D[_k][_lang] = _v
        print('applied %s overrides: %d keys'%(_lang, len(_ov)))

# i18n.js  (orient by language: I18N[lang][key] = html)
INV = {l:{} for l in LANGS}
for k,v in D.items():
    for l in LANGS:
        INV[l][k] = v[l]
with open('i18n.js','w',encoding='utf-8') as f:
    f.write('const I18N = '+json.dumps(INV,ensure_ascii=False)+';\n')

print('built index.html (%d chars) + i18n.js (%d keys)'%(len(html),len(D)))
