# Frontend/Backend Merge Plan: Create Experiment Flow

## Summary
Connect the existing dashboard modal to the backend create flow without modifying `backend/`, `agents/`, or `db/`. The first merged slice will support one end-to-end path:

`dashboard modal -> POST create -> redirect to /experiments/[id] -> poll GET by id -> stop on completed/failed -> show minimal status/debug view`

Use SvelteKit server-side proxy endpoints for backend access, keep the UI simple, and replace the current hardcoded experiment detail mockup with a backend-driven status page for this step.

## Implementation Changes
### 1. Frontend-owned backend proxy
Add a small server-only integration layer in the frontend app so page code never talks directly to `127.0.0.1:8000`.

- Add a shared backend helper in the frontend app to centralize:
  - backend base URL
  - JSON forwarding
  - response/error normalization
- Default backend base URL to `http://127.0.0.1:8000`
- Allow override via a private env var such as `BACKEND_API_BASE_URL`
- Add proxy endpoints:
  - `POST /api/experiment`
  - `GET /api/experiment/[id]`

Public interface added by the frontend:
- `POST /api/experiment`
  - forwards to backend `POST /api/v1/experiment/`
- `GET /api/experiment/[id]`
  - forwards to backend `GET /api/v1/experiment/:id`

### 2. Dashboard modal becomes the create form
Upgrade [`frontend/growthodds/src/routes/dashboard/+page.svelte`](/Users/yatink/Documents/GitHub/GrowthOdds/frontend/growthodds/src/routes/dashboard/+page.svelte) from hardcoded modal UI to a real create-experiment submit flow.

Behavior:
- Keep the current modal and simple form layout
- Bind the textarea to `user_note`
- Keep the mode toggle and map it to:
  - `single` -> `"single"`
  - `ab` -> `"ab_test"`
- On submit, send this payload:
  - `product_id: "prod_123"`
  - `created_by: "1"`
  - `experiment_title: "Post comparison of your product and its top competitor on X"`
  - `experiment_type: "single" | "ab_test"`
  - `goal: "increase signups"`
  - `channel: "x"`
  - `user_note: <textarea value>`
- Treat `user_note` as optional free text; send an empty string if blank after trimming
- Add submission states:
  - idle
  - submitting
  - submit error
- Disable duplicate submits while the request is in flight
- On successful create:
  - read `experiment_id` from the response
  - close the modal
  - navigate to `/experiments/[id]`
- On failed create:
  - keep the modal open
  - show a compact inline error message

Svelte implementation defaults:
- Use runes mode only
- Use `$state` for modal/form/request state
- Use `$derived` for computed labels and button state
- Keep `$effect` limited to modal body-scroll lock and detail-page polling cleanup

### 3. Replace the experiment detail mockup with a backend-driven status page
Convert [`frontend/growthodds/src/routes/experiments/[id]/+page.svelte`](/Users/yatink/Documents/GitHub/GrowthOdds/frontend/growthodds/src/routes/experiments/[id]/+page.svelte) into a minimal live status screen for this first integration step.

Route data flow:
- Add a sibling `+page.ts` to fetch `/api/experiment/[id]` once on load
- Pass the initial GET payload into the page
- In the page component, continue polling client-side every 3 seconds when status is non-terminal

Polling contract:
- Watch `response.experiment.status`
- Continue polling for:
  - `queued`
  - `running`
- Stop polling for:
  - `completed`
  - `failed`
- Clear the interval on:
  - terminal status
  - route change/unmount

Rendered UI for this step:
- Experiment ID
- Current status badge/text
- Short state-specific message:
  - `queued`: waiting to start
  - `running`: processing
  - `completed`: processing finished
  - `failed`: generation failed
- Last fetched response rendered in a simple debug-friendly block
  - formatted JSON or equivalent field dump
- Simple retry action only for refetching the GET request manually after failures/network errors
- No attempt to map backend data into the current metrics/timeline mockup yet

### 4. Light route/nav hardening for touched screens
Avoid broken navigation inside the merged flow while keeping scope tight.

- Keep `/dashboard` as the main entry route for this step
- Update the root route to redirect or route cleanly into `/dashboard` rather than rendering bare `home`
- Remove or neutralize broken links that point to non-existent pages from touched screens
- Do not build a full experiments index or actions page in this step

## Types / Interfaces
Frontend types to add:
- create request payload
- create response
- experiment GET response
- experiment status union:
  - `"queued" | "running" | "completed" | "failed"`

These types should live in the frontend app and mirror the documented backend contract only as far as needed for this flow.

## Test Plan
Automated:
- `bun run check`
- Add Playwright coverage for the merged flow using mocked frontend proxy responses:
  - create success redirects to `/experiments/[id]`
  - detail page polls from `queued`/`running` into `completed`
  - detail page stops polling after `completed`
  - detail page stops polling after `failed`
  - create failure shows inline modal error and does not navigate

Manual:
- Start backend services per [`backend-usage.md`](/Users/yatink/Documents/GitHub/GrowthOdds/backend-usage.md)
- Submit from the dashboard with both modes
- Confirm POST body matches the chosen hardcoded values
- Confirm redirect lands on the correct experiment ID page
- Confirm polling every ~3 seconds
- Confirm polling stops on `completed` and `failed`

## Assumptions
- Backend code is untouched
- `backend-usage.md` is the sole source of backend contract truth for this step
- The first merged experiment page is intentionally minimal and debug-oriented
- The current detail mockup is deferred until the backend GET response shape is stable enough to map into a richer UI
- Any routes not required for this create flow remain out of scope
