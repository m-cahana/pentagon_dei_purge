<script>
    import * as d3 from 'd3';
    import { onMount } from 'svelte';
    
    // Props for customization
    export let dataPath = '/data/cleaned_titles_with_keywords.csv'; // Path to the data file
    export let title = 'Purged Websites by Theme'; // Main title
    export let narratives = []; // Optional pre-defined narratives
    
    let container;
    let scrollContainer;
    let titles;
    let width;
    let height;
    let margin = 20;
    let svg;
    let simulation;
    let resizeTimer;
    let keywordGroups = [];
    let currentSection = 0;
    let sections = [];
    let isVisualizationVisible = false;
    let isInitialized = false;

    // Helper function to format numbers with commas
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    // Function to handle window resize
    function handleResize() {
        // Clear any previous resize timer
        clearTimeout(resizeTimer);
        
        // Set a timer to avoid excessive redraws during resize
        resizeTimer = setTimeout(() => {
            if (titles) {
                updateVisualizationSize();
                createVisualization(titles);
                
                // Reset to current section after resize
                setTimeout(() => {
                    updateVisualization(currentSection);
                }, 100);
            }
        }, 250);
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
        
        console.log(`Container size updated: ${width}x${height}`);
    }

    onMount(() => {
        // Initialize size based on container
        updateVisualizationSize();
        
        // Add resize listener
        window.addEventListener('resize', handleResize);
        
        // Add scroll listener
        window.addEventListener('scroll', handleScroll);
        
        // Use a path relative to the static/public folder
        d3.csv(dataPath)
            .then((data) => {
                titles = data;
                console.log("Data loaded:", titles.slice(0, 5));
                
                // Check what columns are available
                if (titles.length > 0) {
                    console.log("Available columns:", Object.keys(titles[0]));
                }
                
                // Process data
                keywordGroups = processData(titles);
                
                // Create visualization
                createVisualization(titles);
                
                // Set up sections for scrollytelling
                setupSections();
                
                // Set initialized flag
                isInitialized = true;
                
                // Initial check for visibility
                setTimeout(() => {
                    checkVisualizationVisibility();
                    updateVisualization(0);
                }, 500);
            })
            .catch(error => {
                console.error("Error loading CSV:", error);
                console.error("Make sure to copy your CSV file to the static folder!");
            });
            
        // Clean up event listeners on component destruction
        return () => {
            window.removeEventListener('resize', handleResize);
            window.removeEventListener('scroll', handleScroll);
        };
    });
    
    function setupSections() {
        // If narratives were provided as props, use those
        if (narratives && narratives.length > 0) {
            sections = narratives;
            return;
        }
        
        // Otherwise, create sections based on circles in the visualization
        // First section is overview
        sections = [{
            id: -1,
            title: "Overview",
            description: "This visualization shows the main themes of purged websites. Scroll down to explore each theme in detail.",
            group: null
        }];
        
        // Find all circles in the visualization
        const circles = container.querySelectorAll('circle');
        const labels = container.querySelectorAll('text');
        
        console.log("Found circles:", circles.length);
        
        // Create a section for each circle (up to 5)
        const maxSections = Math.min(5, circles.length);
        
        for (let i = 0; i < maxSections; i++) {
            const circle = circles[i];
            const label = labels[i];
            
            if (circle && label) {
                // Extract group name and percentage from label text
                const labelText = label.textContent || '';
                const match = labelText.match(/(.*) \((\d+\.\d+)%\)/);
                
                if (match) {
                    const groupName = match[1];
                    const percentage = match[2];
                    
                    // Get count from circle radius (approximate)
                    const radius = parseFloat(circle.getAttribute('r') || '0');
                    const count = Math.round(radius * 10); // Approximate count based on radius
                    
                    sections.push({
                        id: i,
                        title: groupName,
                        count: count,
                        formattedCount: count.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
                        percentage: percentage,
                        description: `The "${groupName}" theme contains approximately ${count.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")} purged websites, representing ${percentage}% of all purged content.`,
                        circle: circle,
                        label: label
                    });
                }
            }
        }
        
        console.log("Scrolly sections created:", sections);
    }
    
    function checkVisualizationVisibility() {
        if (!container || !scrollContainer) return;
        
        const containerRect = container.getBoundingClientRect();
        const scrollContainerRect = scrollContainer.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        
        // Check if the intro section is in view
        const introSection = document.querySelector('.intro-section');
        const introRect = introSection ? introSection.getBoundingClientRect() : null;
        
        // Check if the end spacer is in view
        const endSpacer = document.querySelector('.end-spacer');
        const endRect = endSpacer ? endSpacer.getBoundingClientRect() : null;
        
        // Calculate when the visualization should become fixed
        // Only change state when the intro section has scrolled significantly (at least 50% out of view)
        // to prevent flickering at the transition point
        const shouldBeVisible = 
            (introRect && introRect.bottom < windowHeight * 0.5) && 
            !(endRect && endRect.top < windowHeight * 0.8);
            
        // Only update if the state is changing to prevent unnecessary re-renders
        if (shouldBeVisible !== isVisualizationVisible) {
            isVisualizationVisible = shouldBeVisible;
            
            // If becoming visible, ensure the SVG is properly sized
            if (isVisualizationVisible && svg) {
                // Small delay to ensure smooth transition
                setTimeout(() => {
                    updateVisualization(currentSection);
                }, 50);
            }
        }
    }
    
    function handleScroll() {
        checkVisualizationVisibility();
        
        // Update current section based on scroll position
        if (!scrollContainer) return;
        
        const scrollSections = scrollContainer.querySelectorAll('.scrolly-section');
        let newSection = 0;
        
        // Find which section is currently in view
        scrollSections.forEach((section, i) => {
            const rect = section.getBoundingClientRect();
            
            // If the section is in the viewport
            if (rect.top < window.innerHeight * 0.75 && rect.bottom > window.innerHeight * 0.25) {
                newSection = i;
            }
        });
        
        // Only update if the section changed
        if (newSection !== currentSection) {
            currentSection = newSection;
            updateVisualization(currentSection);
        }
    }

    function createVisualization(titlesData) {
        // Clear any existing SVG
        d3.select(container).selectAll("svg").remove();
        
        console.log(`Creating visualization with dimensions: ${width}x${height}`);
        
        // Create SVG with responsive dimensions
        svg = d3.select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", `0 0 ${width} ${height}`)
            .attr("preserveAspectRatio", "xMidYMid meet")
            .append("g")
            .attr("transform", `translate(${width/2},${height/2})`); // Center the visualization
            
        // Create a color scale
        const color = d3.scaleOrdinal()
            .domain(keywordGroups.map(d => d.group))
            .range([
                "#2D3E40", // Dark military teal
                "#4A5D23", // Army green
                "#3F4A3C", // Olive drab
                "#5D5C61", // Slate gray
                "#7D2E33", // Military maroon
                "#2C3539", // Gunmetal
                "#556B2F", // Dark olive green
                "#36454F", // Charcoal
                "#4E5754", // Feldgrau (German field gray)
                "#1F2937", // Navy blue-gray
                "#5F4B32", // Military brown
                "#3D3B30"  // Taupe gray
            ]);
            
        // Calculate the base size for circles based on container dimensions and screen size
        let baseSize;
        const isSmallScreen = width < 768;
        
        if (isSmallScreen) {
            // Improved sizing for small screens - not too small
            baseSize = Math.min(width, height) / 8;
            console.log(`Small screen detected. Base circle size: ${baseSize}`);
        } else {
            // Larger circles for big screens
            baseSize = Math.min(width, height) / 6;
            console.log(`Large screen detected. Base circle size: ${baseSize}`);
        }
            
        // Size scale for circles - responsive to container size with larger range
        const size = d3.scaleLinear()
            .domain([0, d3.max(keywordGroups, d => d.count)])
            .range(isSmallScreen ? 
                [Math.max(20, baseSize * 0.4), Math.max(60, baseSize * 1.2)] : // Ensure minimum sizes for small screens
                [baseSize * 0.4, baseSize * 1.5]   // Larger range for big screens
            );
            
        // Create a simulation with forces - centered in the middle
        if (simulation) simulation.stop(); // Stop any existing simulation
        
        // Adjust force strength based on container size but ensure it's not too weak on small screens
        const forceStrength = isSmallScreen ? 
            Math.max(30, Math.min(width, height) / 10) :  // Stronger minimum force for small screens
            Math.min(width, height) / 8;    // Stronger force for large screens
        
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
            .style("cursor", "grab")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended))
            .on("mouseover", function() {
                d3.select(this)
                    .attr("stroke", "#333")
                    .attr("stroke-width", 2);
            })
            .on("mouseout", function() {
                d3.select(this)
                    .attr("stroke", "white")
                    .attr("stroke-width", 1);
            });
            
        // Calculate font size based on container dimensions
        const fontSize = isSmallScreen ?
            Math.max(9, Math.min(width, height) / 70) :  // Smaller font for small screens
            Math.max(11, Math.min(width, height) / 60);  // Larger font for big screens
        
        console.log(`Font size: ${fontSize}px`);
            
        // Add labels to the circles
        const labels = svg.selectAll("text")
            .data(keywordGroups)
            .join("text")
            .attr("text-anchor", "middle")
            .attr("dominant-baseline", "middle")
            .attr("class", d => `label-${d.id}`) // Add class for targeting specific labels
            .text(d => `${d.group} (${d.percentage}%)`)
            .style("font-size", `${fontSize}px`) 
            .style("font-family", "sans-serif")
            .style("font-weight", "bold") 
            .style("pointer-events", "none")
            .style("fill", "#333");
            
        // Tick function for the simulation
        function ticked() {
            // Calculate bounds to keep circles within view
            const radius = d => size(d.count);
            const boundWidth = width / 2 - margin;
            const boundHeight = height / 2 - margin;
            
            circles
                .attr("cx", d => {
                    return d.x = Math.max(-boundWidth + radius(d), Math.min(boundWidth - radius(d), d.x));
                })
                .attr("cy", d => {
                    return d.y = Math.max(-boundHeight + radius(d), Math.min(boundHeight - radius(d), d.y));
                });
                
            labels
                .attr("x", d => d.x)
                .attr("y", d => d.y);
        }
    
        // Drag functions
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
            d3.select(this).style("cursor", "grabbing");
        }
        
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
        
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
            d3.select(this).style("cursor", "grab");
        }
    }
    
    function updateVisualization(sectionIndex) {
        if (!isInitialized || !container) return;
        
        const section = sections[sectionIndex];
        const svg = container.querySelector('svg g');
        
        if (!svg) {
            console.error("Could not find SVG element in circle packing visualization");
            return;
        }
        
        // Reset all circles
        const circles = container.querySelectorAll('circle');
        const labels = container.querySelectorAll('text');
        
        circles.forEach(circle => {
            d3.select(circle)
                .transition()
                .duration(1000)
                .attr("opacity", 0.3); // Make non-focused circles more transparent
        });
        
        labels.forEach(label => {
            d3.select(label)
                .transition()
                .duration(1000)
                .attr("opacity", 0.3);
        });
        
        // If we're on the overview section, show all circles equally
        // but don't zoom out if we're on a small screen and already zoomed in
        if (section.id === -1) {
            // Only reset zoom on larger screens or initial view
            const isSmallScreen = window.innerWidth < 768;
            if (!isSmallScreen) {
                // Reset zoom on larger screens
                d3.select(svg)
                    .transition()
                    .duration(1000)
                    .attr("transform", `translate(${svg.getBoundingClientRect().width/2},${svg.getBoundingClientRect().height/2}) scale(1)`);
            }
                
            // Show all circles
            circles.forEach(circle => {
                d3.select(circle)
                    .transition()
                    .duration(1000)
                    .attr("opacity", 0.8);
            });
            
            labels.forEach(label => {
                d3.select(label)
                    .transition()
                    .duration(1000)
                    .attr("opacity", 1);
            });
            
            return;
        }
        
        // For other sections, highlight the specific circle
        if (section.circle) {
            const circle = section.circle;
            const label = section.label;
            
            // Get the circle's position and radius
            const cx = parseFloat(circle.getAttribute("cx") || "0");
            const cy = parseFloat(circle.getAttribute("cy") || "0");
            const r = parseFloat(circle.getAttribute("r") || "0");
            
            // Get SVG dimensions
            const svgRect = svg.getBoundingClientRect();
            const width = svgRect.width;
            const height = svgRect.height;
            
            // Calculate zoom scale (make the circle take up about 1/3 of the view)
            // Use a more moderate scale on small screens
            const isSmallScreen = window.innerWidth < 768;
            const scale = isSmallScreen ? 
                Math.min(width, height) / (r * 8) : // Less zoom on small screens
                Math.min(width, height) / (r * 6);  // More zoom on large screens
            
            // Zoom to the circle - center it in the viewport
            d3.select(svg)
                .transition()
                .duration(1000)
                .attr("transform", `translate(${width/2 - cx * scale},${height/2 - cy * scale}) scale(${scale})`);
                
            // Highlight the current circle
            d3.select(circle)
                .transition()
                .duration(1000)
                .attr("opacity", 1)
                .attr("stroke-width", 2 / scale)
                .attr("stroke", "#333");
                
            if (label) {
                d3.select(label)
                    .transition()
                    .duration(1000)
                    .attr("opacity", 1)
                    .style("font-weight", "bold");
            }
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
            group.id = i; // Add an ID for each group to reference in scrolly
        });
        
        return filteredResult;
    }
