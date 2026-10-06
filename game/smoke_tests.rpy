# Run with: renpy.sh PATH_TO_PROJECT test basic_tactics
testsuite basic_tactics:
    teardown:
        exit

    testcase launch_move_reset:
        pause until screen "tactics_demo"
        assert eval (tactics_view.state.selected_uid == "knight")
        screenshot "demo-start.png"

        # Click the visible part of the scout, then an adjacent ground tile.
        click pos (430, 350)
        assert eval (tactics_view.state.selected_uid == "scout")
        click pos (376, 347)
        assert eval (tactics_view.state.selected.cell.x == 0 and tactics_view.state.selected.cell.y == 4 and tactics_view.state.selected.cell.z == 0)
        screenshot "demo-moved.png"

        # Tapping outside the board must leave the unit in place.
        click pos (50, 650)
        assert eval (tactics_view.state.selected.cell.x == 0 and tactics_view.state.selected.cell.y == 4)

        click "RESET"
        assert eval (tactics_view.state.selected_uid == "knight")
        assert eval (tactics_view.state.units[1].cell.x == 1 and tactics_view.state.units[1].cell.y == 4 and tactics_view.state.units[1].cell.z == 0)
        screenshot "demo-reset.png"
