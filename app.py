import streamlit as st
import extra_streamlit_components as stx
from streamlit_extras.annotated_text import annotated_text

from stella_fortune import Stella
stl = Stella()


@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()


def show_annotated_text(prefix, pref, bloodtype, zodiac, suffix):
    annotated_text(
        prefix,
        (pref, "", '#ffad60'),
        " x ",
        (bloodtype, "", '#d9534f'),
        " x ",
        (zodiac, "", '#96ceb4'),
        suffix,
    )


### ページ設定
st.set_page_config(
    page_title="ステラちゃん占い",
    page_icon="🔮",
    layout="centered"
)

st.header('🔮ステラちゃん占い')
show_annotated_text('', '出身地', '血液型', '星座', ' = 2,256通りの占い')

tab1, tab2 = st.tabs(["ランキング", "検索"])

# ランキング
with tab1:
    st.write(f"今日の運勢ランキング")

    rank_table = stl.get_rank_table()
    for i, (p, b, z) in enumerate(rank_table[:20]):
        show_annotated_text(f"　{i+1:>2d}位 ", p, b, z, '')

# 検索
with tab2:
    # デフォルト値
    cookie_manager = get_manager()
    try:
        ip = stl.pref_list.index(cookie_manager.get(cookie='pref'))
        ib = stl.bloodtype_list.index(cookie_manager.get(cookie='bloodtype'))
        iz = stl.zodiac_list.index(cookie_manager.get(cookie='zodiac'))
    except:
        ip, ib, iz = [None] * 3

    # 入力
    pref = st.selectbox('出身地:', stl.pref_list, index=ip)
    bloodtype = st.selectbox('血液型:', stl.bloodtype_list, index=ib)
    zodiac = st.selectbox('星座:', stl.zodiac_list, index=iz)

    if pref and bloodtype and zodiac:
        # 入力の保存
        cookie_manager.set('pref', pref, max_age=14*24*60*60, key=0)
        cookie_manager.set('bloodtype', bloodtype, max_age=14*24*60*60, key=1)
        cookie_manager.set('zodiac', zodiac, max_age=14*24*60*60, key=2)

        # 表示
        rank = stl.get_rank(pref, bloodtype, zodiac)
        show_annotated_text(f"今日の ", pref, bloodtype, zodiac, ' の運勢')
        st.metric('2,256 位中', f"{rank:,} 位")


