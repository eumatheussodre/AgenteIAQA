import React, { useState } from "react";
import api from "../api";
import { darkTheme } from "../darkTheme";

export default function ExportarRelatorio() {
  const [casos, setCasos] = useState("");
  const [nome, setNome] = useState("relatorio_de_testes");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");

  const exportar = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErro("");
    setStatus("");
    try {
      const form = new FormData();
      casos.split("\n").forEach(c => form.append("casos", c));
      form.append("nome_base", nome);
      await api.post("/api/exportar-relatorio", form);
      setStatus("Relatório exportado com sucesso!");
    } catch (err) {
      setErro("Erro ao exportar relatório.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={darkTheme.pageBg}>
      <div style={darkTheme.cardStyle}>
        <h2 style={darkTheme.titleStyle}>📑 Exportar Relatório</h2>
        <form onSubmit={exportar}>
          <label style={darkTheme.labelStyle}>Casos de Teste (um por linha):
            <textarea value={casos} onChange={e => setCasos(e.target.value)} rows={6} style={darkTheme.inputStyle} required />
          </label>
          <label style={darkTheme.labelStyle}>Nome base do relatório:
            <input type="text" value={nome} onChange={e => setNome(e.target.value)} style={darkTheme.inputStyle} />
          </label>
          <button type="submit" disabled={loading} style={darkTheme.buttonStyle}>
            {loading ? "Exportando..." : "Exportar"}
          </button>
        </form>
        {erro && <div style={darkTheme.erroStyle}>{erro}</div>}
        {status && <div style={darkTheme.statusStyle}>{status}</div>}
      </div>
    </div>
  );
}

// ...estilos agora via darkTheme...
