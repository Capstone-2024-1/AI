from konlpy.tag import Kkma
import jpype
jpype.startJVM(jpype.getDefaultJVMPath(), '-Xmx4096m')

# 텍스트 파일 읽기
read = open('Embedding/output.txt', 'r', encoding='utf-8')
text = read.read()
read.close()

# 형태소 분석
kkma = Kkma()
sentences = kkma.sentences(text)
for idx, sentence in enumerate(sentences):
    sentences[idx] = kkma.morphs(sentence)

# 결과를 파일로 저장
with open('morphs_output.txt', 'w', encoding='utf-8') as f:
    for morphs in sentences:
        f.write(' '.join(morphs) + '\n')
