import { env } from '$env/dynamic/private';
import { json } from '@sveltejs/kit';

import { getApiErrorMessage } from '$lib/experiments';

const DEFAULT_BACKEND_API_BASE_URL = 'http://127.0.0.1:8000';

function getBackendApiBaseUrl() {
	return (env.BACKEND_API_BASE_URL || DEFAULT_BACKEND_API_BASE_URL).replace(/\/+$/, '');
}

async function readResponsePayload(response: Response) {
	const text = await response.text();

	if (!text) {
		return null;
	}

	try {
		return JSON.parse(text) as unknown;
	} catch {
		return text;
	}
}

export async function proxyBackendJson(path: string, init: RequestInit = {}) {
	const headers = new Headers(init.headers);
	headers.set('accept', 'application/json');

	try {
		const response = await fetch(`${getBackendApiBaseUrl()}${path}`, {
			...init,
			headers
		});
		const payload = await readResponsePayload(response);

		if (!response.ok) {
			return json(
				{
					message: getApiErrorMessage(payload, 'Backend request failed.'),
					details: payload
				},
				{
					status: response.status,
					headers: {
						'cache-control': 'no-store'
					}
				}
			);
		}

		return json(payload, {
			status: response.status,
			headers: {
				'cache-control': 'no-store'
			}
		});
	} catch {
		return json(
			{
				message: 'Unable to reach the backend service.',
				details: {
					baseUrl: getBackendApiBaseUrl()
				}
			},
			{
				status: 502,
				headers: {
					'cache-control': 'no-store'
				}
			}
		);
	}
}
