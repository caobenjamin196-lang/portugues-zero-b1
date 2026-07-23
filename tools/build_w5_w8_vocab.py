#!/usr/bin/env python3
# build_w5_w8_vocab.py — 一次性脚本：为 W5-W8 生成每周 100 个频率词汇并合并进现有数据
# 读取现有 data/*.json，只追加/合并，绝不改动 w1-w4 已有条目。
# 变位机器复制自 tools/build_weekly_vocab.py，并修正两点：
#   1) -car 动词 eu 形式保持 -co（c 发 /k/，如 trocar→troco）；c→ç 只适用于 -cer/-cir（nascer→nasço）
#   2) 补充 W5-W8 新增不规则动词（葡/西）
import json, os, copy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# ============ 动词变位机器（复制自 build_weekly_vocab.py）============
# conj 顺序: [eu, tu, ele/ela/você, nós, eles/elas/vocês]
PT_IRREG = {
    "ser": ["sou", "és", "é", "somos", "são"],
    "estar": ["estou", "estás", "está", "estamos", "estão"],
    "ter": ["tenho", "tens", "tem", "temos", "têm"],
    "haver": ["hei", "hás", "há", "havemos", "hão"],
    "ir": ["vou", "vais", "vai", "vamos", "vão"],
    "fazer": ["faço", "fazes", "faz", "fazemos", "fazem"],
    "poder": ["posso", "podes", "pode", "podemos", "podem"],
    "querer": ["quero", "queres", "quer", "queremos", "querem"],
    "dar": ["dou", "dás", "dá", "damos", "dão"],
    "ver": ["vejo", "vês", "vê", "vemos", "veem"],
    "dizer": ["digo", "dizes", "diz", "dizemos", "dizem"],
    "saber": ["sei", "sabes", "sabe", "sabemos", "sabem"],
    "vir": ["venho", "vens", "vem", "vimos", "vêm"],
    "sair": ["saio", "sais", "sai", "saímos", "saem"],
    "ouvir": ["ouço", "ouves", "ouve", "ouvimos", "ouvem"],
    "sentir": ["sinto", "sentes", "sente", "sentimos", "sentem"],
    "dormir": ["durmo", "dormes", "dorme", "dormimos", "dormem"],
    "pedir": ["peço", "pedes", "pede", "pedimos", "pedem"],
    "seguir": ["sigo", "segues", "segue", "seguimos", "seguem"],
    "conseguir": ["consigo", "consegues", "consegue", "conseguimos", "conseguem"],
    "preferir": ["prefiro", "preferes", "prefere", "preferimos", "preferem"],
    "servir": ["sirvo", "serves", "serve", "servimos", "servem"],
    "dirigir": ["dirijo", "diriges", "dirige", "dirigimos", "dirigem"],
    "trazer": ["trago", "trazes", "traz", "trazemos", "trazem"],
    "ler": ["leio", "lês", "lê", "lemos", "leem"],
    # ---- W5-W8 新增 ----
    "pôr": ["ponho", "pões", "põe", "pomos", "põem"],
    "rir": ["rio", "ris", "ri", "rimos", "riem"],
    "cair": ["caio", "cais", "cai", "caímos", "caem"],
    "prever": ["prevejo", "prevês", "prevê", "prevemos", "preveem"],
    "supor": ["suponho", "supões", "supõe", "supomos", "supõem"],
    "sugerir": ["sugiro", "sugeres", "sugere", "sugerimos", "sugerem"],
    "mentir": ["minto", "mentes", "mente", "mentimos", "mentem"],
    "diminuir": ["diminuo", "diminuis", "diminui", "diminuímos", "diminuem"],
    "proibir": ["proíbo", "proíbes", "proíbe", "proibimos", "proíbem"],
}

def conj_pt(inf):
    """规则动词现在时变位（-cer/-cir→-ço、-ger/-gir→-jo；-car 动词 eu 保持 -co）"""
    if inf in PT_IRREG:
        return PT_IRREG[inf]
    stem, end = inf[:-2], inf[-2:]
    if end == "ar":
        endings = ["o", "as", "a", "amos", "am"]
    elif end == "er":
        endings = ["o", "es", "e", "emos", "em"]
    else:
        endings = ["o", "es", "e", "imos", "em"]
    forms = [stem + e for e in endings]
    eu = forms[0]
    if stem.endswith("c") and end in ("er", "ir"):  # nascer→nasço, agradecer→agradeço
        eu = stem[:-1] + "ço"
    elif stem.endswith("g") and end in ("er", "ir"):  # exigir→exijo, proteger→protejo, eleger→elejo
        eu = stem[:-1] + "jo"
    forms[0] = eu
    return forms

ES_IRREG = {
    "ser": ["soy", "eres", "es", "somos", "son"],
    "estar": ["estoy", "estás", "está", "estamos", "están"],
    "tener": ["tengo", "tienes", "tiene", "tenemos", "tienen"],
    "haber": ["he", "has", "ha", "hemos", "han"],
    "ir": ["voy", "vas", "va", "vamos", "van"],
    "hacer": ["hago", "haces", "hace", "hacemos", "hacen"],
    "poder": ["puedo", "puedes", "puede", "podemos", "pueden"],
    "querer": ["quiero", "quieres", "quiere", "queremos", "quieren"],
    "dar": ["doy", "das", "da", "damos", "dan"],
    "ver": ["veo", "ves", "ve", "vemos", "ven"],
    "decir": ["digo", "dices", "dice", "decimos", "dicen"],
    "saber": ["sé", "sabes", "sabe", "sabemos", "saben"],
    "venir": ["vengo", "vienes", "viene", "venimos", "vienen"],
    "salir": ["salgo", "sales", "sale", "salimos", "salen"],
    "oír": ["oigo", "oyes", "oye", "oímos", "oyen"],
    "traer": ["traigo", "traes", "trae", "traemos", "traen"],
    "conducir": ["conduzco", "conduces", "conduce", "conducimos", "conducen"],
    "conocer": ["conozco", "conoces", "conoce", "conocemos", "conocen"],
    "ofrecer": ["ofrezco", "ofreces", "ofrece", "ofrecemos", "ofrecen"],
    "valer": ["valgo", "vales", "vale", "valemos", "valen"],
    "encontrar": ["encuentro", "encuentras", "encuentra", "encontramos", "encuentran"],
    "volver": ["vuelvo", "vuelves", "vuelve", "volvemos", "vuelven"],
    "empezar": ["empiezo", "empiezas", "empieza", "empezamos", "empiezan"],
    "cerrar": ["cierro", "cierras", "cierra", "cerramos", "cierran"],
    "entender": ["entiendo", "entiendes", "entiende", "entendemos", "entienden"],
    "pensar": ["pienso", "piensas", "piensa", "pensamos", "piensan"],
    "recordar": ["recuerdo", "recuerdas", "recuerda", "recordamos", "recuerdan"],
    "perder": ["pierdo", "pierdes", "pierde", "perdemos", "pierden"],
    "jugar": ["juego", "juegas", "juega", "jugamos", "juegan"],
    "sentar": ["siento", "sientas", "sienta", "sentamos", "sientan"],
    "despertar": ["despierto", "despiertas", "despierta", "despertamos", "despiertan"],
    "mostrar": ["muestro", "muestras", "muestra", "mostramos", "muestran"],
    "llover": ["llueve", "llueve", "llueve", "llovemos", "llueven"],
    "costar": ["cuesto", "cuestas", "cuesta", "costamos", "cuestan"],
    "sentir": ["siento", "sientes", "siente", "sentimos", "sienten"],
    "dormir": ["duermo", "duermes", "duerme", "dormimos", "duermen"],
    "pedir": ["pido", "pides", "pide", "pedimos", "piden"],
    "seguir": ["sigo", "sigues", "sigue", "seguimos", "siguen"],
    "conseguir": ["consigo", "consigues", "consigue", "conseguimos", "consiguen"],
    "elegir": ["elijo", "eliges", "elige", "elegimos", "eligen"],
    "preferir": ["prefiero", "prefieres", "prefiere", "preferimos", "prefieren"],
    "servir": ["sirvo", "sirves", "sirve", "servimos", "sirven"],
    "leer": ["leo", "lees", "lee", "leemos", "leen"],
    # ---- W5-W8 新增（西语不规则现在时）----
    "poner": ["pongo", "pones", "pone", "ponemos", "ponen"],
    "nacer": ["nazco", "naces", "nace", "nacemos", "nacen"],
    "morir": ["muero", "mueres", "muere", "morimos", "mueren"],
    "crecer": ["crezco", "creces", "crece", "crecemos", "crecen"],
    "contar": ["cuento", "cuentas", "cuenta", "contamos", "cuentan"],
    "soñar": ["sueño", "sueñas", "sueña", "soñamos", "sueñan"],
    "reír": ["río", "ríes", "ríe", "reímos", "ríen"],
    "gobernar": ["gobierno", "gobiernas", "gobierna", "gobernamos", "gobiernan"],
    "disminuir": ["disminuyo", "disminuyes", "disminuye", "disminuimos", "disminuyen"],
    "caer": ["caigo", "caes", "cae", "caemos", "caen"],
    "atender": ["atiendo", "atiendes", "atiende", "atendemos", "atienden"],
    "volar": ["vuelo", "vuelas", "vuela", "volamos", "vuelan"],
    "prever": ["preveo", "prevés", "prevé", "prevemos", "prevén"],
    "suponer": ["supongo", "supones", "supone", "suponemos", "suponen"],
    "sugerir": ["sugiero", "sugieres", "sugiere", "sugerimos", "sugieren"],
    "confiar": ["confío", "confías", "confía", "confiamos", "confían"],
    "prohibir": ["prohíbo", "prohíbes", "prohíbe", "prohibimos", "prohíben"],
    "agradecer": ["agradezco", "agradeces", "agradece", "agradecemos", "agradecen"],
    "mentir": ["miento", "mientes", "miente", "mentimos", "mienten"],
    "concordar": ["concuerdo", "concuerdas", "concuerda", "concordamos", "concuerdan"],
    "reconocer": ["reconozco", "reconoces", "reconoce", "reconocemos", "reconocen"],
}

def es_line(es_inf):
    if es_inf in ES_IRREG:
        forms = ES_IRREG[es_inf]
    else:
        stem, end = es_inf[:-2], es_inf[-2:]
        if end == "ar":
            endings = ["o", "as", "a", "amos", "an"]
        elif end == "er":
            endings = ["o", "es", "e", "emos", "en"]
        else:
            endings = ["o", "es", "e", "imos", "en"]
        forms = [stem + e for e in endings]
    return f"{es_inf}: {'/'.join(forms)}"

