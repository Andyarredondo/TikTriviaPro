# TikTrivia Pro Master Specification

**Version:** 1.1 **Status:** Authoritative Project Constitution

------------------------------------------------------------------------

# 1. Project Philosophy

TikTrivia Pro is a professional livestream production platform.

It is **NOT** a clone of any television game show.

Every design decision must support the live host first.

------------------------------------------------------------------------

# 2. Core Terminology

  Use                 Never Use
  ------------------- -------------------------------------
  Friendly Feud       Family Feud
  Live Players        Contestants
  Live Players        Team A / Team B
  Production Studio   Production Manager (future UI name)
  Viewer Overlay      Audience Display

Never introduce: - Strike controls - Team scoring - TV-specific
mechanics - Television terminology unless explicitly requested.

------------------------------------------------------------------------

# 3. Architecture

The application consists of three independent applications.

1.  Host Dashboard
2.  Viewer Overlay
3.  Production Studio

Each evolves independently.

------------------------------------------------------------------------

# 4. Host Dashboard

Purpose: Run the livestream.

Contains: - Live Players - Game Preview - Production - Game Controls -
Broadcast - Random Deck - Event Log

Does NOT contain: - Display panel - Team scoring - Strike controls -
Production editing

Dashboard Rule:

If a control is not used during most live shows, it does not belong
here.

------------------------------------------------------------------------

# 5. Viewer Overlay

Purpose: Only what viewers need.

Goals: - Maximum readability - Large answer plaques - Smooth
animations - Broadcast quality - Independent styling

Viewer Overlay must never share layout CSS with the Host Dashboard.

------------------------------------------------------------------------

# 6. Production Studio

Purpose: - Create productions - Edit productions - Validate
productions - Schedule productions - Organize productions

Only playback controls belong on the Host Dashboard.

------------------------------------------------------------------------

# 7. Friendly Feud Rules

Friendly Feud is an original TikTrivia Pro game.

Players are individual livestream viewers.

No Team A / Team B.

No strike system.

Points are awarded manually by the host.

------------------------------------------------------------------------

# 8. UI Standards

Dark theme.

Compact controls.

Minimal scrolling.

Professional broadcast appearance.

Design for speed over decoration.

------------------------------------------------------------------------

# 9. CSS Organization

Target structure:

``` text
ui/src/styles/
    HostDashboard.css
    ViewerOverlay.css
    ProductionStudio.css
    SharedTheme.css
    Buttons.css
    Cards.css
```

No shared page layout CSS between Host Dashboard and Viewer Overlay.

------------------------------------------------------------------------

# 10. Development Workflow

1.  Freeze backend.
2.  Design before coding.
3.  Modify one page at a time.
4.  Freeze approved pages.
5.  Add functionality after layout approval.
6.  Commit every milestone.

------------------------------------------------------------------------

# 11. Copilot Rules

Every Copilot prompt should begin with:

> Read `docs/TikTriviaPro_Master_Specification.md`. This document is the
> authoritative project specification.

Copilot MUST:

-   Modify ONLY the files listed.
-   Preserve all existing API calls.
-   Preserve all state management.
-   Preserve all backend logic.
-   Preserve existing database code.
-   Preserve routing.
-   Preserve production engine.
-   Preserve game engine logic.
-   Preserve viewer overlay unless explicitly instructed.
-   Never recreate working code.
-   Never rename working APIs.
-   Never introduce TV game mechanics.
-   Never change project terminology.
-   Never create duplicate components.
-   Never create new files unless explicitly instructed.
-   Never delete working functionality.
-   Never redesign pages unless explicitly instructed.

When asked to redesign a page:

-   Keep functionality.
-   Replace layout only.
-   Preserve behavior.

Every response should include: - Files Modified - Summary - Confirmation
that backend logic was preserved.

------------------------------------------------------------------------

# 12. Git Workflow

Before changes: - git pull

After approval: - git status - git add . - git commit - git push

------------------------------------------------------------------------

# 13. Future Milestones

1.  Host Dashboard
2.  Viewer Overlay
3.  Production Studio
4.  Friendly Feud
5.  Trivia Challenge
6.  Name Those Tunes
7.  Additional Game Engines

------------------------------------------------------------------------

This document is the authoritative specification for TikTrivia Pro.
