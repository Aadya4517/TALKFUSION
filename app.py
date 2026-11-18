from __future__ import annotations

import streamlit as st

from braille.encoder import UnsupportedCharacterError, text_to_braille
from braille.serial_device import list_serial_ports, send_braille_text

st.set_page_config(
    page_title="TalkFusion | Accessible Communication",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .block-container { padding-top: 2rem; padding-bottom: 3rem; }
      .hero { padding: 1.6rem; border: 1px solid rgba(128,128,128,.25);
              border-radius: 16px; margin-bottom: 1.25rem; }
      .muted { color: #7b8492; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("🗣️ TalkFusion")
    st.caption("Accessible multilingual communication")
    page = st.radio(
        "Navigation",
        ["Overview", "Braille Studio", "Roadmap"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Portfolio build · Phase 1")

if page == "Overview":
    st.markdown(
        """
        <div class="hero">
          <h1>Communication should have no barriers.</h1>
          <p class="muted">TalkFusion is an accessibility-first project exploring multilingual
          communication through text, voice, images and Braille.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.subheader("Project modules")
    columns = st.columns(3)
    modules = [
        ("🔤", "Text translation", "Planned", "Translate text between supported languages."),
        ("🎙️", "Voice translation", "Planned", "Convert speech to translated spoken output."),
        ("📷", "Image translation", "Planned", "Extract text from images before translation."),
        ("⠿", "Braille Studio", "Available", "Convert basic English text into on-screen Braille."),
        ("📚", "Dictionary", "Planned", "Explore definitions, synonyms and examples."),
        ("🔌", "Braille hardware", "Prototype", "Optional local serial output for compatible devices."),
    ]
    for index, (symbol, name, status, description) in enumerate(modules):
        with columns[index % 3]:
            with st.container(border=True):
                st.markdown(f"### {symbol} {name}")
                if status == "Available":
                    st.success(status)
                elif status == "Prototype":
                    st.warning(status)
                else:
                    st.info(status)
                st.write(description)

    st.info("Start with **Braille Studio** in the sidebar. The other modules will be integrated in later development phases.")

elif page == "Braille Studio":
    st.title("Braille Studio")
    st.write("Convert basic English text into uncontracted Braille characters.")
    st.caption("Prototype scope: A–Z, 0–9, common punctuation, spaces and line breaks. This is not a complete UEB transcription engine.")

    source_text = st.text_area(
        "Enter text",
        placeholder="For example: Hello, TalkFusion!\nMy room number is 204.",
        height=150,
        key="braille_source",
    )
    convert_clicked = st.button("Convert to Braille", type="primary", use_container_width=True)

    if convert_clicked:
        if not source_text.strip():
            st.warning("Enter some text before converting.")
            st.session_state.pop("braille_result", None)
        else:
            try:
                st.session_state["braille_result"] = text_to_braille(source_text)
                st.session_state["braille_error"] = None
            except (UnsupportedCharacterError, TypeError) as error:
                st.session_state["braille_result"] = None
                st.session_state["braille_error"] = str(error)

    if st.session_state.get("braille_error"):
        st.error(st.session_state["braille_error"])

    braille_result = st.session_state.get("braille_result")
    if braille_result:
        st.subheader("Braille output")
        st.text_area(
            "Braille characters",
            value=braille_result,
            height=150,
            key="braille_output_display",
            disabled=True,
        )
        st.download_button(
            "Download Braille text",
            data=braille_result.encode("utf-8"),
            file_name="talkfusion_braille.txt",
            mime="text/plain; charset=utf-8",
            use_container_width=True,
        )

        st.divider()
        st.subheader("Optional local hardware output")
        st.warning(
            "This sends UTF-8 Braille characters over a serial port. It will work only if your "
            "specific device accepts this format. Many displays and embossers require a device-specific protocol. "
            "A cloud-hosted app cannot directly access a USB device attached to your computer."
        )
        ports = list_serial_ports()
        port_options = ports if ports else ["No local serial ports detected"]
        selected_port = st.selectbox("Serial port", port_options, disabled=not ports)
        baudrate = st.number_input("Baud rate", min_value=300, max_value=115200, value=9600, step=300)
        hardware_confirmed = st.checkbox(
            "I have verified that my connected device accepts UTF-8 Braille Unicode over serial."
        )
        if st.button("Send to Braille device", disabled=not ports or not hardware_confirmed):
            try:
                bytes_written = send_braille_text(braille_result, selected_port, int(baudrate))
                st.success(f"Sent {bytes_written} bytes to {selected_port}.")
            except (RuntimeError, ValueError) as error:
                st.error(str(error))
    else:
        st.caption("Your converted Braille output will appear here.")

elif page == "Roadmap":
    st.title("Development roadmap")
    st.write("The project is being developed in testable phases instead of adding disconnected features.")
    roadmap = [
        ("Phase 1", "Project foundation and basic Braille conversion", "In progress"),
        ("Phase 2", "Shared translation service and text translation page", "Next"),
        ("Phase 3", "Image upload, OCR preview and translation", "Planned"),
        ("Phase 4", "Voice input, transcription and speech output", "Planned"),
        ("Phase 5", "Dictionary, saved words and history", "Planned"),
        ("Phase 6", "Device-specific Braille integration and deployment", "Planned"),
        ("Phase 7", "Automated testing, accessibility review and portfolio documentation", "Planned"),
    ]
    for phase, description, status in roadmap:
        with st.container(border=True):
            left, right = st.columns([4, 1])
            left.markdown(f"**{phase}**  \n{description}")
            right.write(status)

st.divider()
st.caption("TalkFusion · Built with Python and Streamlit · Accessibility-first prototype")