# ============ W5-W8 动词注册表 ============
# infinitive -> (meaning, type, es_infinitive, note)；es_infinitive 为 None 时用 note 首段自定义西语对照
VERBS = {
    # ---- W5：叙事高频动词 ----
    "assistir": ("观看/出席", "regular -ar", "asistir", "assistir a + 观看对象：assisto ao jogo；巴西口语 assistir TV 常省略 a"),
    "contar": ("讲述/数", "regular -ar", "contar", "西语 cuento 双元音化，葡语 conto 没有；contar uma história 讲故事"),
    "terminar": ("结束", "regular -ar", "terminar", None),
    "visitar": ("拜访/参观", "regular -ar", "visitar", None),
    "pôr": ("放/摆", "irregular", "poner", "eu ponho 不规则；põe/pões/põem 带尖音符；pôr a mesa 摆桌子"),
    "faltar": ("缺少/没到", "regular -ar", "faltar", "Falta sal 没盐了；faltar à aula 缺课"),
    "nascer": ("出生", "regular -er", "nacer", "eu nasço（c→ç）；西语 nazco 也不规则"),
    "morrer": ("死/去世", "regular -er", "morir", "西语 muero 双元音化，葡语 morro 没有"),
    "crescer": ("长大/成长", "regular -er", "crecer", "eu cresço（c→ç）"),
    "casar": ("结婚", "regular -ar", "casar", "casar(-se) com：Ela casou com um brasileiro"),
    "namorar": ("谈恋爱", "regular -ar", None, "西语 enamorarse: me enamoro/te enamoras/se enamora/nos enamoramos/se enamoran——葡语 namorar=和某人谈恋爱（稳定交往）"),
    "divorciar": ("离婚", "regular -ar", "divorciar", "divorciar-se：Eles se divorciaram"),
    "convidar": ("邀请", "regular -ar", "invitar", "convidar para：convidei ele para o jantar"),
    "ligar": ("打电话/打开（电器）", "regular -ar", "llamar", "ligar para alguém 打电话给某人；ligar a TV 开电视"),
    "sonhar": ("做梦/梦想", "regular -ar", "soñar", "sonhar com：Sonhei com você"),
    "descansar": ("休息", "regular -ar", "descansar", None),
    "celebrar": ("庆祝", "regular -ar", "celebrar", None),
    "chorar": ("哭", "regular -ar", "llorar", "西语 ll→葡语 ch：llorar→chorar"),
    "rir": ("笑", "irregular", "reír", "现在时 rio/ris/ri/rimos/riem；rio 也是'河流'，语境区分"),
    # ---- W6：报道常用动词 ----
    "publicar": ("发表/刊登", "regular -ar", "publicar", None),
    "anunciar": ("宣布", "regular -ar", "anunciar", None),
    "declarar": ("声明", "regular -ar", "declarar", None),
    "explicar": ("解释", "regular -ar", "explicar", None),
    "discutir": ("讨论", "regular -ir", "discutir", None),
    "votar": ("投票/表决", "regular -ar", "votar", "votar em alguém 投票给某人"),
    "eleger": ("选举", "regular -er", "elegir", "eu elejo（g→j）"),
    "governar": ("治理/执政", "regular -ar", "gobernar", "西语 gobierno 双元音化，葡语 governo 没有"),
    "protestar": ("抗议", "regular -ar", "protestar", "protestar contra 抗议…"),
    "reclamar": ("抱怨/投诉", "regular -ar", "reclamar", "reclamar de：reclamar do serviço 投诉服务"),
    "roubar": ("偷/抢", "regular -ar", "robar", None),
    "prender": ("逮捕", "regular -er", "prender", None),
    "matar": ("杀死", "regular -ar", "matar", None),
    "investigar": ("调查", "regular -ar", "investigar", None),
    "proteger": ("保护", "regular -er", "proteger", "eu protejo（g→j）"),
    "aumentar": ("增加/上涨", "regular -ar", "aumentar", None),
    "diminuir": ("减少", "irregular", "disminuir", "nós diminuímos（í 带音符，同 caímos 模式）；西语 disminuyo 不规则"),
    "cair": ("下降/跌倒", "irregular", "caer", "eu caio；nós caímos（同 sair 模式）；O dólar caiu 美元跌了"),
    "dever": ("欠/应该", "regular -er", "deber", "Eu devo estudar 我应该学习；dever dinheiro 欠钱"),
    "participar": ("参加", "regular -ar", "participar", "participar de：participar da reunião 参加会议"),
    "atender": ("接待/接听/满足", "regular -er", "atender", "atender o telefone 接电话；atender clientes 接待客户；atender um pedido 满足请求"),
    # ---- W7：计划类动词 ----
    "planejar": ("计划/规划", "regular -ar", "planear", "对应西语 planear；巴西也常用 planejar=planificar"),
    "organizar": ("组织/安排", "regular -ar", "organizar", None),
    "arrumar": ("收拾/整理", "regular -ar", None, "西语 arreglar: arreglo/arreglas/arregla/arreglamos/arreglan——葡语 arrumar=收拾/整理/打包：arrumar a mala"),
    "reservar": ("预订", "regular -ar", "reservar", None),
    "confirmar": ("确认", "regular -ar", "confirmar", None),
    "cancelar": ("取消", "regular -ar", "cancelar", None),
    "adiar": ("推迟", "regular -ar", "adiar", None),
    "embarcar": ("登机/上船", "regular -ar", "embarcar", None),
    "voar": ("飞", "regular -ar", "volar", "西语 vuelo 双元音化，葡语 voo 没有"),
    "pousar": ("降落", "regular -ar", "aterrizar", "反义词 decolar=起飞"),
    "decolar": ("起飞", "regular -ar", "despegar", "反义词 pousar=降落"),
    "nadar": ("游泳", "regular -ar", "nadar", None),
    "caminhar": ("徒步/走路", "regular -ar", "caminar", None),
    "relaxar": ("放松", "regular -ar", "relajar", None),
    "aproveitar": ("享受/利用", "regular -ar", "aprovechar", "Aproveite! 好好享受吧！；aproveitar o tempo 利用时间"),
    "prever": ("预测/预见", "irregular", "prever", "变位同 ver：prevejo/prevês/prevê/prevemos/preveem"),
    "prometer": ("答应", "regular -er", "prometer", "变位与西语完全一致"),
    "gastar": ("花费/花钱", "regular -ar", "gastar", "gastar dinheiro/tempo 花钱/花时间"),
    "trocar": ("换/兑换/交换", "regular -ar", "cambiar", "trocar dinheiro 换钱；trocar de roupa 换衣服；trocar A por B 用 A 换 B"),
    "alugar": ("租", "regular -ar", "alquilar", "alugar um carro/apartamento 租车/租房"),
    # ---- W8：情感观点动词 ----
    "amar": ("爱", "regular -ar", "amar", None),
    "desejar": ("祝愿/渴望", "regular -ar", "desear", "desejar que + 虚拟式：Desejo que tudo corra bem"),
    "duvidar": ("怀疑", "regular -ar", "dudar", "duvidar que + 虚拟式：Duvido que ele venha"),
    "temer": ("害怕/担心", "regular -er", "temer", "temer que + 虚拟式：Temo que chova"),
    "imaginar": ("想象", "regular -ar", "imaginar", "Imagina! 你想想看！；imaginar que + 虚拟式（表疑虑）"),
    "supor": ("猜想", "irregular", "suponer", "变位同 pôr：suponho/supões/supõe/supomos/supõem"),
    "sugerir": ("建议", "irregular", "sugerir", "eu sugiro（e→i）；sugerir que + 虚拟式"),
    "exigir": ("要求", "regular -ir", "exigir", "eu exijo（g→j）；exigir que + 虚拟式"),
    "lamentar": ("遗憾/惋惜", "regular -ar", "lamentar", "lamentar que + 虚拟式：Lamento que não possas vir"),
    "confiar": ("信任", "regular -ar", "confiar", "confiar em：Confio em você"),
    "aceitar": ("接受", "regular -ar", "aceitar", None),
    "recusar": ("拒绝", "regular -ar", "rechazar", None),
    "proibir": ("禁止", "irregular", "prohibir", "eu proíbo（í 带音符）；proibir que + 虚拟式；É proibido fumar"),
    "aconselhar": ("劝告", "regular -ar", "aconsejar", "aconselhar alguém a + 不定式：Aconselho você a descansar"),
    "elogiar": ("表扬", "regular -ar", "elogiar", None),
    "perdoar": ("原谅", "regular -ar", "perdonar", None),
    "agradecer": ("感谢", "regular -er", "agradecer", "eu agradeço（c→ç）；agradecer por：Agradeço pela ajuda"),
    "mentir": ("说谎", "irregular", "mentir", "eu minto（e→i，同 sentir 模式）"),
    "concordar": ("同意", "regular -ar", "concordar", "concordar com：Concordo com você"),
    "insistir": ("坚持", "regular -ir", "insistir", "insistir em：Ele insiste em ir；insistir que + 虚拟式"),
    "reconhecer": ("承认/认出", "regular -er", "reconocer", "eu reconheço（c→ç）"),
}


# ============ 词表（条目格式与 build_weekly_vocab.py 一致）============
# (rank, pt, pos, zh, example_pt, example_zh, falseFriend, verb_infinitive)
E = lambda rank, pt, pos, zh, xpt, xzh, ff=None, vb=None: (rank, pt, pos, zh, xpt, xzh, ff, vb)

