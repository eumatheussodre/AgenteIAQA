import React, { useState } from "react";
import axios from "axios";

export default function CasosIA() {
  const [requisito, setRequisito] = useState("");
  const [caso, setCaso] = useState("");
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");

  const gerarCaso = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErro("");
    setCaso("");
    try {
      const resp = await axios.post("http://localhost:8000/gerar-caso-ia/", { requisito });
      setCaso(resp.data.caso);
    } catch (err) {
      setErro("Erro ao gerar caso de teste.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Gerar Caso de Teste (IA)</h2>
      <form onSubmit={gerarCaso}>
        <label>
          Requisito:
          <textarea
            value={requisito}
            onChange={e => setRequisito(e.target.value)}
            rows={4}
            style={{ width: "100%", marginTop: 8 }}
            required
          />
        </label>
        <button type="submit" disabled={loading} style={{ marginTop: 16 }}>
          {loading ? "Gerando..." : "Gerar Caso de Teste"}
        </button>
      </form>
      {erro && <div style={{ color: "red", marginTop: 16 }}>{erro}</div>}
      {caso && (
        <div style={{ marginTop: 24 }}>
          <strong>Caso de Teste Gerado:</strong>
          <pre style={{ background: "#f4f4f4", padding: 12 }}>{caso}</pre>
        </div>
      )}
    </div>
  );
}
