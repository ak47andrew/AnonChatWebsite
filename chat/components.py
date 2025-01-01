import reflex as rx
from .utils import Message
from typing import List

def chat_bubble(message: Message):
    return rx.box(
        rx.hstack(
            rx.cond(
                message.pfp,
                rx.avatar(src=message.pfp, size="sm", name=message.name,bg="lightgray"),
                rx.avatar(name=message.name, size="sm",bg="lightgray")
            ),

            rx.text(message.name, font_weight="bold"),
            spacing="2",
             align_items="center"

        ),


        rx.text(message.content),
        rx.cond(
            message.attachment,
            rx.cond(
                message.attachment.endswith((".mp4", ".webm", ".ogg")),  # Basic video check
                rx.video(url=message.attachment, width="250px", controls=True),
                rx.image(src=message.attachment, width="250px", border_radius="md"),
            ),
        ),

        padding="1em",
        border_radius="lg",
        margin_bottom="0.5em",
        bg="lightgray" if not message.is_me else "lightblue",
        align_self="start" if not message.is_me else "end",
        max_width="60%",
    )

def chat_view(messages: List[Message], partner_name:str, pfp:str):
  return rx.container(
        rx.vstack(
            rx.heading(f"Chat with {partner_name}", size="5"),
              rx.hstack(
                rx.cond(
                    pfp,
                    rx.avatar(src=pfp, size="md", name=partner_name, bg="lightgray"),
                    rx.avatar(name=partner_name, size="md", bg="lightgray")
                ),

                rx.text(f"Partner: {partner_name}"),
                spacing="2",
                align_items="center"

             ),


            rx.divider(),

            rx.foreach(messages, chat_bubble),

            width="100%",
            padding="1em",
        ),
        max_width="800px",

    )
