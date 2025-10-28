<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Sistema de Gestão de Pontos de Interesse - Polícia Federal">
    <title>GeoPoints PF - Sistema de Mapeamento</title>
    
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <header class="app-header">
        <div class="header-content">
            <div class="brand">
                <i class="fas fa-map-marked-alt"></i>
                <div>
                    <h1>GeoPoints PF</h1>
                    <p>Sistema de Gestão de Pontos de Interesse</p>
                </div>
            </div>
            <div class="header-actions">
                <button class="btn-icon" id="toggleStats" title="Estatísticas">
                    <i class="fas fa-chart-bar"></i>
                </button>
                <button class="btn-icon" id="exportData" title="Exportar GeoJSON">
                    <i class="fas fa-download"></i>
                </button>
            </div>
        </div>
    </header>

    <main class="app-container">
        <!-- Sidebar -->
        <aside class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <h2><i class="fas fa-sliders-h"></i> Painel de Controle</h2>
                <button class="btn-icon btn-collapse" id="toggleSidebar" title="Ocultar painel">
                    <i class="fas fa-chevron-left"></i>
                </button>
            </div>

            <button class="btn btn-primary btn-block" id="addBtn">
                <i class="fas fa-plus-circle"></i>
                Adicionar Novo Ponto
            </button>

            <div class="filtros-section">
                <h3><i class="fas fa-filter"></i> Filtros</h3>
                
                <div class="form-group">
                    <label for="searchInput">
                        <i class="fas fa-search"></i> Buscar
                    </label>
                    <div class="search-input">
                        <i class="fas fa-search"></i>
                        <input 
                            type="text" 
                            id="searchInput" 
                            class="form-control" 
                            placeholder="Nome ou descrição..."
                        >
                    </div>
                </div>

                <div class="form-group">
                    <label for="categoryFilter">
                        <i class="fas fa-folder"></i> Categoria
                    </label>
                    <select id="categoryFilter" class="form-control">
                        <option value="">Todas as categorias</option>
                        {% for key, cat in categorias.items() %}
                        <option value="{{ key }}">{{ cat.nome }}</option>
                        {% endfor %}
                    </select>
                </div>

                <button class="btn btn-block btn-secondary" id="clearFilters">
                    <i class="fas fa-times"></i> Limpar Filtros
                </button>
            </div>

            <div class="legend-section">
                <h3><i class="fas fa-palette"></i> Legendas</h3>
                <div class="category-legend">
                    {% for key, cat in categorias.items() %}
                    <div class="category-item">
                        <div class="category-color cat-{{ key }}" style="background-color: {{ cat.cor }}"></div>
                        <span>{{ cat.nome }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div class="stats-section">
                <h3><i class="fas fa-chart-pie"></i> Estatísticas</h3>
                <div id="stats" class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">--</div>
                        <div class="stat-label">Total de Pontos</div>
                    </div>
                </div>
            </div>
        </aside>

        <div class="map-container">
            <div id="map"></div>
        </div>
    </main>

    <div id="toast" class="toast hidden"></div>

    <script>
        window.CATEGORIAS = {{ categorias | tojson }};
    </script>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="{{ url_for('static', filename='js/mapa.js') }}"></script>
</body>
</html>
