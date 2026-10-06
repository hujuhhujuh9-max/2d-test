define config.name = "RenFletPy 2D Test"
define config.version = "0.1.0"
define config.main_menu = False
define config.save_directory = "renfletpy-2d-test"
define config.screen_width = 1280
define config.screen_height = 720

init -10 python:
    from tactics import TacticsDisplayable, run_self_test

    run_self_test()
    tactics_view = TacticsDisplayable()

screen tactics_demo():
    add tactics_view

    frame:
        xalign 0.015
        yalign 0.02
        background Solid("#cc171a20")
        padding (18, 14)

        vbox:
            spacing 4
            text "RENFLETPY / 2D TEST" size 25 bold True
            text "Pure 2D - board[z][y][x] - face-level overlap" size 16 color "#b8bec8"
            text "Tap a blue unit, then tap a blue tile." size 16 color "#d9dde3"

    hbox:
        xalign 0.985
        yalign 0.02
        spacing 10

        textbutton "RESET":
            action Function(tactics_view.reset)
            xminimum 120
            yminimum 54

        textbutton "QUIT":
            action Quit(confirm=False)
            xminimum 100
            yminimum 54

label start:
    show screen tactics_demo
    $ renpy.pause(hard=True)
    jump start
