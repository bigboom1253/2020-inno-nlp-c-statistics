import re
from nltk.tokenize import sent_tokenize
from konlpy.tag import Kkma
from konlpy.tag import Okt

class LuhnSummarize:
    def __init__(self, text):
        self.text = text
        self.keyword_lst = []

    # 키워드 추출
    def keyword(self, minimum=0.005, maximum=0.5):
        okt = Okt()
        okt_tokens = okt.morphs(self.text)
        # 중복 제거하여 개별 단어 세트 만들기
        word_type = set(okt_tokens)
        freq_dic = {}
        # 각 단어 빈도 딕셔너리에 저장
        for x in word_type:
            if re.search('[0-9가-힣a-zA-z]', x):
                freq_dic[x] = okt_tokens.count(x)

        # 개별 단어 빈도 / 총 빈도 기준으로 키워드 추출
        total = sum(freq_dic.values())
        keyword_lst = []
        for word, freq in freq_dic.items():
            if minimum < freq/total < maximum:    
                keyword_lst.append(word)
        self.keyword_lst = keyword_lst
        print('{}개 유형 단어 중에서 {}개 단어를 키워드로 추출하였습니다.'.format(len(word_type), len(keyword_lst)))
        return keyword_lst


    # 문장 중요도 계산
    def keysentence(self, sent_num = 3):
        okt = Okt()
        # 개별 문장 리스트
        sent_lst = sent_tokenize(self.text)
        sent_lst = [x.strip() for x in sent_lst]
        # 문장 중요도 계산
        sent_sig_dic = {}
        for x in sent_lst:
            # 문장이 비어있으면 제외하고 실행
            if x:
                sent_tokens = okt.morphs(x)
                s_kw_dic = {}
                for idx, token in enumerate(sent_tokens):
                    if token in self.keyword_lst:
                        s_kw_dic[token] = idx
                start = min(s_kw_dic.values())    # 윈도우 시작
                end = max(s_kw_dic.values())  # 윈도우 끝
                word_num = end-start+1
                kw_num = len(s_kw_dic)
                sent_sig = kw_num**2/word_num
                sent_sig_dic[x] = sent_sig
        sent_sig_lst = list(sent_sig_dic.items())
        sent_sig_lst.sort(key=lambda x: x[1], reverse=True)
        for idx, x in enumerate(sent_sig_lst[:sent_num]):
            print(idx+1, x[0])