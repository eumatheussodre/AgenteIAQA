import faker from "faker";

export function gerarMassaDados(quantidade, campos) {
    const resultado = [];
    for (let i = 0; i < quantidade; i++) {
        const item = {};
        campos.forEach((campo) => {
            switch (campo) {
                case "nome":
                    item[campo] = faker.name.findName(); break;
                case "email":
                    item[campo] = faker.internet.email(); break;
                case "cpf":
                    item[campo] = faker.random.number({ min: 10000000000, max: 99999999999 }).toString(); break;
                case "cnpj":
                    item[campo] = faker.random.number({ min: 10000000000000, max: 99999999999999 }).toString(); break;
                case "telefone":
                    item[campo] = faker.phone.phoneNumber(); break;
                case "endereco":
                    item[campo] = faker.address.streetAddress(); break;
                case "data_nascimento":
                    item[campo] = faker.date.past(40, new Date(2005, 0, 1)).toISOString().split('T')[0]; break;
                case "empresa":
                    item[campo] = faker.company.companyName(); break;
                default:
                    item[campo] = "-";
            }
        });
        resultado.push(item);
    }
    return resultado;
}

export function gerarMassaBancaria(quantidade, permitirNegativo) {
    const resultado = [];
    for (let i = 0; i < quantidade; i++) {
        resultado.push({
            conta: faker.finance.account(),
            agencia: faker.finance.account(4),
            saldo: permitirNegativo
                ? faker.finance.amount(-1000, 10000, 2)
                : faker.finance.amount(0, 10000, 2),
            titular: faker.name.findName(),
            banco: faker.company.companyName(),
        });
    }
    return resultado;
}