# ---- W5（过去时周）：时间/日期/星期月份/数字进阶/家庭生活/叙事 ----
W5 = [
    E(401, "ontem", "副词", "昨天", "Eu estudei ontem à noite.", "我昨晚学习了。"),
    E(402, "anteontem", "副词", "前天", "Anteontem foi feriado.", "前天是假日。"),
    E(403, "madrugada", "名词", "凌晨", "O ônibus chegou de madrugada.", "公交车凌晨才到。"),
    E(404, "feriado", "名词", "假日", "Ontem foi feriado nacional.", "昨天是全国假日。"),
    E(405, "aniversário", "名词", "生日 / 周年", "O aniversário dela é em julho.", "她的生日在七月。"),
    E(406, "data", "名词", "日期", "Que data é hoje?", "今天几号？"),
    E(407, "calendário", "名词", "日历", "O calendário está na parede.", "日历挂在墙上。"),
    E(408, "século", "名词", "世纪", "O prédio é do século passado.", "这栋楼是上世纪的。"),
    E(409, "década", "名词", "十年", "Eles moraram aqui por uma década.", "他们在这里住过十年。"),
    E(410, "fim de semana", "名词词组", "周末", "No fim de semana eu descansei.", "周末我休息了。"),
    E(411, "semana passada", "词组", "上周", "Na semana passada eu viajei.", "上周我去旅行了。"),
    E(412, "passado", "形容词/名词", "过去的 / 过去", "o ano passado", "去年"),
    E(413, "infância", "名词", "童年", "A minha infância foi feliz.", "我的童年很幸福。"),
    E(414, "juventude", "名词", "青春", "Na juventude ele jogava futebol.", "年轻时他常踢足球。"),
    E(415, "velhice", "名词", "晚年", "Na velhice ela morou com os filhos.", "晚年她和孩子们住在一起。"),
    E(416, "nascimento", "名词", "出生", "a data de nascimento", "出生日期"),
    E(417, "morte", "名词", "死亡", "A morte do avô foi triste.", "外公的去世令人悲伤。"),
    E(418, "história", "名词", "故事 / 历史", "A avó contava histórias.", "奶奶以前常讲故事。"),
    E(419, "começo", "名词", "开始 / 开头", "no começo do ano", "在年初"),
    E(420, "início", "名词", "起初 / 开始", "no início da história", "在故事的开头"),
    E(421, "meio", "名词/形容词", "中间 / 半", "no meio do caminho", "在半路上"),
    E(422, "fim", "名词", "结束", "no fim do filme", "在电影结尾"),
    E(423, "final", "名词/形容词", "结局 / 最后的", "o final da história", "故事的结局"),
    E(424, "parte", "名词", "部分", "a primeira parte do livro", "书的第一部分"),
    E(425, "memória", "名词", "记忆", "Tenho boa memória da infância.", "我对童年记忆犹新。"),
    E(426, "lembrança", "名词", "回忆 / 纪念品", "Essa foto é uma boa lembrança.", "这张照片是美好的回忆。"),
    E(427, "sonho", "名词", "梦 / 梦想", "O sonho dele era ser piloto.", "他的梦想是当飞行员。"),
    E(428, "pesadelo", "名词", "噩梦", "Eu tive um pesadelo ontem.", "我昨晚做了个噩梦。"),
    E(429, "conto", "名词", "短篇小说", "O conto é muito famoso.", "这篇短篇小说很有名。"),
    E(430, "segunda-feira", "名词", "星期一", "Na segunda-feira eu trabalhei.", "周一我上班了。"),
    E(431, "terça-feira", "名词", "星期二", "A reunião foi na terça-feira.", "会议是在周二开的。"),
    E(432, "quarta-feira", "名词", "星期三", "Na quarta-feira choveu muito.", "周三雨下得很大。"),
    E(433, "quinta-feira", "名词", "星期四", "Ela chegou na quinta-feira.", "她周四到的。"),
    E(434, "sexta-feira", "名词", "星期五", "Sexta-feira passada fomos ao bar.", "上周五我们去了酒吧。"),
    E(435, "sábado", "名词", "星期六", "No sábado eu dormi até tarde.", "周六我睡到很晚。"),
    E(436, "domingo", "名词", "星期日", "No domingo almoçamos em família.", "周日我们全家一起吃了午饭。"),
    E(437, "janeiro", "名词", "一月", "Em janeiro faz muito calor no Brasil.", "巴西一月很热。"),
    E(438, "agosto", "名词", "八月", "Agosto é seco em São Paulo.", "圣保罗八月很干燥。"),
    E(439, "setembro", "名词", "九月", "Ela nasceu em setembro.", "她出生在九月。"),
    E(440, "dezembro", "名词", "十二月", "Em dezembro tem festa na empresa.", "十二月公司有聚会。"),
    E(441, "zero", "数词", "零", "O time perdeu por dois a zero.", "球队零比二输了。"),
    E(442, "mil", "数词", "一千", "O carro custou trinta mil reais.", "这辆车花了三万雷亚尔。"),
    E(443, "milhão", "数词", "百万", "São Paulo tem doze milhões de pessoas.", "圣保罗有一千两百万人口。"),
    E(444, "número", "名词", "数字 / 号码", "Qual é o seu número de telefone?", "你的电话号码是多少？"),
    E(445, "metade", "名词", "一半", "Eu comi a metade do bolo.", "我吃了一半蛋糕。"),
    E(446, "dobro", "名词", "双倍", "O preço subiu para o dobro.", "价格涨了一倍。"),
    E(447, "par", "形容词/名词", "双数的 / 一双", "um número par", "一个偶数"),
    E(448, "ímpar", "形容词", "单数的", "um número ímpar", "一个奇数"),
    E(449, "marido", "名词", "丈夫", "O marido dela é médico.", "她丈夫是医生。"),
    E(450, "esposa", "名词", "妻子", "A esposa dele nasceu no Rio.", "他妻子出生在里约。", "西语 esposa=妻子（同义），但复数 esposas=手铐！葡语'手铐'是 algemas"),
    E(451, "casal", "名词", "夫妻 / 情侣", "O casal se conheceu na faculdade.", "这对夫妻是在大学认识的。"),
    E(452, "avô", "名词", "祖父 / 外公", "O meu avô era professor.", "我爷爷以前是老师。"),
    E(453, "avó", "名词", "祖母 / 外婆", "A minha avó fazia bolo no domingo.", "我奶奶以前周日总做蛋糕。"),
    E(454, "neto", "名词", "孙子 / 外孙", "A avó tem cinco netos.", "奶奶有五个孙辈。"),
    E(455, "neta", "名词", "孙女 / 外孙女", "A neta dela nasceu em 2020.", "她的孙女 2020 年出生。"),
    E(456, "tio", "名词", "叔叔 / 舅舅", "O meu tio morava perto da gente.", "我叔叔以前住得离我们很近。"),
    E(457, "tia", "名词", "阿姨 / 姑姑", "A tia trouxe presentes.", "阿姨带来了礼物。"),
    E(458, "primo", "名词", "堂 / 表兄弟", "Eu brincava com os meus primos.", "我以前常和表兄弟们玩。"),
    E(459, "prima", "名词", "堂 / 表姐妹", "A prima dela se casou em maio.", "她的表姐五月结婚了。"),
    E(460, "sobrinho", "名词", "侄子 / 外甥", "O sobrinho dele tem dez anos.", "他的侄子十岁。"),
    E(461, "sogro", "名词", "岳父 / 公公", "O sogro dela era muito simpático.", "她的岳父人很好。"),
    E(462, "sogra", "名词", "岳母 / 婆婆", "A sogra cozinha muito bem.", "岳母做饭特别好吃。"),
    E(463, "cunhado", "名词", "姐夫 / 内兄（姻亲男性）", "O cunhado dele é engenheiro.", "他的姐夫是工程师。"),
    E(464, "genro", "名词", "女婿", "O genro dela é chinês.", "她的女婿是中国人。"),
    E(465, "nora", "名词", "儿媳", "A nora dela fala três línguas.", "她的儿媳会说三种语言。"),
    E(466, "bebê", "名词", "婴儿", "O bebê chorou a noite toda.", "宝宝哭了一整夜。"),
    E(467, "criança", "名词", "孩子", "As crianças brincavam no quintal.", "孩子们当时在院子里玩。", "西语'孩子'是 niño；crianza 在西语=养育（名词）。葡语 criança 只指孩子"),
    E(468, "adolescente", "名词", "青少年", "Ele era adolescente em 2010.", "2010 年他还是个青少年。"),
    E(469, "adulto", "名词", "成年人", "Quando adulto, ele saiu de casa.", "成年后他搬出了家。"),
    E(470, "idoso", "名词", "老人", "O idoso caminhava devagar.", "老人慢慢地走着。"),
    E(471, "parente", "名词", "亲戚", "Os parentes vieram para a festa.", "亲戚们都来参加聚会了。（注意：葡语'父母'是 pais）"),
    E(472, "padrinho", "名词", "教父 / 证婚人（阴性 madrinha）", "O padrinho do casamento era o tio.", "婚礼的证婚人是叔叔。"),
    E(473, "casamento", "名词", "婚礼", "O casamento foi na praia.", "婚礼是在海滩举行的。"),
    E(474, "festa", "名词", "聚会 / 派对", "A festa foi muito boa.", "聚会很棒。"),
    E(475, "presente", "名词", "礼物", "Ele ganhou um presente de aniversário.", "他收到了一份生日礼物。", "西语'礼物'是 regalo；presente 在西语=出席的/现在（时态）"),
    E(476, "bolo", "名词", "蛋糕", "O bolo de chocolate estava ótimo.", "巧克力蛋糕特别好吃。"),
    E(477, "jantar", "名词", "晚餐", "O jantar foi servido às oito.", "晚餐八点上的。"),
    E(478, "churrasco", "名词", "巴西烤肉", "No domingo teve churrasco.", "周日吃了巴西烤肉。"),
    E(479, "reunião", "名词", "会议 / 聚会", "A reunião começou atrasada.", "会议晚开始了。"),
    E(480, "encontro", "名词", "见面 / 约会", "O encontro foi num café.", "见面是在一家咖啡馆。"),
    E(481, "rato", "名词", "老鼠", "Um rato passou pela cozinha.", "一只老鼠跑过了厨房。", "西语 rato=片刻；葡语'片刻'是 momento；西语'老鼠'是 ratón/rata"),
    E(482, "assistir", "动词", "观看 / 出席", "Nós assistimos ao jogo no bar.", "我们在酒吧看了比赛。", "西语 asistir=参加/出席；葡语 assistir (a)=观看；葡语'参加'是 participar/comparecer", "assistir"),
    E(483, "contar", "动词", "讲述 / 数", "A avó contou uma história.", "奶奶讲了一个故事。", None, "contar"),
    E(484, "terminar", "动词", "结束", "O filme terminou às dez.", "电影十点结束的。", None, "terminar"),
    E(485, "visitar", "动词", "拜访 / 参观", "Nós visitamos a avó no domingo.", "我们周日去看望了奶奶。", None, "visitar"),
    E(486, "pôr", "动词", "放 / 摆", "Ele pôs o livro na mesa.", "他把书放在了桌上。", None, "pôr"),
    E(487, "faltar", "动词", "缺少 / 没到", "Faltou água na festa?", "聚会上水不够了吗？", None, "faltar"),
    E(488, "nascer", "动词", "出生", "Eu nasci numa cidade pequena.", "我出生在一个小城。", None, "nascer"),
    E(489, "morrer", "动词", "死 / 去世", "O avô dele morreu em 2019.", "他爷爷 2019 年去世了。", None, "morrer"),
    E(490, "crescer", "动词", "长大 / 成长", "Eu cresci no interior.", "我在内地长大。", None, "crescer"),
    E(491, "casar", "动词", "结婚", "Eles se casaram em 2015.", "他们 2015 年结的婚。", None, "casar"),
    E(492, "namorar", "动词", "谈恋爱", "Eles namoraram por dois anos.", "他们谈了两年恋爱。", None, "namorar"),
    E(493, "divorciar", "动词", "离婚", "Eles se divorciaram no ano passado.", "他们去年离婚了。", None, "divorciar"),
    E(494, "convidar", "动词", "邀请", "Ela convidou os amigos para o jantar.", "她邀请了朋友们吃晚饭。", None, "convidar"),
    E(495, "ligar", "动词", "打电话 / 打开（电器）", "Eu liguei para a minha mãe ontem.", "我昨天给妈妈打了电话。", "西语 ligar=绑/调情；葡语'绑'是 amarrar；葡语 ligar=打电话/接通（电器）", "ligar"),
    E(496, "sonhar", "动词", "做梦 / 梦想", "Eu sonhei com você ontem.", "我昨晚梦到你了。", None, "sonhar"),
    E(497, "descansar", "动词", "休息", "No sábado eu descansei o dia todo.", "周六我休息了一整天。", None, "descansar"),
    E(498, "celebrar", "动词", "庆祝", "Nós celebramos o aniversário dela.", "我们庆祝了她的生日。", None, "celebrar"),
    E(499, "chorar", "动词", "哭", "A criança chorou muito.", "孩子哭得很厉害。", None, "chorar"),
    E(500, "rir", "动词", "笑", "Todos riram da piada.", "大家都被这个笑话逗笑了。", None, "rir"),
]

