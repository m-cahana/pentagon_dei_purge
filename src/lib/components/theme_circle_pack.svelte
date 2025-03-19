<script>
    import * as d3 from 'd3';
    import { onMount } from 'svelte';
    
    let dataPath = '/data/cleaned_titles_with_themes.csv'; // Path to the data file
    let colorScheme = [
                "#3F3B2E", // Jacko Bean
                "#A4895C", // Café Au Lait
                "#5B533F", // Olive Drab Camouflage
                "#736246", // Boy Red
                "#96794E", // Pale Brown
                "#252B1F", // Pine Tree
                "#57453B", // Dark Brown (from French Camouflage)
                "#8A705D", // Medium Brown (from French Camouflage)
                "#534E3B", // Olive Gray (from French Camouflage)
                "#4A5A3F", // Army Green (from Green Camouflage)
                "#8E965B", // Olive Green (from Green Camouflage)
                "#46B030"  // Military Green (from Bright Camouflage)
            ];
    
    let container;
    let width;
    let height;
    let data = {name: "root", children: []};
    
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
    function formatNumber(num) {
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
            .catch(error => {
                console.error("Error loading CSV:", error);
            });
            
        // Clean up event listeners on component destruction
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    });

    // Process the CSV data into a hierarchical structure for circle packing
    function processData(csvData) {
        // Group titles by theme
        const themeGroups = d3.group(csvData, d => d.theme || "Unknown");

        const totalTitles = csvData.length;
        
        // Convert to hierarchical structure for circle packing
        data = {
            name: "root",
            children: Array.from(themeGroups, ([theme, titles]) => ({
                name: theme,
                value: titles.length,
                percentage: (titles.length / totalTitles * 100).toFixed(1),
                formattedCount: formatNumber(titles.length),
                children: titles.map(title => ({
                    name: title.title,
                    value: 1
                }))
            }))
        };
        
        // Sort by size (descending)
        data.children.sort((a, b) => b.value - a.value);
        
        return data;
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
                .force('collision', d3.forceCollide().radius(d => d.r + 3).strength(0.8))
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
        const allNodes = createForceLayout();
        const themeNodes = allNodes.filter(node => node.depth === 1);
        
        // Create a container for all circles
        const nodes = svg.append("g")
            .selectAll("g")
            .data(allNodes)
            .join("g")
            .attr("transform", d => `translate(${d.x},${d.y})`);
        
        // Add circles
        nodes.append("circle")
            .attr("r", d => d.r)
            .attr("fill", d => d.depth === 1 ? color(d.data.name) : "white")
            .attr("fill-opacity", d => d.depth === 1 ? 0.8 : 0)
            .attr("stroke", d => d.depth === 1 ? "#fff" : "none")
            .attr("stroke-width", d => d.depth === 1 ? 1 : 0)
            .attr("class", d => `circle-${d.data.name.replace(/\s+/g, '-').toLowerCase()}`)
            
        // Create a new group specifically for labels that will be on top of everything
        const labelsGroup = svg.append("g")
            .attr("class", "labels-container")
            .raise(); // Explicitly raise this group to the top of the SVG
        
        // Re-create the labels in this top-level group
        themeNodes.forEach(d => {
            if (d.depth === 1) {
                const labelGroup = labelsGroup.append("g")
                    .attr("transform", `translate(${d.x},${d.y})`)
                    .attr("class", "theme-label-group")
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
            
        // Add a tooltip
        const tooltip = d3.select("body").select(".theme-tooltip") || 
            d3.select("body").append("div")
                .attr("class", "theme-tooltip")
                .style("position", "absolute")
                .style("padding", "8px")
                .style("background", "rgba(255, 255, 255, 0.9)")
                .style("border", "1px solid #ddd")
                .style("border-radius", "4px")
                .style("pointer-events", "none")
                .style("font-size", "14px")
                .style("font-family", "Arial, sans-serif")
                .style("box-shadow", "0 2px 4px rgba(0, 0, 0, 0.1)")
                .style("z-index", "100")
                .style("text-align", "center")
                .style("opacity", 0);
    }
</script>

<div class="theme-circle-pack">
    
    <div class="visualization-container">
        <div class="theme-circle-pack__container" bind:this={container}>
            <!-- Circle packing visualization will be rendered here -->
        </div>
    </div>
</div>

<style>
    .theme-circle-pack {
        width: 100%;
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .visualization-container {
        position: relative;
        width: 100%;
        height: auto;
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
    
    h1 {
        text-align: center;
        margin-bottom: 20px;
        font-size: 24px;
        width: 100%;
        font-family: Helvetica !important;
        font-weight: 300 !important;
    }
    
    /* Label styling */
    :global(.theme-title),
    :global(.theme-count) {
        fill: #1e1d1d;
        font-weight: 400;
        font-family: Arial !important;
    }
    
    /* Media query for small screens */
    @media (max-width: 768px) {
        .theme-circle-pack {
            padding: 10px;
        }
        
        h1 {
            font-size: 20px;
        }
        
        .theme-circle-pack__container {
            height: 60vh;
        }
        
        /* Adjust label text sizes for smaller screens */
        :global(.theme-title),
        :global(.theme-count) {
            font-weight: 500; /* Slightly reduced weight for better readability at small sizes */
        }
    }
    
    /* Media query for very small screens */
    @media (max-width: 480px) {
        .theme-circle-pack__container {
            height: 50vh;
        }
    }
</style> 