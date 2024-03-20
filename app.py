import streamlit as st

from stella_fortune import Stella

stl = Stella()

### ページ設定
st.set_page_config(
    page_title="ステラちゃん占い",
    page_icon="🔮",
    layout="centered"
)

st.title('ステラちゃん占い')
st.subheader('出身地×血液型×星座 = 2,256通りの占い')

tab1, tab2 = st.tabs(["ランキング", "検索"])

with tab1:
    st.write(f"今日の運勢ランキング")

    rank_table = stl.get_rank_table()
    for i, (p, b, z) in enumerate(rank_table[:10]):
        st.write(f"{i+1}位  {p} x {b} x {z}")

with tab2:
    # デフォルト値
    ip = st.session_state.get('pref', None)
    ib = st.session_state.get('bloodtype', None)
    iz = st.session_state.get('zodiac', None)

    # 入力
    pref = st.selectbox('出身地:', stl.pref_list, index=ip)
    bloodtype = st.selectbox('血液型:', stl.bloodtype_list, index=ib)
    zodiac = st.selectbox('星座:', stl.zodiac_list, index=iz)

    if pref and bloodtype and zodiac:
        # 入力の保存
        st.session_state['pref'] = stl.pref_list.index(pref)
        st.session_state['bloodtype'] = stl.bloodtype_list.index(bloodtype)
        st.session_state['zodiac'] = stl.zodiac_list.index(zodiac)

        # 表示
        rank = stl.get_rank(pref, bloodtype, zodiac)
        st.write(f"今日の {pref} x {bloodtype} x {zodiac} の運勢")
        st.write(f"{rank:,} / 2,256 位")