# ---- W6（新闻阅读周）：新闻/社会/城市/工作/经济 ----
W6 = [
    E(501, "governo", "名词", "政府", "O governo anunciou novas medidas.", "政府宣布了新措施。"),
    E(502, "presidente", "名词", "总统 / 主席", "O presidente falou à imprensa.", "总统对媒体讲了话。"),
    E(503, "ministro", "名词", "部长", "O ministro da Saúde deu entrevista.", "卫生部长接受了采访。"),
    E(504, "política", "名词", "政治 / 政策", "A política econômica mudou.", "经济政策变了。"),
    E(505, "eleição", "名词", "选举", "A eleição foi em outubro.", "选举在十月举行。"),
    E(506, "voto", "名词", "选票", "Cada voto é importante.", "每一票都很重要。"),
    E(507, "partido", "名词", "政党", "O partido ganhou a eleição.", "该党赢得了选举。"),
    E(508, "lei", "名词", "法律", "A nova lei começa em janeiro.", "新法律一月生效。"),
    E(509, "direito", "名词", "权利 / 法学", "Todos têm direito à saúde.", "人人享有健康权。"),
    E(510, "justiça", "名词", "司法 / 公正", "O caso foi para a justiça.", "案子进入了司法程序。"),
    E(511, "tribunal", "名词", "法院", "O tribunal julga o caso hoje.", "法院今天审理此案。"),
    E(512, "juiz", "名词", "法官", "O juiz decidiu o caso.", "法官对案件作出了裁决。"),
    E(513, "crime", "名词", "犯罪", "O crime aconteceu à noite.", "犯罪发生在夜里。"),
    E(514, "polícia", "名词", "警察 / 警方", "A polícia investiga o caso.", "警方正在调查此案。"),
    E(515, "policial", "名词", "警察（个体）", "O policial prendeu o ladrão.", "警察抓住了小偷。"),
    E(516, "ladrão", "名词", "小偷", "O ladrão roubou um celular.", "小偷偷了一部手机。"),
    E(517, "prisão", "名词", "监狱 / 逮捕", "Ele foi levado para a prisão.", "他被送进了监狱。"),
    E(518, "segurança", "名词", "安全", "A segurança da cidade melhorou.", "城市治安改善了。"),
    E(519, "violência", "名词", "暴力", "A violência é um problema social.", "暴力是一个社会问题。"),
    E(520, "acidente", "名词", "事故", "O acidente foi na avenida principal.", "事故发生在主干道。"),
    E(521, "incêndio", "名词", "火灾", "O incêndio destruiu o prédio.", "大火烧毁了大楼。"),
    E(522, "enchente", "名词", "洪水", "A enchente deixou famílias sem casa.", "洪水让一些家庭无家可归。"),
    E(523, "guerra", "名词", "战争", "A guerra mudou o país.", "战争改变了这个国家。"),
    E(524, "paz", "名词", "和平", "Todos querem a paz.", "人人都渴望和平。"),
    E(525, "ataque", "名词", "袭击", "O ataque foi na madrugada.", "袭击发生在凌晨。"),
    E(526, "greve", "名词", "罢工", "A greve dos ônibus começou hoje.", "公交罢工今天开始。"),
    E(527, "avenida", "名词", "大街", "O acidente foi na Avenida Paulista.", "事故发生在保利斯塔大街。"),
    E(528, "bairro", "名词", "街区", "O bairro é tranquilo e seguro.", "这个街区安静又安全。"),
    E(529, "prefeitura", "名词", "市政府", "A prefeitura vai construir uma escola.", "市政府将建一所学校。"),
    E(530, "prefeito", "名词", "市长", "O prefeito inaugurou o parque.", "市长为公园揭幕。"),
    E(531, "trânsito", "名词", "交通", "O trânsito está parado no centro.", "市中心交通堵死了。"),
    E(532, "morador", "名词", "居民", "Os moradores reclamam do barulho.", "居民们抱怨噪音。"),
    E(533, "cidadão", "名词", "公民 / 市民", "O cidadão tem direitos e deveres.", "公民有权利也有义务。"),
    E(534, "população", "名词", "人口 / 民众", "A população da cidade cresceu.", "本市人口增长了。"),
    E(535, "economia", "名词", "经济", "A economia do país cresceu este ano.", "今年国家经济增长了。"),
    E(536, "crise", "名词", "危机", "A crise afetou muitas empresas.", "危机影响了很多公司。"),
    E(537, "negócio", "名词", "生意 / 商业", "O negócio foi fechado ontem.", "生意昨天谈成了。"),
    E(538, "indústria", "名词", "工业", "A indústria cresce na região.", "该地区工业在增长。"),
    E(539, "fábrica", "名词", "工厂", "A fábrica fechou as portas.", "工厂倒闭了。"),
    E(540, "funcionário", "名词", "职员 / 雇员", "A empresa tem cem funcionários.", "这家公司有一百名员工。"),
    E(541, "chefe", "名词", "老板 / 上司", "O chefe convocou uma reunião.", "老板召集了会议。"),
    E(542, "gerente", "名词", "经理", "O gerente apresentou os resultados.", "经理公布了业绩。"),
    E(543, "cliente", "名词", "客户", "O cliente reclamou do serviço.", "客户投诉了服务。"),
    E(544, "salário", "名词", "工资", "O salário mínimo vai aumentar.", "最低工资要涨了。"),
    E(545, "emprego", "名词", "工作 / 职位", "Ele conseguiu um emprego novo.", "他找到了一份新工作。"),
    E(546, "desemprego", "名词", "失业", "O desemprego caiu este ano.", "今年失业率下降了。"),
    E(547, "imposto", "名词", "税", "O imposto sobre produtos subiu.", "产品税上调了。"),
    E(548, "inflação", "名词", "通货膨胀", "A inflação subiu no último mês.", "上个月通胀上升了。"),
    E(549, "dólar", "名词", "美元", "O dólar subiu hoje.", "美元今天涨了。"),
    E(550, "real", "名词/形容词", "雷亚尔 / 真实的", "O produto custa cinquenta reais.", "这个产品五十雷亚尔。", "巴西货币 real（复数 reais）；西语 real=真实的/皇家的，西语没有这种货币"),
    E(551, "moeda", "名词", "货币", "O real é a moeda do Brasil.", "雷亚尔是巴西的货币。"),
    E(552, "dívida", "名词", "债务 / 欠款", "A empresa pagou as dívidas.", "公司还清了债务。"),
    E(553, "lucro", "名词", "利润", "O lucro da empresa aumentou.", "公司利润增加了。"),
    E(554, "investimento", "名词", "投资", "O investimento gerou empregos.", "这项投资创造了就业。"),
    E(555, "aumento", "名词", "上涨 / 增加", "O aumento do preço começou ontem.", "涨价是从昨天开始的。"),
    E(556, "taxa", "名词", "费率 / 税率", "A taxa de juros caiu.", "利率下降了。"),
    E(557, "crescimento", "名词", "增长", "O crescimento da economia foi bom.", "经济增长表现不错。"),
    E(558, "produto", "名词", "产品", "O produto chega às lojas em maio.", "产品五月上架。"),
    E(559, "serviço", "名词", "服务", "O serviço da empresa é bom.", "这家公司的服务不错。"),
    E(560, "projeto", "名词", "项目", "O projeto foi aprovado ontem.", "项目昨天获批了。"),
    E(561, "contrato", "名词", "合同", "O contrato foi assinado hoje.", "合同今天签了。"),
    E(562, "doença", "名词", "疾病", "A doença se espalhou rápido.", "疾病传播得很快。"),
    E(563, "médico", "名词", "医生", "O médico atendeu vinte pacientes.", "医生接诊了二十个病人。"),
    E(564, "remédio", "名词", "药", "O remédio está na farmácia.", "这药在药店有售。"),
    E(565, "vacina", "名词", "疫苗", "A vacina chegou aos postos de saúde.", "疫苗已到达卫生站。"),
    E(566, "notícia", "名词", "新闻 / 消息", "A notícia saiu no jornal de hoje.", "这条新闻上了今天的报纸。"),
    E(567, "reportagem", "名词", "报道", "A reportagem mostrou a enchente.", "报道播出了洪水的情况。"),
    E(568, "jornalista", "名词", "记者", "A jornalista entrevistou o prefeito.", "记者采访了市长。"),
    E(569, "imprensa", "名词", "新闻界 / 报刊", "A imprensa divulgou o caso.", "媒体公开了此案。"),
    E(570, "mídia", "名词", "媒体", "A mídia falou sobre a crise.", "媒体报道了这场危机。"),
    E(571, "manchete", "名词", "头条", "A manchete de hoje é sobre a eleição.", "今天的头条是关于选举的。"),
    E(572, "programa", "名词", "节目 / 方案", "O programa de TV começou tarde.", "电视节目很晚才开始。"),
    E(573, "pesquisa", "名词", "调查 / 研究", "A pesquisa mostra o resultado.", "调查显示了结果。"),
    E(574, "resultado", "名词", "结果", "O resultado saiu na sexta-feira.", "结果周五出来了。"),
    E(575, "problema", "名词", "问题", "O problema foi resolvido.", "问题解决了。"),
    E(576, "caso", "名词", "案件 / 情况", "O caso está com a polícia.", "案件在警方手里。"),
    E(577, "fato", "名词", "事实 / 西装", "O jornal publicou os fatos.", "报纸刊出了事实。", "葡语 fato=事实；也=西装（=西语 traje）；西语'事实'是 hecho/facto"),
    E(578, "sucesso", "名词", "成功", "O filme fez muito sucesso.", "这部电影大获成功。", "西语 suceso=事件（新闻常用）；葡语'事件'是 acontecimento/incidente；sucesso=成功"),
    E(579, "propina", "名词", "贿赂（巴西）", "O político recebeu propina.", "这名政客收受了贿赂。", "西语 propina=小费；巴西葡语 propina=贿赂/黑钱；葡语'小费'是 gorjeta"),
    E(580, "publicar", "动词", "发表 / 刊登", "O jornal publicou a entrevista.", "报纸刊登了采访。", None, "publicar"),
    E(581, "anunciar", "动词", "宣布", "O governo anunciou o novo plano.", "政府宣布了新方案。", None, "anunciar"),
    E(582, "declarar", "动词", "声明", "O presidente declarou emergência.", "总统宣布进入紧急状态。", None, "declarar"),
    E(583, "explicar", "动词", "解释", "O ministro explicou a decisão.", "部长解释了这项决定。", None, "explicar"),
    E(584, "discutir", "动词", "讨论", "O Congresso discute a nova lei.", "国会正在讨论新法律。", None, "discutir"),
    E(585, "votar", "动词", "投票 / 表决", "Os deputados votam amanhã.", "议员们明天表决。", None, "votar"),
    E(586, "eleger", "动词", "选举", "O povo elegeu o novo prefeito.", "民众选出了新市长。", None, "eleger"),
    E(587, "governar", "动词", "治理 / 执政", "Ela governa o estado há quatro anos.", "她治理这个州已经四年了。", None, "governar"),
    E(588, "protestar", "动词", "抗议", "Os estudantes protestaram contra o aumento.", "学生们抗议涨价。", None, "protestar"),
    E(589, "reclamar", "动词", "抱怨 / 投诉", "Os moradores reclamaram do barulho.", "居民们抱怨噪音。", None, "reclamar"),
    E(590, "roubar", "动词", "偷 / 抢", "Roubaram o banco da cidade.", "城里的银行被抢了。", None, "roubar"),
    E(591, "prender", "动词", "逮捕", "A polícia prendeu o suspeito.", "警方逮捕了嫌疑人。", None, "prender"),
    E(592, "matar", "动词", "杀死", "O ladrão matou o dono da loja.", "小偷杀害了店主。", None, "matar"),
    E(593, "investigar", "动词", "调查", "A polícia investiga o crime.", "警方在调查这起犯罪。", None, "investigar"),
    E(594, "proteger", "动词", "保护", "O programa protege as crianças.", "该项目保护儿童。", None, "proteger"),
    E(595, "aumentar", "动词", "增加 / 上涨", "Os preços aumentaram de novo.", "物价又涨了。", None, "aumentar"),
    E(596, "diminuir", "动词", "减少", "O desemprego diminuiu este ano.", "今年失业减少了。", None, "diminuir"),
    E(597, "cair", "动词", "下降 / 跌倒", "O dólar caiu hoje.", "美元今天跌了。", None, "cair"),
    E(598, "dever", "动词", "欠 / 应该", "A empresa deve milhões ao banco.", "公司欠银行数百万。", None, "dever"),
    E(599, "participar", "动词", "参加", "Mil pessoas participaram do protesto.", "一千人参加了抗议。", None, "participar"),
    E(600, "atender", "动词", "接待 / 接听 / 满足", "O hospital atendeu cem pacientes.", "医院接诊了一百位病人。", "西语 atender=注意/接待；葡语 atender=接待/接听(电话)/满足(要求)；'注意'葡语是 prestar atenção", "atender"),
]


