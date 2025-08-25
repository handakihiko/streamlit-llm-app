# streamlit-llm-app

Streamlit 上で入力テキストを送信すると、選択した「専門家」として LLM が回答するアプリです

---

## アプリ概要

- 単一の入力フォームに質問を入力
- ラジオボタンで「専門家の種類」を選択  
  - 経済学者 / 医師 / エンジニア
- 選択した専門家ロールに応じて **LLM のシステムプロンプトが切り替わり**、回答が変化
- LangChain の `ChatPromptTemplate` → `ChatOpenAI` → `StrOutputParser` を使用

---

## 操作方法

1. サイドのラジオボタンで「専門家の種類」を選択  
2. テキストエリアに質問を入力  
3. 「送信」ボタンをクリック  
4. 回答が画面に表示されます ✅

---

## ローカル環境での実行方法 (VSCode)

### 1. 仮想環境の作成
```bash
# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
