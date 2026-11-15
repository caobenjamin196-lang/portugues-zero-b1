#!/usr/bin/env python3
"""W14 词汇构建：rank 1301-1400 追加到 frequency-vocab.json，动词变位合并进 verb-conjugations.json"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "frequency-vocab.json"
CONJ = ROOT / "data" / "verb-conjugations.json"

C = lambda eu, tu, ele, nos, eles, es: {"eu": eu, "tu": tu, "ele/ela/você": ele, "nós": nos, "eles/elas/vocês": eles, "es": es}

ENTRIES = [
("alma","名词","灵魂 / 心灵","Ela tem uma alma generosa.","她有一颗慷慨的心灵。",{}),
("sombra","名词","影子 / 阴影","Descansamos à sombra da árvore.","我们在树荫下休息。",{}),
("solidão","名词","孤独","A solidão da noite o assustava.","夜晚的孤独让他害怕。",{}),
("silêncio","名词","沉默 / 寂静","Um silêncio pesado caiu na sala.","一阵沉重的沉默笼罩了房间。",{}),
("suspiro","名词","叹息 / 深呼吸","Ela deu um suspiro de alívio.","她松了口气。",{}),
("lágrima","名词","眼泪","Uma lágrima rolou pelo rosto.","一滴泪滑过脸庞。",{}),
("sorriso","名词","微笑","O sorriso dela iluminou o dia.","她的微笑照亮了一天。",{}),
("abraço","名词","拥抱","Ele me deu um abraço apertado.","他给了我一个紧紧的拥抱。",{}),
("beijo","名词","吻","O primeiro beijo foi na praia.","初吻在海边。",{}),
("adeus","名词","永别 / 再见","Dissemos adeus na estação.","我们在车站告别。",{"falseFriend":"葡语 adeus 语气重、偏「永别」，日常再见用 tchau；西语 adiós 日常通用"}),
("despedida","名词","告别 / 送别会","A despedida foi emocionante.","送别很感人。",{}),
("promessa","名词","承诺 / 诺言","Ele cumpriu a promessa.","他兑现了诺言。",{}),
("ternura","名词","温柔 / 柔情","Ela olhou o filho com ternura.","她温柔地看着儿子。",{}),
("paixão","名词","激情 / 热恋","Vivem uma grande paixão.","他们正经历一场热恋。",{}),
("ódio","名词","仇恨","O ódio destrói quem o sente.","仇恨毁掉的是怀有它的人。",{}),
("rancor","名词","积怨 / 怨恨","Ele guarda rancor do passado.","他对过去怀恨在心。",{}),
("mágoa","名词","伤心 / 委屈","A mágoa ainda não passou.","那份伤心还没过去。",{}),
("angústia","名词","焦虑 / 痛苦","A angústia apertava o peito.","焦虑揪紧了胸口。",{}),
("desespero","名词","绝望","No desespero, ele gritou.","绝望中他喊了出来。",{}),
("consolo","名词","安慰","Suas palavras foram um consolo.","她的话是一种安慰。",{}),
("perdão","名词","原谅 / 宽恕","Ele pediu perdão ajoelhado.","他跪着请求原谅。",{}),
("arrependimento","名词","悔恨 / 懊悔","O arrependimento veio tarde.","悔悟来得太晚。",{}),
("sorte","名词","运气","Que sorte a nossa!","我们真走运！",{}),
("azar","名词","坏运气 / 倒霉","Deu azar: choveu no casamento.","真倒霉：婚礼下雨了。",{"falseFriend":"⚠️ 西语 azar = 随机/机遇（中性）；葡语 azar 固定贬义 = 倒霉"}),
("milagre","名词","奇迹","Foi um milagre ninguém se ferir.","没人受伤真是奇迹。",{}),
("fantasia","名词","幻想 / 化妆服","A fantasia virou realidade.","幻想变成了现实。",{}),
("enigma","名词","谜 / 谜团","O caso continua um enigma.","这案子仍是个谜。",{}),
("horizonte","名词","地平线 / 视野","O sol sumiu no horizonte.","太阳消失在地平线上。",{}),
("amanhecer","名词","黎明 / 拂晓","O amanhecer na roça é lindo.","乡下的黎明很美。",{}),
("entardecer","名词","傍晚 / 黄昏","O entardecer pintou o céu.","黄昏染红了天空。",{}),
("anoitecer","名词","夜幕降临","Chegamos ao anoitecer.","我们入夜时到达。",{}),
("brisa","名词","微风","A brisa do mar refrescava.","海风带来凉意。",{}),
("trovão","名词","雷","O trovão assustou as crianças.","雷声吓到了孩子们。",{}),
("relâmpago","名词","闪电","Um relâmpago rachou o céu.","一道闪电划破天空。",{}),
("névoa","名词","薄雾","A névoa cobria o vale.","薄雾笼罩着山谷。",{}),
("neblina","名词","浓雾","A neblina fechou a estrada.","浓雾封锁了道路。",{}),
("maré","名词","潮汐","A maré está subindo.","潮水在上涨。",{}),
("concha","名词","贝壳","Achei uma concha na areia.","我在沙滩上捡到一只贝壳。",{}),
("vela","名词","帆 / 蜡烛","O barco abriu as velas.","船张开了帆。",{}),
("farol","名词","灯塔 / 车灯","O farol guiava os navios.","灯塔为船只引航。",{}),
("porto","名词","港口","O navio atracou no porto.","船停靠在港口。",{}),
("cais","名词","码头","Pescadores no cais ao amanhecer.","黎明时码头上的渔民。",{}),
("trilha","名词","小径 / 步道","A trilha sobe até o pico.","小径一路通到峰顶。",{}),
("atalho","名词","捷径","Pegamos um atalho pelo campo.","我们抄了田间的一条捷径。",{}),
("encruzilhada","名词","十字路口","Paramos na encruzilhada.","我们在十字路口停下。",{}),
("aldeia","名词","村庄","A aldeia fica na montanha.","村庄在山上。",{}),
("vila","名词","小镇 / 居民区","A vila cresceu devagar.","小镇慢慢发展起来。",{}),
("casarão","名词","大宅 / 老宅","O casarão virou museu.","老宅变成了博物馆。",{}),
("sobrado","名词","两层楼房","Mora num sobrado antigo.","他住在一栋老式两层楼房里。",{}),
("varanda","名词","门廊 / 阳台","Tomamos café na varanda.","我们在门廊喝了咖啡。",{}),
("quintal","名词","后院","As crianças brincam no quintal.","孩子们在后院玩。",{}),
("roseira","名词","玫瑰丛","A roseira floresceu na primavera.","玫瑰丛在春天开了花。",{}),
("espinho","名词","刺","O espinho furou o dedo.","刺扎了手指。",{}),
("pétala","名词","花瓣","Pétalas caíram no chão.","花瓣落了一地。",{}),
("tronco","名词","树干","O tronco era oco por dentro.","树干里面是空的。",{}),
("galho","名词","树枝","O pássaro pousou no galho.","鸟落在树枝上。",{}),
("semente","名词","种子","Plantei a semente na horta.","我把种子种在菜园里。",{}),
("vendaval","名词","狂风 / 大风","O vendaval derrubou árvores.","狂风刮倒了大树。",{}),
("penumbra","名词","昏暗 / 半暗","Na penumbra, mal vi o rosto dela.","昏暗中我几乎看不清她的脸。",{}),
("clarão","名词","闪光 / 亮光","Um clarão iluminou a sala.","一道亮光照亮了房间。",{}),
("escuridão","名词","黑暗","A escuridão era total.","一片漆黑。",{}),
("luar","名词","月光","O luar entrava pela janela.","月光从窗户照进来。",{}),
("cantiga","名词","歌谣 / 儿歌","A avó cantava uma cantiga antiga.","祖母唱着一首老歌谣。",{}),
("melodia","名词","旋律","A melodia ficou na cabeça.","旋律萦绕在脑海里。",{}),
("sino","名词","钟","O sino da igreja tocou.","教堂的钟响了。",{"falseFriend":"⚠️ 西语 sino = 命运/而是（连词）；葡语 sino = 钟，「命运」葡语是 destino"}),
("torre","名词","塔","A torre do castelo data do século XVI.","城堡的塔建于十六世纪。",{}),
("ponte","名词","桥","A ponte liga as duas margens.","桥连接两岸。",{}),
("penhasco","名词","悬崖","A casa fica à beira do penhasco.","房子在悬崖边上。",{"falseFriend":"西语 peñasco；注意葡语 nh 对应西语 ñ"}),
("vale","名词","山谷","O vale ficava verde na chuva.","雨后山谷一片翠绿。",{}),
("gruta","名词","岩洞 / 石窟","A gruta escondia um lago.","岩洞里藏着一个湖。",{}),
("poço","名词","水井","O poço secou na estiagem.","水井在旱季干了。",{}),
("riacho","名词","小溪","O riacho cruza a fazenda.","小溪穿过农场。",{}),
("capricho","名词","任性 / 心血来潮","Foi um capricho do destino.","那是命运的一时兴起。",{}),
("afeto","名词","深情 / 慈爱","Ele trata os alunos com afeto.","他深情地对待学生。",{}),
("carinho","名词","疼爱 / 亲昵","Ela fez carinho no gato.","她亲昵地抚摸了猫。",{}),
("delicadeza","名词","细腻 / 体贴","A delicadeza do gesto comoveu todos.","这个体贴的举动感动了大家。",{}),
("doçura","名词","甜美 / 温柔","A doçura da voz dela acalmava.","她甜美的嗓音让人平静。",{}),
("amargura","名词","苦涩 / 痛苦","A amargura marcou seus anos finais.","苦涩伴随了他的晚年。",{}),
("delírio","名词","谵妄 / 狂热","No delírio da febre, falava sem parar.","高烧说胡话时他不停地说。",{}),
("devaneio","名词","胡思乱想 / 呓语","Era só um devaneio de poeta.","那只是诗人的胡思乱想。",{}),
("pesar","名词","悲痛 / 惋惜","Expressou seu pesar pela perda.","他对这个损失表达了悲痛。",{}),
("luto","名词","哀悼 / 丧期","A família está de luto.","一家人在服丧。",{}),
("recordação","名词","回忆 / 纪念品","Guardo a recordação com carinho.","我珍藏着这份回忆。",{}),
("nostalgia","名词","怀旧 / 乡愁","Uma nostalgia tomou conta dele.","一阵乡愁涌上心头。",{}),
("ausência","名词","缺席 / 不在","A ausência dela foi notada.","她的缺席被注意到了。",{}),
("juramento","名词","誓言","Fizeram um juramento de amor.","他们立下爱的誓言。",{}),
("confissão","名词","忏悔 / 坦白","A confissão aliviou a culpa.","坦白减轻了愧疚。",{}),
("orvalho","名词","露水","O orvalho brilhava na grama.","露水在草地上闪光。",{"falseFriend":"西语 rocío；葡语 orvalho——词形完全不同"}),
("suspirar","动词","叹息 / 渴望","Ela suspirou de saudade.","她思念地叹了口气。",{"conj":C("suspiro","suspiras","suspira","suspiramos","suspiram","suspirar: suspiro/suspiras/suspira/suspiramos/suspiran")}),
("sussurrar","动词","低语 / 耳语","Ele sussurrou um segredo.","他悄声说了一个秘密。",{"conj":C("sussurro","sussurras","sussurra","sussurramos","sussurram","susurrar: susurro/susurras/susurra/susurramos/susurran")}),
("soluçar","动词","抽泣 / 呜咽","A criança soluçava baixinho.","孩子小声抽泣着。",{"conj":C("soluço","soluças","soluça","soluçamos","soluçam","sollozar: sollozo/sollozas/solloza/sollozamos/sollozan")}),
("acariciar","动词","爱抚 / 轻抚","Ela acariciou o rosto do filho.","她轻抚着儿子的脸。",{"conj":C("acaricio","acaricias","acaricia","acariciamos","acariciam","acariciar: acaricio/acaricias/acaricia/acariciamos/acarician")}),
("ousar","动词","敢于 / 胆敢","Ninguém ousou discordar.","没人敢反对。",{"conj":C("ouso","ousas","ousa","ousamos","ousam","osar: oso/osas/osa/osamos/osan")}),
("consolar","动词","安慰","Ela consolou o amigo chorando.","她安慰了哭泣的朋友。",{"conj":C("consolo","consolas","consola","consolamos","consolam","consolar: consuelo/consuelas/consuela/consolamos/consuelan（词干 o→ue）")}),
("arrepender","动词","后悔 / 懊悔（常用反身）","Ele se arrependeu de tudo.","他对一切都后悔了。",{"conj":C("arrependo","arrependes","arrepende","arrependemos","arrependem","arrepentirse: me arrepiento/te arrepientes/se arrepiente/nos arrepentimos/se arrepienten")}),
("contemplar","动词","凝视 / 静观","Contemplamos o pôr do sol em silêncio.","我们静静地看日落。",{"conj":C("contemplo","contemplas","contempla","contemplamos","contemplam","contemplar: contemplo/contemplas/contempla/contemplamos/contemplan")}),
("fitar","动词","盯着看 / 注视","Ela fitou os olhos dele.","她注视着他的眼睛。",{"conj":C("fito","fitas","fita","fitamos","fitam","mirar fijamente / clavar la vista")}),
("tremer","动词","颤抖","Suas mãos tremiam de frio.","他的手冻得发抖。",{"conj":C("tremo","tremes","treme","trememos","tremem","temblar: tiemblo/tiemblas/tiembla/temblamos/tiemblan（词干 e→ie）")}),
("vaguear","动词","游荡 / 徘徊","Vagueamos pelas ruas da vila.","我们在小镇的街上闲逛。",{"conj":C("vagueio","vagueias","vagueia","vagueamos","vagueiam","vagar: vago/vagas/vaga/vagamos/vagan")}),
("gemer","动词","呻吟 / 呜咽","O ferido gemia de dor.","伤员疼得呻吟。",{"conj":C("gemo","gemes","geme","gememos","gemem","gemir: gimo/gimes/gime/gemimos/gimen（e→i）")}),
]

assert len(ENTRIES) == 100, len(ENTRIES)

v = json.loads(VOCAB.read_text(encoding="utf-8"))
allpt = {e["pt"] for wk, entries in v.items() if wk.startswith("w") for e in entries}
dups = [pt for pt, *_ in ENTRIES if pt in allpt]
assert not dups, f"重复词: {dups}"

w14 = []
for i, (pt, pos, zh, ex_pt, ex_zh, extra) in enumerate(ENTRIES):
    e = {"rank": 1301 + i, "pt": pt, "pos": pos, "zh": zh,
         "example": {"pt": ex_pt, "zh": ex_zh}}
    if extra.get("derivedFrom"):
        e["derivedFrom"] = extra["derivedFrom"]
    if extra.get("falseFriend"):
        e["falseFriend"] = extra["falseFriend"]
    if extra.get("conj"):
        e["conjugations"] = extra["conj"]
    w14.append(e)

v["w14"] = w14
v["description"] = v["description"].replace("W13=1201-1300。", "W13=1201-1300，W14=1301-1400。")
VOCAB.write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

vc = json.loads(CONJ.read_text(encoding="utf-8"))
have = {x["infinitive"] for x in vc["verbs"]}
NOTES = {
 "suspirar": ("regular -ar", "suspirar de/por = 因…叹息/渴望；suspiro = 叹息"),
 "sussurrar": ("regular -ar", "sussurrar algo a alguém = 对某人耳语"),
 "soluçar": ("regular -ar", "soluçar = 抽泣（介于哭与喘之间）"),
 "acariciar": ("regular -ar", "acariciar = 轻抚；carícia = 爱抚"),
 "ousar": ("regular -ar", "ousar + 不定式 = 敢于做；ousadia = 大胆"),
 "consolar": ("regular -ar", "consolar alguém = 安慰某人；consolo = 安慰"),
 "arrepender": ("regular -er（常用反身）", "arrepender-se de = 后悔…；arrependimento = 悔恨"),
 "contemplar": ("regular -ar", "contemplar = 静观/凝视（带敬意）"),
 "fitar": ("regular -ar", "fitar os olhos em = 注视；文学高频"),
 "tremer": ("regular -er", "tremer de frio/medo = 冷/怕得发抖"),
 "vaguear": ("regular -ar", "vaguear pelas ruas = 在街头游荡"),
 "gemer": ("regular -er", "gemer de dor = 疼得呻吟；gemido = 呻吟声"),
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
vc["description"] = vc["description"].replace(f"（{len(vc['verbs'])-added} 个", f"（{len(vc['verbs'])} 个").replace("W1-W13", "W1-W14")
CONJ.write_text(json.dumps(vc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

verbs = sum(1 for e in w14 if e["pos"] == "动词")
der = sum(1 for e in w14 if "derivedFrom" in e)
ff = sum(1 for e in w14 if "falseFriend" in e)
print(f"OK w14: 100 词 rank 1301-1400 · 动词 {verbs} · 派生 {der} · 假朋友 {ff} · 变位表新增 {added}（总 {len(vc['verbs'])}）")
