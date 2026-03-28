export type ExperimentStatus = 'queued' | 'running' | 'completed' | 'failed';

export type CreateExperimentRequest = {
	product_id: string;
	created_by: string;
	experiment_title: string;
	experiment_type: 'single' | 'ab_test';
	goal: string;
	channel: string;
	user_note: string;
};

export type CreateExperimentResponse = {
	experiment_id: string;
	status: ExperimentStatus;
};

export type ExperimentListItem = {
	id: string;
	title?: string;
	status: ExperimentStatus;
	created_at?: string | null;
};

export type ExperimentListResponse = {
	experiments: ExperimentListItem[];
};

export type ExperimentRecord = {
	id: string;
	status: ExperimentStatus;
	title?: string;
	type?: string;
	goal?: string;
	channel?: string;
	user_note?: string;
	product_id?: string;
	user_id?: number;
	created_at?: string | null;
	updated_at?: string | null;
	[key: string]: unknown;
};

export type ExperimentGetResponse = {
	experiment: ExperimentRecord;
	run: Record<string, unknown> | string;
	outputs: Array<Record<string, unknown>>;
};

export type ApiErrorResponse = {
	message: string;
	details?: unknown;
};

export function getApiErrorMessage(payload: unknown, fallback: string) {
	if (payload && typeof payload === 'object') {
		if ('message' in payload && typeof payload.message === 'string' && payload.message.trim()) {
			return payload.message;
		}

		if ('detail' in payload && typeof payload.detail === 'string' && payload.detail.trim()) {
			return payload.detail;
		}
	}

	if (typeof payload === 'string' && payload.trim()) {
		return payload;
	}

	return fallback;
}

export function isTerminalExperimentStatus(status: ExperimentStatus | null | undefined) {
	return status === 'completed' || status === 'failed';
}

export function getExperimentStatusMessage(status: ExperimentStatus | null | undefined) {
	switch (status) {
		case 'queued':
			return 'waiting to start';
		case 'running':
			return 'processing';
		case 'completed':
			return 'processing finished';
		case 'failed':
			return 'generation failed';
		default:
			return 'status unavailable';
	}
}
