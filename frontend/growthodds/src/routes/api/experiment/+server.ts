import { json } from '@sveltejs/kit';

import { proxyBackendJson } from '$lib/server/backend';
import type { CreateExperimentRequest } from '$lib/experiments';

import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
	let payload: CreateExperimentRequest;

	try {
		payload = (await request.json()) as CreateExperimentRequest;
	} catch {
		return json(
			{
				message: 'Request body must be valid JSON.'
			},
			{ status: 400 }
		);
	}

	return proxyBackendJson('/api/v1/experiment/', {
		method: 'POST',
		headers: {
			'content-type': 'application/json'
		},
		body: JSON.stringify(payload)
	});
};
