# 🌐 Multi Language Translator

A simple Python-based **multi-language text translator** that helps you translate text between different languages.  
The project is designed to be beginner-friendly and easy to extend, using a separate configuration file to manage supported languages.

---

## ✨ Features

- 🔁 Translate text between multiple languages  
- 📂 Uses a `language.json` file to manage supported languages and codes  
- 🧱 Clean, minimal project structure  
- 💡 Easy to customize and extend (add new languages or change the UI/logic)

---

## 🗂 Project Structure

```
Multi_language_translator/
│
├── app.py            # Main application script (core translation logic + interface)
├── language.json     # List / mapping of supported languages and their codes
├── requirements.txt  # Python dependencies
└── .gitattributes    # Git settings (line endings, text normalization, etc.)
```

---

## ✅ Prerequisites

- Python 3.8+ installed  
- `pip` installed (comes with most Python installations)

---

## 🔧 Installation

1. **Clone the repository**

```
git clone https://github.com/arya-nsv/Multi_language_translator.git
cd Multi_language_translator
```

2. **Create a virtual environment (optional but recommended)**

```
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate   # macOS / Linux
```

3. **Install dependencies**

```
pip install -r requirements.txt
```

---

## 🚀 Usage

1. Run the application:

```
python app.py
```

2. Follow the application interface to:
- Select source & target languages  
- Enter text  
- View translation  

---

## 🌍 Managing Languages (`language.json`)

Example structure:

```
{
  "en": "English",
  "fr": "French",
  "es": "Spanish",
  "de": "German"
}
```

---

## 🛠️ Customization Ideas

- Add error handling  
- Add translation history  
- Build a GUI using Tkinter / Streamlit  
- Add text‑to‑speech  

---

## 🤝 Contribution

1. Fork  
2. Create a branch  
3. Commit changes  
4. Open a pull request  

---

## 👤 Author  
Developed by **Arya**.
