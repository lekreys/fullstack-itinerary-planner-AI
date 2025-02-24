
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage , AIMessage , SystemMessage
from langchain.prompts import PromptTemplate

API_KEY = "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"


llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=API_KEY)

# Membuat daftar pesan untuk input
messages = [
    SystemMessage(content="Kamu adalah seorang trip planner."),
    HumanMessage(content="Rekomendasi 2 tempat pantai?")
]

# Memanggil model
response = llm.invoke(messages)

# Menampilkan hasil
print(response.content)
