import { expect, test, type Page } from '@playwright/test';

const appUrl = 'http://localhost:4173';

function buildExperimentResponse(id: string, status: 'queued' | 'running' | 'completed' | 'failed') {
	return {
		experiment: {
			id,
			status,
			title: 'Post comparison of your product and its top competitor on X'
		},
		run: {
			status
		},
		outputs: []
	};
}

async function openCreateModal(page: Page) {
	await page.goto(`${appUrl}/dashboard`);
	await page.getByTestId('open-create-modal').click();
	await page.getByTestId('user-note-input').fill('focus on simpler UX');
}

test('create success redirects and polling stops after completed', async ({ page }) => {
	let capturedPayload: Record<string, unknown> | undefined;
	let getRequestCount = 0;
	const experimentId = 'exp-completed';
	const statuses = ['queued', 'running', 'completed'] as const;

	await page.route('**/api/experiment', async (route) => {
		capturedPayload = route.request().postDataJSON() as Record<string, unknown>;

		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({
				experiment_id: experimentId,
				status: 'queued'
			})
		});
	});

	await page.route(`**/api/experiment/${experimentId}`, async (route) => {
		const status = statuses[Math.min(getRequestCount, statuses.length - 1)];
		getRequestCount += 1;

		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify(buildExperimentResponse(experimentId, status))
		});
	});

	await openCreateModal(page);
	await page.getByTestId('submit-create').click();

	await expect(page).toHaveURL(`${appUrl}/experiments/${experimentId}`);
	await expect(page.getByTestId('status-badge')).toHaveText(/completed/i, { timeout: 10000 });
	await expect(page.getByText('processing finished')).toBeVisible();
	await expect.poll(() => getRequestCount).toBe(3);
	await page.waitForTimeout(3500);
	expect(getRequestCount).toBe(3);
	expect(capturedPayload).toEqual({
		product_id: 'prod_123',
		created_by: '1',
		experiment_title: 'Post comparison of your product and its top competitor on X',
		experiment_type: 'ab_test',
		goal: 'increase signups',
		channel: 'x',
		user_note: 'focus on simpler UX'
	});
});

test('detail page stops polling after failed', async ({ page }) => {
	let getRequestCount = 0;
	let capturedPayload: Record<string, unknown> | undefined;
	const experimentId = 'exp-failed';
	const statuses = ['queued', 'failed'] as const;

	await page.route('**/api/experiment', async (route) => {
		capturedPayload = route.request().postDataJSON() as Record<string, unknown>;

		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({
				experiment_id: experimentId,
				status: 'queued'
			})
		});
	});

	await page.route(`**/api/experiment/${experimentId}`, async (route) => {
		const status = statuses[Math.min(getRequestCount, statuses.length - 1)];
		getRequestCount += 1;

		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify(buildExperimentResponse(experimentId, status))
		});
	});

	await openCreateModal(page);
	await page.getByRole('button', { name: 'Single Post' }).click();
	await page.getByTestId('submit-create').click();

	await expect(page).toHaveURL(`${appUrl}/experiments/${experimentId}`);
	await expect(page.getByTestId('status-badge')).toHaveText(/failed/i, { timeout: 7000 });
	await expect(page.getByText('generation failed')).toBeVisible();
	await expect.poll(() => getRequestCount).toBe(2);
	await page.waitForTimeout(3500);
	expect(getRequestCount).toBe(2);
	expect(capturedPayload?.experiment_type).toBe('single');
});

test('create failure shows inline error and does not navigate', async ({ page }) => {
	await page.route('**/api/experiment', async (route) => {
		await route.fulfill({
			status: 500,
			contentType: 'application/json',
			body: JSON.stringify({
				message: 'Unable to create experiment right now.'
			})
		});
	});

	await openCreateModal(page);
	await page.getByTestId('submit-create').click();

	await expect(page).toHaveURL(`${appUrl}/dashboard`);
	await expect(page.getByTestId('create-modal')).toBeVisible();
	await expect(page.getByTestId('create-error')).toHaveText(
		'Unable to create experiment right now.'
	);
});
