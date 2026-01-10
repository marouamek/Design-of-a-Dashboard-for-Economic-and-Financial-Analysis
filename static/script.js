// ===========================================================================
// Variables globales / mapping
// ===========================================================================

// Données globales pour les graphiques
let ipcDataGlobal = [];
let pieChart = null;
let filtreAnneeInitialise = false;
// Ajout : registre des graphiques multi-lignes par id
const lineMultiCharts = {};

// Mapping des groupes (si besoin d'évolution plus tard)
const group_map = {
    alimentation: "alimentation",
    sante: "sante",
    logement: "logement",
    transport: "transport"
};

// Mapping des sous-groupes par identifiant de graphique
const sous_groupe_map = {
    ChartCereales: [
        "pain et cereales",
        "sucre et produits sucres",
    ],

    ChartViandes: [
        "viande et abats de mouton",
        "viande et abats de boeuf",
        "volaille, lapin et oeuf",
        "poisson frais",
        "viandes et poissons en conserve",
    ],

    ChartLegumesFruits: [
        "legumes",
        "fruits",
        "pommes de terre",
    ],

    ChartHuilesLait: [
        "huiles et graisses",
        "lait fromage et derives",
    ],

    ChartBoissons: [
        "boissons non alcoolisees",
        "cafe the et infusion",
    ],

    ChartAutresAliments: [
        "autres produits alimentaires",
    ],

    ChartEnergie: [
        "electricite et gaz",
        "combustibles",
    ],

    ChartEau: [
        "eau potable",
    ],

    ChartLogement: [
        "loyers et charges",
        "entretien et reparation",
    ],

    ChartMedicament: [
        "medicaments sur ordonnance",
        "medicaments non remboursables",
    ],

    ChartSoinsMed: [
        "appareils et materiels therapeutiques",
        "soins et services medicaux",
    ],

    ChartCosmetiques: [
        "biens et articles de toilette",
        "coiffure, bain et douche",
    ],

    ChartVehicules: [
        "achat vehicules, cycles et motocycles",
        "autres depenses pour vehicules"
    ],

    ChartEntretienVehicules: [
        "reparation et entretien de vehicules",
        "pieces detachees et accessoires vehicule"
    ],

    ChartTransportsPublics: [
        "transports"
    ],

    ChartTelecommunications: [
        "postes et telecommunications"
    ]
};


// ===========================================================================
// Initialisation de la page
// ===========================================================================

// Page actuelle (définie dans le template HTML via data-page)
const page = document.body.dataset.page;

// Au chargement de la page : on charge toutes les données nécessaires
window.onload = function () {
    loadData(page);
};


// ===========================================================================
// Chargement principal des données
// ===========================================================================

