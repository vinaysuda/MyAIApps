from datetime import datetime
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from typing import Literal

load_dotenv()


class ActionItem(BaseModel):
    task: str
    assignee: str | None = None
    due_date: datetime | None = None


class MeetingNotes(BaseModel):
    title: str
    date: datetime
    attendees: list[str]
    summary: str
    sentiment: Literal["Positive", "Neutral", "Negative"]
    action_items: list[ActionItem]
    next_meeting: datetime | None = None


# Use with OpenAI
client = OpenAI(base_url="https://demogpt4o-6358-resource.openai.azure.com/openai/v1/")

response = client.responses.parse(
    model="gpt-5-mini",
    input="""
    Meeting: Q1 Planning
    Date: January 15, 2025
    Attendees: Alice, Bob, Charlie
    
    We discussed the roadmap. Alice will prepare the budget by Friday. It is not looking good.
    Bob is handling the technical specs. Next sync on January 22.
    """,
    text_format=MeetingNotes,
)

notes = response.output_parsed
print(f"Meeting: {notes.title}")
print(f"Date: {notes.date}")
print(f"Attendees: {', '.join(notes.attendees)}")
for item in notes.action_items:
    print(f"  - {item.task} ({item.assignee})")
print(f"Sentiment: {notes.sentiment}")
