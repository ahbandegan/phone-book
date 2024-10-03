from sqlite3 import *
from flet import *


class Database:
    def __init__(self):
        super().__init__()
        self.db = connect("identifier.db")
        self.cursor = self.db.cursor()

    def save(self, id, name, phone):
        self.cursor.execute(
            """
            INSERT INTO phone_number (id, username, phone_number) VALUES (?, ?, ?)
            """, (id, name, phone)
        )
        self.db.commit()

    def show(self):
        self.cursor.execute("SELECT * FROM phone_number")
        return self.cursor.fetchall()

    def delete(self, id):
        self.cursor.execute("""
        DELETE
            FROM phone_number
            WHERE id = ?
        """,(id, )
        )
        self.db.commit()

    def update(self, id , new_phone):
        self.cursor.execute(
            """
                UPDATE phone_number
                    SET phone_number = ?
                    WHERE id = ?
            """, (new_phone, id)
        )
        self.db.commit()

class Content(Row):
    def __init__(self, name:str, phone, id:int):
        super().__init__()
        self.id = id
        self.backup_phone = phone.split("\n")
        self.name = Text(name, size=20)
        self.avatar = CircleAvatar(
            content=Row(
                [
                    Text(name[0].upper(), size=20),
                ], alignment='center'
            ),
            data=self.id
        )
        self.phone = PopupMenuButton(
            items=[
                PopupMenuItem(
                    text=i,
                    on_click=self.copy
                )
                for i in self.backup_phone
            ],
            tooltip="phones number",
        )
        self.phone_edit = TextField(
            value=phone,
            multiline=True,
            width=250,
            max_lines=4
        )
        self.edit = IconButton(icon=icons.EDIT, on_click=self.edit)
        self.save = IconButton(icon=icons.SAVE, on_click=self.save)
        self.delete = IconButton(icon=icons.DELETE, on_click=self.delete)

        self.alert = AlertDialog(
            content=Column(
                [
                    self.phone_edit,
                    self.save,
                ],
                height=150
            ),
        )
        self.snake = SnackBar(
            content=Row(
                [
                    Text("phone number is copied to clipboard", color="white", size=15),
                ]
            ),
            bgcolor="#666666",
        )
        self.controls = [
            self.alert,
            self.avatar,
            self.name,
            self.phone,
            self.edit,
            self.delete,
            self.snake
        ]

    def edit(self, e):
        self.alert.open = True
        self.update()

    def save(self, e):
        self.alert.open = False
        self.phone.items.clear()
        self.backup_phone = self.phone_edit.value.split("\n")
        Database().update(self.id, self.phone_edit.value)
        for i in self.backup_phone:
            self.phone.items.append(
                PopupMenuItem(
                    text=i,
                    on_click = self.copy,
                )
            )
        self.update()

    def copy(self, e):
        copy = e.control.text.split(":")
        self.page.set_clipboard(copy[1].strip())
        self.snake.open = True
        self.update()

    def delete(self, e):
        Database().delete(int(self.avatar.data))
        self.controls.clear()
        self.update()

def main(page: Page):
    def add(e):
        if name.value != "" and phone.value != "":
            id.value = str(int(id.value) + 1)
            name.error_text = None
            phone.error_text = None
            page.close(create)
            contents.controls.append(
                Content(name.value, phone.value, id.value)
            )
            Database().save(id.value, name.value, phone.value)
            name.value = ""
            phone.value = ""
            page.update()

        if name.value == "":
            if name.value != "":
                phone.error_text = None
            name.error_text = "filling dis fild"
            page.update()

        elif phone.value == "":
            if name.value != "":
                name.error_text = None
            phone.error_text = "filling dis fild"
            page.update()

    def op(e):
        page.open(create)

    page.window.width = 500
    page.window.height = 500
    page.appbar = AppBar(
        title=Text("phone book")
    )
    page.add(Divider(5))


    id = Text("0")
    name = TextField(
        hint_text="enter name",
        width=200,
    )
    phone = TextField(
        multiline=True,
        hint_text="Press Enter to make the next few numbers",
        tooltip="title: phone number",
        width=200,
        max_lines = 4
    )
    create = AlertDialog(
        title=Text("filling"),
        content=Column(
            [
                name,
                Row(
                    [
                        phone
                    ]
                ),
                Row(
                    [
                        IconButton(
                            icon=icons.ADD,
                            on_click=add,
                            width=50,
                            height=50
                        )
                    ], alignment='center'
                )
            ],
            height=220,
        )
    )
    contents = Column()
    main_page = Container(
        border_radius= 20,
        content=contents,
        width=350,
        height=440,
        theme_mode="light"
    )

    history = Database().show()
    for (id2, name2, phone2) in history:
        id.value = id2
        contents.controls.append(
            Content(name2, phone2, int(id2))
        )

    page.overlay.append(create)
    page.floating_action_button = FloatingActionButton(
        icon=icons.ADD,
        on_click=op
    )
    page.theme_mode = "light"
    page.add(
        main_page,
    )

if __name__ == '__main__':
    app(main)