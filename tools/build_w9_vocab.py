#!/usr/bin/env python3
"""W9 词汇构建：rank 801-900 追加到 frequency-vocab.json，动词变位合并进 verb-conjugations.json"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "frequency-vocab.json"
CONJ = ROOT / "data" / "verb-conjugations.json"

# (pt, pos, zh, ex_pt, ex_zh, extra)
# extra: falseFriend / derivedFrom / conj
C = lambda eu, tu, ele, nos, eles, es: {"eu": eu, "tu": tu, "ele/ela/você": ele, "nós": nos, "eles/elas/vocês": eles, "es": es}

ENTRIES = [
("processo","名词","过程 / 诉讼","O processo judicial durou cinco anos.","这场诉讼持续了五年。",{}),
("advogado","名词","律师","O advogado apresentou novas provas.","律师提交了新证据。",{}),
("testemunha","名词","证人","A testemunha confirmou o depoimento.","证人确认了证词。",{}),
("réu","名词","被告","O réu negou todas as acusações.","被告否认了所有指控。",{}),
("acusação","名词","指控 / 控告","A acusação divulgou documentos novos.","控方公布了新文件。",{}),
("defesa","名词","辩护 / 防守","A defesa pediu mais prazo.","辩方要求延长期限。",{}),
("sentença","名词","判决","A sentença será lida amanhã.","判决将于明天宣读。",{}),
("julgar","动词","审判 / 评判","O juiz julga o caso amanhã.","法官明天审理此案。",{"conj":C("julgo","julgas","julga","julgamos","julgam","juzgar: juzgo/juzgas/juzga/juzgamos/juzgan")}),
("julgamento","名词","审判 / 审理","O julgamento começa na próxima semana.","审判下周开始。",{}),
("prova","名词","证据 / 考试","As provas foram analisadas pelo juiz.","证据已由法官分析。",{}),
("evidência","名词","证据 / 迹象","Não há evidências suficientes.","证据不足。",{}),
("depoimento","名词","证词 / 供述","O depoimento durou duas horas.","供述持续了两个小时。",{}),
("denúncia","名词","举报 / 控告","A denúncia foi registrada na delegacia.","举报已在警局登记。",{}),
("acusar","动词","指控","Acusaram-no de fraude.","他们指控他欺诈。",{"conj":C("acuso","acusas","acusa","acusamos","acusam","acusar: acuso/acusas/acusa/acusamos/acusan")}),
("suspeito","名词","嫌疑人；也可作形容词「可疑的」","O suspeito foi interrogado ontem.","嫌疑人昨天接受了讯问。",{}),
("vítima","名词","受害者","A vítima prestou depoimento hoje.","受害者今天做了笔录。",{}),
("culpado","形容词","有罪的","O réu foi considerado culpado.","被告被判有罪。",{}),
("inocente","形容词","无辜的","Todos são inocentes até prova em contrário.","在反证之前，人人无罪。",{}),
("culpa","名词","过错 / 内疚","A culpa não foi provada.","过错未被证实。",{}),
("pena","名词","刑罚；é uma pena = 真遗憾","A pena máxima é de dez anos.","最高刑罚为十年。",{}),
("multa","名词","罚款","Ele pagou uma multa de trânsito.","他交了一笔交通罚款。",{}),
("condenar","动词","判刑 / 谴责","Ele foi condenado a cinco anos.","他被判了五年徒刑。",{"conj":C("condeno","condenas","condena","condenamos","condenam","condenar: condeno/condenas/condena/condenamos/condenan")}),
("delegacia","名词","警察局（分局）","O caso foi registrado na delegacia.","案件已在警局备案。",{}),
("audiência","名词","听证（会）/ 受众","A audiência foi marcada para março.","听证会定在三月。",{}),
("código","名词","法典 / 代码","O Código Civil foi atualizado.","民法典已更新。",{}),
("artigo","名词","条款 / 文章","O artigo quinto garante esse direito.","第五条保障这项权利。",{}),
("cláusula","名词","（合同）条款","A cláusula proíbe a revenda.","该条款禁止转售。",{}),
("documento","名词","文件 / 证件","Envie os documentos por e-mail.","请把文件发到邮箱。",{}),
("defender","动词","辩护 / 捍卫","Ela defende os direitos do povo.","她捍卫人民的权利。",{"conj":C("defendo","defendes","defende","defendemos","defendem","defender: defiendo/defiendes/defiende/defendemos/defienden")}),
("formulário","名词","表格","Preencha o formulário online.","请在线填写表格。",{}),
("assinatura","名词","签名 / 订阅","Falta a assinatura do gerente.","还缺经理的签名。",{}),
("assinar","动词","签署","Assine o contrato aqui, por favor.","请在这里签署合同。",{"falseFriend":"西语「签署」是 firmar；西语 asignar = 分配，别混","conj":C("assino","assinas","assina","assinamos","assinam","firmar: firmo/firmas/firma/firmamos/firman")}),
("registro","名词","登记 / 记录","O registro foi feito no cartório.","登记已在公证处完成。",{}),
("cartório","名词","公证处","Leve o contrato ao cartório.","把合同拿到公证处。",{}),
("licença","名词","许可 / 执照","A licença vence no fim do ano.","执照年底到期。",{}),
("autorização","名词","授权 / 许可","É preciso autorização por escrito.","需要书面授权。",{}),
("permissão","名词","允许","Pedimos permissão para entrar.","我们请求允许进入。",{}),
("proibição","名词","禁止","A proibição entrou em vigor.","禁令已生效。",{}),
("obrigação","名词","义务","Votar é uma obrigação no Brasil.","在巴西，投票是义务。",{}),
("cumprir","动词","履行 / 遵守","Todos devem cumprir a lei.","人人都要遵守法律。",{"conj":C("cumpro","cumpres","cumpre","cumprimos","cumprem","cumplir: cumplo/cumples/cumple/cumplimos/cumplen")}),
("responsabilidade","名词","责任","A empresa assumiu a responsabilidade.","公司承担了责任。",{}),
("prazo","名词","期限","O prazo termina na sexta-feira.","期限周五截止。",{}),
("vigor","名词","生效（entrar em vigor 生效）","A nova lei entra em vigor em janeiro.","新法一月生效。",{}),
("ministério","名词","（政府的）部","O Ministério da Saúde divulgou dados.","卫生部公布了数据。",{}),
("secretaria","名词","秘书处 / （州）厅","A Secretaria de Educação mudou as regras.","教育厅修改了规定。",{}),
("departamento","名词","部门","O departamento jurídico revisou o texto.","法务部门审核了文本。",{}),
("órgão","名词","机关 / 器官","O órgão público respondeu ao pedido.","该公共机关回复了申请。",{}),
("instituição","名词","机构","É uma instituição respeitada.","这是一家受尊敬的机构。",{}),
("administração","名词","管理 / 行政","A administração pública mudou muito.","公共行政变化很大。",{}),
("gestão","名词","管理 / 治理","A nova gestão cortou gastos.","新管理层削减了开支。",{}),
("autoridade","名词","当局 / 权威","As autoridades locais investigam o caso.","地方当局正在调查此案。",{}),
("servidor","名词","公务员 / 服务器","O servidor público assinou o documento.","这位公务员签署了文件。",{}),
("cargo","名词","职位 / 职务","Ele ocupa um cargo de confiança.","他担任一个要职。",{}),
("orçamento","名词","预算","O orçamento foi aprovado.","预算已获批准。",{}),
("verba","名词","拨款 / 经费","A verba do projeto foi cortada.","项目拨款被削减了。",{}),
("recurso","名词","资源 / 上诉","A defesa entrou com um recurso.","辩方提起了上诉。",{}),
("impor","动词","强加 / 征收（pôr 加前缀 im-）","O governo impôs novas taxas.","政府征收了新税。",{"derivedFrom":"pôr","conj":C("imponho","impões","impõe","impomos","impõem","imponer: impongo/impones/impone/imponemos/imponen")}),
("opor-se","动词","反对（pôr 加前缀 op-）","Eles se opuseram à nova lei.","他们反对这项新法。",{"derivedFrom":"pôr","conj":C("me oponho","te opões","se opõe","nos opomos","se opõem","oponerse: me opongo/te opones/se opone/nos oponemos/se oponen")}),
("expor","动词","阐述 / 展出（pôr 加前缀 ex-）","O relatório expõe os riscos.","报告阐述了风险。",{"derivedFrom":"pôr","conj":C("exponho","expões","expõe","expomos","expõem","exponer: expongo/expones/expone/exponemos/exponen")}),
("obter","动词","获得（ter 加前缀 ob-）","Ela obteve a licença ontem.","她昨天拿到了许可。",{"derivedFrom":"ter","conj":C("obtenho","obténs","obtém","obtemos","obtêm","obtener: obtengo/obtienes/obtiene/obtenemos/obtienen")}),
("reter","动词","保留 / 扣留（ter 加前缀 re-）","A empresa reteve os documentos.","公司扣留了文件。",{"derivedFrom":"ter","conj":C("retenho","reténs","retém","retemos","retêm","retener: retengo/retienes/retiene/retenemos/retienen")}),
("satisfazer","动词","使满意（fazer 加前缀 satis-）","O resultado satisfaz a todos.","结果令所有人满意。",{"derivedFrom":"fazer","conj":C("satisfaço","satisfazes","satisfaz","satisfazemos","satisfazem","satisfacer: satisfago/satisfaces/satisface/satisfacemos/satisfacen")}),
("fenômeno","名词","现象","É um fenômeno raro.","这是一种罕见的现象。",{}),
("aspecto","名词","方面 / 外观","Esse aspecto é muito importante.","这一方面非常重要。",{}),
("fator","名词","因素","O preço é um fator decisivo.","价格是决定性因素。",{}),
("elemento","名词","元素 / 要素","É um elemento essencial do contrato.","这是合同的基本要素。",{}),
("estrutura","名词","结构","A estrutura do texto é clara.","文本结构清晰。",{}),
("função","名词","功能 / 职务","Qual é a função desse botão?","这个按钮的功能是什么？",{}),
("papel","名词","纸 / 角色","O papel da escola mudou.","学校的角色变了。",{}),
("nível","名词","水平 / 级别","O nível do mar subiu.","海平面上升了。",{}),
("critério","名词","标准","Os critérios de avaliação mudaram.","评审标准变了。",{}),
("método","名词","方法","É um método muito eficiente.","这是个很高效的方法。",{}),
("estratégia","名词","战略 / 策略","A estratégia da empresa funcionou.","公司的战略奏效了。",{}),
("objetivo","名词","目标；也可作形容词「客观的」","Nosso objetivo principal é crescer.","我们的主要目标是增长。",{}),
("meta","名词","目标 / 指标","Batemos a meta de vendas.","我们完成了销售指标。",{}),
("finalidade","名词","目的","A finalidade da lei é proteger.","该法的目的是保护。",{}),
("consequência","名词","后果","As consequências da crise apareceram.","危机的后果显现了。",{}),
("causa","名词","原因 / 事业","A causa do acidente é desconhecida.","事故原因不明。",{}),
("efeito","名词","效果 / 影响","O efeito do remédio foi rápido.","药效来得很快。",{}),
("risco","名词","风险","Não corra riscos desnecessários.","不要冒不必要的风险。",{}),
("desafio","名词","挑战","É um grande desafio para todos.","这对所有人都是巨大的挑战。",{}),
("oportunidade","名词","机会","É uma oportunidade única.","这是独一无二的机会。",{}),
("tendência","名词","趋势","É uma tendência mundial.","这是一个全球趋势。",{}),
("impacto","名词","影响 / 冲击","O impacto da lei foi grande.","该法的影响很大。",{}),
("desenvolvimento","名词","发展","O desenvolvimento econômico acelerou.","经济发展加快了。",{}),
("meio ambiente","名词","环境","Proteger o meio ambiente é urgente.","保护环境刻不容缓。",{}),
("poluição","名词","污染","A poluição do ar piorou.","空气污染恶化了。",{}),
("energia","名词","能源 / 精力","Energia solar é o futuro.","太阳能是未来。",{}),
("consumidor","名词","消费者","A lei protege o consumidor.","法律保护消费者。",{}),
("produção","名词","生产","A produção aumentou este ano.","今年产量增加了。",{}),
("comércio","名词","商业 / 贸易","O comércio local cresceu.","本地商业增长了。",{}),
("exportação","名词","出口","As exportações cresceram muito.","出口大幅增长。",{}),
("renda","名词","收入","A renda familiar aumentou.","家庭收入增加了。",{}),
("pobreza","名词","贫困","Combater a pobreza é urgente.","消除贫困刻不容缓。",{}),
("desigualdade","名词","不平等","A desigualdade social diminuiu.","社会不平等缩小了。",{}),
("sensível","形容词","敏感的 / 易感的","Ele é muito sensível a críticas.","他对批评很敏感。",{"falseFriend":"西语 sensible = 明智的；葡语 sensível = 敏感的，「明智的」葡语是 sensato"}),
("raro","形容词","稀有的 / 罕见的","É um caso raro na medicina.","这是医学上的罕见病例。",{"falseFriend":"西语 raro 常表「奇怪的」；葡语 raro = 稀有的，「奇怪」用 estranho"}),
("concurso","名词","竞赛 / 公开招考","Ele passou no concurso público.","他通过了公务员招考。",{}),
("edital","名词","公告 / 招考简章","O edital foi publicado hoje.","公告今天发布了。",{}),
("ata","名词","会议纪要","A ata da reunião foi assinada.","会议纪要已签署。",{}),
]

assert len(ENTRIES) == 100, len(ENTRIES)

v = json.loads(VOCAB.read_text(encoding="utf-8"))
allpt = {e["pt"] for wk, entries in v.items() if wk.startswith("w") for e in entries}
dups = [pt for pt, *_ in ENTRIES if pt in allpt]
assert not dups, f"重复词: {dups}"

w9 = []
for i, (pt, pos, zh, ex_pt, ex_zh, extra) in enumerate(ENTRIES):
    e = {"rank": 801 + i, "pt": pt, "pos": pos, "zh": zh,
         "example": {"pt": ex_pt, "zh": ex_zh}}
    if extra.get("derivedFrom"):
        e["derivedFrom"] = extra["derivedFrom"]
    if extra.get("falseFriend"):
        e["falseFriend"] = extra["falseFriend"]
    if extra.get("conj"):
        e["conjugations"] = extra["conj"]
    w9.append(e)

v["w9"] = w9
v["description"] = v["description"].replace("W8=701-800。", "W8=701-800，W9=801-900。")
VOCAB.write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

# 合并动词变位表
vc = json.loads(CONJ.read_text(encoding="utf-8"))
have = {x["infinitive"] for x in vc["verbs"]}
NOTES = {
 "impor": ("irregular（pôr 族）", "imponer 同族：eu imponho；perfeito impus/impôs"),
 "opor-se": ("irregular（pôr 族，反身）", "反身代词前置（口语）或后置：me oponho / oponho-me"),
 "expor": ("irregular（pôr 族）", "exponer 同族：eu exponho"),
 "obter": ("irregular（ter 族）", "obtener 同族：eu obtenho；ele obtém（重音）"),
 "reter": ("irregular（ter 族）", "retener 同族：eu retenho；eles retêm"),
 "satisfazer": ("irregular（fazer 族）", "satisfacer 同族：eu satisfaço"),
 "cumprir": ("regular -ir", "与西语 cumplir 规则对应：cumpro≈cumplo"),
 "julgar": ("regular -ar", "西语 juzgar：z→j 对应"),
 "condenar": ("regular -ar", "condenar alguém a + 刑期：condenado a cinco anos"),
 "defender": ("regular -er", "西语 defender 词干变位（defiendo）；葡语无变位：eu defendo"),
 "acusar": ("regular -ar", "acusar alguém de algo：指控某人某事"),
 "assinar": ("regular -ar", "西语「签署」用 firmar；asignar=分配"),
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
vc["description"] = vc["description"].replace("（213 个", f"（{len(vc['verbs'])} 个").replace("W1-W8", "W1-W9")
CONJ.write_text(json.dumps(vc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

verbs = sum(1 for e in w9 if e["pos"] == "动词")
der = sum(1 for e in w9 if "derivedFrom" in e)
ff = sum(1 for e in w9 if "falseFriend" in e)
print(f"OK w9: 100 词 rank 801-900 · 动词 {verbs} · 派生 {der} · 假朋友 {ff} · 变位表新增 {added}（总 {len(vc['verbs'])}）")
