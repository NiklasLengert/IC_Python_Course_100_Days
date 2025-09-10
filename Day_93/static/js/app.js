// Enhanced Pokédex Scraper JavaScript

class PokemonScraper {
    constructor() {
        this.isScrapingActive = false;
        this.currentPage = 1;
        this.itemsPerPage = 20;
        this.totalItems = 0;
        this.filters = {
            type: 'all',
            generation: 'all',
            search: ''
        };
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.initializeScrollToTop();
        this.initializeTooltips();
        this.loadInitialData();
    }
    
    bindEvents() {
        // Search functionality
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.filters.search = e.target.value.toLowerCase();
                    this.filterPokemon();
                }, 300);
            });
        }
        
        // Filter chips
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('filter-chip')) {
                this.handleFilterChip(e.target);
            }
        });
        
        // Load more button
        const loadMoreBtn = document.getElementById('load-more-btn');
        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', () => this.loadMorePokemon());
        }
        
        // Scraping controls
        const startBtn = document.getElementById('start-scraping-btn');
        if (startBtn) {
            startBtn.addEventListener('click', () => this.startScraping());
        }
        
        // Scroll to top
        window.addEventListener('scroll', () => this.handleScroll());
        
        // Infinite scroll
        window.addEventListener('scroll', () => this.handleInfiniteScroll());
    }
    
    async startScraping() {
        if (this.isScrapingActive) return;
        
        this.isScrapingActive = true;
        this.updateScrapingButton(true);
        
        try {
            const response = await fetch('/start_scraping', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to start scraping');
            }
            
            this.startProgressTracking();
            this.showToast('Scraping started successfully!', 'success');
            
        } catch (error) {
            console.error('Error starting scraping:', error);
            this.showToast('Failed to start scraping. Please try again.', 'error');
            this.isScrapingActive = false;
            this.updateScrapingButton(false);
        }
    }
    
    async startProgressTracking() {
        const progressContainer = document.getElementById('progress-container');
        const progressRing = document.getElementById('progress-ring');
        const progressText = document.getElementById('progress-text');
        const progressDetails = document.getElementById('progress-details');
        const timeEstimate = document.getElementById('time-estimate');
        
        if (!progressContainer) return;
        
        progressContainer.style.display = 'block';
        
        const checkProgress = async () => {
            try {
                const response = await fetch('/progress');
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Update progress ring
                const percentage = data.percentage || 0;
                const circumference = 2 * Math.PI * 45;
                const offset = circumference - (percentage / 100) * circumference;
                
                if (progressRing) {
                    progressRing.style.strokeDashoffset = offset;
                }
                
                // Update text elements
                if (progressText) {
                    progressText.textContent = `${Math.round(percentage)}%`;
                }
                
                if (progressDetails) {
                    progressDetails.innerHTML = `
                        <div class="d-flex justify-content-between mb-2">
                            <span>Completed:</span>
                            <span><strong>${data.completed || 0}/${data.total || 151}</strong></span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span>Current:</span>
                            <span><strong>${data.current_pokemon || 'Initializing...'}</strong></span>
                        </div>
                        <div class="d-flex justify-content-between">
                            <span>Status:</span>
                            <span class="text-primary"><strong>${data.status || 'Starting...'}</strong></span>
                        </div>
                    `;
                }
                
                if (timeEstimate && data.eta) {
                    timeEstimate.textContent = `ETA: ${data.eta}`;
                }
                
                // Check if scraping is complete
                if (data.status === 'completed' || percentage >= 100) {
                    this.completeScraping(data);
                    return;
                }
                
                if (data.status === 'error') {
                    throw new Error(data.message || 'Scraping failed');
                }
                
                // Continue polling
                setTimeout(checkProgress, 2000);
                
            } catch (error) {
                console.error('Error checking progress:', error);
                this.showToast(`Progress tracking error: ${error.message}`, 'error');
                this.isScrapingActive = false;
                this.updateScrapingButton(false);
            }
        };
        
        checkProgress();
    }
    
    completeScraping(data) {
        this.isScrapingActive = false;
        this.updateScrapingButton(false);
        
        // Update final progress
        const progressText = document.getElementById('progress-text');
        const progressDetails = document.getElementById('progress-details');
        
        if (progressText) {
            progressText.textContent = '100%';
        }
        
        if (progressDetails) {
            progressDetails.innerHTML = `
                <div class="text-center">
                    <i class="fas fa-check-circle fa-2x text-success mb-2"></i>
                    <div><strong>Scraping Complete!</strong></div>
                    <div class="small text-muted">
                        ${data.completed || 151} Pokémon collected
                    </div>
                </div>
            `;
        }
        
        // Show completion message
        this.showToast('Pokédex scraping completed successfully!', 'success');
        
        // Add view data button
        setTimeout(() => {
            const completionActions = document.createElement('div');
            completionActions.className = 'text-center mt-3';
            completionActions.innerHTML = `
                <a href="/data" class="btn btn-success me-2">
                    <i class="fas fa-database me-2"></i>View Data
                </a>
                <a href="/download" class="btn btn-info">
                    <i class="fas fa-download me-2"></i>Download CSV
                </a>
            `;
            
            const progressContainer = document.getElementById('progress-container');
            if (progressContainer) {
                progressContainer.appendChild(completionActions);
            }
        }, 1000);
    }
    
    updateScrapingButton(isActive) {
        const startBtn = document.getElementById('start-scraping-btn');
        if (!startBtn) return;
        
        if (isActive) {
            startBtn.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2"></span>
                Scraping in Progress...
            `;
            startBtn.disabled = true;
            startBtn.classList.add('btn-secondary');
            startBtn.classList.remove('btn-primary');
        } else {
            startBtn.innerHTML = `
                <i class="fas fa-play me-2"></i>
                Start Scraping
            `;
            startBtn.disabled = false;
            startBtn.classList.add('btn-primary');
            startBtn.classList.remove('btn-secondary');
        }
    }
    
    async loadInitialData() {
        const pokemonGrid = document.getElementById('pokemon-grid');
        if (!pokemonGrid) return;
        
        try {
            const response = await fetch(`/api/pokemon?page=1&per_page=${this.itemsPerPage}`);
            const data = await response.json();
            
            if (data.data && data.data.length > 0) {
                this.totalItems = data.total || 0;
                this.updatePagination(data);
            }
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }
    
    async loadMorePokemon() {
        const loadMoreBtn = document.getElementById('load-more-btn');
        if (!loadMoreBtn) return;
        
        loadMoreBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
        loadMoreBtn.disabled = true;
        
        try {
            this.currentPage++;
            const response = await fetch(`/api/pokemon?page=${this.currentPage}&per_page=${this.itemsPerPage}`);
            const data = await response.json();
            
            if (data.data && data.data.length > 0) {
                this.appendPokemonCards(data.data);
                this.updatePagination(data);
                this.updateStatBars();
            }
        } catch (error) {
            console.error('Error loading more Pokemon:', error);
            this.showToast('Failed to load more Pokémon', 'error');
        } finally {
            loadMoreBtn.innerHTML = '<i class="fas fa-plus me-2"></i>Load More Pokémon';
            loadMoreBtn.disabled = false;
        }
    }
    
    appendPokemonCards(pokemonList) {
        const grid = document.getElementById('pokemon-grid');
        if (!grid) return;
        
        pokemonList.forEach((pokemon, index) => {
            const card = this.createPokemonCard(pokemon);
            // Stagger animation
            setTimeout(() => {
                grid.appendChild(card);
            }, index * 100);
        });
    }
    
    createPokemonCard(pokemon) {
        const div = document.createElement('div');
        div.className = 'col-xl-3 col-lg-4 col-md-6 mb-4 pokemon-item';
        div.dataset.name = pokemon.name.toLowerCase();
        div.dataset.type = pokemon.type_1.toLowerCase();
        div.dataset.number = pokemon.number;
        
        const type2Badge = pokemon.type_2 ? 
            `<span class="type-badge type-${pokemon.type_2.toLowerCase()}">${pokemon.type_2}</span>` : '';
        
        div.innerHTML = `
            <div class="card pokemon-card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <span class="badge bg-secondary pokemon-font">#${String(pokemon.number).padStart(3, '0')}</span>
                        <div>
                            <span class="type-badge type-${pokemon.type_1.toLowerCase()}">${pokemon.type_1}</span>
                            ${type2Badge}
                        </div>
                    </div>
                    
                    <h5 class="card-title pokemon-font text-center mb-3">${pokemon.name}</h5>
                    
                    <div class="row text-center mb-3">
                        <div class="col-4">
                            <small class="text-muted d-block">Height</small>
                            <strong>${pokemon.height_m}m</strong>
                        </div>
                        <div class="col-4">
                            <small class="text-muted d-block">Weight</small>
                            <strong>${pokemon.weight_kg}kg</strong>
                        </div>
                        <div class="col-4">
                            <small class="text-muted d-block">BMI</small>
                            <strong>${pokemon.bmi || 'N/A'}</strong>
                        </div>
                    </div>

                    <div class="mb-3">
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <small class="text-muted">Base Stats</small>
                            <small class="badge bg-primary">${pokemon.stat_total}</small>
                        </div>
                        <div class="stat-bar" data-width="${Math.round(pokemon.stat_total / 800 * 100)}"></div>
                    </div>

                    <div class="row small text-muted">
                        <div class="col-6">HP: ${pokemon.stat_hp}</div>
                        <div class="col-6">ATK: ${pokemon.stat_attack}</div>
                        <div class="col-6">DEF: ${pokemon.stat_defense}</div>
                        <div class="col-6">SPE: ${pokemon.stat_speed}</div>
                    </div>
                </div>
            </div>
        `;
        
        return div;
    }
    
    filterPokemon() {
        const pokemonItems = document.querySelectorAll('.pokemon-item');
        let visibleCount = 0;
        
        pokemonItems.forEach(item => {
            const name = item.dataset.name;
            const type = item.dataset.type;
            const number = item.dataset.number;
            
            let matches = true;
            
            // Search filter
            if (this.filters.search) {
                matches = matches && (
                    name.includes(this.filters.search) || 
                    type.includes(this.filters.search) || 
                    number.includes(this.filters.search)
                );
            }
            
            // Type filter
            if (this.filters.type !== 'all') {
                matches = matches && type === this.filters.type;
            }
            
            if (matches) {
                item.style.display = 'block';
                item.classList.add('animate__fadeIn');
                visibleCount++;
            } else {
                item.style.display = 'none';
            }
        });
        
        // Update results count
        this.updateResultsCount(visibleCount);
    }
    
    updateResultsCount(count) {
        const resultsCount = document.getElementById('results-count');
        if (resultsCount) {
            resultsCount.textContent = `Showing ${count} Pokémon`;
        }
    }
    
    handleFilterChip(chip) {
        // Remove active class from all chips
        document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked chip
        chip.classList.add('active');
        
        // Update filter
        const filterType = chip.dataset.filter;
        const filterValue = chip.dataset.value;
        
        if (filterType === 'type') {
            this.filters.type = filterValue;
        } else if (filterType === 'generation') {
            this.filters.generation = filterValue;
        }
        
        this.filterPokemon();
    }
    
    updateStatBars() {
        // Animate stat bars
        setTimeout(() => {
            const statBars = document.querySelectorAll('.stat-bar[data-width]');
            statBars.forEach(bar => {
                const width = bar.dataset.width + '%';
                bar.style.width = width;
            });
        }, 100);
    }
    
    updatePagination(data) {
        const loadMoreBtn = document.getElementById('load-more-btn');
        if (loadMoreBtn) {
            if (data.page >= data.total_pages || data.data.length < this.itemsPerPage) {
                loadMoreBtn.style.display = 'none';
            } else {
                loadMoreBtn.style.display = 'block';
            }
        }
    }
    
    handleScroll() {
        const scrollToTopBtn = document.querySelector('.scroll-to-top');
        if (scrollToTopBtn) {
            if (window.pageYOffset > 300) {
                scrollToTopBtn.classList.add('visible');
            } else {
                scrollToTopBtn.classList.remove('visible');
            }
        }
    }
    
    handleInfiniteScroll() {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 1000) {
            const loadMoreBtn = document.getElementById('load-more-btn');
            if (loadMoreBtn && loadMoreBtn.style.display !== 'none' && !loadMoreBtn.disabled) {
                this.loadMorePokemon();
            }
        }
    }
    
    initializeScrollToTop() {
        const scrollToTopBtn = document.createElement('div');
        scrollToTopBtn.className = 'scroll-to-top';
        scrollToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
        scrollToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        document.body.appendChild(scrollToTopBtn);
    }
    
    initializeTooltips() {
        // Initialize Bootstrap tooltips if available
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
        }
    }
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        toast.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas ${this.getToastIcon(type)} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close btn-close-white ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Auto hide after 5 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }
    
    getToastIcon(type) {
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };
        return icons[type] || icons.info;
    }
}

// Performance monitoring
class PerformanceMonitor {
    constructor() {
        this.metrics = {
            loadTime: 0,
            renderTime: 0,
            memoryUsage: 0,
            networkRequests: 0
        };
        this.init();
    }
    
    init() {
        this.measureLoadTime();
        this.monitorNetworkRequests();
        this.measureMemoryUsage();
    }
    
    measureLoadTime() {
        window.addEventListener('load', () => {
            const perfData = performance.getEntriesByType('navigation')[0];
            this.metrics.loadTime = perfData.loadEventEnd - perfData.loadEventStart;
            this.updatePerformanceDisplay();
        });
    }
    
    monitorNetworkRequests() {
        const originalFetch = window.fetch;
        window.fetch = (...args) => {
            this.metrics.networkRequests++;
            this.updatePerformanceDisplay();
            return originalFetch(...args);
        };
    }
    
    measureMemoryUsage() {
        if (performance.memory) {
            this.metrics.memoryUsage = performance.memory.usedJSHeapSize / 1024 / 1024;
            this.updatePerformanceDisplay();
        }
    }
    
    updatePerformanceDisplay() {
        const metricsContainer = document.getElementById('performance-metrics');
        if (metricsContainer) {
            metricsContainer.innerHTML = `
                <div class="metric-card">
                    <span class="metric-value">${Math.round(this.metrics.loadTime)}ms</span>
                    <div class="metric-label">Load Time</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${this.metrics.networkRequests}</span>
                    <div class="metric-label">API Calls</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${Math.round(this.metrics.memoryUsage)}MB</span>
                    <div class="metric-label">Memory Usage</div>
                </div>
            `;
        }
    }
}

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    const scraper = new PokemonScraper();
    const monitor = new PerformanceMonitor();
    
    // Initialize stat bars animation on data page
    scraper.updateStatBars();
    
    console.log('🚀 Pokédex Scraper initialized successfully!');
});
