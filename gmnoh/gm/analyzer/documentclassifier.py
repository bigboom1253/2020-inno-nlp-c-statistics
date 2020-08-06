import numpy as np
import pandas as pd

class nbc():
    def __init__(self, content, all_cls, keywords, k = 0.5):
        self.content = content
        self.all_cls = all_cls
        self.k = k
        self.keywords = keywords
        self.cls = list(set(all_cls))

    def train(self):
        # class 분류
        self.cls_doc = []

        for i in self.cls:
            tmp = []
            for j in range(len(self.all_cls)):
                if self.all_cls[j] == i:
                    tmp.append(self.content[j])
            self.cls_doc.append(tmp)

        # class별 확률
        self.cls_prob = []

        for i in range(len(self.cls)):
            prob = np.log(len(self.cls_doc[i]) / len(self.all_cls))
            self.cls_prob.append(prob)

        # class별 토큰화
        self.cls_token = []

        for i in self.cls_doc:
            self.cls_token.append(" ".join(i).split())

        self.tokens = []

        for i in self.cls_token:
            self.tokens = set(self.tokens).union(set(i))
        self.tokens = list(self.tokens)

        # 각 class 단어별 log 확률
        self.cls_cnt = []

        for i in self.cls_token:
            self.cls_cnt.append([i.count(j) for j in self.tokens])

        self.cls_log = []

        for i in self.cls_cnt:
            self.cls_log.append([np.log((j+self.k)/(2*self.k+sum(i))) for j in i])

    def predict(self):
        # 각 class별 keyword 토큰이 들어있을 확률
        self.cls_prob_word = []

        for i in range(len(self.cls)):
            sum = 0
            for j in self.keywords:
                sum += self.cls_log[i][self.tokens.index(j)]
            self.cls_prob_word.append(np.exp(sum + self.cls_prob[i]))

        # keyword가 포함된 class일 확률
        self.cls_result = []

        sum = 0
        for i in self.cls_prob_word:
            sum += i

        for i in range(len(self.cls)):
            self.cls_result.append(self.cls_prob_word[i] / sum)

    def get_prob(self):
        self.train()
        self.predict()
        
        return dict(zip(self.cls, self.cls_result))