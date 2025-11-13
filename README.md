# 🎨 AI Wireframe Generator (Anthropic)

A Streamlit-based application that generates complete, responsive **HTML wireframes** using **Anthropic Claude 3 models**. This tool is designed for rapid prototyping, UI concept exploration, and generating multi-section website mockups with minimal effort.

---

## 🚀 Features

* Generate full **responsive HTML5 websites** with:

  * Landing, About, Features, Pricing, Contact sections
  * Smooth scrolling navigation
  * Inline CSS styling
  * Unsplash placeholder images
* Customize:

  * Page list (add/delete sections)
  * Theme color
  * Creativity level (temperature)
* Download generated HTML directly
* Streamlit-powered clean UI

---

## 🛠️ Tech Stack

* **Python 3.11+**
* **Streamlit** for the UI
* **Anthropic Claude 3 (Haiku/Sonnet/Opus)** via API
* **python-dotenv** for environment configuration

---

## 📦 Installation & Setup

### 1️⃣ Clone the project

```bash
git clone <your-repo-url>
cd ai_webpage_generator
```

### 2️⃣ Create a virtual environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install streamlit anthropic python-dotenv
```

### 4️⃣ Add your Anthropic API key

Create a `.env` file:

```bash
ANTHROPIC_API_KEY=your_api_key_here
```

---

## ▶️ Running the App

Start Streamlit:

```bash
streamlit run app.py
```

Then open the app in your browser (Streamlit will provide a link).

---

## 🧠 How It Works

1. You provide:

   * Startup name
   * Concept description
   * List of page sections
   * Theme color
   * Creativity level

2. The app sends a structured prompt to **Anthropic Claude 3**.

3. Claude returns a complete HTML wireframe.

4. You download the ready-to-open `.html` file.

---

## 📁 Project Structure

```
ai_webpage_generator/
│── app.py          # Main Streamlit application
│── .env            # API key (not committed)
│── venv/           # Virtual environment
│── README.md       # Documentation
```

---

## ⚠️ Disclaimer

This app is intended for **educational and prototyping purposes only**.
Generated HTML is **not production-ready** and should be reviewed before real deployment.

---

## 👤 Author

**Developed by:** *Alhad Bhadekar*

---

## 📄 License

This project is for personal and educational use. Add a license here if distributing.
