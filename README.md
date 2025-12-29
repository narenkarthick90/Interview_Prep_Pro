# Interview Prep Pro

**Ace your next interview with personalized, AI-driven practice.**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Gemini API](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-8E75B2)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

**Interview Prep Pro** is an interactive interview simulation tool designed to help students and job seekers prepare for high-stakes technical and behavioral interviews.

Unlike static question banks, this tool uses **Google's Gemini 2.5 Flash** model to generate real-time, context-aware questions tailored to a specific **Company** (e.g., Google), **Role** (e.g., Product Manager), and **Round** (e.g., System Design). It listens to your answers and provides instant, graded feedback with a "Gold Standard" ideal answer.

## Key Features

* **Dynamic Question Engine:** Generates 20 unique, non-generic questions based on your target company and role.
* **Real-Time Evaluation:** Sophisticated AI analysis of your answers, grading you on Relevance, Clarity, and Technical Accuracy.
* **Instant Feedback Loop:** Receive actionable advice on strengths and areas for improvement immediately.
* **The "Gold Standard":** View an AI-generated "Ideal Answer" for every question to benchmark your performance.
* **Session Tracking:** Tracks your progress through the interview loop.

## Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Python)
* **AI Engine:** [Google Gemini API](https://ai.google.dev/) (Model: `gemini-2.5-flash`)
* **Language:** Python 3.x
* **Data Handling:** Streamlit Session State (No external DB required for MVP)

## Getting Started

Follow these instructions to set up the project locally.

### Prerequisites

1.  A **Google Gemini API Key** (Get it for free [here](https://aistudio.google.com/app/apikey)).

### Installation

1.  **Access the APP**
    *Use this link:
    
3.  **Access the App**
    * The app should open automatically in your browser at `http://localhost:8501`.
    * Enter your API Key in the sidebar to start simulating interviews.

## Project Structure

```bash
interview-prep-pro/
├── interview_2.py                # Main application logic
├── requirements.txt      # Python dependencies
├── README.md             # Documentation
└── .gitignore            # Files to ignore (e.g., __pycache__)
