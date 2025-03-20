<script lang="ts">
    import * as d3 from 'd3';
    import { onMount } from 'svelte';
    import Scrolly from "$lib/components/helpers/scrolly.svelte";
    
    // Props for customization
    let {
        dataPath = '/data/cleaned_titles_with_themes.csv', // Path to the data file
        colorScheme = [
            "var(--color-military-green)" // military color scheme
        ],
        // New props for scrolly content
        scrollContent = {
            0: "The largest groups targeted by the Pentagon's DEI purge are women and Black people.",
            1: "Asian Americans, Pacific Islanders, and Hispanic people trail not too far behind.",
            2: "Native Americans and LGBTQ+ people are also significant targets.",
            3: 'There are a fair amount of websites that relate to generic DEI content, like websites that discuss "diversity" or "inclusion" without mentioning any specific groups.',
            4: "And there's a large segment of websites that don't belong to any defined theme. These websites' titles alone aren't very informative. If their full content wasn't already purged, I suspect we'd find these websites were targeted because they fit into a specific theme."
        },
        // Add highlightMap prop to specify which themes to highlight at each step
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
    interface ThemeChild {
        name: string;
        value: number;
    }
    
    interface ThemeItem {
        name: string;
        value: number;
        percentage: string;
        formattedCount: string;
        children: ThemeChild[];
    }
    
    interface DataStructure {
        name: string;
        children: ThemeItem[];
    }
    
    let data: DataStructure = {name: "root", children: []};
    let value = $state(0);
    let allNodes: any[] = [];
    let themeNodes: any[] = [];
    
    interface ThemeNode {
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
        
        // Load and process the data
        d3.csv(dataPath)
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
        // Group titles by theme
        const themeGroups = d3.group(csvData, (d: DataItem) => d.theme || "Unknown");

        const totalTitles = csvData.length;
        
        // Convert to hierarchical structure for circle packing
        data = {
            name: "root",
            children: Array.from(themeGroups, ([theme, titles]) => ({
                name: theme,
                value: titles.length,
                percentage: (titles.length / totalTitles * 100).toFixed(1),
                formattedCount: formatNumber(titles.length),
                children: titles.map((title: DataItem) => ({
                    name: title.title,
                    value: 1
                }))
            }))
        };
        
        // Sort by size (descending)
        data.children.sort((a, b) => b.value - a.value);
        
        return data;
    }

    // Function to normalize theme names for CSS class names
    function normalizeForCSS(name: string): string {
        // Replace spaces with hyphens, remove + character, and convert to lowercase
        return name.replace(/\s+/g, '-').replace(/\+/g, '').toLowerCase();
    }

    // Function to highlight themes based on current scroll position
    function highlightThemes(currentValue: number) {
        // Get themes to highlight for this scroll position
        const themesToHighlight = getThemesToHighlight(currentValue);
        
        // First, mark all themes as non-highlighted
        d3.selectAll(".theme-circle")
            .classed("highlighted", false)
            .classed("dimmed", true);
        
        // Then, highlight the specific themes
        if (themesToHighlight.length > 0) {
            themesToHighlight.forEach(themeName => {
                // Use case-insensitive substring matching for more flexibility
                themeNodes.forEach(node => {
                    const nodeName = node.data.name;
                    // Check if the theme name contains the string to highlight (case insensitive)
                    if (nodeName === themeName) {
                        // Use normalized CSS class name (without + character)
                        d3.select(`.circle-${normalizeForCSS(nodeName)}`)
                            .classed("highlighted", true)
                            .classed("dimmed", false);
                            
                        // Also highlight the associated label
                        d3.select(`.label-${normalizeForCSS(nodeName)}`)
                            .classed("highlighted", true);
                    }
                });
            });
        }
    }
    
    // Get themes to highlight from props based on current scroll value
    function getThemesToHighlight(currentValue: number): string[] {
        // Use themes from highlightMap prop if available, or return empty array
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
            const themes = data.children;
            const totalValue = themes.reduce((sum, theme) => sum + theme.value, 0);
            const averageValue = totalValue / themes.length;
            
            // Calculate the total number of titles for scaling
            const maxValue = Math.max(...themes.map(theme => theme.value));
            
            // Calculate safe area to ensure circles don't get cut off
            // Scale down the maximum radius on smaller screens
            const sizeMultiplier = width < 768 ? 0.2 : 0.25; // Smaller multiplier on small screens
            const maxPossibleRadius = Math.min(width, height) * sizeMultiplier;
            
            // Adjust minimum size based on screen size
            const minRadius = width < 768 ? 30 : 40;
            
            // Create nodes for force simulation with constraints to prevent edge cutting
            const forceNodes = themes.map(theme => {
                // Size circles based on square root of their value for area proportionality
                // Using square root ensures the area is proportional to the value
                const sizeFactor = Math.sqrt(theme.value / maxValue);
                
                // Size range with minimum size to ensure visibility of small themes
                const radius = Math.max(minRadius, maxPossibleRadius * sizeFactor);
                
                return {
                    depth: 1,
                    data: theme,
                    r: radius,
                    // Start with positions closer to center
                    x: width / 2 + (Math.random() - 0.5) * width * 0.4,
                    y: height / 2 + (Math.random() - 0.5) * height * 0.4
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
            const boundaryPadding = maxRadius + 10; // Add some padding
            
            // Create the force simulation with adjusted parameters
            const simulation = d3.forceSimulation(forceNodes)
                // Centers the nodes in the available space
                .force('center', d3.forceCenter(width / 2, height / 2))
                // Prevents node overlap with minimal padding
                .force('collision', d3.forceCollide().radius((d: any) => d.r + 3).strength(0.8))
                // Add boundary force to keep circles within container
                .force('x', d3.forceX(width / 2).strength(0.1))
                .force('y', d3.forceY(height / 2).strength(0.1))
                // Reduced charge to allow circles to be closer
                .force('charge', d3.forceManyBody().strength(-10))
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
        themeNodes = allNodes.filter(node => node.depth === 1);
        
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
                // Only add styling classes to theme circles (depth === 1)
                if (d.depth === 1) {
                    const themeClass = `circle-${normalizeForCSS(d.data.name)}`;
                    return `theme-circle ${themeClass} dimmed`; // Start dimmed by default
                }
                return "";
            });
            
        // Create a new group specifically for labels that will be on top of everything
        const labelsGroup = svg.append("g")
            .attr("class", "labels-container")
            .raise(); // Explicitly raise this group to the top of the SVG
        
        // Re-create the labels in this top-level group
        themeNodes.forEach(d => {
            if (d.depth === 1) {
                const themeClass = `label-${normalizeForCSS(d.data.name)}`;
                
                const labelGroup = labelsGroup.append("g")
                    .attr("transform", `translate(${d.x},${d.y})`)
                    .attr("class", `theme-label-group ${themeClass}`)
                    .style("pointer-events", "none");
                
                // Calculate font size based on circle radius and screen size
                // Scale down further on small screens
                const fontSizeMultiplier = width < 768 ? 4 : 3.5;
                const maxFontSize = width < 768 ? 16 : 20;
                const fontSize = Math.min(d.r / fontSizeMultiplier, maxFontSize);
                
                // Add theme name
                labelGroup.append("text")
                    .attr("text-anchor", "middle")
                    .attr("dominant-baseline", "central")
                    .attr("class", "theme-title")
                    .style("font-size", fontSize + "px")
                    .append("tspan")
                    .attr("x", 0)
                    .attr("y", -d.r / 10)
                    .text(d.data.name);
                
                // Add count
                labelGroup.append("text")
                    .attr("text-anchor", "middle")
                    .attr("dominant-baseline", "central")
                    .attr("class", "theme-count")
                    .style("font-size", fontSize + "px")
                    .append("tspan")
                    .attr("x", 0)
                    .attr("y", d.r / 5)
                    .text(`${d.data.formattedCount} (${d.data.percentage}%)`);
            }
        });
        
        // Initial highlight based on current value
        highlightThemes(value);
    }
    
    // Replace legacy reactive statement with $effect
    $effect(() => {
        if (value !== undefined && themeNodes.length > 0) {
            highlightThemes(value);
        }
    });

    // Function to log all circle names for debugging
    function logCircleNames() {
        console.log("=== All Circle Names ===");
        
        // Get all actual circle elements
        const circleElements = d3.selectAll(".theme-circle").nodes();
        
        // Log each circle with its full class list
        circleElements.forEach((circleEl, i) => {
            // Get full class attribute value
            const fullClassValue = circleEl.getAttribute("class");
            
            // Get the corresponding node data for additional context
            const nodeData = themeNodes.find(node => 
                node.depth === 1 && 
                fullClassValue.includes(`circle-${normalizeForCSS(node.data.name)}`)
            );
            
            const themeName = nodeData ? nodeData.data.name : "Unknown";
            
            console.log(`Circle ${i+1}:`);
            console.log(`  Theme name: "${themeName}"`);
            console.log(`  Normalized CSS class: "circle-${normalizeForCSS(themeName)}"`);
            console.log(`  Full class value: "${fullClassValue}"`);
            console.log("-----------------");
        });
        
        console.log(`Total circles: ${circleElements.length}`);
        console.log("======================");
    }
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
    :global(.theme-circle) {
        transition: all 0.3s ease;
    }
    
    :global(.theme-circle.dimmed) {
        opacity: 0.3; /* transparent when not highlighted */
    }
    
    :global(.theme-circle.highlighted) {
        opacity: 0.95; /* Almost fully opaque when highlighted */
        stroke-width: 2px; /* Thicker border */
    }
    
    /* Label styling */
    :global(.theme-title),
    :global(.theme-count) {
        fill: #1e1d1d;
        font-weight: 400;
        font-family: Arial !important;
        transition: opacity 0.3s ease;
    }
    
    :global(.theme-label-group) {
        opacity: 0.5; /* Labels slightly dimmed by default */
        transition: opacity 0.3s ease;
    }
    
    :global(.theme-label-group.highlighted) {
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