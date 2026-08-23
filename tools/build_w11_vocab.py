#!/usr/bin/env python3
"""W11 词汇构建：rank 1001-1100 追加到 frequency-vocab.json，动词变位合并进 verb-conjugations.json"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "frequency-vocab.json"
CONJ = ROOT / "data" / "verb-conjugations.json"

C = lambda eu, tu, ele, nos, eles, es: {"eu": eu, "tu": tu, "ele/ela/você": ele, "nós": nos, "eles/elas/vocês": eles, "es": es}

ENTRIES = [
("biografia","名词","传记","A biografia do inventor saiu em maio.","这位发明家的传记五月出版。",{}),
("autobiografia","名词","自传","Ela está escrevendo a autobiografia.","她正在写自传。",{}),
("antepassado","名词","祖先","Meus antepassados vieram da Itália.","我的祖先来自意大利。",{}),
("descendente","名词","后代 / 后裔","Ele é descendente de japoneses.","他是日本后裔。",{}),
("geração","名词","一代人","A nova geração lê menos.","新一代读书更少。",{}),
("herança","名词","遗产","Recebeu uma herança da avó.","他继承了祖母的遗产。",{}),
("origem","名词","出身 / 起源","Qual é a origem da palavra?","这个词的起源是什么？",{}),
("raiz","名词","根 / 根源","As raízes da cultura brasileira.","巴西文化的根源。",{}),
("reino","名词","王国","O reino durou três séculos.","这个王国延续了三百年。",{}),
("império","名词","帝国","O Império do Brasil acabou em 1889.","巴西帝国于 1889 年终结。",{}),
("colônia","名词","殖民地","O Brasil foi colônia de Portugal.","巴西曾是葡萄牙的殖民地。",{}),
("independência","名词","独立","A independência foi em 1822.","独立发生于 1822 年。",{}),
("revolução","名词","革命","A revolução mudou o país.","革命改变了这个国家。",{}),
("batalha","名词","战役","A batalha durou dois dias.","战役持续了两天。",{}),
("conquista","名词","征服 / 成就","Uma grande conquista da ciência.","科学的一项伟大成就。",{}),
("descobrimento","名词","发现（大发现）","O descobrimento do Brasil foi em 1500.","巴西的发现是在 1500 年。",{}),
("navegação","名词","航海 / 浏览","As navegações abriram novas rotas.","大航海开辟了新航线。",{}),
("expedição","名词","远征 / 考察","A expedição chegou ao polo sul.","考察队抵达了南极。",{}),
("explorador","名词","探险家","O explorador escreveu um diário.","探险家写了一本日记。",{}),
("escravo","名词","奴隶","Os escravos trabalhavam nas fazendas.","奴隶们在种植园劳作。",{}),
("escravidão","名词","奴隶制","A escravidão foi abolida em 1888.","奴隶制于 1888 年被废除。",{}),
("abolição","名词","废除","A abolição foi uma conquista.","废奴是一项伟大的成就。",{}),
("rei","名词","国王","O rei assinou o decreto.","国王签署了法令。",{}),
("rainha","名词","女王 / 王后","A rainha visitou o Brasil.","女王访问了巴西。",{}),
("coroa","名词","王冠","A coroa era de ouro.","王冠是黄金做的。",{}),
("trono","名词","王位","Ele subiu ao trono aos cinco anos.","他五岁登上王位。",{}),
("general","名词","将军","O general liderou o exército.","将军率领了军队。",{}),
("soldado","名词","士兵","Os soldados voltaram para casa.","士兵们回家了。",{}),
("exército","名词","军队","O exército foi derrotado.","军队被打败了。",{}),
("bandeira","名词","旗帜","A bandeira do Brasil é verde e amarela.","巴西国旗是绿黄相间的。",{}),
("hino","名词","国歌 / 赞歌","O hino nacional tocou no estádio.","体育场奏响了国歌。",{}),
("símbolo","名词","象征","O pão-de-açúcar é símbolo do Rio.","糖面包山是里约的象征。",{}),
("monumento","名词","纪念碑","O monumento atrai turistas.","这座纪念碑吸引游客。",{}),
("estátua","名词","雕像","A estátua fica no centro da praça.","雕像在广场中央。",{}),
("museu","名词","博物馆","O museu abre às dez.","博物馆十点开门。",{}),
("ruína","名词","遗迹 / 废墟","As ruínas da cidade antiga.","古城遗迹。",{}),
("tesouro","名词","宝藏","Encontraram um tesouro no navio.","他们在船上发现了宝藏。",{}),
("ouro","名词","黄金","O ouro foi levado para Portugal.","黄金被运去了葡萄牙。",{}),
("prata","名词","白银 / 银","Uma medalha de prata.","一枚银牌。",{}),
("ciclo","名词","周期 / 循环","O ciclo do ouro durou décadas.","黄金周期持续了几十年。",{}),
("prosperidade","名词","繁荣","Um período de prosperidade.","一段繁荣时期。",{}),
("declínio","名词","衰落","O declínio do império foi lento.","帝国的衰落是缓慢的。",{}),
("queda","名词","衰落 / 下跌","A queda da monarquia.","君主制的倒台。",{}),
("ascensão","名词","崛起 / 上升","A ascensão do novo líder.","新领袖的崛起。",{}),
("glória","名词","荣耀","Um momento de glória.","荣耀的时刻。",{}),
("derrota","名词","失败","A derrota foi anunciada no rádio.","失败的消息在广播里宣布了。",{}),
("vitória","名词","胜利","A vitória mudou a história.","这场胜利改变了历史。",{}),
("herói","名词","英雄","Ele virou herói nacional.","他成了民族英雄。",{}),
("lenda","名词","传说","A lenda conta outra versão.","传说讲述了另一个版本。",{}),
("mito","名词","神话","Um mito da cultura indígena.","原住民文化的一个神话。",{}),
("figura","名词","人物 / 形象","Uma figura importante da história.","历史上的重要人物。",{}),
("personalidade","名词","名人 / 个性","Uma personalidade marcante.","一位有影响力的名人。",{}),
("legado","名词","（精神）遗产","Seu legado vive até hoje.","他的遗产流传至今。",{}),
("pioneiro","名词","先驱","Um pioneiro da aviação.","航空先驱。",{}),
("líder","名词","领袖","O líder fez um discurso.","领袖发表了演说。",{}),
("movimento","名词","运动","O movimento abolicionista cresceu.","废奴运动壮大了。",{}),
("resistência","名词","抵抗","A resistência durou anos.","抵抗持续了数年。",{}),
("luta","名词","斗争","A luta pela liberdade.","为自由而斗争。",{}),
("igualdade","名词","平等","A igualdade de direitos.","权利平等。",{}),
("humanidade","名词","人类 / 人性","Um presente para a humanidade.","给人类的礼物。",{}),
("civilização","名词","文明","Uma civilização antiga.","一个古老的文明。",{}),
("época","名词","时代","Naquela época, não havia luz elétrica.","那个时代还没有电灯。",{}),
("período","名词","时期","O período colonial.","殖民时期。",{}),
("fase","名词","阶段","Uma fase difícil da vida.","人生的艰难阶段。",{}),
("etapa","名词","阶段 / 步骤","A próxima etapa do projeto.","项目的下一阶段。",{}),
("contemporâneo","形容词","当代的","Arte contemporânea.","当代艺术。",{}),
("antigo","形容词","古老的 / 前任的","Um costume antigo.","一个古老的习俗。",{}),
("moderno","形容词","现代的","O mundo moderno.","现代世界。",{}),
("atual","形容词","当前的","O governo atual.","现任政府。",{"falseFriend":"西语 actual 也=当前的；但西语 actualmente=目前，葡语 atualmente 同义——注意葡语「实际的」是 real/efetivo"}),
("recente","形容词","最近的","Uma descoberta recente.","最近的发现。",{}),
("arquivo","名词","档案馆 / 文件","O documento está no arquivo.","文件在档案馆里。",{}),
("testemunho","名词","证词 / 见证","Seu testemunho foi decisivo.","他的证词起了决定性作用。",{}),
("relato","名词","叙述 / 讲述","O relato da viagem emocionou todos.","旅行叙述感动了所有人。",{}),
("pesquisador","名词","研究员","A pesquisadora estudou os documentos.","研究员研究了这些文件。",{}),
("historiador","名词","历史学家","O historiador publicou um livro.","历史学家出版了一本书。",{}),
("especialista","名词","专家","Uma especialista em história.","一位历史专家。",{}),
("retrato","名词","肖像 / 写照","Um retrato da época.","那个时代的写照。",{}),
("trajetória","名词","轨迹 / 历程","Uma trajetória impressionante.","一段令人敬佩的历程。",{}),
("carreira","名词","职业生涯","Sua carreira começou cedo.","他的职业生涯开始得很早。",{}),
("enterro","名词","葬礼","O enterro foi no domingo.","葬礼在周日举行。",{}),
("homenagem","名词","致敬","Uma homenagem ao inventor.","向发明家致敬。",{}),
("descoberta","名词","发现","A descoberta mudou a medicina.","这一发现改变了医学。",{}),
("invenção","名词","发明","A invenção do avião.","飞机的发明。",{}),
("criação","名词","创造 / 创作","A criação do parque levou anos.","公园的创建历时数年。",{}),
("contribuição","名词","贡献","Uma contribuição enorme.","巨大的贡献。",{}),
("realização","名词","成就 / 实现","Sua maior realização.","他最大的成就。",{}),
("prêmio","名词","奖项","Ganhou um prêmio internacional.","他获得了一个国际奖项。",{}),
("reconhecimento","名词","认可 / 承认","O reconhecimento veio tarde.","认可姗姗来迟。",{}),
("abster-se","动词","弃权 / 克制（ter 加前缀 abs-）","Três países se abstiveram na votação.","三个国家在投票中弃权。",{"derivedFrom":"ter","conj":C("me abstenho","te absténs","se abstém","nos abstenmos","se abstêm","abstenerse: me abstengo/te abstienes/se abstiene/nos abstenemos/se abstienen")}),
("subtrair","动词","减去 / 窃取（trazer 加前缀 sub-）","Subtraia dez do total.","从总数中减去十。",{"derivedFrom":"trazer","conj":C("subtraio","subtrais","subtrai","subtraímos","subtraem","sustraer: sustraigo/sustraes/sustrae/sustraemos/sustraen")}),
("transcrever","动词","转录 / 誊写（escrever 加前缀 trans-）","Ela transcreveu a carta antiga.","她誊写了那封古旧的信。",{"derivedFrom":"escrever","conj":C("transcrevo","transcreves","transcreve","transcrevemos","transcrevem","transcribir: transcribo/transcribes/transcribe/transcribimos/transcriben")}),
("sorrir","动词","微笑（rir 加前缀 so-）","Ela sorriu para a foto.","她对着镜头微笑。",{"derivedFrom":"rir","conj":C("sorrio","sorris","sorri","sorrimos","sorriem","sonreír: sonrío/sonríes/sonríe/sonreímos/sonríen")}),
("descobrir","动词","发现（cobrir 加前缀 des-）","Descobriram ouro na região.","他们在该地区发现了黄金。",{"derivedFrom":"cobrir","conj":C("descubro","descobres","descobre","descobrimos","descobrem","descubrir: descubro/descubres/descubre/descubrimos/descubren")}),
("cobrir","动词","覆盖 / 报道","A neve cobriu a cidade.","雪覆盖了城市。",{"conj":C("cubro","cobres","cobre","cobrimos","cobrem","cubrir: cubro/cubres/cubre/cubrimos/cubren")}),
("fugir","动词","逃跑","O ladrão fugiu da prisão.","小偷越狱逃跑了。",{"conj":C("fujo","foges","foge","fugimos","fogem","huir: huyo/huyes/huye/huimos/huyen")}),
("medir","动词","测量 / 量度","O engenheiro mediu a ponte.","工程师测量了大桥。",{"conj":C("meço","medes","mede","medimos","medem","medir: mido/mides/mide/medimos/miden")}),
("pressentir","动词","预感（sentir 加前缀 pres-）","Pressenti que algo ia acontecer.","我预感到有事要发生。",{"derivedFrom":"sentir","conj":C("pressinto","pressentes","pressente","pressentimos","pressentem","presentir: presiento/presientes/presiente/presentimos/presienten")}),
("narrar","动词","叙述 / 讲述","O livro narra a vida do inventor.","这本书讲述了发明家的一生。",{"conj":C("narro","narras","narra","narramos","narram","narrar: narro/narras/narra/narramos/narran")}),
("citar","动词","引用 / 提及","O artigo cita três especialistas.","文章引用了三位专家。",{"conj":C("cito","citas","cita","citamos","citam","citar: cito/citas/cita/citamos/citan")}),
("herdar","动词","继承","Ela herdou a casa dos pais.","她继承了父母的房子。",{"conj":C("herdo","herdas","herda","herdamos","herdam","heredar: heredo/heredas/hereda/heredamos/heredan")}),
]

assert len(ENTRIES) == 100, len(ENTRIES)

v = json.loads(VOCAB.read_text(encoding="utf-8"))
allpt = {e["pt"] for wk, entries in v.items() if wk.startswith("w") for e in entries}
dups = [pt for pt, *_ in ENTRIES if pt in allpt]
assert not dups, f"重复词: {dups}"

w11 = []
for i, (pt, pos, zh, ex_pt, ex_zh, extra) in enumerate(ENTRIES):
    e = {"rank": 1001 + i, "pt": pt, "pos": pos, "zh": zh,
         "example": {"pt": ex_pt, "zh": ex_zh}}
    if extra.get("derivedFrom"):
        e["derivedFrom"] = extra["derivedFrom"]
    if extra.get("falseFriend"):
        e["falseFriend"] = extra["falseFriend"]
    if extra.get("conj"):
        e["conjugations"] = extra["conj"]
    w11.append(e)

v["w11"] = w11
v["description"] = v["description"].replace("W10=901-1000。", "W10=901-1000，W11=1001-1100。")
VOCAB.write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

vc = json.loads(CONJ.read_text(encoding="utf-8"))
have = {x["infinitive"] for x in vc["verbs"]}
NOTES = {
 "abster-se": ("irregular（ter 族，反身）", "abster-se de + 不定式/名词：克制做某事/弃权"),
 "subtrair": ("irregular（trazer 族）", "subtrair de：从…中减去；西语拼写 sustraer（多 s）"),
 "transcrever": ("regular -er（escrever 族）", "⚠️ 西语 transcribir（b）≠ 葡语 transcrever（v）"),
 "sorrir": ("regular -ir（rir 族）", "sorrir para/de：对…微笑；西语 sonreír 词干变位（sonrío）"),
 "descobrir": ("irregular（cobrir 族）", "eu descubro 词干变位：descubro/descobres；西语同构 descubro"),
 "cobrir": ("irregular", "eu cubro 词干变位；分词 coberto（规则）≠ 西语 cubierto"),
 "fugir": ("irregular", "eu fujo（g→j）；fugir de/para：从…逃跑/逃往…"),
 "medir": ("irregular", "eu meço（d→c 拼写变化）；西语 mido 词干变位（e→i）"),
 "pressentir": ("irregular（sentir 族）", "eu pressinto；sentir 族变位规则全部继承"),
 "narrar": ("regular -ar", "西语 narrar 同形同义"),
 "citar": ("regular -ar", "西语 citar 同形同义；也=传唤（法律）"),
 "herdar": ("regular -ar", "herdar de：从…继承；西语 heredar 同义"),
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
vc["description"] = vc["description"].replace(f"（{len(vc['verbs'])-added} 个", f"（{len(vc['verbs'])} 个").replace("W1-W10", "W1-W11")
CONJ.write_text(json.dumps(vc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

verbs = sum(1 for e in w11 if e["pos"] == "动词")
der = sum(1 for e in w11 if "derivedFrom" in e)
ff = sum(1 for e in w11 if "falseFriend" in e)
print(f"OK w11: 100 词 rank 1001-1100 · 动词 {verbs} · 派生 {der} · 假朋友 {ff} · 变位表新增 {added}（总 {len(vc['verbs'])}）")
