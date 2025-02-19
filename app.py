import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GENAI_API_KEY = st.secrets["google"]["GENAI_API_KEY"]

# Configure Google AI API Key
if not GENAI_API_KEY:
    st.error("API key not found! Please set GENAI_API_KEY in the .env file.")
else:
    genai.configure(api_key=GENAI_API_KEY)

def generate_names(prompt):
    """Generates baby names along with their meanings using Google Gemini API."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

def combine_names(father_name, mother_name):
    """Creates a combined baby name from the parents' names."""
    return f"{father_name[:len(father_name)//2]}{mother_name[len(mother_name)//2:]}"

def main():
    st.title("👶 AI-Powered Baby Name Generator with Meanings")

    # User inputs
    gender = st.radio("Select Gender", ["Male", "Female"], index=1)
    country = st.selectbox("Select Country", ["USA", "Nepal", "India", "China", "Japan"])
    starting_letter = st.text_input("Enter a starting letter (optional):", max_chars=1)
    father_name = st.text_input("Enter Father's Name (optional):")
    mother_name = st.text_input("Enter Mother's Name (optional):")
    birth_month = st.selectbox("Select Birth Month", [
        "January", "February", "March", "April", "May", "June", "July", "August", 
        "September", "October", "November", "December"
    ])
    birth_year = st.number_input("Enter Birth Year", min_value=1900, max_value=2100, value=2023)

    # Generate prompt
    prompt = f"Generate 20 unique Newar (Newa) baby names for a {gender} child from Nepal, born in {birth_month} {birth_year}. "
    prompt += "Each name should have deep roots in Newari culture, traditions, and language. Provide meanings that reflect Newar heritage, spirituality, history, or nature. "
    prompt += "Format the output as 'Name - Meaning'. Include a mix of historical, traditional, and modern names."

    
    if starting_letter:
        prompt += f" The names should start with the letter {starting_letter.upper()}."
    
    if father_name and mother_name:
        combined_name = combine_names(father_name, mother_name)
        prompt += f" Include a name inspired by combining the parents' names: {combined_name}."

    # Generate names
    if st.button("🔍 Generate Names"):
        if not gender or not country:
            st.warning("⚠️ Please select both gender and country.")
        else:
            names = generate_names(prompt)
            if "error" in names.lower():
                st.error(names)
            else:
                st.success("🎉 Suggested Names with Meanings:")
                names_list = names.split("\n")
                for line in names_list:
                    if " - " in line:
                        name, meaning = line.split(" - ", 1)
                        st.markdown(f"**{name.strip()}** - *{meaning.strip()}*")
                    else:
                        st.write(line)

if __name__ == "__main__":
    main()
