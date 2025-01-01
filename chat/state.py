import reflex as rx
from .utils import fetch_messages_from_db, Message
from typing import List, Dict, Any, Optional


class State(rx.State):
    """The app state."""

    chats: List[Dict[str, Any]] = []
    selected_chat: Optional[str] = None
    current_chat_messages: List[Message] = []
    is_loading: bool = False # Add a loading indicator

    def get_chats(self):
        self.is_loading = True
        all_messages = fetch_messages_from_db()

        chats_summary: Dict[str, Dict[str, Any]] = {}
        for msg in all_messages:
            dialog_id = msg.dialog_id
            if dialog_id not in chats_summary:
                chats_summary[dialog_id] = {
                    "dialog_id": dialog_id,
                    "partner_name": msg.name,
                    "pfp": msg.pfp,
                    "message_count": 0,
                    "has_attachment": False,
                }
            chats_summary[dialog_id]["message_count"] += 1
            if msg.attachment:
                chats_summary[dialog_id]["has_attachment"] = True

        self.chats = list(chats_summary.values())
        self.is_loading = False  # Set loading to false after data is fetched
        if self.selected_chat: # Refresh messages if a chat was already selected
            self.get_chat_messages()


    def select_chat(self, dialog_id: str):
        self.selected_chat = dialog_id
        self.get_chat_messages()

    def get_chat_messages(self):
        if not self.selected_chat: return []

        all_messages = fetch_messages_from_db()
        self.current_chat_messages = [
            msg for msg in all_messages if msg.dialog_id == self.selected_chat
        ]
        return self.current_chat_messages

    def go_back(self):
        self.selected_chat = None
        self.current_chat_messages = []
