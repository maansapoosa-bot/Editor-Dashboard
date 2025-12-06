
const colors = {
    primary: '#3b82f6',   // Blue
    secondary: '#10b981', // Emerald
    accent: '#f59e0b',    // Amber
    danger: '#ef4444',    // Red
    purple: '#8b5cf6',    // Violet
    teal: '#14b8a6'       // Teal
};

const palette = [colors.primary, colors.secondary, colors.accent, colors.purple, colors.teal, colors.danger];

// Common Options
const commonOptions = {
    responsive: true,
    maintainAspectRatio: false, // Critical for custom sizing
    plugins: {
        legend: {
            position: 'bottom',
            labels: {
                usePointStyle: true,
                padding: 20,
                font: {
                    family: "'Inter', sans-serif",
                    size: 12
                }
            }
        }
    },
    layout: {
        padding: 10
    }
};

// Doughnut Chart (Posts by Author)
new Chart(document.getElementById('authorChart'), {
    type: 'doughnut',
    data: {
        labels: authorLabels,
        datasets: [{
            data: authorData,
            backgroundColor: palette,
            borderWidth: 0,
            hoverOffset: 4
        }]
    },
    options: {
        ...commonOptions,
        cutout: '70%', // Thinner ring
    }
});



// Line Chart
new Chart(document.getElementById('timeChart'), {
    type: 'line',
    data: {
        labels: dateLabels,
        datasets: [{
            label: 'Posts Published',
            data: dateData,
            borderColor: colors.primary,
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            tension: 0.4, // Smooth curves
            fill: true,
            pointRadius: 4,
            pointBackgroundColor: '#fff',
            pointBorderColor: colors.primary,
            pointBorderWidth: 2
        }]
    },
    options: {
        ...commonOptions,
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    display: true,
                    color: 'rgba(0,0,0,0.05)'
                },
                ticks: {
                    stepSize: 1
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        }
    }
});

// Bar Chart
new Chart(document.getElementById('topEditorsChart'), {
    type: 'bar',
    data: {
        labels: topEditorLabels,
        datasets: [{
            label: 'Total Posts',
            data: topEditorData,
            backgroundColor: colors.accent,
            borderRadius: 6, // Rounded bars
            barThickness: 30
        }]
    },
    options: {
        ...commonOptions,
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0,0,0,0.05)'
                },
                ticks: {
                    stepSize: 1
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        }
    }
});
