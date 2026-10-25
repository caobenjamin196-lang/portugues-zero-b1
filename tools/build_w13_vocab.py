#!/usr/bin/env python3
"""W13 词汇构建：rank 1201-1300 追加到 frequency-vocab.json，动词变位合并进 verb-conjugations.json"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "frequency-vocab.json"
CONJ = ROOT / "data" / "verb-conjugations.json"

C = lambda eu, tu, ele, nos, eles, es: {"eu": eu, "tu": tu, "ele/ela/você": ele, "nós": nos, "eles/elas/vocês": eles, "es": es}

ENTRIES = [
("time","名词","球队 / 队伍","O time venceu o campeonato.","球队赢得了冠军。",{}),
("campeonato","名词","锦标赛 / 联赛","O campeonato começa em março.","联赛三月开赛。",{}),
("torneio","名词","巡回赛 / 杯赛","O torneio reúne oito seleções.","这项赛事汇集了八支国家队。",{}),
("medalha","名词","奖牌","Ela ganhou a medalha de ouro.","她赢得了金牌。",{}),
("gol","名词","进球","O gol saiu aos quarenta minutos.","进球出现在第 40 分钟。",{}),
("jogador","名词","球员 / 运动员","O jogador assinou contrato novo.","这名球员签了新合同。",{}),
("técnico","名词","主教练 / 技术员","O técnico mudou a formação.","主教练换了阵型。",{"falseFriend":"⚠️ 体育新闻里 técnico = 主教练（西语 entrenador）；「技术员」才是西语 técnico 的原义"}),
("treinador","名词","教练 / 训练师","O treinador elogiou a equipe.","教练表扬了队伍。",{}),
("árbitro","名词","裁判","O árbitro marcou pênalti.","裁判判了点球。",{}),
("torcida","名词","球迷（群体）","A torcida lotou o estádio.","球迷把球场坐满了。",{}),
("estádio","名词","体育场","O estádio recebeu sessenta mil pessoas.","体育场迎来了六万人。",{}),
("campeão","名词","冠军","O Brasil foi campeão cinco vezes.","巴西五次夺冠。",{}),
("empate","名词","平局","O jogo terminou em empate.","比赛以平局结束。",{}),
("classificação","名词","排名 / 晋级 / 分类","A classificação foi comemorada.","晋级引发了庆祝。",{}),
("rodada","名词","轮次 / 回合","A rodada decide o líder.","这一轮决定榜首。",{"falseFriend":"西语 ronda；葡语 rodada 兼指「一轮酒」（rodada de cerveja）"}),
("seleção","名词","国家队 / 选拔","A seleção joga na terça.","国家队周二比赛。",{}),
("convocação","名词","征召名单 / 召集","A convocação saiu hoje.","征召名单今天公布。",{}),
("lesão","名词","伤病 / 损伤","A lesão tirou ele do jogo.","伤病让他缺席比赛。",{}),
("contratação","名词","签约引进 / 雇用","A contratação custou dez milhões.","这笔引援花了一千万。",{}),
("transferência","名词","转会 / 转账","A transferência foi confirmada.","转会已获确认。",{}),
("notebook","名词","笔记本电脑","Comprei um notebook novo.","我买了台新笔记本。",{"falseFriend":"西语说 portátil；葡语直接用 notebook，「笔记本（纸）」是 caderno"}),
("impressora","名词","打印机","A impressora está sem tinta.","打印机没墨了。",{}),
("senha","名词","密码 / 排队号码","Esqueci a senha do banco.","我忘了银行密码。",{"falseFriend":"西语密码 = contraseña；葡语 senha 兼指密码和排队叫号单"}),
("usuário","名词","用户","O número de usuários cresceu.","用户数量增长了。",{}),
("robô","名词","机器人","O robô faz cirurgias.","机器人可以做手术。",{}),
("automação","名词","自动化","A automação mudou a fábrica.","自动化改变了工厂。",{}),
("inovação","名词","创新","A inovação atrai investidores.","创新吸引投资者。",{}),
("cientista","名词","科学家","A cientista publicou o estudo.","这位科学家发表了研究。",{}),
("laboratório","名词","实验室","O laboratório testou as amostras.","实验室检测了样本。",{}),
("experimento","名词","实验","O experimento durou seis meses.","实验持续了六个月。",{}),
("tratamento","名词","治疗 / 处理","O tratamento é gratuito.","治疗是免费的。",{}),
("sintoma","名词","症状","Os sintomas desapareceram.","症状消失了。",{}),
("vírus","名词","病毒","O vírus se espalha no inverno.","病毒在冬季传播。",{}),
("bactéria","名词","细菌","A bactéria resiste a antibióticos.","这种细菌对抗生素有耐药性。",{}),
("epidemia","名词","流行病（局部）","A epidemia atingiu a região.","疫情袭击了该地区。",{}),
("pandemia","名词","大流行病（全球）","A pandemia mudou o mundo.","大流行改变了世界。",{}),
("surto","名词","（疫情）暴发","Um surto foi registrado na cidade.","该市记录了一起暴发。",{}),
("dose","名词","剂量","A segunda dose é essencial.","第二剂必不可少。",{}),
("eficácia","名词","效力 / 有效率","A eficácia da vacina é alta.","疫苗的有效率很高。",{}),
("amostra","名词","样本","As amostras foram analisadas.","样本已被分析。",{}),
("paciente","名词","病人","O paciente recebeu alta.","病人出院了。",{}),
("cirurgia","名词","手术","A cirurgia foi um sucesso.","手术很成功。",{}),
("diagnóstico","名词","诊断","O diagnóstico saiu rápido.","诊断很快出来了。",{}),
("manifestação","名词","示威 / 表现","A manifestação reuniu milhares.","示威聚集了数千人。",{}),
("protesto","名词","抗议","O protesto foi pacífico.","抗议是和平的。",{}),
("marcha","名词","游行 / 行进","A marcha seguiu pela avenida.","游行队伍沿大道行进。",{}),
("mobilização","名词","动员","A mobilização começou na internet.","动员始于网络。",{}),
("petição","名词","请愿书","A petição já tem mil assinaturas.","请愿书已有一千个签名。",{}),
("abaixo-assinado","名词","联名请愿书","O abaixo-assinado foi entregue ao prefeito.","联名请愿书交给了市长。",{}),
("referendo","名词","全民公投","O referendo será em outubro.","公投将在十月举行。",{}),
("plebiscito","名词","全民表决","O plebiscito definiu o futuro.","全民表决决定了未来。",{}),
("mandato","名词","任期","O mandato termina em dezembro.","任期十二月结束。",{}),
("posse","名词","就职 / 占有","A posse do presidente foi histórica.","总统就职典礼具有历史意义。",{"falseFriend":"⚠️ 新闻里 posse 常指「就职」（posse presidencial）；西语 posesión 同义但葡语也用 tomar posse 这个固定搭配"}),
("renúncia","名词","辞职","A renúncia surpreendeu o país.","辞职震惊了全国。",{}),
("impeachment","名词","弹劾","O impeachment foi aprovado.","弹劾案获得通过。",{}),
("operação","名词","（警方）行动 / 手术 / 运营","A operação prendeu dez pessoas.","这次行动逮捕了十人。",{}),
("flagrante","名词","现行抓捕","Ele foi preso em flagrante.","他被当场抓获。",{"falseFriend":"⚠️ 西语 flagrante = 明目张胆的；葡语 em flagrante = 现行犯当场抓获，新闻高频词"}),
("condenação","名词","定罪 / 谴责","A condenação foi anunciada ontem.","判决昨天宣布。",{}),
("absolvição","名词","无罪释放","A absolvição encerrou o caso.","无罪判决了结此案。",{}),
("promotor","名词","检察官","O promotor pediu a condenação.","检察官请求定罪。",{"falseFriend":"⚠️ 葡语 promotor (de justiça) = 检察官；西语 promotor = 推广者/发起人"}),
("delegado","名词","警长 / 代表","O delegado comandou a investigação.","警长指挥了调查。",{"falseFriend":"⚠️ 葡语 delegado = 警长（巴西警察系统）；西语 delegado = 代表/特派员"}),
("perito","名词","鉴定专家","O perito examinou as provas.","鉴定专家检验了证据。",{}),
("ação","名词","行动 / 诉讼 / 股票","A ação judicial começa em maio.","诉讼五月开庭。",{}),
("índice","名词","指数 / 比率","O índice de desemprego caiu.","失业率下降了。",{}),
("cotação","名词","报价 / 汇率","A cotação do dólar subiu.","美元汇率上涨。",{}),
("alta","名词","上涨 / 出院","O dólar teve alta de dois por cento.","美元上涨了 2%。",{}),
("baixa","名词","下跌 / 减员","A baixa nas vendas preocupa.","销量下跌令人担忧。",{}),
("recorde","名词","纪录","As exportações bateram recorde.","出口创了纪录。",{}),
("superávit","名词","顺差 / 盈余","O país registrou superávit.","该国录得顺差。",{}),
("déficit","名词","赤字 / 逆差","O déficit fiscal aumentou.","财政赤字增加了。",{}),
("tarifa","名词","关税 / 资费","A tarifa de energia vai subir.","电价将要上调。",{}),
("acordo","名词","协议 / 一致","O acordo foi assinado hoje.","协议今天签署。",{}),
("importação","名词","进口","A importação de trigo cresceu.","小麦进口增加了。",{}),
("seca","名词","干旱","A seca castiga o nordeste.","干旱肆虐东北部。",{}),
("queimada","名词","烧荒 / 野火","As queimadas aumentaram no cerrado.","塞拉多的烧荒增多了。",{}),
("desmatamento","名词","毁林","O desmatamento caiu dez por cento.","毁林下降了 10%。",{}),
("biodiversidade","名词","生物多样性","A Amazônia tem biodiversidade única.","亚马孙拥有独特的生物多样性。",{}),
("espécie","名词","物种 / 种类","A espécie está ameaçada.","该物种受到威胁。",{}),
("extinção","名词","灭绝","A extinção do animal seria irreversível.","该动物的灭绝将不可逆转。",{}),
("habitat","名词","栖息地","O habitat foi destruído.","栖息地被破坏了。",{}),
("sustentabilidade","名词","可持续性","A sustentabilidade virou prioridade.","可持续性成了优先事项。",{}),
("reciclagem","名词","回收利用","A reciclagem cresce nas cidades.","回收利用在城市中增长。",{}),
("lixo","名词","垃圾","O lixo é recolhido de manhã.","垃圾早上清运。",{}),
("resíduo","名词","废弃物 / 残留","Os resíduos foram tratados.","废弃物已处理。",{}),
("emissão","名词","排放","A emissão de gases caiu.","气体排放下降了。",{}),
("carbono","名词","碳","A meta é reduzir o carbono.","目标是减少碳排放。",{}),
("solar","形容词","太阳能的","A energia solar avança no país.","太阳能在全国推进。",{"falseFriend":"葡语 solar 作名词 = 庄园大宅（历史建筑）；作形容词 = 太阳能的，与西语一致"}),
("eólica","形容词","风力的","A energia eólica bateu recorde.","风电创了纪录。",{}),
("contratar","动词","雇用 / 签约","O clube contratou um novo técnico.","俱乐部签了新教练。",{"conj":C("contrato","contratas","contrata","contratamos","contratam","contratar: contrato/contratas/contrata/contratamos/contratan")}),
("demitir","动词","解雇 / 辞退","A empresa demitiu cem funcionários.","公司解雇了一百名员工。",{"conj":C("demito","demites","demite","demitimos","demitem","despedir: despido/despides/despide/despedimos/despiden")}),
("treinar","动词","训练 / 执教","A equipe treina todos os dias.","队伍每天训练。",{"conj":C("treino","treinas","treina","treinamos","treinam","entrenar: entreno/entrenas/entrena/entrenamos/entrenan")}),
("negociar","动词","谈判 / 协商","Os sindicatos negociam o salário.","工会正在谈工资。",{"conj":C("negocio","negocias","negocia","negociamos","negociam","negociar: negocio/negocias/negocia/negociamos/negocian")}),
("divulgar","动词","公布 / 发布","O IBGE divulgou os dados.","地理统计局公布了数据。",{"conj":C("divulgo","divulgas","divulga","divulgamos","divulgam","divulgar: divulgo/divulgas/divulga/divulgamos/divulgan")}),
("revelar","动词","揭示 / 透露","O relatório revelou falhas graves.","报告揭示了严重缺陷。",{"conj":C("revelo","revelas","revela","revelamos","revelam","revelar: revelo/revelas/revela/revelamos/revelan")}),
("alertar","动词","警告 / 提醒","Os médicos alertaram para o risco.","医生们警告了风险。",{"conj":C("alerto","alertas","alerta","alertamos","alertam","alertar: alerto/alertas/alerta/alertamos/alertan")}),
("restringir","动词","限制","A lei restringe o acesso.","该法律限制访问。",{"conj":C("restrinjo","restringes","restringe","restringimos","restringem","restringir: restrinjo/restringes/restringe/restringimos/restringen")}),
("corrigir","动词","纠正 / 批改","O governo corrigiu o valor.","政府修正了数值。",{"conj":C("corrijo","corriges","corrige","corrigimos","corrigem","corregir: corrijo/corriges/corrige/corregimos/corrigen")}),
("registrar","动词","记录 / 登记","A cidade registrou recorde de calor.","该市录得高温纪录。",{"conj":C("registro","registras","registra","registramos","registram","registrar: registro/registras/registra/registramos/registran")}),
("empatar","动词","踢平 / 打平","O time empatou no último minuto.","球队在最后一分钟扳平。",{"conj":C("empato","empatas","empata","empatamos","empatam","empatar: empato/empatas/empata/empatamos/empatan")}),
("vencer","动词","战胜 / 获胜 / 到期","O Brasil venceu por dois a zero.","巴西 2 比 0 获胜。",{"conj":C("venço","vences","vence","vencemos","vencem","vencer: venzo/vences/vence/vencemos/vencen")}),
]

assert len(ENTRIES) == 100, len(ENTRIES)

v = json.loads(VOCAB.read_text(encoding="utf-8"))
allpt = {e["pt"] for wk, entries in v.items() if wk.startswith("w") for e in entries}
dups = [pt for pt, *_ in ENTRIES if pt in allpt]
assert not dups, f"重复词: {dups}"

w13 = []
for i, (pt, pos, zh, ex_pt, ex_zh, extra) in enumerate(ENTRIES):
    e = {"rank": 1201 + i, "pt": pt, "pos": pos, "zh": zh,
         "example": {"pt": ex_pt, "zh": ex_zh}}
    if extra.get("derivedFrom"):
        e["derivedFrom"] = extra["derivedFrom"]
    if extra.get("falseFriend"):
        e["falseFriend"] = extra["falseFriend"]
    if extra.get("conj"):
        e["conjugations"] = extra["conj"]
    w13.append(e)

v["w13"] = w13
v["description"] = v["description"].replace("W12=1101-1200。", "W12=1101-1200，W13=1201-1300。")
VOCAB.write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

vc = json.loads(CONJ.read_text(encoding="utf-8"))
have = {x["infinitive"] for x in vc["verbs"]}
NOTES = {
 "contratar": ("regular -ar", "新闻高频：contratar um técnico = 签教练；名词 contratação"),
 "demitir": ("regular -ir", "demitir alguém = 解雇某人；demissão = 解雇（名词）"),
 "treinar": ("regular -ar", "treinar (alguém/para) = 训练；treinador = 教练"),
 "negociar": ("regular -ar", "negociar com = 与…谈判；negociação = 谈判"),
 "divulgar": ("regular -ar（g→gu 仅未来虚拟式）", "divulgar dados/resultados = 公布数据；新闻高频"),
 "revelar": ("regular -ar", "revelar que… = 透露…；revelação = 揭示/新星"),
 "alertar": ("regular -ar", "alertar para/sobre = 警告…；alerta = 警报"),
 "restringir": ("irregular（g→j）", "eu restrinjo；restringir o acesso = 限制访问"),
 "corrigir": ("irregular（g→j）", "eu corrijo；correção = 修正/批改"),
 "registrar": ("regular -ar", "registrar recorde/ocorrência = 录得纪录/立案；registro = 记录"),
 "empatar": ("regular -ar", "empatar com = 与…战平；empate = 平局"),
 "vencer": ("regular -er（c→ç：eu venço）", "vencer por X a Y = X 比 Y 获胜；vencido = 输家/已到期"),
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
vc["description"] = vc["description"].replace(f"（{len(vc['verbs'])-added} 个", f"（{len(vc['verbs'])} 个").replace("W1-W12", "W1-W13")
CONJ.write_text(json.dumps(vc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

verbs = sum(1 for e in w13 if e["pos"] == "动词")
der = sum(1 for e in w13 if "derivedFrom" in e)
ff = sum(1 for e in w13 if "falseFriend" in e)
print(f"OK w13: 100 词 rank 1201-1300 · 动词 {verbs} · 派生 {der} · 假朋友 {ff} · 变位表新增 {added}（总 {len(vc['verbs'])}）")
