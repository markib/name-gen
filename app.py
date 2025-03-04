import streamlit as st
import google.generativeai as genai
print(genai.__version__)
import os
from dotenv import load_dotenv
import datetime
import random

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
    model_name = "gemini-2.0-flash"  # Or any model name you want to try
    try:
        model = genai.GenerativeModel(model_name)
        print(f"Model '{model_name}' is available.")
        response = model.generate_content(prompt)
        return response.text.strip()
    except ValueError as e:
        if "Unknown model" in str(e):
            print(f"Model '{model_name}' is not available (version 0.8.4).")
        else:
            print(f"An error occurred: {e}")    
    except Exception as e:
        return f"An error occurred: {str(e)}"


def combine_names(father_name, mother_name):
    """Creates a combined baby name from the parents' names."""
    return f"{father_name[:len(father_name)//2]}{mother_name[len(mother_name)//2:]}"


def get_cultural_elements(country):
    """Returns cultural elements based on the selected country."""
    cultural_elements = {
        "United States": "American values, diversity, innovation",
        "Nepal": "Himalayan culture, Buddhist and Hindu traditions",
        "India": "Vedic traditions, diverse regional cultures",
        # Add more countries and their cultural elements
    }
    return cultural_elements.get(country, "local traditions and culture")


def main():
    st.title("👶 AI-Powered Baby Name Generator with Meanings")

    # Initialize session state
    if "starting_letter" not in st.session_state:
        st.session_state.starting_letter = "None"
    if "generated_names" not in st.session_state:
        st.session_state.generated_names = []

    # User inputs
    gender = st.radio("Select Gender", ["Male", "Female", "Unisex"], index=1)
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
        "Saudi Arabia",
        "Turkey",
        "Iran",
    ]
    country = st.selectbox("Select Country", country_list)

    # Starting Letter Selection
    st.subheader("Select a Starting Letter (optional)")
    cols = st.columns(7)
    for index, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        if cols[index % 7].button(letter, key=f"letter_{letter}"):
            st.session_state.starting_letter = letter

    st.write(
        f"Selected Letter: **{st.session_state.starting_letter}**"
        if st.session_state.starting_letter != "None"
        else "No letter selected."
    )

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

    current_year = datetime.datetime.now().year
    birth_year = st.number_input(
        "Enter Birth Year", min_value=1900, max_value=2100, value=current_year
    )

    name_length = st.selectbox("Select Name Length", ["Short", "Medium", "Long"])

    # Additional cultural preferences
    cultural_importance = st.slider("Importance of Cultural Significance", 1, 10, 5)
    modern_twist = st.checkbox("Include modern twists on traditional names")

    # Generate prompt
    cultural_elements = get_cultural_elements(country)
    prompt = f"""Generate 20 unique baby names for a {gender} child from {country}, born in {birth_month} {birth_year}. Follow these guidelines:

    1. Names should reflect the cultural heritage, traditions, and language of {country}, emphasizing {cultural_elements}.
    2. Provide meanings that showcase the country's heritage, spirituality, history, nature, and if applicable, local scientific achievements.
    3. Include a diverse mix of:
       a) Traditional names with cultural significance (importance level: {cultural_importance}/10)
       b) Names inspired by local celestial beliefs, zodiac signs, or astrological concepts
       c) Names related to important festivals, rituals, or ceremonies in {country}
       d) Nature-inspired names reflecting the country's landscape or wildlife
       e) Names derived from local literature, mythology, or historical figures
       f) {f"Modern names that blend traditional elements with contemporary concepts" if modern_twist else "Classic names that have stood the test of time"}

    4. Ensure the names are authentic to {country}'s culture and appropriate for a child born in {birth_year}.
    5. Format each entry as 'Name - Meaning', providing a brief explanation of the name's cultural or linguistic significance.
    6. For names with complex pronunciations, include a simple pronunciation guide in parentheses.
    7. Aim for a balance between unique and familiar names within the culture.

    {f"The names should start with the letter {st.session_state.starting_letter}." if st.session_state.starting_letter != "None" else ""}
    {f"The names should be {name_length.lower()}-length names." if name_length else ""}

    Ensure all names are respectful and culturally appropriate."""

    if father_name and mother_name:
        combined_name = combine_names(father_name, mother_name)
        prompt += f" Include a name inspired by combining the parents' names: {combined_name}."

    # Generate names
    if st.button("🔍 Generate Names", key="generate_button"):
        if not gender or not country:
            st.warning("⚠️ Please select both gender and country.")
        else:
            with st.spinner("Generating names..."):
                names = generate_names(prompt)
            if "error" in names.lower():
                st.error(names)
            else:
                st.session_state.generated_names = names.split("\n")
                st.success("🎉 Suggested Names with Meanings:")
                for line in st.session_state.generated_names:
                    if " - " in line:
                        name, meaning = line.split(" - ", 1)
                        st.markdown(f"**{name.strip()}** - *{meaning.strip()}*")
                    else:
                        st.write(line)

    # Favorite name selection
    if st.session_state.generated_names:
        st.subheader("Select your favorite names")
        favorite_names = st.multiselect(
            "Choose your favorite names",
            [
                name.split(" - ")[0].strip()
                for name in st.session_state.generated_names
                if " - " in name
            ],
        )
        if favorite_names:
            st.write("Your favorite names:")
            for name in favorite_names:
                st.write(name)

    # Random name suggestion
    if st.button("Suggest a Random Name"):
        if st.session_state.generated_names:
            random_name = random.choice(
                [name for name in st.session_state.generated_names if " - " in name]
            )
            name, meaning = random_name.split(" - ", 1)
            st.success(f"Random Suggestion: **{name.strip()}** - *{meaning.strip()}*")
        else:
            st.warning("Please generate names first.")


if __name__ == "__main__":
    main()
