import React, { useState } from "react";
import api from "../api";
import { darkTheme } from "../darkTheme";

export default function LlamaIA() {
  const [prompt, setPrompt] = useState("");
  const [resposta, setResposta] = useState("");
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");

  const enviarPrompt = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErro("");
    setResposta("");
    try {
      // endpoint ajustado para backend Express local
      const resp = await api.post("/api/llama", { prompt });
      if (resp.data && resp.data.resposta) {
        setResposta(resp.data.resposta);
      } else {
        setErro("Resposta inválida do Llama.");
      }
    } catch (err) {
      setErro("Erro ao consultar o Llama.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={darkTheme.pageBg}>
      <div style={darkTheme.cardStyle}>
        <h2 style={darkTheme.titleStyle}>🤖 Chat com Llama (local)</h2>
        <form onSubmit={enviarPrompt}>
          <label style={darkTheme.labelStyle}>
            Prompt:
            <textarea
              value={prompt}
              onChange={e => setPrompt(e.target.value)}
              rows={4}
              style={darkTheme.inputStyle}
              required
            />
          </label>
          <button type="submit" disabled={loading} style={darkTheme.buttonStyle}>
            {loading ? "Enviando..." : "Enviar"}
          </button>
        </form>
        {erro && <div style={darkTheme.erroStyle}>{erro}</div>}
        {resposta && (
          <div style={{ marginTop: 24 }}>
            <strong>Resposta do Llama:</strong>
            <pre style={darkTheme.preStyle}>{resposta}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

// ...estilos agora via darkTheme...
