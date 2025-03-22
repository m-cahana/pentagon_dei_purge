<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import { getDataPath } from '$lib/utils/paths';
    
    // State with minimal typing
    let allData = [];
    let filteredData = [];
    let searchQuery = '';
    let currentPage = 1;
    let itemsPerPage = 10;
    let totalPages = 1;
    let uniqueThemes = [];
    let selectedTheme = 'All Groups';
    let uniqueTypes = [];
    let selectedType = 'All Types';
    let isLoading = false;
    let isVisible = false;
    let observer;
    let containerRef;
    
    // Theme color mapping - different shades of green
    const themeColors = {
        // Default military green for fallback
        'default': '#4b5320',
        // Different greens for specific themes (examples)
        'Women': '#2e8b57', // sea green
        'Black': '#006400', // dark green
        'Hispanic': '#228b22', // forest green
        'Asian or Pacific Islander': '#3cb371', // medium sea green
        'Native American': '#008000', // green
        'LGBTQ+': '#32cd32', // lime green
        'Generic DEI': '#6b8e23', // olive drab
        'Other': '#556b2f', // dark olive green
    };
    
    // Type color mapping - different shades of green
    const typeColors = {
        // Default color for fallback
        'default': '#264027',
        'Explicit heritage and DEI events': '#1d8348', // dark green
        'Everyday celebrations of heritage or ethnicity': '#117a65', // jungle green
        'Facts of history that relate to a specific ethnic group': '#0e6655', // teal
        'Mentions of personnel that highlight their ethnicity': '#148f77', // persian green
        "Military personnel that belong to a specific ethnic group, even if that isn't explicity mentioned": '#1abc9c', // turquoise
        'Other': '#48c9b0', // medium turquoise
    };
    
    // Function to get color for a theme
    function getThemeColor(theme) {
        return themeColors[theme] || themeColors['default'];
    }
    
    // Function to get color for a type
    function getTypeColor(type) {
        return typeColors[type] || typeColors['default'];
    }
    
    // Intersection Observer to detect when component is visible
    onMount(() => {
        observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !isVisible && allData.length === 0) {
                isVisible = true;
                loadData();
            }
        }, { threshold: 0.1 });
        
        if (containerRef) {
            observer.observe(containerRef);
        }
        
        return () => {
            if (observer && containerRef) {
                observer.unobserve(containerRef);
                observer.disconnect();
            }
        };
    });
    
    // Load data using d3.csv for direct column access
    function loadData() {
        isLoading = true;
        
        // Use our utility function to get the proper path
        const dataFilePath = getDataPath('cleaned_titles_with_themes_and_types.csv');
        
        d3.csv(dataFilePath)
            .then(data => {
                // Data comes pre-parsed with columns as properties
                console.log("CSV loaded successfully:", data.length, "rows");
                console.log("Sample row:", data[0]);
                
                // Store the data
                allData = data;
                
                // Extract unique themes directly
                const themeSet = new Set();
                data.forEach(row => {
                    if (row.theme && row.theme.trim()) {
                        themeSet.add(row.theme);
                    }
                });
                
                uniqueThemes = Array.from(themeSet).sort();
                console.log(`Found ${uniqueThemes.length} unique themes:`, uniqueThemes);
                
                // Extract unique types
                const typeSet = new Set();
                data.forEach(row => {
                    if (row.type && row.type.trim()) {
                        typeSet.add(row.type);
                    }
                });
                
                uniqueTypes = Array.from(typeSet).sort();
                console.log(`Found ${uniqueTypes.length} unique types:`, uniqueTypes);
                
                // Initial filtering
                filterData();
                isLoading = false;
            })
            .catch(error => {
                console.error("Error loading CSV:", error);
                isLoading = false;
            });
    }
    
    // Filter data based on search, theme, and type
    function filterData() {
        let results = [...allData];
        
        // Apply theme filter
        if (selectedTheme !== 'All Groups') {
            results = results.filter(item => item.theme === selectedTheme);
        }
        
        // Apply type filter
        if (selectedType !== 'All Types') {
            results = results.filter(item => item.type === selectedType);
        }
        
        // Apply search filter
        const query = searchQuery.toLowerCase().trim();
        if (query) {
            results = results.filter(item => 
                (item.title?.toLowerCase() || '').includes(query) || 
                (item.theme?.toLowerCase() || '').includes(query) ||
                (item.type?.toLowerCase() || '').includes(query) ||
                (item.url?.toLowerCase() || '').includes(query)
            );
        }
        
        // Update filtered data
        filteredData = results;
        
        // Update pagination
        totalPages = Math.max(Math.ceil(filteredData.length / itemsPerPage), 1);
        
        // Reset to first page when filters change
        if (currentPage > totalPages) {
            currentPage = 1;
        }
    }
    
    // Get current page items
    function getCurrentPageItems() {
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        return filteredData.slice(start, end);
    }
    
    // Handle page navigation
    function goToPage(page) {
        if (page >= 1 && page <= totalPages) {
            currentPage = page;
        }
    }
    
    function handleSearchInput() {
        filterData();
    }
    
    function handleThemeChange() {
        filterData();
    }
    
    function handleTypeChange() {
        filterData();
    }
    
    // Function to format URL for display
    function formatUrl(url) {
        // Return short version if too long
        if (!url) return '';
        return url.length > 40 ? url.substring(0, 37) + '...' : url;
    }
    
    // Function to format numbers with commas
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
</script>

