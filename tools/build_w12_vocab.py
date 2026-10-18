#!/usr/bin/env python3
"""W12 词汇构建：rank 1101-1200 追加到 frequency-vocab.json，动词变位合并进 verb-conjugations.json"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "frequency-vocab.json"
CONJ = ROOT / "data" / "verb-conjugations.json"

C = lambda eu, tu, ele, nos, eles, es: {"eu": eu, "tu": tu, "ele/ela/você": ele, "nós": nos, "eles/elas/vocês": eles, "es": es}

ENTRIES = [
("embaraçada","形容词","尴尬的 / 难为情的","Ela ficou embaraçada com a pergunta.","她被这个问题弄得很尴尬。",{"falseFriend":"⚠️ 西语 embarazada = 怀孕的！葡语 embaraçada = 尴尬的；「怀孕」葡语说 grávida"}),
("apelido","名词","昵称 / 绰号","Meu apelido na escola era Beto.","我在学校的绰号叫 Beto。",{"falseFriend":"⚠️ 西语 apellido = 姓；葡语 apelido = 绰号，「姓」葡语是 sobrenome"}),
("sobrenome","名词","姓","Silva é o sobrenome mais comum do Brasil.","Silva 是巴西最常见的姓。",{"falseFriend":"⚠️ 西语 sobrenombre = 绰号；葡语 sobrenome = 姓——与 apelido 恰好对调"}),
("balcão","名词","柜台 / 吧台","Ele pagou no balcão.","他在柜台付了钱。",{"falseFriend":"⚠️ 西语 balcón = 阳台；葡语 balcão = 柜台，「阳台」葡语是 sacada/varanda"}),
("sacada","名词","阳台 / 妙语","O apartamento tem uma sacada grande.","这套公寓有个大阳台。",{"falseFriend":"⚠️ 西语 sacada = 取出/发球；葡语 sacada = 阳台（也=妙语 sacada genial）"}),
("manga","名词","芒果 / 袖子","Comprei mangas na feira.","我在集市买了芒果。",{"falseFriend":"⚠️ 西语 manga = 袖子、芒果是 mango；葡语 manga 兼指芒果和袖子"}),
("receita","名词","食谱 / 处方 / 收入","A receita do bolo é da minha avó.","这个蛋糕食谱是我祖母的。",{}),
("padaria","名词","面包店","A padaria abre às seis.","面包店六点开门。",{}),
("açougue","名词","肉店","Comprei carne no açougue.","我在肉店买了肉。",{}),
("feira","名词","集市 / 展会","A feira livre é aos sábados.","露天集市每周六开。",{}),
("supermercado","名词","超市","O supermercado fecha às dez.","超市十点关门。",{}),
("lanchonete","名词","小吃店 / 快餐店","Almocei numa lanchonete.","我在小吃店吃了午饭。",{}),
("farmácia","名词","药店","A farmácia fica na esquina.","药店在街角。",{}),
("consulta","名词","问诊 / 查询","Tenho consulta às três.","我三点有门诊。",{}),
("xarope","名词","糖浆 / 止咳糖浆","Tomei um xarope para tosse.","我喝了止咳糖浆。",{"falseFriend":"西语 jarabe；葡语 xarope——词形完全不同"}),
("toalha","名词","毛巾","Peguei uma toalha limpa.","我拿了一条干净毛巾。",{}),
("joelho","名词","膝盖","Machuquei o joelho jogando bola.","我踢球伤了膝盖。",{}),
("lanche","名词","点心 / 快餐","Fiz um lanche à tarde.","下午我吃了点心。",{}),
("pipoca","名词","爆米花","Compramos pipoca no cinema.","我们在电影院买了爆米花。",{}),
("abacaxi","名词","菠萝","O abacaxi está maduro.","菠萝熟了。",{"falseFriend":"西语 piña；葡语 abacaxi——西语 ananás 在葡语指南洋品种，日常说 abacaxi"}),
("xícara","名词","（带把的）杯子","Uma xícara de café, por favor.","请来一杯咖啡。",{}),
("compromisso","名词","约会 / 承诺 / 日程安排","Tenho um compromisso às oito.","我八点有个约。",{"falseFriend":"西语 compromiso = 承诺；葡语 compromisso 兼指「约会/日程」——Tenho um compromisso = 我有约"}),
("legal","形容词","酷的 / 棒的（口语）；合法的","Que filme legal!","多棒的电影！",{"falseFriend":"西语 legal 口语也=棒（拉美）；葡语 legal 使用频率极高，注意它兼指「合法的」"}),
("beleza","名词","美；（口语）好/没问题","— Vamos lá às sete? — Beleza!","「七点见？」「好！」",{}),
("valeu","感叹词","谢了（口语）","Valeu pela ajuda!","谢谢帮忙！",{"falseFriend":"西语用 vale/gracias；葡语 valeu 来自 valer 的过去时，巴西口语万能道谢词"}),
("cara","名词","脸；（口语）家伙","Esse cara é muito gente boa.","那家伙人很好。",{"falseFriend":"西语 cara = 脸；葡语 cara 口语兼指「家伙/人」（类似 tío）"}),
("mano","名词","哥们（口语）","E aí, mano? Tudo bem?","哥们，最近怎样？",{}),
("gata","名词","母猫；（口语）美女","A gata do vizinho sumiu.","邻居家的母猫丢了。",{"falseFriend":"西语 gata = 母猫；葡语口语 gata 也=美女（gato=帅哥），注意语境"}),
("grana","名词","钱（口语）","Estou sem grana este mês.","这个月我没钱。",{}),
("trampo","名词","活儿 / 工作（口语）","O trampo foi puxado.","这活儿很累。",{}),
("perrengue","名词","困境 / 折腾（口语）","Passei um perrengue no aeroporto.","我在机场折腾惨了。",{}),
("rolê","名词","出门玩 / 兜风（口语）","Vamos dar um rolê no centro?","去市中心逛逛吗？",{}),
("baita","形容词","巨大的 / 超棒的（口语）","Uma baita festa!","超棒的派对！",{}),
("balada","名词","夜店 / 派对（口语）","A balada começa à meia-noite.","夜店午夜开场。",{}),
("jeitinho","名词","小聪明 / 变通办法","Ele deu um jeitinho e resolveu.","他想了个变通办法解决了。",{}),
("gambiarra","名词","土法临时修补","Fiz uma gambiarra no chuveiro.","我给淋浴器做了个土法应急修理。",{}),
("cafuné","名词","亲昵地挠头","Ela fez cafuné no filho.","她亲昵地挠了挠儿子的头。",{}),
("xodó","名词","心头好 / 宝贝","Esse copo é meu xodó.","这个杯子是我的心头好。",{}),
("zoeira","名词","胡闹 / 玩笑（口语）","É só zoeira, não leva a sério.","只是玩笑，别当真。",{}),
("firmeza","名词","可靠 / 赞（口语）","Esse cara é firmeza.","这人很靠谱。",{}),
("mó","副词","非常（口语，maior 缩合）","Foi mó legal.","简直太棒了。",{}),
("discurso","名词","演说 / 话语","O discurso durou uma hora.","演说持续了一小时。",{}),
("faculdade","名词","大学（本科）/ 学院","Ela estuda numa faculdade pública.","她在一所公立大学读书。",{}),
("palestra","名词","讲座","A palestra foi lotada.","讲座座无虚席。",{}),
("sessão","名词","场次 / 会议","A sessão das oito está esgotada.","八点场售罄了。",{}),
("ingresso","名词","门票 / 入场券","Comprei os ingressos online.","我在网上买了票。",{"falseFriend":"⚠️ 西语 ingreso = 收入/入学；葡语 ingresso = 门票（西语门票 = entrada/boleto）"}),
("cartaz","名词","海报","O cartaz do filme é bonito.","电影海报很好看。",{}),
("folheto","名词","小册子 / 传单","Distribuíram folhetos na rua.","他们在街上发传单。",{}),
("dicionário","名词","词典","Consultei o dicionário.","我查了词典。",{}),
("gramática","名词","语法（书）","A gramática do português.","葡语语法。",{}),
("vocabulário","名词","词汇（表）","Meu vocabulário está crescendo.","我的词汇量在增长。",{}),
("sinônimo","名词","同义词","Qual é o sinônimo de rápido?","rápido 的同义词是什么？",{}),
("antônimo","名词","反义词","O antônimo de alto é baixo.","alto 的反义词是 baixo。",{}),
("provérbio","名词","谚语","Um provérbio brasileiro famoso.","一句著名的巴西谚语。",{}),
("ditado","名词","俗语 / 听写","Um ditado popular: quem canta seus males espanta.","一句俗语：唱歌驱忧。",{"falseFriend":"西语 dictado = 听写；葡语 ditado 兼指俗语（ditado popular）"}),
("gíria","名词","俚语","Gíria de jovem muda rápido.","年轻人的俚语变得快。",{}),
("sotaque","名词","口音","Ela tem sotaque carioca.","她有里约口音。",{"falseFriend":"⚠️ 西语 acento 兼指口音和重音符号；葡语「口音」= sotaque，acento 只=重音符号"}),
("dialeto","名词","方言","Os dialetos do nordeste.","东北部的方言。",{}),
("pronúncia","名词","发音","Sua pronúncia é ótima.","你的发音很棒。",{}),
("ortografia","名词","拼写 / 正字法","A reforma ortográfica de 2009.","2009 年正字法改革。",{}),
("acento","名词","重音符号","O acento agudo do é.","é 的尖音符。",{}),
("hífen","名词","连字符","Palavras com hífen.","带连字符的词。",{}),
("pontuação","名词","标点","Revise a pontuação.","检查一下标点。",{}),
("maiúscula","名词","大写字母","Comece com letra maiúscula.","用大写字母开头。",{}),
("minúscula","名词","小写字母","Escreva em minúsculas.","用小写写。",{}),
("itálico","名词","斜体","A palavra está em itálico.","这个词是斜体。",{}),
("negrito","名词","粗体","O título está em negrito.","标题是粗体。",{}),
("parágrafo","名词","段落","Leia o primeiro parágrafo.","读第一段。",{}),
("verso","名词","诗句","Um verso de Drummond.","德鲁蒙德的一句诗。",{}),
("rima","名词","押韵","Amor rima com dor.","amor 和 dor 押韵。",{}),
("poema","名词","诗","Escreveu um poema para ela.","他为她写了一首诗。",{}),
("poeta","名词","诗人","O poeta morreu jovem.","诗人英年早逝。",{}),
("fábula","名词","寓言","Uma fábula de Esopo.","一则伊索寓言。",{}),
("crônica","名词","纪事小品文（巴西特色文体）","A crônica sai no jornal de domingo.","小品文登在周日报纸上。",{}),
("ensaio","名词","随笔 / 散文","Um ensaio sobre a saudade.","一篇关于 saudade 的随笔。",{}),
("narrativa","名词","叙事","A narrativa é envolvente.","叙事引人入胜。",{}),
("protagonista","名词","主角","O protagonista é um menino.","主角是个男孩。",{}),
("narrador","名词","叙述者","O narrador conta tudo em primeira pessoa.","叙述者用第一人称讲述一切。",{}),
("desfecho","名词","结局","O desfecho surpreendeu todos.","结局出乎所有人意料。",{}),
("ironia","名词","讽刺","A ironia do texto é sutil.","文章的讽刺很含蓄。",{}),
("humor","名词","幽默 / 心情","O humor do autor é único.","作者的幽默独一无二。",{}),
("metáfora","名词","隐喻","Uma metáfora bonita.","一个漂亮的隐喻。",{}),
("linguagem","名词","语言 / 语言风格","A linguagem do poema é simples.","这首诗的语言很朴实。",{}),
("formal","形容词","正式的","Linguagem formal.","正式语言。",{}),
("informal","形容词","非正式的","Um tom informal.","非正式的语气。",{}),
("coloquial","形容词","口语的","Expressão coloquial.","口语表达。",{}),
("trocadilho","名词","双关 / 文字游戏","Um trocadilho engraçado.","一个有趣的双关。",{}),
("pressa","名词","匆忙","Sem pressa!","不着急！",{}),
("topar","动词","愿意 / 接受（口语）","Ele topou na hora.","他当场就答应了。",{"falseFriend":"⚠️ 西语 topar = 碰撞/偶遇；葡语口语 topar = 愿意（topar com = 偶遇）","conj":C("topo","topas","topa","topamos","topam","topar: topo/topas/topa/topamos/topan（西语=碰撞）")}),
("aprontar","动词","捣乱 / 准备（口语）","As crianças aprontaram na aula.","孩子们上课时捣乱了。",{"conj":C("apronto","aprontas","apronta","aprontamos","aprontam","preparar: preparo/preparas/prepara/preparamos/preparan")}),
("zoar","动词","取笑 / 闹腾（俚语）","Eles zoaram o amigo.","他们取笑了朋友。",{"conj":C("zoo","zoas","zoa","zoamos","zoam","bromear: bromeo/bromeas/bromea/bromeamos/bromean")}),
("paquerar","动词","调情 / 眉目传情","Ele paquerou a colega.","他跟同事调情。",{"conj":C("paquero","paqueras","paquera","paqueramos","paqueram","coquetear: coqueteo/coqueteas/coquetea/coqueteamos/coquetean")}),
("pospor","动词","推迟 / 置于…后（pôr 加前缀 pos-）","O jogo foi posposto.","比赛被推迟了。",{"derivedFrom":"pôr","conj":C("posponho","pospões","pospõe","pospomos","pospõem","posponer: pospongo/pospones/pospone/posponemos/posponen")}),
("retrair","动词","缩回 / 使退缩（trazer 加前缀 re-）","O gato retraiu as garras.","猫收回了爪子。",{"derivedFrom":"trazer","conj":C("retraio","retrais","retrai","retraímos","retraem","retraer: retraigo/retraes/retrae/retraemos/retraen")}),
("encobrir","动词","掩盖 / 包庇（cobrir 加前缀 en-）","Ele tentou encobrir o erro.","他试图掩盖错误。",{"derivedFrom":"cobrir","conj":C("encubro","encobres","encobre","encobrimos","encobrem","encubrir: encubro/encubres/encubre/encubrimos/encubren")}),
("vestir","动词","穿（衣）","Ela vestiu o casaco e saiu.","她穿上外套出门了。",{"conj":C("visto","vestes","veste","vestimos","vestem","vestir: visto/vistes/viste/vestimos/visten")}),
("despedir","动词","解雇 / 送别（pedir 加前缀 des-）","Despedimo-nos na porta.","我们在门口道别了。",{"derivedFrom":"pedir","conj":C("despeço","despedes","despede","despedimos","despedem","despedir: despido/despides/despide/despedimos/despiden")}),
("desmentir","动词","否认 / 辟谣（mentir 加前缀 des-）","O ministro desmentiu a notícia.","部长否认了这条新闻。",{"derivedFrom":"mentir","conj":C("desminto","desmentes","desmente","desmentimos","desmentem","desmentir: desmiento/desmientes/desmiente/desmentimos/desmienten")}),
("divertir","动词","使开心 / 娱乐","O palhaço divertiu as crianças.","小丑逗乐了孩子们。",{"conj":C("divirto","divertes","diverte","divertimos","divertem","divertir: divierto/diviertes/divierte/divertimos/divierten")}),
("surgir","动词","出现 / 涌现","Surgiu um problema novo.","出现了一个新问题。",{"conj":C("surjo","surges","surge","surgimos","surgem","surgir: surjo/surges/surge/surgimos/surgen")}),
]

assert len(ENTRIES) == 100, len(ENTRIES)

v = json.loads(VOCAB.read_text(encoding="utf-8"))
allpt = {e["pt"] for wk, entries in v.items() if wk.startswith("w") for e in entries}
dups = [pt for pt, *_ in ENTRIES if pt in allpt]
assert not dups, f"重复词: {dups}"

w12 = []
for i, (pt, pos, zh, ex_pt, ex_zh, extra) in enumerate(ENTRIES):
    e = {"rank": 1101 + i, "pt": pt, "pos": pos, "zh": zh,
         "example": {"pt": ex_pt, "zh": ex_zh}}
    if extra.get("derivedFrom"):
        e["derivedFrom"] = extra["derivedFrom"]
    if extra.get("falseFriend"):
        e["falseFriend"] = extra["falseFriend"]
    if extra.get("conj"):
        e["conjugations"] = extra["conj"]
    w12.append(e)

v["w12"] = w12
v["description"] = v["description"].replace("W11=1001-1100。", "W11=1001-1100，W12=1101-1200。")
VOCAB.write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

vc = json.loads(CONJ.read_text(encoding="utf-8"))
have = {x["infinitive"] for x in vc["verbs"]}
NOTES = {
 "topar": ("regular -ar", "topar + 不定式 = 愿意做；topar com = 偶遇"),
 "aprontar": ("regular -ar", "aprontar (algo) = 捣乱/准备；口语高频"),
 "zoar": ("regular -ar", "zoar alguém = 取笑某人；名词 zoeira"),
 "paquerar": ("regular -ar", "paquerar alguém = 和某人调情；名词 paquera"),
 "pospor": ("irregular（pôr 族）", "正式用词：pospor para + 日期；perfeito pospôs"),
 "retrair": ("irregular（trazer 族）", "retrair-se = 退缩；分词 retraído（也=内向的）"),
 "encobrir": ("irregular（cobrir 族）", "eu encubro；encobrir um crime = 包庇罪行"),
 "vestir": ("irregular", "eu visto（e→i）；vestir-se = 穿衣服（反身）"),
 "despedir": ("irregular（pedir 族）", "eu despeço；despedir-se de = 向…告别"),
 "desmentir": ("irregular（mentir 族）", "eu desminto；desmentir um boato = 辟谣"),
 "divertir": ("irregular", "eu divirto；divertir-se = 玩得开心（反身）"),
 "surgir": ("regular -ir（词干 g→j）", "eu surjo；surgir de/em = 出现于"),
}
added = 0
for pt, pos, zh, ex_pt, ex_zh, extra in ENTRIES:
    if not extra.get("conj") or pt in have:
        continue
    conj = extra["conj"]
    typ, note = NOTES[pt]
    vc["verbs"].append({
        "infinitive": pt,
        "meaning": zh.split("（")[0],
        "type": typ,
        "conjugation": {k: conj[k] for k in ["eu", "tu", "ele/ela/você", "nós", "eles/elas/vocês"]},
        "spanish": conj["es"],
        "note": note,
    })
    added += 1
vc["description"] = vc["description"].replace(f"（{len(vc['verbs'])-added} 个", f"（{len(vc['verbs'])} 个").replace("W1-W11", "W1-W12")
CONJ.write_text(json.dumps(vc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

verbs = sum(1 for e in w12 if e["pos"] == "动词")
der = sum(1 for e in w12 if "derivedFrom" in e)
ff = sum(1 for e in w12 if "falseFriend" in e)
print(f"OK w12: 100 词 rank 1101-1200 · 动词 {verbs} · 派生 {der} · 假朋友 {ff} · 变位表新增 {added}（总 {len(vc['verbs'])}）")
