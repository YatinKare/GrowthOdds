import { proxyBackendJson } from '$lib/server/backend';

import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ params }) => {
	return proxyBackendJson(`/api/v1/experiment/${encodeURIComponent(params.id)}`, {
		method: 'GET'
	});
};
