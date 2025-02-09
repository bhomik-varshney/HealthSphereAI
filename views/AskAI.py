import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage
API_KEY = "xxxxx-xxxxx"
from langgraph.graph import Graph
from langchain_groq import ChatGroq
import time
import pdfplumber
import pytesseract
import spacy
from PIL import Image



llm = ChatGroq(model = "llama-3.3-70b-versatile",api_key = API_KEY)

if "chat_memory" not in st.session_state:
    st.session_state["chat_memory"] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)



if "message_log" not in st.session_state:
    st.session_state["message_log"] = {}
def func1(input):
    memory = st.session_state["chat_memory"]
    chat_history = memory.load_memory_variables({}).get("chat_history", [])
    formatted_history = "\n".join(
        [f"User: {msg.content}" if isinstance(msg, HumanMessage) else f"AI: {msg.content}" for msg in chat_history])
    prompt_template = f"""
You are **HealthSphere AI**, an expert medical AI specializing in **healthcare, medicine, and human biology**.  
Your goal is to provide **accurate, science-backed answers** to **all medical-related questions**, including:
- Medical conditions, symptoms, and treatments  
- Human anatomy and physiology  
- Neuroscience and mental health  
- Pharmacology and common medications  
- Medical research and advancements  
- First aid and emergency care  
- Nutrition and preventive healthcare  

### **Previous Conversation:**
{formatted_history}
        
---

### **User's Query:**
{input}

---

### **Response Strategy:**

1️⃣ **Medical Explanation & Diagnosis:**  
   - If the user asks a **general medical question**, provide a **concise, factual answer**.  
   - If the user **describes symptoms**, suggest **possible medical conditions** based on symptoms.  
   - If necessary, ask for **one additional investigation or symptom clarification**.  
   - Example:  
     **User:** "I have headaches and nausea for the past few days."  
     **HealthSphere AI:** "This could be due to dehydration, migraine, or an underlying infection. Do you also experience sensitivity to light?"  

2️⃣ **Treatment & Remedies:**  
   - After identifying possible conditions, **suggest treatments**.  
   - Include **simple home remedies, lifestyle changes, and precautions**.  
   - Suggest **over-the-counter medications (if applicable and safe)**.  
   - Example:  
     *"For mild flu symptoms, rest, hydration, and paracetamol may help. If symptoms persist, seek medical advice."*  

3️⃣ **User Engagement & Next Steps:**  
   - Ask the user if they **want to explore possible medications and remedies**.  
   - If they agree, **list safe and general treatment options**.  
   - Remind them to **consult a healthcare provider for confirmation**.  

---

⚠️ **Important Notes:**
- **Do NOT provide final diagnoses.** Clearly state that this is an **AI-based assumption**.
- Keep responses **concise, supportive, and medically accurate**.
- Always **recommend consulting a medical professional for confirmation**.
"""

    message = llm.invoke(prompt_template).content
    memory.save_context(
        inputs={"input": input},
        outputs={"output": message}
    )
    (st.session_state["message_log"])[input] = message
    return message



workflow = Graph()
workflow.add_node("function_1",func1)
workflow.set_entry_point("function_1")
workflow.set_finish_point("function_1")
app = workflow.compile()

if "selectBox" not in st.session_state:
    st.session_state["selectBox"] = None


with st.sidebar:
    st.title("Features")
    select_box = st.selectbox("",options=["Chat","Report Analysis"])
    st.session_state["selectBox"] = select_box
    st.caption(f"HealthSphere AI is an intelligent healthcare assistant providing expert medical insights, symptom analysis, and treatment guidance. It explains complex medical concepts, suggests over-the-counter remedies, and encourages well-being. With an empathetic tone, it ensures users receive accurate, science-backed healthcare information while promoting professional medical consultation when necessary.")
st.write("")

