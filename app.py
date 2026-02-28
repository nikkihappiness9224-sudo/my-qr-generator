import streamlit as st
import qrcode
from io import BytesIO

st.title("QR Code Generator")

# Get input from user
url = st.text_input("Enter the URL or text:")

if url:
    # Generate the QR code
    qr = qrcode.make(url)
    
    # Save to a memory buffer
    buf = BytesIO()
    qr.save(buf, format="PNG")
    byte_im = buf.getvalue()

    # Show the image on the website
    st.image(byte_im, caption="Your Generated QR Code")

    # Add a download button
    st.download_button(
        label="Download Image",
        data=byte_im,
        file_name="qr_code.png",
        mime="image/png"
    )