import json
from collections import Counter
files = ['exercises/w05-quiz.json','exercises/w06-quiz.json','exercises/w07-quiz.json','exercises/w08-quiz.json',
         'data/frequency-vocab.json','data/curriculum.json','data/vocabulary.json','data/verb-conjugations.json']
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    print('OK', f)
print()
for n in [5,6,7,8]:
    d = json.load(open(f'exercises/w0{n}-quiz.json', encoding='utf-8'))
    qs = d['questions']
    c = Counter(q['type'] for q in qs)
    sc = c['single_choice']
    total = len(qs)
    auto = total - sum(1 for q in qs if q.get('aiGraded'))
    vocab = [q for q in qs if '_vocab_' in q['id']]
    ai = [q for q in qs if q.get('aiGraded')]
    dup = [q['id'] for q in qs if q['type']=='single_choice' and len(set(q['options']))!=len(q['options'])]
    badans = [q['id'] for q in qs if q['type']=='single_choice' and q['answer'] not in q['options']]
    ids = [q['id'] for q in qs]
    dupids = [i for i in set(ids) if ids.count(i)>1]
    print(f"w{n}: total={total} auto={auto} types={dict(c)} choice%={sc/total*100:.0f} vocab={len(vocab)} ai={len(ai)} dupOpt={dup} badAns={badans} dupIds={dupids}")
