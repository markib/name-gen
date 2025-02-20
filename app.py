import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import datetime

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

    # Initialize session state for starting letter
    if "starting_letter" not in st.session_state:
        st.session_state.starting_letter = "None"

    # User inputs
    gender = st.radio("Select Gender", ["Male", "Female"], index=1)
    # Manually defined list of countries
    country_list = [
        "United States",
        "Nepal",
        "India",
        "Bangladesh",
        "Sri Lanka",
        "Pakistan",
        "China",
        "Japan",
        "Germany",
        "France",
        "Australia",
        "Brazil",
        "Canada",
        "Russia",
        "South Korea",
        "UK",
        "Italy",
        "Spain",
        "Mexico",
        "South Africa",
        "Egypt",
        "Thailand",
        "Argentina",
        "Nigeria",
        "Indonesia",
        "Pakistan",
        "Bangladesh",
        "Saudi Arabia",
        "Turkey",
        "Iran",
    ]
    country = st.selectbox("Select Country", country_list)

    # Display A-Z Letter Selector in Multiple Columns
    st.subheader("Select a Starting Letter (optional)")
    cols = st.columns(7)  # Split into 7 columns for better visibility

    for index, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        if cols[index % 7].button(letter, key=f"letter_{letter}"):
            st.session_state.starting_letter = letter

    st.write(
        f"Selected Letter: **{st.session_state.starting_letter}**"
        if st.session_state.starting_letter != "None"
        else "No letter selected."
    )

    # Add Clear Selection button
    if st.button("Clear Letter Selection"):
        st.session_state.starting_letter = "None"
        st.experimental_rerun()

    father_name = st.text_input("Enter Father's Name (optional):")
    mother_name = st.text_input("Enter Mother's Name (optional):")
    birth_month = st.selectbox(
        "Select Birth Month",
        [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
    )

    # Get the current year dynamically
    current_year = datetime.datetime.now().year

    birth_year = st.number_input(
        "Enter Birth Year", min_value=1900, max_value=2100, value=current_year
    )

    # Name Length Selection
    name_length = st.selectbox("Select Name Length", ["Short", "Medium", "Long"])

    # Generate prompt
# Generate prompt
    prompt = f"""Generate 20 unique baby names for a {gender} child from {country}, born in {birth_month} {birth_year}. Follow these guidelines:

    1. Names should reflect the cultural heritage, traditions, and language of {country}.
    2. Provide meanings that showcase the country's heritage, spirituality, history, nature, and if applicable, local scientific achievements.
    3. Include a diverse mix of:
    a) Traditional names with cultural significance
    b) Names inspired by local celestial beliefs, zodiac signs, or astrological concepts
    c) Names related to important festivals, rituals, or ceremonies in {country}
    d) Nature-inspired names reflecting the country's landscape or wildlife
    e) Names derived from local literature, mythology, or historical figures
    f) Modern names that blend traditional elements with contemporary concepts

    4. Ensure the names are authentic to {country}'s culture and appropriate for a child born in {birth_year}.
    5. Format each entry as 'Name - Meaning', providing a brief explanation of the name's cultural or linguistic significance.
    6. For names with complex pronunciations, include a simple pronunciation guide in parentheses.
    7. Aim for a balance between unique and familiar names within the culture.

    {f"The names should start with the letter {st.session_state.starting_letter}." if st.session_state.starting_letter != "None" else ""}

    {f"The names should be {name_length.lower()}-length names." if name_length else ""}

    {f"Include a name inspired by combining the parents' names: {combined_name}." if father_name and mother_name else ""}

    Ensure all names are respectful and culturally appropriate."""


    # Modify prompt based on name length
    if name_length == "Short":
        prompt += "The names should be short (4-6 letters). "
    elif name_length == "Medium":
        prompt += "The names should be medium-length (7-9 letters). "
    else:
        prompt += "The names should be long (10+ letters). "

    # Add starting letter if selected
    if st.session_state.starting_letter != "None":
        prompt += f" The names should start with the letter {st.session_state.starting_letter}."

    if father_name and mother_name:
        combined_name = combine_names(father_name, mother_name)
        prompt += f" Include a name inspired by combining the parents' names: {combined_name}."

    # Generate names
    if st.button("🔍 Generate Names", key="generate_button"):
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
