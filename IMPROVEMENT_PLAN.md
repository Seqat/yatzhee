# Yahtzee Improvement Plan

## Current assessment

The project is already a complete and playable Tkinter-based Yahtzee game. Its main strength is that the core experience works well. The next step is to make the project more maintainable, testable, and easier to extend.

## Main goals

1. Improve code structure and maintainability
2. Strengthen gameplay reliability
3. Improve the developer experience and onboarding
4. Prepare the project for future features and release

## Recommended roadmap

### Phase 1 — Structure the project as a proper Python package

- Split the single-file implementation in [yahtzee.py](yahtzee.py) into smaller modules such as:
  - game rules and scoring
  - game state and turn flow
  - AI logic
  - Tkinter UI components
  - shared constants and theme settings
- Adopt a regular Python package layout with a clear entry point instead of relying on one large script.
- Introduce a modern packaging file such as a pyproject configuration so the app can be installed and run more cleanly.

### Phase 2 — Make the game logic testable

- Add automated tests for:
  - scoring categories
  - upper section bonus logic
  - turn flow and category assignment
  - AI category selection behavior
- Prefer lightweight tests around the core rules rather than UI-driven tests.
- Cover edge cases such as invalid category selection, repeated scoring, and game-over handling.
- Use a standard test runner such as pytest or unittest, which fits well with current Python tooling support.

### Phase 3 — Improve reliability and UX

- Separate the game model from the Tkinter widgets so state updates are easier to reason about.
- Add validation to prevent invalid actions such as rolling after the game is over or scoring the same category twice.
- Improve the user experience with:
  - clearer turn and roll feedback
  - an onboarding/help screen
  - optional settings such as theme toggles or sound effects
- Consider adding persistence features like high scores or a replay history.

### Phase 4 — Developer experience and release readiness

- Add linting and formatting tools such as ruff or black.
- Add a CI workflow to run tests automatically on pushes and pull requests.
- Update the README with clearer installation, development, and run instructions.
- Add screenshots and, if desired, a packaged desktop launcher for macOS and Windows.

## Suggested implementation order

1. Extract the scoring logic into a dedicated module.
2. Add tests around the scoring and turn rules.
3. Refactor the game state into a model layer.
4. Introduce packaging and a proper entry point.
5. Improve the UI and add player-facing polish.
6. Add CI and release-oriented tooling.

## Definition of done

The project will be considered meaningfully improved when:

- the game logic is isolated from the UI,
- the core rules are covered by automated tests,
- the project can be installed and run as a package,
- and the repository is easier to maintain and extend.