def prev_messages():
    if len(st.session_state["message_log"]) != 0:
        for prompt, message in (st.session_state["message_log"]).items():
            st.html(f"""<p style = "padding:20px;color:white;border-radius: 25px;
                  border: 2px solid #73AD21">{prompt}</p>""")
            st.markdown(f"""
                <div style="color:white; padding:20px; border-radius: 25px; 
                border: 2px solid rgb(277,66,52)">
                {message}
                </div>
                """, unsafe_allow_html=True)
    else:
        pass

if st.session_state["selectBox"] == "Chat":
    st.html(f"""<h1 style = "font-size:50px;margin-top:0px;margin-bottom:0px;text-align:center;font-family: 'Georgia', serif;
    font-weight: bold;">HealthSphere AI</h1>""")
    message = st.chat_input("How can I assist you today ?")



    prev_messages()
    if message:
        time.sleep(0.5)
        st.write("Your Prompt")
        st.html(f"""<p style = "padding:20px;color:white;border-radius: 25px;
          border: 2px solid #73AD21">{message}</p>""")
        start = time.time()
        response = app.invoke(message)
        currTime = time.time()-start
        st.caption(f"""time : {currTime} seconds""")
        st.write("Response")
        time.sleep(0.5)

        st.markdown(f"""
        <div style="color:white; padding:20px; border-radius: 25px; 
        border: 2px solid rgb(277,66,52)">
        {response}
        </div>
        """, unsafe_allow_html=True)
    else:
        # st.html(f"""<p style = "text-align:center;padding-top:150px;font-family: 'Merriweather', sans-serif;font-size: 20px;line-height: 1.6">Hello there ! I am ThinkSwift AI, how can I assist you ?</p>""")
        st.html(f"""
        <p style="text-align:center; padding-top:150px; font-family: 'Merriweather', sans-serif; font-size: 20px; line-height: 1.6; list-style-position: inside;padding-left:0px">
            Hello there !
        </p>
        <p style=" text-align:center; padding-top:0px; font-family: 'Merriweather', sans-serif; font-size: 20px; line-height: 1.6; list-style-position: inside;">I am HealthSphere AI, how can I assist you?</p>
        """)
else:
    st.html(f"""<h1 style = "font-size:50px;margin-top:0px;margin-bottom:0px;text-align:center;font-family: 'Georgia', serif;
        font-weight: bold;">Report Analysis</h1>""")
    nlp = spacy.load("en_core_web_sm")  # Named Entity Recognition (NER)
    st.write("")
    uploaded_file = st.file_uploader("Upload a PDF or Image (PNG, JPG)", type=["pdf", "png", "jpg", "jpeg"])


    def extract_text_from_pdf(file):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + " "
        return text.strip()


    def extract_text_from_image(file):
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return text.strip() if text else "No text found in the image."


    def analyze_text_nlu(text):
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities


    if uploaded_file:
        file_type = uploaded_file.type

        if file_type == "application/pdf":
            extracted_text = extract_text_from_pdf(uploaded_file)
        elif file_type in ["image/png", "image/jpeg"]:
            extracted_text = extract_text_from_image(uploaded_file)
        else:
            extracted_text = "Unsupported file format."

        entities = analyze_text_nlu(extracted_text)
        prompt_template = f"""
        Analyze the given medical report and extract key health insights.

        ### 📜 Extracted Report Data:
        {extracted_text}

        ### 🔍 Detected Entities (Named Entity Recognition - NLU):
        - **NLU data extracted:** {entities}


        ### 🔎 Your Tasks:
        1 **Identify Any Abnormalities** in the report.
        2 **Identify Disease (if any). tell if it is severe or not.
        3 **List Major Symptoms the User May Feel** based on detected conditions.
        4 **Provide Health Improvement Suggestions** with lifestyle changes, diet, or precautions.


        ⚠️ **Important:**
        - Keep the response concise and medically accurate.
        - Maintain an empathetic and supportive tone.
        """
        # Question-Answering System
        if st.button("Analyze"):
            answer = llm.invoke(prompt_template).content
            st.markdown(f"""
                            <div style="color:white; padding:20px; border-radius: 25px; 
                            border: 2px solid rgb(277,66,52)">
                            {answer}
                            </div>
                            """, unsafe_allow_html=True)
