from typing import List, Optional
from dataclasses import dataclass
import pymongo
from pymongo.collection import Collection

@dataclass
class Message:
    dialog_id: str
    name: str
    pfp: Optional[str]
    is_me: bool
    content: str
    attachment: Optional[str]

def fetch_messages_from_db() -> List[Message]:
    client = pymongo.MongoClient("localhost", 27017)
    db = client["anonChatAutoSkip"]
    messages_collection: Collection = db["messages"]
    my_messages_collection: Collection = db["my_messages"]
    partners_collection: Collection = db["partners"]

    all_messages = list(messages_collection.find()) + list(my_messages_collection.find())

    chat_messages: List[Message] = []
    for msg in all_messages:
        partner = partners_collection.find_one({"partner": msg.get("sender")})
        username = partner.get("username") if partner else "Unknown" # Fallback if partner not found
        profile_picture = partner.get("profilePicture") if partner else None # Fallback

        chat_messages.append(
            Message(
                dialog_id=msg.get("dialogId"),
                name=username,
                pfp=profile_picture,
                is_me=msg.get("sender") == "192db419-684b-4865-a2fa-443963a14976",
                content=msg.get("text"),
                attachment=msg.get("uri"),
            )
        )
    client.close()
    return chat_messages
