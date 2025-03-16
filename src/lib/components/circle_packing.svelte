<script>
    import * as d3 from 'd3';
    import { onMount } from 'svelte';
    
    let container;
    let titles;
    let width = 800;
    let height = 800;
    let margin = 20;
    let svg;
    let simulation;
    let currentSection = 0;
    let sections = [];
    let scrollyContainer;
    let isVisualizationVisible = false;
    let isInitialized = false;
    let scrollProgress = 0; // Track scroll progress

    // Helper function to format numbers with commas
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    onMount(() => {
        // Use a path relative to the static/public folder
        d3.csv('/data/cleaned_titles_with_keywords.csv')
            .then((data) => {
                titles = data;
                console.log("Data loaded:", titles.slice(0, 5));
                
                // Check what columns are available
                if (titles.length > 0) {
                    console.log("Available columns:", Object.keys(titles[0]));
                }
                
                // Create visualization but keep it hidden initially
                createVisualization(titles);
                setupScrolly();
                
                // Set initialized flag after everything is set up
                isInitialized = true;
                
                // Force initial check for visibility
                checkVisualizationVisibility();
                
                // Set initial section
                if (sections.length > 0) {
                    updateVisualization(0);
                }
            })
            .catch(error => {
                console.error("Error loading CSV:", error);
                console.error("Make sure to copy your CSV file to the static folder!");
                console.error("Run this command in your terminal:");
                console.error("mkdir -p static && cp data/processed/cleaned_titles_with_keywords.csv static/");
            });
    });

    function checkVisualizationVisibility() {
        // Only check visibility if initialization is complete
        if (!isInitialized || !container || !scrollyContainer) return;
        
        // Get the position of the circle-packing container and scrolly sections
        const containerRect = container.getBoundingClientRect();
        const scrollySections = scrollyContainer.querySelectorAll('.scrolly-section');
        const windowHeight = window.innerHeight;
        
        // Check if any scrolly section is in view
        let isAnyScrollySectionVisible = false;
        let isFirstSectionVisible = false;
        
        scrollySections.forEach((section, index) => {
            const rect = section.getBoundingClientRect();
            if (rect.top < windowHeight && rect.bottom > 0) {
                isAnyScrollySectionVisible = true;
                
                // Check if this is the first section
                if (index === 0) {
                    isFirstSectionVisible = true;
                }
            }
        });
        
        // Get the circle-packing element
        const circlePacking = document.querySelector('.circle-packing');
        const circlePackingRect = circlePacking ? circlePacking.getBoundingClientRect() : null;
        
        // Calculate scroll progress for the circle-packing element
        if (circlePackingRect) {
            // Calculate how far the element has been scrolled into view
            // 0 = just entering view from bottom, 1 = fully in view
            scrollProgress = Math.min(1, Math.max(0, 
                (windowHeight - circlePackingRect.top) / (windowHeight + circlePackingRect.height)
            ));
        }
        
        const wasVisible = isVisualizationVisible;
        
        // Show visualization when either:
        // 1. The circle-packing container is at least partially in view
        // 2. Any scrolly section is in view
        if ((circlePackingRect && circlePackingRect.top < windowHeight && circlePackingRect.bottom > 0) || 
            isAnyScrollySectionVisible) {
            isVisualizationVisible = true;
            
            // If we're showing the visualization for the first time or returning to the first section,
            // reset to zoomed out view
            if ((!wasVisible || isFirstSectionVisible) && svg) {
                resetZoom();
            }
        } else {
            isVisualizationVisible = false;
        }
    }

    // Helper function to reset zoom to show all circles
    function resetZoom() {
        if (!svg) return;
        
        svg.transition()
            .duration(1000)
            .attr("transform", `translate(${margin},${margin}) scale(1)`);
            
        // Show all circles equally
        svg.selectAll("circle")
            .transition()
            .duration(1000)
            .attr("opacity", 0.8);
            
        svg.selectAll("text")
            .transition()
            .duration(1000)
            .attr("opacity", 1);
    }

    function createVisualization(titlesData) {
        // Clear any existing SVG
        d3.select(container).selectAll("svg").remove();
        
        // Process data to get counts by keyword group
        const keywordGroups = processData(titlesData);
        console.log("Keyword groups:", keywordGroups);
        
        // Calculate total count for percentages
        const totalCount = keywordGroups.reduce((sum, group) => sum + group.count, 0);
        
        // Add percentage to each group
        keywordGroups.forEach((group, i) => {
            group.percentage = (group.count / totalCount * 100).toFixed(1);
            group.formattedCount = formatNumber(group.count); // Add formatted count
            group.id = i; // Add an ID for each group to reference in scrolly
        });
        
        // Create SVG
        svg = d3.select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", `translate(${margin},${margin})`);
            
        // Create a color scale
        const color = d3.scaleOrdinal()
            .domain(keywordGroups.map(d => d.group))
            .range(d3.schemeCategory10);
            
        // Size scale for circles - INCREASED SIZE RANGE
        const size = d3.scaleLinear()
            .domain([0, d3.max(keywordGroups, d => d.count)])
            .range([30, 120]); // Increased from [10, 80]
            
        // Create a simulation with forces
        simulation = d3.forceSimulation(keywordGroups)
            .force("center", d3.forceCenter(width/2 - margin, height/2 - margin))
            .force("charge", d3.forceManyBody().strength(100)) 
            .force("collide", d3.forceCollide().radius(d => size(d.count) + 2).iterations(8))
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
            .attr("class", d => `circle-${d.id}`)
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
            
        // Add labels to the circles
        const labels = svg.selectAll("text")
            .data(keywordGroups)
            .join("text")
            .attr("text-anchor", "middle")
            .attr("dominant-baseline", "middle")
            .attr("class", d => `label-${d.id}`)
            .text(d => `${d.group} (${d.percentage}%)`)
            .style("font-size", "11px") 
            .style("font-family", "sans-serif")
            .style("font-weight", "bold") 
            .style("pointer-events", "none")
            .style("fill", "#333");
            
        // Tick function for the simulation
        function ticked() {
            circles
                .attr("cx", d => {
                    return d.x = Math.max(size(d.count), Math.min(width - margin*2 - size(d.count), d.x));
                })
                .attr("cy", d => {
                    return d.y = Math.max(size(d.count), Math.min(height - margin*2 - size(d.count), d.y));
                });
                
            labels
                .attr("x", d => d.x)
                .attr("y", d => d.y);
        }
        
        // Add title
        svg.append("text")
            .attr("x", (width - margin*2) / 2)
            .attr("y", 0)
            .attr("text-anchor", "middle")
            .style("font-size", "16px")
            .style("font-weight", "bold")
            .text("Keyword Groups by Title Count");
            
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
        
        // Create sections for scrollytelling based on top groups
        sections = keywordGroups.slice(0, 5).map(group => ({
            id: group.id,
            title: group.group,
            count: group.count,
            formattedCount: group.formattedCount,
            percentage: group.percentage,
            description: `The "${group.group}" keyword group contains ${group.formattedCount} titles, representing ${group.percentage}% of all Pentagon job titles.`
        }));
        
    }
    
    function setupScrolly() {
        // Set up scroll event listener for both scrolly and visibility
        window.addEventListener('scroll', () => {
            handleScroll();
            checkVisualizationVisibility();
        });
        
        // Initial check for current section
        handleScroll();
    }
    
    function handleScroll() {
        if (!scrollyContainer) return;
        
        const scrollSections = scrollyContainer.querySelectorAll('.scrolly-section');
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
    
    function updateVisualization(sectionIndex) {
        if (!svg || sections.length === 0) return;
        
        const section = sections[sectionIndex];
        
        // Reset all circles
        svg.selectAll("circle")
            .transition()
            .duration(1000)
            .attr("opacity", 0.3); // Make non-focused circles more transparent
            
        svg.selectAll("text")
            .transition()
            .duration(1000)
            .attr("opacity", 0.3);
        
        // If we're on the overview section, show all circles equally
        if (section.id === -1) {
            // Reset zoom
            svg.transition()
                .duration(1000)
                .attr("transform", `translate(${margin},${margin}) scale(1)`);
                
            // Show all circles
            svg.selectAll("circle")
                .transition()
                .duration(1000)
                .attr("opacity", 0.8);
                
            svg.selectAll("text")
                .transition()
                .duration(1000)
                .attr("opacity", 1);
                
            return;
        }
        
        // Highlight the current circle
        const currentCircle = svg.select(`.circle-${section.id}`);
        const currentLabel = svg.select(`.label-${section.id}`);
        
        if (!currentCircle.empty()) {
            // Get the circle's position and radius
            const cx = parseFloat(currentCircle.attr("cx"));
            const cy = parseFloat(currentCircle.attr("cy"));
            const r = parseFloat(currentCircle.attr("r"));
            
            // Calculate zoom scale (make the circle take up about 1/3 of the view)
            const scale = Math.min(width, height) / (r * 6);
            
            // Zoom to the circle - center it in the viewport
            svg.transition()
                .duration(1000)
                .attr("transform", `translate(${width/2 - cx * scale},${height/2 - cy * scale}) scale(${scale})`);
                
            // Highlight the current circle
            currentCircle.transition()
                .duration(1000)
                .attr("opacity", 1)
                .attr("stroke-width", 2 / scale)
                .attr("stroke", "#333");
                
            currentLabel.transition()
                .duration(1000)
                .attr("opacity", 1)
                .style("font-size", `${11 / scale}px`)
                .style("font-weight", "bold");
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
        return result.filter(d => d.count >= 5).sort((a, b) => b.count - a.count);
    }
</script>

<div class="circle-packing">
   <h1>Pentagon Titles by Keyword Group</h1>
   
   <div class="visualization-container">
       <div class="circle-packing__container" 
            bind:this={container} 
            class:visible={isVisualizationVisible}>
           <!-- D3 visualization will be rendered here -->
       </div>
       
       <!-- Add a placeholder to ensure the container has height before visualization is visible -->
       <div class="placeholder" style="height: 100vh;"></div>
       
       <div class="scrolly-container" bind:this={scrollyContainer}>
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
                                       <span class="stat-label">Titles</span>
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
   
   {#if !titles}
       <p class="loading">Loading data... (If this persists, check console for errors)</p>
   {/if}
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
    }
    
    .circle-packing__container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        border: none;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1;
        opacity: 0;
        visibility: hidden;
        transition: opacity 1s ease-in-out, visibility 0s linear 1s;
        transform: translateY(100vh); /* Start off-screen at the bottom */
        transition: opacity 1s ease-in-out, visibility 0s linear 1s, transform 1s ease-in-out;
    }
    
    .circle-packing__container.visible {
        opacity: 1;
        visibility: visible;
        transform: translateY(0); /* Move to center when visible */
        transition: opacity 1s ease-in-out, visibility 0s linear, transform 1s ease-in-out;
    }
    
    .placeholder {
        width: 100%;
        position: relative;
        z-index: 0;
        height: 100vh; /* Ensure consistent height */
    }
    
    .scrolly-container {
        position: relative;
        z-index: 2;
        pointer-events: none; /* Allow clicks to pass through to the visualization */
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
    
    /* Make SVG responsive */
    :global(svg) {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 0 auto;
    }
    
    h1 {
        text-align: center;
        margin-bottom: 20px;
        font-size: 24px;
        width: 100%;
    }
    
    h2 {
        margin-top: 0;
        margin-bottom: 10px;
        font-size: 20px;
    }
    
    .loading {
        text-align: center;
        font-style: italic;
        color: #666;
        width: 100%;
    }
    
    /* Media query for small screens */
    @media (max-width: 768px) {
        .circle-packing {
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
    }
</style>