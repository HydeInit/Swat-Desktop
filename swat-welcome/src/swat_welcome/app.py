"""SWAT Welcome - first-run profile selection prototype.

Reads profiles, lets the user pick some, and shows a dry-run plan.
Installs nothing, touches nothing outside its own terminal window."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, SelectionList, Static

from swat_cli.profile import ProfileError, load_profiles
from swat_welcome.plan import build_plan


class WelcomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(
                "Welcome to SWAT.\n\n"
                "This is a preview of profile-based setup - pick the kind of "
                "development work you'll be doing, and see what would be set "
                "up for you. Nothing is installed by this preview.",
                id="welcome-text",
            ),
            Button("Continue", id="continue", variant="primary"),
            id="welcome-body",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "continue":
            self.app.push_screen(ProfileScreen())


class ProfileScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        try:
            profiles = load_profiles()
        except ProfileError as exc:
            yield Static(f"Could not load profiles: {exc}", id="profile-error")
            yield Footer()
            return

        self._profiles = {p.id: p for p in profiles}
        options = [(f"{p.name} - {p.description}", p.id) for p in profiles]
        yield Vertical(
            Static("Select the profiles you're interested in:", id="profile-prompt"),
            SelectionList[str](*options, id="profile-list"),
            Button("Show plan", id="show-plan", variant="primary"),
            id="profile-body",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "show-plan":
            return
        selection_list = self.query_one(SelectionList)
        selected_ids = selection_list.selected
        profiles = [self._profiles[pid] for pid in selected_ids]
        self.app.push_screen(PlanScreen(build_plan(profiles)))


class PlanScreen(Screen):
    def __init__(self, plan_text: str) -> None:
        super().__init__()
        self._plan_text = plan_text

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(self._plan_text, id="plan-text"),
            Button("Done", id="done", variant="primary"),
            id="plan-body",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "done":
            self.app.exit()


class SwatWelcomeApp(App):
    TITLE = "SWAT Welcome"

    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen())


def run() -> None:
    SwatWelcomeApp().run()


if __name__ == "__main__":
    run()
