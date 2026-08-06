import pytest

from swat_welcome.app import PlanScreen, ProfileScreen, SwatWelcomeApp, WelcomeScreen


@pytest.mark.asyncio
async def test_full_click_through_shows_plan_for_selected_profile():
    app = SwatWelcomeApp()
    async with app.run_test() as pilot:
        assert isinstance(app.screen, WelcomeScreen)

        await pilot.click("#continue")
        assert isinstance(app.screen, ProfileScreen)

        # Select the first profile in the list, then show the plan.
        selection_list = app.screen.query_one("SelectionList")
        selection_list.select(selection_list.get_option_at_index(0))
        await pilot.pause()

        await pilot.click("#show-plan")
        assert isinstance(app.screen, PlanScreen)
        assert "Dry run" in app.screen._plan_text
