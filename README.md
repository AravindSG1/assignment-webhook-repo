# 📡 Webhook Receiver – Flask App

This repository contains the backend application for receiving and processing GitHub webhook events like **push**, **pull request**, and **merge** actions. It is designed to integrate with a companion repo (e.g., [`action-repo`](https://github.com/AravindSG1/assignment-action-repo)) that triggers GitHub webhooks.

---

## 🔧 Tech Stack

- **Python 3 / Flask** – Backend framework
- **MongoDB** – Storage for webhook events
- **Flask-PyMongo** – MongoDB integration with Flask
- **HTML + JS** – Simple UI for viewing events

---

## 📬 What It Does

- Receives webhook events via:  
  `POST /webhook/receiver`
- Stores them in MongoDB with relevant info:  
  `action`, `author`, `branches`, `timestamp`
- Provides a simple UI that polls every 15 seconds:  
  `GET /webhook/events`

Supported GitHub actions:
- `PUSH`
- `PULL_REQUEST`
- `MERGE` (optional for bonus)

---

## 🚀 How to Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/your-username/webhook-repo.git
cd webhook-repo  
```

### 2. Set up environment
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Start MongoDB
Ensure MongoDB is running locally on:
``` 
mongodb://localhost:27017/database 
```
### 4. Run the Flask server
```
python run.py
```
Server will run on:  
`http://127.0.0.1:5000`

## 🔁 Webhook Routes
### 🔹 POST /webhook/receiver
This is the GitHub webhook endpoint. It receives events and stores them in MongoDB.

Example payload:
```
{
  "request_id": "commit_or_pr_id",
  "author": "username",
  "action": "PUSH",
  "from_branch": "dev",
  "to_branch": "main"
}

```
### 🔹 GET /webhook/events
Returns the latest 20 webhook events (within the last 15 seconds) for the frontend to display.

## 🖥️ Web UI
- Simple HTML + JS frontend polls every 15s

- Automatically updates latest GitHub activity

- Handles event formatting for:

    - PUSH: `Alice pushed to main on <time>`

    - PULL_REQUEST: `Bob submitted a pull request from dev to main on <time>`

    - MERGE: `Charlie merged branch dev to main on <time>`

## 📎 Linked Repository
This `webhook-repo` works together with the GitHub webhook sender repo:
👉 [`action-repo`](https://github.com/AravindSG1/assignment-action-repo)

## 🛡️ Notes
- Ensure MongoDB is running before you start the Flask server.

- Time is stored and displayed in UTC format.