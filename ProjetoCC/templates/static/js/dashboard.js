function renderiza_grafico_agua(url) {

    fetch(url)
        .then(response => response.json())
        .then(data => {

            const canvas = document.getElementById('grafico_agua');

            if (!canvas) {
                console.error('Canvas grafico_agua não encontrado.');
                return;
            }

            new Chart(canvas, {
                type: 'line',

                data: {
                    labels: data.labels,

                    datasets: [
                        {
                            label: 'Água consumida (L)',
                            data: data.dados,
                            borderWidth: 2,
                            tension: 0.3
                        }
                    ]
                },

                options: {
                    responsive: true,

                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

        })
        .catch(error => {
            console.error('Erro ao carregar gráfico de água:', error);
        });
}


function renderiza_grafico_cardio(url) {

    fetch(url)
        .then(response => response.json())
        .then(data => {

            const canvas = document.getElementById('grafico_cardio');

            if (!canvas) {
                console.error('Canvas grafico_cardio não encontrado.');
                return;
            }

            new Chart(canvas, {
                type: 'line',

                data: {
                    labels: data.labels,

                    datasets: [
                        {
                            label: 'Tempo de cardio (min)',
                            data: data.dados,
                            borderWidth: 1
                        }
                    ]
                },

                options: {
                    responsive: true,

                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

        })
        .catch(error => {
            console.error('Erro ao carregar gráfico de cardio:', error);
        });
}


function renderiza_calendario_adesao(url) {

    fetch(url)
        .then(response => response.json())
        .then(data => {

            criar_calendario(
                'calendario_dieta',
                data,
                'dieta'
            );

            criar_calendario(
                'calendario_treino',
                data,
                'treino'
            );

        })
        .catch(error => {
            console.error(
                'Erro ao carregar calendário de adesão:',
                error
            );
        });
}


function criar_calendario(id, data, tipo) {

    const container = document.getElementById(id);

    if (!container) {
        return;
    }

    container.innerHTML = '';

    const ano = data.ano;
    const mes = data.mes;

    // Nome do mês
    const nomeMes = new Intl.DateTimeFormat(
        'pt-BR',
        {
            month: 'long',
            year: 'numeric'
        }
    ).format(
        new Date(ano, mes - 1, 1)
    );

    const titulo = document.createElement('h4');

    titulo.textContent =
        nomeMes.charAt(0).toUpperCase()
        + nomeMes.slice(1);

    container.appendChild(titulo);


    // Grade do calendário
    const calendario = document.createElement('div');

    calendario.classList.add('calendario');


    // Dias da semana
    const diasSemana = [
        'Seg',
        'Ter',
        'Qua',
        'Qui',
        'Sex',
        'Sáb',
        'Dom'
    ];

    diasSemana.forEach(dia => {

        const elemento = document.createElement('div');

        elemento.classList.add('dia-semana');

        elemento.textContent = dia;

        calendario.appendChild(elemento);

    });


    // Descobre em qual dia da semana começa o mês
    const primeiroDia = new Date(
        ano,
        mes - 1,
        1
    ).getDay();

    // JavaScript considera domingo = 0.
    // Aqui transformamos segunda-feira em primeiro dia.
    const espacosAntes = (primeiroDia + 6) % 7;


    // Cria espaços vazios antes do dia 1
    for (let i = 0; i < espacosAntes; i++) {

        const vazio = document.createElement('div');

        vazio.classList.add('dia-vazio');

        calendario.appendChild(vazio);

    }


    // Quantidade de dias do mês
    const quantidadeDias = new Date(
        ano,
        mes,
        0
    ).getDate();


    for (let dia = 1; dia <= quantidadeDias; dia++) {

        const celula = document.createElement('div');

        celula.classList.add('dia-calendario');

        celula.textContent = dia;


        // Procura um registro daquele dia
        const registro = data.registros.find(
            item => item.dia === dia
        );


        if (registro) {

            if (registro[tipo]) {

                celula.classList.add('dia-cumprido');

            } else {

                celula.classList.add('dia-nao-cumprido');

            }

        } else {

            celula.classList.add('dia-sem-registro');

        }


        calendario.appendChild(celula);

    }


    container.appendChild(calendario);
}

function renderiza_grafico_peso(url) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const canvas = document.getElementById('grafico_peso');
            if (!canvas) {
                console.error('Canvas grafico_peso não encontrado.');
                return;
            }

            new Chart(canvas, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Peso (kg)',
                            data: data.dados,
                            borderWidth: 2,
                            tension: 0.3
                        }
                    ]
                },

                options: {

                    responsive: true,

                    scales: {

                        y: {
                            beginAtZero: false
                        }

                    }
                }

            });

        })
        .catch(error => {
            console.error(
                'Erro ao carregar gráfico de peso:',
                error
            );
        });
}