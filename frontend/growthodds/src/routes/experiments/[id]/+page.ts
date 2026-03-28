import { getApiErrorMessage, type ExperimentGetResponse } from '$lib/experiments';

import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
	try {
		const response = await fetch(`/api/experiment/${params.id}`, {
			headers: {
				accept: 'application/json'
			},
			cache: 'no-store'
		});
		const payload = await response.json().catch(() => null);

		if (!response.ok) {
			return {
				experimentId: params.id,
				initialResponse: null,
				initialError: getApiErrorMessage(payload, 'Unable to load experiment.')
			};
		}

		return {
			experimentId: params.id,
			initialResponse: payload as ExperimentGetResponse,
			initialError: null
		};
	} catch {
		return {
			experimentId: params.id,
			initialResponse: null,
			initialError: 'Unable to load experiment.'
		};
	}
};
