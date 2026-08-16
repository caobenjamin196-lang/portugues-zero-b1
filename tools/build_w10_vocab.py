#!/usr/bin/env python3
"""W10 词汇构建：rank 901-1000 追加到 frequency-vocab.json，动词变位合并进 verb-conjugations.json"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "frequency-vocab.json"
CONJ = ROOT / "data" / "verb-conjugations.json"

C = lambda eu, tu, ele, nos, eles, es: {"eu": eu, "tu": tu, "ele/ela/você": ele, "nós": nos, "eles/elas/vocês": eles, "es": es}

ENTRIES = [
("coluna","名词","专栏 / 柱子","Ela escreve uma coluna semanal.","她写一个每周专栏。",{}),
("redação","名词","编辑部 / 作文","A redação fica no segundo andar.","编辑部在二楼。",{}),
("editor","名词","编辑 / 主编","O editor revisou o texto.","编辑审改了稿件。",{}),
("repórter","名词","记者","A repórter fez uma pergunta difícil.","记者问了一个尖锐的问题。",{}),
("entrevista","名词","采访 / 面试","A entrevista sai amanhã no jornal.","采访明天见报。",{}),
("leitor","名词","读者","Os leitores enviaram cartas.","读者们寄来了信。",{}),
("público","名词","公众 / 观众","O público aplaudiu muito.","观众热烈鼓掌。",{}),
("transmissão","名词","播出 / 传输","A transmissão ao vivo começou.","直播开始了。",{}),
("episódio","名词","（剧）集 / 事件","O último episódio foi ótimo.","最后一集很棒。",{}),
("série","名词","连续剧 / 系列","Estou vendo uma série nova.","我在看一部新剧。",{}),
("novela","名词","（电视）肥皂剧","A novela das oito é muito popular.","八点档肥皂剧很受欢迎。",{"falseFriend":"西语 novela = 长篇小说；葡语 novela 常指电视肥皂剧，「长篇小说」葡语是 romance"}),
("documentário","名词","纪录片","O documentário mostra a Amazônia.","这部纪录片展示亚马逊。",{}),
("editorial","名词","社论","O editorial criticou o governo.","社论批评了政府。",{}),
("análise","名词","分析","A análise dos dados levou dias.","数据分析花了好几天。",{}),
("resumo","名词","摘要 / 梗概","Escreva um resumo do artigo.","写一份这篇文章的摘要。",{}),
("título","名词","标题 / 头衔","O título chamou atenção.","标题很吸引眼球。",{}),
("capa","名词","封面","A capa da revista ficou linda.","杂志封面很漂亮。",{}),
("edição","名词","版本 / 期号","A edição de hoje traz uma entrevista.","今天这一期有一篇采访。",{}),
("publicação","名词","发表 / 出版物","A publicação do livro foi adiada.","这本书的出版被推迟了。",{}),
("versão","名词","版本","Prefiro a versão original.","我更喜欢原版。",{}),
("fonte","名词","来源 / 喷泉","A fonte não foi revelada.","消息来源未被披露。",{}),
("informação","名词","信息 / 消息","Essa informação é confidencial.","这条信息是机密的。",{}),
("dados","名词","数据（dado 的复数）","Os dados mostram uma queda.","数据显示下降。",{}),
("boato","名词","谣言","É só um boato, não acredite.","那只是谣言，别信。",{}),
("polêmica","名词","争议","A declaração causou polêmica.","这番言论引发了争议。",{}),
("controvérsia","名词","争论 / 争议","O tema gerou controvérsia.","这个话题引起了争论。",{}),
("escândalo","名词","丑闻","O escândalo derrubou o ministro.","丑闻让部长下台了。",{}),
("repercussão","名词","反响 / 影响","A repercussão foi enorme.","反响巨大。",{}),
("destaque","名词","亮点 / 头条位置","O jogo foi o destaque do dia.","这场比赛是当天的焦点。",{}),
("foco","名词","焦点 / 重点","O foco da reportagem é a educação.","报道的重点是教育。",{}),
("questão","名词","问题 / 议题","Essa questão é complicada.","这个问题很复杂。",{}),
("tema","名词","主题","O tema da redação foi meio ambiente.","作文主题是环境。",{}),
("assunto","名词","话题 / 事情","Mudemos de assunto.","我们换个话题吧。",{}),
("conteúdo","名词","内容","O conteúdo do curso é ótimo.","课程内容很棒。",{}),
("expressão","名词","表达 / 短语","Essa expressão é muito usada.","这个表达很常用。",{}),
("termo","名词","术语","Explique esse termo técnico.","解释一下这个专业术语。",{}),
("conceito","名词","概念","O conceito é difícil de definir.","这个概念很难定义。",{}),
("definição","名词","定义","Qual é a definição correta?","正确定义是什么？",{}),
("descrição","名词","描述","A descrição do produto está errada.","产品描述有误。",{}),
("explicação","名词","解释","A explicação foi clara.","解释很清楚。",{}),
("argumento","名词","论点 / 论据","Esse argumento é fraco.","这个论点站不住脚。",{}),
("visão","名词","视野 / 观点","Ela tem uma visão ampla.","她视野开阔。",{}),
("posição","名词","位置 / 立场","Qual é a sua posição?","你的立场是什么？",{}),
("atitude","名词","态度","Gosto da sua atitude.","我喜欢你的态度。",{}),
("comportamento","名词","行为","O comportamento dele mudou.","他的行为变了。",{}),
("rotina","名词","日常 / 惯例","Minha rotina é corrida.","我的日常很紧张。",{}),
("cobertura","名词","报道 / 覆盖","A cobertura da eleição foi ampla.","选举报道很全面。",{}),
("site","名词","网站","O site saiu do ar.","网站宕机了。",{}),
("página","名词","页面","A página não carrega.","页面加载不出来。",{}),
("link","名词","链接","Clique no link abaixo.","点击下面的链接。",{}),
("tela","名词","屏幕","A tela do celular quebrou.","手机屏幕碎了。",{}),
("aplicativo","名词","应用程序（App）","Baixe o aplicativo do banco.","下载银行的 App。",{}),
("postagem","名词","帖子 / 发文","A postagem teve mil curtidas.","这条帖子有一千个赞。",{}),
("seguidor","名词","关注者 / 粉丝","Ele tem muitos seguidores.","他有很多粉丝。",{}),
("perfil","名词","个人主页 / 侧写","Atualizei meu perfil.","我更新了个人主页。",{}),
("compartilhamento","名词","分享 / 转发","O compartilhamento é livre.","可以自由转发。",{}),
("curtida","名词","点赞","A foto teve muitas curtidas.","这张照片有很多赞。",{}),
("algoritmo","名词","算法","O algoritmo mudou de novo.","算法又变了。",{}),
("canal","名词","频道 / 渠道","Um canal de notícias.","一个新闻频道。",{}),
("temporada","名词","（剧）季 / 季节","A segunda temporada estreia em maio.","第二季五月开播。",{}),
("personagem","名词","角色 / 人物","Meu personagem favorito morreu.","我最喜欢的角色死了。",{}),
("enredo","名词","剧情 / 情节","O enredo é cheio de surpresas.","剧情充满反转。",{"falseFriend":"西语 enredo = 纠缠/乱子；葡语 enredo = 剧情/情节"}),
("ator","名词","演员（男）","O ator ganhou um prêmio.","这位男演员获了奖。",{}),
("atriz","名词","演员（女）","A atriz mora no Rio.","这位女演员住在里约。",{}),
("diretor","名词","导演 / 主任","O diretor do filme é brasileiro.","这部电影的导演是巴西人。",{}),
("autor","名词","作者","A autora assinou meu livro.","作者在我的书上签了名。",{}),
("obra","名词","作品 / 工程","Uma obra importante da literatura.","一部重要的文学作品。",{}),
("capítulo","名词","章节","Li três capítulos hoje.","我今天读了三章。",{}),
("gênero","名词","类型 / 性别","Que gênero de filme você gosta?","你喜欢什么类型的电影？",{}),
("estilo","名词","风格","O estilo do autor é único.","这位作者风格独特。",{}),
("tom","名词","语气 / 音调","O tom do texto é irônico.","文章的语气很讽刺。",{}),
("patrocínio","名词","赞助","O evento tem patrocínio de bancos.","活动有银行赞助。",{}),
("anúncio","名词","广告 / 公告","Vi um anúncio no metrô.","我在地铁看到一则广告。",{}),
("propaganda","名词","广告 / 宣传","A propaganda aumentou as vendas.","广告提升了销量。",{}),
("marca","名词","品牌 / 标记","Uma marca famosa de roupas.","一个著名服装品牌。",{}),
("campanha","名词","活动 / 战役","A campanha de vacinação começou.","疫苗接种活动开始了。",{}),
("pauta","名词","议程 / 选题","Esse tema está na pauta do dia.","这个议题在今天的日程上。",{}),
("apuração","名词","采访核实","A apuração levou meses.","采访核实花了几个月。",{}),
("checagem","名词","事实核查","A checagem de fatos é essencial.","事实核查至关重要。",{}),
("credibilidade","名词","可信度","O jornal perdeu credibilidade.","这家报纸失去了公信力。",{}),
("ética","名词","伦理 / 职业道德","A ética jornalística importa.","新闻伦理很重要。",{}),
("sigilo","名词","保密","O caso está sob sigilo.","案件处于保密状态。",{}),
("vazamento","名词","泄露","O vazamento de dados foi grave.","数据泄露很严重。",{}),
("bastidores","名词","幕后（复数常用）","Os bastidores da política.","政治的幕后。",{}),
("gravação","名词","录制 / 录像","A gravação foi feita no estúdio.","录制是在演播室完成的。",{}),
("internet","名词","互联网","A internet caiu de novo.","网络又断了。",{}),
("imagem","名词","图像 / 形象","A imagem ficou borrada.","图像模糊了。",{}),
("estreia","名词","首映 / 首演","A estreia do filme é sexta.","电影周五首映。",{}),
("dispor","动词","支配 / 拥有（pôr 加前缀 dis-）","Dispomos de poucos recursos.","我们可用的资源很少。",{"derivedFrom":"pôr","conj":C("disponho","dispões","dispõe","dispomos","dispõem","disponer: dispongo/dispones/dispone/disponemos/disponen")}),
("repor","动词","补充 / 恢复（pôr 加前缀 re-）","Precisamos repor o estoque.","我们需要补充库存。",{"derivedFrom":"pôr","conj":C("reponho","repões","repõe","repomos","repõem","reponer: repongo/repones/repone/reponemos/reponen")}),
("entreter","动词","娱乐 / 使消遣（ter 加前缀 entre-）","O filme entretém toda a família.","这部电影让全家都开心。",{"derivedFrom":"ter","conj":C("entretenho","entreténs","entretém","entretemos","entretêm","entretener: entretengo/entretienes/entretiene/entretenemos/entretienen")}),
("deter","动词","拘留 / 阻止（ter 加前缀 de-）","A polícia deteve o suspeito.","警方拘留了嫌疑人。",{"derivedFrom":"ter","conj":C("detenho","deténs","detém","detemos","detêm","detener: detengo/detienes/detienen/detenemos/detienen".replace("detienen/detenemos","detiene/detenemos"))}),
("predizer","动词","预言 / 预测（dizer 加前缀 pre-）","Ninguém pode predizer o futuro.","没人能预言未来。",{"derivedFrom":"dizer","conj":C("predigo","predizes","prediz","predizemos","predizem","predecir: predigo/predices/predice/predecimos/predicen")}),
("intervir","动词","干预 / 介入（vir 加前缀 inter-）","O governo interveio na crise.","政府干预了危机。",{"derivedFrom":"vir","conj":C("intervenho","intervéns","intervém","intervimos","intervêm","intervenir: intervengo/intervienes/interviene/intervenimos/intervienen")}),
("distrair","动词","分散注意 / 消遣（trazer 加前缀 dis-）","O celular me distrai o tempo todo.","手机总是让我分心。",{"derivedFrom":"trazer","conj":C("distraio","distrais","distrai","distraímos","distraem","distraer: distraigo/distraes/distrae/distraemos/distraen")}),
("extrair","动词","提取 / 摘录（trazer 加前缀 ex-）","Extraíram informações do relatório.","他们从报告中提取了信息。",{"derivedFrom":"trazer","conj":C("extraio","extrais","extrai","extraímos","extraem","extraer: extraigo/extraes/extrae/extraemos/extraen")}),
("prescrever","动词","开处方 / 规定（escrever 加前缀 pre-）","O médico prescreveu um remédio.","医生开了一种药。",{"derivedFrom":"escrever","conj":C("prescrevo","prescreves","prescreve","prescrevemos","prescrevem","prescribir: prescribo/prescribes/prescribe/prescribimos/prescriben")}),
("avaliar","动词","评估 / 评价","O professor avaliou os alunos.","老师评估了学生。",{"conj":C("avalio","avalias","avalia","avaliamos","avaliam","evaluar: evalúo/evalúas/evalúa/evaluamos/evalúan")}),
("analisar","动词","分析","Vamos analisar os dados.","我们来分析数据。",{"conj":C("analiso","analisas","analisa","analisamos","analisam","analizar: analizo/analizas/analiza/analizamos/analizan")}),
("comentar","动词","评论 / 谈论","Todos comentaram a notícia.","大家都在谈论这条新闻。",{"conj":C("comento","comentas","comenta","comentamos","comentam","comentar: comento/comentas/comenta/comentamos/comentan")}),
]

assert len(ENTRIES) == 100, len(ENTRIES)

v = json.loads(VOCAB.read_text(encoding="utf-8"))
allpt = {e["pt"] for wk, entries in v.items() if wk.startswith("w") for e in entries}
dups = [pt for pt, *_ in ENTRIES if pt in allpt]
assert not dups, f"重复词: {dups}"

w10 = []
for i, (pt, pos, zh, ex_pt, ex_zh, extra) in enumerate(ENTRIES):
    e = {"rank": 901 + i, "pt": pt, "pos": pos, "zh": zh,
         "example": {"pt": ex_pt, "zh": ex_zh}}
    if extra.get("derivedFrom"):
        e["derivedFrom"] = extra["derivedFrom"]
    if extra.get("falseFriend"):
        e["falseFriend"] = extra["falseFriend"]
    if extra.get("conj"):
        e["conjugations"] = extra["conj"]
    w10.append(e)

v["w10"] = w10
v["description"] = v["description"].replace("W9=801-900。", "W9=801-900，W10=901-1000。")
VOCAB.write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

vc = json.loads(CONJ.read_text(encoding="utf-8"))
have = {x["infinitive"] for x in vc["verbs"]}
NOTES = {
 "dispor": ("irregular（pôr 族）", "dispor de + 名词 = 拥有/可用；disponer 同族"),
 "repor": ("irregular（pôr 族）", "repor o estoque 补货；perfeito repôs"),
 "entreter": ("irregular（ter 族）", "entretener 同族：ele entretém（重音）"),
 "deter": ("irregular（ter 族）", "detener 同族：eu detenho；perfeito deteve"),
 "predizer": ("irregular（dizer 族）", "predecir 同族：eu predigo；perfeito predisse"),
 "intervir": ("irregular（vir 族）", "intervenir 同族：eu intervenho；perfeito interveio"),
 "distrair": ("irregular（trazer 族）", "distraer 同族：eu distraio；nós distraímos（重音）"),
 "extrair": ("irregular（trazer 族）", "extraer 同族：eu extraio；perfeito extraiu"),
 "prescrever": ("regular -er（escrever 族）", "⚠️ 西语 prescribir（b）≠ 葡语 prescrever（v）——拼写陷阱"),
 "avaliar": ("regular -ar", "西语 evaluar 带重音（evalúo）；葡语 avalio 无重音"),
 "analisar": ("regular -ar", "analizar 同族：z→s"),
 "comentar": ("regular -ar", "comentar 同形同义"),
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
vc["description"] = vc["description"].replace(f"（{len(vc['verbs'])-added} 个", f"（{len(vc['verbs'])} 个").replace("W1-W9", "W1-W10")
CONJ.write_text(json.dumps(vc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

verbs = sum(1 for e in w10 if e["pos"] == "动词")
der = sum(1 for e in w10 if "derivedFrom" in e)
ff = sum(1 for e in w10 if "falseFriend" in e)
print(f"OK w10: 100 词 rank 901-1000 · 动词 {verbs} · 派生 {der} · 假朋友 {ff} · 变位表新增 {added}（总 {len(vc['verbs'])}）")