# ---- W7（将来时周）：旅行/交通/天气/自然/计划 ----
W7 = [
    E(601, "viagem", "名词", "旅行", "A viagem será em julho.", "旅行将在七月。"),
    E(602, "passagem", "名词", "机票 / 车票", "Comprei a passagem para o Rio.", "我买好了去里约的票。"),
    E(603, "bilhete", "名词", "票", "O bilhete custa cem reais.", "票一百雷亚尔。"),
    E(604, "passaporte", "名词", "护照", "O passaporte está na gaveta.", "护照在抽屉里。"),
    E(605, "visto", "名词", "签证", "O visto sai na próxima semana.", "签证下周就下来。"),
    E(606, "bagagem", "名词", "行李", "A bagagem chega na esteira três.", "行李在三号传送带上。"),
    E(607, "mala", "名词", "行李箱", "A mala está no táxi.", "行李箱在出租车上。", "西语'行李箱'是 maleta；mala 在西语是 malo 的阴性（坏的）"),
    E(608, "mochila", "名词", "背包", "A mochila está pesada.", "背包很重。"),
    E(609, "hotel", "名词", "酒店", "O hotel fica perto da praia.", "酒店离海滩很近。"),
    E(610, "pousada", "名词", "客栈 / 民宿", "A pousada é simples e aconchegante.", "客栈简朴又温馨。"),
    E(611, "reserva", "名词", "预订", "A reserva está no seu nome.", "预订用的是你的名字。"),
    E(612, "recepção", "名词", "前台", "A chave está na recepção.", "钥匙在前台。"),
    E(613, "aeroporto", "名词", "机场", "O aeroporto fica longe do centro.", "机场离市中心很远。"),
    E(614, "voo", "名词", "航班", "O voo sai às sete da manhã.", "航班早上七点起飞。"),
    E(615, "passageiro", "名词", "乘客", "Os passageiros embarcam agora.", "乘客们现在开始登机。"),
    E(616, "assento", "名词", "座位", "O meu assento é na janela.", "我的座位靠窗。"),
    E(617, "atraso", "名词", "延误", "O voo teve um atraso de duas horas.", "航班延误了两小时。"),
    E(618, "destino", "名词", "目的地", "O destino final é Lisboa.", "最终目的地是里斯本。"),
    E(619, "passeio", "名词", "短途游 / 游览", "O passeio de barco foi ótimo.", "乘船游览很棒。"),
    E(620, "turista", "名词", "游客", "Os turistas vão adorar a cidade.", "游客们会喜欢这座城市。"),
    E(621, "turismo", "名词", "旅游业", "O turismo cresce na região.", "该地区的旅游业在增长。"),
    E(622, "guia", "名词", "导游 / 指南", "O guia explicou a história do lugar.", "导游讲解了这个地方的历史。"),
    E(623, "mapa", "名词", "地图", "O mapa está no celular.", "地图在手机上。"),
    E(624, "foto", "名词", "照片", "Vou tirar muitas fotos na viagem.", "旅行中我要拍很多照片。"),
    E(625, "estação", "名词", "车站 / 季节", "A estação de trem fica no centro.", "火车站在市中心。"),
    E(626, "plataforma", "名词", "站台", "O trem sai da plataforma dois.", "火车从二号站台出发。"),
    E(627, "rodovia", "名词", "公路", "A rodovia está cheia no feriado.", "假日公路很堵。"),
    E(628, "estrada", "名词", "道路 / 公路", "A estrada é bonita e perigosa.", "这条路风景美但危险。"),
    E(629, "pedágio", "名词", "过路费", "O pedágio custa dez reais.", "过路费十雷亚尔。"),
    E(630, "carona", "名词", "搭便车", "Ele vai me dar carona até o aeroporto.", "他会顺路送我去机场。"),
    E(631, "norte", "名词", "北方", "O norte do Brasil é quente.", "巴西北部很热。"),
    E(632, "sul", "名词", "南方", "No sul faz frio no inverno.", "南方冬天冷。"),
    E(633, "leste", "名词", "东方（注意：西语 este→葡语 leste）", "O sol nasce a leste.", "太阳从东边升起。"),
    E(634, "oeste", "名词", "西方", "O sol se põe a oeste.", "太阳在西边落下。"),
    E(635, "fronteira", "名词", "边境", "A fronteira fica a cem quilômetros.", "边境在一百公里外。"),
    E(636, "alfândega", "名词", "海关", "A mala parou na alfândega.", "行李在海关被拦下了。"),
    E(637, "navio", "名词", "轮船", "O navio sai no sábado.", "轮船周六起航。"),
    E(638, "barco", "名词", "小船", "Vamos de barco até a ilha.", "我们坐船去岛上。"),
    E(639, "mar", "名词", "大海", "O mar está calmo hoje.", "今天海面很平静。"),
    E(640, "oceano", "名词", "大洋", "O oceano Atlântico é enorme.", "大西洋浩瀚无边。"),
    E(641, "onda", "名词", "浪", "As ondas estão grandes hoje.", "今天浪很大。"),
    E(642, "areia", "名词", "沙", "A areia é branca e fina.", "沙子又白又细。"),
    E(643, "ilha", "名词", "岛", "A ilha tem praias lindas.", "岛上有美丽的海滩。"),
    E(644, "montanha", "名词", "山", "A montanha fica a duas horas daqui.", "山离这里两小时车程。"),
    E(645, "serra", "名词", "山脉 / 山区", "A serra é fria à noite.", "山区夜里冷。"),
    E(646, "rio", "名词", "河流", "O rio atravessa a cidade.", "河流穿过城市。"),
    E(647, "lago", "名词", "湖", "O lago é perfeito para nadar.", "这个湖很适合游泳。"),
    E(648, "floresta", "名词", "森林", "A floresta Amazônica é enorme.", "亚马孙森林广袤无边。"),
    E(649, "mata", "名词", "树林", "A mata tem muitos pássaros.", "树林里有很多鸟。"),
    E(650, "campo", "名词", "田野 / 乡下", "No campo o céu é mais limpo.", "乡下的天空更清澈。"),
    E(651, "natureza", "名词", "大自然", "Eu adoro o contato com a natureza.", "我热爱亲近大自然。"),
    E(652, "paisagem", "名词", "风景", "A paisagem da estrada é linda.", "沿途风景很美。"),
    E(653, "cachoeira", "名词", "瀑布", "A cachoeira fica no meio da mata.", "瀑布在树林深处。"),
    E(654, "árvore", "名词", "树", "A árvore dá uma sombra boa.", "这棵树的树荫很舒服。"),
    E(655, "planta", "名词", "植物", "As plantas precisam de água.", "植物需要水。"),
    E(656, "animal", "名词", "动物", "Os animais vivem livres na reserva.", "动物们在保护区里自由生活。"),
    E(657, "pássaro", "名词", "鸟", "Os pássaros cantam de manhã.", "鸟儿清晨歌唱。"),
    E(658, "sol", "名词", "太阳", "O sol vai brilhar o fim de semana todo.", "整个周末都会出太阳。"),
    E(659, "lua", "名词", "月亮", "A lua está cheia hoje.", "今晚的月亮很圆。"),
    E(660, "estrela", "名词", "星星", "No campo dá para ver muitas estrelas.", "在乡下能看到很多星星。"),
    E(661, "céu", "名词", "天空", "O céu está limpo e azul.", "天空晴朗湛蓝。"),
    E(662, "nuvem", "名词", "云", "As nuvens indicam chuva.", "这些云预示着要下雨。"),
    E(663, "chuva", "名词", "雨", "A chuva vai começar à tarde.", "雨下午开始下。"),
    E(664, "tempestade", "名词", "暴风雨", "A tempestade vem do mar.", "暴风雨从海上而来。"),
    E(665, "vento", "名词", "风", "O vento derrubou a árvore.", "大风刮倒了树。"),
    E(666, "neve", "名词", "雪", "No sul do Brasil às vezes neva.", "巴西南部有时会下雪。"),
    E(667, "pôr do sol", "名词词组", "日落", "O pôr do sol na praia é lindo.", "海滩的日落很美。"),
    E(668, "clima", "名词", "气候", "O clima da serra é perfeito.", "山区的气候很舒服。"),
    E(669, "temperatura", "名词", "气温", "A temperatura vai cair amanhã.", "明天气温会下降。"),
    E(670, "grau", "名词", "度（温度）", "Hoje faz trinta graus.", "今天三十度。"),
    E(671, "calor", "名词", "热", "O calor vai até março.", "炎热的天气会持续到三月。"),
    E(672, "previsão", "名词", "预报", "A previsão do tempo indica sol.", "天气预报说是晴天。"),
    E(673, "verão", "名词", "夏天", "No verão as praias ficam cheias.", "夏天海滩上人很多。"),
    E(674, "inverno", "名词", "冬天", "No inverno faz frio na serra.", "冬天山区很冷。"),
    E(675, "primavera", "名词", "春天", "A primavera começa em setembro.", "春天九月开始。"),
    E(676, "outono", "名词", "秋天", "No outono as folhas caem.", "秋天树叶落下。"),
    E(677, "rede", "名词", "吊床 / 网络 / 网", "Vou descansar na rede.", "我要在吊床上休息。", "西语 red=网/网络；葡语 rede 还指'吊床'（西语是 hamaca）"),
    E(678, "logo", "副词", "马上 / 回头", "Eu ligo logo para você.", "我马上给你打电话。", "西语 luego=稍后/然后；葡语 logo=马上，比 luego 更'立刻'"),
    E(679, "futuro", "名词", "未来", "O futuro da empresa é promissor.", "公司的未来很有前景。"),
    E(680, "plano", "名词", "计划", "O plano é viajar em dezembro.", "计划是十二月去旅行。"),
    E(681, "planejar", "动词", "计划 / 规划", "Nós planejamos a viagem juntos.", "我们一起规划旅行。", None, "planejar"),
    E(682, "organizar", "动词", "组织 / 安排", "Ela organizou tudo em uma semana.", "她一周内安排好了一切。", None, "organizar"),
    E(683, "arrumar", "动词", "收拾 / 整理", "Eu arrumo a mala hoje à noite.", "我今晚收拾行李。", None, "arrumar"),
    E(684, "reservar", "动词", "预订", "Já reservei o hotel.", "我已经订好了酒店。", None, "reservar"),
    E(685, "confirmar", "动词", "确认", "Confirma o voo amanhã.", "明天确认一下航班。", None, "confirmar"),
    E(686, "cancelar", "动词", "取消", "Eles cancelaram o passeio.", "他们取消了游览。", None, "cancelar"),
    E(687, "adiar", "动词", "推迟", "A viagem foi adiada para julho.", "旅行推迟到七月了。", None, "adiar"),
    E(688, "embarcar", "动词", "登机 / 上船", "Nós embarcamos às oito.", "我们八点登机。", None, "embarcar"),
    E(689, "voar", "动词", "飞", "O avião voa sobre o mar.", "飞机飞过大海。", None, "voar"),
    E(690, "pousar", "动词", "降落", "O avião pousa às nove.", "飞机九点降落。", None, "pousar"),
    E(691, "decolar", "动词", "起飞", "O avião decola em dez minutos.", "飞机十分钟后起飞。", None, "decolar"),
    E(692, "nadar", "动词", "游泳", "Nós nadamos no mar todo dia.", "我们每天在海里游泳。", None, "nadar"),
    E(693, "caminhar", "动词", "徒步 / 走路", "Vamos caminhar até a cachoeira.", "我们要徒步走到瀑布。", None, "caminhar"),
    E(694, "relaxar", "动词", "放松", "Na praia eu só relaxo.", "在海滩我只放松。", None, "relaxar"),
    E(695, "aproveitar", "动词", "享受 / 利用", "Aproveita o feriado!", "好好享受假期吧！", None, "aproveitar"),
    E(696, "prever", "动词", "预测 / 预见", "O instituto prevê chuva para amanhã.", "气象部门预计明天有雨。", None, "prever"),
    E(697, "prometer", "动词", "答应", "Eu prometo que vou visitar você.", "我答应你会去看你。", None, "prometer"),
    E(698, "gastar", "动词", "花费 / 花钱", "Eu gasto pouco nas viagens.", "我旅行花钱不多。", None, "gastar"),
    E(699, "trocar", "动词", "换 / 兑换 / 交换", "Preciso trocar dólares por reais.", "我得把美元换成雷亚尔。", "西语 trocar=以物易物（少用）；葡语 trocar=换/兑换（高频）；西语'换钱'是 cambiar", "trocar"),
    E(700, "alugar", "动词", "租", "Vamos alugar um carro na viagem.", "旅行中我们要租一辆车。", None, "alugar"),
]

