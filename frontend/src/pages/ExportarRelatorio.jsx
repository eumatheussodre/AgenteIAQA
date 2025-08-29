import React, { useState } from "react";
import axios from "axios";

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
      await axios.post("http://localhost:8000/exportar-relatorio/", form);
      setStatus("Relatório exportado com sucesso!");
    } catch (err) {
      setErro("Erro ao exportar relatório.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Exportar Relatório</h2>
      <form onSubmit={exportar}>
        <label>Casos de Teste (um por linha):
          <textarea value={casos} onChange={e => setCasos(e.target.value)} rows={6} style={{ width: "100%", marginTop: 8 }} required />
        </label>
        <br/>
        <label>Nome base do relatório:
          <input type="text" value={nome} onChange={e => setNome(e.target.value)} style={{ width: "100%", marginTop: 8 }} />
        </label>
        <br/>
        <button type="submit" disabled={loading} style={{ marginTop: 16 }}>
          {loading ? "Exportando..." : "Exportar"}
        </button>
      </form>
      {erro && <div style={{ color: "red", marginTop: 16 }}>{erro}</div>}
      {status && <div style={{ color: "green", marginTop: 16 }}>{status}</div>}
    </div>
  );
}
