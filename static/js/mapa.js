let map;
let markers = [];
let tempMarker = null;
let addingMode = false;
const categorias = window.CATEGORIAS || {};

function initMap() {
    map = L.map('map').setView([-15.7801, -47.9292], 11);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19,
        minZoom: 10
    }).addTo(map);

    const bounds = L.latLngBounds(
        L.latLng(-16.0, -48.3),
        L.latLng(-15.5, -47.3)
    );
    map.setMaxBounds(bounds);

    loadPoints();
    
    loadStats();

    map.on('click', onMapClick);
    
    console.log('Mapa inicializado com sucesso');
}



async function loadPoints(filters = {}) {
    try {
        let url = '/api/pontos';
        const params = new URLSearchParams();
        
        if (filters.categoria) {
            params.append('categoria', filters.categoria);
        }
        if (filters.busca) {
            params.append('busca', filters.busca);
        }
        
        if (params.toString()) {
            url += '?' + params.toString();
        }

        const response = await fetch(url);
        const data = await response.json();

        if (data.sucesso) {
            markers.forEach(marker => map.removeLayer(marker));
            markers = [];

            data.pontos.forEach(ponto => {
                addMarkerToMap(ponto);
            });

            console.log(`${data.total} ponto(s) carregado(s)`);
        } else {
            console.error('Erro ao carregar pontos:', data.erro);
            showToast(data.erro || 'Erro ao carregar pontos', 'error');
        }
    } catch (error) {
        console.error('Erro ao carregar pontos:', error);
        showToast('Erro ao carregar pontos', 'error');
    }
}

function addMarkerToMap(ponto) {
    const categoria = categorias[ponto.categoria] || categorias['outros'];
    
    const icon = L.divIcon({
        className: 'custom-marker',
        html: `<div style="background-color: ${categoria.cor}; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>`,
        iconSize: [30, 30],
        iconAnchor: [15, 15],
        popupAnchor: [0, -15]
    });

    const marker = L.marker([ponto.latitude, ponto.longitude], { icon })
        .addTo(map)
        .bindPopup(createPopupContent(ponto));

    markers.push(marker);
}

function createPopupContent(ponto) {
    const categoria = categorias[ponto.categoria] || categorias['outros'];
    
    return `
        <div style="min-width: 220px; padding: 5px;">
            <h3 style="margin: 0 0 10px 0; color: ${categoria.cor}; font-size: 16px; font-weight: 600;">
                ${ponto.nome}
            </h3>
            <p style="margin: 5px 0; font-size: 12px; color: #666;">
                <strong>Categoria:</strong> ${categoria.nome}
            </p>
            ${ponto.descricao ? `
                <p style="margin: 8px 0; font-size: 13px; color: #334155; line-height: 1.4;">
                    ${ponto.descricao}
                </p>
            ` : ''}
            <p style="margin: 8px 0 10px 0; font-size: 11px; color: #999; font-family: monospace;">
                📍 ${ponto.latitude.toFixed(6)}, ${ponto.longitude.toFixed(6)}
            </p>
            <button onclick="deletePonto(${ponto.id})" 
                style="width: 100%; padding: 8px; background: #dc2626; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500; transition: background 0.2s;">
                🗑️ Excluir Ponto
            </button>
        </div>
    `;
}



function onMapClick(e) {
    if (!addingMode) return;

    if (tempMarker) {
        map.removeLayer(tempMarker);
    }

    tempMarker = L.marker(e.latlng, {
        icon: L.divIcon({
            className: 'temp-marker',
            html: '<div style="background-color: #f59e0b; width: 35px; height: 35px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3); animation: pulse 1.5s infinite;"></div>',
            iconSize: [35, 35],
            iconAnchor: [17.5, 17.5],
            popupAnchor: [0, -17]
        })
    }).addTo(map);

    // Abre popup de formulário
    tempMarker.bindPopup(createAddPointForm(e.latlng.lat, e.latlng.lng), {
        maxWidth: 300,
        closeButton: false
    }).openPopup();
}