# ---- W8（虚拟式观点周）：情感/观点/心理/抽象/人际 ----
W8 = [
    E(701, "sentimento", "名词", "感情", "O amor é um sentimento forte.", "爱是一种强烈的感情。"),
    E(702, "emoção", "名词", "情绪 / 激动", "A emoção do jogo foi grande.", "比赛令人非常激动。"),
    E(703, "amor", "名词", "爱", "O amor de mãe é único.", "母爱是独一无二的。"),
    E(704, "alegria", "名词", "喜悦", "A notícia trouxe muita alegria.", "这条消息带来了巨大的喜悦。"),
    E(705, "tristeza", "名词", "悲伤", "A tristeza passou com o tempo.", "悲伤随时间消散了。"),
    E(706, "raiva", "名词", "愤怒", "Ele falou com raiva.", "他愤怒地说。"),
    E(707, "ciúme", "名词", "嫉妒 / 吃醋", "O ciúme estraga relações.", "嫉妒会毁掉关系。"),
    E(708, "inveja", "名词", "羡慕 / 嫉妒", "A inveja é um sentimento ruim.", "嫉妒是一种糟糕的情绪。"),
    E(709, "orgulho", "名词", "骄傲 / 自豪", "Os pais sentem orgulho do filho.", "父母为儿子感到骄傲。"),
    E(710, "vergonha", "名词", "羞愧", "Ele sentiu vergonha do erro.", "他为自己的错误感到羞愧。"),
    E(711, "saudade", "名词", "思念（葡语特有词，西语无对应）", "Eu sinto saudade da minha família.", "我想念我的家人。"),
    E(712, "medo", "名词", "恐惧", "O medo do escuro é comum.", "怕黑很常见。"),
    E(713, "esperança", "名词", "希望", "A esperança é a última que morre.", "希望是最后消逝的（谚语）。"),
    E(714, "ansiedade", "名词", "焦虑", "A ansiedade atrapalha o sono.", "焦虑影响睡眠。"),
    E(715, "estresse", "名词", "压力", "O estresse do trabalho é grande.", "工作压力很大。"),
    E(716, "calma", "名词", "平静", "A calma do mar é bonita.", "海面的平静很美。"),
    E(717, "felicidade", "名词", "幸福", "Desejo muita felicidade para você.", "祝你幸福满满。"),
    E(718, "sofrimento", "名词", "痛苦", "O sofrimento passou.", "痛苦过去了。"),
    E(719, "prazer", "名词", "快乐 / 荣幸", "É um prazer conhecer você.", "很荣幸认识你。"),
    E(720, "dor", "名词", "疼痛 / 痛苦", "A dor de cabeça passou.", "头痛好了。"),
    E(721, "coragem", "名词", "勇气", "É preciso coragem para mudar.", "改变需要勇气。"),
    E(722, "paciência", "名词", "耐心", "Ensinar exige paciência.", "教书需要耐心。"),
    E(723, "confiança", "名词", "信任", "A confiança leva tempo.", "信任需要时间。"),
    E(724, "ideia", "名词", "想法 / 主意", "A ideia dela é ótima.", "她的主意很棒。"),
    E(725, "opinião", "名词", "观点", "Na minha opinião, ele tem razão.", "在我看来，他是对的。"),
    E(726, "pensamento", "名词", "思想 / 想法", "O pensamento dele mudou.", "他的想法变了。"),
    E(727, "mente", "名词", "头脑 / 心智", "A mente humana é complexa.", "人类的心智很复杂。"),
    E(728, "cabeça", "名词", "头 / 头脑", "Eu tenho dor de cabeça.", "我头疼。"),
    E(729, "coração", "名词", "心 / 心脏", "O coração bate forte.", "心跳得很快。"),
    E(730, "bravo", "形容词", "生气的", "Fica bravo comigo não!", "别生我的气！", "西语 bravo=凶猛的/野的（toro bravo）；西语'生气'是 enfadado/enojado"),
    E(731, "imaginação", "名词", "想象力", "A imaginação das crianças é incrível.", "孩子们的想象力惊人。"),
    E(732, "desejo", "名词", "愿望", "O desejo de viajar cresce.", "想旅行的愿望越来越强烈。"),
    E(733, "vontade", "名词", "意愿 / 念头", "Eu tenho vontade de chorar.", "我想哭。"),
    E(734, "intenção", "名词", "意图", "A intenção dele era boa.", "他的本意是好的。"),
    E(735, "dúvida", "名词", "疑问", "Tenho uma dúvida sobre o texto.", "我对这段文字有个疑问。"),
    E(736, "certeza", "名词", "确信", "Tenho certeza de que ele vem.", "我确信他会来。"),
    E(737, "verdade", "名词", "真相 / 事实", "É verdade que ele saiu?", "他走了是真的吗？"),
    E(738, "mentira", "名词", "谎言", "A mentira tem perna curta.", "谎言腿短（谚语：谎言站不住脚）。"),
    E(739, "segredo", "名词", "秘密", "O segredo foi revelado.", "秘密被揭开了。"),
    E(740, "mistério", "名词", "谜团", "O caso continua um mistério.", "这个案子仍是个谜。"),
    E(741, "surpresa", "名词", "惊喜 / 惊讶", "A festa foi uma surpresa.", "这个聚会是个惊喜。"),
    E(742, "realidade", "名词", "现实", "A realidade é diferente do sonho.", "现实与梦想不同。"),
    E(743, "experiência", "名词", "经验 / 经历", "A experiência dele conta muito.", "他的经验很重要。"),
    E(744, "conhecimento", "名词", "知识", "O conhecimento liberta.", "知识让人自由。"),
    E(745, "inteligência", "名词", "智力 / 智能", "A inteligência artificial avança.", "人工智能在进步。"),
    E(746, "talento", "名词", "天赋", "Ela tem talento para a música.", "她有音乐天赋。"),
    E(747, "jeito", "名词", "方式 / 窍门（西语无对应词）", "Dá um jeito nisso!", "想办法搞定这事！"),
    E(748, "maneira", "名词", "方式 / 样子", "Que maneira linda de falar!", "多么美好的表达方式！"),
    E(749, "gracioso", "形容词", "优雅的 / 雅致的", "A dança dela é graciosa.", "她的舞姿很优雅。", "西语 gracioso=滑稽有趣的；葡语'有趣的'是 engraçado"),
    E(750, "sociedade", "名词", "社会", "A sociedade muda rápido.", "社会变化很快。"),
    E(751, "relação", "名词", "关系", "A relação entre os países melhorou.", "两国关系改善了。"),
    E(752, "amizade", "名词", "友谊", "A amizade verdadeira é rara.", "真正的友谊很稀有。"),
    E(753, "namoro", "名词", "恋爱关系", "O namoro deles começou na escola.", "他们的恋爱始于校园。"),
    E(754, "parceiro", "名词", "伙伴", "Ele é um bom parceiro de trabalho.", "他是个好搭档。"),
    E(755, "colega", "名词", "同事 / 同学", "A minha colega discorda de mim.", "我的同事不同意我。"),
    E(756, "vizinho", "名词", "邻居", "O vizinho faz muito barulho.", "邻居很吵。"),
    E(757, "cultura", "名词", "文化", "A cultura brasileira é rica.", "巴西文化很丰富。"),
    E(758, "tradição", "名词", "传统", "É tradição da família.", "这是家里的传统。"),
    E(759, "costume", "名词", "习惯 / 习俗", "É costume comer tarde aqui.", "这里习惯晚吃饭。"),
    E(760, "religião", "名词", "宗教", "A religião é importante para ele.", "宗教对他很重要。"),
    E(761, "fé", "名词", "信仰", "A fé ajuda nos momentos difíceis.", "信仰帮助人度过困难时刻。"),
    E(762, "Deus", "名词", "上帝", "Graças a Deus!", "谢天谢地！"),
    E(763, "arte", "名词", "艺术", "A arte moderna é difícil.", "现代艺术很难懂。"),
    E(764, "cinema", "名词", "电影院 / 电影", "Vamos ao cinema sábado?", "周六我们去看电影吗？"),
    E(765, "romance", "名词", "长篇小说", "O romance vendeu um milhão de cópias.", "这部小说卖出了一百万册。", "西语 romance=叙事诗/罗曼史；西语'长篇小说'是 novela"),
    E(766, "crítica", "名词", "评论 / 批评", "A crítica do filme foi boa.", "这部电影的影评不错。"),
    E(767, "comentário", "名词", "评论", "Os comentários no site foram duros.", "网站上的评论很尖锐。"),
    E(768, "debate", "名词", "辩论", "O debate foi transmitido ao vivo.", "辩论进行了现场直播。"),
    E(769, "sugestão", "名词", "建议", "Aceito a sua sugestão.", "我接受你的建议。"),
    E(770, "conselho", "名词", "忠告", "O conselho do avô sempre ajuda.", "爷爷的忠告总是有用。"),
    E(771, "ponto de vista", "名词词组", "观点", "Do meu ponto de vista, está errado.", "从我的观点看，这是错的。"),
    E(772, "razão", "名词", "理由 / 道理", "Você tem razão.", "你说得对。"),
    E(773, "motivo", "名词", "动机 / 原因", "O motivo da festa é o aniversário.", "聚会的原因是生日。"),
    E(774, "sentido", "名词", "意义 / 感觉", "Essa palavra tem outro sentido.", "这个词有别的意思。"),
    E(775, "influência", "名词", "影响", "A influência da mídia é grande.", "媒体的影响很大。"),
    E(776, "liberdade", "名词", "自由", "A liberdade tem preço.", "自由是有代价的。"),
    E(777, "respeito", "名词", "尊重", "O respeito vem em primeiro lugar.", "尊重是第一位的。"),
    E(778, "preconceito", "名词", "偏见", "O preconceito ainda existe.", "偏见依然存在。"),
    E(779, "erro", "名词", "错误", "Admitir o erro é difícil.", "承认错误很难。"),
    E(780, "amar", "动词", "爱", "Eu te amo.", "我爱你。", None, "amar"),
    E(781, "desejar", "动词", "祝愿 / 渴望", "Desejo tudo de bom para você.", "祝你一切顺利。", None, "desejar"),
    E(782, "duvidar", "动词", "怀疑", "Eu duvido que ele venha.", "我怀疑他会来。", None, "duvidar"),
    E(783, "temer", "动词", "害怕 / 担心", "Eu temo que chova amanhã.", "我担心明天会下雨。", None, "temer"),
    E(784, "imaginar", "动词", "想象", "Imagina só a surpresa dele!", "想象一下他会有多惊喜！", None, "imaginar"),
    E(785, "supor", "动词", "猜想", "Suponho que você tem razão.", "我想你是对的。", None, "supor"),
    E(786, "sugerir", "动词", "建议", "Sugiro que você descanse.", "我建议你休息。", None, "sugerir"),
    E(787, "exigir", "动词", "要求", "O chefe exige pontualidade.", "老板要求准时。", None, "exigir"),
    E(788, "lamentar", "动词", "遗憾 / 惋惜", "Lamento que você não possa vir.", "很遗憾你不能来。", None, "lamentar"),
    E(789, "confiar", "动词", "信任", "Eu confio em você.", "我信任你。", None, "confiar"),
    E(790, "aceitar", "动词", "接受", "Aceito as condições.", "我接受这些条件。", None, "aceitar"),
    E(791, "recusar", "动词", "拒绝", "Ele recusou o convite.", "他拒绝了邀请。", None, "recusar"),
    E(792, "proibir", "动词", "禁止", "É proibido fumar aqui.", "这里禁止吸烟。", None, "proibir"),
    E(793, "aconselhar", "动词", "劝告", "Eu aconselho você a estudar mais.", "我劝你多学习。", None, "aconselhar"),
    E(794, "elogiar", "动词", "表扬", "O professor elogiou o aluno.", "老师表扬了学生。", None, "elogiar"),
    E(795, "perdoar", "动词", "原谅", "Eu perdoo você.", "我原谅你。", None, "perdoar"),
    E(796, "agradecer", "动词", "感谢", "Agradeço pela ajuda.", "感谢你的帮助。", None, "agradecer"),
    E(797, "mentir", "动词", "说谎", "Não minta para mim!", "别对我说谎！", None, "mentir"),
    E(798, "concordar", "动词", "同意", "Concordo com você.", "我同意你。", None, "concordar"),
    E(799, "insistir", "动词", "坚持", "Ele insiste na ideia.", "他坚持这个想法。", None, "insistir"),
    E(800, "reconhecer", "动词", "承认 / 认出", "Reconheço que errei.", "我承认我错了。", None, "reconhecer"),
]


