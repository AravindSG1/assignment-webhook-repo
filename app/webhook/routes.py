# app/webhook/routes.py
from flask import Blueprint, request, jsonify
from app.extensions import mongo
from datetime import datetime, timezone, timedelta
from flask import render_template

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json

    action_type = ""
    from_branch = ""
    to_branch = ""
    request_id = ""
    author = ""

    # Handle PUSH
    if "commits" in data:
        action_type = "PUSH"
        from_branch = None
        to_branch = data["ref"].split("/")[-1]  # refs/heads/main
        request_id = data["head_commit"]["id"]
        author = data["head_commit"]["author"]["name"]

    # Handle PULL_REQUEST
    elif data.get("pull_request"):
        action_type = "PULL_REQUEST"
        pr = data["pull_request"]
        request_id = str(pr["id"])
        from_branch = pr["head"]["ref"]
        to_branch = pr["base"]["ref"]
        author = pr["user"]["login"]

        # Handle MERGE
        if pr.get("merged"):
            action_type = "MERGE"

    # Insert into Mongo
    entry = {
        "request_id": request_id,
        "author": author,
        "action": action_type,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    mongo.db.webhook_events.insert_one(entry)
    return jsonify({"status": "saved"}), 200


@webhook.route('/events', methods=["GET"])
def get_events():
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(seconds=15)  # only recent events from last 15s

    events = mongo.db.webhook_events.find({
        "timestamp": {"$gte": cutoff.isoformat()}
    }).sort("timestamp", -1)

    result = []
    for e in events:
        result.append({
            "author": e.get("author"),
            "action": e.get("action"),
            "from_branch": e.get("from_branch"),
            "to_branch": e.get("to_branch"),
            "timestamp": e.get("timestamp")
        })

    return jsonify(result), 200


@webhook.route('/', methods=["GET"])
def index():
    return render_template('index.html')


# test code remove codes below
# from flask import Blueprint
# from app.extensions import mongo

# webhook = Blueprint('webhook', __name__)

# @webhook.route('/test-db')
# def test_db():
#     try:
#         # Try to list collections in the database
#         collections = mongo.db.list_collection_names()
#         return f"Connected to MongoDB! Collections: {collections}"
#     except Exception as e:
#         return f"Database connection failed: {str(e)}"