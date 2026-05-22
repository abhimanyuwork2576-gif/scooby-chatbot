import streamlit as st
import difflib
import json
from datetime import datetime

# Load data from JSON file
with open("boarding_data.json") as f:
    data = json.load(f)

st.title("🐶 Scooby Pet Hostel Chatbot")

def parse_date(date_str):
    for fmt in ["%d-%m-%Y", "%d/%m/%Y", "%d %m %Y", "%d%m%Y"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def chatbot_logic(user_input):
    user_input = user_input.lower()

    if "charge" in user_input or "price" in user_input or "paisa" in user_input:
        return f"🐾 Charges are ₹{data['charges']['dog']}/day."

    elif "time" in user_input or "open" in user_input or "timing" in user_input:
        return f"⏰ We are open {data['timings']}."

    elif "facility" in user_input or "service" in user_input:
        return "🏠 Facilities include:\n- " + "\n- ".join(data['facilities'])

    elif "location" in user_input or "address" in user_input or "map" in user_input:
        return f"📍 Location is {data['location']}\n🗺️ Map: {data['map_link']}"

    elif "book" in user_input or "booking" in user_input or "reserve" in user_input:
        nature = st.text_input("Is your pet aggressive or friendly?")
        if nature:
            match = difflib.get_close_matches(nature.lower(), ["aggressive", "friendly"], n=1, cutoff=0.6)
            if match and match[0] == "aggressive":
                return "⚠️ Sorry, we can’t take aggressive pets because there is no cage system."
            elif match and match[0] == "friendly":
                breed = st.text_input("Enter dog breed:")
                start_date_str = st.text_input("Enter start date (DDMMYYYY or DD-MM-YYYY):")
                end_date_str = st.text_input("Enter end date (DDMMYYYY or DD-MM-YYYY):")

                if start_date_str and end_date_str:
                    start_date = parse_date(start_date_str)
                    end_date = parse_date(end_date_str)

                    if not start_date or not end_date:
                        return "⚠️ Invalid date format. Please enter like 25-05-2026 or 25052026."

                    days = (end_date - start_date).days
                    if days <= 0:
                        return "⚠️ Invalid dates. End date must be after start date."

                    total = data['charges']['dog'] * days
                    advance = 100
                    remaining = total - advance

                    # 👉 Show total BEFORE paid
                    st.write(f"\n💰 Total Charges: ₹{total}\n"
                             f"📅 Duration: {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')} ({days} days)\n"
                             f"🔑 Please pay ₹{advance} advance via UPI: {data['payment_info']}")

                    paid = st.text_input("Type 'paid' after advance payment:")
                    if paid.lower() == "paid":
                        return (f"\n🎉 Successful Booking!\n"
                                f"🐶 Pet: {breed}\n"
                                f"📅 Duration: {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')} ({days} days)\n"
                                f"💰 Total Charges: ₹{total}\n"
                                f"🔑 Advance Paid: ₹{advance}\n"
                                f"💳 Remaining at Check-in: ₹{remaining}\n"
                                f"✅ Thank you! Your booking is confirmed.\n")
                    else:
                        return "⚠️ Booking not confirmed. Advance payment required."
                else:
                    return "Please enter booking dates."
            else:
                return "🤔 Please specify clearly if your pet is 'aggressive' or 'friendly'."
        else:
            return "Please enter pet nature first."
    else:
        return "🤔 Sorry, I didn’t understand. Try asking about charges, timings, facilities, booking, or location."

# UI
user_input = st.text_input("You:")
if user_input:
    reply = chatbot_logic(user_input)
    st.write("Chatbot:", reply)
