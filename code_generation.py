import streamlit as st
from openai import AzureOpenAI

st.set_page_config(page_title="AI Code Generator", layout="centered")
st.title("Code Generator")

# Step 1: Input Azure OpenAI Configuration
AZURE_OPENAI_KEY = st.text_input("Enter your Azure OpenAI Key:", type="password")
AZURE_OPENAI_ENDPOINT = st.text_input("Enter your Azure OpenAI Endpoint:")
AZURE_OPENAI_DEPLOYMENT = st.text_input("Enter your Azure OpenAI Deployment Name:")

# Step 2: Get user input
prompt = st.text_area("Describe your problem", height=120)
language = st.selectbox("Select Programming Language", ["python", "java", "c"])

# Step 3: Generate Code
if st.button("Generate Code"):
    if not prompt.strip():
        st.warning("Please enter a valid problem statement.")
    elif not AZURE_OPENAI_KEY:
        st.warning("Please enter your Azure OpenAI Key.")
    elif not AZURE_OPENAI_ENDPOINT:
        st.warning("Please enter your Azure OpenAI Endpoint.")
    elif not AZURE_OPENAI_DEPLOYMENT:
        st.warning("Please enter your Azure OpenAI Deployment Name.")
    else:
        # Create a focused prompt for code generation only
        language_names = {"python": "Python", "java": "Java", "c": "C"}
        system_prompt = f"You are an expert {language_names[language]} code generator. Generate ONLY {language_names[language]} code with NO explanations, NO comments, NO markdown formatting. Just pure code."
        
        user_prompt = f"Generate {language_names[language]} code for the following requirement:\n\n{prompt}"

        with st.spinner("Generating code..."):
            try:
                # Configure Azure OpenAI Client
                client = AzureOpenAI(
                    api_key=AZURE_OPENAI_KEY,
                    api_version="2024-02-15-preview",
                    azure_endpoint=AZURE_OPENAI_ENDPOINT
                )
                
                messages = [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
                
                response = client.chat.completions.create(
                    model=AZURE_OPENAI_DEPLOYMENT,
                    messages=messages,
                    temperature=0.3,
                    max_tokens=1024
                )
                
                generated_code = response.choices[0].message.content.strip()
                
                # Remove markdown code blocks if present
                if generated_code.startswith("```"):
                    generated_code = generated_code.split("```")[1]
                    if generated_code.startswith(language):
                        generated_code = generated_code[len(language):].lstrip("\n")
                
                st.success("Generated Code:")
                st.code(generated_code, language=language)
            except Exception as e:
                st.error(f"❌ Error: {e}")
