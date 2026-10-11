# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Internship (August–October) 2026

> 🎓 This project was built during the [ **Tips Hindawi** ](https://www.tipshindawi.com/) **Internship (August–October) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        | tasnim ahmed mohamed                 |
| Project Name     | Echoes of Time: AI Memoir & Illustration |
| GitHub Username  | tasnim20ahmed                        |
| Internship Batch | August–October 2026                  |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en)[cite: 5]                         |

---

# 📖 Project Overview

Echoes of Time is an interactive, AI-driven biographical application designed to transform spoken or typed personal memories into timeless, literary autobiography chapters accompanied by custom 35mm film illustrations. The platform bridges a local Streamlit frontend with cloud-hosted generative AI backends (Qwen on Kaggle and SDXL on Google Colab).

---

# ✨ Features

* **Interactive AI Biographer:** Conducts a live interview via text or voice input, asking thoughtful, personalized follow-up questions to help users explore their memories deeper.
* **Smart Voice Integration:** Features speech-to-text transcription and text-to-speech audio playback for a seamless conversational experience.
* **Structured Narrative Extraction:** Utilizes Qwen 2.5 (7B-Instruct) running in 4-bit quantization, coupled with LangChain and Pydantic, to parse transcripts into strict JSON memoir schemas.
* **Context-Aware RAG Pipeline:** Integrates FAISS vector search with Hugging Face embeddings to retrieve historical and cultural context, enriching the biographical tone.
* **AI Visual Generation:** Connects to an external image generation backend (SDXL) to paint vintage-style photographs matching the narrative.
* **Custom Vintage UI:** Styled with a bespoke beige and olive-green theme for an immersive personal journaling aesthetic.

---

# 🛠️ Technologies Used

* **Frontend:** Streamlit, HTML/CSS
* **Orchestration & Parsing:** LangChain, Pydantic
* **AI & Machine Learning:** PyTorch, Hugging Face Transformers, Qwen 2.5 7B, FAISS, Sentence-Transformers
* **Audio & Speech:** `speech_recognition`, `audio_recorder_streamlit`, `gTTS`
* **Backend Networking:** FastAPI, Uvicorn, Ngrok

---

# ⚙️ Installation

Explain how to install and run the project.

---

# 🚀 Usage

* Connect the Backends: At the very top of the page, paste your Kaggle and Colab ngrok URLs into the "Backend Connections" input boxes to link the AI models to the website.

* Share a Memory: Use the chat area at the bottom of the screen. You can either click the microphone icon to tell your story out loud or type your memory into the text box.

* Chat with the Biographer: The AI will listen to your memory, read it aloud using text-to-speech, and ask you a thoughtful follow-up question. Answer the question to add more depth, sensory details, and emotions to your story.

* Generate the Chapter: Once you feel you have shared enough details, click the "See the memory" button.

* View Your Memoir: The website will process your conversation and display a beautifully written autobiography chapter—complete with a title, life era, location, and core wisdom—alongside a custom vintage 35mm photograph of your memory.

* Regenerate (Optional): If you want a different visual interpretation of your story, click the "Regenerate Photo" button to paint a new picture.

---

# 📸 Demo

[Watch the Video Demo Here](https://your-video-link-here.com)

---

# 📈 Results

The application successfully manages a distributed architecture, leveraging cloud GPUs for heavy LLM inference and image generation while maintaining a lightweight local frontend. It accurately extracts structured JSON narratives from natural conversation and generates highly relevant, stylized images that match the emotional tone of the user's memory.

---

# 🔮 Future Improvements

* Implement multilingual support for Arabic language generation and text-to-speech.

* Add a feature to export the finalized memoir chapters and images into a downloadable PDF book.

* Expand the FAISS vector database with more diverse historical and cultural eras.

---

# 📚 About the Internship

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Internship (August–October) 2026**, and it will be showcased on the official [Tips Hindawi](https://www.tipshindawi.com/) website.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the internship encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the internship, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.
