import json
import os
from collections import Counter

def run_analysis():
    if not os.path.exists("study_logs.json"):
        return None

    with open("study_logs.json", "r") as f:
        try:
            logs = json.load(f)
        except:
            return None

    if not logs:
        return None

    total_questions = len(logs)

    # Handle both key formats "query" and "user_query"
    all_words = []
    recent = []
    for log in logs:
        query = log.get("query") or log.get("user_query") or ""
        words = query.lower().split()
        all_words.extend([w for w in words if len(w) > 3])
        recent.append(query)

    top_topics = Counter(all_words).most_common(5)

    # Agent usage count
    agent_counts = Counter()
    for log in logs:
        responses = log.get("responses", {})
        for agent in responses.keys():
            agent_counts[agent] += 1

    return {
        "total": total_questions,
        "top_topics": top_topics,
        "agent_counts": dict(agent_counts),
        "recent": recent[-3:]
    }

if __name__ == "__main__":
    data = run_analysis()
    if data:
        print(f"Total questions: {data['total']}")
        print(f"Top topics: {data['top_topics']}")
        print(f"Agent usage: {data['agent_counts']}")
    else:
        print("No data yet!")
