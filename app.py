# app.py (Live Research Assistant dengan Tavily)

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from langchain_community.tools.tavily_search import TavilySearchResults

# --- SETUP DASAR ---
load_dotenv()
# Gunakan model yang lebih besar dan kapabel untuk tugas riset yang kompleks
llm = ChatGroq(model_name="llama3-70b-8192", temperature=0, api_key=os.getenv("GROQ_API_KEY"))

# --- DEFINISI STATE GRAFIK ---
# State akan menampung semua informasi selama proses riset
class ResearchState(TypedDict):
    topic: str
    plan: str
    research_results: List[dict]
    report: str

# --- DEFINISI ALAT (TOOLS) ---
# Kita gunakan alat pencarian Tavily yang profesional
tavily_tool = TavilySearchResults(max_results=5)

# --- DEFINISI NODE (AGEN) ---

def planner_node(state: ResearchState):
    print("--- [MASUK NODE PERENCANA] ---")
    prompt = ChatPromptTemplate.from_template(
        "Anda adalah seorang perencana riset ahli. Buatlah rencana riset yang detail dan terstruktur (dalam format poin-poin) untuk topik berikut: {topic}"
    )
    chain = prompt | llm | StrOutputParser()
    plan = chain.invoke({"topic": state['topic']})
    return {"plan": plan}

def search_node(state: ResearchState):
    print("--- [MASUK NODE PENCARI] ---")
    research_plan = state['plan']
    
    # Prompt untuk mengubah rencana menjadi query pencarian yang efektif
    prompt = ChatPromptTemplate.from_template(
        "Anda adalah seorang asisten riset AI. Berdasarkan rencana riset ini, buatlah satu query pencarian Google yang paling efektif dan komprehensif untuk menemukan jawabannya.\n\n"
        "Rencana:\n{plan}"
    )
    
    query_chain = prompt | llm | StrOutputParser()
    search_query = query_chain.invoke({"plan": research_plan})
    print(f"Melakukan pencarian live di internet dengan query: '{search_query}'")
    
    # Menjalankan alat pencarian Tavily
    research_data = tavily_tool.invoke({"query": search_query})
    return {"research_results": research_data}

def writer_node(state: ResearchState):
    print("--- [MASUK NODE PENULIS LAPORAN] ---")
    topic = state['topic']
    research_data = state['research_results']

    prompt = ChatPromptTemplate.from_template(
        "Anda adalah seorang penulis laporan riset profesional. Tugas Anda adalah menulis sebuah laporan yang ringkas dan terstruktur berdasarkan topik dan data hasil pencarian internet berikut.\n\n"
        "Topik Utama: {topic}\n\n"
        "Data Hasil Pencarian (dalam format JSON):\n{research}\n\n"
        "Instruksi: Susun data tersebut menjadi sebuah laporan yang koheren, informatif, dan mudah dibaca dalam Bahasa Indonesia. Buat judul, beberapa sub-judul, dan kesimpulan."
    )
    
    chain = prompt | llm | StrOutputParser()
    report = chain.invoke({"topic": topic, "research": research_data})
    return {"report": report}


# --- MEMBANGUN GRAFIK ---
workflow = StateGraph(ResearchState)
workflow.add_node("planner", planner_node)
workflow.add_node("searcher", search_node)
workflow.add_node("writer", writer_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "searcher")
workflow.add_edge("searcher", "writer")
workflow.add_edge("writer", END)

app = workflow.compile()

# --- MENJALANKAN GRAFIK ---
topic_to_research = "Prospek dan tantangan investasi energi terbarukan di IKN pasca 2025"
final_state = app.invoke({"topic": topic_to_research})

# Menampilkan hasil akhir
print("\n\n==================== LAPORAN RISET FINAL ====================")
print(final_state['report'])
print("======================================================")