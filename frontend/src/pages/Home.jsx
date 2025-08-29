import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>AgenteIAQA</h1>
      <p>Escolha uma funcionalidade:</p>
      <ul style={{ fontSize: 18 }}>
        <li><Link to="/casos">Gerar Casos de Teste (IA)</Link></li>
        <li><Link to="/massa">Gerar Massa de Dados</Link></li>
        <li><Link to="/bancaria">Gerar Massa Bancária</Link></li>
        <li><Link to="/exportar">Exportar Relatório</Link></li>
      </ul>
    </div>
  );
}
