# 👗 Outfit Finder

An AI-powered outfit analysis and shopping recommendation application that identifies clothing items from uploaded images and helps users find similar products online.

## Overview

Outfit Finder uses Google's Gemini AI to analyze outfit images, identify individual clothing items, and generate detailed descriptions of their colors and styles.

The application then uses the identified clothing information to search for similar products online, helping users discover items that match the original outfit.

The goal of this project is to combine multimodal AI, full-stack development, and shopping API integration into one interactive application.

## Features

- **AI Image Recognition:** Upload an outfit image and use Gemini AI to identify individual clothing items.
- **Clothing Classification:** Identify clothing categories, colors, and styles.
- **Confidence Scores:** Display AI confidence scores for identified items.
- **Automated Search Queries:** Generate product search terms based on the clothing analysis.
- **Product Discovery:** Search Google Shopping for similar clothing items.
- **Product Comparisons:** View product information, prices, merchants, and images.
- **Interactive Interface:** Explore identified clothing items and shopping results through a React frontend.

## Tech Stack

**Frontend**
- React
- TypeScript
- Vite
- CSS

**Backend**
- Python
- FastAPI
- Pydantic
- REST APIs

**AI & External Services**
- Google Gemini API for multimodal image analysis
- SerpApi for Google Shopping search results

## How It Works

1. **Image Upload:** The user uploads an image containing an outfit.
2. **AI Analysis:** The backend sends the image to Google's Gemini API for analysis.
3. **Item Identification:** Gemini identifies clothing items and generates structured information, including category, color, style, description, and confidence score.
4. **Product Search:** The application uses the generated search queries to retrieve similar products through SerpApi.
5. **Results Display:** The frontend presents the identified outfit items and matching shopping results.

## Architecture

The application follows a full-stack architecture:

- **React frontend:** Handles image uploads, user interactions, and displaying results.
- **FastAPI backend:** Manages API requests, image analysis, and shopping searches.
- **Gemini integration:** Processes uploaded images and returns structured clothing information.
- **SerpApi integration:** Retrieves relevant shopping products and pricing information.

## Getting Started

### Prerequisites

- Python 3
- Node.js and npm
- Google Gemini API key
- SerpApi API key

### 1. Clone the repository

```bash
git clone https://github.com/pavithrarajan26/outfit-finder.git
cd outfit-finder
```

### 2. Set up the backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file inside the `backend` directory:

```env
GEMINI_API_KEY=your_gemini_api_key
SERPAPI_KEY=your_serpapi_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Replace the placeholder values with your own API keys. Never commit your `.env` file to GitHub.

### 4. Start the backend

```bash
fastapi dev main.py
```

The backend documentation is available at:

`http://127.0.0.1:8000/docs`

### 5. Set up the frontend

Open a second terminal window:

```bash
cd outfit-finder/frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in your browser.

## Future Improvements

- Save analyzed outfits and shopping results.
- Add filters for price, brand, and clothing category.
- Improve product matching based on image similarity.
- Add user accounts and personalized recommendations.
- Deploy the application for public access.

## Author

**Pavithra Rajan**  
Computer Science and Engineering Student

[GitHub](https://github.com/pavithrarajan26)

## App Screenshots

### AI Outfit Analysis

![Outfit analysis results](outfit-analysis.png)
