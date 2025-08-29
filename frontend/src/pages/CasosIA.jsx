import React, { useState } from "react";
import api from "../api";
import { darkTheme } from "../darkTheme";

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
      const resp = await api.post("/api/gerar-caso-ia", { requisito });
      if (resp.data && resp.data.caso) {
        setCaso(resp.data.caso);
      } else {
        setErro("Resposta inválida do backend.");
      }
    } catch (err) {
      setErro("Erro ao gerar caso de teste.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={darkTheme.pageBg}>
      <div style={darkTheme.cardStyle}>
        <h2 style={darkTheme.titleStyle}>🧪 Gerar Caso de Teste (IA)</h2>
        <form onSubmit={gerarCaso}>
          <label style={darkTheme.labelStyle}>
            Requisito:
            <textarea
              value={requisito}
              onChange={e => setRequisito(e.target.value)}
              rows={4}
              style={darkTheme.inputStyle}
              required
            />
          </label>
          <button type="submit" disabled={loading} style={darkTheme.buttonStyle}>
            {loading ? "Gerando..." : "Gerar Caso de Teste"}
          </button>
        </form>
        {erro && <div style={darkTheme.erroStyle}>{erro}</div>}
        {caso && (
          <div style={{ marginTop: 24 }}>
            <strong>Caso de Teste Gerado:</strong>
            <pre style={darkTheme.preStyle}>{caso}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

// ...estilos agora via darkTheme...