</script>

<div class="circle-pack-scroll">
   <h1>{title}</h1>
   
   <!-- Introduction section that scrolls out of view -->
   <div class="intro-section">
       <p class="intro-text">
           Scroll down to explore the main themes of purged websites through an interactive visualization.
           Each circle represents a theme, with size indicating the number of websites in that category.
       </p>
   </div>
   
   <div class="visualization-container">
       <!-- Circle packing container that becomes fixed during scrolling -->
       <div class="circle-packing__container" 
            bind:this={container} 
            class:fixed={isVisualizationVisible}>
           <!-- The existing circle packing visualization will be rendered here -->
       </div>
       
       <!-- Placeholder to maintain scroll space when container becomes fixed -->
       <div class="visualization-placeholder" class:hidden={!isVisualizationVisible}></div>
       
       <div class="scrolly-container" bind:this={scrollContainer}>
           {#if sections.length > 0}
               {#each sections as section, i}
                   <div class="scrolly-section" id={`section-${i}`}>
                       <div class="scrolly-content">
                           <h2>{section.title}</h2>
                           <p>{section.description}</p>
                           {#if section.id >= 0}
                               <div class="stats">
                                   <div class="stat">
                                       <span class="stat-value">{section.formattedCount}</span>
                                       <span class="stat-label">Websites</span>
                                   </div>
                                   <div class="stat">
                                       <span class="stat-value">{section.percentage}%</span>
                                       <span class="stat-label">of Total</span>
                                   </div>
                               </div>
                           {/if}
                       </div>
                   </div>
               {/each}
               <!-- Add a spacer at the end to allow scrolling through all sections -->
               <div class="end-spacer"></div>
           {/if}
       </div>
   </div>
   
   <!-- Conclusion section that appears after scrolling through all sections -->
   <div class="conclusion-section">
       <h2>Explore More</h2>
       <p>
           You've explored the main themes of purged websites. Continue scrolling to see more detailed analyses and findings.
       </p>
   </div>
</div>

<style>
    .circle-pack-scroll {
        width: 100%;
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .intro-section {
        width: 100%;
        min-height: 50vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 40px 20px;
    }
    
    .intro-text {
        font-size: 18px;
        line-height: 1.6;
        max-width: 600px;
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
        /* Remove transition on opacity to prevent visual jumps */
    }
    
    .circle-packing__container.fixed {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        z-index: 1;
        /* Ensure the fixed container has the same dimensions and appearance */
        transform: translateZ(0); /* Force GPU acceleration for smoother transitions */
    }
    
    /* Add a placeholder to maintain scroll space when container becomes fixed */
    .scrolly-container {
        position: relative;
        z-index: 2;
        pointer-events: none; /* Allow clicks to pass through to the visualization */
        /* Remove margin-top to prevent jumps */
    }
    
    /* Add a placeholder div to maintain scroll space */
    .visualization-placeholder {
        height: 80vh;
        min-height: 400px;
        width: 100%;
        transition: opacity 0.3s ease;
    }
    
    .visualization-placeholder.hidden {
        display: none;
    }
    
    .scrolly-section {
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding: 0 20px;
    }
    
    .scrolly-content {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 8px;
        padding: 20px;
        max-width: 350px;
        pointer-events: auto; /* Make the content boxes clickable */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-right: 5%;
    }
    
    /* Add spacer at the end to allow scrolling through all sections */
    .end-spacer {
        height: 50vh;
    }
    
    .conclusion-section {
        width: 100%;
        min-height: 50vh;
        padding: 60px 20px;
        text-align: center;
    }
    
    .stats {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }
    
    .stat {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }
    
    .stat-label {
        font-size: 14px;
        color: #666;
    }
    
    h1 {
        text-align: center;
        margin-bottom: 20px;
        font-size: 24px;
        width: 100%;
        font-family: Helvetica !important;
        font-weight: 300 !important;
    }
    
    h2 {
        margin-top: 0;
        margin-bottom: 10px;
        font-size: 20px;
    }
    
    /* Media query for small screens */
    @media (max-width: 768px) {
        .circle-pack-scroll {
            padding: 10px;
        }
        
        .scrolly-content {
            max-width: 280px;
            padding: 15px;
            margin: 0 10px;
        }
        
        h1 {
            font-size: 20px;
        }
        
        h2 {
            font-size: 18px;
        }
        
        .stat-value {
            font-size: 20px;
        }
        
        .intro-text {
            font-size: 16px;
        }
    }
</style> 