<div class="title-search-container" bind:this={containerRef}>
    <h2>Purged Website Identify Groups & Content Types</h2>
    
    {#if isLoading}
        <div class="loading">Loading data...</div>
    {:else if !isVisible}
        <div class="loading">Scroll to load data</div>
    {:else}
        <div class="search-filters">
            <div class="search-bar">
                <input 
                    type="text" 
                    placeholder="Search for a title..." 
                    bind:value={searchQuery}
                    on:input={handleSearchInput}
                />
            </div>
            
            <div class="theme-filter">
                <label for="theme-select">Group:</label>
                <select 
                    id="theme-select" 
                    bind:value={selectedTheme}
                    on:change={handleThemeChange}
                >
                    <option>All Groups</option>
                    {#each uniqueThemes as theme}
                        <option>{theme}</option>
                    {/each}
                </select>
            </div>
            
            <div class="type-filter">
                <label for="type-select">Type:</label>
                <select 
                    id="type-select" 
                    bind:value={selectedType}
                    on:change={handleTypeChange}
                >
                    <option>All Types</option>
                    {#each uniqueTypes as type}
                        <option>{type}</option>
                    {/each}
                </select>
            </div>
        </div>
        
        <div class="results-container">
            <p class="results-count">
                {#if filteredData.length === 0}
                    No matching results
                {:else}
                    Showing {formatNumber((currentPage - 1) * itemsPerPage + 1)}-{formatNumber(Math.min(currentPage * itemsPerPage, filteredData.length))} of {formatNumber(filteredData.length)} titles
                {/if}
            </p>
            
            <table class="results-table">
                <thead>
                    <tr>
                        <th class="title-column">Title</th>
                        <th class="theme-column">Group</th>
                        <th class="type-column">Type</th>
                        <th class="url-column">URL</th>
                    </tr>
                </thead>
                <tbody>
                    {#if getCurrentPageItems().length === 0}
                        <tr>
                            <td colspan="4" class="no-results">No results found</td>
                        </tr>
                    {:else}
                        {#each getCurrentPageItems() as item}
                            <tr>
                                <td class="title-column">{item.title || 'Untitled'}</td>
                                <td class="theme-column">
                                    <span class="theme-tag" style="background-color: {getThemeColor(item.theme)}">
                                        {item.theme || 'Unknown'}
                                    </span>
                                </td>
                                <td class="type-column">
                                    <span class="type-tag" style="background-color: {getTypeColor(item.type)}">
                                        {item.type || 'Unknown'}
                                    </span>
                                </td>
                                <td class="url-column">
                                    {#if item.url}
                                        <a href={item.url} target="_blank" rel="noopener noreferrer" title={item.url}>
                                            {formatUrl(item.url)}
                                        </a>
                                    {:else}
                                        -
                                    {/if}
                                </td>
                            </tr>
                        {/each}
                    {/if}
                </tbody>
            </table>
            
            {#if totalPages > 1}
                <div class="pagination">
                    <button 
                        class="pagination-btn" 
                        disabled={currentPage === 1}
                        on:click={() => goToPage(1)}
                        title="First page"
                    >
                        &#171; <!-- Double left arrow -->
                    </button>
                    
                    <button 
                        class="pagination-btn" 
                        disabled={currentPage === 1}
                        on:click={() => goToPage(currentPage - 1)}
                        title="Previous page"
                    >
                        &#8249; <!-- Single left arrow -->
                    </button>
                    
                    <span class="page-indicator">
                        Page {formatNumber(currentPage)} of {formatNumber(totalPages)}
                    </span>
                    
                    <button 
                        class="pagination-btn" 
                        disabled={currentPage === totalPages}
                        on:click={() => goToPage(currentPage + 1)}
                        title="Next page"
                    >
                        &#8250; <!-- Single right arrow -->
                    </button>
                    
                    <button 
                        class="pagination-btn" 
                        disabled={currentPage === totalPages}
                        on:click={() => goToPage(totalPages)}
                        title="Last page"
                    >
                        &#187; <!-- Double right arrow -->
                    </button>
                </div>
            {/if}
        </div>
    {/if}
</div>

<style>
    .title-search-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    h2 {
        margin-bottom: 1rem;
        font-weight: 400;
    }
    
    .loading {
        text-align: center;
        padding: 2rem;
        color: #666;
    }
    
    .search-filters {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .search-bar {
        flex: 1;
        min-width: 200px;
        margin-right: 1rem;
    }
    
    .search-bar input {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 16px;
        font-family: Helvetica, Arial, sans-serif;
    }
    
    /* Style for placeholder text */
    .search-bar input::placeholder {
        font-style: italic;
        color: #999;
        font-size: 16px;
        font-family: Helvetica, Arial, sans-serif;
    }
    
    /* For Microsoft Edge */
    .search-bar input::-ms-input-placeholder {
        font-style: italic;
        color: #999;
        font-size: 16px;
        font-family: Helvetica, Arial, sans-serif;
    }
    
    /* For Firefox */
    .search-bar input::-moz-placeholder {
        font-style: italic;
        color: #999;
        font-size: 16px;
        font-family: Helvetica, Arial, sans-serif;
        opacity: 1;
    }
    
    /* For Chrome/Safari/Opera */
    .search-bar input::-webkit-input-placeholder {
        font-style: italic;
        color: #999;
        font-size: 16px;
        font-family: Helvetica, Arial, sans-serif;
    }
    
    .theme-filter,
    .type-filter {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        min-width: 180px;
    }
    
    .theme-filter label,
    .type-filter label {
        font-size: 18px;
        font-family: Helvetica, Arial, sans-serif;
    }
    
    .theme-filter select,
    .type-filter select {
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 4px;
        min-width: 140px;
        font-size: 16px;
        font-family: Helvetica, Arial, sans-serif;
    }
    
    .results-count {
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        color: #666;
    }
    
    .results-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1rem;
        table-layout: fixed;
    }
    
    .results-table th,
    .results-table td {
        padding: 0.5rem;
        text-align: left;
        border-bottom: 1px solid #eee;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 0.95rem; /* Standardized font size */
    }
    
    .results-table th {
        background-color: #f5f5f5;
        font-weight: 600; /* Semi-bold for headers */
    }
    
    /* Adjusted column widths */
    .title-column {
        width: 40%; /* Reduced to make space for type column */
        padding-right: 0.75rem; /* Standardized padding */
    }
    
    .theme-column {
        width: 15%; /* Narrower theme column */
        min-width: 100px;
        /* Remove overflow properties to allow content to wrap */
        white-space: normal;
        word-wrap: break-word;
        padding-left: 0.75rem; /* Standardized padding */
        padding-right: 0.75rem; /* Standardized padding */
    }
    
    .type-column {
        width: 15%; /* Same width as theme column */
        min-width: 100px;
        white-space: normal;
        word-wrap: break-word;
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }
    
    .url-column {
        width: 30%; /* Reduced to make space for type column */
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        padding-left: 0.75rem; /* Standardized padding */
        font-size: 0.95rem; /* Match other columns */
    }
    
    .url-column a {
        color: #0066cc;
        text-decoration: none;
        font-size: inherit; /* Inherit from parent to maintain consistency */
    }
    
    .url-column a:hover {
        text-decoration: underline;
    }
    
    .theme-tag,
    .type-tag {
        display: inline-block;
        padding: 0.2rem 0.4rem;
        /* Use inline style for bg color instead */
        color: white;
        border-radius: 4px;
        font-size: 0.95rem; /* Match other text */
        /* Remove nowrap to allow wrapping */
        white-space: normal;
        word-wrap: break-word;
        /* Add small vertical margin if it wraps */
        margin: 0.1rem 0;
        /* Help with line breaks for very long themes */
        hyphens: auto;
    }
    
    .pagination {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
    }
    
    .pagination-btn {
        padding: 0.3rem 0.5rem;
        border: none;
        background-color: transparent;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1.2rem;
        line-height: 1;
        color: #555;
    }
    
    .pagination-btn:disabled {
        opacity: 0.3;
        cursor: not-allowed;
    }
    
    .page-indicator {
        margin: 0 0.5rem;
        font-size: 0.9rem;
        color: #555;
    }
    
    @media (max-width: 768px) {
        .search-filters {
            flex-direction: column;
        }
        
        .theme-filter,
        .type-filter {
            width: 100%;
        }
        
        /* Adjusted column widths for small screens - keep all columns visible */
        .title-column {
            width: 35%; /* Reduced to make space for type */
            padding-right: 0.5rem; /* Smaller but consistent padding */
        }
        
        .theme-column,
        .type-column {
            width: 20%; /* Equal width for theme and type */
            min-width: 80px;
            padding-left: 0.5rem; /* Smaller but consistent padding */
            padding-right: 0.5rem; /* Smaller but consistent padding */
        }
        
        .url-column {
            width: 25%; /* Reduced to make space for type */
            font-size: 0.85rem; /* Slightly smaller text */
            padding-left: 0.5rem; /* Smaller but consistent padding */
        }
        
        /* Make table rows more compact on small screens */
        .results-table th,
        .results-table td {
            padding: 0.3rem 0.4rem;
            font-size: 0.9rem; /* Consistent font size */
        }
        
        /* Reduce title font size slightly for better fit */
        h2 {
            font-size: 1.4rem;
        }
        
        /* More compact theme tags */
        .theme-tag,
        .type-tag {
            padding: 0.15rem 0.3rem;
            font-size: 0.9rem; /* Match other text */
        }
        
        /* Consistent URL font size */
        .url-column,
        .url-column a {
            font-size: 0.9rem; /* Match other text */
        }
        
        /* Smaller search bar text on mobile */
        .search-bar input {
            font-size: 14px;
        }
        
        .search-bar input::placeholder,
        .search-bar input::-webkit-input-placeholder,
        .search-bar input::-moz-placeholder,
        .search-bar input::-ms-input-placeholder {
            font-size: 14px;
        }
        
        /* Smaller theme filter text on mobile */
        .theme-filter label,
        .theme-filter select,
        .type-filter label,
        .type-filter select {
            font-size: 14px;
        }
    }
    
    /* Extra small screens */
    @media (max-width: 480px) {
        .title-column {
            width: 35%;
            padding-right: 0.35rem; /* Even smaller but consistent padding */
        }
        
        .theme-column,
        .type-column {
            width: 20%;
            min-width: 60px;
            padding-left: 0.35rem; /* Even smaller but consistent padding */
            padding-right: 0.35rem; /* Even smaller but consistent padding */
        }
        
        .url-column {
            width: 25%;
            font-size: 0.8rem;
            padding-left: 0.35rem; /* Even smaller but consistent padding */
        }
        
        .results-table th,
        .results-table td {
            padding: 0.25rem 0.3rem;
            font-size: 0.85rem; /* Smaller but consistent across all columns */
        }
        
        .theme-tag,
        .type-tag {
            font-size: 0.85rem; /* Match table text */
        }
        
        .url-column,
        .url-column a {
            font-size: 0.85rem; /* Match other text */
        }
    }
</style> 