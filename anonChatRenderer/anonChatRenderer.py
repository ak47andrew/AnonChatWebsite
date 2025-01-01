import reflex as rx
from typing import Optional, List
from pymongo import MongoClient
from dataclasses import dataclass

@dataclass
class Message:
    dialog_id: str
    name: str
    pfp: Optional[str]
    is_me: bool
    content: str
    attachment: Optional[str]

class State(rx.State):
    messages_cache: List[Message] = []
    chat_summaries_cache: dict = {}
    selected_dialog_id: str = ""


    def fetch_data(self):
        client = MongoClient('localhost', 27017)
        db = client.anonChatAutoSkip
        my_id = "192db419-684b-4865-a2fa-443963a14976"

        all_messages = []

        # Fetch from 'messages' and 'my_messages'
        for collection_name in ["messages", "my_messages"]:
            messages = list(db[collection_name].find())
            for msg in messages:
                partner = db.partners.find_one({"partner": msg["sender"]})
                if partner:
                    all_messages.append(
                        Message(
                            dialog_id=msg["dialogId"],
                            name=partner["username"],
                            pfp=partner["profilePicture"],
                            is_me=msg["sender"] == my_id,
                            content=msg["text"],
                            attachment=msg.get("uri"), # Use get to handle missing uri
                        )
                    )
                else:
                    print(f"Warning: Partner not found for sender {msg['sender']}") #or handle differently
                    all_messages.append(
                        Message(
                            dialog_id=msg["dialogId"],
                            name="Unknown",  # Or some default
                            pfp=None,
                            is_me=msg["sender"] == my_id,
                            content=msg["text"],
                            attachment=msg.get("uri"),
                        )
                    )


        self.messages_cache = all_messages
        self.generate_chat_summaries()
        client.close()


    def generate_chat_summaries(self):
        summaries = {}
        for msg in self.messages_cache:
            if msg.dialog_id not in summaries:
                summaries[msg.dialog_id] = {
                    "partner_name": msg.name,
                    "pfp": msg.pfp,
                    "message_count": 0,
                    "has_attachment": False,
                }
            summaries[msg.dialog_id]["message_count"] += 1
            if msg.attachment:
                summaries[msg.dialog_id]["has_attachment"] = True
        self.chat_summaries_cache = summaries

    @rx.var
    def all_messages(self) -> List[Message]:
        if not self.messages_cache:
            self.fetch_data()
        return self.messages_cache

    @rx.var
    def chat_summaries(self):
        if not self.chat_summaries_cache:
            self.fetch_data()
        return self.chat_summaries_cache

    @rx.var
    def selected_chat_messages(self) -> List[Message]:
        return [msg for msg in self.all_messages if msg.dialog_id == self.selected_dialog_id]

    def select_chat(self, dialog_id: str):
        self.selected_dialog_id = dialog_id
        return rx.redirect(f"/chat/{dialog_id}")


def index():
    ...


def chat_detail(dialog_id:str):
    ...


app = rx.App()
app.add_page(index)
app.add_page(chat_detail, route="/chat/[dialog_id]",on_load=State.fetch_data)
