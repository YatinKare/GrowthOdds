<script lang="ts">
	import ExperimentStatusView from '$lib/components/ExperimentStatusView.svelte';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
</script>

{#key data.experimentId}
	<ExperimentStatusView
		experimentId={data.experimentId}
		initialResponse={data.initialResponse}
		initialError={data.initialError}
	/>
{/key}
