import { getApiErrorMessage, type ExperimentListResponse } from '$lib/experiments';

import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	try {
		const response = await fetch('/api/experiment', {
			headers: {
				accept: 'application/json'
			},
			cache: 'no-store'
		});
		const payload = await response.json().catch(() => null);

		if (!response.ok) {
			return {
				experiments: [],
				initialError: getApiErrorMessage(payload, 'Unable to load experiments.')
			};
		}

		return {
			experiments: (payload as ExperimentListResponse).experiments ?? [],
			initialError: null
		};
	} catch {
		return {
			experiments: [],
			initialError: 'Unable to load experiments.'
		};
	}
};
