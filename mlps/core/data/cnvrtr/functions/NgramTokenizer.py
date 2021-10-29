# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract
import re
import urllib.parse as decode


class NgramTokenizer(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_len = int(self.arg_list[0])

    def apply(self, data):
        try:
            dec_data = decode.unquote(data)
        except:
            dec_data = data

        temp = dec_data.replace('#CRLF#','').replace(' ','') # CRLF가 붙어 올 경우 삭제
        lpFind = set(re.findall(r'\W', temp))  # 정규화를 통한 특수문자 검색
        for token in lpFind:  # 찾은 특수문자를 치환 해서 토크나이징 하는곳
            temp = temp.replace(str(token), ' ' + str(token) + ' ').replace("  ", " ")

        return self.ngram(temp, int(self.arg_list[1]), int(self.arg_list[2]))

        # 0 : 음절 n-gram 분석
        # 1 : 어절 n-gram 분석
        # sentence: 분석할 문장, num_gram: n-gram 단위
        # N gram
        # param : sentence, N gram number, phoneme or word

    def ngram(self, sentence, num_gram, arg2):
        max_len = self.max_len
        text = None

        if arg2 == 0:  # 음절 phoneme
            text = list(sentence)  # split the sentence into an array of characters
        elif arg2 == 1:  # Word 어절
            sentence = sentence.replace('\n', ' ').replace('\r', ' ')
            text = list(sentence.split(' '))

        ngrams = [text[x:x + num_gram] for x in range(0, len(text))]

        lpFirst = ngrams[:len(ngrams) - (num_gram - 1)]  # 전체 데이터에서 num gram 이 잘된 데이터
        lpSecend = ngrams[len(ngrams) - (num_gram - 1):]  # 전체 데이터에서 num gram 이 부족한 데이터 끝쪽

        for lpTemp in lpSecend:  # 부족한 데이터에 PADDING
            for ix in range(abs(num_gram - len(lpTemp))):  # 그램에 갯수에 맞을때까지
                lpTemp.append('#PADDING#')  # PADDING 으로 채움
            lpFirst.append(lpTemp)  # 그것을 잘된 데이터에 붙인다.

        result_len = len(ngrams)

        # padding
        if result_len < max_len:
            list_padding = list()
            list_padd = ['#PADDING#' for _ in range(num_gram)]
            padding = [list_padd for _ in range(max_len - result_len)]
            list_padding += padding
            ngrams += list_padding
        elif result_len > max_len:
            ngrams = ngrams[:self.max_len]

        return ngrams


if __name__ == "__main__":
    payload = "GET /shop/ProdSearch.php?Ccode1=0&Ccode2=2"
    # payload = "The quick brown / fox jumped over the lazy dog"
    # stat_dic[1] == 0 : 어절, 1 : 음절
    tokenizer = NgramTokenizer(stat_dict=None, arg_list=[30, 2, 1])
    print(tokenizer.apply(payload))
