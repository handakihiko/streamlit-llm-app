import os
import streamlit as st
from dotenv import load_dotenv

# ==== 環境変数ロード ====
load_dotenv()
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"  # 念のためOFF

# APIキーの取得（Cloudはst.secrets、ローカルは.env）
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))

# ==== LangChain ====
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ==== LLMチェーンを返す関数 ====
@st.cache_resource(show_spinner=False)
def get_chain(role: str):
    """
    role: 選択された専門家の種類に応じて system prompt を切り替える
    """

    if role == "経済学者":
        system_message = (
            "あなたは経済学の専門家です。マクロ経済・金融政策・産業動向に詳しく、"
            "専門用語をわかりやすく説明できます。"
        )
    elif role == "医師":
        system_message = (
            "あなたは臨床経験豊富な医師です。健康や病気の質問に対し、"
            "一般的な医学知識に基づいて正確で分かりやすい説明を行います。"
        )
    elif role == "エンジニア":
        system_message = (
            "あなたはソフトウェアエンジニアです。プログラミング・システム設計・"
            "AI/機械学習に詳しく、コード例や設計方針を丁寧に解説します。"
        )
    else:
        system_message = "あなたは一般的な専門家として、分かりやすく回答してください。"

    llm = ChatOpenAI(
        model="gpt-5",
        api_key=OPENAI_API_KEY,
        temperature=1,     # gpt-5は固定=1
        max_tokens=512,
        timeout=30,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "ユーザー入力: {question}\n要点を整理して日本語で回答してください。"),
    ])

    parser = StrOutputParser()
    return prompt | llm | parser


# ==== LLM呼び出し関数 ====
def ask_expert(user_text: str, expert_role: str) -> str:
    """
    入力テキストと専門家の種類を受け取り、LLMの回答を返す
    """
    if not user_text.strip():
        return "入力が空です。質問を入力してください。"
    try:
        chain = get_chain(expert_role)
        return chain.invoke({"question": user_text.strip()})
    except Exception as e:
        return f"エラーが発生しました: {type(e).__name__}: {e}"


# ==== Streamlit UI ====
st.set_page_config(page_title="Lesson8 × LangChain × 専門家LLM", page_icon="🤖")

st.title("Lesson8風 LLMアプリ（専門家選択付き）")

st.markdown("""
### アプリ概要
このアプリでは、テキストを入力し、専門家の種類を選んで送信すると、
その分野の専門家としてLLMが回答します。

### 操作方法
1. 下のラジオボタンで「専門家の種類」を選択  
2. テキストエリアに質問や文章を入力  
3. 「送信」ボタンをクリックすると回答が表示されます
""")

# 専門家の種類をラジオボタンで選択
expert_role = st.radio(
    "専門家の種類を選んでください:",
    ["経済学者", "医師", "エンジニア"],
    horizontal=True,
)

# 入力フォーム
with st.form("ask_form"):
    user_text = st.text_area("テキストを入力してください:", height=120)
    submitted = st.form_submit_button("送信")

# 回答表示
if submitted:
    if not OPENAI_API_KEY:
        st.error("OPENAI_API_KEY が未設定です。Cloud では Secrets に設定してください。")
    else:
        with st.spinner(f"{expert_role}として回答中..."):
            answer = ask_expert(user_text, expert_role)
            st.markdown("#### 回答")
            st.write(answer)