// Cette fonction charge les données en fonction de la page actuelle
// - réinitialise les boutons toggle (IPC actif par défaut)
// - effectue les requêtes AJAX
// - met à jour les graphiques et le HTML
function loadData(page) {
    // Réinitialisation des boutons toggle au chargement (IPC par défaut)
    const toggleButtons = document.querySelectorAll('.toggle-btn-var');
    toggleButtons.forEach(button => button.classList.remove('active'));

    // Activation du bouton toggle IPC par défaut
    for (const btn of toggleButtons) {
        if (btn.dataset.type === 'ipc') {
            btn.classList.add('active');
        }
    }

    if (page === 'home') {
        // ---------------------
        // Page d'accueil (home)
        // ---------------------

        // 1) Données pour les 4 cartes principales
        let httpRequest = new XMLHttpRequest();
        httpRequest.open('GET', '/api/cardsData');
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === 4) {
                if (httpRequest.status === 200) {
                    const response = httpRequest.response;
                    const jsonData = JSON.parse(response);
                    document.querySelector('#stat1 .statPop').textContent = jsonData[0];
                    document.querySelector('#stat2 .statPop').textContent = jsonData[1];
                    document.querySelector('#stat3 .statPop').textContent = jsonData[2];
                    document.querySelector('#stat4 .statPop').textContent = jsonData[3] + "%";
                } else {
                    alert("Erreur les données n'ont pas pu être chargées");
                }
            }
        };
        httpRequest.send();

        // 2) Graphique à barres IPC général
        let httpRequest1 = new XMLHttpRequest();
        httpRequest1.open('GET', '/api/ipcGeneral');
        httpRequest1.onreadystatechange = function () {
            if (httpRequest1.readyState === 4 && httpRequest1.status === 200) {
                const response = httpRequest1.response;
                const jsonData1 = JSON.parse(response);
                update_Bars('IPCgeneralChart', jsonData1);
            }
        };
        httpRequest1.send();

        // 3) Graphique en lignes variation IPC général
        let httpRequest2 = new XMLHttpRequest();
        httpRequest2.open('GET', '/api/varIpcGeneral');
        httpRequest2.onreadystatechange = function () {
            if (httpRequest2.readyState === 4) {
                if (httpRequest2.status === 200) {
                    const response = httpRequest2.response;
                    const jsonData2 = JSON.parse(response);
                    console.log(jsonData2);
                    update_Lines('VarChart', jsonData2);
                } else {
                    alert("Erreur les données n'ont pas pu être chargées");
                }
            }
        };
        httpRequest2.send();

        // 4) Graphique en lignes IPC général 2024
        let httpRequest3 = new XMLHttpRequest();
        httpRequest3.open('GET', '/api/ipcGeneral2024');
        httpRequest3.onreadystatechange = function () {
            if (httpRequest3.readyState === 4 && httpRequest3.status === 200) {
                const jsonData4 = JSON.parse(httpRequest3.response);
                update_Lines('IPCgeneralChart2024', jsonData4);
            }
        };
        httpRequest3.send();

        // 5) Graphique en camembert par groupe + filtre année
        let httpRequest4 = new XMLHttpRequest();
        httpRequest4.open('GET', '/api/ipcParGroupe');
        httpRequest4.onreadystatechange = function () {
            if (httpRequest4.readyState === 4 && httpRequest4.status === 200) {
                const jsonData1 = JSON.parse(httpRequest4.response);

                // garder toutes les années globalement pour le filtre année
                ipcDataGlobal = jsonData1;

                if (Array.isArray(jsonData1) && jsonData1.length > 0) {
                    // remplir le select ANNEE seulement 1 fois
                    if (!filtreAnneeInitialise) {
                        remplirFiltreAnnee(jsonData1);
                        filtreAnneeInitialise = true;
                    }

                    // afficher par défaut la première année
                    const firstYear = jsonData1[0];
                    afficherPieParAnnee(firstYear.annee);

                } else {
                    update_Pie('GroupeChart', []);
                }
            }
        };
        httpRequest4.send();
    } else {
        // -------------------------------
        // Pages alimentation / logement /
        // santé / transport
        // -------------------------------

        // 1) Donut IPC général par groupe
        let httpRequest1 = new XMLHttpRequest();
        httpRequest1.open('GET', '/api/ipcDonut/' + page);
        httpRequest1.onreadystatechange = function () {
            if (httpRequest1.readyState === 4 && httpRequest1.status === 200) {
                const jsonData1 = JSON.parse(httpRequest1.response);
                update_Donut('IPC_' + page + '_general', jsonData1);
            }
        };
        httpRequest1.send();

        // 2) Top 3 sous-groupes avec plus d'inflation
        let httpRequest2 = new XMLHttpRequest();
        httpRequest2.open('GET', '/api/top3Inflation/' + page);
        httpRequest2.onreadystatechange = function () {
            if (httpRequest2.readyState === 4 && httpRequest2.status === 200) {
                const jsonData2 = JSON.parse(httpRequest2.response);
                const labels = jsonData2.map(item => item.label);
                const values = jsonData2.map(item => item.variation);

                // Mettre à jour le HTML avec les données des sous-groupes
                labels.forEach((label, index) => {
                    document.getElementById('label-sous-groupe' + index).textContent = label;
                    document.getElementById('value-sous-groupe' + index).textContent = values[index] + '%';
                });
            }
        };
        httpRequest2.send();

        // 3) Graphique en barres : évolution IPC
        let httpRequest3 = new XMLHttpRequest();
        httpRequest3.open('GET', '/api/ipc/' + page);
        httpRequest3.onreadystatechange = function () {
            if (httpRequest3.readyState === 4 && httpRequest3.status === 200) {
                const jsonData3 = JSON.parse(httpRequest3.response);
                update_Bars('IPCgeneral_' + page + '_evolution', jsonData3);
            }
        };
        httpRequest3.send();

        // 4) Graphique en lignes : variation IPC
        let httpRequest4 = new XMLHttpRequest();
        httpRequest4.open('GET', '/api/var/' + page);
        httpRequest4.onreadystatechange = function () {
            if (httpRequest4.readyState === 4 && httpRequest4.status === 200) {
                const jsonData4 = JSON.parse(httpRequest4.response);
                update_Lines('Var_' + page + '_chart', jsonData4);
            }
        };
        httpRequest4.send();

        // 5) Détails IPC pour les sous-groupes selon la page
        if (page === 'alimentation') {
            // sous-groupes alimentation : indices 0 à 5
            loadDetailsIPC(page, 0, 5);
        } else if (page === 'logement') {
            // sous-groupes logement : indices 6 à 8
            loadDetailsIPC(page, 6, 8);
        } else if (page === 'sante') {
            // sous-groupes santé : indices 9 à 11
            loadDetailsIPC(page, 9, 11);
        } else if (page === 'transport') {
            // sous-groupes transport : indices 12 à 15
            loadDetailsIPC(page, 12, 15);
        }
    }
}