function createAddPointForm(lat, lng) {
    const categoriaOptions = Object.entries(categorias)
        .map(([key, cat]) => `<option value="${key}">${cat.nome}</option>`)
        .join('');

    return `
        <div class="popup-form" style="padding: 5px;">
            <h3 style="margin: 0 0 12px 0; font-size: 16px; color: #1e293b; font-weight: 600;">
                ➕ Novo Ponto
            </h3>
            <form id="popupForm" onsubmit="submitPoint(event, ${lat}, ${lng})">
                <div style="margin-bottom: 10px;">
                    <label style="display: block; margin-bottom: 4px; font-size: 13px; font-weight: 500; color: #475569;">Nome:</label>
                    <input type="text" id="popup-nome" required maxlength="200" 
                        style="width: 100%; padding: 8px; border: 2px solid #e2e8f0; border-radius: 6px; font-size: 14px; font-family: inherit;">
                </div>
                
                <div style="margin-bottom: 10px;">
                    <label style="display: block; margin-bottom: 4px; font-size: 13px; font-weight: 500; color: #475569;">Categoria:</label>
                    <select id="popup-categoria" required 
                        style="width: 100%; padding: 8px; border: 2px solid #e2e8f0; border-radius: 6px; font-size: 14px; cursor: pointer;">
                        <option value="">Selecione...</option>
                        ${categoriaOptions}
                    </select>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <label style="display: block; margin-bottom: 4px; font-size: 13px; font-weight: 500; color: #475569;">Descrição (Opcional):</label>
                    <textarea id="popup-descricao" maxlength="1000" rows="3"
                        style="width: 100%; padding: 8px; border: 2px solid #e2e8f0; border-radius: 6px; font-size: 13px; resize: vertical; font-family: inherit;"></textarea>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                    <button type="button" onclick="cancelAddPoint()" 
                        style="padding: 10px; background: #64748b; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500;">
                        Cancelar
                    </button>
                    <button type="submit" 
                        style="padding: 10px; background: #16a34a; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500;">
                        💾 Salvar
                    </button>
                </div>
            </form>
        </div>
    `;
}

