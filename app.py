from datetime import datetime, timedelta, timezone
import math

import streamlit as st
import extra_streamlit_components as stx
from annotated_text import annotated_text, util

import const
from stella_fortune import Stella
stl = Stella()


@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()


@st.cache_data
def get_rank_table(date):
    return stl.get_rank_table(date)


# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')
date = datetime.now(JST)
rank_table = stl.get_rank_table(date)


def get_rank(pref, bloodtype, zodiac):
    rank = rank_table.index((pref, bloodtype, zodiac)) + 1
    return rank


def show_annotated_text(prefix, pref, bloodtype, zodiac, suffix, *, place_holder=None):
    args = (
        prefix,
        (pref, "", '#428D5F'),
        " x ",
        (bloodtype, "", '#A95450'),
        " x ",
        (zodiac, "", '#A99A50'),
        suffix,
    )
    if place_holder:
        place_holder.markdown(
            util.get_annotated_html(*args),
            unsafe_allow_html=True,
        )
    else:
        annotated_text(*args)


### ページ設定
st.set_page_config(
    page_title="ステラちゃん占い",
    page_icon="🔮",
    layout="centered"
)
st.markdown(const.HIDE_ST_STYLE, unsafe_allow_html=True)

st.header('🔮ステラちゃん占い')
show_annotated_text('', '出身地', '血液型', '星座', ' = 2256通りの占い')

tab1, tab2 = st.tabs(["検索", "ランキング"])

# 検索
with tab1:
    # 表示用プレースホルダー
    place_holder_1 = st.empty()
    place_holder_2 = st.empty()

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
        rank = get_rank(pref, bloodtype, zodiac)
        show_annotated_text(f"今日の ", pref, bloodtype, zodiac, ' の運勢', place_holder=place_holder_1)
        place_holder_2.metric('2256 位中', f"{rank} 位")
        if rank <= 10:
            st.balloons()

# ランキング
with tab2:
    st.write(f"{date.strftime('%Y.%m.%d')} の運勢")

    rows_per_page = 20
    total_pages = math.ceil(len(rank_table) / rows_per_page)

    # ランキング表示
    if 'page' not in st.session_state:
        st.session_state['page'] = 1

    l = (st.session_state['page'] - 1) * rows_per_page
    r = min(l + rows_per_page, len(rank_table))
    for i, (p, b, z) in enumerate(rank_table[l:r]):
        show_annotated_text(f"　{l+i+1:>2d}位 ", p, b, z, '')

    # pagination
    cols = st.columns([1, 1, 3, 1, 1], gap='small')

    # ページ数の増減ボタン
    with cols[1]:
        def minus_one_page():
            st.session_state['page'] -= 1
        if st.session_state['page'] > 1:
            st.button(label='＜', on_click=minus_one_page)

    with cols[3]:
        def plus_one_page():
            st.session_state['page'] += 1
        if st.session_state['page'] < total_pages:
            st.button(label='＞', on_click=plus_one_page)

    # ページ数の増減ボタン
    with cols[0]:
        def first_page():
            st.session_state['page'] = 1
        if st.session_state['page'] > 1:
            st.button(label='≪', on_click=first_page)

    with cols[4]:
        def last_page():
            st.session_state['page'] = total_pages
        if st.session_state['page'] < total_pages:
            st.button(label='≫', on_click=last_page)

    # 現在のページ番号
    with cols[2]:
        st.write(f"{l+1} - {r}位 / {len(rank_table)}位")