// ===========================================================================
// Détails IPC / VAR par sous-groupe
// ===========================================================================

// Chargement des détails IPC pour les sous-groupes (graphique multi-lignes)
function loadDetailsIPC(page, min, max) {
    for (let i = min; i <= max; i++) {
        const key = Object.keys(sous_groupe_map)[i];
        let httpRequest = new XMLHttpRequest();
        httpRequest.open('GET', '/api/ipcDetails/' + page + '/' + key);
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === 4 && httpRequest.status === 200) {
                const jsonData4 = JSON.parse(httpRequest.response);
                update_Lines_multiple(key, jsonData4);
            }
        };
        httpRequest.send();
    }
}

// Chargement des détails VAR pour les sous-groupes (non utilisé partout, mais prêt)
function loadDetailsVar(page, min, max) {
    for (let i = min; i <= max; i++) {
        const key = Object.keys(sous_groupe_map)[i];
        let httpRequest = new XMLHttpRequest();
        httpRequest.open('GET', '/api/varDetails/' + page + '/' + key);
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === 4 && httpRequest.status === 200) {
                const jsonData4 = JSON.parse(httpRequest.response);
                update_Lines_multiple(key, jsonData4);
            }
        };
        httpRequest.send();
    }
}


// ===========================================================================
// Toggles IPC / VAR sur les cartes
// ===========================================================================

// Active / désactive visuellement les boutons IPC / VAR de chaque carte
function initChartToggles() {
    const ANIM_MS = 360;

    document.querySelectorAll('.card').forEach(card => {
        const btns = card.querySelectorAll('.toggle-btn-var');

        btns.forEach(btn => {
            btn.addEventListener('click', () => {
                btns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Après l'animation, on force un resize pour que Chart.js se recalcule
                setTimeout(() => window.dispatchEvent(new Event('resize')), ANIM_MS + 20);
            });
        });
    });
}

document.addEventListener('DOMContentLoaded', initChartToggles);


// ===========================================================================
// Fonctions de mise à jour des graphiques
// ===========================================================================

// Graphique en lignes avec plusieurs datasets (sous-groupes)
function update_Lines_multiple(idGraph, jsonData) {
        const ctx = document.getElementById(idGraph).getContext('2d');

    // Détruire l'ancien graphique s'il existe sur ce canvas
    if (lineMultiCharts[idGraph]) {
        lineMultiCharts[idGraph].destroy();
    }
    lineMultiCharts[idGraph] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: jsonData.labels, // Années [2015, 2016, ...]
            datasets: jsonData.datasets.map((dataset, index) => ({
                label: dataset.label,
                data: dataset.data,
                borderColor: getColor(index),
                tension: 0.4,
                fill: false,
                borderWidth: 2
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: true
            },
            scales: {
                y: {
                    beginAtZero: true,
                }
            }
        }
    });
}

// Palette de couleurs pour les multi-lignes
function getColor(index) {
    const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#5be25f', '#9966FF'];
    return colors[index % colors.length];
}

