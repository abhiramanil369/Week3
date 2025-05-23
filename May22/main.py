import asyncio
from langchain.schema import AIMessage, HumanMessage
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.tools.retriever import create_retriever_tool

# --- ChromaDB Setup ---
def setup_chromadb(collection_name="faq_docs"):
    embedding_fn = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key="AIzaSyB0qRY3QIGnlNd_Gz1ux39ljCzgwuO-1GU"
    )
    db = Chroma(
        collection_name=collection_name,
        embedding_function=embedding_fn,
        persist_directory="./chroma_faq"
    )
    return db

# --- Gemini LLM Setup ---
def setup_gemini_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.2,
        google_api_key="AIzaSyB0qRY3QIGnlNd_Gz1ux39ljCzgwuO-1GU",  
        streaming=True,
    )
    return llm

# --- RAG Retriever Tool ---
def build_rag_retriever_tool(chromadb):
    retriever = chromadb.as_retriever(search_kwargs={"k": 4})
    return create_retriever_tool(
        retriever,
        "faq_retriever",
        "Useful for answering questions about the FAQ knowledge base."
    )

# --- Agent Definitions ---
def get_query_handler_agent(llm, retriever_tool):
    tools = [retriever_tool]
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        memory=memory
    )
    return agent

def get_rag_retriever_agent(llm, chromadb):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=chromadb.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True
    )
    return qa_chain

# --- GroupChat Setup (RoundRobin) ---
class RoundRobinGroupChat:
    def __init__(self, agents, max_rounds=5):
        self.agents = agents
        self.max_rounds = max_rounds

    async def achat(self, user_query):
        context = user_query
        last_response = None
        for round_num in range(self.max_rounds):
            for agent_name, agent in self.agents:
                if hasattr(agent, "invoke") or hasattr(agent, "__call__"):
                    output = await asyncio.to_thread(agent, context)
                    if isinstance(output, dict) and "result" in output:
                        response = output["result"]
                    else:
                        response = output
                else:
                    response = await asyncio.to_thread(agent, context)
                last_response = response
                context = str(response)
        return last_response

# --- Main Async Logic ---
async def main():
    chromadb = setup_chromadb()
    llm = setup_gemini_llm()
    retriever_tool = build_rag_retriever_tool(chromadb)
    query_handler = get_query_handler_agent(llm, retriever_tool)
    rag_retriever = get_rag_retriever_agent(llm, chromadb)
    group_agents = [
        ("QueryHandler", query_handler),
        ("RAGRetriever", rag_retriever)
    ]
    group_chat = RoundRobinGroupChat(group_agents, max_rounds=3)
    print("Welcome to the FAQ Chatbot with RAG (Gemini-only, async). Ask your questions!")
    while True:
        user_query = input("You: ")
        if user_query.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        response = await group_chat.achat(user_query)
        print(f"Bot: {response}")

if __name__ == "__main__":
    asyncio.run(main())