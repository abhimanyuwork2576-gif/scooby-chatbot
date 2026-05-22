import streamlit as st
import json
import difflib
from datetime import datetime
from dateutil import parser

# Load JSON data
with open("boarding_data.json") as f:
    data = json.load(f)

# App Title
st.title("🐶 Welcome to Scooby Pet Hostel")
st.markdown("### Clear your doubts below 👇")

# Quick options
options = ["Charges", "Timings", "Facilities", "Location", "Booking"]
choice = st.selectbox("Choose a topic:", options)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = None

if "booking_info" not in st.session_state:
    st.session_state.booking_info = {}

# Show old chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
user_input = st.chat_input("Type your message...")

# Fuzzy matching
def fuzzy_match(user_input, keywords):
    words = user_input.lower().split()
    for word in words:
        match = difflib.get_close_matches(word, keywords, n=1, cutoff=0.7)
        if match:
            return match[0]
    return None

# Flexible date parser
def parse_date_flexible(date_str):
    try:
        return parser.parse(date_str, dayfirst=True)
    except:
        return None

# Dropdown auto input
if choice and not user_input:
    user_input = choice

# Main chatbot logic
if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    st.chat_message("user").write(user_input)

    reply = ""

    keywords = [
        "charges",
        "timings",
        "facilities",
        "location",
        "booking",
        "friendly",
        "aggressive",
        "paid"
    ]

    matched = fuzzy_match(user_input, keywords)

    # Charges
    if matched == "charges":
        reply = f"🐾 Charges are ₹{data['charges']['dog']} per day."

    # Timings
    elif matched == "timings":
        reply = f"⏰ We are open {data['timings']}."

    # Facilities
    elif matched == "facilities":
        reply = "🏠 Facilities include:\n\n"
        for facility in data['facilities']:
            reply += f"• {facility}\n"

    # Location
    elif matched == "location":
        reply = f"📍 {data['location']}\n\n🗺️ Map:\n{data['map_link']}"

    # Booking start
    elif matched == "booking":
        st.session_state.step = "aggressive_friendly"
        reply = "🐶 Is your dog friendly or aggressive?"

    # Friendly/aggressive step
    elif st.session_state.step == "aggressive_friendly":

        if matched == "aggressive":
            reply = "⚠️ Sorry, we cannot take aggressive dogs because there is no cage system."
            st.session_state.step = None

        elif matched == "friendly":
            st.session_state.step = "breed"
            reply = "✅ Great! What is the breed of your dog?"

        else:
            reply = "Please type Friendly or Aggressive."

    # Breed step
    elif st.session_state.step == "breed":
        st.session_state.booking_info["breed"] = user_input
        st.session_state.step = "dog_name"
        reply = "🐕 What is your dog's name?"

    # Dog name step
    elif st.session_state.step == "dog_name":
        st.session_state.booking_info["dog_name"] = user_input
        st.session_state.step = "start_date"
        reply = "📅 Enter the start date."

    # Start date step
    elif st.session_state.step == "start_date":

        start_date = parse_date_flexible(user_input)

        if start_date:
            st.session_state.booking_info["start_date"] = start_date
            st.session_state.step = "end_date"
            reply = "📅 Now enter the end date."
        else:
            reply = "⚠️ Could not understand the date. Try again."

    # End date step
    elif st.session_state.step == "end_date":

        end_date = parse_date_flexible(user_input)

        if end_date:

            start_date = st.session_state.booking_info["start_date"]

            days = (end_date - start_date).days

            if days <= 0:
                reply = "⚠️ End date must be after start date."

            else:

                total = data['charges']['dog'] * days
                advance = 100
                remaining = total - advance

                st.session_state.booking_info["end_date"] = end_date
                st.session_state.booking_info["days"] = days
                st.session_state.booking_info["total"] = total
                st.session_state.booking_info["advance"] = advance
                st.session_state.booking_info["remaining"] = remaining

                st.session_state.step = "payment"

                reply = (
                    f"📅 Booking Duration:\n"
                    f"{start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}\n\n"
                    f"🗓️ Total Days: {days}\n"
                    f"💰 Total Charges: ₹{total}\n"
                    f"🔑 Advance Payment: ₹{advance}\n\n"
                    f"👇 Click below to pay advance.\n"
                    f"After payment type: paid"
                )

        else:
            reply = "⚠️ Could not understand the end date. Try again."

    # Payment confirmation
    elif st.session_state.step == "payment" and matched == "paid":

        info = st.session_state.booking_info

        reply = (
            f"🎉 Booking Confirmed Successfully!\n\n"
            f"🐶 Dog Name: {info['dog_name']}\n"
            f"🐕 Breed: {info['breed']}\n"
            f"📅 Duration: {info['start_date'].strftime('%d-%m-%Y')} "
            f"to {info['end_date'].strftime('%d-%m-%Y')}\n"
            f"🗓️ Total Days: {info['days']}\n"
            f"💰 Total Charges: ₹{info['total']}\n"
            f"🔑 Advance Paid: ₹{info['advance']}\n"
            f"💵 Remaining Amount: ₹{info['remaining']}\n\n"
            f"✅ Thank you for choosing Scooby Pet Hostel!"
        )

        st.session_state.step = None
        st.session_state.booking_info = {}

    # Default reply
    else:
        reply = (
            "🤔 Sorry, I didn't understand.\n\n"
            "You can ask about:\n"
            "• Charges\n"
            "• Timings\n"
            "• Facilities\n"
            "• Location\n"
            "• Booking"
        )

    # Save assistant reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    # Show assistant reply
    st.chat_message("assistant").write(reply)

    # Payment button
    if st.session_state.step == "payment":
        st.link_button(
            "💳 Pay Advance",
            data["payment_info"]
        )

