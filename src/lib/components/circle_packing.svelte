<script>
    import * as d3 from 'd3';
    import { onMount } from 'svelte';
    
    // Props for customization
    export let dataPath = '/data/cleaned_titles_with_keywords.csv'; // Path to the data file
    export let title = 'Purged Websites by Theme'; // Main title
    
    let container;
    let width;
    let height;
    let keywordGroups = [];
    let simulation;
    
    // Helper function to format numbers with commas
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
    
    // Function to handle window resize
    function handleResize() {
        updateVisualizationSize();
        if (keywordGroups.length > 0) {
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
        height = Math.max(height, 300);
    }

    onMount(() => {
        // Initialize size based on container
        updateVisualizationSize();
        
        // Add resize listener
        window.addEventListener('resize', handleResize);
        
        // Use a path relative to the static/public folder
        d3.csv(dataPath)
            .then((data) => {
                // Process data
                keywordGroups = processData(data);
                
                // Create visualization
                createVisualization();
            })
            .catch(error => {
                console.error("Error loading CSV:", error);
            });
            
        // Clean up event listeners on component destruction
        return () => {
            window.removeEventListener('resize', handleResize);
            if (simulation) simulation.stop();
        };
    });

    function createVisualization() {
        // Clear any existing SVG
        d3.select(container).selectAll("svg").remove();
        
        // Create SVG with responsive dimensions
        const svg = d3.select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", `0 0 ${width} ${height}`)
            .attr("preserveAspectRatio", "xMidYMid meet")
            .append("g")
            .attr("transform", `translate(${width/2},${height/2})`); // Center the visualization
            
        // Create a color scale with military-inspired colors
        const color = d3.scaleOrdinal()
            .domain(keywordGroups.map(d => d.group))
            .range([
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
            ]);
            
        // Calculate the base size for circles based on container dimensions
        const isSmallScreen = width < 768;
        const baseSize = isSmallScreen ? 
            Math.min(width, height) / 8 : 
            Math.min(width, height) / 6;
            
        // Size scale for circles - responsive to container size
        const size = d3.scaleLinear()
            .domain([0, d3.max(keywordGroups, d => d.count)])
            .range(isSmallScreen ? 
                [Math.max(20, baseSize * 0.4), Math.max(60, baseSize * 1.2)] : // Ensure minimum sizes for small screens
                [baseSize * 0.4, baseSize * 1.5]   // Larger range for big screens
            );
            
        // Create a simulation with forces
        if (simulation) simulation.stop(); // Stop any existing simulation
        
        const margin = 20; // Margin to keep circles from edges
        
        // Calculate force strength based on container size
        const forceStrength = isSmallScreen ? 
            Math.max(30, Math.min(width, height) / 10) :
            Math.min(width, height) / 8;
        
        simulation = d3.forceSimulation(keywordGroups)
            .force("center", d3.forceCenter(0, 0)) // Center at origin (will be translated to center of SVG)
            .force("charge", d3.forceManyBody().strength(forceStrength)) 
            .force("collide", d3.forceCollide().radius(d => size(d.count) + (isSmallScreen ? 2 : 4)).iterations(8))
            .on("tick", ticked);
            
        // Create circles for each keyword group
        const circles = svg.selectAll("circle")
            .data(keywordGroups)
            .join("circle")
            .attr("r", d => size(d.count))
            .attr("fill", d => color(d.group))
            .attr("fill-opacity", 0.8)
            .attr("stroke", "white")
            .attr("stroke-width", 1)
            .attr("class", d => `circle-${d.id}`) // Add class for targeting specific circles
            .style("cursor", "pointer")
            .on("mouseover", function(event, d) {
                d3.select(this)
                    .attr("stroke", "#333")
                    .attr("stroke-width", 2);
                    
                // Show tooltip with count
                tooltip
                    .style("opacity", 1)
                    .html(`<strong>${d.group}</strong><br>${d.formattedCount} websites (${d.percentage}%)`)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 28) + "px");
            })
            .on("mouseout", function() {
                d3.select(this)
                    .attr("stroke", "white")
                    .attr("stroke-width", 1);
                    
                tooltip.style("opacity", 0);
            });
            
        // Calculate font size based on container dimensions
        const fontSize = isSmallScreen ?
            Math.max(9, Math.min(width, height) / 70) :  // Smaller font for small screens
            Math.max(11, Math.min(width, height) / 60);  // Larger font for big screens
            
        // Add labels to the circles
        const labels = svg.selectAll("text")
            .data(keywordGroups)
            .join("text")
            .attr("text-anchor", "middle") // Center text horizontally
            .attr("dominant-baseline", "central") // Better vertical centering
            .attr("class", d => `label-${d.id}`)
            .style("font-size", `${fontSize}px`) 
            .style("font-family", "Arial, sans-serif")
            .style("font-weight", "300") 
            .style("pointer-events", "none")
            .style("fill", "white")
            // Important: Set initial x,y position to match the circle
            .attr("x", d => d.x)
            .attr("y", d => d.y);
            
        // Apply text wrapping to labels with a more accurate centering approach
        labels.each(function(d) {
            const text = d3.select(this);
            const radius = size(d.count);
            const labelText = `${d.group} (${d.percentage}%)`;
            
            // Clear existing content
            text.text(null);
            
            // Calculate max width based on circle radius
            const maxWidth = radius * 1.5;
            
            // Split text into words
            const words = labelText.split(/\s+/);
            const lines = [];
            let currentLine = [];
            
            // Create a temporary text element with proper SVG namespace for more accurate measurements
            const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            document.body.appendChild(svg);
            const testText = document.createElementNS("http://www.w3.org/2000/svg", "text");
            testText.style.fontSize = `${fontSize}px`;
            testText.style.fontFamily = "Arial, sans-serif";
            testText.style.fontWeight = "300";
            svg.appendChild(testText);
            
            // Group words into lines that fit within maxWidth
            for (let i = 0; i < words.length; i++) {
                const word = words[i];
                currentLine.push(word);
                
                // Use the temporary text element to measure width
                testText.textContent = currentLine.join(" ");
                const width = testText.getBBox().width;
                
                if (width > maxWidth && currentLine.length > 1) {
                    currentLine.pop(); // Remove last word
                    lines.push(currentLine.join(" ")); // Add current line
                    currentLine = [word]; // Start new line with current word
                }
            }
            
            // Add the last line
            if (currentLine.length > 0) {
                lines.push(currentLine.join(" "));
            }
            
            // Clean up temporary elements
            document.body.removeChild(svg);
            
            // Add each line as a tspan with precise positioning
            const lineHeight = fontSize * 1.2; // Slightly increase line height for better readability
            const totalHeight = lines.length * lineHeight;
            
            // Calculate starting y position to center text vertically within the circle
            // Use relative positioning for tspans to maintain proper positioning during simulation
            const yOffset = -(totalHeight / 2) + (lineHeight / 2);
            
            lines.forEach((line, i) => {
                text.append("tspan")
                    .attr("x", 0) // Center horizontally (text element already has text-anchor: middle)
                    .attr("dy", i === 0 ? yOffset : lineHeight) // First line has offset, others have lineHeight
                    .text(line);
            });
        });
        
        // Add a tooltip
        const tooltip = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);
            
        // Tick function for the simulation
        function ticked() {
            // Calculate bounds to keep circles within view
            const radius = d => size(d.count);
            const boundWidth = width / 2 - margin;
            const boundHeight = height / 2 - margin;
            
            // First, update circle positions
            circles
                .attr("cx", d => {
                    return d.x = Math.max(-boundWidth + radius(d), Math.min(boundWidth - radius(d), d.x));
                })
                .attr("cy", d => {
                    return d.y = Math.max(-boundHeight + radius(d), Math.min(boundHeight - radius(d), d.y));
                });
                
            // Then, update text positions to match their circles
            // This ensures the text always follows its circle
            labels.attr("x", d => d.x)
                  .attr("y", d => d.y);
        }
    }

    function processData(titlesData) {
        // Group by top_keyword_group and count
        const groupedData = d3.group(titlesData, d => d.top_keyword_group || "Unknown");
        
        // Convert to array of objects with group name and count
        const result = Array.from(groupedData, ([group, titles]) => {
            return {
                group,
                count: titles.length
            };
        });
        
        // Filter out groups with very few titles
        const filteredResult = result
            .filter(d => d.count >= 5)
            .sort((a, b) => b.count - a.count);
            
        // Calculate total count for percentages
        const totalCount = filteredResult.reduce((sum, group) => sum + group.count, 0);
        
        // Add percentage and ID to each group
        filteredResult.forEach((group, i) => {
            group.percentage = (group.count / totalCount * 100).toFixed(1);
            group.formattedCount = formatNumber(group.count);
            group.id = i;
        });
        
        return filteredResult;
    }
</script>

<div class="circle-packing">
   {#if title}<h1>{title}</h1>{/if}
   
   <div class="visualization-container">
       <div class="circle-packing__container" bind:this={container}>
           <!-- Circle packing visualization will be rendered here -->
       </div>
   </div>
</div>

<style>
    .circle-packing {
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
    
    .circle-packing__container {
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
    
    :global(.tooltip) {
        position: absolute;
        padding: 8px;
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #ddd;
        border-radius: 4px;
        pointer-events: none;
        font-size: 14px;
        font-family: Arial, sans-serif;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        z-index: 100;
        text-align: center;
    }
    
    /* Media query for small screens */
    @media (max-width: 768px) {
        .circle-packing {
            padding: 10px;
        }
        
        h1 {
            font-size: 20px;
        }
        
        .circle-packing__container {
            height: 60vh;
        }
    }
</style>