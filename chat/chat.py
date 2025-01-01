import reflex as rx
from .state import State
from .components import chat_view, chat_bubble
from typing import List, Dict, Any


def index() -> rx.Component:
    return rx.container(
        rx.cond(
            State.is_loading,
            rx.spinner(size='3'), # Show spinner when loading
            rx.cond(
                State.selected_chat,
                rx.vstack(
                    rx.button("Back", on_click=State.go_back, margin_bottom="1em"),

                    chat_view(State.current_chat_messages,
                            next((chat['partner_name'] for chat in State.chats if chat['dialog_id'] == State.selected_chat), "Unknown"),
                            next((chat['pfp'] for chat in State.chats if chat['dialog_id'] == State.selected_chat), None)
                            ),

                ),


                rx.grid(
                    rx.grid_item(
                        rx.text("Chats", font_size="2xl"),
                         row_span=1,
                         col_span=5,
                         padding_bottom="1em"
                    ),
                    *[
                        rx.grid_item(
                            rx.vstack(
                                rx.hstack(
                                     rx.cond(
                                        chat["pfp"],
                                        rx.avatar(src=chat["pfp"], size="md", name=chat["partner_name"], bg="lightgray"),
                                        rx.avatar(name=chat["partner_name"], size="md", bg="lightgray")
                                    ),
                                    rx.text(chat["partner_name"]),
                                    spacing="2",
                                    align_items="center"
                                ),


                                rx.text(f"Messages: {chat['message_count']}"),
                                rx.cond(
                                    chat["has_attachment"],
                                    rx.icon(tag="attachment"),

                                ),

                                padding="1em",
                                border="1px solid lightgray",
                                border_radius="md",
                                cursor="pointer",
                                _hover={"bg": "lightgray"},

                            ),
                            row_span=1,
                            col_span=1,
                            on_click=lambda id=chat["dialog_id"]: State.select_chat(id) # Capture dialog_id correctly

                        )
                        for chat in State.chats
                    ],
                    template_columns="repeat(5, 1fr)",  # 5 columns
                    gap=4,
                    width="100%",
                    padding="1em",
                ),
            )
        ),

        on_mount=State.get_chats,

    )

# Add state and page to the app.
app = rx.App()
app.add_page(index, on_load=State.get_chats) #Crucially call get_chats on load of the main page.
