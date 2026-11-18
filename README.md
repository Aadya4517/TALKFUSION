# TalkFusion

TalkFusion is an accessibility-first multilingual communication project. The long-term goal is to bring text, speech, image-based text extraction, dictionary support and Braille into one web application.

## Current status

**Phase 1 foundation is in progress.** The working feature is a basic English-to-Braille Studio with on-screen Unicode output and an optional local serial transport prototype.

| Module | Status | Notes |
| --- | --- | --- |
| Basic English Braille | Available | A–Z, digits, common punctuation, spaces and line breaks |
| Local serial output | Prototype | Sends UTF-8 Braille Unicode; requires compatible device/protocol |
| Text translation | Planned | Shared translation service in a later phase |
| Voice translation | Planned | Speech recognition and translated speech output |
| Image translation | Planned | Image upload, OCR review and translation |
| Dictionary | Planned | Definitions, examples, synonyms and antonyms |

## Run locally

Use Python 3.10 or newer.

```bash
python -m venv .venv
```

Activate your environment, then install dependencies:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Legacy module dependencies

The original standalone scripts are preserved in the repository but are not yet wired into the new Streamlit application. To experiment with those older modules, install their separate dependencies with `pip install -r requirements-legacy.txt`. Some packages, especially PyAudio and Tesseract, require operating-system-specific setup. The main `requirements.txt` intentionally contains only what the Phase 1 application needs.

## Braille scope and limitations

The first converter is a deliberately small, uncontracted English Braille prototype. It supports the English alphabet, digits, a limited set of punctuation marks, spaces and line breaks. It does **not** implement all Unified English Braille (UEB) rules, contractions, foreign-language Braille, technical notation or full transcription formatting. Do not use it as a substitute for certified Braille transcription.

## Hardware notes

The serial feature is an optional local prototype. It sends Braille Unicode encoded as UTF-8. Many refreshable Braille displays and embossers require a manufacturer-specific protocol, command framing or character encoding. Confirm the exact model and documentation before connecting hardware.

A Streamlit app hosted in the cloud runs on a remote server and cannot directly access a USB serial device connected to a user's own computer. Hardware testing should initially be done with TalkFusion running locally. A deployed version would need a separate local hardware bridge or device-specific client.

## Planned architecture

```text
app.py                    Streamlit entry point
braille/encoder.py        Pure text-to-Braille conversion logic
braille/serial_device.py  Optional local serial transport
tests/                    Automated unit tests
```

Later phases will introduce reusable translation, speech, OCR and dictionary services, keeping UI code separate from processing logic.

## Standards reference

For standards work, refer to the [International Council on English Braille (ICEB)](https://iceb.org/publications/ueb/) and its current Rules of Unified English Braille. This prototype is not a complete UEB implementation.

## License

No license has been selected yet. Add an appropriate license before inviting external contributions or distributing the project.