# ============ vocabulary.json 精选（每周 22 个，优先假朋友与西语差异词）============
# (pt, zh, es, week, falseFriend)
V = lambda pt, zh, es, week, ff=None: (pt, zh, es, week, ff)

VOCAB_W5 = [
    V("ontem", "昨天", "ayer", 5),
    V("anteontem", "前天", "anteayer", 5),
    V("fim de semana", "周末", "fin de semana", 5),
    V("semana passada", "上周", "la semana pasada", 5),
    V("aniversário", "生日", "cumpleaños", 5),
    V("sábado", "星期六", "sábado", 5),
    V("janeiro", "一月", "enero", 5),
    V("mil", "一千", "mil", 5),
    V("marido", "丈夫", "marido / esposo", 5),
    V("esposa", "妻子", "esposa", 5, "西语 esposa=妻子（同义），但复数 esposas=手铐！葡语'手铐'是 algemas"),
    V("avó", "祖母 / 外婆", "abuela", 5),
    V("primo", "堂 / 表兄弟", "primo", 5),
    V("criança", "孩子", "niño", 5, "西语'孩子'是 niño；crianza 在西语=养育（名词）"),
    V("casamento", "婚礼", "boda / casamiento", 5),
    V("churrasco", "巴西烤肉", "asado / parrillada", 5),
    V("história", "故事 / 历史", "historia", 5),
    V("rato", "老鼠", "ratón", 5, "西语 rato=片刻；葡语'片刻'是 momento"),
    V("presente", "礼物", "regalo", 5, "西语'礼物'是 regalo；presente 在西语=出席的/现在（时态）"),
    V("assistir", "观看 / 出席", "ver / asistir a", 5, "西语 asistir=参加/出席；葡语 assistir(a)=观看；'参加'用 participar"),
    V("ligar", "打电话 / 打开（电器）", "llamar / encender", 5, "西语 ligar=绑/调情；葡语'绑'是 amarrar"),
    V("nascer", "出生", "nacer", 5),
    V("pôr", "放 / 摆", "poner", 5),
]

VOCAB_W6 = [
    V("governo", "政府", "gobierno", 6),
    V("política", "政治 / 政策", "política", 6),
    V("eleição", "选举", "elección", 6),
    V("lei", "法律", "ley", 6),
    V("direito", "权利 / 法学", "derecho", 6),
    V("ladrão", "小偷", "ladrón", 6),
    V("crime", "犯罪", "crimen / delito", 6),
    V("segurança", "安全", "seguridad", 6),
    V("acidente", "事故", "accidente", 6),
    V("bairro", "街区", "barrio", 6),
    V("economia", "经济", "economía", 6),
    V("crise", "危机", "crisis", 6),
    V("salário", "工资", "salario / sueldo", 6),
    V("desemprego", "失业", "desempleo", 6),
    V("real", "雷亚尔 / 真实的", "real", 6, "巴西货币 real（复数 reais）；西语 real=真实的/皇家的"),
    V("propina", "贿赂（巴西）", "soborno", 6, "西语 propina=小费；巴西葡语 propina=贿赂；'小费'葡语是 gorjeta"),
    V("fato", "事实 / 西装", "hecho / traje", 6, "葡语 fato=事实，也=西装（=西语 traje）；西语'事实'是 hecho"),
    V("sucesso", "成功", "éxito", 6, "西语 suceso=事件（新闻常用）；葡语'事件'是 acontecimento；sucesso=成功"),
    V("atender", "接待 / 接听", "atender / contestar", 6, "西语 atender=注意/接待；'注意'葡语是 prestar atenção"),
    V("notícia", "新闻 / 消息", "noticia", 6),
    V("greve", "罢工", "huelga", 6),
    V("dever", "欠 / 应该", "deber", 6),
]