async function submitPoint(event, lat, lng) {
    event.preventDefault();

    const dados = {
        nome: document.getElementById('popup-nome').value,
        categoria: document.getElementById('popup-categoria').value,
        descricao: document.getElementById('popup-descricao').value || '',
        latitude: lat,
        longitude: lng
    };

    try {
        const response = await fetch('/api/pontos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        const result = await response.json();

        if (result.sucesso || response.status === 201) {
            showToast('✅ Ponto adicionado com sucesso!', 'success');
            cancelAddPoint();
            loadPoints();
            loadStats();
        } else {
            showToast(result.erro || 'Erro ao adicionar ponto', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao adicionar ponto', 'error');
    }
}

function cancelAddPoint() {
    addingMode = false;
    
    if (tempMarker) {
        map.removeLayer(tempMarker);
        tempMarker = null;
    }
    
    const addBtn = document.getElementById('addBtn');
    if (addBtn) {
        addBtn.innerHTML = '<i class="fas fa-plus-circle"></i> Adicionar Novo Ponto';
        addBtn.style.background = '';
    }
    
    map.closePopup();
}


async function deletePonto(id) {
    if (!confirm('⚠️ Tem certeza que deseja excluir este ponto?')) {
        return;
    }

    try {
        const response = await fetch(`/api/pontos/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (result.sucesso) {
            showToast('✅ Ponto excluído com sucesso!', 'success');
            map.closePopup();
            loadPoints();
            loadStats();
        } else {
            showToast(result.erro || 'Erro ao excluir ponto', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao excluir ponto', 'error');
    }
}

async function loadStats() {
    try {
        const response = await fetch('/api/estatisticas');
        const data = await response.json();

        if (data.sucesso) {
            const stats = data.estatisticas;
            const total = Object.values(stats).reduce((sum, val) => sum + val, 0);

            let statsHtml = `
                <div class="stat-card">
                    <div class="stat-value">${total}</div>
                    <div class="stat-label">Total de Pontos</div>
                </div>
            `;

            Object.entries(stats).forEach(([key, value]) => {
                const cat = categorias[key];
                if (cat) {
                    statsHtml += `
                        <div class="stat-card" style="border-left: 4px solid ${cat.cor};">
                            <div class="stat-value" style="font-size: 1.5rem;">${value}</div>
                            <div class="stat-label">${cat.nome}</div>
                        </div>
                    `;
                }
            });

            document.getElementById('stats').innerHTML = statsHtml;
        }
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
        document.getElementById('stats').innerHTML = '<p style="color: #ef4444; font-size: 0.875rem;">Erro ao carregar estatísticas</p>';
    }
}


function showToast(message, type = 'info') {
    let toast = document.getElementById('toast');
    
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = 'toast hidden';
        document.body.appendChild(toast);
    }

    toast.textContent = message;
    toast.className = 'toast';
    
    if (type === 'error') {
        toast.style.background = '#dc2626';
    } else if (type === 'success') {
        toast.style.background = '#16a34a';
    } else {
        toast.style.background = '#334155';
    }

    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3500);
}



document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM carregado, inicializando...');
    
    initMap();

    const addBtn = document.getElementById('addBtn');
    if (addBtn) {
        addBtn.addEventListener('click', function() {
            addingMode = !addingMode;
            
            if (addingMode) {
                this.innerHTML = '<i class="fas fa-times"></i> Cancelar Adição';
                this.style.background = '#dc2626';
                showToast('📍 Clique no mapa para adicionar um ponto', 'info');
            } else {
                cancelAddPoint();
            }
        });
    }

    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            const filters = {
                categoria: this.value,
                busca: document.getElementById('searchInput')?.value || ''
            };
            loadPoints(filters);
        });
    }

    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const filters = {
                    categoria: document.getElementById('categoryFilter')?.value || '',
                    busca: this.value
                };
                loadPoints(filters);
            }, 500);
        });
    }

    const clearBtn = document.getElementById('clearFilters');
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            const categoryFilter = document.getElementById('categoryFilter');
            const searchInput = document.getElementById('searchInput');
            
            if (categoryFilter) categoryFilter.value = '';
            if (searchInput) searchInput.value = '';
            
            loadPoints();
            showToast('Filtros limpos', 'info');
        });
    }

    const toggleBtn = document.getElementById('toggleSidebar');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            const sidebar = document.getElementById('sidebar');
            const icon = this.querySelector('i');
            
            sidebar.classList.toggle('collapsed');
            
            if (sidebar.classList.contains('collapsed')) {
                icon.classList.remove('fa-chevron-left');
                icon.classList.add('fa-chevron-right');
            } else {
                icon.classList.remove('fa-chevron-right');
                icon.classList.add('fa-chevron-left');
            }
        });
    }

    const toggleStatsBtn = document.getElementById('toggleStats');
    if (toggleStatsBtn) {
        toggleStatsBtn.addEventListener('click', function() {
            const statsSection = document.querySelector('.stats-section');
            if (statsSection) {
                statsSection.style.display = statsSection.style.display === 'none' ? 'block' : 'none';
            }
        });
    }

    const exportBtn = document.getElementById('exportData');
    if (exportBtn) {
        exportBtn.addEventListener('click', async function() {
            try {
                const response = await fetch('/api/pontos/export/geojson');
                const data = await response.json();
                
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `geopoints_${new Date().toISOString().split('T')[0]}.geojson`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                showToast('✅ Dados exportados com sucesso!', 'success');
            } catch (error) {
                console.error('Erro ao exportar:', error);
                showToast('Erro ao exportar dados', 'error');
            }
        });
    }
});

const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
            opacity: 1;
        }
        50% {
            transform: scale(1.15);
            opacity: 0.7;
        }
    }
    
    .leaflet-popup-content-wrapper {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .leaflet-popup-tip {
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
`;
document.head.appendChild(style);
