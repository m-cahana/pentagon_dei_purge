<script lang="ts">
    import * as d3 from 'd3';
    import { onMount } from 'svelte';
    import Scrolly from "$lib/components/helpers/scrolly.svelte";
    import { getFullPath } from '$lib/utils/paths';
    
    // Props for customization
    let {
        dataPath = '/data/cleaned_titles_with_themes_and_types.csv', // Path to the data file
        colorScheme = [
            "var(--color-military-green)" // military color scheme
        ],
        // New prop to specify which column to use for grouping
        groupByColumn = 'theme', // Default to 'theme', can be changed to 'type' or any other column
        // New prop to add a suffix to CSS class names to avoid conflicts
        classSuffix = '', // Default to empty string (no suffix)
        // Spacing between circles (padding factor)
        circleSpacing = 1, // Multiplier for circle padding (1 = default, 2 = double spacing, etc.)
        // New props for scrolly content
        scrollContent = {
            0: "The largest groups targeted by the Pentagon's DEI purge are women and Black people.",
            1: "Asian Americans, Pacific Islanders, and Hispanic people trail not too far behind.",
            2: "Native Americans and LGBTQ+ people are also significant targets.",
            3: 'There are a fair amount of websites that relate to generic DEI content, like websites that discuss "diversity" or "inclusion" without mentioning any specific groups.',
            4: "And there's a large segment of websites that don't belong to any defined theme. These websites' titles alone aren't very informative. If their full content wasn't already purged, I suspect we'd find these websites were targeted because they fit into a specific theme."
        },
        // Add highlightMap prop to specify which items to highlight at each step
        highlightMap = {
            0: ["Women", "Black"], // Example: highlight "Women" and "Black" themes
            1: ["Hispanic", "Asian or Pacific Islander"], // Example: highlight Hispanic and API themes
            2: ["Native American", "LGBTQ+"], // Example: highlight Native American and LGBTQ+ themes
            3: ["Generic DEI"], 
            4: ["Other"]
        }
    } = $props();
    
    // Extract section indices from scrollContent
    let sectionIndices = $derived(Object.keys(scrollContent).map(Number).sort((a, b) => a - b));
    
    // Add proper type for container to fix "implicit any" error
    let container: HTMLDivElement;
    let width: number;
    let height: number;
    
    // Define proper type for data structure
    interface GroupChild {
        name: string;
        value: number;
    }
    
    interface GroupItem {
        name: string;
        value: number;
        percentage: string;
        formattedCount: string;
        children: GroupChild[];
    }
    
    interface DataStructure {
        name: string;
        children: GroupItem[];
    }
    
    let data: DataStructure = {name: "root", children: []};
    let value = $state(0);
    let allNodes: any[] = [];
    let groupNodes: any[] = [];
    
    interface GroupNode {
        depth: number;
        data: {
            name: string;
            value: number;
            percentage: string;
            formattedCount: string;
            children?: any[];
        };
        r: number;
        x: number;
        y: number;
    }
    
    interface DataItem {
        title: string;
        theme: string;
        type: string;
        [key: string]: any;
    }
    
    // Function to handle window resize
    function handleResize() {
        updateVisualizationSize();
        if (data.children.length > 0) {
            createVisualization();
        }
    }
    
    // Function to update visualization dimensions based on container size
    function updateVisualizationSize() {
        if (!container) return;
        
        const containerRect = container.getBoundingClientRect();
        width = containerRect.width;
        height = containerRect.height;
        
        // Ensure minimum dimensions
        width = Math.max(width, 300);
        height = Math.max(height, 400);
    }

    // Helper function to format numbers with commas
    function formatNumber(num: number): string {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    onMount(() => {
        // Initialize size based on container
        updateVisualizationSize();
        
        // Add resize listener
        window.addEventListener('resize', handleResize);
        
        // Use our utility function to handle the path from props
        const fullDataPath = getFullPath(dataPath);
        console.log(`Loading data from: ${fullDataPath}`);
        
        // Load and process the data
        d3.csv(fullDataPath)
            .then(processData)
            .then(createVisualization)
            .catch((error: any) => {
                console.error("Error loading CSV:", error);
            });
            
        // Clean up event listeners on component destruction
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    });

    // Process the CSV data into a hierarchical structure for circle packing
    function processData(csvData: DataItem[]) {
        // Group titles by the specified column
        const dataGroups = d3.group(csvData, (d: DataItem) => d[groupByColumn] || "Unknown");

        const totalItems = csvData.length;
        
        // Convert to hierarchical structure for circle packing
        data = {
            name: "root",
            children: Array.from(dataGroups, ([groupValue, items]) => ({
                name: groupValue,
                value: items.length,
                percentage: (items.length / totalItems * 100).toFixed(1),
                formattedCount: formatNumber(items.length),
                children: items.map((item: DataItem) => ({
                    name: item.title,
                    value: 1
                }))
            }))
        };
        
        // Sort by size (descending)
        data.children.sort((a, b) => b.value - a.value);
        
        return data;
    }

    // Function to normalize group names for CSS class names
    function normalizeForCSS(name: string): string {
        // Replace spaces with hyphens, remove + character, and convert to lowercase
        return name.replace(/\s+/g, '-').replace(/\+/g, '').toLowerCase();
    }
    
    // Function to create a CSS class name with optional suffix
    function createClassName(prefix: string, name: string): string {
        const normalizedName = normalizeForCSS(name);
        // Add suffix if provided, otherwise just use the normalized name
        return `${prefix}-${normalizedName}${classSuffix ? `-${classSuffix}` : ''}`;
    }

    // Function to highlight groups based on current scroll position
    function highlightGroups(currentValue: number) {
        // Get groups to highlight for this scroll position
        const groupsToHighlight = getGroupsToHighlight(currentValue);
        
        // First, mark all groups as non-highlighted
        d3.selectAll(`.group-circle${classSuffix ? `-${classSuffix}` : ''}`)
            .classed("highlighted", false)
            .classed("dimmed", true);
        
        // Then, highlight the specific groups
        if (groupsToHighlight.length > 0) {
            groupsToHighlight.forEach(groupName => {
                // Use case-insensitive substring matching for more flexibility
                groupNodes.forEach(node => {
                    const nodeName = node.data.name;
                    // Check if the group name matches
                    if (nodeName === groupName) {
                        // Use normalized CSS class name (without + character)
                        d3.select(`.${createClassName('circle', nodeName)}`)
                            .classed("highlighted", true)
                            .classed("dimmed", false);
                            
                        // Also highlight the associated label
                        d3.select(`.${createClassName('label', nodeName)}`)
                            .classed("highlighted", true);
                    }
                });
            });
        }
    }
    
    // Get groups to highlight from props based on current scroll value
    function getGroupsToHighlight(currentValue: number): string[] {
        // Use items from highlightMap prop if available, or return empty array
        return highlightMap[currentValue] || [];
    }

    function createVisualization() {
        // Clear any existing SVG
        d3.select(container).selectAll("svg").remove();
        
        // Create the SVG container
        const svg = d3.select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;");
        
        // Create a color scale
        const color = d3.scaleOrdinal()
            .domain(data.children.map(d => d.name))
            .range(colorScheme);
        
        // Use D3's force layout for a more organic arrangement
        const createForceLayout = () => {
            const groups = data.children;
            const totalValue = groups.reduce((sum, group) => sum + group.value, 0);
            const averageValue = totalValue / groups.length;
            
            // Calculate the total number of titles for scaling
            const maxValue = Math.max(...groups.map(group => group.value));
            
            // Calculate safe area to ensure circles don't get cut off
            // Scale down the maximum radius on smaller screens
            const sizeMultiplier = width < 768 ? 0.2 : 0.25; // Smaller multiplier on small screens
            
            // Adjust the maxPossibleRadius based on circleSpacing to avoid overlapping
            // More spacing means smaller max radius to fit everything
            const spacingFactor = 1 / Math.sqrt(Math.max(1, circleSpacing));
            const maxPossibleRadius = Math.min(width, height) * sizeMultiplier * spacingFactor;
            
            // Adjust minimum size based on screen size
            const minRadius = width < 768 ? 30 : 40;
            
            // Create nodes for force simulation with constraints to prevent edge cutting
            const forceNodes = groups.map(group => {
                // Size circles based on square root of their value for area proportionality
                // Using square root ensures the area is proportional to the value
                const sizeFactor = Math.sqrt(group.value / maxValue);
                
                // Size range with minimum size to ensure visibility of small groups
                const radius = Math.max(minRadius, maxPossibleRadius * sizeFactor);
                
                return {
                    depth: 1,
                    data: group,
                    r: radius,
                    // Start with positions farther apart based on spacing factor
                    x: width / 2 + (Math.random() - 0.5) * width * 0.4 * circleSpacing,
                    y: height / 2 + (Math.random() - 0.5) * height * 0.4 * circleSpacing
                };
            });
            
            // Root node (invisible)
            const rootNode = {
                depth: 0,
                data: data,
                r: 0,
                x: width / 2,
                y: height / 2
            };
            
            // Calculate bounds to keep circles within viewport
            const maxRadius = Math.max(...forceNodes.map(d => d.r));
            const boundaryPadding = maxRadius + 10;
            
            // Create the force simulation with adjusted parameters
            const simulation = d3.forceSimulation(forceNodes)
                // Centers the nodes in the available space
                .force('center', d3.forceCenter(width / 2, height / 2))
                // Prevents node overlap with padding adjusted by circleSpacing
                .force('collision', d3.forceCollide().radius((d: any) => {
                    // Apply spacing factor to the collision radius
                    return d.r + (3 * circleSpacing);
                }).strength(0.85))
                // Add boundary force to keep circles within container
                .force('x', d3.forceX(width / 2).strength(0.1))
                .force('y', d3.forceY(height / 2).strength(0.1))
                // Adjust charge based on spacing - more spacing means more charge
                .force('charge', d3.forceManyBody().strength(-10 * circleSpacing))
                // Run simulation until it stabilizes
                .stop();
                
            // Run the simulation with boundary enforcing
            for (let i = 0; i < 300; ++i) {
                simulation.tick();
                
                // After each tick, enforce boundaries to keep circles within container
                forceNodes.forEach(node => {
                    node.x = Math.max(boundaryPadding, Math.min(width - boundaryPadding, node.x));
                    node.y = Math.max(boundaryPadding, Math.min(height - boundaryPadding, node.y));
                });
            }
            
            return [rootNode, ...forceNodes];
        };
        
        // Generate nodes with force-directed layout
        allNodes = createForceLayout();
        groupNodes = allNodes.filter(node => node.depth === 1);
        
        // Create a container for all circles
        const nodes = svg.append("g")
            .selectAll("g")
            .data(allNodes)
            .join("g")
            .attr("transform", (d: any) => `translate(${d.x},${d.y})`);
        
        // Add circles with CSS classes for styling
        nodes.append("circle")
            .attr("r", (d: any) => d.r)
            .attr("fill", (d: any) => d.depth === 1 ? color(d.data.name) : "white")
            .attr("stroke", (d: any) => d.depth === 1 ? "#fff" : "none")
            .attr("stroke-width", (d: any) => d.depth === 1 ? 1 : 0)
            .attr("class", (d: any) => {
                // Only add styling classes to group circles (depth === 1)
                if (d.depth === 1) {
                    const groupClass = createClassName('circle', d.data.name);
                    // Add suffix to group-circle class if provided
                    const baseClass = classSuffix ? `group-circle-${classSuffix}` : 'group-circle';
                    return `${baseClass} ${groupClass} dimmed`; // Start dimmed by default
                }
                return "";
            });
            
        // Create a new group specifically for labels that will be on top of everything
        const labelsGroup = svg.append("g")
            .attr("class", "labels-container")
            .raise(); // Explicitly raise this group to the top of the SVG
        
        // Re-create the labels in this top-level group
        groupNodes.forEach(d => {
            if (d.depth === 1) {
                const groupClass = createClassName('label', d.data.name);
                
                const labelGroup = labelsGroup.append("g")
                    .attr("transform", `translate(${d.x},${d.y})`)
                    .attr("class", `group-label-group ${groupClass}`)
                    .style("pointer-events", "none");
                
                // Calculate font size based on circle radius and screen size
                const fontSizeMultiplier = width < 768 ? 4 : 3.5;
                const maxFontSize = width < 768 ? 16 : 20;
                const fontSize = Math.min(d.r / fontSizeMultiplier, maxFontSize);
                
                // Add group name
                labelGroup.append("text")
                    .attr("text-anchor", "middle")
                    .attr("dominant-baseline", "central")
                    .attr("class", "group-title")
                    .style("font-size", `${fontSize}px`)
                    .append("tspan")
                    .attr("x", 0)
                    .attr("y", -d.r / 10)
                    .text(d.data.name);
                
                // Add count
                labelGroup.append("text")
                    .attr("text-anchor", "middle")
                    .attr("dominant-baseline", "central")
                    .attr("class", "group-count")
                    .style("font-size", `${fontSize}px`)
                    .append("tspan")
                    .attr("x", 0)
                    .attr("y", d.r / 5)
                    .text(`${d.data.formattedCount} (${d.data.percentage}%)`);
            }
        });
        
        // Initial highlight based on current value
        highlightGroups(value);
    }
    
    // Replace legacy reactive statement with $effect
    $effect(() => {
        if (value !== undefined && groupNodes.length > 0) {
            highlightGroups(value);
        }
    });

</script>

<section id="theme-circle-pack">
    <!-- Fixed visualization that stays in the background -->
    <div class="visualization-container">
        <div class="theme-circle-pack__container" bind:this={container}>
            <!-- Circle packing visualization rendered here -->
        </div>
    </div>

    <div class="spacer"></div>
    
    <!-- Scrolly component for scroll-activated content -->
    <Scrolly bind:value>
        {#each sectionIndices as section}
            {@const active = value === section}
            <div class="step" class:active>
                <div class="step-content">
                    <p>{scrollContent[section]}</p>
                </div>
            </div>
        {/each}
    </Scrolly>
    
    <div class="spacer"></div>
</section>

<style>
    #theme-circle-pack {
        position: relative;
        width: 100%;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .visualization-container {
        position: sticky;
        top: 4em;
        z-index: 1;
        width: 100%;
        height: auto;
        background-color: white;
    }
    
    .visualization-title {
        text-align: center;
        margin: 0;
        padding: 10px 0;
        font-size: 1.5rem;
        font-weight: 500;
    }
    
    .theme-circle-pack__container {
        width: 100%;
        height: 80vh;
        min-height: 400px;
        border: none;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .spacer {
        height: 75vh;
    }
    
    .step {
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding: 0 20px;
        z-index: 5;
        position: relative;
    }
    
    .step-content {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 20px;
        max-width: 350px;
        pointer-events: auto;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-right: 5%;
    }
    
    .step p {
        margin: 0;
        font-family: "Arial";
        font-weight: 200;
    }
    
    .active {
        font-weight: bold;
    }
    
    /* Circle styling with CSS classes */
    :global(.group-circle),
    :global([class^="group-circle-"]) {
        transition: all 0.3s ease;
    }
    
    :global(.group-circle.dimmed),
    :global([class^="group-circle-"].dimmed) {
        opacity: 0.3; /* transparent when not highlighted */
    }
    
    :global(.group-circle.highlighted),
    :global([class^="group-circle-"].highlighted) {
        opacity: 0.95; /* Almost fully opaque when highlighted */
        stroke-width: 2px; /* Thicker border */
    }
    
    /* Label styling */
    :global(.group-title),
    :global(.group-count) {
        fill: #1e1d1d;
        font-weight: 400;
        font-family: Arial !important;
        transition: opacity 0.3s ease;
    }
    
    :global(.group-label-group) {
        opacity: 0.5; /* Labels slightly dimmed by default */
        transition: opacity 0.3s ease;
    }
    
    :global(.group-label-group.highlighted) {
        opacity: 1; /* Full opacity for highlighted labels */
    }
    
    /* Make sure the Scrolly component has proper z-index */
    :global(.scrolly-container) {
        position: relative;
        z-index: 10; /* Higher than both visualization and steps */
    }
    
    /* Media query for small screens */
    @media (max-width: 768px) {
        .theme-circle-pack__container {
            height: 60vh;
        }
        
        .step-content {
            max-width: 280px;
            padding: 15px;
        }
    }
    
    /* Media query for very small screens */
    @media (max-width: 480px) {
        .theme-circle-pack__container {
            height: 50vh;
        }
        
        .step-content {
            max-width: 240px;
            padding: 12px;
        }
    }
</style> 