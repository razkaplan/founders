import streamlit as st
import yaml
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

# Load YAML file
def load_quotes():
    with open("quotes.yml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

# Extract Trending Words
def get_trending_words(quotes):
    words = " ".join([q["quote"] for q in quotes]).split()
    return Counter(words)

# Streamlit App Layout
st.set_page_config(layout="wide")
st.title("🚀 Modern Founders Quotes")

# Load quotes
quotes = load_quotes()

# Generate Word Cloud and Filter Functionality
trending_words = get_trending_words(quotes)
wordcloud = WordCloud(width=600, height=300, background_color=None, mode='RGBA').generate_from_frequencies(trending_words)

# Create columns to center the word cloud
col1, col2, col3 = st.columns([1, 2, 1])

# Display word cloud in the center column
with col2:
    st.image(wordcloud.to_array(), use_container_width=True)

selected_word = st.selectbox("Filter quotes by word:", ["All"] + list(trending_words.keys()))

# Add JavaScript for popup functionality
popup_script = """
<script>
function showClaimPopup(idx) {
    const popup = document.getElementById('claim-popup-' + idx);
    popup.style.display = 'block';
}

function hideClaimPopup(idx) {
    const popup = document.getElementById('claim-popup-' + idx);
    popup.style.display = 'none';
}
</script>
"""
st.markdown(popup_script, unsafe_allow_html=True)

# Add CSS for popup styling
popup_style = """
<style>
.popup-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    z-index: 999;
    justify-content: center;
    align-items: center;
}
.popup-content {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    max-width: 400px;
    width: 80%;
    text-align: center;
    position: relative;
}
.close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
    font-size: 20px;
}
.contact-link {
    display: block;
    margin: 10px 0;
    padding: 8px 15px;
    background-color: #007bff;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    text-align: center;
}
</style>
"""
st.markdown(popup_style, unsafe_allow_html=True)

# Display Quotes
def display_quotes(quotes, selected_word):
    for idx, quote in enumerate(quotes):
        if selected_word != "All" and selected_word.lower() not in quote["quote"].lower():
            continue
        
        with st.container():
            st.markdown(f'<div style="text-align: center;"><strong>"{quote["quote"]}"</strong></div>', unsafe_allow_html=True)
            
            buttons = []
            if quote.get("source"):
                buttons.append(f'<a href="{quote["source"]}" target="_blank" style="padding:5px 10px; background:#007bff; color:white; border-radius:5px; text-decoration:none; display:inline-block;">🔗 Source</a>')
            
            if quote.get("linkedin"):
                buttons.append(f'<a href="{quote["linkedin"]}" target="_blank" style="padding:5px 10px; background:#28a745; color:white; border-radius:5px; text-decoration:none; display:inline-block;">💼 {quote["name"]}</a>')
            else:
                # Create claim button that triggers the popup
                buttons.append(f'<button onclick="showClaimPopup({idx})" style="padding:5px 10px; background:#dc3545; color:white; border-radius:5px; text-decoration:none; border:none; display:inline-block; cursor:pointer;">💼 {quote["name"]} (Claim)</button>')
                
                # Create the popup HTML
                popup_html = f'''
                <div id="claim-popup-{idx}" class="popup-overlay" onclick="hideClaimPopup({idx})">
                    <div class="popup-content" onclick="event.stopPropagation()">
                        <span class="close-button" onclick="hideClaimPopup({idx})">×</span>
                        <h3>Contact me to claim your quote</h3>
                        <p>Get in touch with me to claim this quote:</p>
                        <a href="https://www.linkedin.com/in/razkaplan/" target="_blank" class="contact-link">LinkedIn Profile</a>
                        <a href="https://razkaplan.github.io/gtm/" target="_blank" class="contact-link">My Website</a>
                    </div>
                </div>
                '''
                st.markdown(popup_html, unsafe_allow_html=True)
            
            if quote.get("company_url"):
                company_url = f'{quote["company_url"]}?utm_source=Raz_Kaplan&utm_medium=Raz_Kaplan&utm_campaign=Raz_Kaplan'
                buttons.append(f'<a href="{company_url}" target="_blank" style="padding:5px 10px; background:#ffc107; color:black; border-radius:5px; text-decoration:none; display:inline-block;">🏢 {quote["company"]}</a>')
            else:
                buttons.append(f'<span style="padding:5px 10px; background:#6c757d; color:white; border-radius:5px; text-decoration:none; display:inline-block;">🏢 {quote["company"]}</span>')
            
            st.markdown(f'<div style="text-align: center; margin-top: 10px;">' + " ".join(buttons) + '</div>', unsafe_allow_html=True)
            st.markdown('<hr style="border: 0; height: 1px; background: #ccc; margin: 10px 0;">', unsafe_allow_html=True)

# Display quotes with filtering
st.markdown("<div style='text-align: center; margin-bottom: 20px;'>Select a word from the word cloud to filter quotes</div>", unsafe_allow_html=True)
display_quotes(quotes, selected_word)

# Footer
st.markdown('<hr style="border: 0; height: 1px; background: #ccc; margin: 20px 0;">', unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>Made by <a href='https://razkaplan.github.io/gtm/' target='_blank'>Raz Kaplan</a> | <a href='https://www.linkedin.com/in/razkaplan/' target='_blank'>LinkedIn</a></div>", unsafe_allow_html=True)