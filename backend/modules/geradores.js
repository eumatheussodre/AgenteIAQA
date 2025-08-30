import faker from "faker";

// Configurar o faker para usar locale brasileiro para melhor performance
faker.locale = "pt_BR";

// Cache de dados pré-gerados para melhor performance
const precomputedData = {
    names: [],
    companies: [],
    addresses: []
};

// Função para pré-computar dados se não existirem
function ensurePrecomputedData() {
    if (precomputedData.names.length === 0) {
        for (let i = 0; i < 100; i++) {
            precomputedData.names.push(faker.name.findName());
            precomputedData.companies.push(faker.company.companyName());
            precomputedData.addresses.push(faker.address.streetAddress());
        }
    }
}

export function gerarMassaDados(quantidade, campos) {
    ensurePrecomputedData();

    // Pré-aloca o array com o tamanho necessário
    const resultado = new Array(quantidade);

    // Otimiza a geração usando operações mais rápidas
    for (let i = 0; i < quantidade; i++) {
        const item = {};

        // Usa um loop mais eficiente
        for (const campo of campos) {
            switch (campo) {
                case "nome":
                    item[campo] = precomputedData.names[i % 100]; break;
                case "email":
                    item[campo] = `user${i}@exemplo.com`; break;
                case "cpf":
                    item[campo] = String(Math.floor(Math.random() * 90000000000) + 10000000000); break;
                case "cnpj":
                    item[campo] = String(Math.floor(Math.random() * 90000000000000) + 10000000000000); break;
                case "telefone":
                    item[campo] = `(11) 9${String(Math.floor(Math.random() * 100000000)).padStart(8, '0')}`; break;
                case "endereco":
                    item[campo] = precomputedData.addresses[i % 100]; break;
                case "data_nascimento":
                    const year = 1970 + (i % 50);
                    const month = String(Math.floor(Math.random() * 12) + 1).padStart(2, '0');
                    const day = String(Math.floor(Math.random() * 28) + 1).padStart(2, '0');
                    item[campo] = `${year}-${month}-${day}`; break;
                case "empresa":
                    item[campo] = precomputedData.companies[i % 100]; break;
                default:
                    item[campo] = "-";
            }
        }
        resultado[i] = item;
    }
    return resultado;
}

export function gerarMassaBancaria(quantidade, permitirNegativo) {
    ensurePrecomputedData();

    // Pré-aloca o array com o tamanho necessário
    const resultado = new Array(quantidade);

    for (let i = 0; i < quantidade; i++) {
        const saldo = permitirNegativo
            ? (Math.random() * 11000) - 1000  // -1000 a 10000
            : Math.random() * 10000;          // 0 a 10000

        resultado[i] = {
            conta: String(Math.floor(Math.random() * 900000) + 100000),
            agencia: String(Math.floor(Math.random() * 9000) + 1000),
            saldo: saldo.toFixed(2),
            titular: precomputedData.names[i % 100],
            banco: precomputedData.companies[i % 100],
        };
    }
    return resultado;
}
