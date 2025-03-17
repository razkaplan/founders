import streamlit as st
import yaml
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

# Load YAML file
def load_quotes():
    with open("quotes.yml", "r", encoding="utf-8") as file:
        quotes = yaml.safe_load(file)
        # Reverse the order to show newest quotes first
        return quotes[::-1]

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
wordcloud = WordCloud(width=600, height=300,
                       background_color=None, mode='RGBA').generate_from_frequencies(trending_words)

# Create columns to center the word cloud
col1, col2, col3 = st.columns([1, 2, 1])

# Display word cloud in the center column
with col2:
    st.image(wordcloud.to_array(), use_container_width=True)

selected_word = st.selectbox("Filter quotes by word:", ["All"] + list(trending_words.keys()))

# Custom component for claim popup
def create_claim_popup():
    components_js = """
    <script>
    // Function to create and display the popup
    function showClaimPopup(index) {
        // Create overlay
        var overlay = document.createElement('div');
        overlay.id = 'claim-overlay-' + index;
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.backgroundColor = 'rgba(0,0,0,0.5)';
        overlay.style.display = 'flex';
        overlay.style.justifyContent = 'center';
        overlay.style.alignItems = 'center';
        overlay.style.zIndex = '1000';
        
        // Create popup content
        var popup = document.createElement('div');
        popup.style.backgroundColor = 'white';
        popup.style.padding = '20px';
        popup.style.borderRadius = '10px';
        popup.style.maxWidth = '400px';
        popup.style.width = '80%';
        popup.style.position = 'relative';
        
        // Create close button
        var closeBtn = document.createElement('button');
        closeBtn.innerHTML = '×';
        closeBtn.style.position = 'absolute';
        closeBtn.style.top = '10px';
        closeBtn.style.right = '10px';
        closeBtn.style.border = 'none';
        closeBtn.style.background = 'none';
        closeBtn.style.fontSize = '20px';
        closeBtn.style.cursor = 'pointer';
        closeBtn.onclick = function() {
            document.body.removeChild(overlay);
        };
        
        // Create content
        var title = document.createElement('h3');
        title.innerHTML = 'Contact me to claim your quote';
        
        var desc = document.createElement('p');
        desc.innerHTML = 'Get in touch with me to claim this quote:';
        
        var linkedinLink = document.createElement('a');
        linkedinLink.href = 'https://www.linkedin.com/in/razkaplan/';
        linkedinLink.target = '_blank';
        linkedinLink.innerHTML = 'LinkedIn Profile';
        linkedinLink.style.display = 'block';
        linkedinLink.style.margin = '10px 0';
        linkedinLink.style.padding = '8px 15px';
        linkedinLink.style.backgroundColor = '#007bff';
        linkedinLink.style.color = 'white';
        linkedinLink.style.textDecoration = 'none';
        linkedinLink.style.borderRadius = '5px';
        linkedinLink.style.textAlign = 'center';
        
        var websiteLink = document.createElement('a');
        websiteLink.href = 'https://razkaplan.github.io/gtm/';
        websiteLink.target = '_blank';
        websiteLink.innerHTML = 'My Website';
        websiteLink.style.display = 'block';
        websiteLink.style.margin = '10px 0';
        websiteLink.style.padding = '8px 15px';
        websiteLink.style.backgroundColor = '#007bff';
        websiteLink.style.color = 'white';
        websiteLink.style.textDecoration = 'none';
        websiteLink.style.borderRadius = '5px';
        websiteLink.style.textAlign = 'center';
        
        // Append elements
        popup.appendChild(closeBtn);
        popup.appendChild(title);
        popup.appendChild(desc);
        popup.appendChild(linkedinLink);
        popup.appendChild(websiteLink);
        overlay.appendChild(popup);
        
        // Close when clicking outside
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                document.body.removeChild(overlay);
            }
        });
        
        // Add to body
        document.body.appendChild(overlay);
    }
    </script>
    """
    st.components.v1.html(components_js, height=0)

# Call the function to create popup
create_claim_popup()

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
                # Create claim button that triggers the popup using JavaScript
                buttons.append(f'<button onclick="showClaimPopup({idx})" style="padding:5px 10px; background:#dc3545;color:white; border-radius:5px; text-decoration:none; border:none; display:inline-block; cursor:pointer;">💼 {quote["name"]} (Claim)</button>')
            
            if quote.get("company_url"):
                company_url = f'{quote["company_url"]}?utm_source=Raz_Kaplan&utm_medium=Raz_Kaplan&utm_campaign=Raz_Kaplan'
                buttons.append(f'<a href="{company_url}" target="_blank" style="padding:5px 10px; background:#ffc107; color:black; border-radius:5px; text-decoration:none; display:inline-block;">🏢 {quote["company"]}</a>')
            else:
                buttons.append(f'<span style="padding:5px 10px; background:#6c757d; color:white; border-radius:5px; text-decoration:none; display:inline-block;">🏢 {quote["company"]}</span>')
            
            st.markdown(f'<div style="text-align: center; margin-top: 10px;">' + " ".join(buttons) + '</div>', unsafe_allow_html=True)
            st.markdown('<hr style="border: 0; height: 1px; background: #ccc; margin: 10px 0;">', unsafe_allow_html=True)

# Display quotes with filtering
display_quotes(quotes, selected_word)

# Footer
st.markdown('<hr style="border: 0; height: 1px; background: #ccc; margin: 20px 0;">', unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>Made by <a href='https://razkaplan.github.io/gtm/' "
"target='_blank'>Raz Kaplan</a> | <a href='https://www.linkedin.com/in/razkaplan/' target='_blank'>LinkedIn</a></div>", unsafe_allow_html=True)