// Graphique en barres
function update_Bars(idGraph, jsonData) {
    new Chart(document.getElementById(idGraph), {
        type: 'bar',
        data: {
            labels: jsonData.labels,
            datasets: [{
                label: 'Indice generale IPC',
                backgroundColor: "#3e95cd",
                data: jsonData.data
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: true
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// Graphique en lignes simple (1 dataset)
function update_Lines(idGraph, jsonData) {
    new Chart(document.getElementById(idGraph), {
        type: 'line',
        data: {
            labels: jsonData.labels,
            datasets: [{
                label: 'Evolution',
                data: jsonData.data,
                fill: false,
                borderColor: '#4e73df',
                borderWidth: 2,
                radius: 3,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: true
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// Graphique en camembert (pie)
function update_Pie(idGraph, jsonData) {
    const labels = jsonData.map(e => e.region);
    const data = jsonData.map(e => e.population);

    const ctx = document.getElementById(idGraph);

    // Si un graphique existe déjà, le détruire
    if (pieChart) {
        pieChart.destroy();
        pieChart = null;
    }

    // Créer le nouveau graphique et stocker l'instance dans la variable globale
    pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: "Population (millions)",
                backgroundColor: [
                    '#313e91',
                    '#1C4D8D',
                    '#4988C4',
                    '#5A7ACD',
                    '#8CA9FF',
                    '#52bbbb',
                    '#8CE4FF',
                    '#BDE8F5'
                ],
                data: data
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            legend: {
                position: 'right'
            }
        }
    });
}

// Graphique en donut (doughnut)
let donutChart = null;

function update_Donut(idGraph, jsonData) {
    if (donutChart) {
        donutChart.destroy();
        donutChart = null;
    }

    donutChart = new Chart(document.getElementById(idGraph), {
        type: 'doughnut',
        data: {
            labels: jsonData.labels,
            datasets: [{
                label: "Taux IPC",
                backgroundColor: ["#3661d8", "#e7e7ff"],
                data: jsonData.data
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            legend: {
                display: true,
                position: 'right'
            }
        }
    });
}


// ===========================================================================
// Filtre année (camembert)
// ===========================================================================

// Remplit le select des années à partir des données reçues
function remplirFiltreAnnee(data) {
    const select = document.getElementById('anneeSelect');
    select.innerHTML = '';

    data.forEach(item => {
        const option = document.createElement('option');
        option.value = item.annee;
        option.textContent = item.annee;
        select.appendChild(option);
    });

    select.onchange = function () {
        afficherPieParAnnee(this.value);
    };
}

// Affiche le camembert pour une année donnée
function afficherPieParAnnee(annee) {
    const yearData = ipcDataGlobal.find(y => y.annee == annee);

    if (yearData) {
        const pieArray = yearData.groupes.map(g => ({
            region: g.label,
            population: g.ipc
        }));

        // détruire l'ancien graphique si déjà créé
        if (pieChart) {
            pieChart.destroy();
            pieChart = null;
        }

        update_Pie('GroupeChart', pieArray);

        // récupérer la nouvelle instance du camembert
        pieChart = Chart.getChart("GroupeChart");
    }
}


// ===========================================================================
// Slider horizontal des groupes
// ===========================================================================

// Déplace le slider principal vers la gauche / droite
function moveSlider(direction) {
    const container = document.getElementById('mainSlider');
    const scrollAmount = container.clientWidth;
    const maxScroll = container.scrollWidth - container.clientWidth;

    // Calcul de la position cible
    const targetScroll = container.scrollLeft + (direction * scrollAmount);

    // Logique rotationnelle
    if (targetScroll > maxScroll + 10) {
        // Si on dépasse la fin, on revient au début
        container.scrollTo({ left: 0, behavior: 'smooth' });
    } else if (targetScroll < -10) {
        // Si on dépasse le début, on va à la fin
        container.scrollTo({ left: maxScroll, behavior: 'smooth' });
    } else {
        // Déplacement normal
        container.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
    }
}


// ===========================================================================
// Sidebar (état ouvert / fermé)
// ===========================================================================

const toggleBtn = document.getElementById('toggleSidebar');
const sidebar = document.getElementById('sidebar');
const SIDEBAR_KEY = 'sidebarCollapsed';

// État initial : fermé la première fois
let isCollapsed = localStorage.getItem(SIDEBAR_KEY);
if (isCollapsed === null) {
    isCollapsed = 'true'; // première visite => fermé
    localStorage.setItem(SIDEBAR_KEY, 'true');
}

if (isCollapsed === 'true') {
    sidebar.classList.add('collapsed');
    document.body.classList.add('sidebar-collapsed');
} else {
    sidebar.classList.remove('collapsed');
    document.body.classList.remove('sidebar-collapsed');
}

// Toggle de la sidebar + sauvegarde dans localStorage
toggleBtn.addEventListener('click', function () {
    const nowCollapsed = sidebar.classList.toggle('collapsed');
    document.body.classList.toggle('sidebar-collapsed');
    localStorage.setItem(SIDEBAR_KEY, nowCollapsed ? 'true' : 'false');
});