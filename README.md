# appzlogic-test

This repository is a simple full-stack chat application built with a React/TypeScript frontend and a FastAPI backend. The app communicates with an external chatbot API (using the Hugging Face Inference API with BlenderBot) and provides a WhatsApp-like chat interface.

## Table of Contents

### Prerequisites

- **Backend:** Python 3.7+ installed.
- **Frontend:** Node.js and npm installed.

### Backend Setup

\`\`\`bash
cd backend

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
\`\`\`

### Frontend Setup

\`\`\`bash
cd frontend
npm install
npm start
\`\`\`



### Tests

\`\`\`bash
cd backend
python -m pytest
\`\`\`

\`\`\`bash
cd frontend
npm test
\`\`\`