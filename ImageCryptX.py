import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

# Styling using HTML and CSS
st.markdown("""
    <style>
        .big-font {
            font-size: 36px;
            font-weight: bold;
            color: #0000FF !important; /* Force blue color for the title */
            text-align: center;
            margin-bottom: 20px;
        }
        .about-me {
            font-size: 18px;
            text-align: left;
        }
        .subheading {
            font-size: 22px;
            font-weight: bold;
            margin-top: 20px;
            
        }
        .list-item {
            font-size: 18px;
            color: #333333;
            margin-left: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# XOR Encryption Function
def xor_encrypt(image, key):
    np.random.seed(key)
    image_array = np.array(image)  # Convert to NumPy array
    random_array = np.random.randint(0, 256, image_array.shape, dtype=np.uint8)
    encrypted_image = np.bitwise_xor(image_array, random_array)
    return Image.fromarray(encrypted_image)

# Reverse Pixels Function
def reverse_pixels(image):
    image_array = np.array(image)
    reversed_image = np.flip(image_array, axis=1)
    return Image.fromarray(reversed_image)

# Grayscale Encryption Function
def grayscale_encrypt(image):
    return image.convert("L")

# Add Noise Function
def add_noise(image):
    image_array = np.array(image)
    noise = np.random.randint(0, 50, image_array.shape, dtype=np.uint8)
    noisy_image = np.clip(image_array + noise, 0, 255)
    return Image.fromarray(noisy_image)

# Shift Rows Function
def shift_rows(image):
    image_array = np.array(image)
    shifted_image = np.roll(image_array, shift=10, axis=0)
    return Image.fromarray(shifted_image)

# Main App Function
def main():
    st.sidebar.title("🔒 ImageCryptX")
    page = st.sidebar.radio("Select Page", ["Home", "Encryption", "Decryption"])

    # Home Page
    if page == "Home":
        st.markdown('<h3 class="big-font">🔒 Welcome to ImageCryptX 🔒</h3>', unsafe_allow_html=True)
        st.markdown('<p class="subheading">👋 About Me</p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="about-me">
        Hi, I’m <b>Hafiz Sharjeel Shakeel</b>, a <b>Cybersecurity Penetration Tester and Ethical Hacker</b> passionate about building secure tools and exploring advanced encryption techniques. 
        This tool is designed to demonstrate simple yet effective image encryption and decryption methods.
        </p>
        """, unsafe_allow_html=True)

        st.markdown('<p class="subheading">🛠️ How to Use This Tool</p>', unsafe_allow_html=True)
        st.markdown("""
        <ol class="about-me">
            <li>Navigate to the <b>Encryption</b> page using the sidebar.</li>
            <li>Upload an image and select your desired encryption technique.</li>
            <li>Provide a key (if required), and click <b>Encrypt Image</b>.</li>
            <li>Download the encrypted image.</li>
            <li>To decrypt, visit the <b>Decryption</b> page, upload the encrypted image, and follow similar steps.</li>
        </ol>
        """, unsafe_allow_html=True)

        st.markdown('<p class="subheading">🔑 Techniques Used</p>', unsafe_allow_html=True)
        st.markdown("""
        <ul class="about-me">
            <li><b>XOR Encryption:</b> A reversible encryption technique using pixel manipulation.</li>
            <li><b>Reverse Pixels:</b> Reverses the pixel order of the image.</li>
            <li><b>Shift Rows:</b> Shifts rows of pixels based on a fixed offset.</li>
            <li><b>Grayscale Encryption:</b> Converts the image to grayscale for obfuscation.</li>
            <li><b>Add Noise:</b> Adds random noise to the image to obscure original content.</li>
        </ul>
        <p class="about-me">This tool is built using <b>Streamlit</b>, <b>Python</b>, and <b>Pillow</b>.</p>
        """, unsafe_allow_html=True)

    # Encryption Page
    elif page == "Encryption":
        st.markdown('<h3 class="big-font">🔐 Image Encryption</h3>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload an image to encrypt", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Original Image", use_column_width=True)

            # Select encryption technique
            technique = st.selectbox("Select Encryption Technique", ["XOR Encryption", "Reverse Pixels", "Shift Rows", "Grayscale Encryption", "Add Noise"])
            key = None

            if technique == "XOR Encryption":
                key = st.number_input("Enter an encryption key (integer)", min_value=0, max_value=100000, value=12345)
                encrypted_image = xor_encrypt(image, key)
            elif technique == "Reverse Pixels":
                encrypted_image = reverse_pixels(image)
            elif technique == "Shift Rows":
                encrypted_image = shift_rows(image)
            elif technique == "Grayscale Encryption":
                encrypted_image = grayscale_encrypt(image)
            elif technique == "Add Noise":
                encrypted_image = add_noise(image)

            st.image(encrypted_image, caption="Encrypted Image", use_column_width=True)

            # Download encrypted image
            buffer = BytesIO()
            encrypted_image.save(buffer, format="PNG")
            st.download_button("Download Encrypted Image", buffer.getvalue(), file_name="encrypted_image.png")

    # Decryption Page
    elif page == "Decryption":
        st.markdown('<h3 class="big-font">🔓 Image Decryption</h3>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload an encrypted image to decrypt", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Encrypted Image", use_column_width=True)

            technique = st.selectbox("Select Decryption Technique", ["XOR Decryption"])
            if technique == "XOR Decryption":
                key = st.number_input("Enter the encryption key (integer used during encryption)", min_value=0, max_value=100000, value=12345)
                decrypted_image = xor_encrypt(image, key)  # XOR is reversible
                st.image(decrypted_image, caption="Decrypted Image", use_column_width=True)

                # Download decrypted image
                buffer = BytesIO()
                decrypted_image.save(buffer, format="PNG")
                st.download_button("Download Decrypted Image", buffer.getvalue(), file_name="decrypted_image.png")

if __name__ == "__main__":
    main()
