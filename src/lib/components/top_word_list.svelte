<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    let top_three_words;
    let totalCount = 0;

    // Helper function to format numbers with commas
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    onMount(() => {
        // Load the word combinations data
        const loadWordCombinations = d3.csv('/data/top_three_words.csv');
        
        // Load the total document count data
        const loadTotalDocuments = d3.csv('/data/cleaned_titles_with_themes.csv');
        
        // Wait for both to load
        Promise.all([loadWordCombinations, loadTotalDocuments]).then(([wordData, documentsData]) => {
            // Only take the first 20 word combinations
            top_three_words = wordData.slice(0, 20);
            totalCount = documentsData.length; // The total count is the number of rows
        });
    });

</script>

<div class="word-list-container">
    {#if top_three_words}
        <div class="word-list-header">
            <span class="header-number"></span>
            <span class="header-text">Three-word phrases</span>
            <span class="header-count">Number of titles</span>
        </div>
        <div class="word-list">
            {#each top_three_words as words, index}
                <div class="word-item">
                    <span class="word-number">{index + 1}.</span>
                    <span class="word-text">{words.words}</span>
                    <span class="word-count">{formatNumber(words.count)} ({(parseInt(words.count) / totalCount * 100).toFixed(1)}%)</span>
                </div>
            {/each}
        </div>
    {:else}
        <p>Loading word combinations...</p>
    {/if}
</div>

<style>
    .word-list-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        width: 100%;
        max-width: 600px;
        margin: 0 auto;
        text-align: left;
        font-family: Arial, sans-serif;
        padding: 0 20px;
    }

    h2 {
        margin-bottom: 10px;
        text-align: center;
        font-family: Helvetica !important;
        font-weight: 300 !important;
    }

    .word-list-header {
        display: flex;
        align-items: baseline;
        gap: 2px;
        font-weight: bold;
        border-bottom: 1px solid #ddd;
        padding: 0 10px;
    }

    .header-number {
        min-width: 25px;
    }

    .header-text {
        flex-grow: 1;
        padding-left: 0px;
        margin-left: 0;
    }

    .header-count {
        text-align: right;
        padding-right: 10px;
        min-width: 120px;
    }

    .word-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .word-item {
        display: flex;
        align-items: baseline;
        gap: 2px;
        text-align: left;
        padding: 0 10px;
    }

    .word-number {
        min-width: 25px;
    }

    .word-text {
        flex-grow: 1;
        padding-left: 0;
    }

    .word-count {
        text-align: right;
        padding-right: 10px;
        min-width: 120px;
    }
</style>