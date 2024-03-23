import random
from itertools import product
from datetime import datetime, timedelta, timezone

# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')

class Stella:

    pref_list = [
        '北海道','青森','岩手','宮城','秋田','山形','福島','茨城',
        '栃木','群馬','埼玉','千葉','東京','神奈川','新潟','富山',
        '石川','福井','山梨','長野','岐阜','静岡','愛知','三重',
        '滋賀','京都','大阪','兵庫','奈良','和歌山','鳥取','島根',
        '岡山','広島','山口','徳島','香川','愛媛','高知','福岡',
        '佐賀','長崎','熊本','大分','宮崎','鹿児島','沖縄',
    ]
    bloodtype_list = ['A型', 'B型', 'O型', 'AB型']
    zodiac_list = [
        'おひつじ座','おうし座','ふたご座','かに座','しし座','おとめ座',
        'てんびん座','さそり座','いて座','やぎ座','みずがめ座','うお座',
    ]


    def get_rank(self, pref, bloodtype, zodiac, date=None):
        assert pref in self.pref_list
        assert bloodtype in self.bloodtype_list
        assert zodiac in self.zodiac_list

        rank_table = self.get_rank_table(date)
        rank = rank_table.index((pref, bloodtype, zodiac)) + 1

        return rank


    def get_rank_table(self, date=None):
        # 日ごとの運勢のため、日付8桁表記を乱数のシードとする
        if date is None:
            date = datetime.now(JST)
        seed = date.strftime('%Y%m%d')
        random.seed(seed)

        rank_list = list(product(self.pref_list, self.bloodtype_list, self.zodiac_list))
        random.shuffle(rank_list)
        return rank_list


if __name__ == "__main__":
    stl = Stella()
    print(stl.get_rank_table()[:3])

    (pref, bloodtype, zodiac) = ('北海道','A型','おひつじ座')
    rank = stl.get_rank(pref, bloodtype, zodiac)
    print(f'{pref:<3} {bloodtype:>3} {zodiac:>5} {rank:,d} / 2,304 位')
