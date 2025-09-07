Perfect ✅ I’ll draft a detailed **README.md** so anyone can set up and run your chatbot project easily.

Here’s the file content I’ll generate and add into your project root:

---

# 🤖 Chatbot with Hugging Face API

This project is a **Node.js + Express web app** that serves a chatbot interface.
It uses the **Hugging Face Inference API** (default: `facebook/blenderbot-400M-distill`) as the conversation model.

---

## 🚀 Features

* Frontend UI for chatting with an AI bot
* Backend proxy (`/api/chat`) that connects securely to Hugging Face API
* Environment-based configuration (`.env`)
* Hot reload with `nodemon` during development
* Ready for local testing or deployment

---

## 📂 Project Structure

```
.
├── public/            # Frontend files (index.html, css, js)
├── server.js          # Express backend
├── package.json       # Node.js dependencies
├── .env.example       # Sample environment variables
└── README.md          # Project guide
```

---

## 🛠️ Installation

1. **Clone or unzip the project**

   ```bash
   git clone <your-repo-url>
   cd chatbot-hf
   ```

   *(or unzip the provided `site_fixed_hf.zip`)*

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Set environment variables**
   Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

---

## 🔑 Hugging Face API Token Setup

1. Go to 👉 [https://huggingface.co/join](https://huggingface.co/join) and create a free account.
2. After logging in:

   * Navigate to **Settings → Access Tokens**
   * Create a **New token** with role **Read**
   * Copy the generated token (looks like `hf_xxxxxxxxxxxxx`)
3. Open `.env` and add your token:

   ```env
   HF_API_KEY=hf_your_token_here
   PORT=3000
   ```

---

## ▶️ Running the App

Start the development server:

```bash
npm run dev
```

Or run in production:

```bash
npm start
```

Then open your browser at:
👉 [http://localhost:3000](http://localhost:3000)

---

## 💬 Usage

* Type a message in the chat box and press **Send**
* The backend forwards it to Hugging Face API
* Response is displayed in the chat window

---

## ⚡ Changing the Model

By default, the backend uses:

```
facebook/blenderbot-400M-distill
```

To switch models:

1. Open `server.js`
2. Find this line:

   ```js
   const response = await fetch("https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill", {
   ```
3. Replace with another Hugging Face model (e.g., `microsoft/DialoGPT-medium`).

---

## 📦 Dependencies

* [Express](https://expressjs.com/) – server framework
* [dotenv](https://www.npmjs.com/package/dotenv) – environment variables
* [node-fetch](https://www.npmjs.com/package/node-fetch) – HTTP requests
* [nodemon](https://www.npmjs.com/package/nodemon) – dev auto-reload

---

## ⚠️ Notes

* Free Hugging Face models may be **slower** and **rate-limited**
* For heavier usage, consider hosting your own model on Hugging Face Spaces or using a paid plan
* If `HF_API_KEY` is missing, the chatbot **will not work**