VOCAB_W7 = [
    V("viagem", "旅行", "viaje", 7),
    V("passaporte", "护照", "pasaporte", 7),
    V("mala", "行李箱", "maleta", 7, "西语'行李箱'是 maleta；mala 在西语是 malo 的阴性（坏的）"),
    V("pousada", "客栈 / 民宿", "posada", 7),
    V("aeroporto", "机场", "aeropuerto", 7),
    V("voo", "航班", "vuelo", 7),
    V("destino", "目的地", "destino", 7),
    V("estação", "车站 / 季节", "estación", 7),
    V("leste", "东方", "este（注意：西语 este→葡语 leste）", 7),
    V("mar", "大海", "mar", 7),
    V("pôr do sol", "日落", "puesta de sol", 7),
    V("tempestade", "暴风雨", "tormenta", 7),
    V("clima", "气候", "clima", 7),
    V("previsão", "预报", "pronóstico / previsión", 7),
    V("verão", "夏天", "verano", 7),
    V("rede", "吊床 / 网络", "hamaca / red", 7, "西语 red=网/网络；葡语 rede 还指'吊床'（西语 hamaca）"),
    V("logo", "马上 / 回头", "luego / pronto", 7, "西语 luego=稍后/然后；葡语 logo=马上，比 luego 更'立刻'"),
    V("trocar", "换 / 兑换", "cambiar", 7, "西语 trocar=以物易物（少用）；葡语 trocar=换（高频）；西语'换钱'是 cambiar"),
    V("planejar", "计划 / 规划", "planear / planificar", 7),
    V("aproveitar", "享受 / 利用", "aprovechar", 7),
    V("futuro", "未来", "futuro", 7),
    V("plano", "计划", "plan", 7),
]

VOCAB_W8 = [
    V("sentimento", "感情", "sentimiento", 8),
    V("saudade", "思念（葡语特有词）", "（西语无对应词）", 8),
    V("ideia", "想法", "idea", 8),
    V("opinião", "观点", "opinión", 8),
    V("dúvida", "疑问", "duda", 8),
    V("medo", "恐惧", "miedo", 8),
    V("esperança", "希望", "esperanza", 8),
    V("realidade", "现实", "realidad", 8),
    V("mentira", "谎言", "mentira", 8),
    V("jeito", "方式 / 窍门", "（西语无对应词；dar um jeito=想办法）", 8),
    V("sociedade", "社会", "sociedad", 8),
    V("amizade", "友谊", "amistad", 8),
    V("cultura", "文化", "cultura", 8),
    V("romance", "长篇小说", "novela", 8, "西语 romance=叙事诗/罗曼史；西语'长篇小说'是 novela"),
    V("gracioso", "优雅的", "elegante", 8, "西语 gracioso=滑稽有趣的；葡语'有趣的'是 engraçado"),
    V("bravo", "生气的", "enfadado / enojado", 8, "西语 bravo=凶猛的/野的；西语'生气'是 enfadado/enojado"),
    V("desejar", "祝愿 / 渴望", "desear", 8),
    V("supor", "猜想", "suponer", 8),
    V("sugerir", "建议", "sugerir", 8),
    V("exigir", "要求", "exigir", 8),
    V("lamentar", "遗憾", "lamentar", 8),
    V("mentir", "说谎", "mentir", 8),
]

# ============ 生成 entry（格式与 build_weekly_vocab.py 一致）============
PERSONS = ["eu", "tu", "ele/ela/você", "nós", "eles/elas/vocês"]

def build_entry(t):
    rank, pt, pos, zh, xpt, xzh, ff, vb = t
    e = {"rank": rank, "pt": pt, "pos": pos, "zh": zh,
         "example": {"pt": xpt, "zh": xzh}}
    if ff:
        e["falseFriend"] = ff
    if vb:
        meaning, vtype, es_inf, note = VERBS[vb]
        c = conj_pt(vb)
        conj = {p: c[i] for i, p in enumerate(PERSONS)}
        conj["es"] = es_line(es_inf) if es_inf else note.split("——")[0]
        e["conjugations"] = conj
    return e

def build_verb_row(vb):
    meaning, vtype, es_inf, note = VERBS[vb]
    c = conj_pt(vb)
    v = {
        "infinitive": vb,
        "meaning": meaning,
        "type": vtype,
        "conjugation": {p: c[i] for i, p in enumerate(PERSONS)},
        "spanish": es_line(es_inf) if es_inf else note.split("——")[0],
    }
    if note:
        v["note"] = note
    return v

# ============ 读取现有 JSON 并合并（只追加，绝不改动 w1-w4）============
freq_path = os.path.join(DATA, "frequency-vocab.json")
conj_path = os.path.join(DATA, "verb-conjugations.json")
vocab_path = os.path.join(DATA, "vocabulary.json")

freq = json.load(open(freq_path, encoding="utf-8"))
conj_doc = json.load(open(conj_path, encoding="utf-8"))
vocab = json.load(open(vocab_path, encoding="utf-8"))

# 快照 w1-w4，合并完成后断言未被改动
old_weeks = {k: copy.deepcopy(freq[k]) for k in ("w1", "w2", "w3", "w4")}

weeks_new = {"w5": W5, "w6": W6, "w7": W7, "w8": W8}
for wkey, wlist in weeks_new.items():
    assert len(wlist) == 100, f"{wkey} 词表不是 100 条: {len(wlist)}"
    freq[wkey] = [build_entry(t) for t in wlist]
freq["description"] = ("每周 100 个频率词汇（PT-BR）。W1=频率排名1-100，W2=101-200，W3=201-300，W4=301-400，"
                       "W5=401-500，W6=501-600，W7=601-700，W8=701-800。选词参考 Corpus do Português / "
                       "Routledge Frequency Dictionary 高频区（按教学需要微调）。动词附现在时完整变位与西语对照；"
                       "falseFriend 为西语假朋友警示。")

# 动词变位表：按 infinitive 去重追加
existing_infs = {v["infinitive"] for v in conj_doc["verbs"]}
new_verbs = []
for wlist in weeks_new.values():
    for t in wlist:
        vb = t[7]
        if vb and vb not in existing_infs:
            existing_infs.add(vb)
            new_verbs.append(build_verb_row(vb))
conj_doc["verbs"].extend(new_verbs)
conj_doc["description"] = "W1-W8 每周 100 频率词中全部动词的现在时变位表（PT-BR），含西语对照"

# 核心词汇表：按 (pt, week) 去重追加
existing_keys = {(e["pt"].lower(), e["week"]) for e in vocab["entries"]}
added_vocab = 0
for pt, zh, es, week, ff in VOCAB_W5 + VOCAB_W6 + VOCAB_W7 + VOCAB_W8:
    key = (pt.lower(), week)
    if key in existing_keys:
        continue
    existing_keys.add(key)
    entry = {"pt": pt, "zh": zh, "es": es, "week": week}
    if ff:
        entry["falseFriend"] = ff
    vocab["entries"].append(entry)
    added_vocab += 1
vocab["weeks"] = [1, 2, 3, 4, 5, 6, 7, 8]
vocab["description"] = "W1-W8 核心词汇表（巴西葡语），含假朋友标注。pt=葡语, zh=中文, es=西语对照, falseFriend=假朋友说明"

# w1-w4 未被改动
for k in ("w1", "w2", "w3", "w4"):
    assert freq[k] == old_weeks[k], f"{k} 被意外改动！"

# ============ 写回 ============
for path, doc in ((freq_path, freq), (conj_path, conj_doc), (vocab_path, vocab)):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"written: {path}")

# ============ 质量校验（重新读取写回的文件）============
freq2 = json.load(open(freq_path, encoding="utf-8"))
conj2 = json.load(open(conj_path, encoding="utf-8"))
vocab2 = json.load(open(vocab_path, encoding="utf-8"))

# 1. 四个新周各 100 条；rank 恰好覆盖 401-800 无重复无缺失
all_new_ranks = []
for i, wkey in enumerate(("w5", "w6", "w7", "w8")):
    entries = freq2[wkey]
    assert len(entries) == 100, f"{wkey} 应 100 条，实际 {len(entries)}"
    lo, hi = 401 + i * 100, 500 + i * 100
    assert sorted(e["rank"] for e in entries) == list(range(lo, hi + 1)), f"{wkey} rank 不连续"
    all_new_ranks.extend(e["rank"] for e in entries)
assert sorted(all_new_ranks) == list(range(401, 801)), "rank 401-800 有重复或缺失"

# 2. w5-w8 与 w1-w4 的 pt 无重复（统一 lower）
old_pts = {e["pt"].lower() for k in ("w1", "w2", "w3", "w4") for e in freq2[k]}
new_pts = [e["pt"].lower() for k in ("w5", "w6", "w7", "w8") for e in freq2[k]]
assert len(new_pts) == len(set(new_pts)) == 400, "w5-w8 内部有重复词"
dup = old_pts & set(new_pts)
assert not dup, f"与 w1-w4 重复的词: {dup}"

# 3. 所有动词条目的 conjugations 五人称非空且 es 非空
n_verbs = {}
for wkey in ("w5", "w6", "w7", "w8"):
    n_verbs[wkey] = 0
    for e in freq2[wkey]:
        if "conjugations" in e:
            n_verbs[wkey] += 1
            for p in PERSONS + ["es"]:
                assert e["conjugations"].get(p), f"{wkey} {e['pt']} 变位缺 {p}"

# 4. verb-conjugations.json 中 infinitive 无重复
infs = [v["infinitive"] for v in conj2["verbs"]]
assert len(infs) == len(set(infs)), "infinitive 有重复"
for v in conj2["verbs"]:
    for p in PERSONS:
        assert v["conjugation"].get(p), f"{v['infinitive']} 变位缺 {p}"
    assert v.get("spanish"), f"{v['infinitive']} 缺西语对照"

# 5. JSON 均可解析（上面已 json.load 三次）
print("\n===== 校验全部通过 =====")
print("frequency-vocab.json:", {k: len(freq2[k]) for k in ("w1","w2","w3","w4","w5","w6","w7","w8")})
print("新周动词数:", n_verbs, "合计", sum(n_verbs.values()))
ff_counts = {k: sum(1 for e in freq2[k] if "falseFriend" in e) for k in ("w5","w6","w7","w8")}
print("新周假朋友数:", ff_counts, "合计", sum(ff_counts.values()))
print("verb-conjugations.json: 新增", len(new_verbs), "，总数", len(conj2["verbs"]))
print("vocabulary.json: 新增", added_vocab, "，总数", len(vocab2["entries"]), "，weeks =", vocab2["weeks"])
